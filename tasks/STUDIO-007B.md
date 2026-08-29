# STUDIO-007B â€” Capability Registry & Manual Dispatcher

Status: `APPROVED â€” NOT IMPLEMENTED`

Owner approval: `2026-08-29`

Implementation contract: `tasks/STUDIO-007B-IMPLEMENTATION.md`

Parent: `STUDIO-007`

Dependency: merged and verified `STUDIO-007A` implementation at Pull Request `#18`, merge commit `a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f`

Primary owner: Platform Studio

## Goal

Describe available execution capabilities and let the Studio Owner record one deterministic, explainable manual dispatch decision without granting candidates, role labels, or AI systems authority.

## Accepted contract

A capability record describes an executor ID, organizational role, capability tags, supported input/output types, constraints, availability, zero-cost class, trust level, eligibility, and evidence references. A dispatch decision links one validated `CLAIMABLE` work order to one selected executor and records its immutable work-order digest, the Studio Owner dispatcher, considered alternatives, evidence-based reason, decision time, and expiry.

Registry entries are evidence claims, not permissions or authentication. Only an `INTERNAL_ROLE` record with `ELIGIBLE`, `AVAILABLE`, `ZERO_COST`, compatible capabilities and supported data types may be selected. `REFERENCE`, `NOT_INSTALLED`, `NO_DECISION`, and `ADAPT_PENDING` records are never dispatchable.

Dispatch records do not execute work, mutate the Producer Queue, transition a work order to `CLAIMED`, create a worktree, or grant merge authority. Those actions remain reserved for later accepted contracts.

## Approved implementation direction

- `platform/orchestration/CAPABILITY_DISPATCH.md`
- provider-neutral JSON schemas and deterministic fixtures under `platform/orchestration/`
- a Python standard-library manual-dispatch validator/CLI
- focused no-network tests defined by `tasks/STUDIO-007B-IMPLEMENTATION.md`

The exact authorized paths, vocabulary, behavior, tests, and rollback are controlled by the implementation contract. That contract must merge before implementation begins.

## Accepted v1.0 vocabulary

Capability tags:

- `production.coordination`
- `game-design.systems`
- `narrative.research`
- `engineering.repository`
- `qa.validation`
- `review.integration`

Trust levels:

- `EVIDENCE_PENDING` â€” claim exists but evidence is not yet sufficient for dispatch.
- `EVIDENCE_VERIFIED` â€” declared evidence passed the bounded repository validation required by this contract.
- `RESTRICTED` â€” usable only when every declared constraint is satisfied.

Only `STUDIO_OWNER` may record an active dispatch decision in v1.0. `PRODUCER-01` may prepare work orders and non-binding alternatives but may not impersonate the human dispatcher or activate a selection.

## Out of scope

- Automated ranking, routing, bidding, matching, scheduling, or load balancing.
- New organizational roles, authentication, identity providers, or authority systems.
- Candidate installation, repository grafting, external prompts, dependencies, or network discovery.
- Real providers, credentials, paid services, model calls, execution, claims, worktrees, handoffs, commits, pushes, merges, publishing, or deployment.
- Changes to project truth, canon, source authority, or STUDIO-007A transition rules.

## Required tests

- Reject unknown, unavailable, ineligible, nonzero-cost, or insufficiently evidenced executors.
- Reject capability, input-type, output-type, constraint, work-order state, or work-order digest mismatch.
- Reject expired decisions using an explicit deterministic `as_of` timestamp.
- Prove every active dispatch has a `STUDIO_OWNER` actor, considered alternatives, evidence references, and a non-empty reason.
- Prove external-candidate statuses cannot be dispatched.
- Prove fixtures and CLI run without network access or repository mutation.

## Failure and rollback

If the registry silently creates authority, accepts unevaluated capability claims, performs automatic dispatch, mutates queue state, or permits an external candidate, the contract fails. Rollback removes only STUDIO-007B implementation artifacts; STUDIO-007A remains usable as a manual queue.

## Owner decisions resolved

- The initial capability and trust vocabularies above are accepted for the bounded v1.0 implementation.
- `STUDIO_OWNER` is the only active human dispatcher role in v1.0.
- Existing logical roles may be represented only as evidence-backed executor records; no new role is created.
- Dispatch expiry is evaluated against an explicit supplied UTC timestamp, never an implicit wall clock.
- No external candidate, provider, credential, network action, automatic selection, or nonzero monetary cost is authorized.