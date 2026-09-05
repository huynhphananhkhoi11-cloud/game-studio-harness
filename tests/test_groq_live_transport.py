from __future__ import annotations

import copy
import inspect
import json
import unittest

from scripts import groq_live_transport as live

SECRET = "synthetic-secret-material-1234567890"

def valid_body():
    return live.build_request(
        [{"role": "user", "content": "Return synthetic JSON only."}],
        response_format={"type": "json_object"},
    )

def response_payload(**overrides):
    value = {
        "id": "chatcmpl_synthetic",
        "object": "chat.completion",
        "model": live.MODEL_ID,
        "service_tier": "on_demand",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": '{"status":"ok"}'},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    value.update(overrides)
    return value

class FakeResponse:
    def __init__(self, status=200, body=None, headers=None):
        self.status = status
        if body is None:
            body = json.dumps(response_payload()).encode()
        self.body = body
        self.headers = headers or [
            ("Content-Type", "application/json"),
            ("x-ratelimit-limit-requests", "1000"),
            ("x-ratelimit-remaining-requests", "999"),
        ]
    def getheaders(self):
        return list(self.headers)
    def read(self, n):
        return self.body[:n]

class FakeConnection:
    def __init__(self, response):
        self.response = response
        self.requests = []
        self.closed = False
    def request(self, method, path, body=None, headers=None):
        self.requests.append((method, path, body, dict(headers or {})))
    def getresponse(self):
        return self.response
    def close(self):
        self.closed = True

def factory_for(response, holder=None):
    def factory(**kwargs):
        conn = FakeConnection(response)
        if holder is not None:
            holder.append(conn)
        return conn
    return factory

class GroqLiveTransportTests(unittest.TestCase):
    def assertCode(self, code, fn):
        with self.assertRaises(live.GroqTransportError) as ctx:
            fn()
        self.assertEqual(ctx.exception.code, code)
        self.assertNotIn(SECRET, ctx.exception.safe_message)

    def test_01_source_uses_stdlib_transport_only(self):
        source = inspect.getsource(live)
        self.assertIn("http.client", source)
        self.assertIn("ssl.create_default_context", source)
        for token in ("import requests", "import httpx", "import aiohttp", "os.environ", "getenv(", ".env", "subprocess"):
            self.assertNotIn(token, source)

    def test_02_constants(self):
        self.assertEqual(live.HOST, "api.groq.com")
        self.assertEqual(live.PATH, "/openai/v1/chat/completions")
        self.assertEqual(live.MODEL_ID, "openai/gpt-oss-120b")
        self.assertEqual(live.MAX_RETRIES, 0)
        self.assertEqual(live.MAX_CONCURRENCY, 1)

    def test_03_build_request_locks_external_capabilities(self):
        body = valid_body()
        self.assertEqual(body["tool_choice"], "none")
        self.assertFalse(body["parallel_tool_calls"])
        self.assertEqual(body["citation_options"], "disabled")
        self.assertFalse(body["include_reasoning"])
        self.assertEqual(body["service_tier"], "on_demand")
        self.assertNotIn("tools", body)

    def test_04_invalid_message_role(self):
        self.assertCode("INVALID_REQUEST", lambda: live.build_request([{"role": "tool", "content": "x"}]))

    def test_05_secret_like_prompt_rejected(self):
        self.assertCode(
            "SECRET_MATERIAL",
            lambda: live.build_request([{"role": "user", "content": "Authorization: Bearer abcdefghijklmnop"}]),
        )

    def test_06_completion_ceiling(self):
        self.assertCode(
            "OUTPUT_LIMIT",
            lambda: live.build_request([{"role": "user", "content": "synthetic"}], max_completion_tokens=257),
        )

    def test_07_request_byte_ceiling(self):
        self.assertCode(
            "REQUEST_TOO_LARGE",
            lambda: live.build_request([{"role": "user", "content": "x" * 9000}]),
        )

    def test_08_success_normalizes_without_headers_or_secret(self):
        result = live.perform_request(
            SECRET, valid_body(), connection_factory=factory_for(FakeResponse())
        )
        self.assertEqual(result["model"], live.MODEL_ID)
        self.assertTrue(result["transport_identity_verified"])
        self.assertNotIn("authorization", json.dumps(result).casefold())
        self.assertNotIn(SECRET, json.dumps(result))

    def test_09_response_model_mismatch(self):
        payload = response_payload(model="other/model")
        self.assertCode(
            "MODEL_MISMATCH",
            lambda: live.perform_request(
                SECRET, valid_body(),
                connection_factory=factory_for(FakeResponse(body=json.dumps(payload).encode())),
            ),
        )

    def test_10_tool_calls_rejected(self):
        payload = response_payload()
        payload["choices"][0]["message"]["tool_calls"] = [{"id": "call_x"}]
        self.assertCode(
            "EXTERNAL_CAPABILITY",
            lambda: live.perform_request(
                SECRET, valid_body(),
                connection_factory=factory_for(FakeResponse(body=json.dumps(payload).encode())),
            ),
        )

    def test_11_citations_rejected(self):
        payload = response_payload()
        payload["choices"][0]["message"]["citations"] = [{"url": "https://example.invalid"}]
        self.assertCode(
            "EXTERNAL_CAPABILITY",
            lambda: live.perform_request(
                SECRET, valid_body(),
                connection_factory=factory_for(FakeResponse(body=json.dumps(payload).encode())),
            ),
        )

    def test_12_redirect_rejected(self):
        self.assertCode(
            "REDIRECT",
            lambda: live.perform_request(
                SECRET, valid_body(), connection_factory=factory_for(FakeResponse(status=302))
            ),
        )

    def test_13_auth_rejected_safely(self):
        self.assertCode(
            "AUTH_FAILED",
            lambda: live.perform_request(
                SECRET, valid_body(), connection_factory=factory_for(FakeResponse(status=401, body=b"secret body"))
            ),
        )

    def test_14_quota_rejected_without_retry(self):
        holder = []
        self.assertCode(
            "QUOTA",
            lambda: live.perform_request(
                SECRET, valid_body(), connection_factory=factory_for(FakeResponse(status=429), holder)
            ),
        )
        self.assertEqual(len(holder[0].requests), 1)

    def test_15_server_error_is_one_attempt_and_connection_closes(self):
        holder = []
        self.assertCode(
            "PROVIDER_ERROR",
            lambda: live.perform_request(
                SECRET, valid_body(), connection_factory=factory_for(FakeResponse(status=503), holder)
            ),
        )
        self.assertEqual(len(holder[0].requests), 1)
        self.assertTrue(holder[0].closed)

    def test_16_oversized_response(self):
        huge = b"{" + b"x" * (live.MAX_RESPONSE_BYTES + 10)
        self.assertCode(
            "RESPONSE_TOO_LARGE",
            lambda: live.perform_request(
                SECRET, valid_body(),
                connection_factory=factory_for(FakeResponse(body=huge, headers=[("Content-Type", "application/json")]))
            ),
        )

    def test_17_malformed_json(self):
        self.assertCode(
            "MALFORMED_RESPONSE",
            lambda: live.perform_request(
                SECRET, valid_body(),
                connection_factory=factory_for(FakeResponse(body=b"{not-json"))
            ),
        )

    def test_18_service_tier_mismatch(self):
        payload = response_payload(service_tier="flex")
        self.assertCode(
            "SERVICE_TIER_MISMATCH",
            lambda: live.perform_request(
                SECRET, valid_body(),
                connection_factory=factory_for(FakeResponse(body=json.dumps(payload).encode())),
            ),
        )
