# STUDIO-009P-02 TASK

memory_schema_version: 1

task_id: STUDIO-009P-02
canonical_task_contract: tasks/STUDIO-009P-02.md
implementation_contract: tasks/STUDIO-009P-02-IMPLEMENTATION.md
parent_task: STUDIO-009D
logical_role: Platform Studio / Provider Integration Cell
provider: Cloudflare Workers AI
model_allowlist: @cf/nvidia/nemotron-3-120b-a12b
cost_class: ZERO_COST_ONLY
money_ceiling: 0
state: COMPLETE
branch: agent/studio-009p-02-cloudflare-closeout
base_head: 5e6950d0b17a173a70fcf325061dd7147696c05e
contract_merge: a22f358b471a6f3af2ec19cae2af1da5e2aaacaa
provider_runtime_activity: NONE
network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

objective: Define the Cloudflare Workers AI / Nemotron 3 Super provider child contract without activating any real connection.
completion_boundary: Contract PR only. Implementation is forbidden until this contract merges; STUDIO-009F still gates account/token resolution, HTTPS transport, model/tool calls, quota consumption, connected execution, and spend.

baseline_focused_tests: 362
baseline_total_tests: 759
provider_profile_reserved: provider-profile:cloudflare-workers-ai-free-nemotron-3-super
credential_profile_reserved: credential-profile:cloudflare-workers-ai-api-token
account_ref_reserved: account-ref:cloudflare-workers-ai-owner-account
free_plan_required: true
daily_provider_free_snapshot_neurons: 10000
daily_game_ceiling_neurons: 8000
real_provider_approved_for_connection: false

contract_record_semantics: EFFECTIVE_WHEN_MERGED

implementation_scope_paths: 20
implementation_cumulative_pr_paths_max: 24
implementation_expected_new_tests: 45
implementation_expected_focused_tests: 407
implementation_expected_total_tests: 804
implementation_provider_state: DISABLED
implementation_model_state: DECLARED
implementation_runtime_activity: NONE
implementation_spend: ZERO

qa_result: PASS
qa_reviewed_head: 18b79dd67af466ffd74ccd34828a292e35342741
qa_blockers: 0
qa_provider_runtime_activity: NONE
qa_network_activity: NONE
qa_account_runtime_activity: NONE
qa_credential_runtime_activity: NONE
qa_secret_store_activity: NONE
qa_ai_gateway_activity: NONE
qa_unified_billing_activity: NONE
qa_prepaid_credit_activity: NONE
qa_tool_execution_activity: NONE
qa_remote_mcp_activity: NONE
qa_routing_activity: NONE
qa_connected_execution_activity: NONE
qa_spend: ZERO
<!-- STUDIO-009P-02-QA-CHECKPOINT-0003 -->

review_result: APPROVE
reviewed_qa_head: 3076383d226a93016f086b0feb23d3c04f69f918
review_blockers: 0
review_new_cloudflare_tests: 45
review_focused_tests: 407
review_total_tests: 804
review_probes: 74
review_provider_runtime_activity: NONE
review_network_activity: NONE
review_account_runtime_activity: NONE
review_credential_runtime_activity: NONE
review_secret_store_activity: NONE
review_ai_gateway_activity: NONE
review_unified_billing_activity: NONE
review_prepaid_credit_activity: NONE
review_tool_execution_activity: NONE
review_remote_mcp_activity: NONE
review_routing_activity: NONE
review_connected_execution_activity: NONE
review_spend: ZERO
<!-- STUDIO-009P-02-REVIEW-CHECKPOINT-0004 -->

implementation_pr: 54
implementation_merge: 5e6950d0b17a173a70fcf325061dd7147696c05e
final_review_head: 8173cd76488b2a402b76d33f7e7f2a03bcc38f13
completion_result: COMPLETE
completion_new_tests: 45
completion_focused_tests: 407
completion_total_tests: 804
completion_provider_profile_state: DISABLED
completion_model_profile_state: DECLARED
completion_child_evidence_class: SYNTHETIC
completion_provider_runtime_activity: NONE
completion_network_activity: NONE
completion_account_runtime_activity: NONE
completion_credential_runtime_activity: NONE
completion_secret_store_activity: NONE
completion_ai_gateway_activity: NONE
completion_unified_billing_activity: NONE
completion_prepaid_credit_activity: NONE
completion_tool_execution_activity: NONE
completion_remote_mcp_activity: NONE
completion_routing_activity: NONE
completion_connected_execution_activity: NONE
completion_spend: ZERO
completion_real_provider_approved_for_connection: false
closeout_record_semantics: EFFECTIVE_WHEN_MERGED
next_phase: STUDIO-009E
<!-- STUDIO-009P-02-CLOSEOUT-CHECKPOINT-0005 -->
