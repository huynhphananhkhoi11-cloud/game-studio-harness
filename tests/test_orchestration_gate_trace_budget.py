import copy
import json
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import orchestration_gate_trace_budget as subject


FIXTURES = Path(__file__).resolve().parents[1] / "platform/orchestration/fixtures/007e"
AS_OF = "2026-08-30T16:00:00Z"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class GateTraceBudgetTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load("valid-trace-chain.json")

    def assertInvalid(self, callable_):
        with self.assertRaises(subject.ValidationError):
            callable_()

    def test_valid_gate(self):
        self.assertEqual("gate-01", subject.validate_gate(load("valid-gate-result.json"), as_of=AS_OF)["gate_id"])

    def test_valid_budget(self):
        self.assertEqual("ZERO_COST", subject.validate_budget(load("valid-zero-cost-budget.json"), as_of=AS_OF)["cost_class"])

    def test_valid_bundle(self):
        self.assertEqual("STUDIO-007E", subject.validate_bundle(self.bundle, as_of=AS_OF)["work_order_id"])

    def test_evaluate_accept(self):
        self.assertEqual("PASS", subject.evaluate_attempt(self.bundle, as_of=AS_OF)["decision"])

    def test_evaluate_pause(self):
        self.bundle["quota"]["observed_changed_paths"] = 26
        self.assertEqual("PAUSE", subject.evaluate_attempt(self.bundle, as_of=AS_OF)["decision"])

    def test_evaluate_fail_for_invalid_evidence(self):
        self.bundle["gates"][0]["evidence_references"] = []
        self.assertEqual("FAIL", subject.evaluate_attempt(self.bundle, as_of=AS_OF)["decision"])

    def test_explain_valid_bundle(self):
        result = subject.explain_boundary(self.bundle, as_of=AS_OF)
        self.assertEqual([], result["blockers"])
        self.assertEqual(23, result["remaining"]["changed_paths"])
        self.assertEqual("request independent QA and review", result["next_safe_action"])

    def test_input_not_mutated(self):
        original = copy.deepcopy(self.bundle)
        subject.evaluate_attempt(self.bundle, as_of=AS_OF)
        self.assertEqual(original, self.bundle)

    def test_failed_validation_does_not_mutate_input(self):
        self.bundle["quota"]["observed_changed_paths"] = 26
        original = copy.deepcopy(self.bundle)
        self.assertEqual("PAUSE", subject.evaluate_attempt(self.bundle, as_of=AS_OF)["decision"])
        self.assertEqual(original, self.bundle)

    def test_digest_deterministic(self):
        self.assertEqual(subject.canonical_digest({"a": 1, "b": 2}), subject.canonical_digest({"b": 2, "a": 1}))

    def test_boundary_defaults(self):
        self.assertEqual(0, subject.explain_boundary()["limits"]["money_minor_units"])

    def test_missing_required_gate(self):
        self.bundle["gates"] = [g for g in self.bundle["gates"] if g["gate_type"] != "QA_ACCEPTANCE"]
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_failed_required_gate(self):
        self.bundle["gates"][0]["verdict"] = "FAIL"
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_duplicate_gate_identifier(self):
        self.bundle["gates"][1]["gate_id"] = self.bundle["gates"][0]["gate_id"]
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_future_gate(self):
        gate = load("valid-gate-result.json"); gate["evaluated_at"] = "2026-08-30T16:00:01Z"
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_prior_gate_pair_required(self):
        gate = load("valid-gate-result.json"); gate["prior_gate_id"] = "gate-old"
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_unknown_gate_type(self):
        gate = load("valid-gate-result.json"); gate["gate_type"] = "MAGIC"
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_trace_gap(self):
        self.bundle["trace_events"][1]["sequence_number"] = 3
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_duplicate_trace_identifier(self):
        self.bundle["trace_events"][1]["trace_event_id"] = "trace-01"
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_trace_attempt_regression(self):
        self.bundle["trace_events"][0]["attempt_number"] = 2
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_trace_attempt_must_match_gate_and_quota(self):
        self.bundle["trace_events"][1]["attempt_number"] = 2
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_quota_attempt_must_match_gate_and_trace(self):
        self.bundle["quota"]["attempt_number"] = 2
        self.bundle["quota"]["observed_attempts"] = 2
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_trace_state_continuity(self):
        self.bundle["trace_events"][1]["prior_state"] = "UNRELATED_STATE"
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_trace_future_gate_reference(self):
        self.bundle["trace_events"][0]["observed_at"] = "2026-08-30T15:00:00Z"
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_trace_missing_gate_reference(self):
        self.bundle["trace_events"][0]["gate_ids"].append("gate-missing")
        self.assertInvalid(lambda: subject.validate_bundle(self.bundle, as_of=AS_OF))

    def test_artifact_paths_sorted(self):
        gate = load("valid-gate-result.json"); gate["artifact_identity"]["changed_paths"].reverse()
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_artifact_duplicate_paths(self):
        gate = load("valid-gate-result.json"); gate["artifact_identity"]["changed_paths"] = ["a", "a"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_artifact_absolute_path(self):
        gate = load("valid-gate-result.json"); gate["artifact_identity"]["changed_paths"] = ["/tmp/a"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_artifact_windows_path(self):
        gate = load("valid-gate-result.json"); gate["artifact_identity"]["changed_paths"] = ["C:/tmp/a"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_non_owner_amendment(self):
        quota = load("valid-zero-cost-budget.json")
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"reviewer","approved_role":"QA","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"approved scope"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_valid_owner_path_amendment(self):
        quota = load("valid-zero-cost-budget.json")
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"approved scope"}]
        self.assertEqual(26, subject.validate_budget(quota, as_of=AS_OF)["observed_changed_paths"])

    def test_attempt_limit_not_amendable(self):
        quota = load("valid-zero-cost-budget.json")
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_attempts","prior_value":3,"new_value":4,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"retry"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_unused_amendment_rejected(self):
        quota = load("valid-zero-cost-budget.json")
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"scope"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_expired_owner_amendment_rejected(self):
        quota = load("valid-zero-cost-budget.json")
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T15:29:59Z","reason":"scope"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_amendment_wrong_work_order_rejected(self):
        quota = load("valid-zero-cost-budget.json")
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"OTHER","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"scope"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_amendment_wrong_attempt_rejected(self):
        quota = load("valid-zero-cost-budget.json")
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":2,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"scope"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_amendment_missing_evidence_digest_rejected(self):
        quota = load("valid-zero-cost-budget.json")
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"scope"}]
        self.assertInvalid(lambda: subject.validate_budget(quota, as_of=AS_OF))

    def test_control_character_rejected(self):
        gate = load("valid-gate-result.json"); gate["reasons"] = ["line\nbreak"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_password_assignment_rejected(self):
        gate = load("valid-gate-result.json"); gate["reasons"] = ["password=hunter2"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_token_assignment_rejected(self):
        gate = load("valid-gate-result.json"); gate["evidence_references"] = ["token:abc123secret"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_explain_uses_effective_owner_limit(self):
        quota = self.bundle["quota"]
        quota["observed_changed_paths"] = 26
        quota["owner_amendments"] = [{"amendment_id":"amend-1","limit_name":"max_changed_paths","prior_value":25,"new_value":30,"approved_by":"owner-1","approved_role":"STUDIO_OWNER","evidence_digest":"sha256:"+"b"*64,"work_order_id":"STUDIO-007E","attempt_number":1,"decided_at":"2026-08-30T15:00:00Z","expires_at":"2026-08-30T17:00:00Z","reason":"approved scope"}]
        result = subject.explain_boundary(self.bundle, as_of=AS_OF)
        self.assertEqual(30, result["limits"]["changed_paths"])
        self.assertEqual(4, result["remaining"]["changed_paths"])

    def test_amendment_schema_requires_utc_z(self):
        schema_path = Path(__file__).resolve().parents[1] / "platform/orchestration/schemas/quota-budget.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        amendment = schema["properties"]["owner_amendments"]["items"]["properties"]
        self.assertEqual("Z$", amendment["decided_at"]["pattern"])
        self.assertEqual("Z$", amendment["expires_at"]["pattern"])

    def test_secret_value_rejected(self):
        gate = load("valid-gate-result.json"); gate["reasons"] = ["Bearer abcdefghijklmnopqrstuvwxyz"]
        self.assertInvalid(lambda: subject.validate_gate(gate, as_of=AS_OF))

    def test_secret_safety_name_is_not_false_positive(self):
        gate = load("valid-gate-result.json"); gate["gate_type"] = "SECRET_SAFETY"
        self.assertEqual("SECRET_SAFETY", subject.validate_gate(gate, as_of=AS_OF)["gate_type"])

    def test_no_network_access(self):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network")):
            subject.validate_bundle(self.bundle, as_of=AS_OF)

    def test_no_subprocess_access(self):
        with mock.patch.object(subprocess, "run", side_effect=AssertionError("subprocess")):
            subject.validate_bundle(self.bundle, as_of=AS_OF)

    def test_cli_valid_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bundle.json"
            path.write_text(json.dumps(self.bundle), encoding="utf-8")
            self.assertEqual(0, subject.main(["validate-bundle", str(path), "--as-of", AS_OF]))

    def test_cli_invalid_bundle(self):
        self.bundle["quota"]["monetary_spend_minor_units"] = 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bundle.json"
            path.write_text(json.dumps(self.bundle), encoding="utf-8")
            self.assertEqual(1, subject.main(["validate-bundle", str(path), "--as-of", AS_OF]))


def _make_fixture_test(filename, validator):
    def test(self):
        value = load(filename)
        self.assertInvalid(lambda: validator(value))
    return test


_INVALID = {
    "invalid-missing-evidence.json": lambda x: subject.validate_gate(x, as_of=AS_OF),
    "invalid-unauthorized-gate.json": lambda x: subject.validate_gate(x, as_of=AS_OF),
    "invalid-mutable-artifact.json": lambda x: subject.validate_gate(x, as_of=AS_OF),
    "invalid-mismatched-artifact.json": lambda x: subject.validate_bundle(x, as_of=AS_OF),
    "invalid-broken-correlation.json": lambda x: subject.validate_bundle(x, as_of=AS_OF),
    "invalid-mutated-trace.json": lambda x: subject.validate_bundle(x, as_of=AS_OF),
    "invalid-attempt-ceiling.json": lambda x: subject.validate_budget(x, as_of=AS_OF),
    "invalid-time-ceiling.json": lambda x: subject.validate_budget(x, as_of=AS_OF),
    "invalid-path-ceiling.json": lambda x: subject.validate_budget(x, as_of=AS_OF),
    "invalid-output-ceiling.json": lambda x: subject.validate_budget(x, as_of=AS_OF),
    "invalid-nonzero-budget.json": lambda x: subject.validate_budget(x, as_of=AS_OF),
    "invalid-secret-field.json": lambda x: subject.validate_gate(x, as_of=AS_OF),
}
for _name, _validator in _INVALID.items():
    setattr(GateTraceBudgetTests, "test_fixture_" + _name[:-5].replace("-", "_"), _make_fixture_test(_name, _validator))


if __name__ == "__main__":
    unittest.main()
