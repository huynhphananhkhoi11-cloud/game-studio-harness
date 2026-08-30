# STUDIO-007D - Simulated failover state machine

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent: STUDIO-007

Dependencies: accepted, implemented, reviewed, merged, and retained STUDIO-007A through STUDIO-007C

Primary owner: Platform Studio

Canonical implementation contract: tasks/STUDIO-007D-IMPLEMENTATION.md

## Goal

Prove that interrupted or failed work can be paused, inspected, reassigned, resumed, recovered, or aborted from immutable evidence without connecting a real backup provider.

## Accepted contract

Failover is an explicit state transition, never a hidden retry. The accepted states are HEALTHY, SUSPECTED, PAUSED, HANDOFF_REQUIRED, READY_FOR_REASSIGNMENT, REASSIGNED, RESUMED, RECOVERED, and ABORTED.

Accepted failure classes are TIMEOUT, EXECUTOR_FAILURE, MALFORMED_OUTPUT, VALIDATION_FAILURE, MANUAL_STOP, and CHECKPOINT_MISSING.

Every event records work-order and attempt identity, prior and next state, failure class, detector, evidence, checkpoint and handoff references, claim disposition, recovery action, Owner-gate evidence when required, explicit observation time, and immutable digest inputs.

Attempts start at 1 and may not exceed 3. Reassignment creates the next immutable attempt and may not rewrite prior attempts. Failure of attempt 3 blocks any fourth attempt and requires an Owner-gated ABORTED decision or a separately accepted amendment.

## Transition authority

- Detection and safe pausing may be recorded without an Owner gate.
- READY_FOR_REASSIGNMENT requires a valid durable handoff, a safe checkpoint, an eligible executor record, and a non-live prior writer claim.
- READY_FOR_REASSIGNMENT to REASSIGNED requires explicit STUDIO_OWNER approval.
- A RESUMED transition after previously missing or ambiguous evidence requires explicit STUDIO_OWNER approval plus newly cited valid evidence. Owner approval cannot waive the safe-checkpoint requirement.
- Any transition to ABORTED requires explicit STUDIO_OWNER approval.
- RECOVERED requires deterministic validation evidence; it is not equivalent to QA acceptance or merge approval.

## Approved implementation boundary

The future implementation may create only the sixteen paths listed in section 4 of tasks/STUDIO-007D-IMPLEMENTATION.md, plus material-checkpoint updates to the four-record STUDIO-007D memory package.

Implementation must use Python standard library tooling, deterministic fixtures, explicit as_of input, read-only validation, and immutable prior-event evidence. It must not inspect time implicitly, invoke Git, execute work, contact a provider, or mutate evidence.

## Out of scope

- Real provider failover, health polling, network monitoring, automatic retry, automatic reassignment, or runtime execution.
- Credential switching, paid fallback capacity, dependency installation, hosted services, publication, or deployment.
- Destructive worktree cleanup, history rewriting, claim reuse, or mutation of a prior attempt.
- Treating RECOVERED as QA PASS, integration approval, merge authority, project truth, or publication authority.
- Activating STUDIO-007E or STUDIO-007F.

## Required behavior

- Accept every legal transition and reject every illegal transition deterministically.
- Preserve append-only event and attempt lineage.
- Reject a fourth attempt, hidden retry, stale handoff, live-claim reassignment, missing safe checkpoint, and unsupported failure class.
- Enforce Owner gates for reassignment, evidence-exception resume, and abort.
- Require a new claim and new attempt identity for reassignment.
- Prove invalid inputs leave all source evidence byte-for-byte unchanged.

## Failure and rollback

The contract fails if failover loses evidence, hides an attempt, creates attempt 4, reuses a live claim, bypasses a required Owner gate, resumes without a safe checkpoint, mutates prior evidence, or performs a real provider, Git, credential, network, execution, deletion, publication, or paid action.

Rollback removes only the later STUDIO-007D implementation through an authorized revert. Accepted contracts and memory history remain evidence. Work remains manually recoverable using STUDIO-007C handoffs.

## Owner decisions accepted

- Failure classes: TIMEOUT, EXECUTOR_FAILURE, MALFORMED_OUTPUT, VALIDATION_FAILURE, MANUAL_STOP, CHECKPOINT_MISSING.
- Maximum attempts per work order: 3.
- Owner gate required for REASSIGNED, evidence-exception RESUMED, and ABORTED.
- Detection and pausing remain evidence-only and do not execute recovery.

Studio Owner acceptance date: 2026-08-30.
