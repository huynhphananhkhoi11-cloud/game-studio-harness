# STUDIO-007F State

- memory_schema_version: 1
- task_id: STUDIO-007F
- lifecycle_state: CONTRACT_PR_OPEN
- durability_state: UNMERGED
- canonical_task_contract: tasks/STUDIO-007F-IMPLEMENTATION.md
- dependency_baseline: 2e0c661e438cc901e5a9f40e95357b2419e2665a
- contract_branch: agent/studio-007f-contract
- implementation_branch: agent/studio-007f-provider-adapter
- contract_commit: 3d13ad940ab45e14f4c1e882b078c5762f036f55
- contract_pr: https://github.com/huynhphananhkhoi11-cloud/game-studio-harness/pull/31
- runtime_implementation_created: false
- provider_boundary: MANUAL_AND_FAKE_ONLY
- cost_class: ZERO_COST
- writer_claim: CONTRACT_BRANCH_ONLY
- next_gate: RULES_CI_AND_OWNER_CONTRACT_MERGE

## Invariants

- No STUDIO-007F implementation path exists on this contract branch.
- Contract scope is exactly six paths.
- A real provider cannot be enabled by configuration or fixture substitution.
- The Studio Owner retains merge authority.
