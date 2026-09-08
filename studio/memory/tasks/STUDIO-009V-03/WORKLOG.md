# STUDIO-009V-03 WORKLOG

memory_schema_version: 1

task_id: STUDIO-009V-03
package_path: studio/memory/tasks/STUDIO-009V-03
canonical_task_contract: tasks/STUDIO-009V-03.md

## 2026-09-08 — Contract preparation

- P-03 implementation PR #68 durable merge verified at `ac04040f40f544d70db10dba975481b7da5930ea`.
- P-03 closeout PR #69 durable merge verified at `eae0b9462bca1c7e3819402219c6225a3f56fb0f`.
- Exact provider profile remains `provider-profile:nvidia-nim-free-deepseek-v4-pro-0813`.
- Exact model remains `deepseek-ai/deepseek-v4-pro-0813`.
- Exact future NVIDIA-hosted base remains `https://integrate.api.nvidia.com/v1`; chat path `/v1/chat/completions`.
- Current official model page re-verified `Free Endpoint - Available`, 1M context and OpenAI-compatible example with `max_tokens=16384`.
- NVIDIA Developer page re-verified hosted NIM access for prototyping/development/testing; Trial Terms remain non-production and limit/Credit aware.
- V-03 does not assume permanent free RPM/RPD or permanent Credits.
- First future campaign is bounded to max 3 PUBLIC/SYNTHETIC requests, concurrency 1, retry 0, <=4096 estimated input tokens, <=512 requested output tokens, no tools, no routing and money ceiling 0.
- Contract preparation performs no NVIDIA/account/API-key/model/provider/network activity.
<!-- STUDIO-009V-03-CONTRACT-CHECKPOINT-0001 -->
