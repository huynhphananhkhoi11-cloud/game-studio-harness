from __future__ import annotations
import copy, unittest
from scripts import provider_live_evidence as ev
def reseal(v):
    v=copy.deepcopy(v);v["canonical_digest"]="sha256:"+"0"*64;v["canonical_digest"]=ev.canonical_digest(v);return v
def valid():
    return reseal({"schema_version":"1.0","connected_validation_id":"connected-validation:synthetic-alpha","provider_profile_id":"provider-profile:synthetic-alpha","provider_child_id":"STUDIO-009P-99","provider_model_ref":"model:synthetic-alpha","transport_ref":"transport:synthetic-alpha","credential_profile_ref":"credential-profile:synthetic-alpha","v_contract_ref":"v-contract:synthetic-v99","data_classification":"PUBLIC","max_request_bytes":32768,"max_output_bytes":8192,"request_count":3,"concurrency":1,"retry_count":0,"model_identity_verified":True,"transport_identity_verified":True,"quota_evidence_ref":"quota-evidence:synthetic-alpha","spend_amount":0,"currency":"USD","paid_fallback_allowed":False,"kill_switch_evidence_ref":"kill-switch:synthetic-alpha","revocation_evidence_ref":"revoke-evidence:synthetic-alpha","connected_qa_ref":"qa:connected-alpha","connected_review_ref":"review:connected-alpha","owner_disposition_ref":"owner-disposition:synthetic-alpha","validated_at":"2026-09-04T10:00:00Z","as_of":"2026-09-04T10:00:01Z"})
class EvidenceTests(unittest.TestCase):
    def assertCode(self,code,fn):
        with self.assertRaises(ev.ConnectedEvidenceError) as c: fn()
        self.assertEqual(c.exception.code,code);self.assertNotIn("synthetic-alpha",c.exception.safe_message)
    def test_01_valid(self): self.assertEqual(ev.validate_connected_validation(valid())["decision"],"ACCEPTED")
    def test_02_public(self): self.assertEqual(ev.validate_connected_validation(valid())["data_classification"],"PUBLIC")
    def test_03_request_limit(self):
        v=valid();v["request_count"]=4;v=reseal(v);self.assertCode("REQUEST_LIMIT",lambda:ev.validate_connected_validation(v))
    def test_04_concurrency_limit(self):
        v=valid();v["concurrency"]=2;v=reseal(v);self.assertCode("CONCURRENCY_LIMIT",lambda:ev.validate_connected_validation(v))
    def test_05_retry_limit(self):
        v=valid();v["retry_count"]=1;v=reseal(v);self.assertCode("RETRY_LIMIT",lambda:ev.validate_connected_validation(v))
    def test_06_nonzero_spend(self):
        v=valid();v["spend_amount"]=1;v=reseal(v);self.assertCode("NONZERO_SPEND",lambda:ev.validate_connected_validation(v))
    def test_07_paid_fallback(self):
        v=valid();v["paid_fallback_allowed"]=True;v=reseal(v);self.assertCode("PAID_FALLBACK",lambda:ev.validate_connected_validation(v))
    def test_08_model_identity(self):
        v=valid();v["model_identity_verified"]=False;v=reseal(v);self.assertCode("IDENTITY_UNVERIFIED",lambda:ev.validate_connected_validation(v))
    def test_09_transport_identity(self):
        v=valid();v["transport_identity_verified"]=False;v=reseal(v);self.assertCode("IDENTITY_UNVERIFIED",lambda:ev.validate_connected_validation(v))
    def test_10_public_only(self):
        v=valid();v["data_classification"]="INTERNAL";v=reseal(v);self.assertCode("PUBLIC_ONLY",lambda:ev.validate_connected_validation(v))
    def test_11_missing_v_contract(self):
        v=valid();v["v_contract_ref"]=None;v=reseal(v);self.assertCode("MISSING_V_CONTRACT",lambda:ev.validate_connected_validation(v))
    def test_12_missing_kill(self):
        v=valid();v["kill_switch_evidence_ref"]=None;v=reseal(v);self.assertCode("MISSING_KILL_REVOKE",lambda:ev.validate_connected_validation(v))
    def test_13_missing_revoke(self):
        v=valid();v["revocation_evidence_ref"]=None;v=reseal(v);self.assertCode("MISSING_KILL_REVOKE",lambda:ev.validate_connected_validation(v))
    def test_14_missing_qa(self):
        v=valid();v["connected_qa_ref"]=None;v=reseal(v);self.assertCode("MISSING_CONNECTED_QA",lambda:ev.validate_connected_validation(v))
    def test_15_missing_review(self):
        v=valid();v["connected_review_ref"]=None;v=reseal(v);self.assertCode("MISSING_CONNECTED_REVIEW",lambda:ev.validate_connected_validation(v))
    def test_16_missing_owner(self):
        v=valid();v["owner_disposition_ref"]=None;v=reseal(v);self.assertCode("MISSING_OWNER_DISPOSITION",lambda:ev.validate_connected_validation(v))
    def test_17_chronology(self):
        v=valid();v["validated_at"]="2026-09-04T10:00:02Z";v=reseal(v);self.assertCode("INVALID_TIME",lambda:ev.validate_connected_validation(v))
    def test_18_unknown_field(self):
        v=valid();v["x"]=1;self.assertCode("EXTRA_FIELD",lambda:ev.validate_connected_validation(v))
    def test_19_duplicate_json(self): self.assertCode("DUPLICATE_JSON_KEY",lambda:ev.load_json_document('{"schema_version":"1.0","schema_version":"1.0"}'))
    def test_20_nonfinite_json(self): self.assertCode("INPUT_NUMBER",lambda:ev.load_json_document('{"x":NaN}'))
    def test_21_secret_like(self):
        v=valid();v["provider_model_ref"]="model:sk-ABCDEFGHIJKLMNOPQRSTUV";self.assertCode("SECRET_MATERIAL",lambda:ev.validate_connected_validation(v))
    def test_22_input_immutable(self):
        v=valid();b=copy.deepcopy(v);ev.validate_connected_validation(v);self.assertEqual(v,b)
