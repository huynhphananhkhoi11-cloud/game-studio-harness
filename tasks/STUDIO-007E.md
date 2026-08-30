# STUDIO-007E - Gate, trace, quota and budget

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent: STUDIO-007

Dependencies: accepted, implemented, reviewed, merged, closed out, and retained STUDIO-007A through STUDIO-007D

Primary owner: Platform Studio; final gate authority remains with the named QA, Review and Integration, or Studio Owner role

Canonical implementation contract: tasks/STUDIO-007E-IMPLEMENTATION.md

## Goal

Make every orchestration attempt auditable and bounded while keeping the zero-cost system incapable of authorizing spend, bypassing human approval, executing work, or rewriting evidence.

## Accepted records

A gate result is immutable evidence bound to one work order, attempt, gate type, evaluator identity and role, evidence set, artifact identity, verdict, reasons, and explicit evaluation time.

A trace event is append-only evidence bound to one correlation ID, work order, attempt, actor, capability, state transition, safe input/output references, outcome, explicit event time, and prior-event digest.

A quota-budget record declares ceilings and observed usage from supplied evidence. v1.0 defaults are:

- cost class ZERO_COST;
- monetary budget and spend 0;
- maximum 3 attempts;
- maximum elapsed time 120 minutes;
- maximum 25 unique changed paths;
- maximum output size 2 MiB, equal to 2,097,152 bytes.

Exceeding a ceiling produces a fail-closed PAUSE or FAIL verdict. It never upgrades service, spends money, retries, dispatches, reassigns, merges, or executes work.

## Accepted layered gate authority

- The ENGINEERING role may record deterministic technical evidence and technical gate results.
- The QA role alone issues QA_ACCEPTANCE.
- The REVIEW_INTEGRATION role alone issues REVIEW_INTEGRATION.
- STUDIO_OWNER alone decides merge and permitted bounded quota amendments.
- Concrete evaluator ID is recorded separately from role and does not authenticate itself.

Every work order requires scope-boundary, evidence-integrity, quota-budget, and secret-safety gates. Implementation also requires focused-test and retained-regression gates. Repository-changing work requires QA and Review and Integration verdicts on one immutable head before the separate Studio Owner merge decision.

## Accepted quota amendments

- Attempt ceiling 3 and monetary budget 0 cannot be raised in v1.0.
- Time, changed-path, or output ceilings may change only through a bounded STUDIO_OWNER amendment effective before reliance.
- Late or retroactive evidence cannot erase an earlier breach.
- A breach pauses work; no automatic continuation is authorized.

## Accepted secret policy

Gate and trace records use allowlisted fields. Secret-like keys, credential-bearing values, private-key material, bearer authorization, access or refresh tokens, passwords, session cookies, or embedded authentication values are rejected.

Automatic redaction does not convert unsafe input into accepted evidence. Valid records cite a safe external reference, stable identifier, or content digest.

## Approved implementation boundary

Implementation may begin only after this contract-only Pull Request merges. It may create only the twenty-one paths in section 4 of tasks/STUDIO-007E-IMPLEMENTATION.md and materially update the four STUDIO-007E memory records. Total implementation-Pull-Request scope is therefore at most 25 paths.

Implementation uses Python standard library tooling, deterministic fixtures, caller-supplied as_of, supplied evidence only, immutable lineage, and read-only validation.

## Relationship to earlier orchestration

- STUDIO-007A remains queue and work-order evidence.
- STUDIO-007B remains capability dispatch and eligibility evidence.
- STUDIO-007C remains writer-claim, worktree, and durable-handoff evidence.
- STUDIO-007D remains failover and attempt-lineage evidence.
- STUDIO-007E validates gates, trace continuity, and ceilings only. It does not duplicate or execute earlier capabilities.

## Out of scope

- Billing, payment, token purchase, cost forecasting, telemetry export, hosted observability, or nonzero spend.
- Provider/model calls, credentials, network, subprocess, Git/worktree mutation, execution, dispatch, retry, failover, reassignment, merge, deletion, publication, or deployment.
- Automated Owner approval, quality-gate bypass, evidence rewriting, retroactive authorization, or STUDIO-007F.

## Required behavior

- Reject missing evidence, unsupported gates, unauthorized roles, and mutable or mismatched artifact identities.
- Trace accepted transitions with one correlation ID and append-only digest lineage.
- Stop at attempt, time, path, output, or monetary ceilings.
- Prove money remains zero in every accepted v1.0 record.
- Reject secret-like records instead of silently accepting redaction.
- Prove failed validation leaves input evidence byte-for-byte unchanged.

## Failure and rollback

The contract fails if a gate can be bypassed, trace history rewritten, a secret accepted, a quota breach continues, money becomes nonzero, or a validator performs a prohibited action.

Rollback removes only later STUDIO-007E implementation through an authorized revert. Contracts and memory remain evidence; STUDIO-007A through STUDIO-007D remain operational.

## Owner decisions accepted

- Gate authority: layered ENGINEERING, QA, REVIEW_INTEGRATION, and STUDIO_OWNER roles.
- Defaults: 3 attempts, 120 minutes, 25 unique changed paths, 2 MiB output, and monetary budget 0.
- Secret handling: reject secret-like records; accept only safe references or digests.
- Any nonzero budget or external telemetry requires a separately accepted contract.

Studio Owner acceptance date: 2026-08-30.
