# STUDIO-009V-01 WORKLOG

memory_schema_version: 1

task_id: STUDIO-009V-01
package_path: studio/memory/tasks/STUDIO-009V-01
canonical_task_contract: tasks/STUDIO-009V-01.md

## 2026-09-05 — Contract preparation

- Durable STUDIO-009P-01 offline closeout merge verified at `1b75f250169ccdab3e2d67cbac4047253792c4a7`.
- Durable STUDIO-009R-01 closeout merge verified at `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`.
- Current Groq official evidence re-verified for `openai/gpt-oss-120b`, `api.groq.com/openai/v1`, Free Plan limits, ZDR, billing-tier behavior, and supported tool capabilities.
- Contract keeps `MONEY_CEILING=0`.
- First smoke is bounded to max 3 requests, concurrency 1, retry 0, PUBLIC/SYNTHETIC only, no tools/browser/code/MCP/search/storage/external write.
- V-01 promotion ceiling is `LIVE_VALIDATED`; no worker or routing authority is granted.
- Contract preparation performs no Groq/provider/model/credential runtime activity and no spend.
