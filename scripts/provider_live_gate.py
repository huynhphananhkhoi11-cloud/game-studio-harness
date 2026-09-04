#!/usr/bin/env python3
"""Deterministic STUDIO-009R live-state and worker-mode gate.

Offline metadata validation only. This module performs no provider, network,
credential-store, routing, repository-write, subprocess, or Unity activity.
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

CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "RESTRICTED"}
LIVE_STATES = {
    "DISABLED", "LIVE_VALIDATION_READY", "LIVE_VALIDATED",
    "LIVE_SHADOW_WORKER", "LIVE_BOUNDED_WORKER", "ROUTING_ELIGIBLE",
    "PAUSED", "REVOKED",
}
REFERENCE_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}:[A-Za-z0-9._/-]{1,160}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
LIVE_ID_RE = re.compile(r"^provider-live-state:[a-z0-9][a-z0-9._-]{2,95}$")
PROFILE_ID_RE = re.compile(r"^provider-profile:[a-z0-9][a-z0-9._-]{2,95}$")
CHILD_ID_RE = re.compile(r"^STUDIO-009P-[A-Z0-9][A-Z0-9-]{0,31}$")
WORKER_ID_RE = re.compile(r"^worker-policy:[a-z0-9][a-z0-9._-]{2,95}$")
SAFE_PATH_RE = re.compile(
    r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$|"
    r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*/\*\*$"
)

FORBIDDEN_SECRET_KEYS = {
    "secret", "secret_value", "credential_value", "token", "access_token",
    "refresh_token", "password", "passwd", "private_key", "api_key",
    "authorization", "cookie", "session",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
)

LIVE_FIELDS = {
    "schema_version", "live_state_id", "provider_profile_id", "provider_child_id",
    "offline_merge_ref", "offline_qa_ref", "offline_review_ref",
    "offline_owner_merge_ref", "v_contract_ref", "connected_validation_ref",
    "routing_authority_ref", "state", "allowed_data_classifications",
    "money_ceiling", "paused_at", "revoked_at", "as_of", "canonical_digest",
}
WORKER_FIELDS = {
    "schema_version", "worker_policy_id", "provider_profile_id", "provider_child_id",
    "mode", "work_order_ref", "writer_claim_ref", "worktree_ref", "allowed_paths",
    "repository_write_allowed", "direct_main_write_allowed", "merge_allowed",
    "deploy_allowed", "publish_allowed", "secret_access_allowed",
    "arbitrary_tools_allowed", "local_mediation_required", "money_ceiling",
    "as_of", "canonical_digest",
}

SAFE_MESSAGES = {
    "EXTRA_FIELD": "input contains unknown fields",
    "MISSING_FIELD": "input is missing required fields",
    "INVALID_TYPE": "input has an invalid type",
    "INVALID_FORMAT": "input has invalid format",
    "INVALID_ENUM": "input contains an unsupported value",
    "INVALID_TIME": "input contains invalid chronology",
    "INPUT_ENCODING": "input contains invalid Unicode",
    "INPUT_NUMBER": "non-finite numbers are forbidden",
    "INPUT_SIZE": "input exceeds the accepted byte limit",
    "STRUCTURE_LIMIT": "input structure exceeds validation limits",
    "DUPLICATE_JSON_KEY": "JSON contains duplicate object keys",
    "DIGEST_MISMATCH": "canonical digest does not match",
    "SECRET_MATERIAL": "secret material is forbidden in this interface",
    "NONZERO_BUDGET": "live validation requires zero monetary ceiling",
    "OFFLINE_CHILD_NOT_MERGED": "offline provider lifecycle is not durably complete",
    "MISSING_QA_REVIEW_OWNER": "offline QA, Review, and Owner merge evidence are required",
    "MISSING_V_CONTRACT": "provider-specific V-contract authority is required",
    "MISSING_CONNECTED_EVIDENCE": "connected-validation evidence is required",
    "DATA_CLASS_BROADENING": "live data scope exceeds accepted provider scope",
    "ROUTING_BEFORE_009E": "routing eligibility requires later STUDIO-009E authority",
    "PAUSED_PROVIDER": "paused provider is not eligible for promotion",
    "REVOKED_PROVIDER": "revoked provider is not eligible for promotion",
    "INVALID_TRANSITION": "live-state transition skips a required gate",
    "TARGET_STATE_REQUIRED": "validated target live-state evidence is required",
    "LINEAGE_MISMATCH": "transition lineage does not match the accepted provider child/profile",
    "WORKER_AUTHORITY": "worker policy grants unauthorized authority",
    "WRITER_CLAIM_REQUIRED": "bounded worker requires Work Order, writer claim, worktree, and exact paths",
    "UNSAFE_PATH": "worker path is not a safe repository-relative path",
}


class LiveGateError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "live gate rejected")
        super().__init__(self.safe_message)


def _fail(code: str) -> None:
    raise LiveGateError(code)


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
    except LiveGateError:
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


def _utc(value: Any, *, nullable: bool = False) -> datetime | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        _fail("INVALID_TIME")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        _fail("INVALID_TIME")
    raise AssertionError("unreachable")


def _sorted_classes(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) for item in value):
        _fail("INVALID_TYPE")
    if value != sorted(value) or len(value) != len(set(value)):
        _fail("INVALID_FORMAT")
    if not set(value).issubset(CLASSIFICATIONS):
        _fail("INVALID_ENUM")
    return tuple(value)


def _verify_digest(value: dict[str, Any]) -> None:
    digest = value.get("canonical_digest")
    if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
        _fail("INVALID_FORMAT")
    if digest != canonical_digest(value):
        _fail("DIGEST_MISMATCH")


def validate_live_state(
    record: dict[str, Any],
    *,
    parent_allowed_data_classifications=None,
) -> dict[str, Any]:
    _preflight(record)
    before = canonical_json_bytes(copy.deepcopy(record))
    value = _exact(record, LIVE_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    if not isinstance(value["live_state_id"], str) or not LIVE_ID_RE.fullmatch(value["live_state_id"]):
        _fail("INVALID_FORMAT")
    if not isinstance(value["provider_profile_id"], str) or not PROFILE_ID_RE.fullmatch(value["provider_profile_id"]):
        _fail("INVALID_FORMAT")
    if not isinstance(value["provider_child_id"], str) or not CHILD_ID_RE.fullmatch(value["provider_child_id"]):
        _fail("INVALID_FORMAT")

    state = value["state"]
    if state not in LIVE_STATES:
        _fail("INVALID_ENUM")

    refs = {
        key: _ref(value[key], nullable=True)
        for key in (
            "offline_merge_ref", "offline_qa_ref", "offline_review_ref",
            "offline_owner_merge_ref", "v_contract_ref", "connected_validation_ref",
            "routing_authority_ref",
        )
    }
    classes = _sorted_classes(value["allowed_data_classifications"])
    if (
        parent_allowed_data_classifications is not None
        and not set(classes).issubset(set(parent_allowed_data_classifications))
    ):
        _fail("DATA_CLASS_BROADENING")
    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")

    as_of = _utc(value["as_of"])
    paused_at = _utc(value["paused_at"], nullable=True)
    revoked_at = _utc(value["revoked_at"], nullable=True)
    if paused_at and paused_at > as_of or revoked_at and revoked_at > as_of:
        _fail("INVALID_TIME")

    gated_states = {
        "LIVE_VALIDATION_READY", "LIVE_VALIDATED", "LIVE_SHADOW_WORKER",
        "LIVE_BOUNDED_WORKER", "ROUTING_ELIGIBLE", "PAUSED", "REVOKED",
    }
    if state in gated_states and refs["offline_merge_ref"] is None:
        _fail("OFFLINE_CHILD_NOT_MERGED")
    if state in gated_states and any(
        refs[key] is None for key in ("offline_qa_ref", "offline_review_ref", "offline_owner_merge_ref")
    ):
        _fail("MISSING_QA_REVIEW_OWNER")

    connected_states = {
        "LIVE_VALIDATED", "LIVE_SHADOW_WORKER", "LIVE_BOUNDED_WORKER", "ROUTING_ELIGIBLE",
    }
    if state in connected_states:
        if refs["v_contract_ref"] is None:
            _fail("MISSING_V_CONTRACT")
        if refs["connected_validation_ref"] is None:
            _fail("MISSING_CONNECTED_EVIDENCE")

    if state == "ROUTING_ELIGIBLE" and refs["routing_authority_ref"] is None:
        _fail("ROUTING_BEFORE_009E")
    if state == "PAUSED" and paused_at is None:
        _fail("PAUSED_PROVIDER")
    if state == "REVOKED" and revoked_at is None:
        _fail("REVOKED_PROVIDER")

    _verify_digest(value)
    if canonical_json_bytes(record) != before:
        _fail("INVALID_FORMAT")
    return {
        "live_state_id": value["live_state_id"],
        "provider_profile_id": value["provider_profile_id"],
        "provider_child_id": value["provider_child_id"],
        "state": state,
        "allowed_data_classifications": classes,
        "money_ceiling": 0,
        "live_state_digest": value["canonical_digest"],
        **refs,
    }


def validate_worker_mode_policy(record: dict[str, Any]) -> dict[str, Any]:
    _preflight(record)
    before = canonical_json_bytes(copy.deepcopy(record))
    value = _exact(record, WORKER_FIELDS)

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_ENUM")
    if not isinstance(value["worker_policy_id"], str) or not WORKER_ID_RE.fullmatch(value["worker_policy_id"]):
        _fail("INVALID_FORMAT")
    profile_id = value["provider_profile_id"]
    child_id = value["provider_child_id"]
    if not isinstance(profile_id, str) or not PROFILE_ID_RE.fullmatch(profile_id):
        _fail("INVALID_FORMAT")
    if not isinstance(child_id, str) or not CHILD_ID_RE.fullmatch(child_id):
        _fail("INVALID_FORMAT")

    mode = value["mode"]
    if mode not in {"LIVE_SHADOW_WORKER", "LIVE_BOUNDED_WORKER"}:
        _fail("INVALID_ENUM")
    for key in (
        "direct_main_write_allowed", "merge_allowed", "deploy_allowed",
        "publish_allowed", "secret_access_allowed", "arbitrary_tools_allowed",
    ):
        if value[key] is not False:
            _fail("WORKER_AUTHORITY")
    if value["local_mediation_required"] is not True:
        _fail("WORKER_AUTHORITY")
    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    _utc(value["as_of"])

    paths = value["allowed_paths"]
    if not isinstance(paths, list) or len(paths) != len(set(paths)) or paths != sorted(paths):
        _fail("INVALID_FORMAT")
    for path in paths:
        if (
            not isinstance(path, str)
            or not SAFE_PATH_RE.fullmatch(path)
            or path.startswith(("/", "../"))
            or "/../" in path
        ):
            _fail("UNSAFE_PATH")

    work_order_ref = _ref(value["work_order_ref"], nullable=True)
    writer_claim_ref = _ref(value["writer_claim_ref"], nullable=True)
    worktree_ref = _ref(value["worktree_ref"], nullable=True)
    if mode == "LIVE_SHADOW_WORKER":
        if (
            value["repository_write_allowed"] is not False
            or work_order_ref is not None
            or writer_claim_ref is not None
            or worktree_ref is not None
            or paths
        ):
            _fail("WORKER_AUTHORITY")
    else:
        if (
            value["repository_write_allowed"] is not True
            or work_order_ref is None
            or writer_claim_ref is None
            or worktree_ref is None
            or not paths
        ):
            _fail("WRITER_CLAIM_REQUIRED")

    _verify_digest(value)
    if canonical_json_bytes(record) != before:
        _fail("INVALID_FORMAT")
    return {
        "worker_policy_id": value["worker_policy_id"],
        "provider_profile_id": profile_id,
        "provider_child_id": child_id,
        "mode": mode,
        "allowed_paths": tuple(paths),
        "repository_write_allowed": value["repository_write_allowed"],
        "worker_policy_digest": value["canonical_digest"],
    }


def _require_target_state(current: dict[str, Any], target: str, target_state: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(target_state, dict) or target_state.get("state") != target:
        _fail("TARGET_STATE_REQUIRED")
    current_profile = current.get("provider_profile_id")
    current_child = current.get("provider_child_id")
    if (
        not isinstance(current_profile, str)
        or not isinstance(current_child, str)
        or target_state.get("provider_profile_id") != current_profile
        or target_state.get("provider_child_id") != current_child
    ):
        _fail("LINEAGE_MISMATCH")
    return target_state


def plan_transition(
    current: dict[str, Any],
    target: str,
    *,
    target_state: dict[str, Any] | None = None,
    connected_evidence: dict[str, Any] | None = None,
    worker_policy: dict[str, Any] | None = None,
    routing_authority: bool = False,
) -> dict[str, str]:
    if not isinstance(current, dict):
        _fail("INVALID_TYPE")
    state = current.get("state")
    if state == "REVOKED":
        _fail("REVOKED_PROVIDER")
    if state == "PAUSED":
        _fail("PAUSED_PROVIDER")

    allowed = {
        "DISABLED": {"LIVE_VALIDATION_READY", "PAUSED", "REVOKED"},
        "LIVE_VALIDATION_READY": {"LIVE_VALIDATED", "PAUSED", "REVOKED"},
        "LIVE_VALIDATED": {"LIVE_SHADOW_WORKER", "LIVE_BOUNDED_WORKER", "PAUSED", "REVOKED"},
        "LIVE_SHADOW_WORKER": {"LIVE_BOUNDED_WORKER", "PAUSED", "REVOKED"},
        "LIVE_BOUNDED_WORKER": {"ROUTING_ELIGIBLE", "PAUSED", "REVOKED"},
    }
    if target not in allowed.get(state, set()):
        _fail("INVALID_TRANSITION")

    promotion_targets = {
        "LIVE_VALIDATION_READY", "LIVE_VALIDATED",
        "LIVE_SHADOW_WORKER", "LIVE_BOUNDED_WORKER", "ROUTING_ELIGIBLE",
    }
    normalized_target = None
    if target in promotion_targets:
        normalized_target = _require_target_state(current, target, target_state)

    if target == "LIVE_VALIDATED":
        if not isinstance(connected_evidence, dict):
            _fail("MISSING_CONNECTED_EVIDENCE")
        if connected_evidence.get("decision") != "BOUND_ACCEPTED":
            _fail("MISSING_CONNECTED_EVIDENCE")
        if (
            connected_evidence.get("provider_profile_id") != current.get("provider_profile_id")
            or connected_evidence.get("provider_child_id") != current.get("provider_child_id")
        ):
            _fail("LINEAGE_MISMATCH")
        if normalized_target and connected_evidence.get("v_contract_ref") != normalized_target.get("v_contract_ref"):
            _fail("LINEAGE_MISMATCH")

    if target in {"LIVE_SHADOW_WORKER", "LIVE_BOUNDED_WORKER"}:
        if not isinstance(worker_policy, dict) or worker_policy.get("mode") != target:
            _fail("WORKER_AUTHORITY")
        if (
            worker_policy.get("provider_profile_id") != current.get("provider_profile_id")
            or worker_policy.get("provider_child_id") != current.get("provider_child_id")
        ):
            _fail("LINEAGE_MISMATCH")

    if target == "ROUTING_ELIGIBLE":
        if not routing_authority:
            _fail("ROUTING_BEFORE_009E")
        if normalized_target and normalized_target.get("routing_authority_ref") is None:
            _fail("ROUTING_BEFORE_009E")

    return {"from": state, "to": target, "decision": "ALLOWED"}
