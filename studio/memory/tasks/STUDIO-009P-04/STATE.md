# STUDIO-009P-04 STATE

memory_schema_version: 1

task_id: STUDIO-009P-04
state: CONTRACT_ACCEPTED
logical_role: Platform Studio / Provider Integration Cell
repository_context: game-studio-harness
branch: agent/studio-009p-04-poolside-laguna-s-contract
last_observed_HEAD: 324fb3622f9037b5be8b4b4efead26ee43b50849
durability_state: PR_PENDING
provider: Poolside standalone hosted inference API
provider_profile_id: provider-profile:poolside-direct-laguna-s-2.1
model_allowlist: poolside/laguna-s-2.1
credential_profile_ref: credential-profile:poolside-api-key
account_ref: account-ref:poolside-owner-account
money_ceiling: 0
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
free_evidence: FREE_FOR_LIMITED_TIME_DYNAMIC
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
  - V-03 NVIDIA connected preflight is durably frozen on account verification.
  - Durable freeze checkpoint explicitly permits STUDIO-009P-04_CONTRACT as next provider write track.
  - Exact Poolside model candidate is poolside/laguna-s-2.1.
  - Official model/API/terms/CLI evidence captured in P-04 contract.
  - Direct Poolside standalone endpoint is separated from third-party gateways and Poolside enterprise deployments.
remaining: |
  - Owner reviews and may merge P-04 contract PR.
  - After merge only: bounded offline/synthetic P-04 implementation.
  - QA, Review, Owner implementation merge and closeout remain required.
  - After durable P-04 offline completion: separate V-04 contract.
  - P-05 OpenCode remains planning/read-only only.
blockers: |
  - NONE
exact_next_action: Owner reviews and may merge P-04 contract PR. Do not create/use a Poolside API key for GAME, install/use pool CLI, or call Poolside/Laguna under P-04.
next_phase: STUDIO-009P-04_IMPLEMENTATION_ONLY_AFTER_CONTRACT_MERGE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
<!-- STUDIO-009P-04-CONTRACT-CHECKPOINT-0001 -->
