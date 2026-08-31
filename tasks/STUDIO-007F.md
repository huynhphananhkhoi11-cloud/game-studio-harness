# STUDIO-007F - Provider-neutral executor adapter

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent: STUDIO-007

Dependencies: STUDIO-007A through STUDIO-007E are accepted, implemented, reviewed, merged, and closed out.

Canonical implementation contract: `tasks/STUDIO-007F-IMPLEMENTATION.md`

## Goal

Define one narrow, provider-neutral request/result boundary between validated orchestration evidence and an executor adapter without granting execution, approval, merge, publication, credential, network, or spending authority.

## Accepted v1.0 boundary

- An adapter request contains a validated work-order identity, attempt identity, immutable artifact identity, declared capability, safe input references, correlation ID, and explicit `as_of` time.
- An adapter result contains the matching identity, one terminal status, safe output/evidence references, bounded usage counters, an error class, an optional durable-handoff reference, and the same correlation ID.
- Exact fields are allowlisted; unknown and provider-specific fields fail closed.
- Adapter records are evidence. They do not authenticate an actor, approve a gate, expand scope, select a successor, merge, publish, deploy, or authorize spend.

## Accepted adapters

- `manual`: validates and normalizes a result supplied by a human-controlled process. It never executes the work itself.
- `fake`: returns deterministic fixture-driven outcomes for tests. It never sleeps, reads the system clock, calls a provider, or performs external I/O.

No other adapter type is authorized in v1.0.

## Accepted safety boundary

- Python standard library only.
- Supplied evidence and caller-supplied time only.
- No network, provider SDK, provider/model name, account, credential, token, secret, subprocess, Git mutation, filesystem mutation outside explicit test fixtures, billing, or nonzero cost.
- Secret-like keys and credential-bearing values are rejected rather than redacted into acceptance.
- Validation must leave supplied evidence byte-for-byte unchanged.

## Real providers

A real provider is not a configuration change to v1.0. Each future provider requires a separately owner-accepted contract, threat review, credential plan, budget and cost controls, focused tests, retained regression tests, operational rollback, and explicit merge approval.

## Implementation boundary

Implementation may begin only after this contract Pull Request merges. It may create only the paths listed in section 4 of `tasks/STUDIO-007F-IMPLEMENTATION.md` and materially update the four STUDIO-007F memory records.

## Failure and rollback

The implementation fails if an adapter can use undeclared capability, change orchestration identity, accept secrets, invoke an external system, create nonzero usage cost, fabricate authorization, or produce nondeterministic fake results.

Rollback is an authorized revert of later STUDIO-007F implementation. This contract and memory remain evidence; STUDIO-007A through STUDIO-007E remain operational.

## Owner decisions accepted

- The normalized request/result adapter boundary is accepted.
- v1.0 contains only deterministic `manual` and `fake` adapters.
- No real provider, SDK, account, credential, network access, or cost is authorized.
- Every future real provider needs its own contract, threat review, credential plan, budget, tests, and rollback.

Studio Owner acceptance date: 2026-08-31.
