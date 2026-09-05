# STUDIO-009V-01 RESUME

memory_schema_version: 1

task_id: STUDIO-009V-01
package_path: studio/memory/tasks/STUDIO-009V-01
canonical_task_contract: tasks/STUDIO-009V-01.md
current_state: FAILED_CAMPAIGN_ACKNOWLEDGED_RETRY1_AUTHORIZED
resume_from: 2b811d7ac64e88c396f691cec940ec68784b1457
branch: agent/studio-009v-01-groq-live-validation

safe_checkpoint: STUDIO-009R-01 is durably closed; Groq P-01 is offline COMPLETE and remains connected DISABLED.

next_action: Run the separately generated RETRY1 bounded connected-smoke runner with the new Default Project key. Do not continue or rerun the failed campaign and do not merge PR #60.

prohibited_next_actions: reuse of revoked key; continuation of failed campaign; additional request under failed campaign; tools/browser/code execution/MCP/search/storage; automatic retry; routing; worker promotion; nonzero spend; implementation PR merge before connected QA/Review/Owner disposition; Unity/game work.

fallback: accepted MANUAL/FAKE no-network path.

money_ceiling: 0
provider_runtime_activity: GROQ_V01_FAILED_AUTH_CAMPAIGN_1_REQUEST
network_activity: GROQ_HTTPS_1_AUTH_FAILED_REQUEST
credential_runtime_activity: OWNER_INTERACTIVE_SESSION_ONLY
connected_execution_activity: FAILED_AUTH_VALIDATION_ATTEMPT
spend: UNCONFIRMED

next_gate: RETRY1_BOUNDED_CONNECTED_SMOKE

contract_merge: 2b811d7ac64e88c396f691cec940ec68784b1457
implementation_checkpoint: STUDIO-009V-01-IMPLEMENTATION-CHECKPOINT-0002
provider_live_state: LIVE_VALIDATION_READY
new_tests: 48
focused_tests: 525
total_tests: 922
real_request_count: 0
network_activity: NONE
credential_runtime_activity: NONE
connected_execution_activity: NONE
spend: ZERO
implementation_pr_merge_allowed_now: false
next_phase: STUDIO-009V-01_OWNER_CONNECTED_PREFLIGHT
<!-- STUDIO-009V-01-IMPLEMENTATION-CHECKPOINT-0002 -->

preflight_hardening_checkpoint: STUDIO-009V-01-PREFLIGHT-HARDENING-0002A
model_permission_confirmation_required: true
durable_request_reservation_required: true
post_smoke_spend_confirmation_required: true
observed_spend_claim_before_owner_confirmation: FORBIDDEN
new_tests: 50
focused_tests: 527
total_tests: 924
real_request_count: 0
provider_live_state: LIVE_VALIDATION_READY
spend: ZERO
implementation_pr_merge_allowed_now: false
<!-- STUDIO-009V-01-PREFLIGHT-HARDENING-0002A -->

failed_campaign_id: groq-v01-782697ab855de1bd
failed_campaign_terminal: true
failed_campaign_request_count: 1
failed_campaign_result: AUTH_FAILED
failed_campaign_additional_request_authorized: false
old_key_revoked_owner_confirmed: true
new_key_created_in_default_project_owner_confirmed: true
fresh_retry_campaign_authorized_by_owner: true
retry1_request_ceiling: 3
retry1_concurrency: 1
retry1_retry_count: 0
provider_live_state: LIVE_VALIDATION_READY
observed_spend: UNCONFIRMED
implementation_pr_merge_allowed_now: false
next_phase: STUDIO-009V-01_RETRY1_BOUNDED_CONNECTED_SMOKE
<!-- STUDIO-009V-01-RETRY1-AUTHORIZATION-0003A -->
