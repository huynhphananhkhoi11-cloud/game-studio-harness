#!/usr/bin/env python3
"""Bounded Groq V-01 smoke orchestrator.

Importing this module is offline. execute_smoke performs at most three sequential
requests only when explicitly called with accepted preflight metadata, an active
session lease, and a secret supplier.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Callable

from scripts import groq_live_transport as transport
from scripts import session_credential_bridge as bridge

V_CONTRACT_MERGE = "2b811d7ac64e88c396f691cec940ec68784b1457"
P01_CLOSEOUT_MERGE = "1b75f250169ccdab3e2d67cbac4047253792c4a7"
R01_CLOSEOUT_MERGE = "11c2c2d4a35f37c5712376a3e7b16ca22d848bc7"
PROVIDER_PROFILE_ID = "provider-profile:groq-free-gpt-oss-120b"
PROVIDER_CHILD_ID = "STUDIO-009P-01"
MODEL_ID = "openai/gpt-oss-120b"
HOST = "api.groq.com"

MAX_REQUESTS = 3
CONCURRENCY = 1
RETRY_COUNT = 0
MONEY_CEILING = 0

PREFLIGHT_FIELDS = {
    "v_contract_merge", "p01_closeout_merge", "r01_closeout_merge",
    "provider_profile_id", "provider_child_id", "model", "host",
    "free_tier_confirmed", "zdr_confirmed", "model_permission_confirmed", "money_ceiling",
    "max_requests", "concurrency", "retry_count", "kill_switch_armed", "as_of",
}

PROBES = (
    {
        "id": "STRUCTURED_OUTPUT",
        "messages": [
            {"role": "user", "content": 'This is a synthetic validation. Return JSON only. Return exactly this JSON object: {"status":"ok","value":7}'},
        ],
        "expected": {"status": "ok", "value": 7},
    },
    {
        "id": "INSTRUCTION_DISCIPLINE",
        "messages": [
            {"role": "user", "content": 'This is a synthetic validation. Return JSON only. Return exactly this JSON object: {"decision":"ALLOW","reasons":["synthetic"]}'},
        ],
        "expected": {"decision": "ALLOW", "reasons": ["synthetic"]},
    },
    {
        "id": "SYNTHETIC_TRANSFORM",
        "messages": [
            {"role": "user", "content": 'This is a synthetic validation. Return JSON only. For synthetic items ["beta","alpha","beta"], return exactly {"unique_sorted":["alpha","beta"],"count":2}'},
        ],
        "expected": {"unique_sorted": ["alpha", "beta"], "count": 2},
    },
)

SAFE_MESSAGES = {
    "INVALID_PREFLIGHT": "Groq V-01 preflight metadata is invalid",
    "TIER_NOT_CONFIRMED": "Groq Free tier must be confirmed before connected validation",
    "ZDR_NOT_CONFIRMED": "Groq ZDR must be confirmed before connected validation",
    "MODEL_PERMISSION_NOT_CONFIRMED": "Groq GPT-OSS 120B model permission must be confirmed before connected validation",
    "REQUEST_RESERVATION": "Groq V-01 durable request reservation is required before every network call",
    "NONZERO_BUDGET": "Groq V-01 requires zero monetary ceiling",
    "LINEAGE_MISMATCH": "Groq V-01 lineage does not match accepted contract",
    "KILL_SWITCH": "Groq V-01 kill switch blocks additional calls",
    "REQUEST_LIMIT": "Groq V-01 request ceiling reached",
    "QUALITY_FAILED": "Groq V-01 fixed smoke quality gate failed",
}

class GroqSmokeError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "Groq V-01 smoke rejected")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise GroqSmokeError(code)

class KillSwitch:
    def __init__(self, armed: bool = True):
        self._armed = bool(armed)
    def revoke(self) -> None:
        self._armed = False
    def allows_call(self) -> bool:
        return self._armed

def validate_preflight(value: dict[str, Any]) -> dict[str, Any]:
    before = copy.deepcopy(value)
    if not isinstance(value, dict) or set(value) != PREFLIGHT_FIELDS:
        _fail("INVALID_PREFLIGHT")
    if (
        value["v_contract_merge"] != V_CONTRACT_MERGE
        or value["p01_closeout_merge"] != P01_CLOSEOUT_MERGE
        or value["r01_closeout_merge"] != R01_CLOSEOUT_MERGE
        or value["provider_profile_id"] != PROVIDER_PROFILE_ID
        or value["provider_child_id"] != PROVIDER_CHILD_ID
        or value["model"] != MODEL_ID
        or value["host"] != HOST
    ):
        _fail("LINEAGE_MISMATCH")
    if value["free_tier_confirmed"] is not True:
        _fail("TIER_NOT_CONFIRMED")
    if value["zdr_confirmed"] is not True:
        _fail("ZDR_NOT_CONFIRMED")
    if value["model_permission_confirmed"] is not True:
        _fail("MODEL_PERMISSION_NOT_CONFIRMED")
    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if value["max_requests"] != 3 or isinstance(value["max_requests"], bool):
        _fail("REQUEST_LIMIT")
    if value["concurrency"] != 1 or isinstance(value["concurrency"], bool):
        _fail("INVALID_PREFLIGHT")
    if value["retry_count"] != 0 or isinstance(value["retry_count"], bool):
        _fail("INVALID_PREFLIGHT")
    if value["kill_switch_armed"] is not True:
        _fail("KILL_SWITCH")
    if not isinstance(value["as_of"], str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value["as_of"]
    ):
        _fail("INVALID_PREFLIGHT")
    if value != before:
        _fail("INVALID_PREFLIGHT")
    return copy.deepcopy(value)

def _evaluate(probe: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    content = result.get("content")
    if not isinstance(content, str):
        _fail("QUALITY_FAILED")
    try:
        parsed = json.loads(content)
    except (json.JSONDecodeError, TypeError, ValueError):
        _fail("QUALITY_FAILED")
    if parsed != probe["expected"]:
        _fail("QUALITY_FAILED")
    digest = "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "probe_id": probe["id"],
        "quality": "PASS",
        "content_sha256": digest,
        "model": result.get("model"),
        "service_tier": result.get("service_tier"),
        "finish_reason": result.get("finish_reason"),
        "usage": copy.deepcopy(result.get("usage", {})),
        "quota": copy.deepcopy(result.get("quota", {})),
        "model_identity_verified": result.get("model_identity_verified") is True,
        "transport_identity_verified": result.get("transport_identity_verified") is True,
    }

def execute_smoke(
    preflight: dict[str, Any],
    lease: dict[str, Any],
    *,
    supplier: Callable[[], str],
    request_reserver: Callable[[str, int], int] | None = None,
    transport_fn: Callable[[str, dict[str, Any]], dict[str, Any]] = transport.perform_request,
    kill_switch: KillSwitch | None = None,
) -> dict[str, Any]:
    accepted = validate_preflight(preflight)
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
            body = transport.build_request(
                copy.deepcopy(probe["messages"]),
                max_completion_tokens=256,
                response_format={"type": "json_object"},
            )
            if request_reserver is None:
                _fail("REQUEST_RESERVATION")
            expected_number = request_count + 1
            reserved_number = request_reserver(probe["id"], expected_number)
            if isinstance(reserved_number, bool) or reserved_number != expected_number:
                _fail("REQUEST_RESERVATION")
            request_count = reserved_number
            result = transport_fn(secret, body)
            records.append(_evaluate(probe, result))
        return {
            "status": "SMOKE_PASS",
            "provider_profile_id": PROVIDER_PROFILE_ID,
            "provider_child_id": PROVIDER_CHILD_ID,
            "model": MODEL_ID,
            "host": HOST,
            "request_count": request_count,
            "concurrency": 1,
            "retry_count": 0,
            "money_ceiling": 0,
            "observed_spend": None,
            "post_smoke_spend_confirmation_required": True,
            "quality_pass": True,
            "human_correction_count": 0,
            "records": records,
        }

    return bridge.with_secret(
        lease, consume, as_of=accepted["as_of"], supplier=supplier
    )
