# STUDIO-007F State

- memory_schema_version: 1
- task_id: STUDIO-007F
- lifecycle_state: IMPLEMENTATION_PR_OPEN
- durability_state: UNMERGED
- canonical_task_contract: tasks/STUDIO-007F-IMPLEMENTATION.md
- contract_merge: 3e678e8beb480e8d1aaa1c0aa8a85baccfbb64b8
- implementation_branch: agent/studio-007f-provider-adapter
- implementation_payload_commit: c5aefed34640d1df892b4fb191690f4317c4f78f
- implementation_pr: https://github.com/huynhphananhkhoi11-cloud/game-studio-harness/pull/32
- pr_checkpoint_head: RESOLVE_FROM_PULL_REQUEST
- runtime_implementation_created: true
- provider_boundary: MANUAL_AND_FAKE_ONLY
- focused_tests: 98
- retained_baseline_tests: 252
- expected_total_tests: 350
- cost_class: ZERO_COST
- writer_claim: IMPLEMENTATION_BRANCH_ONLY
- next_gate: OWNER_MERGE_AFTER_FINAL_RULES_CI

## Invariants

- Scope is at most the exact 23 paths authorized by contract.
- No real provider, SDK, account, credential, network access, or nonzero cost exists.
- Adapter results do not grant orchestration or merge authority.
- Studio Owner retains the merge decision.
## QA remediation checkpoint

- hardening_commit: 1cf60b54de7d6dd68a53dfe67a8a8a953a35ea06
- evidence: 98 focused provider-adapter tests and 350 total tests PASS
- remediation: bind FAKE operations to deterministic results; enforce declared input/output kinds and lineage; reject duplicate/hidden/oversized/noncanonical/secret-bearing inputs
- next_gate: repeat independent QA and Review & Integration on the checkpoint head; do not merge yet
## Final QA and Review checkpoint

- reviewed_head: 64c30dcb0a17610df064e8cbebbe7a4827b0136a
- remediation_commit: c2ed85fe9a4fe10ff15c7d8556be9e0fb1a46fb7
- qa_01: PASS
- review_integration: APPROVE
- evidence: 98 focused provider-adapter tests and 350 total tests PASS
- blocking_findings: 0
- next_gate: Rules CI on the final checkpoint head, then explicit Studio Owner merge decision
