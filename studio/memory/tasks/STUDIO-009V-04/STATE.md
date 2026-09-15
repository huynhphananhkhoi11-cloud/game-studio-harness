# STUDIO-009V-04 STATE

memory_schema_version: 1

task_id: STUDIO-009V-04
state: SMOKE_PASS_OWNER_ZERO_COST_CONFIRMED_PENDING_CONNECTED_QA
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-04-smoke-evidence-owner-zero-cost
last_observed_HEAD: c966b37a96794e7471463b631796bb7e1259d366
durability_state: AUTHORIZATION_MERGED_SMOKE_PASS_OWNER_ZERO_COST_CONFIRMATION_PENDING_MERGE

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

provider_runtime_activity: BOUNDED_SMOKE_COMPLETE
poolside_network_activity: EXACTLY_3_SUCCESSFUL_REQUESTS
account_runtime_activity: NONE
credential_runtime_activity: SESSION_ONLY_COMPLETED
secret_store_activity: NONE
pool_cli_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
acp_activity: NONE
routing_activity: NONE
connected_execution_activity: BOUNDED_SMOKE_COMPLETE
spend: ZERO_OWNER_CONFIRMED

completed: |
  - P-04 offline provider child is durably COMPLETE.
  - P-04 implementation PR #74 merged at e7ed2d087117eacad42141ca2d0c6587d16721dc.
  - P-04 closeout PR #75 merged at 3726e2bd031ce2022f5a93ff1d40c404fb815682.
  - P-04 QA PASS and Review APPROVE are durable.
  - Poolside official model/Terms/CLI evidence re-verified for V-04 contract on 2026-09-09.
  - V-03 NVIDIA remains frozen at account verification.

remaining: |
  - Merge this smoke-evidence / Owner zero-cost-confirmation checkpoint after exact-head CI verification.
  - Run independent Connected QA against the immutable merged evidence; zero additional Poolside requests.
  - Run Connected Review/Integration against the immutable QA head; zero additional Poolside requests.
  - Revoke/delete/invalidate the validation key server-side after Connected Review and record safe revocation evidence.
  - Record final Owner disposition; promotion ceiling remains LIVE_VALIDATED and routing remains unauthorized.
blockers: |
  - NONE for progression to independent Connected QA after this checkpoint is durably merged.
exact_next_action: Merge this exact smoke-evidence / Owner zero-cost-confirmation checkpoint after Rules CI success, then run independent Connected QA with zero provider calls.
next_phase: STUDIO-009V-04_CONNECTED_QA
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


smoke_campaign_id: campaign:poolside-v04-c966b37a
smoke_result: PASS
authorization_consumed: true
real_request_count: 3
network_success_count: 3
quality_pass: true
human_correction_count: 0
owner_post_smoke_zero_cost_confirmation: PASS
owner_observed_charge_usd: 0
provider_billing_surface_observation: NOT_EXPOSED
provider_metered_charge_usd: UNAVAILABLE
public_free_api_offer_class: FREE_FOR_LIMITED_TIME
observed_spend_usd: 0
observed_spend_basis: OWNER_CONFIRMED_PUBLIC_FREE_API_OFFER_NO_BILLING_SURFACE_NO_PAYMENT_PURCHASE_OR_PAID_FALLBACK
additional_real_request_authorized: false
validation_key_revocation_pending_after_connected_review: true
provider_live_state: LIVE_VALIDATION_READY
connected_validation_status: SMOKE_PASS_OWNER_ZERO_COST_CONFIRMED_PENDING_CONNECTED_QA
quality_evaluation_status: SMOKE_PASS_OWNER_ZERO_COST_CONFIRMED_PENDING_CONNECTED_QA
next_gate: CONNECTED_QA
<!-- STUDIO-009V-04-SMOKE-OWNER-ZERO-COST-CHECKPOINT-0007 -->
