# STUDIO-009V-04 TASK

memory_schema_version: 1

task_id: STUDIO-009V-04
task_title: Poolside / Laguna S 2.1 bounded connected validation
task_type: provider-specific connected-validation contract and later implementation
canonical_task_contract: tasks/STUDIO-009V-04.md
implementation_contract: tasks/STUDIO-009V-04-IMPLEMENTATION.md
parent_task: STUDIO-009
provider_parent: STUDIO-009P-04
live_governance_parent: STUDIO-009R-01
logical_role: Platform Studio / Connected Validation Cell

provider: Poolside standalone hosted inference API
provider_profile_id: provider-profile:poolside-direct-laguna-s-2.1
provider_child_id: STUDIO-009P-04
model_allowlist: poolside/laguna-s-2.1
credential_profile_ref: credential-profile:poolside-api-key
account_ref: account-ref:poolside-owner-account
cost_class: ZERO_COST_ONLY
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
money_ceiling: 0

task_status: OFFLINE_LIVE_IMPLEMENTATION_READY_PENDING_QA
contract_record_semantics: EFFECTIVE_WHEN_MERGED
base_head: 3726e2bd031ce2022f5a93ff1d40c404fb815682
p04_implementation_merge: e7ed2d087117eacad42141ca2d0c6587d16721dc
p04_closeout_merge: 3726e2bd031ce2022f5a93ff1d40c404fb815682
p04_final_review_head: 7d37dd64db07b63037ad4d3fb434757f3974a589
contract_branch: agent/studio-009v-04-poolside-laguna-s-contract
implementation_branch: agent/studio-009v-04-poolside-laguna-s-live-validation

first_campaign_input_token_ceiling: 4096
first_campaign_completion_token_ceiling: 1024
real_request_ceiling: 3
concurrency_ceiling: 1
automatic_retry_ceiling: 0
request_timeout_seconds_ceiling: 60
request_bytes_ceiling: 32768
response_bytes_ceiling: 131072
allowed_data_classifications: PUBLIC,SYNTHETIC
promotion_ceiling: LIVE_VALIDATED
routing_authority: NONE
worker_authority: NONE
tool_authority: NONE
pool_cli_authority: NONE
mcp_authority: NONE
acp_authority: NONE
production_authority: NONE
money_ceiling_currency: USD

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

v03_nvidia_state: CONNECTED_PREFLIGHT_FROZEN_ACCOUNT_VERIFICATION
p05_opencode_authority: NONE
next_gate: INDEPENDENT_OFFLINE_QA
<!-- STUDIO-009V-04-CONTRACT-CHECKPOINT-0001 -->


offline_live_implementation_base: a7beb556d19da1397cceb09431d47848e69c5b12
offline_live_implementation_scope_paths: 12
offline_live_implementation_memory_paths: 4
offline_live_implementation_cumulative_paths: 16
offline_live_state: LIVE_VALIDATION_READY
connected_validation_status: PENDING_REAL_SMOKE
quality_evaluation_status: PENDING_REAL_SMOKE
connected_execution_authorized: false
new_v04_tests: 119
offline_live_focused_tests: 881
offline_live_total_tests: 1386
offline_live_static_probes: 126
offline_live_provider_runtime_activity: NONE
offline_live_poolside_network_activity: NONE
offline_live_account_activity: NONE
offline_live_api_key_activity: NONE
offline_live_pool_cli_activity: NONE
offline_live_tool_activity: NONE
offline_live_mcp_activity: NONE
offline_live_acp_activity: NONE
offline_live_routing_activity: NONE
offline_live_spend: ZERO
<!-- STUDIO-009V-04-OFFLINE-LIVE-IMPLEMENTATION-CHECKPOINT-0002 -->
