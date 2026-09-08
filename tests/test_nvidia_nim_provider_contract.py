from __future__ import annotations
import copy, json, unittest
from pathlib import Path
from scripts import nvidia_nim_adapter as nv
ROOT=Path(__file__).resolve().parents[1]; PROVIDER=ROOT/"platform/connectivity/providers/nvidia-nim"; FIX=ROOT/"platform/connectivity/fixtures/009p03"
def load(path):
    with open(path,"r",encoding="utf-8") as f: return json.load(f)
def chain(): return [load(PROVIDER/"provider-profile.json"),load(PROVIDER/"child-contract-evidence.json"),load(PROVIDER/"model-profile-deepseek-v4-pro-0813.json"),load(PROVIDER/"transport-policy.json"),load(PROVIDER/"data-policy.json"),load(PROVIDER/"quota-policy.json"),load(PROVIDER/"budget-policy.json")]
class NvidiaNimProviderContractTests(unittest.TestCase):
    def assert_code(self,code,func,*args):
        with self.assertRaises(nv.NvidiaNimAdapterError) as cm: func(*args)
        self.assertEqual(cm.exception.code,code)
    def test_01_valid_static_chain(self):
        out=nv.validate_static_chain(*chain()); self.assertEqual(out["provider_state"],"DISABLED"); self.assertEqual(out["model_state"],"DECLARED"); self.assertEqual(out["child_evidence_class"],"SYNTHETIC")
    def test_02_exact_provider_identity(self): self.assertEqual(load(PROVIDER/"provider-profile.json")["provider_profile_id"],nv.PROVIDER_PROFILE_ID)
    def test_03_exact_model_identity(self): self.assertEqual(load(PROVIDER/"model-profile-deepseek-v4-pro-0813.json")["model_identity_ref"],nv.MODEL_IDENTITY_REF)
    def test_04_capabilities_exact(self): self.assertEqual(load(PROVIDER/"provider-profile.json")["allowed_capabilities"],["REASONING","TEXT_GENERATION"])
    def test_05_money_zero(self): self.assertEqual(load(PROVIDER/"provider-profile.json")["money_ceiling"],0)
    def test_06_transport_host_exact(self): self.assertEqual(load(PROVIDER/"transport-policy.json")["host"],"integrate.api.nvidia.com")
    def test_07_transport_path_exact(self):
        t=load(PROVIDER/"transport-policy.json"); self.assertEqual(t["chat_completions_path"],"/v1/chat/completions"); self.assertEqual(t["canonical_base_url"],"https://integrate.api.nvidia.com/v1")
    def test_08_redirects_disabled(self): self.assertFalse(load(PROVIDER/"transport-policy.json")["allow_redirects"])
    def test_09_transport_offline(self): self.assertEqual(load(PROVIDER/"transport-policy.json")["network_activation"],"NONE_P03_OFFLINE")
    def test_10_data_public_only(self): self.assertEqual(load(PROVIDER/"data-policy.json")["allowed_data_classifications"],["PUBLIC"])
    def test_11_private_export_forbidden(self): self.assertFalse(load(PROVIDER/"data-policy.json")["private_or_unreleased_export_allowed"])
    def test_12_personal_confidential_forbidden(self):
        d=load(PROVIDER/"data-policy.json"); self.assertFalse(d["personal_data_allowed"]); self.assertFalse(d["confidential_or_sensitive_data_allowed"])
    def test_13_dynamic_quota_no_entitlement_invention(self):
        q=load(PROVIDER/"quota-policy.json")["provider_snapshot"]; self.assertIsNone(q["permanent_rpm"]); self.assertIsNone(q["permanent_rpd"])
    def test_14_future_v03_bounds(self):
        v=load(PROVIDER/"quota-policy.json")["future_v03_limits"]; self.assertEqual(v["max_real_requests"],3); self.assertEqual(v["max_concurrency"],1); self.assertEqual(v["max_retries"],0); self.assertFalse(v["tools"]); self.assertFalse(v["streaming"])
    def test_15_budget_paid_paths_forbidden(self):
        b=load(PROVIDER/"budget-policy.json"); self.assertEqual(b["money_ceiling"],0); self.assertTrue(b["zero_cost_trial_required"]); self.assertFalse(b["paid_subscription_allowed"]); self.assertFalse(b["auto_recharge_allowed"]); self.assertFalse(b["paid_fallback_allowed"])
    def test_16_reserved_refs_valid(self): self.assertEqual(nv.validate_reserved_refs(nv.CREDENTIAL_PROFILE_REF,nv.ACCOUNT_REF)["account_ref"],nv.ACCOUNT_REF)
    def test_17_invalid_reserved_ref_rejected(self):
        bad=load(FIX/"invalid-credential-ref.json"); self.assert_code("REFERENCE_MISMATCH",nv.validate_reserved_refs,bad["credential_profile_ref"],bad["account_ref"])
    def test_18_invalid_model_rejected(self):
        args=chain(); args[2]=load(FIX/"invalid-unapproved-model.json")
        with self.assertRaises(nv.NvidiaNimAdapterError): nv.validate_static_chain(*args)
    def test_19_invalid_host_rejected(self):
        args=chain(); args[3]=load(FIX/"invalid-host-or-path.json"); self.assert_code("POLICY_MISMATCH",nv.validate_static_chain,*args)
    def test_20_invalid_data_broadening_rejected(self):
        args=chain(); args[4]=load(FIX/"invalid-data-broadening.json"); self.assert_code("DATA_NOT_ALLOWED",nv.validate_static_chain,*args)
    def test_21_invalid_nonzero_budget_rejected(self):
        args=chain(); args[6]=load(FIX/"invalid-nonzero-budget.json"); self.assert_code("NONZERO_BUDGET",nv.validate_static_chain,*args)
    def test_22_chain_immutable(self):
        args=chain(); before=copy.deepcopy(args); nv.validate_static_chain(*args); self.assertEqual(args,before)
    def test_23_redirect_broadening_rejected(self):
        args=chain(); args[3]["allow_redirects"]=True; self.assert_code("POLICY_MISMATCH",nv.validate_static_chain,*args)
    def test_24_network_activation_broadening_rejected(self):
        args=chain(); args[3]["network_activation"]="LIVE"; self.assert_code("POLICY_MISMATCH",nv.validate_static_chain,*args)
