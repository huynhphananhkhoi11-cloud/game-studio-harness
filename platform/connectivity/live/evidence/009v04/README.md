# STUDIO-009V-04 Poolside connected-validation evidence

This directory is materialized at the **offline live-implementation** checkpoint.

At this checkpoint:

- `provider-live-state.json` is valid only through `LIVE_VALIDATION_READY`;
- `connected-validation.json` is deliberately `PENDING_REAL_SMOKE`;
- `quality-evaluation.json` is deliberately `PENDING_REAL_SMOKE`;
- no Poolside API key, Authorization value, provider error body, private prompt, raw model output, account-private data, or billing-private data may be committed;
- no real Poolside request has occurred;
- observed spend is not fabricated;
- routing authority remains absent.

A later Owner connected preflight must re-prove current standalone free-limited offer / account entitlement / no-paid-path / revocation conditions before any session credential input.

The real smoke is capped at three PUBLIC/SYNTHETIC sequential requests, retry 0, and money ceiling USD 0.


Poolside-specific additions:

- `pool` CLI remains unused and unauthorized;
- `zero_cost_eligibility_verified` remains false until Owner connected preflight;
- `server_side_revocation_verified` remains false until Owner proves the server-side lifecycle;
- completion ceiling is 1024 tokens/request;
- no gateway, enterprise endpoint, local/self-hosted route, tool, MCP, ACP or routing is authorized.

<!-- STUDIO-009V-04-OFFLINE-LIVE-IMPLEMENTATION-CHECKPOINT-0002 -->
