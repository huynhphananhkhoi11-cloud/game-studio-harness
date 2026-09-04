from __future__ import annotations

import copy
import unittest

from scripts import provider_live_evidence as ev


def reseal(value):
    value = copy.deepcopy(value)
    value["canonical_digest"] = "sha256:" + "0" * 64
    value["canonical_digest"] = ev.canonical_digest(value)
    return value


def valid():
    return reseal({
        "schema_version": "1.0",
        "connected_validation_id": "connected-validation:synthetic-alpha",
        "provider_profile_id": "provider-profile:synthetic-alpha",
        "provider_child_id": "STUDIO-009P-99",
        "provider_model_ref": "model:synthetic-alpha",
        "transport_ref": "transport:synthetic-alpha",
        "credential_profile_ref": "credential-profile:synthetic-alpha",
        "v_contract_ref": "v-contract:synthetic-v99",
        "capability_id": "TEXT_GENERATION",
        "data_classification": "PUBLIC",
        "max_request_bytes": 32768,
        "max_output_bytes": 8192,
        "request_count": 3,
        "concurrency": 1,
        "retry_count": 0,
        "model_identity_verified": True,
        "transport_identity_verified": True,
        "quota_evidence_ref": "quota-evidence:synthetic-alpha",
        "spend_amount": 0,
        "currency": "USD",
        "paid_fallback_allowed": False,
        "kill_switch_evidence_ref": "kill-switch:synthetic-alpha",
        "revocation_evidence_ref": "revoke-evidence:synthetic-alpha",
        "connected_qa_ref": "qa:connected-alpha",
        "connected_review_ref": "review:connected-alpha",
        "owner_disposition_ref": "owner-disposition:synthetic-alpha",
        "validated_at": "2026-09-04T10:00:00Z",
        "as_of": "2026-09-04T10:00:01Z",
    })


def constraints():
    return {
        "provider_profile_id": "provider-profile:synthetic-alpha",
        "provider_child_id": "STUDIO-009P-99",
        "provider_model_ref": "model:synthetic-alpha",
        "transport_ref": "transport:synthetic-alpha",
        "credential_profile_ref": "credential-profile:synthetic-alpha",
        "v_contract_ref": "v-contract:synthetic-v99",
        "allowed_capabilities": ["CODE_ANALYSIS", "TEXT_GENERATION"],
        "max_request_bytes": 32768,
        "max_output_bytes": 8192,
        "max_request_count": 3,
        "max_concurrency": 1,
        "max_retry_count": 0,
        "not_before": "2026-09-04T09:00:00Z",
        "expires_at": "2026-09-04T11:00:00Z",
    }


class EvidenceTests(unittest.TestCase):
    def assertCode(self, code, fn):
        with self.assertRaises(ev.ConnectedEvidenceError) as caught:
            fn()
        self.assertEqual(caught.exception.code, code)
        self.assertNotIn("synthetic-alpha", caught.exception.safe_message)

    def test_01_valid_metadata(self):
        self.assertEqual(ev.validate_connected_validation(valid())["decision"], "METADATA_VALID")

    def test_02_public(self):
        self.assertEqual(ev.validate_connected_validation(valid())["data_classification"], "PUBLIC")

    def test_03_request_limit(self):
        value = valid(); value["request_count"] = 4; value = reseal(value)
        self.assertCode("REQUEST_LIMIT", lambda: ev.validate_connected_validation(value))

    def test_04_concurrency_limit(self):
        value = valid(); value["concurrency"] = 2; value = reseal(value)
        self.assertCode("CONCURRENCY_LIMIT", lambda: ev.validate_connected_validation(value))

    def test_05_retry_limit(self):
        value = valid(); value["retry_count"] = 1; value = reseal(value)
        self.assertCode("RETRY_LIMIT", lambda: ev.validate_connected_validation(value))

    def test_06_nonzero_spend(self):
        value = valid(); value["spend_amount"] = 1; value = reseal(value)
        self.assertCode("NONZERO_SPEND", lambda: ev.validate_connected_validation(value))

    def test_07_paid_fallback(self):
        value = valid(); value["paid_fallback_allowed"] = True; value = reseal(value)
        self.assertCode("PAID_FALLBACK", lambda: ev.validate_connected_validation(value))

    def test_08_model_identity(self):
        value = valid(); value["model_identity_verified"] = False; value = reseal(value)
        self.assertCode("IDENTITY_UNVERIFIED", lambda: ev.validate_connected_validation(value))

    def test_09_transport_identity(self):
        value = valid(); value["transport_identity_verified"] = False; value = reseal(value)
        self.assertCode("IDENTITY_UNVERIFIED", lambda: ev.validate_connected_validation(value))

    def test_10_public_only(self):
        value = valid(); value["data_classification"] = "INTERNAL"; value = reseal(value)
        self.assertCode("PUBLIC_ONLY", lambda: ev.validate_connected_validation(value))

    def test_11_missing_v_contract(self):
        value = valid(); value["v_contract_ref"] = None; value = reseal(value)
        self.assertCode("MISSING_V_CONTRACT", lambda: ev.validate_connected_validation(value))

    def test_12_missing_kill(self):
        value = valid(); value["kill_switch_evidence_ref"] = None; value = reseal(value)
        self.assertCode("MISSING_KILL_REVOKE", lambda: ev.validate_connected_validation(value))

    def test_13_missing_revoke(self):
        value = valid(); value["revocation_evidence_ref"] = None; value = reseal(value)
        self.assertCode("MISSING_KILL_REVOKE", lambda: ev.validate_connected_validation(value))

    def test_14_missing_qa(self):
        value = valid(); value["connected_qa_ref"] = None; value = reseal(value)
        self.assertCode("MISSING_CONNECTED_QA", lambda: ev.validate_connected_validation(value))

    def test_15_missing_review(self):
        value = valid(); value["connected_review_ref"] = None; value = reseal(value)
        self.assertCode("MISSING_CONNECTED_REVIEW", lambda: ev.validate_connected_validation(value))

    def test_16_missing_owner(self):
        value = valid(); value["owner_disposition_ref"] = None; value = reseal(value)
        self.assertCode("MISSING_OWNER_DISPOSITION", lambda: ev.validate_connected_validation(value))

    def test_17_chronology(self):
        value = valid(); value["validated_at"] = "2026-09-04T10:00:02Z"; value = reseal(value)
        self.assertCode("INVALID_TIME", lambda: ev.validate_connected_validation(value))

    def test_18_unknown_field(self):
        value = valid(); value["x"] = 1
        self.assertCode("EXTRA_FIELD", lambda: ev.validate_connected_validation(value))

    def test_19_duplicate_json(self):
        self.assertCode("DUPLICATE_JSON_KEY", lambda: ev.load_json_document('{"schema_version":"1.0","schema_version":"1.0"}'))

    def test_20_nonfinite_json(self):
        self.assertCode("INPUT_NUMBER", lambda: ev.load_json_document('{"x":NaN}'))

    def test_21_secret_like(self):
        value = valid(); value["provider_model_ref"] = "model:sk-ABCDEFGHIJKLMNOPQRSTUV"
        self.assertCode("SECRET_MATERIAL", lambda: ev.validate_connected_validation(value))

    def test_22_input_immutable(self):
        value = valid(); before = copy.deepcopy(value)
        ev.validate_connected_validation(value)
        self.assertEqual(value, before)

    def test_23_metadata_only_is_not_bound_authority(self):
        self.assertEqual(ev.validate_connected_validation(valid())["decision"], "METADATA_VALID")

    def test_24_bound_constraints_accepted(self):
        self.assertEqual(ev.validate_connected_validation(valid(), accepted_constraints=constraints())["decision"], "BOUND_ACCEPTED")

    def test_25_profile_lineage_mismatch(self):
        accepted = constraints(); accepted["provider_profile_id"] = "provider-profile:synthetic-beta"
        self.assertCode("LINEAGE_MISMATCH", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_26_child_lineage_mismatch(self):
        accepted = constraints(); accepted["provider_child_id"] = "STUDIO-009P-98"
        self.assertCode("LINEAGE_MISMATCH", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_27_model_mismatch(self):
        accepted = constraints(); accepted["provider_model_ref"] = "model:synthetic-beta"
        self.assertCode("MODEL_TRANSPORT_MISMATCH", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_28_transport_mismatch(self):
        accepted = constraints(); accepted["transport_ref"] = "transport:synthetic-beta"
        self.assertCode("MODEL_TRANSPORT_MISMATCH", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_29_credential_lineage_mismatch(self):
        accepted = constraints(); accepted["credential_profile_ref"] = "credential-profile:synthetic-beta"
        self.assertCode("CREDENTIAL_LINEAGE_MISMATCH", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_30_v_contract_mismatch(self):
        accepted = constraints(); accepted["v_contract_ref"] = "v-contract:synthetic-v98"
        self.assertCode("V_CONTRACT_MISMATCH", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_31_capability_broadening(self):
        accepted = constraints(); accepted["allowed_capabilities"] = ["CODE_ANALYSIS"]
        self.assertCode("CAPABILITY_BROADENING", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_32_request_output_broadening(self):
        accepted = constraints(); accepted["max_request_bytes"] = 16384
        self.assertCode("REQUEST_OUTPUT_BROADENING", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_33_quota_broadening(self):
        accepted = constraints(); accepted["max_request_count"] = 2
        self.assertCode("QUOTA_BROADENING", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))

    def test_34_time_broadening(self):
        accepted = constraints(); accepted["not_before"] = "2026-09-04T10:00:01Z"
        self.assertCode("TIME_BROADENING", lambda: ev.validate_connected_validation(valid(), accepted_constraints=accepted))
