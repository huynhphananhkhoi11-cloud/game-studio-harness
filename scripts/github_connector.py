#!/usr/bin/env python3
"""Fail-closed STUDIO-009B GitHub connector core with injected transport only.

No live transport constructor exists here. The module performs planning,
response validation, and replay-safe in-memory result reuse only.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from typing import Any

from scripts import connectivity_boundary as cb
from scripts import repository_registry as rr


SCHEMA_VERSION = "1.0"
READ_OPERATIONS = {
    "READ_METADATA", "READ_TREE", "READ_BLOB", "READ_PULL_REQUEST", "READ_CHECKS",
}
WRITE_OPERATIONS = {"CREATE_BRANCH", "CREATE_OR_UPDATE_FILE", "OPEN_PULL_REQUEST"}
ALLOWED_OPERATIONS = READ_OPERATIONS | WRITE_OPERATIONS
PR_ONLY_OPERATIONS = {"OPEN_PULL_REQUEST"}
PATH_OPERATIONS = {"READ_TREE", "READ_BLOB", "CREATE_OR_UPDATE_FILE"}
PROTECTED_BRANCHES = {"main", "master", "prod", "production"}
IDEMPOTENCY_RE = re.compile(r"^idem:[A-Za-z0-9._-]{8,120}$")

OPERATION_FIELDS = {
    "schema_version",
    "repository_id",
    "repository_record_digest",
    "operation",
    "base_revision",
    "target_ref",
    "target_paths",
    "data_classification",
    "instruction_authority_path",
    "control_evidence",
    "limits",
    "idempotency_key",
    "replay",
    "as_of",
    "canonical_digest",
}
CONTROL_FIELDS = {
    "task_ref",
    "attempt_ref",
    "queue_ref",
    "dispatch_ref",
    "writer_claim_ref",
    "worktree_ref",
    "gate_ref",
    "trace_ref",
    "quota_budget_ref",
    "boundary_ref",
    "threat_assessment_ref",
    "owner_approval_ref",
}
LIMIT_FIELDS = {
    "max_payload_bytes",
    "max_files",
    "page",
    "per_page",
    "timeout_ms",
    "max_response_bytes",
}
REPLAY_FIELDS = {"issued_at", "expires_at", "prior_result_digest"}
RESULT_FIELDS = {
    "schema_version",
    "repository_id",
    "repository_record_digest",
    "operation",
    "request_digest",
    "idempotency_key",
    "base_revision",
    "resulting_revision",
    "target_ref",
    "paths",
    "status",
    "response_bytes",
    "as_of",
    "canonical_digest",
}
LIMITS = {
    "max_payload_bytes": (0, cb.MAX_INPUT_BYTES),
    "max_files": (1, 100),
    "page": (1, 1000),
    "per_page": (1, 100),
    "timeout_ms": (1, 30_000),
    "max_response_bytes": (1, 2_097_152),
}


class ConnectorValidationError(ValueError):
    """Fail-closed connector error with stable, safe code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message


def _fail(code: str, message: str) -> None:
    raise ConnectorValidationError(code, message)


def canonical_digest(value: dict[str, Any]) -> str:
    return cb.canonical_digest(value)


def _preflight(value: Any) -> None:
    try:
        cb._preflight_content(value)
    except cb.BoundaryValidationError as exc:
        raise ConnectorValidationError(exc.code, exc.safe_message) from None


def _exact(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    try:
        return cb._require_exact_fields(value, expected, label)
    except cb.BoundaryValidationError as exc:
        if label == "control_evidence" and exc.code == "MISSING_CONTROL_EVIDENCE":
            raise ConnectorValidationError("MISSING_CONTROL_EVIDENCE", exc.safe_message) from None
        raise ConnectorValidationError(exc.code, exc.safe_message) from None


def _ref(value: Any, label: str, *, nullable: bool = False) -> str | None:
    try:
        return cb._validate_reference(value, label, nullable=nullable)
    except cb.BoundaryValidationError as exc:
        raise ConnectorValidationError(exc.code, exc.safe_message) from None


def _parse_utc(value: Any, label: str):
    try:
        return cb._parse_utc(value, label)
    except cb.BoundaryValidationError as exc:
        raise ConnectorValidationError(exc.code, exc.safe_message) from None


def _validate_limits(value: Any) -> dict[str, int]:
    limits = _exact(value, LIMIT_FIELDS, "limits")
    normalized: dict[str, int] = {}
    for field, (minimum, maximum) in LIMITS.items():
        item = limits[field]
        if isinstance(item, bool) or not isinstance(item, int):
            _fail("INVALID_LIMIT", "operation limits must be integers")
        if item < minimum or item > maximum:
            _fail("LIMIT_EXCEEDED", "operation limit exceeds accepted bounds")
        normalized[field] = item
    return normalized


def _validate_paths(paths: Any, normalized_record: dict[str, Any], operation: str) -> tuple[str, ...]:
    if not isinstance(paths, list):
        _fail("INVALID_LIST", "target_paths must be a list")
    if len(paths) != len(set(paths)):
        _fail("DUPLICATE_VALUE", "target_paths contains duplicates")
    if paths != sorted(paths):
        _fail("NONCANONICAL_ORDER", "target_paths must be sorted")
    if len(paths) > 100:
        _fail("LIMIT_EXCEEDED", "target_paths exceeds the connector file bound")
    if operation in PATH_OPERATIONS and not paths:
        _fail("MISSING_PATH", "operation requires at least one target path")
    if operation not in PATH_OPERATIONS and paths:
        _fail("UNEXPECTED_PATH", "operation does not accept target paths")
    for path in paths:
        if not isinstance(path, str):
            _fail("UNSAFE_PATH", "target path must be a string")
        try:
            allowed = rr.path_is_allowed(path, normalized_record)
        except rr.RepositoryRegistryError as exc:
            raise ConnectorValidationError(exc.code, exc.safe_message) from None
        if not allowed:
            _fail("PATH_SCOPE_DENIED", "target path is outside the repository allowlist")
    return tuple(paths)


def _validate_control_evidence(
    value: Any,
    *,
    write: bool,
    record: dict[str, Any],
    boundary: dict[str, Any],
    threat_assessment: dict[str, Any],
) -> dict[str, str | None]:
    evidence = _exact(value, CONTROL_FIELDS, "control_evidence")
    nullable = {"writer_claim_ref", "worktree_ref"}
    for field in CONTROL_FIELDS:
        _ref(evidence[field], field, nullable=field in nullable)
    if write:
        if evidence["writer_claim_ref"] is None or evidence["worktree_ref"] is None:
            _fail("MISSING_CONTROL_EVIDENCE", "write operation requires writer claim and worktree evidence")
    elif evidence["writer_claim_ref"] is not None or evidence["worktree_ref"] is not None:
        _fail("UNAUTHORIZED_WRITE", "read operation cannot carry writer/worktree evidence")
    if evidence["owner_approval_ref"] != record["owner_approval_ref"]:
        _fail("OWNER_APPROVAL_REQUIRED", "operation Owner evidence does not match repository approval")
    if evidence["boundary_ref"] != boundary["boundary_id"]:
        _fail("BOUNDARY_LINEAGE", "operation boundary evidence does not match repository evidence")
    if evidence["threat_assessment_ref"] != threat_assessment["assessment_id"]:
        _fail("BOUNDARY_LINEAGE", "operation threat evidence does not match repository evidence")
    if evidence["quota_budget_ref"] != boundary["control_evidence"]["quota_budget_ref"]:
        _fail("BOUNDARY_LINEAGE", "operation zero-budget evidence does not match accepted boundary")
    if evidence["queue_ref"] != boundary["control_evidence"]["queue_ref"]:
        _fail("BOUNDARY_LINEAGE", "operation queue evidence does not match accepted boundary")
    if evidence["dispatch_ref"] != boundary["control_evidence"]["dispatch_ref"]:
        _fail("BOUNDARY_LINEAGE", "operation dispatch evidence does not match accepted boundary")
    if evidence["gate_ref"] != boundary["control_evidence"]["gate_ref"]:
        _fail("BOUNDARY_LINEAGE", "operation gate evidence does not match accepted boundary")
    if evidence["trace_ref"] != boundary["control_evidence"]["trace_ref"]:
        _fail("BOUNDARY_LINEAGE", "operation trace evidence does not match accepted boundary")
    if write:
        if evidence["writer_claim_ref"] != boundary["control_evidence"]["writer_claim_ref"]:
            _fail("BOUNDARY_LINEAGE", "operation writer evidence does not match accepted boundary")
        if evidence["worktree_ref"] != boundary["control_evidence"]["worktree_ref"]:
            _fail("BOUNDARY_LINEAGE", "operation worktree evidence does not match accepted boundary")
    return copy.deepcopy(evidence)


def _validate_replay(value: Any, *, as_of: str) -> dict[str, str | None]:
    replay = _exact(value, REPLAY_FIELDS, "replay")
    issued = _parse_utc(replay["issued_at"], "replay.issued_at")
    expires = _parse_utc(replay["expires_at"], "replay.expires_at")
    current = _parse_utc(as_of, "as_of")
    if issued > current:
        _fail("FUTURE_EVIDENCE", "idempotency evidence is later than as_of")
    if expires <= current:
        _fail("STALE_IDEMPOTENCY", "idempotency evidence is stale")
    if (expires - issued).total_seconds() > 86_400:
        _fail("REPLAY_WINDOW", "idempotency replay window exceeds one day")
    prior = replay["prior_result_digest"]
    if prior is not None and (not isinstance(prior, str) or not cb.DIGEST_RE.fullmatch(prior)):
        _fail("DIGEST_FORMAT", "prior result digest has invalid format")
    return copy.deepcopy(replay)


@dataclass(frozen=True)
class TransportPlan:
    repository_id: str
    repository_record_digest: str
    canonical_url: str
    auth_profile_ref: str
    operation: str
    base_revision: str
    target_ref: str | None
    target_paths: tuple[str, ...]
    data_classification: str
    idempotency_key: str
    max_payload_bytes: int
    max_files: int
    page: int
    per_page: int
    timeout_ms: int
    max_response_bytes: int
    as_of: str
    request_digest: str


def plan_operation(
    repository_record: dict[str, Any],
    operation_envelope: dict[str, Any],
    *,
    boundary: dict[str, Any],
    threat_assessment: dict[str, Any],
) -> TransportPlan:
    """Validate an operation and emit a frozen transport plan."""
    try:
        record = rr.validate_repository_record(
            repository_record, boundary=boundary, threat_assessment=threat_assessment
        )
    except rr.RepositoryRegistryError as exc:
        raise ConnectorValidationError(exc.code, exc.safe_message) from None
    if not rr.repository_available(record):
        _fail("REPOSITORY_DISABLED", "repository record is not active")

    _preflight(operation_envelope)
    before = cb.canonical_json_bytes(copy.deepcopy(operation_envelope))
    envelope = _exact(operation_envelope, OPERATION_FIELDS, "operation")
    if envelope["schema_version"] != SCHEMA_VERSION:
        _fail("UNSUPPORTED_SCHEMA", "unsupported GitHub operation schema version")
    if envelope["repository_id"] != record["repository_id"]:
        _fail("REPOSITORY_MISMATCH", "operation repository identity does not match registry record")
    if envelope["repository_record_digest"] != record["repository_record_digest"]:
        _fail("REGISTRY_LINEAGE", "operation repository digest does not match registry record")

    operation = envelope["operation"]
    if operation not in ALLOWED_OPERATIONS:
        _fail("UNSUPPORTED_OPERATION", "operation is not allowlisted")
    write = operation in WRITE_OPERATIONS
    if write:
        if record["record_status"] != "WRITE_ACTIVE":
            _fail("UNAUTHORIZED_WRITE", "repository is not write-active")
        if record["access_tier"] == "READ_ONLY":
            _fail("UNAUTHORIZED_WRITE", "repository access tier is read-only")
        if operation in PR_ONLY_OPERATIONS and record["access_tier"] != "PR_WRITE":
            _fail("UNAUTHORIZED_WRITE", "operation requires PR_WRITE access")

    base_revision = envelope["base_revision"]
    if not isinstance(base_revision, str) or not cb.REVISION_RE.fullmatch(base_revision):
        _fail("MUTABLE_REVISION", "operation base revision must be an immutable commit SHA")
    if base_revision != record["registration_revision"]:
        _fail("REVISION_MISMATCH", "operation base revision differs from registered immutable revision")

    target_ref = envelope["target_ref"]
    if target_ref is not None:
        try:
            target_ref = cb._validate_branch(target_ref, "target_ref")
        except cb.BoundaryValidationError as exc:
            raise ConnectorValidationError(exc.code, exc.safe_message) from None
    if write:
        if target_ref is None:
            _fail("MISSING_TARGET_REF", "write operation requires a target branch")
        if target_ref == record["default_branch"] or target_ref in PROTECTED_BRANCHES:
            _fail("DEFAULT_BRANCH_WRITE", "write to default or protected branch is denied")
        namespace = record["allowed_branch_namespace"]
        if namespace is None or not target_ref.startswith(namespace) or target_ref == namespace.rstrip("/"):
            _fail("BRANCH_SCOPE_DENIED", "target branch lies outside the approved namespace")

    target_paths = _validate_paths(envelope["target_paths"], record, operation)
    limits = _validate_limits(envelope["limits"])
    if len(target_paths) > limits["max_files"]:
        _fail("LIMIT_EXCEEDED", "target file count exceeds request limit")

    classification = envelope["data_classification"]
    if classification not in record["allowed_classifications"]:
        _fail("DATA_POLICY", "operation data classification is not allowed")

    authority = envelope["instruction_authority_path"]
    if authority is not None:
        if not isinstance(authority, str):
            _fail("AUTHORITY_SCOPE", "instruction authority path has invalid type")
        try:
            cb._validate_path(authority, "instruction_authority_path")
        except cb.BoundaryValidationError as exc:
            raise ConnectorValidationError(exc.code, exc.safe_message) from None
        if authority not in record["instruction_authority_paths"]:
            _fail("AUTHORITY_SCOPE", "instruction authority path is not accepted authority")
    _validate_control_evidence(
        envelope["control_evidence"],
        write=write,
        record=record,
        boundary=boundary,
        threat_assessment=threat_assessment,
    )

    idem = envelope["idempotency_key"]
    if not isinstance(idem, str) or not IDEMPOTENCY_RE.fullmatch(idem):
        _fail("INVALID_IDEMPOTENCY_KEY", "idempotency key has invalid format")
    _validate_replay(envelope["replay"], as_of=envelope["as_of"])
    _parse_utc(envelope["as_of"], "as_of")
    if envelope["as_of"] != repository_record["as_of"]:
        _fail("CHRONOLOGY_MISMATCH", "operation as_of must match repository record as_of")

    supplied = envelope["canonical_digest"]
    if not isinstance(supplied, str) or not cb.DIGEST_RE.fullmatch(supplied):
        _fail("DIGEST_FORMAT", "operation canonical digest has invalid format")
    expected = canonical_digest(envelope)
    if supplied != expected:
        _fail("DIGEST_MISMATCH", "operation canonical digest does not match")
    if cb.canonical_json_bytes(operation_envelope) != before:
        _fail("INPUT_MUTATION", "operation envelope input was mutated")

    return TransportPlan(
        repository_id=record["repository_id"],
        repository_record_digest=record["repository_record_digest"],
        canonical_url=record["canonical_url"],
        auth_profile_ref=record["auth_profile_ref"],
        operation=operation,
        base_revision=base_revision,
        target_ref=target_ref,
        target_paths=target_paths,
        data_classification=classification,
        idempotency_key=idem,
        max_payload_bytes=limits["max_payload_bytes"],
        max_files=limits["max_files"],
        page=limits["page"],
        per_page=limits["per_page"],
        timeout_ms=limits["timeout_ms"],
        max_response_bytes=limits["max_response_bytes"],
        as_of=envelope["as_of"],
        request_digest=expected,
    )


def normalize_result(plan: TransportPlan, raw_result: dict[str, Any]) -> dict[str, Any]:
    """Verify one bounded transport result against the frozen request plan."""
    _preflight(raw_result)
    before = cb.canonical_json_bytes(copy.deepcopy(raw_result))
    result = _exact(raw_result, RESULT_FIELDS, "github_result")
    if result["schema_version"] != SCHEMA_VERSION:
        _fail("UNSUPPORTED_SCHEMA", "unsupported GitHub result schema version")
    exact_pairs = {
        "repository_id": plan.repository_id,
        "repository_record_digest": plan.repository_record_digest,
        "operation": plan.operation,
        "request_digest": plan.request_digest,
        "idempotency_key": plan.idempotency_key,
        "base_revision": plan.base_revision,
        "target_ref": plan.target_ref,
        "as_of": plan.as_of,
    }
    for field, expected in exact_pairs.items():
        if result[field] != expected:
            _fail("RESPONSE_MISMATCH", "transport result does not match the request plan")

    if result["status"] != "OK":
        _fail("TRANSPORT_RESULT_STATUS", "transport result is not an accepted success")
    response_bytes = result["response_bytes"]
    if isinstance(response_bytes, bool) or not isinstance(response_bytes, int) or response_bytes < 0:
        _fail("INVALID_LIMIT", "response size must be a non-negative integer")
    if response_bytes > plan.max_response_bytes:
        _fail("RESPONSE_SIZE", "transport result exceeds the response size bound")

    paths = result["paths"]
    if not isinstance(paths, list) or paths != sorted(paths) or len(paths) != len(set(paths)):
        _fail("RESPONSE_MISMATCH", "transport result paths are not canonical")
    if tuple(paths) != plan.target_paths:
        _fail("RESPONSE_MISMATCH", "transport result paths differ from requested scope")

    resulting_revision = result["resulting_revision"]
    if not isinstance(resulting_revision, str) or not cb.REVISION_RE.fullmatch(resulting_revision):
        _fail("MUTABLE_REVISION", "transport result revision must be immutable")
    if plan.operation == "CREATE_OR_UPDATE_FILE" and resulting_revision == plan.base_revision:
        _fail("RESPONSE_MISMATCH", "file update result must prove a new immutable revision")
    if plan.operation in READ_OPERATIONS and resulting_revision != plan.base_revision:
        _fail("RESPONSE_MISMATCH", "read result revision must match the requested immutable revision")

    supplied = result["canonical_digest"]
    if not isinstance(supplied, str) or not cb.DIGEST_RE.fullmatch(supplied):
        _fail("DIGEST_FORMAT", "result canonical digest has invalid format")
    expected = canonical_digest(result)
    if supplied != expected:
        _fail("DIGEST_MISMATCH", "transport result canonical digest does not match")
    if cb.canonical_json_bytes(raw_result) != before:
        _fail("INPUT_MUTATION", "transport result input was mutated")

    return copy.deepcopy(result)


class DisabledGitHubConnector:
    """Connector core that only runs an injected transport object.

    It has no live transport factory and stores replay state only in memory.
    """

    def __init__(self, transport: Any) -> None:
        if transport is None or not callable(getattr(transport, "execute", None)):
            _fail("TRANSPORT_REQUIRED", "an injected transport with execute(plan) is required")
        self._transport = transport
        self._results: dict[str, tuple[str, dict[str, Any]]] = {}

    def execute(
        self,
        repository_record: dict[str, Any],
        operation_envelope: dict[str, Any],
        *,
        boundary: dict[str, Any],
        threat_assessment: dict[str, Any],
    ) -> dict[str, Any]:
        plan = plan_operation(
            repository_record,
            operation_envelope,
            boundary=boundary,
            threat_assessment=threat_assessment,
        )
        prior = self._results.get(plan.idempotency_key)
        if prior is not None:
            prior_request_digest, prior_result = prior
            if prior_request_digest != plan.request_digest:
                _fail("IDEMPOTENCY_CONFLICT", "idempotency key was previously used for another request")
            return copy.deepcopy(prior_result)

        raw = self._transport.execute(plan)
        if not isinstance(raw, dict):
            _fail("TRANSPORT_RESULT_TYPE", "injected transport must return a result object")
        normalized = normalize_result(plan, raw)
        self._results[plan.idempotency_key] = (plan.request_digest, copy.deepcopy(normalized))
        return copy.deepcopy(normalized)
