from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts import nvidia_nim_live_smoke as s
from scripts import nvidia_nim_session_credential_bridge as b

SECRET = "synthetic_session_secret_0123456789"
AS_OF = "2026-09-08T17:00:00Z"

def preflight():
    return {
        "v_contract_merge": s.V_CONTRACT_MERGE,
        "p03_closeout_merge": s.P03_CLOSEOUT_MERGE,
        "provider_profile_id": s.PROVIDER_PROFILE_ID,
        "provider_child_id": s.PROVIDER_CHILD_ID,
        "model": s.MODEL_ID,
        "host": s.HOST,
        "account_ref": s.ACCOUNT_REF,
        "free_endpoint_confirmed": True,
        "account_free_entitlement_confirmed": True,
        "no_billing_method_required_confirmed": True,
        "no_purchase_required_confirmed": True,
        "revocation_path_confirmed": True,
        "internal_testing_terms_confirmed": True,
        "no_paid_path_confirmed": True,
        "money_ceiling": 0,
        "max_requests": 3,
        "concurrency": 1,
        "retry_count": 0,
        "kill_switch_armed": True,
        "as_of": AS_OF,
    }

def lease():
    x = {
        "schema_version": "1.0",
        "credential_lease_id": "credential-lease:" + "a"*32,
        "credential_profile_id": b.CREDENTIAL_PROFILE_ID,
        "account_ref": b.ACCOUNT_REF,
        "profile_digest": "sha256:" + "b"*64,
        "subject_ref": b.SUBJECT_REF,
        "capability": b.CAPABILITY,
        "purpose": b.PURPOSE,
        "repository_record_digest": None,
        "operation_digest": None,
        "issued_at": "2026-09-08T16:59:00Z",
        "expires_at": "2026-09-08T17:10:00Z",
        "idempotency_key": "v03-smoke-0001",
        "canonical_digest": "",
    }
    x["canonical_digest"] = b.canonical_digest(x)
    return x

def fake_transport(secret, body):
    content_by_prompt = {
        "STRUCTURED_OUTPUT": '{"status":"ok","value":7}',
        "BOUNDED_REASONING": '{"sorted":[1,2,3],"sum":6}',
        "SYNTHETIC_CODE_REVIEW": '{"bug":"uses subtraction","fix":"return a + b"}',
    }
    text = body["messages"][0]["content"]
    probe = next(p["id"] for p in s.PROBES if p["messages"][0]["content"] == text)
    return {
        "status": 200,
        "model": s.MODEL_ID,
        "finish_reason": "stop",
        "content": content_by_prompt[probe],
        "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
        "model_identity_verified": True,
        "transport_identity_verified": True,
        "host": s.HOST,
        "path": "/v1/chat/completions",
        "retry_count": 0,
    }

class NvidiaNimLiveSmokeTests(unittest.TestCase):
    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(s.NvidiaNimSmokeError) as cm:
            fn(*args, **kwargs)
        self.assertEqual(cm.exception.code, code)

    def test_01_preflight_valid(self):
        out = s.validate_preflight(preflight())
        self.assertEqual(out["money_ceiling"], 0)

    def test_02_preflight_immutable(self):
        x = preflight(); before = copy.deepcopy(x)
        s.validate_preflight(x)
        self.assertEqual(x, before)

    def test_03_wrong_contract_merge(self):
        x = preflight(); x["v_contract_merge"] = "wrong"
        self.assert_code("LINEAGE_MISMATCH", s.validate_preflight, x)

    def test_04_free_endpoint_required(self):
        x = preflight(); x["free_endpoint_confirmed"] = False
        self.assert_code("FREE_ENDPOINT_NOT_CONFIRMED", s.validate_preflight, x)

    def test_05_entitlement_required(self):
        x = preflight(); x["account_free_entitlement_confirmed"] = False
        self.assert_code("FREE_ENTITLEMENT_NOT_CONFIRMED", s.validate_preflight, x)

    def test_06_billing_denial_required(self):
        x = preflight(); x["no_billing_method_required_confirmed"] = False
        self.assert_code("BILLING_NOT_DENIED", s.validate_preflight, x)

    def test_07_purchase_denial_required(self):
        x = preflight(); x["no_purchase_required_confirmed"] = False
        self.assert_code("PURCHASE_NOT_DENIED", s.validate_preflight, x)

    def test_08_revocation_required(self):
        x = preflight(); x["revocation_path_confirmed"] = False
        self.assert_code("REVOCATION_NOT_CONFIRMED", s.validate_preflight, x)

    def test_09_terms_required(self):
        x = preflight(); x["internal_testing_terms_confirmed"] = False
        self.assert_code("TERMS_NOT_CONFIRMED", s.validate_preflight, x)

    def test_10_paid_path_denied(self):
        x = preflight(); x["no_paid_path_confirmed"] = False
        self.assert_code("PAID_PATH_NOT_DENIED", s.validate_preflight, x)

    def test_11_money_zero(self):
        x = preflight(); x["money_ceiling"] = 1
        self.assert_code("NONZERO_BUDGET", s.validate_preflight, x)

    def test_12_max_requests_exact(self):
        x = preflight(); x["max_requests"] = 4
        self.assert_code("REQUEST_LIMIT", s.validate_preflight, x)

    def test_13_concurrency_exact(self):
        x = preflight(); x["concurrency"] = 2
        self.assert_code("INVALID_PREFLIGHT", s.validate_preflight, x)

    def test_14_retry_zero(self):
        x = preflight(); x["retry_count"] = 1
        self.assert_code("INVALID_PREFLIGHT", s.validate_preflight, x)

    def test_15_kill_switch_required(self):
        x = preflight(); x["kill_switch_armed"] = False
        self.assert_code("KILL_SWITCH", s.validate_preflight, x)

    def test_16_ledger_initial_state(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            self.assertEqual(led.snapshot()["request_count"], 0)

    def test_17_ledger_reserve(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            out = led.reserve("PROBE_ONE", 1)
            self.assertTrue(out["reserved_before_network"])
            self.assertEqual(led.snapshot()["request_count"], 1)

    def test_18_ledger_wrong_ordinal(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            self.assert_code("REQUEST_RESERVATION", led.reserve, "PROBE_ONE", 2)

    def test_19_ledger_max_three(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            for i in range(1,4): led.reserve("PROBE_"+str(i), i)
            self.assert_code("REQUEST_LIMIT", led.reserve, "PROBE_4", 4)

    def test_20_ledger_persists(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"ledger.json"
            led = s.DurableCampaignLedger(p, "campaign:test-v03")
            led.reserve("PROBE_ONE", 1)
            led2 = s.DurableCampaignLedger(p, "campaign:test-v03")
            self.assertEqual(led2.snapshot()["request_count"], 1)

    def test_21_smoke_pass(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            out = s.execute_smoke(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertEqual(out["status"], "SMOKE_PASS")
            self.assertEqual(out["request_count"], 3)
            self.assertTrue(out["quality_pass"])

    def test_22_smoke_no_raw_output(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            out = s.execute_smoke(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertNotIn('{"status":"ok","value":7}', repr(out))
            self.assertNotIn(SECRET, repr(out))

    def test_23_smoke_ledger_three(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            s.execute_smoke(preflight(), lease(), ledger=led,
                            secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertEqual(led.snapshot()["request_count"], 3)

    def test_24_kill_switch_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            switch = s.KillSwitch(True); switch.revoke()
            self.assert_code("KILL_SWITCH", s.execute_smoke, preflight(), lease(),
                             ledger=led, secret_supplier=lambda: SECRET,
                             transport_fn=fake_transport, kill_switch=switch)

    def test_25_quality_failure(self):
        def bad(secret, body):
            x = fake_transport(secret, body)
            x["content"] = '{"wrong":true}'
            return x
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            self.assert_code("QUALITY_FAILED", s.execute_smoke, preflight(), lease(),
                             ledger=led, secret_supplier=lambda: SECRET, transport_fn=bad)

    def test_26_identity_failure(self):
        def bad(secret, body):
            x = fake_transport(secret, body)
            x["model_identity_verified"] = False
            return x
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            self.assert_code("QUALITY_FAILED", s.execute_smoke, preflight(), lease(),
                             ledger=led, secret_supplier=lambda: SECRET, transport_fn=bad)

    def test_27_failed_request_consumes_reservation(self):
        def fail(secret, body):
            raise RuntimeError("synthetic failure")
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            with self.assertRaises(RuntimeError):
                s.execute_smoke(preflight(), lease(), ledger=led,
                                secret_supplier=lambda: SECRET, transport_fn=fail)
            self.assertEqual(led.snapshot()["request_count"], 1)

    def test_28_invalid_ledger_type(self):
        self.assert_code("REQUEST_RESERVATION", s.execute_smoke, preflight(), lease(),
                         ledger=object(), secret_supplier=lambda: SECRET, transport_fn=fake_transport)

    def test_29_output_hash_present(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            out = s.execute_smoke(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertTrue(out["records"][0]["content_sha256"].startswith("sha256:"))

    def test_30_spend_not_fabricated(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v03")
            out = s.execute_smoke(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertIsNone(out["observed_spend"])
            self.assertTrue(out["post_smoke_spend_confirmation_required"])

# Offline V-03 sidecar/live-state integration tests.
from pathlib import Path as _V03Path
from scripts import provider_live_gate as _v03_live_gate
import json as _v03_json

_V03_ROOT = _V03Path(__file__).resolve().parents[1]
_V03_PROVIDER = _V03_ROOT / "platform/connectivity/providers/nvidia-nim"
_V03_EVIDENCE = _V03_ROOT / "platform/connectivity/live/evidence/009v03"

class NvidiaNimV03OfflineEvidenceTests(unittest.TestCase):
    def _load(self, path):
        with open(path, "r", encoding="utf-8") as handle:
            return _v03_json.load(handle)

    def test_31_live_policy_state_ready(self):
        p = self._load(_V03_PROVIDER / "live-validation-policy.json")
        self.assertEqual(p["current_state"], "LIVE_VALIDATION_READY")
        self.assertFalse(p["connected_execution_authorized"])

    def test_32_live_policy_bounds(self):
        p = self._load(_V03_PROVIDER / "live-validation-policy.json")
        self.assertEqual(p["max_requests"], 3)
        self.assertEqual(p["max_concurrency"], 1)
        self.assertEqual(p["max_retries"], 0)
        self.assertEqual(p["money_ceiling"], 0)

    def test_33_generic_live_state_valid(self):
        record = self._load(_V03_EVIDENCE / "provider-live-state.json")
        out = _v03_live_gate.validate_live_state(
            record, parent_allowed_data_classifications=["PUBLIC"]
        )
        self.assertEqual(out["state"], "LIVE_VALIDATION_READY")
        self.assertEqual(out["money_ceiling"], 0)

    def test_34_live_state_has_no_routing_authority(self):
        record = self._load(_V03_EVIDENCE / "provider-live-state.json")
        self.assertIsNone(record["routing_authority_ref"])
        self.assertEqual(record["allowed_data_classifications"], ["PUBLIC"])

    def test_35_connected_evidence_pending(self):
        record = self._load(_V03_EVIDENCE / "connected-validation.json")
        self.assertEqual(record["status"], "PENDING_REAL_SMOKE")
        self.assertEqual(record["request_count"], 0)
        self.assertIsNone(record["observed_spend"])

    def test_36_quality_evidence_pending(self):
        record = self._load(_V03_EVIDENCE / "quality-evaluation.json")
        self.assertEqual(record["status"], "PENDING_REAL_SMOKE")
        self.assertFalse(record["quality_pass"])
        self.assertEqual(record["probe_count"], 0)

    def test_37_pending_evidence_contains_no_raw_material(self):
        connected = self._load(_V03_EVIDENCE / "connected-validation.json")
        quality = self._load(_V03_EVIDENCE / "quality-evaluation.json")
        self.assertFalse(connected["raw_provider_output_committed"])
        self.assertFalse(connected["raw_credential_committed"])
        self.assertFalse(quality["raw_model_output_committed"])

    def test_38_promotion_ceiling_only_live_validated(self):
        p = self._load(_V03_PROVIDER / "live-validation-policy.json")
        self.assertEqual(p["promotion_ceiling"], "LIVE_VALIDATED")
        self.assertFalse(p["routing"])
        self.assertFalse(p["tools"])
