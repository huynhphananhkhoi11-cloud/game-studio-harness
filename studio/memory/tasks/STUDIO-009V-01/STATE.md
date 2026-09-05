# STUDIO-009V-01 STATE

memory_schema_version: 1

task_id: STUDIO-009V-01
state: CONNECTED_REVIEW_APPROVE_PENDING_OWNER_DISPOSITION
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

provider_runtime_activity: GROQ_V01_TOTAL_4_REQUESTS_RETRY1_PASS
network_activity: GROQ_HTTPS_TOTAL_4_REQUESTS_1_AUTH_FAILED_3_RETRY1_PASS
credential_runtime_activity: OWNER_INTERACTIVE_SESSION_ONLY
secret_store_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
routing_activity: NONE
connected_execution_activity: RETRY1_BOUNDED_VALIDATION_PASS_AFTER_AUTH_FAILURE
spend: ZERO

exact_next_action: Studio Owner revokes the temporary RETRY1 Groq API key, records final V-01 disposition, and only then materializes LIVE_VALIDATED evidence. Do not make another Groq request and do not merge PR #60 yet.
next_phase: STUDIO-009V-01_OWNER_DISPOSITION

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

real_smoke_campaign: groq-v01-retry1-ac2943edca636f95
retry_attempt: RETRY1
retry_authorization_head: 68d9a89becb13b441c2e5744cd3b134a76d03bd3
retry_of_failed_campaign_id: groq-v01-782697ab855de1bd
prior_failed_campaign_request_count: 1
cumulative_v01_real_request_count: 4
real_request_count: 3
real_request_ceiling: 3
real_concurrency: 1
real_retry_count: 0
real_quality_result: PASS
real_human_correction_count: 0
provider_live_state: LIVE_VALIDATION_READY
observed_spend: UNCONFIRMED
post_smoke_spend_confirmation_required: true
additional_real_request_authorized: false
implementation_pr_merge_allowed_now: false
<!-- STUDIO-009V-01-RETRY1-SMOKE-CHECKPOINT-0003B -->

owner_spend_confirmation: PASS
account_tier_observed: FREE
usage_cost_display: <0.01 USD
usage_cost_display_is_not_zero: true
billable_charge_observed_usd: 0
observed_spend_usd: 0
observed_spend_basis: OWNER_OBSERVED_BILLABLE_CHARGE_ON_FREE_TIER
provider_live_state: LIVE_VALIDATION_READY
additional_real_request_authorized: false
implementation_pr_merge_allowed_now: false
next_phase: STUDIO-009V-01_CONNECTED_QA
<!-- STUDIO-009V-01-OWNER-SPEND-CONFIRMATION-0003C -->

connected_qa_ref: qa:connected-groq-v01-2b803e9e6ad3
qa_reviewed_head: 2b803e9e6ad3e1e75432f61aefa161a1a9e64595
qa_result: PASS
qa_blockers: 0
qa_independent_probes: 60
qa_live_tests: 70
qa_focused_tests: 527
qa_total_tests: 924
qa_provider_calls: 0
qa_groq_network_activity: NONE
qa_credential_input_activity: NONE
qa_spend: ZERO
provider_live_state: LIVE_VALIDATION_READY
implementation_pr_merge_allowed_now: false
next_phase: STUDIO-009V-01_CONNECTED_REVIEW
<!-- STUDIO-009V-01-CONNECTED-QA-CHECKPOINT-0003D -->

connected_review_ref: review:connected-groq-v01-1f31119f7f5d
review_reviewed_head: 1f31119f7f5d00db781f5fc60653312dfa25c7d3
review_result: APPROVE
review_blockers: 0
review_independent_probes: 80
review_live_tests: 70
review_focused_tests: 527
review_total_tests: 924
review_provider_calls: 0
review_groq_network_activity: NONE
review_api_key_input_activity: NONE
review_spend: ZERO
provider_live_state: LIVE_VALIDATION_READY
retry1_key_revocation_confirmation: PENDING
owner_disposition_ref: PENDING
implementation_pr_merge_allowed_now: false
next_phase: STUDIO-009V-01_OWNER_DISPOSITION
<!-- STUDIO-009V-01-CONNECTED-REVIEW-CHECKPOINT-0003E -->
