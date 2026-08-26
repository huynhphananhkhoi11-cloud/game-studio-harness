# STUDIO-007F — Provider-neutral adapter interface

Status: `PROPOSED — NOT ACCEPTED — NOT IMPLEMENTED`

Parent: `STUDIO-007`

Dependency: accepted and verified `STUDIO-007A` through `STUDIO-007E`

Primary owner: Platform Studio

## Goal

Define a narrow interface between orchestration records and an executor so future AI or tool providers can be evaluated without changing governance or project contracts.

## Proposed contract

An adapter accepts a validated work order plus explicitly referenced inputs and returns a normalized result containing status, outputs, evidence, usage counters, error class, handoff reference, and trace correlation ID. The adapter cannot change scope, approve gates, merge work, publish, reveal credentials, or select its own successor.

v1.0 includes only deterministic `manual` and `fake` adapters. A provider-specific adapter requires a separate Owner-accepted contract, threat review, credential plan, budget, tests, and rollback.

## Proposed future implementation scope

- `platform/orchestration/PROVIDER_ADAPTER.md`
- `platform/orchestration/schemas/adapter-request.schema.json`
- `platform/orchestration/schemas/adapter-result.schema.json`
- `platform/orchestration/schemas/adapter-capability.schema.json`
- `platform/orchestration/fixtures/007f/manual/`
- `platform/orchestration/fixtures/007f/fake/`
- focused conformance validator and tests approved in the implementation contract

## Out of scope

- Real provider SDKs, endpoints, accounts, credentials, or paid calls.
- DeepSeek harness, Agent Sprite Forge, repo graft, or any candidate integration.
- Prompt libraries, autonomous tool execution, repository mutation, or authority delegation.
- Provider-specific fields in the core work-order contract.

## Required tests for a future implementation

- Manual and fake adapter conformance against identical fixtures.
- Deterministic success, refusal, malformed-output, timeout, and failure results.
- Reject undeclared capabilities and scope expansion.
- Prove no network access and no credential requirement.
- Preserve gate, trace, quota, handoff, and failover semantics across adapters.

## Failure and rollback

If provider details leak into core contracts, an adapter gains authority, or tests require network access or credentials, the contract fails. Rollback removes only 007F artifacts; manual execution through 007A–007E remains available.

## Owner decisions required

- Accept the normalized request/result boundary.
- Accept manual and fake adapter behavior.
- Decide later whether any candidate warrants a separate adaptation contract.
- Approve every real provider, credential, and nonzero budget separately.
