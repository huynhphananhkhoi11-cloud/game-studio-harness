# STUDIO-007C - Writer Claim, worktree & durable handoff

Status: `ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED`

Parent: `STUDIO-007`

Dependencies: accepted, implemented, reviewed, and merged `STUDIO-007A` and `STUDIO-007B`

Primary owner: Platform Studio; Project Studios retain ownership of project truth

Canonical implementation contract: `tasks/STUDIO-007C-IMPLEMENTATION.md`

## Goal

Prevent concurrent writers from silently colliding while preserving recoverable progress through evidence-only worktree records and durable handoffs.

## Accepted contract

A writer claim binds one work order, executor, branch, worktree identity, permitted repository-relative paths, immutable base commit, explicit lease interval, lifecycle status, and evidence references.

Only one active writer may hold a write scope. Exact and ancestor/descendant path overlap fails closed unless one Studio-Owner-approved exception identifies the affected claims, exact overlap, reason, approval evidence, and expiry.

A renewal is a new immutable claim record created by the same writer before the prior claim expires. It preserves work-order, executor, branch, worktree, base, and path scope and cites the prior claim digest. Expiry never transfers authority automatically.

A worktree record is evidence of isolation only. It does not create, modify, delete, or authorize a Git worktree, branch, commit, push, pull request, or merge.

A durable handoff records immutable base and current commit identities, completed and pending work, changed paths, validation evidence, risks, blockers, claim disposition, and an exact resume action. `studio/MEMORY_PROTOCOL.md` and `studio/HANDOFF_PROTOCOL.md` remain authoritative and are not replaced.

## Approved implementation boundary

The future implementation may create only the sixteen paths listed in section 4 of `tasks/STUDIO-007C-IMPLEMENTATION.md`, plus material-checkpoint updates to the four-record STUDIO-007C memory package.

Implementation must use Python standard library tooling, deterministic fixtures, explicit `as_of` input, repository-relative paths, and read-only validation. It must not inspect time implicitly or mutate Git.

## Out of scope

- Automatic branch or worktree creation, checkout, commit, push, pull request, merge, deletion, cleanup, or failover.
- Replacing Git, repository protections, source authority, memory protocol, or handoff protocol.
- Provider, model, credential, network, dependency, hosted service, or nonzero-cost integration.
- Multiple writers editing an overlapping path by default.
- Activating STUDIO-007D through STUDIO-007F.

## Required behavior

- Reject exact and ancestor/descendant path overlap.
- Reject stale, expired, mismatched, ambiguous, credential-bearing, or unsafe claims.
- Accept independent non-overlapping active claims.
- Validate renewal lineage without mutating the earlier claim.
- Accept an overlap exception only when recorded as Studio Owner approval with bounded scope and expiry.
- Verify worktree and handoff identities against explicit expected commits without invoking Git.
- Prove invalid inputs leave all source evidence byte-for-byte unchanged.

## Failure and rollback

The contract fails if claims overlap silently, expiry transfers authority, handoff evidence is not resumable, validation mutates repository history, or any Git/provider/credential action occurs without separate authority.

Rollback removes only the later STUDIO-007C implementation through an authorized revert. Accepted contracts and memory history remain evidence. Writer coordination then returns to the existing manual memory and handoff procedures.

## Owner decisions accepted

- One writer per overlapping path scope.
- Same-writer renewal only before expiry, using immutable lineage evidence.
- No automatic transfer after expiry.
- Studio Owner is the only overlap-exception authority in v1.0.
- Git automation remains separately prohibited.

Studio Owner acceptance date: `2026-08-29`.
