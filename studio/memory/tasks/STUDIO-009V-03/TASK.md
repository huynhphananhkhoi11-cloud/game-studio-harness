# STUDIO-009V-03 TASK

memory_schema_version: 1

task_id: STUDIO-009V-03
task_title: NVIDIA NIM / DeepSeek V4 Pro 0813 bounded connected validation
task_type: provider-specific connected-validation contract and later implementation
canonical_task_contract: tasks/STUDIO-009V-03.md
implementation_contract: tasks/STUDIO-009V-03-IMPLEMENTATION.md
parent_task: STUDIO-009
provider_parent: STUDIO-009P-03
live_governance_parent: STUDIO-009R-01
logical_role: Platform Studio / Connected Validation Cell

provider: NVIDIA-hosted NIM API Catalog
provider_profile_id: provider-profile:nvidia-nim-free-deepseek-v4-pro-0813
provider_child_id: STUDIO-009P-03
model_allowlist: deepseek-ai/deepseek-v4-pro-0813
credential_profile_ref: credential-profile:nvidia-nim-api-key
account_ref: account-ref:nvidia-developer-program-owner-account
cost_class: ZERO_COST_ONLY
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
money_ceiling: 0

task_status: OFFLINE_LIVE_IMPLEMENTATION_REVIEW_APPROVED_PENDING_OWNER_MERGE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
base_head: eae0b9462bca1c7e3819402219c6225a3f56fb0f
p03_implementation_merge: ac04040f40f544d70db10dba975481b7da5930ea
p03_closeout_merge: eae0b9462bca1c7e3819402219c6225a3f56fb0f
contract_branch: agent/studio-009v-03-nvidia-nim-contract
implementation_branch: agent/studio-009v-03-nvidia-nim-live-validation

provider_input_token_upper_ceiling: 32768
provider_output_token_upper_ceiling: 16384
first_campaign_input_token_ceiling: 4096
first_campaign_completion_token_ceiling: 512
real_request_ceiling: 3
concurrency_ceiling: 1
automatic_retry_ceiling: 0
request_timeout_seconds_ceiling: 60
request_bytes_ceiling: 32768
response_bytes_ceiling: 131072
allowed_data_classifications: PUBLIC,SYNTHETIC
promotion_ceiling: LIVE_VALIDATED
routing_authority: NONE
worker_authority: NONE
tool_authority: NONE
production_authority: NONE
money_ceiling_currency: USD

provider_runtime_activity: NONE
network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
tool_execution_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

full_studio_acceptance_authority: STUDIO-009F
automatic_routing_authority: STUDIO-009E
next_gate: RULES_CI_THEN_OWNER_MERGE_V03_IMPLEMENTATION
<!-- STUDIO-009V-03-CONTRACT-CHECKPOINT-0001 -->

offline_live_implementation_base: 5a4290419003605ff8ca4b2a85dbe3653f3d22d5
offline_live_implementation_scope_paths: 12
offline_live_implementation_memory_paths: 4
offline_live_implementation_cumulative_paths: 16
offline_live_state: LIVE_VALIDATION_READY
connected_validation_status: PENDING_REAL_SMOKE
quality_evaluation_status: PENDING_REAL_SMOKE
connected_execution_authorized: false
offline_live_provider_runtime_activity: NONE
offline_live_network_activity: NONE
offline_live_credential_runtime_activity: NONE
offline_live_tool_activity: NONE
offline_live_routing_activity: NONE
offline_live_spend: ZERO
<!-- STUDIO-009V-03-OFFLINE-LIVE-IMPLEMENTATION-CHECKPOINT-0002 -->

pre_qa_reviewed_head: 38b7768ab07fb9f3248dcf04d2345f96442af810
pre_qa_repair_result: PASS
new_v03_tests: 114
nvidia_implementation_tests: 154
pre_qa_repair_probes: 138
pre_qa_live_framework_tests: 70
pre_qa_focused_tests: 662
pre_qa_total_tests: 1167
pre_qa_connected_execution_authorized: false
pre_qa_network_activity: NONE
pre_qa_credential_activity: NONE
pre_qa_tool_activity: NONE
pre_qa_routing_activity: NONE
pre_qa_spend: ZERO
<!-- STUDIO-009V-03-PRE-QA-REPAIR-CHECKPOINT-0003 -->

offline_qa_ref: qa:offline-nvidia-v03-f8a94f04fa22
offline_qa_reviewed_head: f8a94f04fa22d78ef1f45868925cbec11730de35
offline_qa_result: PASS
offline_qa_blockers: 0
offline_qa_independent_probes: 88
offline_qa_nvidia_tests: 154
offline_qa_live_framework_tests: 70
offline_qa_focused_tests: 662
offline_qa_total_tests: 1167
offline_qa_provider_calls: 0
offline_qa_nvidia_network_activity: NONE
offline_qa_api_key_activity: NONE
offline_qa_tool_activity: NONE
offline_qa_routing_activity: NONE
offline_qa_billable_spend_usd: 0
<!-- STUDIO-009V-03-INDEPENDENT-OFFLINE-QA-CHECKPOINT-0004 -->

offline_review_ref: review:offline-nvidia-v03-64998491486f
offline_review_reviewed_qa_head: 64998491486fabbf72dbea24ed89340ccba0ccb8
offline_review_result: APPROVE
offline_review_blockers: 0
offline_review_independent_probes: 130
offline_review_qa_lineage_probes: 38
offline_review_hygiene_probes: 32
offline_review_nvidia_tests: 154
offline_review_live_framework_tests: 70
offline_review_focused_tests: 662
offline_review_total_tests: 1167
offline_review_provider_calls: 0
offline_review_nvidia_network_activity: NONE
offline_review_api_key_activity: NONE
offline_review_tool_activity: NONE
offline_review_routing_activity: NONE
offline_review_billable_spend_usd: 0
<!-- STUDIO-009V-03-INDEPENDENT-OFFLINE-REVIEW-CHECKPOINT-0005 -->
