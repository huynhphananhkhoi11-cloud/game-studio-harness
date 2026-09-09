# STUDIO-009V-04 WORKLOG

memory_schema_version: 1

task_id: STUDIO-009V-04

## Contract research and materialization

- Base authority: `3726e2bd031ce2022f5a93ff1d40c404fb815682` after durable P-04 closeout merge.
- P-04 is COMPLETE; implementation merge `e7ed2d087117eacad42141ca2d0c6587d16721dc`; final Review head `7d37dd64db07b63037ad4d3fb434757f3974a589`.
- V-03 NVIDIA remains frozen on account verification and is not resumed by V-04.
- Exact Poolside model: `poolside/laguna-s-2.1`.
- Exact standalone direct base: `https://inference.poolside.ai/v1`.
- Exact chat path: `/v1/chat/completions`.
- Current public offer remains `Free to use for a limited time`; no permanent free quota is inferred.
- Poolside Terms last updated July 21, 2026: Content can include prompts/code/output/feedback and may be used for model training unless opted out; feedback/safety exceptions remain.
- Terms permit fees for some Products/features and prohibit fee/usage-limit circumvention.
- Poolside CLI standalone setup can create/copy an API key and can store local credentials; initial V-04 keeps `pool` disabled.
- Public CLI docs show local `pool logout`; this is not server-side revocation proof.
- V-04 requires Owner-visible account-level zero-cost eligibility and server-side key revoke/delete/invalidate proof before first real request.
- Future first campaign ceiling: max 3 requests, serial, no retry, <=4096 input estimate, <=1024 completion, <=32768 request bytes, <=131072 response bytes.
- PUBLIC/SYNTHETIC only; tools/MCP/ACP/shell/file/browser/repository write/routing remain disabled.
- Contract activity: no Poolside account/key/provider/model/network/CLI/tool/MCP/ACP/routing activity; spend USD 0.
- Future implementation scope: 18 implementation paths + four V-04 memory paths = maximum 22.
- Contract merge authorizes offline implementation only.

provider_calls: 0
poolside_network_activity: NONE
poolside_api_key_input_activity: NONE
pool_cli_activity: NONE
tool_activity: NONE
mcp_activity: NONE
acp_activity: NONE
routing_activity: NONE
billable_spend_usd: 0
<!-- STUDIO-009V-04-CONTRACT-CHECKPOINT-0001 -->


## Offline live-transport implementation

- V-04 contract merge: `a7beb556d19da1397cceb09431d47848e69c5b12`.
- Implementation scope: 12 provider/live/code/test paths; memory scope: 4; cumulative: 16.
- Reused the already-tested V-03 live architecture as a read-only implementation template, then bound it to exact Poolside V-04 provider/model/host/credential/account lineage.
- Direct transport targets only `https://inference.poolside.ai/v1/chat/completions`.
- Provider remains not connected; live state is only `LIVE_VALIDATION_READY`.
- Connected/quality evidence remains `PENDING_REAL_SMOKE`.
- Session bridge remains hidden Owner-interactive/in-memory only with no env/file/CLI/keychain/browser/clipboard secret lookup.
- `pool` CLI remains disabled.
- First campaign remains max 3 requests, concurrency 1, retry 0, <=4096 input estimate, <=1024 completion, USD 0.
- Server-side key revocation proof and current zero-cost eligibility remain later Owner connected-preflight requirements.
- New V-04 tests: 119; focused: 881; total: 1386; static probes: 126.
- No Poolside account/API-key/provider/model/network/CLI/tool/MCP/ACP/routing activity occurred.
- Spend: USD 0.
- Next gate: independent offline QA.

provider_calls: 0
poolside_network_activity: NONE
poolside_api_key_input_activity: NONE
pool_cli_activity: NONE
tool_activity: NONE
mcp_activity: NONE
acp_activity: NONE
routing_activity: NONE
billable_spend_usd: 0
connected_execution_authorized: false
<!-- STUDIO-009V-04-OFFLINE-LIVE-IMPLEMENTATION-CHECKPOINT-0002 -->
