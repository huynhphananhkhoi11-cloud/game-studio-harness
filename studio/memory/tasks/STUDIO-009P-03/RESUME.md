# STUDIO-009P-03 RESUME

memory_schema_version: 1

task_id: STUDIO-009P-03
package_path: studio/memory/tasks/STUDIO-009P-03
canonical_task_contract: tasks/STUDIO-009P-03.md
implementation_contract: tasks/STUDIO-009P-03-IMPLEMENTATION.md
current_state: IMPLEMENTATION_READY_FOR_QA
resume_from: 11830798fc41c43d517c007fc4adec653d0aaaaf
branch: agent/studio-009p-03-nvidia-nim-implementation
safe_checkpoint: P-03 contract PR #67 is durably merged. Offline/synthetic implementation is materialized with no connected authority.
next_action: Independent QA reviews exact 24-path implementation scope and test evidence. After QA PASS, independent Review/Integration approval is required before Owner merge.
prohibited_next_actions: NVIDIA_API_KEY creation/input/resolution for GAME; NVIDIA/DeepSeek/NIM network/model call; account probing; paid subscription; paid deployment; tool execution; routing; worker promotion; private/unreleased game-data export; nonzero spend; P-04/P-05 authoritative write track.
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
next_gate: P03_IMPLEMENTATION_QA
contract_checkpoint: STUDIO-009P-03-CONTRACT-CHECKPOINT-0001
implementation_checkpoint: STUDIO-009P-03-IMPLEMENTATION-CHECKPOINT-0002
contract_record_semantics: EFFECTIVE_WHEN_MERGED
