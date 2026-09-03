from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from scripts import credential_broker as broker


FIXTURE_DIR = Path("platform/connectivity/fixtures/009c")
REPO_DIGEST = "sha256:0fc4c5aa3ef31ea04278a23f258f8479314a471494df1e8bb021c38d4e8d7e95"
PRIOR_FIXTURE_DIR = Path("platform/connectivity/fixtures")


def repository_evidence():
    repository_record = json.loads(
        (PRIOR_FIXTURE_DIR / "009b/valid-read-only-repository.json").read_text(encoding="utf-8")
    )
    repository_record["as_of"] = "2026-09-03T06:30:00Z"
    repository_record["canonical_digest"] = broker.canonical_digest(repository_record)
    if repository_record["canonical_digest"] != REPO_DIGEST:
        raise AssertionError("derived repository fixture digest drifted")
    return {
        "repository_record": repository_record,
        "boundary": json.loads(
            (PRIOR_FIXTURE_DIR / "009a/valid-read-only-boundary.json").read_text(encoding="utf-8")
        ),
        "threat_assessment": json.loads(
            (PRIOR_FIXTURE_DIR / "009a/valid-threat-assessment.json").read_text(encoding="utf-8")
        ),
    }


def fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def redigest(value):
    value["canonical_digest"] = broker.canonical_digest(value)
    return value


def valid_profile():
    return fixture("valid-repository-profile.json")


def valid_request():
    return fixture("valid-lease-request.json")


def normalized_profile(profile=None):
    return broker.validate_credential_profile(profile or valid_profile(), **repository_evidence())


def valid_operation_envelope(request=None):
    req = request or valid_request()
    capability = req["capability"]
    operation = capability[len("GITHUB_"):] if capability.startswith("GITHUB_") else "READ_METADATA"
    write = operation in {"CREATE_BRANCH", "CREATE_OR_UPDATE_FILE", "OPEN_PULL_REQUEST"}
    target_ref = "agent/studio-009c-test" if write else None
    control = {
        "task_ref": "task:STUDIO-009C",
        "attempt_ref": "attempt:009c-credential",
        "queue_ref": "queue:studio-009a",
        "dispatch_ref": "dispatch:studio-009a",
        "writer_claim_ref": "writer-claim:studio-009a" if write else None,
        "worktree_ref": "worktree:studio-009a" if write else None,
        "gate_ref": "gate:studio-009a",
        "trace_ref": "trace:studio-009a",
        "quota_budget_ref": "quota-budget:studio-009a",
        "boundary_ref": "boundary:studio-009a-read",
        "threat_assessment_ref": "threat-assessment:studio-009a",
        "owner_approval_ref": "owner-approval:studio-009b",
    }
    value = {
        "schema_version": "1.0",
        "repository_id": "repository:game-studio-harness",
        "repository_record_digest": REPO_DIGEST,
        "operation": operation,
        "base_revision": "14802ce03e1d8ac6f5fdbcb6b354b59103a244cb",
        "target_ref": target_ref,
        "target_paths": [],
        "data_classification": "INTERNAL",
        "instruction_authority_path": None,
        "control_evidence": control,
        "limits": {
            "max_payload_bytes": 0,
            "max_files": 1,
            "page": 1,
            "per_page": 1,
            "timeout_ms": 1000,
            "max_response_bytes": 1024,
        },
        "idempotency_key": "idem:credential009c",
        "replay": {
            "issued_at": "2026-09-03T06:29:00Z",
            "expires_at": "2026-09-03T07:00:00Z",
            "prior_result_digest": None,
        },
        "as_of": "2026-09-03T06:30:00Z",
        "canonical_digest": "",
    }
    value["canonical_digest"] = broker.gc.canonical_digest(value)
    return value


def lease_plan(profile, request):
    if profile["subject_type"] == "REPOSITORY":
        evidence = repository_evidence()
        return broker.plan_credential_lease(
            profile,
            request,
            repository_record=evidence["repository_record"],
            operation_envelope=valid_operation_envelope(request),
            boundary=evidence["boundary"],
            threat_assessment=evidence["threat_assessment"],
        )
    return broker.plan_credential_lease(profile, request)


class CredentialProfileTests(unittest.TestCase):
    def test_valid_repository_profile(self):
        result = normalized_profile()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["subject_type"], "REPOSITORY")

    def test_valid_disabled_profile_metadata(self):
        result = broker.validate_credential_profile(
            fixture("valid-disabled-profile.json"),
            **repository_evidence(),
        )
        self.assertEqual(result["profile_status"], "DISABLED")

    def test_invalid_embedded_secret_field(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(
                fixture("invalid-embedded-secret.json"),
                **repository_evidence(),
            )
        self.assertEqual(ctx.exception.code, "SECRET_MATERIAL")

    def test_subject_mismatch(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(
                fixture("invalid-subject-mismatch.json"),
                **repository_evidence(),
            )
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_expired_profile(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(
                fixture("invalid-expired-profile.json"),
                **repository_evidence(),
            )
        self.assertEqual(ctx.exception.code, "EXPIRED_PROFILE")

    def test_revoked_profile_metadata_is_valid(self):
        result = broker.validate_credential_profile(
            fixture("invalid-revoked-profile.json"),
            **repository_evidence(),
        )
        self.assertEqual(result["profile_status"], "REVOKED")

    def test_missing_owner_evidence(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(
                fixture("invalid-missing-owner-evidence.json"),
                **repository_evidence(),
            )
        self.assertEqual(ctx.exception.code, "MISSING_FIELD")

    def test_missing_repository_binding_argument(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(valid_profile())
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_repository_digest_mismatch(self):
        evidence = repository_evidence()
        evidence["repository_record"]["canonical_digest"] = "sha256:" + "f" * 64
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(valid_profile(), **evidence)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_repository_auth_profile_mismatch(self):
        evidence = repository_evidence()
        evidence["repository_record"]["auth_profile_ref"] = "auth-profile:other"
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(valid_profile(), **evidence)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_digest_mismatch(self):
        profile = valid_profile()
        profile["trace_ref"] = "trace:changed"
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "DIGEST_MISMATCH")

    def test_digest_format(self):
        profile = valid_profile()
        profile["canonical_digest"] = "bad"
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "DIGEST_FORMAT")

    def test_extra_field(self):
        profile = valid_profile()
        profile["metadata"] = "x"
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "EXTRA_FIELD")

    def test_subject_credential_class_mismatch(self):
        profile = valid_profile()
        profile["credential_class"] = "PROVIDER_AUTH"
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_invalid_status(self):
        profile = valid_profile()
        profile["status"] = "PAUSED"
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "INVALID_ENUM")

    def test_invalid_max_lease_bool(self):
        profile = valid_profile()
        profile["max_lease_seconds"] = True
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "LEASE_LIMIT")

    def test_invalid_max_lease_too_long(self):
        profile = valid_profile()
        profile["max_lease_seconds"] = 3601
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "LEASE_LIMIT")

    def test_future_profile_not_before(self):
        profile = valid_profile()
        profile["not_before"] = "2026-10-01T00:00:00Z"
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "FUTURE_EVIDENCE")

    def test_rotation_after_expiry_invalid(self):
        profile = valid_profile()
        profile["rotation_deadline"] = "2027-01-01T00:00:00Z"
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "INVALID_TIME")

    def test_unsorted_capabilities_rejected(self):
        profile = valid_profile()
        profile["allowed_capabilities"] = list(reversed(profile["allowed_capabilities"]))
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "INVALID_FORMAT")

    def test_duplicate_capabilities_rejected(self):
        profile = valid_profile()
        profile["allowed_capabilities"] = ["GITHUB_READ_METADATA", "GITHUB_READ_METADATA"]
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(ctx.exception.code, "INVALID_FORMAT")

    def test_profile_input_immutable(self):
        profile = valid_profile()
        before = copy.deepcopy(profile)
        broker.validate_credential_profile(profile, **repository_evidence())
        self.assertEqual(profile, before)

    def test_service_profile_requires_null_repository_digest(self):
        profile = valid_profile()
        profile["credential_profile_id"] = "credential-profile:service-one"
        profile["subject_type"] = "SERVICE"
        profile["subject_ref"] = "service:internal"
        profile["credential_class"] = "SERVICE_AUTH"
        profile["repository_record_digest"] = None
        profile["auth_profile_ref"] = "auth-profile:service"
        redigest(profile)
        result = broker.validate_credential_profile(profile)
        self.assertEqual(result["subject_type"], "SERVICE")

    def test_nonrepository_with_repository_digest_rejected(self):
        profile = valid_profile()
        profile["credential_profile_id"] = "credential-profile:service-two"
        profile["subject_type"] = "SERVICE"
        profile["subject_ref"] = "service:internal"
        profile["credential_class"] = "SERVICE_AUTH"
        profile["auth_profile_ref"] = "auth-profile:service"
        redigest(profile)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")


class JsonAndStructuralTests(unittest.TestCase):
    def test_load_valid_json(self):
        value = broker.load_json_document(json.dumps(valid_profile()))
        self.assertEqual(value["schema_version"], "1.0")

    def test_duplicate_json_key(self):
        text = '{"schema_version":"1.0","schema_version":"1.0"}'
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.load_json_document(text)
        self.assertEqual(ctx.exception.code, "DUPLICATE_JSON_KEY")

    def test_top_level_array_rejected(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.load_json_document("[]")
        self.assertEqual(ctx.exception.code, "INVALID_TYPE")

    def test_nan_rejected(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.load_json_document('{"x":NaN}')
        self.assertEqual(ctx.exception.code, "INPUT_NUMBER")

    def test_secret_value_pattern_rejected(self):
        profile = valid_profile()
        profile["trace_ref"] = "https://user:syntheticpass@example.invalid/x"
        redigest(profile)
        # Reference format catches this safely; public failure still contains no input.
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertNotIn("syntheticpass", ctx.exception.safe_message)

    def test_nonfinite_float_rejected(self):
        profile = valid_profile()
        profile["max_lease_seconds"] = float("inf")
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.validate_credential_profile(profile, **repository_evidence())
        self.assertIn(ctx.exception.code, {"INPUT_ENCODING", "INPUT_NUMBER"})

    def test_deep_structure_rejected(self):
        value = {"x": 1}
        for _ in range(broker.cb.MAX_STRUCTURE_DEPTH + 2):
            value = {"x": value}
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker._preflight(value)
        self.assertEqual(ctx.exception.code, "STRUCTURE_LIMIT")


class LeasePlanningTests(unittest.TestCase):
    def test_repository_request_requires_operation_envelope_evidence(self):
        evidence = repository_evidence()
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.plan_credential_lease(
                normalized_profile(),
                valid_request(),
                repository_record=evidence["repository_record"],
                operation_envelope=None,
                boundary=evidence["boundary"],
                threat_assessment=evidence["threat_assessment"],
            )
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_operation_digest_must_match_revalidated_operation(self):
        request = valid_request()
        request["operation_digest"] = "sha256:" + "e" * 64
        redigest(request)
        evidence = repository_evidence()
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.plan_credential_lease(
                normalized_profile(),
                request,
                repository_record=evidence["repository_record"],
                operation_envelope=valid_operation_envelope(),
                boundary=evidence["boundary"],
                threat_assessment=evidence["threat_assessment"],
            )
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_capability_must_match_revalidated_operation(self):
        request = valid_request()
        request["capability"] = "GITHUB_READ_TREE"
        redigest(request)
        evidence = repository_evidence()
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.plan_credential_lease(
                normalized_profile(),
                request,
                repository_record=evidence["repository_record"],
                operation_envelope=valid_operation_envelope(),
                boundary=evidence["boundary"],
                threat_assessment=evidence["threat_assessment"],
            )
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_stale_operation_time_rejected(self):
        request = valid_request()
        evidence = repository_evidence()
        operation = valid_operation_envelope(request)
        operation["as_of"] = "2026-09-03T06:29:00Z"
        operation["replay"]["issued_at"] = "2026-09-03T06:28:00Z"
        operation["canonical_digest"] = broker.gc.canonical_digest(operation)
        request["operation_digest"] = operation["canonical_digest"]
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.plan_credential_lease(
                normalized_profile(), request,
                repository_record=evidence["repository_record"],
                operation_envelope=operation,
                boundary=evidence["boundary"],
                threat_assessment=evidence["threat_assessment"],
            )
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_operation_queue_lineage_mismatch_rejected(self):
        request = valid_request()
        request["queue_ref"] = "queue:other"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_operation_attempt_lineage_mismatch_rejected(self):
        request = valid_request()
        request["attempt_ref"] = "attempt:other"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_profile_gate_lineage_mismatch_rejected(self):
        request = valid_request()
        request["gate_ref"] = "gate:other"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_request_cannot_precede_profile_as_of(self):
        request = valid_request()
        request["as_of"] = "2026-09-03T06:29:00Z"
        request["replay"]["issued_at"] = "2026-09-03T06:28:00Z"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "FUTURE_EVIDENCE")

    def test_valid_lease_plan(self):
        plan = lease_plan(normalized_profile(), valid_request())
        self.assertEqual(plan.capability, "GITHUB_READ_METADATA")
        self.assertEqual(plan.expires_at, "2026-09-03T06:35:00Z")

    def test_valid_lease_normalization_has_no_locator(self):
        result = broker.normalize_lease(
            lease_plan(normalized_profile(), valid_request())
        )
        self.assertNotIn("secret_locator_ref", result)
        self.assertNotIn("secret_store_ref", result)

    def test_lease_digest_is_canonical(self):
        result = broker.normalize_lease(
            lease_plan(normalized_profile(), valid_request())
        )
        self.assertEqual(result["canonical_digest"], broker.canonical_digest(result))

    def test_scope_broadening_fixture(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(
                normalized_profile(), fixture("invalid-scope-broadening.json")
            )
        self.assertEqual(ctx.exception.code, "SCOPE_BROADENING")

    def test_replay_fixture(self):
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(
                normalized_profile(), fixture("invalid-replay-request.json")
            )
        self.assertEqual(ctx.exception.code, "REPLAY")

    def test_disabled_profile_cannot_issue(self):
        profile = broker.validate_credential_profile(
            fixture("valid-disabled-profile.json"),
            **repository_evidence(),
        )
        request = valid_request()
        request["credential_profile_id"] = profile["credential_profile_id"]
        request["profile_digest"] = profile["profile_digest"]
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "PROFILE_NOT_ACTIVE")

    def test_revoked_profile_cannot_issue(self):
        profile = broker.validate_credential_profile(
            fixture("invalid-revoked-profile.json"),
            **repository_evidence(),
        )
        request = valid_request()
        request["profile_digest"] = profile["profile_digest"]
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "REVOKED_PROFILE")

    def test_rotation_required_status_cannot_issue(self):
        raw = valid_profile()
        raw["status"] = "ROTATION_REQUIRED"
        redigest(raw)
        profile = broker.validate_credential_profile(raw, **repository_evidence())
        request = valid_request()
        request["profile_digest"] = profile["profile_digest"]
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "ROTATION_REQUIRED")

    def test_rotation_deadline_cannot_be_crossed(self):
        raw = valid_profile()
        raw["rotation_deadline"] = "2026-09-03T06:32:00Z"
        redigest(raw)
        profile = broker.validate_credential_profile(raw, **repository_evidence())
        request = valid_request()
        request["profile_digest"] = profile["profile_digest"]
        request["requested_lease_seconds"] = 180
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "LEASE_LIMIT")

    def test_profile_lease_maximum(self):
        raw = valid_profile()
        raw["max_lease_seconds"] = 60
        redigest(raw)
        profile = broker.validate_credential_profile(raw, **repository_evidence())
        request = valid_request()
        request["profile_digest"] = profile["profile_digest"]
        request["requested_lease_seconds"] = 61
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "LEASE_LIMIT")

    def test_global_lease_maximum(self):
        request = valid_request()
        request["requested_lease_seconds"] = 3601
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LEASE_LIMIT")

    def test_bool_lease_duration_rejected(self):
        request = valid_request()
        request["requested_lease_seconds"] = True
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LEASE_LIMIT")

    def test_nonzero_budget_rejected(self):
        request = valid_request()
        request["money_ceiling"] = 1
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "NONZERO_BUDGET")

    def test_bool_budget_rejected(self):
        request = valid_request()
        request["money_ceiling"] = True
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "NONZERO_BUDGET")

    def test_subject_mismatch_request(self):
        request = valid_request()
        request["subject_ref"] = "repository:other"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_profile_digest_mismatch_request(self):
        request = valid_request()
        request["profile_digest"] = "sha256:" + "e" * 64
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_repository_digest_mismatch_request(self):
        request = valid_request()
        request["repository_record_digest"] = "sha256:" + "e" * 64
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_owner_approval_mismatch(self):
        request = valid_request()
        request["owner_approval_ref"] = "owner-approval:other"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "OWNER_APPROVAL_REQUIRED")

    def test_request_digest_mismatch(self):
        request = valid_request()
        request["purpose"] = "REPOSITORY_READ"
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(normalized_profile(), request)
        self.assertEqual(ctx.exception.code, "DIGEST_MISMATCH")

    def test_request_input_immutable(self):
        request = valid_request()
        before = copy.deepcopy(request)
        lease_plan(normalized_profile(), request)
        self.assertEqual(request, before)

    def test_write_requires_writer_claim_and_worktree(self):
        raw = valid_profile()
        raw["allowed_capabilities"] = [
            "GITHUB_CREATE_BRANCH",
            "GITHUB_READ_BLOB",
            "GITHUB_READ_METADATA",
            "GITHUB_READ_TREE",
        ]
        redigest(raw)
        profile = broker.validate_credential_profile(raw, **repository_evidence())
        request = valid_request()
        request["profile_digest"] = profile["profile_digest"]
        request["capability"] = "GITHUB_CREATE_BRANCH"
        request["writer_claim_ref"] = None
        request["worktree_ref"] = None
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "WRITE_EVIDENCE_REQUIRED")

    def test_write_with_writer_claim_and_worktree(self):
        raw = valid_profile()
        raw["allowed_capabilities"] = [
            "GITHUB_CREATE_BRANCH",
            "GITHUB_READ_BLOB",
            "GITHUB_READ_METADATA",
            "GITHUB_READ_TREE",
        ]
        redigest(raw)
        profile = broker.validate_credential_profile(raw, **repository_evidence())
        request = valid_request()
        request["profile_digest"] = profile["profile_digest"]
        request["capability"] = "GITHUB_CREATE_BRANCH"
        request["writer_claim_ref"] = "writer-claim:009c"
        request["worktree_ref"] = "worktree:009c"
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_provider_profile_cannot_issue(self):
        raw = valid_profile()
        raw["credential_profile_id"] = "credential-profile:provider-meta"
        raw["auth_profile_ref"] = "auth-profile:provider-meta"
        raw["subject_type"] = "PROVIDER"
        raw["subject_ref"] = "provider-profile:future"
        raw["credential_class"] = "PROVIDER_AUTH"
        raw["repository_record_digest"] = None
        redigest(raw)
        profile = broker.validate_credential_profile(raw)
        request = valid_request()
        request["credential_profile_id"] = profile["credential_profile_id"]
        request["profile_digest"] = profile["profile_digest"]
        request["subject_ref"] = profile["subject_ref"]
        request["repository_record_digest"] = None
        request["operation_digest"] = None
        redigest(request)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            lease_plan(profile, request)
        self.assertEqual(ctx.exception.code, "PROVIDER_NOT_AUTHORIZED")


class FakeBrokerTests(unittest.TestCase):
    def setUp(self):
        self.profile = normalized_profile()
        self.request = valid_request()
        self.plan = lease_plan(self.profile, self.request)
        self.store = broker.FakeSecretStore({"secret-locator:fixture-001": {"synthetic": "value"}})
        self.fake = broker.FakeCredentialBroker(self.store)

    def test_issue_accesses_fake_store_once(self):
        result = self.fake.issue(self.plan)
        self.assertTrue(result["credential_lease_id"].startswith("credential-lease:"))
        self.assertEqual(self.fake.store_access_count, 1)

    def test_same_replay_returns_same_result_without_second_store_access(self):
        first = self.fake.issue(self.plan)
        second = self.fake.issue(self.plan)
        self.assertEqual(first, second)
        self.assertEqual(self.fake.store_access_count, 1)

    def test_replay_result_is_copy(self):
        first = self.fake.issue(self.plan)
        first["purpose"] = "MUTATED"
        second = self.fake.issue(self.plan)
        self.assertNotEqual(second["purpose"], "MUTATED")

    def test_conflicting_idempotency_rejected(self):
        self.fake.issue(self.plan)
        changed = valid_request()
        changed["purpose"] = "REPOSITORY_READ"
        redigest(changed)
        other_plan = lease_plan(self.profile, changed)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            self.fake.issue(other_plan)
        self.assertEqual(ctx.exception.code, "IDEMPOTENCY_CONFLICT")
        self.assertEqual(self.fake.store_access_count, 1)

    def test_missing_fake_store_entry(self):
        fake = broker.FakeCredentialBroker(broker.FakeSecretStore({}))
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            fake.issue(self.plan)
        self.assertEqual(ctx.exception.code, "STORE_UNAVAILABLE")

    def test_disable_blocks_issue(self):
        self.fake.disable(self.profile["credential_profile_id"])
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            self.fake.issue(self.plan)
        self.assertEqual(ctx.exception.code, "PROFILE_NOT_ACTIVE")

    def test_rotation_required_blocks_issue(self):
        self.fake.require_rotation(self.profile["credential_profile_id"])
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            self.fake.issue(self.plan)
        self.assertEqual(ctx.exception.code, "ROTATION_REQUIRED")

    def test_revoke_blocks_issue(self):
        self.fake.revoke(self.profile["credential_profile_id"])
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            self.fake.issue(self.plan)
        self.assertEqual(ctx.exception.code, "REVOKED_PROFILE")

    def test_revoked_cannot_reactivate(self):
        self.fake.revoke(self.profile["credential_profile_id"])
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            self.fake.enable_eligible(
                self.profile["credential_profile_id"],
                "owner-approval:fresh",
                self.profile["owner_approval_ref"],
            )
        self.assertEqual(ctx.exception.code, "LIFECYCLE_CONFLICT")

    def test_disabled_can_enable_with_fresh_reference(self):
        pid = self.profile["credential_profile_id"]
        self.fake.disable(pid)
        self.fake.enable_eligible(
            pid, "owner-approval:fresh", self.profile["owner_approval_ref"]
        )
        result = self.fake.issue(self.plan)
        self.assertTrue(result["credential_lease_id"])

    def test_same_owner_evidence_cannot_reactivate_disabled_profile(self):
        pid = self.profile["credential_profile_id"]
        self.fake.disable(pid)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            self.fake.enable_eligible(
                pid,
                self.profile["owner_approval_ref"],
                self.profile["owner_approval_ref"],
            )
        self.assertEqual(ctx.exception.code, "OWNER_APPROVAL_REQUIRED")

    def test_expire_lease_after_expiry(self):
        result = self.fake.issue(self.plan)
        self.assertTrue(
            self.fake.expire_lease(
                result["credential_lease_id"], "2026-09-03T06:35:00Z"
            )
        )

    def test_expire_lease_before_expiry_returns_false(self):
        result = self.fake.issue(self.plan)
        self.assertFalse(
            self.fake.expire_lease(
                result["credential_lease_id"], "2026-09-03T06:34:59Z"
            )
        )

    def test_expire_unknown_lease_returns_false(self):
        self.assertFalse(
            self.fake.expire_lease(
                "credential-lease:" + "a" * 32, "2026-09-03T06:40:00Z"
            )
        )


class EventTests(unittest.TestCase):
    def event(self, action="DISABLE", lease_id=None):
        profile = normalized_profile()
        value = {
            "schema_version": "1.0",
            "credential_event_id": "credential-event:event-001",
            "credential_profile_id": profile["credential_profile_id"],
            "profile_digest": profile["profile_digest"],
            "credential_lease_id": lease_id,
            "action": action,
            "owner_approval_ref": profile["owner_approval_ref"],
            "control_ref": "control:studio-009c",
            "as_of": "2026-09-03T06:31:00Z",
            "canonical_digest": "",
        }
        redigest(value)
        return profile, value

    def test_valid_disable_event(self):
        profile, event = self.event()
        result = broker.normalize_credential_event(profile, event)
        self.assertEqual(result["action"], "DISABLE")

    def test_valid_lease_issued_event(self):
        profile, event = self.event(
            "LEASE_ISSUED", "credential-lease:" + "a" * 32
        )
        result = broker.normalize_credential_event(profile, event)
        self.assertEqual(result["action"], "LEASE_ISSUED")

    def test_revoked_profile_enable_event_rejected(self):
        raw = valid_profile()
        raw["status"] = "REVOKED"
        redigest(raw)
        profile = broker.validate_credential_profile(raw, **repository_evidence())
        event = {
            "schema_version": "1.0",
            "credential_event_id": "credential-event:enable-revoked",
            "credential_profile_id": profile["credential_profile_id"],
            "profile_digest": profile["profile_digest"],
            "credential_lease_id": None,
            "action": "ENABLE_ELIGIBLE",
            "owner_approval_ref": profile["owner_approval_ref"],
            "control_ref": "control:studio-009c",
            "as_of": "2026-09-03T06:31:00Z",
            "canonical_digest": "",
        }
        redigest(event)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.normalize_credential_event(profile, event)
        self.assertEqual(ctx.exception.code, "LIFECYCLE_CONFLICT")

    def test_lease_event_requires_lease_id(self):
        profile, event = self.event("LEASE_ISSUED", None)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.normalize_credential_event(profile, event)
        self.assertEqual(ctx.exception.code, "LIFECYCLE_CONFLICT")

    def test_unknown_action_rejected(self):
        profile, event = self.event()
        event["action"] = "DELETE_SECRET"
        redigest(event)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.normalize_credential_event(profile, event)
        self.assertEqual(ctx.exception.code, "INVALID_ENUM")

    def test_event_profile_mismatch(self):
        profile, event = self.event()
        event["credential_profile_id"] = "credential-profile:other"
        redigest(event)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.normalize_credential_event(profile, event)
        self.assertEqual(ctx.exception.code, "LINEAGE_MISMATCH")

    def test_event_owner_mismatch(self):
        profile, event = self.event()
        event["owner_approval_ref"] = "owner-approval:other"
        redigest(event)
        with self.assertRaises(broker.CredentialBrokerError) as ctx:
            broker.normalize_credential_event(profile, event)
        self.assertEqual(ctx.exception.code, "OWNER_APPROVAL_REQUIRED")

    def test_event_input_immutable(self):
        profile, event = self.event()
        before = copy.deepcopy(event)
        broker.normalize_credential_event(profile, event)
        self.assertEqual(event, before)


class SourceBoundaryTests(unittest.TestCase):
    def test_broker_source_has_no_live_runtime_imports(self):
        source = Path("scripts/credential_broker.py").read_text(encoding="utf-8")
        forbidden = [
            "import socket",
            "import requests",
            "urllib.request",
            "import subprocess",
            "import keyring",
            "os.environ",
            "load_dotenv",
            "github.",
            "boto3",
            "hvac",
            "azure.keyvault",
        ]
        for token in forbidden:
            self.assertNotIn(token, source)

    def test_redaction_source_has_no_live_runtime_imports(self):
        source = Path("scripts/credential_redaction.py").read_text(encoding="utf-8")
        for token in ("import socket", "import requests", "import subprocess", "os.environ"):
            self.assertNotIn(token, source)

    def test_broker_has_no_system_clock_calls(self):
        source = Path("scripts/credential_broker.py").read_text(encoding="utf-8")
        for token in ("datetime.now(", "datetime.utcnow(", "time.time(", "date.today("):
            self.assertNotIn(token, source)

    def test_fixture_directory_has_no_private_key_block(self):
        for path in FIXTURE_DIR.glob("*.json"):
            self.assertNotIn("BEGIN PRIVATE KEY", path.read_text(encoding="utf-8"))

    def test_normalized_lease_contains_no_secret_metadata_refs(self):
        result = broker.normalize_lease(
            lease_plan(normalized_profile(), valid_request())
        )
        serialized = json.dumps(result, sort_keys=True)
        self.assertNotIn("secret-locator", serialized)
        self.assertNotIn("secret-store", serialized)


if __name__ == "__main__":
    unittest.main()
