#!/usr/bin/env python3
"""Bounded Cloudflare Workers AI V-02 smoke orchestrator.

Import is offline. execute_smoke can issue at most three sequential requests only
after accepted Owner preflight, a Cloudflare-specific lease, hidden account/token
suppliers, and durable request/neuron reservations.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Callable

from scripts import cloudflare_live_transport as transport
from scripts import cloudflare_session_credential_bridge as bridge

V_CONTRACT_MERGE = "2f9eeaf6b2bb56546155e3d962082bc20525a8cb"
V_SCOPE_CORRECTION_MERGE = "2dc93b84951999cce22c5c5a6c9e956e722f3c18"
P02_CLOSEOUT_MERGE = "3cf7165c3263f8595b66a0d029b96022840adef3"
R01_CLOSEOUT_MERGE = "11c2c2d4a35f37c5712376a3e7b16ca22d848bc7"

PROVIDER_PROFILE_ID = "provider-profile:cloudflare-workers-ai-free-nemotron-3-super"
PROVIDER_CHILD_ID = "STUDIO-009P-02"
MODEL_ID = "@cf/nvidia/nemotron-3-120b-a12b"
HOST = "api.cloudflare.com"
ACCOUNT_REF = "account-ref:cloudflare-workers-ai-owner-account"

MAX_REQUESTS = 3
CONCURRENCY = 1
RETRY_COUNT = 0
MONEY_CEILING = 0
CAMPAIGN_NEURON_CEILING = 2000
RESERVED_NEURONS_PER_REQUEST = 512

PREFLIGHT_FIELDS = {
    "v_contract_merge", "v_scope_correction_merge", "p02_closeout_merge", "r01_closeout_merge",
    "provider_profile_id", "provider_child_id", "model", "host", "account_ref",
    "workers_free_confirmed", "model_free_eligible_confirmed", "neuron_headroom_confirmed",
    "token_permissions_confirmed", "no_paid_path_confirmed", "money_ceiling",
    "max_requests", "concurrency", "retry_count", "campaign_neuron_ceiling",
    "kill_switch_armed", "as_of",
}

PROBES = (
    {
        "id": "STRUCTURED_OUTPUT",
        "messages": [{"role": "user", "content": 'This is a synthetic validation. Return JSON only. Return exactly this JSON object: {"status":"ok","value":7}'}],
        "expected": {"status": "ok", "value": 7},
    },
    {
        "id": "INSTRUCTION_DISCIPLINE",
        "messages": [{"role": "user", "content": 'This is a synthetic validation. Return JSON only. Return exactly this JSON object: {"decision":"ALLOW","reasons":["synthetic"]}'}],
        "expected": {"decision": "ALLOW", "reasons": ["synthetic"]},
    },
    {
        "id": "SYNTHETIC_TRANSFORM",
        "messages": [{"role": "user", "content": 'This is a synthetic validation. Return JSON only. For synthetic items ["beta","alpha","beta"], return exactly {"unique_sorted":["alpha","beta"],"count":2}'}],
        "expected": {"unique_sorted": ["alpha", "beta"], "count": 2},
    },
)

SAFE_MESSAGES = {
    "INVALID_PREFLIGHT": "Cloudflare V-02 preflight metadata is invalid",
    "LINEAGE_MISMATCH": "Cloudflare V-02 lineage does not match accepted contract",
    "FREE_TIER_NOT_CONFIRMED": "Cloudflare Workers Free eligibility must be confirmed",
    "MODEL_FREE_NOT_CONFIRMED": "Cloudflare model free eligibility must be confirmed",
    "NEURON_HEADROOM_NOT_CONFIRMED": "Cloudflare free-neuron headroom must be confirmed",
    "TOKEN_PERMISSIONS_NOT_CONFIRMED": "Cloudflare API token permissions must be confirmed",
    "PAID_PATH_NOT_DENIED": "Cloudflare paid paths must be explicitly denied",
    "NONZERO_BUDGET": "Cloudflare V-02 requires zero monetary ceiling",
    "REQUEST_LIMIT": "Cloudflare V-02 request ceiling reached",
    "REQUEST_RESERVATION": "Cloudflare V-02 durable request/neuron reservation is required",
    "NEURON_LIMIT": "Cloudflare V-02 campaign neuron ceiling would be exceeded",
    "KILL_SWITCH": "Cloudflare V-02 kill switch blocks additional calls",
    "QUALITY_FAILED": "Cloudflare V-02 fixed smoke quality gate failed",
}

class CloudflareSmokeError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "Cloudflare V-02 smoke rejected")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise CloudflareSmokeError(code)

class KillSwitch:
    def __init__(self, armed: bool = True):
        self._armed = bool(armed)
    def revoke(self) -> None:
        self._armed = False
    def allows_call(self) -> bool:
        return self._armed

def validate_preflight(value):
    before = copy.deepcopy(value)
    if not isinstance(value, dict) or set(value) != PREFLIGHT_FIELDS:
        _fail("INVALID_PREFLIGHT")
    if (
        value["v_contract_merge"] != V_CONTRACT_MERGE
        or value["v_scope_correction_merge"] != V_SCOPE_CORRECTION_MERGE
        or value["p02_closeout_merge"] != P02_CLOSEOUT_MERGE
        or value["r01_closeout_merge"] != R01_CLOSEOUT_MERGE
        or value["provider_profile_id"] != PROVIDER_PROFILE_ID
        or value["provider_child_id"] != PROVIDER_CHILD_ID
        or value["model"] != MODEL_ID
        or value["host"] != HOST
        or value["account_ref"] != ACCOUNT_REF
    ):
        _fail("LINEAGE_MISMATCH")
    if value["workers_free_confirmed"] is not True:
        _fail("FREE_TIER_NOT_CONFIRMED")
    if value["model_free_eligible_confirmed"] is not True:
        _fail("MODEL_FREE_NOT_CONFIRMED")
    if value["neuron_headroom_confirmed"] is not True:
        _fail("NEURON_HEADROOM_NOT_CONFIRMED")
    if value["token_permissions_confirmed"] is not True:
        _fail("TOKEN_PERMISSIONS_NOT_CONFIRMED")
    if value["no_paid_path_confirmed"] is not True:
        _fail("PAID_PATH_NOT_DENIED")
    if isinstance(value["money_ceiling"], bool) or value["money_ceiling"] != 0:
        _fail("NONZERO_BUDGET")
    if isinstance(value["max_requests"], bool) or value["max_requests"] != MAX_REQUESTS:
        _fail("REQUEST_LIMIT")
    if isinstance(value["concurrency"], bool) or value["concurrency"] != CONCURRENCY:
        _fail("INVALID_PREFLIGHT")
    if isinstance(value["retry_count"], bool) or value["retry_count"] != RETRY_COUNT:
        _fail("INVALID_PREFLIGHT")
    if isinstance(value["campaign_neuron_ceiling"], bool) or value["campaign_neuron_ceiling"] != CAMPAIGN_NEURON_CEILING:
        _fail("NEURON_LIMIT")
    if value["kill_switch_armed"] is not True:
        _fail("KILL_SWITCH")
    if not isinstance(value["as_of"], str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value["as_of"]
    ):
        _fail("INVALID_PREFLIGHT")
    if value != before:
        _fail("INVALID_PREFLIGHT")
    return copy.deepcopy(value)

def _strict_json_object(content):
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                _fail("QUALITY_FAILED")
            result[key] = value
        return result
    try:
        value = json.loads(content, object_pairs_hook=hook, parse_constant=lambda _: _fail("QUALITY_FAILED"))
    except CloudflareSmokeError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError):
        _fail("QUALITY_FAILED")
    if not isinstance(value, dict):
        _fail("QUALITY_FAILED")
    return value

def _evaluate(probe, result):
    content = result.get("content")
    if not isinstance(content, str):
        _fail("QUALITY_FAILED")
    if _strict_json_object(content) != probe["expected"]:
        _fail("QUALITY_FAILED")
    estimated = result.get("estimated_neurons")
    if estimated is not None:
        if isinstance(estimated, bool) or not isinstance(estimated, int) or estimated < 0:
            _fail("NEURON_LIMIT")
        if estimated > RESERVED_NEURONS_PER_REQUEST:
            _fail("NEURON_LIMIT")
    digest = "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "probe_id": probe["id"],
        "quality": "PASS",
        "content_sha256": digest,
        "model": result.get("model"),
        "finish_reason": result.get("finish_reason"),
        "usage": copy.deepcopy(result.get("usage", {})),
        "estimated_neurons": estimated,
        "model_identity_verified": result.get("model_identity_verified") is True,
        "transport_identity_verified": result.get("transport_identity_verified") is True,
        "account_identity_verified": result.get("account_identity_verified") is True,
    }

def execute_smoke(
    preflight,
    lease,
    *,
    account_supplier,
    secret_supplier,
    reservation_fn=None,
    transport_fn=transport.perform_request,
    kill_switch=None,
):
    accepted = validate_preflight(preflight)
    switch = kill_switch or KillSwitch(True)
    if not switch.allows_call():
        _fail("KILL_SWITCH")
    request_count = 0
    reserved_neurons = 0

    def consume(account_id, secret):
        nonlocal request_count, reserved_neurons
        records = []
        for probe in PROBES:
            if not switch.allows_call():
                _fail("KILL_SWITCH")
            if request_count >= MAX_REQUESTS:
                _fail("REQUEST_LIMIT")
            if reservation_fn is None:
                _fail("REQUEST_RESERVATION")
            expected_number = request_count + 1
            expected_cumulative = reserved_neurons + RESERVED_NEURONS_PER_REQUEST
            if expected_cumulative > CAMPAIGN_NEURON_CEILING:
                _fail("NEURON_LIMIT")
            reservation = reservation_fn(probe["id"], expected_number, RESERVED_NEURONS_PER_REQUEST)
            if not isinstance(reservation, dict) or set(reservation) != {
                "request_ordinal", "cumulative_reserved_neurons"
            }:
                _fail("REQUEST_RESERVATION")
            if (
                isinstance(reservation["request_ordinal"], bool)
                or reservation["request_ordinal"] != expected_number
                or isinstance(reservation["cumulative_reserved_neurons"], bool)
                or reservation["cumulative_reserved_neurons"] != expected_cumulative
            ):
                _fail("REQUEST_RESERVATION")
            request_count = reservation["request_ordinal"]
            reserved_neurons = reservation["cumulative_reserved_neurons"]
            body = transport.build_request(
                copy.deepcopy(probe["messages"]),
                max_completion_tokens=256,
                response_format={"type": "json_object"},
            )
            result = transport_fn(account_id, secret, body)
            records.append(_evaluate(probe, result))

        return {
            "status": "SMOKE_PASS",
            "provider_profile_id": PROVIDER_PROFILE_ID,
            "provider_child_id": PROVIDER_CHILD_ID,
            "model": MODEL_ID,
            "host": HOST,
            "account_ref": ACCOUNT_REF,
            "request_count": request_count,
            "reserved_neurons": reserved_neurons,
            "campaign_neuron_ceiling": CAMPAIGN_NEURON_CEILING,
            "concurrency": CONCURRENCY,
            "retry_count": RETRY_COUNT,
            "money_ceiling": MONEY_CEILING,
            "observed_neurons": None,
            "observed_spend": None,
            "post_smoke_neuron_confirmation_required": True,
            "post_smoke_spend_confirmation_required": True,
            "quality_pass": True,
            "human_correction_count": 0,
            "records": records,
        }

    return bridge.with_account_and_secret(
        lease, consume, as_of=accepted["as_of"],
        account_supplier=account_supplier, secret_supplier=secret_supplier,
    )
