#!/usr/bin/env python3
"""Session-only NVIDIA NIM credential bridge for STUDIO-009V-03.

Import is offline. This module never reads environment variables, dotenv files,
files, CLI arguments, browser stores, clipboard contents, keychains, or remote
secret stores. A real key can exist only inside an Owner-interactive call.
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
CREDENTIAL_PROFILE_ID = "credential-profile:nvidia-nim-api-key"
ACCOUNT_REF = "account-ref:nvidia-developer-program-owner-account"
SUBJECT_REF = "provider:nvidia-nim"
CAPABILITY = "MODEL_INFERENCE"
PURPOSE = "NVIDIA_V03_CONNECTED_VALIDATION"

LEASE_ID_RE = re.compile(r"^credential-lease:[0-9a-f]{32}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
IDEMPOTENCY_RE = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

LEASE_FIELDS = {
    "schema_version", "credential_lease_id", "credential_profile_id",
    "account_ref", "profile_digest", "subject_ref", "capability", "purpose",
    "repository_record_digest", "operation_digest", "issued_at", "expires_at",
    "idempotency_key", "canonical_digest",
}

SAFE_MESSAGES = {
    "INVALID_LEASE": "NVIDIA V-03 credential lease metadata is invalid",
    "LEASE_LINEAGE": "credential lease lineage is not authorized for NVIDIA V-03",
    "LEASE_TIME": "NVIDIA V-03 credential lease is outside its accepted time window",
    "LEASE_DIGEST": "NVIDIA V-03 credential lease digest does not match",
    "INTERACTIVE_REQUIRED": "Owner-interactive NVIDIA key input is required",
    "INVALID_SECRET": "NVIDIA V-03 session credential is invalid",
    "SECRET_ESCAPE": "NVIDIA credential material escaped the trusted call boundary",
    "TEST_SECRET_REQUIRED": "deterministic tests require an explicitly synthetic credential supplier",
}

class NvidiaSessionCredentialError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "NVIDIA session credential bridge rejected input")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise NvidiaSessionCredentialError(code)

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
    if lease["credential_profile_id"] != CREDENTIAL_PROFILE_ID or lease["account_ref"] != ACCOUNT_REF:
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
        "account_ref": lease["account_ref"],
        "subject_ref": lease["subject_ref"],
        "capability": lease["capability"],
        "purpose": lease["purpose"],
        "issued_at": lease["issued_at"],
        "expires_at": lease["expires_at"],
        "canonical_digest": lease["canonical_digest"],
    }

def _validate_secret(value: Any) -> str:
    if not isinstance(value, str) or not (16 <= len(value) <= 512):
        _fail("INVALID_SECRET")
    if any(ch.isspace() or ord(ch) < 32 for ch in value):
        _fail("INVALID_SECRET")
    return value

def _contains_secret(value: Any, secret: str) -> bool:
    stack = [value]
    seen = 0
    while stack:
        item = stack.pop()
        seen += 1
        if seen > 10000:
            _fail("SECRET_ESCAPE")
        if isinstance(item, str) and secret in item:
            return True
        if isinstance(item, dict):
            stack.extend(item.keys())
            stack.extend(item.values())
        elif isinstance(item, (list, tuple, set)):
            stack.extend(item)
    return False

def _consume_secret(
    lease: dict[str, Any],
    consumer: Callable[[str], Any],
    *,
    as_of: str,
    secret_supplier: Callable[[], str],
) -> Any:
    validate_lease(lease, as_of=as_of)
    secret = ""
    try:
        secret = _validate_secret(secret_supplier())
        try:
            result = consumer(secret)
        except Exception as exc:
            if secret and secret in str(exc):
                _fail("SECRET_ESCAPE")
            raise
        if _contains_secret(result, secret):
            _fail("SECRET_ESCAPE")
        return result
    finally:
        secret = ""

def with_secret(
    lease: dict[str, Any],
    consumer: Callable[[str], Any],
    *,
    as_of: str,
) -> Any:
    if not sys.stdin.isatty():
        _fail("INTERACTIVE_REQUIRED")
    return _consume_secret(
        lease,
        consumer,
        as_of=as_of,
        secret_supplier=lambda: getpass.getpass("NVIDIA API key (hidden, session only): "),
    )

def _with_secret_for_test(
    lease: dict[str, Any],
    consumer: Callable[[str], Any],
    *,
    as_of: str,
    secret_supplier: Callable[[], str],
) -> Any:
    def synthetic_supplier() -> str:
        value = _validate_secret(secret_supplier())
        if not value.startswith("synthetic_"):
            _fail("TEST_SECRET_REQUIRED")
        return value

    return _consume_secret(
        lease,
        consumer,
        as_of=as_of,
        secret_supplier=synthetic_supplier,
    )
