#!/usr/bin/env python3
"""Session-only secret bridge for STUDIO-009V-01.

This module never reads environment variables, dotenv files, keychains, browser
stores, files, CLI arguments, or remote secret stores. A real secret may exist
only in process memory during an Owner-interactive call boundary.
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
CREDENTIAL_PROFILE_ID = "credential-profile:groq-api-key"
SUBJECT_REF = "provider:groqcloud"
CAPABILITY = "MODEL_INFERENCE"
PURPOSE = "GROQ_V01_CONNECTED_VALIDATION"

LEASE_ID_RE = re.compile(r"^credential-lease:[0-9a-f]{32}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REF_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}:[A-Za-z0-9._/-]{1,160}$")
IDEMPOTENCY_RE = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

LEASE_FIELDS = {
    "schema_version", "credential_lease_id", "credential_profile_id",
    "profile_digest", "subject_ref", "capability", "purpose",
    "repository_record_digest", "operation_digest", "issued_at", "expires_at",
    "idempotency_key", "canonical_digest",
}

SAFE_MESSAGES = {
    "INVALID_LEASE": "credential lease metadata is invalid",
    "LEASE_LINEAGE": "credential lease lineage is not authorized for Groq V-01",
    "LEASE_TIME": "credential lease is outside its accepted time window",
    "LEASE_DIGEST": "credential lease digest does not match",
    "INTERACTIVE_REQUIRED": "Owner-interactive secret input is required",
    "INVALID_SECRET": "session secret input is invalid",
    "SECRET_ESCAPE": "session secret escaped the trusted call boundary",
}

class SessionCredentialError(ValueError):
    def __init__(self, code: str):
        self.code = code
        self.safe_message = SAFE_MESSAGES.get(code, "session credential bridge rejected input")
        super().__init__(self.safe_message)

def _fail(code: str) -> None:
    raise SessionCredentialError(code)

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

def _validate_secret(secret: Any) -> str:
    if not isinstance(secret, str) or not (16 <= len(secret) <= 512):
        _fail("INVALID_SECRET")
    if any(ch.isspace() or ord(ch) < 32 for ch in secret):
        _fail("INVALID_SECRET")
    return secret

def with_secret(
    lease: dict[str, Any],
    consumer: Callable[[str], Any],
    *,
    as_of: str,
    supplier: Callable[[], str] | None = None,
) -> Any:
    validate_lease(lease, as_of=as_of)
    if supplier is None:
        if not sys.stdin.isatty():
            _fail("INTERACTIVE_REQUIRED")
        supplier = lambda: getpass.getpass("Groq API key (hidden, session only): ")
    secret = ""
    try:
        secret = _validate_secret(supplier())
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
