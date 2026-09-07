from __future__ import annotations
import json
import unittest
from scripts import cloudflare_live_transport as t

ACCOUNT = "0123456789abcdef0123456789abcdef"
SECRET = "cf_test_token_0123456789abcdef"

def body():
    return t.build_request([{"role":"user","content":"synthetic request"}],
                           max_completion_tokens=64, response_format={"type":"json_object"})

def success_value(content='{"status":"ok","value":7}', model=t.MODEL_ID, usage=None):
    if usage is None: usage={"prompt_tokens":100,"completion_tokens":20,"total_tokens":120}
    return {"id":"x","object":"chat.completion","created":1,"model":model,
            "choices":[{"index":0,"message":{"role":"assistant","content":content},"finish_reason":"stop"}],
            "usage":usage}

class FakeResponse:
    def __init__(self,status=200,value=None,raw=None,headers=None):
        self.status=status
        if raw is None: raw=json.dumps(value if value is not None else success_value()).encode()
        self.raw=raw
        self.headers=headers if headers is not None else [("Content-Type","application/json"),("Content-Length",str(len(raw)))]
    def getheaders(self): return list(self.headers)
    def read(self,n=-1): return self.raw if n<0 else self.raw[:n]

class FakeConnection:
    def __init__(self,response):
        self.response=response; self.path=None; self.closed=False
    def request(self,method,path,body=None,headers=None):
        self.method=method; self.path=path; self.payload=body; self.headers=headers
    def getresponse(self): return self.response
    def close(self): self.closed=True

class Factory:
    def __init__(self,response): self.conn=FakeConnection(response); self.host=None
    def __call__(self,*,host,timeout,context): self.host=host; self.timeout=timeout; return self.conn

class CloudflareLiveTransportTests(unittest.TestCase):
    def assert_code(self,code,fn):
        with self.assertRaises(t.CloudflareTransportError) as cm: fn()
        self.assertEqual(cm.exception.code,code)
    def perform(self,response,request_body=None):
        f=Factory(response); out=t.perform_request(ACCOUNT,SECRET,request_body or body(),connection_factory=f); return out,f
    def test_01_build_valid(self):
        x=body(); self.assertEqual(x["model"],t.MODEL_ID); self.assertEqual(x["tool_choice"],"none"); self.assertFalse(x["store"])
    def test_02_build_input_immutable(self):
        msgs=[{"role":"user","content":"synthetic"}]; before=[dict(msgs[0])]; t.build_request(msgs); self.assertEqual(msgs,before)
    def test_03_invalid_model_body(self):
        x=body(); x["model"]="other"; self.assert_code("INVALID_REQUEST",lambda:t.perform_request(ACCOUNT,SECRET,x,connection_factory=Factory(FakeResponse())))
    def test_04_invalid_message_role(self):
        self.assert_code("INVALID_REQUEST",lambda:t.build_request([{"role":"assistant","content":"x"}]))
    def test_05_secret_like_prompt(self):
        self.assert_code("SECRET_MATERIAL",lambda:t.build_request([{"role":"user","content":"Authorization: Bearer hidden"}]))
    def test_06_output_limit(self):
        self.assert_code("OUTPUT_LIMIT",lambda:t.build_request([{"role":"user","content":"x"}],max_completion_tokens=257))
    def test_07_invalid_response_format(self):
        self.assert_code("INVALID_REQUEST",lambda:t.build_request([{"role":"user","content":"x"}],response_format={"type":"text"}))
    def test_08_invalid_account(self):
        self.assert_code("INVALID_ACCOUNT",lambda:t.perform_request("abc",SECRET,body(),connection_factory=Factory(FakeResponse())))
    def test_09_invalid_secret(self):
        self.assert_code("INVALID_SECRET",lambda:t.perform_request(ACCOUNT,"short",body(),connection_factory=Factory(FakeResponse())))
    def test_10_success_and_no_account_escape(self):
        out,f=self.perform(FakeResponse(value=success_value())); self.assertEqual(out["model"],t.MODEL_ID); self.assertNotIn(ACCOUNT,repr(out)); self.assertTrue(out["account_identity_verified"]); self.assertEqual(f.host,t.HOST)
    def test_11_exact_account_path_internal_only(self):
        out,f=self.perform(FakeResponse(value=success_value())); self.assertEqual(f.conn.path,f"/client/v4/accounts/{ACCOUNT}/ai/v1/chat/completions"); self.assertEqual(out["path_template"],t.BASE_PATH_TEMPLATE+t.CHAT_PATH)
    def test_12_redirect(self):
        self.assert_code("REDIRECT",lambda:self.perform(FakeResponse(status=302,value={})))
    def test_13_auth_401(self):
        self.assert_code("AUTH_FAILED",lambda:self.perform(FakeResponse(status=401,value={"errors":[]})))
    def test_14_paid_5035(self):
        self.assert_code("PAID_PLAN_REQUIRED",lambda:self.perform(FakeResponse(status=403,value={"errors":[{"code":5035}]})))
    def test_15_free_quota_3036(self):
        self.assert_code("FREE_QUOTA_EXHAUSTED",lambda:self.perform(FakeResponse(status=429,value={"errors":[{"code":3036}]})))
    def test_16_capacity_3040(self):
        self.assert_code("CAPACITY_UNAVAILABLE",lambda:self.perform(FakeResponse(status=429,value={"errors":[{"code":3040}]})))
    def test_17_unknown_429(self):
        self.assert_code("QUOTA",lambda:self.perform(FakeResponse(status=429,value={"errors":[{"code":9999}]})))
    def test_18_provider_500(self):
        self.assert_code("PROVIDER_ERROR",lambda:self.perform(FakeResponse(status=500,value={})))
    def test_19_content_type(self):
        raw=json.dumps(success_value()).encode(); r=FakeResponse(status=200,raw=raw,headers=[("Content-Type","text/plain"),("Content-Length",str(len(raw)))])
        self.assert_code("CONTENT_TYPE",lambda:self.perform(r))
    def test_20_oversized_content_length(self):
        r=FakeResponse(status=200,value=success_value(),headers=[("Content-Type","application/json"),("Content-Length",str(t.MAX_RESPONSE_BYTES+1))])
        self.assert_code("RESPONSE_TOO_LARGE",lambda:self.perform(r))
    def test_21_duplicate_json(self):
        self.assert_code("MALFORMED_RESPONSE",lambda:self.perform(FakeResponse(status=200,raw=b'{"model":"x","model":"y"}')))
    def test_22_model_mismatch(self):
        self.assert_code("MODEL_MISMATCH",lambda:self.perform(FakeResponse(value=success_value(model="other"))))
    def test_23_tool_calls_forbidden(self):
        v=success_value(); v["choices"][0]["message"]["tool_calls"]=[{"id":"call_1"}]
        self.assert_code("EXTERNAL_CAPABILITY",lambda:self.perform(FakeResponse(value=v)))
    def test_24_usage_estimate(self):
        out,_=self.perform(FakeResponse(value=success_value())); self.assertEqual(out["usage"],{"input_tokens":100,"output_tokens":20,"total_tokens":120}); self.assertEqual(out["estimated_neurons"],t.estimate_neurons(100,20))
    def test_25_network_exception(self):
        def broken(**kwargs): raise OSError("synthetic")
        self.assert_code("NETWORK_ERROR",lambda:t.perform_request(ACCOUNT,SECRET,body(),connection_factory=broken))
