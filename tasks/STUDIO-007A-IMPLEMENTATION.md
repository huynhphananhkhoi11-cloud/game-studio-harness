# STUDIO-007A-IMPLEMENTATION — Work Order & Producer Queue v1.0

## 1. Purpose

Authorize one bounded, zero-cost implementation of the accepted STUDIO-007A work-order envelope and file-backed Producer Queue.

This is an implementation contract. It does not implement runtime behavior itself. The contract-only Pull Request must merge before any implementation file listed below is created.

## 2. Approval and identity

- Status: `APPROVED — IMPLEMENTATION NOT STARTED`
- Approved by: Studio Owner
- Approval date: `2026-08-26`
- Parent umbrella: `tasks/STUDIO-007.md`
- Parent capability contract: `tasks/STUDIO-007A.md`
- Proposal merge: Pull Request `#16`, merge commit `e04a933e2c0dd18438822f4c9fdabd2f6af9c4e5`
- Contract branch: `agent/studio-007a-contract`
- Planned implementation branch: `agent/studio-007a-work-order-queue`
- Platform memory package: `studio/memory/tasks/STUDIO-007A/`

The Studio Owner authorization is limited to this contract. It does not activate STUDIO-007B through STUDIO-007F.

## 3. Accepted implementation decisions

### 3.1 Records and storage

- JSON is the canonical snapshot format for one work order.
- JSON Lines is the append-only transition-event format for one work order.
- A queue root contains `work-orders/` snapshots and `events/` histories keyed by work-order ID.
- The ordered queue is derived from validated snapshots; no central mutable index or external database is authoritative.
- Priority is an integer from 0 through 100. Higher values are processed first, then earlier `created_at`, then lexical `work_order_id` as the deterministic tie-breaker.
- Timestamps use ISO 8601 UTC with a `Z` suffix.
- Monetary budget is fixed at `0` for v1.0.

### 3.2 Tooling

- The implementation uses Python standard library only.
- The schemas document normative fields and constraints. The repository CLI enforces the accepted subset without adding a JSON Schema dependency.
- The CLI may create a draft, validate a queue root, list the derived queue, and append an authorized active transition.
- Actor IDs and roles are repository evidence claims, not authentication. Git review remains the authority boundary.
- File updates must use a temporary sibling file plus atomic replacement where supported; an interrupted write must not be presented as a valid completed transition.

### 3.3 Active authority and transitions

- `PRODUCER-01` may create and edit `DRAFT` records.
- Only `STUDIO_OWNER` may transition `DRAFT` to `READY`.
- `PRODUCER-01` may transition a validated `READY` record to `CLAIMABLE`.
- `PRODUCER-01` may transition `DRAFT`, `READY`, or `CLAIMABLE` to `BLOCKED` with a non-empty reason, and may return `BLOCKED` to `DRAFT` after the blocker is addressed.
- Only `STUDIO_OWNER` may transition `DRAFT`, `READY`, `CLAIMABLE`, or `BLOCKED` to `CANCELLED`.
- `CLAIMED`, `QA_PENDING`, `OWNER_PENDING`, and `DONE` are recognized reserved states but every transition into or out of them is rejected by 007A.
- The validator and CLI must never infer approval from a role label, test pass, AI output, branch, or commit.

## 4. Exact implementation scope

After this contract-only Pull Request is merged, the implementation may create exactly:

- `platform/orchestration/WORK_ORDER_QUEUE.md`
- `platform/orchestration/schemas/work-order.schema.json`
- `platform/orchestration/schemas/queue-entry.schema.json`
- `platform/orchestration/queue/README.md`
- `platform/orchestration/fixtures/007a/valid-work-order.json`
- `platform/orchestration/fixtures/007a/valid-events.jsonl`
- `platform/orchestration/fixtures/007a/invalid-missing-scope.json`
- `platform/orchestration/fixtures/007a/invalid-nonzero-budget.json`
- `platform/orchestration/fixtures/007a/invalid-illegal-transition.jsonl`
- `platform/orchestration/fixtures/007a/invalid-duplicate-event.jsonl`
- `scripts/orchestration_queue.py`
- `tests/test_orchestration_queue.py`

During implementation, the active memory package may update exactly its existing four records under `studio/memory/tasks/STUDIO-007A/` at material checkpoints required by `studio/MEMORY_PROTOCOL.md`.

No other file may be created, modified, deleted, renamed, or moved without a separately accepted amendment.

## 5. Required work-order fields

The schema and validator must require:

- schema version and unique `work_order_id`;
- producer and requesting organizational unit;
- optional project identifier that is explicit even when not applicable;
- bounded objective;
- permitted paths and prohibited actions;
- required capability tags;
- input and expected-output references;
- acceptance gates;
- integer priority and monetary budget ceiling;
- dependency IDs and attempt number;
- current state and Owner-gate requirement;
- `created_at`, `updated_at`, and last transition-event ID.

Empty objectives, absolute machine paths, credential-bearing values, duplicate IDs, missing scopes, nonzero monetary budgets, and unsupported schema versions are invalid.

## 6. Required transition-event behavior

Every event must contain a unique event ID, work-order ID, prior state, next state, actor ID, actor role, UTC timestamp, non-empty reason, attempt number, and resulting snapshot digest.

The implementation must reject:

- an event whose work-order ID or prior state does not match the snapshot;
- duplicate event IDs or replay that changes the prior result;
- decreasing timestamps within one work-order history;
- unauthorized or reserved transitions;
- transition events that expand permitted paths, remove prohibited actions, raise budget, or change the bounded objective;
- a snapshot that cannot be reconciled with its append-only event history.

## 7. Required CLI behavior

The standard-library CLI must provide bounded commands equivalent to:

- `create-draft` — create one new validated `DRAFT` snapshot and initial event;
- `validate` — validate one queue root without changing it;
- `list` — display the deterministic derived queue without changing it;
- `transition` — append one active authorized transition and update its snapshot.

The CLI must fail closed, return a nonzero exit status on invalid input, print a concise error without secrets, and never perform Git commit, push, pull request, merge, network, provider, credential, or deletion actions.

## 8. Required tests

Focused tests must prove:

- valid work-order and event fixtures pass;
- missing scope, nonzero budget, duplicate ID, malformed timestamp, and unsupported schema fail;
- queue ordering follows priority, creation time, and ID deterministically;
- duplicate work-order and event IDs fail;
- replay is idempotent only when the existing event and resulting digest are identical;
- every unauthorized, reserved, or illegal transition fails;
- scope, objective, prohibition, and budget escalation through a transition fails;
- actor-role boundaries above are enforced as declared evidence rules;
- CLI commands return correct exit codes and do not mutate data on validation failure;
- tests use temporary queue roots and do not create tracked live work orders.

Required repository checks:

```text
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_orchestration_queue -v
python -m unittest discover -s tests -p "test*.py" -v
```

GitHub Actions Rules CI must pass on push and pull-request events.

## 9. Acceptance criteria

- [ ] The contract-only Pull Request changes exactly the parent contract and four-record memory package plus this implementation contract.
- [ ] The contract-only Pull Request is merged before implementation starts.
- [ ] The implementation Pull Request changes only the exact paths in section 4 and the four existing memory records at material checkpoints.
- [ ] No dependency, provider, credential, network service, workflow, or nonzero budget is added.
- [ ] No live work order is committed as part of implementation.
- [ ] All valid, negative, ordering, replay, transition, and no-mutation tests pass.
- [ ] The complete existing test suite and Rules CI pass.
- [ ] Independent QA returns `PASS` and Review & Integration returns `APPROVE` against one immutable implementation head.
- [ ] The Studio Owner makes the final merge decision.

## 10. Rollback

Rollback of the later implementation is the ordinary revert of its implementation commit. The twelve implementation files may be removed together only by an authorized revert; the accepted contracts and memory history remain evidence.

After rollback, intake returns to the existing manual task-contract process. No project truth, source authority, Git history, credential, provider, or external service may be altered to manufacture recovery.

## 11. Explicit non-goals

This contract does not authorize:

- STUDIO-007B dispatcher or capability-registry behavior;
- STUDIO-007C writer claim, worktree provisioning, or handoff automation;
- STUDIO-007D failover or retry;
- STUDIO-007E quality-gate verdicts, telemetry, quota upgrades, or spend;
- STUDIO-007F adapters or any real/fake AI executor;
- automatic assignment, execution, review, approval, commit, push, merge, publishing, or deployment;
- installation, adaptation, import, vendoring, or execution of any external candidate;
- a game engine, framework, runtime provider, paid service, or production platform decision.

## 12. Workflow after contract merge

1. Reconcile the merged contract and memory package against current `main`.
2. Create `agent/studio-007a-work-order-queue` from the verified merge commit.
3. Acquire the single writer claim and refresh the memory package.
4. Create only the twelve implementation files in section 4.
5. Run focused, negative, full-suite, and Rules CI checks.
6. Obtain independent QA and Review & Integration verdicts against one immutable head.
7. Studio Owner decides whether to merge the implementation.
