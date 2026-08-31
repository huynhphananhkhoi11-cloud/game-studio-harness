# STUDIO-007F Resume

## Current checkpoint

The provider-neutral adapter implementation is committed on `agent/studio-007f-provider-adapter` and remains unmerged.

- Contract merge: `3e678e8beb480e8d1aaa1c0aa8a85baccfbb64b8`
- Implementation payload commit: `IMPLEMENTATION_COMMIT_PLACEHOLDER`
- PR checkpoint head: resolve from the Pull Request before every gate
- Implementation Pull Request: `IMPLEMENTATION_PR_PLACEHOLDER`
- Evidence target: 79 focused tests and 331 total tests

## Resume sequence

1. Confirm Rules CI succeeds on the exact implementation head.
2. Confirm the diff contains only the 19 authorized implementation paths and four memory paths.
3. Conduct independent QA against schema, lineage, zero-cost, provider-neutrality, determinism, and immutability requirements.
4. Conduct independent Review and Integration on the same immutable head.
5. Remediate findings on the same branch and repeat all gates when needed.
6. Merge only by explicit Studio Owner decision.
7. Create a separate closeout Pull Request that records final evidence and releases the writer claim.

## Stop conditions

Stop on a changed base, dirty worktree, scope beyond 23 paths, failing test, failed CI, mutable evidence, nondeterministic output, secret/provider/network field, nonzero cost, or any attempt to grant adapter authority.
