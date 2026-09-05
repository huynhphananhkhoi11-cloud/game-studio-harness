# STUDIO-009V-01 STATE

memory_schema_version: 1

task_id: STUDIO-009V-01
state: FAILED_CAMPAIGN_ACKNOWLEDGED_RETRY1_AUTHORIZED
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-01-groq-live-validation
base_head: 2b811d7ac64e88c396f691cec940ec68784b1457
durability_state: PR_PENDING

provider: GroqCloud
provider_profile_id: provider-profile:groq-free-gpt-oss-120b
provider_child_id: STUDIO-009P-01
model: openai/gpt-oss-120b
host: api.groq.com
endpoint: /openai/v1/chat/completions
credential_profile_ref: credential-profile:groq-api-key
money_ceiling: 0
live_state_ceiling: LIVE_VALIDATED

completed: |
  - Verified STUDIO-009P-01 offline lifecycle is durably closed.
  - Verified STUDIO-009R-01 progressive live framework is durably closed.
  - Re-verified current official Groq model, endpoint, Free Plan limits, billing-tier distinction, ZDR capability, and tool capabilities.
  - Defined bounded V-01 contract and implementation scope.

remaining: |
  - Studio Owner must confirm the active Groq organization is Free tier, ZDR is enabled, and openai/gpt-oss-120b is permitted.
  - The first connected smoke must use a durable local request ledger that reserves each request before network I/O.
  - After the smoke, observed spend must be confirmed separately; code may not pre-claim observed spend zero.
  - Connected QA, Review and Owner disposition remain required before implementation merge.

blockers: |
  - NONE

provider_runtime_activity: GROQ_V01_FAILED_AUTH_CAMPAIGN_1_REQUEST
network_activity: GROQ_HTTPS_1_AUTH_FAILED_REQUEST
credential_runtime_activity: OWNER_INTERACTIVE_SESSION_ONLY
secret_store_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
routing_activity: NONE
connected_execution_activity: FAILED_AUTH_VALIDATION_ATTEMPT
spend: UNCONFIRMED

exact_next_action: Run the separately generated RETRY1 bounded connected-smoke runner using the newly created Default Project key. Do not reuse the old key, do not continue the failed campaign, and do not merge PR #60.
next_phase: STUDIO-009V-01_RETRY1_BOUNDED_CONNECTED_SMOKE

contract_merge: 2b811d7ac64e88c396f691cec940ec68784b1457
implementation_result: OFFLINE_READY
implementation_provider_live_state: LIVE_VALIDATION_READY
implementation_new_tests: 48
implementation_live_tests: 70
implementation_focused_tests: 525
implementation_total_tests: 922
implementation_real_request_count: 0
implementation_retry_count: 0
implementation_concurrency: 1
implementation_money_ceiling: 0
implementation_provider_runtime_activity: NONE
implementation_network_activity: NONE
implementation_credential_runtime_activity: NONE
implementation_tool_execution_activity: NONE
implementation_routing_activity: NONE
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
hardened_live_tests: 70
hardened_focused_tests: 527
hardened_total_tests: 924
real_request_count: 0
provider_live_state: LIVE_VALIDATION_READY
network_activity: NONE
credential_runtime_activity: NONE
connected_execution_activity: NONE
spend: ZERO
<!-- STUDIO-009V-01-PREFLIGHT-HARDENING-0002A -->

failed_campaign_id: groq-v01-782697ab855de1bd
failed_campaign_request_count: 1
failed_campaign_result: AUTH_FAILED
failed_campaign_terminal: true
failed_campaign_additional_request_authorized: false
old_key_revoked_owner_confirmed: true
new_key_created_in_default_project_owner_confirmed: true
fresh_retry_campaign_authorized_by_owner: true
retry1_request_ceiling: 3
retry1_concurrency: 1
retry1_retry_count: 0
retry1_money_ceiling: 0
provider_live_state: LIVE_VALIDATION_READY
observed_spend: UNCONFIRMED
implementation_pr_merge_allowed_now: false
<!-- STUDIO-009V-01-RETRY1-AUTHORIZATION-0003A -->
