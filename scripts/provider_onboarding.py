#!/usr/bin/env python3
"""Deterministic STUDIO-009D provider-onboarding framework.

This module validates provider-neutral onboarding metadata and plans eligibility.
It does not connect to providers, resolve credentials, access secret stores,
perform network or subprocess activity, route work, use a system clock for
acceptance decisions, or authorize spend.
"""

from __future__ import annotations

import copy
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable

from scripts import connectivity_boundary as cb
from scripts import credential_redaction as cr

SCHEMA_VERSION = "1.0"
MAX_REQUEST_BYTES = 2_097_152
MAX_OUTPUT_BYTES = 2_097_152

PROFILE_STATUSES = {"CANDIDATE", "DISABLED", "ELIGIBLE", "PAUSED", "REVOKED", "EXPIRED"}
MODEL_STATUSES = {"DECLARED", "ELIGIBLE", "PAUSED", "REVOKED"}
EVIDENCE_CLASSES = {"SYNTHETIC", "REAL"}
EVENT_ACTIONS = {"REGISTER_CANDIDATE", "MARK_ELIGIBLE", "PAUSE", "REVOKE", "EXPIRE"}
CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "RESTRICTED"}

PROFILE_ID_RE = re.compile(r"^provider-profile:[a-z0-9][a-z0-9._-]{2,95}$")
MODEL_ID_RE = re.compile(r"^provider-model:[a-z0-9][a-z0-9._-]{2,95}$")
BINDING_ID_RE = re.compile(r"^provider-capability:[a-z0-9][a-z0-9._-]{2,95}$")
EVENT_ID_RE = re.compile(r"^provider-event:[a-z0-9][a-z0-9._-]{2,95}$")
CHILD_ID_RE = re.compile(r"^STUDIO-009P-[A-Z0-9][A-Z0-9-]{0,31}$")
CAPABILITY_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

PROFILE_FIELDS = {
    "schema_version", "provider_profile_id", "provider_identity_ref",
    "transport_profile_ref", "credential_profile_ref", "data_policy_ref",
    "allowed_data_classifications", "allowed_capabilities", "quota_policy_ref",
    "budget_policy_ref", "money_ceiling", "kill_switch_ref",
    "incident_response_ref", "rollback_ref", "owner_approval_ref", "status",
    "not_before", "expires_at", "as_of", "canonical_digest",
}
CHILD_FIELDS = {
    "schema_version", "child_contract_id", "provider_profile_id",
    "provider_profile_digest", "evidence_class", "owner_acceptance_ref",
    "provider_identity_evidence_ref", "transport_evidence_ref",
    "credential_profile_ref", "credential_evidence_ref",
    "model_policy_evidence_ref", "capability_evidence_ref",
    "data_export_evidence_ref", "quota_evidence_ref", "budget_evidence_ref",
    "kill_switch_evidence_ref", "incident_response_evidence_ref",
    "rollback_evidence_ref", "accepted_at", "expires_at", "revoked_at",
    "as_of", "canonical_digest",
}
MODEL_FIELDS = {
    "schema_version", "provider_model_profile_id", "provider_profile_id",
    "provider_profile_digest", "child_contract_id", "child_contract_digest",
    "model_identity_ref", "model_version_policy_ref",
    "allowed_data_classifications", "max_request_bytes", "max_output_bytes",
    "owner_approval_ref", "status", "not_before", "expires_at", "as_of",
    "canonical_digest",
}
BINDING_FIELDS = {
    "schema_version", "capability_binding_id", "provider_profile_id",
    "provider_profile_digest", "provider_model_profile_id",
    "model_profile_digest", "child_contract_id", "child_contract_digest",
    "capability_id", "allowed_data_classifications", "max_request_bytes",
    "max_output_bytes", "owner_approval_ref", "as_of", "canonical_digest",
}
EVENT_FIELDS = {
    "schema_version", "provider_onboarding_event_id", "provider_profile_id",
    "provider_profile_digest", "child_contract_id", "child_contract_digest",
    "action", "owner_approval_ref", "control_ref", "as_of",
    "canonical_digest",
}

_FORBIDDEN_SECRET_KEYS = {
    "secret", "secret_value", "credential_value", "token", "access_token",
    "refresh_token", "password", "passwd", "private_key", "api_key",
    "authorization", "cookie", "session", "session_token",
}
_SAFE_MESSAGES = {
    "EXTRA_FIELD": "input contains unknown fields",
    "MISSING_FIELD": "input is missing required fields",
    "INVALID_TYPE": "input has an invalid type",
    "INVALID_FORMAT": "input has invalid format",
    "INVALID_ENUM": "input contains an unsupported value",
    "INVALID_TIME": "input contains invalid chronology",
    "FUTURE_EVIDENCE": "evidence is later than the caller-supplied time",
    "EXPIRED_PROFILE": "provider profile is expired",
    "EXPIRED_EVIDENCE": "provider child-contract evidence is expired",
    "REVOKED_PROFILE": "provider profile is revoked",
    "REVOKED_EVIDENCE": "provider child-contract evidence is revoked",
    "PAUSED_PROFILE": "provider profile is paused",
    "OWNER_APPROVAL_REQUIRED": "Owner approval evidence is required",
    "MISSING_CHILD_CONTRACT": "accepted provider child-contract evidence is required",
    "LINEAGE_MISMATCH": "provider onboarding lineage does not match accepted evidence",
    "SCOPE_BROADENING": "provider onboarding scope exceeds accepted scope",
    "NONZERO_BUDGET": "STUDIO-009D requires a zero monetary ceiling",
    "ACTIVE_FORBIDDEN": "STUDIO-009D cannot create an ACTIVE provider state",
    "SECRET_MATERIAL": "secret material is forbidden in this interface",
    "INPUT_ENCODING": "input contains invalid Unicode",
    "INPUT_NUMBER": "non-finite numbers are forbidden",
    "INPUT_SIZE": "input exceeds the accepted byte limit",
    "STRUCTURE_LIMIT": "input structure exceeds validation limits",
    "DUPLICATE_JSON_KEY": "JSON contains duplicate object keys",
    "DIGEST_FORMAT": "canonical digest has invalid format",
    "DIGEST_MISMATCH": "canonical digest does not match",
    "INPUT_MUTATION": "validator input was mutated",
    "DUPLICATE_PROVIDER": "provider identity conflicts with an existing profile",
    "UNDECLARED_CAPABILITY": "capability is not declared by the provider profile",
    "LIFECYCLE_CONFLICT": "provider lifecycle transition is not allowed",
}


class ProviderOnboardingError(ValueError):
    """Stable public error that never includes untrusted input."""

    def __init__(self, code: str) -> None:
        message = _SAFE_MESSAGES.get(code, "provider onboarding rejected")
        super().__init__(message)
        self.code = code
        self.safe_message = message


def _fail(code: str) -> None:
    raise ProviderOnboardingError(code)


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


def _walk_bounded(value: Any) -> Iterable[tuple[str | None, Any]]:
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
        value = json.loads(
            text,
            object_pairs_hook=no_duplicates,
            parse_constant=lambda _: _fail("INPUT_NUMBER"),
        )
    except ProviderOnboardingError:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        _fail("INVALID_FORMAT")
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    _preflight(value)
    return value


def _require_exact_fields(value: Any, expected: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    keys = set(value)
    if expected - keys:
        _fail("MISSING_FIELD")
    if keys - expected:
        _fail("EXTRA_FIELD")
    return value


def _require_reference(value: Any, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if (
        not isinstance(value, str)
        or not cb.REFERENCE_RE.fullmatch(value)
        or "://" in value
        or value.startswith(("http:", "https:"))
    ):
        _fail("INVALID_FORMAT")
    return value


def _require_digest(value: Any, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not cb.DIGEST_RE.fullmatch(value):
        _fail("DIGEST_FORMAT")
    return value


def _require_id(value: Any, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        _fail("INVALID_FORMAT")
    return value


def _parse_utc(value: Any) -> datetime:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        _fail("INVALID_TIME")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        _fail("INVALID_TIME")
    raise AssertionError("unreachable")


def _sorted_unique(value: Any, *, allowed: set[str] | None = None, pattern: re.Pattern[str] | None = None) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        _fail("INVALID_TYPE")
    if any(not isinstance(item, str) for item in value):
        _fail("INVALID_TYPE")
    if value != sorted(value) or len(set(value)) != len(value):
        _fail("INVALID_FORMAT")
    if allowed is not None and not set(value).issubset(allowed):
        _fail("INVALID_ENUM")
    if pattern is not None and any(not pattern.fullmatch(item) for item in value):
        _fail("INVALID_FORMAT")
    return tuple(value)


def _verify_digest(record: dict[str, Any]) -> str:
    supplied = _require_digest(record["canonical_digest"])
    expected = canonical_digest(record)
    if supplied != expected:
        _fail("DIGEST_MISMATCH")
    return expected


def _verify_immutable(value: dict[str, Any], before: bytes) -> None:
    if _canonical_bytes(value) != before:
        _fail("INPUT_MUTATION")


def _bounded_integer(value: Any, *, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not (low <= value <= high):
        _fail("INVALID_TYPE")
    return value


def validate_provider_profile(
    profile: dict[str, Any],
    *,
    existing_profiles: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate provider-neutral profile metadata without resolving a provider."""
    _preflight(profile)
    before = _canonical_bytes(copy.deepcopy(profile))
    value = _require_exact_fields(profile, PROFILE_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    profile_id = _require_id(value["provider_profile_id"], PROFILE_ID_RE)
    provider_identity_ref = _require_reference(value["provider_identity_ref"])
    transport_profile_ref = _require_reference(value["transport_profile_ref"])
    credential_profile_ref = _require_reference(value["credential_profile_ref"])
    data_policy_ref = _require_reference(value["data_policy_ref"])
    classes = _sorted_unique(value["allowed_data_classifications"], allowed=CLASSIFICATIONS)
    capabilities = _sorted_unique(value["allowed_capabilities"], pattern=CAPABILITY_RE)
    quota_policy_ref = _require_reference(value["quota_policy_ref"])
    budget_policy_ref = _require_reference(value["budget_policy_ref"])
    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    kill_switch_ref = _require_reference(value["kill_switch_ref"])
    incident_response_ref = _require_reference(value["incident_response_ref"])
    rollback_ref = _require_reference(value["rollback_ref"])
    owner_approval_ref = _require_reference(value["owner_approval_ref"])

    status = value["status"]
    if status == "ACTIVE":
        _fail("ACTIVE_FORBIDDEN")
    if status not in PROFILE_STATUSES:
        _fail("INVALID_ENUM")

    not_before = _parse_utc(value["not_before"])
    expires_at = _parse_utc(value["expires_at"])
    as_of = _parse_utc(value["as_of"])
    if not_before >= expires_at:
        _fail("INVALID_TIME")
    if as_of < not_before:
        _fail("FUTURE_EVIDENCE")
    if as_of >= expires_at or status == "EXPIRED":
        _fail("EXPIRED_PROFILE")

    digest = _verify_digest(value)

    if existing_profiles is not None:
        for existing in existing_profiles:
            if not isinstance(existing, dict):
                _fail("INVALID_TYPE")
            existing_id = existing.get("provider_profile_id")
            existing_identity = existing.get("provider_identity_ref")
            if existing_id == profile_id and canonical_digest(existing) != digest:
                _fail("DUPLICATE_PROVIDER")
            if existing_id != profile_id and existing_identity == provider_identity_ref:
                _fail("DUPLICATE_PROVIDER")

    _verify_immutable(profile, before)
    normalized = {
        "provider_profile_id": profile_id,
        "provider_identity_ref": provider_identity_ref,
        "transport_profile_ref": transport_profile_ref,
        "credential_profile_ref": credential_profile_ref,
        "data_policy_ref": data_policy_ref,
        "allowed_data_classifications": classes,
        "allowed_capabilities": capabilities,
        "quota_policy_ref": quota_policy_ref,
        "budget_policy_ref": budget_policy_ref,
        "money_ceiling": 0,
        "kill_switch_ref": kill_switch_ref,
        "incident_response_ref": incident_response_ref,
        "rollback_ref": rollback_ref,
        "owner_approval_ref": owner_approval_ref,
        "profile_status": status,
        "not_before": value["not_before"],
        "expires_at": value["expires_at"],
        "as_of": value["as_of"],
        "profile_digest": digest,
    }
    cr.assert_public_safe(normalized)
    return normalized


def validate_child_contract_evidence(
    evidence: dict[str, Any],
    *,
    normalized_profile: dict[str, Any],
) -> dict[str, Any]:
    """Validate one STUDIO-009P* evidence record against one provider profile."""
    _preflight(evidence)
    before = _canonical_bytes(copy.deepcopy(evidence))
    value = _require_exact_fields(evidence, CHILD_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    child_id = _require_id(value["child_contract_id"], CHILD_ID_RE)
    if value["provider_profile_id"] != normalized_profile["provider_profile_id"]:
        _fail("LINEAGE_MISMATCH")
    if value["provider_profile_digest"] != normalized_profile["profile_digest"]:
        _fail("LINEAGE_MISMATCH")
    _require_digest(value["provider_profile_digest"])

    evidence_class = value["evidence_class"]
    if evidence_class not in EVIDENCE_CLASSES:
        _fail("INVALID_ENUM")

    owner_acceptance_ref = _require_reference(value["owner_acceptance_ref"])
    refs = {}
    for field in (
        "provider_identity_evidence_ref", "transport_evidence_ref",
        "credential_profile_ref", "credential_evidence_ref",
        "model_policy_evidence_ref", "capability_evidence_ref",
        "data_export_evidence_ref", "quota_evidence_ref", "budget_evidence_ref",
        "kill_switch_evidence_ref", "incident_response_evidence_ref",
        "rollback_evidence_ref",
    ):
        refs[field] = _require_reference(value[field])

    if refs["credential_profile_ref"] != normalized_profile["credential_profile_ref"]:
        _fail("LINEAGE_MISMATCH")

    accepted_at = _parse_utc(value["accepted_at"])
    expires_at = _parse_utc(value["expires_at"])
    as_of = _parse_utc(value["as_of"])
    revoked_at = value["revoked_at"]
    if accepted_at >= expires_at:
        _fail("INVALID_TIME")
    if accepted_at > as_of:
        _fail("FUTURE_EVIDENCE")
    if as_of >= expires_at:
        _fail("EXPIRED_EVIDENCE")
    if revoked_at is not None:
        revoked_time = _parse_utc(revoked_at)
        if revoked_time > as_of:
            _fail("FUTURE_EVIDENCE")
        _fail("REVOKED_EVIDENCE")

    digest = _verify_digest(value)
    _verify_immutable(evidence, before)
    normalized = {
        "child_contract_id": child_id,
        "provider_profile_id": normalized_profile["provider_profile_id"],
        "provider_profile_digest": normalized_profile["profile_digest"],
        "evidence_class": evidence_class,
        "owner_acceptance_ref": owner_acceptance_ref,
        "credential_profile_ref": refs["credential_profile_ref"],
        "accepted_at": value["accepted_at"],
        "expires_at": value["expires_at"],
        "as_of": value["as_of"],
        "child_contract_digest": digest,
        **refs,
    }
    cr.assert_public_safe(normalized)
    return normalized


def validate_model_profile(
    model: dict[str, Any],
    *,
    normalized_profile: dict[str, Any],
    normalized_child: dict[str, Any],
) -> dict[str, Any]:
    _preflight(model)
    before = _canonical_bytes(copy.deepcopy(model))
    value = _require_exact_fields(model, MODEL_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    model_id = _require_id(value["provider_model_profile_id"], MODEL_ID_RE)
    if (
        value["provider_profile_id"] != normalized_profile["provider_profile_id"]
        or value["provider_profile_digest"] != normalized_profile["profile_digest"]
        or value["child_contract_id"] != normalized_child["child_contract_id"]
        or value["child_contract_digest"] != normalized_child["child_contract_digest"]
    ):
        _fail("LINEAGE_MISMATCH")
    _require_digest(value["provider_profile_digest"])
    _require_digest(value["child_contract_digest"])
    model_identity_ref = _require_reference(value["model_identity_ref"])
    model_version_policy_ref = _require_reference(value["model_version_policy_ref"])
    classes = _sorted_unique(value["allowed_data_classifications"], allowed=CLASSIFICATIONS)
    if not set(classes).issubset(set(normalized_profile["allowed_data_classifications"])):
        _fail("SCOPE_BROADENING")
    max_request = _bounded_integer(value["max_request_bytes"], low=1, high=MAX_REQUEST_BYTES)
    max_output = _bounded_integer(value["max_output_bytes"], low=1, high=MAX_OUTPUT_BYTES)
    owner_ref = _require_reference(value["owner_approval_ref"])
    if owner_ref != normalized_profile["owner_approval_ref"]:
        _fail("OWNER_APPROVAL_REQUIRED")

    status = value["status"]
    if status not in MODEL_STATUSES:
        _fail("INVALID_ENUM")
    not_before = _parse_utc(value["not_before"])
    expires_at = _parse_utc(value["expires_at"])
    as_of = _parse_utc(value["as_of"])
    if not_before >= expires_at:
        _fail("INVALID_TIME")
    if as_of < not_before:
        _fail("FUTURE_EVIDENCE")
    if as_of >= expires_at:
        _fail("EXPIRED_EVIDENCE")

    digest = _verify_digest(value)
    _verify_immutable(model, before)
    normalized = {
        "provider_model_profile_id": model_id,
        "provider_profile_id": normalized_profile["provider_profile_id"],
        "provider_profile_digest": normalized_profile["profile_digest"],
        "child_contract_id": normalized_child["child_contract_id"],
        "child_contract_digest": normalized_child["child_contract_digest"],
        "model_identity_ref": model_identity_ref,
        "model_version_policy_ref": model_version_policy_ref,
        "allowed_data_classifications": classes,
        "max_request_bytes": max_request,
        "max_output_bytes": max_output,
        "owner_approval_ref": owner_ref,
        "model_status": status,
        "not_before": value["not_before"],
        "expires_at": value["expires_at"],
        "as_of": value["as_of"],
        "model_profile_digest": digest,
    }
    cr.assert_public_safe(normalized)
    return normalized


def validate_capability_binding(
    binding: dict[str, Any],
    *,
    normalized_profile: dict[str, Any],
    normalized_child: dict[str, Any],
    normalized_model: dict[str, Any],
) -> dict[str, Any]:
    _preflight(binding)
    before = _canonical_bytes(copy.deepcopy(binding))
    value = _require_exact_fields(binding, BINDING_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    binding_id = _require_id(value["capability_binding_id"], BINDING_ID_RE)
    if (
        value["provider_profile_id"] != normalized_profile["provider_profile_id"]
        or value["provider_profile_digest"] != normalized_profile["profile_digest"]
        or value["provider_model_profile_id"] != normalized_model["provider_model_profile_id"]
        or value["model_profile_digest"] != normalized_model["model_profile_digest"]
        or value["child_contract_id"] != normalized_child["child_contract_id"]
        or value["child_contract_digest"] != normalized_child["child_contract_digest"]
    ):
        _fail("LINEAGE_MISMATCH")
    _require_digest(value["provider_profile_digest"])
    _require_digest(value["model_profile_digest"])
    _require_digest(value["child_contract_digest"])

    capability = value["capability_id"]
    if not isinstance(capability, str) or not CAPABILITY_RE.fullmatch(capability):
        _fail("INVALID_FORMAT")
    if capability not in normalized_profile["allowed_capabilities"]:
        _fail("UNDECLARED_CAPABILITY")

    classes = _sorted_unique(value["allowed_data_classifications"], allowed=CLASSIFICATIONS)
    if not set(classes).issubset(set(normalized_model["allowed_data_classifications"])):
        _fail("SCOPE_BROADENING")
    max_request = _bounded_integer(value["max_request_bytes"], low=1, high=normalized_model["max_request_bytes"])
    max_output = _bounded_integer(value["max_output_bytes"], low=1, high=normalized_model["max_output_bytes"])
    owner_ref = _require_reference(value["owner_approval_ref"])
    if owner_ref != normalized_profile["owner_approval_ref"]:
        _fail("OWNER_APPROVAL_REQUIRED")
    as_of = _parse_utc(value["as_of"])
    if as_of < _parse_utc(normalized_model["as_of"]) or as_of >= _parse_utc(normalized_model["expires_at"]):
        _fail("INVALID_TIME")

    digest = _verify_digest(value)
    _verify_immutable(binding, before)
    normalized = {
        "capability_binding_id": binding_id,
        "provider_profile_id": normalized_profile["provider_profile_id"],
        "provider_profile_digest": normalized_profile["profile_digest"],
        "provider_model_profile_id": normalized_model["provider_model_profile_id"],
        "model_profile_digest": normalized_model["model_profile_digest"],
        "child_contract_id": normalized_child["child_contract_id"],
        "child_contract_digest": normalized_child["child_contract_digest"],
        "capability_id": capability,
        "allowed_data_classifications": classes,
        "max_request_bytes": max_request,
        "max_output_bytes": max_output,
        "owner_approval_ref": owner_ref,
        "as_of": value["as_of"],
        "capability_binding_digest": digest,
    }
    cr.assert_public_safe(normalized)
    return normalized


@dataclass(frozen=True)
class EligibilityPlan:
    eligibility: str
    refusal_code: str
    provider_profile_id: str
    profile_digest: str
    child_contract_id: str | None
    child_contract_digest: str | None
    provider_model_profile_id: str | None
    model_profile_digest: str | None
    capability_binding_id: str | None
    capability_binding_digest: str | None
    as_of: str

    def to_dict(self) -> dict[str, Any]:
        result = {
            "eligibility": self.eligibility,
            "refusal_code": self.refusal_code,
            "provider_profile_id": self.provider_profile_id,
            "profile_digest": self.profile_digest,
            "child_contract_id": self.child_contract_id,
            "child_contract_digest": self.child_contract_digest,
            "provider_model_profile_id": self.provider_model_profile_id,
            "model_profile_digest": self.model_profile_digest,
            "capability_binding_id": self.capability_binding_id,
            "capability_binding_digest": self.capability_binding_digest,
            "as_of": self.as_of,
        }
        cr.assert_public_safe(result)
        return result


def plan_eligibility(
    normalized_profile: dict[str, Any],
    *,
    normalized_child: dict[str, Any] | None,
    normalized_model: dict[str, Any] | None,
    normalized_binding: dict[str, Any] | None,
    as_of: str,
) -> EligibilityPlan:
    """Plan onboarding eligibility only; never create transport or provider authority."""
    now = _parse_utc(as_of)
    base = dict(
        provider_profile_id=normalized_profile["provider_profile_id"],
        profile_digest=normalized_profile["profile_digest"],
        child_contract_id=None if normalized_child is None else normalized_child["child_contract_id"],
        child_contract_digest=None if normalized_child is None else normalized_child["child_contract_digest"],
        provider_model_profile_id=None if normalized_model is None else normalized_model["provider_model_profile_id"],
        model_profile_digest=None if normalized_model is None else normalized_model["model_profile_digest"],
        capability_binding_id=None if normalized_binding is None else normalized_binding["capability_binding_id"],
        capability_binding_digest=None if normalized_binding is None else normalized_binding["capability_binding_digest"],
        as_of=as_of,
    )

    status = normalized_profile["profile_status"]
    if status == "REVOKED":
        return EligibilityPlan("INELIGIBLE", "REVOKED_PROFILE", **base)
    if status == "PAUSED":
        return EligibilityPlan("INELIGIBLE", "PAUSED_PROFILE", **base)
    if now >= _parse_utc(normalized_profile["expires_at"]):
        return EligibilityPlan("INELIGIBLE", "EXPIRED_PROFILE", **base)
    if normalized_profile["money_ceiling"] != 0:
        return EligibilityPlan("INELIGIBLE", "NONZERO_BUDGET", **base)
    if normalized_child is None:
        return EligibilityPlan("INELIGIBLE", "MISSING_CHILD_CONTRACT", **base)
    if normalized_model is None or normalized_binding is None:
        return EligibilityPlan("INELIGIBLE", "LINEAGE_MISMATCH", **base)

    if (
        normalized_child["provider_profile_id"] != normalized_profile["provider_profile_id"]
        or normalized_child["provider_profile_digest"] != normalized_profile["profile_digest"]
        or normalized_model["provider_profile_id"] != normalized_profile["provider_profile_id"]
        or normalized_model["provider_profile_digest"] != normalized_profile["profile_digest"]
        or normalized_binding["provider_profile_id"] != normalized_profile["provider_profile_id"]
        or normalized_binding["provider_profile_digest"] != normalized_profile["profile_digest"]
        or normalized_model["child_contract_id"] != normalized_child["child_contract_id"]
        or normalized_binding["child_contract_id"] != normalized_child["child_contract_id"]
        or normalized_binding["provider_model_profile_id"] != normalized_model["provider_model_profile_id"]
        or normalized_binding["model_profile_digest"] != normalized_model["model_profile_digest"]
    ):
        return EligibilityPlan("INELIGIBLE", "LINEAGE_MISMATCH", **base)

    if now < _parse_utc(normalized_profile["as_of"]):
        return EligibilityPlan("INELIGIBLE", "FUTURE_EVIDENCE", **base)
    if now < _parse_utc(normalized_child["as_of"]) or now >= _parse_utc(normalized_child["expires_at"]):
        return EligibilityPlan("INELIGIBLE", "EXPIRED_EVIDENCE", **base)
    if now < _parse_utc(normalized_model["as_of"]) or now >= _parse_utc(normalized_model["expires_at"]):
        return EligibilityPlan("INELIGIBLE", "EXPIRED_EVIDENCE", **base)

    return EligibilityPlan("ELIGIBLE", "NONE", **base)


def normalize_onboarding_event(
    event: dict[str, Any],
    *,
    normalized_profile: dict[str, Any],
    normalized_child: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize metadata-only lifecycle evidence without changing provider authority."""
    _preflight(event)
    before = _canonical_bytes(copy.deepcopy(event))
    value = _require_exact_fields(event, EVENT_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    event_id = _require_id(value["provider_onboarding_event_id"], EVENT_ID_RE)
    if (
        value["provider_profile_id"] != normalized_profile["provider_profile_id"]
        or value["provider_profile_digest"] != normalized_profile["profile_digest"]
    ):
        _fail("LINEAGE_MISMATCH")
    _require_digest(value["provider_profile_digest"])
    action = value["action"]
    if action not in EVENT_ACTIONS:
        _fail("INVALID_ENUM")
    owner_ref = _require_reference(value["owner_approval_ref"])
    control_ref = _require_reference(value["control_ref"])
    if owner_ref != normalized_profile["owner_approval_ref"]:
        _fail("OWNER_APPROVAL_REQUIRED")

    child_id = value["child_contract_id"]
    child_digest = value["child_contract_digest"]
    if action == "REGISTER_CANDIDATE":
        if child_id is not None or child_digest is not None:
            _fail("LIFECYCLE_CONFLICT")
        if normalized_profile["profile_status"] not in {"CANDIDATE", "DISABLED"}:
            _fail("LIFECYCLE_CONFLICT")
    else:
        if normalized_child is None:
            _fail("MISSING_CHILD_CONTRACT")
        if (
            child_id != normalized_child["child_contract_id"]
            or child_digest != normalized_child["child_contract_digest"]
        ):
            _fail("LINEAGE_MISMATCH")
        _require_id(child_id, CHILD_ID_RE)
        _require_digest(child_digest)

    as_of = _parse_utc(value["as_of"])
    if as_of < _parse_utc(normalized_profile["as_of"]):
        _fail("FUTURE_EVIDENCE")
    status = normalized_profile["profile_status"]

    if action == "MARK_ELIGIBLE" and status not in {"CANDIDATE", "DISABLED", "ELIGIBLE"}:
        _fail("LIFECYCLE_CONFLICT")
    if action == "PAUSE" and status in {"REVOKED", "EXPIRED"}:
        _fail("LIFECYCLE_CONFLICT")
    if action == "REVOKE" and status == "REVOKED":
        _fail("LIFECYCLE_CONFLICT")
    if action == "EXPIRE" and as_of < _parse_utc(normalized_profile["expires_at"]):
        _fail("LIFECYCLE_CONFLICT")
    if status == "REVOKED" and action != "REVOKE":
        _fail("LIFECYCLE_CONFLICT")

    digest = _verify_digest(value)
    _verify_immutable(event, before)
    normalized = {
        "provider_onboarding_event_id": event_id,
        "provider_profile_id": normalized_profile["provider_profile_id"],
        "profile_digest": normalized_profile["profile_digest"],
        "child_contract_id": child_id,
        "child_contract_digest": child_digest,
        "action": action,
        "owner_approval_ref": owner_ref,
        "control_ref": control_ref,
        "as_of": value["as_of"],
        "event_digest": digest,
    }
    cr.assert_public_safe(normalized)
    return normalized
