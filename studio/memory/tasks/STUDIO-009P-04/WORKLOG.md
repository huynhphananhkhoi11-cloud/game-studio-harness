# STUDIO-009P-04 WORKLOG

memory_schema_version: 1

task_id: STUDIO-009P-04

## Contract research and materialization

- Base authority: `324fb3622f9037b5be8b4b4efead26ee43b50849` after durable V-03 freeze merge.
- V-03 remains `CONNECTED_PREFLIGHT_FROZEN_ACCOUNT_VERIFICATION`; P-04 does not resume or modify NVIDIA connected validation.
- Selected provider path: Poolside standalone hosted inference API, direct provider endpoint only.
- Exact model: `poolside/laguna-s-2.1`.
- Current public model evidence: 118B total / 8B active / up to 1M model context, agentic coding focus, thinking/no-thinking modes.
- Current standalone API example: `https://inference.poolside.ai/v1`, OpenAI-compatible chat API.
- Current availability evidence: `Free to use for a limited time`; no permanent free quota is inferred.
- Terms evidence: Content may be used for product/model improvement and training unless opt-out; initial GAME data remains PUBLIC/SYNTHETIC regardless of opt-out.
- CLI evidence: `pool` can persist credentials and expose repository/tool/MCP/secret surfaces, so CLI/harness use is excluded from P-04 and initial V-04.
- Third-party gateways, enterprise deployment endpoints, local/self-hosted inference and paid routes are out of scope.
- Contract activity: no Poolside account/key/provider/model/tool/CLI/MCP/ACP/routing activity; spend zero.
- Exact future offline implementation scope: 20 implementation paths + four P-04 memory paths, maximum 24.
- Next gate: Owner contract review and merge.

<!-- STUDIO-009P-04-CONTRACT-CHECKPOINT-0001 -->
