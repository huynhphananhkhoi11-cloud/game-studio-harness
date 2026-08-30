import copy
import io
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from scripts.orchestration_handoff import (
    HandoffError,
    canonical_digest,
    explain_handoff,
    main,
    validate_claim,
    validate_claim_set,
    validate_handoff,
    validate_worktree,
)


FIXTURES = Path("platform/orchestration/fixtures/007c")
AS_OF = "2026-08-30T10:00:00Z"
BASE = "633cbb319d2bc6c6361cf602ae67d5b4f49e308b"
CURRENT = "ad736df31294f0974ded6f78d0e8c4bdc4b8890c"


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def valid_claim():
    return fixture("valid-writer-claim.json")


def valid_worktree():
    return fixture("valid-worktree-record.json")


def valid_handoff():
    return fixture("valid-durable-handoff.json")


def overlapping_claim(fixture_name):
    case = fixture(fixture_name)
    claim = valid_claim()
    claim.update(case["mutations"])
    claim["permitted_paths"] = case["permitted_paths"]
    return claim, case["expected_error"]


def valid_exception(left, right, paths):
    return {
        "exception_id": "EXCEPTION-OVERLAP-001",
        "claim_ids": [left["claim_id"], right["claim_id"]],
        "overlapping_paths": paths,
        "reason": "Studio Owner bounded one overlap for independent review.",
        "approver_role": "STUDIO_OWNER",
        "approval_reference": "studio/memory/tasks/STUDIO-007C/STATE.md",
        "decided_at": "2026-08-30T09:00:00Z",
        "expires_at": "2026-08-30T11:00:00Z",
    }


def renewal(prior):
    claim = copy.deepcopy(prior)
    claim.update(
        claim_id="STUDIO-007C-WRITER-0002",
        issued_at="2026-08-30T10:30:00Z",
        expires_at="2026-08-31T10:30:00Z",
        lease_revision=2,
        prior_claim_id=prior["claim_id"],
        prior_claim_digest=canonical_digest(prior),
    )
    return claim


class ClaimValidationTests(unittest.TestCase):
    def test_valid_claim_passes_at_explicit_as_of(self):
        self.assertEqual(validate_claim(valid_claim(), AS_OF)["executor_id"],
                         "ENGINEERING-01")

    def test_declared_expired_fixture_fails(self):
        case = fixture("invalid-expired-claim.json")
        claim = valid_claim()
        claim.update(case["mutations"])
        with self.assertRaisesRegex(HandoffError, case["expected_error"]):
            validate_claim(claim, case["as_of"])

    def test_exact_overlap_fails_in_both_orders(self):
        left = valid_claim()
        right, expected = overlapping_claim("invalid-exact-overlap.json")
        for claims in ([left, right], [right, left]):
            with self.subTest(order=claims[0]["claim_id"]), \
                    self.assertRaisesRegex(HandoffError, expected):
                validate_claim_set(claims, AS_OF)

    def test_ancestor_overlap_fails_in_both_orders(self):
        left = valid_claim()
        right, expected = overlapping_claim("invalid-ancestor-overlap.json")
        for claims in ([left, right], [right, left]):
            with self.subTest(order=claims[0]["claim_id"]), \
                    self.assertRaisesRegex(HandoffError, expected):
                validate_claim_set(claims, AS_OF)

    def test_text_prefix_without_component_boundary_is_independent(self):
        bundle = fixture("valid-independent-claims.json")
        active = validate_claim_set(bundle["claims"], AS_OF, bundle["exceptions"])
        self.assertEqual(len(active), 2)

    def test_duplicate_ids_and_paths_fail(self):
        claim = valid_claim()
        claim["permitted_paths"].append(claim["permitted_paths"][0])
        with self.assertRaisesRegex(HandoffError, "duplicates"):
            validate_claim(claim)
        claim = valid_claim()
        with self.assertRaisesRegex(HandoffError, "duplicate claim_id"):
            validate_claim_set([claim, copy.deepcopy(claim)], AS_OF)

    def test_unsafe_absolute_parent_backslash_and_secret_fail(self):
        cases = [
            ("C:/private/file", "repository-relative"),
            ("../private/file", "unsafe"),
            ("private//file", "unsafe"),
            ("private/./file", "unsafe"),
            ("private\\file", "forward slashes"),
            ("ghp_abcdefghijklmnopqrstuvwxyz123456", "credential"),
        ]
        for path_value, expected in cases:
            claim = valid_claim()
            claim["permitted_paths"] = [path_value]
            with self.subTest(path=path_value), self.assertRaisesRegex(HandoffError, expected):
                validate_claim(claim)

    def test_shape_digest_chronology_and_status_fail_closed(self):
        mutations = [
            (lambda c: c.update(extra=True), "unsupported fields"),
            (lambda c: c.pop("branch"), "missing fields"),
            (lambda c: c.update(work_order_digest="bad"), "work_order_digest"),
            (lambda c: c.update(expires_at=c["issued_at"]), "follow issued_at"),
            (lambda c: c.update(status="ACTIVE"), "unsupported claim status"),
        ]
        for mutate, expected in mutations:
            claim = valid_claim()
            mutate(claim)
            with self.subTest(expected=expected), self.assertRaisesRegex(HandoffError, expected):
                validate_claim(claim)


class RenewalAndExceptionTests(unittest.TestCase):
    def test_valid_same_writer_renewal_passes(self):
        prior = valid_claim()
        renewed = renewal(prior)
        active = validate_claim_set([prior, renewed], "2026-08-30T10:45:00Z")
        self.assertIn(renewed, active)

    def test_post_expiry_renewal_fails(self):
        prior = valid_claim()
        renewed = renewal(prior)
        renewed["issued_at"] = prior["expires_at"]
        renewed["expires_at"] = "2026-08-31T11:16:13Z"
        with self.assertRaisesRegex(HandoffError, "after expiry"):
            validate_claim_set([prior, renewed], "2026-08-30T11:30:00Z")

    def test_cross_writer_renewal_fails(self):
        prior = valid_claim()
        renewed = renewal(prior)
        renewed["executor_id"] = "QA-01"
        with self.assertRaisesRegex(HandoffError, "changed executor_id"):
            validate_claim_set([prior, renewed], "2026-08-30T10:45:00Z")

    def test_scope_changing_renewal_fails(self):
        prior = valid_claim()
        renewed = renewal(prior)
        renewed["permitted_paths"] = ["projects/other"]
        with self.assertRaisesRegex(HandoffError, "changed permitted_paths"):
            validate_claim_set([prior, renewed], "2026-08-30T10:45:00Z")

    def test_digest_mismatched_renewal_fails(self):
        prior = valid_claim()
        renewed = renewal(prior)
        renewed["prior_claim_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(HandoffError, "lineage digest mismatch"):
            validate_claim_set([prior, renewed], "2026-08-30T10:45:00Z")

    def test_bounded_studio_owner_exception_passes(self):
        left = valid_claim()
        right, _ = overlapping_claim("invalid-exact-overlap.json")
        exception = valid_exception(left, right, ["scripts/orchestration_handoff.py"])
        self.assertEqual(len(validate_claim_set([left, right], AS_OF, [exception])), 2)

    def test_unauthorized_exception_fixture_fails(self):
        left = valid_claim()
        right, _ = overlapping_claim("invalid-exact-overlap.json")
        case = fixture("invalid-unauthorized-exception.json")
        expected = case.pop("expected_error")
        with self.assertRaisesRegex(HandoffError, expected):
            validate_claim_set([left, right], AS_OF, [case])

    def test_expired_or_scope_mismatched_exception_fails(self):
        left = valid_claim()
        right, _ = overlapping_claim("invalid-exact-overlap.json")
        exception = valid_exception(left, right, ["scripts/orchestration_handoff.py"])
        exception["expires_at"] = AS_OF
        with self.assertRaisesRegex(HandoffError, "expired"):
            validate_claim_set([left, right], AS_OF, [exception])
        exception = valid_exception(left, right, ["scripts/not-the-overlap.py"])
        with self.assertRaisesRegex(HandoffError, "scope does not match"):
            validate_claim_set([left, right], AS_OF, [exception])


class WorktreeAndHandoffTests(unittest.TestCase):
    def test_valid_worktree_matches_explicit_identity(self):
        result = validate_worktree(valid_worktree(), valid_claim(),
                                   expected_base=BASE, expected_current=CURRENT)
        self.assertEqual(result["status"], "CLEAN")

    def test_mismatched_base_fixture_and_other_identity_fail(self):
        case = fixture("invalid-mismatched-base.json")
        record = valid_worktree()
        record.update(case["mutations"])
        with self.assertRaisesRegex(HandoffError, case["expected_error"]):
            validate_worktree(record, valid_claim(), expected_base=BASE,
                              expected_current=CURRENT)
        for field, value, expected in [
            ("worktree_id", "OTHER-WORKTREE-01", "worktree ID mismatch"),
            ("branch", "agent/other", "branch mismatch"),
            ("current_commit", "0" * 40, "current commit mismatch"),
        ]:
            record = valid_worktree()
            record[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(HandoffError, expected):
                validate_worktree(record, valid_claim(), expected_base=BASE,
                                  expected_current=CURRENT)

    def test_valid_handoff_and_explanation_are_deterministic(self):
        handoff = valid_handoff()
        validate_handoff(handoff, valid_claim(), valid_worktree(),
                         expected_base=BASE, expected_current=CURRENT)
        first = explain_handoff(handoff, valid_claim(), valid_worktree(),
                                expected_base=BASE, expected_current=CURRENT)
        second = explain_handoff(handoff, valid_claim(), valid_worktree(),
                                 expected_base=BASE, expected_current=CURRENT)
        self.assertEqual(first, second)
        self.assertIn("QA-01", first)
        self.assertIn("resume:", first)

    def test_invalid_handoff_commit_and_scope_escape_fail(self):
        case = fixture("invalid-handoff-commit.json")
        handoff = valid_handoff()
        handoff.update(case["mutations"])
        with self.assertRaisesRegex(HandoffError, case["expected_error"]):
            validate_handoff(handoff, valid_claim(), valid_worktree(),
                             expected_base=BASE, expected_current=CURRENT)
        handoff = valid_handoff()
        handoff["changed_paths"] = ["projects/outside/file.md"]
        with self.assertRaisesRegex(HandoffError, "escapes claim scope"):
            validate_handoff(handoff, valid_claim(), valid_worktree(),
                             expected_base=BASE, expected_current=CURRENT)

    def test_handoff_requires_resumable_nonempty_evidence(self):
        for field in ("completed_work", "pending_work", "checks", "evidence_references",
                      "risks", "blockers", "changed_paths"):
            handoff = valid_handoff()
            handoff[field] = []
            with self.subTest(field=field), self.assertRaisesRegex(HandoffError,
                                                                   "must not be empty"):
                validate_handoff(handoff, valid_claim(), valid_worktree(),
                                 expected_base=BASE, expected_current=CURRENT)
        handoff = valid_handoff()
        handoff["resume_action"] = ""
        with self.assertRaisesRegex(HandoffError, "resume_action"):
            validate_handoff(handoff, valid_claim(), valid_worktree(),
                             expected_base=BASE, expected_current=CURRENT)


class CliAndSafetyTests(unittest.TestCase):
    def test_all_commands_have_deterministic_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = {
                "claim": valid_claim(),
                "worktree": valid_worktree(),
                "handoff": valid_handoff(),
                "claim-set": fixture("valid-independent-claims.json"),
            }
            paths = {}
            for name, value in inputs.items():
                path = root / f"{name}.json"
                path.write_text(json.dumps(value), encoding="utf-8")
                paths[name] = path
            identity = ["--claim", str(paths["claim"]), "--worktree",
                        str(paths["worktree"]), "--expected-base", BASE,
                        "--expected-current", CURRENT]
            commands = [
                ["validate-claim", "--claim", str(paths["claim"]), "--as-of", AS_OF],
                ["validate-claim-set", "--claim-set", str(paths["claim-set"]),
                 "--as-of", AS_OF],
                ["validate-worktree", *identity],
                ["validate-handoff", *identity, "--handoff", str(paths["handoff"])],
                ["explain-handoff", *identity, "--handoff", str(paths["handoff"])],
            ]
            with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()):
                self.assertTrue(all(main(command) == 0 for command in commands))
                self.assertIn("resume:", output.getvalue())
            inputs["claim"]["status"] = "BAD"
            paths["claim"].write_text(json.dumps(inputs["claim"]), encoding="utf-8")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(main(commands[0]), 1)

    def test_invalid_validation_is_read_only_and_uses_no_network_subprocess_or_git(self):
        paths = sorted(FIXTURES.glob("*.json"))
        before = {path: path.read_bytes() for path in paths}
        claim = valid_claim()
        handoff = valid_handoff()
        handoff["changed_paths"] = ["outside/scope"]
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
                patch.object(subprocess, "run", side_effect=AssertionError("subprocess forbidden")), \
                patch.object(subprocess, "Popen", side_effect=AssertionError("subprocess forbidden")):
            with self.assertRaises(HandoffError):
                validate_handoff(handoff, claim, valid_worktree(),
                                 expected_base=BASE, expected_current=CURRENT)
        self.assertEqual(before, {path: path.read_bytes() for path in paths})


if __name__ == "__main__":
    unittest.main()
