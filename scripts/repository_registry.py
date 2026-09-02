#!/usr/bin/env python3
"""Deterministic STUDIO-009B repository-registry validator.

This module consumes the accepted STUDIO-009A boundary validator. It performs
no network, Git, credential, provider, subprocess, clock, or repository I/O.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Iterable

from scripts import connectivity_boundary as cb


SCHEMA_VERSION = "1.0"
REPOSITORY_STATUSES = {"DISABLED", "READ_ONLY_ACTIVE", "WRITE_ACTIVE"}
OWNER_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,37}[a-z0-9])?$")
REPOSITORY_NAME_RE = re.compile(r"^[a-z0-9._-]{1,100}$")
BRANCH_NAMESPACE_RE = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*/$")
DIGEST_RE = cb.DIGEST_RE

REPOSITORY_RECORD_FIELDS = {
    "schema_version",
    "repository_id",
    "host",
    "owner",
    "name",
    "canonical_url",
    "default_branch",
    "registration_revision",
    "access_tier",
    "allowed_paths",
    "denied_paths",
    "allowed_branch_namespace",
    "allowed_classifications",
    "instruction_authority_paths",
    "auth_profile_ref",
    "owner_approval_ref",
    "boundary_digest",
    "threat_assessment_digest",
    "registry_version_ref",
    "status",
    "kill_switch_ref",
    "read_only_downgrade_ref",
    "as_of",
    "expires_at",
    "canonical_digest",
}


class RepositoryRegistryError(ValueError):
    """Fail-closed registry error with a stable, safe code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message


def _fail(code: str, message: str) -> None:
    raise RepositoryRegistryError(code, message)


def canonical_digest(value: dict[str, Any]) -> str:
    """Reuse the STUDIO-009A canonical digest implementation."""
    return cb.canonical_digest(value)


def _safe_call(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except cb.BoundaryValidationError as exc:
        raise RepositoryRegistryError(exc.code, exc.safe_message) from None


def _require_reference(value: Any, label: str, *, nullable: bool = False) -> str | None:
    return _safe_call(cb._validate_reference, value, label, nullable=nullable)


def _require_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not DIGEST_RE.fullmatch(value):
        _fail("DIGEST_FORMAT", f"{label} has invalid digest format")
    return value


def _parse_utc(value: Any, label: str):
    return _safe_call(cb._parse_utc, value, label)


def _validate_repository_identity(record: dict[str, Any]) -> tuple[str, str, str]:
    if record["host"] != "github.com":
        _fail("UNSAFE_GITHUB_URL", "repository host must be pinned to github.com")
    owner = record["owner"]
    name = record["name"]
    if not isinstance(owner, str) or not OWNER_RE.fullmatch(owner):
        _fail("INVALID_REPOSITORY_IDENTITY", "repository owner is not canonical")
    if not isinstance(name, str) or not REPOSITORY_NAME_RE.fullmatch(name):
        _fail("INVALID_REPOSITORY_IDENTITY", "repository name is not canonical")
    if name in {".", ".."}:
        _fail("INVALID_REPOSITORY_IDENTITY", "repository name is not canonical")
    expected = f"https://github.com/{owner}/{name}"
    if record["canonical_url"] != expected:
        _fail("UNSAFE_GITHUB_URL", "canonical repository URL is not the pinned GitHub URL")
    return owner, name, expected


def _validate_branch_namespace(value: Any, *, access_tier: str, default_branch: str) -> str | None:
    if access_tier == "READ_ONLY":
        if value is not None:
            _fail("UNAUTHORIZED_WRITE", "read-only records cannot declare a write namespace")
        return None
    if not isinstance(value, str) or not BRANCH_NAMESPACE_RE.fullmatch(value):
        _fail("INVALID_BRANCH_NAMESPACE", "write-capable record requires a canonical branch namespace")
    if default_branch == value.rstrip("/") or default_branch.startswith(value):
        _fail("INVALID_BRANCH_NAMESPACE", "write namespace cannot contain the default branch")
    return value


def _validate_policy(record: dict[str, Any]) -> tuple[list[str], list[str], list[str], list[str]]:
    allowed_paths, denied_paths = _safe_call(
        cb._validate_paths, record["allowed_paths"], record["denied_paths"]
    )
    if record["access_tier"] != "READ_ONLY":
        _safe_call(cb._validate_write_paths, allowed_paths)
    allowed_classes = _safe_call(
        cb._validate_sorted_unique_strings,
        record["allowed_classifications"],
        "allowed_classifications",
        allowed=cb.CLASSIFICATIONS,
    )
    authority_paths = _safe_call(
        cb._validate_sorted_unique_strings,
        record["instruction_authority_paths"],
        "instruction_authority_paths",
    )
    for path in authority_paths:
        _safe_call(cb._validate_path, path, "instruction_authority_paths")
        if not cb._path_is_allowed(path, allowed_paths):
            _fail("AUTHORITY_SCOPE", "instruction authority lies outside allowed repository scope")
        if any(cb._path_contains(denied, path) for denied in denied_paths):
            _fail("AUTHORITY_SCOPE", "instruction authority overlaps denied repository scope")
    return allowed_paths, denied_paths, allowed_classes, authority_paths


def _validate_evidence_binding(
    record: dict[str, Any],
    boundary: dict[str, Any],
    threat_assessment: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        pair = cb.validate_pair(boundary, threat_assessment)
    except cb.BoundaryValidationError as exc:
        raise RepositoryRegistryError(exc.code, exc.safe_message) from None

    boundary_result = pair["boundary"]
    threat_result = pair["threat_assessment"]
    if record["boundary_digest"] != boundary_result["boundary_digest"]:
        _fail("BOUNDARY_LINEAGE", "repository record boundary digest does not match accepted evidence")
    if record["threat_assessment_digest"] != threat_result["threat_digest"]:
        _fail("BOUNDARY_LINEAGE", "repository record threat digest does not match accepted evidence")

    boundary_repo = boundary["repository"]
    if (
        record["repository_id"] != boundary_repo["repository_id"]
        or record["registration_revision"] != boundary_repo["revision"]
        or record["default_branch"] != boundary_repo["default_branch"]
        or record["access_tier"] != boundary_repo["access_tier"]
        or record["allowed_paths"] != boundary_repo["allowed_paths"]
        or record["denied_paths"] != boundary_repo["denied_paths"]
        or record["auth_profile_ref"] != boundary_repo["auth_profile_ref"]
    ):
        _fail("BOUNDARY_LINEAGE", "repository record broadens or changes accepted boundary repository evidence")

    data_policy = boundary["data_policy"]
    if record["allowed_classifications"] != data_policy["allowed_classifications"]:
        _fail("BOUNDARY_LINEAGE", "repository record classification policy differs from accepted boundary")
    if record["instruction_authority_paths"] != data_policy["instruction_authority_paths"]:
        _fail("BOUNDARY_LINEAGE", "repository record authority policy differs from accepted boundary")

    record_as_of = _parse_utc(record["as_of"], "as_of")
    boundary_as_of = _parse_utc(boundary["as_of"], "boundary.as_of")
    threat_as_of = _parse_utc(threat_assessment["as_of"], "threat_assessment.as_of")
    if boundary_as_of > record_as_of or threat_as_of > record_as_of:
        _fail("FUTURE_EVIDENCE", "accepted boundary evidence is later than repository as_of")
    return boundary_result, threat_result


def validate_repository_record(
    record: dict[str, Any],
    *,
    boundary: dict[str, Any],
    threat_assessment: dict[str, Any],
) -> dict[str, Any]:
    """Validate and normalize one repository record without mutating input."""
    try:
        cb._preflight_content(record)
    except cb.BoundaryValidationError as exc:
        raise RepositoryRegistryError(exc.code, exc.safe_message) from None

    before = cb.canonical_json_bytes(copy.deepcopy(record))
    try:
        value = cb._require_exact_fields(record, REPOSITORY_RECORD_FIELDS, "repository_record")
    except cb.BoundaryValidationError as exc:
        if exc.code == "MISSING_FIELD" and isinstance(record, dict) and "owner_approval_ref" not in record:
            _fail("OWNER_APPROVAL_REQUIRED", "repository record requires Owner approval evidence")
        raise RepositoryRegistryError(exc.code, exc.safe_message) from None

    if value["schema_version"] != SCHEMA_VERSION:
        _fail("UNSUPPORTED_SCHEMA", "unsupported repository record schema version")
    repository_id = _require_reference(value["repository_id"], "repository_id")
    owner, name, canonical_url = _validate_repository_identity(value)
    default_branch = _safe_call(cb._validate_branch, value["default_branch"], "default_branch")
    if not isinstance(value["registration_revision"], str) or not cb.REVISION_RE.fullmatch(value["registration_revision"]):
        _fail("MUTABLE_REVISION", "registration revision must be an immutable commit SHA")
    access_tier = value["access_tier"]
    if access_tier not in cb.ACCESS_TIERS:
        _fail("INVALID_ACCESS_TIER", "repository access tier is unsupported")

    allowed_paths, denied_paths, allowed_classes, authority_paths = _validate_policy(value)
    branch_namespace = _validate_branch_namespace(
        value["allowed_branch_namespace"],
        access_tier=access_tier,
        default_branch=default_branch,
    )

    _require_reference(value["auth_profile_ref"], "auth_profile_ref")
    if value["owner_approval_ref"] is None:
        _fail("OWNER_APPROVAL_REQUIRED", "repository record requires Owner approval evidence")
    _require_reference(value["owner_approval_ref"], "owner_approval_ref")
    _require_digest(value["boundary_digest"], "boundary_digest")
    _require_digest(value["threat_assessment_digest"], "threat_assessment_digest")
    _require_reference(value["registry_version_ref"], "registry_version_ref")
    _require_reference(value["kill_switch_ref"], "kill_switch_ref")
    _require_reference(value["read_only_downgrade_ref"], "read_only_downgrade_ref")

    status = value["status"]
    if status not in REPOSITORY_STATUSES:
        _fail("INVALID_STATUS", "repository record status is unsupported")
    if status == "READ_ONLY_ACTIVE" and access_tier != "READ_ONLY":
        _fail("STATUS_ACCESS_CONFLICT", "read-only active status requires READ_ONLY access")
    if status == "WRITE_ACTIVE" and access_tier == "READ_ONLY":
        _fail("STATUS_ACCESS_CONFLICT", "write-active status requires write-capable access")

    as_of = _parse_utc(value["as_of"], "as_of")
    expires_at = _parse_utc(value["expires_at"], "expires_at")
    if expires_at <= as_of:
        _fail("EXPIRED_REPOSITORY", "repository record is expired at as_of")

    boundary_result, threat_result = _validate_evidence_binding(value, boundary, threat_assessment)

    supplied_digest = value["canonical_digest"]
    if not isinstance(supplied_digest, str) or not DIGEST_RE.fullmatch(supplied_digest):
        _fail("DIGEST_FORMAT", "repository record canonical digest has invalid format")
    expected_digest = canonical_digest(value)
    if supplied_digest != expected_digest:
        _fail("DIGEST_MISMATCH", "repository record canonical digest does not match")

    if cb.canonical_json_bytes(record) != before:
        _fail("INPUT_MUTATION", "repository record input was mutated")

    return {
        "status": "PASS",
        "repository_id": repository_id,
        "host": "github.com",
        "owner": owner,
        "name": name,
        "canonical_url": canonical_url,
        "registration_revision": value["registration_revision"],
        "default_branch": default_branch,
        "access_tier": access_tier,
        "allowed_paths": tuple(allowed_paths),
        "denied_paths": tuple(denied_paths),
        "allowed_branch_namespace": branch_namespace,
        "allowed_classifications": tuple(allowed_classes),
        "instruction_authority_paths": tuple(authority_paths),
        "auth_profile_ref": value["auth_profile_ref"],
        "owner_approval_ref": value["owner_approval_ref"],
        "boundary_digest": boundary_result["boundary_digest"],
        "threat_assessment_digest": threat_result["threat_digest"],
        "registry_version_ref": value["registry_version_ref"],
        "record_status": status,
        "kill_switch_ref": value["kill_switch_ref"],
        "read_only_downgrade_ref": value["read_only_downgrade_ref"],
        "as_of": value["as_of"],
        "expires_at": value["expires_at"],
        "repository_record_digest": expected_digest,
    }


def validate_registry(
    entries: Iterable[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]]
) -> tuple[dict[str, Any], ...]:
    """Validate a registry and reject duplicate/conflicting identities."""
    normalized: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}
    seen_urls: dict[str, str] = {}
    for record, boundary, threat_assessment in entries:
        result = validate_repository_record(
            record, boundary=boundary, threat_assessment=threat_assessment
        )
        repo_id = result["repository_id"]
        url_key = result["canonical_url"].casefold()
        digest = result["repository_record_digest"]
        if repo_id in seen_ids:
            code = "DUPLICATE_REPOSITORY" if seen_ids[repo_id] == digest else "CONFLICTING_REPOSITORY"
            _fail(code, "registry contains duplicate or conflicting repository identity")
        if url_key in seen_urls:
            code = "DUPLICATE_REPOSITORY" if seen_urls[url_key] == digest else "CONFLICTING_REPOSITORY"
            _fail(code, "registry contains duplicate or conflicting canonical repository identity")
        seen_ids[repo_id] = digest
        seen_urls[url_key] = digest
        normalized.append(result)
    return tuple(normalized)


def repository_available(normalized_record: dict[str, Any]) -> bool:
    return normalized_record["record_status"] in {"READ_ONLY_ACTIVE", "WRITE_ACTIVE"}


def path_is_allowed(path: str, normalized_record: dict[str, Any]) -> bool:
    """Apply exact/nested allowlists and denied paths."""
    try:
        cb._validate_path(path, "target_path")
    except cb.BoundaryValidationError as exc:
        raise RepositoryRegistryError(exc.code, exc.safe_message) from None
    if not any(cb._path_contains(parent, path) for parent in normalized_record["allowed_paths"]):
        return False
    if any(cb._path_contains(parent, path) for parent in normalized_record["denied_paths"]):
        return False
    return True
