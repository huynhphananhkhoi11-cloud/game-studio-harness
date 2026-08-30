# Writer claim, worktree record, and durable handoff v1.0

This STUDIO-007C capability validates repository evidence without creating authority or mutating Git. `tasks/STUDIO-007C-IMPLEMENTATION.md`, `studio/MEMORY_PROTOCOL.md`, and `studio/HANDOFF_PROTOCOL.md` remain authoritative.

## Boundaries

- A claim records one writer, one work order, an immutable base, an explicit UTC lease, and normalized repository-relative paths.
- Equal and ancestor/descendant paths conflict. A textual prefix without a path-component boundary does not conflict.
- Expiry invalidates ordinary writing but never transfers or releases authority.
- Renewal is a new immutable record from the same writer, issued before expiry, with unchanged identity and scope plus the prior record digest.
- Only a bounded, active `STUDIO_OWNER` exception may cover a declared overlap.
- A worktree record is evidence only. The validator never inspects, creates, changes, or deletes a filesystem worktree or Git reference.
- A durable handoff records exact base/current commits, bounded changed paths, checks, risks, blockers, and one resume action. It supplements rather than replaces canonical memory and handoff records.

## Read-only commands

```text
python -m scripts.orchestration_handoff validate-claim --claim CLAIM.json --as-of 2026-08-30T10:00:00Z
python -m scripts.orchestration_handoff validate-claim-set --claim-set CLAIMS.json --as-of 2026-08-30T10:00:00Z
python -m scripts.orchestration_handoff validate-worktree --claim CLAIM.json --worktree WORKTREE.json --expected-base COMMIT --expected-current COMMIT
python -m scripts.orchestration_handoff validate-handoff --claim CLAIM.json --worktree WORKTREE.json --handoff HANDOFF.json --expected-base COMMIT --expected-current COMMIT
python -m scripts.orchestration_handoff explain-handoff --claim CLAIM.json --worktree WORKTREE.json --handoff HANDOFF.json --expected-base COMMIT --expected-current COMMIT
```

All validation uses Python's standard library, explicit caller-supplied time and commit identities, deterministic JSON fixtures, and fail-closed nonzero exit status. It performs no network, provider, credential, subprocess, Git, publication, execution, routing, or paid action.
