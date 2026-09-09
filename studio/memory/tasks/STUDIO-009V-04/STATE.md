# STUDIO-009V-04 STATE

memory_schema_version: 1

task_id: STUDIO-009V-04
state: CONTRACT_PENDING_OWNER_MERGE
logical_role: Platform Studio / Connected Validation Cell
repository_context: game-studio-harness
branch: agent/studio-009v-04-poolside-laguna-s-contract
last_observed_HEAD: 3726e2bd031ce2022f5a93ff1d40c404fb815682
durability_state: CONTRACT_PR_PENDING

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
  - P-04 offline provider child is durably COMPLETE.
  - P-04 implementation PR #74 merged at e7ed2d087117eacad42141ca2d0c6587d16721dc.
  - P-04 closeout PR #75 merged at 3726e2bd031ce2022f5a93ff1d40c404fb815682.
  - P-04 QA PASS and Review APPROVE are durable.
  - Poolside official model/Terms/CLI evidence re-verified for V-04 contract on 2026-09-09.
  - V-03 NVIDIA remains frozen at account verification.

remaining: |
  - Owner reviews and merges V-04 contract.
  - Only after contract merge: bounded offline live-transport implementation.
  - Independent offline QA and Review/Integration.
  - Owner connected preflight proves current zero-cost eligibility and server-side key revocation path.
  - Only then may bounded real smoke be considered.

blockers: |
  - NONE at contract stage.

exact_next_action: Verify V-04 contract PR and Rules CI. Owner may merge contract only if immutable head is clean; contract merge authorizes offline V-04 implementation only, not Poolside account/key/network activity.
next_phase: STUDIO-009V-04_CONTRACT_OWNER_MERGE_GATE
<!-- STUDIO-009V-04-CONTRACT-CHECKPOINT-0001 -->
