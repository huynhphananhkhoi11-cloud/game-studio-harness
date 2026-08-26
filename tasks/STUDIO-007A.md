# STUDIO-007A — Work Order & Producer Queue

Status: `APPROVED — NOT IMPLEMENTED`

Owner approval: `2026-08-26`

Implementation contract: `tasks/STUDIO-007A-IMPLEMENTATION.md`

Parent: `STUDIO-007`

Primary owner: Platform Studio

## Goal

Define a durable, deterministic work-order envelope and a file-backed producer queue for zero-cost local operation.

## Proposed contract

A work order must identify its ID, producer, requesting organizational unit, project, bounded objective, permitted paths, prohibited actions, required capabilities, inputs, expected outputs, acceptance gates, priority, budget ceiling, dependencies, attempt number, and Owner-gate requirement.

Queue state is data, not authority. Allowed v1.0 states are `DRAFT`, `READY`, `CLAIMABLE`, `CLAIMED`, `BLOCKED`, `QA_PENDING`, `OWNER_PENDING`, `DONE`, and `CANCELLED`. Every transition must record actor, timestamp, reason, and prior state. Only deterministic, append-safe local records are in scope.

## Approved implementation direction

- `platform/orchestration/WORK_ORDER_QUEUE.md`
- `platform/orchestration/schemas/work-order.schema.json`
- `platform/orchestration/schemas/queue-entry.schema.json`
- `platform/orchestration/fixtures/007a/`
- Python standard-library CLI/validator and focused tests defined by the implementation contract

The exact authorized paths, behavior, tests, and rollback are controlled by `tasks/STUDIO-007A-IMPLEMENTATION.md`. That contract must merge before implementation begins.

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

## Owner decisions resolved

- The work-order fields and complete state vocabulary are accepted for compatibility.
- JSON is the provider-neutral record format; a Python standard-library implementation may validate and operate the zero-cost local queue without adding a dependency.
- `PRODUCER-01` may create and edit `DRAFT` records.
- Only the Studio Owner may authorize `DRAFT` to `READY` or cancel a work order.
- STUDIO-007A may activate only intake and basic queue transitions. `CLAIMED`, `QA_PENDING`, `OWNER_PENDING`, and `DONE` remain reserved and inactive until their dependent contracts are separately accepted and implemented.
- No AI/provider, credential, external candidate, network queue, hosted service, or nonzero monetary budget is authorized.
