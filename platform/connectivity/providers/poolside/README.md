# Poolside direct provider profile — STUDIO-009P-04

This directory is the deterministic OFFLINE/SYNTHETIC implementation of the merged P-04 contract.

Provider: Poolside standalone hosted inference API
Exact model: `poolside/laguna-s-2.1`
Direct candidate base URL: `https://inference.poolside.ai/v1`
Chat path: `/v1/chat/completions`

Runtime state is deliberately `DISABLED`; model state is `DECLARED`; child evidence is `SYNTHETIC`.

This implementation performs no Poolside account/API-key lookup, no network request, no `pool` CLI execution, no tool/MCP/ACP/shell/file/browser/repository-write action, no routing/failover, and no spend.

Initial connected data authority remains PUBLIC/SYNTHETIC only. Current public free availability is dynamic (`Free to use for a limited time`) and must be re-proven at a separately merged V-04 connected preflight. Training opt-out does not broaden GAME data authority.

Rollback remains MANUAL/FAKE. V-03 NVIDIA remains independently frozen.
<!-- STUDIO-009P-04-IMPLEMENTATION-CHECKPOINT-0002 -->
