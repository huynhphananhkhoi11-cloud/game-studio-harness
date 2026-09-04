#!/usr/bin/env python3
"""Deterministic STUDIO-009R connected-validation evidence validator.

Validates metadata only. It never resolves credentials or performs provider calls.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "1.0"
MAX_INPUT_BYTES = 1_048_576
MAX_STRUCTURE_DEPTH = 32
MAX_STRUCTURE_NODES = 10_000

REFERENCE_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}:[A-Za-z0-9._/-]{1,160}$")
PROFILE_ID_RE = re.compile(r"^provider-profile:[a-z0-9][a-z0-9._-]{2,95}$")
CHILD_ID_RE = re.compile(r"^STUDIO-009P-[A-Z0-9][A-Z0-9-]{0,31}$")
EVIDENCE_ID_RE = re.compile(r"^connected-validation:[a-z0-9][a-z0-9._-]{2,95}$")
CAPABILITY_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

FORBIDDEN_SECRET_KEYS = {
    "secret", "secret_value", "credential_value", "token", "access_token",
    "refresh_token", "password", "private_key", "api_key", "authorization",
    "cookie", "session",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
)

FIELDS = {
    "schema_version", "connected_validation_id", "provider_profile_id",
    "provider_child_id", "provider_model_ref", "transport_ref",
    "credential_profile_ref", "v_contract_ref", "capability_id",
    "data_classification", "max_request_bytes", "max_output_bytes",
    "request_count", "concurrency", "retry_count", "model_identity_verified",
    "transport_identity_verified", "quota_evidence_ref", "spend_amount",
    "currency", "paid_fallback_allowed", "kill_switch_evidence_ref",
    "revocation_evidence_ref", "connected_qa_ref", "connected_review_ref",
    "owner_disposition_ref", "validated_at", "as_of", "canonical_digest",
}

CONSTRAINT_FIELDS = {
    "provider_profile_id", "provider_child_id", "provider_model_ref",
    "transport_ref", "credential_profile_ref", "v_contract_ref",
    "allowed_capabilities", "max_request_bytes", "max_output_bytes",
    "max_request_count", "max_concurrency", "max_retry_count",
    "not_before", "expires_at",
}

SAFE_MESSAGES = {
    "EXTRA_FIELD": "input contains unknown fields",
    "MISSING_FIELD": "input is missing required fields",
    "INVALID_TYPE": "input has invalid type",
    "INVALID_FORMAT": "input has invalid format",
    "INVALID_TIME": "input contains invalid chronology",
    "INPUT_ENCODING": "input contains invalid Unicode",
    "INPUT_NUMBER": "non-finite numbers are forbidden",
    "INPUT_SIZE": "input exceeds the accepted byte limit",
    "STRUCTURE_LIMIT": "input structure exceeds validation limits",
    "DUPLICATE_JSON_KEY": "JSON contains duplicate object keys",
    "DIGEST_MISMATCH": "canonical digest does not match",
    "SECRET_MATERIAL": "secret material is forbidden in this interface",
    "PUBLIC_ONLY": "initial connected validation is PUBLIC/SYNTHETIC only",
    "REQUEST_LIMIT": "connected smoke exceeds request limit",
    "CONCURRENCY_LIMIT": "connected smoke concurrency must equal one",
    "RETRY_LIMIT": "automatic retry must equal zero",
    "IDENTITY_UNVERIFIED": "provider transport/model identity evidence is incomplete",
    "NONZERO_SPEND": "connected validation requires observed spend zero",
    "PAID_FALLBACK": "paid fallback is forbidden",
    "MISSING_V_CONTRACT": "provider-specific V-contract authority is required",
    "MISSING_KILL_REVOKE": "kill-switch and revocation evidence are required",
    "MISSING_CONNECTED_QA": "connected QA evidence is required",
    "MISSING_CONNECTED_REVIEW": "connected Review evidence is required",
    "MISSING_OWNER_DISPOSITION": "Owner disposition evidence is required",
    "LINEAGE_MISMATCH": "provider child/profile lineage does not match accepted constraints",
    "MODEL_TRANSPORT_MISMATCH": "provider model or transport lineage does not match accepted constraints",
    "CREDENTIAL_LINEAGE_MISMATCH": "credential lineage does not match accepted constraints",
    "V_CONTRACT_MISMATCH": "V-contract lineage does not match accepted constraints",
    "CAPABILITY_BROADENING": "connected capability exceeds accepted constraints",
    "REQUEST_OUTPUT_BROADENING": "request or output ceiling exceeds accepted constraints",
    "QUOTA_BROADENING": "request, concurrency, or retry quota exceeds accepted constraints",
    "TIME_BROADENING": "connected evidence falls outside accepted chronology",
}


class ConnectedEvidenceError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "connected evidence rejected")
        super().__init__(self.safe_message)


def _fail(code: str) -> None:
    raise ConnectedEvidenceError(code)


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except RecursionError:
        _fail("STRUCTURE_LIMIT")
    except (UnicodeEncodeError, ValueError, TypeError):
        _fail("INPUT_ENCODING")
    raise AssertionError("unreachable")


def canonical_digest(value: dict[str, Any]) -> str:
    material = copy.deepcopy(value)
    material.pop("canonical_digest", None)
    return "sha256:" + hashlib.sha256(canonical_json_bytes(material)).hexdigest()


def _walk(value: Any):
    stack = [(None, value, 0)]
    observed = 0
    while stack:
        key, child, depth = stack.pop()
        observed += 1
        if observed > MAX_STRUCTURE_NODES or depth > MAX_STRUCTURE_DEPTH:
            _fail("STRUCTURE_LIMIT")
        yield key, child
        if isinstance(child, dict):
            stack.extend((k, v, depth + 1) for k, v in reversed(list(child.items())))
        elif isinstance(child, list):
            stack.extend((None, v, depth + 1) for v in reversed(child))


def _preflight(value: Any) -> None:
    raw = canonical_json_bytes(value)
    if len(raw) > MAX_INPUT_BYTES:
        _fail("INPUT_SIZE")
    for key, child in _walk(value):
        if key is not None:
            try:
                key.encode("utf-8")
            except UnicodeEncodeError:
                _fail("INPUT_ENCODING")
            if key.casefold() in FORBIDDEN_SECRET_KEYS:
                _fail("SECRET_MATERIAL")
        if isinstance(child, str):
            try:
                child.encode("utf-8")
            except UnicodeEncodeError:
                _fail("INPUT_ENCODING")
            if any(pattern.search(child) for pattern in SECRET_PATTERNS):
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
    if len(raw) > MAX_INPUT_BYTES:
        _fail("INPUT_SIZE")

    def hook(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                _fail("DUPLICATE_JSON_KEY")
            out[key] = value
        return out

    try:
        value = json.loads(
            text, object_pairs_hook=hook, parse_constant=lambda _: _fail("INPUT_NUMBER")
        )
    except ConnectedEvidenceError:
        raise
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        _fail("INVALID_FORMAT")
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    _preflight(value)
    return value


def _exact(value: Any, fields: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    keys = set(value)
    if fields - keys:
        _fail("MISSING_FIELD")
    if keys - fields:
        _fail("EXTRA_FIELD")
    return value


def _ref(value: Any, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if (
        not isinstance(value, str)
        or not REFERENCE_RE.fullmatch(value)
        or "://" in value
    ):
        _fail("INVALID_FORMAT")
    return value


def _utc(value: Any) -> datetime:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        _fail("INVALID_TIME")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        _fail("INVALID_TIME")
    raise AssertionError("unreachable")


def _bounded_int(value: Any, *, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not (low <= value <= high):
        _fail("INVALID_TYPE")
    return value


def _validate_constraints(raw: dict[str, Any]) -> dict[str, Any]:
    value = _exact(raw, CONSTRAINT_FIELDS)
    profile_id = value["provider_profile_id"]
    child_id = value["provider_child_id"]
    if not isinstance(profile_id, str) or not PROFILE_ID_RE.fullmatch(profile_id):
        _fail("INVALID_FORMAT")
    if not isinstance(child_id, str) or not CHILD_ID_RE.fullmatch(child_id):
        _fail("INVALID_FORMAT")
    model_ref = _ref(value["provider_model_ref"])
    transport_ref = _ref(value["transport_ref"])
    credential_ref = _ref(value["credential_profile_ref"])
    v_contract_ref = _ref(value["v_contract_ref"])
    capabilities = value["allowed_capabilities"]
    if (
        not isinstance(capabilities, list)
        or not capabilities
        or capabilities != sorted(capabilities)
        or len(capabilities) != len(set(capabilities))
        or any(not isinstance(item, str) or not CAPABILITY_RE.fullmatch(item) for item in capabilities)
    ):
        _fail("INVALID_FORMAT")
    max_request_bytes = _bounded_int(value["max_request_bytes"], low=1, high=2_097_152)
    max_output_bytes = _bounded_int(value["max_output_bytes"], low=1, high=2_097_152)
    max_request_count = _bounded_int(value["max_request_count"], low=1, high=3)
    max_concurrency = _bounded_int(value["max_concurrency"], low=1, high=1)
    max_retry_count = _bounded_int(value["max_retry_count"], low=0, high=0)
    not_before = _utc(value["not_before"])
    expires_at = _utc(value["expires_at"])
    if not_before >= expires_at:
        _fail("INVALID_TIME")
    return {
        "provider_profile_id": profile_id,
        "provider_child_id": child_id,
        "provider_model_ref": model_ref,
        "transport_ref": transport_ref,
        "credential_profile_ref": credential_ref,
        "v_contract_ref": v_contract_ref,
        "allowed_capabilities": tuple(capabilities),
        "max_request_bytes": max_request_bytes,
        "max_output_bytes": max_output_bytes,
        "max_request_count": max_request_count,
        "max_concurrency": max_concurrency,
        "max_retry_count": max_retry_count,
        "not_before": not_before,
        "expires_at": expires_at,
    }


def validate_connected_validation(
    record: dict[str, Any],
    *,
    initial_smoke: bool = True,
    accepted_constraints: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _preflight(record)
    before = canonical_json_bytes(copy.deepcopy(record))
    value = _exact(record, FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_FORMAT")
    evidence_id = value["connected_validation_id"]
    profile_id = value["provider_profile_id"]
    child_id = value["provider_child_id"]
    capability_id = value["capability_id"]
    if not isinstance(evidence_id, str) or not EVIDENCE_ID_RE.fullmatch(evidence_id):
        _fail("INVALID_FORMAT")
    if not isinstance(profile_id, str) or not PROFILE_ID_RE.fullmatch(profile_id):
        _fail("INVALID_FORMAT")
    if not isinstance(child_id, str) or not CHILD_ID_RE.fullmatch(child_id):
        _fail("INVALID_FORMAT")
    if not isinstance(capability_id, str) or not CAPABILITY_RE.fullmatch(capability_id):
        _fail("INVALID_FORMAT")

    model_ref = _ref(value["provider_model_ref"])
    transport_ref = _ref(value["transport_ref"])
    credential_ref = _ref(value["credential_profile_ref"])
    v_contract_ref = _ref(value["v_contract_ref"], nullable=True)
    if v_contract_ref is None:
        _fail("MISSING_V_CONTRACT")

    if value["data_classification"] not in {"PUBLIC", "INTERNAL", "RESTRICTED"}:
        _fail("INVALID_FORMAT")
    if initial_smoke and value["data_classification"] != "PUBLIC":
        _fail("PUBLIC_ONLY")

    max_request_bytes = _bounded_int(value["max_request_bytes"], low=1, high=2_097_152)
    max_output_bytes = _bounded_int(value["max_output_bytes"], low=1, high=2_097_152)
    if isinstance(value["request_count"], bool) or not isinstance(value["request_count"], int) or not (1 <= value["request_count"] <= 3):
        _fail("REQUEST_LIMIT")
    request_count = value["request_count"]
    if value["concurrency"] != 1 or isinstance(value["concurrency"], bool):
        _fail("CONCURRENCY_LIMIT")
    if value["retry_count"] != 0 or isinstance(value["retry_count"], bool):
        _fail("RETRY_LIMIT")
    if value["model_identity_verified"] is not True or value["transport_identity_verified"] is not True:
        _fail("IDENTITY_UNVERIFIED")

    quota_ref = _ref(value["quota_evidence_ref"], nullable=True)
    if isinstance(value["spend_amount"], bool) or value["spend_amount"] != 0:
        _fail("NONZERO_SPEND")
    if not isinstance(value["currency"], str) or not re.fullmatch(r"^[A-Z]{3}$", value["currency"]):
        _fail("INVALID_FORMAT")
    if value["paid_fallback_allowed"] is not False:
        _fail("PAID_FALLBACK")

    kill_ref = _ref(value["kill_switch_evidence_ref"], nullable=True)
    revoke_ref = _ref(value["revocation_evidence_ref"], nullable=True)
    if kill_ref is None or revoke_ref is None:
        _fail("MISSING_KILL_REVOKE")
    qa_ref = _ref(value["connected_qa_ref"], nullable=True)
    if qa_ref is None:
        _fail("MISSING_CONNECTED_QA")
    review_ref = _ref(value["connected_review_ref"], nullable=True)
    if review_ref is None:
        _fail("MISSING_CONNECTED_REVIEW")
    owner_ref = _ref(value["owner_disposition_ref"], nullable=True)
    if owner_ref is None:
        _fail("MISSING_OWNER_DISPOSITION")

    validated_at = _utc(value["validated_at"])
    as_of = _utc(value["as_of"])
    if validated_at > as_of:
        _fail("INVALID_TIME")

    digest = value["canonical_digest"]
    if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
        _fail("INVALID_FORMAT")
    if digest != canonical_digest(value):
        _fail("DIGEST_MISMATCH")

    decision = "METADATA_VALID"
    if accepted_constraints is not None:
        constraints = _validate_constraints(accepted_constraints)
        if profile_id != constraints["provider_profile_id"] or child_id != constraints["provider_child_id"]:
            _fail("LINEAGE_MISMATCH")
        if model_ref != constraints["provider_model_ref"] or transport_ref != constraints["transport_ref"]:
            _fail("MODEL_TRANSPORT_MISMATCH")
        if credential_ref != constraints["credential_profile_ref"]:
            _fail("CREDENTIAL_LINEAGE_MISMATCH")
        if v_contract_ref != constraints["v_contract_ref"]:
            _fail("V_CONTRACT_MISMATCH")
        if capability_id not in constraints["allowed_capabilities"]:
            _fail("CAPABILITY_BROADENING")
        if max_request_bytes > constraints["max_request_bytes"] or max_output_bytes > constraints["max_output_bytes"]:
            _fail("REQUEST_OUTPUT_BROADENING")
        if (
            request_count > constraints["max_request_count"]
            or value["concurrency"] > constraints["max_concurrency"]
            or value["retry_count"] > constraints["max_retry_count"]
        ):
            _fail("QUOTA_BROADENING")
        if validated_at < constraints["not_before"] or as_of >= constraints["expires_at"]:
            _fail("TIME_BROADENING")
        decision = "BOUND_ACCEPTED"

    if canonical_json_bytes(record) != before:
        _fail("INVALID_FORMAT")
    return {
        "connected_validation_id": evidence_id,
        "provider_profile_id": profile_id,
        "provider_child_id": child_id,
        "provider_model_ref": model_ref,
        "transport_ref": transport_ref,
        "credential_profile_ref": credential_ref,
        "v_contract_ref": v_contract_ref,
        "capability_id": capability_id,
        "data_classification": value["data_classification"],
        "max_request_bytes": max_request_bytes,
        "max_output_bytes": max_output_bytes,
        "request_count": request_count,
        "concurrency": 1,
        "retry_count": 0,
        "spend_amount": 0,
        "quota_evidence_ref": quota_ref,
        "connected_validation_digest": digest,
        "decision": decision,
    }
