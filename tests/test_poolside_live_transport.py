from __future__ import annotations

import copy
import json
import unittest

from scripts import poolside_live_transport as t

SECRET = "synthetic_session_secret_0123456789"

def success_value(content='{"status":"ok","value":7}'):
    return {
        "model": t.MODEL_ID,
        "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }

class FakeResponse:
    def __init__(self, status=200, value=None, raw=None, headers=None):
        self.status = status
        self._raw = raw if raw is not None else json.dumps(
            success_value() if value is None else value
        ).encode("utf-8")
        self._headers = headers if headers is not None else [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(self._raw))),
        ]
    def getheaders(self):
        return list(self._headers)
    def read(self, n=-1):
        return self._raw[:n] if n >= 0 else self._raw

class FakeConnection:
    def __init__(self, response):
        self.response = response
        self.request_args = None
        self.closed = False
    def request(self, method, path, body=None, headers=None):
        self.request_args = (method, path, body, headers)
    def getresponse(self):
        return self.response
    def close(self):
        self.closed = True

def factory_for(conn):
    def factory(**kwargs):
        factory.kwargs = kwargs
        return conn
    return factory

def body():
    return t.build_request(
        [{"role": "user", "content": "Synthetic hello"}],
        estimated_input_tokens=20,
        max_tokens=64,
        response_format={"type": "json_object"},
    )

class PoolsideLiveTransportTests(unittest.TestCase):
    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(t.PoolsideLiveTransportError) as cm:
            fn(*args, **kwargs)
        self.assertEqual(cm.exception.code, code)
        self.assertNotIn(SECRET, str(cm.exception))

    def test_01_constants_exact(self):
        self.assertEqual(t.HOST, "inference.poolside.ai")
        self.assertEqual(t.PATH, "/v1/chat/completions")
        self.assertEqual(t.MODEL_ID, "poolside/laguna-s-2.1")

    def test_02_build_request_valid(self):
        x = body()
        self.assertEqual(x["model"], t.MODEL_ID)
        self.assertFalse(x["stream"])
        self.assertEqual(x["max_tokens"], 64)

    def test_03_messages_immutable(self):
        x = [{"role": "user", "content": "Synthetic"}]
        before = copy.deepcopy(x)
        t.build_request(x, estimated_input_tokens=10)
        self.assertEqual(x, before)

    def test_04_empty_messages_rejected(self):
        self.assert_code("INVALID_REQUEST", t.build_request, [], estimated_input_tokens=0)

    def test_05_assistant_role_rejected(self):
        self.assert_code("INVALID_REQUEST", t.build_request,
                         [{"role": "assistant", "content": "x"}], estimated_input_tokens=1)

    def test_06_extra_message_field_rejected(self):
        self.assert_code("INVALID_REQUEST", t.build_request,
                         [{"role": "user", "content": "x", "name": "n"}], estimated_input_tokens=1)

    def test_07_secret_like_prompt_rejected(self):
        self.assert_code("SECRET_MATERIAL", t.build_request,
                         [{"role": "user", "content": "Authorization: hidden"}], estimated_input_tokens=1)

    def test_08_input_ceiling(self):
        self.assert_code("INPUT_LIMIT", t.build_request,
                         [{"role": "user", "content": "x"}], estimated_input_tokens=4097)

    def test_09_output_ceiling(self):
        self.assert_code("OUTPUT_LIMIT", t.build_request,
                         [{"role": "user", "content": "x"}], estimated_input_tokens=1, max_tokens=1025)

    def test_10_response_format_rejected(self):
        self.assert_code("INVALID_REQUEST", t.build_request,
                         [{"role": "user", "content": "x"}], estimated_input_tokens=1,
                         response_format={"type": "text"})

    def test_11_request_body_rejects_wrong_model(self):
        x = body(); x["model"] = "wrong"
        self.assert_code("INVALID_REQUEST", t.perform_request, SECRET, x,
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_12_invalid_secret_short(self):
        self.assert_code("INVALID_SECRET", t.perform_request, "short", body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_13_direct_host_and_path(self):
        conn = FakeConnection(FakeResponse())
        f = factory_for(conn)
        out = t.perform_request(SECRET, body(), connection_factory=f)
        self.assertEqual(f.kwargs["host"], t.HOST)
        self.assertEqual(conn.request_args[0:2], ("POST", t.PATH))
        self.assertEqual(out["host"], t.HOST)

    def test_14_authorization_header_not_returned(self):
        conn = FakeConnection(FakeResponse())
        out = t.perform_request(SECRET, body(), connection_factory=factory_for(conn))
        self.assertNotIn(SECRET, repr(out))
        self.assertEqual(conn.request_args[3]["Authorization"], "Bearer " + SECRET)

    def test_15_success_model_identity(self):
        out = t.perform_request(SECRET, body(),
                                connection_factory=factory_for(FakeConnection(FakeResponse())))
        self.assertTrue(out["model_identity_verified"])
        self.assertTrue(out["transport_identity_verified"])

    def test_16_usage_normalized(self):
        out = t.perform_request(SECRET, body(),
                                connection_factory=factory_for(FakeConnection(FakeResponse())))
        self.assertEqual(out["usage"], {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15})

    def test_17_wrong_model_response(self):
        v = success_value(); v["model"] = "wrong"
        self.assert_code("MODEL_MISMATCH", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(value=v))))

    def test_18_tool_calls_response_rejected(self):
        v = success_value(); v["choices"][0]["message"]["tool_calls"] = [{"id": "x"}]
        self.assert_code("EXTERNAL_CAPABILITY", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(value=v))))

    def test_19_finish_reason_length_rejected(self):
        v = success_value(); v["choices"][0]["finish_reason"] = "length"
        self.assert_code("MALFORMED_RESPONSE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(value=v))))

    def test_20_redirect_rejected(self):
        self.assert_code("REDIRECT", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=302, raw=b""))))

    def test_21_401(self):
        self.assert_code("AUTH_FAILURE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=401, raw=b"{}"))))

    def test_22_403(self):
        self.assert_code("AUTH_FAILURE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=403, raw=b"{}"))))

    def test_23_422(self):
        self.assert_code("REQUEST_VALIDATION_FAILURE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=422, raw=b"{}"))))

    def test_24_429(self):
        self.assert_code("RATE_LIMIT_OR_CAPACITY", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=429, raw=b"{}"))))

    def test_25_500(self):
        self.assert_code("PROVIDER_EXECUTION_FAILURE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=500, raw=b"{}"))))

    def test_26_402_paid(self):
        self.assert_code("PAID_PATH_REQUIRED", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(status=402, raw=b"{}"))))

    def test_27_wrong_content_type(self):
        r = FakeResponse(headers=[("Content-Type", "text/html")])
        self.assert_code("CONTENT_TYPE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(r)))

    def test_28_malformed_json(self):
        r = FakeResponse(raw=b"{", headers=[("Content-Type","application/json")])
        self.assert_code("MALFORMED_RESPONSE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(r)))

    def test_29_duplicate_json_key(self):
        raw = b'{"model":"poolside/laguna-s-2.1","model":"x"}'
        r = FakeResponse(raw=raw, headers=[("Content-Type","application/json")])
        self.assert_code("MALFORMED_RESPONSE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(r)))

    def test_30_response_size_header(self):
        r = FakeResponse(raw=b"{}", headers=[("Content-Type","application/json"),
                                             ("Content-Length", str(t.MAX_RESPONSE_BYTES + 1))])
        self.assert_code("RESPONSE_TOO_LARGE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(r)))

    def test_31_usage_inconsistent(self):
        v = success_value()
        v["usage"]["total_tokens"] = 99
        self.assert_code("USAGE_INVALID", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(FakeResponse(value=v))))

    def test_32_connection_closed(self):
        conn = FakeConnection(FakeResponse())
        t.perform_request(SECRET, body(), connection_factory=factory_for(conn))
        self.assertTrue(conn.closed)

import inspect as _v04_transport_inspect

class PoolsideLiveTransportPreQaRepairTests(unittest.TestCase):
    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(t.PoolsideLiveTransportError) as cm:
            fn(*args, **kwargs)
        self.assertEqual(cm.exception.code, code)
        self.assertNotIn(SECRET, str(cm.exception))

    def test_repair_01_auth_error_body_redacted(self):
        raw = ("provider diagnostic contains " + SECRET).encode("utf-8")
        r = FakeResponse(status=401, raw=raw, headers=[
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(raw))),
        ])
        self.assert_code("AUTH_FAILURE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(r)))

    def test_repair_02_server_error_body_redacted(self):
        raw = ("unsafe provider body " + SECRET).encode("utf-8")
        r = FakeResponse(status=500, raw=raw, headers=[
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(raw))),
        ])
        self.assert_code("PROVIDER_EXECUTION_FAILURE", t.perform_request, SECRET, body(),
                         connection_factory=factory_for(FakeConnection(r)))

    def test_repair_03_tools_field_rejected(self):
        x = body(); x["tools"] = []
        self.assert_code("INVALID_REQUEST", t.perform_request, SECRET, x,
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_repair_04_remote_mcp_field_rejected(self):
        x = body(); x["remote_mcp"] = []
        self.assert_code("INVALID_REQUEST", t.perform_request, SECRET, x,
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_repair_05_code_execution_field_rejected(self):
        x = body(); x["code_execution"] = False
        self.assert_code("INVALID_REQUEST", t.perform_request, SECRET, x,
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_repair_06_file_search_field_rejected(self):
        x = body(); x["file_search"] = False
        self.assert_code("INVALID_REQUEST", t.perform_request, SECRET, x,
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_repair_07_url_context_field_rejected(self):
        x = body(); x["url_context"] = False
        self.assert_code("INVALID_REQUEST", t.perform_request, SECRET, x,
                         connection_factory=factory_for(FakeConnection(FakeResponse())))

    def test_repair_08_no_host_or_path_override_surface(self):
        params = _v04_transport_inspect.signature(t.perform_request).parameters
        self.assertNotIn("host", params)
        self.assertNotIn("path", params)
        self.assertNotIn("base_url", params)

    def test_repair_09_default_connection_rejects_wrong_host(self):
        self.assert_code("INVALID_REQUEST", t._default_connection,
                         host="partner.example",
                         timeout=t.TIMEOUT_SECONDS,
                         context=None)


class PoolsideV04AdditionalTransportTests(unittest.TestCase):
    def test_poolside_v04_404_normalizes_not_found(self):
        conn = FakeConnection(FakeResponse(status=404, raw=b"{}"))
        with self.assertRaises(t.PoolsideLiveTransportError) as cm:
            t.perform_request(SECRET, body(), connection_factory=factory_for(conn))
        self.assertEqual(cm.exception.code, "NOT_FOUND")

    def test_poolside_v04_acp_field_is_rejected(self):
        x = body(); x["acp"] = False
        with self.assertRaises(t.PoolsideLiveTransportError) as cm:
            t.perform_request(SECRET, x, connection_factory=factory_for(FakeConnection(FakeResponse())))
        self.assertEqual(cm.exception.code, "INVALID_REQUEST")
