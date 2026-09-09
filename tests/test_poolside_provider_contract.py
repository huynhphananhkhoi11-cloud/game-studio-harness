from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts import poolside_adapter as ps

ROOT = Path(__file__).resolve().parents[1]
PROVIDER = ROOT / "platform/connectivity/providers/poolside"
FIX = ROOT / "platform/connectivity/fixtures/009p04"


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def chain():
    return [
        load(PROVIDER / "provider-profile.json"),
        load(PROVIDER / "child-contract-evidence.json"),
        load(PROVIDER / "model-profile-laguna-s-2.1.json"),
        load(PROVIDER / "transport-policy.json"),
        load(PROVIDER / "data-policy.json"),
        load(PROVIDER / "quota-policy.json"),
        load(PROVIDER / "budget-policy.json"),
    ]


class PoolsideProviderContractTests(unittest.TestCase):
    def assert_code(self, code, func, *args):
        with self.assertRaises(ps.PoolsideAdapterError) as cm:
            func(*args)
        self.assertEqual(cm.exception.code, code)

    def test_01_valid_static_chain(self):
        out = ps.validate_static_chain(*chain())
        self.assertEqual(out["provider_state"], "DISABLED")
        self.assertEqual(out["model_state"], "DECLARED")
        self.assertEqual(out["child_evidence_class"], "SYNTHETIC")

    def test_02_exact_provider_identity(self):
        self.assertEqual(load(PROVIDER / "provider-profile.json")["provider_profile_id"], ps.PROVIDER_PROFILE_ID)

    def test_03_exact_model_identity(self):
        self.assertEqual(load(PROVIDER / "model-profile-laguna-s-2.1.json")["model_identity_ref"], ps.MODEL_IDENTITY_REF)

    def test_04_capabilities_exact(self):
        self.assertEqual(load(PROVIDER / "provider-profile.json")["allowed_capabilities"], ["REASONING", "TEXT_GENERATION"])

    def test_05_money_zero(self):
        self.assertEqual(load(PROVIDER / "provider-profile.json")["money_ceiling"], 0)

    def test_06_transport_host_exact(self):
        self.assertEqual(load(PROVIDER / "transport-policy.json")["host"], "inference.poolside.ai")

    def test_07_transport_path_exact(self):
        t = load(PROVIDER / "transport-policy.json")
        self.assertEqual(t["chat_completions_path"], "/v1/chat/completions")
        self.assertEqual(t["canonical_base_url"], "https://inference.poolside.ai/v1")

    def test_08_redirects_disabled(self):
        self.assertFalse(load(PROVIDER / "transport-policy.json")["allow_redirects"])

    def test_09_third_party_gateway_disabled(self):
        self.assertFalse(load(PROVIDER / "transport-policy.json")["third_party_gateway_allowed"])

    def test_10_enterprise_endpoint_disabled(self):
        self.assertFalse(load(PROVIDER / "transport-policy.json")["enterprise_deployment_endpoint_allowed"])

    def test_11_local_self_hosted_disabled(self):
        self.assertFalse(load(PROVIDER / "transport-policy.json")["local_or_self_hosted_allowed"])

    def test_12_transport_offline(self):
        self.assertEqual(load(PROVIDER / "transport-policy.json")["network_activation"], "NONE_P04_OFFLINE")

    def test_13_data_public_only(self):
        self.assertEqual(load(PROVIDER / "data-policy.json")["allowed_data_classifications"], ["PUBLIC"])

    def test_14_private_export_forbidden(self):
        self.assertFalse(load(PROVIDER / "data-policy.json")["private_or_unreleased_export_allowed"])

    def test_15_personal_confidential_forbidden(self):
        d = load(PROVIDER / "data-policy.json")
        self.assertFalse(d["personal_data_allowed"])
        self.assertFalse(d["confidential_or_sensitive_data_allowed"])

    def test_16_training_risk_acknowledged(self):
        self.assertTrue(load(PROVIDER / "data-policy.json")["provider_training_use_risk_acknowledged"])

    def test_17_training_opt_out_does_not_broaden(self):
        self.assertFalse(load(PROVIDER / "data-policy.json")["training_opt_out_broadens_game_authority"])

    def test_18_feedback_submission_forbidden(self):
        self.assertFalse(load(PROVIDER / "data-policy.json")["feedback_submission_allowed"])

    def test_19_dynamic_quota_no_permanent_entitlement(self):
        q = load(PROVIDER / "quota-policy.json")["provider_snapshot"]
        self.assertEqual(q["availability"], "FREE_FOR_LIMITED_TIME_DYNAMIC")
        self.assertIsNone(q["permanent_rpm"])
        self.assertIsNone(q["permanent_rpd"])
        self.assertIsNone(q["free_window_expiry"])

    def test_20_future_v04_request_count(self):
        self.assertEqual(load(PROVIDER / "quota-policy.json")["future_v04_limits"]["max_real_requests"], 3)

    def test_21_future_v04_serial_no_retry(self):
        v = load(PROVIDER / "quota-policy.json")["future_v04_limits"]
        self.assertEqual((v["max_concurrency"], v["max_retries"], v["timeout_seconds"]), (1, 0, 60))

    def test_22_future_v04_token_bounds(self):
        v = load(PROVIDER / "quota-policy.json")["future_v04_limits"]
        self.assertEqual((v["max_input_tokens"], v["max_output_tokens"]), (4096, 1024))

    def test_23_future_v04_byte_bounds(self):
        v = load(PROVIDER / "quota-policy.json")["future_v04_limits"]
        self.assertEqual((v["max_request_bytes"], v["max_response_bytes"]), (32768, 131072))

    def test_24_future_v04_capabilities_disabled(self):
        v = load(PROVIDER / "quota-policy.json")["future_v04_limits"]
        self.assertFalse(v["streaming"])
        self.assertFalse(v["tools"])
        self.assertFalse(v["mcp"])
        self.assertFalse(v["acp"])

    def test_25_budget_zero(self):
        b = load(PROVIDER / "budget-policy.json")
        self.assertEqual(b["money_ceiling"], 0)
        self.assertTrue(b["zero_cost_route_required"])

    def test_26_paid_paths_forbidden(self):
        b = load(PROVIDER / "budget-policy.json")
        for field in (
            "paid_subscription_allowed", "payment_method_requirement_allowed",
            "credit_purchase_allowed", "auto_recharge_allowed",
            "paid_fallback_allowed", "third_party_paid_gateway_allowed",
            "self_hosted_spend_allowed", "production_use_allowed",
        ):
            self.assertFalse(b[field], field)

    def test_27_reserved_refs_valid(self):
        out = ps.validate_reserved_refs(ps.CREDENTIAL_PROFILE_REF, ps.ACCOUNT_REF)
        self.assertEqual(out["account_ref"], ps.ACCOUNT_REF)

    def test_28_invalid_reserved_ref_rejected(self):
        bad = load(FIX / "invalid-credential-ref.json")
        self.assert_code("REFERENCE_MISMATCH", ps.validate_reserved_refs, bad["credential_profile_ref"], bad["account_ref"])

    def test_29_invalid_model_rejected(self):
        args = chain()
        args[2] = load(FIX / "invalid-unapproved-model.json")
        with self.assertRaises(ps.PoolsideAdapterError):
            ps.validate_static_chain(*args)

    def test_30_invalid_host_rejected(self):
        args = chain()
        args[3] = load(FIX / "invalid-host-or-path.json")
        self.assert_code("POLICY_MISMATCH", ps.validate_static_chain, *args)

    def test_31_invalid_data_broadening_rejected(self):
        args = chain()
        args[4] = load(FIX / "invalid-data-broadening.json")
        self.assert_code("DATA_NOT_ALLOWED", ps.validate_static_chain, *args)

    def test_32_invalid_nonzero_budget_rejected(self):
        args = chain()
        args[6] = load(FIX / "invalid-nonzero-budget.json")
        self.assert_code("NONZERO_BUDGET", ps.validate_static_chain, *args)

    def test_33_chain_immutable(self):
        args = chain()
        before = copy.deepcopy(args)
        ps.validate_static_chain(*args)
        self.assertEqual(args, before)

    def test_34_redirect_broadening_rejected(self):
        args = chain()
        args[3]["allow_redirects"] = True
        self.assert_code("POLICY_MISMATCH", ps.validate_static_chain, *args)

    def test_35_network_activation_broadening_rejected(self):
        args = chain()
        args[3]["network_activation"] = "LIVE"
        self.assert_code("POLICY_MISMATCH", ps.validate_static_chain, *args)

    def test_36_gateway_broadening_rejected(self):
        args = chain()
        args[3]["third_party_gateway_allowed"] = True
        self.assert_code("POLICY_MISMATCH", ps.validate_static_chain, *args)
