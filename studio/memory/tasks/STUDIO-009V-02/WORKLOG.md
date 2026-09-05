# STUDIO-009V-02 WORKLOG

memory_schema_version: 1

task_id: STUDIO-009V-02
package_path: studio/memory/tasks/STUDIO-009V-02
canonical_task_contract: tasks/STUDIO-009V-02.md

## 2026-09-05 — Contract preparation

- Durable V-01 Groq closeout verified at `6bdb1daa9b2dee65a3262da8caf8c3ce42a4ac46`.
- Durable P-02 Cloudflare offline closeout PR #55 verified at `3cf7165c3263f8595b66a0d029b96022840adef3`.
- Durable R-01 progressive-live closeout verified at `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`.
- Exact Cloudflare provider profile remains `provider-profile:cloudflare-workers-ai-free-nemotron-3-super`.
- Exact model remains `@cf/nvidia/nemotron-3-120b-a12b`.
- Official Cloudflare evidence re-verified for 10,000 free Neurons/day, 00:00 UTC reset, direct OpenAI-compatible Workers AI endpoint, current model page, data-use policy and token-permission guidance.
- Historical P-02 `STUDIO-009F_ONLY` provider fields were confirmed and are not modified by this contract PR.
- V-02 future live validation is bounded to at most 3 requests, concurrency 1, retry 0, campaign ceiling 2,000 Neurons, PUBLIC/SYNTHETIC only, no AI Gateway, no tools/storage and money ceiling 0.
- Contract preparation performs no Cloudflare/account/token/model/provider runtime activity.
<!-- STUDIO-009V-02-CONTRACT-CHECKPOINT-0001 -->
