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

task_status: COMPLETE
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

next_gate: OWNER_MERGE_V02_CLOSEOUT
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

owner_bounded_smoke_authorization: PASS
owner_smoke_authorization_ref: owner-authorization:cloudflare-v02-6a38a1fb1c03
authorized_real_requests: 3
authorized_concurrency: 1
authorized_retry: 0
authorized_campaign_neuron_ceiling: 2000
authorized_money_ceiling_usd: 0
authorization_consumed: false
real_request_count: 0
provider_live_state: LIVE_VALIDATION_READY
provider_runtime_activity: NONE
network_activity: NONE
account_id_input_activity: NONE
api_token_input_activity: NONE
spend: ZERO
next_gate: EXECUTE_BOUNDED_SMOKE
<!-- STUDIO-009V-02-OWNER-BOUNDED-SMOKE-AUTHORIZATION-0004 -->

smoke_campaign_id: cloudflare-v02-405f777851bb5ca0
smoke_result: PASS
actual_smoke_token_name: GAME-STUDIO-009V-02-RETRY
preflight_token_name_recorded: GAME-STUDIO-009V-02
smoke_token_exposure_status: EXPOSED_IN_CHAT_IMAGE
smoke_token_revocation_confirmed: true
authorization_consumed: true
real_request_count: 3
network_attempt_count: 3
network_success_count: 3
reserved_neurons: 1536
estimated_neurons_from_token_usage: 37
quality_pass: true
human_correction_count: 0
observed_neurons: UNCONFIRMED
observed_spend: UNCONFIRMED
additional_real_request_authorized: false
provider_live_state: LIVE_VALIDATION_READY
next_gate: OWNER_POST_SMOKE_NEURON_SPEND_CONFIRMATION
<!-- STUDIO-009V-02-SMOKE-EVIDENCE-CORRECTED-0005B -->

owner_post_smoke_confirmation: PASS
provider_observed_neurons: 35.18
estimated_neurons_from_token_usage: 37
workers_plan_observed: FREE
workers_paid: false
payment_method_on_file: false
billable_usage_display: NO_DATA
invoice_display: NONE
billable_charge_observed_usd: 0
observed_spend_usd: 0
observed_spend_basis: OWNER_OBSERVED_NO_BILLABLE_USAGE_NO_INVOICE_FREE_PLAN_NO_PAYMENT_METHOD
cost_metric_observation: UNCONFIRMED
smoke_token_revocation_confirmed: true
additional_real_request_authorized: false
provider_live_state: LIVE_VALIDATION_READY
next_gate: CONNECTED_QA
<!-- STUDIO-009V-02-OWNER-NEURON-SPEND-CONFIRMATION-0005C -->

connected_qa_ref: qa:connected-cloudflare-v02-a7d8933418d6
qa_reviewed_head: a7d8933418d6dbb2102a85b984ecec77f0c0b3a4
qa_result: PASS
qa_blockers: 0
qa_independent_probes: 60
qa_smoke_tests: 20
qa_live_tests: 70
qa_focused_tests: 592
qa_total_tests: 989
qa_provider_calls: 0
qa_cloudflare_network_activity: NONE
qa_account_id_input_activity: NONE
qa_api_token_input_activity: NONE
additional_real_request_authorized: false
provider_live_state: LIVE_VALIDATION_READY
next_gate: CONNECTED_REVIEW
<!-- STUDIO-009V-02-CONNECTED-QA-CHECKPOINT-0005D -->

connected_review_ref: review:connected-cloudflare-v02-1564c628a8c8
review_reviewed_head: 1564c628a8c8312bb028de6c2e329c2674becb51
review_result: APPROVE
review_blockers: 0
review_independent_probes: 81
review_smoke_tests: 20
review_live_tests: 70
review_focused_tests: 592
review_total_tests: 989
review_provider_calls: 0
review_cloudflare_network_activity: NONE
review_account_id_input_activity: NONE
review_api_token_input_activity: NONE
additional_real_request_authorized: false
provider_live_state: LIVE_VALIDATION_READY
next_gate: OWNER_FINAL_DISPOSITION
<!-- STUDIO-009V-02-CONNECTED-REVIEW-CHECKPOINT-0005E -->

owner_disposition_ref: owner-disposition:cloudflare-v02-98699b6d605e
owner_disposition: ACCEPT_LIVE_VALIDATED
owner_disposition_basis: OWNER_EXPLICIT_ACCEPTANCE_IN_CHAT
owner_disposition_reviewed_head: 98699b6d605e6b13277b85278a243f6916b988bf
final_connected_validation_ref: connected-validation:cloudflare-v02
final_connected_validation_digest: sha256:807971a3a0f4c1cd094a5b15b0aef96d4193344da08e0298be60d7d994154e59
final_provider_live_state: LIVE_VALIDATED
final_live_state_digest: sha256:9d51b32848ba62732be5356e78cf338c2a7b6734ba4c913c4216a4e55473bd66
promotion_ceiling: LIVE_VALIDATED
worker_authority: NONE
routing_authority: NONE
ai_gateway_authority: NONE
additional_real_request_authorized: false
money_ceiling_usd: 0
finalization_provider_calls: 0
next_gate: OWNER_MERGE_PR64
<!-- STUDIO-009V-02-OWNER-FINAL-DISPOSITION-0005F -->

credential_cleanup_ref: owner-confirmation:cloudflare-v02-no-active-validation-token
initial_validation_token_status: DELETED
smoke_validation_token_status: DELETED
no_active_v02_user_api_tokens_observed: true
all_v02_validation_credentials_inactive: true
revocation_evidence_ref: revocation:cloudflare-v02-all-validation-tokens-owner-confirmed
global_api_key_used_by_v02: false
global_api_key_modified_by_v02_cleanup: false
final_provider_live_state: LIVE_VALIDATED
worker_authority: NONE
routing_authority: NONE
ai_gateway_authority: NONE
additional_real_request_authorized: false
money_ceiling_usd: 0
next_gate: OWNER_MERGE_V02_CREDENTIAL_CLEANUP_PR
<!-- STUDIO-009V-02-POST-MERGE-CREDENTIAL-CLEANUP-0006B -->

closeout_checkpoint: STUDIO-009V-02-CLOSEOUT-CHECKPOINT-0007
implementation_pr: 64
implementation_merge: 3665dcc702e82859c78311e7bde68cb01c5ec6b1
credential_cleanup_pr: 65
credential_cleanup_merge: 1ad620ab0cdb8fa662a0733fadbddde655c5ca31
closeout_result: COMPLETE
closeout_provider_live_state: LIVE_VALIDATED
closeout_smoke_tests: 20
closeout_live_tests: 70
closeout_focused_tests: 592
closeout_total_tests: 989
closeout_qa_result: PASS
closeout_review_result: APPROVE
closeout_owner_disposition: ACCEPT_LIVE_VALIDATED
closeout_initial_validation_token_deleted: true
closeout_smoke_validation_token_deleted: true
closeout_no_active_v02_validation_token: true
closeout_revocation_evidence_ref: revocation:cloudflare-v02-all-validation-tokens-owner-confirmed
closeout_worker_authority: NONE
closeout_routing_authority: NONE
closeout_ai_gateway_authority: NONE
closeout_additional_real_request_authorized: false
closeout_provider_calls: 0
closeout_cloudflare_network_activity: NONE
closeout_account_id_input_activity: NONE
closeout_api_token_input_activity: NONE
closeout_billable_spend_usd: 0
closeout_record_semantics: EFFECTIVE_WHEN_MERGED
next_phase: STUDIO-009P-03_PROVIDER_ONBOARDING_PLANNING_AFTER_DURABLE_V02_CLOSEOUT
<!-- STUDIO-009V-02-CLOSEOUT-CHECKPOINT-0007 -->
