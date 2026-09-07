#!/usr/bin/env python3
"""Narrow direct Cloudflare Workers AI HTTPS transport for STUDIO-009V-02.

Import is offline. A network request is possible only when perform_request is
explicitly called after the V-02 Owner connected preflight.
"""
from __future__ import annotations

import copy
import http.client
import json
import math
import re
import ssl
from typing import Any, Callable

HOST = "api.cloudflare.com"
BASE_PATH_TEMPLATE = "/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1"
CHAT_PATH = "/chat/completions"
MODEL_ID = "@cf/nvidia/nemotron-3-120b-a12b"

MAX_REQUEST_BYTES = 8192
MAX_RESPONSE_BYTES = 65536
MAX_COMPLETION_TOKENS = 256
TIMEOUT_SECONDS = 30
MAX_RETRIES = 0
MAX_CONCURRENCY = 1

INPUT_NEURONS_PER_MILLION = 45455
OUTPUT_NEURONS_PER_MILLION = 136364

ACCOUNT_ID_RE = re.compile(r"^[0-9A-Fa-f]{32}$")

SAFE_MESSAGES = {
    "INVALID_REQUEST": "Cloudflare V-02 request is invalid",
    "SECRET_MATERIAL": "secret or account-like material is forbidden in Cloudflare prompt content",
    "REQUEST_TOO_LARGE": "Cloudflare V-02 request exceeds byte ceiling",
    "OUTPUT_LIMIT": "Cloudflare V-02 completion ceiling exceeded",
    "INVALID_ACCOUNT": "Cloudflare V-02 Account ID is invalid",
    "INVALID_SECRET": "Cloudflare V-02 session token is invalid",
    "NETWORK_ERROR": "Cloudflare V-02 network operation failed",
    "REDIRECT": "Cloudflare V-02 redirects are forbidden",
    "AUTH_FAILED": "Cloudflare V-02 authentication or account permission was rejected",
    "COST_REQUIRED": "Cloudflare V-02 encountered a paid or cost-required path",
    "FREE_QUOTA_EXHAUSTED": "Cloudflare Workers AI free allocation is exhausted",
    "CAPACITY_UNAVAILABLE": "Cloudflare Workers AI capacity is unavailable",
    "PAID_PLAN_REQUIRED": "Cloudflare Workers AI model requires a paid plan",
    "QUOTA": "Cloudflare Workers AI quota was exhausted",
    "PROVIDER_ERROR": "Cloudflare Workers AI returned a server error",
    "UNEXPECTED_STATUS": "Cloudflare Workers AI returned an unexpected status",
    "CONTENT_TYPE": "Cloudflare V-02 response content type is invalid",
    "RESPONSE_TOO_LARGE": "Cloudflare V-02 response exceeds byte ceiling",
    "MALFORMED_RESPONSE": "Cloudflare V-02 response is malformed",
    "MODEL_MISMATCH": "Cloudflare V-02 response model does not match accepted lineage",
    "EXTERNAL_CAPABILITY": "Cloudflare V-02 response indicates forbidden tool or external capability use",
    "USAGE_INVALID": "Cloudflare V-02 usage metadata is invalid",
}

class CloudflareTransportError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "Cloudflare V-02 transport rejected")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise CloudflareTransportError(code)

def _contains_secret_like(text: str) -> bool:
    lowered = text.casefold()
    return (
        "authorization:" in lowered
        or "bearer " in lowered
        or "api_token" in lowered
        or "account_id" in lowered
        or ("-----begin " in lowered and "private key-----" in lowered)
    )

def _walk(value: Any):
    stack = [value]
    seen = 0
    while stack:
        item = stack.pop()
        seen += 1
        if seen > 10000:
            _fail("INVALID_REQUEST")
        yield item
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)

def _validate_messages(messages: Any) -> list[dict[str, str]]:
    if not isinstance(messages, list) or not messages or len(messages) > 8:
        _fail("INVALID_REQUEST")
    result = []
    for item in messages:
        if not isinstance(item, dict) or set(item) != {"role", "content"}:
            _fail("INVALID_REQUEST")
        if item["role"] not in {"system", "user"} or not isinstance(item["content"], str):
            _fail("INVALID_REQUEST")
        try:
            item["content"].encode("utf-8")
        except UnicodeEncodeError:
            _fail("INVALID_REQUEST")
        if _contains_secret_like(item["content"]):
            _fail("SECRET_MATERIAL")
        result.append({"role": item["role"], "content": item["content"]})
    return result

def _encode_body(body: dict[str, Any]) -> bytes:
    try:
        return json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
        _fail("INVALID_REQUEST")
    raise AssertionError("unreachable")

def build_request(messages, *, max_completion_tokens=MAX_COMPLETION_TOKENS, response_format=None):
    before = copy.deepcopy(messages)
    normalized = _validate_messages(messages)
    if isinstance(max_completion_tokens, bool) or not isinstance(max_completion_tokens, int):
        _fail("OUTPUT_LIMIT")
    if not (1 <= max_completion_tokens <= MAX_COMPLETION_TOKENS):
        _fail("OUTPUT_LIMIT")
    if response_format is not None and response_format != {"type": "json_object"}:
        _fail("INVALID_REQUEST")
    body = {
        "model": MODEL_ID,
        "messages": normalized,
        "max_completion_tokens": max_completion_tokens,
        "tool_choice": "none",
        "parallel_tool_calls": False,
        "temperature": 0,
        "stream": False,
        "n": 1,
        "store": False,
    }
    if response_format is not None:
        body["response_format"] = copy.deepcopy(response_format)
    if len(_encode_body(body)) > MAX_REQUEST_BYTES:
        _fail("REQUEST_TOO_LARGE")
    if messages != before:
        _fail("INVALID_REQUEST")
    return body

def _validate_body(body):
    expected = {
        "model", "messages", "max_completion_tokens", "tool_choice",
        "parallel_tool_calls", "temperature", "stream", "n", "store",
    }
    if isinstance(body, dict) and "response_format" in body:
        expected.add("response_format")
    if not isinstance(body, dict) or set(body) != expected:
        _fail("INVALID_REQUEST")
    if body["model"] != MODEL_ID:
        _fail("INVALID_REQUEST")
    _validate_messages(body["messages"])
    value = body["max_completion_tokens"]
    if isinstance(value, bool) or not isinstance(value, int) or not (1 <= value <= MAX_COMPLETION_TOKENS):
        _fail("OUTPUT_LIMIT")
    if body["tool_choice"] != "none" or body["parallel_tool_calls"] is not False:
        _fail("INVALID_REQUEST")
    if body["temperature"] != 0 or body["stream"] is not False or body["n"] != 1 or body["store"] is not False:
        _fail("INVALID_REQUEST")
    if body.get("response_format") not in (None, {"type": "json_object"}):
        _fail("INVALID_REQUEST")

def _validate_account_id(value):
    if not isinstance(value, str) or not ACCOUNT_ID_RE.fullmatch(value):
        _fail("INVALID_ACCOUNT")
    return value

def _validate_secret(value):
    if not isinstance(value, str) or not (16 <= len(value) <= 512):
        _fail("INVALID_SECRET")
    if any(ch.isspace() or ord(ch) < 32 for ch in value):
        _fail("INVALID_SECRET")
    return value

def _path(account_id):
    accepted = _validate_account_id(account_id)
    return f"/client/v4/accounts/{accepted}/ai/v1/chat/completions"

def _default_connection(*, host, timeout, context):
    if host != HOST:
        _fail("INVALID_REQUEST")
    return http.client.HTTPSConnection(host, port=443, timeout=timeout, context=context)

def _header_map(headers):
    result = {}
    if headers is None:
        return result
    for key, value in headers:
        if not isinstance(key, str) or not isinstance(value, str):
            _fail("MALFORMED_RESPONSE")
        result[key.casefold()] = value
    return result

def _load_json_strict(raw):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail("MALFORMED_RESPONSE")
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                _fail("MALFORMED_RESPONSE")
            result[key] = value
        return result
    try:
        value = json.loads(text, object_pairs_hook=hook, parse_constant=lambda _: _fail("MALFORMED_RESPONSE"))
    except CloudflareTransportError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError):
        _fail("MALFORMED_RESPONSE")
    if not isinstance(value, dict):
        _fail("MALFORMED_RESPONSE")
    for item in _walk(value):
        if isinstance(item, float) and not math.isfinite(item):
            _fail("MALFORMED_RESPONSE")
    return value

def _read_bounded(response, headers):
    content_length = headers.get("content-length")
    if content_length is not None:
        if not re.fullmatch(r"[0-9]{1,12}", content_length):
            _fail("MALFORMED_RESPONSE")
        if int(content_length) > MAX_RESPONSE_BYTES:
            _fail("RESPONSE_TOO_LARGE")
    raw = response.read(MAX_RESPONSE_BYTES + 1)
    if not isinstance(raw, (bytes, bytearray)) or len(raw) > MAX_RESPONSE_BYTES:
        _fail("RESPONSE_TOO_LARGE")
    return bytes(raw)

def _error_codes(raw):
    try:
        value = _load_json_strict(raw)
    except CloudflareTransportError:
        return set()
    codes = set()
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            for key, child in item.items():
                if key == "code" and isinstance(child, int) and not isinstance(child, bool):
                    codes.add(child)
                else:
                    stack.append(child)
        elif isinstance(item, list):
            stack.extend(item)
    return codes

def _forbidden_external(value):
    forbidden = {
        "tool_calls", "function_call", "executed_tools", "search_results",
        "citations", "browser_search", "code_interpreter", "mcp_list_tools",
    }
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            for key, child in item.items():
                if key in forbidden and child not in (None, [], {}, ""):
                    return True
                stack.append(child)
        elif isinstance(item, list):
            stack.extend(item)
    return False

def estimate_neurons(input_tokens, output_tokens):
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in (input_tokens, output_tokens)):
        _fail("USAGE_INVALID")
    raw = input_tokens * INPUT_NEURONS_PER_MILLION + output_tokens * OUTPUT_NEURONS_PER_MILLION
    return (raw + 999999) // 1000000

def _usage(value):
    if value is None:
        return {}
    if not isinstance(value, dict):
        _fail("USAGE_INVALID")
    result = {}
    for names, target in [
        (("prompt_tokens", "input_tokens"), "input_tokens"),
        (("completion_tokens", "output_tokens"), "output_tokens"),
        (("total_tokens",), "total_tokens"),
    ]:
        seen = []
        for name in names:
            if name in value:
                number = value[name]
                if isinstance(number, bool) or not isinstance(number, int) or number < 0:
                    _fail("USAGE_INVALID")
                seen.append(number)
        if seen:
            if len(set(seen)) != 1:
                _fail("USAGE_INVALID")
            result[target] = seen[0]
    if all(k in result for k in ("input_tokens", "output_tokens", "total_tokens")):
        if result["total_tokens"] != result["input_tokens"] + result["output_tokens"]:
            _fail("USAGE_INVALID")
    return result

def _normalize_success(value):
    if value.get("model") != MODEL_ID:
        _fail("MODEL_MISMATCH")
    if _forbidden_external(value):
        _fail("EXTERNAL_CAPABILITY")
    choices = value.get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        _fail("MALFORMED_RESPONSE")
    choice = choices[0]
    if not isinstance(choice, dict) or choice.get("finish_reason") != "stop":
        _fail("MALFORMED_RESPONSE")
    message = choice.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        _fail("MALFORMED_RESPONSE")
    content = message["content"]
    try:
        content.encode("utf-8")
    except UnicodeEncodeError:
        _fail("MALFORMED_RESPONSE")
    usage = _usage(value.get("usage"))
    estimated = None
    if "input_tokens" in usage and "output_tokens" in usage:
        estimated = estimate_neurons(usage["input_tokens"], usage["output_tokens"])
    return {
        "status": 200,
        "model": MODEL_ID,
        "finish_reason": "stop",
        "content": content,
        "usage": usage,
        "estimated_neurons": estimated,
        "model_identity_verified": True,
        "transport_identity_verified": True,
        "account_identity_verified": True,
        "host": HOST,
        "path_template": BASE_PATH_TEMPLATE + CHAT_PATH,
        "retry_count": 0,
    }

def perform_request(account_id, secret, body, *, connection_factory=None):
    accepted_account = _validate_account_id(account_id)
    accepted_secret = _validate_secret(secret)
    before = copy.deepcopy(body)
    _validate_body(body)
    payload = _encode_body(body)
    if len(payload) > MAX_REQUEST_BYTES:
        _fail("REQUEST_TOO_LARGE")
    factory = connection_factory or _default_connection
    connection = None
    try:
        context = ssl.create_default_context()
        connection = factory(host=HOST, timeout=TIMEOUT_SECONDS, context=context)
        headers = {
            "Authorization": "Bearer " + accepted_secret,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "GAME-STUDIO-009V-02/1.0",
        }
        connection.request("POST", _path(accepted_account), body=payload, headers=headers)
        response = connection.getresponse()
        status = getattr(response, "status", None)
        if not isinstance(status, int):
            _fail("UNEXPECTED_STATUS")
        response_headers = _header_map(response.getheaders())
        if 300 <= status <= 399:
            _fail("REDIRECT")
        raw = _read_bounded(response, response_headers)
        codes = _error_codes(raw) if status != 200 else set()
        if status == 402:
            _fail("COST_REQUIRED")
        if status in {401, 403}:
            if 5035 in codes:
                _fail("PAID_PLAN_REQUIRED")
            _fail("AUTH_FAILED")
        if status == 429:
            if 3036 in codes:
                _fail("FREE_QUOTA_EXHAUSTED")
            if 3040 in codes:
                _fail("CAPACITY_UNAVAILABLE")
            _fail("QUOTA")
        if 500 <= status <= 599:
            _fail("PROVIDER_ERROR")
        if status != 200:
            _fail("UNEXPECTED_STATUS")
        content_type = response_headers.get("content-type", "")
        if not content_type.casefold().startswith("application/json"):
            _fail("CONTENT_TYPE")
        value = _load_json_strict(raw)
        result = _normalize_success(value)
        if body != before:
            _fail("INVALID_REQUEST")
        return result
    except CloudflareTransportError:
        raise
    except Exception:
        _fail("NETWORK_ERROR")
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
