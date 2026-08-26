# STUDIO-007 — Platform Orchestration umbrella

Status: `PROPOSED — NOT ACCEPTED — NOT IMPLEMENTED`

Proposed baseline: `main@1fa070f77338e12e76bccae2d7eff6bf24ad2ae6`

## 1. Purpose

Define the zero-cost v1.0 control plane that lets the GAME AI Studio issue, route, execute, review, recover, and trace work without granting an AI or external repository authority over Studio truth.

`STUDIO-007` is a task/milestone identifier. It is not a seventh organizational Studio.

## 2. Canonical separation

### Organizational units

- **Studio Owner**: final authority for acceptance, merge, publication, credentials, budget, and irreversible actions.
- **Platform Studio**: owns shared orchestration contracts and infrastructure.
- **Project Studios**: own product truth, project deliverables, release candidates, patches, and product live operations.
- **Dynamic Cells**: temporary execution teams created for bounded work orders.
- **Shared Expert Guilds**: advisory expertise such as QA, history, localization, legal, accessibility, community, and player support.

### Technical capabilities

Work order, queue, dispatcher, writer claim, worktree, durable handoff, simulated failover, quality gate, trace, quota/budget, and provider adapter are capabilities. They do not create organizational authority.

### Task and milestone codes

`STUDIO-001`, `STUDIO-002`, and later identifiers name bounded system-building work. Their count does not equal the number of organizational Studios.

## 3. Umbrella boundaries

This umbrella coordinates six independently reviewable contracts:

| Contract | Capability boundary | Dependency |
| --- | --- | --- |
| STUDIO-007A | Work Order & Producer Queue | existing governance |
| STUDIO-007B | Capability Registry & Manual Dispatcher | 007A |
| STUDIO-007C | Writer Claim, worktree & durable handoff | 007A–007B |
| STUDIO-007D | Simulated failover state machine | 007A–007C |
| STUDIO-007E | Gate, trace, quota & budget | 007A–007D |
| STUDIO-007F | Provider-neutral adapter interface | 007A–007E |

The dependency order defines integration sequencing, not permission to implement a later contract. Each child contract needs its own Owner acceptance, implementation branch, tests, review, and rollback.

## 4. Zero-cost v1.0 rules

- Use repository files, Git, existing CI, deterministic fixtures, and local standard-library tooling.
- Use manual or fake adapters only.
- Do not connect a real model/provider, credential, paid API, hosted queue, or external runtime.
- Do not install candidate code, dependencies, hooks, prompts, or runtime behavior.
- Candidate 01, 03, and 07 remain non-binding `ADAPT` recommendations only.
- Candidate 02, 04, 08, and 09 remain `REFERENCE` only and create no role or authority.
- Do not create a Publishing/Live Operations Studio. Shared build/release infrastructure belongs to Platform Studio; product release and live operations belong to each Project Studio.

## 5. Contract-package scope

This design package may add only:

- `tasks/STUDIO-007.md`
- `tasks/STUDIO-007A.md`
- `tasks/STUDIO-007B.md`
- `tasks/STUDIO-007C.md`
- `tasks/STUDIO-007D.md`
- `tasks/STUDIO-007E.md`
- `tasks/STUDIO-007F.md`

It may not add runtime code, schemas, fixtures, dependencies, workflows, provider integrations, credentials, decisions, or project content.

## 6. Acceptance criteria for this package

- The three layers above remain distinct.
- Each capability has one primary owner and explicit consumers.
- Child contracts have separate scope, tests, failure conditions, and rollback.
- No child contract is activated by merging this proposal package.
- Unresolved decisions are explicitly reserved for the Studio Owner.

## 7. Rollback

Revert the proposal commit or pull request. Because this package contains documentation only, rollback must not alter runtime behavior or project truth.

## 8. Owner decisions still required

- Accept, amend, or reject this umbrella.
- Activate 007A first; later contracts remain inactive until separately accepted.
- Approve any implementation file scope before code is written.
- Approve any future candidate adaptation contract.
- Approve any real provider, credential, spend, publication, or production action.
