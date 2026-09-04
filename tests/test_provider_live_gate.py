from __future__ import annotations
import copy, json, math, unittest
from pathlib import Path
from scripts import provider_live_gate as lg
ROOT=Path(__file__).resolve().parents[1]; FIX=ROOT/"platform"/"connectivity"/"live"/"fixtures"/"009r"
def load(name): return json.loads((FIX/name).read_text(encoding="utf-8"))
def reseal(v):
    v=copy.deepcopy(v); v["canonical_digest"]="sha256:"+"0"*64; v["canonical_digest"]=lg.canonical_digest(v); return v
def shadow_policy():
    return reseal({"schema_version":"1.0","worker_policy_id":"worker-policy:synthetic-shadow","provider_profile_id":"provider-profile:synthetic-alpha","provider_child_id":"STUDIO-009P-99","mode":"LIVE_SHADOW_WORKER","work_order_ref":None,"writer_claim_ref":None,"worktree_ref":None,"allowed_paths":[],"repository_write_allowed":False,"direct_main_write_allowed":False,"merge_allowed":False,"deploy_allowed":False,"publish_allowed":False,"secret_access_allowed":False,"arbitrary_tools_allowed":False,"local_mediation_required":True,"money_ceiling":0,"as_of":"2026-09-04T10:00:00Z"})
def bounded_policy():
    return reseal({"schema_version":"1.0","worker_policy_id":"worker-policy:synthetic-bounded","provider_profile_id":"provider-profile:synthetic-alpha","provider_child_id":"STUDIO-009P-99","mode":"LIVE_BOUNDED_WORKER","work_order_ref":"work-order:synthetic-1","writer_claim_ref":"writer-claim:synthetic-1","worktree_ref":"worktree:synthetic-1","allowed_paths":["Assets/_Game/Gameplay/**"],"repository_write_allowed":True,"direct_main_write_allowed":False,"merge_allowed":False,"deploy_allowed":False,"publish_allowed":False,"secret_access_allowed":False,"arbitrary_tools_allowed":False,"local_mediation_required":True,"money_ceiling":0,"as_of":"2026-09-04T10:00:00Z"})
class LiveGateTests(unittest.TestCase):
    def assertCode(self,code,fn):
        with self.assertRaises(lg.LiveGateError) as c: fn()
        self.assertEqual(c.exception.code,code)
        self.assertNotIn("synthetic-alpha",c.exception.safe_message)
    def test_01_ready_valid(self): self.assertEqual(lg.validate_live_state(load("valid-live-validation-ready.json"))["state"],"LIVE_VALIDATION_READY")
    def test_02_validated_valid(self): self.assertEqual(lg.validate_live_state(load("valid-live-validated.json"))["state"],"LIVE_VALIDATED")
    def test_03_shadow_valid(self): self.assertEqual(lg.validate_live_state(load("valid-shadow-worker.json"))["state"],"LIVE_SHADOW_WORKER")
    def test_04_unmerged_rejected(self): self.assertCode("OFFLINE_CHILD_NOT_MERGED",lambda:lg.validate_live_state(load("invalid-unmerged-offline.json")))
    def test_05_private_scope_rejected(self): self.assertCode("DATA_CLASS_BROADENING",lambda:lg.validate_live_state(load("invalid-private-data.json"),parent_allowed_data_classifications=["PUBLIC"]))
    def test_06_nonzero_budget_rejected(self): self.assertCode("NONZERO_BUDGET",lambda:lg.validate_live_state(load("invalid-nonzero-budget.json")))
    def test_07_routing_before_009e(self): self.assertCode("ROUTING_BEFORE_009E",lambda:lg.validate_live_state(load("invalid-routing-before-009e.json")))
    def test_08_revoked_transition_fails(self): self.assertCode("REVOKED_PROVIDER",lambda:lg.plan_transition(lg.validate_live_state(load("invalid-revoked-provider.json")),"LIVE_VALIDATION_READY"))
    def test_09_unknown_field(self):
        v=load("valid-live-validation-ready.json");v["x"]=1;self.assertCode("EXTRA_FIELD",lambda:lg.validate_live_state(v))
    def test_10_missing_field(self):
        v=load("valid-live-validation-ready.json");del v["offline_qa_ref"];self.assertCode("MISSING_FIELD",lambda:lg.validate_live_state(v))
    def test_11_duplicate_json_key(self): self.assertCode("DUPLICATE_JSON_KEY",lambda:lg.load_json_document('{"schema_version":"1.0","schema_version":"1.0"}'))
    def test_12_nonfinite_json(self): self.assertCode("INPUT_NUMBER",lambda:lg.load_json_document('{"x":NaN}'))
    def test_13_unicode_surrogate(self):
        v=load("valid-live-validation-ready.json");v["live_state_id"]="provider-live-state:\ud800";self.assertCode("INPUT_ENCODING",lambda:lg.validate_live_state(v))
    def test_14_structure_depth(self):
        v={};c=v
        for _ in range(lg.MAX_STRUCTURE_DEPTH+3): c["x"]={};c=c["x"]
        self.assertCode("STRUCTURE_LIMIT",lambda:lg.validate_live_state(v))
    def test_15_secret_field(self):
        v=load("valid-live-validation-ready.json");v["access_token"]="not-used";self.assertCode("SECRET_MATERIAL",lambda:lg.validate_live_state(v))
    def test_16_secret_like_value(self):
        v=load("valid-live-validation-ready.json");v["offline_qa_ref"]="qa:sk-ABCDEFGHIJKLMNOPQRSTUV";self.assertCode("SECRET_MATERIAL",lambda:lg.validate_live_state(v))
    def test_17_input_immutable(self):
        v=load("valid-live-validation-ready.json");b=copy.deepcopy(v);lg.validate_live_state(v);self.assertEqual(v,b)
    def test_18_digest_mismatch(self):
        v=load("valid-live-validation-ready.json");v["canonical_digest"]="sha256:"+"1"*64;self.assertCode("DIGEST_MISMATCH",lambda:lg.validate_live_state(v))
    def test_19_shadow_policy_valid(self): self.assertEqual(lg.validate_worker_mode_policy(shadow_policy())["mode"],"LIVE_SHADOW_WORKER")
    def test_20_bounded_policy_valid(self): self.assertEqual(lg.validate_worker_mode_policy(bounded_policy())["mode"],"LIVE_BOUNDED_WORKER")
    def test_21_shadow_write_forbidden(self):
        v=shadow_policy();v["repository_write_allowed"]=True;v=reseal(v);self.assertCode("WORKER_AUTHORITY",lambda:lg.validate_worker_mode_policy(v))
    def test_22_bounded_claim_required(self):
        v=bounded_policy();v["writer_claim_ref"]=None;v=reseal(v);self.assertCode("WRITER_CLAIM_REQUIRED",lambda:lg.validate_worker_mode_policy(v))
    def test_23_unsafe_path(self):
        v=bounded_policy();v["allowed_paths"]=["../secrets"];v=reseal(v);self.assertCode("UNSAFE_PATH",lambda:lg.validate_worker_mode_policy(v))
    def test_24_merge_forbidden(self):
        v=bounded_policy();v["merge_allowed"]=True;v=reseal(v);self.assertCode("WORKER_AUTHORITY",lambda:lg.validate_worker_mode_policy(v))
    def test_25_transition_disabled_ready(self): self.assertEqual(lg.plan_transition({"state":"DISABLED"},"LIVE_VALIDATION_READY")["decision"],"ALLOWED")
    def test_26_transition_ready_validated_requires_evidence(self): self.assertCode("MISSING_CONNECTED_EVIDENCE",lambda:lg.plan_transition({"state":"LIVE_VALIDATION_READY"},"LIVE_VALIDATED"))
    def test_27_transition_validated_shadow(self): self.assertEqual(lg.plan_transition({"state":"LIVE_VALIDATED"},"LIVE_SHADOW_WORKER",worker_policy=lg.validate_worker_mode_policy(shadow_policy()))["to"],"LIVE_SHADOW_WORKER")
    def test_28_routing_requires_authority(self): self.assertCode("ROUTING_BEFORE_009E",lambda:lg.plan_transition({"state":"LIVE_BOUNDED_WORKER"},"ROUTING_ELIGIBLE"))
