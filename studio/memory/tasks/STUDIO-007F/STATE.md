# STUDIO-007F State

- memory_schema_version: 1
- task_id: STUDIO-007F
- lifecycle_state: IMPLEMENTATION_PR_OPEN
- durability_state: UNMERGED
- canonical_task_contract: tasks/STUDIO-007F-IMPLEMENTATION.md
- contract_merge: 3e678e8beb480e8d1aaa1c0aa8a85baccfbb64b8
- implementation_branch: agent/studio-007f-provider-adapter
- implementation_payload_commit: IMPLEMENTATION_COMMIT_PLACEHOLDER
- implementation_pr: IMPLEMENTATION_PR_PLACEHOLDER
- pr_checkpoint_head: RESOLVE_FROM_PULL_REQUEST
- runtime_implementation_created: true
- provider_boundary: MANUAL_AND_FAKE_ONLY
- focused_tests: 79
- retained_baseline_tests: 252
- expected_total_tests: 331
- cost_class: ZERO_COST
- writer_claim: IMPLEMENTATION_BRANCH_ONLY
- next_gate: RULES_CI_THEN_INDEPENDENT_QA_AND_REVIEW

## Invariants

- Scope is at most the exact 23 paths authorized by contract.
- No real provider, SDK, account, credential, network access, or nonzero cost exists.
- Adapter results do not grant orchestration or merge authority.
- Studio Owner retains the merge decision.
