# STUDIO-008-IMPLEMENTATION - Zero-cost system pilot v1.0

## 1. Purpose

Authorize one deterministic, read-only validation implementation for the six STUDIO-008 pilot scenarios. This file is an implementation contract, not pilot runtime code.

The contract Pull Request must merge before any implementation path below is created.

## 2. Identity and authority

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Final gate authority: Studio Owner
- Contract branch: agent/studio-008-contract
- Planned implementation branch: agent/studio-008-zero-cost-pilot
- Memory package: studio/memory/tasks/STUDIO-008/
- Required baseline: reconciled STUDIO-007 milestone merge 31e912ea19d6308b84be2a036b98ec1989913cd0

This authorization is limited to Manual/Fake zero-cost evidence. It does not authorize a provider, credential, network, spend, deployment, or release.

## 3. Canonical pilot bundle

The validator receives a supplied JSON bundle and explicit ISO 8601 UTC as_of. It never reads the system clock, invokes Git, mutates a worktree, executes orchestration, performs network access, loads credentials, or calls a provider.

The bundle contains stable scenario IDs, work-order and attempt lineage, queue and dispatch references, writer claims, worktree and handoff evidence, failover evidence, gates, trace, budgets, adapter results, rollback proof, expected outcome, and canonical SHA-256 digests.

All fields are allowlisted. Missing/extra fields, duplicate IDs, unsupported versions, invalid chronology, mismatched heads, broken lineage, unsafe paths, secret-like values, ambiguous evidence, or altered digests fail closed.

## 4. Exact implementation path boundary

The implementation Pull Request may create exactly these twenty paths:

1. platform/orchestration/PILOT_ACCEPTANCE.md
2. platform/orchestration/schemas/pilot-bundle.schema.json
3. platform/orchestration/fixtures/008/valid-pilot-bundle.json
4. platform/orchestration/fixtures/008/valid-p01-research-handoff.json
5. platform/orchestration/fixtures/008/valid-p02-engineering-work.json
6. platform/orchestration/fixtures/008/valid-p03-simulated-failover.json
7. platform/orchestration/fixtures/008/valid-p04-writer-conflict.json
8. platform/orchestration/fixtures/008/valid-p05-qa-correction.json
9. platform/orchestration/fixtures/008/valid-p06-owner-gate-approve.json
10. platform/orchestration/fixtures/008/valid-p06-owner-gate-reject.json
11. platform/orchestration/fixtures/008/invalid-missing-scenario.json
12. platform/orchestration/fixtures/008/invalid-nondeterministic-replay.json
13. platform/orchestration/fixtures/008/invalid-unauthorized-write.json
14. platform/orchestration/fixtures/008/invalid-duplicate-writer.json
15. platform/orchestration/fixtures/008/invalid-duplicate-output.json
16. platform/orchestration/fixtures/008/invalid-gate-bypass.json
17. platform/orchestration/fixtures/008/invalid-incomplete-handoff-trace.json
18. platform/orchestration/fixtures/008/invalid-provider-or-spend.json
19. scripts/orchestration_pilot.py
20. tests/test_orchestration_pilot.py

It may materially update only these four existing contract memory paths:

21. studio/memory/tasks/STUDIO-008/TASK.md
22. studio/memory/tasks/STUDIO-008/STATE.md
23. studio/memory/tasks/STUDIO-008/WORKLOG.md
24. studio/memory/tasks/STUDIO-008/RESUME.md

Maximum changed paths: 24. Renames, generated files, dependency changes, workflow changes, and changes outside this list are prohibited.

## 5. Required validation behavior

- Validate P01 through P06 independently and as one canonical bundle.
- Require exact work-order, attempt, correlation, artifact, gate, budget, and digest lineage.
- Require CLAIM_SCOPE_CONFLICT for the deliberate overlap in P04.
- Require a new attempt and new-head gates after P05 correction.
- Require both P06 dispositions and prove no non-owner component can decide either path.
- Canonicalize JSON before hashing and prove key-order-stable replay.
- Reject secret-like keys or values rather than silently redacting them.
- Leave all supplied evidence byte-for-byte unchanged on success and failure.

## 6. Evidence and acceptance

Focused tests must cover all valid and invalid fixtures, canonical replay, chronology, lineage, immutability, zero-cost enforcement, zero-network behavior, role authority, and rollback proof. The full retained suite must also pass.

Acceptance requires the thresholds in tasks/STUDIO-008.md and independent QA plus Review and Integration approval on one immutable head. The Studio Owner separately decides whether to merge and later records one allowed disposition.

## 7. Prohibited behavior

The implementation must not import provider SDKs, read environment credentials, open sockets, make HTTP requests, spawn subprocesses, invoke Git, modify files, dispatch work, claim paths, retry, fail over, merge, delete, publish, deploy, or spend money.

## 8. Rollback

Rollback is an authorized revert of the STUDIO-008 implementation commit and removal of only the twenty implementation paths. The contract and memory remain audit evidence. All STUDIO-001 through STUDIO-007 capabilities remain retained.
