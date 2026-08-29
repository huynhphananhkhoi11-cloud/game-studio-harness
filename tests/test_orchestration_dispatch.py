import copy
import io
import json
from pathlib import Path
import socket
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from scripts.orchestration_dispatch import (
    DispatchError,
    canonical_digest,
    explain,
    main,
    record_decision,
    validate_decision,
    validate_registry,
)
from scripts.orchestration_queue import snapshot_digest


FIXTURES = Path("platform/orchestration/fixtures/007b")
QUEUE_FIXTURE = Path("platform/orchestration/fixtures/007a/valid-work-order.json")
AS_OF = "2026-08-29T08:00:00Z"


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def valid_work_order():
    work_order = json.loads(QUEUE_FIXTURE.read_text(encoding="utf-8"))
    work_order.update(
        work_order_id="WO-007B-001",
        capability_tags=["engineering.repository"],
        state="CLAIMABLE",
        updated_at="2026-08-29T07:00:00Z",
        last_event_id="EV-007B-003",
    )
    return work_order


def valid_bundle():
    registry = fixture("valid-capability-registry.json")
    work_order = valid_work_order()
    decision = fixture("valid-dispatch-decision.json")
    decision["work_order_digest"] = snapshot_digest(work_order)
    return registry, work_order, decision


def negative_case(name):
    case = fixture(name)
    registry, work_order, decision = valid_bundle()
    for key, value in case.get("mutations", {}).items():
        decision[key] = value
    for dotted, value in case.get("registry_mutations", {}).items():
        executor_id, field = dotted.split(".", 1)
        record = next(item for item in registry["records"]
                      if item["executor_id"] == executor_id)
        record[field] = value
    addition = case.get("registry_addition")
    if addition:
        registry["records"].append(addition)
    return registry, work_order, decision, case.get("as_of", AS_OF), case["expected_error"]


class RegistryValidationTests(unittest.TestCase):
    def test_valid_registry_passes_and_indexes_all_roles(self):
        registry = fixture("valid-capability-registry.json")
        records = validate_registry(registry)
        self.assertEqual(len(records), 6)
        self.assertIn("ENGINEERING-01", records)

    def test_duplicate_executor_fails(self):
        registry = fixture("valid-capability-registry.json")
        registry["records"].append(copy.deepcopy(registry["records"][0]))
        with self.assertRaisesRegex(DispatchError, "duplicate executor_id"):
            validate_registry(registry)

    def test_unknown_capability_vocabulary_fails(self):
        registry = fixture("valid-capability-registry.json")
        registry["records"][0]["capability_tags"] = ["automatic.magic-routing"]
        with self.assertRaisesRegex(DispatchError, "unknown vocabulary"):
            validate_registry(registry)

    def test_nonzero_cost_fails(self):
        registry = fixture("valid-capability-registry.json")
        registry["records"][0]["cost_class"] = "PAID"
        with self.assertRaisesRegex(DispatchError, "ZERO_COST"):
            validate_registry(registry)

    def test_external_candidate_cannot_be_eligible(self):
        registry = fixture("valid-capability-registry.json")
        record = copy.deepcopy(registry["records"][3])
        record.update(executor_id="CANDIDATE-99", source_class="EXTERNAL_CANDIDATE")
        registry["records"].append(record)
        with self.assertRaisesRegex(DispatchError, "external candidate"):
            validate_registry(registry)

    def test_pending_evidence_cannot_be_eligible(self):
        registry = fixture("valid-capability-registry.json")
        registry["records"][0]["trust_level"] = "EVIDENCE_PENDING"
        with self.assertRaisesRegex(DispatchError, "EVIDENCE_PENDING"):
            validate_registry(registry)

    def test_unsafe_evidence_path_and_secret_fail(self):
        for evidence, expected in [
            ("../private.txt", "repository-relative|unsafe"),
            ("ghp_abcdefghijklmnopqrstuvwxyz123456", "credential"),
        ]:
            registry = fixture("valid-capability-registry.json")
            registry["records"][0]["evidence_references"] = [evidence]
            with self.subTest(evidence=evidence), self.assertRaisesRegex(DispatchError, expected):
                validate_registry(registry)


class DecisionValidationTests(unittest.TestCase):
    def test_valid_decision_passes(self):
        registry, work_order, decision = valid_bundle()
        selected = validate_decision(registry, work_order, decision, AS_OF)
        self.assertEqual(selected["executor_id"], "ENGINEERING-01")

    def test_all_declared_negative_fixtures_fail_for_intended_reason(self):
        names = [
            "invalid-unknown-executor.json",
            "invalid-unavailable-executor.json",
            "invalid-capability-mismatch.json",
            "invalid-expired-decision.json",
            "invalid-nonhuman-dispatcher.json",
            "invalid-candidate-status.json",
        ]
        for name in names:
            registry, work_order, decision, as_of, expected = negative_case(name)
            with self.subTest(name=name), self.assertRaisesRegex(DispatchError, expected):
                validate_decision(registry, work_order, decision, as_of)

    def test_digest_id_and_state_mismatch_fail(self):
        cases = [
            ("digest", lambda w, d: d.update(work_order_digest="sha256:" + "0" * 64)),
            ("ID mismatch", lambda w, d: d.update(work_order_id="WO-OTHER-001")),
            ("CLAIMABLE", lambda w, d: w.update(state="READY")),
        ]
        for expected, mutate in cases:
            registry, work_order, decision = valid_bundle()
            mutate(work_order, decision)
            with self.subTest(expected=expected), self.assertRaisesRegex(DispatchError, expected):
                validate_decision(registry, work_order, decision, AS_OF)

    def test_input_and_output_mismatch_fail(self):
        for field, value, expected in [
            ("required_input_types", ["research-notes"], "input-type"),
            ("required_output_types", ["review-package"], "output-type"),
        ]:
            registry, work_order, decision = valid_bundle()
            decision[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(DispatchError, expected):
                validate_decision(registry, work_order, decision, AS_OF)

    def test_unsatisfied_restriction_fails(self):
        registry, work_order, decision = valid_bundle()
        work_order["prohibited_actions"].remove("No network access")
        decision["work_order_digest"] = snapshot_digest(work_order)
        with self.assertRaisesRegex(DispatchError, "unsatisfied restrictions"):
            validate_decision(registry, work_order, decision, AS_OF)

    def test_duplicate_and_selected_alternatives_fail(self):
        registry, work_order, decision = valid_bundle()
        decision["considered_alternatives"].append(
            copy.deepcopy(decision["considered_alternatives"][0]))
        with self.assertRaisesRegex(DispatchError, "duplicate alternative"):
            validate_decision(registry, work_order, decision, AS_OF)
        registry, work_order, decision = valid_bundle()
        decision["considered_alternatives"][0]["executor_id"] = "ENGINEERING-01"
        with self.assertRaisesRegex(DispatchError, "selected executor"):
            validate_decision(registry, work_order, decision, AS_OF)

    def test_expiry_uses_explicit_as_of_boundaries(self):
        registry, work_order, decision = valid_bundle()
        with self.assertRaisesRegex(DispatchError, "precede decided_at"):
            validate_decision(registry, work_order, decision, "2026-08-29T07:04:59Z")
        with self.assertRaisesRegex(DispatchError, "expired"):
            validate_decision(registry, work_order, decision, decision["expires_at"])

    def test_explain_is_deterministic_and_contains_evidence(self):
        registry, work_order, decision = valid_bundle()
        first = explain(registry, work_order, decision, AS_OF)
        second = explain(registry, work_order, decision, AS_OF)
        self.assertEqual(first, second)
        self.assertIn("ENGINEERING-01", first)
        self.assertIn("GAME-DESIGN-01", first)
        self.assertIn("evidence:", first)


class RecordingAndCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def write_inputs(self):
        registry, work_order, decision = valid_bundle()
        paths = {}
        for name, value in [("registry", registry), ("work-order", work_order),
                            ("decision", decision)]:
            path = self.root / f"{name}.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            paths[name] = path
        return registry, work_order, decision, paths

    def test_record_and_exact_replay(self):
        registry, work_order, decision, _ = self.write_inputs()
        decisions = self.root / "recorded"
        self.assertEqual(record_decision(decisions, registry, work_order,
                                         decision, AS_OF), "recorded")
        self.assertEqual(record_decision(decisions, registry, work_order,
                                         decision, AS_OF), "replayed")
        altered = copy.deepcopy(decision)
        altered["reason"] = "Different reason"
        before = (decisions / "decisions" / "DSP-007B-001.json").read_bytes()
        with self.assertRaisesRegex(DispatchError, "different content"):
            record_decision(decisions, registry, work_order, altered, AS_OF)
        self.assertEqual(before, (decisions / "decisions" / "DSP-007B-001.json").read_bytes())

    def test_failed_dispatch_does_not_create_output(self):
        registry, work_order, decision, _ = self.write_inputs()
        decision["dispatcher_role"] = "PRODUCER-01"
        decisions = self.root / "recorded"
        with self.assertRaises(DispatchError):
            record_decision(decisions, registry, work_order, decision, AS_OF)
        self.assertFalse(decisions.exists())

    def test_record_does_not_mutate_queue_inputs(self):
        registry, work_order, decision, paths = self.write_inputs()
        before = {name: path.read_bytes() for name, path in paths.items()}
        record_decision(self.root / "recorded", registry, work_order, decision, AS_OF)
        self.assertEqual(before, {name: path.read_bytes() for name, path in paths.items()})

    def test_cli_validate_explain_dispatch_and_exit_codes(self):
        _, _, _, paths = self.write_inputs()
        common = ["--registry", str(paths["registry"]), "--work-order",
                  str(paths["work-order"]), "--decision", str(paths["decision"]),
                  "--as-of", AS_OF]
        with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()):
            self.assertEqual(main(["validate-registry", "--registry",
                                   str(paths["registry"])]), 0)
            self.assertEqual(main(["validate-decision", *common]), 0)
            self.assertEqual(main(["explain", *common]), 0)
            self.assertIn("ENGINEERING-01", output.getvalue())
            self.assertEqual(main(["dispatch", *common, "--decision-root",
                                   str(self.root / "cli-recorded")]), 0)
        bad = json.loads(paths["decision"].read_text())
        bad["dispatcher_role"] = "PRODUCER-01"
        paths["decision"].write_text(json.dumps(bad))
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(["validate-decision", *common]), 1)

    def test_no_network_calls(self):
        registry, work_order, decision, _ = self.write_inputs()
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            validate_decision(registry, work_order, decision, AS_OF)
            record_decision(self.root / "recorded", registry, work_order, decision, AS_OF)

    def test_canonical_digest_is_order_independent(self):
        self.assertEqual(canonical_digest({"a": 1, "b": 2}),
                         canonical_digest({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
