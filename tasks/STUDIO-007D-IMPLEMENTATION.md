# STUDIO-007D-IMPLEMENTATION - Simulated failover state machine v1.0

## 1. Purpose

Authorize one bounded, zero-cost implementation of deterministic failover-event, attempt-lineage, and simulated-transition validators.

This document is an implementation contract. It does not implement runtime behavior. This contract-only Pull Request must merge before any implementation path in section 4 is created.

## 2. Approval and identity

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-08-30
- Parent umbrella: tasks/STUDIO-007.md
- Parent capability contract: tasks/STUDIO-007D.md
- Dependency A: STUDIO-007A implementation retained from PR #18
- Dependency B: STUDIO-007B implementation retained from PR #20
- Dependency C implementation: PR #23, merge commit b42340c0bcbd8f8152509b1d9baf3f7e39c80a30
- Verified dependency baseline: PR #24, merge commit 4a963abda65395034a4c6062e462f24e697a8f28
- Contract branch: agent/studio-007d-contract
- Planned implementation branch: agent/studio-007d-simulated-failover
- Platform memory package: studio/memory/tasks/STUDIO-007D/

This authorization does not activate STUDIO-007E or STUDIO-007F.

## 3. Accepted implementation decisions

### 3.1 Canonical records

- JSON is canonical for immutable failover events and attempt records.
- Every record requires schema version, stable ID, work-order identity and digest, attempt number, state, explicit UTC times, evidence references, and SHA-256 digest inputs.
- Validation requires explicit ISO 8601 UTC as_of. The implementation must not consult the system clock.
- Records are evidence only and cannot authenticate an actor, executor, detector, approver, provider, or repository state.

### 3.2 States and transitions

Accepted states are HEALTHY, SUSPECTED, PAUSED, HANDOFF_REQUIRED, READY_FOR_REASSIGNMENT, REASSIGNED, RESUMED, RECOVERED, and ABORTED.

The legal transition graph is:

- HEALTHY to SUSPECTED
- SUSPECTED to HEALTHY or PAUSED
- PAUSED to RESUMED, HANDOFF_REQUIRED, or ABORTED
- HANDOFF_REQUIRED to READY_FOR_REASSIGNMENT or ABORTED
- READY_FOR_REASSIGNMENT to REASSIGNED or ABORTED
- REASSIGNED to RESUMED or ABORTED
- RESUMED to SUSPECTED, RECOVERED, or ABORTED
- RECOVERED to HEALTHY
- ABORTED is terminal

No omitted transition is legal. One event represents exactly one transition and cites the prior event digest when a prior event exists.

### 3.3 Failure classes

Accepted failure classes are TIMEOUT, EXECUTOR_FAILURE, MALFORMED_OUTPUT, VALIDATION_FAILURE, MANUAL_STOP, and CHECKPOINT_MISSING.

HEALTHY restoration and RECOVERED transitions may use NONE as the failure class. All other transitions require one accepted failure class appropriate to their evidence. Free-form failure classes fail closed.

### 3.4 Attempt ceiling and lineage

- Initial work uses attempt 1.
- Reassignment alone creates attempt 2 or 3.
- Attempt numbers are consecutive and immutable.
- Each later attempt cites the prior attempt ID and digest, failed event ID, durable handoff ID, new writer claim ID, and selected executor evidence.
- Attempt 4 is always rejected in v1.0.
- Failure of attempt 3 prohibits further reassignment. The chain remains paused or handoff-required until an Owner-gated ABORTED event is recorded.
- Same-attempt resume is permitted only from PAUSED when the existing claim and safe checkpoint remain valid. It is never a hidden new attempt.

### 3.5 Handoff, checkpoint, and claim safety

- READY_FOR_REASSIGNMENT requires a STUDIO-007C durable handoff with explicit matching work order, base/current commits, changed paths, checks, blockers, and exact resume action.
- A safe checkpoint must be present, content-addressed, and cited. CHECKPOINT_MISSING may never advance to READY_FOR_REASSIGNMENT or RESUMED until valid checkpoint evidence is added.
- The prior claim must be RELEASED or explicitly expired at caller-supplied as_of. Expiry does not grant reassignment authority.
- Reassignment requires a new claim for the new executor and may not reuse the prior claim ID.
- Validation uses supplied evidence only and does not invoke Git or inspect a worktree.

### 3.6 Owner gates

- READY_FOR_REASSIGNMENT to REASSIGNED requires a bounded STUDIO_OWNER gate record.
- Any transition to ABORTED requires a bounded STUDIO_OWNER gate record.
- RESUMED requires an Owner gate when the chain previously recorded missing or ambiguous mandatory evidence. The gate must cite newly supplied valid evidence and cannot waive the safe checkpoint, claim, handoff, or attempt ceiling.
- Gate records require action, affected work order and attempt, exact transition, reason, approval reference, decided time, expiry time, and evidence digest.
- Owner-gate evidence cannot authenticate the named approver or grant merge, budget, publication, or project authority.

### 3.7 Safety

- Python standard library only; no installation or dependency.
- Schemas document normative shapes; the CLI enforces the accepted semantic subset.
- All commands are read-only and deterministic.
- No network, provider, credential, subprocess, Git, deletion, filesystem-worktree, execution, automatic retry, automatic reassignment, publication, or paid action.
- Invalid input fails closed with nonzero exit status and no source mutation.

## 4. Exact implementation scope

After the contract-only Pull Request merges, implementation may create exactly:

1. platform/orchestration/FAILOVER.md
2. platform/orchestration/schemas/failover-event.schema.json
3. platform/orchestration/schemas/attempt-record.schema.json
4. platform/orchestration/fixtures/007d/valid-healthy-event.json
5. platform/orchestration/fixtures/007d/valid-reassignment-chain.json
6. platform/orchestration/fixtures/007d/valid-recovery-chain.json
7. platform/orchestration/fixtures/007d/invalid-illegal-transition.json
8. platform/orchestration/fixtures/007d/invalid-fourth-attempt.json
9. platform/orchestration/fixtures/007d/invalid-missing-handoff.json
10. platform/orchestration/fixtures/007d/invalid-unsafe-live-claim.json
11. platform/orchestration/fixtures/007d/invalid-unauthorized-reassignment.json
12. platform/orchestration/fixtures/007d/invalid-unauthorized-abort.json
13. platform/orchestration/fixtures/007d/invalid-mutated-prior-attempt.json
14. platform/orchestration/fixtures/007d/invalid-checkpoint-missing-resume.json
15. scripts/orchestration_failover.py
16. tests/test_orchestration_failover.py

During implementation, only material-checkpoint updates may modify the existing four records under studio/memory/tasks/STUDIO-007D/.

No other file may be created, modified, deleted, renamed, or moved without an accepted amendment. STUDIO-007A through STUDIO-007C implementation paths remain unchanged.

## 5. Event validation requirements

Reject missing or extra fields, unsupported schema versions, duplicate IDs, invalid digests, invalid chronology, implicit clock use, unsupported failure classes, illegal transitions, mismatched work-order identity, nonconsecutive lineage, stale evidence, unsafe text, credential-bearing content, and mutable prior-event claims.

## 6. Chain and attempt requirements

- Validate the entire chain from supplied immutable records.
- Require exactly one initial attempt 1.
- Reject gaps, duplicate attempts, attempt 4, prior-attempt mutation, digest mismatch, hidden retry, and reassignment without a new claim.
- Reject transition into READY_FOR_REASSIGNMENT without a safe checkpoint, durable handoff, eligible executor evidence, and safe prior-claim disposition.
- Reject a resumed or recovered claim that lacks deterministic validation evidence.

## 7. Owner-gate requirements

- Enforce STUDIO_OWNER for reassignment, evidence-exception resume, and abort.
- Reject expired, transition-mismatched, work-order-mismatched, attempt-mismatched, malformed, duplicate, unauthorized, or unused gate evidence.
- Never treat a gate as authentication or permission to bypass mandatory safety evidence.

## 8. Required CLI behavior

The CLI must provide bounded commands equivalent to:

- validate-event: validate one event at explicit --as-of.
- validate-attempt: validate one attempt and its cited evidence.
- validate-chain: validate full event and attempt lineage.
- simulate-transition: validate one proposed next transition and print a derived preview without writing evidence.
- explain-failover: print bounded state, attempt, evidence, gates, blockers, and next safe action without mutation.

All commands return nonzero on invalid input.

## 9. Required tests

Focused tests must prove:

- every valid fixture passes and every invalid fixture fails for its intended reason;
- every legal edge is accepted and every omitted edge is rejected;
- attempts are consecutive and attempt 4 fails;
- prior events and attempts remain immutable;
- missing or stale handoff, checkpoint, claim, executor, or validation evidence fails closed;
- live-claim reuse and same-claim reassignment fail;
- reassignment, evidence-exception resume, and abort enforce the correct Owner gate;
- malformed, expired, unauthorized, duplicate, or unused gate evidence fails;
- attempt-3 failure cannot create attempt 4;
- CHECKPOINT_MISSING cannot resume without newly supplied valid checkpoint evidence;
- simulation and explanation are deterministic and read-only;
- failed validation does not mutate any input or fixture;
- tests make no network, subprocess, Git, provider, credential, execution, deletion, publication, or paid calls.

Required repository checks:

python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_orchestration_queue -v
python -m unittest tests.test_orchestration_dispatch -v
python -m unittest tests.test_orchestration_handoff -v
python -m unittest tests.test_orchestration_failover -v
python -m unittest discover -s tests -p "test*.py" -v

GitHub Actions Rules CI must pass on push and pull-request events.

## 10. Acceptance criteria

- Contract-only PR changes exactly tasks/STUDIO-007D.md, this contract, and the four-record STUDIO-007D memory package.
- Contract-only PR merges before implementation begins.
- Implementation PR changes only the sixteen section 4 paths and material-checkpoint updates to the four memory records.
- No dependency, network, provider, credential, subprocess, Git automation, execution, external runtime, workflow, or nonzero spending is added.
- All positive, negative, transition, lineage, attempt-ceiling, handoff, checkpoint, claim, gate, no-mutation, and no-network tests pass.
- Retained 007A, 007B, and 007C tests, full suite, whitespace check, and Rules CI pass.
- Independent QA returns PASS and Review & Integration returns APPROVE against one immutable implementation head.
- Studio Owner makes the final merge decision.

## 11. Rollback

Rollback is an authorized revert of the later implementation commit. The sixteen implementation files may be removed together only by an authorized revert; contracts and memory history remain evidence.

After rollback, recovery returns to STUDIO-007C durable handoffs and manual Studio Owner coordination. STUDIO-007A through STUDIO-007C remain operational.

## 12. Explicit non-goals

This contract does not authorize real failover, provider calls, model calls, credentials, network access, external code, dependency installation, automatic retry, automatic reassignment, Git or worktree mutation, execution, deletion, publication, deployment, nonzero spending, STUDIO-007E, or STUDIO-007F.

## 13. Workflow after contract merge

1. Reconcile the merged contract and memory package against current main.
2. Create agent/studio-007d-simulated-failover from the verified contract merge.
3. Acquire one verified ENGINEERING-01 writer claim.
4. Create only the sixteen implementation paths in section 4.
5. Run data, retained 007A/007B/007C, focused 007D, full-suite, and whitespace checks.
6. Obtain independent QA and Review & Integration verdicts on one immutable head.
7. Studio Owner decides whether to merge the implementation.
