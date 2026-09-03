# STUDIO-009P-02 RESUME

memory_schema_version: 1

task_id: STUDIO-009P-02
resume_from: 1b75f250169ccdab3e2d67cbac4047253792c4a7
branch: agent/studio-009p-02-cloudflare-contract
provider: Cloudflare Workers AI
model_allowlist: @cf/nvidia/nemotron-3-120b-a12b
status: CONTRACT_ACCEPTED

safe_checkpoint: STUDIO-009P-01 is COMPLETE on main at 1b75f250169ccdab3e2d67cbac4047253792c4a7; STUDIO-009P-02 is contract-only until its PR merges.
next_action: Studio Owner reviews and may merge the STUDIO-009P-02 contract PR. After merge, create only the bounded offline/synthetic implementation.
prohibited_next_actions: Cloudflare account discovery; raw account ID capture; API token creation/enrollment/resolution; Workers AI HTTP call; real model call; AI Gateway; Unified Billing; prepaid credits; storage services; paid Workers activation; tool execution; routing; connected execution; nonzero spend.
fallback: STUDIO-007F/STUDIO-008 MANUAL/FAKE; STUDIO-009P-01 Groq remains independently accepted but is not automatically activated.

contract_checkpoint: STUDIO-009P-02-CONTRACT-CHECKPOINT-0001
contract_record_semantics: EFFECTIVE_WHEN_MERGED
