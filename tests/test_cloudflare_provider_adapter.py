from __future__ import annotations
import copy
import unittest
from scripts import cloudflare_workers_ai_adapter as cf


def request():
    return {
        "model": cf.MODEL_ID,
        "data_classification": "PUBLIC",
        "messages": [{"role": "user", "content": "synthetic hello"}],
        "estimated_input_tokens": 100,
        "max_output_tokens": 64,
        "local_tools": [{"name": "lookup_fixture", "description": "Read an accepted local fixture"}],
        "built_in_tools": [],
        "remote_mcp": [],
        "storage_services": [],
        "ai_gateway": False,
        "third_party_routing": False,
    }


def response():
    return {
        "synthetic": True,
        "model": cf.MODEL_ID,
        "output_text": "synthetic result",
        "tool_requests": [],
        "usage": {"input_tokens": 100, "output_tokens": 20},
        "stop_reason": "stop",
    }

class CloudflareProviderAdapterTests(unittest.TestCase):
    def assert_code(self, code, func, *args):
        with self.assertRaises(cf.CloudflareAdapterError) as cm:
            func(*args)
        self.assertEqual(cm.exception.code, code)

    def test_01_normalize_valid_request(self):
        src = request(); before = copy.deepcopy(src)
        out = cf.normalize_request(src)
        self.assertEqual(src, before); self.assertEqual(out["model"], cf.MODEL_ID)

    def test_02_reject_model(self):
        x = request(); x["model"] = "other"
        self.assert_code("MODEL_NOT_ALLOWLISTED", cf.normalize_request, x)

    def test_03_reject_data(self):
        x = request(); x["data_classification"] = "INTERNAL"
        self.assert_code("DATA_NOT_ALLOWED", cf.normalize_request, x)

    def test_04_reject_input_limit(self):
        x = request(); x["estimated_input_tokens"] = 16385
        self.assert_code("INPUT_LIMIT", cf.normalize_request, x)

    def test_05_reject_output_limit(self):
        x = request(); x["max_output_tokens"] = 4097
        self.assert_code("OUTPUT_LIMIT", cf.normalize_request, x)

    def test_06_reject_builtin_tool(self):
        x = request(); x["built_in_tools"] = ["browser"]
        self.assert_code("BUILTIN_TOOL_FORBIDDEN", cf.normalize_request, x)

    def test_07_reject_remote_mcp(self):
        x = request(); x["remote_mcp"] = ["remote"]
        self.assert_code("REMOTE_MCP_FORBIDDEN", cf.normalize_request, x)

    def test_08_reject_storage(self):
        x = request(); x["storage_services"] = ["R2"]
        self.assert_code("STORAGE_FORBIDDEN", cf.normalize_request, x)

    def test_09_reject_ai_gateway(self):
        x = request(); x["ai_gateway"] = True
        self.assert_code("AI_GATEWAY_FORBIDDEN", cf.normalize_request, x)

    def test_10_reject_third_party_routing(self):
        x = request(); x["third_party_routing"] = True
        self.assert_code("THIRD_PARTY_ROUTING_FORBIDDEN", cf.normalize_request, x)

    def test_11_reject_raw_account_field(self):
        x = request(); x["account_id"] = "not-allowed"
        self.assert_code("SECRET_MATERIAL", cf.normalize_request, x)

    def test_12_tool_definition_valid(self):
        out = cf.normalize_request(request())
        self.assertEqual(out["local_tools"][0]["name"], "lookup_fixture")

    def test_13_tool_definition_invalid(self):
        x = request(); x["local_tools"] = [{"name": "bad space", "description": "x"}]
        self.assert_code("LOCAL_TOOL_INVALID", cf.normalize_request, x)

    def test_14_estimate_neurons_deterministic(self):
        self.assertEqual(cf.estimate_neurons(1000, 1000), 182)

    def test_15_quota_evidence_valid(self):
        out = cf.normalize_quota_evidence({"synthetic": True, "consumed_neurons": 7000, "provider_free_neurons": 10000, "game_daily_neurons": 8000})
        self.assertEqual(out["game_remaining_neurons"], 1000)

    def test_16_quota_game_limit(self):
        self.assert_code("QUOTA_LIMIT", cf.normalize_quota_evidence, {"synthetic": True, "consumed_neurons": 8001, "provider_free_neurons": 10000, "game_daily_neurons": 8000})

    def test_17_error_3036(self):
        self.assertEqual(cf.normalize_error({"synthetic": True, "http_status": 429, "internal_code": 3036})["error_code"], "FREE_QUOTA_EXHAUSTED")

    def test_18_error_3040(self):
        self.assertEqual(cf.normalize_error({"synthetic": True, "http_status": 429, "internal_code": 3040})["error_code"], "CAPACITY_UNAVAILABLE")

    def test_19_error_5035(self):
        self.assertEqual(cf.normalize_error({"synthetic": True, "http_status": 403, "internal_code": 5035})["error_code"], "PAID_PLAN_REQUIRED")

    def test_20_unknown_error_no_retry(self):
        out = cf.normalize_error({"synthetic": True, "http_status": 500, "internal_code": 1})
        self.assertEqual(out["error_code"], "PROVIDER_ERROR"); self.assertFalse(out["retry_allowed"])

    def test_21_synthetic_response_valid(self):
        src = response(); before = copy.deepcopy(src)
        out = cf.normalize_synthetic_response(src)
        self.assertEqual(src, before); self.assertEqual(out["network_activity"], "NONE")

    def test_22_reject_real_response(self):
        x = response(); x["synthetic"] = False
        self.assert_code("SYNTHETIC_REQUIRED", cf.normalize_synthetic_response, x)

    def test_23_reject_response_model(self):
        x = response(); x["model"] = "other"
        self.assert_code("MODEL_NOT_ALLOWLISTED", cf.normalize_synthetic_response, x)

    def test_24_plan_tool_request_not_executed(self):
        x = response(); x["stop_reason"] = "tool_request"; x["tool_requests"] = [{"id": "call_1", "name": "lookup_fixture", "arguments": {"id": "fixture-1"}}]
        out = cf.plan_local_tool_requests(x, ["lookup_fixture"])
        self.assertEqual(out[0]["execution"], "NOT_EXECUTED")

    def test_25_reject_unapproved_tool_request(self):
        x = response(); x["stop_reason"] = "tool_request"; x["tool_requests"] = [{"id": "call_1", "name": "danger", "arguments": {}}]
        self.assert_code("LOCAL_TOOL_NOT_ALLOWED", cf.plan_local_tool_requests, x, ["lookup_fixture"])

# STUDIO-009V-02 live-policy additions.
import json as _v02_json
from pathlib import Path as _V02Path
_V02_ROOT = _V02Path(__file__).resolve().parents[1]
_V02_PROVIDER = _V02_ROOT / "platform/connectivity/providers/cloudflare-workers-ai"


def _v02_chain():
    return [
        _v02_json.loads((_V02_PROVIDER / "provider-profile.json").read_text(encoding="utf-8")),
        _v02_json.loads((_V02_PROVIDER / "child-contract-evidence.json").read_text(encoding="utf-8")),
        _v02_json.loads((_V02_PROVIDER / "model-profile-nemotron-3-super.json").read_text(encoding="utf-8")),
        _v02_json.loads((_V02_PROVIDER / "transport-policy.json").read_text(encoding="utf-8")),
        _v02_json.loads((_V02_PROVIDER / "data-policy.json").read_text(encoding="utf-8")),
        _v02_json.loads((_V02_PROVIDER / "quota-policy.json").read_text(encoding="utf-8")),
        _v02_json.loads((_V02_PROVIDER / "budget-policy.json").read_text(encoding="utf-8")),
    ]

class CloudflareV02AdapterTests(unittest.TestCase):
    def _load(self,name): return _v02_json.loads((_V02_PROVIDER/name).read_text(encoding="utf-8"))
    def test_26_v02_live_policy_valid(self):
        out=cf.validate_live_validation_policy(self._load("live-validation-policy.json"))
        self.assertEqual(out["connected_validation_authority"],"STUDIO-009V-02_ONLY")
    def test_27_static_chain_accepts_v02_transport_data(self):
        self.assertEqual(cf.validate_static_chain(*_v02_chain())["provider_state"],"DISABLED")
    def test_28_old_transport_activation_rejected(self):
        args=_v02_chain(); args[3]["network_activation"]="STUDIO-009F_ONLY"
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_static_chain(*args)
        self.assertEqual(cm.exception.code,"POLICY_MISMATCH")
    def test_29_old_data_activation_rejected(self):
        args=_v02_chain(); args[4]["connected_activation"]="STUDIO-009F_ONLY"
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_static_chain(*args)
        self.assertEqual(cm.exception.code,"DATA_NOT_ALLOWED")
    def test_30_live_policy_paid_broadening_rejected(self):
        value=self._load("live-validation-policy.json"); value["paid_fallback_allowed"]=True
        with self.assertRaises(cf.CloudflareAdapterError): cf.validate_live_validation_policy(value)
