from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts import groq_live_smoke as smoke
from scripts import groq_live_transport as transport
from scripts import provider_live_evidence
from scripts import provider_live_gate
from scripts import session_credential_bridge as bridge

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "platform" / "connectivity" / "live" / "evidence" / "009v01"
SECRET = "synthetic-secret-material-1234567890"
AS_OF = "2026-09-05T01:00:00Z"

def preflight():
    return {
        "v_contract_merge": smoke.V_CONTRACT_MERGE,
        "p01_closeout_merge": smoke.P01_CLOSEOUT_MERGE,
        "r01_closeout_merge": smoke.R01_CLOSEOUT_MERGE,
        "provider_profile_id": smoke.PROVIDER_PROFILE_ID,
        "provider_child_id": smoke.PROVIDER_CHILD_ID,
        "model": smoke.MODEL_ID,
        "host": smoke.HOST,
        "free_tier_confirmed": True,
        "zdr_confirmed": True,
        "model_permission_confirmed": True,
        "money_ceiling": 0,
        "max_requests": 3,
        "concurrency": 1,
        "retry_count": 0,
        "kill_switch_armed": True,
        "as_of": AS_OF,
    }

def lease():
    value = {
        "schema_version": "1.0",
        "credential_lease_id": "credential-lease:" + "c" * 32,
        "credential_profile_id": bridge.CREDENTIAL_PROFILE_ID,
        "profile_digest": "sha256:" + "d" * 64,
        "subject_ref": bridge.SUBJECT_REF,
        "capability": bridge.CAPABILITY,
        "purpose": bridge.PURPOSE,
        "repository_record_digest": None,
        "operation_digest": None,
        "issued_at": "2026-09-05T00:59:00Z",
        "expires_at": "2026-09-05T01:10:00Z",
        "idempotency_key": "studio-009v-01-smoke",
        "canonical_digest": "",
    }
    value["canonical_digest"] = bridge.canonical_digest(value)
    return value

def success_transport():
    expected = iter([probe["expected"] for probe in smoke.PROBES])
    calls = []
    def fn(secret, body):
        calls.append(copy.deepcopy(body))
        value = next(expected)
        return {
            "status": 200,
            "model": smoke.MODEL_ID,
            "service_tier": "on_demand",
            "finish_reason": "stop",
            "content": json.dumps(value, separators=(",", ":")),
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            "quota": {"remaining_requests": 999},
            "model_identity_verified": True,
            "transport_identity_verified": True,
            "host": smoke.HOST,
            "path": transport.PATH,
            "retry_count": 0,
        }
    return fn, calls

def memory_reserver():
    state = {"count": 0, "probes": []}
    def reserve(probe_id, expected_number):
        if expected_number != state["count"] + 1:
            return -1
        state["count"] = expected_number
        state["probes"].append(probe_id)
        return expected_number
    return reserve, state

class GroqLiveSmokeTests(unittest.TestCase):
    def assertSmokeCode(self, code, fn):
        with self.assertRaises(smoke.GroqSmokeError) as ctx:
            fn()
        self.assertEqual(ctx.exception.code, code)

    def test_01_constants_and_fixed_probe_count(self):
        self.assertEqual(smoke.MAX_REQUESTS, 3)
        self.assertEqual(len(smoke.PROBES), 3)
        self.assertEqual(smoke.MONEY_CEILING, 0)

    def test_02_valid_preflight(self):
        self.assertEqual(smoke.validate_preflight(preflight())["host"], "api.groq.com")

    def test_03_free_tier_confirmation_required(self):
        value = preflight()
        value["free_tier_confirmed"] = False
        self.assertSmokeCode("TIER_NOT_CONFIRMED", lambda: smoke.validate_preflight(value))

    def test_04_zdr_confirmation_required(self):
        value = preflight()
        value["zdr_confirmed"] = False
        self.assertSmokeCode("ZDR_NOT_CONFIRMED", lambda: smoke.validate_preflight(value))

    def test_05_zero_money_required(self):
        value = preflight()
        value["money_ceiling"] = 1
        self.assertSmokeCode("NONZERO_BUDGET", lambda: smoke.validate_preflight(value))

    def test_06_exact_contract_lineage_required(self):
        value = preflight()
        value["v_contract_merge"] = "0" * 40
        self.assertSmokeCode("LINEAGE_MISMATCH", lambda: smoke.validate_preflight(value))

    def test_07_request_ceiling_is_exact_three(self):
        value = preflight()
        value["max_requests"] = 4
        self.assertSmokeCode("REQUEST_LIMIT", lambda: smoke.validate_preflight(value))

    def test_08_retry_must_be_zero(self):
        value = preflight()
        value["retry_count"] = 1
        self.assertSmokeCode("INVALID_PREFLIGHT", lambda: smoke.validate_preflight(value))

    def test_09_concurrency_must_be_one(self):
        value = preflight()
        value["concurrency"] = 2
        self.assertSmokeCode("INVALID_PREFLIGHT", lambda: smoke.validate_preflight(value))

    def test_10_successful_smoke_is_three_sequential_requests(self):
        fn, calls = success_transport()
        reserve, ledger = memory_reserver()
        result = smoke.execute_smoke(
            preflight(), lease(), supplier=lambda: SECRET, request_reserver=reserve, transport_fn=fn
        )
        self.assertEqual(result["request_count"], 3)
        self.assertTrue(result["quality_pass"])
        self.assertIsNone(result["observed_spend"])
        self.assertTrue(result["post_smoke_spend_confirmation_required"])
        self.assertEqual(ledger["count"], 3)
        self.assertEqual(len(calls), 3)
        self.assertTrue(all(call["tool_choice"] == "none" for call in calls))

    def test_11_quality_failure_stops_automatically(self):
        calls = []
        def bad(secret, body):
            calls.append(1)
            return {
                "model": smoke.MODEL_ID, "service_tier": "on_demand",
                "finish_reason": "stop", "content": '{"wrong":true}',
                "usage": {}, "quota": {},
                "model_identity_verified": True, "transport_identity_verified": True,
            }
        self.assertSmokeCode(
            "QUALITY_FAILED",
            lambda: smoke.execute_smoke(
                preflight(), lease(), supplier=lambda: SECRET,
                request_reserver=memory_reserver()[0], transport_fn=bad
            ),
        )
        self.assertEqual(len(calls), 1)

    def test_12_kill_switch_blocks_additional_request(self):
        switch = smoke.KillSwitch(True)
        calls = []
        first_expected = smoke.PROBES[0]["expected"]
        def fn(secret, body):
            calls.append(1)
            switch.revoke()
            return {
                "model": smoke.MODEL_ID, "service_tier": "on_demand",
                "finish_reason": "stop",
                "content": json.dumps(first_expected, separators=(",", ":")),
                "usage": {}, "quota": {},
                "model_identity_verified": True, "transport_identity_verified": True,
            }
        self.assertSmokeCode(
            "KILL_SWITCH",
            lambda: smoke.execute_smoke(
                preflight(), lease(), supplier=lambda: SECRET,
                request_reserver=memory_reserver()[0], transport_fn=fn, kill_switch=switch
            ),
        )
        self.assertEqual(len(calls), 1)

    def test_13_transport_failure_has_no_automatic_second_call(self):
        calls = []
        def fn(secret, body):
            calls.append(1)
            raise transport.GroqTransportError("QUOTA")
        with self.assertRaises(transport.GroqTransportError):
            smoke.execute_smoke(
                preflight(), lease(), supplier=lambda: SECRET,
                request_reserver=memory_reserver()[0], transport_fn=fn
            )
        self.assertEqual(len(calls), 1)

    def test_14_result_contains_digest_not_raw_output(self):
        fn, _ = success_transport()
        result = smoke.execute_smoke(
            preflight(), lease(), supplier=lambda: SECRET,
            request_reserver=memory_reserver()[0], transport_fn=fn
        )
        serialized = json.dumps(result)
        self.assertNotIn('{"status":"ok","value":7}', serialized)
        self.assertIn("content_sha256", serialized)

    def test_15_model_permission_confirmation_required(self):
        value = preflight()
        value["model_permission_confirmed"] = False
        self.assertSmokeCode(
            "MODEL_PERMISSION_NOT_CONFIRMED",
            lambda: smoke.validate_preflight(value),
        )

    def test_16_request_reservation_is_mandatory(self):
        fn, calls = success_transport()
        self.assertSmokeCode(
            "REQUEST_RESERVATION",
            lambda: smoke.execute_smoke(
                preflight(), lease(), supplier=lambda: SECRET, transport_fn=fn
            ),
        )
        self.assertEqual(calls, [])

    def test_17_ready_evidence_validates_generic_live_gate(self):
        value = json.loads((EVIDENCE / "provider-live-state.json").read_text(encoding="utf-8"))
        normalized = provider_live_gate.validate_live_state(
            value, parent_allowed_data_classifications=["PUBLIC"]
        )
        self.assertEqual(normalized["state"], "LIVE_VALIDATION_READY")

    def test_18_pending_connected_evidence_is_not_accepted_as_live_validated(self):
        value = json.loads((EVIDENCE / "connected-validation.json").read_text(encoding="utf-8"))
        with self.assertRaises(provider_live_evidence.ConnectedEvidenceError):
            provider_live_evidence.validate_connected_validation(value)
