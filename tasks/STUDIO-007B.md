# STUDIO-007B — Capability Registry & Manual Dispatcher

Status: `PROPOSED — NOT ACCEPTED — NOT IMPLEMENTED`

Parent: `STUDIO-007`

Dependency: accepted and verified `STUDIO-007A`

Primary owner: Platform Studio

## Goal

Describe available execution capabilities and let a human dispatcher make a recorded, explainable assignment without granting candidates or AI systems authority.

## Proposed contract

A capability record describes an executor ID, capability tags, supported input/output types, constraints, availability, cost class, trust level, and evidence reference. A dispatch decision links one work order to one selected executor and records the human dispatcher, considered alternatives, reason, and expiry.

Registry entries are claims to validate, not permissions. `REFERENCE` candidates never become executors. `ADAPT` recommendations cannot enter the registry as usable capabilities until a separate Owner-accepted adaptation contract is implemented and verified.

## Proposed future implementation scope

- `platform/orchestration/CAPABILITY_DISPATCH.md`
- `platform/orchestration/schemas/capability-record.schema.json`
- `platform/orchestration/schemas/dispatch-decision.schema.json`
- `platform/orchestration/fixtures/007b/`
- focused validator and tests approved in the implementation contract

## Out of scope

- Automated ranking, routing, bidding, or load balancing.
- New organizational roles or authority systems.
- Candidate installation, repository grafting, external prompts, or dependencies.
- Real providers, credentials, paid services, or network discovery.

## Required tests for a future implementation

- Reject unknown or unavailable executor IDs.
- Reject capability mismatch and expired dispatch decisions.
- Prove every dispatch has a human actor and evidence-based reason.
- Prove `REFERENCE`, `NOT INSTALLED`, and `NO DECISION` candidates cannot be dispatched.
- Deterministic manual-dispatch fixtures and no-network execution.

## Failure and rollback

If the registry silently creates authority, accepts unevaluated capabilities, or performs automatic dispatch, the contract fails. Rollback removes only 007B artifacts; 007A remains usable as a manual queue.

## Owner decisions required

- Accept the initial capability vocabulary and trust levels.
- Name the humans allowed to record dispatch decisions.
- Approve any future executor or candidate adaptation separately.
