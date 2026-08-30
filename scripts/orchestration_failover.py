"""Deterministic, read-only STUDIO-007D failover evidence validator."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
MAX_ATTEMPTS = 3
ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9._-]{2,63}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
STATES = {
    "HEALTHY", "SUSPECTED", "PAUSED", "HANDOFF_REQUIRED",
    "READY_FOR_REASSIGNMENT", "REASSIGNED", "RESUMED",
    "RECOVERED", "ABORTED",
}
FAILURE_CLASSES = {
    "NONE", "TIMEOUT", "EXECUTOR_FAILURE", "MALFORMED_OUTPUT",
    "VALIDATION_FAILURE", "MANUAL_STOP", "CHECKPOINT_MISSING",
}
LEGAL_TRANSITIONS = {
    "HEALTHY": {"SUSPECTED"},
    "SUSPECTED": {"HEALTHY", "PAUSED"},
    "PAUSED": {"RESUMED", "HANDOFF_REQUIRED", "ABORTED"},
    "HANDOFF_REQUIRED": {"READY_FOR_REASSIGNMENT", "ABORTED"},
    "READY_FOR_REASSIGNMENT": {"REASSIGNED", "ABORTED"},
    "REASSIGNED": {"RESUMED", "ABORTED"},
    "RESUMED": {"SUSPECTED", "RECOVERED", "ABORTED"},
    "RECOVERED": {"HEALTHY"},
    "ABORTED": set(),
}
EVENT_KEYS = {
    "schema_version", "event_id", "work_order_id", "work_order_digest",
    "attempt_id", "attempt_number", "prior_state", "next_state",
    "failure_class", "detector_id", "evidence_references",
    "checkpoint_id", "handoff_id", "claim_disposition",
    "recovery_action", "owner_gate_id", "prior_event_id",
    "prior_event_digest", "observed_at",
}
ATTEMPT_KEYS = {
    "schema_version", "attempt_id", "work_order_id", "work_order_digest",
    "attempt_number", "executor_id", "state", "claim_id",
    "prior_attempt_id", "prior_attempt_digest", "failed_event_id",
    "handoff_id", "checkpoint_id", "selected_executor_evidence",
    "validation_evidence", "created_at",
}
CHAIN_KEYS = {
    "schema_version", "work_order_id", "work_order_digest", "events",
    "attempts", "claims", "handoffs", "checkpoints", "executors",
    "owner_gates",
}
CLAIM_KEYS = {
    "claim_id", "work_order_id", "writer_id", "branch", "path_scope",
    "status", "claimed_at", "expires_at", "released_at",
}
HANDOFF_KEYS = {
    "handoff_id", "work_order_id", "claim_id", "base_commit",
    "current_commit", "changed_paths", "checks", "blockers",
    "exact_resume_action", "created_at",
}
CHECKPOINT_KEYS = {
    "checkpoint_id", "work_order_id", "content_digest", "status",
    "evidence_references", "created_at",
}
EXECUTOR_KEYS = {
    "executor_id", "eligible", "capabilities", "evidence_references",
    "observed_at",
}
GATE_KEYS = {
    "gate_id", "work_order_id", "attempt_number", "prior_state",
    "next_state", "action", "approver_role", "approval_reference",
    "reason", "decided_at", "expires_at", "evidence_digest",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(token|password|secret|api[_-]?key)\s*[:=]\s*\S+"),
    re.compile(r"https?://[^\s/@:]+:[^\s/@]+@"),
)


class FailoverError(ValueError):
    """Raised when supplied evidence fails closed."""


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise FailoverError(message)


def _exact_keys(record: dict[str, Any], keys: set[str], label: str) -> None:
    _require(isinstance(record, dict), f"{label} must be an object")
    missing = sorted(keys - set(record))
    extra = sorted(set(record) - keys)
    _require(not missing and not extra, f"{label} keys mismatch; missing={missing}, extra={extra}")


def _identifier(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(ID_RE.fullmatch(value)), f"invalid {label}")
    return value


def _digest(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(DIGEST_RE.fullmatch(value)), f"invalid {label}")
    return value


def _timestamp(value: Any, label: str) -> datetime:
    _require(isinstance(value, str) and value.endswith("Z"), f"{label} must be explicit UTC")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise FailoverError(f"invalid {label}") from exc
    _require(parsed.tzinfo == timezone.utc, f"{label} must be UTC")
    return parsed


def _safe_text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    _require(isinstance(value, str), f"{label} must be text")
    _require(allow_empty or bool(value.strip()), f"{label} must not be empty")
    _require(not any(pattern.search(value) for pattern in SECRET_PATTERNS), f"{label} contains unsafe secret-like text")
    return value


def _strings(value: Any, label: str, *, nonempty: bool = True) -> list[str]:
    _require(isinstance(value, list), f"{label} must be a list")
    _require(not nonempty or bool(value), f"{label} must not be empty")
    for index, item in enumerate(value):
        _safe_text(item, f"{label}[{index}]")
    return value


def _repo_path(value: Any, label: str) -> str:
    value = _safe_text(value, label)
    path = Path(value)
    _require(not path.is_absolute() and ".." not in path.parts and "\\" not in value, f"invalid {label}")
    return value


def validate_event(event: dict[str, Any], as_of: str) -> dict[str, Any]:
    _exact_keys(event, EVENT_KEYS, "event")
    now = _timestamp(as_of, "as_of")
    _require(event["schema_version"] == SCHEMA_VERSION, "unsupported event schema_version")
    _identifier(event["event_id"], "event_id")
    _identifier(event["work_order_id"], "work_order_id")
    _digest(event["work_order_digest"], "work_order_digest")
    _identifier(event["attempt_id"], "attempt_id")
    _require(type(event["attempt_number"]) is int and 1 <= event["attempt_number"] <= MAX_ATTEMPTS, "invalid attempt_number")
    _require(event["prior_state"] in STATES and event["next_state"] in STATES, "unsupported state")
    _require(event["next_state"] in LEGAL_TRANSITIONS[event["prior_state"]], "illegal transition")
    _require(event["failure_class"] in FAILURE_CLASSES, "unsupported failure_class")
    if event["next_state"] in {"HEALTHY", "RECOVERED"}:
        _require(event["failure_class"] == "NONE", "restoration requires NONE failure_class")
    else:
        _require(event["failure_class"] != "NONE", "non-restoration transition requires failure evidence")
    _identifier(event["detector_id"], "detector_id")
    for index, ref in enumerate(_strings(event["evidence_references"], "evidence_references")):
        _repo_path(ref, f"evidence_references[{index}]")
    for field in ("checkpoint_id", "handoff_id", "owner_gate_id", "prior_event_id"):
        if event[field] is not None:
            _identifier(event[field], field)
    if event["prior_event_id"] is None:
        _require(event["prior_event_digest"] is None, "prior_event_digest requires prior_event_id")
    else:
        _digest(event["prior_event_digest"], "prior_event_digest")
    _require(event["claim_disposition"] in {"ACTIVE", "RELEASED", "EXPIRED"}, "invalid claim_disposition")
    _safe_text(event["recovery_action"], "recovery_action")
    _require(_timestamp(event["observed_at"], "observed_at") <= now, "event is in the future")
    return event


def validate_attempt(attempt: dict[str, Any], as_of: str) -> dict[str, Any]:
    _exact_keys(attempt, ATTEMPT_KEYS, "attempt")
    now = _timestamp(as_of, "as_of")
    _require(attempt["schema_version"] == SCHEMA_VERSION, "unsupported attempt schema_version")
    for field in ("attempt_id", "work_order_id", "executor_id", "claim_id", "checkpoint_id"):
        _identifier(attempt[field], field)
    _digest(attempt["work_order_digest"], "work_order_digest")
    number = attempt["attempt_number"]
    _require(type(number) is int and 1 <= number <= MAX_ATTEMPTS, "invalid attempt_number")
    _require(attempt["state"] in STATES, "unsupported attempt state")
    if number == 1:
        for field in ("prior_attempt_id", "prior_attempt_digest", "failed_event_id", "handoff_id"):
            _require(attempt[field] is None, f"initial attempt must not set {field}")
    else:
        for field in ("prior_attempt_id", "failed_event_id", "handoff_id"):
            _identifier(attempt[field], field)
        _digest(attempt["prior_attempt_digest"], "prior_attempt_digest")
    for field in ("selected_executor_evidence", "validation_evidence"):
        for index, ref in enumerate(_strings(attempt[field], field)):
            _repo_path(ref, f"{field}[{index}]")
    _require(_timestamp(attempt["created_at"], "created_at") <= now, "attempt is in the future")
    return attempt


def _index(records: Any, key: str, label: str) -> dict[str, dict[str, Any]]:
    _require(isinstance(records, list), f"{label} must be a list")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        _require(isinstance(record, dict) and isinstance(record.get(key), str), f"invalid {label} record")
        _require(record[key] not in result, f"duplicate {key}")
        result[record[key]] = record
    return result


def _validate_claim(claim: dict[str, Any], work_order_id: str, as_of: datetime) -> None:
    _exact_keys(claim, CLAIM_KEYS, "claim")
    for field in ("claim_id", "work_order_id", "writer_id"):
        _identifier(claim[field], field)
    _require(claim["work_order_id"] == work_order_id, "claim work order mismatch")
    _safe_text(claim["branch"], "branch")
    for index, path in enumerate(_strings(claim["path_scope"], "path_scope")):
        _repo_path(path, f"path_scope[{index}]")
    _require(claim["status"] in {"CLAIMED", "RELEASED"}, "unsupported claim status")
    claimed = _timestamp(claim["claimed_at"], "claimed_at")
    expires = _timestamp(claim["expires_at"], "expires_at")
    _require(claimed < expires, "claim chronology invalid")
    if claim["status"] == "RELEASED":
        _require(claim["released_at"] is not None, "released claim lacks released_at")
        released = _timestamp(claim["released_at"], "released_at")
        _require(claimed <= released <= as_of, "released_at chronology invalid")
    else:
        _require(claim["released_at"] is None, "live claim cannot set released_at")


def _claim_safe(claim: dict[str, Any], as_of: datetime) -> bool:
    return claim["status"] == "RELEASED" or _timestamp(claim["expires_at"], "expires_at") <= as_of


def _validate_handoff(handoff: dict[str, Any], work_order_id: str, as_of: datetime) -> None:
    _exact_keys(handoff, HANDOFF_KEYS, "handoff")
    for field in ("handoff_id", "work_order_id", "claim_id"):
        _identifier(handoff[field], field)
    _require(handoff["work_order_id"] == work_order_id, "handoff work order mismatch")
    _require(bool(COMMIT_RE.fullmatch(handoff["base_commit"])), "invalid base_commit")
    _require(bool(COMMIT_RE.fullmatch(handoff["current_commit"])), "invalid current_commit")
    for field in ("changed_paths", "checks", "blockers"):
        for index, value in enumerate(_strings(handoff[field], field)):
            if field == "changed_paths":
                _repo_path(value, f"{field}[{index}]")
    _safe_text(handoff["exact_resume_action"], "exact_resume_action")
    _require(_timestamp(handoff["created_at"], "handoff created_at") <= as_of, "handoff is in the future")


def _validate_checkpoint(checkpoint: dict[str, Any], work_order_id: str, as_of: datetime) -> None:
    _exact_keys(checkpoint, CHECKPOINT_KEYS, "checkpoint")
    _identifier(checkpoint["checkpoint_id"], "checkpoint_id")
    _require(checkpoint["work_order_id"] == work_order_id, "checkpoint work order mismatch")
    _digest(checkpoint["content_digest"], "checkpoint content_digest")
    _require(checkpoint["status"] in {"SAFE", "MISSING", "INVALID"}, "invalid checkpoint status")
    _strings(checkpoint["evidence_references"], "checkpoint evidence_references")
    _require(_timestamp(checkpoint["created_at"], "checkpoint created_at") <= as_of, "checkpoint is in the future")


def _validate_executor(executor: dict[str, Any], as_of: datetime) -> None:
    _exact_keys(executor, EXECUTOR_KEYS, "executor")
    _identifier(executor["executor_id"], "executor_id")
    _require(type(executor["eligible"]) is bool, "executor eligible must be boolean")
    _strings(executor["capabilities"], "capabilities")
    _strings(executor["evidence_references"], "executor evidence_references")
    _require(_timestamp(executor["observed_at"], "executor observed_at") <= as_of, "executor evidence is in the future")


def _validate_gate(gate: dict[str, Any], work_order_id: str, as_of: datetime) -> None:
    _exact_keys(gate, GATE_KEYS, "owner gate")
    _identifier(gate["gate_id"], "gate_id")
    _require(gate["work_order_id"] == work_order_id, "gate work order mismatch")
    _require(type(gate["attempt_number"]) is int and 1 <= gate["attempt_number"] <= MAX_ATTEMPTS, "gate attempt mismatch")
    _require(gate["prior_state"] in STATES and gate["next_state"] in STATES, "gate state invalid")
    _require(gate["approver_role"] == "STUDIO_OWNER", "gate approver is unauthorized")
    _require(gate["action"] in {"REASSIGN", "EVIDENCE_RESUME", "ABORT"}, "gate action invalid")
    _safe_text(gate["approval_reference"], "approval_reference")
    _safe_text(gate["reason"], "gate reason")
    decided = _timestamp(gate["decided_at"], "gate decided_at")
    expires = _timestamp(gate["expires_at"], "gate expires_at")
    _require(decided <= as_of < expires, "gate is expired or not yet effective")
    _digest(gate["evidence_digest"], "gate evidence_digest")


def validate_chain(chain: dict[str, Any], as_of: str) -> dict[str, Any]:
    original = copy.deepcopy(chain)
    _exact_keys(chain, CHAIN_KEYS, "chain")
    now = _timestamp(as_of, "as_of")
    _require(chain["schema_version"] == SCHEMA_VERSION, "unsupported chain schema_version")
    work_order_id = _identifier(chain["work_order_id"], "work_order_id")
    work_digest = _digest(chain["work_order_digest"], "work_order_digest")
    events = _index(chain["events"], "event_id", "events")
    attempts = _index(chain["attempts"], "attempt_id", "attempts")
    claims = _index(chain["claims"], "claim_id", "claims")
    handoffs = _index(chain["handoffs"], "handoff_id", "handoffs")
    checkpoints = _index(chain["checkpoints"], "checkpoint_id", "checkpoints")
    executors = _index(chain["executors"], "executor_id", "executors")
    gates = _index(chain["owner_gates"], "gate_id", "owner_gates")
    for event in events.values():
        validate_event(event, as_of)
        _require(event["work_order_id"] == work_order_id and event["work_order_digest"] == work_digest, "event identity mismatch")
    for attempt in attempts.values():
        validate_attempt(attempt, as_of)
        _require(attempt["work_order_id"] == work_order_id and attempt["work_order_digest"] == work_digest, "attempt identity mismatch")
    for claim in claims.values():
        _validate_claim(claim, work_order_id, now)
    for handoff in handoffs.values():
        _validate_handoff(handoff, work_order_id, now)
        _require(handoff["claim_id"] in claims, "handoff cites missing claim")
    for checkpoint in checkpoints.values():
        _validate_checkpoint(checkpoint, work_order_id, now)
    for executor in executors.values():
        _validate_executor(executor, now)
    for gate in gates.values():
        _validate_gate(gate, work_order_id, now)
    ordered_attempts = sorted(attempts.values(), key=lambda item: item["attempt_number"])
    _require(ordered_attempts and [a["attempt_number"] for a in ordered_attempts] == list(range(1, len(ordered_attempts) + 1)), "attempt numbers must be consecutive")
    _require(len(ordered_attempts) <= MAX_ATTEMPTS, "attempt 4 is forbidden")
    for index, attempt in enumerate(ordered_attempts):
        _require(attempt["claim_id"] in claims, "attempt cites missing claim")
        _require(attempt["checkpoint_id"] in checkpoints, "attempt cites missing checkpoint")
        _require(attempt["executor_id"] in executors and executors[attempt["executor_id"]]["eligible"], "attempt executor is not eligible")
        _require(checkpoints[attempt["checkpoint_id"]]["status"] == "SAFE", "attempt requires safe checkpoint")
        if index:
            prior = ordered_attempts[index - 1]
            _require(attempt["prior_attempt_id"] == prior["attempt_id"], "prior attempt ID mismatch")
            _require(attempt["prior_attempt_digest"] == canonical_digest(prior), "prior attempt digest mismatch")
            _require(attempt["failed_event_id"] in events, "later attempt cites missing failed event")
            _require(attempt["handoff_id"] in handoffs, "later attempt cites missing handoff")
            failed_event = events[attempt["failed_event_id"]]
            cited_handoff = handoffs[attempt["handoff_id"]]
            _require(failed_event["attempt_id"] == prior["attempt_id"], "failed event does not belong to prior attempt")
            _require(failed_event["failure_class"] != "NONE", "failed event lacks failure evidence")
            _require(cited_handoff["claim_id"] == prior["claim_id"], "handoff does not belong to prior claim")
            _require(
                _timestamp(failed_event["observed_at"], "failed event observed_at")
                <= _timestamp(cited_handoff["created_at"], "handoff created_at")
                <= _timestamp(attempt["created_at"], "attempt created_at"),
                "failed event, handoff, and attempt chronology invalid",
            )
            _require(attempt["claim_id"] != prior["claim_id"], "reassignment must use a new claim")
            _require(_claim_safe(claims[prior["claim_id"]], now), "prior claim remains live")
    ordered_events = list(chain["events"])
    used_gates: set[str] = set()
    for index, event in enumerate(ordered_events):
        _require(event["attempt_id"] in attempts, "event cites missing attempt")
        current_attempt = attempts[event["attempt_id"]]
        _require(event["attempt_number"] == current_attempt["attempt_number"], "event attempt number mismatch")
        if index == 0:
            _require(event["prior_event_id"] is None, "first event cannot cite a prior event")
        else:
            prior = ordered_events[index - 1]
            _require(event["prior_event_id"] == prior["event_id"], "prior event ID mismatch")
            _require(event["prior_event_digest"] == canonical_digest(prior), "prior event digest mismatch")
            _require(event["prior_state"] == prior["next_state"], "event state chain is discontinuous")
            _require(_timestamp(prior["observed_at"], "prior observed_at") <= _timestamp(event["observed_at"], "observed_at"), "event chronology invalid")
        if event["next_state"] == "READY_FOR_REASSIGNMENT":
            _require(event["handoff_id"] in handoffs, "READY_FOR_REASSIGNMENT requires handoff")
            _require(event["checkpoint_id"] in checkpoints and checkpoints[event["checkpoint_id"]]["status"] == "SAFE", "READY_FOR_REASSIGNMENT requires safe checkpoint")
            _require(_claim_safe(claims[current_attempt["claim_id"]], now), "READY_FOR_REASSIGNMENT requires non-live claim")
            expected_disposition = "RELEASED" if claims[current_attempt["claim_id"]]["status"] == "RELEASED" else "EXPIRED"
            _require(event["claim_disposition"] == expected_disposition, "claim disposition does not match claim evidence")
            _require(any(record["eligible"] for record in executors.values()), "READY_FOR_REASSIGNMENT requires eligible executor evidence")
        gate_action = None
        if event["prior_state"] == "READY_FOR_REASSIGNMENT" and event["next_state"] == "REASSIGNED":
            gate_action = "REASSIGN"
        elif event["next_state"] == "ABORTED":
            gate_action = "ABORT"
        elif event["next_state"] == "RESUMED" and any(e["failure_class"] == "CHECKPOINT_MISSING" for e in ordered_events[:index]):
            gate_action = "EVIDENCE_RESUME"
        if gate_action:
            _require(event["owner_gate_id"] in gates, f"{gate_action} requires owner gate")
            gate = gates[event["owner_gate_id"]]
            _require(gate["action"] == gate_action and gate["prior_state"] == event["prior_state"] and gate["next_state"] == event["next_state"] and gate["attempt_number"] == event["attempt_number"], "owner gate does not match transition")
            used_gates.add(gate["gate_id"])
        else:
            _require(event["owner_gate_id"] is None, "unexpected owner gate")
        if event["failure_class"] == "CHECKPOINT_MISSING":
            _require(
                event["checkpoint_id"] in checkpoints
                and checkpoints[event["checkpoint_id"]]["status"] in {"MISSING", "INVALID"},
                "CHECKPOINT_MISSING requires missing or invalid checkpoint evidence",
            )
        if event["next_state"] == "RESUMED":
            _require(event["checkpoint_id"] in checkpoints and checkpoints[event["checkpoint_id"]]["status"] == "SAFE", "resume requires newly supplied safe checkpoint")
            prior_missing = [e for e in ordered_events[:index] if e["failure_class"] == "CHECKPOINT_MISSING"]
            if prior_missing:
                safe_checkpoint = checkpoints[event["checkpoint_id"]]
                _require(
                    _timestamp(safe_checkpoint["created_at"], "safe checkpoint created_at")
                    >= _timestamp(prior_missing[-1]["observed_at"], "missing checkpoint observed_at"),
                    "resume checkpoint predates missing-checkpoint evidence",
                )
    for attempt_index, attempt in enumerate(ordered_attempts):
        attempt_events = [event for event in ordered_events if event["attempt_id"] == attempt["attempt_id"]]
        if attempt_index == 0:
            _require(attempt_events, "initial attempt has no event evidence")
            _require(attempt_events[0]["prior_state"] == attempt["state"], "initial attempt state mismatch")
        else:
            creation_events = [event for event in attempt_events if event["next_state"] == "REASSIGNED"]
            _require(len(creation_events) == 1 and attempt["state"] == "REASSIGNED", "later attempt lacks one reassignment event")
    _require(used_gates == set(gates), "duplicate or unused owner gate evidence")
    _require(chain == original, "validation mutated input")
    return chain


def simulate_transition(chain: dict[str, Any], proposal: dict[str, Any], as_of: str) -> dict[str, Any]:
    validate_chain(chain, as_of)
    validate_event(proposal, as_of)
    last = chain["events"][-1] if chain["events"] else None
    if last:
        _require(proposal["prior_event_id"] == last["event_id"], "proposal must cite latest event")
        _require(proposal["prior_event_digest"] == canonical_digest(last), "proposal prior digest mismatch")
        _require(proposal["prior_state"] == last["next_state"], "proposal state mismatch")
    preview_chain = copy.deepcopy(chain)
    preview_chain["events"].append(copy.deepcopy(proposal))
    validate_chain(preview_chain, as_of)
    return {
        "accepted": True,
        "attempt_number": proposal["attempt_number"],
        "from": proposal["prior_state"],
        "to": proposal["next_state"],
        "writes_performed": False,
    }


def explain_failover(chain: dict[str, Any], as_of: str) -> dict[str, Any]:
    validate_chain(chain, as_of)
    last_event = chain["events"][-1] if chain["events"] else None
    last_attempt = max(chain["attempts"], key=lambda item: item["attempt_number"])
    state = last_event["next_state"] if last_event else last_attempt["state"]
    return {
        "work_order_id": chain["work_order_id"],
        "state": state,
        "attempt_number": last_attempt["attempt_number"],
        "attempts_remaining": MAX_ATTEMPTS - last_attempt["attempt_number"],
        "blockers": [] if state in {"HEALTHY", "RECOVERED"} else ["manual evidence review required"],
        "next_safe_action": "retain evidence" if state == "HEALTHY" else "follow the legal transition graph",
        "writes_performed": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-event", "validate-attempt", "validate-chain", "explain-failover"):
        command = sub.add_parser(name)
        command.add_argument("--input", required=True)
        command.add_argument("--as-of", required=True)
    simulation = sub.add_parser("simulate-transition")
    simulation.add_argument("--chain", required=True)
    simulation.add_argument("--proposal", required=True)
    simulation.add_argument("--as-of", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate-event":
            result = validate_event(load_json(args.input), args.as_of)
        elif args.command == "validate-attempt":
            result = validate_attempt(load_json(args.input), args.as_of)
        elif args.command == "validate-chain":
            result = validate_chain(load_json(args.input), args.as_of)
        elif args.command == "simulate-transition":
            result = simulate_transition(load_json(args.chain), load_json(args.proposal), args.as_of)
        else:
            result = explain_failover(load_json(args.input), args.as_of)
    except (FailoverError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
