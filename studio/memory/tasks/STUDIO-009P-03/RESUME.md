# STUDIO-009P-03 RESUME

memory_schema_version: 1

task_id: STUDIO-009P-03
package_path: studio/memory/tasks/STUDIO-009P-03
canonical_task_contract: tasks/STUDIO-009P-03.md
implementation_contract: tasks/STUDIO-009P-03-IMPLEMENTATION.md
current_state: CONTRACT_ACCEPTED_PENDING_OWNER_MERGE
resume_from: cbcdd527fc549ccf474667661244e452bdcfc5a5
branch: agent/studio-009p-03-nvidia-nim-contract
safe_checkpoint: STUDIO-009V-02 is durably COMPLETE. Groq V-01 and Cloudflare V-02 remain independently LIVE_VALIDATED without automatic routing authority.
next_action: Owner reviews and may merge the P-03 NVIDIA NIM contract PR. After durable merge, create only bounded offline/synthetic implementation.
prohibited_next_actions: NVIDIA_API_KEY creation/input/resolution for GAME; NVIDIA/DeepSeek/NIM network/model call; account probing; paid subscription; partner endpoint; paid deployment; tool execution; routing; worker promotion; private/unreleased game-data export; nonzero spend; P-04/P-05 authoritative write track.
fallback: STUDIO-007F/STUDIO-008 MANUAL/FAKE.
provider: NVIDIA-hosted NIM API Catalog
model_allowlist: deepseek-ai/deepseek-v4-pro-0813
cost_class: ZERO_COST_ONLY
usage_class: INTERNAL_TESTING_EVALUATION_ONLY
money_ceiling: 0
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
tool_execution_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO
next_gate: OWNER_MERGE_P03_CONTRACT_PR
contract_checkpoint: STUDIO-009P-03-CONTRACT-CHECKPOINT-0001
contract_record_semantics: EFFECTIVE_WHEN_MERGED