"""Read-only STUDIO-007C writer-claim, worktree, and handoff validation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

from scripts.orchestration_queue import parse_utc


SCHEMA_VERSION = 1
CLAIM_STATUSES = {"CLAIMED", "TRANSFER_PENDING", "RELEASED", "UNKNOWN"}
WORKTREE_STATUSES = {"CLEAN", "DIRTY", "UNKNOWN"}
DISPOSITIONS = CLAIM_STATUSES
CLAIM_KEYS = {
    "schema_version", "claim_id", "work_order_id", "work_order_digest",
    "executor_id", "branch", "worktree_id", "base_commit", "permitted_paths",
    "issued_at", "expires_at", "status", "lease_revision", "prior_claim_id",
    "prior_claim_digest", "evidence_references",
}
EXCEPTION_KEYS = {
    "exception_id", "claim_ids", "overlapping_paths", "reason", "approver_role",
    "approval_reference", "decided_at", "expires_at",
}
WORKTREE_KEYS = {
    "schema_version", "worktree_id", "branch", "base_commit", "current_commit",
    "permitted_paths", "status", "evidence_references", "observed_at",
}
HANDOFF_KEYS = {
    "schema_version", "handoff_id", "work_order_id", "claim_id", "sender_id",
    "receiver_id", "branch", "worktree_id", "base_commit", "current_commit",
    "completed_work", "pending_work", "changed_paths", "checks",
    "evidence_references", "risks", "blockers", "claim_disposition",
    "resume_action", "created_at",
}
ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9._-]{2,63}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
SECRET_VALUE_RES = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/:]+:[^\s/@]+@"),
]


class HandoffError(ValueError):
    """A fail-closed claim, worktree, or handoff validation error."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise HandoffError(message)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _exact_keys(value: Any, expected: set[str], label: str) -> None:
    _require(isinstance(value, dict), f"{label} must be a JSON object")
    missing = expected - set(value)
    extra = set(value) - expected
    _require(not missing, f"{label} missing fields: " + ", ".join(sorted(missing)))
    _require(not extra, f"{label} has unsupported fields: " + ", ".join(sorted(extra)))


def _contains_secret(value: Any) -> bool:
    if isinstance(value, str):
        return any(pattern.search(value) for pattern in SECRET_VALUE_RES)
    if isinstance(value, list):
        return any(_contains_secret(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_secret(item) for item in value.values())
    return False


def _strings(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    _require(isinstance(value, list), f"{field} must be an array")
    if nonempty:
        _require(bool(value), f"{field} must not be empty")
    _require(all(isinstance(item, str) and item.strip() for item in value),
             f"{field} entries must be non-empty strings")
    _require(len(value) == len(set(value)), f"{field} contains duplicates")
    return value


def _repo_path(value: str, field: str) -> None:
    _require(isinstance(value, str) and value.strip(), f"{field} must not be empty")
    _require(not value.startswith(("/", "\\")) and not WINDOWS_ABSOLUTE_RE.match(value),
             f"{field} must be repository-relative")
    _require("\\" not in value, f"{field} must use forward slashes")
    _require(not any(ord(character) < 32 for character in value),
             f"{field} contains a control character")
    raw_parts = value.split("/")
    _require(all(part not in ("", ".", "..") for part in raw_parts),
             f"{field} contains an unsafe path segment")
    parts = PurePosixPath(value).parts
    _require(bool(parts), f"{field} contains an unsafe path segment")
    _require(":" not in parts[0], f"{field} must not contain a URI or drive prefix")


def _identifier(value: Any, field: str) -> None:
    _require(isinstance(value, str) and ID_RE.fullmatch(value) is not None,
             f"invalid {field}")


def _commit(value: Any, field: str) -> None:
    _require(isinstance(value, str) and COMMIT_RE.fullmatch(value) is not None,
             f"invalid {field}")


def _path_overlap(left: str, right: str) -> bool:
    left_parts = PurePosixPath(left).parts
    right_parts = PurePosixPath(right).parts
    size = min(len(left_parts), len(right_parts))
    return left_parts[:size] == right_parts[:size]


def _inside(path: str, scopes: list[str]) -> bool:
    return any(_path_overlap(scope, path) and
               len(PurePosixPath(scope).parts) <= len(PurePosixPath(path).parts)
               for scope in scopes)


def validate_claim(claim: Any, as_of: str | None = None) -> dict[str, Any]:
    _exact_keys(claim, CLAIM_KEYS, "claim")
    _require(claim["schema_version"] == SCHEMA_VERSION,
             "unsupported claim schema version")
    for field in ("claim_id", "work_order_id", "executor_id", "worktree_id"):
        _identifier(claim[field], field)
    _require(isinstance(claim["branch"], str) and claim["branch"].strip(),
             "branch must not be empty")
    _require(not claim["branch"].startswith(("/", "-")) and
             ".." not in claim["branch"] and "\\" not in claim["branch"],
             "branch is unsafe")
    _commit(claim["base_commit"], "base_commit")
    _require(isinstance(claim["work_order_digest"], str) and
             DIGEST_RE.fullmatch(claim["work_order_digest"]) is not None,
             "invalid work_order_digest")
    paths = _strings(claim["permitted_paths"], "permitted_paths", nonempty=True)
    for index, path in enumerate(paths):
        _repo_path(path, f"permitted_paths[{index}]")
    _require(claim["status"] in CLAIM_STATUSES, "unsupported claim status")
    _require(type(claim["lease_revision"]) is int and claim["lease_revision"] >= 1,
             "lease_revision must be a positive integer")
    issued = parse_utc(claim["issued_at"], "issued_at")
    expires = parse_utc(claim["expires_at"], "expires_at")
    _require(expires > issued, "expires_at must follow issued_at")
    evidence = _strings(claim["evidence_references"], "evidence_references",
                        nonempty=True)
    for index, path in enumerate(evidence):
        _repo_path(path, f"evidence_references[{index}]")
    if claim["lease_revision"] == 1:
        _require(claim["prior_claim_id"] is None and
                 claim["prior_claim_digest"] is None,
                 "initial claim cannot declare renewal lineage")
    else:
        _identifier(claim["prior_claim_id"], "prior_claim_id")
        _require(isinstance(claim["prior_claim_digest"], str) and
                 DIGEST_RE.fullmatch(claim["prior_claim_digest"]) is not None,
                 "invalid prior_claim_digest")
    _require(not _contains_secret(claim), "claim contains a credential-bearing value")
    if as_of is not None:
        instant = parse_utc(as_of, "as_of")
        _require(instant >= issued, "as_of must not precede issued_at")
        if claim["status"] == "CLAIMED":
            _require(instant < expires, "claim is expired")
    return claim


def _validate_renewal(claim: dict[str, Any], prior: dict[str, Any]) -> None:
    _require(claim["lease_revision"] == prior["lease_revision"] + 1,
             "renewal revision is not sequential")
    _require(claim["prior_claim_digest"] == canonical_digest(prior),
             "renewal lineage digest mismatch")
    for field in ("work_order_id", "work_order_digest", "executor_id", "branch",
                  "worktree_id", "base_commit", "permitted_paths"):
        _require(claim[field] == prior[field], f"renewal changed {field}")
    issued = parse_utc(claim["issued_at"], "issued_at")
    _require(issued >= parse_utc(prior["issued_at"], "prior.issued_at"),
             "renewal precedes prior issue")
    _require(issued < parse_utc(prior["expires_at"], "prior.expires_at"),
             "renewal was issued after expiry")


def _validate_exception(exception: Any, left: dict[str, Any], right: dict[str, Any],
                        overlaps: list[str], as_of: str) -> bool:
    _exact_keys(exception, EXCEPTION_KEYS, "overlap exception")
    _identifier(exception["exception_id"], "exception_id")
    claim_ids = _strings(exception["claim_ids"], "exception.claim_ids", nonempty=True)
    _require(len(claim_ids) == 2 and set(claim_ids) == {left["claim_id"], right["claim_id"]},
             "exception claim IDs do not match")
    paths = _strings(exception["overlapping_paths"], "exception.overlapping_paths",
                     nonempty=True)
    _require(set(paths) == set(overlaps), "exception overlap scope does not match")
    for index, path in enumerate(paths):
        _repo_path(path, f"exception.overlapping_paths[{index}]")
    _require(exception["approver_role"] == "STUDIO_OWNER",
             "only STUDIO_OWNER may approve an overlap exception")
    for field in ("reason", "approval_reference"):
        _require(isinstance(exception[field], str) and exception[field].strip(),
                 f"exception.{field} must not be empty")
    _repo_path(exception["approval_reference"], "exception.approval_reference")
    decided = parse_utc(exception["decided_at"], "exception.decided_at")
    expires = parse_utc(exception["expires_at"], "exception.expires_at")
    instant = parse_utc(as_of, "as_of")
    _require(expires > decided, "exception expiry must follow decision")
    _require(decided <= instant < expires, "overlap exception is expired or not active")
    _require(not _contains_secret(exception), "exception contains a credential-bearing value")
    return True


def validate_claim_set(claims: Any, as_of: str,
                       exceptions: Any | None = None) -> list[dict[str, Any]]:
    _require(isinstance(claims, list) and claims, "claims must be a non-empty array")
    _require(isinstance(exceptions if exceptions is not None else [], list),
             "exceptions must be an array")
    instant = parse_utc(as_of, "as_of")
    by_id: dict[str, dict[str, Any]] = {}
    for claim in claims:
        validate_claim(claim)
        _require(claim["claim_id"] not in by_id,
                 f"duplicate claim_id: {claim['claim_id']}")
        by_id[claim["claim_id"]] = claim
    for claim in claims:
        if claim["lease_revision"] > 1:
            prior_id = claim["prior_claim_id"]
            _require(prior_id in by_id, "renewal prior claim is missing")
            _validate_renewal(claim, by_id[prior_id])
    active_candidates = [
        claim for claim in claims if claim["status"] == "CLAIMED" and
        parse_utc(claim["issued_at"]) <= instant < parse_utc(claim["expires_at"])
    ]
    superseded_ids = {
        claim["prior_claim_id"] for claim in active_candidates
        if claim["prior_claim_id"] is not None
    }
    active = [claim for claim in active_candidates
              if claim["claim_id"] not in superseded_ids]
    supplied = exceptions or []
    for left_index, left in enumerate(active):
        for right in active[left_index + 1:]:
            if (left.get("prior_claim_id") == right["claim_id"] or
                    right.get("prior_claim_id") == left["claim_id"]):
                continue
            overlaps = sorted({path for left_path in left["permitted_paths"]
                               for right_path in right["permitted_paths"]
                               if _path_overlap(left_path, right_path)
                               for path in [left_path if len(PurePosixPath(left_path).parts) >=
                                            len(PurePosixPath(right_path).parts) else right_path]})
            if overlaps:
                matching = [item for item in supplied
                            if isinstance(item, dict) and
                            set(item.get("claim_ids", [])) ==
                            {left["claim_id"], right["claim_id"]}]
                _require(len(matching) == 1,
                         "active writer claims have overlapping path scope")
                _validate_exception(matching[0], left, right, overlaps, as_of)
    return active


def validate_worktree(record: Any, claim: Any, *, expected_base: str,
                      expected_current: str) -> dict[str, Any]:
    validate_claim(claim)
    _exact_keys(record, WORKTREE_KEYS, "worktree record")
    _require(record["schema_version"] == SCHEMA_VERSION,
             "unsupported worktree schema version")
    _identifier(record["worktree_id"], "worktree_id")
    _commit(record["base_commit"], "worktree base_commit")
    _commit(record["current_commit"], "worktree current_commit")
    _commit(expected_base, "expected_base")
    _commit(expected_current, "expected_current")
    _require(record["worktree_id"] == claim["worktree_id"], "worktree ID mismatch")
    _require(record["branch"] == claim["branch"], "worktree branch mismatch")
    _require(record["base_commit"] == claim["base_commit"] == expected_base,
             "worktree base commit mismatch")
    _require(record["current_commit"] == expected_current,
             "worktree current commit mismatch")
    paths = _strings(record["permitted_paths"], "worktree.permitted_paths", nonempty=True)
    for index, path in enumerate(paths):
        _repo_path(path, f"worktree.permitted_paths[{index}]")
    _require(paths == claim["permitted_paths"], "worktree permitted paths mismatch")
    _require(record["status"] in WORKTREE_STATUSES, "unsupported worktree status")
    evidence = _strings(record["evidence_references"],
                        "worktree.evidence_references", nonempty=True)
    for index, path in enumerate(evidence):
        _repo_path(path, f"worktree.evidence_references[{index}]")
    parse_utc(record["observed_at"], "worktree.observed_at")
    _require(not _contains_secret(record), "worktree record contains a credential-bearing value")
    return record


def validate_handoff(handoff: Any, claim: Any, worktree: Any, *,
                     expected_base: str, expected_current: str) -> dict[str, Any]:
    validate_worktree(worktree, claim, expected_base=expected_base,
                      expected_current=expected_current)
    _exact_keys(handoff, HANDOFF_KEYS, "handoff")
    _require(handoff["schema_version"] == SCHEMA_VERSION,
             "unsupported handoff schema version")
    for field in ("handoff_id", "work_order_id", "claim_id", "sender_id",
                  "receiver_id", "worktree_id"):
        _identifier(handoff[field], field)
    _require(handoff["work_order_id"] == claim["work_order_id"],
             "handoff work-order mismatch")
    _require(handoff["claim_id"] == claim["claim_id"], "handoff claim mismatch")
    _require(handoff["sender_id"] == claim["executor_id"], "handoff sender mismatch")
    _require(handoff["branch"] == claim["branch"] == worktree["branch"],
             "handoff branch mismatch")
    _require(handoff["worktree_id"] == claim["worktree_id"] == worktree["worktree_id"],
             "handoff worktree mismatch")
    _commit(handoff["base_commit"], "handoff base_commit")
    _commit(handoff["current_commit"], "handoff current_commit")
    _require(handoff["base_commit"] == expected_base == worktree["base_commit"],
             "handoff base commit mismatch")
    _require(handoff["current_commit"] == expected_current == worktree["current_commit"],
             "handoff current commit mismatch")
    for field in ("completed_work", "pending_work", "checks", "evidence_references",
                  "risks", "blockers"):
        values = _strings(handoff[field], f"handoff.{field}", nonempty=True)
        if field == "evidence_references":
            for index, path in enumerate(values):
                _repo_path(path, f"handoff.evidence_references[{index}]")
    changed = _strings(handoff["changed_paths"], "handoff.changed_paths", nonempty=True)
    for index, path in enumerate(changed):
        _repo_path(path, f"handoff.changed_paths[{index}]")
        _require(_inside(path, claim["permitted_paths"]),
                 f"handoff.changed_paths[{index}] escapes claim scope")
    _require(handoff["claim_disposition"] in DISPOSITIONS,
             "unsupported claim disposition")
    _require(isinstance(handoff["resume_action"], str) and
             handoff["resume_action"].strip(), "resume_action must not be empty")
    parse_utc(handoff["created_at"], "handoff.created_at")
    _require(not _contains_secret(handoff), "handoff contains a credential-bearing value")
    return handoff


def explain_handoff(handoff: Any, claim: Any, worktree: Any, *,
                    expected_base: str, expected_current: str) -> str:
    validate_handoff(handoff, claim, worktree, expected_base=expected_base,
                     expected_current=expected_current)
    lines = [
        f"handoff: {handoff['handoff_id']}",
        f"work_order: {handoff['work_order_id']}",
        f"claim: {handoff['claim_id']} ({handoff['claim_disposition']})",
        f"sender: {handoff['sender_id']}",
        f"receiver: {handoff['receiver_id']}",
        f"branch: {handoff['branch']}",
        f"worktree: {handoff['worktree_id']}",
        f"base: {handoff['base_commit']}",
        f"current: {handoff['current_commit']}",
        "checks: " + "; ".join(handoff["checks"]),
        "blockers: " + "; ".join(handoff["blockers"]),
        f"resume: {handoff['resume_action']}",
    ]
    return "\n".join(lines) + "\n"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HandoffError(f"cannot read valid JSON from {path}") from exc


def _common_identity(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--claim", type=Path, required=True)
    parser.add_argument("--worktree", type=Path, required=True)
    parser.add_argument("--expected-base", required=True)
    parser.add_argument("--expected-current", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    claim = sub.add_parser("validate-claim")
    claim.add_argument("--claim", type=Path, required=True)
    claim.add_argument("--as-of", required=True)
    claim_set = sub.add_parser("validate-claim-set")
    claim_set.add_argument("--claim-set", type=Path, required=True)
    claim_set.add_argument("--as-of", required=True)
    worktree = sub.add_parser("validate-worktree")
    _common_identity(worktree)
    for name in ("validate-handoff", "explain-handoff"):
        command = sub.add_parser(name)
        _common_identity(command)
        command.add_argument("--handoff", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate-claim":
            validate_claim(load_json(args.claim), args.as_of)
            print("VALID")
        elif args.command == "validate-claim-set":
            bundle = load_json(args.claim_set)
            _exact_keys(bundle, {"claims", "exceptions"}, "claim set")
            validate_claim_set(bundle["claims"], args.as_of, bundle["exceptions"])
            print("VALID")
        elif args.command == "validate-worktree":
            validate_worktree(load_json(args.worktree), load_json(args.claim),
                              expected_base=args.expected_base,
                              expected_current=args.expected_current)
            print("VALID")
        else:
            handoff = load_json(args.handoff)
            claim = load_json(args.claim)
            worktree = load_json(args.worktree)
            if args.command == "validate-handoff":
                validate_handoff(handoff, claim, worktree,
                                 expected_base=args.expected_base,
                                 expected_current=args.expected_current)
                print("VALID")
            else:
                print(explain_handoff(handoff, claim, worktree,
                                      expected_base=args.expected_base,
                                      expected_current=args.expected_current), end="")
        return 0
    except (HandoffError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
