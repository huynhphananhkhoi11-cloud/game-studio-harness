# STUDIO-009V-02 TASK

memory_schema_version: 1

task_id: STUDIO-009V-02
task_title: Cloudflare Workers AI bounded connected validation
task_type: provider-specific connected-validation contract and later implementation
canonical_task_contract: tasks/STUDIO-009V-02.md
implementation_contract: tasks/STUDIO-009V-02-IMPLEMENTATION.md
parent_task: STUDIO-009
provider_parent: STUDIO-009P-02
live_governance_parent: STUDIO-009R-01
logical_role: Platform Studio / Connected Validation Cell

provider: Cloudflare Workers AI
provider_profile_id: provider-profile:cloudflare-workers-ai-free-nemotron-3-super
provider_child_id: STUDIO-009P-02
model_allowlist: @cf/nvidia/nemotron-3-120b-a12b
credential_profile_ref: credential-profile:cloudflare-workers-ai-api-token
account_ref: account-ref:cloudflare-workers-ai-owner-account
cost_class: ZERO_COST_ONLY
money_ceiling: 0

task_status: OWNER_CONNECTED_PREFLIGHT_ACCEPTED_PENDING_SMOKE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
base_head: 2dc93b84951999cce22c5c5a6c9e956e722f3c18
planned_contract_branch: agent/studio-009v-02-cloudflare-contract
planned_implementation_branch: agent/studio-009v-02-cloudflare-live-validation

real_request_ceiling: 3
concurrency_ceiling: 1
automatic_retry_ceiling: 0
request_timeout_seconds_ceiling: 30
request_bytes_ceiling: 8192
response_bytes_ceiling: 65536
completion_tokens_ceiling: 256
campaign_neuron_ceiling: 2000
daily_game_neuron_ceiling: 8000
provider_free_snapshot_neurons_per_day: 10000
allowed_data_classifications: PUBLIC,SYNTHETIC
promotion_ceiling: LIVE_VALIDATED
routing_authority: NONE
worker_authority: NONE
ai_gateway_authority: NONE
money_ceiling_currency: USD

provider_runtime_activity: NONE
network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
ai_gateway_activity: NONE
unified_billing_activity: NONE
prepaid_credit_activity: NONE
tool_execution_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

legacy_p02_activation_boundary: STUDIO-009F_ONLY
v02_reconciliation_required: true
v02_connected_validation_authority: STUDIO-009V-02_ONLY
full_studio_acceptance_authority: STUDIO-009F
automatic_routing_authority: STUDIO-009E

next_gate: OWNER_AUTHORIZE_BOUNDED_SMOKE
<!-- STUDIO-009V-02-CONTRACT-CHECKPOINT-0001 -->

contract_pr: 62
contract_head: 756f54aa2c86eefc102b28ed1a31cd3e1cebf584
contract_merge: 2f9eeaf6b2bb56546155e3d962082bc20525a8cb
credential_bridge_correction_reason: EXISTING_SESSION_CREDENTIAL_BRIDGE_IS_GROQ_V01_SPECIFIC
credential_bridge_correction_strategy: DEDICATED_CLOUDFLARE_SESSION_BRIDGE
corrected_implementation_cumulative_paths_max: 22
shared_groq_bridge_modification_authority: NONE
provider_runtime_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
network_activity: NONE
spend: ZERO
next_gate: OWNER_MERGE_V02_CREDENTIAL_BRIDGE_CORRECTION
<!-- STUDIO-009V-02-CREDENTIAL-BRIDGE-CORRECTION-0001A -->

implementation_base: 2dc93b84951999cce22c5c5a6c9e956e722f3c18
implementation_branch: agent/studio-009v-02-cloudflare-live-validation
implementation_paths: 20
implementation_authorized_paths_max: 22
implementation_new_tests: 65
implementation_live_tests: 70
implementation_focused_tests: 592
implementation_total_tests: 989
provider_live_state: LIVE_VALIDATION_READY
connected_validation_status: PENDING_OWNER_CONNECTED_PREFLIGHT
credential_bridge: scripts/cloudflare_session_credential_bridge.py
shared_groq_bridge_modification: NONE
real_account_id_input: NONE
real_api_token_input: NONE
provider_runtime_activity: NONE
network_activity: NONE
spend: ZERO
next_gate: OWNER_CONNECTED_PREFLIGHT
<!-- STUDIO-009V-02-IMPLEMENTATION-CHECKPOINT-0002 -->

owner_connected_preflight: PASS
workers_plan_observed: FREE
token_name: GAME-STUDIO-009V-02
token_permissions: WORKERS_AI_READ+WORKERS_AI_EDIT
token_scope: THIS_ACCOUNT_ONLY
account_id_ready_locally: true
api_token_ready_locally: true
raw_account_id_persisted: false
api_token_persisted: false
neuron_usage_observability: UNAVAILABLE_BEFORE_FIRST_INFERENCE
headroom_preconfirmation: UNAVAILABLE
free_allocation_fail_closed_code: 3036
real_request_authorized_by_this_checkpoint: false
provider_runtime_activity: NONE
network_activity: NONE
spend: ZERO
<!-- STUDIO-009V-02-OWNER-CONNECTED-PREFLIGHT-0003 -->
