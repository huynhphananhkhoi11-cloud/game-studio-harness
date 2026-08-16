import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_project_studio.py"
sys.path.insert(0, str(ROOT))

from scripts.validate_project_studio import (  # noqa: E402
    AUTHORIZED_MILESTONE_PATHS,
    AMENDMENT_PATH,
    EXTERNAL_CANDIDATES,
    GDD_BLOBS,
    MEMORY_PACKAGE,
    PRODUCTION_SAVE_SYSTEM_PATH,
    RULES_TEST_PATH,
    git_blob_sha,
    git_text_blob_sha,
    validate_repository,
)

CANDIDATE_REGISTER_PATH = Path("studio/EXTERNAL_CAPABILITY_CANDIDATES.md")


def candidate_register_fixture(mode: str) -> str:
    """Build a register fixture independent of the repository's current mode."""
    lines = ["# External Capability Candidate Register", ""]
    for index, url in enumerate(EXTERNAL_CANDIDATES, start=1):
        lines.extend(
            [
                f"## CANDIDATE-{index:02d} — fixture-{index:02d}",
                "",
                f"- URL: {url}",
                f"- bounded evaluation purpose: Deterministic fixture purpose {index:02d}.",
            ]
        )
        if mode == "BASELINE_UNASSESSED":
            lines.extend(
                [
                    "- assessment: `UNASSESSED`",
                    "- license: `NOT REVIEWED`",
                    "- security: `NOT REVIEWED`",
                    "- pinned commit or tag: `NONE`",
                    "- compatibility: `UNRESOLVED`",
                ]
            )
        elif mode == "EVALUATED":
            reference = f"{index:040x}"
            lines.extend(
                [
                    "- assessment: `EVALUATED`",
                    f"- evaluated reference: `{reference}`",
                    f"- immutable reference: {url}/commit/{reference}",
                    "- license: `FIXTURE LICENSE CONCLUSION`",
                    "- security: `FIXTURE SECURITY CONCLUSION`",
                    "- compatibility: `FIXTURE COMPATIBILITY CONCLUSION`",
                    "- recommendation: `REFERENCE`",
                    f"- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-{index:02d}-fixture`",
                    "- evidence limitation: Static fixture evidence only.",
                ]
            )
        else:
            raise ValueError(f"unsupported candidate-register fixture mode: {mode}")
        lines.extend(
            [
                "- installation: `NOT INSTALLED`",
                "- adoption decision: `NO DECISION`",
                "",
            ]
        )
    return "\n".join(lines)


class ValidateProjectStudioTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name) / "repo"
        self.repo.mkdir()
        required = set(AUTHORIZED_MILESTONE_PATHS) | set(GDD_BLOBS) | {PRODUCTION_SAVE_SYSTEM_PATH}
        for relative in required:
            source = ROOT / relative
            self.assertTrue(source.is_file(), f"test setup missing {relative}")
            destination = self.repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        self.write_candidate_register(candidate_register_fixture("BASELINE_UNASSESSED"))

    def tearDown(self):
        self.tempdir.cleanup()

    def errors(self):
        return validate_repository(self.repo, check_git=False)

    def codes(self):
        return {error.code for error in self.errors()}

    def write_candidate_register(self, content):
        path = self.repo / CANDIDATE_REGISTER_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def assert_valid(self):
        errors = self.errors()
        self.assertEqual([], errors, "\n".join(error.format() for error in errors))

    def test_valid_structure_passes(self):
        self.assert_valid()

    def test_repository_candidate_register_state_passes(self):
        shutil.copy2(ROOT / CANDIDATE_REGISTER_PATH, self.repo / CANDIDATE_REGISTER_PATH)
        self.assert_valid()

    def test_evaluated_structure_and_immutable_commit_urls_pass(self):
        self.write_candidate_register(candidate_register_fixture("EVALUATED"))
        self.assert_valid()

    def test_mixed_candidate_transition_is_blocked(self):
        content = candidate_register_fixture("EVALUATED")
        content = content.replace("assessment: `EVALUATED`", "assessment: `UNASSESSED`", 1)
        self.write_candidate_register(content)
        self.assertIn("CANDIDATE_STATE", self.codes())

    def test_malformed_evaluated_reference_is_blocked(self):
        content = candidate_register_fixture("EVALUATED")
        content = content.replace("evaluated reference: `0000000000000000000000000000000000000001`", "evaluated reference: `ABC123`", 1)
        self.write_candidate_register(content)
        self.assertIn("CANDIDATE_STATE", self.codes())

    def test_mismatched_immutable_reference_is_blocked(self):
        content = candidate_register_fixture("EVALUATED")
        content = content.replace(
            f"immutable reference: {EXTERNAL_CANDIDATES[0]}/commit/0000000000000000000000000000000000000001",
            f"immutable reference: {EXTERNAL_CANDIDATES[0]}/commit/0000000000000000000000000000000000000002",
            1,
        )
        self.write_candidate_register(content)
        self.assertIn("CANDIDATE_STATE", self.codes())

    def test_duplicate_explicit_canonical_url_is_blocked(self):
        content = candidate_register_fixture("EVALUATED")
        marker = f"- URL: {EXTERNAL_CANDIDATES[0]}"
        content = content.replace(marker, marker + "\n" + marker, 1)
        self.write_candidate_register(content)
        self.assertIn("CANDIDATES", self.codes())

    def test_production_gdd_hash_constants_match_sources(self):
        for relative, expected in GDD_BLOBS.items():
            self.assertEqual(expected, git_blob_sha(ROOT / relative))

    def test_missing_required_file_is_blocked(self):
        (self.repo / "projects/si-tu-chapter-1/ARTIFACT_MAP.md").unlink()
        self.assertIn("MISSING_FILE", self.codes())

    def test_extra_memory_file_is_blocked(self):
        (self.repo / MEMORY_PACKAGE / "EXTRA.md").write_text("unexpected\n", encoding="utf-8")
        self.assertIn("MEMORY_PACKAGE", self.codes())

    def test_missing_amendment_is_blocked(self):
        (self.repo / AMENDMENT_PATH).unlink()
        self.assertIn("MISSING_FILE", self.codes())

    def test_altered_windows_test_patch_is_blocked(self):
        path = self.repo / RULES_TEST_PATH
        path.write_text(path.read_text(encoding="utf-8") + "# unauthorized change\n", encoding="utf-8")
        self.assertIn("TEST_PATCH", self.codes())

    def test_production_save_edit_is_blocked(self):
        path = self.repo / PRODUCTION_SAVE_SYSTEM_PATH
        path.write_text(path.read_text(encoding="utf-8") + "# unauthorized change\n", encoding="utf-8")
        self.assertIn("PRODUCTION_IMMUTABILITY", self.codes())

    def test_windows_crlf_checkout_preserves_text_blob_identity(self):
        for relative in (PRODUCTION_SAVE_SYSTEM_PATH, RULES_TEST_PATH):
            path = self.repo / relative
            lf_bytes = path.read_bytes().replace(b"\r\n", b"\n")
            expected = git_text_blob_sha(path)
            path.write_bytes(lf_bytes.replace(b"\n", b"\r\n"))
            self.assertEqual(expected, git_text_blob_sha(path))
        self.assert_valid()

    def test_altered_source_hash_is_blocked(self):
        source = self.repo / next(iter(GDD_BLOBS))
        source.write_bytes(source.read_bytes() + b"TEST-ONLY")
        self.assertIn("SOURCE_HASH", self.codes())

    def test_inconsistent_memory_schema_is_blocked(self):
        state = self.repo / MEMORY_PACKAGE / "STATE.md"
        content = state.read_text(encoding="utf-8")
        state.write_text(content.replace("memory_schema_version: 1", "memory_schema_version: 2", 1), encoding="utf-8")
        self.assertIn("MEMORY_SCHEMA", self.codes())

    def test_referenced_checkpoint_missing_required_evidence_is_blocked(self):
        path = self.repo / MEMORY_PACKAGE / "WORKLOG.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace("  evidence_reference: WORKTREE_ONLY;", "  missing_evidence_reference: WORKTREE_ONLY;", 1)
        path.write_text(content, encoding="utf-8")
        self.assertIn("MEMORY_CHECKPOINT", self.codes())

    def test_state_and_resume_checkpoint_mismatch_is_blocked(self):
        path = self.repo / MEMORY_PACKAGE / "RESUME.md"
        content = path.read_text(encoding="utf-8")
        checkpoint_pattern = r"(?m)^(last_safe_checkpoint_id:\s*)(STUDIO-005-CP-\d{4})\s*$"
        match = re.search(checkpoint_pattern, content)
        self.assertIsNotNone(match, "test setup missing RESUME checkpoint")
        current = match.group(2)
        mismatched = "STUDIO-005-CP-0001" if current != "STUDIO-005-CP-0001" else "STUDIO-005-CP-0002"
        content = re.sub(checkpoint_pattern, rf"\g<1>{mismatched}", content, count=1)
        path.write_text(content, encoding="utf-8")
        self.assertIn("MEMORY_CHECKPOINT", self.codes())

    def test_unsafe_external_candidate_status_is_blocked(self):
        path = self.repo / "studio/EXTERNAL_CAPABILITY_CANDIDATES.md"
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("installation: `NOT INSTALLED`", "installation: `INSTALLED`"), encoding="utf-8")
        self.assertIn("CANDIDATE_STATE", self.codes())

    def test_conflicting_external_candidate_status_is_blocked(self):
        path = self.repo / "studio/EXTERNAL_CAPABILITY_CANDIDATES.md"
        content = path.read_text(encoding="utf-8")
        marker = "- adoption decision: `NO DECISION`"
        prefix, candidate_blocks = content.split("## CANDIDATE-01", 1)
        content = prefix + "## CANDIDATE-01" + candidate_blocks.replace(
            marker, marker + "\n- adoption decision: `ADOPT`", 1
        )
        path.write_text(content, encoding="utf-8")
        self.assertIn("CANDIDATE_STATE", self.codes())

    def test_duplicate_safe_external_candidate_status_is_blocked(self):
        path = self.repo / "studio/EXTERNAL_CAPABILITY_CANDIDATES.md"
        content = path.read_text(encoding="utf-8")
        marker = "- installation: `NOT INSTALLED`"
        prefix, candidate_blocks = content.split("## CANDIDATE-01", 1)
        content = prefix + "## CANDIDATE-01" + candidate_blocks.replace(marker, marker + "\n" + marker, 1)
        path.write_text(content, encoding="utf-8")
        self.assertIn("CANDIDATE_STATE", self.codes())

    def test_missing_external_candidate_is_blocked(self):
        path = self.repo / "studio/EXTERNAL_CAPABILITY_CANDIDATES.md"
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace(EXTERNAL_CANDIDATES[0], "https://example.invalid/missing"), encoding="utf-8")
        self.assertIn("CANDIDATES", self.codes())

    def test_forbidden_automatic_precedence_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/SOURCE_AUTHORITY.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nV23 automatically supersedes V22.\n")
        self.assertIn("SOURCE_PRECEDENCE", self.codes())

    def test_unrelated_negation_does_not_hide_precedence_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/SOURCE_AUTHORITY.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nV23 automatically supersedes V22; this is not optional.\n")
        self.assertIn("SOURCE_PRECEDENCE", self.codes())

    def test_directly_negated_precedence_remains_valid(self):
        path = self.repo / "projects/si-tu-chapter-1/SOURCE_AUTHORITY.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nV23 does not automatically supersede V22.\n")
        self.assert_valid()

    def test_one_draft_claimed_as_higher_authority_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/PROJECT_STUDIO.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nV22 has higher authority than V23.\n")
        self.assertIn("SOURCE_PRECEDENCE", self.codes())

    def test_forbidden_owner_level_role_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/DECISIONS.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nProject Studio Owner approves this test-only line.\n")
        self.assertIn("FORBIDDEN_ROLE", self.codes())

    def test_unauthorized_engine_selection_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/PROJECT_STUDIO.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nEngine selected: Unity.\n")
        self.assertIn("TECH_SELECTION", self.codes())

    def test_unrelated_negation_does_not_hide_engine_selection_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/PROJECT_STUDIO.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nEngine selected: Unity; no review required.\n")
        self.assertIn("TECH_SELECTION", self.codes())

    def test_directly_negated_engine_selection_remains_valid(self):
        path = self.repo / "projects/si-tu-chapter-1/PROJECT_STUDIO.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nNo engine is selected.\n")
        self.assert_valid()

    def test_completion_sequence_regression_is_blocked(self):
        path = self.repo / MEMORY_PACKAGE / "STATE.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace(
            "  - The Studio Owner merged Pull Request #9 into main as implementation merge commit 4e812242c9bc6f96b141e60ff2cf4344bef30ea8.",
            "  - Studio Owner authorization is required before commit, push, or draft Pull Request creation.",
            1,
        )
        path.write_text(content, encoding="utf-8")
        self.assertIn("DELIVERY_SEQUENCE", self.codes())

    def test_stale_worktree_only_durability_is_blocked(self):
        path = self.repo / MEMORY_PACKAGE / "STATE.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace("durability_state: MERGED", "durability_state: WORKTREE_ONLY", 1)
        path.write_text(content, encoding="utf-8")
        self.assertIn("ANCHOR", self.codes())

    def test_missing_delivered_pr_reference_is_blocked(self):
        path = self.repo / MEMORY_PACKAGE / "STATE.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace(
            "last_verified_persisted_ref: main at implementation merge commit 4e812242c9bc6f96b141e60ff2cf4344bef30ea8; Pull Request #9 merged",
            "last_verified_persisted_ref: NONE",
            1,
        )
        path.write_text(content, encoding="utf-8")
        self.assertIn("ANCHOR", self.codes())

    def test_project_studio_must_remain_complete(self):
        path = self.repo / "projects/si-tu-chapter-1/PROJECT_STUDIO.md"
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("- `status`: `COMPLETE`", "- `status`: `HANDOFF`", 1), encoding="utf-8")
        self.assertIn("STATE", self.codes())

    def test_complete_memory_requires_released_writer(self):
        path = self.repo / MEMORY_PACKAGE / "STATE.md"
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("  status: RELEASED", "  status: CLAIMED", 1), encoding="utf-8")
        self.assertIn("WRITER_CLAIM", self.codes())

    def test_copying_cannot_automatically_create_official_content(self):
        path = self.repo / "projects/si-tu-chapter-1/SOURCE_AUTHORITY.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\nCopying V23 makes the passage official canon.\n")
        self.assertIn("OFFICIALIZATION", self.codes())

    def test_official_status_without_promotion_gate_is_blocked(self):
        path = self.repo / "projects/si-tu-chapter-1/SOURCE_AUTHORITY.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace("NOT_YET_DESIGNATED", "DESIGNATED")
        content = content.replace("Studio Owner approval", "automatic approval")
        path.write_text(content, encoding="utf-8")
        codes = self.codes()
        self.assertTrue({"ANCHOR", "OFFICIAL_GDD"} & codes)

    def test_cli_exit_code_for_valid_and_invalid_fixture(self):
        valid = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.repo), "--skip-git-scope"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
        self.assertIn("PASS", valid.stdout)

        (self.repo / "projects/si-tu-chapter-1/PROJECT_STUDIO.md").unlink()
        invalid = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.repo), "--skip-git-scope"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, invalid.returncode)
        self.assertIn("FAIL", invalid.stdout)


if __name__ == "__main__":
    unittest.main()
