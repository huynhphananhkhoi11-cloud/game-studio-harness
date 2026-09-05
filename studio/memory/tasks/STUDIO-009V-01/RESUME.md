# STUDIO-009V-01 RESUME

memory_schema_version: 1

task_id: STUDIO-009V-01
package_path: studio/memory/tasks/STUDIO-009V-01
canonical_task_contract: tasks/STUDIO-009V-01.md
current_state: OFFLINE_IMPLEMENTATION_HARDENED_READY_FOR_OWNER_PREFLIGHT
resume_from: 2b811d7ac64e88c396f691cec940ec68784b1457
branch: agent/studio-009v-01-groq-live-validation

safe_checkpoint: STUDIO-009R-01 is durably closed; Groq P-01 is offline COMPLETE and remains connected DISABLED.

next_action: Confirm Free tier, ZDR, and GPT-OSS 120B model permission in Groq Console; then run the bounded connected-smoke runner with durable request reservation. Do not merge PR #60 yet.

prohibited_next_actions: real Groq API key entry; credential resolution; Groq/network/model call; tools/browser/code execution/MCP/search/storage; automatic retry; routing; worker promotion; repository write authority; nonzero spend; Unity/game work.

fallback: accepted MANUAL/FAKE no-network path.

money_ceiling: 0
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
connected_execution_activity: NONE
spend: ZERO

next_gate: OWNER_CONNECTED_PREFLIGHT

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
