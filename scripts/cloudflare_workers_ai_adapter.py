#!/usr/bin/env python3
"""Deterministic offline Cloudflare Workers AI adapter for STUDIO-009P-02.

No network, account discovery, credential resolution, provider SDK/CLI call,
AI Gateway, billing, storage service, tool execution, routing, or spend occurs.
"""

from __future__ import annotations

import copy
import math
import re
from typing import Any, Iterable

from scripts import credential_redaction as cr
from scripts import provider_onboarding as po

PROVIDER_PROFILE_ID = "provider-profile:cloudflare-workers-ai-free-nemotron-3-super"
MODEL_PROFILE_ID = "provider-model:cloudflare-nemotron-3-super"
CHILD_CONTRACT_ID = "STUDIO-009P-02"
MODEL_ID = "@cf/nvidia/nemotron-3-120b-a12b"
MODEL_IDENTITY_REF = "model-id:cf/nvidia/nemotron-3-120b-a12b"
HOST = "api.cloudflare.com"
BASE_PATH_TEMPLATE = "/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1"
BASE_URL_TEMPLATE = "https://api.cloudflare.com/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1"
CHAT_PATH = "/chat/completions"
TRANSPORT_PROFILE_REF = "transport-profile:cloudflare-workers-ai-https-openai-v1"
CREDENTIAL_PROFILE_REF = "credential-profile:cloudflare-workers-ai-api-token"
ACCOUNT_REF = "account-ref:cloudflare-workers-ai-owner-account"
DATA_POLICY_REF = "data-policy:cloudflare-public-synthetic-no-storage"
QUOTA_POLICY_REF = "quota-policy:cloudflare-workers-free-nemotron-3-super"
BUDGET_POLICY_REF = "budget-policy:cloudflare-zero"

MAX_INPUT_TOKENS = 16384
MAX_OUTPUT_TOKENS = 4096
MAX_REQUEST_BYTES = 65536
MAX_OUTPUT_BYTES = 32768
MAX_CONCURRENCY = 1
MAX_RETRIES = 0
TIMEOUT_SECONDS = 60
PROVIDER_FREE_NEURONS = 10000
GAME_DAILY_NEURONS = 8000
INPUT_NEURONS_PER_MILLION = 45455
OUTPUT_NEURONS_PER_MILLION = 136364
ALLOWED_DATA_CLASSIFICATIONS = ("PUBLIC",)
ALLOWED_CAPABILITIES = ("LOCAL_TOOL_REQUEST", "REASONING", "TEXT_GENERATION")

_FORBIDDEN_FIELD_NAMES = {
    "secret", "secret_value", "credential_value", "token", "access_token",
    "refresh_token", "password", "passwd", "private_key", "api_key",
    "authorization", "cookie", "session", "session_token", "account_id",
    "raw_account_id", "cloudflare_account_id", "cloudflare_api_token",
}
_TOOL_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
_CALL_ID_RE = re.compile(r"^call_[A-Za-z0-9_-]{1,64}$")

_SAFE_MESSAGES = {
    "INVALID_TYPE": "Cloudflare adapter input has an invalid type",
    "EXTRA_FIELD": "Cloudflare adapter input contains unknown fields",
    "MISSING_FIELD": "Cloudflare adapter input is missing required fields",
    "MODEL_NOT_ALLOWLISTED": "Cloudflare model is not allowlisted",
    "DATA_NOT_ALLOWED": "data classification is not allowed for Cloudflare",
    "INPUT_LIMIT": "estimated Cloudflare input exceeds contract ceiling",
    "OUTPUT_LIMIT": "requested Cloudflare output exceeds contract ceiling",
    "REQUEST_TOO_LARGE": "Cloudflare request exceeds byte ceiling",
    "OUTPUT_TOO_LARGE": "synthetic Cloudflare output exceeds byte ceiling",
    "BUILTIN_TOOL_FORBIDDEN": "Cloudflare built-in tools are forbidden",
    "REMOTE_MCP_FORBIDDEN": "Cloudflare remote MCP is forbidden",
    "LOCAL_TOOL_INVALID": "local tool definition is invalid",
    "LOCAL_TOOL_NOT_ALLOWED": "local tool request is not allowlisted",
    "STORAGE_FORBIDDEN": "Cloudflare storage services are forbidden",
    "AI_GATEWAY_FORBIDDEN": "Cloudflare AI Gateway is forbidden",
    "THIRD_PARTY_ROUTING_FORBIDDEN": "third-party provider routing is forbidden",
    "SECRET_MATERIAL": "secret or raw account material is forbidden",
    "SYNTHETIC_REQUIRED": "offline Cloudflare adapter accepts synthetic responses only",
    "RESPONSE_INVALID": "synthetic Cloudflare response is invalid",
    "USAGE_INVALID": "synthetic Cloudflare usage is invalid",
    "POLICY_MISMATCH": "Cloudflare policy does not match the accepted contract",
    "CONTRACT_METADATA_INVALID": "Cloudflare metadata failed generic onboarding validation",
    "NONZERO_BUDGET": "Cloudflare monetary ceiling must remain zero",
    "PAID_PATH_FORBIDDEN": "paid Cloudflare path is forbidden",
    "FREE_QUOTA_EXHAUSTED": "Cloudflare free allocation is exhausted",
    "CAPACITY_UNAVAILABLE": "Cloudflare capacity is unavailable",
    "PAID_PLAN_REQUIRED": "Cloudflare model requires Workers Paid",
    "PROVIDER_ERROR": "Cloudflare provider error is not eligible for automatic retry",
    "QUOTA_INVALID": "Cloudflare quota evidence is invalid",
    "QUOTA_LIMIT": "GAME Cloudflare daily quota ceiling exceeded",
    "REFERENCE_MISMATCH": "Cloudflare reserved reference does not match contract",
}


class CloudflareAdapterError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        self.safe_message = _SAFE_MESSAGES.get(code, "Cloudflare adapter rejected input")
        super().__init__(self.safe_message)


def _fail(code: str) -> None:
    raise CloudflareAdapterError(code)


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


def validate_reserved_refs(credential_ref: Any, account_ref: Any) -> dict[str, str]:
    if credential_ref != CREDENTIAL_PROFILE_REF or account_ref != ACCOUNT_REF:
        _fail("REFERENCE_MISMATCH")
    return {"credential_profile_ref": CREDENTIAL_PROFILE_REF, "account_ref": ACCOUNT_REF}


def validate_static_chain(profile, child, model, transport, data_policy, quota_policy, budget_policy):
    snapshots = [copy.deepcopy(x) for x in (profile, child, model, transport, data_policy, quota_policy, budget_policy)]
    for value in snapshots:
        _public_preflight(value)
    try:
        normalized_profile = po.validate_provider_profile(profile)
        normalized_child = po.validate_child_contract_evidence(child, normalized_profile=normalized_profile)
        normalized_model = po.validate_model_profile(model, normalized_profile=normalized_profile, normalized_child=normalized_child)
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
        "account_resolution_authority": "NONE",
        "credential_resolution_authority": "NONE",
        "money_ceiling": 0,
    }
    cr.assert_public_safe(result)
    originals = (profile, child, model, transport, data_policy, quota_policy, budget_policy)
    for original, snapshot in zip(originals, snapshots):
        if original != snapshot:
            _fail("POLICY_MISMATCH")
    return result


def _validate_transport_policy(value):
    expected = {"schema_version", "transport_profile_id", "scheme", "host", "base_path_template", "canonical_base_url_template", "chat_completions_path", "accepted_account_ref", "allow_redirects", "allowed_protocols", "ai_gateway_allowed", "network_activation"}
    v = _exact_fields(value, expected)
    if (
        v["schema_version"] != "1.0"
        or v["transport_profile_id"] != TRANSPORT_PROFILE_REF
        or v["scheme"] != "https"
        or v["host"] != HOST
        or v["base_path_template"] != BASE_PATH_TEMPLATE
        or v["canonical_base_url_template"] != BASE_URL_TEMPLATE
        or v["chat_completions_path"] != CHAT_PATH
        or v["accepted_account_ref"] != ACCOUNT_REF
        or v["allow_redirects"] is not False
        or v["allowed_protocols"] != ["HTTPS"]
        or v["ai_gateway_allowed"] is not False
        or v["network_activation"] != "STUDIO-009F_ONLY"
    ):
        _fail("POLICY_MISMATCH")


def _validate_data_policy(value):
    expected = {"schema_version", "data_policy_id", "allowed_data_classifications", "denied_data_classifications", "synthetic_data_allowed", "provider_training_without_explicit_consent_allowed", "storage_services_allowed", "ai_gateway_logging_allowed", "connected_activation"}
    v = _exact_fields(value, expected)
    if (
        v["schema_version"] != "1.0"
        or v["data_policy_id"] != DATA_POLICY_REF
        or v["allowed_data_classifications"] != ["PUBLIC"]
        or v["denied_data_classifications"] != ["INTERNAL", "RESTRICTED"]
        or v["synthetic_data_allowed"] is not True
        or v["provider_training_without_explicit_consent_allowed"] is not False
        or v["storage_services_allowed"] is not False
        or v["ai_gateway_logging_allowed"] is not False
        or v["connected_activation"] != "STUDIO-009F_ONLY"
    ):
        _fail("DATA_NOT_ALLOWED")


def _validate_quota_policy(value):
    expected = {"schema_version", "quota_policy_id", "provider_snapshot", "game_limits", "error_normalization", "paid_upgrade_allowed", "automatic_quota_increase_allowed", "on_ineligible"}
    v = _exact_fields(value, expected)
    if v["schema_version"] != "1.0" or v["quota_policy_id"] != QUOTA_POLICY_REF:
        _fail("POLICY_MISMATCH")
    if v["provider_snapshot"] != {"free_neurons_per_day": 10000, "reset": "00:00 UTC", "input_neurons_per_million_tokens": 45455, "output_neurons_per_million_tokens": 136364}:
        _fail("POLICY_MISMATCH")
    if v["game_limits"] != {"max_daily_neurons": 8000, "max_concurrency": 1, "max_retries": 0, "timeout_seconds": 60, "max_input_tokens": 16384, "max_output_tokens": 4096}:
        _fail("POLICY_MISMATCH")
    if v["error_normalization"] != {"3036": "FREE_QUOTA_EXHAUSTED", "3040": "CAPACITY_UNAVAILABLE", "5035": "PAID_PLAN_REQUIRED"}:
        _fail("POLICY_MISMATCH")
    if v["paid_upgrade_allowed"] is not False or v["automatic_quota_increase_allowed"] is not False:
        _fail("PAID_PATH_FORBIDDEN")
    if v["on_ineligible"] != "FAILOVER_OR_MANUAL_FAKE":
        _fail("POLICY_MISMATCH")


def _validate_budget_policy(value):
    expected = {"schema_version", "budget_policy_id", "currency", "money_ceiling", "workers_free_required", "paid_plan_allowed", "auto_recharge_allowed", "unified_billing_allowed", "prepaid_credits_allowed", "chargeable_fallback_allowed", "promotional_credit_broadens_authority"}
    v = _exact_fields(value, expected)
    if v["schema_version"] != "1.0" or v["budget_policy_id"] != BUDGET_POLICY_REF or v["currency"] != "USD":
        _fail("POLICY_MISMATCH")
    if v["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if v["workers_free_required"] is not True:
        _fail("PAID_PATH_FORBIDDEN")
    for name in ("paid_plan_allowed", "auto_recharge_allowed", "unified_billing_allowed", "prepaid_credits_allowed", "chargeable_fallback_allowed", "promotional_credit_broadens_authority"):
        if v[name] is not False:
            _fail("PAID_PATH_FORBIDDEN")


def _normalize_tool_definitions(value):
    if not isinstance(value, list):
        _fail("LOCAL_TOOL_INVALID")
    result = []
    names = set()
    for item in value:
        v = _exact_fields(item, {"name", "description"})
        if not isinstance(v["name"], str) or not _TOOL_NAME_RE.fullmatch(v["name"]) or v["name"] in names:
            _fail("LOCAL_TOOL_INVALID")
        if not isinstance(v["description"], str) or len(v["description"]) > 256:
            _fail("LOCAL_TOOL_INVALID")
        names.add(v["name"])
        result.append({"name": v["name"], "description": v["description"]})
    return result


def normalize_request(request):
    snapshot = copy.deepcopy(request)
    _public_preflight(request, byte_limit=MAX_REQUEST_BYTES)
    v = _exact_fields(request, {"model", "data_classification", "messages", "estimated_input_tokens", "max_output_tokens", "local_tools", "built_in_tools", "remote_mcp", "storage_services", "ai_gateway", "third_party_routing"})
    if v["model"] != MODEL_ID:
        _fail("MODEL_NOT_ALLOWLISTED")
    if v["data_classification"] not in ALLOWED_DATA_CLASSIFICATIONS:
        _fail("DATA_NOT_ALLOWED")
    estimated = _require_int(v["estimated_input_tokens"], 0, MAX_INPUT_TOKENS, "INPUT_LIMIT")
    output_tokens = _require_int(v["max_output_tokens"], 1, MAX_OUTPUT_TOKENS, "OUTPUT_LIMIT")
    if not isinstance(v["messages"], list) or not v["messages"]:
        _fail("INVALID_TYPE")
    messages = []
    for message in v["messages"]:
        m = _exact_fields(message, {"role", "content"})
        if m["role"] not in {"system", "user", "assistant"} or not isinstance(m["content"], str):
            _fail("INVALID_TYPE")
        messages.append({"role": m["role"], "content": m["content"]})
    if v["built_in_tools"] != []:
        _fail("BUILTIN_TOOL_FORBIDDEN")
    if v["remote_mcp"] != []:
        _fail("REMOTE_MCP_FORBIDDEN")
    if v["storage_services"] != []:
        _fail("STORAGE_FORBIDDEN")
    if v["ai_gateway"] is not False:
        _fail("AI_GATEWAY_FORBIDDEN")
    if v["third_party_routing"] is not False:
        _fail("THIRD_PARTY_ROUTING_FORBIDDEN")
    tools = _normalize_tool_definitions(v["local_tools"])
    result = {"model": MODEL_ID, "data_classification": "PUBLIC", "messages": messages, "estimated_input_tokens": estimated, "max_output_tokens": output_tokens, "local_tools": tools, "built_in_tools": [], "remote_mcp": [], "storage_services": [], "ai_gateway": False, "third_party_routing": False}
    cr.assert_public_safe(result)
    if request != snapshot:
        _fail("INVALID_TYPE")
    return result


def estimate_neurons(input_tokens: Any, output_tokens: Any) -> int:
    i = _require_int(input_tokens, 0, MAX_INPUT_TOKENS, "INPUT_LIMIT")
    o = _require_int(output_tokens, 0, MAX_OUTPUT_TOKENS, "OUTPUT_LIMIT")
    numerator = i * INPUT_NEURONS_PER_MILLION + o * OUTPUT_NEURONS_PER_MILLION
    return (numerator + 999999) // 1000000


def normalize_quota_evidence(value):
    snapshot = copy.deepcopy(value)
    _public_preflight(value)
    v = _exact_fields(value, {"synthetic", "consumed_neurons", "provider_free_neurons", "game_daily_neurons"})
    if v["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    consumed = _require_int(v["consumed_neurons"], 0, PROVIDER_FREE_NEURONS, "QUOTA_INVALID")
    if v["provider_free_neurons"] != PROVIDER_FREE_NEURONS or v["game_daily_neurons"] != GAME_DAILY_NEURONS:
        _fail("QUOTA_INVALID")
    if consumed > GAME_DAILY_NEURONS:
        _fail("QUOTA_LIMIT")
    result = {"synthetic": True, "consumed_neurons": consumed, "game_remaining_neurons": GAME_DAILY_NEURONS - consumed, "provider_free_neurons": PROVIDER_FREE_NEURONS, "network_activity": "NONE"}
    cr.assert_public_safe(result)
    if value != snapshot:
        _fail("INVALID_TYPE")
    return result


def normalize_error(value):
    snapshot = copy.deepcopy(value)
    _public_preflight(value)
    v = _exact_fields(value, {"synthetic", "http_status", "internal_code"})
    if v["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    status = _require_int(v["http_status"], 100, 599, "INVALID_TYPE")
    code = _require_int(v["internal_code"], 0, 9999, "INVALID_TYPE")
    mapping = {(429, 3036): "FREE_QUOTA_EXHAUSTED", (429, 3040): "CAPACITY_UNAVAILABLE", (403, 5035): "PAID_PLAN_REQUIRED"}
    normalized = mapping.get((status, code), "PROVIDER_ERROR")
    result = {"error_code": normalized, "retry_allowed": False, "paid_upgrade_allowed": False, "failover_or_manual_fake": True, "network_activity": "NONE"}
    cr.assert_public_safe(result)
    if value != snapshot:
        _fail("INVALID_TYPE")
    return result


def _normalize_tool_requests(value):
    if not isinstance(value, list):
        _fail("RESPONSE_INVALID")
    result = []
    seen = set()
    for item in value:
        v = _exact_fields(item, {"id", "name", "arguments"})
        if not isinstance(v["id"], str) or not _CALL_ID_RE.fullmatch(v["id"]) or v["id"] in seen:
            _fail("RESPONSE_INVALID")
        if not isinstance(v["name"], str) or not _TOOL_NAME_RE.fullmatch(v["name"]):
            _fail("RESPONSE_INVALID")
        if not isinstance(v["arguments"], dict):
            _fail("RESPONSE_INVALID")
        _public_preflight(v["arguments"])
        seen.add(v["id"])
        result.append({"id": v["id"], "name": v["name"], "arguments": copy.deepcopy(v["arguments"])})
    return result


def normalize_synthetic_response(value):
    snapshot = copy.deepcopy(value)
    _public_preflight(value, byte_limit=MAX_OUTPUT_BYTES)
    v = _exact_fields(value, {"synthetic", "model", "output_text", "tool_requests", "usage", "stop_reason"})
    if v["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    if v["model"] != MODEL_ID:
        _fail("MODEL_NOT_ALLOWLISTED")
    if not isinstance(v["output_text"], str) or v["stop_reason"] not in {"stop", "tool_request"}:
        _fail("RESPONSE_INVALID")
    usage = _exact_fields(v["usage"], {"input_tokens", "output_tokens"})
    input_tokens = _require_int(usage["input_tokens"], 0, MAX_INPUT_TOKENS, "USAGE_INVALID")
    output_tokens = _require_int(usage["output_tokens"], 0, MAX_OUTPUT_TOKENS, "USAGE_INVALID")
    tool_requests = _normalize_tool_requests(v["tool_requests"])
    if v["stop_reason"] == "tool_request" and not tool_requests:
        _fail("RESPONSE_INVALID")
    result = {"synthetic": True, "model": MODEL_ID, "output_text": v["output_text"], "tool_requests": tool_requests, "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "estimated_neurons": estimate_neurons(input_tokens, output_tokens)}, "stop_reason": v["stop_reason"], "network_activity": "NONE"}
    cr.assert_public_safe(result)
    if value != snapshot:
        _fail("INVALID_TYPE")
    return result


def plan_local_tool_requests(response, allowed_tool_names):
    normalized = normalize_synthetic_response(response)
    if not isinstance(allowed_tool_names, (set, tuple, list)) or any(not isinstance(x, str) or not _TOOL_NAME_RE.fullmatch(x) for x in allowed_tool_names):
        _fail("LOCAL_TOOL_INVALID")
    allowed = set(allowed_tool_names)
    planned = []
    for request in normalized["tool_requests"]:
        if request["name"] not in allowed:
            _fail("LOCAL_TOOL_NOT_ALLOWED")
        planned.append({"id": request["id"], "name": request["name"], "arguments": copy.deepcopy(request["arguments"]), "execution": "NOT_EXECUTED"})
    cr.assert_public_safe(planned)
    return planned
