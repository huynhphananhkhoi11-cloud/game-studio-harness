#!/usr/bin/env python3
"""Deterministic offline Groq adapter for STUDIO-009P-01.

This module never performs network activity, credential resolution, provider
SDK/CLI calls, tool execution, routing, or spend. It validates Groq-specific
metadata and normalizes synthetic request/response evidence only.
"""

from __future__ import annotations

import copy
import math
import re
from typing import Any, Iterable

from scripts import credential_redaction as cr
from scripts import provider_onboarding as po

PROVIDER_PROFILE_ID = "provider-profile:groq-free-gpt-oss-120b"
MODEL_PROFILE_ID = "provider-model:groq-gpt-oss-120b"
CHILD_CONTRACT_ID = "STUDIO-009P-01"
MODEL_ID = "openai/gpt-oss-120b"
MODEL_IDENTITY_REF = "model-id:openai/gpt-oss-120b"
BASE_URL = "https://api.groq.com/openai/v1"
HOST = "api.groq.com"
TRANSPORT_PROFILE_REF = "transport-profile:groq-https-openai-v1"
CREDENTIAL_PROFILE_REF = "credential-profile:groq-api-key"
DATA_POLICY_REF = "data-policy:groq-public-synthetic-zdr"
QUOTA_POLICY_REF = "quota-policy:groq-free-gpt-oss-120b"
BUDGET_POLICY_REF = "budget-policy:groq-zero"
CONNECTED_VALIDATION_AUTHORITY = "STUDIO-009V-01_ONLY"

MAX_INPUT_TOKENS = 32768
MAX_OUTPUT_TOKENS = 8192
MAX_REQUEST_BYTES = 131072
MAX_OUTPUT_BYTES = 65536
MAX_CONCURRENCY = 1
MAX_RETRIES = 0
TIMEOUT_SECONDS = 60
ALLOWED_DATA_CLASSIFICATIONS = ("PUBLIC",)
ALLOWED_CAPABILITIES = (
    "LOCAL_TOOL_REQUEST",
    "REASONING",
    "STRUCTURED_OUTPUT",
    "TEXT_GENERATION",
)

_FORBIDDEN_FIELD_NAMES = {
    "secret", "secret_value", "credential_value", "token", "access_token",
    "refresh_token", "password", "passwd", "private_key", "api_key",
    "authorization", "cookie", "session", "session_token",
}
_TOOL_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
_CALL_ID_RE = re.compile(r"^call_[A-Za-z0-9_-]{1,64}$")

_SAFE_MESSAGES = {
    "INVALID_TYPE": "Groq adapter input has an invalid type",
    "EXTRA_FIELD": "Groq adapter input contains unknown fields",
    "MISSING_FIELD": "Groq adapter input is missing required fields",
    "MODEL_NOT_ALLOWLISTED": "Groq model is not allowlisted",
    "DATA_NOT_ALLOWED": "data classification is not allowed for Groq",
    "OUTPUT_LIMIT": "requested Groq output exceeds contract ceiling",
    "INPUT_LIMIT": "estimated Groq input exceeds contract ceiling",
    "REQUEST_TOO_LARGE": "Groq request exceeds byte ceiling",
    "OUTPUT_TOO_LARGE": "synthetic Groq output exceeds byte ceiling",
    "BUILTIN_TOOL_FORBIDDEN": "Groq built-in tools are forbidden",
    "REMOTE_MCP_FORBIDDEN": "Groq remote MCP is forbidden",
    "LOCAL_TOOL_INVALID": "local tool definition is invalid",
    "LOCAL_TOOL_NOT_ALLOWED": "local tool request is not allowlisted",
    "SECRET_MATERIAL": "secret-like material is forbidden",
    "SYNTHETIC_REQUIRED": "offline Groq adapter accepts synthetic responses only",
    "RESPONSE_INVALID": "synthetic Groq response is invalid",
    "USAGE_INVALID": "synthetic Groq usage is invalid",
    "POLICY_MISMATCH": "Groq policy does not match the accepted contract",
    "CONTRACT_METADATA_INVALID": "Groq provider metadata failed generic onboarding validation",
    "NONZERO_BUDGET": "Groq monetary ceiling must remain zero",
    "PAID_PATH_FORBIDDEN": "paid Groq fallback is forbidden",
    "RATE_LIMIT_INVALID": "Groq rate-limit evidence is invalid",
}


class GroqAdapterError(ValueError):
    """Stable public error with no untrusted text."""

    def __init__(self, code: str) -> None:
        self.code = code
        self.safe_message = _SAFE_MESSAGES.get(code, "Groq adapter rejected input")
        super().__init__(self.safe_message)


def _fail(code: str) -> None:
    raise GroqAdapterError(code)


def _exact_fields(value: Any, expected: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("INVALID_TYPE")
    keys = set(value)
    if expected - keys:
        _fail("MISSING_FIELD")
    if keys - expected:
        _fail("EXTRA_FIELD")
    return value


def _walk(value: Any) -> Iterable[tuple[str | None, Any]]:
    stack: list[tuple[str | None, Any, int]] = [(None, value, 0)]
    observed = 0
    while stack:
        key, item, depth = stack.pop()
        observed += 1
        if observed > po.cb.MAX_STRUCTURE_NODES or depth > po.cb.MAX_STRUCTURE_DEPTH:
            _fail("INVALID_TYPE")
        yield key, item
        if isinstance(item, dict):
            stack.extend((k, v, depth + 1) for k, v in reversed(list(item.items())))
        elif isinstance(item, list):
            stack.extend((None, v, depth + 1) for v in reversed(item))


def _public_preflight(value: Any, *, byte_limit: int | None = None) -> None:
    try:
        raw = po.cb.canonical_json_bytes(value)
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
        _fail("INVALID_TYPE")
    if byte_limit is not None and len(raw) > byte_limit:
        _fail("REQUEST_TOO_LARGE")
    for key, item in _walk(value):
        if key is not None and key.casefold() in _FORBIDDEN_FIELD_NAMES:
            _fail("SECRET_MATERIAL")
        if isinstance(item, str) and cr.contains_secret_like(item):
            _fail("SECRET_MATERIAL")
        if isinstance(item, float) and not math.isfinite(item):
            _fail("INVALID_TYPE")


def _require_int(value: Any, low: int, high: int, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not (low <= value <= high):
        _fail(code)
    return value


def validate_static_chain(
    profile: dict[str, Any],
    child: dict[str, Any],
    model: dict[str, Any],
    transport: dict[str, Any],
    data_policy: dict[str, Any],
    quota_policy: dict[str, Any],
    budget_policy: dict[str, Any],
) -> dict[str, Any]:
    """Validate the accepted Groq contract as disabled/offline metadata."""
    snapshots = [copy.deepcopy(x) for x in (profile, child, model, transport, data_policy, quota_policy, budget_policy)]
    for value in snapshots:
        _public_preflight(value)

    try:
        normalized_profile = po.validate_provider_profile(profile)
        normalized_child = po.validate_child_contract_evidence(
            child, normalized_profile=normalized_profile
        )
        normalized_model = po.validate_model_profile(
            model,
            normalized_profile=normalized_profile,
            normalized_child=normalized_child,
        )
    except po.ProviderOnboardingError:
        _fail("CONTRACT_METADATA_INVALID")

    if (
        normalized_profile["provider_profile_id"] != PROVIDER_PROFILE_ID
        or normalized_profile["profile_status"] != "DISABLED"
        or normalized_profile["transport_profile_ref"] != TRANSPORT_PROFILE_REF
        or normalized_profile["credential_profile_ref"] != CREDENTIAL_PROFILE_REF
        or normalized_profile["data_policy_ref"] != DATA_POLICY_REF
        or normalized_profile["quota_policy_ref"] != QUOTA_POLICY_REF
        or normalized_profile["budget_policy_ref"] != BUDGET_POLICY_REF
        or tuple(normalized_profile["allowed_data_classifications"]) != ALLOWED_DATA_CLASSIFICATIONS
        or tuple(normalized_profile["allowed_capabilities"]) != ALLOWED_CAPABILITIES
    ):
        _fail("POLICY_MISMATCH")

    if normalized_profile["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if (
        normalized_child["child_contract_id"] != CHILD_CONTRACT_ID
        or normalized_child["evidence_class"] != "SYNTHETIC"
        or normalized_child["credential_profile_ref"] != CREDENTIAL_PROFILE_REF
    ):
        _fail("POLICY_MISMATCH")
    if (
        normalized_model["provider_model_profile_id"] != MODEL_PROFILE_ID
        or normalized_model["model_identity_ref"] != MODEL_IDENTITY_REF
        or normalized_model["model_status"] != "DECLARED"
        or tuple(normalized_model["allowed_data_classifications"]) != ALLOWED_DATA_CLASSIFICATIONS
        or normalized_model["max_request_bytes"] != MAX_REQUEST_BYTES
        or normalized_model["max_output_bytes"] != MAX_OUTPUT_BYTES
    ):
        _fail("MODEL_NOT_ALLOWLISTED")

    _validate_transport_policy(transport)
    _validate_data_policy(data_policy)
    _validate_quota_policy(quota_policy)
    _validate_budget_policy(budget_policy)

    result = {
        "provider_profile_id": normalized_profile["provider_profile_id"],
        "provider_profile_digest": normalized_profile["profile_digest"],
        "child_contract_id": normalized_child["child_contract_id"],
        "child_contract_digest": normalized_child["child_contract_digest"],
        "provider_model_profile_id": normalized_model["provider_model_profile_id"],
        "model_profile_digest": normalized_model["model_profile_digest"],
        "model_id": MODEL_ID,
        "provider_state": "DISABLED",
        "model_state": "DECLARED",
        "network_authority": "NONE",
        "credential_resolution_authority": "NONE",
        "money_ceiling": 0,
    }
    cr.assert_public_safe(result)

    originals = (profile, child, model, transport, data_policy, quota_policy, budget_policy)
    for original, snapshot in zip(originals, snapshots):
        if original != snapshot:
            _fail("POLICY_MISMATCH")
    return result


def _validate_transport_policy(value: dict[str, Any]) -> None:
    expected = {
        "schema_version", "transport_profile_id", "scheme", "host", "base_path",
        "canonical_base_url", "allow_redirects", "allowed_protocols", "network_activation",
    }
    v = _exact_fields(value, expected)
    if (
        v["schema_version"] != "1.0"
        or v["transport_profile_id"] != TRANSPORT_PROFILE_REF
        or v["scheme"] != "https"
        or v["host"] != HOST
        or v["base_path"] != "/openai/v1"
        or v["canonical_base_url"] != BASE_URL
        or v["allow_redirects"] is not False
        or v["allowed_protocols"] != ["HTTPS"]
        or v["network_activation"] != CONNECTED_VALIDATION_AUTHORITY
    ):
        _fail("POLICY_MISMATCH")


def _validate_data_policy(value: dict[str, Any]) -> None:
    expected = {
        "schema_version", "data_policy_id", "allowed_data_classifications",
        "denied_data_classifications", "synthetic_data_allowed",
        "zero_data_retention_required", "connected_activation",
    }
    v = _exact_fields(value, expected)
    if (
        v["schema_version"] != "1.0"
        or v["data_policy_id"] != DATA_POLICY_REF
        or v["allowed_data_classifications"] != ["PUBLIC"]
        or v["denied_data_classifications"] != ["INTERNAL", "RESTRICTED"]
        or v["synthetic_data_allowed"] is not True
        or v["zero_data_retention_required"] is not True
        or v["connected_activation"] != CONNECTED_VALIDATION_AUTHORITY
    ):
        _fail("DATA_NOT_ALLOWED")


def _validate_quota_policy(value: dict[str, Any]) -> None:
    expected = {
        "schema_version", "quota_policy_id", "provider_snapshot", "game_limits",
        "on_429", "paid_upgrade_allowed",
    }
    v = _exact_fields(value, expected)
    if v["schema_version"] != "1.0" or v["quota_policy_id"] != QUOTA_POLICY_REF:
        _fail("POLICY_MISMATCH")
    if v["provider_snapshot"] != {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000}:
        _fail("POLICY_MISMATCH")
    if v["game_limits"] != {
        "max_concurrency": 1,
        "max_retries": 0,
        "timeout_seconds": 60,
        "max_input_tokens": 32768,
        "max_output_tokens": 8192,
    }:
        _fail("POLICY_MISMATCH")
    if v["on_429"] != "FAILOVER_OR_MANUAL_FAKE":
        _fail("POLICY_MISMATCH")
    if v["paid_upgrade_allowed"] is not False:
        _fail("PAID_PATH_FORBIDDEN")


def _validate_budget_policy(value: dict[str, Any]) -> None:
    expected = {
        "schema_version", "budget_policy_id", "currency", "money_ceiling",
        "paid_plan_allowed", "auto_recharge_allowed", "payg_fallback_allowed",
        "promotional_credit_broadens_authority",
    }
    v = _exact_fields(value, expected)
    if (
        v["schema_version"] != "1.0"
        or v["budget_policy_id"] != BUDGET_POLICY_REF
        or v["currency"] != "USD"
    ):
        _fail("POLICY_MISMATCH")
    if v["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if any(
        v[name] is not False
        for name in (
            "paid_plan_allowed", "auto_recharge_allowed", "payg_fallback_allowed",
            "promotional_credit_broadens_authority",
        )
    ):
        _fail("PAID_PATH_FORBIDDEN")


def normalize_request(request: dict[str, Any]) -> dict[str, Any]:
    """Normalize one offline request plan without constructing a network request."""
    snapshot = copy.deepcopy(request)
    _public_preflight(request, byte_limit=MAX_REQUEST_BYTES)
    v = _exact_fields(
        request,
        {
            "model", "data_classification", "messages", "estimated_input_tokens",
            "max_output_tokens", "local_tools", "built_in_tools", "remote_mcp",
        },
    )
    if v["model"] != MODEL_ID:
        _fail("MODEL_NOT_ALLOWLISTED")
    if v["data_classification"] not in ALLOWED_DATA_CLASSIFICATIONS:
        _fail("DATA_NOT_ALLOWED")
    estimated = _require_int(v["estimated_input_tokens"], 0, MAX_INPUT_TOKENS, "INPUT_LIMIT")
    output_tokens = _require_int(v["max_output_tokens"], 1, MAX_OUTPUT_TOKENS, "OUTPUT_LIMIT")

    if not isinstance(v["messages"], list) or not v["messages"]:
        _fail("INVALID_TYPE")
    normalized_messages = []
    for message in v["messages"]:
        m = _exact_fields(message, {"role", "content"})
        if m["role"] not in {"system", "user", "assistant"}:
            _fail("INVALID_TYPE")
        if not isinstance(m["content"], str):
            _fail("INVALID_TYPE")
        normalized_messages.append({"role": m["role"], "content": m["content"]})

    if v["built_in_tools"] != []:
        _fail("BUILTIN_TOOL_FORBIDDEN")
    if v["remote_mcp"] != []:
        _fail("REMOTE_MCP_FORBIDDEN")
    local_tools = _normalize_tool_definitions(v["local_tools"])

    result = {
        "model": MODEL_ID,
        "data_classification": "PUBLIC",
        "messages": normalized_messages,
        "estimated_input_tokens": estimated,
        "max_output_tokens": output_tokens,
        "local_tools": local_tools,
        "built_in_tools": [],
        "remote_mcp": [],
    }
    cr.assert_public_safe(result)
    if request != snapshot:
        _fail("INVALID_TYPE")
    return result


def _normalize_tool_definitions(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) > 16:
        _fail("LOCAL_TOOL_INVALID")
    names: set[str] = set()
    result: list[dict[str, Any]] = []
    for tool in value:
        t = _exact_fields(tool, {"name", "description", "parameters"})
        if (
            not isinstance(t["name"], str)
            or not _TOOL_NAME_RE.fullmatch(t["name"])
            or t["name"] in names
            or not isinstance(t["description"], str)
            or not isinstance(t["parameters"], dict)
        ):
            _fail("LOCAL_TOOL_INVALID")
        _public_preflight(t)
        names.add(t["name"])
        result.append(copy.deepcopy(t))
    return result


def normalize_synthetic_response(response: dict[str, Any]) -> dict[str, Any]:
    """Normalize a synthetic Groq-shaped response; real provider output is rejected."""
    snapshot = copy.deepcopy(response)
    _public_preflight(response)
    v = _exact_fields(
        response, {"synthetic", "model", "output_text", "finish_reason", "usage", "tool_calls"}
    )
    if v["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    if v["model"] != MODEL_ID:
        _fail("MODEL_NOT_ALLOWLISTED")
    if not isinstance(v["output_text"], str):
        _fail("RESPONSE_INVALID")
    if len(v["output_text"].encode("utf-8")) > MAX_OUTPUT_BYTES:
        _fail("OUTPUT_TOO_LARGE")
    if v["finish_reason"] not in {"stop", "length", "tool_calls"}:
        _fail("RESPONSE_INVALID")

    usage = _exact_fields(v["usage"], {"input_tokens", "output_tokens", "total_tokens"})
    input_tokens = _require_int(usage["input_tokens"], 0, MAX_INPUT_TOKENS, "USAGE_INVALID")
    output_tokens = _require_int(usage["output_tokens"], 0, MAX_OUTPUT_TOKENS, "USAGE_INVALID")
    total_tokens = _require_int(
        usage["total_tokens"], 0, MAX_INPUT_TOKENS + MAX_OUTPUT_TOKENS, "USAGE_INVALID"
    )
    if total_tokens != input_tokens + output_tokens:
        _fail("USAGE_INVALID")

    if not isinstance(v["tool_calls"], list) or len(v["tool_calls"]) > 16:
        _fail("RESPONSE_INVALID")
    calls = []
    for call in v["tool_calls"]:
        c = _exact_fields(call, {"id", "name", "arguments"})
        if (
            not isinstance(c["id"], str)
            or not _CALL_ID_RE.fullmatch(c["id"])
            or not isinstance(c["name"], str)
            or not _TOOL_NAME_RE.fullmatch(c["name"])
            or not isinstance(c["arguments"], dict)
        ):
            _fail("RESPONSE_INVALID")
        _public_preflight(c)
        calls.append(copy.deepcopy(c))

    result = {
        "synthetic": True,
        "model": MODEL_ID,
        "output_text": v["output_text"],
        "finish_reason": v["finish_reason"],
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "tool_calls": calls,
    }
    cr.assert_public_safe(result)
    if response != snapshot:
        _fail("RESPONSE_INVALID")
    return result


def plan_local_tool_requests(
    normalized_response: dict[str, Any], allowed_tool_names: Iterable[str]
) -> list[dict[str, Any]]:
    """Return a no-execution tool plan for already-normalized synthetic output."""
    allowed = set(allowed_tool_names)
    if any(not isinstance(name, str) or not _TOOL_NAME_RE.fullmatch(name) for name in allowed):
        _fail("LOCAL_TOOL_INVALID")
    result = []
    for call in normalized_response.get("tool_calls", []):
        if call["name"] not in allowed:
            _fail("LOCAL_TOOL_NOT_ALLOWED")
        result.append({
            "id": call["id"],
            "name": call["name"],
            "arguments": copy.deepcopy(call["arguments"]),
            "execution": "NOT_EXECUTED",
        })
    cr.assert_public_safe(result)
    return result


def normalize_rate_limit_headers(headers: dict[str, Any]) -> dict[str, Any]:
    """Normalize synthetic HTTP header evidence without making an HTTP request."""
    if not isinstance(headers, dict):
        _fail("RATE_LIMIT_INVALID")
    lowered = {}
    for key, value in headers.items():
        if not isinstance(key, str) or not isinstance(value, str):
            _fail("RATE_LIMIT_INVALID")
        lowered[key.casefold()] = value

    def nonnegative_int(name: str) -> int | None:
        raw = lowered.get(name)
        if raw is None:
            return None
        if not raw.isdigit():
            _fail("RATE_LIMIT_INVALID")
        return int(raw)

    result = {
        "limit_requests_rpd": nonnegative_int("x-ratelimit-limit-requests"),
        "remaining_requests_rpd": nonnegative_int("x-ratelimit-remaining-requests"),
        "limit_tokens_tpm": nonnegative_int("x-ratelimit-limit-tokens"),
        "remaining_tokens_tpm": nonnegative_int("x-ratelimit-remaining-tokens"),
        "reset_requests": lowered.get("x-ratelimit-reset-requests"),
        "reset_tokens": lowered.get("x-ratelimit-reset-tokens"),
        "retry_after_seconds": nonnegative_int("retry-after"),
    }
    for name in ("reset_requests", "reset_tokens"):
        value = result[name]
        if value is not None and (len(value) > 64 or cr.contains_secret_like(value)):
            _fail("RATE_LIMIT_INVALID")
    if (
        result["limit_requests_rpd"] is not None
        and result["remaining_requests_rpd"] is not None
        and result["remaining_requests_rpd"] > result["limit_requests_rpd"]
    ):
        _fail("RATE_LIMIT_INVALID")
    if (
        result["limit_tokens_tpm"] is not None
        and result["remaining_tokens_tpm"] is not None
        and result["remaining_tokens_tpm"] > result["limit_tokens_tpm"]
    ):
        _fail("RATE_LIMIT_INVALID")
    cr.assert_public_safe(result)
    return result


def normalize_error(status_code: int) -> dict[str, Any]:
    if isinstance(status_code, bool) or not isinstance(status_code, int):
        _fail("INVALID_TYPE")
    if status_code == 402:
        code = "COST_REQUIRED"
    elif status_code == 429:
        code = "QUOTA_EXHAUSTED"
    elif status_code in {401, 403}:
        code = "AUTHORIZATION_FAILED"
    elif status_code == 408:
        code = "TIMEOUT"
    elif status_code == 400:
        code = "PROVIDER_REJECTED"
    elif 500 <= status_code <= 599:
        code = "PROVIDER_UNAVAILABLE"
    else:
        code = "PROVIDER_ERROR"
    return {
        "normalized_error": code,
        "retry_allowed": False,
        "paid_fallback_allowed": False,
        "money_ceiling": 0,
    }


def offline_execution_plan(request: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_request(request)
    return {
        "provider": "GROQ",
        "model": MODEL_ID,
        "normalized_request": normalized,
        "network": "DISABLED",
        "credential_resolution": "DISABLED",
        "provider_call": "DISABLED",
        "tool_execution": "DISABLED",
        "routing": "DISABLED",
        "money_ceiling": 0,
        "fallback": "MANUAL_FAKE",
    }
