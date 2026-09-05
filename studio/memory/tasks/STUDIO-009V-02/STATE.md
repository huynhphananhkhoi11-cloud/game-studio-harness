# STUDIO-009V-02 STATE

memory_schema_version: 1

task_id: STUDIO-009V-02
state: CONTRACT_READY_FOR_OWNER_MERGE
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-02-cloudflare-contract
base_head: 6bdb1daa9b2dee65a3262da8caf8c3ce42a4ac46
durability_state: PR_PENDING

provider: Cloudflare Workers AI
provider_profile_id: provider-profile:cloudflare-workers-ai-free-nemotron-3-super
provider_child_id: STUDIO-009P-02
model: @cf/nvidia/nemotron-3-120b-a12b
host: api.cloudflare.com
base_path_template: /client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1
endpoint: /chat/completions
credential_profile_ref: credential-profile:cloudflare-workers-ai-api-token
account_ref: account-ref:cloudflare-workers-ai-owner-account
money_ceiling: 0
live_state_ceiling: LIVE_VALIDATED

completed: |
  - Verified STUDIO-009V-01 Groq durable closeout.
  - Verified STUDIO-009P-02 Cloudflare offline lifecycle is COMPLETE.
  - Verified STUDIO-009R-01 permits a provider-specific STUDIO-009V-02 track.
  - Re-verified current Cloudflare official pricing, model, OpenAI-compatible endpoint, data-use and API-token guidance.
  - Confirmed the existing P-02 provider files retain historical STUDIO-009F_ONLY values that require explicit V-02 reconciliation later.
  - Defined bounded V-02 contract and future implementation scope.

remaining: |
  - Studio Owner reviews and may merge the V-02 contract PR.
  - No Account ID or API token is requested before durable contract merge.
  - After durable contract merge, prepare offline live transport/smoke implementation and deterministic hostile tests.
  - Only then may a separate Owner connected preflight authorize a bounded real smoke.

blockers: |
  - NONE

provider_runtime_activity: NONE
network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
ai_gateway_activity: NONE
unified_billing_activity: NONE
prepaid_credit_activity: NONE
tool_execution_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

exact_next_action: Studio Owner reviews and may merge the STUDIO-009V-02 contract Pull Request. Do not enter a Cloudflare Account ID or API token and do not call Cloudflare before the contract is durable.
next_phase: STUDIO-009V-02_OWNER_MERGE_CONTRACT
<!-- STUDIO-009V-02-CONTRACT-CHECKPOINT-0001 -->
