# STUDIO-009P-02 STATE

memory_schema_version: 1

task_id: STUDIO-009P-02
state: CONTRACT_ACCEPTED
logical_role: Platform Studio / Provider Integration Cell
repository_context: game-studio-harness
branch: agent/studio-009p-02-cloudflare-contract
last_observed_HEAD: 1b75f250169ccdab3e2d67cbac4047253792c4a7
durability_state: PR_PENDING
provider: Cloudflare Workers AI
provider_profile_id: provider-profile:cloudflare-workers-ai-free-nemotron-3-super
model_allowlist: @cf/nvidia/nemotron-3-120b-a12b
credential_profile_ref: credential-profile:cloudflare-workers-ai-api-token
account_ref: account-ref:cloudflare-workers-ai-owner-account
money_ceiling: 0
workers_free_required: true
daily_provider_free_snapshot_neurons: 10000
daily_game_ceiling_neurons: 8000
real_provider_approved_for_connection: false
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

completed: |
  - STUDIO-009P-01 Groq child is COMPLETE through merged closeout PR #52.
  - Owner selected Cloudflare Workers AI as the second provider child.
  - Exact model candidate is @cf/nvidia/nemotron-3-120b-a12b.
  - Current official Free-plan, model, data, endpoint, authentication, quota, and error evidence was captured in the child contract.

remaining: |
  - Merge the STUDIO-009P-02 contract PR.
  - Only after merge, create the bounded offline/synthetic implementation runner.
  - QA, Final Review and Integration, Owner implementation merge, and closeout remain required.

blockers: |
  - NONE

exact_next_action: Studio Owner reviews and may merge the STUDIO-009P-02 contract PR. Do not create a Cloudflare token/account connection or run implementation before contract merge.

contract_record_semantics: EFFECTIVE_WHEN_MERGED
next_phase: STUDIO-009P-02_IMPLEMENTATION_ONLY_AFTER_CONTRACT_MERGE
<!-- STUDIO-009P-02-CONTRACT-CHECKPOINT-0001 -->
