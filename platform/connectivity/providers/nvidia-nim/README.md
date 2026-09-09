# NVIDIA NIM / DeepSeek V4 Pro 0813 — offline provider child

STUDIO-009P-03 implements deterministic provider metadata and an offline/synthetic adapter for the NVIDIA-hosted NIM API Catalog candidate `deepseek-ai/deepseek-v4-pro-0813`.

This directory grants no connected authority. The provider profile remains `DISABLED`, the model remains `DECLARED`, the child evidence remains `SYNTHETIC`, and the monetary ceiling remains USD 0.

Accepted future transport identity is HTTPS host `integrate.api.nvidia.com`, base `/v1`, chat path `/v1/chat/completions`. P-03 itself performs no HTTPS request, account lookup, API-key resolution, model inference, tool execution, routing, failover, production use, or spend.

Data boundary is PUBLIC/synthetic only. PRIVATE, unreleased, personal, confidential, controlled, sensitive, secret-bearing, or otherwise unapproved GAME data is forbidden.

Free/trial entitlement is dynamic evidence, not a permanent quota. Any later STUDIO-009V-03 smoke must re-prove current no-cost eligibility and remain fail-closed if billing, subscription, or uncertain entitlement is encountered.

Rollback remains MANUAL/FAKE. Automatic routing/failover remains STUDIO-009E. Full connected multi-provider acceptance remains STUDIO-009F.

## STUDIO-009V-03 offline live-validation preparation

V-03 adds a separate `live-validation-policy.json` and provider-specific live transport/smoke/session-credential code while preserving the P-03 historical core:

- provider profile remains `DISABLED`;
- model profile remains `DECLARED`;
- P-03 transport/data/quota/budget core values remain unchanged;
- V-03 current live state is only `LIVE_VALIDATION_READY`;
- connected evidence and quality evidence remain pending;
- no NVIDIA API key has been requested/input/resolved by this implementation;
- no NVIDIA request has occurred;
- no tools, routing, worker promotion, production use, paid path, or nonzero spend is authorized.

The later connected campaign is capped at three PUBLIC/SYNTHETIC sequential requests with retry 0 and must pass a separate Owner connected preflight.
