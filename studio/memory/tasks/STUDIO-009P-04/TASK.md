# STUDIO-009P-04 TASK

memory_schema_version: 1

task_id: STUDIO-009P-04
task_title: Poolside / Laguna S 2.1 provider onboarding
canonical_task_contract: tasks/STUDIO-009P-04.md
implementation_contract: tasks/STUDIO-009P-04-IMPLEMENTATION.md
parent_task: STUDIO-009D
logical_role: Platform Studio / Provider Integration Cell
provider: Poolside standalone hosted inference API
model_allowlist: poolside/laguna-s-2.1
provider_profile_reserved: provider-profile:poolside-direct-laguna-s-2.1
credential_profile_reserved: credential-profile:poolside-api-key
account_ref_reserved: account-ref:poolside-owner-account
cost_class: ZERO_COST_ONLY
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
money_ceiling: 0
state: OFFLINE_IMPLEMENTATION_QA_PASS_PENDING_REVIEW
branch: agent/studio-009p-04-poolside-laguna-s-implementation
base_head: 99b852677c8c41114b52eefdad70760b63c0ceda
contract_merge: 99b852677c8c41114b52eefdad70760b63c0ceda
provider_runtime_activity: NONE
poolside_network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
pool_cli_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
acp_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO
objective: Define Poolside direct Laguna S 2.1 provider child contract without activating a real connection.
completion_boundary: Contract PR only. Offline implementation is forbidden until merge. Real Poolside activity requires separately merged STUDIO-009V-04.
v03_nvidia_state: CONNECTED_PREFLIGHT_FROZEN_ACCOUNT_VERIFICATION
p05_opencode_authority: NONE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
contract_checkpoint: STUDIO-009P-04-CONTRACT-CHECKPOINT-0001

implementation_checkpoint: STUDIO-009P-04-IMPLEMENTATION-CHECKPOINT-0002
implementation_base: 99b852677c8c41114b52eefdad70760b63c0ceda
implementation_scope_paths: 20
implementation_cumulative_pr_paths: 24
implementation_new_poolside_tests: 100
implementation_focused_tests: 762
implementation_total_tests: 1267
implementation_provider_profile_state: DISABLED
implementation_model_profile_state: DECLARED
implementation_child_evidence_class: SYNTHETIC
implementation_provider_runtime_activity: NONE
implementation_poolside_network_activity: NONE
implementation_account_runtime_activity: NONE
implementation_credential_runtime_activity: NONE
implementation_secret_store_activity: NONE
implementation_pool_cli_activity: NONE
implementation_tool_execution_activity: NONE
implementation_remote_mcp_activity: NONE
implementation_acp_activity: NONE
implementation_routing_activity: NONE
implementation_connected_execution_activity: NONE
implementation_spend: ZERO
next_phase: STUDIO-009P-04_INDEPENDENT_REVIEW_INTEGRATION
<!-- STUDIO-009P-04-IMPLEMENTATION-CHECKPOINT-0002 -->

qa_result: PASS
qa_reviewed_head: 9b0a208a8dd1a3c1382a20f9fd1c405fbf8fabf0
qa_blockers: 0
qa_new_poolside_tests: 100
qa_cli_regression_tests: 5
qa_focused_tests: 762
qa_total_tests: 1267
qa_probes: 112
qa_provider_runtime_activity: NONE
qa_poolside_network_activity: NONE
qa_credential_runtime_activity: NONE
qa_pool_cli_activity: NONE
qa_tool_execution_activity: NONE
qa_remote_mcp_activity: NONE
qa_acp_activity: NONE
qa_routing_activity: NONE
qa_connected_execution_activity: NONE
qa_spend: ZERO
<!-- STUDIO-009P-04-QA-CHECKPOINT-0003 -->
