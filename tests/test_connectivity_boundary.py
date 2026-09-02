import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts import connectivity_boundary as cb


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "platform" / "connectivity" / "fixtures" / "009a"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def reseal(record):
    record["canonical_digest"] = cb.canonical_digest(record)
    return record


class BoundaryFixtureTests(unittest.TestCase):
    def assertBoundaryError(self, name, code):
        with self.assertRaises(cb.BoundaryValidationError) as caught:
            cb.validate_boundary(load(name))
        self.assertEqual(caught.exception.code, code)

    def test_valid_read_only_boundary(self):
        result = cb.validate_boundary(load("valid-read-only-boundary.json"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["access_tier"], "READ_ONLY")

    def test_valid_branch_write_boundary(self):
        result = cb.validate_boundary(load("valid-branch-write-boundary.json"))
        self.assertEqual(result["access_tier"], "BRANCH_WRITE")

    def test_valid_threat_assessment(self):
        result = cb.validate_threat_assessment(load("valid-threat-assessment.json"))
        self.assertEqual(result["threat_count"], 9)

    def test_valid_pair(self):
        result = cb.validate_pair(load("valid-read-only-boundary.json"), load("valid-threat-assessment.json"))
        self.assertEqual(result["status"], "PASS")

    def test_invalid_prompt_injection_fixture(self):
        self.assertBoundaryError("invalid-prompt-injection.json", "PROMPT_INJECTION")

    def test_invalid_secret_field_fixture(self):
        self.assertBoundaryError("invalid-secret-field.json", "SECRET_MATERIAL")

    def test_invalid_path_traversal_fixture(self):
        self.assertBoundaryError("invalid-path-traversal.json", "UNSAFE_PATH")

    def test_invalid_default_branch_write_fixture(self):
        self.assertBoundaryError("invalid-default-branch-write.json", "UNAUTHORIZED_WRITE")

    def test_invalid_provider_identity_fixture(self):
        self.assertBoundaryError("invalid-provider-identity.json", "PROVIDER_IDENTITY")

    def test_invalid_nonzero_budget_fixture(self):
        self.assertBoundaryError("invalid-nonzero-budget.json", "NONZERO_BUDGET")

    def test_invalid_missing_control_fixture(self):
        self.assertBoundaryError("invalid-missing-control-evidence.json", "MISSING_CONTROL_EVIDENCE")

    def test_invalid_extra_field_fixture(self):
        self.assertBoundaryError("invalid-extra-field.json", "EXTRA_FIELD")

    def test_invalid_missing_threat_fixture(self):
        with self.assertRaises(cb.BoundaryValidationError) as caught:
            cb.validate_threat_assessment(load("invalid-missing-threat.json"))
        self.assertEqual(caught.exception.code, "THREAT_SET")


class BoundaryBehaviorTests(unittest.TestCase):
    def boundary(self):
        return load("valid-read-only-boundary.json")

    def threat(self):
        return load("valid-threat-assessment.json")

    def assertBoundaryCode(self, value, code):
        with self.assertRaises(cb.BoundaryValidationError) as caught:
            cb.validate_boundary(value)
        self.assertEqual(caught.exception.code, code)

    def test_canonical_digest_is_stable_across_key_order(self):
        record = self.boundary()
        reversed_record = dict(reversed(list(record.items())))
        self.assertEqual(cb.canonical_digest(record), cb.canonical_digest(reversed_record))

    def test_digest_tampering_fails_closed(self):
        record = self.boundary(); record["task_id"] = "STUDIO-009B"
        self.assertBoundaryCode(record, "DIGEST_MISMATCH")

    def test_nested_extra_field_fails_closed(self):
        record = self.boundary(); record["repository"]["admin"] = False; reseal(record)
        self.assertBoundaryCode(record, "EXTRA_FIELD")

    def test_bool_is_not_zero_budget(self):
        record = self.boundary(); record["money_ceiling"] = False; reseal(record)
        self.assertBoundaryCode(record, "NONZERO_BUDGET")

    def test_unsorted_paths_fail_closed(self):
        record = self.boundary(); record["repository"]["allowed_paths"] = list(reversed(record["repository"]["allowed_paths"])); reseal(record)
        self.assertBoundaryCode(record, "NONCANONICAL_ORDER")

    def test_denied_overlap_fails_closed(self):
        record = self.boundary(); record["repository"]["denied_paths"] = [".env", ".git", "credentials", "tasks/private"]; reseal(record)
        self.assertBoundaryCode(record, "PATH_SCOPE_OVERLAP")

    def test_backslash_path_fails_closed(self):
        record = self.boundary(); record["repository"]["allowed_paths"] = ["AGENTS.md", "platform\\connectivity", "tasks"]; reseal(record)
        self.assertBoundaryCode(record, "UNSAFE_PATH")

    def test_sensitive_allowed_root_fails_closed(self):
        record = self.boundary(); record["repository"]["allowed_paths"] = [".env", "AGENTS.md", "tasks"]; reseal(record)
        self.assertBoundaryCode(record, "UNSAFE_PATH")

    def test_instruction_authority_must_be_allowed(self):
        record = self.boundary(); record["data_policy"]["instruction_authority_paths"] = ["README.md"]; reseal(record)
        self.assertBoundaryCode(record, "AUTHORITY_SCOPE")

    def test_classification_must_be_allowed_by_policy(self):
        record = self.boundary(); record["provider_request"]["data_classification"] = "RESTRICTED"; reseal(record)
        self.assertBoundaryCode(record, "DATA_POLICY")

    def test_content_defaults_to_untrusted(self):
        record = self.boundary(); record["data_policy"]["untrusted_content_default"] = False; reseal(record)
        self.assertBoundaryCode(record, "PROMPT_INJECTION")

    def test_read_only_rejects_writer_claim(self):
        record = self.boundary(); record["control_evidence"]["writer_claim_ref"] = "writer-claim:unexpected"; reseal(record)
        self.assertBoundaryCode(record, "UNAUTHORIZED_WRITE")

    def test_write_requires_worktree_and_writer_claim(self):
        record = load("valid-branch-write-boundary.json"); record["control_evidence"]["worktree_ref"] = None; reseal(record)
        self.assertBoundaryCode(record, "MISSING_CONTROL_EVIDENCE")

    def test_future_boundary_evidence_fails_closed(self):
        record = self.boundary(); record["created_at"] = "2026-09-01T14:06:00Z"; reseal(record)
        self.assertBoundaryCode(record, "FUTURE_EVIDENCE")

    def test_invalid_calendar_time_fails_closed(self):
        record = self.boundary(); record["created_at"] = "2026-02-30T14:00:00Z"; reseal(record)
        self.assertBoundaryCode(record, "INVALID_TIME")

    def test_boundary_input_is_immutable_on_success(self):
        record = self.boundary(); before = copy.deepcopy(record); cb.validate_boundary(record)
        self.assertEqual(record, before)

    def test_boundary_input_is_immutable_on_failure(self):
        record = self.boundary(); record["money_ceiling"] = 1; before = copy.deepcopy(record)
        with self.assertRaises(cb.BoundaryValidationError): cb.validate_boundary(record)
        self.assertEqual(record, before)

    def test_threats_must_be_canonically_sorted(self):
        record = self.threat(); record["threats"] = list(reversed(record["threats"])); reseal(record)
        with self.assertRaises(cb.BoundaryValidationError) as caught: cb.validate_threat_assessment(record)
        self.assertEqual(caught.exception.code, "NONCANONICAL_ORDER")

    def test_duplicate_threat_fails_closed(self):
        record = self.threat(); record["threats"][-1] = copy.deepcopy(record["threats"][0]); record["threats"] = sorted(record["threats"], key=lambda item: item["threat_id"]); reseal(record)
        with self.assertRaises(cb.BoundaryValidationError) as caught: cb.validate_threat_assessment(record)
        self.assertEqual(caught.exception.code, "THREAT_SET")

    def test_evidence_free_mitigation_fails_closed(self):
        record = self.threat(); record["threats"][0]["evidence_refs"] = []; reseal(record)
        with self.assertRaises(cb.BoundaryValidationError) as caught: cb.validate_threat_assessment(record)
        self.assertEqual(caught.exception.code, "INVALID_LIST")

    def test_assessment_lineage_must_match_boundary(self):
        record = self.threat(); record["boundary_digest"] = "sha256:" + "0" * 64; reseal(record)
        with self.assertRaises(cb.BoundaryValidationError) as caught: cb.validate_threat_assessment(record, boundary=self.boundary())
        self.assertEqual(caught.exception.code, "BOUNDARY_LINEAGE")

    def test_threat_input_is_immutable(self):
        record = self.threat(); before = copy.deepcopy(record); cb.validate_threat_assessment(record)
        self.assertEqual(record, before)

    def test_secret_value_is_not_echoed(self):
        record = self.boundary(); secret = "Bearer do-not-echo-this-value"; record["provider_request"]["capability_id"] = secret
        with self.assertRaises(cb.BoundaryValidationError) as caught: cb.validate_boundary(record)
        self.assertNotIn(secret, str(caught.exception))

    def test_source_has_no_clock_subprocess_git_or_network_use(self):
        source = (ROOT / "scripts" / "connectivity_boundary.py").read_text(encoding="utf-8")
        for token in ["datetime.now", "time.time", "subprocess", "import socket", "urllib", "requests", "git "]:
            self.assertNotIn(token, source)

    def test_fixture_bytes_are_unchanged_by_validation(self):
        path = FIXTURES / "valid-read-only-boundary.json"; before = path.read_bytes(); cb.validate_boundary(json.loads(before))
        self.assertEqual(path.read_bytes(), before)


class BoundaryCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "connectivity_boundary.py"), *map(str, args)], cwd=ROOT, text=True, capture_output=True, check=False)

    def test_cli_pair_passes(self):
        result = self.run_cli("validate-pair", FIXTURES / "valid-read-only-boundary.json", FIXTURES / "valid-threat-assessment.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")

    def test_cli_failure_is_stable_and_safe(self):
        result = self.run_cli("validate-boundary", FIXTURES / "invalid-secret-field.json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error_code"], "SECRET_MATERIAL")
        self.assertNotIn("redacted-value", result.stdout)


if __name__ == "__main__":
    unittest.main()
