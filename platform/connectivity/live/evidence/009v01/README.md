# STUDIO-009V-01 connected evidence staging

This directory is the sanitized evidence staging area for Groq V-01.

At the offline implementation checkpoint:

- `provider-live-state.json` is valid only through `LIVE_VALIDATION_READY`;
- `connected-validation.json` is deliberately `PENDING_REAL_SMOKE` and is not valid connected evidence;
- `quality-evaluation.json` is deliberately pending;
- no API key, raw Authorization header, raw provider error body, private prompt, or raw model output may be committed here.

A later bounded smoke may update these files only after the Studio Owner confirms Free tier and ZDR, supplies the key through hidden session-only input, and the smoke remains within the merged V-01 envelope.

## Failed authentication campaign and fresh retry authorization

- Failed campaign: `groq-v01-782697ab855de1bd`
- Implementation head: `c50469518be364476aee0ded221eabe7dab2f878`
- Reserved/attempted requests: `1`
- Failed slot: `1` / `STRUCTURED_OUTPUT`
- Result: `AUTH_FAILED`
- Automatic retry: `0`
- Remaining requests in failed campaign are NOT authorized.
- API key value persisted: `false`
- Raw provider output persisted: `false`
- Observed spend: `UNCONFIRMED`
- Studio Owner acknowledged the failed campaign.
- Studio Owner confirmed the failed key was revoked.
- Studio Owner confirmed a new key was created in `Default Project`.
- Studio Owner authorized one fresh retry campaign under the same 3-request / concurrency-1 / retry-0 / zero-money envelope.
- Provider live state remains `LIVE_VALIDATION_READY`.
<!-- STUDIO-009V-01-RETRY1-AUTHORIZATION-0003A -->

## RETRY1 bounded connected smoke checkpoint

- Campaign: `groq-v01-retry1-ac2943edca636f95`
- Completed: `2026-09-05T03:06:30Z`
- RETRY1 real requests: `3`
- Prior failed campaign real requests: `1`
- Cumulative V-01 real requests across authorized campaigns: `4`
- RETRY1 authorization head: `68d9a89becb13b441c2e5744cd3b134a76d03bd3`
- Prior failed campaign: `groq-v01-782697ab855de1bd`
- Concurrency: `1`
- Automatic retry: `0`
- Data: PUBLIC/SYNTHETIC fixed probes only
- Exact model: `openai/gpt-oss-120b`
- Exact transport: `https://api.groq.com/openai/v1/chat/completions`
- Raw provider output persisted: `false`
- Credential persisted: `false`
- Fixed quality probes: `PASS`
- Human correction count: `0`
- Observed spend: `UNCONFIRMED`
- Provider live state remains `LIVE_VALIDATION_READY`; QA, Review, Owner spend confirmation and Owner disposition are still required before `LIVE_VALIDATED`.
<!-- STUDIO-009V-01-RETRY1-SMOKE-CHECKPOINT-0003B -->

## Owner spend confirmation after RETRY1 smoke

- RETRY1 campaign: `groq-v01-retry1-ac2943edca636f95`
- Smoke evidence head: `efb14fea3963310f4a99336270e978d51dd1f1a1`
- Owner observed account tier: `FREE`
- Groq Usage cost display for `openai/gpt-oss-120b - on_demand`: `<0.01 USD`
- The `<0.01 USD` usage-cost display is recorded literally and is NOT represented as zero.
- Owner observed billable charge / amount due: `0 USD`
- `observed_spend=0` is therefore scoped to actual billable charge observed by the Owner, not the provider's sub-cent usage-cost metric.
- No additional Groq request was made for spend confirmation.
- Provider live state remains `LIVE_VALIDATION_READY`.
- Next gate: independent Connected QA.
<!-- STUDIO-009V-01-OWNER-SPEND-CONFIRMATION-0003C -->

## Independent Connected QA

- Immutable spend-confirmed head reviewed: `2b803e9e6ad3e1e75432f61aefa161a1a9e64595`
- QA result: `PASS`
- QA blockers: `0`
- QA reference: `qa:connected-groq-v01-2b803e9e6ad3`
- Independent probes: `60`
- Tests: `70` live / `527` focused / `924` total
- RETRY1 requests reviewed: `3`
- Prior failed authentication request preserved: `1`
- Cumulative V-01 real request history: `4`
- Free-tier billable charge observed: `0 USD`
- Literal Groq Usage cost display remains `<0.01 USD` and is not rewritten as zero.
- No provider/Groq/model request and no API-key input occurred during Connected QA.
- Provider live state remains `LIVE_VALIDATION_READY`.
- Connected Review and Owner disposition remain required before PR #60 may merge.
<!-- STUDIO-009V-01-CONNECTED-QA-CHECKPOINT-0003D -->

## Independent Connected Review and Integration

- Immutable Connected-QA head reviewed: `1f31119f7f5d00db781f5fc60653312dfa25c7d3`
- Underlying spend-confirmed head: `2b803e9e6ad3e1e75432f61aefa161a1a9e64595`
- Review result: `APPROVE`
- Review blockers: `0`
- Review reference: `review:connected-groq-v01-1f31119f7f5d`
- Independent integration/review probes: `80`
- Tests: `70` live / `527` focused / `924` total
- Verified exact 20-path PR scope, Groq/model/transport/credential lineage, bounded RETRY1 request envelope, prior failed-campaign lineage, sanitized evidence, QA durability, Free-tier zero billable charge, and the `LIVE_VALIDATED` promotion ceiling.
- Literal provider usage-cost metric remains `<0.01 USD`; observed billable charge remains `0 USD`.
- No Groq/provider/model request, API-key input, routing, tool execution, MCP, deployment, or publication occurred during Review.
- Provider state remains `LIVE_VALIDATION_READY`.
- Final Studio Owner disposition remains required. The temporary RETRY1 API key should be revoked before final `LIVE_VALIDATED` materialization so revocation evidence is durable.
- PR #60 must not merge before the Owner-disposition checkpoint is committed and Rules CI passes.
<!-- STUDIO-009V-01-CONNECTED-REVIEW-CHECKPOINT-0003E -->
