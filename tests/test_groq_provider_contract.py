from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts import groq_provider_adapter as ga
from scripts import provider_onboarding as po


ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "platform" / "connectivity" / "providers" / "groq"
FIX = ROOT / "platform" / "connectivity" / "fixtures" / "009p01"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class GroqProviderContractTests(unittest.TestCase):
    def test_01_contract_is_child_only(self):
        text = (ROOT / "tasks" / "STUDIO-009P-01.md").read_text(encoding="utf-8")
        self.assertIn("CONTRACT ONLY", text)
        self.assertIn("STUDIO-009F", text)
        self.assertIn("Monetary ceiling: integer zero", text)

    def test_02_implementation_scope_is_exact_20(self):
        text = (ROOT / "tasks" / "STUDIO-009P-01-IMPLEMENTATION.md").read_text(encoding="utf-8")
        section = text.split("## Implementation boundary", 1)[0]
        paths = re.findall(r"^\d+\. `([^`]+)`$", section, flags=re.M)
        self.assertEqual(len(paths), 20)
        self.assertEqual(len(set(paths)), 20)
        self.assertIn("scripts/groq_provider_adapter.py", paths)

    def test_03_provider_profile_valid_but_disabled(self):
        raw = load(PROV / "provider-profile.json")
        normalized = po.validate_provider_profile(raw)
        self.assertEqual(normalized["profile_status"], "DISABLED")
        self.assertEqual(normalized["money_ceiling"], 0)
        self.assertEqual(normalized["allowed_data_classifications"], ("PUBLIC",))

    def test_04_child_evidence_is_synthetic(self):
        profile = po.validate_provider_profile(load(PROV / "provider-profile.json"))
        child = po.validate_child_contract_evidence(
            load(PROV / "child-contract-evidence.json"), normalized_profile=profile
        )
        self.assertEqual(child["child_contract_id"], "STUDIO-009P-01")
        self.assertEqual(child["evidence_class"], "SYNTHETIC")

    def test_05_model_is_declared_and_exact(self):
        profile = po.validate_provider_profile(load(PROV / "provider-profile.json"))
        child = po.validate_child_contract_evidence(
            load(PROV / "child-contract-evidence.json"), normalized_profile=profile
        )
        model = po.validate_model_profile(
            load(PROV / "model-profile-gpt-oss-120b.json"),
            normalized_profile=profile,
            normalized_child=child,
        )
        self.assertEqual(model["model_status"], "DECLARED")
        self.assertEqual(model["model_identity_ref"], "model-id:openai/gpt-oss-120b")

    def test_06_full_static_chain_is_disabled(self):
        result = ga.validate_static_chain(
            load(PROV / "provider-profile.json"),
            load(PROV / "child-contract-evidence.json"),
            load(PROV / "model-profile-gpt-oss-120b.json"),
            load(PROV / "transport-policy.json"),
            load(PROV / "data-policy.json"),
            load(PROV / "quota-policy.json"),
            load(PROV / "budget-policy.json"),
        )
        self.assertEqual(result["provider_state"], "DISABLED")
        self.assertEqual(result["network_authority"], "NONE")
        self.assertEqual(result["money_ceiling"], 0)

    def test_07_unapproved_model_fixture_fails(self):
        with self.assertRaises(ga.GroqAdapterError) as ctx:
            ga.validate_static_chain(
                load(FIX / "valid-groq-provider.json"),
                load(FIX / "valid-groq-child-evidence.json"),
                load(FIX / "invalid-unapproved-model.json"),
                load(PROV / "transport-policy.json"),
                load(PROV / "data-policy.json"),
                load(PROV / "quota-policy.json"),
                load(PROV / "budget-policy.json"),
            )
        self.assertEqual(ctx.exception.code, "MODEL_NOT_ALLOWLISTED")

    def test_08_invalid_host_fixture_fails(self):
        with self.assertRaises(ga.GroqAdapterError) as ctx:
            ga.validate_static_chain(
                load(PROV / "provider-profile.json"),
                load(PROV / "child-contract-evidence.json"),
                load(PROV / "model-profile-gpt-oss-120b.json"),
                load(FIX / "invalid-host.json"),
                load(PROV / "data-policy.json"),
                load(PROV / "quota-policy.json"),
                load(PROV / "budget-policy.json"),
            )
        self.assertEqual(ctx.exception.code, "POLICY_MISMATCH")

    def test_09_data_broadening_fixture_fails(self):
        with self.assertRaises(ga.GroqAdapterError) as ctx:
            ga.validate_static_chain(
                load(PROV / "provider-profile.json"),
                load(PROV / "child-contract-evidence.json"),
                load(PROV / "model-profile-gpt-oss-120b.json"),
                load(PROV / "transport-policy.json"),
                load(FIX / "invalid-data-broadening.json"),
                load(PROV / "quota-policy.json"),
                load(PROV / "budget-policy.json"),
            )
        self.assertEqual(ctx.exception.code, "DATA_NOT_ALLOWED")

    def test_10_nonzero_budget_fixture_fails(self):
        with self.assertRaises(ga.GroqAdapterError) as ctx:
            ga.validate_static_chain(
                load(PROV / "provider-profile.json"),
                load(PROV / "child-contract-evidence.json"),
                load(PROV / "model-profile-gpt-oss-120b.json"),
                load(PROV / "transport-policy.json"),
                load(PROV / "data-policy.json"),
                load(PROV / "quota-policy.json"),
                load(FIX / "invalid-nonzero-budget.json"),
            )
        self.assertEqual(ctx.exception.code, "NONZERO_BUDGET")

    def test_11_invalid_credential_lineage_fails_closed(self):
        with self.assertRaises(ga.GroqAdapterError) as ctx:
            ga.validate_static_chain(
                load(PROV / "provider-profile.json"),
                load(FIX / "invalid-credential-ref.json"),
                load(PROV / "model-profile-gpt-oss-120b.json"),
                load(PROV / "transport-policy.json"),
                load(PROV / "data-policy.json"),
                load(PROV / "quota-policy.json"),
                load(PROV / "budget-policy.json"),
            )
        self.assertEqual(ctx.exception.code, "CONTRACT_METADATA_INVALID")

    def test_12_policy_files_contain_no_credential_value(self):
        combined = "\n".join(
            (PROV / name).read_text(encoding="utf-8")
            for name in (
                "provider-profile.json", "model-profile-gpt-oss-120b.json",
                "child-contract-evidence.json", "transport-policy.json",
                "data-policy.json", "quota-policy.json", "budget-policy.json",
            )
        )
        self.assertNotRegex(combined, r"\bsk-[A-Za-z0-9_-]{16,}\b")
        self.assertNotIn("Bearer ", combined)

    def test_13_readme_keeps_connected_gate(self):
        text = (PROV / "README.md").read_text(encoding="utf-8")
        self.assertIn("STUDIO-009F remains the only connected activation gate", text)
        self.assertIn("no provider SDK", text)

    def test_14_memory_records_zero_activity(self):
        state = (ROOT / "studio" / "memory" / "tasks" / "STUDIO-009P-01" / "STATE.md").read_text(encoding="utf-8")
        self.assertIn("money_ceiling: 0", state)
        self.assertIn("provider_runtime_activity: NONE", state)
        self.assertIn("network_activity: NONE", state)
        self.assertIn("connected_execution_activity: NONE", state)
