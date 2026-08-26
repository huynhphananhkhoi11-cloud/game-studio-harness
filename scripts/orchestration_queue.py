"""Zero-cost STUDIO-007A work-order and Producer Queue implementation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from datetime import datetime
from typing import Any, Iterable


SCHEMA_VERSION = 1
STATES = {
    "DRAFT", "READY", "CLAIMABLE", "CLAIMED", "BLOCKED",
    "QA_PENDING", "OWNER_PENDING", "DONE", "CANCELLED",
}
RESERVED_STATES = {"CLAIMED", "QA_PENDING", "OWNER_PENDING", "DONE"}
ACTIVE_TRANSITIONS = {
    ("DRAFT", "READY"): {"STUDIO_OWNER"},
    ("READY", "CLAIMABLE"): {"PRODUCER-01"},
    ("DRAFT", "BLOCKED"): {"PRODUCER-01"},
    ("READY", "BLOCKED"): {"PRODUCER-01"},
    ("CLAIMABLE", "BLOCKED"): {"PRODUCER-01"},
    ("BLOCKED", "DRAFT"): {"PRODUCER-01"},
    ("DRAFT", "CANCELLED"): {"STUDIO_OWNER"},
    ("READY", "CANCELLED"): {"STUDIO_OWNER"},
    ("CLAIMABLE", "CANCELLED"): {"STUDIO_OWNER"},
    ("BLOCKED", "CANCELLED"): {"STUDIO_OWNER"},
}
WORK_ORDER_KEYS = {
    "schema_version", "work_order_id", "producer_id", "requesting_unit",
    "project_id", "objective", "permitted_paths", "prohibited_actions",
    "capability_tags", "input_references", "expected_output_references",
    "acceptance_gates", "priority", "budget_ceiling", "dependency_ids",
    "attempt", "state", "owner_gate_required", "created_at", "updated_at",
    "last_event_id",
}
EVENT_KEYS = {
    "schema_version", "event_id", "work_order_id", "prior_state",
    "next_state", "actor_id", "actor_role", "timestamp", "reason",
    "attempt", "resulting_snapshot_digest",
}
LIST_FIELDS = {
    "permitted_paths", "prohibited_actions", "capability_tags",
    "input_references", "expected_output_references", "acceptance_gates",
    "dependency_ids",
}
NONEMPTY_LIST_FIELDS = {
    "permitted_paths", "prohibited_actions", "capability_tags",
    "expected_output_references", "acceptance_gates",
}
IMMUTABLE_TRANSITION_FIELDS = WORK_ORDER_KEYS - {
    "state", "updated_at", "last_event_id",
}
WORK_ORDER_ID_RE = re.compile(r"^WO-[A-Z0-9][A-Z0-9._-]{2,63}$")
EVENT_ID_RE = re.compile(r"^EV-[A-Z0-9][A-Z0-9._-]{2,63}$")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
SECRET_VALUE_RES = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/:]+:[^\s/@]+@"),
]


class QueueError(ValueError):
    """A fail-closed validation or queue-operation error."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise QueueError(message)


def parse_utc(timestamp: Any, field: str = "timestamp") -> datetime:
    _require(isinstance(timestamp, str) and timestamp.endswith("Z"),
             f"{field} must use ISO 8601 UTC with Z suffix")
    try:
        value = datetime.fromisoformat(timestamp[:-1] + "+00:00")
    except ValueError as exc:
        raise QueueError(f"{field} is not a valid ISO 8601 timestamp") from exc
    _require(value.utcoffset() is not None and value.utcoffset().total_seconds() == 0,
             f"{field} must be UTC")
    return value


def _validate_strings(values: Any, field: str, nonempty: bool) -> None:
    _require(isinstance(values, list), f"{field} must be an array")
    if nonempty:
        _require(bool(values), f"{field} must not be empty")
    _require(all(isinstance(item, str) and item.strip() for item in values),
             f"{field} entries must be non-empty strings")
    _require(len(values) == len(set(values)), f"{field} contains duplicates")


def _validate_repo_path(value: str, field: str) -> None:
    _require(not value.startswith(("/", "\\")) and not WINDOWS_ABSOLUTE_RE.match(value),
             f"{field} must be repository-relative")
    _require("\\" not in value, f"{field} must use forward slashes")
    parts = PurePosixPath(value).parts
    _require(bool(parts) and all(part not in ("", ".", "..") for part in parts),
             f"{field} contains an unsafe path segment")
    _require(":" not in parts[0], f"{field} must not contain a URI or drive prefix")


def _contains_secret(value: Any) -> bool:
    if isinstance(value, str):
        return any(pattern.search(value) for pattern in SECRET_VALUE_RES)
    if isinstance(value, list):
        return any(_contains_secret(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_secret(item) for item in value.values())
    return False


def validate_work_order(snapshot: Any) -> None:
    _require(isinstance(snapshot, dict), "work order must be a JSON object")
    missing = WORK_ORDER_KEYS - set(snapshot)
    extra = set(snapshot) - WORK_ORDER_KEYS
    _require(not missing, "work order missing fields: " + ", ".join(sorted(missing)))
    _require(not extra, "work order has unsupported fields: " + ", ".join(sorted(extra)))
    _require(snapshot["schema_version"] == SCHEMA_VERSION, "unsupported work-order schema version")
    _require(isinstance(snapshot["work_order_id"], str) and WORK_ORDER_ID_RE.fullmatch(snapshot["work_order_id"]),
             "invalid work_order_id")
    for field in ("producer_id", "requesting_unit", "objective", "last_event_id"):
        _require(isinstance(snapshot[field], str) and snapshot[field].strip(), f"{field} must not be empty")
    _require(snapshot["project_id"] is None or
             (isinstance(snapshot["project_id"], str) and snapshot["project_id"].strip()),
             "project_id must be an explicit string or null")
    for field in LIST_FIELDS:
        _validate_strings(snapshot[field], field, field in NONEMPTY_LIST_FIELDS)
    for index, value in enumerate(snapshot["permitted_paths"]):
        _validate_repo_path(value, f"permitted_paths[{index}]")
    for field in ("input_references", "expected_output_references"):
        for index, value in enumerate(snapshot[field]):
            _validate_repo_path(value, f"{field}[{index}]")
    _require(type(snapshot["priority"]) is int and 0 <= snapshot["priority"] <= 100,
             "priority must be an integer from 0 through 100")
    _require(type(snapshot["budget_ceiling"]) is int and snapshot["budget_ceiling"] == 0,
             "budget_ceiling must be integer 0")
    _require(type(snapshot["attempt"]) is int and snapshot["attempt"] >= 1,
             "attempt must be a positive integer")
    _require(snapshot["state"] in STATES, "unsupported work-order state")
    _require(type(snapshot["owner_gate_required"]) is bool,
             "owner_gate_required must be boolean")
    created = parse_utc(snapshot["created_at"], "created_at")
    updated = parse_utc(snapshot["updated_at"], "updated_at")
    _require(updated >= created, "updated_at must not precede created_at")
    _require(not _contains_secret(snapshot), "work order contains a credential-bearing value")


def validate_event(event: Any) -> None:
    _require(isinstance(event, dict), "queue event must be a JSON object")
    missing = EVENT_KEYS - set(event)
    extra = set(event) - EVENT_KEYS
    _require(not missing, "event missing fields: " + ", ".join(sorted(missing)))
    _require(not extra, "event has unsupported fields: " + ", ".join(sorted(extra)))
    _require(event["schema_version"] == SCHEMA_VERSION, "unsupported event schema version")
    _require(isinstance(event["event_id"], str) and EVENT_ID_RE.fullmatch(event["event_id"]),
             "invalid event_id")
    _require(isinstance(event["work_order_id"], str) and WORK_ORDER_ID_RE.fullmatch(event["work_order_id"]),
             "invalid event work_order_id")
    _require(event["prior_state"] is None or event["prior_state"] in STATES,
             "unsupported prior_state")
    _require(event["next_state"] in STATES, "unsupported next_state")
    for field in ("actor_id", "actor_role", "reason"):
        _require(isinstance(event[field], str) and event[field].strip(), f"{field} must not be empty")
    _require(event["actor_role"] in {"PRODUCER-01", "STUDIO_OWNER"}, "unsupported actor_role")
    parse_utc(event["timestamp"])
    _require(type(event["attempt"]) is int and event["attempt"] >= 1,
             "event attempt must be a positive integer")
    digest = event["resulting_snapshot_digest"]
    _require(isinstance(digest, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", digest),
             "invalid resulting_snapshot_digest")
    _require(not _contains_secret(event), "event contains a credential-bearing value")


def snapshot_digest(snapshot: dict[str, Any]) -> str:
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _validate_role_transition(prior: str, next_state: str, role: str, reason: str) -> None:
    _require(prior not in RESERVED_STATES and next_state not in RESERVED_STATES,
             "transitions into or out of reserved states are rejected")
    roles = ACTIVE_TRANSITIONS.get((prior, next_state))
    _require(roles is not None, f"illegal transition {prior} -> {next_state}")
    _require(role in roles, f"{role} is not authorized for {prior} -> {next_state}")
    _require(bool(reason.strip()), "transition reason must not be empty")


def validate_transition_change(before: dict[str, Any], after: dict[str, Any]) -> None:
    """Reject objective, scope, prohibition, budget, or other immutable changes."""
    for field in IMMUTABLE_TRANSITION_FIELDS:
        _require(before.get(field) == after.get(field),
                 f"transition may not change {field}")


def build_transition(snapshot: dict[str, Any], *, event_id: str, next_state: str,
                     actor_id: str, actor_role: str, timestamp: str,
                     reason: str) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_work_order(snapshot)
    _require(EVENT_ID_RE.fullmatch(event_id) is not None, "invalid event_id")
    parse_utc(timestamp)
    _validate_role_transition(snapshot["state"], next_state, actor_role, reason)
    _require(parse_utc(timestamp) >= parse_utc(snapshot["updated_at"]),
             "transition timestamp must not decrease")
    updated = copy.deepcopy(snapshot)
    updated["state"] = next_state
    updated["updated_at"] = timestamp
    updated["last_event_id"] = event_id
    validate_transition_change(snapshot, updated)
    validate_work_order(updated)
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "work_order_id": snapshot["work_order_id"],
        "prior_state": snapshot["state"],
        "next_state": next_state,
        "actor_id": actor_id,
        "actor_role": actor_role,
        "timestamp": timestamp,
        "reason": reason,
        "attempt": snapshot["attempt"],
        "resulting_snapshot_digest": snapshot_digest(updated),
    }
    validate_event(event)
    return updated, event


def _reconstructed_snapshot(final_snapshot: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    reconstructed = copy.deepcopy(final_snapshot)
    reconstructed["state"] = event["next_state"]
    reconstructed["updated_at"] = event["timestamp"]
    reconstructed["last_event_id"] = event["event_id"]
    reconstructed["attempt"] = event["attempt"]
    return reconstructed


def validate_history(snapshot: dict[str, Any], events: list[dict[str, Any]]) -> None:
    validate_work_order(snapshot)
    _require(bool(events), "event history must not be empty")
    seen: dict[str, dict[str, Any]] = {}
    prior_timestamp: datetime | None = None
    expected_prior: str | None = None
    for index, event in enumerate(events):
        validate_event(event)
        _require(event["work_order_id"] == snapshot["work_order_id"],
                 "event work_order_id does not match snapshot")
        if event["event_id"] in seen:
            _require(seen[event["event_id"]] == event,
                     "duplicate event replay differs from original")
            raise QueueError("duplicate event_id in history")
        seen[event["event_id"]] = event
        current_time = parse_utc(event["timestamp"])
        if prior_timestamp is not None:
            _require(current_time >= prior_timestamp, "event timestamps decrease")
        prior_timestamp = current_time
        if index == 0:
            _require(event["prior_state"] is None and event["next_state"] == "DRAFT",
                     "initial event must be null -> DRAFT")
            _require(event["actor_role"] == "PRODUCER-01",
                     "initial DRAFT must be created by PRODUCER-01")
            _require(event["timestamp"] == snapshot["created_at"],
                     "initial event timestamp must match created_at")
        else:
            _require(event["prior_state"] == expected_prior,
                     "event prior_state does not continue history")
            _validate_role_transition(event["prior_state"], event["next_state"],
                                      event["actor_role"], event["reason"])
        expected_prior = event["next_state"]
        _require(event["attempt"] == snapshot["attempt"],
                 "event attempt does not match snapshot")
        reconstructed = _reconstructed_snapshot(snapshot, event)
        _require(snapshot_digest(reconstructed) == event["resulting_snapshot_digest"],
                 "event digest cannot be reconciled with immutable snapshot fields")
    last = events[-1]
    _require(snapshot["state"] == last["next_state"], "snapshot state does not match history")
    _require(snapshot["updated_at"] == last["timestamp"], "snapshot updated_at does not match history")
    _require(snapshot["last_event_id"] == last["event_id"], "snapshot last_event_id does not match history")
    _require(snapshot_digest(snapshot) == last["resulting_snapshot_digest"],
             "snapshot digest does not match final event")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QueueError(f"cannot read valid JSON from {path}") from exc


def read_events(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise QueueError(f"cannot read event history {path}") from exc
    _require(bool(lines) and all(line.strip() for line in lines),
             f"event history {path} contains no events or blank records")
    events = []
    for number, line in enumerate(lines, 1):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise QueueError(f"invalid JSONL at {path}:{number}") from exc
    return events


def load_queue(queue_root: Path) -> list[tuple[dict[str, Any], list[dict[str, Any]]]]:
    orders_dir = queue_root / "work-orders"
    events_dir = queue_root / "events"
    _require(orders_dir.is_dir(), "queue root is missing work-orders directory")
    _require(events_dir.is_dir(), "queue root is missing events directory")
    pairs = []
    seen_orders: set[str] = set()
    seen_events: set[str] = set()
    snapshots = sorted(orders_dir.glob("*.json"))
    for path in snapshots:
        snapshot = read_json(path)
        validate_work_order(snapshot)
        work_order_id = snapshot["work_order_id"]
        _require(path.stem == work_order_id, f"snapshot filename does not match {work_order_id}")
        _require(work_order_id not in seen_orders, f"duplicate work_order_id {work_order_id}")
        seen_orders.add(work_order_id)
        event_path = events_dir / f"{work_order_id}.jsonl"
        _require(event_path.is_file(), f"missing event history for {work_order_id}")
        events = read_events(event_path)
        validate_history(snapshot, events)
        for event in events:
            _require(event["event_id"] not in seen_events,
                     f"duplicate event_id across queue: {event['event_id']}")
            seen_events.add(event["event_id"])
        pairs.append((snapshot, events))
    orphan_histories = {path.stem for path in events_dir.glob("*.jsonl")} - seen_orders
    _require(not orphan_histories,
             "orphan event histories: " + ", ".join(sorted(orphan_histories)))
    return pairs


def validate_queue(queue_root: Path) -> list[str]:
    try:
        load_queue(queue_root)
        return []
    except QueueError as exc:
        return [str(exc)]


def ordered_snapshots(queue_root: Path) -> list[dict[str, Any]]:
    snapshots = [snapshot for snapshot, _ in load_queue(queue_root)]
    return sorted(snapshots, key=lambda item: (
        -item["priority"], parse_utc(item["created_at"]), item["work_order_id"]
    ))


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except Exception:
        try:
            temporary_path.unlink(missing_ok=True)
        finally:
            raise


def _json_text(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _events_text(events: Iterable[dict[str, Any]]) -> str:
    return "".join(json.dumps(event, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")) + "\n" for event in events)


def create_draft(queue_root: Path, snapshot: dict[str, Any], event: dict[str, Any]) -> str:
    validate_work_order(snapshot)
    validate_event(event)
    validate_history(snapshot, [event])
    _require(snapshot["state"] == "DRAFT", "create-draft accepts only DRAFT snapshots")
    _require(event["actor_role"] == "PRODUCER-01", "create-draft requires PRODUCER-01")
    snapshot_path = queue_root / "work-orders" / f"{snapshot['work_order_id']}.json"
    event_path = queue_root / "events" / f"{snapshot['work_order_id']}.jsonl"
    if snapshot_path.exists() or event_path.exists():
        if snapshot_path.is_file() and event_path.is_file():
            existing_snapshot = read_json(snapshot_path)
            existing_events = read_events(event_path)
            if existing_snapshot == snapshot and existing_events == [event]:
                return "replayed"
        raise QueueError(f"work order {snapshot['work_order_id']} already exists with different content")
    if queue_root.exists() and any(queue_root.iterdir()):
        pairs = load_queue(queue_root)
        _require(all(item[0]["work_order_id"] != snapshot["work_order_id"] for item in pairs),
                 f"duplicate work_order_id {snapshot['work_order_id']}")
        _require(all(existing["event_id"] != event["event_id"]
                     for _, history in pairs for existing in history),
                 f"duplicate event_id across queue: {event['event_id']}")
    _atomic_write(event_path, _events_text([event]))
    _atomic_write(snapshot_path, _json_text(snapshot))
    return "created"


def transition(queue_root: Path, work_order_id: str, *, event_id: str,
               next_state: str, actor_id: str, actor_role: str,
               timestamp: str, reason: str) -> str:
    pairs = load_queue(queue_root)
    pair = next((item for item in pairs if item[0]["work_order_id"] == work_order_id), None)
    _require(pair is not None, f"unknown work_order_id {work_order_id}")
    snapshot, events = pair
    matches = [event for _, history in pairs for event in history if event["event_id"] == event_id]
    if matches:
        _require(len(matches) == 1, f"duplicate event_id {event_id}")
        existing = matches[0]
        same_request = (
            existing["work_order_id"] == work_order_id and
            existing["next_state"] == next_state and
            existing["actor_id"] == actor_id and
            existing["actor_role"] == actor_role and
            existing["timestamp"] == timestamp and
            existing["reason"] == reason and
            existing["attempt"] == snapshot["attempt"] and
            snapshot_digest(snapshot) == existing["resulting_snapshot_digest"] and
            snapshot["last_event_id"] == event_id
        )
        _require(same_request, "event replay differs from existing result")
        return "replayed"
    updated, event = build_transition(
        snapshot, event_id=event_id, next_state=next_state,
        actor_id=actor_id, actor_role=actor_role, timestamp=timestamp,
        reason=reason,
    )
    event_path = queue_root / "events" / f"{work_order_id}.jsonl"
    snapshot_path = queue_root / "work-orders" / f"{work_order_id}.json"
    _atomic_write(event_path, _events_text(events + [event]))
    _atomic_write(snapshot_path, _json_text(updated))
    return "transitioned"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create-draft")
    create.add_argument("--queue-root", type=Path, required=True)
    create.add_argument("--snapshot", type=Path, required=True)
    create.add_argument("--event", type=Path, required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--queue-root", type=Path, required=True)
    listing = subparsers.add_parser("list")
    listing.add_argument("--queue-root", type=Path, required=True)
    move = subparsers.add_parser("transition")
    move.add_argument("--queue-root", type=Path, required=True)
    move.add_argument("--work-order-id", required=True)
    move.add_argument("--event-id", required=True)
    move.add_argument("--next-state", required=True)
    move.add_argument("--actor-id", required=True)
    move.add_argument("--actor-role", required=True)
    move.add_argument("--timestamp", required=True)
    move.add_argument("--reason", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "create-draft":
            result = create_draft(args.queue_root, read_json(args.snapshot), read_json(args.event))
            print(result.upper())
        elif args.command == "validate":
            errors = validate_queue(args.queue_root)
            if errors:
                raise QueueError(errors[0])
            print("OK")
        elif args.command == "list":
            print(json.dumps(ordered_snapshots(args.queue_root), ensure_ascii=False, indent=2))
        elif args.command == "transition":
            result = transition(
                args.queue_root, args.work_order_id, event_id=args.event_id,
                next_state=args.next_state, actor_id=args.actor_id,
                actor_role=args.actor_role, timestamp=args.timestamp,
                reason=args.reason,
            )
            print(result.upper())
        return 0
    except QueueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
