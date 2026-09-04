from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts import provider_live_gate as lg


ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "platform" / "connectivity" / "live" / "fixtures" / "009r"


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def reseal(value):
    value = copy.deepcopy(value)
    value["canonical_digest"] = "sha256:" + "0" * 64
    value["canonical_digest"] = lg.canonical_digest(value)
    return value


def shadow_policy(profile="provider-profile:synthetic-alpha", child="STUDIO-009P-99"):
    return reseal({
        "schema_version": "1.0",
        "worker_policy_id": "worker-policy:synthetic-shadow",
        "provider_profile_id": profile,
        "provider_child_id": child,
        "mode": "LIVE_SHADOW_WORKER",
        "work_order_ref": None,
        "writer_claim_ref": None,
        "worktree_ref": None,
        "allowed_paths": [],
        "repository_write_allowed": False,
        "direct_main_write_allowed": False,
        "merge_allowed": False,
        "deploy_allowed": False,
        "publish_allowed": False,
        "secret_access_allowed": False,
        "arbitrary_tools_allowed": False,
        "local_mediation_required": True,
        "money_ceiling": 0,
        "as_of": "2026-09-04T10:00:00Z",
    })


def bounded_policy(profile="provider-profile:synthetic-alpha", child="STUDIO-009P-99"):
    return reseal({
        "schema_version": "1.0",
        "worker_policy_id": "worker-policy:synthetic-bounded",
        "provider_profile_id": profile,
        "provider_child_id": child,
        "mode": "LIVE_BOUNDED_WORKER",
        "work_order_ref": "work-order:synthetic-1",
        "writer_claim_ref": "writer-claim:synthetic-1",
        "worktree_ref": "worktree:synthetic-1",
        "allowed_paths": ["Assets/_Game/Gameplay/**"],
        "repository_write_allowed": True,
        "direct_main_write_allowed": False,
        "merge_allowed": False,
        "deploy_allowed": False,
        "publish_allowed": False,
        "secret_access_allowed": False,
        "arbitrary_tools_allowed": False,
        "local_mediation_required": True,
        "money_ceiling": 0,
        "as_of": "2026-09-04T10:00:00Z",
    })


def disabled_state():
    value = load("valid-live-validation-ready.json")
    value["state"] = "DISABLED"
    value["offline_merge_ref"] = None
    value["offline_qa_ref"] = None
    value["offline_review_ref"] = None
    value["offline_owner_merge_ref"] = None
    value["v_contract_ref"] = None
    value["connected_validation_ref"] = None
    value["routing_authority_ref"] = None
    return lg.validate_live_state(reseal(value))


def ready_state():
    return lg.validate_live_state(load("valid-live-validation-ready.json"))


def validated_state():
    return lg.validate_live_state(load("valid-live-validated.json"))


def shadow_state():
    return lg.validate_live_state(load("valid-shadow-worker.json"))


def bounded_state():
    value = load("valid-shadow-worker.json")
    value["state"] = "LIVE_BOUNDED_WORKER"
    return lg.validate_live_state(reseal(value))


def routing_state():
    value = load("invalid-routing-before-009e.json")
    value["routing_authority_ref"] = "routing-authority:studio-009e-synthetic"
    return lg.validate_live_state(reseal(value))


def bound_connected_evidence(profile="provider-profile:synthetic-alpha", child="STUDIO-009P-99"):
    return {
        "decision": "BOUND_ACCEPTED",
        "provider_profile_id": profile,
        "provider_child_id": child,
        "v_contract_ref": "v-contract:synthetic-v99",
    }


class LiveGateTests(unittest.TestCase):
    def assertCode(self, code, fn):
        with self.assertRaises(lg.LiveGateError) as caught:
            fn()
        self.assertEqual(caught.exception.code, code)
        self.assertNotIn("synthetic-alpha", caught.exception.safe_message)

    def test_01_ready_valid(self):
        self.assertEqual(ready_state()["state"], "LIVE_VALIDATION_READY")

    def test_02_validated_valid(self):
        self.assertEqual(validated_state()["state"], "LIVE_VALIDATED")

    def test_03_shadow_valid(self):
        self.assertEqual(shadow_state()["state"], "LIVE_SHADOW_WORKER")

    def test_04_unmerged_rejected(self):
        self.assertCode("OFFLINE_CHILD_NOT_MERGED", lambda: lg.validate_live_state(load("invalid-unmerged-offline.json")))

    def test_05_private_scope_rejected(self):
        self.assertCode(
            "DATA_CLASS_BROADENING",
            lambda: lg.validate_live_state(load("invalid-private-data.json"), parent_allowed_data_classifications=["PUBLIC"]),
        )

    def test_06_nonzero_budget_rejected(self):
        self.assertCode("NONZERO_BUDGET", lambda: lg.validate_live_state(load("invalid-nonzero-budget.json")))

    def test_07_routing_before_009e(self):
        self.assertCode("ROUTING_BEFORE_009E", lambda: lg.validate_live_state(load("invalid-routing-before-009e.json")))

    def test_08_revoked_transition_fails(self):
        self.assertCode(
            "REVOKED_PROVIDER",
            lambda: lg.plan_transition(
                lg.validate_live_state(load("invalid-revoked-provider.json")),
                "LIVE_VALIDATION_READY",
                target_state=ready_state(),
            ),
        )

    def test_09_unknown_field(self):
        value = load("valid-live-validation-ready.json"); value["x"] = 1
        self.assertCode("EXTRA_FIELD", lambda: lg.validate_live_state(value))

    def test_10_missing_field(self):
        value = load("valid-live-validation-ready.json"); del value["offline_qa_ref"]
        self.assertCode("MISSING_FIELD", lambda: lg.validate_live_state(value))

    def test_11_duplicate_json_key(self):
        self.assertCode("DUPLICATE_JSON_KEY", lambda: lg.load_json_document('{"schema_version":"1.0","schema_version":"1.0"}'))

    def test_12_nonfinite_json(self):
        self.assertCode("INPUT_NUMBER", lambda: lg.load_json_document('{"x":NaN}'))

    def test_13_unicode_surrogate(self):
        value = load("valid-live-validation-ready.json"); value["live_state_id"] = "provider-live-state:\ud800"
        self.assertCode("INPUT_ENCODING", lambda: lg.validate_live_state(value))

    def test_14_structure_depth(self):
        value = {}; cursor = value
        for _ in range(lg.MAX_STRUCTURE_DEPTH + 3):
            cursor["x"] = {}; cursor = cursor["x"]
        self.assertCode("STRUCTURE_LIMIT", lambda: lg.validate_live_state(value))

    def test_15_secret_field(self):
        value = load("valid-live-validation-ready.json"); value["access_token"] = "not-used"
        self.assertCode("SECRET_MATERIAL", lambda: lg.validate_live_state(value))

    def test_16_secret_like_value(self):
        value = load("valid-live-validation-ready.json"); value["offline_qa_ref"] = "qa:sk-ABCDEFGHIJKLMNOPQRSTUV"
        self.assertCode("SECRET_MATERIAL", lambda: lg.validate_live_state(value))

    def test_17_input_immutable(self):
        value = load("valid-live-validation-ready.json"); before = copy.deepcopy(value)
        lg.validate_live_state(value)
        self.assertEqual(value, before)

    def test_18_digest_mismatch(self):
        value = load("valid-live-validation-ready.json"); value["canonical_digest"] = "sha256:" + "1" * 64
        self.assertCode("DIGEST_MISMATCH", lambda: lg.validate_live_state(value))

    def test_19_shadow_policy_valid(self):
        self.assertEqual(lg.validate_worker_mode_policy(shadow_policy())["mode"], "LIVE_SHADOW_WORKER")

    def test_20_bounded_policy_valid(self):
        self.assertEqual(lg.validate_worker_mode_policy(bounded_policy())["mode"], "LIVE_BOUNDED_WORKER")

    def test_21_shadow_write_forbidden(self):
        value = shadow_policy(); value["repository_write_allowed"] = True; value = reseal(value)
        self.assertCode("WORKER_AUTHORITY", lambda: lg.validate_worker_mode_policy(value))

    def test_22_bounded_claim_required(self):
        value = bounded_policy(); value["writer_claim_ref"] = None; value = reseal(value)
        self.assertCode("WRITER_CLAIM_REQUIRED", lambda: lg.validate_worker_mode_policy(value))

    def test_23_unsafe_path(self):
        value = bounded_policy(); value["allowed_paths"] = ["../secrets"]; value = reseal(value)
        self.assertCode("UNSAFE_PATH", lambda: lg.validate_worker_mode_policy(value))

    def test_24_merge_forbidden(self):
        value = bounded_policy(); value["merge_allowed"] = True; value = reseal(value)
        self.assertCode("WORKER_AUTHORITY", lambda: lg.validate_worker_mode_policy(value))

    def test_25_transition_disabled_ready(self):
        result = lg.plan_transition(disabled_state(), "LIVE_VALIDATION_READY", target_state=ready_state())
        self.assertEqual(result["decision"], "ALLOWED")

    def test_26_transition_ready_validated_requires_bound_evidence(self):
        self.assertCode(
            "MISSING_CONNECTED_EVIDENCE",
            lambda: lg.plan_transition(ready_state(), "LIVE_VALIDATED", target_state=validated_state()),
        )

    def test_27_transition_validated_shadow(self):
        result = lg.plan_transition(
            validated_state(),
            "LIVE_SHADOW_WORKER",
            target_state=shadow_state(),
            worker_policy=lg.validate_worker_mode_policy(shadow_policy()),
        )
        self.assertEqual(result["to"], "LIVE_SHADOW_WORKER")

    def test_28_routing_requires_authority(self):
        self.assertCode(
            "ROUTING_BEFORE_009E",
            lambda: lg.plan_transition(
                bounded_state(), "ROUTING_ELIGIBLE", target_state=routing_state(), routing_authority=False
            ),
        )

    def test_29_ready_requires_validated_target_state(self):
        self.assertCode(
            "TARGET_STATE_REQUIRED",
            lambda: lg.plan_transition(disabled_state(), "LIVE_VALIDATION_READY"),
        )

    def test_30_connected_evidence_cross_profile_rejected(self):
        self.assertCode(
            "LINEAGE_MISMATCH",
            lambda: lg.plan_transition(
                ready_state(),
                "LIVE_VALIDATED",
                target_state=validated_state(),
                connected_evidence=bound_connected_evidence(profile="provider-profile:synthetic-beta"),
            ),
        )

    def test_31_shadow_worker_cross_profile_rejected(self):
        policy = lg.validate_worker_mode_policy(shadow_policy(profile="provider-profile:synthetic-beta"))
        self.assertCode(
            "LINEAGE_MISMATCH",
            lambda: lg.plan_transition(validated_state(), "LIVE_SHADOW_WORKER", target_state=shadow_state(), worker_policy=policy),
        )

    def test_32_bounded_worker_cross_child_rejected(self):
        policy = lg.validate_worker_mode_policy(bounded_policy(child="STUDIO-009P-98"))
        self.assertCode(
            "LINEAGE_MISMATCH",
            lambda: lg.plan_transition(validated_state(), "LIVE_BOUNDED_WORKER", target_state=bounded_state(), worker_policy=policy),
        )

    def test_33_target_state_cross_lineage_rejected(self):
        target = ready_state().copy()
        target["provider_profile_id"] = "provider-profile:synthetic-beta"
        self.assertCode(
            "LINEAGE_MISMATCH",
            lambda: lg.plan_transition(disabled_state(), "LIVE_VALIDATION_READY", target_state=target),
        )

    def test_34_worker_profile_id_format_strict(self):
        value = shadow_policy(); value["provider_profile_id"] = "profile:wrong"; value = reseal(value)
        self.assertCode("INVALID_FORMAT", lambda: lg.validate_worker_mode_policy(value))

    def test_35_bound_connected_evidence_transition_allowed(self):
        result = lg.plan_transition(
            ready_state(),
            "LIVE_VALIDATED",
            target_state=validated_state(),
            connected_evidence=bound_connected_evidence(),
        )
        self.assertEqual(result["decision"], "ALLOWED")

    def test_36_routing_with_explicit_authority_allowed(self):
        result = lg.plan_transition(
            bounded_state(),
            "ROUTING_ELIGIBLE",
            target_state=routing_state(),
            routing_authority=True,
        )
        self.assertEqual(result["to"], "ROUTING_ELIGIBLE")
