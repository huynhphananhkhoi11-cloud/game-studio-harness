# STUDIO-009P-01 TASK

memory_schema_version: 1

task_id: STUDIO-009P-01
canonical_task_contract: tasks/STUDIO-009P-01.md
parent_task: STUDIO-009D
logical_role: Platform Studio / Provider Integration Cell
provider: GroqCloud
model_allowlist: openai/gpt-oss-120b
cost_class: ZERO_COST_ONLY
money_ceiling: 0
state: CONTRACT
branch: agent/studio-009p-01-groq-contract
base_head: fb538c930e90ba8f7174d8a52c6e358978b5353b
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
connected_execution_activity: NONE
spend: ZERO

objective: Create the first real-provider child contract for Groq without activating a provider.
completion_boundary: Contract PR only; implementation/network/credential/model-call authority remains absent.

updated_at: 2026-09-03T10:11:16Z
updater: Studio Owner contract runner