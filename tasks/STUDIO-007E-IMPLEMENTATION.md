# STUDIO-007E-IMPLEMENTATION - Gate, trace, quota and budget v1.0

## 1. Purpose

Authorize one bounded zero-cost implementation of deterministic gate-result, append-only trace, and quota-budget validators.

This is an implementation contract, not runtime code. This contract-only Pull Request must merge before any implementation path in section 4 is created.

## 2. Approval and identity

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-08-30
- Parent umbrella: tasks/STUDIO-007.md
- Parent capability contract: tasks/STUDIO-007E.md
- Verified dependency baseline: STUDIO-007D closeout PR #27, merge commit 37da4427c4d0f82ce6ec550321c0ad92ac874a73
- Contract branch: agent/studio-007e-contract
- Planned implementation branch: agent/studio-007e-gate-trace-budget
- Memory package: studio/memory/tasks/STUDIO-007E/

This authorization does not activate STUDIO-007F.

## 3. Accepted decisions

### 3.1 Canonical evidence

- JSON is canonical for gate results, trace events, quota-budget records, observed usage, and bounded Owner amendments.
- Schema version 1, stable IDs, work-order and attempt identity, explicit UTC time, evidence references, artifact identity, and SHA-256 digest inputs are mandatory where applicable.
- Validation receives explicit ISO 8601 UTC as_of and never consults the system clock.
- Records are evidence only and do not authenticate actors, evaluators, approvers, repositories, providers, or billing systems.
- Missing or extra fields, duplicate IDs, invalid time, invalid digest, unsupported enum, or mismatched identity fail closed.

### 3.2 Gate types and authority

Accepted gate types:

- SCOPE_BOUNDARY
- EVIDENCE_INTEGRITY
- QUOTA_BUDGET
- SECRET_SAFETY
- FOCUSED_TESTS
- RETAINED_REGRESSION
- QA_ACCEPTANCE
- REVIEW_INTEGRATION
- OWNER_DECISION

Authority mapping:

- ENGINEERING may evaluate the first six technical gates.
- QA alone may issue QA_ACCEPTANCE.
- REVIEW_INTEGRATION alone may issue REVIEW_INTEGRATION.
- STUDIO_OWNER alone may issue OWNER_DECISION.
- evaluator_id is separate from evaluator_role and does not authenticate itself.
- No evaluator may substitute a gate or convert PASS into merge authority.

Every work order requires SCOPE_BOUNDARY, EVIDENCE_INTEGRITY, QUOTA_BUDGET, and SECRET_SAFETY. Implementation adds FOCUSED_TESTS and RETAINED_REGRESSION. Repository-changing work adds QA_ACCEPTANCE and REVIEW_INTEGRATION on one immutable head before the separate Owner decision.

### 3.3 Gate-result semantics

A result records gate ID, work order, attempt, gate type, evaluator ID/role, evidence, artifact identity, verdict, bounded reasons, evaluated_at, and ordered prior-gate identity when present.

Verdicts are PASS, FAIL, and PAUSE. PASS applies only to one gate. FAIL marks invalid or insufficient evidence. PAUSE marks a ceiling or safe stop. Results are append-only and content-addressed. Later results cannot mutate or retroactively authorize earlier results.

Artifact identity requires repository identity, forty-hex commit SHA, applicable changed-path references, and SHA-256 artifact digest. QA, integration, and Owner evidence must bind to the same immutable head. Validation never invokes Git.

### 3.4 Trace semantics

- One work-order execution uses one stable correlation ID.
- Sequence starts at 1 and is consecutive.
- The first event has no prior identity; later events cite exact prior event ID and canonical digest.
- Time is nondecreasing and not later than supplied as_of.
- Events record actor ID/role, capability, prior/next state, safe references, outcome, gate IDs, quota ID, observed_at, and artifact identity.
- Transitions must correspond to supplied accepted orchestration evidence; 007E does not invent queue, dispatch, claim, handoff, or failover transitions.
- Gaps, forks, cycles, altered history, broken correlation, mismatched attempts, future evidence, or late authorization fail closed.

### 3.5 Default ceilings

- cost_class: ZERO_COST
- monetary_budget_minor_units: 0
- monetary_spend_minor_units: 0
- max_attempts: 3
- max_elapsed_seconds: 7200
- max_changed_paths: 25
- max_output_bytes: 2097152

Observed usage is explicit. The validator does not measure the clock, inspect files, run Git, count provider tokens, or query billing.

Attempts are positive and consecutive. Elapsed time uses explicit started_at/evaluated_at. Changed paths are normalized, repository-relative, and unique. Output is a nonnegative byte count. Money must stay exactly zero. A breach requires PAUSE or FAIL and forbids accepted continuation.

### 3.6 Bounded Owner amendment

- Attempt ceiling 3 and monetary zero are immutable in v1.0.
- STUDIO_OWNER may amend max_elapsed_seconds, max_changed_paths, or max_output_bytes only.
- Amendment records prior/new value, reason, evidence digest, decided_at, expires_at, work order, and attempt.
- It must be effective before reliance.
- Expired, late, retroactive, duplicate, unused, mismatched, or unauthorized amendments fail.
- Amendment cannot authorize prohibited activity.

### 3.7 Secret safety

- Schemas allowlist fields and reject additional properties.
- Recursive keys/values representing passwords, secrets, credentials, private keys, bearer authorization, access/refresh tokens, cookies, or authentication material fail closed.
- Automatic redaction is not acceptance.
- Safe records may store opaque references, stable IDs, or SHA-256 digests.
- Reasons and references are bounded and reject control characters and credential-like content.

### 3.8 Safety boundary

Python standard library only. Commands are deterministic and read-only. No dependency, network, telemetry, provider/model, credential, subprocess, Git/worktree, billing, execution, retry, failover, reassignment, merge, deletion, publication, deployment, or paid action.

## 4. Exact implementation scope

After the contract Pull Request merges, implementation may create exactly:

1. platform/orchestration/GATE_TRACE_BUDGET.md
2. platform/orchestration/schemas/gate-result.schema.json
3. platform/orchestration/schemas/trace-event.schema.json
4. platform/orchestration/schemas/quota-budget.schema.json
5. platform/orchestration/fixtures/007e/valid-gate-result.json
6. platform/orchestration/fixtures/007e/valid-trace-chain.json
7. platform/orchestration/fixtures/007e/valid-zero-cost-budget.json
8. platform/orchestration/fixtures/007e/invalid-missing-evidence.json
9. platform/orchestration/fixtures/007e/invalid-unauthorized-gate.json
10. platform/orchestration/fixtures/007e/invalid-mutable-artifact.json
11. platform/orchestration/fixtures/007e/invalid-mismatched-artifact.json
12. platform/orchestration/fixtures/007e/invalid-broken-correlation.json
13. platform/orchestration/fixtures/007e/invalid-mutated-trace.json
14. platform/orchestration/fixtures/007e/invalid-attempt-ceiling.json
15. platform/orchestration/fixtures/007e/invalid-time-ceiling.json
16. platform/orchestration/fixtures/007e/invalid-path-ceiling.json
17. platform/orchestration/fixtures/007e/invalid-output-ceiling.json
18. platform/orchestration/fixtures/007e/invalid-nonzero-budget.json
19. platform/orchestration/fixtures/007e/invalid-secret-field.json
20. scripts/orchestration_gate_trace_budget.py
21. tests/test_orchestration_gate_trace_budget.py

Only material-checkpoint updates may modify the four existing records under studio/memory/tasks/STUDIO-007E/. Total implementation-PR scope is at most 25 paths.

No other file may be created, modified, deleted, renamed, or moved without accepted amendment. STUDIO-007A through STUDIO-007D implementation paths remain unchanged.

## 5. Validation requirements

Gate validation must enforce exact role authority, nonempty bounded evidence/reasons, immutable artifact identity, allowed verdicts, ordered lineage, and same-head QA/integration evidence. Mutable references, branch-only identity, missing commit, digest mismatch, gate substitution, duplication, or unauthorized roles fail.

Trace validation must enforce one correlation ID, consecutive sequence, exact prior digests, consistent work-order/attempt/artifact identity, chronology, applicable gate/quota evidence at event time, and append-only history. Fork, gap, cycle, mutation, future evidence, or retroactive authorization fail.

Budget validation applies exactly 3 attempts, 7200 seconds, 25 paths, 2097152 bytes, and zero money. Negative usage, duplicate/absolute/traversal paths, malformed time, unsupported cost class, mismatched work order, continued work after breach, or invalid amendment fail.

## 6. Required CLI

- validate-gate: validate one gate result at explicit --as-of.
- validate-trace: validate one trace chain.
- validate-budget: validate quota and observed usage.
- validate-bundle: validate linked gates, trace, quota, and artifact identity.
- evaluate-attempt: derive PASS, FAIL, or PAUSE without writing.
- explain-boundary: print gates, usage, remaining ceilings, blockers, and next safe action without mutation.

Invalid input returns nonzero.

## 7. Required tests

Focused tests prove:

- valid fixtures pass and invalid fixtures fail for intended reasons;
- exact gate-to-role mapping and same-head QA/integration binding;
- missing evidence and mutable/mismatched artifacts fail;
- trace correlation, sequence, chronology, identity, and prior digests are append-only;
- mutation, fork, gap, cycle, future evidence, or retroactive authority fail;
- attempts above 3, time above 7200 seconds, paths above 25, output above 2097152 bytes, or any nonzero money fail or require PAUSE as specified;
- duplicate, traversal, absolute, or malformed paths fail;
- unauthorized, expired, late, duplicate, unused, or retroactive amendments fail;
- attempt ceiling and monetary zero cannot be amended;
- secret-like keys and credential-bearing values fail while safe references/digests pass;
- evaluation/explanation are deterministic and read-only;
- failed validation does not mutate input;
- no network, subprocess, Git, provider/model, credential, telemetry, billing, execution, deletion, publication, deployment, or paid call occurs.

Required repository checks:

python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_orchestration_queue -v
python -m unittest tests.test_orchestration_dispatch -v
python -m unittest tests.test_orchestration_handoff -v
python -m unittest tests.test_orchestration_failover -v
python -m unittest tests.test_orchestration_gate_trace_budget -v
python -m unittest discover -s tests -p "test*.py" -v

Rules CI must pass on push and pull-request events.

## 8. Acceptance criteria

- Contract PR changes exactly tasks/STUDIO-007E.md, this contract, and four STUDIO-007E memory records.
- Contract PR merges before implementation.
- Implementation PR changes only the twenty-one section-4 paths plus four memory records, total at most 25.
- No prohibited dependency, call, mutation, execution, telemetry, billing, or spending.
- Positive, negative, authority, artifact, trace, quota, amendment, secret, no-mutation, and no-call tests pass.
- Retained 007A through 007D tests, full suite, whitespace, and Rules CI pass.
- Independent QA returns PASS and Review and Integration returns APPROVE on one immutable head.
- Studio Owner makes final merge decision.

## 9. Rollback

Rollback is an authorized revert of later implementation. The twenty-one implementation files may be removed together only through authorized revert; contracts/memory remain evidence and 007A through 007D remain operational.

## 10. Explicit non-goals

No billing, nonzero money, telemetry, provider/model, credential, network, external code, dependency, dispatch, retry, failover, reassignment, Git/worktree mutation, execution, automatic merge, deletion, publication, deployment, STUDIO-007F, or human-approval bypass.

## 11. Workflow after contract merge

1. Reconcile merged contract/memory against main.
2. Create agent/studio-007e-gate-trace-budget from verified contract merge.
3. Acquire one verified ENGINEERING writer claim.
4. Create only section-4 implementation paths.
5. Run retained 007A through 007D, focused 007E, full-suite, and whitespace checks.
6. Obtain QA and Review and Integration verdicts on one immutable head.
7. Studio Owner decides merge.
