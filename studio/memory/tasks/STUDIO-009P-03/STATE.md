# STUDIO-009P-03 STATE

memory_schema_version: 1

task_id: STUDIO-009P-03
state: CONTRACT_ACCEPTED
logical_role: Platform Studio / Provider Integration Cell
repository_context: game-studio-harness
branch: agent/studio-009p-03-nvidia-nim-contract
last_observed_HEAD: cbcdd527fc549ccf474667661244e452bdcfc5a5
durability_state: PR_PENDING
provider: NVIDIA-hosted NIM API Catalog
provider_profile_id: provider-profile:nvidia-nim-free-deepseek-v4-pro-0813
model_allowlist: deepseek-ai/deepseek-v4-pro-0813
credential_profile_ref: credential-profile:nvidia-nim-api-key
account_ref: account-ref:nvidia-developer-program-owner-account
money_ceiling: 0
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
trial_only: true
allowed_data: PUBLIC_SYNTHETIC_ONLY
connected_authority: NONE
worker_authority: NONE
routing_authority: NONE
tool_authority: NONE
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
  - STUDIO-009V-02 Cloudflare closeout is durable on the locked base.
  - Owner selected NVIDIA-hosted NIM as P-03 provider track.
  - Exact model candidate: deepseek-ai/deepseek-v4-pro-0813.
  - Official model/API/trial/data evidence captured in P-03 contract.
remaining: |
  - Owner reviews and may merge P-03 contract PR.
  - After merge only: bounded offline/synthetic implementation.
  - QA, Review, Owner implementation merge and closeout remain required.
  - After durable P-03 offline completion: V-03 contract.
  - Poolside P/V-04 and OpenCode P/V-05 remain planning-only.
blockers: |
  - NONE
exact_next_action: Owner reviews and may merge P-03 contract PR. Do not create/use an NVIDIA API key for GAME and do not call NVIDIA/DeepSeek under P-03.
next_phase: STUDIO-009P-03_IMPLEMENTATION_ONLY_AFTER_CONTRACT_MERGE
contract_record_semantics: EFFECTIVE_WHEN_MERGED
<!-- STUDIO-009P-03-CONTRACT-CHECKPOINT-0001 -->