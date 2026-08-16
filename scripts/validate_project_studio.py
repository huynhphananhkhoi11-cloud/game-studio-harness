#!/usr/bin/env python3
"""Deterministically validate the SITU-CH1 Project Studio baseline."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

BASELINE_COMMIT = "4e5f3ae84724271363b8f098cfeeceda8ffe9b98"
CONTRACT_COMMIT = "531235536db678ec93c1f8a11ed4e31bbb0bfeff"
AUDITED_IMPLEMENTATION_COMMIT = "c22d75a4f3b1cc041cec4370d2571564d3f86744"
AUDITED_CORRECTION_COMMIT = "8212a080f7a22a96a521829d81e00a7763bb2d50"
IMPLEMENTATION_MERGE_COMMIT = "4e812242c9bc6f96b141e60ff2cf4344bef30ea8"
DELIVERY_PULL_REQUEST = "#9"
CONTRACT_BLOB = "cf09f87461f78500e380a68600fae53df7dc1d02"
EXPECTED_BRANCHES = {"agent/studio-005-closeout", "main"}

CONTRACT_PATH = Path("tasks/STUDIO-005.md")
AMENDMENT_PATH = Path("tasks/STUDIO-005-AMENDMENT-001.md")
RULES_TEST_PATH = Path("tests/test_rules_prototype.py")
BASELINE_RULES_TEST_BLOB = "bd0b5f4e6ec35b1b3579660e30df8f7e3e18884e"
AMENDED_RULES_TEST_BLOB = "5446c1a7858fa67db75833b37b9fa97037baaaf0"
PRODUCTION_SAVE_SYSTEM_PATH = Path("prototype/rules/save_system.py")
PRODUCTION_SAVE_SYSTEM_BLOB = "4909eb5c8f0ab885c51222b164f2ea6b8ed2603c"

PROJECT_ROOT = Path("projects/si-tu-chapter-1")
MEMORY_PACKAGE = PROJECT_ROOT / "memory/tasks/STUDIO-005"
MEMORY_FILES = {"TASK.md", "STATE.md", "WORKLOG.md", "RESUME.md"}

GDD_BLOBS = {
    Path("source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v22_Ban_Chi_Tiet_Day_Du.docx"):
        "a6d6d5519f5fe7b201207a4bfa2cffc1be8ecd3c",
    Path("source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v23_Hieu_Chinh_MQ01.docx"):
        "e73d3b03a78160f761320184ddbe48f5339d752a",
}

IMPLEMENTATION_PATHS = {
    Path("projects/si-tu-chapter-1/PROJECT_STUDIO.md"),
    Path("projects/si-tu-chapter-1/SOURCE_AUTHORITY.md"),
    Path("projects/si-tu-chapter-1/ARTIFACT_MAP.md"),
    Path("projects/si-tu-chapter-1/DECISIONS.md"),
    Path("projects/si-tu-chapter-1/cells/SITU-BASELINE-001.md"),
    Path("projects/si-tu-chapter-1/memory/tasks/STUDIO-005/TASK.md"),
    Path("projects/si-tu-chapter-1/memory/tasks/STUDIO-005/STATE.md"),
    Path("projects/si-tu-chapter-1/memory/tasks/STUDIO-005/WORKLOG.md"),
    Path("projects/si-tu-chapter-1/memory/tasks/STUDIO-005/RESUME.md"),
    Path("studio/EXTERNAL_CAPABILITY_CANDIDATES.md"),
    Path("scripts/validate_project_studio.py"),
    Path("tests/test_validate_project_studio.py"),
    RULES_TEST_PATH,
    AMENDMENT_PATH,
    Path("AGENTS.md"),
    Path("README.md"),
}
AUTHORIZED_MILESTONE_PATHS = IMPLEMENTATION_PATHS | {CONTRACT_PATH}

EXTERNAL_CANDIDATES = [
    "https://github.com/obra/superpowers",
    "https://github.com/anthropics/skills",
    "https://github.com/mattpocock/skills",
    "https://github.com/garrytan/gstack",
    "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
    "https://github.com/Egonex-AI/Understand-Anything",
    "https://github.com/addyosmani/agent-skills",
    "https://github.com/bojieli/ai-agent-book",
    "https://github.com/msitarzewski/agency-agents",
    "https://github.com/santifer/career-ops",
]

CANDIDATE_SHARED_SAFE_FIELDS = {
    "installation": "NOT INSTALLED",
    "adoption decision": "NO DECISION",
}

CANDIDATE_BASELINE_FIELDS = {
    "assessment": "UNASSESSED",
    "license": "NOT REVIEWED",
    "security": "NOT REVIEWED",
    "pinned commit or tag": "NONE",
    "compatibility": "UNRESOLVED",
}

CANDIDATE_EVALUATED_RECOMMENDATIONS = {"ADOPT", "ADAPT", "REFERENCE", "DEFER", "REJECT"}
CANDIDATE_EVALUATED_ONLY_FIELDS = (
    "evaluated reference",
    "immutable reference",
    "recommendation",
    "report anchor",
    "evidence limitation",
)

CHECKPOINT_REQUIRED_FIELDS = (
    "timestamp",
    "actor",
    "action",
    "scope_files",
    "command_or_check",
    "evidence_reference",
    "outcome",
    "rationale",
    "resulting_state",
    "correction_of",
)

TEXT_PATHS = sorted(
    [path for path in IMPLEMENTATION_PATHS if path.suffix in {".md", ".py"}],
    key=str,
)


@dataclass(frozen=True)
class ValidationError:
    """One deterministic validation failure."""

    code: str
    path: Path
    message: str

    def format(self) -> str:
        return f"FAIL [{self.code}] {self.path}: {self.message}"


def git_blob_sha(path: Path) -> str:
    """Return the Git blob SHA-1 for the current bytes at path."""
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git compatibility


def git_text_blob_sha(path: Path) -> str:
    """Return the canonical Git blob SHA-1 for a text worktree file.

    Git may materialize a tracked LF blob with CRLF line endings in a Windows
    worktree.  The clean form stored by this repository is LF, so normalize
    CRLF before computing the blob identity.  This is deliberately separate
    from ``git_blob_sha`` because binary GDD source artifacts must remain
    byte-for-byte identical.
    """
    data = path.read_bytes().replace(b"\r\n", b"\n")
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git compatibility


def _error(errors: list[ValidationError], code: str, path: Path, message: str) -> None:
    errors.append(ValidationError(code, path, message))


def _read_text(root: Path, relative: Path, errors: list[ValidationError]) -> str | None:
    path = root / relative
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        _error(errors, "READ", relative, f"cannot read as UTF-8: {exc}")
        return None


def _require_tokens(
    errors: list[ValidationError],
    relative: Path,
    content: str,
    tokens: Iterable[str],
) -> None:
    for token in tokens:
        if token not in content:
            _error(errors, "ANCHOR", relative, f"missing required anchor {token!r}")


def _validate_required_paths(root: Path, errors: list[ValidationError]) -> None:
    for relative in sorted(AUTHORIZED_MILESTONE_PATHS, key=str):
        path = root / relative
        if not path.is_file():
            _error(errors, "MISSING_FILE", relative, "required milestone file is missing")

    package = root / MEMORY_PACKAGE
    if not package.is_dir():
        _error(errors, "MEMORY_PACKAGE", MEMORY_PACKAGE, "memory package directory is missing")
        return
    actual = {entry.name for entry in package.iterdir()}
    if actual != MEMORY_FILES:
        _error(
            errors,
            "MEMORY_PACKAGE",
            MEMORY_PACKAGE,
            f"must contain exactly {sorted(MEMORY_FILES)}; found {sorted(actual)}",
        )


def _validate_text_hygiene(root: Path, errors: list[ValidationError]) -> None:
    for relative in TEXT_PATHS:
        path = root / relative
        if not path.is_file():
            continue
        content = _read_text(root, relative, errors)
        if content is None:
            continue
        open_token = "{" * 2
        close_token = "}" * 2
        if open_token in content or close_token in content:
            _error(errors, "PLACEHOLDER", relative, "unrendered bundle placeholder remains")
        if not content.endswith("\n"):
            _error(errors, "TEXT_HYGIENE", relative, "file must end with one newline")
        for number, line in enumerate(content.splitlines(), start=1):
            if line.rstrip(" \t") != line:
                _error(errors, "TEXT_HYGIENE", relative, f"trailing whitespace at line {number}")


def _validate_amendment_and_test(root: Path, errors: list[ValidationError]) -> None:
    amendment = _read_text(root, AMENDMENT_PATH, errors)
    if amendment is not None:
        _require_tokens(
            errors,
            AMENDMENT_PATH,
            amendment,
            [
                "`amendment_id`: `STUDIO-005-AMENDMENT-001`",
                "`approval_status`: `OWNER_APPROVED`",
                "53 passed, 1 error",
                "tests/test_rules_prototype.py::RulesTests::test_save_roundtrip",
                "https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile",
                "https://docs.python.org/3/library/os.html#os.replace",
                "producing an amended implementation scope of exactly 16 paths",
                "No other file may be created, modified, deleted, renamed, or moved.",
                "call `save()` twice",
                "does not authorize any change to `prototype/rules/save_system.py`",
                "V22 and V23 remain immutable, co-equal",
                "`official_integrated_gdd` remains `NOT_YET_DESIGNATED`",
                "must not rewrite it",
            ],
        )

    rules_test = root / RULES_TEST_PATH
    if rules_test.is_file():
        actual = git_text_blob_sha(rules_test)
        if actual != AMENDED_RULES_TEST_BLOB:
            _error(
                errors,
                "TEST_PATCH",
                RULES_TEST_PATH,
                f"expected amended Git blob {AMENDED_RULES_TEST_BLOB}, found {actual}",
            )

    save_system = root / PRODUCTION_SAVE_SYSTEM_PATH
    if not save_system.is_file():
        _error(errors, "PRODUCTION_IMMUTABILITY", PRODUCTION_SAVE_SYSTEM_PATH, "production save module is missing")
    else:
        actual = git_text_blob_sha(save_system)
        if actual != PRODUCTION_SAVE_SYSTEM_BLOB:
            _error(
                errors,
                "PRODUCTION_IMMUTABILITY",
                PRODUCTION_SAVE_SYSTEM_PATH,
                f"expected Git blob {PRODUCTION_SAVE_SYSTEM_BLOB}, found {actual}",
            )


def _validate_project_identity(root: Path, errors: list[ValidationError]) -> None:
    project_path = PROJECT_ROOT / "PROJECT_STUDIO.md"
    source_path = PROJECT_ROOT / "SOURCE_AUTHORITY.md"
    artifact_path = PROJECT_ROOT / "ARTIFACT_MAP.md"
    decisions_path = PROJECT_ROOT / "DECISIONS.md"
    cell_path = PROJECT_ROOT / "cells/SITU-BASELINE-001.md"

    contents: dict[Path, str] = {}
    for relative in (project_path, source_path, artifact_path, decisions_path, cell_path):
        text = _read_text(root, relative, errors)
        if text is not None:
            contents[relative] = text

    project = contents.get(project_path, "")
    _require_tokens(
        errors,
        project_path,
        project,
        [
            "`project_studio_id`: `SITU-CH1`",
            "`repository_or_namespace`: `projects/si-tu-chapter-1/`",
            "`project_memory_root`: `projects/si-tu-chapter-1/memory/tasks`",
            "`memory_schema_requirement`: `memory_schema_version: 1`",
            "`official_integrated_gdd`: `NOT_YET_DESIGNATED`",
            "AUTHOR_CREATED_WORKING_DRAFT",
            "CO_EQUAL_INPUT",
            "SITU-BASELINE-001",
            "SOURCE_AUTHORITY.md",
            "Studio Owner approval",
        ],
    )
    status_match = re.search(r"(?m)^- `status`: `([A-Z]+)`$", project)
    if not status_match or status_match.group(1) != "COMPLETE":
        _error(errors, "STATE", project_path, "closed bootstrap status must be COMPLETE")

    cell = contents.get(cell_path, "")
    _require_tokens(
        errors,
        cell_path,
        cell,
        [
            "`cell_id`: `SITU-BASELINE-001`",
            "Producer / Coordination",
            "Narrative / Research",
            "Engineering",
            "QA",
            "Review & Integration",
            "LEVEL 2",
            "tasks/STUDIO-005.md",
        ],
    )
    cell_state_match = re.search(r"(?m)^- `state`: `([A-Z]+)`$", cell)
    if not cell_state_match or cell_state_match.group(1) != "COMPLETE":
        _error(errors, "STATE", cell_path, "closed Cell state must be COMPLETE")
    if status_match and cell_state_match and status_match.group(1) != cell_state_match.group(1):
        _error(errors, "STATE", cell_path, "Cell state must match Project Studio bootstrap status")

    source = contents.get(source_path, "")
    _require_tokens(
        errors,
        source_path,
        source,
        [
            "`source_relationship`: `CO-EQUAL`",
            "`official_integrated_gdd`: `NOT_YET_DESIGNATED`",
            "`AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT`",
            "Design provenance",
            "Historical evidence",
            "Official project authority",
            "bounded content unit",
            "Test internal logic",
            "historical evidence classification",
            "independent review",
            "Studio Owner approval",
            "Materialize durably",
            "MQ01_evidence_register.csv",
            "MQ01_decision_log.md",
            "MQ01_scene_brief.md",
            "Bao_cao_QA_MQ01.md",
            "DOC01",
            "DIRECT",
            "RECONSTRUCTION",
            "INFERENCE",
            "FICTION",
            "UNRESOLVED",
            "A copied passage does not become official solely because it was copied",
        ],
    )
    for relative, expected in GDD_BLOBS.items():
        _require_tokens(errors, source_path, source, [str(relative).replace("\\", "/"), expected])

    decisions = contents.get(decisions_path, "")
    _require_tokens(
        errors,
        decisions_path,
        decisions,
        [
            "OWNER_DECISION-SOURCE-001",
            "CO_EQUAL_INPUT",
            "official_integrated_gdd: NOT_YET_DESIGNATED",
            "Design provenance, historical evidence, and official project authority",
            "Studio Owner approval",
            "DOC01",
            CONTRACT_COMMIT,
        ],
    )

    artifact = contents.get(artifact_path, "")
    for anchor in [
        "source/",
        "docs/design/",
        "docs/HISTORICAL_CONTENT_SYSTEM.md",
        ".agents/skills/historical-game-builder/",
        "data/vertical_slice/",
        "prototype/rules/",
        "reports/",
        "tests/",
        "projects/si-tu-chapter-1/",
        "tasks/STUDIO-005.md",
        "AUTHOR_CREATED_WORKING_DRAFT",
        "CO_EQUAL_INPUT",
        "UNKNOWN",
        "UNRESOLVED",
        "NONE",
    ]:
        if anchor not in artifact:
            _error(errors, "ARTIFACT_MAP", artifact_path, f"missing coverage anchor {anchor!r}")


def _validate_source_hashes(
    root: Path,
    errors: list[ValidationError],
    expected_gdd_blobs: Mapping[Path, str],
) -> None:
    for relative, expected in expected_gdd_blobs.items():
        path = root / relative
        if not path.is_file():
            _error(errors, "SOURCE_HASH", relative, "immutable GDD source is missing")
            continue
        actual = git_blob_sha(path)
        if actual != expected:
            _error(errors, "SOURCE_HASH", relative, f"expected Git blob {expected}, found {actual}")


def _validate_memory(root: Path, errors: list[ValidationError]) -> None:
    memory: dict[str, str] = {}
    for name in sorted(MEMORY_FILES):
        relative = MEMORY_PACKAGE / name
        content = _read_text(root, relative, errors)
        if content is None:
            continue
        memory[name] = content
        if not re.search(r"(?m)^memory_schema_version:\s*1\s*$", content):
            _error(errors, "MEMORY_SCHEMA", relative, "memory_schema_version must be 1")
        _require_tokens(
            errors,
            relative,
            content,
            ["task_id: STUDIO-005", "canonical_task_contract: tasks/STUDIO-005.md"],
        )

    task = memory.get("TASK.md", "")
    _require_tokens(
        errors,
        MEMORY_PACKAGE / "TASK.md",
        task,
        [
            "memory_root: projects/si-tu-chapter-1/memory/tasks",
            "package_path: projects/si-tu-chapter-1/memory/tasks/STUDIO-005",
            "project_studio: SITU-CH1",
            "Cell SITU-BASELINE-001",
        ],
    )
    for relative in sorted(IMPLEMENTATION_PATHS, key=str):
        if str(relative).replace("\\", "/") not in task:
            _error(errors, "MEMORY_SCOPE", MEMORY_PACKAGE / "TASK.md", f"missing authorized path {relative}")

    state = memory.get("STATE.md", "")
    _require_tokens(
        errors,
        MEMORY_PACKAGE / "STATE.md",
        state,
        [
            "branch: main",
            f"last_observed_HEAD: {IMPLEMENTATION_MERGE_COMMIT}",
            "durability_state: MERGED",
            f"last_verified_persisted_ref: main at implementation merge commit {IMPLEMENTATION_MERGE_COMMIT}; Pull Request {DELIVERY_PULL_REQUEST} merged",
            "official_integrated_gdd: NOT_YET_DESIGNATED",
            "exactly the 16 implementation paths",
            f"QA-01 v14 returned APPROVE with zero findings against correction head {AUDITED_CORRECTION_COMMIT}",
            f"merged Pull Request {DELIVERY_PULL_REQUEST} into main as implementation merge commit {IMPLEMENTATION_MERGE_COMMIT}",
            "active_writer_claim:",
        ],
    )
    state_match = re.search(r"(?m)^state:\s*(ACTIVE|BLOCKED|HANDOFF|COMPLETE)$", state)
    writer_match = re.search(r"(?ms)^active_writer_claim:\s*\n\s*status:\s*(CLAIMED|RELEASED|UNKNOWN|TRANSFER_PENDING)", state)
    if not state_match:
        _error(errors, "MEMORY_STATE", MEMORY_PACKAGE / "STATE.md", "invalid current state")
    if not writer_match:
        _error(errors, "WRITER_CLAIM", MEMORY_PACKAGE / "STATE.md", "invalid writer claim")
    if state_match and writer_match:
        current_state, writer_state = state_match.group(1), writer_match.group(1)
        if current_state == "ACTIVE" and writer_state != "CLAIMED":
            _error(errors, "WRITER_CLAIM", MEMORY_PACKAGE / "STATE.md", "ACTIVE requires one CLAIMED writer")
        if current_state == "HANDOFF" and writer_state not in {"RELEASED", "TRANSFER_PENDING"}:
            _error(errors, "WRITER_CLAIM", MEMORY_PACKAGE / "STATE.md", "HANDOFF requires RELEASED or TRANSFER_PENDING")
        if current_state == "COMPLETE" and writer_state != "RELEASED":
            _error(errors, "WRITER_CLAIM", MEMORY_PACKAGE / "STATE.md", "COMPLETE requires a RELEASED writer")

    worklog = memory.get("WORKLOG.md", "")
    _require_tokens(
        errors,
        MEMORY_PACKAGE / "WORKLOG.md",
        worklog,
        ["checkpoint_id: STUDIO-005-CP-0001", "outcome: observed", "correction_of: NONE"],
    )

    checkpoint_headers = list(
        re.finditer(r"(?m)^- checkpoint_id:\s*(STUDIO-005-CP-(\d{4}))\s*$", worklog)
    )
    checkpoint_blocks: dict[str, str] = {}
    checkpoint_numbers: list[int] = []
    for index, header in enumerate(checkpoint_headers):
        checkpoint_id = header.group(1)
        checkpoint_numbers.append(int(header.group(2)))
        end = checkpoint_headers[index + 1].start() if index + 1 < len(checkpoint_headers) else len(worklog)
        block = worklog[header.start():end]
        if checkpoint_id in checkpoint_blocks:
            _error(errors, "MEMORY_CHECKPOINT", MEMORY_PACKAGE / "WORKLOG.md", f"duplicate checkpoint {checkpoint_id}")
            continue
        checkpoint_blocks[checkpoint_id] = block
        for field in CHECKPOINT_REQUIRED_FIELDS:
            values = re.findall(rf"(?m)^  {re.escape(field)}:\s*([^\r\n]+)\s*$", block)
            if len(values) != 1 or not values[0].strip():
                _error(
                    errors,
                    "MEMORY_CHECKPOINT",
                    MEMORY_PACKAGE / "WORKLOG.md",
                    f"{checkpoint_id} must contain exactly one non-empty {field} field",
                )
        outcome = re.search(r"(?m)^  outcome:\s*([^\r\n]+)\s*$", block)
        if outcome and outcome.group(1).strip() not in {
            "attempted", "failed", "partial", "completed", "reviewed", "accepted", "observed"
        }:
            _error(
                errors,
                "MEMORY_CHECKPOINT",
                MEMORY_PACKAGE / "WORKLOG.md",
                f"{checkpoint_id} has unsupported outcome {outcome.group(1).strip()!r}",
            )
    if checkpoint_numbers and checkpoint_numbers != list(range(1, len(checkpoint_numbers) + 1)):
        _error(
            errors,
            "MEMORY_CHECKPOINT",
            MEMORY_PACKAGE / "WORKLOG.md",
            "checkpoint IDs must be unique and sequential from STUDIO-005-CP-0001",
        )

    resume = memory.get("RESUME.md", "")
    _require_tokens(
        errors,
        MEMORY_PACKAGE / "RESUME.md",
        resume,
        [
            "current_state:",
            "required_read_order:",
            "TASK.md",
            "STATE.md",
            "WORKLOG.md",
            "first_verification_actions:",
            "python scripts/validate_project_studio.py",
            "writer_transfer_status:",
        ],
    )
    if state_match:
        resume_state = re.search(r"(?m)^current_state:\s*(ACTIVE|BLOCKED|HANDOFF|COMPLETE)$", resume)
        if not resume_state or resume_state.group(1) != state_match.group(1):
            _error(errors, "MEMORY_STATE", MEMORY_PACKAGE / "RESUME.md", "current_state must match STATE.md")

    state_checkpoint = re.search(r"(?m)^last_safe_checkpoint_id:\s*(STUDIO-005-CP-\d{4})\s*$", state)
    resume_checkpoint = re.search(r"(?m)^last_safe_checkpoint_id:\s*(STUDIO-005-CP-\d{4})\s*$", resume)
    if not state_checkpoint:
        _error(errors, "MEMORY_CHECKPOINT", MEMORY_PACKAGE / "STATE.md", "missing valid last_safe_checkpoint_id")
    if not resume_checkpoint:
        _error(errors, "MEMORY_CHECKPOINT", MEMORY_PACKAGE / "RESUME.md", "missing valid last_safe_checkpoint_id")
    if state_checkpoint and resume_checkpoint:
        state_checkpoint_id = state_checkpoint.group(1)
        if resume_checkpoint.group(1) != state_checkpoint_id:
            _error(errors, "MEMORY_CHECKPOINT", MEMORY_PACKAGE / "RESUME.md", "last_safe_checkpoint_id must match STATE.md")
        if state_checkpoint_id not in checkpoint_blocks:
            _error(
                errors,
                "MEMORY_CHECKPOINT",
                MEMORY_PACKAGE / "WORKLOG.md",
                f"referenced last safe checkpoint {state_checkpoint_id} is missing",
            )


def _candidate_field_values(block: str, field: str) -> list[str]:
    """Return non-empty values from explicit candidate list fields."""
    return re.findall(rf"(?mi)^\s*-\s*{re.escape(field)}:\s*(\S.*)$", block)


def _candidate_backtick_values(block: str, field: str) -> list[str]:
    """Return values when the complete field value is one backtick token."""
    return re.findall(rf"(?mi)^\s*-\s*{re.escape(field)}:\s*`([^`]+)`\s*$", block)


def _validate_exact_candidate_field(
    errors: list[ValidationError],
    relative: Path,
    candidate_id: str,
    block: str,
    field: str,
    expected_value: str,
) -> None:
    raw_values = _candidate_field_values(block, field)
    values = _candidate_backtick_values(block, field)
    if len(raw_values) != 1 or values != [expected_value]:
        _error(
            errors,
            "CANDIDATE_STATE",
            relative,
            f"CANDIDATE-{candidate_id} requires exactly one {field!r} value "
            f"equal to {expected_value!r}; found {values}",
        )


def _validate_external_candidates(root: Path, errors: list[ValidationError]) -> None:
    relative = Path("studio/EXTERNAL_CAPABILITY_CANDIDATES.md")
    content = _read_text(root, relative, errors)
    if content is None:
        return

    headers = list(re.finditer(r"(?m)^## CANDIDATE-(\d{2})\b.*$", content))
    expected_ids = [f"{number:02d}" for number in range(1, 11)]
    if [match.group(1) for match in headers] != expected_ids:
        _error(errors, "CANDIDATES", relative, "candidate sections must be exactly CANDIDATE-01 through CANDIDATE-10")
        return

    blocks: list[tuple[str, str, str]] = []
    explicit_urls: list[str] = []
    assessments: list[str | None] = []
    for index, (match, expected_url) in enumerate(zip(headers, EXTERNAL_CANDIDATES)):
        candidate_id = match.group(1)
        end = headers[index + 1].start() if index + 1 < len(headers) else len(content)
        block = content[match.end():end]
        blocks.append((candidate_id, expected_url, block))

        raw_urls = _candidate_field_values(block, "URL")
        urls = [
            value
            for value in raw_urls
            if re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value)
        ]
        explicit_urls.extend(urls)
        if len(raw_urls) != 1 or urls != [expected_url]:
            _error(
                errors,
                "CANDIDATES",
                relative,
                f"CANDIDATE-{candidate_id} requires exactly one canonical URL equal to {expected_url!r}; found {urls}",
            )

        purposes = _candidate_field_values(block, "bounded evaluation purpose")
        if len(purposes) != 1:
            _error(
                errors,
                "CANDIDATE_STATE",
                relative,
                f"CANDIDATE-{candidate_id} must contain exactly one non-empty bounded evaluation purpose",
            )

        raw_assessments = _candidate_field_values(block, "assessment")
        assessment_values = _candidate_backtick_values(block, "assessment")
        assessments.append(
            assessment_values[0]
            if len(raw_assessments) == 1 and len(assessment_values) == 1
            else None
        )

        for field, expected_value in CANDIDATE_SHARED_SAFE_FIELDS.items():
            _validate_exact_candidate_field(
                errors, relative, candidate_id, block, field, expected_value
            )

    if Counter(explicit_urls) != Counter(EXTERNAL_CANDIDATES):
        _error(errors, "CANDIDATES", relative, "explicit canonical candidate URL multiset mismatch")

    if all(value == "UNASSESSED" for value in assessments):
        mode = "BASELINE_UNASSESSED"
    elif all(value == "EVALUATED" for value in assessments):
        mode = "EVALUATED"
    else:
        mode = None
        _error(
            errors,
            "CANDIDATE_STATE",
            relative,
            f"candidate register must be wholly BASELINE_UNASSESSED or wholly EVALUATED; found {assessments}",
        )

    for candidate_id, expected_url, block in blocks:
        if mode == "BASELINE_UNASSESSED":
            for field, expected_value in CANDIDATE_BASELINE_FIELDS.items():
                _validate_exact_candidate_field(
                    errors, relative, candidate_id, block, field, expected_value
                )
            for field in CANDIDATE_EVALUATED_ONLY_FIELDS:
                if _candidate_field_values(block, field):
                    _error(
                        errors,
                        "CANDIDATE_STATE",
                        relative,
                        f"CANDIDATE-{candidate_id} baseline mode must not contain evaluated field {field!r}",
                    )
        elif mode == "EVALUATED":
            if _candidate_field_values(block, "pinned commit or tag"):
                _error(
                    errors,
                    "CANDIDATE_STATE",
                    relative,
                    f"CANDIDATE-{candidate_id} evaluated mode must not contain 'pinned commit or tag'",
                )

            raw_references = _candidate_field_values(block, "evaluated reference")
            references = _candidate_backtick_values(block, "evaluated reference")
            if (
                len(raw_references) != 1
                or len(references) != 1
                or re.fullmatch(r"[0-9a-f]{40}", references[0]) is None
            ):
                _error(
                    errors,
                    "CANDIDATE_STATE",
                    relative,
                    f"CANDIDATE-{candidate_id} requires exactly one 40-lowercase-hex evaluated reference",
                )
                evaluated_reference = None
            else:
                evaluated_reference = references[0]

            immutable_references = _candidate_field_values(block, "immutable reference")
            expected_immutable = (
                f"{expected_url}/commit/{evaluated_reference}" if evaluated_reference is not None else None
            )
            if expected_immutable is None or immutable_references != [expected_immutable]:
                _error(
                    errors,
                    "CANDIDATE_STATE",
                    relative,
                    f"CANDIDATE-{candidate_id} immutable reference must match its canonical URL and evaluated reference",
                )

            for field in ("license", "security", "compatibility", "evidence limitation"):
                values = _candidate_field_values(block, field)
                if len(values) != 1 or not values[0].strip(" `;\t"):
                    _error(
                        errors,
                        "CANDIDATE_STATE",
                        relative,
                        f"CANDIDATE-{candidate_id} requires exactly one non-empty {field!r} conclusion",
                    )

            raw_recommendations = _candidate_field_values(block, "recommendation")
            recommendations = _candidate_backtick_values(block, "recommendation")
            if (
                len(raw_recommendations) != 1
                or len(recommendations) != 1
                or recommendations[0] not in CANDIDATE_EVALUATED_RECOMMENDATIONS
            ):
                _error(
                    errors,
                    "CANDIDATE_STATE",
                    relative,
                    f"CANDIDATE-{candidate_id} recommendation must be one of "
                    f"{sorted(CANDIDATE_EVALUATED_RECOMMENDATIONS)}",
                )

            raw_report_anchors = _candidate_field_values(block, "report anchor")
            report_anchors = _candidate_backtick_values(block, "report anchor")
            if (
                len(raw_report_anchors) != 1
                or len(report_anchors) != 1
                or re.fullmatch(
                    r"studio/EXTERNAL_CAPABILITY_EVALUATION\.md#[a-z0-9][a-z0-9-]*",
                    report_anchors[0],
                )
                is None
            ):
                _error(
                    errors,
                    "CANDIDATE_STATE",
                    relative,
                    f"CANDIDATE-{candidate_id} requires exactly one report anchor under "
                    "studio/EXTERNAL_CAPABILITY_EVALUATION.md",
                )


def _claim_clauses(line: str) -> list[str]:
    """Split one prose line so negation cannot leak across assertions."""
    return [clause.strip() for clause in re.split(r"[;.!?]+", line) if clause.strip()]


def _assertion_is_directly_negated(clause: str, match: re.Match[str]) -> bool:
    """Return whether the matched assertion itself is explicitly negated."""
    assertion_prefix = clause[:match.end()].lower()
    direct_negation = re.compile(
        r"(?:^|[-*:(]\s*)(?:no|neither)\b|"
        r"\b(?:does|do|did|is|are|was|were|must|may|might|can|could|will|would|should|has|have|had)\s+not\b|"
        r"\bcannot\b|\bnever\b|"
        r"\bnot\s+(?:automatically\s+)?(?:supersedes?|overrides?|corrects?|takes?\s+precedence|"
        r"higher\s+authority|has\s+priority|preferred|official|canon|selected|adopted|installed|"
        r"enabled|approved|trusted|production-ready)\b",
        re.IGNORECASE,
    )
    return direct_negation.search(assertion_prefix) is not None


def _validate_authority_language(root: Path, errors: list[ValidationError]) -> None:
    project_files = sorted((root / PROJECT_ROOT).rglob("*.md")) if (root / PROJECT_ROOT).exists() else []
    forbidden_roles = ("Project Owner", "Project Studio Owner", "Platform Studio Owner")
    positive_precedence = re.compile(
        r"\b(?:v22|v23)\b[^;.!?]*?\b(?:automatically\s+)?(?:supersedes?|overrides?|corrects?|takes?\s+precedence|higher\s+authority|has\s+priority|preferred)\b",
        re.IGNORECASE,
    )
    positive_officialization = re.compile(
        r"(?:\b(?:v22|v23)\b[^;.!?]*?\b(?:is|becomes?)\b[^;.!?]*?\b(?:official|canon)\b)|"
        r"(?:\b(?:copying|copied|filename|version\s+number|recency|completeness|qa|model)\b[^;.!?]*?"
        r"\b(?:makes?|becomes?|creates?|grants?)\b[^;.!?]*?\b(?:official|canon|authority)\b)",
        re.IGNORECASE,
    )
    for absolute in project_files:
        relative = absolute.relative_to(root)
        try:
            content = absolute.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for role in forbidden_roles:
            if role in content:
                _error(errors, "FORBIDDEN_ROLE", relative, f"must not introduce owner-level role {role!r}")
        for number, line in enumerate(content.splitlines(), start=1):
            for clause in _claim_clauses(line):
                precedence_match = positive_precedence.search(clause)
                if precedence_match and not _assertion_is_directly_negated(clause, precedence_match):
                    _error(errors, "SOURCE_PRECEDENCE", relative, f"positive draft-precedence assertion at line {number}: {clause}")
                official_match = positive_officialization.search(clause)
                if official_match and not _assertion_is_directly_negated(clause, official_match):
                    _error(errors, "OFFICIALIZATION", relative, f"unsupported automatic officialization at line {number}: {clause}")

    authority_files = [
        PROJECT_ROOT / "PROJECT_STUDIO.md",
        PROJECT_ROOT / "SOURCE_AUTHORITY.md",
        PROJECT_ROOT / "DECISIONS.md",
        MEMORY_PACKAGE / "STATE.md",
        MEMORY_PACKAGE / "RESUME.md",
        Path("README.md"),
    ]
    for relative in authority_files:
        content = _read_text(root, relative, errors)
        if content is None:
            continue
        normalized = content.replace("`", "")
        if "official_integrated_gdd: NOT_YET_DESIGNATED" not in normalized:
            _error(errors, "OFFICIAL_GDD", relative, "must preserve official_integrated_gdd: NOT_YET_DESIGNATED")


def _validate_no_technology_selection(root: Path, errors: list[ValidationError]) -> None:
    scan_paths = [
        PROJECT_ROOT / "PROJECT_STUDIO.md",
        PROJECT_ROOT / "SOURCE_AUTHORITY.md",
        PROJECT_ROOT / "ARTIFACT_MAP.md",
        PROJECT_ROOT / "DECISIONS.md",
        PROJECT_ROOT / "cells/SITU-BASELINE-001.md",
        Path("studio/EXTERNAL_CAPABILITY_CANDIDATES.md"),
        Path("README.md"),
    ]
    positive_selection = re.compile(
        r"(?:\b(?:engine|language|framework|runtime|model|provider|router|database|dependency|external\s+capability|skill)\b"
        r"[^;.!?]*?\b(?:selected|adopted|installed|enabled|approved|trusted|production-ready)\b)|"
        r"(?:\b(?:selected|adopted|installed|enabled|approved)\b[^;.!?]*?"
        r"\b(?:engine|language|framework|runtime|model|provider|router|database|dependency|external\s+capability|skill)\b)",
        re.IGNORECASE,
    )
    for relative in scan_paths:
        content = _read_text(root, relative, errors)
        if content is None:
            continue
        for number, line in enumerate(content.splitlines(), start=1):
            for clause in _claim_clauses(line):
                selection_match = positive_selection.search(clause)
                if selection_match and not _assertion_is_directly_negated(clause, selection_match):
                    _error(errors, "TECH_SELECTION", relative, f"unauthorized positive selection at line {number}: {clause}")


def _validate_delivery_sequence(root: Path, errors: list[ValidationError]) -> None:
    targets = {
        MEMORY_PACKAGE / "STATE.md": (
            r"(?ms)^completed:\s*\|\s*\n(?P<body>.*?)(?=^remaining:)",
            ("QA-01 v14", "Review & Integration", "merged Pull Request #9", "STUDIO-005 is COMPLETE"),
        ),
        MEMORY_PACKAGE / "RESUME.md": (
            r"(?ms)^completed_summary:\s*\|\s*\n(?P<body>.*?)(?=^remaining_summary:)",
            ("QA-01 v14", "Review & Integration", "merged Pull Request #9", "STUDIO-005 is COMPLETE"),
        ),
        PROJECT_ROOT / "cells/SITU-BASELINE-001.md": (
            r"(?ms)^## 7\. Completion evidence\s*\n(?P<body>.*?)(?=^## 8\.)",
            ("QA-01 v14", "Review & Integration", "merged Pull Request `#9`", IMPLEMENTATION_MERGE_COMMIT),
        ),
    }
    for relative, (pattern, ordered_tokens) in targets.items():
        content = _read_text(root, relative, errors)
        if content is None:
            continue
        match = re.search(pattern, content)
        if not match:
            _error(errors, "DELIVERY_SEQUENCE", relative, "cannot locate the bounded delivery/handoff section")
            continue
        body = match.group("body")
        positions = [body.find(token) for token in ordered_tokens]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            _error(
                errors,
                "DELIVERY_SEQUENCE",
                relative,
                "must order QA approval -> Review & Integration approval -> PR #9 merge -> COMPLETE",
            )

    state = _read_text(root, MEMORY_PACKAGE / "STATE.md", errors)
    resume = _read_text(root, MEMORY_PACKAGE / "RESUME.md", errors)
    forbidden = "Studio Owner authorization is required before commit, push, or draft Pull Request creation"
    if state is not None and forbidden in state:
        _error(errors, "DELIVERY_SEQUENCE", MEMORY_PACKAGE / "STATE.md", "memory cannot regress to a pre-delivery state after PR #9 exists")
    if resume is not None and forbidden in resume:
        _error(errors, "DELIVERY_SEQUENCE", MEMORY_PACKAGE / "RESUME.md", "memory cannot regress to a pre-delivery state after PR #9 exists")

    stale_tokens = ("REQUEST CHANGES", "rerun required", "Review & Integration verdict: NONE", "Pull Request: #9 OPEN DRAFT")
    for relative, content in (
        (MEMORY_PACKAGE / "STATE.md", state),
        (MEMORY_PACKAGE / "RESUME.md", resume),
    ):
        if content is None:
            continue
        for token in stale_tokens:
            if token in content:
                _error(errors, "DELIVERY_SEQUENCE", relative, f"completed memory retains stale state {token!r}")


def _validate_agent_and_readme(root: Path, errors: list[ValidationError]) -> None:
    agents = _read_text(root, Path("AGENTS.md"), errors)
    if agents is not None:
        _require_tokens(
            errors,
            Path("AGENTS.md"),
            agents,
            [
                "Project Studio `SITU-CH1`",
                "PROJECT_STUDIO.md",
                "SOURCE_AUTHORITY.md",
                "DECISIONS.md",
                "ARTIFACT_MAP.md",
                "AUTHOR_CREATED_WORKING_DRAFT",
                "CO_EQUAL_INPUT",
                "V22",
                "V23",
                "DOC01",
                "design provenance",
                "historical evidence",
                "official project authority",
                "content-promotion gate",
                "Pull Request",
            ],
        )

    readme = _read_text(root, Path("README.md"), errors)
    if readme is not None:
        _require_tokens(
            errors,
            Path("README.md"),
            readme,
            [
                "Project Studio `SITU-CH1`",
                "projects/si-tu-chapter-1/ARTIFACT_MAP.md",
                "projects/si-tu-chapter-1/SOURCE_AUTHORITY.md",
                "CO_EQUAL_INPUT",
                "official_integrated_gdd: NOT_YET_DESIGNATED",
                "memory/tasks/<TASK-ID>/",
                "Pull Request",
                "`main`",
            ],
        )


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def _status_paths(output: str) -> set[Path]:
    paths: set[Path] = set()
    for line in output.splitlines():
        if not line:
            continue
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", maxsplit=1)[1]
        paths.add(Path(value.strip('"')))
    return paths


def _validate_git_scope(root: Path, errors: list[ValidationError]) -> None:
    branch = _run_git(root, "branch", "--show-current")
    if branch.returncode != 0:
        _error(errors, "GIT", Path("."), f"cannot resolve branch: {branch.stderr.strip()}")
        return
    if branch.stdout.strip() not in EXPECTED_BRANCHES:
        _error(
            errors,
            "GIT",
            Path("."),
            f"expected one of {sorted(EXPECTED_BRANCHES)}, found {branch.stdout.strip()!r}",
        )

    contract_blob = _run_git(root, "rev-parse", f"{CONTRACT_COMMIT}:{CONTRACT_PATH.as_posix()}")
    if contract_blob.returncode != 0 or contract_blob.stdout.strip() != CONTRACT_BLOB:
        _error(errors, "CONTRACT", CONTRACT_PATH, "contract commit/blob does not match the approved baseline")
    contract_diff = _run_git(root, "diff", "--quiet", CONTRACT_COMMIT, "--", CONTRACT_PATH.as_posix())
    if contract_diff.returncode != 0:
        _error(errors, "CONTRACT", CONTRACT_PATH, "contract changed after the contract-only commit")

    committed = _run_git(root, "diff", "--name-only", f"{BASELINE_COMMIT}..HEAD")
    status = _run_git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if committed.returncode != 0 or status.returncode != 0:
        _error(errors, "GIT", Path("."), "cannot compute milestone scope")
        return
    committed_paths = {Path(line) for line in committed.stdout.splitlines() if line.strip()}
    working_paths = _status_paths(status.stdout)
    actual = committed_paths | working_paths
    if actual != AUTHORIZED_MILESTONE_PATHS:
        missing = sorted(str(path) for path in AUTHORIZED_MILESTONE_PATHS - actual)
        extra = sorted(str(path) for path in actual - AUTHORIZED_MILESTONE_PATHS)
        _error(errors, "SCOPE", Path("."), f"milestone scope mismatch; missing={missing}, extra={extra}")

    for relative, expected in GDD_BLOBS.items():
        result = _run_git(root, "rev-parse", f"HEAD:{relative.as_posix()}")
        if result.returncode != 0 or result.stdout.strip() != expected:
            _error(errors, "SOURCE_HASH", relative, "HEAD does not retain the approved GDD blob")


def validate_repository(
    root: str | Path,
    *,
    check_git: bool = True,
    expected_gdd_blobs: Mapping[Path, str] | None = None,
) -> list[ValidationError]:
    """Return every independent validation error for one repository root."""
    repo_root = Path(root).resolve()
    errors: list[ValidationError] = []
    _validate_required_paths(repo_root, errors)
    _validate_text_hygiene(repo_root, errors)
    _validate_amendment_and_test(repo_root, errors)
    _validate_project_identity(repo_root, errors)
    _validate_source_hashes(repo_root, errors, expected_gdd_blobs or GDD_BLOBS)
    _validate_memory(repo_root, errors)
    _validate_external_candidates(repo_root, errors)
    _validate_authority_language(repo_root, errors)
    _validate_no_technology_selection(repo_root, errors)
    _validate_delivery_sequence(repo_root, errors)
    _validate_agent_and_readme(repo_root, errors)
    if check_git:
        _validate_git_scope(repo_root, errors)
    return errors


def run(root: str | Path, *, check_git: bool = True) -> int:
    errors = validate_repository(root, check_git=check_git)
    if errors:
        for error in errors:
            print(error.format())
        print(f"FAIL: {len(errors)} Project Studio validation error(s)")
        return 1
    print("PASS: SITU-CH1 Project Studio baseline is structurally valid")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument(
        "--skip-git-scope",
        action="store_true",
        help="skip Git branch/scope checks for isolated unit-test fixtures",
    )
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return run(args.root, check_git=not args.skip_git_scope)


if __name__ == "__main__":
    raise SystemExit(main())
