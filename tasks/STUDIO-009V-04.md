# STUDIO-009V-04 — Poolside / Laguna S 2.1 bounded connected validation contract

Status: ACCEPTED SCOPE — CONTRACT ONLY — THIS PR AUTHORIZES NO POOLSIDE ACCOUNT, KEY OR NETWORK ACTIVITY

Parent: `tasks/STUDIO-009.md`

Provider parent: `tasks/STUDIO-009P-04.md`

Progressive-live authority: `tasks/STUDIO-009R-01.md`

Predecessor connected-validation tracks:
- STUDIO-009V-01 Groq — COMPLETE
- STUDIO-009V-02 Cloudflare — COMPLETE
- STUDIO-009V-03 NVIDIA — FROZEN AT ACCOUNT VERIFICATION

Primary owner: Studio Owner

Provider: Poolside standalone hosted inference API

Provider profile: `provider-profile:poolside-direct-laguna-s-2.1`

Provider child: `STUDIO-009P-04`

Exact model: `poolside/laguna-s-2.1`

Credential profile: `credential-profile:poolside-api-key`

Account reference: `account-ref:poolside-owner-account`

Cost class: ZERO_COST_ONLY

Usage class: INTERNAL_TESTING_EVALUATION_ONLY

MONEY_CEILING=0 USD

## 1. Purpose

Define a narrowly bounded connected-validation track for the already-complete P-04 Poolside child.

This contract does not itself create or inspect a Poolside account, create/copy/input an API key, call Poolside/Laguna, install or execute the `pool` CLI, send provider traffic, consume quota, use tools/MCP/ACP, enable routing, export private GAME data, or spend money.

Merging this contract authorizes only the later deterministic/offline V-04 live-transport implementation. A real Poolside request still requires that offline implementation to merge, pass independent QA and Review/Integration, and then pass a separate Owner connected preflight.

## 2. Durable prerequisites

Any later V-04 connected activity must fail closed unless all remain true:

- P-04 contract/offline implementation/QA/Review/closeout are durable on `main`;
- P-04 implementation PR #74 is durably merged at `e7ed2d087117eacad42141ca2d0c6587d16721dc`;
- P-04 closeout PR #75 is durably merged at `3726e2bd031ce2022f5a93ff1d40c404fb815682`;
- P-04 state is COMPLETE;
- provider profile remains `DISABLED`;
- model profile remains `DECLARED`;
- child evidence remains `SYNTHETIC`;
- P-04 grants no connected authority;
- STUDIO-009R-01 progressive-live governance remains accepted;
- provider profile is exactly `provider-profile:poolside-direct-laguna-s-2.1`;
- provider child is exactly `STUDIO-009P-04`;
- model is exactly `poolside/laguna-s-2.1`;
- credential lineage is exactly `credential-profile:poolside-api-key`;
- account reference is exactly `account-ref:poolside-owner-account`;
- direct host remains exactly `inference.poolside.ai`;
- direct base path remains `/v1`;
- direct chat path remains `/v1/chat/completions`;
- MONEY_CEILING=0;
- V-03 NVIDIA remains frozen and is not resumed by V-04;
- P-05 OpenCode remains non-authoritative while V-04 is the active write track.

Any mismatch requires a fresh Owner decision before real Poolside activity.

## 3. Official Poolside evidence snapshot — re-verified 2026-09-09

Current official Poolside sources show:

- model `poolside/laguna-s-2.1`;
- 118B total parameters / 8B active;
- model context evidence up to 1M;
- OpenAI-compatible chat API;
- standalone direct example base URL `https://inference.poolside.ai/v1`;
- public wording `Free to use for a limited time`;
- standalone setup can open `platform.poolside.ai` where the user creates or copies an API key;
- Poolside CLI can store credentials in `~/.config/poolside/credentials.json` and can resolve `POOLSIDE_API_KEY` / `POOLSIDE_TOKEN`;
- `pool logout` removes locally stored credentials but is not proof of server-side API-key revocation;
- Terms of Use were last updated July 21, 2026;
- Terms define Content to include prompts, code, output and feedback;
- Terms permit Content use to provide/maintain/improve/develop Products, including model training, unless opted out;
- direct Site users may select Training Opt-Out under User Settings;
- feedback-linked or safety-review Content can remain usable under stated exceptions;
- certain Products/features may require fees and fees may change;
- Terms prohibit access intended to circumvent applicable fees or usage limits.

Authoritative sources:

- https://poolside.ai/models
- https://poolside.ai/blog/introducing-laguna-s-2-1
- https://poolside.ai/legal/eula
- https://docs.poolside.ai/cli/install
- https://docs.poolside.ai/cli/cli-reference
- https://platform.poolside.ai/

The public `docs.poolside.ai/api` deployment documentation describes deployment-specific API domains and is not authority to replace the standalone endpoint identity captured from the public model page.

All evidence is dynamic. Activation-time UI/docs override stale assumptions and must fail closed on conflict.

## 4. Exact provider/model/transport boundary

Only this lineage may later be validated:

- provider: Poolside standalone hosted inference API;
- provider profile: `provider-profile:poolside-direct-laguna-s-2.1`;
- child: `STUDIO-009P-04`;
- model: `poolside/laguna-s-2.1`;
- HTTPS only;
- host: `inference.poolside.ai`;
- base path: `/v1`;
- chat path: `/v1/chat/completions`;
- canonical base URL: `https://inference.poolside.ai/v1`;
- redirects: forbidden;
- caller/model-supplied host/path/model: forbidden;
- OpenRouter/Baseten/Vercel/Kilo/other gateways: forbidden;
- enterprise/deployment-specific Poolside endpoints: forbidden;
- local/self-hosted Laguna: forbidden;
- automatic endpoint/model/provider substitution: forbidden.

Provider-generated prose is never identity, billing or account evidence.

## 5. Account and credential boundary

Reserved lineage:

- credential profile: `credential-profile:poolside-api-key`;
- account ref: `account-ref:poolside-owner-account`.

The contract PR performs zero account/key activity.

After contract merge and only after the offline V-04 implementation has passed QA/Review, Owner connected preflight may inspect current Poolside account/UI state for:

- standalone zero-cost eligibility;
- exact direct API/model availability;
- absence of mandatory payment/billing/subscription for the bounded campaign;
- API-key creation/selection controls;
- a server-side key revocation/deletion/invalidation path.

The current public CLI documentation only proves local credential removal via `pool logout`; that is insufficient for GAME server-side revocation proof.

Before the first real request:

- the Owner must prove an account-level server-side revocation/deletion/invalidation path;
- any validation key must be dedicated/temporary where the UI permits;
- raw key input must be hidden Owner-interactive, local, session-only and in-memory;
- no `.env`, ambient environment variable, CLI argument, credential file, browser extraction, keychain automation, clipboard automation or remote secret store is authorized;
- raw key must never be committed, printed, logged, returned, serialized, placed in prompt/model context, trace, evidence, memory, screenshot, URL, shell history or command line;
- deterministic tests use synthetic credential suppliers only.

If account identity, zero-cost status or revocation path is ambiguous, do not create/input/use the key.

## 6. Data, terms and training boundary

Connected prompts remain restricted to PUBLIC and synthetic validation content.

Forbidden:

- private/unreleased GAME canon;
- proprietary source code not separately approved for export;
- unreleased assets;
- credentials/secrets;
- personal data;
- confidential/sensitive/regulatory data;
- data without submission rights;
- production workload data.

Training Opt-Out, if available and enabled, does not broaden GAME data authority.

No feedback/rating is submitted during initial V-04 because Terms treat feedback specially.

## 7. Zero-cost eligibility preflight

Before any real API-key input or request, Owner must confirm using current Poolside UI/docs:

- standalone `poolside/laguna-s-2.1` access is currently available;
- direct route remains `https://inference.poolside.ai/v1`;
- the account can run the bounded campaign at USD 0;
- no subscription purchase is required;
- no credit purchase is required;
- no payment-method requirement is required for this bounded GAME campaign;
- no auto-recharge or paid fallback applies;
- no third-party paid route is selected;
- no production plan is activated for this track;
- current free availability is sufficient for at most three tiny requests;
- Terms/data policy have not changed incompatibly.

`Free to use for a limited time` is dynamic evidence, not a permanent entitlement.

If zero-cost eligibility is absent, expired, exhausted, ambiguous, payment-gated or cannot be proven, V-04 is `ZERO_COST_ELIGIBILITY_UNPROVEN` and no key/request is allowed.

## 8. First connected smoke envelope

Maximum campaign:

- real requests: 3;
- concurrency: exactly 1;
- automatic retries: exactly 0;
- timeout: <=60 seconds;
- estimated input: <=4096 tokens/request;
- requested completion: <=1024 tokens/request;
- serialized request body: <=32768 bytes;
- response read: <=131072 bytes;
- data: PUBLIC/SYNTHETIC only;
- streaming: false;
- tools/functions: none;
- Remote MCP: none;
- ACP: none;
- shell/code execution: none;
- file access/search: none;
- browser/URL context: none;
- repository write: none;
- automatic model fallback: none;
- automatic provider fallback: none;
- MONEY_CEILING=0.

Every real request must be reserved in a bounded local campaign ledger before network I/O. A failed request consumes its reservation. No automatic retry.

A successful smoke may not be repeated merely to improve evidence without fresh Owner authorization.

## 9. Fixed synthetic quality probes

Reachability is not acceptance.

At most three fixed PUBLIC/SYNTHETIC probes may cover:

1. strict instruction/structured-output compliance;
2. bounded reasoning/checking without tools;
3. synthetic GAME-style coding/transformation/review using invented non-project content.

Acceptance requires the fixed rubric to pass without hidden human correction.

## 10. Poolside CLI / harness denial

V-04 evaluates the direct text-only provider/model path, not the Poolside agent harness.

Forbidden:

- installing/executing `pool`;
- Poolside repository context;
- terminal/shell agent actions;
- tool definitions/execution;
- MCP;
- ACP;
- Poolside secret storage;
- Poolside credential-file access;
- file/repository mutation;
- browser/search grounding.

A later harness/tool-capability task is separate.

## 11. Safe evidence

Later connected evidence may preserve only sanitized facts needed to prove:

- provider profile;
- exact model;
- exact host/path;
- HTTP status and safe Content-Type;
- bounded request count;
- safe response/model metadata;
- token usage if exposed;
- fixed quality-rubric result;
- current zero-cost preflight evidence reference;
- server-side key lifecycle evidence reference;
- Owner-confirmed monetary result.

Do not persist raw prompt/output if not needed for the rubric. Never persist raw API keys.

Do not invent quota, remaining free entitlement or billable amount if Poolside does not expose authoritative data.

## 12. Fail-closed normalization

Implementation must normalize at minimum:

- 401/403 -> authentication/authorization failure without secret echo;
- 404 -> endpoint/model not found;
- 422 -> request-validation failure;
- 429 -> rate-limit/capacity/eligibility failure;
- 5xx -> provider execution failure;
- timeout -> terminal campaign failure;
- redirect -> host-policy failure;
- wrong host/path/model -> identity failure;
- malformed JSON -> response failure;
- oversized response -> response failure;
- unsafe provider error body -> redacted failure;
- unexpected tool/function output -> unauthorized-capability failure;
- missing current free eligibility -> `ZERO_COST_ELIGIBILITY_UNPROVEN`;
- billing/subscription/payment required -> `PAID_PATH_REQUIRED`;
- key revocation path unproven -> `CREDENTIAL_REVOCATION_UNPROVEN`;
- Terms/data-policy drift -> terminal policy failure.

No failure authorizes retry escalation, payment, model/provider/endpoint fallback, CLI/tool activation or scope broadening.

## 13. Live-state ceiling

V-04 may move Poolside only:

`DISABLED -> LIVE_VALIDATION_READY -> LIVE_VALIDATED`

It does not authorize:

- LIVE_SHADOW_WORKER;
- LIVE_BOUNDED_WORKER;
- ROUTING_ELIGIBLE;
- automatic routing/failover;
- repository writer authority;
- merge/deploy/publish authority;
- production use.

STUDIO-009E remains automatic routing/failover authority.
STUDIO-009F remains full connected multi-provider acceptance.

## 14. Kill and credential lifecycle

Before first request, implementation must prove a local kill path that prevents further Poolside calls.

Immediate stop conditions:

- suspected key exposure;
- account/key ambiguity;
- model/host/path mismatch;
- standalone free offer disappearance;
- billing/subscription/payment requirement;
- unexpected redirect;
- zero-cost ambiguity;
- nonzero billable charge;
- Terms/data-policy drift;
- unexpected tool/external-execution signal.

After connected QA and Review, the validation key must be revoked/deleted/invalidated server-side and safe revocation evidence recorded before final Owner disposition unless a later explicit Owner decision changes the lifecycle.

If server-side revocation cannot be proven, V-04 cannot close as accepted.

Rollback remains MANUAL/FAKE. Groq/Cloudflare are not automatic fallbacks; NVIDIA remains frozen.

## 15. Contract-only boundary

This contract PR must not:

- create/login/inspect a Poolside account;
- create/request/display/copy/input/resolve a Poolside API key;
- call Poolside/Laguna;
- send HTTPS traffic to `inference.poolside.ai`;
- execute `pool`;
- execute a model/tool/MCP/ACP;
- consume real quota;
- enable routing;
- grant worker authority;
- export private GAME data;
- change dependencies;
- spend money.

## 16. Contract acceptance

Requires:

- exact main baseline `3726e2bd031ce2022f5a93ff1d40c404fb815682`;
- exact seven-path contract allowlist;
- deterministic contract-content/hygiene validation PASS;
- existing Poolside offline tests exactly 100;
- STUDIO-007F CLI regression tests exactly 5;
- retained provider/connectivity focused tests exactly 762;
- retained full suite exactly 1267;
- `git diff --check` PASS;
- Rules CI success on immutable contract head;
- zero Poolside/account/API-key/model/network/CLI/tool/MCP/ACP/routing activity;
- zero connected execution;
- zero spend;
- separate Studio Owner merge decision.

Only after durable contract merge may the offline V-04 live-transport/smoke implementation begin.

<!-- STUDIO-009V-04-CONTRACT-CHECKPOINT-0001 -->
