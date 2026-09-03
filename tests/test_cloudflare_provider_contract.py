from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path

from scripts import cloudflare_workers_ai_adapter as cf

ROOT = Path(__file__).resolve().parents[1]
PROVIDER = ROOT / "platform/connectivity/providers/cloudflare-workers-ai"
FIX = ROOT / "platform/connectivity/fixtures/009p02"

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chain():
    return [
        load(PROVIDER / "provider-profile.json"),
        load(PROVIDER / "child-contract-evidence.json"),
        load(PROVIDER / "model-profile-nemotron-3-super.json"),
        load(PROVIDER / "transport-policy.json"),
        load(PROVIDER / "data-policy.json"),
        load(PROVIDER / "quota-policy.json"),
        load(PROVIDER / "budget-policy.json"),
    ]

class CloudflareProviderContractTests(unittest.TestCase):
    def test_01_valid_static_chain(self):
        out = cf.validate_static_chain(*chain())
        self.assertEqual(out["provider_state"], "DISABLED")
        self.assertEqual(out["model_state"], "DECLARED")

    def test_02_profile_money_zero(self):
        self.assertEqual(load(PROVIDER / "provider-profile.json")["money_ceiling"], 0)

    def test_03_profile_capabilities_exact(self):
        self.assertEqual(load(PROVIDER / "provider-profile.json")["allowed_capabilities"], ["LOCAL_TOOL_REQUEST", "REASONING", "TEXT_GENERATION"])

    def test_04_model_identity_exact(self):
        self.assertEqual(load(PROVIDER / "model-profile-nemotron-3-super.json")["model_identity_ref"], cf.MODEL_IDENTITY_REF)

    def test_05_transport_host_exact(self):
        self.assertEqual(load(PROVIDER / "transport-policy.json")["host"], "api.cloudflare.com")

    def test_06_transport_no_redirects(self):
        self.assertFalse(load(PROVIDER / "transport-policy.json")["allow_redirects"])

    def test_07_transport_account_ref(self):
        self.assertEqual(load(PROVIDER / "transport-policy.json")["accepted_account_ref"], cf.ACCOUNT_REF)

    def test_08_ai_gateway_disabled(self):
        self.assertFalse(load(PROVIDER / "transport-policy.json")["ai_gateway_allowed"])

    def test_09_data_public_only(self):
        self.assertEqual(load(PROVIDER / "data-policy.json")["allowed_data_classifications"], ["PUBLIC"])

    def test_10_storage_disabled(self):
        self.assertFalse(load(PROVIDER / "data-policy.json")["storage_services_allowed"])

    def test_11_quota_provider_snapshot(self):
        self.assertEqual(load(PROVIDER / "quota-policy.json")["provider_snapshot"]["free_neurons_per_day"], 10000)

    def test_12_quota_game_ceiling(self):
        self.assertEqual(load(PROVIDER / "quota-policy.json")["game_limits"]["max_daily_neurons"], 8000)

    def test_13_error_mapping_exact(self):
        self.assertEqual(load(PROVIDER / "quota-policy.json")["error_normalization"], {"3036": "FREE_QUOTA_EXHAUSTED", "3040": "CAPACITY_UNAVAILABLE", "5035": "PAID_PLAN_REQUIRED"})

    def test_14_budget_free_required(self):
        b = load(PROVIDER / "budget-policy.json")
        self.assertTrue(b["workers_free_required"])
        self.assertEqual(b["money_ceiling"], 0)

    def test_15_budget_paid_paths_disabled(self):
        b = load(PROVIDER / "budget-policy.json")
        self.assertFalse(any(b[k] for k in ["paid_plan_allowed", "auto_recharge_allowed", "unified_billing_allowed", "prepaid_credits_allowed", "chargeable_fallback_allowed"]))

    def test_16_invalid_unapproved_model_rejected(self):
        args = chain(); args[2] = load(FIX / "invalid-unapproved-model.json")
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_static_chain(*args)
        self.assertEqual(cm.exception.code, "MODEL_NOT_ALLOWLISTED")

    def test_17_invalid_host_rejected(self):
        args = chain(); args[3] = load(FIX / "invalid-host-or-account-path.json")
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_static_chain(*args)
        self.assertEqual(cm.exception.code, "POLICY_MISMATCH")

    def test_18_invalid_data_broadening_rejected(self):
        args = chain(); args[4] = load(FIX / "invalid-data-broadening.json")
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_static_chain(*args)
        self.assertEqual(cm.exception.code, "DATA_NOT_ALLOWED")

    def test_19_invalid_nonzero_budget_rejected(self):
        args = chain(); args[6] = load(FIX / "invalid-nonzero-budget.json")
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_static_chain(*args)
        self.assertEqual(cm.exception.code, "NONZERO_BUDGET")

    def test_20_invalid_reserved_refs_rejected(self):
        bad = load(FIX / "invalid-credential-or-account-ref.json")
        with self.assertRaises(cf.CloudflareAdapterError) as cm: cf.validate_reserved_refs(bad["credential_profile_ref"], bad["account_ref"])
        self.assertEqual(cm.exception.code, "REFERENCE_MISMATCH")
