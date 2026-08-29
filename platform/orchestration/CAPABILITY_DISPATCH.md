# Capability Registry & Manual Dispatcher v1.0

STUDIO-007B records evidence-backed executor capabilities and one explicit
Studio Owner dispatch decision. Registry data and role labels are claims, not
authentication, permission, execution, approval, or merge authority.

## Inputs

- one validated capability registry;
- one STUDIO-007A work-order snapshot in `CLAIMABLE` state;
- one human-authored dispatch decision;
- one explicit ISO 8601 UTC `as_of` timestamp.

The validator never reads the wall clock. A decision is valid only when
`decided_at <= as_of < expires_at`.

## Eligible selection

The selected record must be an existing `INTERNAL_ROLE` with:

- `ELIGIBLE` eligibility;
- `AVAILABLE` availability;
- `ZERO_COST` cost class;
- `EVIDENCE_VERIFIED` trust, or `RESTRICTED` trust whose constraints are
  explicitly satisfied by the work order;
- every required capability, input type, and output type.

External candidates and records marked `REFERENCE`, `NOT_INSTALLED`,
`NO_DECISION`, `ADAPT_PENDING`, or `EVIDENCE_PENDING` cannot be selected.

## Authority boundary

Only a decision with `dispatcher_role: STUDIO_OWNER` is active in v1.0.
`PRODUCER-01` may prepare non-binding alternatives but cannot activate a
selection. The decision must include considered alternatives, a reason,
evidence references, an immutable work-order digest, and an expiry.

A valid dispatch does not mutate the Producer Queue, move a work order to
`CLAIMED`, create a worktree, call a model, execute an agent, or perform Git
operations. Those behaviors remain outside STUDIO-007B.

## CLI

```text
validate-registry  validate registry claims without mutation
validate-decision  validate a manual decision at explicit --as-of
dispatch           atomically record one validated decision
explain            print selection, alternatives, reason, evidence, and expiry
```

Run `python scripts/orchestration_dispatch.py --help` for arguments.
The implementation uses only the Python standard library and performs no
network, provider, credential, deletion, ranking, or paid action.
