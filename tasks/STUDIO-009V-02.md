# STUDIO-009V-02 — Cloudflare Workers AI bounded connected validation contract

Status: ACCEPTED SCOPE — CONTRACT ONLY — CONNECTED EXECUTION NOT AUTHORIZED UNTIL MERGE

Parent: `tasks/STUDIO-009.md`

Provider parent: `tasks/STUDIO-009P-02.md`

Progressive-live authority: `tasks/STUDIO-009R-01.md`

Predecessor connected-validation track: `STUDIO-009V-01` Groq — COMPLETE

Primary owner: Studio Owner

Cost class: ZERO_COST_ONLY

Money ceiling: `0 USD`

## 1. Purpose

Authorize a narrowly bounded provider-specific connected-validation track for the already-complete Cloudflare Workers AI offline child.

This V-track may validate one exact Cloudflare-hosted model through the direct Workers AI OpenAI-compatible REST endpoint. It does not grant normal worker authority, automatic routing/failover, AI Gateway routing, repository writer authority, deployment/publication authority, prepaid-credit authority, Workers Paid authority, or nonzero spend.

The contract itself performs zero Cloudflare/account/token/model/network activity.

## 2. Durable prerequisites

The later implementation must fail closed unless all remain true:

- STUDIO-009P-02 Cloudflare offline implementation and closeout are durable; closeout PR #55 merged at `3cf7165c3263f8595b66a0d029b96022840adef3`;
- STUDIO-009R-01 progressive-live framework and closeout are durable at `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`;
- STUDIO-009V-01 Groq is durably closed on main before this V-02 contract begins;
- generic live gate/evidence semantics remain accepted and unweakened;
- provider profile remains exactly `provider-profile:cloudflare-workers-ai-free-nemotron-3-super`;
- provider child remains exactly `STUDIO-009P-02`;
- model remains exactly `@cf/nvidia/nemotron-3-120b-a12b`;
- credential lineage remains exactly `credential-profile:cloudflare-workers-ai-api-token`;
- account identity reference remains exactly `account-ref:cloudflare-workers-ai-owner-account`;
- `MONEY_CEILING=0`.

Any mismatch requires a new Owner decision before a real Cloudflare request.

## 3. Reconciliation of pre-009R Cloudflare policy

The existing P-02 offline files still contain historical `STUDIO-009F_ONLY` activation values. Those values predate STUDIO-009R-01.

STUDIO-009R-01 later created provider-specific V-tracks and explicitly permits STUDIO-009V-02 for Cloudflare bounded connected validation before STUDIO-009F.

This contract does not silently rewrite the historical P-02 record. The later V-02 implementation must reconcile only the Cloudflare provider-specific fields required to express:

- connected validation authority: `STUDIO-009V-02_ONLY`;
- maximum promotion: `LIVE_VALIDATED`;
- worker authority: `NONE`;
- routing authority: `NONE`;
- full integrated studio acceptance: still STUDIO-009F;
- automatic routing/failover: still STUDIO-009E.

Historical P-02 evidence remains historical and valid.

## 4. Official Cloudflare evidence snapshot — re-verified 2026-09-05

Current official Cloudflare documentation states:

- Workers AI Free includes a total free allocation of 10,000 Neurons per day;
- limits reset daily at 00:00 UTC;
- usage beyond the free allocation requires Workers Paid;
- Workers AI backend billing remains neuron-based even when model pricing is displayed in token-equivalent units;
- some models require a paid billing method, but `@cf/nvidia/nemotron-3-120b-a12b` is not in the current paid-required list;
- `@cf/nvidia/nemotron-3-120b-a12b` is Cloudflare-hosted, text generation, reasoning-capable and function-calling-capable;
- current model-page context window: 256,000 tokens;
- current model-page unit pricing: $0.50 per million input tokens and $1.50 per million output tokens;
- Workers AI supports OpenAI-compatible `/v1/chat/completions`;
- direct Workers AI base URL is `https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1`;
- Workers AI customer content is not used to train Workers AI models or improve Cloudflare/third-party services without explicit consent;
- customer content may be stored if the customer explicitly combines Workers AI with storage products such as R2, KV, Durable Objects or Vectorize.

Authoritative sources:

- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/workers-ai/platform/data-usage/
- https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/
- https://developers.cloudflare.com/workers-ai/get-started/rest-api/
- https://developers.cloudflare.com/workers-ai/models/nemotron-3-120b-a12b/
- https://developers.cloudflare.com/fundamentals/api/reference/permissions/

These are evidence snapshots, not permanent entitlements. Activation-time evidence overrides stale assumptions and must fail closed on conflict.

## 5. Exact provider/model/transport boundary

Only this connected lineage may be validated:

- provider: Cloudflare Workers AI;
- provider profile: `provider-profile:cloudflare-workers-ai-free-nemotron-3-super`;
- provider child: `STUDIO-009P-02`;
- model: `@cf/nvidia/nemotron-3-120b-a12b`;
- scheme: HTTPS;
- host: `api.cloudflare.com`;
- fixed base-path template: `/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1`;
- chat path: `/chat/completions`;
- transport: direct Workers AI REST/OpenAI-compatible endpoint only;
- redirects: forbidden;
- caller/model-supplied host or base URL: forbidden;
- caller/model-supplied account ID: forbidden;
- model alias/substitution: forbidden;
- AI Gateway route/header: forbidden;
- third-party model routing: forbidden.

No `cf-aig-gateway-id` is permitted. V-02 is not an AI Gateway validation.

Response prose is never provider/model/account identity evidence.

## 6. Account identity and credential boundary

Cloudflare REST requires an account identifier plus a Cloudflare API token.

Reserved lineage:

- account ref: `account-ref:cloudflare-workers-ai-owner-account`;
- credential profile: `credential-profile:cloudflare-workers-ai-api-token`.

For this first V-02 validation:

- raw Account ID is provided only by the Owner to the trusted local process after preflight;
- raw API token is provided only by hidden Owner-interactive session input;
- neither value may be committed to repo, memory, evidence, prompt, model output, trace, exception, URL printed to console, command line, screenshot captured for GAME evidence, `.env`, environment variable, keychain, browser-storage extraction, clipboard automation, or persistent local token cache;
- only opaque refs/digests may be durable;
- the API token must be temporary/revocable for the V-02 campaign;
- the token must not contain unrelated broad permissions.

Cloudflare documentation currently exposes a Workers AI token template and Workers AI account permissions. Documentation is not perfectly uniform about Read-only versus Read+Edit for custom tokens; V-02 therefore must not guess a privilege set. Owner preflight must use the Cloudflare Workers AI token template or another current official minimum-permission configuration verified immediately before the smoke. No Billing Edit, AI Gateway Edit, account-admin or unrelated scope is authorized.

## 7. Zero-cost and account-plan preflight

Before a real request, Studio Owner must confirm in Cloudflare Dashboard:

- the account used for V-02 is on a Workers Free path suitable for Workers AI;
- `@cf/nvidia/nemotron-3-120b-a12b` is still eligible without a paid billing method;
- no Workers Paid activation is being used for this V-track;
- no prepaid AI Gateway credits are being used;
- no Unified Billing path is being used;
- no paid-only model, third-party model or gateway route is involved;
- current Workers AI neuron usage leaves sufficient free headroom for the bounded campaign;
- no paid fallback, auto-upgrade, recharge or credit purchase is authorized.

Ambiguity means no smoke.

After the smoke, Owner must separately confirm observed neuron usage and observed billable charge. Code may not pre-claim spend zero.

## 8. First connected smoke envelope

One Owner-authorized campaign may issue at most three real requests.

Hard ceilings:

- request count: maximum 3;
- concurrency: exactly 1;
- automatic retry: exactly 0;
- timeout: maximum 30 seconds;
- serialized request body: maximum 8,192 bytes;
- response body read: maximum 65,536 bytes;
- requested completion: maximum 256 tokens per request;
- input classification: PUBLIC/SYNTHETIC only;
- campaign conservative neuron ceiling: 2,000 Neurons;
- retained P-02 daily GAME ceiling: 8,000 Neurons;
- current provider free-allocation snapshot: 10,000 Neurons/day;
- money ceiling: 0 USD.

The 2,000-Neuron campaign ceiling is intentionally much lower than the existing 8,000-Neuron daily GAME ceiling and the current 10,000-Neuron provider free allocation.

Every real request must be durably reserved in a local bounded campaign ledger before network I/O. No automatic retry is permitted. A failed campaign is terminal unless Owner creates a fresh disposition.

## 9. Tool, storage and external-capability denial

Although the model supports function calling, V-02 does not authorize tools.

For every smoke request:

- no tool/function definitions;
- no tool execution;
- no AI Gateway;
- no gateway logging/caching;
- no storage service;
- no R2/KV/Durable Objects/Vectorize;
- no AI Search/AutoRAG;
- no browser/search grounding;
- no Remote MCP;
- no code execution;
- no batch/fine-tuning/LoRA;
- no external write/publication;
- no third-party provider route;
- no streaming if it weakens the bounded response-body guarantee.

Unexpected tool/function-call output or evidence of undeclared external execution fails the probe.

## 10. Synthetic quality probes

Reachability is not acceptance.

At most three fixed PUBLIC/SYNTHETIC probes may cover:

1. strict structured-output compliance;
2. deterministic instruction discipline and bounded reasoning;
3. GAME-style synthetic transformation/checking.

Prompts contain no private GAME canon, unreleased asset, personal data, credential, raw account ID or repository secret.

Acceptance requires zero human correction on the fixed probe rubric.

## 11. Quota and neuron evidence

Cloudflare uses Neurons as the backend consumption unit.

V-02 must:

- retain the existing provider neuron conversion snapshot only as an estimate;
- bound the campaign by both request count and a conservative neuron ceiling;
- capture safe provider usage/token metadata where exposed;
- avoid inventing neuron consumption when the response does not expose authoritative neuron usage;
- require Owner dashboard confirmation after the smoke;
- distinguish model unit-price display from actual billable charge;
- fail if usage requires Workers Paid or any nonzero billable charge.

Quota exhaustion does not authorize retry, paid upgrade or alternate model.

## 12. Fail-closed normalization

Implementation must safely normalize at least:

- HTTP 401/403 credential/account/permission failure;
- HTTP 429 and Cloudflare internal `3036` free allocation exhaustion;
- HTTP 429 and internal `3040` capacity unavailable;
- HTTP 403 and internal `5035` paid-plan-required;
- timeout;
- redirect;
- wrong account path;
- wrong model;
- malformed JSON;
- oversized response;
- unsafe provider error body;
- unexpected tool/function-call output;
- payment/tier ambiguity.

No raw provider error body is committed or echoed if it could contain sensitive values.

## 13. Live-state ceiling

This V-track may move Cloudflare only:

`DISABLED -> LIVE_VALIDATION_READY -> LIVE_VALIDATED`

It does not authorize:

- `LIVE_SHADOW_WORKER`;
- `LIVE_BOUNDED_WORKER`;
- `ROUTING_ELIGIBLE`;
- automatic routing/failover;
- repository writer claims;
- deployment/publication.

STUDIO-009E remains routing/failover authority. STUDIO-009F remains full connected studio acceptance.

## 14. Kill, revoke and temporary-token lifecycle

Before the first request, implementation must prove a local kill path preventing any further calls.

After connected QA and Review, the temporary V-02 token must be revoked/deleted before final Owner disposition unless an explicit later Owner decision changes that lifecycle.

Immediate stop conditions include account/model mismatch, token exposure, paid requirement, quota anomaly, unexpected gateway/tool/storage activity, nonzero billable charge or provider-policy drift.

## 15. Contract-only boundary

This contract PR must not:

- request or resolve a Cloudflare Account ID;
- create or request a real API token;
- call Cloudflare;
- call the model;
- consume Neurons;
- change Cloudflare provider runtime code/policies;
- reconcile the legacy `STUDIO-009F_ONLY` values yet;
- enable AI Gateway;
- change dependencies;
- grant worker/routing authority;
- spend money.

## 16. Contract acceptance

Requires:

- exact main baseline `6bdb1daa9b2dee65a3262da8caf8c3ce42a4ac46`;
- exact seven-path contract allowlist;
- deterministic data validation PASS;
- 70 live-framework tests PASS;
- 527 focused connectivity/provider tests PASS;
- 924 total retained tests PASS;
- `git diff --check` PASS;
- Rules CI success on immutable contract head;
- zero Cloudflare/account/token/model runtime activity;
- zero connected execution;
- zero spend;
- separate Studio Owner merge decision.

Only after durable contract merge may the bounded offline implementation track begin.

<!-- STUDIO-009V-02-CONTRACT-CHECKPOINT-0001 -->

## 17. Credential-bridge scope correction

Post-merge implementation preflight found that the existing `scripts/session_credential_bridge.py` is not provider-neutral: it is intentionally bound to Groq V-01 (`credential-profile:groq-api-key`, `provider:groqcloud`, `GROQ_V01_CONNECTED_VALIDATION`).

STUDIO-009V-02 must therefore not reuse that module as if it were Cloudflare-neutral and must not broaden the already-validated Groq bridge under this provider track.

The corrected V-02 implementation is authorized to add a dedicated:

- `scripts/cloudflare_session_credential_bridge.py`
- `tests/test_cloudflare_session_credential_bridge.py`

The Cloudflare bridge must preserve the same session-only, hidden Owner-interactive, no-ambient-secret and no-secret-escape guarantees while binding exactly:

- credential profile: `credential-profile:cloudflare-workers-ai-api-token`
- subject: Cloudflare Workers AI
- purpose: STUDIO-009V-02 connected validation
- no persistent Account ID or API token

This correction changes implementation scope only. It authorizes zero Cloudflare/account/token/network/model activity and does not broaden the `LIVE_VALIDATED`, money, routing, worker, AI Gateway or data ceilings.

<!-- STUDIO-009V-02-CREDENTIAL-BRIDGE-CORRECTION-0001A -->
