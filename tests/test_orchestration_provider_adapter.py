from __future__ import annotations

import ast
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "orchestration_provider_adapter.py"
FIXTURES = ROOT / "platform" / "orchestration" / "fixtures" / "007f"
SCHEMAS = ROOT / "platform" / "orchestration" / "schemas"
AS_OF = "2026-08-31T01:00:00Z"

SPEC = importlib.util.spec_from_file_location("orchestration_provider_adapter", SCRIPT)
adapter = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(adapter)


def load(relative: str):
    return json.loads((FIXTURES / relative).read_text(encoding="utf-8"))


def valid_manual_success():
    return load("manual/valid-success-result.json")


def valid_fake_success():
    return load("fake/valid-success-result.json")


class SchemaTests(unittest.TestCase):
    def test_all_three_schemas_are_valid_json(self):
        for name in ("adapter-request", "adapter-result", "adapter-capability"):
            self.assertIsInstance(json.loads((SCHEMAS / f"{name}.schema.json").read_text()), dict)

    def test_all_three_schemas_fail_closed_on_extra_fields(self):
        for name in ("adapter-request", "adapter-result", "adapter-capability"):
            schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text())
            self.assertFalse(schema["additionalProperties"])

    def test_request_schema_required_fields_match_runtime(self):
        schema = json.loads((SCHEMAS / "adapter-request.schema.json").read_text())
        self.assertEqual(set(schema["required"]), adapter.REQUEST_FIELDS)

    def test_result_schema_required_fields_match_runtime(self):
        schema = json.loads((SCHEMAS / "adapter-result.schema.json").read_text())
        self.assertEqual(set(schema["required"]), adapter.RESULT_FIELDS)

    def test_capability_schema_required_fields_match_runtime(self):
        schema = json.loads((SCHEMAS / "adapter-capability.schema.json").read_text())
        self.assertEqual(set(schema["required"]), adapter.CAPABILITY_FIELDS)

    def test_result_schema_enforces_zero_money(self):
        schema = json.loads((SCHEMAS / "adapter-result.schema.json").read_text())
        money = schema["properties"]["usage_counters"]["properties"]["monetary_minor_units"]
        self.assertEqual(money, {"const": 0})

    def test_capability_schema_allows_only_manual_and_fake(self):
        schema = json.loads((SCHEMAS / "adapter-capability.schema.json").read_text())
        self.assertEqual(set(schema["properties"]["adapter_type"]["enum"]), {"MANUAL", "FAKE"})

    def test_capability_schema_requires_network_false(self):
        schema = json.loads((SCHEMAS / "adapter-capability.schema.json").read_text())
        self.assertEqual(schema["properties"]["network_access"], {"const": False})

    def test_capability_schema_binds_adapter_to_operation(self):
        schema = json.loads((SCHEMAS / "adapter-capability.schema.json").read_text())
        self.assertGreaterEqual(len(schema["allOf"]), 2)

    def test_result_schema_binds_status_to_error_class(self):
        schema = json.loads((SCHEMAS / "adapter-result.schema.json").read_text())
        self.assertGreaterEqual(len(schema["allOf"]), 4)


class FixtureTests(unittest.TestCase):
    def test_valid_request_fixture(self):
        bundle = load("manual/valid-request.json")
        self.assertIs(adapter.validate_bundle(bundle, as_of=AS_OF), bundle)

    def test_valid_manual_success_fixture(self):
        bundle = valid_manual_success()
        self.assertIs(adapter.validate_bundle(bundle, as_of=AS_OF), bundle)

    def test_valid_manual_refusal_fixture(self):
        bundle = load("manual/valid-refusal-result.json")
        self.assertIs(adapter.validate_bundle(bundle, as_of=AS_OF), bundle)

    def test_valid_fake_success_fixture(self):
        bundle = valid_fake_success()
        self.assertIs(adapter.validate_bundle(bundle, as_of=AS_OF), bundle)

    def test_valid_fake_timeout_fixture(self):
        bundle = load("fake/valid-timeout-result.json")
        self.assertIs(adapter.validate_bundle(bundle, as_of=AS_OF), bundle)

    def test_valid_fake_failure_fixture(self):
        bundle = load("fake/valid-failure-result.json")
        self.assertIs(adapter.validate_bundle(bundle, as_of=AS_OF), bundle)

    def test_invalid_undeclared_capability_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-undeclared-capability.json"), as_of=AS_OF)

    def test_invalid_scope_expansion_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-scope-expansion.json"), as_of=AS_OF)

    def test_invalid_mismatched_correlation_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-mismatched-correlation.json"), as_of=AS_OF)

    def test_invalid_provider_field_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-provider-field.json"), as_of=AS_OF)

    def test_invalid_credential_field_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-credential-field.json"), as_of=AS_OF)

    def test_invalid_network_capability_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-network-capability.json"), as_of=AS_OF)

    def test_invalid_malformed_result_fixture(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_bundle(load("invalid-malformed-result.json"), as_of=AS_OF)


class CapabilityTests(unittest.TestCase):
    def setUp(self):
        self.capability = valid_manual_success()["capability"]

    def test_capability_accepts_exact_record(self):
        self.assertIs(adapter.validate_capability(self.capability), self.capability)

    def test_capability_rejects_extra_field(self):
        self.capability["extra"] = False
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_missing_field(self):
        del self.capability["deterministic"]
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_real_adapter(self):
        self.capability["adapter_type"] = "REAL"
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_manual_fake_operation(self):
        self.capability["operation"] = "SIMULATE_SUCCESS"
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_nondeterminism(self):
        self.capability["deterministic"] = False
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_nonzero_cost_class(self):
        self.capability["cost_class"] = "PAID"
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_network(self):
        self.capability["network_access"] = True
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_authority(self):
        self.capability["authority_grants"] = ["MERGE"]
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_rejects_unsorted_kinds(self):
        self.capability["accepted_input_kinds"].reverse()
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)

    def test_capability_requires_result_output_kind(self):
        self.capability["produced_output_kinds"] = ["HANDOFF_REFERENCE"]
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_capability(self.capability)


class RequestTests(unittest.TestCase):
    def setUp(self):
        bundle = valid_manual_success()
        self.request = bundle["request"]
        self.capability = bundle["capability"]

    def validate(self):
        return adapter.validate_request(self.request, self.capability, as_of=AS_OF)

    def test_request_accepts_exact_record(self):
        self.assertIs(self.validate(), self.request)

    def test_request_rejects_extra_provider_field(self):
        self.request["provider"] = "example"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_secret_value(self):
        self.request["input_references"][0] = "evidence://password=very-secret-value"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_undeclared_capability(self):
        self.request["capability_id"] = "capability:other"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_adapter_mismatch(self):
        self.request["adapter_type"] = "FAKE"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_missing_gate(self):
        self.request["gate_evidence_references"].remove("gate://secret-safety")
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_unsafe_reference_scheme(self):
        self.request["input_references"][0] = "https://provider.example/input"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_reference_traversal(self):
        self.request["input_references"][0] = "artifact://repo/../secret"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_duplicate_references(self):
        self.request["input_references"].append(self.request["input_references"][0])
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_unsorted_references(self):
        self.request["input_references"].reverse()
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_attempt_four(self):
        self.request["attempt_number"] = 4
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_future_creation(self):
        self.request["created_at"] = "2026-08-31T02:00:00Z"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_request_rejects_as_of_mismatch(self):
        with self.assertRaises(adapter.AdapterError):
            adapter.validate_request(self.request, self.capability, as_of="2026-08-31T01:00:01Z")

    def test_request_validation_preserves_bytes(self):
        before = adapter.canonical_json(self.request)
        self.validate()
        self.assertEqual(adapter.canonical_json(self.request), before)

    def test_request_rejects_undeclared_artifact_input_kind(self):
        self.capability["accepted_input_kinds"] = ["EVIDENCE_REFERENCE", "WORK_ORDER_REFERENCE"]
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_request_rejects_undeclared_work_order_input_kind(self):
        self.capability["accepted_input_kinds"] = ["ARTIFACT_REFERENCE", "EVIDENCE_REFERENCE"]
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_request_rejects_trace_for_another_correlation(self):
        self.request["trace_reference"] = "trace://correlation/007f-999"
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_request_rejects_budget_for_another_work_order(self):
        self.request["budget_reference"] = "budget://zero-cost/007f-999"
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_request_rejects_provider_labeled_reference(self):
        self.request["input_references"][1] = "evidence://provider/example"
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_request_rejects_noncanonical_timestamp(self):
        self.request["created_at"] = "2026-08-31T00:30:00.000Z"
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_failed_request_validation_preserves_bytes(self):
        self.request["trace_reference"] = "trace://correlation/007f-999"
        before = adapter.canonical_json(self.request)
        with self.assertRaises(adapter.AdapterError): self.validate()
        self.assertEqual(adapter.canonical_json(self.request), before)


class ResultTests(unittest.TestCase):
    def setUp(self):
        bundle = valid_manual_success()
        self.request = bundle["request"]
        self.capability = bundle["capability"]
        self.result = bundle["result"]

    def validate(self):
        return adapter.validate_result(
            self.result, self.request, self.capability, as_of=AS_OF
        )

    def test_result_accepts_exact_record(self):
        self.assertIs(self.validate(), self.result)

    def test_result_rejects_request_identity_mismatch(self):
        self.result["request_id"] = "request:other"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_artifact_mismatch(self):
        self.result["artifact_identity"]["artifact_digest"] = "sha256:" + "b" * 64
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_correlation_mismatch(self):
        self.result["correlation_id"] = "correlation:other"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_success_error(self):
        self.result["error_class"] = "ADAPTER_FAILURE"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_success_without_output(self):
        self.result["output_references"] = []
        self.result["usage_counters"]["output_references"] = 0
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_failure_with_output(self):
        self.result["status"] = "FAILURE"
        self.result["error_class"] = "ADAPTER_FAILURE"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_nonzero_money(self):
        self.result["usage_counters"]["monetary_minor_units"] = 1
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_wrong_input_counter(self):
        self.result["usage_counters"]["input_references"] = 99
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_wrong_output_counter(self):
        self.result["usage_counters"]["output_references"] = 0
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_output_over_budget(self):
        self.result["usage_counters"]["output_bytes"] = 2097153
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_inaccurate_output_byte_counter(self):
        self.result["usage_counters"]["output_bytes"] += 1
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_future_completion(self):
        self.result["completed_at"] = "2026-08-31T01:00:01Z"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_completion_before_request(self):
        self.result["completed_at"] = "2026-08-31T00:00:00Z"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_rejects_unsafe_handoff(self):
        self.result["handoff_reference"] = "https://example.invalid/handoff"
        with self.assertRaises(adapter.AdapterError):
            self.validate()

    def test_result_validation_preserves_bytes(self):
        before = adapter.canonical_json(self.result)
        self.validate()
        self.assertEqual(adapter.canonical_json(self.result), before)

    def test_result_rejects_handoff_without_declared_output_kind(self):
        self.capability["produced_output_kinds"] = ["RESULT_REFERENCE"]
        self.result["handoff_reference"] = "handoff://007f/result"
        with self.assertRaises(adapter.AdapterError): self.validate()

    def test_failed_result_validation_preserves_bytes(self):
        self.result["correlation_id"] = "correlation:other"
        before = adapter.canonical_json(self.result)
        with self.assertRaises(adapter.AdapterError): self.validate()
        self.assertEqual(adapter.canonical_json(self.result), before)


class AdapterBehaviorTests(unittest.TestCase):
    def test_manual_normalization_returns_canonical_copy(self):
        bundle = valid_manual_success()
        normalized = adapter.normalize_manual_result(
            bundle["request"], bundle["capability"], bundle["result"], as_of=AS_OF
        )
        self.assertEqual(normalized, bundle["result"])
        self.assertIsNot(normalized, bundle["result"])

    def test_manual_normalization_rejects_missing_result(self):
        bundle = load("manual/valid-request.json")
        with self.assertRaises(adapter.AdapterError):
            adapter.normalize_manual_result(
                bundle["request"], bundle["capability"], None, as_of=AS_OF
            )

    def test_manual_normalization_rejects_fake_capability(self):
        bundle = valid_fake_success()
        with self.assertRaises(adapter.AdapterError):
            adapter.normalize_manual_result(
                bundle["request"], bundle["capability"], bundle["result"], as_of=AS_OF
            )

    def test_fake_success_is_deterministic(self):
        bundle = valid_fake_success()
        first = adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF)
        second = adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF)
        self.assertEqual(adapter.canonical_json(first), adapter.canonical_json(second))

    def test_fake_success_matches_fixture(self):
        bundle = valid_fake_success()
        self.assertEqual(adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF), bundle["result"])

    def test_fake_timeout_matches_fixture(self):
        bundle = load("fake/valid-timeout-result.json")
        self.assertEqual(adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF), bundle["result"])

    def test_fake_failure_matches_fixture(self):
        bundle = load("fake/valid-failure-result.json")
        self.assertEqual(adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF), bundle["result"])

    def test_fake_refusal_operation_is_deterministic(self):
        bundle = valid_fake_success()
        bundle["capability"]["capability_id"] = "capability:007f:fake-refusal"
        bundle["capability"]["operation"] = "SIMULATE_REFUSAL"
        bundle["request"]["capability_id"] = "capability:007f:fake-refusal"
        first = adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF)
        second = adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF)
        self.assertEqual(first, second)
        self.assertEqual((first["status"], first["error_class"]), ("REFUSED", "REFUSAL"))

    def test_fake_bundle_rejects_outcome_not_declared_by_operation(self):
        bundle = load("fake/valid-failure-result.json")
        bundle["result"]["status"] = "TIMEOUT"
        bundle["result"]["error_class"] = "TIMEOUT"
        with self.assertRaises(adapter.AdapterError): adapter.validate_bundle(bundle, as_of=AS_OF)

    def test_fake_bundle_rejects_tampered_deterministic_result_id(self):
        bundle = valid_fake_success()
        bundle["result"]["result_id"] = "result:tampered"
        with self.assertRaises(adapter.AdapterError): adapter.validate_bundle(bundle, as_of=AS_OF)

    def test_fake_preserves_request_and_capability(self):
        bundle = valid_fake_success()
        before = copy.deepcopy(bundle)
        adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF)
        self.assertEqual(bundle, before)

    def test_fake_rejects_manual_operation(self):
        bundle = valid_manual_success()
        with self.assertRaises(adapter.AdapterError):
            adapter.run_fake(bundle["request"], bundle["capability"], as_of=AS_OF)

    def test_canonical_digest_is_stable_across_key_order(self):
        left = {"b": 2, "a": 1}
        right = {"a": 1, "b": 2}
        self.assertEqual(adapter.canonical_digest(left), adapter.canonical_digest(right))

    def test_runtime_imports_are_standard_and_read_only(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported <= {"__future__", "argparse", "copy", "hashlib", "json", "re", "sys", "datetime", "pathlib", "typing"})
        self.assertTrue(imported.isdisjoint({"socket", "subprocess", "urllib", "requests", "http", "os"}))

    def test_runtime_does_not_read_system_clock(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("datetime.now", source)
        self.assertNotIn("datetime.utcnow", source)
        self.assertNotIn("time.time", source)

    def test_runtime_contains_no_process_or_network_call(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for forbidden in ("subprocess.", "socket.", "urlopen(", "requests.", "os.system("):
            self.assertNotIn(forbidden, source)


class JsonBoundaryTests(unittest.TestCase):
    def write_json_text(self, text: str, *, name: str = "input.json") -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_loader_rejects_duplicate_json_keys(self):
        path = self.write_json_text('{"schema_version":"1.0","schema_version":"1.0"}')
        with self.assertRaises(adapter.AdapterError): adapter.load_json(path)

    def test_loader_rejects_hidden_json_file(self):
        path = self.write_json_text('{}', name=".secret.json")
        with self.assertRaises(adapter.AdapterError): adapter.load_json(path)

    def test_forbidden_scan_rejects_compound_provider_key(self):
        with self.assertRaises(adapter.AdapterError): adapter._scan_forbidden({"provider_name": "example"})

    def test_digest_cli_rejects_secret_bearing_json(self):
        path = self.write_json_text('{"api_key":"not-allowed"}')
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = adapter.main(["digest", "--input", str(path)])
        self.assertEqual((code, stdout.getvalue()), (1, ""))
        self.assertIn("ERROR:", stderr.getvalue())


class CliTests(unittest.TestCase):
    def call(self, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = adapter.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_cli_validates_bundle(self):
        path = FIXTURES / "manual" / "valid-success-result.json"
        code, output, error = self.call(["validate-bundle", "--input", str(path), "--as-of", AS_OF])
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(json.loads(output)["schema_version"], "1.0")

    def test_cli_rejects_invalid_bundle(self):
        path = FIXTURES / "invalid-network-capability.json"
        code, output, error = self.call(["validate-bundle", "--input", str(path), "--as-of", AS_OF])
        self.assertEqual((code, output), (1, ""))
        self.assertIn("ERROR:", error)

    def test_cli_runs_fake(self):
        path = FIXTURES / "fake" / "valid-success-result.json"
        code, output, error = self.call(["run-fake", "--input", str(path), "--as-of", AS_OF])
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(json.loads(output)["status"], "SUCCESS")

    def test_cli_normalizes_manual(self):
        path = FIXTURES / "manual" / "valid-refusal-result.json"
        code, output, error = self.call(["normalize-manual", "--input", str(path), "--as-of", AS_OF])
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(json.loads(output)["status"], "REFUSED")

    def test_cli_digest_is_canonical(self):
        path = FIXTURES / "manual" / "valid-request.json"
        code, output, error = self.call(["digest", "--input", str(path)])
        self.assertEqual((code, error), (0, ""))
        self.assertRegex(json.loads(output)["digest"], r"^sha256:[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
