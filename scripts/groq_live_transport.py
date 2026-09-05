#!/usr/bin/env python3
"""Narrow Groq HTTPS transport for STUDIO-009V-01.

No call occurs on import. Production network access is possible only when
perform_request is explicitly invoked after the V-01 contract gate.
"""
from __future__ import annotations

import copy
import hashlib
import http.client
import json
import math
import re
import ssl
from typing import Any, Callable

HOST = "api.groq.com"
PATH = "/openai/v1/chat/completions"
BASE_URL = "https://api.groq.com/openai/v1"
MODEL_ID = "openai/gpt-oss-120b"
SERVICE_TIER = "on_demand"
TOOL_CHOICE = "none"
CITATION_OPTIONS = "disabled"

MAX_REQUEST_BYTES = 8192
MAX_RESPONSE_BYTES = 65536
MAX_COMPLETION_TOKENS = 256
TIMEOUT_SECONDS = 30
MAX_RETRIES = 0
MAX_CONCURRENCY = 1

SAFE_MESSAGES = {
    "INVALID_REQUEST": "Groq V-01 request is invalid",
    "SECRET_MATERIAL": "secret-like material is forbidden in Groq prompt content",
    "REQUEST_TOO_LARGE": "Groq V-01 request exceeds byte ceiling",
    "OUTPUT_LIMIT": "Groq V-01 completion ceiling exceeded",
    "INVALID_SECRET": "Groq session secret is invalid",
    "NETWORK_ERROR": "Groq V-01 network operation failed",
    "REDIRECT": "Groq V-01 redirects are forbidden",
    "AUTH_FAILED": "Groq V-01 authentication was rejected",
    "COST_REQUIRED": "Groq V-01 encountered a paid/cost-required path",
    "QUOTA": "Groq V-01 quota was exhausted",
    "CAPACITY": "Groq V-01 provider capacity was unavailable",
    "PROVIDER_ERROR": "Groq V-01 provider returned a server error",
    "UNEXPECTED_STATUS": "Groq V-01 provider returned an unexpected status",
    "CONTENT_TYPE": "Groq V-01 response content type is invalid",
    "RESPONSE_TOO_LARGE": "Groq V-01 response exceeds byte ceiling",
    "MALFORMED_RESPONSE": "Groq V-01 response is malformed",
    "MODEL_MISMATCH": "Groq V-01 response model does not match accepted lineage",
    "EXTERNAL_CAPABILITY": "Groq V-01 response indicates forbidden external capability use",
    "SERVICE_TIER_MISMATCH": "Groq V-01 response used an unexpected service tier",
    "QUOTA_HEADER_INVALID": "Groq V-01 quota headers are malformed",
}

class GroqTransportError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "Groq V-01 transport rejected")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise GroqTransportError(code)

def _contains_secret_like(text: str) -> bool:
    lowered = text.casefold()
    if "api_key" in lowered or "authorization:" in lowered or "bearer " in lowered:
        return True
    patterns = (
        r"\bgsk_[A-Za-z0-9_-]{10,}\b",
        r"\bsk-[A-Za-z0-9_-]{16,}\b",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    )
    return any(re.search(pattern, text) for pattern in patterns)

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
    normalized = []
    for message in messages:
        if not isinstance(message, dict) or set(message) != {"role", "content"}:
            _fail("INVALID_REQUEST")
        if message["role"] not in {"system", "user"} or not isinstance(message["content"], str):
            _fail("INVALID_REQUEST")
        try:
            message["content"].encode("utf-8")
        except UnicodeEncodeError:
            _fail("INVALID_REQUEST")
        if _contains_secret_like(message["content"]):
            _fail("SECRET_MATERIAL")
        normalized.append({"role": message["role"], "content": message["content"]})
    return normalized

def build_request(
    messages: list[dict[str, str]],
    *,
    max_completion_tokens: int = MAX_COMPLETION_TOKENS,
    response_format: dict[str, Any] | None = None,
) -> dict[str, Any]:
    before = copy.deepcopy(messages)
    normalized_messages = _validate_messages(messages)
    if isinstance(max_completion_tokens, bool) or not isinstance(max_completion_tokens, int):
        _fail("OUTPUT_LIMIT")
    if not (1 <= max_completion_tokens <= MAX_COMPLETION_TOKENS):
        _fail("OUTPUT_LIMIT")
    if response_format is not None:
        if response_format != {"type": "json_object"}:
            _fail("INVALID_REQUEST")
    body = {
        "model": MODEL_ID,
        "messages": normalized_messages,
        "max_completion_tokens": max_completion_tokens,
        "tool_choice": TOOL_CHOICE,
        "parallel_tool_calls": False,
        "citation_options": CITATION_OPTIONS,
        "service_tier": SERVICE_TIER,
        "reasoning_effort": "low",
        "temperature": 0,
        "stream": False,
        "n": 1,
    }
    if response_format is not None:
        body["response_format"] = copy.deepcopy(response_format)
    raw = _encode_body(body)
    if len(raw) > MAX_REQUEST_BYTES:
        _fail("REQUEST_TOO_LARGE")
    if messages != before:
        _fail("INVALID_REQUEST")
    return body

def _validate_body(body: dict[str, Any]) -> None:
    expected = {
        "model", "messages", "max_completion_tokens", "tool_choice",
        "parallel_tool_calls", "citation_options", "service_tier",
        "reasoning_effort", "temperature", "stream", "n",
    }
    keys = set(body)
    if "response_format" in keys:
        expected.add("response_format")
    if keys != expected:
        _fail("INVALID_REQUEST")
    if body["model"] != MODEL_ID:
        _fail("INVALID_REQUEST")
    if body["tool_choice"] != "none" or body["parallel_tool_calls"] is not False:
        _fail("INVALID_REQUEST")
    if body["citation_options"] != "disabled":
        _fail("INVALID_REQUEST")
    if body["service_tier"] != "on_demand":
        _fail("INVALID_REQUEST")
    if body["stream"] is not False or body["n"] != 1:
        _fail("INVALID_REQUEST")
    _validate_messages(body["messages"])
    if body.get("response_format") not in (None, {"type": "json_object"}):
        _fail("INVALID_REQUEST")
    value = body["max_completion_tokens"]
    if isinstance(value, bool) or not isinstance(value, int) or not (1 <= value <= MAX_COMPLETION_TOKENS):
        _fail("OUTPUT_LIMIT")

def _encode_body(body: dict[str, Any]) -> bytes:
    try:
        raw = json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
        _fail("INVALID_REQUEST")
    return raw

def _default_connection(*, host: str, timeout: int, context: ssl.SSLContext):
    if host != HOST:
        _fail("INVALID_REQUEST")
    return http.client.HTTPSConnection(host, port=443, timeout=timeout, context=context)

def _load_json_strict(raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail("MALFORMED_RESPONSE")
    def hook(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                _fail("MALFORMED_RESPONSE")
            out[key] = value
        return out
    try:
        value = json.loads(
            text, object_pairs_hook=hook, parse_constant=lambda _: _fail("MALFORMED_RESPONSE")
        )
    except GroqTransportError:
        raise
    except (json.JSONDecodeError, ValueError):
        _fail("MALFORMED_RESPONSE")
    if not isinstance(value, dict):
        _fail("MALFORMED_RESPONSE")
    for item in _walk(value):
        if isinstance(item, float) and not math.isfinite(item):
            _fail("MALFORMED_RESPONSE")
    return value

def _header_map(headers: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    if headers is None:
        return result
    for key, value in headers:
        if not isinstance(key, str) or not isinstance(value, str):
            _fail("QUOTA_HEADER_INVALID")
        result[key.casefold()] = value
    return result

def _quota(headers: dict[str, str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    numeric = {
        "x-ratelimit-limit-requests": "limit_requests",
        "x-ratelimit-remaining-requests": "remaining_requests",
        "x-ratelimit-limit-tokens": "limit_tokens",
        "x-ratelimit-remaining-tokens": "remaining_tokens",
    }
    for header, name in numeric.items():
        if header in headers:
            value = headers[header]
            if not re.fullmatch(r"[0-9]{1,12}", value):
                _fail("QUOTA_HEADER_INVALID")
            out[name] = int(value)
    for header, name in (
        ("x-ratelimit-reset-requests", "reset_requests"),
        ("x-ratelimit-reset-tokens", "reset_tokens"),
    ):
        if header in headers:
            value = headers[header]
            if not re.fullmatch(r"[0-9dhms.]{1,64}", value):
                _fail("QUOTA_HEADER_INVALID")
            out[name] = value
    return out

def _forbidden_external_capability(value: Any) -> bool:
    forbidden_keys = {
        "tool_calls", "executed_tools", "mcp_list_tools", "search_results",
        "citations", "browser_search", "code_interpreter",
    }
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            for key, child in item.items():
                if key in forbidden_keys and child not in (None, [], {}, ""):
                    return True
                stack.append(child)
        elif isinstance(item, list):
            stack.extend(item)
    return False

def _normalize_success(value: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    if value.get("model") != MODEL_ID:
        _fail("MODEL_MISMATCH")
    if value.get("service_tier") not in (None, SERVICE_TIER):
        _fail("SERVICE_TIER_MISMATCH")
    if _forbidden_external_capability(value):
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
    usage = value.get("usage")
    normalized_usage = {}
    if usage is not None:
        if not isinstance(usage, dict):
            _fail("MALFORMED_RESPONSE")
        for source, target in (
            ("prompt_tokens", "prompt_tokens"),
            ("completion_tokens", "completion_tokens"),
            ("total_tokens", "total_tokens"),
        ):
            if source in usage:
                number = usage[source]
                if isinstance(number, bool) or not isinstance(number, int) or number < 0:
                    _fail("MALFORMED_RESPONSE")
                normalized_usage[target] = number
    return {
        "status": 200,
        "model": MODEL_ID,
        "service_tier": value.get("service_tier"),
        "finish_reason": "stop",
        "content": content,
        "usage": normalized_usage,
        "quota": _quota(headers),
        "model_identity_verified": True,
        "transport_identity_verified": True,
        "host": HOST,
        "path": PATH,
        "retry_count": 0,
    }

def perform_request(
    secret: str,
    body: dict[str, Any],
    *,
    connection_factory: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(secret, str) or not (16 <= len(secret) <= 512) or any(ch.isspace() for ch in secret):
        _fail("INVALID_SECRET")
    before = copy.deepcopy(body)
    _validate_body(body)
    payload = _encode_body(body)
    if len(payload) > MAX_REQUEST_BYTES:
        _fail("REQUEST_TOO_LARGE")

    factory = connection_factory or _default_connection
    connection = None
    response = None
    try:
        context = ssl.create_default_context()
        connection = factory(host=HOST, timeout=TIMEOUT_SECONDS, context=context)
        headers = {
            "Authorization": "Bearer " + secret,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "GAME-STUDIO-009V-01/1.0",
        }
        connection.request("POST", PATH, body=payload, headers=headers)
        response = connection.getresponse()
        status = getattr(response, "status", None)
        if not isinstance(status, int):
            _fail("UNEXPECTED_STATUS")
        header_map = _header_map(response.getheaders())
        if 300 <= status <= 399:
            _fail("REDIRECT")
        if status in {401, 403}:
            _fail("AUTH_FAILED")
        if status == 402:
            _fail("COST_REQUIRED")
        if status == 429:
            _fail("QUOTA")
        if status == 498:
            _fail("CAPACITY")
        if 500 <= status <= 599:
            _fail("PROVIDER_ERROR")
        if status != 200:
            _fail("UNEXPECTED_STATUS")
        content_type = header_map.get("content-type", "")
        if not content_type.casefold().startswith("application/json"):
            _fail("CONTENT_TYPE")
        content_length = header_map.get("content-length")
        if content_length is not None:
            if not re.fullmatch(r"[0-9]{1,12}", content_length):
                _fail("MALFORMED_RESPONSE")
            if int(content_length) > MAX_RESPONSE_BYTES:
                _fail("RESPONSE_TOO_LARGE")
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        if not isinstance(raw, (bytes, bytearray)) or len(raw) > MAX_RESPONSE_BYTES:
            _fail("RESPONSE_TOO_LARGE")
        value = _load_json_strict(bytes(raw))
        result = _normalize_success(value, header_map)
        if body != before:
            _fail("INVALID_REQUEST")
        return result
    except GroqTransportError:
        raise
    except Exception:
        _fail("NETWORK_ERROR")
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
