# STUDIO-009V-03 STATE

memory_schema_version: 1

task_id: STUDIO-009V-03
state: CONTRACT_READY_FOR_OWNER_MERGE
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-03-nvidia-nim-contract
base_head: eae0b9462bca1c7e3819402219c6225a3f56fb0f
durability_state: PR_PENDING

provider: NVIDIA-hosted NIM API Catalog
provider_profile_id: provider-profile:nvidia-nim-free-deepseek-v4-pro-0813
provider_child_id: STUDIO-009P-03
model: deepseek-ai/deepseek-v4-pro-0813
host: integrate.api.nvidia.com
base_path: /v1
endpoint: /v1/chat/completions
credential_profile_ref: credential-profile:nvidia-nim-api-key
account_ref: account-ref:nvidia-developer-program-owner-account
money_ceiling: 0
live_state_ceiling: LIVE_VALIDATED
allowed_data: PUBLIC_SYNTHETIC_ONLY

completed: |
  - Verified P-03 implementation PR #68 durable merge at ac04040f40f544d70db10dba975481b7da5930ea.
  - Verified P-03 closeout PR #69 durable merge at eae0b9462bca1c7e3819402219c6225a3f56fb0f.
  - Verified P-03 completion remains provider DISABLED / model DECLARED / evidence SYNTHETIC with connected authority NONE and spend ZERO.
  - Verified STUDIO-009R-01 preserves provider-specific V-track authority separation.
  - Re-verified official NVIDIA NIM Developer access, exact model Free Endpoint, exact NVIDIA-hosted OpenAI-compatible base, context/max-token evidence and Trial Terms.
  - Defined bounded V-03 contract and future 22-path implementation scope.

remaining: |
  - Studio Owner reviews and may merge the V-03 contract PR.
  - No NVIDIA API key is created/requested/input before durable contract merge and later offline implementation/preflight.
  - After contract merge, prepare offline live transport/smoke/credential-bridge code and hostile tests.
  - Only then may separate Owner connected preflight authorize a bounded real smoke.

blockers: |
  - NONE

provider_runtime_activity: NONE
network_activity: NONE
account_runtime_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
tool_execution_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO

exact_next_action: Studio Owner reviews and may merge the STUDIO-009V-03 contract Pull Request. Do not create/input an NVIDIA API key and do not call NVIDIA before the contract is durable and the later offline live implementation passes its gates.
next_phase: STUDIO-009V-03_OWNER_MERGE_CONTRACT
<!-- STUDIO-009V-03-CONTRACT-CHECKPOINT-0001 -->
