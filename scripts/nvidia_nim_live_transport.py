#!/usr/bin/env python3
"""Direct NVIDIA-hosted NIM HTTPS transport for STUDIO-009V-03.

Import is offline. Network I/O occurs only when perform_request is explicitly
called after the separate Owner connected preflight.
"""
from __future__ import annotations

import copy
import http.client
import json
import math
import re
import ssl
from typing import Any

HOST = "integrate.api.nvidia.com"
PATH = "/v1/chat/completions"
MODEL_ID = "deepseek-ai/deepseek-v4-pro-0813"

MAX_ESTIMATED_INPUT_TOKENS = 4096
MAX_REQUEST_BYTES = 32768
MAX_RESPONSE_BYTES = 131072
MAX_COMPLETION_TOKENS = 512
TIMEOUT_SECONDS = 60
MAX_RETRIES = 0
MAX_CONCURRENCY = 1

SAFE_MESSAGES = {
    "INVALID_REQUEST": "NVIDIA V-03 request is invalid",
    "SECRET_MATERIAL": "secret-like material is forbidden in NVIDIA V-03 prompt content",
    "INPUT_LIMIT": "NVIDIA V-03 estimated input exceeds first-campaign ceiling",
    "OUTPUT_LIMIT": "NVIDIA V-03 completion ceiling exceeded",
    "REQUEST_TOO_LARGE": "NVIDIA V-03 request exceeds byte ceiling",
    "INVALID_SECRET": "NVIDIA V-03 session credential is invalid",
    "NETWORK_ERROR": "NVIDIA V-03 network operation failed",
    "REDIRECT": "NVIDIA V-03 redirects are forbidden",
    "AUTH_FAILURE": "NVIDIA V-03 authentication or authorization failed",
    "PAID_PATH_REQUIRED": "NVIDIA V-03 encountered a paid or billing-required path",
    "REQUEST_VALIDATION_FAILURE": "NVIDIA V-03 request validation failed",
    "RATE_LIMIT_OR_CAPACITY": "NVIDIA V-03 rate limit, capacity, or entitlement prevented execution",
    "PROVIDER_EXECUTION_FAILURE": "NVIDIA V-03 provider execution failed",
    "UNEXPECTED_STATUS": "NVIDIA V-03 provider returned an unexpected status",
    "CONTENT_TYPE": "NVIDIA V-03 response content type is invalid",
    "RESPONSE_TOO_LARGE": "NVIDIA V-03 response exceeds byte ceiling",
    "MALFORMED_RESPONSE": "NVIDIA V-03 response is malformed",
    "MODEL_MISMATCH": "NVIDIA V-03 response model does not match accepted lineage",
    "EXTERNAL_CAPABILITY": "NVIDIA V-03 response indicates forbidden tool or external capability use",
    "USAGE_INVALID": "NVIDIA V-03 usage metadata is invalid",
    "TIMEOUT": "NVIDIA V-03 request timed out",
}

class NvidiaNimTransportError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "NVIDIA V-03 transport rejected")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise NvidiaNimTransportError(code)

def _contains_secret_like(text: str) -> bool:
    lowered = text.casefold()
    return (
        "authorization:" in lowered
        or "bearer " in lowered
        or "api_key" in lowered
        or "private key" in lowered
        or "credential_value" in lowered
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
    out = []
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
        out.append({"role": item["role"], "content": item["content"]})
    return out

def _bounded_int(value: Any, low: int, high: int, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not (low <= value <= high):
        _fail(code)
    return value

def _encode_body(body: dict[str, Any]) -> bytes:
    try:
        return json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
        _fail("INVALID_REQUEST")
    raise AssertionError("unreachable")

def build_request(
    messages: Any,
    *,
    estimated_input_tokens: int,
    max_tokens: int = 128,
    response_format: dict[str, str] | None = None,
) -> dict[str, Any]:
    before = copy.deepcopy(messages)
    normalized = _validate_messages(messages)
    _bounded_int(estimated_input_tokens, 0, MAX_ESTIMATED_INPUT_TOKENS, "INPUT_LIMIT")
    _bounded_int(max_tokens, 1, MAX_COMPLETION_TOKENS, "OUTPUT_LIMIT")
    if response_format is not None and response_format != {"type": "json_object"}:
        _fail("INVALID_REQUEST")
    body = {
        "model": MODEL_ID,
        "messages": normalized,
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": False,
    }
    if response_format is not None:
        body["response_format"] = copy.deepcopy(response_format)
    if len(_encode_body(body)) > MAX_REQUEST_BYTES:
        _fail("REQUEST_TOO_LARGE")
    if messages != before:
        _fail("INVALID_REQUEST")
    return body

def _validate_body(body: Any) -> None:
    if not isinstance(body, dict):
        _fail("INVALID_REQUEST")
    expected = {"model", "messages", "max_tokens", "temperature", "stream"}
    if "response_format" in body:
        expected.add("response_format")
    if set(body) != expected:
        _fail("INVALID_REQUEST")
    if body["model"] != MODEL_ID:
        _fail("INVALID_REQUEST")
    _validate_messages(body["messages"])
    _bounded_int(body["max_tokens"], 1, MAX_COMPLETION_TOKENS, "OUTPUT_LIMIT")
    if body["temperature"] != 0 or body["stream"] is not False:
        _fail("INVALID_REQUEST")
    if body.get("response_format") not in (None, {"type": "json_object"}):
        _fail("INVALID_REQUEST")

def _validate_secret(value: Any) -> str:
    if not isinstance(value, str) or not (16 <= len(value) <= 512):
        _fail("INVALID_SECRET")
    if any(ch.isspace() or ord(ch) < 32 for ch in value):
        _fail("INVALID_SECRET")
    return value

def _default_connection(*, host: str, timeout: int, context):
    if host != HOST:
        _fail("INVALID_REQUEST")
    return http.client.HTTPSConnection(host, port=443, timeout=timeout, context=context)

def _header_map(headers: Any) -> dict[str, str]:
    result = {}
    if headers is None:
        return result
    for key, value in headers:
        if not isinstance(key, str) or not isinstance(value, str):
            _fail("MALFORMED_RESPONSE")
        result[key.casefold()] = value
    return result

def _read_bounded(response: Any, headers: dict[str, str]) -> bytes:
    length = headers.get("content-length")
    if length is not None:
        if not re.fullmatch(r"[0-9]{1,12}", length):
            _fail("MALFORMED_RESPONSE")
        if int(length) > MAX_RESPONSE_BYTES:
            _fail("RESPONSE_TOO_LARGE")
    raw = response.read(MAX_RESPONSE_BYTES + 1)
    if not isinstance(raw, (bytes, bytearray)) or len(raw) > MAX_RESPONSE_BYTES:
        _fail("RESPONSE_TOO_LARGE")
    return bytes(raw)

def _load_json_strict(raw: bytes) -> dict[str, Any]:
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
        value = json.loads(
            text,
            object_pairs_hook=hook,
            parse_constant=lambda _: _fail("MALFORMED_RESPONSE"),
        )
    except NvidiaNimTransportError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError):
        _fail("MALFORMED_RESPONSE")
    if not isinstance(value, dict):
        _fail("MALFORMED_RESPONSE")
    for item in _walk(value):
        if isinstance(item, float) and not math.isfinite(item):
            _fail("MALFORMED_RESPONSE")
    return value

def _usage(value: Any) -> dict[str, int]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        _fail("USAGE_INVALID")
    result = {}
    mapping = {
        "prompt_tokens": "input_tokens",
        "completion_tokens": "output_tokens",
        "total_tokens": "total_tokens",
    }
    for src, dst in mapping.items():
        if src in value:
            number = value[src]
            if isinstance(number, bool) or not isinstance(number, int) or number < 0:
                _fail("USAGE_INVALID")
            result[dst] = number
    if all(k in result for k in ("input_tokens", "output_tokens", "total_tokens")):
        if result["total_tokens"] != result["input_tokens"] + result["output_tokens"]:
            _fail("USAGE_INVALID")
    return result

def _external_capability(value: dict[str, Any]) -> bool:
    forbidden = {
        "tool_calls", "function_call", "executed_tools", "search_results",
        "browser_search", "code_interpreter", "mcp_list_tools",
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

def _normalize_success(value: dict[str, Any]) -> dict[str, Any]:
    if value.get("model") != MODEL_ID:
        _fail("MODEL_MISMATCH")
    if _external_capability(value):
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
    if message.get("tool_calls") not in (None, [], {}):
        _fail("EXTERNAL_CAPABILITY")
    content = message["content"]
    try:
        content.encode("utf-8")
    except UnicodeEncodeError:
        _fail("MALFORMED_RESPONSE")
    return {
        "status": 200,
        "model": MODEL_ID,
        "finish_reason": "stop",
        "content": content,
        "usage": _usage(value.get("usage")),
        "model_identity_verified": True,
        "transport_identity_verified": True,
        "host": HOST,
        "path": PATH,
        "retry_count": 0,
    }

def perform_request(secret: str, body: dict[str, Any], *, connection_factory=None) -> dict[str, Any]:
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
            "User-Agent": "GAME-STUDIO-009V-03/1.0",
        }
        connection.request("POST", PATH, body=payload, headers=headers)
        response = connection.getresponse()
        status = getattr(response, "status", None)
        if not isinstance(status, int):
            _fail("UNEXPECTED_STATUS")
        response_headers = _header_map(response.getheaders())
        if 300 <= status <= 399:
            _fail("REDIRECT")
        raw = _read_bounded(response, response_headers)
        if status == 402:
            _fail("PAID_PATH_REQUIRED")
        if status in {401, 403}:
            _fail("AUTH_FAILURE")
        if status in {400, 422}:
            _fail("REQUEST_VALIDATION_FAILURE")
        if status == 429:
            _fail("RATE_LIMIT_OR_CAPACITY")
        if 500 <= status <= 599:
            _fail("PROVIDER_EXECUTION_FAILURE")
        if status != 200:
            _fail("UNEXPECTED_STATUS")
        content_type = response_headers.get("content-type", "")
        if not content_type.casefold().startswith("application/json"):
            _fail("CONTENT_TYPE")
        result = _normalize_success(_load_json_strict(raw))
        if body != before:
            _fail("INVALID_REQUEST")
        return result
    except NvidiaNimTransportError:
        raise
    except TimeoutError:
        _fail("TIMEOUT")
    except (OSError, ssl.SSLError, http.client.HTTPException):
        _fail("NETWORK_ERROR")
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
