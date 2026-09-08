from __future__ import annotations
import copy, unittest
from scripts import nvidia_nim_adapter as nv
def request(): return {"model":nv.MODEL_ID,"data_classification":"PUBLIC","messages":[{"role":"user","content":"synthetic hello"}],"estimated_input_tokens":100,"max_output_tokens":64,"stream":False,"tools":[],"remote_mcp":[],"code_execution":False,"file_search":False,"url_context":False,"routing":False,"retries":0,"concurrency":1,"timeout_seconds":60}
def response(): return {"synthetic":True,"model":nv.MODEL_ID,"output_text":"synthetic result","usage":{"input_tokens":100,"output_tokens":20},"finish_reason":"stop"}
class NvidiaNimProviderAdapterTests(unittest.TestCase):
    def assert_code(self,code,func,*args):
        with self.assertRaises(nv.NvidiaNimAdapterError) as cm: func(*args)
        self.assertEqual(cm.exception.code,code)
    def test_01_valid_request(self):
        src=request(); before=copy.deepcopy(src); out=nv.normalize_request(src); self.assertEqual(src,before); self.assertEqual(out["model"],nv.MODEL_ID); self.assertEqual(out["network_activity"],"NONE")
    def test_02_model_rejected(self): x=request(); x["model"]="other"; self.assert_code("MODEL_NOT_ALLOWLISTED",nv.normalize_request,x)
    def test_03_nonpublic_data_rejected(self): x=request(); x["data_classification"]="INTERNAL"; self.assert_code("DATA_NOT_ALLOWED",nv.normalize_request,x)
    def test_04_input_ceiling(self): x=request(); x["estimated_input_tokens"]=32769; self.assert_code("INPUT_LIMIT",nv.normalize_request,x)
    def test_05_output_ceiling(self): x=request(); x["max_output_tokens"]=16385; self.assert_code("OUTPUT_LIMIT",nv.normalize_request,x)
    def test_06_streaming_disabled(self): x=request(); x["stream"]=True; self.assert_code("POLICY_MISMATCH",nv.normalize_request,x)
    def test_07_tools_disabled(self): x=request(); x["tools"]=["browser"]; self.assert_code("TOOL_FORBIDDEN",nv.normalize_request,x)
    def test_08_remote_mcp_disabled(self): x=request(); x["remote_mcp"]=["remote"]; self.assert_code("REMOTE_MCP_FORBIDDEN",nv.normalize_request,x)
    def test_09_code_execution_disabled(self): x=request(); x["code_execution"]=True; self.assert_code("CODE_EXECUTION_FORBIDDEN",nv.normalize_request,x)
    def test_10_file_search_disabled(self): x=request(); x["file_search"]=True; self.assert_code("FILE_SEARCH_FORBIDDEN",nv.normalize_request,x)
    def test_11_url_context_disabled(self): x=request(); x["url_context"]=True; self.assert_code("URL_CONTEXT_FORBIDDEN",nv.normalize_request,x)
    def test_12_routing_disabled(self): x=request(); x["routing"]=True; self.assert_code("ROUTING_FORBIDDEN",nv.normalize_request,x)
    def test_13_retry_fixed_zero(self): x=request(); x["retries"]=1; self.assert_code("POLICY_MISMATCH",nv.normalize_request,x)
    def test_14_concurrency_fixed_one(self): x=request(); x["concurrency"]=2; self.assert_code("POLICY_MISMATCH",nv.normalize_request,x)
    def test_15_timeout_fixed(self): x=request(); x["timeout_seconds"]=61; self.assert_code("POLICY_MISMATCH",nv.normalize_request,x)
    def test_16_secret_field_rejected(self): x=request(); x["api_key"]="nvapi-example"; self.assert_code("SECRET_MATERIAL",nv.normalize_request,x)
    def test_17_secret_like_message_rejected(self): x=request(); x["messages"][0]["content"]="Bearer abcdefghijklmnopqrstuvwxyz"; self.assert_code("SECRET_MATERIAL",nv.normalize_request,x)
    def test_18_valid_synthetic_response(self):
        src=response(); before=copy.deepcopy(src); out=nv.normalize_synthetic_response(src); self.assertEqual(src,before); self.assertEqual(out["provider_runtime_activity"],"NONE"); self.assertEqual(out["spend_usd"],0)
    def test_19_real_response_rejected(self): x=response(); x["synthetic"]=False; self.assert_code("SYNTHETIC_REQUIRED",nv.normalize_synthetic_response,x)
    def test_20_response_model_rejected(self): x=response(); x["model"]="other"; self.assert_code("MODEL_NOT_ALLOWLISTED",nv.normalize_synthetic_response,x)
    def test_21_usage_rejected(self): x=response(); x["usage"]["output_tokens"]=16385; self.assert_code("USAGE_INVALID",nv.normalize_synthetic_response,x)
    def test_22_finish_reason_rejected(self): x=response(); x["finish_reason"]="tool_calls"; self.assert_code("RESPONSE_INVALID",nv.normalize_synthetic_response,x)
    def test_23_zero_cost_evidence_valid(self):
        out=nv.normalize_quota_evidence({"synthetic":True,"free_endpoint_visible":True,"account_limit_observed":True,"billing_required":False,"subscription_required":False}); self.assertTrue(out["zero_cost_eligible"]); self.assertIsNone(out["permanent_rpm_assumed"])
    def test_24_unproven_free_rejected(self): self.assert_code("ZERO_COST_ELIGIBILITY_UNPROVEN",nv.normalize_quota_evidence,{"synthetic":True,"free_endpoint_visible":False,"account_limit_observed":True,"billing_required":False,"subscription_required":False})
    def test_25_unobserved_account_limit_rejected(self): self.assert_code("ZERO_COST_ELIGIBILITY_UNPROVEN",nv.normalize_quota_evidence,{"synthetic":True,"free_endpoint_visible":True,"account_limit_observed":False,"billing_required":False,"subscription_required":False})
    def test_26_billing_required_rejected(self): self.assert_code("PAID_PATH_REQUIRED",nv.normalize_quota_evidence,{"synthetic":True,"free_endpoint_visible":True,"account_limit_observed":True,"billing_required":True,"subscription_required":False})
    def test_27_subscription_required_rejected(self): self.assert_code("PAID_PATH_REQUIRED",nv.normalize_quota_evidence,{"synthetic":True,"free_endpoint_visible":True,"account_limit_observed":True,"billing_required":False,"subscription_required":True})
    def test_28_real_quota_evidence_rejected(self): self.assert_code("SYNTHETIC_REQUIRED",nv.normalize_quota_evidence,{"synthetic":False,"free_endpoint_visible":True,"account_limit_observed":True,"billing_required":False,"subscription_required":False})
    def test_29_429_fail_closed(self): out=nv.normalize_error({"synthetic":True,"http_status":429,"error_type":None}); self.assertEqual(out["error_code"],"RATE_LIMIT_OR_CAPACITY"); self.assertFalse(out["retry_allowed"])
    def test_30_auth_fail_closed(self): self.assertEqual(nv.normalize_error({"synthetic":True,"http_status":401,"error_type":None})["error_code"],"AUTH_FAILURE")
    def test_31_403_fail_closed(self): self.assertEqual(nv.normalize_error({"synthetic":True,"http_status":403,"error_type":None})["error_code"],"AUTH_FAILURE")
    def test_32_422_fail_closed(self): self.assertEqual(nv.normalize_error({"synthetic":True,"http_status":422,"error_type":None})["error_code"],"REQUEST_VALIDATION_FAILURE")
    def test_33_500_fail_closed(self): self.assertEqual(nv.normalize_error({"synthetic":True,"http_status":500,"error_type":None})["error_code"],"PROVIDER_EXECUTION_FAILURE")
    def test_34_timeout_fail_closed(self): out=nv.normalize_error({"synthetic":True,"http_status":None,"error_type":"timeout"}); self.assertEqual(out["error_code"],"TIMEOUT"); self.assertFalse(out["retry_allowed"])
    def test_35_malformed_fail_closed(self): self.assertEqual(nv.normalize_error({"synthetic":True,"http_status":None,"error_type":"malformed"})["error_code"],"MALFORMED_RESPONSE")
    def test_36_redirect_fail_closed(self): self.assertEqual(nv.normalize_error({"synthetic":True,"http_status":None,"error_type":"redirect"})["error_code"],"MALFORMED_RESPONSE")
    def test_37_error_no_paid_or_fallback_authority(self):
        out=nv.normalize_error({"synthetic":True,"http_status":429,"error_type":None}); self.assertFalse(out["paid_upgrade_allowed"]); self.assertFalse(out["model_fallback_allowed"]); self.assertFalse(out["provider_fallback_allowed"])
    def test_38_real_error_evidence_rejected(self): self.assert_code("SYNTHETIC_REQUIRED",nv.normalize_error,{"synthetic":False,"http_status":429,"error_type":None})
    def test_39_request_immutable(self): src=request(); before=copy.deepcopy(src); nv.normalize_request(src); self.assertEqual(src,before)
    def test_40_response_immutable(self): src=response(); before=copy.deepcopy(src); nv.normalize_synthetic_response(src); self.assertEqual(src,before)
