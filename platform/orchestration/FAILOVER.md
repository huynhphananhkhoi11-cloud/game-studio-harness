# Simulated failover v1.0

STUDIO-007D validates immutable failover evidence. It does not execute work,
retry a provider, reassign an executor, mutate Git, inspect a worktree, or grant
authority. All time-sensitive decisions use caller-supplied UTC `--as-of`.

## States

The accepted states and edges are:

- `HEALTHY -> SUSPECTED`
- `SUSPECTED -> HEALTHY | PAUSED`
- `PAUSED -> RESUMED | HANDOFF_REQUIRED | ABORTED`
- `HANDOFF_REQUIRED -> READY_FOR_REASSIGNMENT | ABORTED`
- `READY_FOR_REASSIGNMENT -> REASSIGNED | ABORTED`
- `REASSIGNED -> RESUMED | ABORTED`
- `RESUMED -> SUSPECTED | RECOVERED | ABORTED`
- `RECOVERED -> HEALTHY`
- `ABORTED` is terminal.

The accepted failure classes are `TIMEOUT`, `EXECUTOR_FAILURE`,
`MALFORMED_OUTPUT`, `VALIDATION_FAILURE`, `MANUAL_STOP`, and
`CHECKPOINT_MISSING`. Restoration to `HEALTHY` or `RECOVERED` uses `NONE`.

## Safety invariants

- Attempts begin at 1, remain consecutive and never exceed 3.
- Each later attempt cites the canonical digest of the prior attempt.
- Each event after the first cites the canonical digest of the prior event.
- Reassignment requires a new claim, safe checkpoint, durable handoff, eligible
  executor evidence, and non-live prior claim.
- `READY_FOR_REASSIGNMENT -> REASSIGNED` and every `ABORTED` transition require
  an unexpired `STUDIO_OWNER` gate.
- Resume after recorded `CHECKPOINT_MISSING` requires new safe-checkpoint
  evidence and an `EVIDENCE_RESUME` Owner gate.
- Duplicate, expired, mismatched, unauthorized, or unused gates fail closed.

Canonical digests are SHA-256 over compact JSON with sorted keys and ASCII
escaping, prefixed by `sha256:`.

## CLI

```text
python -m scripts.orchestration_failover validate-event --input EVENT.json --as-of 2026-08-30T18:00:00Z
python -m scripts.orchestration_failover validate-attempt --input ATTEMPT.json --as-of 2026-08-30T18:00:00Z
python -m scripts.orchestration_failover validate-chain --input CHAIN.json --as-of 2026-08-30T18:00:00Z
python -m scripts.orchestration_failover simulate-transition --chain CHAIN.json --proposal EVENT.json --as-of 2026-08-30T18:00:00Z
python -m scripts.orchestration_failover explain-failover --input CHAIN.json --as-of 2026-08-30T18:00:00Z
```

Every command is deterministic and read-only. Invalid evidence exits nonzero.
