#!/usr/bin/env python3
"""Session-only Cloudflare Account ID + API-token bridge for STUDIO-009V-02.

Import is offline. This module never reads environment variables, dotenv files,
files, CLI arguments, browser stores, clipboard contents, keychains, or remote
secret stores. Real values can exist only inside an Owner-interactive call.
"""
from __future__ import annotations

import copy
import getpass
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from typing import Any, Callable

SCHEMA_VERSION = "1.0"
CREDENTIAL_PROFILE_ID = "credential-profile:cloudflare-workers-ai-api-token"
ACCOUNT_REF = "account-ref:cloudflare-workers-ai-owner-account"
SUBJECT_REF = "provider:cloudflare-workers-ai"
CAPABILITY = "MODEL_INFERENCE"
PURPOSE = "CLOUDFLARE_V02_CONNECTED_VALIDATION"

LEASE_ID_RE = re.compile(r"^credential-lease:[0-9a-f]{32}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
IDEMPOTENCY_RE = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
ACCOUNT_ID_RE = re.compile(r"^[0-9A-Fa-f]{32}$")

LEASE_FIELDS = {
    "schema_version", "credential_lease_id", "credential_profile_id",
    "profile_digest", "subject_ref", "capability", "purpose",
    "repository_record_digest", "operation_digest", "issued_at", "expires_at",
    "idempotency_key", "canonical_digest",
}

SAFE_MESSAGES = {
    "INVALID_LEASE": "Cloudflare credential lease metadata is invalid",
    "LEASE_LINEAGE": "credential lease lineage is not authorized for Cloudflare V-02",
    "LEASE_TIME": "Cloudflare credential lease is outside its accepted time window",
    "LEASE_DIGEST": "Cloudflare credential lease digest does not match",
    "INTERACTIVE_REQUIRED": "Owner-interactive Cloudflare account/token input is required",
    "INVALID_ACCOUNT": "Cloudflare Account ID input is invalid",
    "INVALID_SECRET": "Cloudflare session token input is invalid",
    "SECRET_ESCAPE": "Cloudflare account/token material escaped the trusted call boundary",
}

class CloudflareSessionCredentialError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "Cloudflare session credential bridge rejected input")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise CloudflareSessionCredentialError(code)

def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
        _fail("INVALID_LEASE")
    raise AssertionError("unreachable")

def canonical_digest(value: dict[str, Any]) -> str:
    material = copy.deepcopy(value)
    material.pop("canonical_digest", None)
    return "sha256:" + hashlib.sha256(canonical_json_bytes(material)).hexdigest()

def _utc(value: Any) -> datetime:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        _fail("INVALID_LEASE")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        _fail("INVALID_LEASE")
    raise AssertionError("unreachable")

def validate_lease(lease: dict[str, Any], *, as_of: str) -> dict[str, Any]:
    before = canonical_json_bytes(copy.deepcopy(lease))
    if not isinstance(lease, dict) or set(lease) != LEASE_FIELDS:
        _fail("INVALID_LEASE")
    if lease["schema_version"] != SCHEMA_VERSION:
        _fail("INVALID_LEASE")
    if not isinstance(lease["credential_lease_id"], str) or not LEASE_ID_RE.fullmatch(lease["credential_lease_id"]):
        _fail("INVALID_LEASE")
    if lease["credential_profile_id"] != CREDENTIAL_PROFILE_ID:
        _fail("LEASE_LINEAGE")
    if not isinstance(lease["profile_digest"], str) or not DIGEST_RE.fullmatch(lease["profile_digest"]):
        _fail("INVALID_LEASE")
    if lease["subject_ref"] != SUBJECT_REF or lease["capability"] != CAPABILITY or lease["purpose"] != PURPOSE:
        _fail("LEASE_LINEAGE")
    if lease["repository_record_digest"] is not None or lease["operation_digest"] is not None:
        _fail("LEASE_LINEAGE")
    if not isinstance(lease["idempotency_key"], str) or not IDEMPOTENCY_RE.fullmatch(lease["idempotency_key"]):
        _fail("INVALID_LEASE")
    issued = _utc(lease["issued_at"])
    expires = _utc(lease["expires_at"])
    observed = _utc(as_of)
    if not (issued <= observed < expires):
        _fail("LEASE_TIME")
    if not isinstance(lease["canonical_digest"], str) or not DIGEST_RE.fullmatch(lease["canonical_digest"]):
        _fail("INVALID_LEASE")
    if lease["canonical_digest"] != canonical_digest(lease):
        _fail("LEASE_DIGEST")
    if canonical_json_bytes(lease) != before:
        _fail("INVALID_LEASE")
    return {
        "credential_lease_id": lease["credential_lease_id"],
        "credential_profile_id": lease["credential_profile_id"],
        "profile_digest": lease["profile_digest"],
        "subject_ref": lease["subject_ref"],
        "capability": lease["capability"],
        "purpose": lease["purpose"],
        "issued_at": lease["issued_at"],
        "expires_at": lease["expires_at"],
        "canonical_digest": lease["canonical_digest"],
    }

def _validate_account_id(value: Any) -> str:
    if not isinstance(value, str) or not ACCOUNT_ID_RE.fullmatch(value):
        _fail("INVALID_ACCOUNT")
    return value

def _validate_secret(value: Any) -> str:
    if not isinstance(value, str) or not (16 <= len(value) <= 512):
        _fail("INVALID_SECRET")
    if any(ch.isspace() or ord(ch) < 32 for ch in value):
        _fail("INVALID_SECRET")
    return value

def _contains_material(value: Any, account_id: str, secret: str) -> bool:
    stack = [value]
    seen = 0
    while stack:
        item = stack.pop()
        seen += 1
        if seen > 10000:
            _fail("SECRET_ESCAPE")
        if isinstance(item, str) and (account_id in item or secret in item):
            return True
        if isinstance(item, dict):
            stack.extend(item.keys())
            stack.extend(item.values())
        elif isinstance(item, (list, tuple, set)):
            stack.extend(item)
    return False

def with_account_and_secret(
    lease: dict[str, Any],
    consumer: Callable[[str, str], Any],
    *,
    as_of: str,
    account_supplier: Callable[[], str] | None = None,
    secret_supplier: Callable[[], str] | None = None,
) -> Any:
    validate_lease(lease, as_of=as_of)
    if account_supplier is None or secret_supplier is None:
        if not sys.stdin.isatty():
            _fail("INTERACTIVE_REQUIRED")
    if account_supplier is None:
        account_supplier = lambda: getpass.getpass("Cloudflare Account ID (hidden, session only): ")
    if secret_supplier is None:
        secret_supplier = lambda: getpass.getpass("Cloudflare API token (hidden, session only): ")

    account_id = ""
    secret = ""
    try:
        account_id = _validate_account_id(account_supplier())
        secret = _validate_secret(secret_supplier())
        try:
            result = consumer(account_id, secret)
        except Exception as exc:
            text = str(exc)
            if (account_id and account_id in text) or (secret and secret in text):
                _fail("SECRET_ESCAPE")
            raise
        if _contains_material(result, account_id, secret):
            _fail("SECRET_ESCAPE")
        return result
    finally:
        account_id = ""
        secret = ""
