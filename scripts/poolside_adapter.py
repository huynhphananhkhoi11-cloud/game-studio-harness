#!/usr/bin/env python3
"""Deterministic offline Poolside adapter for STUDIO-009P-04.

No network, Poolside account discovery, API-key resolution, Poolside CLI,
provider SDK, model inference, tool/MCP/ACP/shell/file/browser execution,
repository write, routing, production use, or spend occurs.
"""
from __future__ import annotations

import copy
import math
from typing import Any, Iterable

from scripts import credential_redaction as cr
from scripts import provider_onboarding as po

PROVIDER_PROFILE_ID = "provider-profile:poolside-direct-laguna-s-2.1"
MODEL_PROFILE_ID = "provider-model:poolside-laguna-s-2.1"
CHILD_CONTRACT_ID = "STUDIO-009P-04"
MODEL_ID = "poolside/laguna-s-2.1"
MODEL_IDENTITY_REF = "model-id:poolside/laguna-s-2.1"

HOST = "inference.poolside.ai"
BASE_PATH = "/v1"
BASE_URL = "https://inference.poolside.ai/v1"
CHAT_PATH = "/v1/chat/completions"

TRANSPORT_PROFILE_REF = "transport-profile:poolside-direct-https-openai-v1"
CREDENTIAL_PROFILE_REF = "credential-profile:poolside-api-key"
ACCOUNT_REF = "account-ref:poolside-owner-account"
DATA_POLICY_REF = "data-policy:poolside-public-synthetic-training-risk"
QUOTA_POLICY_REF = "quota-policy:poolside-free-limited-dynamic"
BUDGET_POLICY_REF = "budget-policy:poolside-zero"

MAX_INPUT_TOKENS = 4096
MAX_OUTPUT_TOKENS = 1024
MAX_REQUEST_BYTES = 32768
MAX_OUTPUT_BYTES = 131072
MAX_CONCURRENCY = 1
MAX_RETRIES = 0
TIMEOUT_SECONDS = 60

ALLOWED_DATA_CLASSIFICATIONS = ("PUBLIC",)
ALLOWED_CAPABILITIES = ("REASONING", "TEXT_GENERATION")

_FORBIDDEN_FIELD_NAMES = {
    "secret", "secret_value", "credential_value", "token", "access_token",
    "refresh_token", "password", "passwd", "private_key", "api_key",
    "authorization", "cookie", "session", "session_token", "raw_api_key",
    "poolside_api_key", "poolside_token",
}

_SAFE_MESSAGES = {
    "INVALID_TYPE": "Poolside adapter input has an invalid type",
    "EXTRA_FIELD": "Poolside adapter input contains unknown fields",
    "MISSING_FIELD": "Poolside adapter input is missing required fields",
    "MODEL_NOT_ALLOWLISTED": "Poolside model is not allowlisted",
    "DATA_NOT_ALLOWED": "data classification is not allowed for Poolside validation",
    "INPUT_LIMIT": "estimated Poolside input exceeds GAME contract ceiling",
    "OUTPUT_LIMIT": "requested Poolside output exceeds GAME contract ceiling",
    "REQUEST_TOO_LARGE": "Poolside synthetic request exceeds byte ceiling",
    "TOOL_FORBIDDEN": "tool execution is forbidden under STUDIO-009P-04",
    "REMOTE_MCP_FORBIDDEN": "remote MCP is forbidden under STUDIO-009P-04",
    "ACP_FORBIDDEN": "ACP is forbidden under STUDIO-009P-04",
    "SHELL_FORBIDDEN": "shell execution is forbidden under STUDIO-009P-04",
    "FILE_ACCESS_FORBIDDEN": "file access is forbidden under STUDIO-009P-04",
    "BROWSER_FORBIDDEN": "browser execution is forbidden under STUDIO-009P-04",
    "URL_CONTEXT_FORBIDDEN": "URL context is forbidden under STUDIO-009P-04",
    "ROUTING_FORBIDDEN": "routing or failover is forbidden under STUDIO-009P-04",
    "POOL_CLI_FORBIDDEN": "Poolside CLI execution is forbidden under STUDIO-009P-04",
    "REPOSITORY_WRITE_FORBIDDEN": "repository write is forbidden under STUDIO-009P-04",
    "CREDENTIAL_FILE_FORBIDDEN": "Poolside credential-file access is forbidden",
    "SECRET_MATERIAL": "secret material is forbidden",
    "SYNTHETIC_REQUIRED": "offline Poolside adapter accepts synthetic evidence only",
    "RESPONSE_INVALID": "synthetic Poolside response is invalid",
    "USAGE_INVALID": "synthetic Poolside usage is invalid",
    "POLICY_MISMATCH": "Poolside policy does not match the accepted contract",
    "CONTRACT_METADATA_INVALID": "Poolside metadata failed generic onboarding validation",
    "NONZERO_BUDGET": "Poolside monetary ceiling must remain zero",
    "PAID_PATH_REQUIRED": "Poolside path requires a paid or billing-enabled route",
    "ZERO_COST_ELIGIBILITY_UNPROVEN": "Poolside zero-cost eligibility is unproven",
    "RATE_LIMIT_OR_CAPACITY": "Poolside rate limit or capacity prevented execution",
    "AUTH_FAILURE": "Poolside authentication or authorization failed",
    "NOT_FOUND": "Poolside endpoint or exact model was not found",
    "REQUEST_VALIDATION_FAILURE": "Poolside request validation failed",
    "PROVIDER_EXECUTION_FAILURE": "Poolside provider execution failed",
    "TIMEOUT": "Poolside request timed out",
    "MALFORMED_RESPONSE": "Poolside response was malformed",
    "REDIRECT_FORBIDDEN": "Poolside transport redirected outside accepted identity",
    "MODEL_IDENTITY_MISMATCH": "Poolside response model identity did not match",
    "UNEXPECTED_CAPABILITY": "Poolside response attempted an unauthorized capability",
    "TERMS_DRIFT": "Poolside terms or data-policy evidence changed",
    "REFERENCE_MISMATCH": "Poolside reserved reference does not match contract",
}


class PoolsideAdapterError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        self.safe_message = _SAFE_MESSAGES.get(code, "Poolside adapter rejected input")
        super().__init__(self.safe_message)


def _fail(code: str) -> None:
    raise PoolsideAdapterError(code)


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
    stack = [(None, value, 0)]
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


def _public_preflight(value: Any, byte_limit: int | None = None) -> None:
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
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        _fail(code)
    return value


def validate_reserved_refs(credential_ref: str, account_ref: str) -> dict[str, str]:
    if credential_ref != CREDENTIAL_PROFILE_REF or account_ref != ACCOUNT_REF:
        _fail("REFERENCE_MISMATCH")
    return {
        "credential_profile_ref": CREDENTIAL_PROFILE_REF,
        "account_ref": ACCOUNT_REF,
    }


def validate_static_chain(
    profile: dict[str, Any],
    child: dict[str, Any],
    model: dict[str, Any],
    transport: dict[str, Any],
    data_policy: dict[str, Any],
    quota_policy: dict[str, Any],
    budget_policy: dict[str, Any],
) -> dict[str, Any]:
    originals = (profile, child, model, transport, data_policy, quota_policy, budget_policy)
    snapshots = [copy.deepcopy(item) for item in originals]
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
        "child_contract_id": normalized_child["child_contract_id"],
        "provider_model_profile_id": normalized_model["provider_model_profile_id"],
        "model_id": MODEL_ID,
        "provider_state": "DISABLED",
        "model_state": "DECLARED",
        "child_evidence_class": "SYNTHETIC",
        "network_authority": "NONE",
        "credential_resolution_authority": "NONE",
        "pool_cli_authority": "NONE",
        "tool_authority": "NONE",
        "mcp_authority": "NONE",
        "acp_authority": "NONE",
        "routing_authority": "NONE",
        "money_ceiling": 0,
    }
    cr.assert_public_safe(result)

    for original, snapshot in zip(originals, snapshots):
        if original != snapshot:
            _fail("POLICY_MISMATCH")
    return result


def _validate_transport_policy(value: dict[str, Any]) -> None:
    expected_fields = {
        "schema_version", "transport_profile_id", "scheme", "host", "base_path",
        "canonical_base_url", "chat_completions_path",
        "accepted_credential_profile_ref", "accepted_account_ref",
        "allow_redirects", "allowed_protocols", "third_party_gateway_allowed",
        "enterprise_deployment_endpoint_allowed", "local_or_self_hosted_allowed",
        "network_activation",
    }
    value = _exact_fields(value, expected_fields)
    expected = {
        "schema_version": "1.0",
        "transport_profile_id": TRANSPORT_PROFILE_REF,
        "scheme": "https",
        "host": HOST,
        "base_path": BASE_PATH,
        "canonical_base_url": BASE_URL,
        "chat_completions_path": CHAT_PATH,
        "accepted_credential_profile_ref": CREDENTIAL_PROFILE_REF,
        "accepted_account_ref": ACCOUNT_REF,
        "allow_redirects": False,
        "allowed_protocols": ["HTTPS"],
        "third_party_gateway_allowed": False,
        "enterprise_deployment_endpoint_allowed": False,
        "local_or_self_hosted_allowed": False,
        "network_activation": "NONE_P04_OFFLINE",
    }
    if value != expected:
        _fail("POLICY_MISMATCH")


def _validate_data_policy(value: dict[str, Any]) -> None:
    expected_fields = {
        "schema_version", "data_policy_id", "allowed_data_classifications",
        "denied_data_classifications", "synthetic_data_allowed",
        "private_or_unreleased_export_allowed", "personal_data_allowed",
        "confidential_or_sensitive_data_allowed",
        "provider_training_use_risk_acknowledged",
        "training_opt_out_broadens_game_authority",
        "feedback_submission_allowed", "connected_activation",
    }
    value = _exact_fields(value, expected_fields)
    expected = {
        "schema_version": "1.0",
        "data_policy_id": DATA_POLICY_REF,
        "allowed_data_classifications": ["PUBLIC"],
        "denied_data_classifications": ["INTERNAL", "RESTRICTED"],
        "synthetic_data_allowed": True,
        "private_or_unreleased_export_allowed": False,
        "personal_data_allowed": False,
        "confidential_or_sensitive_data_allowed": False,
        "provider_training_use_risk_acknowledged": True,
        "training_opt_out_broadens_game_authority": False,
        "feedback_submission_allowed": False,
        "connected_activation": "NONE_P04_OFFLINE",
    }
    if value != expected:
        _fail("DATA_NOT_ALLOWED")


def _validate_quota_policy(value: dict[str, Any]) -> None:
    expected_fields = {
        "schema_version", "quota_policy_id", "provider_snapshot",
        "future_v04_limits", "free_eligibility_must_be_reverified",
        "billing_path_allowed", "payment_method_requirement_allowed",
        "automatic_quota_increase_allowed", "on_unproven",
    }
    value = _exact_fields(value, expected_fields)
    if value["schema_version"] != "1.0" or value["quota_policy_id"] != QUOTA_POLICY_REF:
        _fail("POLICY_MISMATCH")
    if value["provider_snapshot"] != {
        "availability": "FREE_FOR_LIMITED_TIME_DYNAMIC",
        "permanent_rpm": None,
        "permanent_rpd": None,
        "free_window_expiry": None,
        "account_level_zero_cost_required": True,
    }:
        _fail("POLICY_MISMATCH")
    if value["future_v04_limits"] != {
        "max_real_requests": 3,
        "max_concurrency": 1,
        "max_retries": 0,
        "timeout_seconds": 60,
        "max_input_tokens": 4096,
        "max_output_tokens": 1024,
        "max_request_bytes": 32768,
        "max_response_bytes": 131072,
        "streaming": False,
        "tools": False,
        "mcp": False,
        "acp": False,
    }:
        _fail("POLICY_MISMATCH")
    if (
        value["free_eligibility_must_be_reverified"] is not True
        or value["billing_path_allowed"] is not False
        or value["payment_method_requirement_allowed"] is not False
        or value["automatic_quota_increase_allowed"] is not False
        or value["on_unproven"] != "FAIL_CLOSED"
    ):
        _fail("PAID_PATH_REQUIRED")


def _validate_budget_policy(value: dict[str, Any]) -> None:
    expected_fields = {
        "schema_version", "budget_policy_id", "currency", "money_ceiling",
        "zero_cost_route_required", "paid_subscription_allowed",
        "payment_method_requirement_allowed", "credit_purchase_allowed",
        "auto_recharge_allowed", "paid_fallback_allowed",
        "third_party_paid_gateway_allowed", "self_hosted_spend_allowed",
        "production_use_allowed",
    }
    value = _exact_fields(value, expected_fields)
    if (
        value["schema_version"] != "1.0"
        or value["budget_policy_id"] != BUDGET_POLICY_REF
        or value["currency"] != "USD"
    ):
        _fail("POLICY_MISMATCH")
    if value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if value["zero_cost_route_required"] is not True:
        _fail("PAID_PATH_REQUIRED")
    denied = (
        "paid_subscription_allowed", "payment_method_requirement_allowed",
        "credit_purchase_allowed", "auto_recharge_allowed",
        "paid_fallback_allowed", "third_party_paid_gateway_allowed",
        "self_hosted_spend_allowed", "production_use_allowed",
    )
    if any(value[field] is not False for field in denied):
        _fail("PAID_PATH_REQUIRED")


def normalize_request(value: dict[str, Any]) -> dict[str, Any]:
    snapshot = copy.deepcopy(value)
    _public_preflight(value, MAX_REQUEST_BYTES)
    expected_fields = {
        "model", "data_classification", "messages", "estimated_input_tokens",
        "max_output_tokens", "stream", "tools", "remote_mcp", "acp",
        "shell_execution", "file_access", "browser", "url_context", "routing",
        "retries", "concurrency", "timeout_seconds", "pool_cli",
        "repository_write",
    }
    value = _exact_fields(value, expected_fields)

    if value["model"] != MODEL_ID:
        _fail("MODEL_NOT_ALLOWLISTED")
    if value["data_classification"] != "PUBLIC":
        _fail("DATA_NOT_ALLOWED")
    if not isinstance(value["messages"], list) or not value["messages"]:
        _fail("INVALID_TYPE")
    for message in value["messages"]:
        message = _exact_fields(message, {"role", "content"})
        if message["role"] not in {"system", "user", "assistant"}:
            _fail("INVALID_TYPE")
        if not isinstance(message["content"], str):
            _fail("INVALID_TYPE")

    _require_int(value["estimated_input_tokens"], 0, MAX_INPUT_TOKENS, "INPUT_LIMIT")
    _require_int(value["max_output_tokens"], 1, MAX_OUTPUT_TOKENS, "OUTPUT_LIMIT")

    if value["stream"] is not False:
        _fail("POLICY_MISMATCH")
    if value["tools"] not in ([], False, None):
        _fail("TOOL_FORBIDDEN")
    if value["remote_mcp"] not in ([], False, None):
        _fail("REMOTE_MCP_FORBIDDEN")
    if value["acp"] not in ([], False, None):
        _fail("ACP_FORBIDDEN")
    if value["shell_execution"] is not False:
        _fail("SHELL_FORBIDDEN")
    if value["file_access"] is not False:
        _fail("FILE_ACCESS_FORBIDDEN")
    if value["browser"] is not False:
        _fail("BROWSER_FORBIDDEN")
    if value["url_context"] is not False:
        _fail("URL_CONTEXT_FORBIDDEN")
    if value["routing"] is not False:
        _fail("ROUTING_FORBIDDEN")
    if value["pool_cli"] is not False:
        _fail("POOL_CLI_FORBIDDEN")
    if value["repository_write"] is not False:
        _fail("REPOSITORY_WRITE_FORBIDDEN")
    if (
        value["retries"] != MAX_RETRIES
        or value["concurrency"] != MAX_CONCURRENCY
        or value["timeout_seconds"] != TIMEOUT_SECONDS
    ):
        _fail("POLICY_MISMATCH")

    result = {
        "synthetic": True,
        "model": MODEL_ID,
        "messages": copy.deepcopy(value["messages"]),
        "max_tokens": value["max_output_tokens"],
        "stream": False,
        "tools": [],
        "network_activity": "NONE",
        "credential_activity": "NONE",
        "pool_cli_activity": "NONE",
        "tool_activity": "NONE",
        "mcp_activity": "NONE",
        "acp_activity": "NONE",
        "routing_activity": "NONE",
        "repository_write_activity": "NONE",
    }
    _public_preflight(result, MAX_REQUEST_BYTES)
    if value != snapshot:
        _fail("POLICY_MISMATCH")
    return result


def normalize_synthetic_response(value: dict[str, Any]) -> dict[str, Any]:
    snapshot = copy.deepcopy(value)
    _public_preflight(value, MAX_OUTPUT_BYTES)
    value = _exact_fields(
        value, {"synthetic", "model", "output_text", "usage", "finish_reason", "tool_calls"}
    )
    if value["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    if value["model"] != MODEL_ID:
        _fail("MODEL_NOT_ALLOWLISTED")
    if not isinstance(value["output_text"], str):
        _fail("RESPONSE_INVALID")
    usage = _exact_fields(value["usage"], {"input_tokens", "output_tokens"})
    _require_int(usage["input_tokens"], 0, MAX_INPUT_TOKENS, "USAGE_INVALID")
    _require_int(usage["output_tokens"], 0, MAX_OUTPUT_TOKENS, "USAGE_INVALID")
    if value["finish_reason"] not in {"stop", "length"}:
        _fail("RESPONSE_INVALID")
    if value["tool_calls"] not in ([], False, None):
        _fail("UNEXPECTED_CAPABILITY")

    result = {
        "model": MODEL_ID,
        "output_text": value["output_text"],
        "usage": copy.deepcopy(usage),
        "finish_reason": value["finish_reason"],
        "network_activity": "NONE",
        "provider_runtime_activity": "NONE",
        "pool_cli_activity": "NONE",
        "tool_execution_activity": "NONE",
        "mcp_activity": "NONE",
        "acp_activity": "NONE",
        "routing_activity": "NONE",
        "spend_usd": 0,
    }
    cr.assert_public_safe(result)
    if value != snapshot:
        _fail("POLICY_MISMATCH")
    return result


def normalize_zero_cost_evidence(value: dict[str, Any]) -> dict[str, Any]:
    snapshot = copy.deepcopy(value)
    _public_preflight(value)
    value = _exact_fields(
        value,
        {
            "synthetic", "free_limited_offer_visible", "account_zero_cost_eligible",
            "billing_required", "payment_method_required", "subscription_required",
            "credit_purchase_required",
        },
    )
    if value["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    for field in (
        "free_limited_offer_visible", "account_zero_cost_eligible",
        "billing_required", "payment_method_required", "subscription_required",
        "credit_purchase_required",
    ):
        if not isinstance(value[field], bool):
            _fail("INVALID_TYPE")
    if (
        value["billing_required"]
        or value["payment_method_required"]
        or value["subscription_required"]
        or value["credit_purchase_required"]
    ):
        _fail("PAID_PATH_REQUIRED")
    if not value["free_limited_offer_visible"] or not value["account_zero_cost_eligible"]:
        _fail("ZERO_COST_ELIGIBILITY_UNPROVEN")
    result = {
        "zero_cost_eligible": True,
        "entitlement_basis": "FREE_FOR_LIMITED_TIME_DYNAMIC_ACCOUNT_PROOF_REQUIRED",
        "permanent_rpm_assumed": None,
        "permanent_rpd_assumed": None,
        "free_window_expiry_assumed": None,
        "money_ceiling": 0,
    }
    cr.assert_public_safe(result)
    if value != snapshot:
        _fail("POLICY_MISMATCH")
    return result


def normalize_error(value: dict[str, Any]) -> dict[str, Any]:
    snapshot = copy.deepcopy(value)
    _public_preflight(value)
    value = _exact_fields(value, {"synthetic", "http_status", "error_type"})
    if value["synthetic"] is not True:
        _fail("SYNTHETIC_REQUIRED")
    status = value["http_status"]
    error_type = value["error_type"]
    if status is not None and (isinstance(status, bool) or not isinstance(status, int)):
        _fail("INVALID_TYPE")
    if error_type is not None and not isinstance(error_type, str):
        _fail("INVALID_TYPE")

    if status in (401, 403):
        code = "AUTH_FAILURE"
    elif status == 404:
        code = "NOT_FOUND"
    elif status == 422:
        code = "REQUEST_VALIDATION_FAILURE"
    elif status == 429:
        code = "RATE_LIMIT_OR_CAPACITY"
    elif isinstance(status, int) and 500 <= status <= 599:
        code = "PROVIDER_EXECUTION_FAILURE"
    elif error_type == "timeout":
        code = "TIMEOUT"
    elif error_type == "malformed":
        code = "MALFORMED_RESPONSE"
    elif error_type == "redirect":
        code = "REDIRECT_FORBIDDEN"
    elif error_type == "model_mismatch":
        code = "MODEL_IDENTITY_MISMATCH"
    elif error_type == "unexpected_tool":
        code = "UNEXPECTED_CAPABILITY"
    elif error_type == "terms_drift":
        code = "TERMS_DRIFT"
    else:
        code = "PROVIDER_EXECUTION_FAILURE"

    result = {
        "error_code": code,
        "safe_message": _SAFE_MESSAGES[code],
        "retry_allowed": False,
        "paid_upgrade_allowed": False,
        "model_fallback_allowed": False,
        "provider_fallback_allowed": False,
        "tool_activation_allowed": False,
        "routing_allowed": False,
    }
    cr.assert_public_safe(result)
    if value != snapshot:
        _fail("POLICY_MISMATCH")
    return result


def validate_harness_request(value: dict[str, Any]) -> dict[str, str]:
    snapshot = copy.deepcopy(value)
    _public_preflight(value)
    value = _exact_fields(
        value,
        {
            "pool_cli", "credential_file_access", "repository_write",
            "tools", "mcp", "acp",
        },
    )
    if value["pool_cli"] is not False:
        _fail("POOL_CLI_FORBIDDEN")
    if value["credential_file_access"] is not False:
        _fail("CREDENTIAL_FILE_FORBIDDEN")
    if value["repository_write"] is not False:
        _fail("REPOSITORY_WRITE_FORBIDDEN")
    if value["tools"] not in ([], False, None):
        _fail("TOOL_FORBIDDEN")
    if value["mcp"] not in ([], False, None):
        _fail("REMOTE_MCP_FORBIDDEN")
    if value["acp"] not in ([], False, None):
        _fail("ACP_FORBIDDEN")
    if value != snapshot:
        _fail("POLICY_MISMATCH")
    return {
        "pool_cli_activity": "NONE",
        "credential_file_activity": "NONE",
        "repository_write_activity": "NONE",
        "tool_activity": "NONE",
        "mcp_activity": "NONE",
        "acp_activity": "NONE",
    }
