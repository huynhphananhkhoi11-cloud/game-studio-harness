# STUDIO-007D — Simulated failover state machine

Status: `PROPOSED — NOT ACCEPTED — NOT IMPLEMENTED`

Parent: `STUDIO-007`

Dependency: accepted and verified `STUDIO-007A` through `STUDIO-007C`

Primary owner: Platform Studio

## Goal

Prove that interrupted or failed work can be paused, inspected, reassigned, and resumed from durable evidence without connecting a real backup provider.

## Proposed contract

Failover is a state transition, not a hidden retry. Proposed states are `HEALTHY`, `SUSPECTED`, `PAUSED`, `HANDOFF_REQUIRED`, `READY_FOR_REASSIGNMENT`, `REASSIGNED`, `RESUMED`, `RECOVERED`, and `ABORTED`.

Each event records work-order ID, attempt, prior and next state, failure class, detector, evidence, checkpoint, claim disposition, selected recovery action, and Owner-gate requirement. Reassignment creates a new attempt and may not rewrite prior evidence.

## Proposed future implementation scope

- `platform/orchestration/FAILOVER.md`
- `platform/orchestration/schemas/failover-event.schema.json`
- `platform/orchestration/schemas/attempt-record.schema.json`
- `platform/orchestration/fixtures/007d/`
- focused state-machine validator and tests approved in the implementation contract

## Out of scope

- Real provider failover, health polling, network monitoring, or automatic retry.
- Credential switching or paid fallback capacity.
- Destructive worktree cleanup or history rewriting.
- Treating a failed QA gate as successful execution.

## Required tests for a future implementation

- Legal transition table coverage and illegal-transition rejection.
- Timeout, executor failure, malformed output, and manual-stop simulations.
- New-attempt creation with immutable prior evidence.
- Recovery from the last valid durable handoff.
- Abort when no safe checkpoint or eligible executor exists.

## Failure and rollback

If failover loses evidence, reuses a live claim unsafely, hides attempts, or advances without a valid checkpoint, the contract fails. Rollback removes only 007D artifacts; work remains manually recoverable using 007C handoffs.

## Owner decisions required

- Accept failure classes and transition authority.
- Set retry/attempt ceilings.
- Decide which transitions require an explicit Owner gate.
