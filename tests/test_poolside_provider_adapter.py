from __future__ import annotations

import copy
import unittest

from scripts import poolside_adapter as ps


def request():
    return {
        "model": ps.MODEL_ID,
        "data_classification": "PUBLIC",
        "messages": [{"role": "user", "content": "synthetic hello"}],
        "estimated_input_tokens": 100,
        "max_output_tokens": 64,
        "stream": False,
        "tools": [],
        "remote_mcp": [],
        "acp": [],
        "shell_execution": False,
        "file_access": False,
        "browser": False,
        "url_context": False,
        "routing": False,
        "retries": 0,
        "concurrency": 1,
        "timeout_seconds": 60,
        "pool_cli": False,
        "repository_write": False,
    }


def response():
    return {
        "synthetic": True,
        "model": ps.MODEL_ID,
        "output_text": "synthetic result",
        "usage": {"input_tokens": 100, "output_tokens": 20},
        "finish_reason": "stop",
        "tool_calls": [],
    }


def zero_cost():
    return {
        "synthetic": True,
        "free_limited_offer_visible": True,
        "account_zero_cost_eligible": True,
        "billing_required": False,
        "payment_method_required": False,
        "subscription_required": False,
        "credit_purchase_required": False,
    }


def harness():
    return {
        "pool_cli": False,
        "credential_file_access": False,
        "repository_write": False,
        "tools": [],
        "mcp": [],
        "acp": [],
    }


class PoolsideProviderAdapterTests(unittest.TestCase):
    def assert_code(self, code, func, *args):
        with self.assertRaises(ps.PoolsideAdapterError) as cm:
            func(*args)
        self.assertEqual(cm.exception.code, code)

    def test_01_valid_request(self):
        src = request(); before = copy.deepcopy(src)
        out = ps.normalize_request(src)
        self.assertEqual(src, before)
        self.assertEqual(out["model"], ps.MODEL_ID)
        self.assertEqual(out["network_activity"], "NONE")

    def test_02_model_rejected(self):
        x = request(); x["model"] = "other"
        self.assert_code("MODEL_NOT_ALLOWLISTED", ps.normalize_request, x)

    def test_03_nonpublic_data_rejected(self):
        x = request(); x["data_classification"] = "INTERNAL"
        self.assert_code("DATA_NOT_ALLOWED", ps.normalize_request, x)

    def test_04_input_ceiling(self):
        x = request(); x["estimated_input_tokens"] = 4097
        self.assert_code("INPUT_LIMIT", ps.normalize_request, x)

    def test_05_output_ceiling(self):
        x = request(); x["max_output_tokens"] = 1025
        self.assert_code("OUTPUT_LIMIT", ps.normalize_request, x)

    def test_06_streaming_disabled(self):
        x = request(); x["stream"] = True
        self.assert_code("POLICY_MISMATCH", ps.normalize_request, x)

    def test_07_tools_disabled(self):
        x = request(); x["tools"] = ["browser"]
        self.assert_code("TOOL_FORBIDDEN", ps.normalize_request, x)

    def test_08_remote_mcp_disabled(self):
        x = request(); x["remote_mcp"] = ["remote"]
        self.assert_code("REMOTE_MCP_FORBIDDEN", ps.normalize_request, x)

    def test_09_acp_disabled(self):
        x = request(); x["acp"] = ["agent"]
        self.assert_code("ACP_FORBIDDEN", ps.normalize_request, x)

    def test_10_shell_disabled(self):
        x = request(); x["shell_execution"] = True
        self.assert_code("SHELL_FORBIDDEN", ps.normalize_request, x)

    def test_11_file_access_disabled(self):
        x = request(); x["file_access"] = True
        self.assert_code("FILE_ACCESS_FORBIDDEN", ps.normalize_request, x)

    def test_12_browser_disabled(self):
        x = request(); x["browser"] = True
        self.assert_code("BROWSER_FORBIDDEN", ps.normalize_request, x)

    def test_13_url_context_disabled(self):
        x = request(); x["url_context"] = True
        self.assert_code("URL_CONTEXT_FORBIDDEN", ps.normalize_request, x)

    def test_14_routing_disabled(self):
        x = request(); x["routing"] = True
        self.assert_code("ROUTING_FORBIDDEN", ps.normalize_request, x)

    def test_15_retry_fixed_zero(self):
        x = request(); x["retries"] = 1
        self.assert_code("POLICY_MISMATCH", ps.normalize_request, x)

    def test_16_concurrency_fixed_one(self):
        x = request(); x["concurrency"] = 2
        self.assert_code("POLICY_MISMATCH", ps.normalize_request, x)

    def test_17_timeout_fixed(self):
        x = request(); x["timeout_seconds"] = 61
        self.assert_code("POLICY_MISMATCH", ps.normalize_request, x)

    def test_18_pool_cli_disabled(self):
        x = request(); x["pool_cli"] = True
        self.assert_code("POOL_CLI_FORBIDDEN", ps.normalize_request, x)

    def test_19_repository_write_disabled(self):
        x = request(); x["repository_write"] = True
        self.assert_code("REPOSITORY_WRITE_FORBIDDEN", ps.normalize_request, x)

    def test_20_secret_field_rejected(self):
        x = request(); x["api_key"] = "synthetic-not-a-real-key"
        self.assert_code("SECRET_MATERIAL", ps.normalize_request, x)

    def test_21_secret_like_message_rejected(self):
        x = request(); x["messages"][0]["content"] = "Bearer abcdefghijklmnopqrstuvwxyz"
        self.assert_code("SECRET_MATERIAL", ps.normalize_request, x)

    def test_22_missing_field_rejected(self):
        x = request(); del x["routing"]
        self.assert_code("MISSING_FIELD", ps.normalize_request, x)

    def test_23_extra_field_rejected(self):
        x = request(); x["unexpected"] = False
        self.assert_code("EXTRA_FIELD", ps.normalize_request, x)

    def test_24_messages_must_be_nonempty(self):
        x = request(); x["messages"] = []
        self.assert_code("INVALID_TYPE", ps.normalize_request, x)

    def test_25_role_rejected(self):
        x = request(); x["messages"][0]["role"] = "tool"
        self.assert_code("INVALID_TYPE", ps.normalize_request, x)

    def test_26_content_type_rejected(self):
        x = request(); x["messages"][0]["content"] = 7
        self.assert_code("INVALID_TYPE", ps.normalize_request, x)

    def test_27_request_byte_ceiling(self):
        x = request(); x["messages"][0]["content"] = "x" * 40000
        self.assert_code("REQUEST_TOO_LARGE", ps.normalize_request, x)

    def test_28_request_immutable(self):
        src = request(); before = copy.deepcopy(src)
        ps.normalize_request(src)
        self.assertEqual(src, before)

    def test_29_valid_response(self):
        src = response(); before = copy.deepcopy(src)
        out = ps.normalize_synthetic_response(src)
        self.assertEqual(src, before)
        self.assertEqual(out["provider_runtime_activity"], "NONE")
        self.assertEqual(out["spend_usd"], 0)

    def test_30_real_response_rejected(self):
        x = response(); x["synthetic"] = False
        self.assert_code("SYNTHETIC_REQUIRED", ps.normalize_synthetic_response, x)

    def test_31_response_model_rejected(self):
        x = response(); x["model"] = "other"
        self.assert_code("MODEL_NOT_ALLOWLISTED", ps.normalize_synthetic_response, x)

    def test_32_response_output_usage_rejected(self):
        x = response(); x["usage"]["output_tokens"] = 1025
        self.assert_code("USAGE_INVALID", ps.normalize_synthetic_response, x)

    def test_33_response_input_usage_rejected(self):
        x = response(); x["usage"]["input_tokens"] = 4097
        self.assert_code("USAGE_INVALID", ps.normalize_synthetic_response, x)

    def test_34_finish_reason_rejected(self):
        x = response(); x["finish_reason"] = "tool_calls"
        self.assert_code("RESPONSE_INVALID", ps.normalize_synthetic_response, x)

    def test_35_tool_calls_rejected(self):
        x = response(); x["tool_calls"] = [{"name": "shell"}]
        self.assert_code("UNEXPECTED_CAPABILITY", ps.normalize_synthetic_response, x)

    def test_36_response_immutable(self):
        src = response(); before = copy.deepcopy(src)
        ps.normalize_synthetic_response(src)
        self.assertEqual(src, before)

    def test_37_zero_cost_valid(self):
        out = ps.normalize_zero_cost_evidence(zero_cost())
        self.assertTrue(out["zero_cost_eligible"])
        self.assertEqual(out["money_ceiling"], 0)

    def test_38_free_offer_unproven(self):
        x = zero_cost(); x["free_limited_offer_visible"] = False
        self.assert_code("ZERO_COST_ELIGIBILITY_UNPROVEN", ps.normalize_zero_cost_evidence, x)

    def test_39_account_zero_cost_unproven(self):
        x = zero_cost(); x["account_zero_cost_eligible"] = False
        self.assert_code("ZERO_COST_ELIGIBILITY_UNPROVEN", ps.normalize_zero_cost_evidence, x)

    def test_40_billing_required(self):
        x = zero_cost(); x["billing_required"] = True
        self.assert_code("PAID_PATH_REQUIRED", ps.normalize_zero_cost_evidence, x)

    def test_41_payment_method_required(self):
        x = zero_cost(); x["payment_method_required"] = True
        self.assert_code("PAID_PATH_REQUIRED", ps.normalize_zero_cost_evidence, x)

    def test_42_subscription_required(self):
        x = zero_cost(); x["subscription_required"] = True
        self.assert_code("PAID_PATH_REQUIRED", ps.normalize_zero_cost_evidence, x)

    def test_43_credit_purchase_required(self):
        x = zero_cost(); x["credit_purchase_required"] = True
        self.assert_code("PAID_PATH_REQUIRED", ps.normalize_zero_cost_evidence, x)

    def test_44_real_zero_cost_evidence_rejected(self):
        x = zero_cost(); x["synthetic"] = False
        self.assert_code("SYNTHETIC_REQUIRED", ps.normalize_zero_cost_evidence, x)

    def test_45_401_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 401, "error_type": None})["error_code"], "AUTH_FAILURE")

    def test_46_403_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 403, "error_type": None})["error_code"], "AUTH_FAILURE")

    def test_47_404_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 404, "error_type": None})["error_code"], "NOT_FOUND")

    def test_48_422_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 422, "error_type": None})["error_code"], "REQUEST_VALIDATION_FAILURE")

    def test_49_429_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 429, "error_type": None})["error_code"], "RATE_LIMIT_OR_CAPACITY")

    def test_50_500_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 500, "error_type": None})["error_code"], "PROVIDER_EXECUTION_FAILURE")

    def test_51_503_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": 503, "error_type": None})["error_code"], "PROVIDER_EXECUTION_FAILURE")

    def test_52_timeout_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "timeout"})["error_code"], "TIMEOUT")

    def test_53_malformed_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "malformed"})["error_code"], "MALFORMED_RESPONSE")

    def test_54_redirect_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "redirect"})["error_code"], "REDIRECT_FORBIDDEN")

    def test_55_model_mismatch_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "model_mismatch"})["error_code"], "MODEL_IDENTITY_MISMATCH")

    def test_56_unexpected_tool_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "unexpected_tool"})["error_code"], "UNEXPECTED_CAPABILITY")

    def test_57_terms_drift_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "terms_drift"})["error_code"], "TERMS_DRIFT")

    def test_58_unknown_error_fail_closed(self):
        self.assertEqual(ps.normalize_error({"synthetic": True, "http_status": None, "error_type": "other"})["error_code"], "PROVIDER_EXECUTION_FAILURE")

    def test_59_error_has_no_retry(self):
        out = ps.normalize_error({"synthetic": True, "http_status": 429, "error_type": None})
        self.assertFalse(out["retry_allowed"])
        self.assertFalse(out["tool_activation_allowed"])

    def test_60_error_has_no_paid_or_fallback(self):
        out = ps.normalize_error({"synthetic": True, "http_status": 429, "error_type": None})
        self.assertFalse(out["paid_upgrade_allowed"])
        self.assertFalse(out["model_fallback_allowed"])
        self.assertFalse(out["provider_fallback_allowed"])
        self.assertFalse(out["routing_allowed"])

    def test_61_harness_all_disabled_valid(self):
        out = ps.validate_harness_request(harness())
        self.assertEqual(out["pool_cli_activity"], "NONE")
        self.assertEqual(out["repository_write_activity"], "NONE")

    def test_62_harness_pool_cli_rejected(self):
        x = harness(); x["pool_cli"] = True
        self.assert_code("POOL_CLI_FORBIDDEN", ps.validate_harness_request, x)

    def test_63_harness_credential_file_rejected(self):
        x = harness(); x["credential_file_access"] = True
        self.assert_code("CREDENTIAL_FILE_FORBIDDEN", ps.validate_harness_request, x)

    def test_64_harness_capability_and_write_rejected(self):
        cases = [
            ("repository_write", True, "REPOSITORY_WRITE_FORBIDDEN"),
            ("tools", ["shell"], "TOOL_FORBIDDEN"),
            ("mcp", ["server"], "REMOTE_MCP_FORBIDDEN"),
            ("acp", ["agent"], "ACP_FORBIDDEN"),
        ]
        for field, value, code in cases:
            with self.subTest(field=field):
                x = harness(); x[field] = value
                self.assert_code(code, ps.validate_harness_request, x)
