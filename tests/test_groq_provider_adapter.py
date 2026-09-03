from __future__ import annotations

import copy
import inspect
import unittest

from scripts import groq_provider_adapter as ga


def valid_request():
    return {
        "model": "openai/gpt-oss-120b",
        "data_classification": "PUBLIC",
        "messages": [{"role": "user", "content": "synthetic public test"}],
        "estimated_input_tokens": 100,
        "max_output_tokens": 256,
        "local_tools": [],
        "built_in_tools": [],
        "remote_mcp": [],
    }


def valid_response():
    return {
        "synthetic": True,
        "model": "openai/gpt-oss-120b",
        "output_text": "synthetic response",
        "finish_reason": "stop",
        "usage": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120},
        "tool_calls": [],
    }


class GroqProviderAdapterTests(unittest.TestCase):
    def assertCode(self, code, fn):
        with self.assertRaises(ga.GroqAdapterError) as ctx:
            fn()
        self.assertEqual(ctx.exception.code, code)
        self.assertNotIn("synthetic public test", ctx.exception.safe_message)

    def test_01_source_has_no_network_or_secret_runtime(self):
        source = inspect.getsource(ga)
        forbidden = (
            "import socket", "import requests", "urllib.request", "import httpx",
            "import aiohttp", "import grpc", "import websocket", "import subprocess",
            "import keyring", "os.environ", "getenv(", ".env",
        )
        for token in forbidden:
            self.assertNotIn(token, source)

    def test_02_constants_lock_exact_provider_model(self):
        self.assertEqual(ga.MODEL_ID, "openai/gpt-oss-120b")
        self.assertEqual(ga.HOST, "api.groq.com")
        self.assertEqual(ga.BASE_URL, "https://api.groq.com/openai/v1")
        self.assertEqual(ga.MAX_RETRIES, 0)

    def test_03_valid_request_normalizes(self):
        req = valid_request()
        out = ga.normalize_request(req)
        self.assertEqual(out["model"], ga.MODEL_ID)
        self.assertEqual(out["data_classification"], "PUBLIC")

    def test_04_wrong_model_fails(self):
        req = valid_request()
        req["model"] = "qwen/qwen3.8-27b"
        self.assertCode("MODEL_NOT_ALLOWLISTED", lambda: ga.normalize_request(req))

    def test_05_nonpublic_data_fails(self):
        req = valid_request()
        req["data_classification"] = "INTERNAL"
        self.assertCode("DATA_NOT_ALLOWED", lambda: ga.normalize_request(req))

    def test_06_output_limit_fails(self):
        req = valid_request()
        req["max_output_tokens"] = ga.MAX_OUTPUT_TOKENS + 1
        self.assertCode("OUTPUT_LIMIT", lambda: ga.normalize_request(req))

    def test_07_input_estimate_limit_fails(self):
        req = valid_request()
        req["estimated_input_tokens"] = ga.MAX_INPUT_TOKENS + 1
        self.assertCode("INPUT_LIMIT", lambda: ga.normalize_request(req))

    def test_08_builtin_tools_fail(self):
        req = valid_request()
        req["built_in_tools"] = ["browser_search"]
        self.assertCode("BUILTIN_TOOL_FORBIDDEN", lambda: ga.normalize_request(req))

    def test_09_remote_mcp_fails(self):
        req = valid_request()
        req["remote_mcp"] = [{"server": "synthetic"}]
        self.assertCode("REMOTE_MCP_FORBIDDEN", lambda: ga.normalize_request(req))

    def test_10_secret_like_material_fails(self):
        req = valid_request()
        req["messages"][0]["content"] = "api_key=abcdef1234567890"
        self.assertCode("SECRET_MATERIAL", lambda: ga.normalize_request(req))

    def test_11_local_tool_schema_is_bounded(self):
        req = valid_request()
        req["local_tools"] = [{
            "name": "lookup_symbol",
            "description": "read-only synthetic lookup",
            "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}}},
        }]
        out = ga.normalize_request(req)
        self.assertEqual(out["local_tools"][0]["name"], "lookup_symbol")

    def test_12_duplicate_local_tool_name_fails(self):
        req = valid_request()
        tool = {"name": "lookup_symbol", "description": "x", "parameters": {}}
        req["local_tools"] = [copy.deepcopy(tool), copy.deepcopy(tool)]
        self.assertCode("LOCAL_TOOL_INVALID", lambda: ga.normalize_request(req))

    def test_13_valid_synthetic_response_normalizes(self):
        out = ga.normalize_synthetic_response(valid_response())
        self.assertTrue(out["synthetic"])
        self.assertEqual(out["usage"]["total_tokens"], 120)

    def test_14_real_response_shape_is_rejected(self):
        res = valid_response()
        res["synthetic"] = False
        self.assertCode("SYNTHETIC_REQUIRED", lambda: ga.normalize_synthetic_response(res))

    def test_15_response_model_mismatch_fails(self):
        res = valid_response()
        res["model"] = "other/model"
        self.assertCode("MODEL_NOT_ALLOWLISTED", lambda: ga.normalize_synthetic_response(res))

    def test_16_usage_mismatch_fails(self):
        res = valid_response()
        res["usage"]["total_tokens"] = 999
        self.assertCode("USAGE_INVALID", lambda: ga.normalize_synthetic_response(res))

    def test_17_local_tool_request_is_planned_not_executed(self):
        res = valid_response()
        res["finish_reason"] = "tool_calls"
        res["tool_calls"] = [{
            "id": "call_abc123",
            "name": "lookup_symbol",
            "arguments": {"symbol": "route"},
        }]
        normalized = ga.normalize_synthetic_response(res)
        plan = ga.plan_local_tool_requests(normalized, ["lookup_symbol"])
        self.assertEqual(plan[0]["execution"], "NOT_EXECUTED")

    def test_18_unapproved_tool_call_fails(self):
        res = valid_response()
        res["finish_reason"] = "tool_calls"
        res["tool_calls"] = [{
            "id": "call_abc123",
            "name": "write_file",
            "arguments": {"path": "x"},
        }]
        normalized = ga.normalize_synthetic_response(res)
        self.assertCode(
            "LOCAL_TOOL_NOT_ALLOWED",
            lambda: ga.plan_local_tool_requests(normalized, ["lookup_symbol"]),
        )

    def test_19_rate_limit_headers_normalize(self):
        out = ga.normalize_rate_limit_headers({
            "x-ratelimit-limit-requests": "1000",
            "x-ratelimit-remaining-requests": "999",
            "x-ratelimit-limit-tokens": "8000",
            "x-ratelimit-remaining-tokens": "7000",
            "x-ratelimit-reset-requests": "1h2m",
            "x-ratelimit-reset-tokens": "2s",
        })
        self.assertEqual(out["limit_requests_rpd"], 1000)
        self.assertEqual(out["remaining_tokens_tpm"], 7000)

    def test_20_invalid_rate_limit_evidence_fails(self):
        self.assertCode(
            "RATE_LIMIT_INVALID",
            lambda: ga.normalize_rate_limit_headers({
                "x-ratelimit-limit-requests": "100",
                "x-ratelimit-remaining-requests": "101",
            }),
        )

    def test_21_429_maps_to_quota_without_retry(self):
        out = ga.normalize_error(429)
        self.assertEqual(out["normalized_error"], "QUOTA_EXHAUSTED")
        self.assertFalse(out["retry_allowed"])
        self.assertEqual(out["money_ceiling"], 0)

    def test_22_402_maps_to_cost_required(self):
        out = ga.normalize_error(402)
        self.assertEqual(out["normalized_error"], "COST_REQUIRED")
        self.assertFalse(out["paid_fallback_allowed"])

    def test_23_request_input_is_immutable(self):
        req = valid_request()
        before = copy.deepcopy(req)
        ga.normalize_request(req)
        self.assertEqual(req, before)

    def test_24_response_input_is_immutable(self):
        res = valid_response()
        before = copy.deepcopy(res)
        ga.normalize_synthetic_response(res)
        self.assertEqual(res, before)

    def test_25_offline_plan_disables_every_effect(self):
        plan = ga.offline_execution_plan(valid_request())
        self.assertEqual(plan["network"], "DISABLED")
        self.assertEqual(plan["credential_resolution"], "DISABLED")
        self.assertEqual(plan["provider_call"], "DISABLED")
        self.assertEqual(plan["tool_execution"], "DISABLED")
        self.assertEqual(plan["routing"], "DISABLED")
        self.assertEqual(plan["money_ceiling"], 0)
