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

task_status: CONTRACT_READY_FOR_OWNER_MERGE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
base_head: 11c2c2d4a35f37c5712376a3e7b16ca22d848bc7
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

next_gate: OWNER_MERGE_CONTRACT
