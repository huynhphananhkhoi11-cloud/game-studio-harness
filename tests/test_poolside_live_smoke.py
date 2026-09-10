from __future__ import annotations

import copy
import json
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from datetime import datetime, timezone
import inspect as _v04_inspect

from scripts import poolside_live_smoke as s
from scripts import poolside_session_credential_bridge as b

SECRET = "synthetic_session_secret_0123456789"
AS_OF = "2026-09-08T17:00:00Z"

def preflight():
    return {
        "v_contract_merge": s.V_CONTRACT_MERGE,
        "p04_closeout_merge": s.P04_CLOSEOUT_MERGE,
        "provider_profile_id": s.PROVIDER_PROFILE_ID,
        "provider_child_id": s.PROVIDER_CHILD_ID,
        "model": s.MODEL_ID,
        "host": s.HOST,
        "account_ref": s.ACCOUNT_REF,
        "standalone_offer_confirmed": True,
        "account_zero_cost_confirmed": True,
        "no_billing_method_required_confirmed": True,
        "no_purchase_required_confirmed": True,
        "server_side_revocation_confirmed": True,
        "terms_data_policy_compatible_confirmed": True,
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
        "idempotency_key": "v04-smoke-0001",
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

class PoolsideLiveSmokeTests(unittest.TestCase):
    def setUp(self):
        self._now_patch = mock.patch.object(
            s,
            "_utc_now",
            return_value=datetime(2026, 9, 8, 17, 0, 0, tzinfo=timezone.utc),
        )
        self._now_patch.start()

    def tearDown(self):
        self._now_patch.stop()

    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(s.PoolsideLiveSmokeError) as cm:
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
        x = preflight(); x["standalone_offer_confirmed"] = False
        self.assert_code("STANDALONE_OFFER_NOT_CONFIRMED", s.validate_preflight, x)

    def test_05_entitlement_required(self):
        x = preflight(); x["account_zero_cost_confirmed"] = False
        self.assert_code("ZERO_COST_ELIGIBILITY_UNPROVEN", s.validate_preflight, x)

    def test_06_billing_denial_required(self):
        x = preflight(); x["no_billing_method_required_confirmed"] = False
        self.assert_code("BILLING_NOT_DENIED", s.validate_preflight, x)

    def test_07_purchase_denial_required(self):
        x = preflight(); x["no_purchase_required_confirmed"] = False
        self.assert_code("PURCHASE_NOT_DENIED", s.validate_preflight, x)

    def test_08_revocation_required(self):
        x = preflight(); x["server_side_revocation_confirmed"] = False
        self.assert_code("CREDENTIAL_REVOCATION_UNPROVEN", s.validate_preflight, x)

    def test_09_terms_required(self):
        x = preflight(); x["terms_data_policy_compatible_confirmed"] = False
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
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            self.assertEqual(led.snapshot()["request_count"], 0)

    def test_17_ledger_reserve(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            out = led.reserve("PROBE_ONE", 1)
            self.assertTrue(out["reserved_before_network"])
            self.assertEqual(led.snapshot()["request_count"], 1)

    def test_18_ledger_wrong_ordinal(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            self.assert_code("REQUEST_RESERVATION", led.reserve, "PROBE_ONE", 2)

    def test_19_ledger_max_three(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            for i in range(1,4): led.reserve("PROBE_"+str(i), i)
            self.assert_code("REQUEST_LIMIT", led.reserve, "PROBE_4", 4)

    def test_20_ledger_persists(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"ledger.json"
            led = s.DurableCampaignLedger(p, "campaign:test-v04")
            led.reserve("PROBE_ONE", 1)
            led2 = s.DurableCampaignLedger(p, "campaign:test-v04")
            self.assertEqual(led2.snapshot()["request_count"], 1)

    def test_21_smoke_pass(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            out = s._execute_smoke_for_test(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertEqual(out["status"], "SMOKE_PASS")
            self.assertEqual(out["request_count"], 3)
            self.assertTrue(out["quality_pass"])

    def test_22_smoke_no_raw_output(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            out = s._execute_smoke_for_test(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertNotIn('{"status":"ok","value":7}', repr(out))
            self.assertNotIn(SECRET, repr(out))

    def test_23_smoke_ledger_three(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            s._execute_smoke_for_test(preflight(), lease(), ledger=led,
                            secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertEqual(led.snapshot()["request_count"], 3)

    def test_24_kill_switch_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            switch = s.KillSwitch(True); switch.revoke()
            self.assert_code("KILL_SWITCH", s._execute_smoke_for_test, preflight(), lease(),
                             ledger=led, secret_supplier=lambda: SECRET,
                             transport_fn=fake_transport, kill_switch=switch)

    def test_25_quality_failure(self):
        def bad(secret, body):
            x = fake_transport(secret, body)
            x["content"] = '{"wrong":true}'
            return x
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            self.assert_code("QUALITY_FAILED", s._execute_smoke_for_test, preflight(), lease(),
                             ledger=led, secret_supplier=lambda: SECRET, transport_fn=bad)

    def test_26_identity_failure(self):
        def bad(secret, body):
            x = fake_transport(secret, body)
            x["model_identity_verified"] = False
            return x
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            self.assert_code("QUALITY_FAILED", s._execute_smoke_for_test, preflight(), lease(),
                             ledger=led, secret_supplier=lambda: SECRET, transport_fn=bad)

    def test_27_failed_request_consumes_reservation(self):
        def fail(secret, body):
            raise RuntimeError("synthetic failure")
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            with self.assertRaises(RuntimeError):
                s._execute_smoke_for_test(preflight(), lease(), ledger=led,
                                secret_supplier=lambda: SECRET, transport_fn=fail)
            self.assertEqual(led.snapshot()["request_count"], 1)

    def test_28_invalid_ledger_type(self):
        self.assert_code("REQUEST_RESERVATION", s._execute_smoke_for_test, preflight(), lease(),
                         ledger=object(), secret_supplier=lambda: SECRET, transport_fn=fake_transport)

    def test_29_output_hash_present(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            out = s._execute_smoke_for_test(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertTrue(out["records"][0]["content_sha256"].startswith("sha256:"))

    def test_30_spend_not_fabricated(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            out = s._execute_smoke_for_test(preflight(), lease(), ledger=led,
                                  secret_supplier=lambda: SECRET, transport_fn=fake_transport)
            self.assertIsNone(out["observed_spend"])
            self.assertTrue(out["post_smoke_spend_confirmation_required"])

# Offline V-04 sidecar/live-state integration tests.
from pathlib import Path as _V04Path
from scripts import provider_live_gate as _v04_live_gate
import json as _v04_json

_V04_ROOT = _V04Path(__file__).resolve().parents[1]
_V04_PROVIDER = _V04_ROOT / "platform/connectivity/providers/poolside"
_V04_EVIDENCE = _V04_ROOT / "platform/connectivity/live/evidence/009v04"

class PoolsideV04OfflineEvidenceTests(unittest.TestCase):
    def _load(self, path):
        with open(path, "r", encoding="utf-8") as handle:
            return _v04_json.load(handle)

    def test_31_live_policy_state_ready(self):
        p = self._load(_V04_PROVIDER / "live-validation-policy.json")
        self.assertEqual(p["current_state"], "LIVE_VALIDATION_READY")
        self.assertFalse(p["connected_execution_authorized"])

    def test_32_live_policy_bounds(self):
        p = self._load(_V04_PROVIDER / "live-validation-policy.json")
        self.assertEqual(p["max_requests"], 3)
        self.assertEqual(p["max_concurrency"], 1)
        self.assertEqual(p["max_retries"], 0)
        self.assertEqual(p["money_ceiling"], 0)

    def test_33_generic_live_state_valid(self):
        record = self._load(_V04_EVIDENCE / "provider-live-state.json")
        out = _v04_live_gate.validate_live_state(
            record, parent_allowed_data_classifications=["PUBLIC"]
        )
        self.assertEqual(out["state"], "LIVE_VALIDATION_READY")
        self.assertEqual(out["money_ceiling"], 0)

    def test_34_live_state_has_no_routing_authority(self):
        record = self._load(_V04_EVIDENCE / "provider-live-state.json")
        self.assertIsNone(record["routing_authority_ref"])
        self.assertEqual(record["allowed_data_classifications"], ["PUBLIC"])

    def test_35_connected_evidence_pending(self):
        record = self._load(_V04_EVIDENCE / "connected-validation.json")
        self.assertEqual(record["status"], "PENDING_REAL_SMOKE")
        self.assertEqual(record["request_count"], 0)
        self.assertIsNone(record["observed_spend"])

    def test_36_quality_evidence_pending(self):
        record = self._load(_V04_EVIDENCE / "quality-evaluation.json")
        self.assertEqual(record["status"], "PENDING_REAL_SMOKE")
        self.assertFalse(record["quality_pass"])
        self.assertEqual(record["probe_count"], 0)

    def test_37_pending_evidence_contains_no_raw_material(self):
        connected = self._load(_V04_EVIDENCE / "connected-validation.json")
        quality = self._load(_V04_EVIDENCE / "quality-evaluation.json")
        self.assertFalse(connected["raw_provider_output_committed"])
        self.assertFalse(connected["raw_credential_committed"])
        self.assertFalse(quality["raw_model_output_committed"])

    def test_38_promotion_ceiling_only_live_validated(self):
        p = self._load(_V04_PROVIDER / "live-validation-policy.json")
        self.assertEqual(p["promotion_ceiling"], "LIVE_VALIDATED")
        self.assertFalse(p["routing"])
        self.assertFalse(p["tools"])

class PoolsideV04PreQaRepairTests(unittest.TestCase):
    def setUp(self):
        self._now_patch = mock.patch.object(
            s,
            "_utc_now",
            return_value=datetime(2026, 9, 8, 17, 0, 0, tzinfo=timezone.utc),
        )
        self._now_patch.start()

    def tearDown(self):
        self._now_patch.stop()

    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(s.PoolsideLiveSmokeError) as cm:
            fn(*args, **kwargs)
        self.assertEqual(cm.exception.code, code)

    def test_repair_01_public_smoke_has_no_test_injection(self):
        params = _v04_inspect.signature(s.execute_smoke).parameters
        self.assertNotIn("secret_supplier", params)
        self.assertNotIn("transport_fn", params)

    def test_repair_02_stale_preflight_rejected(self):
        x = preflight(); x["as_of"] = "2026-09-08T16:44:59Z"
        self.assert_code("PREFLIGHT_STALE", s.validate_preflight, x)

    def test_repair_03_future_preflight_rejected(self):
        x = preflight(); x["as_of"] = "2026-09-08T17:02:01Z"
        self.assert_code("PREFLIGHT_STALE", s.validate_preflight, x)

    def test_repair_04_concurrent_campaign_lock_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            lock = s.CampaignExecutionLock(led)
            lock.acquire()
            try:
                self.assert_code(
                    "CAMPAIGN_ACTIVE",
                    s._execute_smoke_for_test,
                    preflight(),
                    lease(),
                    ledger=led,
                    secret_supplier=lambda: SECRET,
                    transport_fn=fake_transport,
                )
            finally:
                lock.release()

    def test_repair_05_tampered_ledger_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"ledger.json"
            led = s.DurableCampaignLedger(p, "campaign:test-v04")
            value = led.snapshot()
            value["request_count"] = 1
            value["reservations"] = []
            p.write_text(json.dumps(value), encoding="utf-8")
            self.assert_code("LEDGER_INVALID", led.snapshot)

    def test_repair_06_unsafe_failure_revokes_switch(self):
        def fail(secret, body):
            raise RuntimeError("synthetic failure")
        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            switch = s.KillSwitch(True)
            with self.assertRaises(RuntimeError):
                s._execute_smoke_for_test(
                    preflight(), lease(), ledger=led,
                    secret_supplier=lambda: SECRET,
                    transport_fn=fail,
                    kill_switch=switch,
                )
            self.assertFalse(switch.allows_call())
            self.assertEqual(led.snapshot()["request_count"], 1)

    def test_repair_07_live_smoke_omits_undocumented_response_format(self):
        seen = []
        def checking_transport(secret, body):
            seen.append(copy.deepcopy(body))
            self.assertNotIn("response_format", body)
            return fake_transport(secret, body)

        with tempfile.TemporaryDirectory() as d:
            led = s.DurableCampaignLedger(Path(d)/"ledger.json", "campaign:test-v04")
            out = s._execute_smoke_for_test(
                preflight(), lease(), ledger=led,
                secret_supplier=lambda: SECRET,
                transport_fn=checking_transport,
            )
            self.assertEqual(out["status"], "SMOKE_PASS")
            self.assertEqual(len(seen), 3)

    def test_repair_08_manual_fake_fallback_retained(self):
        resume = (
            _V04_ROOT / "studio/memory/tasks/STUDIO-009V-04/RESUME.md"
        ).read_text(encoding="utf-8")
        self.assertIn("MANUAL/FAKE", resume)


class PoolsideV04AdditionalOfflineBoundaryTests(unittest.TestCase):
    def test_poolside_v04_policy_disables_pool_cli_and_acp(self):
        p = self._load(_V04_PROVIDER / "live-validation-policy.json") if hasattr(self, "_load") else None
        if p is None:
            with open(_V04_PROVIDER / "live-validation-policy.json", "r", encoding="utf-8") as h:
                p = _v04_json.load(h)
        self.assertFalse(p["pool_cli"])
        self.assertFalse(p["acp"])
        self.assertTrue(p["server_side_credential_revocation_required"])

    def test_poolside_v04_connected_placeholder_does_not_fabricate_entitlement_or_revocation(self):
        with open(_V04_EVIDENCE / "connected-validation.json", "r", encoding="utf-8") as h:
            record = _v04_json.load(h)
        self.assertFalse(record["zero_cost_eligibility_verified"])
        self.assertFalse(record["server_side_revocation_verified"])
        self.assertFalse(record["pool_cli_used"])

    def test_poolside_v04_no_subprocess_or_provider_sdk_in_live_modules(self):
        import scripts.poolside_live_transport as _t
        import scripts.poolside_live_smoke as _s
        import scripts.poolside_session_credential_bridge as _b
        self.assertNotIn("subprocess", _t.__dict__)
        self.assertNotIn("subprocess", _s.__dict__)
        self.assertNotIn("subprocess", _b.__dict__)
        self.assertNotIn("requests", _t.__dict__)
        self.assertNotIn("httpx", _t.__dict__)
