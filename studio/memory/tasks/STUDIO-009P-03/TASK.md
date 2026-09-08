# STUDIO-009P-03 TASK

memory_schema_version: 1

task_id: STUDIO-009P-03
task_title: NVIDIA NIM / DeepSeek V4 Pro 0813 provider onboarding
canonical_task_contract: tasks/STUDIO-009P-03.md
implementation_contract: tasks/STUDIO-009P-03-IMPLEMENTATION.md
parent_task: STUDIO-009D
logical_role: Platform Studio / Provider Integration Cell
provider: NVIDIA-hosted NIM API Catalog
model_allowlist: deepseek-ai/deepseek-v4-pro-0813
provider_profile_reserved: provider-profile:nvidia-nim-free-deepseek-v4-pro-0813
credential_profile_reserved: credential-profile:nvidia-nim-api-key
account_ref_reserved: account-ref:nvidia-developer-program-owner-account
cost_class: ZERO_COST_ONLY
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
money_ceiling: 0
state: COMPLETE
branch: agent/studio-009p-03-nvidia-nim-closeout
contract_merge: 11830798fc41c43d517c007fc4adec653d0aaaaf
provider_runtime_activity: NONE
network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO
objective: Deterministically implement the NVIDIA NIM provider child offline/synthetically without activating a real connection.
completion_boundary: Implementation PR only. Real NVIDIA activity requires separately merged STUDIO-009V-03.
p04_poolside_authority: NONE
p05_opencode_authority: NONE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
contract_checkpoint: STUDIO-009P-03-CONTRACT-CHECKPOINT-0001
implementation_checkpoint: STUDIO-009P-03-IMPLEMENTATION-CHECKPOINT-0002

qa_result: PASS
qa_reviewed_head: a06a737fb32bb3dc195a871fa1580a33bd31c09a
qa_blockers: 0
qa_new_nvidia_tests: 64
qa_focused_tests: 548
qa_total_tests: 1053
qa_probes: 66
qa_provider_runtime_activity: NONE
qa_network_activity: NONE
qa_credential_runtime_activity: NONE
qa_tool_execution_activity: NONE
qa_routing_activity: NONE
qa_spend: ZERO
<!-- STUDIO-009P-03-QA-CHECKPOINT-0003 -->

review_result: APPROVE
reviewed_qa_head: b81f52e1ee31aa566c81e69fc343d686652b2b98
review_blockers: 0
review_new_nvidia_tests: 64
review_focused_tests: 548
review_total_tests: 1053
review_probes: 113
review_provider_runtime_activity: NONE
review_network_activity: NONE
review_credential_runtime_activity: NONE
review_tool_execution_activity: NONE
review_routing_activity: NONE
review_spend: ZERO
<!-- STUDIO-009P-03-REVIEW-CHECKPOINT-0004 -->

implementation_pr: 68
implementation_merge: ac04040f40f544d70db10dba975481b7da5930ea
final_review_head: b8e19364e8795acc7edf750c5c6d3ca3b345841a
completion_result: COMPLETE
completion_new_nvidia_tests: 64
completion_focused_tests: 548
completion_total_tests: 1053
completion_provider_profile_state: DISABLED
completion_model_profile_state: DECLARED
completion_child_evidence_class: SYNTHETIC
completion_provider_runtime_activity: NONE
completion_network_activity: NONE
completion_account_runtime_activity: NONE
completion_credential_runtime_activity: NONE
completion_secret_store_activity: NONE
completion_tool_execution_activity: NONE
completion_remote_mcp_activity: NONE
completion_routing_activity: NONE
completion_connected_execution_activity: NONE
completion_spend: ZERO
completion_real_provider_approved_for_connection: false
closeout_record_semantics: EFFECTIVE_WHEN_MERGED
next_phase: STUDIO-009V-03_CONTRACT
<!-- STUDIO-009P-03-CLOSEOUT-CHECKPOINT-0005 -->
