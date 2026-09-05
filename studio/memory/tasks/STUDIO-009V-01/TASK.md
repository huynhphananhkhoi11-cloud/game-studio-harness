# STUDIO-009V-01 TASK

memory_schema_version: 1

task_id: STUDIO-009V-01
task_title: Groq bounded connected validation
task_type: provider-specific connected-validation contract and implementation
canonical_task_contract: tasks/STUDIO-009V-01.md
implementation_contract: tasks/STUDIO-009V-01-IMPLEMENTATION.md
parent_task: STUDIO-009
provider_parent: STUDIO-009P-01
live_governance_parent: STUDIO-009R-01
logical_role: Platform Studio / Connected Validation Cell
provider: GroqCloud
provider_profile_id: provider-profile:groq-free-gpt-oss-120b
provider_child_id: STUDIO-009P-01
model_allowlist: openai/gpt-oss-120b
credential_profile_ref: credential-profile:groq-api-key
cost_class: ZERO_COST_ONLY
money_ceiling: 0

task_status: OFFLINE_IMPLEMENTATION_HARDENED_READY_FOR_OWNER_PREFLIGHT
contract_record_semantics: EFFECTIVE_WHEN_MERGED
base_head: 2b811d7ac64e88c396f691cec940ec68784b1457
planned_contract_branch: agent/studio-009v-01-groq-contract
planned_implementation_branch: agent/studio-009v-01-groq-live-validation

real_request_ceiling: 3
concurrency_ceiling: 1
automatic_retry_ceiling: 0
request_timeout_seconds_ceiling: 30
request_bytes_ceiling: 8192
response_bytes_ceiling: 65536
completion_tokens_ceiling: 256
allowed_data_classifications: PUBLIC,SYNTHETIC
promotion_ceiling: LIVE_VALIDATED
routing_authority: NONE
worker_authority: NONE
money_ceiling_currency: USD

provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

next_gate: OWNER_CONNECTED_PREFLIGHT

contract_pr: 59
contract_head: 297d93a3b8dba6a1dd33eb87237dc12df47cba03
contract_merge: 2b811d7ac64e88c396f691cec940ec68784b1457
implementation_status: OFFLINE_IMPLEMENTATION_READY_FOR_CONNECTED_PREFLIGHT
implementation_scope_paths: 16
implementation_cumulative_paths: 20
implementation_new_tests: 48
implementation_live_tests: 70
implementation_focused_tests: 525
implementation_total_tests: 922
implementation_provider_live_state: LIVE_VALIDATION_READY
implementation_real_request_count: 0
implementation_provider_runtime_activity: NONE
implementation_network_activity: NONE
implementation_credential_runtime_activity: NONE
implementation_connected_execution_activity: NONE
implementation_spend: ZERO
implementation_next_gate: OWNER_CONNECTED_PREFLIGHT
<!-- STUDIO-009V-01-IMPLEMENTATION-CHECKPOINT-0002 -->

preflight_hardening_result: PASS
model_permission_confirmation_required: true
durable_request_reservation_required: true
post_smoke_spend_confirmation_required: true
observed_spend_claim_before_owner_confirmation: FORBIDDEN
hardened_new_tests: 50
hardened_focused_tests: 527
hardened_total_tests: 924
real_request_count: 0
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
spend: ZERO
<!-- STUDIO-009V-01-PREFLIGHT-HARDENING-0002A -->
