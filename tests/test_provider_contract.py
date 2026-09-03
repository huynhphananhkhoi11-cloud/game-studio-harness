from __future__ import annotations

import ast
import copy
import json
import re
import unittest
from pathlib import Path

from scripts import provider_onboarding as po


ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "platform" / "connectivity" / "fixtures" / "009d"
SCHEMAS = ROOT / "platform" / "connectivity" / "schemas"
TEMPLATE = ROOT / "tasks" / "STUDIO-009P-TEMPLATE.md"
DOC = ROOT / "platform" / "connectivity" / "PROVIDER_ONBOARDING.md"
SOURCE = ROOT / "scripts" / "provider_onboarding.py"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ProviderContractTests(unittest.TestCase):
    def test_01_exact_five_schemas_present(self):
        expected = {
            "provider-profile.schema.json",
            "provider-model.schema.json",
            "provider-capability-binding.schema.json",
            "provider-child-contract-evidence.schema.json",
            "provider-onboarding-event.schema.json",
        }
        observed = {p.name for p in SCHEMAS.glob("provider-*.schema.json") if p.name in expected}
        self.assertEqual(observed, expected)

    def test_02_schemas_fail_closed_on_extra_fields(self):
        for path in SCHEMAS.glob("provider-*.schema.json"):
            schema = load_json(path)
            self.assertIs(schema.get("additionalProperties"), False, path.name)
            self.assertEqual(set(schema["required"]), set(schema["properties"]), path.name)

    def test_03_schemas_define_no_raw_secret_fields(self):
        forbidden = {"token","access_token","refresh_token","password","passwd","secret","secret_value","private_key","api_key","authorization","cookie","session"}
        for path in SCHEMAS.glob("provider-*.schema.json"):
            props = set(load_json(path)["properties"])
            self.assertTrue(props.isdisjoint(forbidden), path.name)

    def test_04_ten_json_fixtures_present(self):
        self.assertEqual(len(list(FIX.glob("*.json"))), 10)

    def test_05_all_provider_fixtures_are_synthetic(self):
        text = "\n".join(p.read_text(encoding="utf-8").lower() for p in FIX.glob("*.json"))
        for real_name in ("openai", "anthropic", "gemini", "claude", "grok", "deepseek", "mistral"):
            self.assertNotIn(real_name, text)
        self.assertIn("synthetic", text)

    def test_06_valid_fixture_digests_are_canonical(self):
        for name in ("valid-disabled-provider.json","valid-eligible-provider.json","valid-model-profile.json","valid-child-contract-evidence.json"):
            value = load_json(FIX / name)
            self.assertEqual(value["canonical_digest"], po.canonical_digest(value), name)

    def test_07_invalid_fixture_digests_still_bind_their_mutated_record(self):
        for name in ("invalid-provider-identity.json","invalid-model-scope.json","invalid-data-policy-broadening.json","invalid-credential-profile.json","invalid-nonzero-budget.json"):
            value = load_json(FIX / name)
            self.assertEqual(value["canonical_digest"], po.canonical_digest(value), name)

    def test_08_template_requires_provider_identity_and_sources(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("authoritative provider", text)
        self.assertIn("authoritative source", text)

    def test_09_template_requires_model_and_endpoint_policy(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("Model identity and version policy", text)
        self.assertIn("Endpoint, host, and transport allowlist", text)

    def test_10_template_requires_credential_and_data_policy(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("credential_profile_ref", text)
        self.assertIn("Data export, retention, and training policy", text)

    def test_11_template_requires_quota_and_budget_window(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("Quota, rate, timeout, and retry limits", text)
        self.assertIn("currency", text)
        self.assertIn("time window", text)

    def test_12_template_requires_kill_incident_rollback_and_gates(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        for phrase in ("Kill switch", "Incident response", "MANUAL/FAKE rollback", "QA and Review"):
            self.assertIn(phrase, text)

    def test_13_template_requires_studio_009f_for_activation(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("STUDIO-009F", text)
        self.assertIn("DOES NOT activate", text)

    def test_14_framework_doc_states_eligible_is_not_live(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("ELIGIBLE", text)
        self.assertIn("does not approve or activate a real provider", text)

    def test_15_source_imports_have_no_network_provider_or_subprocess_modules(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        forbidden = {"socket","requests","urllib","httpx","grpc","websocket","subprocess","os","keyring","boto3"}
        self.assertTrue(imports.isdisjoint(forbidden), imports & forbidden)

    def test_16_source_exposes_no_active_provider_state_or_production_constructor(self):
        self.assertNotIn("ACTIVE", po.PROFILE_STATUSES)
        self.assertFalse(hasattr(po, "connect_provider"))
        self.assertFalse(hasattr(po, "create_transport"))
        self.assertFalse(hasattr(po, "resolve_credential"))
        self.assertFalse(hasattr(po, "route_request"))


if __name__ == "__main__":
    unittest.main()
