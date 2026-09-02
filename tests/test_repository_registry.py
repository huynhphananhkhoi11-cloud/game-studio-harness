import copy
import json
import unittest
from pathlib import Path

from scripts import connectivity_boundary as cb
from scripts import repository_registry as rr


ROOT = Path(__file__).resolve().parents[1]
FIX009A = ROOT / "platform" / "connectivity" / "fixtures" / "009a"
FIX009B = ROOT / "platform" / "connectivity" / "fixtures" / "009b"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fixture009a(name):
    return load(FIX009A / name)


def fixture009b(name):
    return load(FIX009B / name)


def reseal(record):
    record["canonical_digest"] = rr.canonical_digest(record)
    return record


def read_evidence():
    return fixture009a("valid-read-only-boundary.json"), fixture009a("valid-threat-assessment.json")


def write_evidence(access="PR_WRITE"):
    boundary = fixture009a("valid-branch-write-boundary.json")
    boundary["repository"]["access_tier"] = access
    boundary["canonical_digest"] = cb.canonical_digest(boundary)
    threat = fixture009a("valid-threat-assessment.json")
    threat["boundary_id"] = boundary["boundary_id"]
    threat["boundary_digest"] = boundary["canonical_digest"]
    threat["canonical_digest"] = cb.canonical_digest(threat)
    return boundary, threat


def make_write_record(access="PR_WRITE"):
    boundary, threat = write_evidence(access)
    record = fixture009b("valid-read-only-repository.json")
    record["access_tier"] = access
    record["allowed_paths"] = copy.deepcopy(boundary["repository"]["allowed_paths"])
    record["denied_paths"] = copy.deepcopy(boundary["repository"]["denied_paths"])
    record["allowed_branch_namespace"] = "agent/"
    record["allowed_classifications"] = copy.deepcopy(boundary["data_policy"]["allowed_classifications"])
    record["instruction_authority_paths"] = copy.deepcopy(boundary["data_policy"]["instruction_authority_paths"])
    record["boundary_digest"] = boundary["canonical_digest"]
    record["threat_assessment_digest"] = threat["canonical_digest"]
    record["status"] = "WRITE_ACTIVE"
    reseal(record)
    return record, boundary, threat


class RepositoryRegistryFixtureTests(unittest.TestCase):
    def assertRecordError(self, name, code):
        boundary, threat = read_evidence()
        with self.assertRaises(rr.RepositoryRegistryError) as caught:
            rr.validate_repository_record(fixture009b(name), boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, code)

    def test_valid_read_only_repository(self):
        boundary, threat = read_evidence()
        result = rr.validate_repository_record(
            fixture009b("valid-read-only-repository.json"),
            boundary=boundary,
            threat_assessment=threat,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["access_tier"], "READ_ONLY")
        self.assertEqual(result["record_status"], "READ_ONLY_ACTIVE")

    def test_valid_disabled_repository_is_structurally_valid(self):
        boundary, threat = read_evidence()
        result = rr.validate_repository_record(
            fixture009b("valid-disabled-repository.json"),
            boundary=boundary,
            threat_assessment=threat,
        )
        self.assertEqual(result["record_status"], "DISABLED")

    def test_disabled_repository_is_not_available(self):
        boundary, threat = read_evidence()
        result = rr.validate_repository_record(
            fixture009b("valid-disabled-repository.json"),
            boundary=boundary,
            threat_assessment=threat,
        )
        self.assertFalse(rr.repository_available(result))

    def test_invalid_embedded_credential_fixture(self):
        self.assertRecordError("invalid-embedded-credential.json", "SECRET_MATERIAL")

    def test_invalid_unapproved_repository_fixture(self):
        self.assertRecordError("invalid-unapproved-repository.json", "OWNER_APPROVAL_REQUIRED")

    def test_invalid_unsafe_github_url_fixture(self):
        self.assertRecordError("invalid-unsafe-github-url.json", "UNSAFE_GITHUB_URL")


class RepositoryRegistryBehaviorTests(unittest.TestCase):
    def record(self):
        return fixture009b("valid-read-only-repository.json")

    def assertError(self, record, code, boundary=None, threat=None):
        if boundary is None or threat is None:
            boundary, threat = read_evidence()
        with self.assertRaises(rr.RepositoryRegistryError) as caught:
            rr.validate_repository_record(record, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, code)

    def test_host_is_pinned_to_github_com(self):
        record = self.record(); record["host"] = "127.0.0.1"; reseal(record)
        self.assertError(record, "UNSAFE_GITHUB_URL")

    def test_unicode_confusable_host_fails(self):
        record = self.record(); record["host"] = "gіthub.com"; reseal(record)
        self.assertError(record, "UNSAFE_GITHUB_URL")

    def test_query_string_url_fails(self):
        record = self.record(); record["canonical_url"] += "?ref=main"; reseal(record)
        self.assertError(record, "UNSAFE_GITHUB_URL")

    def test_fragment_url_fails(self):
        record = self.record(); record["canonical_url"] += "#token"; reseal(record)
        self.assertError(record, "UNSAFE_GITHUB_URL")

    def test_alternate_port_url_fails(self):
        record = self.record()
        record["canonical_url"] = record["canonical_url"].replace("github.com/", "github.com:443/")
        reseal(record)
        self.assertError(record, "UNSAFE_GITHUB_URL")

    def test_extra_field_fails_closed(self):
        record = self.record(); record["admin"] = False; reseal(record)
        self.assertError(record, "EXTRA_FIELD")

    def test_missing_field_fails_closed(self):
        record = self.record(); del record["registry_version_ref"]; reseal(record)
        self.assertError(record, "MISSING_FIELD")

    def test_mutable_registration_revision_fails(self):
        record = self.record(); record["registration_revision"] = "main"; reseal(record)
        self.assertError(record, "MUTABLE_REVISION")

    def test_invalid_access_tier_fails(self):
        record = self.record(); record["access_tier"] = "ADMIN"; reseal(record)
        self.assertError(record, "INVALID_ACCESS_TIER")

    def test_read_only_record_cannot_have_write_namespace(self):
        record = self.record(); record["allowed_branch_namespace"] = "agent/"; reseal(record)
        self.assertError(record, "UNAUTHORIZED_WRITE")

    def test_write_record_requires_namespace(self):
        record, boundary, threat = make_write_record()
        record["allowed_branch_namespace"] = None; reseal(record)
        self.assertError(record, "INVALID_BRANCH_NAMESPACE", boundary, threat)

    def test_write_status_conflicts_with_read_only_access(self):
        record = self.record(); record["status"] = "WRITE_ACTIVE"; reseal(record)
        self.assertError(record, "STATUS_ACCESS_CONFLICT")

    def test_read_only_active_conflicts_with_write_access(self):
        record, boundary, threat = make_write_record()
        record["status"] = "READ_ONLY_ACTIVE"; reseal(record)
        self.assertError(record, "STATUS_ACCESS_CONFLICT", boundary, threat)

    def test_expired_record_fails(self):
        record = self.record(); record["expires_at"] = record["as_of"]; reseal(record)
        self.assertError(record, "EXPIRED_REPOSITORY")

    def test_future_boundary_evidence_fails(self):
        record = self.record()
        record["as_of"] = "2026-09-01T14:04:59Z"
        record["expires_at"] = "2026-12-31T23:59:59Z"
        reseal(record)
        self.assertError(record, "FUTURE_EVIDENCE")

    def test_digest_tamper_fails(self):
        record = self.record(); record["registry_version_ref"] = "registry-version:changed"
        self.assertError(record, "DIGEST_MISMATCH")

    def test_boundary_digest_binding_fails_closed(self):
        record = self.record(); record["boundary_digest"] = "sha256:" + "0" * 64; reseal(record)
        self.assertError(record, "BOUNDARY_LINEAGE")

    def test_threat_digest_binding_fails_closed(self):
        record = self.record(); record["threat_assessment_digest"] = "sha256:" + "0" * 64; reseal(record)
        self.assertError(record, "BOUNDARY_LINEAGE")

    def test_access_cannot_broaden_boundary(self):
        record = self.record(); record["access_tier"] = "PR_WRITE"; record["allowed_branch_namespace"] = "agent/"; record["status"] = "WRITE_ACTIVE"; reseal(record)
        self.assertError(record, "BOUNDARY_LINEAGE")

    def test_paths_cannot_broaden_boundary(self):
        record = self.record(); record["allowed_paths"] = ["AGENTS.md", "platform", "tasks"]; reseal(record)
        self.assertError(record, "BOUNDARY_LINEAGE")

    def test_classification_policy_must_match_boundary(self):
        record = self.record(); record["allowed_classifications"] = ["PUBLIC"]; reseal(record)
        self.assertError(record, "BOUNDARY_LINEAGE")

    def test_authority_policy_must_match_boundary(self):
        record = self.record(); record["instruction_authority_paths"] = ["AGENTS.md"]; reseal(record)
        self.assertError(record, "BOUNDARY_LINEAGE")

    def test_unsorted_allowed_paths_fail(self):
        record = self.record(); record["allowed_paths"] = list(reversed(record["allowed_paths"])); reseal(record)
        self.assertError(record, "NONCANONICAL_ORDER")

    def test_scope_overlap_fails(self):
        record = self.record(); record["denied_paths"] = [".env", ".git", "credentials", "tasks/private"]; reseal(record)
        self.assertError(record, "PATH_SCOPE_OVERLAP")

    def test_canonical_digest_is_key_order_stable(self):
        record = self.record()
        reversed_record = dict(reversed(list(record.items())))
        self.assertEqual(rr.canonical_digest(record), rr.canonical_digest(reversed_record))

    def test_input_is_immutable_on_success(self):
        record = self.record(); before = copy.deepcopy(record); boundary, threat = read_evidence()
        rr.validate_repository_record(record, boundary=boundary, threat_assessment=threat)
        self.assertEqual(record, before)

    def test_input_is_immutable_on_failure(self):
        record = self.record(); record["canonical_url"] += "?x=1"; reseal(record); before = copy.deepcopy(record)
        with self.assertRaises(rr.RepositoryRegistryError):
            rr.validate_repository_record(record, boundary=read_evidence()[0], threat_assessment=read_evidence()[1])
        self.assertEqual(record, before)

    def test_duplicate_registry_identity_fails(self):
        boundary, threat = read_evidence(); record = self.record()
        with self.assertRaises(rr.RepositoryRegistryError) as caught:
            rr.validate_registry([(record, boundary, threat), (copy.deepcopy(record), boundary, threat)])
        self.assertEqual(caught.exception.code, "DUPLICATE_REPOSITORY")

    def test_conflicting_registry_identity_fails(self):
        boundary, threat = read_evidence()
        first = self.record()
        second = fixture009b("valid-disabled-repository.json")
        with self.assertRaises(rr.RepositoryRegistryError) as caught:
            rr.validate_registry([(first, boundary, threat), (second, boundary, threat)])
        self.assertEqual(caught.exception.code, "CONFLICTING_REPOSITORY")

    def test_exact_allowlist_path_is_allowed(self):
        boundary, threat = read_evidence()
        record = rr.validate_repository_record(self.record(), boundary=boundary, threat_assessment=threat)
        self.assertTrue(rr.path_is_allowed("AGENTS.md", record))

    def test_nested_allowlist_path_is_allowed(self):
        boundary, threat = read_evidence()
        record = rr.validate_repository_record(self.record(), boundary=boundary, threat_assessment=threat)
        self.assertTrue(rr.path_is_allowed("tasks/STUDIO-009B.md", record))

    def test_outside_allowlist_path_is_denied(self):
        boundary, threat = read_evidence()
        record = rr.validate_repository_record(self.record(), boundary=boundary, threat_assessment=threat)
        self.assertFalse(rr.path_is_allowed("README.md", record))

    def test_secret_error_does_not_echo_value(self):
        record = self.record(); secret = "Bearer do-not-echo-this-value"; record["unexpected"] = secret
        boundary, threat = read_evidence()
        with self.assertRaises(rr.RepositoryRegistryError) as caught:
            rr.validate_repository_record(record, boundary=boundary, threat_assessment=threat)
        self.assertNotIn(secret, str(caught.exception))

    def test_write_record_validates_against_pr_write_boundary(self):
        record, boundary, threat = make_write_record()
        result = rr.validate_repository_record(record, boundary=boundary, threat_assessment=threat)
        self.assertEqual(result["access_tier"], "PR_WRITE")
        self.assertEqual(result["record_status"], "WRITE_ACTIVE")


if __name__ == "__main__":
    unittest.main()
