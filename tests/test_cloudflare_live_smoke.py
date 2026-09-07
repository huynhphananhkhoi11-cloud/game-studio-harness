from __future__ import annotations
import unittest
from scripts import cloudflare_live_smoke as s
from scripts import cloudflare_session_credential_bridge as b

AS_OF="2026-09-05T08:00:00Z"
ACCOUNT="0123456789abcdef0123456789abcdef"
SECRET="cf_test_token_0123456789abcdef"

def preflight():
    return {"v_contract_merge":s.V_CONTRACT_MERGE,"v_scope_correction_merge":s.V_SCOPE_CORRECTION_MERGE,
            "p02_closeout_merge":s.P02_CLOSEOUT_MERGE,"r01_closeout_merge":s.R01_CLOSEOUT_MERGE,
            "provider_profile_id":s.PROVIDER_PROFILE_ID,"provider_child_id":s.PROVIDER_CHILD_ID,
            "model":s.MODEL_ID,"host":s.HOST,"account_ref":s.ACCOUNT_REF,
            "workers_free_confirmed":True,"model_free_eligible_confirmed":True,
            "neuron_usage_observability":"UNAVAILABLE_BEFORE_FIRST_INFERENCE",
            "free_allocation_fail_closed_confirmed":True,"token_permissions_confirmed":True,
            "no_paid_path_confirmed":True,"money_ceiling":0,"max_requests":3,"concurrency":1,
            "retry_count":0,"campaign_neuron_ceiling":2000,"kill_switch_armed":True,"as_of":AS_OF}

def lease():
    x={"schema_version":"1.0","credential_lease_id":"credential-lease:"+"b"*32,
       "credential_profile_id":b.CREDENTIAL_PROFILE_ID,"profile_digest":"sha256:"+"1"*64,
       "subject_ref":b.SUBJECT_REF,"capability":b.CAPABILITY,"purpose":b.PURPOSE,
       "repository_record_digest":None,"operation_digest":None,"issued_at":"2026-09-05T07:59:00Z",
       "expires_at":"2026-09-05T08:10:00Z","idempotency_key":"v02-smoke-test","canonical_digest":"sha256:"+"0"*64}
    x["canonical_digest"]=b.canonical_digest(x); return x

def reservation():
    state={"count":0,"neurons":0}
    def reserve(probe_id,ordinal,neurons):
        state["count"]+=1; state["neurons"]+=neurons
        return {"request_ordinal":state["count"],"cumulative_reserved_neurons":state["neurons"]}
    return reserve

def fake_transport(account_id,secret,body):
    values=['{"status":"ok","value":7}','{"decision":"ALLOW","reasons":["synthetic"]}','{"unique_sorted":["alpha","beta"],"count":2}']
    fake_transport.i+=1
    return {"status":200,"model":s.MODEL_ID,"finish_reason":"stop","content":values[fake_transport.i-1],
            "usage":{"input_tokens":20,"output_tokens":10,"total_tokens":30},"estimated_neurons":3,
            "model_identity_verified":True,"transport_identity_verified":True,"account_identity_verified":True}
fake_transport.i=0

class CloudflareLiveSmokeTests(unittest.TestCase):
    def setUp(self): fake_transport.i=0
    def assert_code(self,code,fn):
        with self.assertRaises(s.CloudflareSmokeError) as cm: fn()
        self.assertEqual(cm.exception.code,code)
    def test_01_valid_preflight(self): self.assertEqual(s.validate_preflight(preflight())["max_requests"],3)
    def test_02_wrong_contract_merge(self):
        x=preflight(); x["v_contract_merge"]="bad"; self.assert_code("LINEAGE_MISMATCH",lambda:s.validate_preflight(x))
    def test_03_free_false(self):
        x=preflight(); x["workers_free_confirmed"]=False; self.assert_code("FREE_TIER_NOT_CONFIRMED",lambda:s.validate_preflight(x))
    def test_04_model_free_false(self):
        x=preflight(); x["model_free_eligible_confirmed"]=False; self.assert_code("MODEL_FREE_NOT_CONFIRMED",lambda:s.validate_preflight(x))
    def test_05_usage_observability_and_fail_closed_required(self):
        x=preflight(); x["neuron_usage_observability"]="UNVERIFIED"; self.assert_code("NEURON_USAGE_OBSERVABILITY",lambda:s.validate_preflight(x))
        x=preflight(); x["free_allocation_fail_closed_confirmed"]=False; self.assert_code("FREE_ALLOCATION_FAIL_CLOSED",lambda:s.validate_preflight(x))
    def test_06_permissions_false(self):
        x=preflight(); x["token_permissions_confirmed"]=False; self.assert_code("TOKEN_PERMISSIONS_NOT_CONFIRMED",lambda:s.validate_preflight(x))
    def test_07_paid_path_not_denied(self):
        x=preflight(); x["no_paid_path_confirmed"]=False; self.assert_code("PAID_PATH_NOT_DENIED",lambda:s.validate_preflight(x))
    def test_08_nonzero_budget(self):
        x=preflight(); x["money_ceiling"]=1; self.assert_code("NONZERO_BUDGET",lambda:s.validate_preflight(x))
    def test_09_request_ceiling(self):
        x=preflight(); x["max_requests"]=4; self.assert_code("REQUEST_LIMIT",lambda:s.validate_preflight(x))
    def test_10_retry_ceiling(self):
        x=preflight(); x["retry_count"]=1; self.assert_code("INVALID_PREFLIGHT",lambda:s.validate_preflight(x))
    def test_11_kill_preflight(self):
        x=preflight(); x["kill_switch_armed"]=False; self.assert_code("KILL_SWITCH",lambda:s.validate_preflight(x))
    def test_12_invalid_as_of(self):
        x=preflight(); x["as_of"]="bad"; self.assert_code("INVALID_PREFLIGHT",lambda:s.validate_preflight(x))
    def test_13_reservation_required(self):
        self.assert_code("REQUEST_RESERVATION",lambda:s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,transport_fn=fake_transport))
    def test_14_bad_reservation_ordinal(self):
        def bad(p,o,n): return {"request_ordinal":9,"cumulative_reserved_neurons":512}
        self.assert_code("REQUEST_RESERVATION",lambda:s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,reservation_fn=bad,transport_fn=fake_transport))
    def test_15_bad_reservation_neurons(self):
        def bad(p,o,n): return {"request_ordinal":o,"cumulative_reserved_neurons":1999}
        self.assert_code("REQUEST_RESERVATION",lambda:s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,reservation_fn=bad,transport_fn=fake_transport))
    def test_16_kill_switch_blocks(self):
        self.assert_code("KILL_SWITCH",lambda:s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,reservation_fn=reservation(),transport_fn=fake_transport,kill_switch=s.KillSwitch(False)))
    def test_17_success_three_calls(self):
        out=s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,reservation_fn=reservation(),transport_fn=fake_transport)
        self.assertEqual(out["status"],"SMOKE_PASS"); self.assertEqual(out["request_count"],3); self.assertEqual(out["reserved_neurons"],1536)
    def test_18_quality_failure(self):
        def bad_transport(a,k,body): return {"model":s.MODEL_ID,"finish_reason":"stop","content":'{"wrong":true}',"usage":{},"estimated_neurons":0,"model_identity_verified":True,"transport_identity_verified":True,"account_identity_verified":True}
        self.assert_code("QUALITY_FAILED",lambda:s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,reservation_fn=reservation(),transport_fn=bad_transport))
    def test_19_no_account_or_token_escape(self):
        out=s.execute_smoke(preflight(),lease(),account_supplier=lambda:ACCOUNT,secret_supplier=lambda:SECRET,reservation_fn=reservation(),transport_fn=fake_transport)
        self.assertNotIn(ACCOUNT,repr(out)); self.assertNotIn(SECRET,repr(out))
    def test_20_preflight_immutable(self):
        x=preflight(); before=dict(x); s.validate_preflight(x); self.assertEqual(x,before)

# <!-- STUDIO-009V-02-OWNER-CONNECTED-PREFLIGHT-0003 -->
