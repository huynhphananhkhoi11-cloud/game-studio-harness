# STUDIO-007C-IMPLEMENTATION - Writer Claim, worktree & durable handoff v1.0

## 1. Purpose

Authorize one bounded, zero-cost implementation of the accepted STUDIO-007C writer-claim, worktree-record, and durable-handoff validators.

This document is an implementation contract. It does not implement runtime behavior. This contract-only Pull Request must merge before any implementation path in section 4 is created.

## 2. Approval and identity

- Status: `APPROVED - IMPLEMENTATION NOT STARTED`
- Approved by: Studio Owner
- Approval date: `2026-08-29`
- Parent umbrella: `tasks/STUDIO-007.md`
- Parent capability contract: `tasks/STUDIO-007C.md`
- Dependency A: PR `#18`, merge commit `a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f`
- Dependency B implementation: PR `#20`, merge commit `2a559c420c72b835fb48da91699f3cda9717c516`
- Verified dependency baseline: PR `#21`, merge commit `23f6668dcd072f666c248b9c9fc0fa0bb533a5c1`
- Contract branch: `agent/studio-007c-contract`
- Planned implementation branch: `agent/studio-007c-writer-worktree-handoff`
- Platform memory package: `studio/memory/tasks/STUDIO-007C/`

This authorization does not activate STUDIO-007D through STUDIO-007F.

## 3. Accepted implementation decisions

### 3.1 Claim identity and lifecycle

- JSON is canonical for immutable writer-claim records.
- A claim requires schema version, claim ID, work-order ID and digest, executor ID, branch, worktree ID, base commit, permitted paths, issued time, expiry time, lifecycle status, evidence, and content digest inputs.
- Lifecycle values align with `studio/MEMORY_PROTOCOL.md`: `CLAIMED`, `TRANSFER_PENDING`, `RELEASED`, and `UNKNOWN`.
- Only one unambiguous, unexpired `CLAIMED` record permits ordinary writing.
- Validation requires explicit ISO 8601 UTC `as_of`; the implementation must not consult the system clock.
- Expiry invalidates ordinary writing but never releases, transfers, deletes, or overwrites evidence automatically.

### 3.2 Paths and overlap

- Permitted paths use normalized repository-relative POSIX syntax.
- Absolute paths, empty segments, `.` or `..`, backslashes, drive prefixes, control characters, credentials, and paths outside the declared work-order scope fail closed.
- Two active scopes overlap when paths are equal or one path is an ancestor of the other by path component.
- Prefix text without a component boundary is not overlap.
- Independent non-overlapping claims may coexist.

### 3.3 Renewal and exception authority

- Renewal creates a new immutable record by the same executor before expiry.
- Renewal preserves work-order ID and digest, executor, branch, worktree, base commit, and permitted paths.
- Renewal increments the lease revision and cites the previous claim ID and SHA-256 digest.
- Only `STUDIO_OWNER` may approve an overlap exception.
- An exception requires affected claim IDs, exact overlapping paths, reason, approval reference, decided time, and expiry time.
- The exception is evidence only and cannot authenticate the named approver or grant merge authority.

### 3.4 Worktree records

- Worktree records use logical repository-relative identity; machine-specific absolute paths are prohibited.
- A record binds worktree ID, branch, base commit, current commit, permitted paths, status, evidence, and observed time.
- Validation checks shape, commit syntax, claim consistency, and explicit expected values only.
- No command may invoke or mutate Git.

### 3.5 Durable handoffs

- Handoffs require work-order and claim identity, sender and intended receiver, branch/worktree identity, base and current commits, completed and pending work, changed paths, checks, evidence, risks, blockers, claim disposition, and exact resume action.
- Changed paths must remain within the claim scope.
- Base/current identities must match explicit caller-supplied expectations.
- A handoff supplements but never replaces `studio/HANDOFF_PROTOCOL.md` or the four-record memory package.

### 3.6 Safety

- Python standard library only; no installation or dependency.
- Schemas document normative shapes; the CLI enforces the accepted subset.
- Validation and explanation are read-only.
- No network, provider, credential, subprocess, Git, deletion, execution, automatic routing, failover, publication, or paid action.
- Invalid input fails closed with nonzero exit status and no source mutation.

## 4. Exact implementation scope

After the contract-only Pull Request merges, implementation may create exactly:

1. `platform/orchestration/WRITER_WORKTREE_HANDOFF.md`
2. `platform/orchestration/schemas/writer-claim.schema.json`
3. `platform/orchestration/schemas/worktree-record.schema.json`
4. `platform/orchestration/schemas/durable-handoff.schema.json`
5. `platform/orchestration/fixtures/007c/valid-writer-claim.json`
6. `platform/orchestration/fixtures/007c/valid-independent-claims.json`
7. `platform/orchestration/fixtures/007c/valid-worktree-record.json`
8. `platform/orchestration/fixtures/007c/valid-durable-handoff.json`
9. `platform/orchestration/fixtures/007c/invalid-exact-overlap.json`
10. `platform/orchestration/fixtures/007c/invalid-ancestor-overlap.json`
11. `platform/orchestration/fixtures/007c/invalid-expired-claim.json`
12. `platform/orchestration/fixtures/007c/invalid-mismatched-base.json`
13. `platform/orchestration/fixtures/007c/invalid-unauthorized-exception.json`
14. `platform/orchestration/fixtures/007c/invalid-handoff-commit.json`
15. `scripts/orchestration_handoff.py`
16. `tests/test_orchestration_handoff.py`

During implementation, only material-checkpoint updates may modify the existing four records under `studio/memory/tasks/STUDIO-007C/`.

No other file may be created, modified, deleted, renamed, or moved without an accepted amendment. STUDIO-007A and STUDIO-007B implementation paths remain unchanged.

## 5. Claim validation requirements

Reject missing or extra fields, unsupported schema versions, duplicate IDs, duplicate paths, invalid digests, unsafe paths, credentials, invalid chronology, implicit clock use, invalid status combinations, work-order mismatch, executor mismatch, branch/worktree mismatch, and base mismatch.

Claim validation must not authenticate an executor or infer that work was performed.

## 6. Conflict and renewal requirements

- Detect equal path and ancestor/descendant overlap in either claim order.
- Treat path components, not raw string prefix, as the overlap boundary.
- Evaluate only claims active at explicit `as_of`.
- Reject ambiguous simultaneous active writers.
- Accept non-overlapping claims.
- Validate renewal lineage and reject post-expiry, cross-writer, scope-changing, or digest-mismatched renewal.
- Accept only bounded, unexpired Studio-Owner-recorded overlap exceptions.

## 7. Worktree and handoff requirements

- Validate record identity without accessing the local filesystem or invoking Git.
- Reject machine-specific absolute paths and mismatched commit identities.
- Require every changed path to be inside the claim scope.
- Require non-empty completed/pending declarations, evidence, validation results, risk/blocker declarations, and exact resume action.
- Reject handoff claims of acceptance, merge, authority, or execution that lack explicit evidence fields.

## 8. Required CLI behavior

The CLI must provide bounded commands equivalent to:

- `validate-claim` - validate one claim at explicit `--as-of`.
- `validate-claim-set` - detect conflicts and validate renewals/exceptions.
- `validate-worktree` - validate one worktree record against a claim and explicit expected commits.
- `validate-handoff` - validate one handoff against claim/worktree evidence and explicit expected commits.
- `explain-handoff` - print bounded identity, state, checks, blockers, and resume action without mutation.

All commands fail closed and return nonzero exit status on invalid input.

## 9. Required tests

Focused tests must prove:

- every valid fixture passes and every invalid fixture fails for its intended reason;
- exact and ancestor/descendant overlap are detected in both input orders;
- textual prefixes without a component boundary do not conflict;
- independent claims coexist;
- expiry and renewal use only explicit `as_of`;
- post-expiry, changed-scope, cross-writer, and invalid-lineage renewals fail;
- only bounded Studio Owner exceptions pass;
- worktree and handoff commit mismatches fail;
- changed paths cannot escape claim scope;
- failed validation does not mutate any input or fixture;
- CLI exit codes and explanation behavior are deterministic;
- tests make no network, subprocess, Git, filesystem-worktree, or provider calls.

Required repository checks:

```text
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_orchestration_queue -v
python -m unittest tests.test_orchestration_dispatch -v
python -m unittest tests.test_orchestration_handoff -v
python -m unittest discover -s tests -p "test*.py" -v
```

GitHub Actions Rules CI must pass on push and pull-request events.

## 10. Acceptance criteria

- [ ] Contract-only PR changes exactly `tasks/STUDIO-007C.md`, this contract, and the four-record STUDIO-007C memory package.
- [ ] Contract-only PR merges before implementation begins.
- [ ] Implementation PR changes only the sixteen section 4 paths and material-checkpoint updates to the four existing memory records.
- [ ] No dependency, network, provider, credential, subprocess, Git automation, external runtime, workflow, or nonzero spending is added.
- [ ] All positive, negative, overlap, renewal, expiry, exception, no-mutation, and no-network tests pass.
- [ ] Retained 007A and 007B tests, full suite, whitespace check, and Rules CI pass.
- [ ] Independent QA returns `PASS` and Review & Integration returns `APPROVE` against one immutable implementation head.
- [ ] Studio Owner makes the final merge decision.

## 11. Rollback

Rollback is an authorized revert of the later implementation commit. The sixteen implementation files may be removed together only by an authorized revert; contracts and memory history remain evidence.

After rollback, coordination returns to the existing manual `studio/MEMORY_PROTOCOL.md` and `studio/HANDOFF_PROTOCOL.md` procedures. STUDIO-007A and STUDIO-007B remain operational.

## 12. Explicit non-goals

This contract does not authorize automatic Git/worktree operations, concurrent overlapping writers by default, runtime execution, failover, STUDIO-007D through STUDIO-007F, provider/model calls, credentials, network access, external code, dependency installation, project-content changes, publication, deployment, or nonzero spending.

## 13. Workflow after contract merge

1. Reconcile the merged contract and memory package against current `main`.
2. Create `agent/studio-007c-writer-worktree-handoff` from the verified contract merge commit.
3. Acquire one verified writer claim as `ENGINEERING-01`.
4. Create only the sixteen implementation paths in section 4.
5. Run data validation, retained 007A/007B tests, focused 007C tests, full suite, and whitespace checks.
6. Obtain independent QA and Review & Integration verdicts against one immutable implementation head.
7. Studio Owner decides whether to merge the implementation.
