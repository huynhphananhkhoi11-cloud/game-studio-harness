#!/usr/bin/env python3
"""Deterministic secret-like text redaction for STUDIO-009C.

No credential source, environment, keyring, filesystem store, network, clock,
provider, or subprocess integration is present in this module.
"""

from __future__ import annotations

import re
from typing import Any

REDACTED = "[REDACTED]"
MAX_REDACTION_CHARS = 4096
MAX_REDACTION_ITEMS = 4096

_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.I | re.S),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|token|password|passwd|secret)\s*[:=]\s*[^\s,;]{6,}"),
    re.compile(r"https?://[^/@\s]+:[^/@\s]+@"),
)

SAFE_MESSAGES = {
    "EXTRA_FIELD": "input contains unknown fields",
    "MISSING_FIELD": "input is missing required fields",
    "INVALID_TYPE": "input has an invalid type",
    "INVALID_FORMAT": "input has invalid format",
    "INVALID_ENUM": "input contains an unsupported value",
    "INVALID_TIME": "input contains invalid chronology",
    "FUTURE_EVIDENCE": "evidence is later than the caller-supplied time",
    "EXPIRED_PROFILE": "credential profile is expired",
    "PROFILE_NOT_ACTIVE": "credential profile is not active",
    "ROTATION_REQUIRED": "credential profile requires rotation",
    "REVOKED_PROFILE": "credential profile is revoked",
    "OWNER_APPROVAL_REQUIRED": "Owner approval evidence is required",
    "SCOPE_BROADENING": "requested credential scope exceeds approved scope",
    "WRITE_EVIDENCE_REQUIRED": "write-capable credential use requires writer and worktree evidence",
    "NONZERO_BUDGET": "credential use requires a zero monetary ceiling",
    "LEASE_LIMIT": "requested credential lease exceeds the accepted duration",
    "REPLAY": "credential request replay evidence is invalid",
    "IDEMPOTENCY_CONFLICT": "idempotency key conflicts with prior credential request",
    "DIGEST_FORMAT": "canonical digest has invalid format",
    "DIGEST_MISMATCH": "canonical digest does not match",
    "LINEAGE_MISMATCH": "credential lineage does not match accepted evidence",
    "SECRET_MATERIAL": "secret material is forbidden in this interface",
    "INPUT_ENCODING": "input contains invalid Unicode",
    "INPUT_NUMBER": "non-finite numbers are forbidden",
    "INPUT_SIZE": "input exceeds the accepted byte limit",
    "STRUCTURE_LIMIT": "input structure exceeds validation limits",
    "DUPLICATE_JSON_KEY": "JSON contains duplicate object keys",
    "INPUT_MUTATION": "validator input was mutated",
    "STORE_UNAVAILABLE": "credential store entry is unavailable",
    "PROVIDER_NOT_AUTHORIZED": "provider credential use is not authorized in STUDIO-009C",
    "LIFECYCLE_CONFLICT": "credential lifecycle transition is not allowed",
}


class SafeCredentialError(ValueError):
    """Stable public error that never includes untrusted or secret-bearing input."""

    def __init__(self, code: str) -> None:
        message = SAFE_MESSAGES.get(code, "credential operation rejected")
        super().__init__(message)
        self.code = code
        self.safe_message = message


def safe_error(code: str) -> SafeCredentialError:
    return SafeCredentialError(code)


def contains_secret_like(text: Any) -> bool:
    """Return True only for bounded text matching secret-like patterns."""
    if not isinstance(text, str):
        return False
    candidate = text[:MAX_REDACTION_CHARS]
    return any(pattern.search(candidate) for pattern in _SECRET_PATTERNS)


def redact_text(text: Any) -> str:
    """Redact secret-like substrings from bounded public diagnostic text."""
    if not isinstance(text, str):
        return REDACTED
    candidate = text[:MAX_REDACTION_CHARS]
    for pattern in _SECRET_PATTERNS:
        candidate = pattern.sub(REDACTED, candidate)
    return candidate


def assert_public_safe(value: Any) -> None:
    """Boundedly prove that public result data contains no obvious secret-like text."""
    stack = [value]
    observed = 0
    while stack:
        item = stack.pop()
        observed += 1
        if observed > MAX_REDACTION_ITEMS:
            raise safe_error("STRUCTURE_LIMIT")
        if isinstance(item, str):
            if contains_secret_like(item):
                raise safe_error("SECRET_MATERIAL")
        elif isinstance(item, dict):
            stack.extend(item.keys())
            stack.extend(item.values())
        elif isinstance(item, (list, tuple)):
            stack.extend(item)
