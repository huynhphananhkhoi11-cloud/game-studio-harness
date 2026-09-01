
import copy
import json
import unittest
from pathlib import Path

from scripts.orchestration_pilot import PilotValidationError, canonical_digest, load_json, validate_bundle, validate_scenario


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "platform/orchestration/fixtures/008"
AS_OF = "2026-09-01T06:00:00Z"


class PilotScenarioTests(unittest.TestCase):
    def load(self, name):
        return load_json(FIXTURES / name)

    def assert_invalid_scenario(self, name, code):
        record = self.load(name)
        before = copy.deepcopy(record)
        with self.assertRaisesRegex(PilotValidationError, code):
            validate_scenario(record, AS_OF)
        self.assertEqual(before, record)

    def assert_mutation_fails(self, name, code, mutation, supplied_as_of=AS_OF):
        record = self.load(name)
        mutation(record)
        record["expected_digest"] = canonical_digest(record)
        before = copy.deepcopy(record)
        with self.assertRaisesRegex(PilotValidationError, code):
            validate_scenario(record, supplied_as_of)
        self.assertEqual(before, record)

    def test_p01_research_handoff(self):
        result = validate_scenario(self.load("valid-p01-research-handoff.json"), AS_OF)
        self.assertEqual("P01", result["scenario_id"])

    def test_p02_engineering_work(self):
        self.assertEqual("PASS", validate_scenario(self.load("valid-p02-engineering-work.json"), AS_OF)["verdict"])

    def test_p03_simulated_failover(self):
        self.assertEqual("PASS", validate_scenario(self.load("valid-p03-simulated-failover.json"), AS_OF)["verdict"])

    def test_p04_writer_conflict(self):
        self.assertEqual("PASS", validate_scenario(self.load("valid-p04-writer-conflict.json"), AS_OF)["verdict"])

    def test_p05_qa_correction(self):
        self.assertEqual("PASS", validate_scenario(self.load("valid-p05-qa-correction.json"), AS_OF)["verdict"])

    def test_p06_approve(self):
        self.assertEqual("PASS", validate_scenario(self.load("valid-p06-owner-gate-approve.json"), AS_OF)["verdict"])

    def test_p06_reject(self):
        self.assertEqual("PASS", validate_scenario(self.load("valid-p06-owner-gate-reject.json"), AS_OF)["verdict"])

    def test_key_order_stable_digest(self):
        record = self.load("valid-p01-research-handoff.json")
        reversed_record = dict(reversed(list(record.items())))
        self.assertEqual(canonical_digest(record), canonical_digest(reversed_record))

    def test_wrong_as_of_fails_closed(self):
        record = self.load("valid-p01-research-handoff.json")
        with self.assertRaisesRegex(PilotValidationError, "AS_OF"):
            validate_scenario(record, "2026-09-01T06:00:01Z")

    def test_extra_field_fails_closed(self):
        record = self.load("valid-p01-research-handoff.json")
        record["extra"] = True
        record["expected_digest"] = canonical_digest(record)
        with self.assertRaisesRegex(PilotValidationError, "FIELD_SET"):
            validate_scenario(record, AS_OF)

    def test_secret_like_key_fails_closed(self):
        record = self.load("valid-p01-research-handoff.json")
        record["evidence"]["api_key"] = "not-a-real-secret"
        record["expected_digest"] = canonical_digest(record)
        with self.assertRaisesRegex(PilotValidationError, "SECRET_LIKE_EVIDENCE"):
            validate_scenario(record, AS_OF)

    def test_trace_gap_fails_closed(self):
        record = self.load("valid-p03-simulated-failover.json")
        record["trace"][1]["sequence"] = 3
        record["expected_digest"] = canonical_digest(record)
        with self.assertRaisesRegex(PilotValidationError, "TRACE_SEQUENCE"):
            validate_scenario(record, AS_OF)

    def test_validation_is_read_only(self):
        record = self.load("valid-p05-qa-correction.json")
        before = json.dumps(record, sort_keys=True)
        validate_scenario(record, AS_OF)
        self.assertEqual(before, json.dumps(record, sort_keys=True))

    def test_nonhex_attempt_head_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "HEAD_SHA",
            lambda value: value["attempts"][0].__setitem__("head_sha", "z" * 40),
        )

    def test_unknown_trace_attempt_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "TRACE_ATTEMPT",
            lambda value: value["trace"][0].__setitem__("attempt_id", "unknown-attempt"),
        )

    def test_unauthorized_gate_role_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "GATE_AUTHORITY",
            lambda value: value["gates"][0].__setitem__("role", "STUDIO_OWNER"),
        )

    def test_gate_head_must_bind_known_attempt(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "GATE_HEAD",
            lambda value: value["gates"][0].__setitem__("head_sha", "2" * 40),
        )

    def test_p02_unsafe_relative_path_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p02-engineering-work.json", "P02_PATHS",
            lambda value: value["claims"][0].__setitem__("paths", ["../escape.txt"]),
        )

    def test_p03_requires_old_writer_release(self):
        self.assert_mutation_fails(
            "valid-p03-simulated-failover.json", "P03_WRITER_RELEASE",
            lambda value: value["evidence"].__setitem__("old_attempt_writer_released", False),
        )

    def test_p04_derives_overlap_from_claim_paths(self):
        self.assert_mutation_fails(
            "valid-p04-writer-conflict.json", "P04_OVERLAP_PROOF",
            lambda value: value["claims"][1].__setitem__("paths", ["different/path.txt"]),
        )

    def test_p05_corrected_gate_must_bind_new_head(self):
        self.assert_mutation_fails(
            "valid-p05-qa-correction.json", "P05_CORRECTED_GATE",
            lambda value: value["gates"][1].__setitem__("head_sha", "5" * 40),
        )

    def test_p06_requires_owner_gate_type(self):
        def mutate(value):
            value["gates"][0]["gate_type"] = "EVIDENCE_INTEGRITY"
            value["gates"][0]["role"] = "ENGINEERING"
            value["gates"][0]["verdict"] = "PASS"
        self.assert_mutation_fails("valid-p06-owner-gate-approve.json", "P06_GATE_TYPE", mutate)

    def test_invalid_utc_time_fails_closed(self):
        invalid_time = "2026-09-01 06:00:00"
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "AS_OF",
            lambda value: value.__setitem__("as_of", invalid_time), invalid_time,
        )

    def test_boolean_is_not_accepted_as_integer_zero(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "ZERO_TOLERANCE",
            lambda value: value["metrics"].__setitem__("unauthorized_writes", False),
        )

    def test_nested_extra_field_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "ADAPTER_FIELDS",
            lambda value: value["adapter"].__setitem__("extra", False),
        )

    def test_material_handoff_is_required(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "HANDOFF_MATERIAL",
            lambda value: value["handoffs"][0].__setitem__("material_transition", False),
        )

    def test_boolean_zero_cost_value_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "ZERO_COST_TYPE",
            lambda value: value["budget"].__setitem__("network_calls", False),
        )

    def test_gate_verdict_must_match_gate_type(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "GATE_VERDICT",
            lambda value: value["gates"][0].__setitem__("verdict", "REJECT"),
        )

    def test_unsupported_attempt_status_fails_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "ATTEMPT_STATUS",
            lambda value: value["attempts"][0].__setitem__("status", "UNKNOWN"),
        )

    def test_p05_requires_qa_failed_to_completed_statuses(self):
        self.assert_mutation_fails(
            "valid-p05-qa-correction.json", "P05_ATTEMPT_STATUS",
            lambda value: value["attempts"][0].__setitem__("status", "COMPLETED"),
        )

    def test_unexpected_claims_fail_closed(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "UNEXPECTED_CLAIMS",
            lambda value: value.__setitem__("claims", [{"claim_id": "claim-extra", "valid": True, "paths": ["extra.txt"]}]),
        )

    def test_p01_sources_must_be_a_list(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "P01_SOURCES",
            lambda value: value["evidence"].__setitem__("source_refs", "source:not-a-list"),
        )

    def test_p03_gate_must_bind_recovery_head(self):
        self.assert_mutation_fails(
            "valid-p03-simulated-failover.json", "P03_GATE_HEAD",
            lambda value: value["gates"][0].__setitem__("head_sha", "3" * 40),
        )

    def test_duplicate_claim_paths_fail_closed(self):
        self.assert_mutation_fails(
            "valid-p02-engineering-work.json", "P02_PATHS",
            lambda value: value["claims"][0].__setitem__("paths", ["allowed/example.txt", "allowed/example.txt"]),
        )

    def test_non_object_attempt_fails_with_validation_error(self):
        self.assert_mutation_fails(
            "valid-p01-research-handoff.json", "ATTEMPT_FIELDS",
            lambda value: value.__setitem__("attempts", ["not-an-object"]),
        )


class PilotBundleTests(unittest.TestCase):
    def load(self, name):
        return load_json(FIXTURES / name)

    def test_valid_bundle(self):
        result = validate_bundle(self.load("valid-pilot-bundle.json"), FIXTURES, AS_OF)
        self.assertEqual("PASS", result["verdict"])
        self.assertEqual(6, result["required_scenarios_passed"])
        self.assertEqual(2, result["owner_paths_passed"])

    def test_bundle_replay_is_deterministic(self):
        bundle = self.load("valid-pilot-bundle.json")
        first = validate_bundle(copy.deepcopy(bundle), FIXTURES, AS_OF)
        second = validate_bundle(copy.deepcopy(bundle), FIXTURES, AS_OF)
        self.assertEqual(first, second)

    def test_missing_scenario(self):
        with self.assertRaisesRegex(PilotValidationError, "SCENARIO_COVERAGE"):
            validate_bundle(self.load("invalid-missing-scenario.json"), FIXTURES, AS_OF)

    def test_nondeterministic_digest(self):
        with self.assertRaisesRegex(PilotValidationError, "BUNDLE_DIGEST"):
            validate_bundle(self.load("invalid-nondeterministic-replay.json"), FIXTURES, AS_OF)

    def test_unauthorized_write(self):
        record = self.load("invalid-unauthorized-write.json")
        with self.assertRaisesRegex(PilotValidationError, "ZERO_TOLERANCE"):
            validate_scenario(record, AS_OF)

    def test_duplicate_writer(self):
        record = self.load("invalid-duplicate-writer.json")
        with self.assertRaisesRegex(PilotValidationError, "ZERO_TOLERANCE"):
            validate_scenario(record, AS_OF)

    def test_duplicate_output(self):
        record = self.load("invalid-duplicate-output.json")
        with self.assertRaisesRegex(PilotValidationError, "ZERO_TOLERANCE"):
            validate_scenario(record, AS_OF)

    def test_gate_bypass(self):
        record = self.load("invalid-gate-bypass.json")
        with self.assertRaisesRegex(PilotValidationError, "ZERO_TOLERANCE"):
            validate_scenario(record, AS_OF)

    def test_incomplete_handoff_trace(self):
        record = self.load("invalid-incomplete-handoff-trace.json")
        with self.assertRaisesRegex(PilotValidationError, "HANDOFF_COVERAGE"):
            validate_scenario(record, AS_OF)

    def test_provider_or_spend(self):
        record = self.load("invalid-provider-or-spend.json")
        with self.assertRaisesRegex(PilotValidationError, "ZERO_COST"):
            validate_scenario(record, AS_OF)

    def test_duplicate_scenario_filename_fails_closed(self):
        bundle = self.load("valid-pilot-bundle.json")
        bundle["scenario_files"]["P03"] = bundle["scenario_files"]["P02"]
        bundle["expected_digest"] = canonical_digest(bundle)
        with self.assertRaisesRegex(PilotValidationError, "FIXTURE_UNIQUENESS"):
            validate_bundle(bundle, FIXTURES, AS_OF)

    def test_non_string_scenario_filename_fails_closed(self):
        bundle = self.load("valid-pilot-bundle.json")
        bundle["scenario_files"]["P03"] = 3
        bundle["expected_digest"] = canonical_digest(bundle)
        with self.assertRaisesRegex(PilotValidationError, "FIXTURE_PATH"):
            validate_bundle(bundle, FIXTURES, AS_OF)


if __name__ == "__main__":
    unittest.main()
