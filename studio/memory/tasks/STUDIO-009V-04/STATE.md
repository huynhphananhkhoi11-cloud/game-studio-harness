# STUDIO-009V-04 STATE

memory_schema_version: 1

task_id: STUDIO-009V-04
state: OWNER_BOUNDED_SMOKE_AUTHORIZED_PENDING_EXECUTION
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-04-owner-bounded-smoke-authorization
last_observed_HEAD: e47210ec73c7a03e1cbce9abc67c84ac6e48f745
durability_state: OWNER_CONNECTED_PREFLIGHT_MERGED_BOUNDED_SMOKE_AUTHORIZATION_PENDING_MERGE

provider: Poolside standalone hosted inference API
provider_profile_id: provider-profile:poolside-direct-laguna-s-2.1
provider_child_id: STUDIO-009P-04
model_allowlist: poolside/laguna-s-2.1
credential_profile_ref: credential-profile:poolside-api-key
account_ref: account-ref:poolside-owner-account
money_ceiling: 0
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
allowed_data: PUBLIC_SYNTHETIC_ONLY
connected_authority: NONE
worker_authority: NONE
routing_authority: NONE
tool_authority: NONE
pool_cli_authority: NONE
mcp_authority: NONE
acp_authority: NONE

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

completed: |
  - P-04 offline provider child is durably COMPLETE.
  - P-04 implementation PR #74 merged at e7ed2d087117eacad42141ca2d0c6587d16721dc.
  - P-04 closeout PR #75 merged at 3726e2bd031ce2022f5a93ff1d40c404fb815682.
  - P-04 QA PASS and Review APPROVE are durable.
  - Poolside official model/Terms/CLI evidence re-verified for V-04 contract on 2026-09-09.
  - V-03 NVIDIA remains frozen at account verification.

remaining: |
  - Merge this bounded-smoke authorization checkpoint after exact-head CI verification.
  - Only after durable merge may the dedicated smoke runner ask for the API key through hidden local input.
  - Execute at most three fixed PUBLIC/SYNTHETIC requests, serially, retry 0, USD 0.
  - Stop on identity, billing, redirect, auth, quota, policy, quality or capability anomaly.
  - Record sanitized smoke/quality evidence; no raw key or raw provider output is committed.
  - Obtain Owner post-smoke monetary confirmation, then Connected QA and Review with zero extra calls.
  - Revoke/delete/invalidate the validation key server-side before final Owner disposition.
blockers: |
  - NONE at Owner connected preflight checkpoint.

exact_next_action: Verify this authorization PR and Rules CI, then Owner may merge it. After durable merge only, run the dedicated bounded-smoke runner; the key is entered only through its hidden session prompt.
next_phase: STUDIO-009V-04_EXECUTE_OWNER_AUTHORIZED_BOUNDED_SMOKE
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


qa_result: PASS
qa_reviewed_head: 224c6c10f49cabdb7033b26b1354fab3ea90daf4
qa_blockers: 0
qa_new_v04_tests: 119
qa_cli_regression_tests: 5
qa_focused_tests: 881
qa_total_tests: 1386
qa_probes: 101
qa_live_state: LIVE_VALIDATION_READY
qa_connected_validation_status: PENDING_REAL_SMOKE
qa_quality_evaluation_status: PENDING_REAL_SMOKE
connected_execution_authorized: false
qa_provider_runtime_activity: NONE
qa_poolside_network_activity: NONE
qa_account_activity: NONE
qa_api_key_activity: NONE
qa_pool_cli_activity: NONE
qa_tool_activity: NONE
qa_mcp_activity: NONE
qa_acp_activity: NONE
qa_routing_activity: NONE
qa_spend: ZERO
<!-- STUDIO-009V-04-OFFLINE-QA-CHECKPOINT-0003 -->


review_result: APPROVE
review_reviewed_qa_head: 80fc99b028d35ee77b221ab051fc25e1bad613f9
review_implementation_head: 224c6c10f49cabdb7033b26b1354fab3ea90daf4
review_blockers: 0
review_new_v04_tests: 119
review_cli_regression_tests: 5
review_focused_tests: 881
review_total_tests: 1386
review_probes: 152
review_live_state: LIVE_VALIDATION_READY
review_connected_validation_status: PENDING_REAL_SMOKE
review_quality_evaluation_status: PENDING_REAL_SMOKE
connected_execution_authorized: false
review_provider_runtime_activity: NONE
review_poolside_network_activity: NONE
review_account_activity: NONE
review_api_key_activity: NONE
review_pool_cli_activity: NONE
review_tool_activity: NONE
review_mcp_activity: NONE
review_acp_activity: NONE
review_routing_activity: NONE
review_spend: ZERO
<!-- STUDIO-009V-04-OFFLINE-REVIEW-CHECKPOINT-0004 -->

offline_implementation_pr: 77
offline_implementation_merge: 1848295279a4ebf5681c4a2026dd4c274738d52d
offline_implementation_review_head: 86df7f1174c4084a1f75c9d44750caf28da982d3
owner_connected_preflight: PASS
exact_model_confirmed: poolside/laguna-s-2.1
exact_direct_base_url_confirmed: https://inference.poolside.ai/v1
account_zero_cost_confirmed: true
no_billing_method_required_confirmed: true
no_purchase_required_confirmed: true
server_side_revocation_confirmed: true
terms_data_policy_compatible_confirmed: true
training_opt_out_enabled: true
no_paid_path_confirmed: true
owner_reports_validation_api_key_created: true
raw_api_key_input_into_game_runtime: false
raw_api_key_persisted_in_repo: false
real_request_authorized_by_this_checkpoint: false
real_request_count: 0
provider_live_state: LIVE_VALIDATION_READY
connected_validation_status: PENDING_REAL_SMOKE
quality_evaluation_status: PENDING_REAL_SMOKE
poolside_model_request_activity: NONE
billable_spend_usd: 0
next_gate: OWNER_AUTHORIZE_BOUNDED_SMOKE
<!-- STUDIO-009V-04-OWNER-CONNECTED-PREFLIGHT-CHECKPOINT-0005 -->

owner_bounded_smoke_authorization: PASS
owner_smoke_authorization_ref: owner-authorization:poolside-v04-e47210ec73c7
authorization_base_merge: e47210ec73c7a03e1cbce9abc67c84ac6e48f745
authorized_real_requests: 3
authorized_probe_ids: STRUCTURED_OUTPUT,BOUNDED_REASONING,SYNTHETIC_CODE_REVIEW
authorized_max_tokens_per_request: 128
authorized_concurrency: 1
authorized_retry: 0
authorized_data: PUBLIC_SYNTHETIC_ONLY
authorized_money_ceiling_usd: 0
authorized_pool_cli: false
authorized_tools: false
authorized_mcp: false
authorized_acp: false
authorized_routing: false
credential_input_mode: HIDDEN_OWNER_INTERACTIVE_SESSION_ONLY
real_request_count_at_authorization: 0
connected_execution_activity_at_authorization: NONE
network_activity_at_authorization: NONE
billable_spend_usd_at_authorization: 0
next_gate: EXECUTE_OWNER_AUTHORIZED_BOUNDED_SMOKE
<!-- STUDIO-009V-04-OWNER-BOUNDED-SMOKE-AUTHORIZATION-CHECKPOINT-0006 -->
