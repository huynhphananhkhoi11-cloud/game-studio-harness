#!/usr/bin/env python3
"""Deterministic, zero-cost provider-neutral adapter validation for STUDIO-007F."""

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


class AdapterError(ValueError):
    """Raised when adapter evidence violates the STUDIO-007F contract."""


ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REFERENCE_RE = re.compile(
    r"^(?:artifact|evidence|gate|trace|budget|handoff|fixture)://"
    r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,510}$"
)
TIMESTAMP_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
MAX_INPUT_BYTES = 2097152

ADAPTER_TYPES = {"MANUAL", "FAKE"}
OPERATIONS = {
    "NORMALIZE_MANUAL_RESULT",
    "SIMULATE_SUCCESS",
    "SIMULATE_REFUSAL",
    "SIMULATE_TIMEOUT",
    "SIMULATE_FAILURE",
}
OPERATION_ADAPTER = {
    "NORMALIZE_MANUAL_RESULT": "MANUAL",
    "SIMULATE_SUCCESS": "FAKE",
    "SIMULATE_REFUSAL": "FAKE",
    "SIMULATE_TIMEOUT": "FAKE",
    "SIMULATE_FAILURE": "FAKE",
}
OPERATION_OUTCOME = {
    "SIMULATE_SUCCESS": ("SUCCESS", "NONE"),
    "SIMULATE_REFUSAL": ("REFUSED", "REFUSAL"),
    "SIMULATE_TIMEOUT": ("TIMEOUT", "TIMEOUT"),
    "SIMULATE_FAILURE": ("FAILURE", "ADAPTER_FAILURE"),
}
STATUS_ERROR = {
    "SUCCESS": {"NONE"},
    "REFUSED": {"REFUSAL"},
    "TIMEOUT": {"TIMEOUT"},
    "FAILURE": {"MALFORMED_OUTPUT", "ADAPTER_FAILURE"},
}
INPUT_KINDS = {"ARTIFACT_REFERENCE", "EVIDENCE_REFERENCE", "WORK_ORDER_REFERENCE"}
OUTPUT_KINDS = {"RESULT_REFERENCE", "HANDOFF_REFERENCE"}
REQUIRED_GATES = {
    "gate://scope-boundary",
    "gate://evidence-integrity",
    "gate://quota-budget",
    "gate://secret-safety",
}

ARTIFACT_FIELDS = {"repository", "commit_sha", "artifact_digest"}
CAPABILITY_FIELDS = {
    "schema_version", "capability_id", "adapter_type", "operation",
    "accepted_input_kinds", "produced_output_kinds", "deterministic",
    "cost_class", "network_access", "authority_grants",
}
REQUEST_FIELDS = {
    "schema_version", "request_id", "work_order_id", "attempt_number",
    "adapter_type", "capability_id", "correlation_id", "artifact_identity",
    "input_references", "gate_evidence_references", "trace_reference",
    "budget_reference", "created_at", "as_of",
}
COUNTER_FIELDS = {
    "input_references", "output_references", "output_bytes",
    "monetary_minor_units",
}
RESULT_FIELDS = {
    "schema_version", "result_id", "request_id", "work_order_id",
    "attempt_number", "adapter_type", "capability_id", "correlation_id",
    "artifact_identity", "status", "output_references",
    "evidence_references", "usage_counters", "error_class",
    "handoff_reference", "completed_at",
}
BUNDLE_FIELDS = {"schema_version", "as_of", "capability", "request", "result"}

FORBIDDEN_KEYS = {
    "account", "account_id", "api_key", "apikey", "authorization", "bearer",
    "client_secret", "credential", "credentials", "endpoint", "model",
    "password", "private_key", "provider", "refresh_token", "secret",
    "session_cookie", "token", "access_token",
}
FORBIDDEN_KEY_TOKENS = {
    "account", "apikey", "authorization", "bearer", "credential",
    "credentials", "endpoint", "model", "password", "provider", "secret",
    "token",
}
FORBIDDEN_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)^bearer\s+[A-Za-z0-9._~+/=-]{12,}$"),
    re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(?:password|token|secret|api[_-]?key|authorization|cookie)\s*[:=]\s*\S+"),
    re.compile(r"(?i)(?:^|[/:._-])(?:provider|model|endpoint|account)(?:[/:._=-]|$)"),
)


def _error(message: str) -> None:
    raise AdapterError(message)


def _exact(record: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(record, dict):
        _error(f"{label} must be an object")
    missing = sorted(fields - set(record))
    extra = sorted(set(record) - fields)
    if missing or extra:
        _error(f"{label} fields differ; missing={missing}, extra={extra}")
    return record


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        _error(f"{label} is not a valid identifier")
    return value


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        _error(f"{label} must be an integer >= {minimum}")
    return value


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not TIMESTAMP_RE.fullmatch(value):
        _error(f"{label} must be a canonical UTC timestamp with whole seconds")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise AdapterError(f"{label} is not a valid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        _error(f"{label} must be UTC")
    return parsed


def _scan_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            normalized = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
            tokens = set(normalized.split("_"))
            if lowered in FORBIDDEN_KEYS or normalized in FORBIDDEN_KEYS or tokens & FORBIDDEN_KEY_TOKENS:
                _error(f"forbidden provider or secret field at {path}.{key}")
            _scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_forbidden(child, f"{path}[{index}]")
    elif isinstance(value, str):
        for pattern in FORBIDDEN_VALUE_PATTERNS:
            if pattern.search(value):
                _error(f"secret-like value is forbidden at {path}")


def _string_list(
    value: Any,
    label: str,
    *,
    allowed: set[str] | None = None,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        _error(f"{label} must be a{' non-empty' if nonempty else ''} list")
    if any(not isinstance(item, str) or not item or len(item) > 512 for item in value):
        _error(f"{label} contains an invalid string")
    if len(set(value)) != len(value):
        _error(f"{label} must not contain duplicates")
    if allowed is not None and any(item not in allowed for item in value):
        _error(f"{label} contains an unsupported value")
    if value != sorted(value):
        _error(f"{label} must be sorted")
    return value


def _reference(value: Any, label: str, *, scheme: str | None = None) -> str:
    if not isinstance(value, str) or not REFERENCE_RE.fullmatch(value):
        _error(f"{label} is not a safe reference")
    if ".." in value or "\\" in value or "//" in value.split("://", 1)[1]:
        _error(f"{label} is not normalized")
    if scheme is not None and not value.startswith(scheme + "://"):
        _error(f"{label} must use the {scheme} scheme")
    return value


def _references(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    values = _string_list(value, label, nonempty=nonempty)
    for item in values:
        _reference(item, label)
    return values


def canonical_json(record: Any) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_digest(record: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(record).encode("utf-8")).hexdigest()


def validate_artifact(record: Any) -> dict[str, Any]:
    record = _exact(record, ARTIFACT_FIELDS, "artifact_identity")
    _identifier(record["repository"], "artifact repository")
    if not isinstance(record["commit_sha"], str) or not SHA_RE.fullmatch(record["commit_sha"]):
        _error("artifact commit_sha must be 40 lowercase hexadecimal characters")
    if not isinstance(record["artifact_digest"], str) or not DIGEST_RE.fullmatch(record["artifact_digest"]):
        _error("artifact_digest must be a SHA-256 digest")
    return record


def validate_capability(record: Any) -> dict[str, Any]:
    original = copy.deepcopy(record)
    _scan_forbidden(record)
    record = _exact(record, CAPABILITY_FIELDS, "capability")
    if record["schema_version"] != "1.0":
        _error("unsupported capability schema_version")
    _identifier(record["capability_id"], "capability_id")
    if record["adapter_type"] not in ADAPTER_TYPES:
        _error("unsupported adapter_type")
    operation = record["operation"]
    if operation not in OPERATIONS:
        _error("unsupported operation")
    if OPERATION_ADAPTER[operation] != record["adapter_type"]:
        _error("operation is not declared for this adapter type")
    _string_list(record["accepted_input_kinds"], "accepted_input_kinds", allowed=INPUT_KINDS, nonempty=True)
    _string_list(record["produced_output_kinds"], "produced_output_kinds", allowed=OUTPUT_KINDS, nonempty=True)
    if "RESULT_REFERENCE" not in record["produced_output_kinds"]:
        _error("capability must declare RESULT_REFERENCE output")
    if record["deterministic"] is not True:
        _error("v1.0 capabilities must be deterministic")
    if record["cost_class"] != "ZERO_COST":
        _error("cost_class must be ZERO_COST")
    if record["network_access"] is not False:
        _error("network_access must be false")
    if record["authority_grants"] != []:
        _error("adapter capability cannot grant authority")
    if record != original:
        _error("capability validation mutated input")
    return record


def validate_request(record: Any, capability: Any, *, as_of: str) -> dict[str, Any]:
    original = copy.deepcopy(record)
    _scan_forbidden(record)
    record = _exact(record, REQUEST_FIELDS, "adapter request")
    capability = validate_capability(capability)
    if record["schema_version"] != "1.0":
        _error("unsupported request schema_version")
    for key in ("request_id", "work_order_id", "capability_id", "correlation_id"):
        _identifier(record[key], key)
    attempt = _integer(record["attempt_number"], "attempt_number", 1)
    if attempt > 3:
        _error("attempt_number exceeds the v1.0 ceiling")
    if record["adapter_type"] not in ADAPTER_TYPES:
        _error("unsupported adapter_type")
    if record["adapter_type"] != capability["adapter_type"]:
        _error("request adapter_type does not match capability")
    if record["capability_id"] != capability["capability_id"]:
        _error("request cites an undeclared capability")
    validate_artifact(record["artifact_identity"])
    inputs = _references(record["input_references"], "input_references", nonempty=True)
    accepted = set(capability["accepted_input_kinds"])
    for reference in inputs:
        if reference.startswith("artifact://"):
            required_kind = "ARTIFACT_REFERENCE"
        elif reference.startswith("evidence://work-order/"):
            required_kind = "WORK_ORDER_REFERENCE"
        else:
            required_kind = "EVIDENCE_REFERENCE"
        if required_kind not in accepted:
            _error(f"request uses undeclared input kind {required_kind}")
    gates = _references(record["gate_evidence_references"], "gate_evidence_references", nonempty=True)
    if not REQUIRED_GATES.issubset(gates):
        _error("request lacks required gate evidence")
    _reference(record["trace_reference"], "trace_reference", scheme="trace")
    _reference(record["budget_reference"], "budget_reference", scheme="budget")
    correlation_suffix = record["correlation_id"].split(":", 1)[-1].replace(":", "-")
    work_order_suffix = record["work_order_id"].split(":", 1)[-1].replace(":", "-")
    if record["trace_reference"] != f"trace://correlation/{correlation_suffix}":
        _error("trace_reference does not bind the request correlation_id")
    if record["budget_reference"] != f"budget://zero-cost/{work_order_suffix}":
        _error("budget_reference does not bind the request work_order_id")
    created = _timestamp(record["created_at"], "created_at")
    embedded_as_of = _timestamp(record["as_of"], "request as_of")
    supplied_as_of = _timestamp(as_of, "as_of")
    if record["as_of"] != as_of:
        _error("request as_of must equal caller-supplied as_of")
    if created > embedded_as_of or embedded_as_of != supplied_as_of:
        _error("request chronology is invalid")
    if record != original:
        _error("request validation mutated input")
    return record


def _validate_usage(record: Any, request: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    record = _exact(record, COUNTER_FIELDS, "usage_counters")
    if record["input_references"] != len(request["input_references"]):
        _error("input usage counter does not match request evidence")
    if record["output_references"] != len(result["output_references"]):
        _error("output usage counter does not match result evidence")
    _integer(record["output_bytes"], "output_bytes")
    expected_output_bytes = len(canonical_json(result["output_references"]).encode("utf-8"))
    if record["output_bytes"] != expected_output_bytes:
        _error("output_bytes does not match canonical output-reference evidence")
    if record["output_bytes"] > 2097152:
        _error("output_bytes exceeds the inherited v1.0 ceiling")
    if record["monetary_minor_units"] != 0:
        _error("monetary usage must remain zero")
    return record


def validate_result(
    record: Any,
    request: Any,
    capability: Any,
    *,
    as_of: str,
) -> dict[str, Any]:
    original = copy.deepcopy(record)
    _scan_forbidden(record)
    record = _exact(record, RESULT_FIELDS, "adapter result")
    request = validate_request(request, capability, as_of=as_of)
    capability = validate_capability(capability)
    if record["schema_version"] != "1.0":
        _error("unsupported result schema_version")
    for key in ("result_id", "request_id", "work_order_id", "capability_id", "correlation_id"):
        _identifier(record[key], key)
    for key in (
        "request_id", "work_order_id", "attempt_number", "adapter_type",
        "capability_id", "correlation_id", "artifact_identity",
    ):
        if record[key] != request[key]:
            _error(f"result {key} does not match request")
    if record["adapter_type"] != capability["adapter_type"]:
        _error("result adapter type does not match capability")
    status = record["status"]
    error_class = record["error_class"]
    if status not in STATUS_ERROR or error_class not in STATUS_ERROR[status]:
        _error("result status and error_class are incompatible")
    outputs = _references(record["output_references"], "output_references")
    _references(record["evidence_references"], "evidence_references", nonempty=True)
    if status == "SUCCESS" and not outputs:
        _error("SUCCESS requires at least one output reference")
    if status != "SUCCESS" and outputs:
        _error("non-success result cannot claim output references")
    handoff = record["handoff_reference"]
    if handoff is not None:
        _reference(handoff, "handoff_reference", scheme="handoff")
        if "HANDOFF_REFERENCE" not in capability["produced_output_kinds"]:
            _error("result uses undeclared HANDOFF_REFERENCE output")
    _validate_usage(record["usage_counters"], request, record)
    completed = _timestamp(record["completed_at"], "completed_at")
    if completed < _timestamp(request["created_at"], "created_at"):
        _error("result predates its request")
    if completed > _timestamp(as_of, "as_of"):
        _error("result is in the future relative to as_of")
    if record != original:
        _error("result validation mutated input")
    return record


def validate_bundle(bundle: Any, *, as_of: str | None = None) -> dict[str, Any]:
    original = copy.deepcopy(bundle)
    _scan_forbidden(bundle)
    bundle = _exact(bundle, BUNDLE_FIELDS, "adapter fixture bundle")
    if bundle["schema_version"] != "1.0":
        _error("unsupported bundle schema_version")
    effective_as_of = bundle["as_of"] if as_of is None else as_of
    if bundle["as_of"] != effective_as_of:
        _error("bundle as_of differs from caller-supplied as_of")
    validate_request(bundle["request"], bundle["capability"], as_of=effective_as_of)
    if bundle["result"] is not None:
        validate_result(
            bundle["result"], bundle["request"], bundle["capability"],
            as_of=effective_as_of,
        )
        if bundle["capability"]["adapter_type"] == "FAKE":
            expected = _build_fake_result(bundle["request"], bundle["capability"], as_of=effective_as_of)
            if canonical_json(bundle["result"]) != canonical_json(expected):
                _error("FAKE result does not match its declared deterministic operation")
    if bundle != original:
        _error("bundle validation mutated input")
    return bundle


def normalize_manual_result(
    request: Any,
    capability: Any,
    supplied_result: Any,
    *,
    as_of: str,
) -> dict[str, Any]:
    if not isinstance(capability, dict) or capability.get("operation") != "NORMALIZE_MANUAL_RESULT":
        _error("manual normalization requires NORMALIZE_MANUAL_RESULT")
    validate_result(supplied_result, request, capability, as_of=as_of)
    return json.loads(canonical_json(supplied_result))


def _build_fake_result(request: dict[str, Any], capability: dict[str, Any], *, as_of: str) -> dict[str, Any]:
    operation = capability["operation"]
    if operation not in OPERATION_OUTCOME:
        _error("fake adapter requires a SIMULATE operation")
    status, error_class = OPERATION_OUTCOME[operation]
    seed = canonical_digest({"request": request, "capability": capability, "as_of": as_of})
    suffix = seed.split(":", 1)[1][:24]
    output_references = []
    if status == "SUCCESS":
        output_references = [f"fixture://007f/fake/output-{suffix}"]
    result = {
        "schema_version": "1.0",
        "result_id": f"result:{suffix}",
        "request_id": request["request_id"],
        "work_order_id": request["work_order_id"],
        "attempt_number": request["attempt_number"],
        "adapter_type": request["adapter_type"],
        "capability_id": request["capability_id"],
        "correlation_id": request["correlation_id"],
        "artifact_identity": copy.deepcopy(request["artifact_identity"]),
        "status": status,
        "output_references": output_references,
        "evidence_references": [f"evidence://adapter/{capability['capability_id']}"],
        "usage_counters": {
            "input_references": len(request["input_references"]),
            "output_references": len(output_references),
            "output_bytes": len(canonical_json(output_references).encode("utf-8")),
            "monetary_minor_units": 0,
        },
        "error_class": error_class,
        "handoff_reference": None,
        "completed_at": as_of,
    }
    return result


def run_fake(request: Any, capability: Any, *, as_of: str) -> dict[str, Any]:
    request_original = copy.deepcopy(request)
    capability_original = copy.deepcopy(capability)
    validate_request(request, capability, as_of=as_of)
    result = _build_fake_result(request, capability, as_of=as_of)
    validate_result(result, request, capability, as_of=as_of)
    if request != request_original or capability != capability_original:
        _error("fake adapter mutated input")
    return result


def load_json(path: str | Path) -> Any:
    source = Path(path)
    if source.suffix.lower() != ".json" or any(part.startswith(".") for part in source.parts):
        _error("input must be an explicit non-hidden JSON file")
    if source.stat().st_size > MAX_INPUT_BYTES:
        _error("input JSON exceeds the v1.0 size ceiling")
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _error(f"duplicate JSON key is forbidden: {key}")
            result[key] = value
        return result
    with source.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicates)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate-bundle")
    validate.add_argument("--input", required=True)
    validate.add_argument("--as-of", required=True)
    fake = sub.add_parser("run-fake")
    fake.add_argument("--input", required=True)
    fake.add_argument("--as-of", required=True)
    manual = sub.add_parser("normalize-manual")
    manual.add_argument("--input", required=True)
    manual.add_argument("--as-of", required=True)
    digest = sub.add_parser("digest")
    digest.add_argument("--input", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        bundle = load_json(args.input)
        if args.command == "validate-bundle":
            result = validate_bundle(bundle, as_of=args.as_of)
        elif args.command == "run-fake":
            validate_bundle(bundle, as_of=args.as_of)
            result = run_fake(bundle["request"], bundle["capability"], as_of=args.as_of)
        elif args.command == "normalize-manual":
            validate_bundle(bundle, as_of=args.as_of)
            if bundle["result"] is None:
                _error("manual bundle requires a supplied result")
            result = normalize_manual_result(
                bundle["request"], bundle["capability"], bundle["result"],
                as_of=args.as_of,
            )
        else:
            _scan_forbidden(bundle)
            result = {"digest": canonical_digest(bundle)}
    except (AdapterError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
