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
state: CONTRACT_ACCEPTED
branch: agent/studio-009p-02-cloudflare-contract
base_head: 1b75f250169ccdab3e2d67cbac4047253792c4a7
contract_merge: NONE
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
