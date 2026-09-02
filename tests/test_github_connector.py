import copy
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from scripts import connectivity_boundary as cb
from scripts import github_connector as gc
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


def reseal(value):
    value["canonical_digest"] = gc.canonical_digest(value)
    return value


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
    record["canonical_digest"] = rr.canonical_digest(record)
    return record, boundary, threat


def make_read_operation():
    record = fixture009b("valid-read-only-repository.json")
    boundary, threat = read_evidence()
    operation = {
        "schema_version": "1.0",
        "repository_id": record["repository_id"],
        "repository_record_digest": record["canonical_digest"],
        "operation": "READ_BLOB",
        "base_revision": record["registration_revision"],
        "target_ref": None,
        "target_paths": ["AGENTS.md"],
        "data_classification": "INTERNAL",
        "instruction_authority_path": "AGENTS.md",
        "control_evidence": {
            "task_ref": "task:STUDIO-009B",
            "attempt_ref": "attempt:studio-009b-read-001",
            "queue_ref": boundary["control_evidence"]["queue_ref"],
            "dispatch_ref": boundary["control_evidence"]["dispatch_ref"],
            "writer_claim_ref": None,
            "worktree_ref": None,
            "gate_ref": boundary["control_evidence"]["gate_ref"],
            "trace_ref": boundary["control_evidence"]["trace_ref"],
            "quota_budget_ref": boundary["control_evidence"]["quota_budget_ref"],
            "boundary_ref": boundary["boundary_id"],
            "threat_assessment_ref": threat["assessment_id"],
            "owner_approval_ref": record["owner_approval_ref"],
        },
        "limits": {
            "max_payload_bytes": 0,
            "max_files": 10,
            "page": 1,
            "per_page": 50,
            "timeout_ms": 5000,
            "max_response_bytes": 524288,
        },
        "idempotency_key": "idem:studio-009b-read-001",
        "replay": {
            "issued_at": "2026-09-01T14:04:00Z",
            "expires_at": "2026-09-01T14:06:00Z",
            "prior_result_digest": None,
        },
        "as_of": record["as_of"],
    }
    reseal(operation)
    return record, operation, boundary, threat


def make_write_operation():
    record, boundary, threat = make_write_record()
    operation = fixture009b("valid-pr-write-operation.json")
    return record, operation, boundary, threat


def make_result(plan, *, mutation=None):
    resulting = plan.base_revision if plan.operation in gc.READ_OPERATIONS or plan.operation in {"CREATE_BRANCH", "OPEN_PULL_REQUEST"} else "f" * 40
    result = {
        "schema_version": "1.0",
        "repository_id": plan.repository_id,
        "repository_record_digest": plan.repository_record_digest,
        "operation": plan.operation,
        "request_digest": plan.request_digest,
        "idempotency_key": plan.idempotency_key,
        "base_revision": plan.base_revision,
        "resulting_revision": resulting,
        "target_ref": plan.target_ref,
        "paths": list(plan.target_paths),
        "status": "OK",
        "response_bytes": 128,
        "as_of": plan.as_of,
    }
    if mutation is not None:
        mutation(result)
    reseal(result)
    return result


class RecordingFakeTransport:
    def __init__(self, mutation=None):
        self.calls = []
        self.mutation = mutation

    def execute(self, plan):
        self.calls.append(plan)
        return make_result(plan, mutation=self.mutation)


class BadTypeTransport:
    def execute(self, plan):
        return "not-an-object"


class ConnectorFixtureTests(unittest.TestCase):
    def assertOperationFixtureError(self, name, code):
        record, _, boundary, threat = make_write_operation()
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, fixture009b(name), boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, code)

    def test_valid_pr_write_operation_fixture(self):
        record, operation, boundary, threat = make_write_operation()
        plan = gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(plan.operation, "CREATE_OR_UPDATE_FILE")

    def test_invalid_default_branch_write_fixture(self):
        self.assertOperationFixtureError("invalid-default-branch-write.json", "DEFAULT_BRANCH_WRITE")

    def test_invalid_path_escape_fixture(self):
        self.assertOperationFixtureError("invalid-path-escape.json", "UNSAFE_PATH")

    def test_invalid_mutable_revision_fixture(self):
        self.assertOperationFixtureError("invalid-mutable-revision.json", "MUTABLE_REVISION")

    def test_invalid_missing_owner_evidence_fixture(self):
        self.assertOperationFixtureError("invalid-missing-owner-evidence.json", "MISSING_CONTROL_EVIDENCE")


class ConnectorPlanningTests(unittest.TestCase):
    def test_transport_plan_is_frozen(self):
        record, operation, boundary, threat = make_write_operation()
        plan = gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        with self.assertRaises(FrozenInstanceError):
            plan.operation = "READ_METADATA"

    def test_disabled_repository_is_rejected_before_transport(self):
        record = fixture009b("valid-disabled-repository.json")
        _, operation, boundary, threat = make_read_operation()
        operation["repository_record_digest"] = record["canonical_digest"]; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "REPOSITORY_DISABLED")

    def test_read_only_repository_rejects_write(self):
        record, operation, boundary, threat = make_read_operation()
        operation["operation"] = "CREATE_BRANCH"
        operation["target_paths"] = []
        operation["target_ref"] = "agent/test"
        reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "UNAUTHORIZED_WRITE")

    def test_read_blob_plan_is_valid(self):
        record, operation, boundary, threat = make_read_operation()
        plan = gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(plan.target_paths, ("AGENTS.md",))

    def test_nested_allowlist_path_is_valid(self):
        record, operation, boundary, threat = make_read_operation()
        operation["target_paths"] = ["tasks/STUDIO-009B.md"]; reseal(operation)
        plan = gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(plan.target_paths, ("tasks/STUDIO-009B.md",))

    def test_outside_allowlist_path_is_denied(self):
        record, operation, boundary, threat = make_read_operation()
        operation["target_paths"] = ["README.md"]; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "PATH_SCOPE_DENIED")

    def test_protected_branch_is_denied(self):
        record, operation, boundary, threat = make_write_operation()
        operation["target_ref"] = "production"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "DEFAULT_BRANCH_WRITE")

    def test_branch_outside_namespace_is_denied(self):
        record, operation, boundary, threat = make_write_operation()
        operation["target_ref"] = "feature/outside"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "BRANCH_SCOPE_DENIED")

    def test_missing_target_ref_is_denied_for_write(self):
        record, operation, boundary, threat = make_write_operation()
        operation["target_ref"] = None; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "MISSING_TARGET_REF")

    def test_write_requires_writer_claim(self):
        record, operation, boundary, threat = make_write_operation()
        operation["control_evidence"]["writer_claim_ref"] = None; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "MISSING_CONTROL_EVIDENCE")

    def test_read_rejects_writer_claim(self):
        record, operation, boundary, threat = make_read_operation()
        operation["control_evidence"]["writer_claim_ref"] = "writer-claim:unexpected"
        operation["control_evidence"]["worktree_ref"] = "worktree:unexpected"
        reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "UNAUTHORIZED_WRITE")

    def test_open_pull_request_requires_pr_write(self):
        record, boundary, threat = make_write_record("BRANCH_WRITE")
        operation = fixture009b("valid-pr-write-operation.json")
        operation["repository_record_digest"] = record["canonical_digest"]
        operation["operation"] = "OPEN_PULL_REQUEST"
        operation["target_paths"] = []
        operation["control_evidence"]["boundary_ref"] = boundary["boundary_id"]
        operation["control_evidence"]["threat_assessment_ref"] = threat["assessment_id"]
        reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "UNAUTHORIZED_WRITE")

    def test_open_pull_request_valid_with_pr_write(self):
        record, operation, boundary, threat = make_write_operation()
        operation["operation"] = "OPEN_PULL_REQUEST"; operation["target_paths"] = []; reseal(operation)
        plan = gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(plan.operation, "OPEN_PULL_REQUEST")

    def test_unsupported_operation_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["operation"] = "MERGE_PULL_REQUEST"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "UNSUPPORTED_OPERATION")

    def test_extra_field_fails_closed(self):
        record, operation, boundary, threat = make_write_operation()
        operation["merge"] = False; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "EXTRA_FIELD")

    def test_repository_identity_mismatch_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["repository_id"] = "repository:other"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "REPOSITORY_MISMATCH")

    def test_repository_digest_mismatch_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["repository_record_digest"] = "sha256:" + "0" * 64; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "REGISTRY_LINEAGE")

    def test_revision_mismatch_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["base_revision"] = "0" * 40; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "REVISION_MISMATCH")

    def test_classification_outside_policy_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["data_classification"] = "RESTRICTED"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "DATA_POLICY")

    def test_unapproved_instruction_authority_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["instruction_authority_path"] = "scripts/repository_registry.py"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "AUTHORITY_SCOPE")

    def test_boolean_limit_is_not_integer(self):
        record, operation, boundary, threat = make_write_operation()
        operation["limits"]["max_files"] = True; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "INVALID_LIMIT")

    def test_oversized_limit_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["limits"]["timeout_ms"] = 30001; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "LIMIT_EXCEEDED")

    def test_file_count_limit_is_enforced(self):
        record, operation, boundary, threat = make_write_operation()
        operation["limits"]["max_files"] = 0; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "LIMIT_EXCEEDED")

    def test_stale_replay_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["replay"]["expires_at"] = operation["as_of"]; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "STALE_IDEMPOTENCY")

    def test_future_replay_evidence_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["replay"]["issued_at"] = "2026-09-01T14:05:01Z"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "FUTURE_EVIDENCE")

    def test_replay_window_is_bounded(self):
        record, operation, boundary, threat = make_write_operation()
        operation["replay"]["issued_at"] = "2026-08-31T14:04:00Z"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "REPLAY_WINDOW")

    def test_invalid_idempotency_key_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["idempotency_key"] = "short"; reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "INVALID_IDEMPOTENCY_KEY")

    def test_operation_as_of_must_match_registry(self):
        record, operation, boundary, threat = make_write_operation()
        operation["as_of"] = "2026-09-01T14:05:01Z"
        operation["replay"]["expires_at"] = "2026-09-01T14:06:01Z"
        reseal(operation)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "CHRONOLOGY_MISMATCH")

    def test_operation_digest_tamper_fails(self):
        record, operation, boundary, threat = make_write_operation()
        operation["target_ref"] = "agent/tampered"
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "DIGEST_MISMATCH")

    def test_operation_input_is_immutable(self):
        record, operation, boundary, threat = make_write_operation()
        before_record = copy.deepcopy(record); before_operation = copy.deepcopy(operation)
        gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(record, before_record)
        self.assertEqual(operation, before_operation)


class ConnectorExecutionTests(unittest.TestCase):
    def plan(self, read=False):
        if read:
            record, operation, boundary, threat = make_read_operation()
        else:
            record, operation, boundary, threat = make_write_operation()
        plan = gc.plan_operation(record, operation, boundary=boundary, threat_assessment=threat)
        return record, operation, boundary, threat, plan

    def test_fake_transport_result_is_accepted(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport()
        connector = gc.DisabledGitHubConnector(fake)
        result = connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(result["status"], "OK")
        self.assertEqual(len(fake.calls), 1)

    def test_duplicate_request_returns_prior_result_without_transport(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport()
        connector = gc.DisabledGitHubConnector(fake)
        first = connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        second = connector.execute(record, copy.deepcopy(operation), boundary=boundary, threat_assessment=threat)
        self.assertEqual(first, second)
        self.assertEqual(len(fake.calls), 1)

    def test_idempotency_conflict_does_not_repeat_transport(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport()
        connector = gc.DisabledGitHubConnector(fake)
        connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        changed = copy.deepcopy(operation)
        changed["target_paths"] = ["platform/connectivity/GITHUB_CONNECTOR.md"]
        reseal(changed)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, changed, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "IDEMPOTENCY_CONFLICT")
        self.assertEqual(len(fake.calls), 1)

    def test_response_repository_mismatch_fails(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport(lambda result: result.__setitem__("repository_id", "repository:other"))
        connector = gc.DisabledGitHubConnector(fake)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "RESPONSE_MISMATCH")

    def test_response_operation_mismatch_fails(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport(lambda result: result.__setitem__("operation", "READ_METADATA"))
        connector = gc.DisabledGitHubConnector(fake)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "RESPONSE_MISMATCH")

    def test_response_path_mismatch_fails(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport(lambda result: result.__setitem__("paths", []))
        connector = gc.DisabledGitHubConnector(fake)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "RESPONSE_MISMATCH")

    def test_mutable_result_revision_fails(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport(lambda result: result.__setitem__("resulting_revision", "main"))
        connector = gc.DisabledGitHubConnector(fake)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "MUTABLE_REVISION")

    def test_read_result_revision_mismatch_fails(self):
        record, operation, boundary, threat, _ = self.plan(read=True)
        fake = RecordingFakeTransport(lambda result: result.__setitem__("resulting_revision", "f" * 40))
        connector = gc.DisabledGitHubConnector(fake)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "RESPONSE_MISMATCH")

    def test_response_size_bound_is_enforced(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport(lambda result: result.__setitem__("response_bytes", 600000))
        connector = gc.DisabledGitHubConnector(fake)
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "RESPONSE_SIZE")

    def test_result_digest_tamper_fails(self):
        _, _, _, _, plan = self.plan()
        result = make_result(plan)
        result["status"] = "OK"
        result["canonical_digest"] = "sha256:" + "0" * 64
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.normalize_result(plan, result)
        self.assertEqual(caught.exception.code, "DIGEST_MISMATCH")

    def test_non_object_transport_result_fails(self):
        record, operation, boundary, threat, _ = self.plan()
        connector = gc.DisabledGitHubConnector(BadTypeTransport())
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        self.assertEqual(caught.exception.code, "TRANSPORT_RESULT_TYPE")

    def test_result_input_is_immutable(self):
        _, _, _, _, plan = self.plan()
        result = make_result(plan); before = copy.deepcopy(result)
        gc.normalize_result(plan, result)
        self.assertEqual(result, before)

    def test_returned_duplicate_result_is_a_copy(self):
        record, operation, boundary, threat, _ = self.plan()
        fake = RecordingFakeTransport()
        connector = gc.DisabledGitHubConnector(fake)
        first = connector.execute(record, operation, boundary=boundary, threat_assessment=threat)
        first["status"] = "MUTATED-BY-CALLER"
        second = connector.execute(record, copy.deepcopy(operation), boundary=boundary, threat_assessment=threat)
        self.assertEqual(second["status"], "OK")

    def test_transport_is_required(self):
        with self.assertRaises(gc.ConnectorValidationError) as caught:
            gc.DisabledGitHubConnector(None)
        self.assertEqual(caught.exception.code, "TRANSPORT_REQUIRED")


class NoExternalActivityTests(unittest.TestCase):
    def test_connector_source_has_no_live_transport_dependencies(self):
        source = (ROOT / "scripts" / "github_connector.py").read_text(encoding="utf-8")
        forbidden = [
            "import socket", "import subprocess", "import urllib", "from urllib",
            "import requests", "import httpx", "import keyring", "from github",
            "import github", "import git", "from git", "os.environ",
            "datetime.now", "time.time", "gh api", "graphql",
        ]
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source.lower() if token == "graphql" else source)

    def test_registry_source_has_no_external_activity_dependencies(self):
        source = (ROOT / "scripts" / "repository_registry.py").read_text(encoding="utf-8")
        forbidden = [
            "import socket", "import subprocess", "import urllib", "from urllib",
            "import requests", "import httpx", "import keyring", "from github",
            "import github", "import git", "from git", "os.environ",
            "datetime.now", "time.time",
        ]
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_connector_has_no_live_transport_factory(self):
        self.assertFalse(hasattr(gc, "LiveGitHubTransport"))
        self.assertFalse(hasattr(gc, "GitHubHttpTransport"))

    def test_fixture_bytes_unchanged_by_planning(self):
        path = FIX009B / "valid-pr-write-operation.json"
        before = path.read_bytes()
        record, _, boundary, threat = make_write_operation()
        gc.plan_operation(record, json.loads(before), boundary=boundary, threat_assessment=threat)
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
