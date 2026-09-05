# STUDIO-009V-01 RESUME

memory_schema_version: 1

task_id: STUDIO-009V-01
package_path: studio/memory/tasks/STUDIO-009V-01
canonical_task_contract: tasks/STUDIO-009V-01.md
current_state: CONTRACT_READY_FOR_OWNER_MERGE
resume_from: 11c2c2d4a35f37c5712376a3e7b16ca22d848bc7
branch: agent/studio-009v-01-groq-contract

safe_checkpoint: STUDIO-009R-01 is durably closed; Groq P-01 is offline COMPLETE and remains connected DISABLED.

next_action: Studio Owner reviews and may merge the V-01 contract Pull Request. Only after durable merge may the V-01 implementation prepare a trusted transport and bounded connected smoke.

prohibited_next_actions: real Groq API key entry; credential resolution; Groq/network/model call; tools/browser/code execution/MCP/search/storage; automatic retry; routing; worker promotion; repository write authority; nonzero spend; Unity/game work.

fallback: accepted MANUAL/FAKE no-network path.

money_ceiling: 0
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
connected_execution_activity: NONE
spend: ZERO

next_gate: OWNER_MERGE_CONTRACT
