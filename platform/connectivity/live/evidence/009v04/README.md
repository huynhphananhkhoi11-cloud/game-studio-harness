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


## Bounded real-smoke PASS and Owner zero-cost confirmation

Campaign `campaign:poolside-v04-c966b37a` completed exactly 3 real requests / 3 network successes against `poolside/laguna-s-2.1` on `inference.poolside.ai`.

All fixed probes passed without human correction. Only safe hashes, model/transport identity, finish reason, and token-usage metadata are retained. No raw API key, Authorization value, prompt, raw model output, provider error body, account-private data, or billing-private data is committed.

Owner post-smoke monetary basis:
- Poolside official model/release material was re-verified on 2026-09-10 as stating the Laguna API is free to use for a limited time.
- The Owner reports no Billing / Usage / Credits / Payment / Invoices / Subscription surface exposed in the account UI used for this validation.
- No payment-method requirement, subscription purchase, credit purchase, auto-recharge, or paid fallback was encountered before or during the bounded campaign.
- The public `poolsideai/pool` repository establishes the public Poolside CLI/agent and direct Poolside inference integration, but is not treated as pricing authority.
- The Owner explicitly accepts the available evidence as sufficient to confirm the bounded V-04 campaign remained at USD 0.
- Provider-metered billable charge remains unavailable because no authoritative billing meter is exposed; this absence is recorded rather than invented.

No additional real request is authorized. Connected QA must review this immutable evidence without contacting Poolside.

<!-- STUDIO-009V-04-SMOKE-OWNER-ZERO-COST-CHECKPOINT-0007 -->
