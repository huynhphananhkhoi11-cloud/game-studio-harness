#!/usr/bin/env python3
"""Deterministic STUDIO-009A integration-boundary and threat validator."""

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


SCHEMA_VERSION = "1.0"
MAX_INPUT_BYTES = 1_048_576
MAX_STRUCTURE_DEPTH = 32
MAX_STRUCTURE_NODES = 10_000
ACCESS_TIERS = {"READ_ONLY", "BRANCH_WRITE", "PR_WRITE"}
CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "RESTRICTED"}
ZONES = {
    "OWNER_CONTROL", "STUDIO_CONTROL_PLANE", "REPOSITORY_CONTENT",
    "EXECUTION_SANDBOX", "EXTERNAL_PROVIDER", "SECRET_STORE",
}
REQUIRED_THREATS = {
    "T-PROMPT-INJECTION", "T-SECRET-LEAKAGE", "T-UNAUTHORIZED-WRITE",
    "T-SUPPLY-CHAIN-EXECUTION", "T-COST-RUNAWAY", "T-DUPLICATE-WORK",
    "T-WEBHOOK-SPOOF-REPLAY", "T-PROVIDER-IDENTITY-CONFUSION",
    "T-OWNER-GATE-BYPASS",
}

BOUNDARY_FIELDS = {
    "schema_version", "boundary_id", "task_id", "created_at", "as_of",
    "repository", "data_policy", "provider_request", "control_evidence",
    "money_ceiling", "canonical_digest",
}
REPOSITORY_FIELDS = {
    "repository_id", "revision", "default_branch", "access_tier",
    "allowed_paths", "denied_paths", "auth_profile_ref",
}
DATA_POLICY_FIELDS = {
    "allowed_classifications", "instruction_authority_paths",
    "untrusted_content_default",
}
PROVIDER_REQUEST_FIELDS = {
    "capability_id", "data_classification", "provider_profile_ref",
}
CONTROL_EVIDENCE_FIELDS = {
    "queue_ref", "dispatch_ref", "writer_claim_ref", "worktree_ref",
    "gate_ref", "trace_ref", "quota_budget_ref", "adapter_ref",
    "owner_approval_ref", "threat_assessment_ref",
}
ASSESSMENT_FIELDS = {
    "schema_version", "assessment_id", "boundary_id", "boundary_digest",
    "assessed_at", "as_of", "threats", "canonical_digest",
}
THREAT_FIELDS = {
    "threat_id", "source_zone", "target_zone", "decision", "controls",
    "evidence_refs",
}

REFERENCE_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}:[A-Za-z0-9._/-]{1,160}$")
BOUNDARY_ID_RE = re.compile(r"^boundary:[a-z0-9][a-z0-9._-]{2,63}$")
ASSESSMENT_ID_RE = re.compile(r"^threat-assessment:[a-z0-9][a-z0-9._-]{2,63}$")
TASK_ID_RE = re.compile(r"^STUDIO-[0-9]{3}[A-Z]?$")
CAPABILITY_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
CONTROL_RE = re.compile(r"^C-[A-Z0-9-]{3,63}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
BRANCH_RE = re.compile(r"^[A-Za-z0-9._/-]{1,120}$")
PATH_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]+$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

SECRET_KEYS = {
    "secret", "token", "password", "passwd", "private_key", "api_key",
    "access_key", "authorization", "cookie", "session", "credential",
}
REFERENCE_KEY_EXCEPTIONS = {"auth_profile_ref", "provider_profile_ref"}
PROVIDER_IDENTITY_KEYS = {
    "provider_name", "model_name", "endpoint", "base_url", "account_id",
    "organization_id", "transport", "sdk",
}
PROMPT_INJECTION_PATTERNS = (
    "ignore previous instructions", "ignore all previous", "override contract",
    "reveal secrets", "show system prompt", "bypass owner gate",
)
SECRET_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"https?://[^/@\s]+:[^/@\s]+@"),
)
SENSITIVE_ALLOWED_ROOTS = {
    ".env", ".git", ".ssh", "secrets", "credentials", "token-cache",
    "private-keys", "browser-profile",
}
WINDOWS_RESERVED_NAMES = {
    "aux", "con", "nul", "prn",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


class BoundaryValidationError(ValueError):
    """Fail-closed error with a stable, non-secret-bearing code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message


def _fail(code: str, message: str) -> None:
    raise BoundaryValidationError(code, message)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_digest(value: dict[str, Any]) -> str:
    material = copy.deepcopy(value)
    material.pop("canonical_digest", None)
    return "sha256:" + hashlib.sha256(canonical_json_bytes(material)).hexdigest()


def _require_exact_fields(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("INVALID_TYPE", f"{label} must be an object")
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        code = "MISSING_CONTROL_EVIDENCE" if label == "control_evidence" else "MISSING_FIELD"
        _fail(code, f"{label} is missing required fields")
    if extra:
        _fail("EXTRA_FIELD", f"{label} contains unknown fields")
    return value


def _require_string(value: Any, pattern: re.Pattern[str], label: str) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        _fail("INVALID_FORMAT", f"{label} has invalid format")
    return value


def _parse_utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        _fail("INVALID_TIME", f"{label} must be second-precision UTC ending in Z")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        _fail("INVALID_TIME", f"{label} is not a real UTC timestamp")
    return parsed


def _walk(value: Any) -> Iterable[tuple[str | None, Any]]:
    stack: list[tuple[str | None, Any, int]] = [(None, value, 0)]
    observed = 0
    while stack:
        key, child, depth = stack.pop()
        observed += 1
        if observed > MAX_STRUCTURE_NODES or depth > MAX_STRUCTURE_DEPTH:
            _fail("STRUCTURE_LIMIT", "input structure exceeds validation limits")
        yield key, child
        if isinstance(child, dict):
            stack.extend((nested_key, nested, depth + 1) for nested_key, nested in reversed(list(child.items())))
        elif isinstance(child, list):
            stack.extend((None, nested, depth + 1) for nested in reversed(child))


def _preflight_content(value: Any) -> None:
    for key, child in _walk(value):
        if key is not None:
            lowered = key.lower()
            if lowered in PROVIDER_IDENTITY_KEYS:
                _fail("PROVIDER_IDENTITY", "provider-specific identity fields are forbidden")
            if key not in REFERENCE_KEY_EXCEPTIONS and any(term in lowered for term in SECRET_KEYS):
                _fail("SECRET_MATERIAL", "secret-like fields are forbidden")
        if isinstance(child, str):
            lowered_value = child.lower()
            if any(pattern in lowered_value for pattern in PROMPT_INJECTION_PATTERNS):
                _fail("PROMPT_INJECTION", "instruction-confusion content is forbidden")
            if any(pattern.search(child) for pattern in SECRET_VALUE_PATTERNS):
                _fail("SECRET_MATERIAL", "credential-bearing values are forbidden")


def _validate_reference(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    return _require_string(value, REFERENCE_RE, label)


def _validate_sorted_unique_strings(
    value: Any,
    label: str,
    *,
    allowed: set[str] | None = None,
    case_insensitive: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not value:
        _fail("INVALID_LIST", f"{label} must be a non-empty list")
    if any(not isinstance(item, str) for item in value):
        _fail("INVALID_LIST", f"{label} must contain strings")
    if len(set(value)) != len(value):
        _fail("DUPLICATE_VALUE", f"{label} contains duplicates")
    if case_insensitive and len({item.casefold() for item in value}) != len(value):
        _fail("DUPLICATE_VALUE", f"{label} contains case-alias duplicates")
    if value != sorted(value):
        _fail("NONCANONICAL_ORDER", f"{label} must be sorted")
    if allowed is not None and not set(value).issubset(allowed):
        _fail("INVALID_ENUM", f"{label} contains unsupported values")
    return value


def _validate_path(path: str, label: str, *, denied: bool = False) -> str:
    if not isinstance(path, str) or not path or len(path) > 240:
        _fail("UNSAFE_PATH", f"{label} contains an invalid path")
    if path.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", path) or "\\" in path:
        _fail("UNSAFE_PATH", f"{label} must be repository-relative POSIX paths")
    if any(ord(char) < 32 or ord(char) == 127 for char in path):
        _fail("UNSAFE_PATH", f"{label} contains control characters")
    segments = path.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        _fail("UNSAFE_PATH", f"{label} contains traversal or empty segments")
    if any(not PATH_SEGMENT_RE.fullmatch(segment) or segment.endswith((".", " ")) for segment in segments):
        _fail("UNSAFE_PATH", f"{label} contains non-portable path segments")
    if any(segment.split(".", 1)[0].casefold() in WINDOWS_RESERVED_NAMES for segment in segments):
        _fail("UNSAFE_PATH", f"{label} contains a reserved path segment")
    root = segments[0].lower()
    if not denied and root in SENSITIVE_ALLOWED_ROOTS:
        _fail("UNSAFE_PATH", f"{label} exposes a credential-bearing path")
    return path


def _path_contains(parent: str, child: str) -> bool:
    normalized_parent = parent.casefold()
    normalized_child = child.casefold()
    return normalized_child == normalized_parent or normalized_child.startswith(normalized_parent.rstrip("/") + "/")


def _validate_branch(value: Any, label: str) -> str:
    branch = _require_string(value, BRANCH_RE, label)
    if (
        branch.startswith(("/", ".")) or branch.endswith(("/", ".", ".lock"))
        or "//" in branch or ".." in branch or "@{" in branch
    ):
        _fail("INVALID_FORMAT", f"{label} is not a safe Git branch name")
    return branch


def _validate_paths(allowed_paths: Any, denied_paths: Any) -> tuple[list[str], list[str]]:
    allowed = _validate_sorted_unique_strings(allowed_paths, "allowed_paths", case_insensitive=True)
    denied = _validate_sorted_unique_strings(denied_paths, "denied_paths", case_insensitive=True)
    for path in allowed:
        _validate_path(path, "allowed_paths")
    for path in denied:
        _validate_path(path, "denied_paths", denied=True)
    for allowed_path in allowed:
        for denied_path in denied:
            if _path_contains(allowed_path, denied_path) or _path_contains(denied_path, allowed_path):
                _fail("PATH_SCOPE_OVERLAP", "allowed and denied path scopes overlap")
    return allowed, denied


def _path_is_allowed(path: str, allowed_paths: list[str]) -> bool:
    return any(_path_contains(allowed, path) for allowed in allowed_paths)


def _validate_digest(record: dict[str, Any], label: str) -> str:
    supplied = record.get("canonical_digest")
    if not isinstance(supplied, str) or not DIGEST_RE.fullmatch(supplied):
        _fail("DIGEST_FORMAT", f"{label} canonical digest has invalid format")
    expected = canonical_digest(record)
    if supplied != expected:
        _fail("DIGEST_MISMATCH", f"{label} canonical digest does not match")
    return expected


def validate_boundary(boundary: dict[str, Any]) -> dict[str, Any]:
    _preflight_content(boundary)
    before = canonical_json_bytes(copy.deepcopy(boundary))
    record = _require_exact_fields(boundary, BOUNDARY_FIELDS, "boundary")
    if record["schema_version"] != SCHEMA_VERSION:
        _fail("UNSUPPORTED_SCHEMA", "unsupported boundary schema version")
    boundary_id = _require_string(record["boundary_id"], BOUNDARY_ID_RE, "boundary_id")
    task_id = _require_string(record["task_id"], TASK_ID_RE, "task_id")
    created_at = _parse_utc(record["created_at"], "created_at")
    as_of = _parse_utc(record["as_of"], "as_of")
    if created_at > as_of:
        _fail("FUTURE_EVIDENCE", "boundary evidence is later than as_of")

    repository = _require_exact_fields(record["repository"], REPOSITORY_FIELDS, "repository")
    repository_id = _validate_reference(repository["repository_id"], "repository_id")
    _require_string(repository["revision"], REVISION_RE, "revision")
    _validate_branch(repository["default_branch"], "default_branch")
    access_tier = repository["access_tier"]
    if access_tier not in ACCESS_TIERS:
        _fail("UNAUTHORIZED_WRITE", "repository access tier is not authorized")
    allowed_paths, _ = _validate_paths(repository["allowed_paths"], repository["denied_paths"])
    _validate_reference(repository["auth_profile_ref"], "auth_profile_ref")

    data_policy = _require_exact_fields(record["data_policy"], DATA_POLICY_FIELDS, "data_policy")
    allowed_classes = _validate_sorted_unique_strings(
        data_policy["allowed_classifications"], "allowed_classifications", allowed=CLASSIFICATIONS,
    )
    authority_paths = _validate_sorted_unique_strings(
        data_policy["instruction_authority_paths"], "instruction_authority_paths",
    )
    for path in authority_paths:
        _validate_path(path, "instruction_authority_paths")
        if not _path_is_allowed(path, allowed_paths):
            _fail("AUTHORITY_SCOPE", "instruction authority lies outside allowed repository scope")
    if data_policy["untrusted_content_default"] is not True:
        _fail("PROMPT_INJECTION", "repository content must default to untrusted")

    provider = _require_exact_fields(record["provider_request"], PROVIDER_REQUEST_FIELDS, "provider_request")
    _require_string(provider["capability_id"], CAPABILITY_RE, "capability_id")
    if provider["data_classification"] not in CLASSIFICATIONS:
        _fail("INVALID_ENUM", "unsupported provider data classification")
    if provider["data_classification"] not in allowed_classes:
        _fail("DATA_POLICY", "requested data classification is not allowed")
    _validate_reference(provider["provider_profile_ref"], "provider_profile_ref")

    evidence = _require_exact_fields(record["control_evidence"], CONTROL_EVIDENCE_FIELDS, "control_evidence")
    for field in CONTROL_EVIDENCE_FIELDS - {"writer_claim_ref", "worktree_ref"}:
        _validate_reference(evidence[field], field)
    writer_ref = _validate_reference(evidence["writer_claim_ref"], "writer_claim_ref", nullable=True)
    worktree_ref = _validate_reference(evidence["worktree_ref"], "worktree_ref", nullable=True)
    if access_tier == "READ_ONLY":
        if writer_ref is not None or worktree_ref is not None:
            _fail("UNAUTHORIZED_WRITE", "read-only boundary cannot carry writer evidence")
    elif writer_ref is None or worktree_ref is None:
        _fail("MISSING_CONTROL_EVIDENCE", "write-capable boundary requires writer and worktree evidence")

    money = record["money_ceiling"]
    if isinstance(money, bool) or not isinstance(money, int) or money != 0:
        _fail("NONZERO_BUDGET", "STUDIO-009A money ceiling must be integer zero")

    digest = _validate_digest(record, "boundary")
    if canonical_json_bytes(boundary) != before:
        _fail("INPUT_MUTATION", "boundary input was mutated")
    return {
        "status": "PASS", "boundary_id": boundary_id, "task_id": task_id,
        "repository_id": repository_id, "access_tier": access_tier,
        "boundary_digest": digest, "as_of": record["as_of"],
    }


def validate_threat_assessment(assessment: dict[str, Any], *, boundary: dict[str, Any] | None = None) -> dict[str, Any]:
    _preflight_content(assessment)
    before = canonical_json_bytes(copy.deepcopy(assessment))
    record = _require_exact_fields(assessment, ASSESSMENT_FIELDS, "threat_assessment")
    if record["schema_version"] != SCHEMA_VERSION:
        _fail("UNSUPPORTED_SCHEMA", "unsupported threat-assessment schema version")
    assessment_id = _require_string(record["assessment_id"], ASSESSMENT_ID_RE, "assessment_id")
    boundary_id = _require_string(record["boundary_id"], BOUNDARY_ID_RE, "boundary_id")
    boundary_digest = _require_string(record["boundary_digest"], DIGEST_RE, "boundary_digest")
    assessed_at = _parse_utc(record["assessed_at"], "assessed_at")
    as_of = _parse_utc(record["as_of"], "as_of")
    if assessed_at > as_of:
        _fail("FUTURE_EVIDENCE", "threat assessment is later than as_of")
    threats = record["threats"]
    if not isinstance(threats, list):
        _fail("INVALID_LIST", "threats must be a list")
    observed: list[str] = []
    for item in threats:
        threat = _require_exact_fields(item, THREAT_FIELDS, "threat")
        threat_id = threat["threat_id"]
        if threat_id not in REQUIRED_THREATS:
            _fail("THREAT_SET", "unknown threat ID")
        observed.append(threat_id)
        if threat["source_zone"] not in ZONES or threat["target_zone"] not in ZONES:
            _fail("INVALID_ENUM", "unknown trust zone")
        if threat["decision"] not in {"MITIGATED", "NOT_APPLICABLE"}:
            _fail("THREAT_DECISION", "unsupported threat decision")
        controls = _validate_sorted_unique_strings(threat["controls"], "controls")
        if any(not CONTROL_RE.fullmatch(control) for control in controls):
            _fail("INVALID_FORMAT", "control ID has invalid format")
        refs = _validate_sorted_unique_strings(threat["evidence_refs"], "evidence_refs")
        for ref in refs:
            _validate_reference(ref, "evidence_ref")
    if len(set(observed)) != len(observed) or set(observed) != REQUIRED_THREATS:
        _fail("THREAT_SET", "required threats must appear exactly once")
    if observed != sorted(observed):
        _fail("NONCANONICAL_ORDER", "threats must be sorted by threat_id")

    digest = _validate_digest(record, "threat assessment")
    if boundary is not None:
        boundary_result = validate_boundary(boundary)
        if boundary_id != boundary_result["boundary_id"] or boundary_digest != boundary_result["boundary_digest"]:
            _fail("BOUNDARY_LINEAGE", "threat assessment does not match the validated boundary")
        expected_ref = boundary["control_evidence"]["threat_assessment_ref"]
        if expected_ref != assessment_id:
            _fail("BOUNDARY_LINEAGE", "boundary threat reference does not match assessment identity")
        if record["as_of"] != boundary["as_of"]:
            _fail("BOUNDARY_LINEAGE", "boundary and assessment as_of values differ")
    if canonical_json_bytes(assessment) != before:
        _fail("INPUT_MUTATION", "threat-assessment input was mutated")
    return {
        "status": "PASS", "assessment_id": assessment_id,
        "boundary_id": boundary_id, "boundary_digest": boundary_digest,
        "threat_digest": digest, "threat_count": len(threats), "as_of": record["as_of"],
    }


def validate_pair(boundary: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
    boundary_result = validate_boundary(boundary)
    threat_result = validate_threat_assessment(assessment, boundary=boundary)
    return {"status": "PASS", "boundary": boundary_result, "threat_assessment": threat_result}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            _fail("DUPLICATE_JSON_KEY", "JSON object contains duplicate keys")
        value[key] = child
    return value


def _load_json(path: str) -> dict[str, Any]:
    with Path(path).open("rb") as handle:
        raw = handle.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        _fail("INPUT_SIZE", "JSON input exceeds the accepted size limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail("INPUT_ENCODING", "JSON input must use UTF-8")
    value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(value, dict):
        _fail("INVALID_TYPE", "fixture root must be an object")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    boundary = sub.add_parser("validate-boundary")
    boundary.add_argument("boundary")
    threat = sub.add_parser("validate-threat")
    threat.add_argument("assessment")
    pair = sub.add_parser("validate-pair")
    pair.add_argument("boundary")
    pair.add_argument("assessment")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate-boundary":
            result = validate_boundary(_load_json(args.boundary))
        elif args.command == "validate-threat":
            result = validate_threat_assessment(_load_json(args.assessment))
        else:
            result = validate_pair(_load_json(args.boundary), _load_json(args.assessment))
    except (BoundaryValidationError, json.JSONDecodeError, OSError) as exc:
        if isinstance(exc, BoundaryValidationError):
            code, message = exc.code, exc.safe_message
        else:
            code, message = "INPUT_ERROR", "unable to read valid JSON input"
        print(json.dumps({"status": "FAIL", "error_code": code, "message": message}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
