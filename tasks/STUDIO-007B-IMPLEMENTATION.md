# STUDIO-007B-IMPLEMENTATION â€” Capability Registry & Manual Dispatcher v1.0

## 1. Purpose

Authorize one bounded, zero-cost implementation of the accepted STUDIO-007B capability registry and human-recorded manual dispatcher.

This is an implementation contract. It does not implement runtime behavior itself. The contract-only Pull Request must merge before any implementation file listed below is created.

## 2. Approval and identity

- Status: `APPROVED â€” IMPLEMENTATION NOT STARTED`
- Approved by: Studio Owner
- Approval date: `2026-08-29`
- Parent umbrella: `tasks/STUDIO-007.md`
- Parent capability contract: `tasks/STUDIO-007B.md`
- Dependency implementation: Pull Request `#18`, merge commit `a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f`
- Contract branch: `agent/studio-007b-capability-dispatcher`
- Planned implementation branch: `agent/studio-007b-manual-dispatch`
- Platform memory package: `studio/memory/tasks/STUDIO-007B/`

The Studio Owner authorization is limited to this contract. It does not activate STUDIO-007C through STUDIO-007F.

## 3. Accepted implementation decisions

### 3.1 Registry records

- JSON is the canonical format for one registry document containing unique capability records.
- Every record requires `executor_id`, `organizational_role`, `source_class`, `eligibility`, `capability_tags`, supported input/output types, constraints, availability, cost class, trust level, and repository-relative evidence references.
- `source_class` is either `INTERNAL_ROLE` or `EXTERNAL_CANDIDATE`; only `INTERNAL_ROLE` is dispatchable.
- Eligibility values are `ELIGIBLE`, `REFERENCE`, `NOT_INSTALLED`, `NO_DECISION`, and `ADAPT_PENDING`; only `ELIGIBLE` is dispatchable.
- Availability values are `AVAILABLE` and `UNAVAILABLE`; only `AVAILABLE` is dispatchable.
- Cost class is fixed to `ZERO_COST` for v1.0.
- Trust levels are `EVIDENCE_PENDING`, `EVIDENCE_VERIFIED`, and `RESTRICTED`. `EVIDENCE_PENDING` is never dispatchable. `RESTRICTED` requires all declared constraints to appear in the work order's prohibitions or acceptance gates.
- Registry order is not preference, priority, ranking, or authority.

### 3.2 Initial capability vocabulary

- `production.coordination`
- `game-design.systems`
- `narrative.research`
- `engineering.repository`
- `qa.validation`
- `review.integration`

The implementation rejects unknown capability tags. Vocabulary expansion requires an accepted amendment.

### 3.3 Manual dispatch decisions

- JSON is the canonical format for one immutable dispatch decision.
- Every decision requires a unique decision ID, work-order ID and SHA-256 digest, selected executor ID, required capability and data-type claims, considered alternatives, dispatcher identity and role, evidence references, non-empty reason, `decided_at`, and `expires_at`.
- Only `dispatcher_role: STUDIO_OWNER` is active in v1.0.
- The selected work order must be a validated STUDIO-007A snapshot in `CLAIMABLE` state.
- Validation requires an explicit ISO 8601 UTC `as_of` value. It rejects `as_of` before `decided_at` or at/after `expires_at`; it must not consult the system clock.
- Exact replay of an identical decision is idempotent. A reused decision ID with different content fails closed.
- A valid decision is evidence of manual selection only. It does not mutate queue files, claim work, execute an agent, or authenticate any actor.

### 3.4 Tooling and safety

- Python standard library only; no dependency or installation.
- Schemas document the normative shapes; the CLI enforces the accepted subset.
- CLI operations are read-only except for optionally writing one validated decision to a caller-supplied output directory using sibling temporary files and atomic replacement.
- The CLI performs no network, provider, credential, Git, deletion, execution, automatic ranking, or paid action.
- All paths and evidence references are repository-relative and credential-bearing values fail closed.

## 4. Exact implementation scope

After this contract-only Pull Request is merged, the implementation may create exactly:

- `platform/orchestration/CAPABILITY_DISPATCH.md`
- `platform/orchestration/schemas/capability-registry.schema.json`
- `platform/orchestration/schemas/dispatch-decision.schema.json`
- `platform/orchestration/fixtures/007b/valid-capability-registry.json`
- `platform/orchestration/fixtures/007b/valid-dispatch-decision.json`
- `platform/orchestration/fixtures/007b/invalid-unknown-executor.json`
- `platform/orchestration/fixtures/007b/invalid-unavailable-executor.json`
- `platform/orchestration/fixtures/007b/invalid-capability-mismatch.json`
- `platform/orchestration/fixtures/007b/invalid-expired-decision.json`
- `platform/orchestration/fixtures/007b/invalid-nonhuman-dispatcher.json`
- `platform/orchestration/fixtures/007b/invalid-candidate-status.json`
- `scripts/orchestration_dispatch.py`
- `tests/test_orchestration_dispatch.py`

During implementation, the active memory package may update exactly its existing four records under `studio/memory/tasks/STUDIO-007B/` at material checkpoints required by `studio/MEMORY_PROTOCOL.md`.

No other file may be created, modified, deleted, renamed, or moved without a separately accepted amendment. In particular, `scripts/orchestration_queue.py`, its schemas, tests, and queue records remain unchanged.

## 5. Required registry behavior

The validator must reject missing or extra fields, unsupported schema versions, duplicate executor IDs, duplicate tags or types, unknown vocabulary, empty evidence, unsafe paths, credentials, nonzero cost, contradictory eligibility/source combinations, and invalid trust/availability combinations.

The valid fixture may describe only these existing logical executor IDs:

- `PRODUCER-01`
- `GAME-DESIGN-01`
- `NARRATIVE-RESEARCH-01`
- `ENGINEERING-01`
- `QA-01`
- `REVIEW-INTEGRATION-01`

These IDs are evidence claims, not authentication or new authority. The fixture must not claim that every role supports every capability.

## 6. Required dispatch behavior

The validator must reject:

- an unknown, duplicate, unavailable, ineligible, external-candidate, nonzero-cost, or evidence-pending selected executor;
- missing required capability tags or unsupported input/output types;
- unsatisfied restrictions;
- a work order outside `CLAIMABLE`, a work-order ID mismatch, or digest mismatch;
- a missing, non-Owner, blank, or credential-bearing dispatcher identity;
- missing alternatives, evidence, or explanation;
- duplicate alternative IDs, selection of the chosen executor as an alternative, or unknown alternatives presented as available;
- invalid chronology, implicit-clock validation, or expired decisions;
- replay that reuses a decision ID with different content;
- any attempt to mutate the STUDIO-007A queue or enter `CLAIMED`.

## 7. Required CLI behavior

The standard-library CLI must provide bounded commands equivalent to:

- `validate-registry` â€” validate one registry without changing files;
- `validate-decision` â€” validate one decision against one registry and one work-order snapshot at explicit `--as-of`;
- `dispatch` â€” validate and atomically record one manual decision in a caller-supplied decision root;
- `explain` â€” print the selected executor, considered alternatives, reason, evidence, and expiry without mutation.

The CLI must fail closed, return a nonzero exit status on invalid input, avoid printing secrets, and never rank executors or infer a decision.

## 8. Required tests

Focused tests must prove:

- valid registry, work-order, and decision fixtures pass;
- every invalid fixture in section 4 fails for its intended reason;
- duplicate executor and decision IDs fail;
- exact decision replay is idempotent and altered replay fails without mutation;
- only the Studio Owner dispatcher role is accepted;
- capability, type, restriction, eligibility, trust, availability, cost, state, ID, and digest boundaries are enforced;
- expiry uses only explicit deterministic `as_of` input;
- CLI exit codes are correct and validation/explanation do not mutate inputs;
- a failed dispatch leaves the output directory unchanged;
- queue snapshots and events remain byte-for-byte unchanged;
- tests use temporary decision roots and make no network calls.

Required repository checks:

```text
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_orchestration_queue -v
python -m unittest tests.test_orchestration_dispatch -v
python -m unittest discover -s tests -p "test*.py" -v
```

GitHub Actions Rules CI must pass on push and pull-request events.

## 9. Acceptance criteria

- [ ] The contract-only Pull Request changes exactly `tasks/STUDIO-007B.md`, this implementation contract, and the four-record STUDIO-007B memory package.
- [ ] The contract-only Pull Request is merged before implementation starts.
- [ ] The implementation Pull Request changes only the thirteen paths in section 4 and material-checkpoint updates to the four existing memory records.
- [ ] No dependency, provider, credential, network service, external candidate execution, workflow, or nonzero budget is added.
- [ ] No live registry or dispatch decision is committed outside deterministic fixtures.
- [ ] All positive, negative, replay, expiry, no-mutation, and no-network tests pass.
- [ ] The complete existing test suite and Rules CI pass.
- [ ] Independent QA returns `PASS` and Review & Integration returns `APPROVE` against one immutable implementation head.
- [ ] The Studio Owner makes the final merge decision.

## 10. Rollback

Rollback of the later implementation is the ordinary revert of its implementation commit. The thirteen implementation files may be removed together only by an authorized revert; accepted contracts and memory history remain evidence.

After rollback, STUDIO-007A remains usable as a manual file-backed queue and dispatch returns to a human-readable, non-executable record outside the 007B runtime.

## 11. Explicit non-goals

This contract does not authorize STUDIO-007C claims/worktrees/handoffs, STUDIO-007D failover, STUDIO-007E gates/trace/quota/budget, STUDIO-007F adapters, automated routing, execution, model calls, provider connections, credentials, external code, project-content changes, commits, pushes, merges, publication, or deployment.

## 12. Workflow after contract merge

1. Reconcile the merged contract and memory package against current `main`.
2. Create `agent/studio-007b-manual-dispatch` from the verified merge commit.
3. Acquire the single writer claim as `ENGINEERING-01`.
4. Create only the thirteen implementation files in section 4.
5. Run data validation, retained 007A tests, focused 007B tests, full suite, and whitespace checks.
6. Obtain independent QA and Review & Integration verdicts against one immutable head.
7. Studio Owner decides whether to merge the implementation.