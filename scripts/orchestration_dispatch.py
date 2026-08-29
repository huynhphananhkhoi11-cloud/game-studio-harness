"""Zero-cost STUDIO-007B capability registry and manual dispatcher."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from typing import Any

from scripts.orchestration_queue import parse_utc, snapshot_digest, validate_work_order


SCHEMA_VERSION = 1
CAPABILITY_TAGS = {
    "production.coordination",
    "game-design.systems",
    "narrative.research",
    "engineering.repository",
    "qa.validation",
    "review.integration",
}
INTERNAL_EXECUTOR_IDS = {
    "PRODUCER-01",
    "GAME-DESIGN-01",
    "NARRATIVE-RESEARCH-01",
    "ENGINEERING-01",
    "QA-01",
    "REVIEW-INTEGRATION-01",
}
SOURCE_CLASSES = {"INTERNAL_ROLE", "EXTERNAL_CANDIDATE"}
ELIGIBILITY_VALUES = {
    "ELIGIBLE", "REFERENCE", "NOT_INSTALLED", "NO_DECISION", "ADAPT_PENDING"
}
AVAILABILITY_VALUES = {"AVAILABLE", "UNAVAILABLE"}
TRUST_LEVELS = {"EVIDENCE_PENDING", "EVIDENCE_VERIFIED", "RESTRICTED"}
ALTERNATIVE_OUTCOMES = {"CONSIDERED_NOT_SELECTED", "INELIGIBLE", "UNAVAILABLE"}

REGISTRY_KEYS = {"schema_version", "registry_id", "updated_at", "records"}
RECORD_KEYS = {
    "executor_id", "organizational_role", "source_class", "eligibility",
    "capability_tags", "input_types", "output_types", "constraints",
    "availability", "cost_class", "trust_level", "evidence_references",
}
DECISION_KEYS = {
    "schema_version", "decision_id", "work_order_id", "work_order_digest",
    "selected_executor_id", "required_capability_tags", "required_input_types",
    "required_output_types", "considered_alternatives", "dispatcher_id",
    "dispatcher_role", "reason", "evidence_references", "decided_at", "expires_at",
}
ALTERNATIVE_KEYS = {"executor_id", "outcome", "reason"}

REGISTRY_ID_RE = re.compile(r"^REG-[A-Z0-9][A-Z0-9._-]{2,63}$")
DECISION_ID_RE = re.compile(r"^DSP-[A-Z0-9][A-Z0-9._-]{2,63}$")
EXECUTOR_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9._-]{2,63}$")
TYPE_RE = re.compile(r"^[a-z0-9][a-z0-9._+-]{1,63}$")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
SECRET_VALUE_RES = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/:]+:[^\s/@]+@"),
]


class DispatchError(ValueError):
    """A fail-closed registry or manual-dispatch error."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DispatchError(message)


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
    _require(not value.startswith(("/", "\\")) and not WINDOWS_ABSOLUTE_RE.match(value),
             f"{field} must be repository-relative")
    _require("\\" not in value, f"{field} must use forward slashes")
    parts = PurePosixPath(value).parts
    _require(bool(parts) and all(part not in ("", ".", "..") for part in parts),
             f"{field} contains an unsafe path segment")
    _require(":" not in parts[0], f"{field} must not contain a URI or drive prefix")


def _exact_keys(value: Any, expected: set[str], label: str) -> None:
    _require(isinstance(value, dict), f"{label} must be a JSON object")
    missing = expected - set(value)
    extra = set(value) - expected
    _require(not missing, f"{label} missing fields: " + ", ".join(sorted(missing)))
    _require(not extra, f"{label} has unsupported fields: " + ", ".join(sorted(extra)))


def validate_registry(registry: Any) -> dict[str, dict[str, Any]]:
    _exact_keys(registry, REGISTRY_KEYS, "registry")
    _require(registry["schema_version"] == SCHEMA_VERSION,
             "unsupported registry schema version")
    _require(isinstance(registry["registry_id"], str) and
             REGISTRY_ID_RE.fullmatch(registry["registry_id"]), "invalid registry_id")
    parse_utc(registry["updated_at"], "registry.updated_at")
    _require(isinstance(registry["records"], list) and registry["records"],
             "registry.records must be a non-empty array")
    _require(not _contains_secret(registry), "registry contains a credential-bearing value")

    by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(registry["records"]):
        label = f"records[{index}]"
        _exact_keys(record, RECORD_KEYS, label)
        executor_id = record["executor_id"]
        _require(isinstance(executor_id, str) and EXECUTOR_ID_RE.fullmatch(executor_id),
                 f"{label}.executor_id is invalid")
        _require(executor_id not in by_id, f"duplicate executor_id: {executor_id}")
        _require(isinstance(record["organizational_role"], str) and
                 record["organizational_role"].strip(),
                 f"{label}.organizational_role must not be empty")
        _require(record["source_class"] in SOURCE_CLASSES,
                 f"{label}.source_class is unsupported")
        _require(record["eligibility"] in ELIGIBILITY_VALUES,
                 f"{label}.eligibility is unsupported")
        _require(record["availability"] in AVAILABILITY_VALUES,
                 f"{label}.availability is unsupported")
        _require(record["cost_class"] == "ZERO_COST",
                 f"{label}.cost_class must be ZERO_COST")
        _require(record["trust_level"] in TRUST_LEVELS,
                 f"{label}.trust_level is unsupported")

        capabilities = _strings(record["capability_tags"],
                                f"{label}.capability_tags", nonempty=True)
        _require(set(capabilities) <= CAPABILITY_TAGS,
                 f"{label}.capability_tags contains unknown vocabulary")
        for field in ("input_types", "output_types"):
            values = _strings(record[field], f"{label}.{field}", nonempty=True)
            _require(all(TYPE_RE.fullmatch(item) for item in values),
                     f"{label}.{field} contains an invalid type")
        _strings(record["constraints"], f"{label}.constraints")
        evidence = _strings(record["evidence_references"],
                            f"{label}.evidence_references", nonempty=True)
        for evidence_index, path in enumerate(evidence):
            _repo_path(path, f"{label}.evidence_references[{evidence_index}]")

        if record["source_class"] == "INTERNAL_ROLE":
            _require(executor_id in INTERNAL_EXECUTOR_IDS,
                     f"unknown internal executor_id: {executor_id}")
        else:
            _require(record["eligibility"] != "ELIGIBLE",
                     "external candidate cannot be ELIGIBLE")
        if record["eligibility"] == "ELIGIBLE":
            _require(record["source_class"] == "INTERNAL_ROLE",
                     "ELIGIBLE executor must be INTERNAL_ROLE")
            _require(record["trust_level"] != "EVIDENCE_PENDING",
                     "ELIGIBLE executor cannot be EVIDENCE_PENDING")
        by_id[executor_id] = record
    return by_id


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _selected_executor(record: dict[str, Any], decision: dict[str, Any],
                       work_order: dict[str, Any]) -> None:
    _require(record["source_class"] == "INTERNAL_ROLE",
             "selected executor is an external candidate")
    _require(record["eligibility"] == "ELIGIBLE", "selected executor is ineligible")
    _require(record["availability"] == "AVAILABLE", "selected executor is unavailable")
    _require(record["cost_class"] == "ZERO_COST", "selected executor is not zero-cost")
    _require(record["trust_level"] != "EVIDENCE_PENDING",
             "selected executor evidence is pending")
    _require(set(decision["required_capability_tags"]) <= set(record["capability_tags"]),
             "selected executor has a capability mismatch")
    _require(set(decision["required_input_types"]) <= set(record["input_types"]),
             "selected executor has an input-type mismatch")
    _require(set(decision["required_output_types"]) <= set(record["output_types"]),
             "selected executor has an output-type mismatch")
    if record["trust_level"] == "RESTRICTED":
        satisfied = set(work_order["prohibited_actions"]) | set(work_order["acceptance_gates"])
        _require(set(record["constraints"]) <= satisfied,
                 "selected executor has unsatisfied restrictions")


def validate_decision(registry: Any, work_order: Any, decision: Any,
                      as_of: str) -> dict[str, Any]:
    by_id = validate_registry(registry)
    try:
        validate_work_order(work_order)
    except ValueError as exc:
        raise DispatchError(f"invalid work order: {exc}") from exc
    _exact_keys(decision, DECISION_KEYS, "decision")
    _require(decision["schema_version"] == SCHEMA_VERSION,
             "unsupported decision schema version")
    _require(isinstance(decision["decision_id"], str) and
             DECISION_ID_RE.fullmatch(decision["decision_id"]), "invalid decision_id")
    _require(not _contains_secret(decision), "decision contains a credential-bearing value")
    _require(work_order["state"] == "CLAIMABLE", "work order must be CLAIMABLE")
    _require(decision["work_order_id"] == work_order["work_order_id"],
             "work-order ID mismatch")
    _require(decision["work_order_digest"] == snapshot_digest(work_order),
             "work-order digest mismatch")
    _require(isinstance(decision["dispatcher_id"], str) and
             decision["dispatcher_id"].strip(), "dispatcher_id must not be empty")
    _require(decision["dispatcher_role"] == "STUDIO_OWNER",
             "only STUDIO_OWNER may record a dispatch")
    _require(isinstance(decision["reason"], str) and decision["reason"].strip(),
             "dispatch reason must not be empty")

    capabilities = _strings(decision["required_capability_tags"],
                            "required_capability_tags", nonempty=True)
    _require(set(capabilities) == set(work_order["capability_tags"]),
             "decision capabilities must match the work order")
    _require(set(capabilities) <= CAPABILITY_TAGS,
             "decision contains unknown capability vocabulary")
    for field in ("required_input_types", "required_output_types"):
        values = _strings(decision[field], field, nonempty=True)
        _require(all(TYPE_RE.fullmatch(item) for item in values),
                 f"{field} contains an invalid type")
    evidence = _strings(decision["evidence_references"],
                        "evidence_references", nonempty=True)
    for index, path in enumerate(evidence):
        _repo_path(path, f"evidence_references[{index}]")

    selected_id = decision["selected_executor_id"]
    _require(selected_id in by_id, f"unknown selected executor_id: {selected_id}")
    _selected_executor(by_id[selected_id], decision, work_order)

    alternatives = decision["considered_alternatives"]
    _require(isinstance(alternatives, list) and alternatives,
             "considered_alternatives must not be empty")
    alternative_ids: list[str] = []
    for index, alternative in enumerate(alternatives):
        label = f"considered_alternatives[{index}]"
        _exact_keys(alternative, ALTERNATIVE_KEYS, label)
        executor_id = alternative["executor_id"]
        _require(isinstance(executor_id, str) and executor_id.strip(),
                 f"{label}.executor_id must not be empty")
        _require(executor_id in by_id, f"unknown alternative executor_id: {executor_id}")
        _require(executor_id != selected_id, "selected executor cannot be an alternative")
        _require(executor_id not in alternative_ids, "duplicate alternative executor_id")
        _require(alternative["outcome"] in ALTERNATIVE_OUTCOMES,
                 f"{label}.outcome is unsupported")
        _require(isinstance(alternative["reason"], str) and
                 alternative["reason"].strip(), f"{label}.reason must not be empty")
        alternative_ids.append(executor_id)

    decided_at = parse_utc(decision["decided_at"], "decided_at")
    expires_at = parse_utc(decision["expires_at"], "expires_at")
    explicit_as_of = parse_utc(as_of, "as_of")
    _require(expires_at > decided_at, "expires_at must follow decided_at")
    _require(explicit_as_of >= decided_at, "as_of must not precede decided_at")
    _require(explicit_as_of < expires_at, "dispatch decision is expired")
    return by_id[selected_id]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DispatchError(f"cannot read valid JSON from {path}") from exc


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp",
                                               dir=str(path.parent), text=True)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


def record_decision(decision_root: Path, registry: Any, work_order: Any,
                    decision: Any, as_of: str) -> str:
    validate_decision(registry, work_order, decision, as_of)
    path = decision_root / "decisions" / f"{decision['decision_id']}.json"
    rendered = json.dumps(decision, indent=2, ensure_ascii=False) + "\n"
    if path.exists():
        existing = load_json(path)
        if canonical_digest(existing) == canonical_digest(decision):
            return "replayed"
        raise DispatchError("decision_id already exists with different content")
    _atomic_write(path, rendered)
    return "recorded"


def explain(registry: Any, work_order: Any, decision: Any, as_of: str) -> str:
    selected = validate_decision(registry, work_order, decision, as_of)
    alternative_ids = [item["executor_id"] for item in decision["considered_alternatives"]]
    return "\n".join([
        f"decision_id: {decision['decision_id']}",
        f"work_order_id: {decision['work_order_id']}",
        f"selected_executor_id: {selected['executor_id']}",
        "considered_alternatives: " + ", ".join(alternative_ids),
        f"reason: {decision['reason']}",
        "evidence: " + ", ".join(decision["evidence_references"]),
        f"expires_at: {decision['expires_at']}",
    ])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    registry = commands.add_parser("validate-registry")
    registry.add_argument("--registry", type=Path, required=True)

    def decision_arguments(command: argparse.ArgumentParser) -> None:
        command.add_argument("--registry", type=Path, required=True)
        command.add_argument("--work-order", type=Path, required=True)
        command.add_argument("--decision", type=Path, required=True)
        command.add_argument("--as-of", required=True)

    validate = commands.add_parser("validate-decision")
    decision_arguments(validate)
    dispatch = commands.add_parser("dispatch")
    decision_arguments(dispatch)
    dispatch.add_argument("--decision-root", type=Path, required=True)
    explanation = commands.add_parser("explain")
    decision_arguments(explanation)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        registry = load_json(args.registry)
        if args.command == "validate-registry":
            validate_registry(registry)
            print("PASS: capability registry is valid")
            return 0
        work_order = load_json(args.work_order)
        decision = load_json(args.decision)
        if args.command == "validate-decision":
            validate_decision(registry, work_order, decision, args.as_of)
            print("PASS: manual dispatch decision is valid")
        elif args.command == "dispatch":
            print(record_decision(args.decision_root, registry, work_order,
                                  decision, args.as_of))
        elif args.command == "explain":
            print(explain(registry, work_order, decision, args.as_of))
        return 0
    except (DispatchError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
