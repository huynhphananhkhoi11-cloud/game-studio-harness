# STUDIO-007F Resume

## Current checkpoint

The provider-neutral adapter contract is accepted and recorded on `agent/studio-007f-contract`.

- Baseline: `2e0c661e438cc901e5a9f40e95357b2419e2665a`
- Contract commit: `CONTRACT_COMMIT_PLACEHOLDER`
- Contract Pull Request: `CONTRACT_PR_PLACEHOLDER`
- Runtime implementation: not started

## Resume sequence

1. Confirm the contract Pull Request head has successful Rules CI.
2. Review that exactly six contract/memory paths changed and no implementation path exists.
3. Merge only by explicit Studio Owner decision.
4. Fetch the resulting `main` merge commit.
5. Create `agent/studio-007f-provider-adapter` from that exact merge commit.
6. Implement only the nineteen paths and four memory updates authorized by the contract.
7. Run focused tests, retained regression, independent QA, Review and Integration, and Owner merge.
8. Finish with a separate closeout Pull Request.

## Stop conditions

Stop if the baseline changes unexpectedly, worktree is dirty, scope exceeds the contract, any provider/network/credential/cost field appears, Rules CI is absent or failing, or runtime implementation is requested before contract merge.
