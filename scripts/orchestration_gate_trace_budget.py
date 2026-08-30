#!/usr/bin/env python3
"""Deterministic, read-only validation for STUDIO-007E gate, trace, and quota records."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class ValidationError(ValueError):
    """Raised when an orchestration record violates the STUDIO-007E contract."""


ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
DRIVE_RE = re.compile(r"^[A-Za-z]:")
SECRET_KEYS = {
    "api_key", "apikey", "authorization", "bearer", "client_secret", "credential",
    "credentials", "password", "private_key", "refresh_token", "secret",
    "session_cookie", "token", "access_token",
}
SECRET_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)^bearer\s+[A-Za-z0-9._~+/=-]{12,}$"),
    re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)

GATE_ROLE = {
    "SCOPE_BOUNDARY": "ENGINEERING",
    "EVIDENCE_INTEGRITY": "ENGINEERING",
    "QUOTA_BUDGET": "ENGINEERING",
    "SECRET_SAFETY": "ENGINEERING",
    "FOCUSED_TESTS": "ENGINEERING",
    "RETAINED_REGRESSION": "ENGINEERING",
    "QA_ACCEPTANCE": "QA",
    "REVIEW_INTEGRATION": "REVIEW_INTEGRATION",
    "OWNER_DECISION": "STUDIO_OWNER",
}
BASE_GATES = {"SCOPE_BOUNDARY", "EVIDENCE_INTEGRITY", "QUOTA_BUDGET", "SECRET_SAFETY"}
IMPLEMENTATION_GATES = {"FOCUSED_TESTS", "RETAINED_REGRESSION"}
REPOSITORY_GATES = {"QA_ACCEPTANCE", "REVIEW_INTEGRATION"}

ARTIFACT_FIELDS = {"repository", "commit_sha", "artifact_digest", "changed_paths"}
GATE_FIELDS = {
    "schema_version", "gate_id", "work_order_id", "attempt_number", "gate_type",
    "evaluator_id", "evaluator_role", "evidence_references", "artifact_identity",
    "verdict", "reasons", "evaluated_at", "prior_gate_id", "prior_gate_digest",
}
TRACE_FIELDS = {
    "schema_version", "trace_event_id", "correlation_id", "sequence_number",
    "work_order_id", "attempt_number", "actor_id", "actor_role", "capability",
    "prior_state", "next_state", "input_references", "output_references", "outcome",
    "gate_ids", "quota_id", "artifact_identity", "observed_at", "prior_event_id",
    "prior_event_digest",
}
QUOTA_FIELDS = {
    "schema_version", "quota_id", "work_order_id", "attempt_number", "cost_class",
    "monetary_budget", "monetary_spend", "max_attempts", "max_elapsed_seconds",
    "max_changed_paths", "max_output_bytes", "started_at", "evaluated_at",
    "observed_attempts", "observed_changed_paths", "observed_output_bytes",
    "owner_amendments",
}
BUNDLE_FIELDS = {
    "schema_version", "work_order_id", "work_order_type", "repository_changing",
    "artifact_identity", "gates", "trace_events", "quota",
}
AMENDMENT_FIELDS = {
    "amendment_id", "limit_name", "prior_value", "new_value", "approved_by",
    "approved_role", "decided_at", "expires_at", "reason",
}


def _error(message: str) -> None:
    raise ValidationError(message)


def _exact(record: dict[str, Any], fields: set[str], label: str) -> None:
    if not isinstance(record, dict):
        _error(f"{label} must be an object")
    missing = sorted(fields - set(record))
    extra = sorted(set(record) - fields)
    if missing or extra:
        _error(f"{label} fields differ; missing={missing}, extra={extra}")


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        _error(f"{label} is not a valid identifier")
    return value


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        _error(f"{label} must be an integer >= {minimum}")
    return value


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        _error(f"{label} must be a non-negative number")
    return float(value)


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        _error(f"{label} must be an explicit UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValidationError(f"{label} is not a valid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        _error(f"{label} must be UTC")
    return parsed


def _as_of(value: str) -> datetime:
    return _timestamp(value, "as_of")


def _string_list(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        _error(f"{label} must be a{' non-empty' if nonempty else ''} list")
    if any(not isinstance(item, str) or not item or len(item) > 512 for item in value):
        _error(f"{label} contains an invalid string")
    if len(set(value)) != len(value):
        _error(f"{label} must not contain duplicates")
    return value


def canonical_digest(record: Any) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _path(value: str) -> None:
    if (
        not value or value.startswith(("/", "\\")) or DRIVE_RE.match(value)
        or "\\" in value or "//" in value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        _error(f"changed path is not normalized repository-relative: {value!r}")


def validate_artifact(record: dict[str, Any]) -> dict[str, Any]:
    _exact(record, ARTIFACT_FIELDS, "artifact_identity")
    _identifier(record["repository"], "artifact repository")
    if not isinstance(record["commit_sha"], str) or not SHA_RE.fullmatch(record["commit_sha"]):
        _error("artifact commit_sha must be 40 lowercase hexadecimal characters")
    if not isinstance(record["artifact_digest"], str) or not DIGEST_RE.fullmatch(record["artifact_digest"]):
        _error("artifact_digest must be a sha256 digest")
    paths = _string_list(record["changed_paths"], "changed_paths")
    for item in paths:
        _path(item)
    if paths != sorted(paths):
        _error("changed_paths must be sorted")
    return record


def _scan_secrets(value: Any, path: str = "$", *, key_context: str | None = None) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in SECRET_KEYS:
                _error(f"secret-like field is forbidden at {path}.{key}")
            _scan_secrets(child, f"{path}.{key}", key_context=lowered)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_secrets(child, f"{path}[{index}]", key_context=key_context)
    elif isinstance(value, str):
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                _error(f"secret-like value is forbidden at {path}")


def validate_gate(record: dict[str, Any], *, as_of: str) -> dict[str, Any]:
    _scan_secrets(record)
    _exact(record, GATE_FIELDS, "gate result")
    if record["schema_version"] != "1.0":
        _error("unsupported gate schema_version")
    for key in ("gate_id", "work_order_id", "evaluator_id"):
        _identifier(record[key], key)
    attempt = _integer(record["attempt_number"], "attempt_number", 1)
    if attempt > 3:
        _error("attempt_number exceeds the default ceiling of 3")
    gate_type = record["gate_type"]
    if gate_type not in GATE_ROLE:
        _error("unknown gate_type")
    if record["evaluator_role"] != GATE_ROLE[gate_type]:
        _error(f"{gate_type} requires evaluator_role {GATE_ROLE[gate_type]}")
    _string_list(record["evidence_references"], "evidence_references", nonempty=True)
    _string_list(record["reasons"], "reasons", nonempty=True)
    validate_artifact(record["artifact_identity"])
    if record["verdict"] not in {"PASS", "FAIL", "PAUSE"}:
        _error("invalid gate verdict")
    if _timestamp(record["evaluated_at"], "evaluated_at") > _as_of(as_of):
        _error("gate evaluation is in the future relative to as_of")
    prior_id, prior_digest = record["prior_gate_id"], record["prior_gate_digest"]
    if (prior_id is None) != (prior_digest is None):
        _error("prior_gate_id and prior_gate_digest must both be null or both be present")
    if prior_id is not None:
        _identifier(prior_id, "prior_gate_id")
        if not isinstance(prior_digest, str) or not DIGEST_RE.fullmatch(prior_digest):
            _error("prior_gate_digest must be a sha256 digest")
    return record


def _effective_limits(record: dict[str, Any], *, as_of: str) -> dict[str, int]:
    limits = {
        "max_elapsed_seconds": 7200,
        "max_changed_paths": 25,
        "max_output_bytes": 2097152,
    }
    amendments = record["owner_amendments"]
    if not isinstance(amendments, list):
        _error("owner_amendments must be a list")
    seen: set[str] = set()
    evaluated_at = _timestamp(record["evaluated_at"], "evaluated_at")
    for index, item in enumerate(amendments):
        _exact(item, AMENDMENT_FIELDS, f"owner_amendments[{index}]")
        amendment_id = _identifier(item["amendment_id"], "amendment_id")
        if amendment_id in seen:
            _error("owner amendment identifiers must be unique")
        seen.add(amendment_id)
        name = item["limit_name"]
        if name not in limits:
            _error("only time, path, and output ceilings may be amended")
        prior = _integer(item["prior_value"], "prior_value", 1)
        new = _integer(item["new_value"], "new_value", 1)
        if prior != limits[name] or new <= prior:
            _error("owner amendment must extend the current limit")
        _identifier(item["approved_by"], "approved_by")
        if item["approved_role"] != "STUDIO_OWNER":
            _error("quota amendment requires STUDIO_OWNER approval")
        decided = _timestamp(item["decided_at"], "decided_at")
        expires = _timestamp(item["expires_at"], "expires_at")
        if decided > evaluated_at or decided > _as_of(as_of) or expires < evaluated_at:
            _error("owner amendment is not effective at evaluation time")
        if not isinstance(item["reason"], str) or not item["reason"]:
            _error("owner amendment requires a reason")
        limits[name] = new
    return limits


def validate_budget(record: dict[str, Any], *, as_of: str) -> dict[str, Any]:
    _scan_secrets(record)
    _exact(record, QUOTA_FIELDS, "quota budget")
    if record["schema_version"] != "1.0":
        _error("unsupported quota schema_version")
    for key in ("quota_id", "work_order_id"):
        _identifier(record[key], key)
    attempt = _integer(record["attempt_number"], "attempt_number", 1)
    if record["cost_class"] != "ZERO_COST":
        _error("cost_class must be ZERO_COST")
    if _number(record["monetary_budget"], "monetary_budget") != 0:
        _error("monetary_budget must remain zero")
    if _number(record["monetary_spend"], "monetary_spend") != 0:
        _error("monetary_spend must remain zero")
    if record["max_attempts"] != 3:
        _error("max_attempts is immutable and must equal 3")
    if record["max_elapsed_seconds"] != 7200 or record["max_changed_paths"] != 25 or record["max_output_bytes"] != 2097152:
        _error("base quota ceilings must equal the STUDIO-007E defaults")
    started = _timestamp(record["started_at"], "started_at")
    evaluated = _timestamp(record["evaluated_at"], "evaluated_at")
    now = _as_of(as_of)
    if started > evaluated or evaluated > now:
        _error("quota chronology is invalid")
    observed_attempts = _integer(record["observed_attempts"], "observed_attempts", 1)
    observed_paths = _integer(record["observed_changed_paths"], "observed_changed_paths")
    observed_output = _integer(record["observed_output_bytes"], "observed_output_bytes")
    if attempt != observed_attempts:
        _error("attempt_number must equal observed_attempts")
    limits = _effective_limits(record, as_of=as_of)
    if observed_attempts > 3:
        _error("attempt ceiling exceeded")
    elapsed = int((evaluated - started).total_seconds())
    if elapsed > limits["max_elapsed_seconds"]:
        _error("elapsed-time ceiling exceeded")
    if observed_paths > limits["max_changed_paths"]:
        _error("changed-path ceiling exceeded")
    if observed_output > limits["max_output_bytes"]:
        _error("output-size ceiling exceeded")
    for amendment in record["owner_amendments"]:
        observed = {
            "max_elapsed_seconds": elapsed,
            "max_changed_paths": observed_paths,
            "max_output_bytes": observed_output,
        }[amendment["limit_name"]]
        if observed <= amendment["prior_value"]:
            _error("owner amendment is unused and therefore not evidence-bearing")
    return record


def validate_trace(
    records: list[dict[str, Any]], *, gates: Iterable[dict[str, Any]], as_of: str
) -> list[dict[str, Any]]:
    if not isinstance(records, list) or not records:
        _error("trace_events must be a non-empty list")
    gate_index = {gate["gate_id"]: gate for gate in gates}
    first: dict[str, Any] | None = None
    previous: dict[str, Any] | None = None
    for index, record in enumerate(records):
        _scan_secrets(record)
        _exact(record, TRACE_FIELDS, f"trace_events[{index}]")
        if record["schema_version"] != "1.0":
            _error("unsupported trace schema_version")
        for key in ("trace_event_id", "correlation_id", "work_order_id", "actor_id", "capability", "quota_id"):
            _identifier(record[key], key)
        if record["actor_role"] not in {"ENGINEERING", "QA", "REVIEW_INTEGRATION", "STUDIO_OWNER"}:
            _error("invalid actor_role")
        if record["outcome"] not in {"ACCEPTED", "PAUSED", "FAILED"}:
            _error("invalid trace outcome")
        _identifier(record["prior_state"], "prior_state")
        _identifier(record["next_state"], "next_state")
        _string_list(record["input_references"], "input_references")
        _string_list(record["output_references"], "output_references")
        gate_ids = _string_list(record["gate_ids"], "gate_ids")
        validate_artifact(record["artifact_identity"])
        observed = _timestamp(record["observed_at"], "observed_at")
        if observed > _as_of(as_of):
            _error("trace event is in the future relative to as_of")
        sequence = _integer(record["sequence_number"], "sequence_number", 1)
        attempt = _integer(record["attempt_number"], "attempt_number", 1)
        if attempt > 3:
            _error("trace attempt exceeds the default ceiling")
        if first is None:
            first = record
            if sequence != 1 or record["prior_event_id"] is not None or record["prior_event_digest"] is not None:
                _error("first trace event must start at sequence 1 with no predecessor")
        else:
            assert previous is not None and first is not None
            if sequence != previous["sequence_number"] + 1:
                _error("trace sequence must be consecutive")
            if record["correlation_id"] != first["correlation_id"] or record["work_order_id"] != first["work_order_id"]:
                _error("trace correlation or work order changed")
            if record["artifact_identity"] != first["artifact_identity"]:
                _error("trace artifact identity changed")
            if attempt < previous["attempt_number"] or attempt > previous["attempt_number"] + 1:
                _error("trace attempt chronology is invalid")
            if observed < _timestamp(previous["observed_at"], "previous observed_at"):
                _error("trace time chronology is invalid")
            if record["prior_event_id"] != previous["trace_event_id"]:
                _error("trace predecessor identifier is broken")
            if record["prior_event_digest"] != canonical_digest(previous):
                _error("trace predecessor digest is broken or mutated")
        for gate_id in gate_ids:
            gate = gate_index.get(gate_id)
            if gate is None or gate["verdict"] != "PASS":
                _error("trace references a missing or non-passing gate")
            if _timestamp(gate["evaluated_at"], "gate evaluated_at") > observed:
                _error("trace references a gate that was not yet effective")
        previous = record
    return records


def required_gate_types(work_order_type: str, repository_changing: bool) -> set[str]:
    required = set(BASE_GATES)
    if work_order_type == "IMPLEMENTATION":
        required |= IMPLEMENTATION_GATES
    if repository_changing:
        required |= REPOSITORY_GATES
    return required


def validate_bundle(record: dict[str, Any], *, as_of: str) -> dict[str, Any]:
    _scan_secrets(record)
    _exact(record, BUNDLE_FIELDS, "validation bundle")
    if record["schema_version"] != "1.0":
        _error("unsupported bundle schema_version")
    work_order = _identifier(record["work_order_id"], "work_order_id")
    if record["work_order_type"] not in {"CONTRACT", "IMPLEMENTATION", "DOCUMENTATION", "RESEARCH", "OTHER"}:
        _error("invalid work_order_type")
    if not isinstance(record["repository_changing"], bool):
        _error("repository_changing must be boolean")
    artifact = validate_artifact(record["artifact_identity"])
    if not isinstance(record["gates"], list) or not record["gates"]:
        _error("gates must be a non-empty list")
    gates = [validate_gate(item, as_of=as_of) for item in record["gates"]]
    ids: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for gate in gates:
        if gate["gate_id"] in ids:
            _error("gate identifiers must be unique")
        ids.add(gate["gate_id"])
        by_id[gate["gate_id"]] = gate
        if gate["work_order_id"] != work_order or gate["artifact_identity"] != artifact:
            _error("gate is bound to a different work order or artifact")
        if gate["prior_gate_id"] is not None:
            prior = by_id.get(gate["prior_gate_id"])
            if prior is None or gate["prior_gate_digest"] != canonical_digest(prior):
                _error("gate predecessor is missing or mutated")
    required = required_gate_types(record["work_order_type"], record["repository_changing"])
    passing = {gate["gate_type"] for gate in gates if gate["verdict"] == "PASS"}
    missing = sorted(required - passing)
    if missing:
        _error(f"mandatory passing gates are missing: {missing}")
    quota = validate_budget(record["quota"], as_of=as_of)
    if quota["work_order_id"] != work_order:
        _error("quota is bound to a different work order")
    traces = validate_trace(record["trace_events"], gates=gates, as_of=as_of)
    for trace in traces:
        if trace["work_order_id"] != work_order or trace["quota_id"] != quota["quota_id"]:
            _error("trace is bound to a different work order or quota")
        if trace["artifact_identity"] != artifact:
            _error("trace is bound to a different artifact")
    return record


def evaluate_attempt(record: dict[str, Any], *, as_of: str) -> dict[str, Any]:
    try:
        validate_bundle(copy.deepcopy(record), as_of=as_of)
    except ValidationError as exc:
        return {"decision": "PAUSE", "reasons": [str(exc)]}
    return {"decision": "ACCEPT", "reasons": ["all mandatory gates and quota boundaries passed"]}


def explain_boundary() -> dict[str, Any]:
    return {
        "cost_class": "ZERO_COST",
        "default_limits": {"attempts": 3, "elapsed_seconds": 7200, "changed_paths": 25, "output_bytes": 2097152, "money": 0},
        "amendable_by_studio_owner": ["elapsed_seconds", "changed_paths", "output_bytes"],
        "immutable": ["attempts", "money"],
    }


def _load(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-gate", "validate-trace", "validate-budget", "validate-bundle", "evaluate-attempt"):
        command = sub.add_parser(name)
        command.add_argument("path")
        command.add_argument("--as-of", required=True)
        if name == "validate-trace":
            command.add_argument("--gates", required=True)
    sub.add_parser("explain-boundary")
    args = parser.parse_args(argv)
    try:
        if args.command == "explain-boundary":
            result = explain_boundary()
        else:
            payload = _load(args.path)
            if args.command == "validate-gate":
                result = validate_gate(payload, as_of=args.as_of)
            elif args.command == "validate-budget":
                result = validate_budget(payload, as_of=args.as_of)
            elif args.command == "validate-trace":
                result = validate_trace(payload, gates=_load(args.gates), as_of=args.as_of)
            elif args.command == "validate-bundle":
                result = validate_bundle(payload, as_of=args.as_of)
            else:
                result = evaluate_attempt(payload, as_of=args.as_of)
                if result["decision"] != "ACCEPT":
                    print(json.dumps(result, sort_keys=True))
                    return 1
        print(json.dumps({"status": "PASS", "result": result}, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
