#!/usr/bin/env python3
"""Bounded Poolside V-04 smoke orchestrator.

Import is offline. execute_smoke can issue at most three sequential requests
only after accepted Owner preflight, a dedicated session credential lease,
and durable request reservation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from scripts import poolside_live_transport as transport
from scripts import poolside_session_credential_bridge as bridge

V_CONTRACT_MERGE = "a7beb556d19da1397cceb09431d47848e69c5b12"
P04_CLOSEOUT_MERGE = "3726e2bd031ce2022f5a93ff1d40c404fb815682"
PROVIDER_PROFILE_ID = "provider-profile:poolside-direct-laguna-s-2.1"
PROVIDER_CHILD_ID = "STUDIO-009P-04"
MODEL_ID = "poolside/laguna-s-2.1"
HOST = "inference.poolside.ai"
ACCOUNT_REF = "account-ref:poolside-owner-account"

MAX_REQUESTS = 3
CONCURRENCY = 1
RETRY_COUNT = 0
MONEY_CEILING = 0

PREFLIGHT_FIELDS = {
    "v_contract_merge", "p04_closeout_merge", "provider_profile_id",
    "provider_child_id", "model", "host", "account_ref",
    "standalone_offer_confirmed", "account_zero_cost_confirmed",
    "no_billing_method_required_confirmed", "no_purchase_required_confirmed",
    "server_side_revocation_confirmed", "terms_data_policy_compatible_confirmed",
    "no_paid_path_confirmed", "money_ceiling", "max_requests",
    "concurrency", "retry_count", "kill_switch_armed", "as_of",
}

PROBES = (
    {
        "id": "STRUCTURED_OUTPUT",
        "estimated_input_tokens": 96,
        "messages": [{"role": "user", "content":
            'Synthetic validation. Return JSON only, exactly: {"status":"ok","value":7}'}],
        "expected": {"status": "ok", "value": 7},
    },
    {
        "id": "BOUNDED_REASONING",
        "estimated_input_tokens": 128,
        "messages": [{"role": "user", "content":
            'Synthetic validation. Return JSON only. For integers [3,1,2], return exactly: {"sorted":[1,2,3],"sum":6}'}],
        "expected": {"sorted": [1, 2, 3], "sum": 6},
    },
    {
        "id": "SYNTHETIC_CODE_REVIEW",
        "estimated_input_tokens": 192,
        "messages": [{"role": "user", "content":
            'Synthetic validation. A fictional function add(a,b) returns a-b. Return JSON only, exactly: {"bug":"uses subtraction","fix":"return a + b"}'}],
        "expected": {"bug": "uses subtraction", "fix": "return a + b"},
    },
)

SAFE_MESSAGES = {
    "INVALID_PREFLIGHT": "Poolside V-04 preflight metadata is invalid",
    "LINEAGE_MISMATCH": "Poolside V-04 lineage does not match accepted contract",
    "STANDALONE_OFFER_NOT_CONFIRMED": "Poolside standalone free-limited offer must be confirmed",
    "ZERO_COST_ELIGIBILITY_UNPROVEN": "Poolside account zero-cost eligibility must be confirmed",
    "BILLING_NOT_DENIED": "Poolside billing requirement must be explicitly denied",
    "PURCHASE_NOT_DENIED": "Poolside subscription/credit-purchase requirement must be explicitly denied",
    "CREDENTIAL_REVOCATION_UNPROVEN": "Poolside server-side key revocation/deletion/invalidation path must be confirmed",
    "TERMS_NOT_CONFIRMED": "Poolside Terms/data-policy compatibility must be confirmed",
    "PAID_PATH_NOT_DENIED": "Poolside paid path must be explicitly denied",
    "NONZERO_BUDGET": "Poolside V-04 requires zero monetary ceiling",
    "REQUEST_LIMIT": "Poolside V-04 request ceiling reached",
    "REQUEST_RESERVATION": "Poolside V-04 durable request reservation is required",
    "KILL_SWITCH": "Poolside V-04 kill switch blocks additional calls",
    "QUALITY_FAILED": "Poolside V-04 fixed smoke quality gate failed",
    "LEDGER_INVALID": "Poolside V-04 campaign ledger is invalid",
    "CAMPAIGN_ACTIVE": "Poolside V-04 campaign is already active",
    "PREFLIGHT_STALE": "Poolside V-04 connected preflight is stale or future-dated",
}

class PoolsideLiveSmokeError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "Poolside V-04 smoke rejected")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise PoolsideLiveSmokeError(code)

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

class KillSwitch:
    def __init__(self, armed: bool = True):
        self._armed = bool(armed)
    def revoke(self) -> None:
        self._armed = False
    def allows_call(self) -> bool:
        return self._armed

class CampaignExecutionLock:
    def __init__(self, ledger: "DurableCampaignLedger"):
        self.path = ledger.path.with_name(ledger.path.name + ".lock")
        self.campaign_id = ledger.campaign_id
        self._held = False

    def acquire(self) -> None:
        try:
            fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            _fail("CAMPAIGN_ACTIVE")
        try:
            payload = (self.campaign_id + "\n").encode("utf-8")
            os.write(fd, payload)
            os.fsync(fd)
        finally:
            os.close(fd)
        self._held = True

    def release(self) -> None:
        if not self._held:
            return
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        finally:
            self._held = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()
        return False

def validate_preflight(value: Any) -> dict[str, Any]:
    before = copy.deepcopy(value)
    if not isinstance(value, dict) or set(value) != PREFLIGHT_FIELDS:
        _fail("INVALID_PREFLIGHT")
    if (
        value["v_contract_merge"] != V_CONTRACT_MERGE
        or value["p04_closeout_merge"] != P04_CLOSEOUT_MERGE
        or value["provider_profile_id"] != PROVIDER_PROFILE_ID
        or value["provider_child_id"] != PROVIDER_CHILD_ID
        or value["model"] != MODEL_ID
        or value["host"] != HOST
        or value["account_ref"] != ACCOUNT_REF
    ):
        _fail("LINEAGE_MISMATCH")
    confirmations = (
        ("standalone_offer_confirmed", "STANDALONE_OFFER_NOT_CONFIRMED"),
        ("account_zero_cost_confirmed", "ZERO_COST_ELIGIBILITY_UNPROVEN"),
        ("no_billing_method_required_confirmed", "BILLING_NOT_DENIED"),
        ("no_purchase_required_confirmed", "PURCHASE_NOT_DENIED"),
        ("server_side_revocation_confirmed", "CREDENTIAL_REVOCATION_UNPROVEN"),
        ("terms_data_policy_compatible_confirmed", "TERMS_NOT_CONFIRMED"),
        ("no_paid_path_confirmed", "PAID_PATH_NOT_DENIED"),
    )
    for field, code in confirmations:
        if value[field] is not True:
            _fail(code)
    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if isinstance(value["max_requests"], bool) or value["max_requests"] != MAX_REQUESTS:
        _fail("REQUEST_LIMIT")
    if isinstance(value["concurrency"], bool) or value["concurrency"] != CONCURRENCY:
        _fail("INVALID_PREFLIGHT")
    if isinstance(value["retry_count"], bool) or value["retry_count"] != RETRY_COUNT:
        _fail("INVALID_PREFLIGHT")
    if value["kill_switch_armed"] is not True:
        _fail("KILL_SWITCH")
    if not isinstance(value["as_of"], str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value["as_of"]
    ):
        _fail("INVALID_PREFLIGHT")
    observed = datetime.strptime(value["as_of"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    age_seconds = (_utc_now() - observed).total_seconds()
    if age_seconds < -120 or age_seconds > 900:
        _fail("PREFLIGHT_STALE")
    if value != before:
        _fail("INVALID_PREFLIGHT")
    return copy.deepcopy(value)

class DurableCampaignLedger:
    def __init__(self, path: str | Path, campaign_id: str):
        self.path = Path(path)
        self.campaign_id = campaign_id
        if not isinstance(campaign_id, str) or not re.fullmatch(r"campaign:[a-z0-9._-]{3,96}", campaign_id):
            _fail("LEDGER_INVALID")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({
                "schema_version": "1.0",
                "campaign_id": campaign_id,
                "request_count": 0,
                "reservations": [],
                "money_ceiling": 0,
            })

    def _read(self) -> dict[str, Any]:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            _fail("LEDGER_INVALID")
        if (
            not isinstance(value, dict)
            or set(value) != {"schema_version", "campaign_id", "request_count", "reservations", "money_ceiling"}
            or value.get("schema_version") != "1.0"
            or value.get("campaign_id") != self.campaign_id
            or value.get("money_ceiling") != 0
            or not isinstance(value.get("request_count"), int)
            or isinstance(value.get("request_count"), bool)
            or not isinstance(value.get("reservations"), list)
        ):
            _fail("LEDGER_INVALID")
        count = value["request_count"]
        reservations = value["reservations"]
        if count < 0 or count > MAX_REQUESTS or len(reservations) != count:
            _fail("LEDGER_INVALID")
        for ordinal, record in enumerate(reservations, start=1):
            if (
                not isinstance(record, dict)
                or set(record) != {"request_ordinal", "probe_id", "reserved_before_network"}
                or record.get("request_ordinal") != ordinal
                or record.get("reserved_before_network") is not True
                or not isinstance(record.get("probe_id"), str)
                or not re.fullmatch(r"[A-Z0-9_]{3,64}", record["probe_id"])
            ):
                _fail("LEDGER_INVALID")
        return value

    def _write(self, value: dict[str, Any]) -> None:
        raw = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
        fd, temp_name = tempfile.mkstemp(prefix=".v04-ledger-", dir=str(self.path.parent))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self.path)
        except Exception:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise

    def reserve(self, probe_id: str, expected_ordinal: int) -> dict[str, Any]:
        value = self._read()
        if value["request_count"] >= MAX_REQUESTS:
            _fail("REQUEST_LIMIT")
        if expected_ordinal != value["request_count"] + 1:
            _fail("REQUEST_RESERVATION")
        if not isinstance(probe_id, str) or not re.fullmatch(r"[A-Z0-9_]{3,64}", probe_id):
            _fail("REQUEST_RESERVATION")
        value["request_count"] = expected_ordinal
        value["reservations"].append({
            "request_ordinal": expected_ordinal,
            "probe_id": probe_id,
            "reserved_before_network": True,
        })
        self._write(value)
        return {
            "request_ordinal": expected_ordinal,
            "reserved_before_network": True,
            "ledger_campaign_id": self.campaign_id,
        }

    def snapshot(self) -> dict[str, Any]:
        return copy.deepcopy(self._read())

def _strict_json_object(content: Any) -> dict[str, Any]:
    if not isinstance(content, str):
        _fail("QUALITY_FAILED")
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                _fail("QUALITY_FAILED")
            result[key] = value
        return result
    try:
        value = json.loads(
            content,
            object_pairs_hook=hook,
            parse_constant=lambda _: _fail("QUALITY_FAILED"),
        )
    except PoolsideLiveSmokeError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError):
        _fail("QUALITY_FAILED")
    if not isinstance(value, dict):
        _fail("QUALITY_FAILED")
    return value

def _evaluate(probe: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    content = result.get("content")
    if _strict_json_object(content) != probe["expected"]:
        _fail("QUALITY_FAILED")
    if result.get("model_identity_verified") is not True or result.get("transport_identity_verified") is not True:
        _fail("QUALITY_FAILED")
    return {
        "probe_id": probe["id"],
        "quality": "PASS",
        "content_sha256": "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "model": result.get("model"),
        "finish_reason": result.get("finish_reason"),
        "usage": copy.deepcopy(result.get("usage", {})),
        "model_identity_verified": True,
        "transport_identity_verified": True,
    }

def _execute_smoke_core(
    preflight: dict[str, Any],
    lease: dict[str, Any],
    *,
    ledger: DurableCampaignLedger,
    transport_fn,
    kill_switch: KillSwitch | None,
    secret_runner,
    secret_supplier=None,
) -> dict[str, Any]:
    accepted = validate_preflight(preflight)
    if not isinstance(ledger, DurableCampaignLedger):
        _fail("REQUEST_RESERVATION")
    switch = kill_switch or KillSwitch(True)
    if not switch.allows_call():
        _fail("KILL_SWITCH")
    request_count = 0

    def consume(secret: str):
        nonlocal request_count
        records = []
        for probe in PROBES:
            if not switch.allows_call():
                _fail("KILL_SWITCH")
            if request_count >= MAX_REQUESTS:
                _fail("REQUEST_LIMIT")
            expected = request_count + 1
            reservation = ledger.reserve(probe["id"], expected)
            if reservation != {
                "request_ordinal": expected,
                "reserved_before_network": True,
                "ledger_campaign_id": ledger.campaign_id,
            }:
                _fail("REQUEST_RESERVATION")
            request_count = expected
            body = transport.build_request(
                copy.deepcopy(probe["messages"]),
                estimated_input_tokens=probe["estimated_input_tokens"],
                max_tokens=128,
            )
            result = transport_fn(secret, body)
            records.append(_evaluate(probe, result))
        return {
            "status": "SMOKE_PASS",
            "provider_profile_id": PROVIDER_PROFILE_ID,
            "provider_child_id": PROVIDER_CHILD_ID,
            "model": MODEL_ID,
            "host": HOST,
            "account_ref": ACCOUNT_REF,
            "request_count": request_count,
            "concurrency": CONCURRENCY,
            "retry_count": RETRY_COUNT,
            "money_ceiling": MONEY_CEILING,
            "observed_spend": None,
            "post_smoke_spend_confirmation_required": True,
            "credential_revocation_required": True,
            "quality_pass": True,
            "human_correction_count": 0,
            "records": records,
            "ledger": ledger.snapshot(),
        }

    with CampaignExecutionLock(ledger):
        try:
            if secret_supplier is None:
                return secret_runner(lease, consume, as_of=accepted["as_of"])
            return secret_runner(
                lease,
                consume,
                as_of=accepted["as_of"],
                secret_supplier=secret_supplier,
            )
        except Exception:
            switch.revoke()
            raise

def execute_smoke(
    preflight: dict[str, Any],
    lease: dict[str, Any],
    *,
    ledger: DurableCampaignLedger,
    kill_switch: KillSwitch | None = None,
) -> dict[str, Any]:
    return _execute_smoke_core(
        preflight,
        lease,
        ledger=ledger,
        transport_fn=transport.perform_request,
        kill_switch=kill_switch,
        secret_runner=bridge.with_secret,
    )

def _execute_smoke_for_test(
    preflight: dict[str, Any],
    lease: dict[str, Any],
    *,
    ledger: DurableCampaignLedger,
    secret_supplier,
    transport_fn=transport.perform_request,
    kill_switch: KillSwitch | None = None,
) -> dict[str, Any]:
    return _execute_smoke_core(
        preflight,
        lease,
        ledger=ledger,
        transport_fn=transport_fn,
        kill_switch=kill_switch,
        secret_runner=bridge._with_secret_for_test,
        secret_supplier=secret_supplier,
    )
