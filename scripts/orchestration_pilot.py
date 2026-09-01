#!/usr/bin/env python3
"""Deterministic, read-only STUDIO-008 pilot evidence validator."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


class PilotValidationError(ValueError):
    """Raised when supplied pilot evidence fails closed."""


SCENARIO_IDS = {"P01", "P02", "P03", "P04", "P05", "P06_APPROVE", "P06_REJECT"}
REQUIRED_PILOT_PATHS = {"P01", "P02", "P03", "P04", "P05", "P06_APPROVE", "P06_REJECT"}
ALLOWED_ADAPTERS = {"manual", "fake"}
ALLOWED_OWNER_DECISIONS = {"APPROVE", "REJECT"}
SECRET_FRAGMENTS = (
    "authorization",
    "access_token",
    "refresh_token",
    "api_key",
    "password",
    "private_key",
    "session_cookie",
    "credential",
    "bearer ",
)
SAFE_SECRET_KEYS = {"credential_reads"}
TOP_LEVEL_KEYS = {
    "schema_version",
    "kind",
    "scenario_id",
    "work_order_id",
    "correlation_id",
    "as_of",
    "expected_outcome",
    "attempts",
    "claims",
    "handoffs",
    "trace",
    "gates",
    "budget",
    "adapter",
    "metrics",
    "rollback",
    "evidence",
    "expected_digest",
}
BUNDLE_KEYS = {"schema_version", "kind", "as_of", "scenario_files", "scenario_digests", "expected_digest"}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def canonical_digest(value: dict[str, Any]) -> str:
    normalized = copy.deepcopy(value)
    normalized.pop("expected_digest", None)
    return hashlib.sha256(_canonical_bytes(normalized)).hexdigest()


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise PilotValidationError(f"{code}: {message}")


def _reject_secret_like(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered_key = str(key).lower()
            _require(
                lowered_key in SAFE_SECRET_KEYS
                or not any(fragment.strip() in lowered_key for fragment in SECRET_FRAGMENTS),
                "SECRET_LIKE_EVIDENCE",
                f"unsafe key at {path}.{key}",
            )
            _reject_secret_like(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_secret_like(child, f"{path}[{index}]")
    elif isinstance(value, str):
        lowered_value = value.lower()
        _require(
            not any(fragment in lowered_value for fragment in SECRET_FRAGMENTS),
            "SECRET_LIKE_EVIDENCE",
            f"unsafe value at {path}",
        )


def _ids_are_unique(items: Iterable[dict[str, Any]], key: str) -> bool:
    values = [item.get(key) for item in items]
    return None not in values and len(values) == len(set(values))


def _validate_common(record: dict[str, Any], supplied_as_of: str) -> None:
    _require(set(record) == TOP_LEVEL_KEYS, "FIELD_SET", "scenario fields must match the allowlist")
    _require(record["schema_version"] == 1, "SCHEMA_VERSION", "only schema version 1 is accepted")
    _require(record["kind"] == "pilot_scenario", "KIND", "kind must be pilot_scenario")
    _require(record["scenario_id"] in SCENARIO_IDS, "SCENARIO_ID", "unsupported scenario")
    _require(record["as_of"] == supplied_as_of, "AS_OF", "record and supplied as_of must match")
    _require(canonical_digest(record) == record["expected_digest"], "DIGEST", "scenario digest mismatch")
    _reject_secret_like(record)

    attempts = record["attempts"]
    _require(isinstance(attempts, list) and attempts, "ATTEMPTS", "at least one attempt is required")
    _require(_ids_are_unique(attempts, "attempt_id"), "ATTEMPT_ID", "attempt IDs must be unique")
    for attempt in attempts:
        _require(set(attempt) == {"attempt_id", "head_sha", "status"}, "ATTEMPT_FIELDS", "invalid attempt fields")
        _require(len(attempt["head_sha"]) == 40, "HEAD_SHA", "attempt head must be forty characters")

    trace = record["trace"]
    _require(isinstance(trace, list) and trace, "TRACE", "trace evidence is required")
    _require(_ids_are_unique(trace, "event_id"), "TRACE_ID", "trace event IDs must be unique")
    for index, event in enumerate(trace, start=1):
        _require(
            set(event) == {"event_id", "sequence", "correlation_id", "attempt_id", "transition", "prior_event_id"},
            "TRACE_FIELDS",
            "invalid trace fields",
        )
        _require(event["sequence"] == index, "TRACE_SEQUENCE", "trace sequence must be consecutive")
        _require(event["correlation_id"] == record["correlation_id"], "TRACE_CORRELATION", "correlation mismatch")
        expected_prior = None if index == 1 else trace[index - 2]["event_id"]
        _require(event["prior_event_id"] == expected_prior, "TRACE_LINEAGE", "broken prior-event lineage")

    handoffs = record["handoffs"]
    _require(isinstance(handoffs, list) and handoffs, "HANDOFF", "durable handoff evidence is required")
    _require(all(item.get("durable") is True for item in handoffs), "HANDOFF_DURABILITY", "handoffs must be durable")

    budget = record["budget"]
    _require(
        budget == {
            "cost_class": "ZERO_COST",
            "monetary_budget_minor_units": 0,
            "monetary_spend_minor_units": 0,
            "network_calls": 0,
            "credential_reads": 0,
        },
        "ZERO_COST",
        "budget, spend, network, and credential use must remain zero",
    )
    adapter = record["adapter"]
    _require(adapter.get("name") in ALLOWED_ADAPTERS, "ADAPTER", "only manual or fake adapters are accepted")
    _require(adapter.get("network") is False, "ADAPTER_NETWORK", "adapter network must be false")
    _require(adapter.get("provider") is None, "REAL_PROVIDER", "real provider evidence is prohibited")
    _require(adapter.get("executed") is False, "EXECUTION", "validator accepts evidence only")

    metrics = record["metrics"]
    for zero_key in ("unauthorized_writes", "duplicate_writers", "duplicate_outputs", "gate_bypasses"):
        _require(metrics.get(zero_key) == 0, "ZERO_TOLERANCE", f"{zero_key} must be zero")
    _require(metrics.get("handoff_coverage_percent") == 100, "HANDOFF_COVERAGE", "handoff coverage must be 100")
    _require(metrics.get("trace_coverage_percent") == 100, "TRACE_COVERAGE", "trace coverage must be 100")
    _require(record["rollback"].get("manual_demonstrated") is True, "ROLLBACK", "manual rollback proof is required")


def validate_scenario(record: dict[str, Any], supplied_as_of: str) -> dict[str, Any]:
    before = _canonical_bytes(record)
    _validate_common(record, supplied_as_of)
    scenario_id = record["scenario_id"]
    evidence = record["evidence"]

    if scenario_id == "P01":
        _require(len(evidence.get("source_refs", [])) >= 1, "P01_SOURCES", "research sources are required")
        _require(len(evidence.get("limitations", [])) >= 1, "P01_LIMITATIONS", "limitations are required")
        _require(evidence.get("canonical_promoted") is False, "P01_CANON", "research cannot self-promote")
        _require(evidence.get("write_authority") is False, "P01_AUTHORITY", "research has no write authority")
    elif scenario_id == "P02":
        _require(len(record["claims"]) == 1 and record["claims"][0].get("valid") is True, "P02_CLAIM", "one valid claim is required")
        _require(evidence.get("isolated_worktree") is True, "P02_WORKTREE", "isolated worktree is required")
        _require(evidence.get("allowed_paths_only") is True, "P02_PATHS", "only allowed paths may change")
        _require(evidence.get("focused_tests") == "PASS", "P02_FOCUSED_TESTS", "focused tests must pass")
        _require(evidence.get("retained_regression") == "PASS", "P02_REGRESSION", "retained regression must pass")
    elif scenario_id == "P03":
        _require(len(record["attempts"]) == 2, "P03_ATTEMPTS", "failover requires exactly two attempts")
        _require(record["attempts"][0]["status"] == "SAFE_STOP", "P03_SAFE_STOP", "old attempt must safe-stop")
        _require(record["attempts"][1]["status"] == "COMPLETED", "P03_RECOVERY", "new attempt must complete")
        _require(evidence.get("human_reassignment_approved") is True, "P03_APPROVAL", "human approval is required")
    elif scenario_id == "P04":
        _require(record["expected_outcome"] == "CLAIM_SCOPE_CONFLICT", "P04_OUTCOME", "conflict outcome is required")
        _require(evidence.get("overlap_detected") is True, "P04_OVERLAP", "overlap must be detected")
        _require(evidence.get("failure_code") == "CLAIM_SCOPE_CONFLICT", "P04_CODE", "wrong conflict code")
        _require(evidence.get("output_created") is False, "P04_OUTPUT", "conflict must create no output")
    elif scenario_id == "P05":
        _require(len(record["attempts"]) == 2, "P05_ATTEMPTS", "correction requires a new attempt")
        old_head, new_head = (item["head_sha"] for item in record["attempts"])
        _require(old_head != new_head, "P05_HEAD", "corrected head must differ")
        _require(evidence.get("prior_approval_head") == old_head, "P05_PRIOR_GATE", "prior approval must bind old head")
        _require(evidence.get("corrected_gate_head") == new_head, "P05_NEW_GATE", "new gates must bind corrected head")
        _require(evidence.get("prior_approval_reused") is False, "P05_REUSE", "old approval cannot be reused")
    else:
        decision = "APPROVE" if scenario_id == "P06_APPROVE" else "REJECT"
        _require(evidence.get("decision") == decision, "P06_DECISION", "owner decision path mismatch")
        _require(evidence.get("decision") in ALLOWED_OWNER_DECISIONS, "P06_DECISION", "unsupported decision")
        _require(evidence.get("decider_role") == "STUDIO_OWNER", "P06_ROLE", "only Studio Owner may decide")
        _require(evidence.get("bypass_possible") is False, "P06_BYPASS", "owner gate cannot be bypassed")

    _require(before == _canonical_bytes(record), "IMMUTABILITY", "validation mutated supplied evidence")
    return {"scenario_id": scenario_id, "verdict": "PASS", "digest": record["expected_digest"]}


def validate_bundle(bundle: dict[str, Any], fixture_directory: Path, supplied_as_of: str) -> dict[str, Any]:
    before = _canonical_bytes(bundle)
    _require(set(bundle) == BUNDLE_KEYS, "BUNDLE_FIELDS", "bundle fields must match the allowlist")
    _require(bundle["schema_version"] == 1 and bundle["kind"] == "pilot_bundle", "BUNDLE_VERSION", "invalid bundle identity")
    _require(bundle["as_of"] == supplied_as_of, "BUNDLE_AS_OF", "bundle as_of mismatch")
    _require(canonical_digest(bundle) == bundle["expected_digest"], "BUNDLE_DIGEST", "bundle digest mismatch")
    _reject_secret_like(bundle)

    files = bundle["scenario_files"]
    digests = bundle["scenario_digests"]
    _require(set(files) == REQUIRED_PILOT_PATHS, "SCENARIO_COVERAGE", "all pilot paths are required")
    _require(set(digests) == REQUIRED_PILOT_PATHS, "DIGEST_COVERAGE", "all scenario digests are required")

    results = []
    for scenario_id in sorted(REQUIRED_PILOT_PATHS):
        filename = files[scenario_id]
        _require(Path(filename).name == filename, "FIXTURE_PATH", "scenario references must be basenames")
        scenario = json.loads((fixture_directory / filename).read_text(encoding="utf-8"))
        _require(scenario["scenario_id"] == scenario_id, "SCENARIO_REFERENCE", "scenario reference mismatch")
        _require(scenario["expected_digest"] == digests[scenario_id], "SCENARIO_DIGEST_REFERENCE", "digest reference mismatch")
        results.append(validate_scenario(scenario, supplied_as_of))

    _require(before == _canonical_bytes(bundle), "BUNDLE_IMMUTABILITY", "validation mutated bundle evidence")
    return {
        "verdict": "PASS",
        "scenario_paths_passed": 7,
        "required_scenarios_passed": 6,
        "owner_paths_passed": 2,
        "results": results,
        "bundle_digest": bundle["expected_digest"],
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--fixture-directory", type=Path)
    args = parser.parse_args()
    record = load_json(args.path)
    if record.get("kind") == "pilot_bundle":
        fixture_directory = args.fixture_directory or args.path.parent
        result = validate_bundle(record, fixture_directory, args.as_of)
    else:
        result = validate_scenario(record, args.as_of)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
