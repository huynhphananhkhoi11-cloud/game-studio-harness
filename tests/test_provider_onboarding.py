from __future__ import annotations

import copy
import inspect
import json
import math
import unittest
from pathlib import Path

from scripts import provider_onboarding as po


ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "platform" / "connectivity" / "fixtures" / "009d"


def load(name: str):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def reseal(value):
    value = copy.deepcopy(value)
    value["canonical_digest"] = "sha256:" + "0" * 64
    value["canonical_digest"] = po.canonical_digest(value)
    return value


def valid_chain():
    profile_raw = load("valid-eligible-provider.json")
    child_raw = load("valid-child-contract-evidence.json")
    model_raw = load("valid-model-profile.json")
    profile = po.validate_provider_profile(profile_raw)
    child = po.validate_child_contract_evidence(child_raw, normalized_profile=profile)
    model = po.validate_model_profile(model_raw, normalized_profile=profile, normalized_child=child)
    binding_raw = {
        "schema_version": "1.0",
        "capability_binding_id": "provider-capability:synthetic-text",
        "provider_profile_id": profile["provider_profile_id"],
        "provider_profile_digest": profile["profile_digest"],
        "provider_model_profile_id": model["provider_model_profile_id"],
        "model_profile_digest": model["model_profile_digest"],
        "child_contract_id": child["child_contract_id"],
        "child_contract_digest": child["child_contract_digest"],
        "capability_id": "TEXT_GENERATION",
        "allowed_data_classifications": ["INTERNAL", "PUBLIC"],
        "max_request_bytes": 131072,
        "max_output_bytes": 131072,
        "owner_approval_ref": profile["owner_approval_ref"],
        "as_of": "2026-09-03T08:10:00Z",
        "canonical_digest": "sha256:" + "0" * 64,
    }
    binding_raw["canonical_digest"] = po.canonical_digest(binding_raw)
    binding = po.validate_capability_binding(
        binding_raw,
        normalized_profile=profile,
        normalized_child=child,
        normalized_model=model,
    )
    return profile_raw, child_raw, model_raw, binding_raw, profile, child, model, binding


class ProviderOnboardingTests(unittest.TestCase):
    def assertCode(self, code, fn):
        with self.assertRaises(po.ProviderOnboardingError) as ctx:
            fn()
        self.assertEqual(ctx.exception.code, code)
        self.assertNotIn("synthetic-alpha", ctx.exception.safe_message)

    def test_01_valid_disabled_profile(self):
        result = po.validate_provider_profile(load("valid-disabled-provider.json"))
        self.assertEqual(result["profile_status"], "DISABLED")
        self.assertEqual(result["money_ceiling"], 0)

    def test_02_valid_eligible_profile(self):
        result = po.validate_provider_profile(load("valid-eligible-provider.json"))
        self.assertEqual(result["profile_status"], "ELIGIBLE")
        self.assertNotIn("endpoint", result)

    def test_03_invalid_provider_identity_fixture(self):
        self.assertCode("INVALID_FORMAT", lambda: po.validate_provider_profile(load("invalid-provider-identity.json")))

    def test_04_invalid_nonzero_budget_fixture(self):
        self.assertCode("NONZERO_BUDGET", lambda: po.validate_provider_profile(load("invalid-nonzero-budget.json")))

    def test_05_active_state_forbidden(self):
        value = load("valid-eligible-provider.json")
        value["status"] = "ACTIVE"
        value = reseal(value)
        self.assertCode("ACTIVE_FORBIDDEN", lambda: po.validate_provider_profile(value))

    def test_06_profile_future_evidence(self):
        value = load("valid-eligible-provider.json")
        value["as_of"] = "2026-01-01T00:00:00Z"
        value = reseal(value)
        self.assertCode("FUTURE_EVIDENCE", lambda: po.validate_provider_profile(value))

    def test_07_profile_expired(self):
        value = load("valid-eligible-provider.json")
        value["as_of"] = "2027-01-01T00:00:00Z"
        value = reseal(value)
        self.assertCode("EXPIRED_PROFILE", lambda: po.validate_provider_profile(value))

    def test_08_profile_duplicate_identity(self):
        current = load("valid-eligible-provider.json")
        other = copy.deepcopy(current)
        other["provider_profile_id"] = "provider-profile:synthetic-beta"
        other = reseal(other)
        self.assertCode("DUPLICATE_PROVIDER", lambda: po.validate_provider_profile(other, existing_profiles=[current]))

    def test_09_profile_conflicting_same_id(self):
        current = load("valid-eligible-provider.json")
        other = copy.deepcopy(current)
        other["allowed_capabilities"] = ["CODE_ANALYSIS"]
        other = reseal(other)
        self.assertCode("DUPLICATE_PROVIDER", lambda: po.validate_provider_profile(other, existing_profiles=[current]))

    def test_10_profile_unknown_field(self):
        value = load("valid-eligible-provider.json")
        value["provider_name"] = "synthetic"
        self.assertCode("EXTRA_FIELD", lambda: po.validate_provider_profile(value))

    def test_11_profile_missing_owner(self):
        value = load("valid-eligible-provider.json")
        del value["owner_approval_ref"]
        self.assertCode("MISSING_FIELD", lambda: po.validate_provider_profile(value))

    def test_12_profile_secret_field(self):
        value = load("valid-eligible-provider.json")
        value["access_token"] = "secret-value"
        self.assertCode("SECRET_MATERIAL", lambda: po.validate_provider_profile(value))

    def test_13_profile_secret_like_value(self):
        value = load("valid-eligible-provider.json")
        value["provider_identity_ref"] = "provider-id:sk-ABCDEFGHIJKLMNOPQRSTUV"
        value = reseal(value)
        self.assertCode("SECRET_MATERIAL", lambda: po.validate_provider_profile(value))

    def test_14_duplicate_json_keys(self):
        text = '{"schema_version":"1.0","schema_version":"1.0"}'
        self.assertCode("DUPLICATE_JSON_KEY", lambda: po.load_json_document(text))

    def test_15_nonfinite_number(self):
        self.assertCode("INPUT_NUMBER", lambda: po.load_json_document('{"value":NaN}'))

    def test_16_input_size_bound(self):
        text = '{"x":"' + ("a" * (po.cb.MAX_INPUT_BYTES + 10)) + '"}'
        self.assertCode("INPUT_SIZE", lambda: po.load_json_document(text))

    def test_17_structure_depth_bound(self):
        value = {}
        cursor = value
        for i in range(po.cb.MAX_STRUCTURE_DEPTH + 3):
            cursor["x"] = {}
            cursor = cursor["x"]
        self.assertCode("STRUCTURE_LIMIT", lambda: po.validate_provider_profile(value))

    def test_18_unicode_surrogate_rejected(self):
        value = load("valid-eligible-provider.json")
        value["provider_identity_ref"] = "provider-id:\ud800"
        self.assertCode("INPUT_ENCODING", lambda: po.validate_provider_profile(value))

    def test_19_profile_input_immutable(self):
        value = load("valid-eligible-provider.json")
        before = copy.deepcopy(value)
        po.validate_provider_profile(value)
        self.assertEqual(value, before)

    def test_20_valid_child_contract(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        child = po.validate_child_contract_evidence(load("valid-child-contract-evidence.json"), normalized_profile=profile)
        self.assertEqual(child["evidence_class"], "SYNTHETIC")
        self.assertTrue(child["child_contract_id"].startswith("STUDIO-009P-"))

    def test_21_real_evidence_class_is_metadata_only(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        value = load("valid-child-contract-evidence.json")
        value["evidence_class"] = "REAL"
        value = reseal(value)
        child = po.validate_child_contract_evidence(value, normalized_profile=profile)
        self.assertEqual(child["evidence_class"], "REAL")
        self.assertNotIn("connected", child)

    def test_22_invalid_credential_profile_fixture(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        self.assertCode("LINEAGE_MISMATCH", lambda: po.validate_child_contract_evidence(load("invalid-credential-profile.json"), normalized_profile=profile))

    def test_23_child_profile_digest_mismatch(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        value = load("valid-child-contract-evidence.json")
        value["provider_profile_digest"] = "sha256:" + "1" * 64
        value = reseal(value)
        self.assertCode("LINEAGE_MISMATCH", lambda: po.validate_child_contract_evidence(value, normalized_profile=profile))

    def test_24_child_future_acceptance(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        value = load("valid-child-contract-evidence.json")
        value["accepted_at"] = "2026-10-01T00:00:00Z"
        value = reseal(value)
        self.assertCode("FUTURE_EVIDENCE", lambda: po.validate_child_contract_evidence(value, normalized_profile=profile))

    def test_25_child_expired(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        value = load("valid-child-contract-evidence.json")
        value["as_of"] = "2027-01-01T00:00:00Z"
        value = reseal(value)
        self.assertCode("EXPIRED_EVIDENCE", lambda: po.validate_child_contract_evidence(value, normalized_profile=profile))

    def test_26_child_revoked(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        value = load("valid-child-contract-evidence.json")
        value["revoked_at"] = "2026-09-03T08:05:00Z"
        value = reseal(value)
        self.assertCode("REVOKED_EVIDENCE", lambda: po.validate_child_contract_evidence(value, normalized_profile=profile))

    def test_27_valid_model_profile(self):
        _, _, _, _, profile, child, _, _ = valid_chain()
        model = po.validate_model_profile(load("valid-model-profile.json"), normalized_profile=profile, normalized_child=child)
        self.assertEqual(model["model_status"], "ELIGIBLE")

    def test_28_invalid_model_scope_fixture(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        child = po.validate_child_contract_evidence(load("valid-child-contract-evidence.json"), normalized_profile=profile)
        self.assertCode("SCOPE_BROADENING", lambda: po.validate_model_profile(load("invalid-model-scope.json"), normalized_profile=profile, normalized_child=child))

    def test_29_invalid_data_policy_fixture(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        child = po.validate_child_contract_evidence(load("valid-child-contract-evidence.json"), normalized_profile=profile)
        self.assertCode("SCOPE_BROADENING", lambda: po.validate_model_profile(load("invalid-data-policy-broadening.json"), normalized_profile=profile, normalized_child=child))

    def test_30_model_lineage_mismatch(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        child = po.validate_child_contract_evidence(load("valid-child-contract-evidence.json"), normalized_profile=profile)
        value = load("valid-model-profile.json")
        value["child_contract_digest"] = "sha256:" + "2" * 64
        value = reseal(value)
        self.assertCode("LINEAGE_MISMATCH", lambda: po.validate_model_profile(value, normalized_profile=profile, normalized_child=child))

    def test_31_model_owner_mismatch(self):
        profile = po.validate_provider_profile(load("valid-eligible-provider.json"))
        child = po.validate_child_contract_evidence(load("valid-child-contract-evidence.json"), normalized_profile=profile)
        value = load("valid-model-profile.json")
        value["owner_approval_ref"] = "owner-approval:other"
        value = reseal(value)
        self.assertCode("OWNER_APPROVAL_REQUIRED", lambda: po.validate_model_profile(value, normalized_profile=profile, normalized_child=child))

    def test_32_valid_capability_binding(self):
        *_, binding = valid_chain()
        self.assertEqual(binding["capability_id"], "TEXT_GENERATION")

    def test_33_undeclared_capability(self):
        profile_raw, child_raw, model_raw, binding_raw, profile, child, model, _ = valid_chain()
        binding_raw["capability_id"] = "IMAGE_GENERATION"
        binding_raw = reseal(binding_raw)
        self.assertCode("UNDECLARED_CAPABILITY", lambda: po.validate_capability_binding(binding_raw, normalized_profile=profile, normalized_child=child, normalized_model=model))

    def test_34_capability_data_broadening(self):
        _, _, _, binding_raw, profile, child, model, _ = valid_chain()
        binding_raw["allowed_data_classifications"] = ["RESTRICTED"]
        binding_raw = reseal(binding_raw)
        self.assertCode("SCOPE_BROADENING", lambda: po.validate_capability_binding(binding_raw, normalized_profile=profile, normalized_child=child, normalized_model=model))

    def test_35_capability_model_lineage_mismatch(self):
        _, _, _, binding_raw, profile, child, model, _ = valid_chain()
        binding_raw["model_profile_digest"] = "sha256:" + "3" * 64
        binding_raw = reseal(binding_raw)
        self.assertCode("LINEAGE_MISMATCH", lambda: po.validate_capability_binding(binding_raw, normalized_profile=profile, normalized_child=child, normalized_model=model))

    def test_36_eligibility_success(self):
        *_, profile, child, model, binding = valid_chain()
        plan = po.plan_eligibility(profile, normalized_child=child, normalized_model=model, normalized_binding=binding, as_of="2026-09-03T08:10:00Z")
        self.assertEqual(plan.eligibility, "ELIGIBLE")
        self.assertEqual(plan.refusal_code, "NONE")
        self.assertNotIn("endpoint", plan.to_dict())

    def test_37_eligibility_missing_child_fixture(self):
        data = load("invalid-missing-child-contract.json")
        profile = po.validate_provider_profile(data["provider_profile"])
        plan = po.plan_eligibility(profile, normalized_child=None, normalized_model=None, normalized_binding=None, as_of=data["as_of"])
        self.assertEqual(plan.refusal_code, "MISSING_CHILD_CONTRACT")

    def test_38_eligibility_paused(self):
        *_, profile, child, model, binding = valid_chain()
        profile = dict(profile)
        profile["profile_status"] = "PAUSED"
        plan = po.plan_eligibility(profile, normalized_child=child, normalized_model=model, normalized_binding=binding, as_of="2026-09-03T08:10:00Z")
        self.assertEqual(plan.refusal_code, "PAUSED_PROFILE")

    def test_39_eligibility_revoked(self):
        *_, profile, child, model, binding = valid_chain()
        profile = dict(profile)
        profile["profile_status"] = "REVOKED"
        plan = po.plan_eligibility(profile, normalized_child=child, normalized_model=model, normalized_binding=binding, as_of="2026-09-03T08:10:00Z")
        self.assertEqual(plan.refusal_code, "REVOKED_PROFILE")

    def test_40_register_candidate_event(self):
        profile_raw = load("valid-disabled-provider.json")
        profile_raw["status"] = "CANDIDATE"
        profile_raw = reseal(profile_raw)
        profile = po.validate_provider_profile(profile_raw)
        event = {
            "schema_version": "1.0",
            "provider_onboarding_event_id": "provider-event:register-synthetic",
            "provider_profile_id": profile["provider_profile_id"],
            "provider_profile_digest": profile["profile_digest"],
            "child_contract_id": None,
            "child_contract_digest": None,
            "action": "REGISTER_CANDIDATE",
            "owner_approval_ref": profile["owner_approval_ref"],
            "control_ref": "control:studio-009d",
            "as_of": "2026-09-03T08:10:00Z",
            "canonical_digest": "sha256:" + "0" * 64,
        }
        event["canonical_digest"] = po.canonical_digest(event)
        result = po.normalize_onboarding_event(event, normalized_profile=profile)
        self.assertEqual(result["action"], "REGISTER_CANDIDATE")

    def test_41_mark_eligible_event(self):
        *_, profile, child, model, binding = valid_chain()
        profile = dict(profile)
        profile["profile_status"] = "DISABLED"
        event = {
            "schema_version": "1.0",
            "provider_onboarding_event_id": "provider-event:eligible-synthetic",
            "provider_profile_id": profile["provider_profile_id"],
            "provider_profile_digest": profile["profile_digest"],
            "child_contract_id": child["child_contract_id"],
            "child_contract_digest": child["child_contract_digest"],
            "action": "MARK_ELIGIBLE",
            "owner_approval_ref": profile["owner_approval_ref"],
            "control_ref": "control:studio-009d",
            "as_of": "2026-09-03T08:10:00Z",
            "canonical_digest": "sha256:" + "0" * 64,
        }
        event["canonical_digest"] = po.canonical_digest(event)
        result = po.normalize_onboarding_event(event, normalized_profile=profile, normalized_child=child)
        self.assertEqual(result["action"], "MARK_ELIGIBLE")

    def test_42_mark_eligible_requires_child(self):
        profile = po.validate_provider_profile(load("valid-disabled-provider.json"))
        event = {
            "schema_version": "1.0",
            "provider_onboarding_event_id": "provider-event:no-child",
            "provider_profile_id": profile["provider_profile_id"],
            "provider_profile_digest": profile["profile_digest"],
            "child_contract_id": None,
            "child_contract_digest": None,
            "action": "MARK_ELIGIBLE",
            "owner_approval_ref": profile["owner_approval_ref"],
            "control_ref": "control:studio-009d",
            "as_of": "2026-09-03T08:10:00Z",
            "canonical_digest": "sha256:" + "0" * 64,
        }
        event["canonical_digest"] = po.canonical_digest(event)
        self.assertCode("MISSING_CHILD_CONTRACT", lambda: po.normalize_onboarding_event(event, normalized_profile=profile))

    def test_43_safe_error_does_not_echo_input(self):
        value = load("valid-eligible-provider.json")
        value["provider_identity_ref"] = "UNTRUSTED-SENTINEL"
        try:
            po.validate_provider_profile(value)
        except po.ProviderOnboardingError as exc:
            self.assertNotIn("UNTRUSTED-SENTINEL", str(exc))
            self.assertNotIn("UNTRUSTED-SENTINEL", exc.safe_message)
        else:
            self.fail("expected rejection")

    def test_44_production_source_has_no_live_runtime_calls(self):
        source = inspect.getsource(po)
        forbidden = (
            "import socket", "import requests", "urllib.request", "import subprocess",
            "os.environ", "getenv(", "keyring", "Credential Manager",
            "boto3", "google.cloud", "httpx", "grpc", "websocket",
            "datetime.now(", "utcnow(", "time.time(",
        )
        for token in forbidden:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
