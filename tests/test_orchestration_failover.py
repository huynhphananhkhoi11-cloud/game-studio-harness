from __future__ import annotations

import copy
import io
import json
import socket
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from scripts import orchestration_failover as failover


AS_OF = "2026-08-30T18:00:00Z"
FIXTURES = Path(__file__).parents[1] / "platform" / "orchestration" / "fixtures" / "007d"
DIGEST = "sha256:" + "a" * 64
BASE = "1" * 40
HEAD = "2" * 40


def event(event_id, attempt_id, attempt_number, prior, nxt, failure, observed, previous=None, **overrides):
    record = {
        "schema_version": 1,
        "event_id": event_id,
        "work_order_id": "WO-007D-001",
        "work_order_digest": DIGEST,
        "attempt_id": attempt_id,
        "attempt_number": attempt_number,
        "prior_state": prior,
        "next_state": nxt,
        "failure_class": failure,
        "detector_id": "DETECTOR-01",
        "evidence_references": ["studio/evidence/failover.txt"],
        "checkpoint_id": "CHECKPOINT-001",
        "handoff_id": None,
        "claim_disposition": "ACTIVE",
        "recovery_action": "Review immutable evidence and follow the legal transition graph.",
        "owner_gate_id": None,
        "prior_event_id": previous["event_id"] if previous else None,
        "prior_event_digest": failover.canonical_digest(previous) if previous else None,
        "observed_at": observed,
    }
    record.update(overrides)
    return record


def claim(claim_id, writer, status="CLAIMED", expires="2026-08-31T00:00:00Z"):
    return {
        "claim_id": claim_id,
        "work_order_id": "WO-007D-001",
        "writer_id": writer,
        "branch": "agent/studio-007d-simulated-failover",
        "path_scope": ["platform/orchestration"],
        "status": status,
        "claimed_at": "2026-08-30T10:00:00Z",
        "expires_at": expires,
        "released_at": "2026-08-30T11:00:00Z" if status == "RELEASED" else None,
    }


def checkpoint(checkpoint_id="CHECKPOINT-001", status="SAFE"):
    return {
        "checkpoint_id": checkpoint_id,
        "work_order_id": "WO-007D-001",
        "content_digest": "sha256:" + ("b" if checkpoint_id.endswith("1") else "c") * 64,
        "status": status,
        "evidence_references": ["studio/evidence/checkpoint.txt"],
        "created_at": "2026-08-30T10:30:00Z",
    }


def executor(executor_id):
    return {
        "executor_id": executor_id,
        "eligible": True,
        "capabilities": ["deterministic-validation"],
        "evidence_references": ["studio/evidence/executor.txt"],
        "observed_at": "2026-08-30T10:30:00Z",
    }


def attempt(attempt_id, number, executor_id, claim_id, checkpoint_id, prior=None, failed=None, handoff=None):
    return {
        "schema_version": 1,
        "attempt_id": attempt_id,
        "work_order_id": "WO-007D-001",
        "work_order_digest": DIGEST,
        "attempt_number": number,
        "executor_id": executor_id,
        "state": "HEALTHY" if number == 1 else "REASSIGNED",
        "claim_id": claim_id,
        "prior_attempt_id": prior["attempt_id"] if prior else None,
        "prior_attempt_digest": failover.canonical_digest(prior) if prior else None,
        "failed_event_id": failed,
        "handoff_id": handoff,
        "checkpoint_id": checkpoint_id,
        "selected_executor_evidence": ["studio/evidence/selection.txt"],
        "validation_evidence": ["studio/evidence/validation.txt"],
        "created_at": "2026-08-30T10:00:00Z" if number == 1 else "2026-08-30T12:30:00Z",
    }


def handoff():
    return {
        "handoff_id": "HANDOFF-001",
        "work_order_id": "WO-007D-001",
        "claim_id": "CLAIM-001",
        "base_commit": BASE,
        "current_commit": HEAD,
        "changed_paths": ["platform/orchestration/FAILOVER.md"],
        "checks": ["focused tests PASS"],
        "blockers": ["NONE"],
        "exact_resume_action": "Validate the new claim and resume from CHECKPOINT-002.",
        "created_at": "2026-08-30T12:00:00Z",
    }


def gate():
    return {
        "gate_id": "GATE-001",
        "work_order_id": "WO-007D-001",
        "attempt_number": 2,
        "prior_state": "READY_FOR_REASSIGNMENT",
        "next_state": "REASSIGNED",
        "action": "REASSIGN",
        "approver_role": "STUDIO_OWNER",
        "approval_reference": "studio/evidence/owner-approval.txt",
        "reason": "Bounded reassignment after durable handoff.",
        "decided_at": "2026-08-30T12:15:00Z",
        "expires_at": "2026-08-31T00:00:00Z",
        "evidence_digest": "sha256:" + "d" * 64,
    }


def valid_reassignment_chain():
    first = attempt("ATTEMPT-001", 1, "EXECUTOR-01", "CLAIM-001", "CHECKPOINT-001")
    second = attempt("ATTEMPT-002", 2, "EXECUTOR-02", "CLAIM-002", "CHECKPOINT-002", first, "EVENT-003", "HANDOFF-001")
    events = []
    events.append(event("EVENT-001", "ATTEMPT-001", 1, "HEALTHY", "SUSPECTED", "TIMEOUT", "2026-08-30T11:10:00Z"))
    events.append(event("EVENT-002", "ATTEMPT-001", 1, "SUSPECTED", "PAUSED", "TIMEOUT", "2026-08-30T11:20:00Z", events[-1]))
    events.append(event("EVENT-003", "ATTEMPT-001", 1, "PAUSED", "HANDOFF_REQUIRED", "EXECUTOR_FAILURE", "2026-08-30T11:30:00Z", events[-1]))
    events.append(event("EVENT-004", "ATTEMPT-001", 1, "HANDOFF_REQUIRED", "READY_FOR_REASSIGNMENT", "EXECUTOR_FAILURE", "2026-08-30T12:05:00Z", events[-1], handoff_id="HANDOFF-001", claim_disposition="RELEASED"))
    events.append(event("EVENT-005", "ATTEMPT-002", 2, "READY_FOR_REASSIGNMENT", "REASSIGNED", "EXECUTOR_FAILURE", "2026-08-30T12:20:00Z", events[-1], checkpoint_id="CHECKPOINT-002", handoff_id="HANDOFF-001", owner_gate_id="GATE-001"))
    events.append(event("EVENT-006", "ATTEMPT-002", 2, "REASSIGNED", "RESUMED", "VALIDATION_FAILURE", "2026-08-30T12:40:00Z", events[-1], checkpoint_id="CHECKPOINT-002"))
    return {
        "schema_version": 1,
        "work_order_id": "WO-007D-001",
        "work_order_digest": DIGEST,
        "events": events,
        "attempts": [first, second],
        "claims": [claim("CLAIM-001", "ENGINEERING-01", "RELEASED"), claim("CLAIM-002", "ENGINEERING-02")],
        "handoffs": [handoff()],
        "checkpoints": [checkpoint(), checkpoint("CHECKPOINT-002")],
        "executors": [executor("EXECUTOR-01"), executor("EXECUTOR-02")],
        "owner_gates": [gate()],
    }


def valid_recovery_chain():
    chain = valid_reassignment_chain()
    prior = chain["events"][-1]
    recovered = event("EVENT-007", "ATTEMPT-002", 2, "RESUMED", "RECOVERED", "NONE", "2026-08-30T13:00:00Z", prior, checkpoint_id="CHECKPOINT-002")
    healthy = event("EVENT-008", "ATTEMPT-002", 2, "RECOVERED", "HEALTHY", "NONE", "2026-08-30T13:10:00Z", recovered, checkpoint_id="CHECKPOINT-002")
    chain["events"].extend([recovered, healthy])
    return chain


def simple_abort_chain(with_gate=True):
    first = attempt("ATTEMPT-001", 1, "EXECUTOR-01", "CLAIM-001", "CHECKPOINT-001")
    events = [event("EVENT-001", "ATTEMPT-001", 1, "HEALTHY", "SUSPECTED", "MANUAL_STOP", "2026-08-30T11:00:00Z")]
    events.append(event("EVENT-002", "ATTEMPT-001", 1, "SUSPECTED", "PAUSED", "MANUAL_STOP", "2026-08-30T11:10:00Z", events[-1]))
    abort_gate = gate()
    abort_gate.update({"attempt_number": 1, "prior_state": "PAUSED", "next_state": "ABORTED", "action": "ABORT"})
    events.append(event("EVENT-003", "ATTEMPT-001", 1, "PAUSED", "ABORTED", "MANUAL_STOP", "2026-08-30T11:20:00Z", events[-1], owner_gate_id="GATE-001" if with_gate else None))
    return {"schema_version": 1, "work_order_id": "WO-007D-001", "work_order_digest": DIGEST,
            "events": events, "attempts": [first], "claims": [claim("CLAIM-001", "ENGINEERING-01")],
            "handoffs": [], "checkpoints": [checkpoint()], "executors": [executor("EXECUTOR-01")],
            "owner_gates": [abort_gate] if with_gate else []}


class FailoverTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def test_all_valid_fixtures(self):
        failover.validate_event(self.load("valid-healthy-event.json"), AS_OF)
        failover.validate_chain(self.load("valid-reassignment-chain.json"), AS_OF)
        failover.validate_chain(self.load("valid-recovery-chain.json"), AS_OF)

    def test_all_invalid_fixtures(self):
        for path in sorted(FIXTURES.glob("invalid-*.json")):
            with self.subTest(path=path.name), self.assertRaises(failover.FailoverError):
                failover.validate_chain(self.load(path.name), AS_OF)

    def test_every_legal_edge(self):
        for prior, destinations in failover.LEGAL_TRANSITIONS.items():
            for nxt in destinations:
                failure = "NONE" if nxt in {"HEALTHY", "RECOVERED"} else "MANUAL_STOP"
                failover.validate_event(event("EVENT-EDGE", "ATTEMPT-001", 1, prior, nxt, failure, "2026-08-30T11:00:00Z"), AS_OF)

    def test_every_omitted_edge_rejected(self):
        for prior in failover.STATES:
            for nxt in failover.STATES - failover.LEGAL_TRANSITIONS[prior]:
                with self.assertRaises(failover.FailoverError):
                    failover.validate_event(event("EVENT-EDGE", "ATTEMPT-001", 1, prior, nxt, "MANUAL_STOP", "2026-08-30T11:00:00Z"), AS_OF)

    def test_attempt_four_rejected(self):
        record = attempt("ATTEMPT-004", 4, "EXECUTOR-04", "CLAIM-004", "CHECKPOINT-001")
        with self.assertRaisesRegex(failover.FailoverError, "attempt_number"):
            failover.validate_attempt(record, AS_OF)

    def test_prior_attempt_mutation_rejected(self):
        chain = valid_reassignment_chain()
        chain["attempts"][1]["prior_attempt_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(failover.FailoverError, "prior attempt digest"):
            failover.validate_chain(chain, AS_OF)

    def test_live_prior_claim_rejected(self):
        chain = valid_reassignment_chain()
        chain["claims"][0] = claim("CLAIM-001", "ENGINEERING-01")
        with self.assertRaisesRegex(failover.FailoverError, "claim remains live"):
            failover.validate_chain(chain, AS_OF)

    def test_same_claim_reassignment_rejected(self):
        chain = valid_reassignment_chain()
        chain["attempts"][1]["claim_id"] = "CLAIM-001"
        with self.assertRaisesRegex(failover.FailoverError, "new claim"):
            failover.validate_chain(chain, AS_OF)

    def test_missing_handoff_rejected(self):
        chain = valid_reassignment_chain()
        chain["handoffs"] = []
        with self.assertRaises(failover.FailoverError):
            failover.validate_chain(chain, AS_OF)

    def test_unauthorized_reassignment_rejected(self):
        chain = valid_reassignment_chain()
        chain["events"][4]["owner_gate_id"] = None
        chain["owner_gates"] = []
        with self.assertRaisesRegex(failover.FailoverError, "owner gate"):
            failover.validate_chain(chain, AS_OF)

    def test_unauthorized_abort_rejected(self):
        with self.assertRaisesRegex(failover.FailoverError, "owner gate"):
            failover.validate_chain(simple_abort_chain(False), AS_OF)

    def test_authorized_abort_accepted(self):
        failover.validate_chain(simple_abort_chain(True), AS_OF)

    def test_expired_gate_rejected(self):
        chain = valid_reassignment_chain()
        chain["owner_gates"][0]["expires_at"] = "2026-08-30T12:16:00Z"
        with self.assertRaisesRegex(failover.FailoverError, "expired"):
            failover.validate_chain(chain, AS_OF)

    def test_unused_gate_rejected(self):
        chain = valid_reassignment_chain()
        extra = copy.deepcopy(chain["owner_gates"][0])
        extra["gate_id"] = "GATE-002"
        chain["owner_gates"].append(extra)
        with self.assertRaisesRegex(failover.FailoverError, "unused"):
            failover.validate_chain(chain, AS_OF)

    def test_missing_checkpoint_resume_rejected(self):
        chain = valid_reassignment_chain()
        chain["checkpoints"][1]["status"] = "MISSING"
        with self.assertRaisesRegex(failover.FailoverError, "safe checkpoint"):
            failover.validate_chain(chain, AS_OF)

    def test_validation_does_not_mutate(self):
        chain = valid_recovery_chain()
        before = copy.deepcopy(chain)
        failover.validate_chain(chain, AS_OF)
        self.assertEqual(before, chain)

    def test_failed_validation_does_not_mutate(self):
        chain = valid_reassignment_chain()
        chain["events"][1]["next_state"] = "RECOVERED"
        before = copy.deepcopy(chain)
        with self.assertRaises(failover.FailoverError):
            failover.validate_chain(chain, AS_OF)
        self.assertEqual(before, chain)

    def test_explanation_is_deterministic(self):
        chain = valid_recovery_chain()
        self.assertEqual(failover.explain_failover(chain, AS_OF), failover.explain_failover(chain, AS_OF))
        self.assertFalse(failover.explain_failover(chain, AS_OF)["writes_performed"])

    def test_simulation_is_read_only(self):
        chain = valid_recovery_chain()
        before = copy.deepcopy(chain)
        last = chain["events"][-1]
        proposal = event(
            "EVENT-009", "ATTEMPT-002", 2, "HEALTHY", "SUSPECTED",
            "TIMEOUT", "2026-08-30T13:20:00Z", last,
            checkpoint_id="CHECKPOINT-002",
        )
        preview = failover.simulate_transition(chain, proposal, AS_OF)
        self.assertTrue(preview["accepted"])
        self.assertFalse(preview["writes_performed"])
        self.assertEqual(before, chain)

    def test_cli_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chain.json"
            path.write_text(json.dumps(valid_recovery_chain()), encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(0, failover.main(["validate-chain", "--input", str(path), "--as-of", AS_OF]))
            self.assertIn("work_order_id", out.getvalue())
            path.write_text("{}", encoding="utf-8")
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(1, failover.main(["validate-chain", "--input", str(path), "--as-of", AS_OF]))

    def test_no_network_or_subprocess(self):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network call")), \
             mock.patch.object(subprocess, "run", side_effect=AssertionError("subprocess call")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("subprocess call")):
            failover.validate_chain(valid_recovery_chain(), AS_OF)


if __name__ == "__main__":
    unittest.main()
