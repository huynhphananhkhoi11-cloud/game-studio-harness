#!/usr/bin/env python3
"""Deterministic STUDIO-009C credential broker and fake secret lifecycle.

This module validates credential metadata, plans bounded credential leases, and
provides an injected in-memory fake store for tests. It performs no environment
credential lookup, keyring access, filesystem secret retrieval, network call,
provider call, subprocess credential retrieval, or system-clock decision.
"""

from __future__ import annotations

import copy
import json
import math
import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from scripts import connectivity_boundary as cb
from scripts import credential_redaction as cr
from scripts import repository_registry as rr
from scripts import github_connector as gc

SCHEMA_VERSION = "1.0"
MAX_LEASE_SECONDS = 3600
MAX_REPLAY_WINDOW_SECONDS = 86400

PROFILE_STATUSES = {"DISABLED", "ACTIVE", "REVOKED", "ROTATION_REQUIRED"}
SUBJECT_TYPES = {"REPOSITORY", "PROVIDER", "SERVICE"}
CREDENTIAL_CLASSES = {"REPOSITORY_AUTH", "PROVIDER_AUTH", "SERVICE_AUTH"}
EVENT_ACTIONS = {
    "DISABLE",
    "ENABLE_ELIGIBLE",
    "REVOKE",
    "ROTATION_REQUIRED",
    "LEASE_ISSUED",
    "LEASE_EXPIRED",
}
WRITE_CAPABILITIES = {
    "GITHUB_CREATE_BRANCH",
    "GITHUB_CREATE_OR_UPDATE_FILE",
    "GITHUB_OPEN_PULL_REQUEST",
}

PROFILE_ID_RE = re.compile(r"^credential-profile:[a-z0-9][a-z0-9._-]{2,95}$")
REQUEST_ID_RE = re.compile(r"^credential-request:[a-z0-9][a-z0-9._-]{2,95}$")
LEASE_ID_RE = re.compile(r"^credential-lease:[0-9a-f]{32}$")
EVENT_ID_RE = re.compile(r"^credential-event:[a-z0-9][a-z0-9._-]{2,95}$")
CAPABILITY_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
PURPOSE_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
IDEMPOTENCY_RE = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")

PROFILE_FIELDS = {
    "schema_version",
    "credential_profile_id",
    "auth_profile_ref",
    "subject_type",
    "subject_ref",
    "credential_class",
    "auth_scheme_ref",
    "secret_store_ref",
    "secret_locator_ref",
    "allowed_capabilities",
    "allowed_purposes",
    "repository_record_digest",
    "owner_approval_ref",
    "boundary_digest",
    "gate_ref",
    "trace_ref",
    "kill_switch_ref",
    "lifecycle_ref",
    "status",
    "not_before",
    "expires_at",
    "rotation_deadline",
    "max_lease_seconds",
    "as_of",
    "canonical_digest",
}

REQUEST_FIELDS = {
    "schema_version",
    "request_id",
    "credential_profile_id",
    "profile_digest",
    "task_ref",
    "attempt_ref",
    "queue_ref",
    "dispatch_ref",
    "writer_claim_ref",
    "worktree_ref",
    "gate_ref",
    "trace_ref",
    "quota_budget_ref",
    "owner_approval_ref",
    "subject_ref",
    "capability",
    "purpose",
    "repository_record_digest",
    "operation_digest",
    "requested_lease_seconds",
    "money_ceiling",
    "replay",
    "as_of",
    "canonical_digest",
}
REPLAY_FIELDS = {"idempotency_key", "issued_at", "expires_at"}

LEASE_FIELDS = {
    "schema_version",
    "credential_lease_id",
    "credential_profile_id",
    "profile_digest",
    "subject_ref",
    "capability",
    "purpose",
    "repository_record_digest",
    "operation_digest",
    "issued_at",
    "expires_at",
    "idempotency_key",
    "canonical_digest",
}

EVENT_FIELDS = {
    "schema_version",
    "credential_event_id",
    "credential_profile_id",
    "profile_digest",
    "credential_lease_id",
    "action",
    "owner_approval_ref",
    "control_ref",
    "as_of",
    "canonical_digest",
}

_FORBIDDEN_SECRET_KEYS = {
    "secret",
    "secret_value",
    "credential_value",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "private_key",
    "api_key",
    "authorization",
    "cookie",
    "session",
    "session_token",
}


class CredentialBrokerError(cr.SafeCredentialError):
    """Fail-closed STUDIO-009C validation error."""


def _fail(code: str) -> None:
    raise CredentialBrokerError(code)


def canonical_digest(value: dict[str, Any]) -> str:
    return cb.canonical_digest(value)


def _canonical_bytes(value: Any) -> bytes:
    try:
        return cb.canonical_json_bytes(value)
    except RecursionError:
        _fail("STRUCTURE_LIMIT")
    except (UnicodeEncodeError, ValueError, TypeError):
        _fail("INPUT_ENCODING")
    raise AssertionError("unreachable")


def _require_exact_fields(value: Any, expected: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    keys = set(value)
    if expected - keys:
        _fail("MISSING_FIELD")
    if keys - expected:
        _fail("EXTRA_FIELD")
    return value


def _walk_bounded(value: Any):
    stack: list[tuple[str | None, Any, int]] = [(None, value, 0)]
    observed = 0
    while stack:
        key, child, depth = stack.pop()
        observed += 1
        if observed > cb.MAX_STRUCTURE_NODES or depth > cb.MAX_STRUCTURE_DEPTH:
            _fail("STRUCTURE_LIMIT")
        yield key, child
        if isinstance(child, dict):
            stack.extend((k, v, depth + 1) for k, v in reversed(list(child.items())))
        elif isinstance(child, list):
            stack.extend((None, v, depth + 1) for v in reversed(child))


def _preflight(value: Any) -> None:
    encoded = _canonical_bytes(value)
    if len(encoded) > cb.MAX_INPUT_BYTES:
        _fail("INPUT_SIZE")
    for key, child in _walk_bounded(value):
        if key is not None:
            try:
                key.encode("utf-8")
            except UnicodeEncodeError:
                _fail("INPUT_ENCODING")
            if key.casefold() in _FORBIDDEN_SECRET_KEYS:
                _fail("SECRET_MATERIAL")
        if isinstance(child, str):
            try:
                child.encode("utf-8")
            except UnicodeEncodeError:
                _fail("INPUT_ENCODING")
            if cr.contains_secret_like(child):
                _fail("SECRET_MATERIAL")
        elif isinstance(child, float) and not math.isfinite(child):
            _fail("INPUT_NUMBER")


def load_json_document(text: str) -> dict[str, Any]:
    if not isinstance(text, str):
        _fail("INVALID_TYPE")
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        _fail("INPUT_ENCODING")
    if len(raw) > cb.MAX_INPUT_BYTES:
        _fail("INPUT_SIZE")

    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                _fail("DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    try:
        value = json.loads(text, object_pairs_hook=no_duplicates, parse_constant=lambda _: _fail("INPUT_NUMBER"))
    except CredentialBrokerError:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        _fail("INVALID_FORMAT")
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    _preflight(value)
    return value


def _require_reference(value: Any, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not cb.REFERENCE_RE.fullmatch(value):
        _fail("INVALID_FORMAT")
    return value


def _require_digest(value: Any) -> str:
    if not isinstance(value, str) or not cb.DIGEST_RE.fullmatch(value):
        _fail("DIGEST_FORMAT")
    return value


def _require_id(value: Any, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        _fail("INVALID_FORMAT")
    return value


def _parse_utc(value: Any):
    try:
        return cb._parse_utc(value, "credential_time")
    except cb.BoundaryValidationError:
        _fail("INVALID_TIME")


def _sorted_unique_enum(value: Any, pattern: re.Pattern[str]) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        _fail("INVALID_TYPE")
    if any(not isinstance(item, str) or not pattern.fullmatch(item) for item in value):
        _fail("INVALID_FORMAT")
    if value != sorted(value) or len(set(value)) != len(value):
        _fail("INVALID_FORMAT")
    return tuple(value)


def _verify_digest(record: dict[str, Any]) -> str:
    supplied = _require_digest(record["canonical_digest"])
    expected = canonical_digest(record)
    if supplied != expected:
        _fail("DIGEST_MISMATCH")
    return expected


def _verify_immutable(record: dict[str, Any], before: bytes) -> None:
    if _canonical_bytes(record) != before:
        _fail("INPUT_MUTATION")


def _validate_repository_binding(
    profile: dict[str, Any],
    repository_record: dict[str, Any] | None,
    boundary: dict[str, Any] | None,
    threat_assessment: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if profile["subject_type"] == "REPOSITORY":
        if repository_record is None or boundary is None or threat_assessment is None:
            _fail("LINEAGE_MISMATCH")
        try:
            normalized_repository = rr.validate_repository_record(
                repository_record,
                boundary=boundary,
                threat_assessment=threat_assessment,
            )
        except rr.RepositoryRegistryError:
            _fail("LINEAGE_MISMATCH")
        if (
            profile["subject_ref"] != normalized_repository.get("repository_id")
            or profile["repository_record_digest"] != normalized_repository.get("repository_record_digest")
            or profile["auth_profile_ref"] != normalized_repository.get("auth_profile_ref")
            or profile["boundary_digest"] != normalized_repository.get("boundary_digest")
        ):
            _fail("LINEAGE_MISMATCH")
        return normalized_repository
    if profile["repository_record_digest"] is not None:
        _fail("LINEAGE_MISMATCH")
    if repository_record is not None or boundary is not None or threat_assessment is not None:
        _fail("LINEAGE_MISMATCH")
    return None


def validate_credential_profile(
    profile: dict[str, Any],
    *,
    repository_record: dict[str, Any] | None = None,
    boundary: dict[str, Any] | None = None,
    threat_assessment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate exact credential-profile metadata without resolving a secret."""
    _preflight(profile)
    before = _canonical_bytes(copy.deepcopy(profile))
    value = _require_exact_fields(profile, PROFILE_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    profile_id = _require_id(value["credential_profile_id"], PROFILE_ID_RE)
    auth_profile_ref = _require_reference(value["auth_profile_ref"])
    subject_type = value["subject_type"]
    if subject_type not in SUBJECT_TYPES:
        _fail("INVALID_ENUM")
    subject_ref = _require_reference(value["subject_ref"])
    credential_class = value["credential_class"]
    if credential_class not in CREDENTIAL_CLASSES:
        _fail("INVALID_ENUM")
    expected_class = {
        "REPOSITORY": "REPOSITORY_AUTH",
        "PROVIDER": "PROVIDER_AUTH",
        "SERVICE": "SERVICE_AUTH",
    }[subject_type]
    if credential_class != expected_class:
        _fail("LINEAGE_MISMATCH")
    _require_reference(value["auth_scheme_ref"])
    _require_reference(value["secret_store_ref"])
    _require_reference(value["secret_locator_ref"])
    capabilities = _sorted_unique_enum(value["allowed_capabilities"], CAPABILITY_RE)
    purposes = _sorted_unique_enum(value["allowed_purposes"], PURPOSE_RE)

    if value["repository_record_digest"] is not None:
        _require_digest(value["repository_record_digest"])
    _require_reference(value["owner_approval_ref"])
    _require_digest(value["boundary_digest"])
    _require_reference(value["gate_ref"])
    _require_reference(value["trace_ref"])
    _require_reference(value["kill_switch_ref"])
    _require_reference(value["lifecycle_ref"])

    status = value["status"]
    if status not in PROFILE_STATUSES:
        _fail("INVALID_ENUM")

    not_before = _parse_utc(value["not_before"])
    expires_at = _parse_utc(value["expires_at"])
    rotation_deadline = _parse_utc(value["rotation_deadline"])
    as_of = _parse_utc(value["as_of"])
    if not_before >= expires_at or rotation_deadline > expires_at:
        _fail("INVALID_TIME")
    if as_of < not_before:
        _fail("FUTURE_EVIDENCE")
    if as_of >= expires_at:
        _fail("EXPIRED_PROFILE")

    max_lease = value["max_lease_seconds"]
    if isinstance(max_lease, bool) or not isinstance(max_lease, int) or not (1 <= max_lease <= MAX_LEASE_SECONDS):
        _fail("LEASE_LIMIT")

    _validate_repository_binding(value, repository_record, boundary, threat_assessment)
    digest = _verify_digest(value)
    _verify_immutable(profile, before)

    return {
        "status": "PASS",
        "credential_profile_id": profile_id,
        "auth_profile_ref": auth_profile_ref,
        "subject_type": subject_type,
        "subject_ref": subject_ref,
        "credential_class": credential_class,
        "allowed_capabilities": capabilities,
        "allowed_purposes": purposes,
        "repository_record_digest": value["repository_record_digest"],
        "owner_approval_ref": value["owner_approval_ref"],
        "boundary_digest": value["boundary_digest"],
        "gate_ref": value["gate_ref"],
        "trace_ref": value["trace_ref"],
        "kill_switch_ref": value["kill_switch_ref"],
        "lifecycle_ref": value["lifecycle_ref"],
        "profile_status": status,
        "not_before": value["not_before"],
        "expires_at": value["expires_at"],
        "rotation_deadline": value["rotation_deadline"],
        "max_lease_seconds": max_lease,
        "as_of": value["as_of"],
        "secret_store_ref": value["secret_store_ref"],
        "secret_locator_ref": value["secret_locator_ref"],
        "profile_digest": digest,
    }


def _profile_usable(normalized_profile: dict[str, Any], as_of) -> None:
    status = normalized_profile["profile_status"]
    if status == "REVOKED":
        _fail("REVOKED_PROFILE")
    if status == "ROTATION_REQUIRED":
        _fail("ROTATION_REQUIRED")
    if status != "ACTIVE":
        _fail("PROFILE_NOT_ACTIVE")
    if as_of >= _parse_utc(normalized_profile["rotation_deadline"]):
        _fail("ROTATION_REQUIRED")
    if as_of >= _parse_utc(normalized_profile["expires_at"]):
        _fail("EXPIRED_PROFILE")


def _validate_replay(replay: Any, as_of) -> tuple[str, Any, Any]:
    replay = _require_exact_fields(replay, REPLAY_FIELDS)
    key = replay["idempotency_key"]
    if not isinstance(key, str) or not IDEMPOTENCY_RE.fullmatch(key):
        _fail("REPLAY")
    issued = _parse_utc(replay["issued_at"])
    expires = _parse_utc(replay["expires_at"])
    if issued > as_of or as_of >= expires or expires <= issued:
        _fail("REPLAY")
    if (expires - issued).total_seconds() > MAX_REPLAY_WINDOW_SECONDS:
        _fail("REPLAY")
    return key, issued, expires


@dataclass(frozen=True)
class CredentialLeasePlan:
    request_digest: str
    credential_profile_id: str
    profile_digest: str
    subject_ref: str
    capability: str
    purpose: str
    repository_record_digest: str | None
    operation_digest: str | None
    secret_store_ref: str
    secret_locator_ref: str
    issued_at: str
    expires_at: str
    idempotency_key: str

    @property
    def lease_id(self) -> str:
        material = self.request_digest.removeprefix("sha256:")
        return "credential-lease:" + material[:32]


def plan_credential_lease(
    normalized_profile: dict[str, Any],
    request: dict[str, Any],
    *,
    repository_record: dict[str, Any] | None = None,
    operation_envelope: dict[str, Any] | None = None,
    boundary: dict[str, Any] | None = None,
    threat_assessment: dict[str, Any] | None = None,
) -> CredentialLeasePlan:
    """Plan one immutable lease from an already validated profile."""
    _preflight(request)
    before = _canonical_bytes(copy.deepcopy(request))
    value = _require_exact_fields(request, REQUEST_FIELDS)
    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    _require_id(value["request_id"], REQUEST_ID_RE)

    as_of = _parse_utc(value["as_of"])
    _profile_usable(normalized_profile, as_of)
    if as_of < _parse_utc(normalized_profile["as_of"]):
        _fail("FUTURE_EVIDENCE")

    if value["credential_profile_id"] != normalized_profile["credential_profile_id"]:
        _fail("LINEAGE_MISMATCH")
    if value["profile_digest"] != normalized_profile["profile_digest"]:
        _fail("LINEAGE_MISMATCH")
    _require_digest(value["profile_digest"])

    for field in (
        "task_ref", "attempt_ref", "queue_ref", "dispatch_ref", "gate_ref",
        "trace_ref", "quota_budget_ref", "owner_approval_ref", "subject_ref",
    ):
        _require_reference(value[field])
    _require_reference(value["writer_claim_ref"], nullable=True)
    _require_reference(value["worktree_ref"], nullable=True)

    if value["owner_approval_ref"] != normalized_profile["owner_approval_ref"]:
        _fail("OWNER_APPROVAL_REQUIRED")
    if value["subject_ref"] != normalized_profile["subject_ref"]:
        _fail("LINEAGE_MISMATCH")
    if value["gate_ref"] != normalized_profile["gate_ref"] or value["trace_ref"] != normalized_profile["trace_ref"]:
        _fail("LINEAGE_MISMATCH")

    capability = value["capability"]
    purpose = value["purpose"]
    if not isinstance(capability, str) or not CAPABILITY_RE.fullmatch(capability):
        _fail("INVALID_FORMAT")
    if not isinstance(purpose, str) or not PURPOSE_RE.fullmatch(purpose):
        _fail("INVALID_FORMAT")
    if capability not in normalized_profile["allowed_capabilities"]:
        _fail("SCOPE_BROADENING")
    if purpose not in normalized_profile["allowed_purposes"]:
        _fail("SCOPE_BROADENING")

    if normalized_profile["subject_type"] == "PROVIDER":
        _fail("PROVIDER_NOT_AUTHORIZED")

    if capability in WRITE_CAPABILITIES:
        if value["writer_claim_ref"] is None or value["worktree_ref"] is None:
            _fail("WRITE_EVIDENCE_REQUIRED")

    if normalized_profile["subject_type"] == "REPOSITORY":
        _require_digest(value["repository_record_digest"])
        _require_digest(value["operation_digest"])
        if value["repository_record_digest"] != normalized_profile["repository_record_digest"]:
            _fail("LINEAGE_MISMATCH")
        if repository_record is None or operation_envelope is None or boundary is None or threat_assessment is None:
            _fail("LINEAGE_MISMATCH")
        try:
            operation_plan = gc.plan_operation(
                repository_record,
                operation_envelope,
                boundary=boundary,
                threat_assessment=threat_assessment,
            )
        except gc.ConnectorValidationError:
            _fail("LINEAGE_MISMATCH")
        if (
            operation_plan.repository_id != normalized_profile["subject_ref"]
            or operation_plan.repository_record_digest != value["repository_record_digest"]
            or operation_plan.request_digest != value["operation_digest"]
            or operation_plan.as_of != value["as_of"]
            or capability != "GITHUB_" + operation_plan.operation
        ):
            _fail("LINEAGE_MISMATCH")
        operation_control = operation_envelope["control_evidence"]
        for field in (
            "task_ref", "attempt_ref", "queue_ref", "dispatch_ref",
            "writer_claim_ref", "worktree_ref", "gate_ref", "trace_ref",
            "quota_budget_ref",
        ):
            if value[field] != operation_control[field]:
                _fail("LINEAGE_MISMATCH")
    else:
        if value["repository_record_digest"] is not None or value["operation_digest"] is not None:
            _fail("LINEAGE_MISMATCH")
        if repository_record is not None or operation_envelope is not None or boundary is not None or threat_assessment is not None:
            _fail("LINEAGE_MISMATCH")

    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")

    seconds = value["requested_lease_seconds"]
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        _fail("LEASE_LIMIT")
    if not (1 <= seconds <= min(MAX_LEASE_SECONDS, normalized_profile["max_lease_seconds"])):
        _fail("LEASE_LIMIT")

    idempotency_key, _, _ = _validate_replay(value["replay"], as_of)
    digest = _verify_digest(value)
    expires = as_of + timedelta(seconds=seconds)
    profile_expiry = _parse_utc(normalized_profile["expires_at"])
    rotation_deadline = _parse_utc(normalized_profile["rotation_deadline"])
    if expires > profile_expiry or expires > rotation_deadline:
        _fail("LEASE_LIMIT")

    _verify_immutable(request, before)
    plan = CredentialLeasePlan(
        request_digest=digest,
        credential_profile_id=normalized_profile["credential_profile_id"],
        profile_digest=normalized_profile["profile_digest"],
        subject_ref=normalized_profile["subject_ref"],
        capability=capability,
        purpose=purpose,
        repository_record_digest=value["repository_record_digest"],
        operation_digest=value["operation_digest"],
        secret_store_ref=normalized_profile["secret_store_ref"],
        secret_locator_ref=normalized_profile["secret_locator_ref"],
        issued_at=value["as_of"],
        expires_at=expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
        idempotency_key=idempotency_key,
    )
    cr.assert_public_safe({
        "request_digest": plan.request_digest,
        "credential_profile_id": plan.credential_profile_id,
        "subject_ref": plan.subject_ref,
        "capability": plan.capability,
        "purpose": plan.purpose,
    })
    return plan


def normalize_lease(plan: CredentialLeasePlan) -> dict[str, Any]:
    result = {
        "schema_version": SCHEMA_VERSION,
        "credential_lease_id": plan.lease_id,
        "credential_profile_id": plan.credential_profile_id,
        "profile_digest": plan.profile_digest,
        "subject_ref": plan.subject_ref,
        "capability": plan.capability,
        "purpose": plan.purpose,
        "repository_record_digest": plan.repository_record_digest,
        "operation_digest": plan.operation_digest,
        "issued_at": plan.issued_at,
        "expires_at": plan.expires_at,
        "idempotency_key": plan.idempotency_key,
        "canonical_digest": "",
    }
    result["canonical_digest"] = canonical_digest(result)
    _require_exact_fields(result, LEASE_FIELDS)
    cr.assert_public_safe(result)
    return result


def normalize_credential_event(
    normalized_profile: dict[str, Any],
    event: dict[str, Any],
) -> dict[str, Any]:
    _preflight(event)
    before = _canonical_bytes(copy.deepcopy(event))
    value = _require_exact_fields(event, EVENT_FIELDS)
    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    _require_id(value["credential_event_id"], EVENT_ID_RE)
    if value["credential_profile_id"] != normalized_profile["credential_profile_id"]:
        _fail("LINEAGE_MISMATCH")
    if value["profile_digest"] != normalized_profile["profile_digest"]:
        _fail("LINEAGE_MISMATCH")
    if value["credential_lease_id"] is not None:
        _require_id(value["credential_lease_id"], LEASE_ID_RE)
    if value["action"] not in EVENT_ACTIONS:
        _fail("INVALID_ENUM")
    if value["action"] == "ENABLE_ELIGIBLE" and normalized_profile["profile_status"] == "REVOKED":
        _fail("LIFECYCLE_CONFLICT")
    if value["action"] in {"LEASE_ISSUED", "LEASE_EXPIRED"} and value["credential_lease_id"] is None:
        _fail("LIFECYCLE_CONFLICT")
    if value["action"] not in {"LEASE_ISSUED", "LEASE_EXPIRED"} and value["credential_lease_id"] is not None:
        _fail("LIFECYCLE_CONFLICT")
    _require_reference(value["owner_approval_ref"])
    _require_reference(value["control_ref"])
    _parse_utc(value["as_of"])
    if value["owner_approval_ref"] != normalized_profile["owner_approval_ref"]:
        _fail("OWNER_APPROVAL_REQUIRED")
    digest = _verify_digest(value)
    _verify_immutable(event, before)
    result = copy.deepcopy(value)
    result["canonical_digest"] = digest
    cr.assert_public_safe(result)
    return result


class FakeSecretStore:
    """Injected in-memory fake. Values never enter normalized broker outputs."""

    def __init__(self, entries: dict[str, Any] | None = None) -> None:
        source = entries or {}
        if not isinstance(source, dict):
            _fail("INVALID_TYPE")
        for locator_ref, synthetic_value in source.items():
            _require_reference(locator_ref)
            cr.assert_public_safe(synthetic_value)
        self._entries = copy.deepcopy(source)
        self.access_count = 0

    def resolve(self, locator_ref: str) -> Any:
        self.access_count += 1
        if locator_ref not in self._entries:
            _fail("STORE_UNAVAILABLE")
        return copy.deepcopy(self._entries[locator_ref])


class FakeCredentialBroker:
    """In-memory credential lease simulator with deterministic replay behavior."""

    def __init__(self, store: FakeSecretStore) -> None:
        if not isinstance(store, FakeSecretStore):
            _fail("INVALID_TYPE")
        self._store = store
        self._replay: dict[str, tuple[str, dict[str, Any]]] = {}
        self._profile_state: dict[str, str] = {}
        self._leases: dict[str, dict[str, Any]] = {}

    @property
    def store_access_count(self) -> int:
        return self._store.access_count

    def _set_profile_state(self, profile_id: str, state: str) -> None:
        _require_id(profile_id, PROFILE_ID_RE)
        if state not in PROFILE_STATUSES:
            _fail("INVALID_ENUM")
        current = self._profile_state.get(profile_id)
        if current == "REVOKED" and state != "REVOKED":
            _fail("LIFECYCLE_CONFLICT")
        self._profile_state[profile_id] = state

    def revoke(self, profile_id: str) -> None:
        self._set_profile_state(profile_id, "REVOKED")

    def require_rotation(self, profile_id: str) -> None:
        if self._profile_state.get(profile_id) == "REVOKED":
            _fail("LIFECYCLE_CONFLICT")
        self._set_profile_state(profile_id, "ROTATION_REQUIRED")

    def disable(self, profile_id: str) -> None:
        if self._profile_state.get(profile_id) == "REVOKED":
            _fail("LIFECYCLE_CONFLICT")
        self._set_profile_state(profile_id, "DISABLED")

    def enable_eligible(
        self,
        profile_id: str,
        fresh_owner_approval_ref: str,
        previous_owner_approval_ref: str,
    ) -> None:
        _require_reference(fresh_owner_approval_ref)
        _require_reference(previous_owner_approval_ref)
        if fresh_owner_approval_ref == previous_owner_approval_ref:
            _fail("OWNER_APPROVAL_REQUIRED")
        if self._profile_state.get(profile_id) == "REVOKED":
            _fail("LIFECYCLE_CONFLICT")
        self._profile_state[profile_id] = "ACTIVE"

    def issue(self, plan: CredentialLeasePlan) -> dict[str, Any]:
        if not isinstance(plan, CredentialLeasePlan):
            _fail("INVALID_TYPE")
        state = self._profile_state.get(plan.credential_profile_id, "ACTIVE")
        if state == "REVOKED":
            _fail("REVOKED_PROFILE")
        if state == "ROTATION_REQUIRED":
            _fail("ROTATION_REQUIRED")
        if state != "ACTIVE":
            _fail("PROFILE_NOT_ACTIVE")

        prior = self._replay.get(plan.idempotency_key)
        if prior is not None:
            prior_digest, prior_result = prior
            if prior_digest != plan.request_digest:
                _fail("IDEMPOTENCY_CONFLICT")
            return copy.deepcopy(prior_result)

        # The fake resolves a synthetic in-memory object only to prove store access.
        # It is intentionally never serialized, returned, logged, or persisted.
        self._store.resolve(plan.secret_locator_ref)

        result = normalize_lease(plan)
        self._replay[plan.idempotency_key] = (plan.request_digest, copy.deepcopy(result))
        self._leases[result["credential_lease_id"]] = copy.deepcopy(result)
        return result

    def expire_lease(self, lease_id: str, as_of: str) -> bool:
        _require_id(lease_id, LEASE_ID_RE)
        moment = _parse_utc(as_of)
        lease = self._leases.get(lease_id)
        if lease is None:
            return False
        if moment >= _parse_utc(lease["expires_at"]):
            del self._leases[lease_id]
            return True
        return False
