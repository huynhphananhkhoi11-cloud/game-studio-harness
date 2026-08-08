import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_evidence_register.py"
FIXTURE = ROOT / "tests" / "fixtures" / "evidence_register_valid.csv"
TEMPLATE = ROOT / ".agents" / "skills" / "historical-game-builder" / "assets" / "evidence_register_template.csv"
sys.path.insert(0, str(ROOT))

from scripts.validate_evidence_register import EXPECTED_HEADER, validate_file  # noqa: E402


class ValidateEvidenceRegisterTests(unittest.TestCase):
    def write_rows(self, rows, header=None):
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False)
        path = Path(handle.name)
        with handle:
            writer = csv.DictWriter(handle, fieldnames=header or EXPECTED_HEADER, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return path

    def valid_row(self, **overrides):
        row = {
            "claim_id": "TEST-ONLY-X01",
            "scene_id": "TEST-ONLY-SCENE",
            "claim": "TEST-ONLY placeholder claim, not historical.",
            "domain": "test-domain",
            "evidence_level": "DIRECT",
            "source_citation": "TEST-ONLY Source; TEST-ONLY Title; TEST-ONLY Edition",
            "locator": "TEST-ONLY p. 1",
            "source_url": "https://example.test/source",
            "premise_or_constraint": "",
            "allowed_use": "player-facing fact",
            "decision": "KEEP",
            "notes": "TEST-ONLY",
        }
        row.update(overrides)
        return row

    def reasons(self, path):
        errors, warnings = validate_file(path)
        return [message.reason for message in errors], [message.reason for message in warnings]

    def test_fixture_valid_passes(self):
        errors, warnings = validate_file(FIXTURE)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_header_only_template_passes_with_warning(self):
        errors, warnings = validate_file(TEMPLATE)
        self.assertEqual(errors, [])
        self.assertTrue(any("header-only" in warning.reason for warning in warnings))

    def test_wrong_header_order_is_blocked(self):
        header = EXPECTED_HEADER[:]
        header[0], header[1] = header[1], header[0]
        path = self.write_rows([], header=header)
        errors, _ = self.reasons(path)
        self.assertTrue(any("required order" in reason for reason in errors))

    def test_duplicate_claim_id_is_blocked(self):
        path = self.write_rows([self.valid_row(), self.valid_row(claim_id="TEST-ONLY-X01")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("unique" in reason for reason in errors))

    def test_invalid_evidence_level_is_blocked(self):
        path = self.write_rows([self.valid_row(evidence_level="CERTAIN")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("invalid evidence_level" in reason for reason in errors))

    def test_invalid_decision_is_blocked(self):
        path = self.write_rows([self.valid_row(decision="APPROVE")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("invalid decision" in reason for reason in errors))

    def test_direct_requires_citation_locator_url(self):
        path = self.write_rows([self.valid_row(source_citation="", locator="", source_url="")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("DIRECT requires nonblank source_citation" in reason for reason in errors))
        self.assertTrue(any("DIRECT requires nonblank locator" in reason for reason in errors))
        self.assertTrue(any("DIRECT requires nonblank source_url" in reason for reason in errors))

    def test_reconstruction_requires_citation_locator_url(self):
        path = self.write_rows([self.valid_row(evidence_level="RECONSTRUCTION", source_citation="", locator="", source_url="")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("RECONSTRUCTION requires nonblank source_citation" in reason for reason in errors))
        self.assertTrue(any("RECONSTRUCTION requires nonblank locator" in reason for reason in errors))
        self.assertTrue(any("RECONSTRUCTION requires nonblank source_url" in reason for reason in errors))

    def test_inference_requires_premise(self):
        path = self.write_rows([self.valid_row(evidence_level="INFERENCE", source_citation="", locator="", source_url="", premise_or_constraint="")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("INFERENCE requires premise_or_constraint" in reason for reason in errors))

    def test_fiction_requires_constraint(self):
        path = self.write_rows([self.valid_row(evidence_level="FICTION", source_citation="", locator="", source_url="", premise_or_constraint="")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("FICTION requires premise_or_constraint" in reason for reason in errors))

    def test_unresolved_keep_or_change_is_blocked(self):
        path = self.write_rows([self.valid_row(evidence_level="UNRESOLVED", source_citation="", locator="", source_url="", premise_or_constraint="TEST-ONLY unknown", decision="KEEP")])
        errors, _ = self.reasons(path)
        self.assertTrue(any("UNRESOLVED decision must be HOLD or REMOVE" in reason for reason in errors))

    def test_multiple_errors_collected_in_same_file(self):
        path = self.write_rows([
            self.valid_row(claim_id="", decision="ALSO-BAD", source_citation="", locator="", source_url="ftp://example.test")
        ])
        errors, _ = self.reasons(path)
        self.assertGreaterEqual(len(errors), 5)
        self.assertTrue(any("required field claim_id" in reason for reason in errors))
        self.assertTrue(any("invalid decision" in reason for reason in errors))

    def test_cli_exit_code_for_valid_and_invalid_input(self):
        valid = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        self.assertIn("PASS", valid.stdout)

        invalid_path = self.write_rows([self.valid_row(evidence_level="BAD")])
        invalid = subprocess.run([sys.executable, str(SCRIPT), str(invalid_path)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("FAIL", invalid.stdout)


if __name__ == "__main__":
    unittest.main()
