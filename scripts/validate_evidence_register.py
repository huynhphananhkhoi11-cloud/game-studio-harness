#!/usr/bin/env python3
"""Validate Historical Content Evidence Register CSV files."""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

EXPECTED_HEADER = [
    "claim_id",
    "scene_id",
    "claim",
    "domain",
    "evidence_level",
    "source_citation",
    "locator",
    "source_url",
    "premise_or_constraint",
    "allowed_use",
    "decision",
    "notes",
]
EVIDENCE_LEVELS = {"DIRECT", "RECONSTRUCTION", "INFERENCE", "FICTION", "UNRESOLVED"}
DECISIONS = {"KEEP", "CHANGE", "REMOVE", "HOLD"}
REQUIRED_FIELDS = {"claim_id", "scene_id", "claim", "domain", "evidence_level", "allowed_use", "decision"}
SOURCE_REQUIRED_LEVELS = {"DIRECT", "RECONSTRUCTION"}


@dataclass(frozen=True)
class ValidationMessage:
    """One validation warning or error."""

    path: Path
    line_number: int | None
    claim_id: str | None
    level: str
    reason: str

    def format(self) -> str:
        location = f"{self.path}"
        if self.line_number is not None:
            location += f": line {self.line_number}"
        if self.claim_id:
            location += f" claim_id={self.claim_id}"
        return f"{self.level}: {location}: {self.reason}"


def _blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def validate_header(path: Path, header: Sequence[str] | None) -> list[ValidationMessage]:
    """Return header errors for exact schema, ordering, duplicates, and column count."""
    errors: list[ValidationMessage] = []
    if header is None:
        return [ValidationMessage(path, 1, None, "FAIL", "missing CSV header")]
    if len(set(header)) != len(header):
        seen: set[str] = set()
        duplicates = sorted({name for name in header if name in seen or seen.add(name)})
        errors.append(ValidationMessage(path, 1, None, "FAIL", f"duplicate header column(s): {', '.join(duplicates)}"))
    missing = [name for name in EXPECTED_HEADER if name not in header]
    extra = [name for name in header if name not in EXPECTED_HEADER]
    if missing:
        errors.append(ValidationMessage(path, 1, None, "FAIL", f"missing header column(s): {', '.join(missing)}"))
    if extra:
        errors.append(ValidationMessage(path, 1, None, "FAIL", f"unexpected header column(s): {', '.join(extra)}"))
    if list(header) != EXPECTED_HEADER:
        errors.append(ValidationMessage(path, 1, None, "FAIL", "header must contain exactly the 12 required columns in the required order"))
    return errors


def validate_row(path: Path, row: dict[str, str], line_number: int, seen_claim_ids: set[str]) -> list[ValidationMessage]:
    """Validate one data row and collect all independent errors."""
    errors: list[ValidationMessage] = []
    claim_id = (row.get("claim_id") or "").strip() or None

    for field in EXPECTED_HEADER:
        if field not in row:
            continue
        value = row.get(field)
        if value is None:
            errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", f"row has missing value for column {field}"))

    for field in REQUIRED_FIELDS:
        if _blank(row.get(field)):
            errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", f"required field {field} is blank"))

    if claim_id:
        if claim_id in seen_claim_ids:
            errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", "claim_id must be unique within the file"))
        else:
            seen_claim_ids.add(claim_id)

    evidence_level = (row.get("evidence_level") or "").strip()
    decision = (row.get("decision") or "").strip()
    if evidence_level and evidence_level not in EVIDENCE_LEVELS:
        errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", f"invalid evidence_level {evidence_level!r}"))
    if decision and decision not in DECISIONS:
        errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", f"invalid decision {decision!r}"))

    if evidence_level in SOURCE_REQUIRED_LEVELS:
        for field in ("source_citation", "locator", "source_url"):
            if _blank(row.get(field)):
                errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", f"{evidence_level} requires nonblank {field}"))
        source_url = (row.get("source_url") or "").strip()
        if source_url and not (source_url.startswith("http://") or source_url.startswith("https://")):
            errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", "source_url must start with http:// or https://"))

    if evidence_level == "INFERENCE" and _blank(row.get("premise_or_constraint")):
        errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", "INFERENCE requires premise_or_constraint explaining premise and inference step"))
    if evidence_level == "FICTION" and _blank(row.get("premise_or_constraint")):
        errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", "FICTION requires premise_or_constraint explaining historical constraint"))
    if evidence_level == "UNRESOLVED":
        if _blank(row.get("premise_or_constraint")):
            errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", "UNRESOLVED requires premise_or_constraint explaining what remains unknown"))
        if decision and decision not in {"HOLD", "REMOVE"}:
            errors.append(ValidationMessage(path, line_number, claim_id, "FAIL", "UNRESOLVED decision must be HOLD or REMOVE"))

    return errors


def validate_file(path: str | Path) -> tuple[list[ValidationMessage], list[ValidationMessage]]:
    """Validate a CSV file and return (errors, warnings). Does not access networks."""
    csv_path = Path(path)
    errors: list[ValidationMessage] = []
    warnings: list[ValidationMessage] = []
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            errors.extend(validate_header(csv_path, reader.fieldnames))
            rows = list(reader)
    except OSError as exc:
        return [ValidationMessage(csv_path, None, None, "FAIL", f"cannot read file: {exc}")], warnings
    except csv.Error as exc:
        return [ValidationMessage(csv_path, None, None, "FAIL", f"CSV parse error: {exc}")], warnings

    if not rows and not errors:
        warnings.append(ValidationMessage(csv_path, 1, None, "WARNING", "header-only template has no data rows"))

    seen_claim_ids: set[str] = set()
    if not errors:
        for index, row in enumerate(rows, start=2):
            errors.extend(validate_row(csv_path, row, index, seen_claim_ids))
    return errors, warnings


def run(paths: Iterable[str | Path]) -> int:
    """Validate paths, print PASS/FAIL messages, and return a process exit code."""
    any_errors = False
    for path in paths:
        errors, warnings = validate_file(path)
        for warning in warnings:
            print(warning.format())
        if errors:
            any_errors = True
            for error in errors:
                print(error.format())
        else:
            print(f"PASS: {path}")
    return 1 if any_errors else 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("Usage: python scripts/validate_evidence_register.py PATH [PATH ...]", file=sys.stderr)
        return 1
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
