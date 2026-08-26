# STUDIO-007A — Work Order & Producer Queue

Status: `PROPOSED — NOT ACCEPTED — NOT IMPLEMENTED`

Parent: `STUDIO-007`

Primary owner: Platform Studio

## Goal

Define a durable, deterministic work-order envelope and a file-backed producer queue for zero-cost local operation.

## Proposed contract

A work order must identify its ID, producer, requesting organizational unit, project, bounded objective, permitted paths, prohibited actions, required capabilities, inputs, expected outputs, acceptance gates, priority, budget ceiling, dependencies, attempt number, and Owner-gate requirement.

Queue state is data, not authority. Allowed v1.0 states are `DRAFT`, `READY`, `CLAIMABLE`, `CLAIMED`, `BLOCKED`, `QA_PENDING`, `OWNER_PENDING`, `DONE`, and `CANCELLED`. Every transition must record actor, timestamp, reason, and prior state. Only deterministic, append-safe local records are in scope.

## Proposed future implementation scope

- `platform/orchestration/WORK_ORDER_QUEUE.md`
- `platform/orchestration/schemas/work-order.schema.json`
- `platform/orchestration/schemas/queue-entry.schema.json`
- `platform/orchestration/fixtures/007a/`
- focused validator and tests approved in the implementation contract

These paths are reserved proposals, not permission to create them.

## Out of scope

- Automatic agent selection or execution.
- Network queues, databases, hosted services, cron jobs, or paid APIs.
- Provider configuration, credentials, prompts, or candidate installation.
- Changes to project truth or existing source-authority rules.

## Required tests for a future implementation

- Valid and invalid work-order fixtures.
- Deterministic ordering by explicit priority and creation sequence.
- Duplicate-ID rejection and idempotent replay.
- Illegal transition rejection.
- Path-scope and budget-ceiling validation.
- No-network test execution using existing repository tooling.

## Failure and rollback

If queue records are ambiguous, non-deterministic, or permit scope escalation, the contract fails. Rollback removes only 007A implementation artifacts and returns intake to the existing manual task-contract process; existing task files and project truth remain intact.

## Owner decisions required

- Accept the work-order fields and state vocabulary.
- Accept the implementation paths and validator approach.
- Decide who may promote `DRAFT` to `READY` and who may cancel work.
