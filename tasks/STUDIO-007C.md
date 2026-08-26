# STUDIO-007C — Writer Claim, worktree & durable handoff

Status: `PROPOSED — NOT ACCEPTED — NOT IMPLEMENTED`

Parent: `STUDIO-007`

Dependency: accepted and verified `STUDIO-007A` and `STUDIO-007B`

Primary owner: Platform Studio; Project Studios retain ownership of project truth

## Goal

Prevent concurrent writers from silently colliding while preserving recoverable progress through isolated worktrees and durable handoffs.

## Proposed contract

A writer claim binds one work order, executor, branch/worktree identity, permitted paths, base commit, lease period, and status. Overlapping write scopes are rejected unless an Owner-approved exception is recorded. A worktree isolates changes but grants no merge authority.

A durable handoff records the immutable base and current commit, completed work, pending work, changed paths, validation evidence, risks, blockers, and exact resume command or action. Existing memory and handoff protocols remain authoritative; 007C references and validates them rather than replacing them.

## Proposed future implementation scope

- `platform/orchestration/WRITER_WORKTREE_HANDOFF.md`
- `platform/orchestration/schemas/writer-claim.schema.json`
- `platform/orchestration/schemas/worktree-record.schema.json`
- `platform/orchestration/schemas/durable-handoff.schema.json`
- `platform/orchestration/fixtures/007c/`
- focused validator and tests approved in the implementation contract

## Out of scope

- Automatic branch creation, commit, push, pull request, merge, or deletion.
- Replacing Git, repository protections, memory protocol, or source authority.
- Multiple writers editing the same path by default.
- Provider or credential integration.

## Required tests for a future implementation

- Detect exact and ancestor/descendant path overlap.
- Reject stale, expired, or mismatched claims.
- Accept independent non-overlapping claims.
- Verify handoff commit identities, required evidence, and resumability.
- Simulate a writer conflict without changing repository history.

## Failure and rollback

If claims can overlap silently, work cannot be resumed, or the control plane performs Git mutations without explicit authority, the contract fails. Rollback removes only 007C artifacts and returns writer coordination to existing manual claim and handoff procedures.

## Owner decisions required

- Accept claim lease and renewal rules.
- Accept overlap-exception authority.
- Approve any future automation of Git operations separately.
