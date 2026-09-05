# STUDIO-009V-01 STATE

memory_schema_version: 1

task_id: STUDIO-009V-01
state: CONTRACT_READY_FOR_OWNER_MERGE
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-01-groq-contract
base_head: 11c2c2d4a35f37c5712376a3e7b16ca22d848bc7
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
  - Studio Owner reviews and may merge the contract Pull Request.
  - No real credential or Groq request before contract merge.
  - After durable contract merge, implement offline transport/tests first, then run at most three bounded PUBLIC/SYNTHETIC requests.

blockers: |
  - NONE

provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
tool_execution_activity: NONE
remote_mcp_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

exact_next_action: Studio Owner reviews and may merge the STUDIO-009V-01 contract Pull Request. Do not enter a Groq API key or call Groq before the contract is durable.
next_phase: STUDIO-009V-01_OWNER_MERGE_CONTRACT
