# STUDIO-009V-03 — NVIDIA NIM / DeepSeek V4 Pro 0813 bounded connected validation contract

Status: ACCEPTED SCOPE — CONTRACT ONLY — CONNECTED EXECUTION NOT AUTHORIZED UNTIL MERGE

Parent: `tasks/STUDIO-009.md`

Provider parent: `tasks/STUDIO-009P-03.md`

Progressive-live authority: `tasks/STUDIO-009R-01.md`

Predecessor V-tracks: STUDIO-009V-01 Groq — COMPLETE; STUDIO-009V-02 Cloudflare — COMPLETE

Primary owner: Studio Owner

Provider: NVIDIA-hosted NIM API Catalog

Provider profile: `provider-profile:nvidia-nim-free-deepseek-v4-pro-0813`

Provider child: `STUDIO-009P-03`

Exact model: `deepseek-ai/deepseek-v4-pro-0813`

Credential profile: `credential-profile:nvidia-nim-api-key`

Account reference: `account-ref:nvidia-developer-program-owner-account`

Cost class: ZERO_COST_ONLY

Usage class: INTERNAL_TESTING_EVALUATION_ONLY

MONEY_CEILING=0 USD

## 1. Purpose

Authorize a narrowly bounded provider-specific connected-validation track for the already-complete NVIDIA-hosted NIM P-03 child.

This V-track may later validate the exact NVIDIA-hosted Free Endpoint for `deepseek-ai/deepseek-v4-pro-0813` through NVIDIA's direct OpenAI-compatible HTTPS endpoint.

It does not grant persistent worker authority, automatic routing/failover, repository writer authority, merge/deploy/publish authority, tools, production use, partner-endpoint use, paid subscription, purchased credits, self-hosted deployment, or nonzero spend.

This contract PR performs zero NVIDIA/account/API-key/model/network activity.

## 2. Durable prerequisites

A later V-03 implementation and connected smoke must fail closed unless all remain true:

- P-03 contract, offline implementation, QA, Review and closeout are durable on `main`;
- P-03 implementation PR #68 is durably merged at `ac04040f40f544d70db10dba975481b7da5930ea`;
- P-03 closeout PR #69 is durably merged at `eae0b9462bca1c7e3819402219c6225a3f56fb0f`;
- P-03 state remains COMPLETE;
- P-03 provider remains DISABLED for connected execution;
- P-03 model remains DECLARED;
- P-03 evidence remains SYNTHETIC;
- STUDIO-009R-01 progressive-live governance remains accepted and unweakened;
- provider profile remains exactly `provider-profile:nvidia-nim-free-deepseek-v4-pro-0813`;
- provider child remains exactly `STUDIO-009P-03`;
- model remains exactly `deepseek-ai/deepseek-v4-pro-0813`;
- credential lineage remains exactly `credential-profile:nvidia-nim-api-key`;
- account identity reference remains exactly `account-ref:nvidia-developer-program-owner-account`;
- host remains exactly `integrate.api.nvidia.com`;
- MONEY_CEILING=0.

Any mismatch requires a new Owner decision before a real NVIDIA request.

## 3. Official NVIDIA evidence snapshot — re-verified 2026-09-08

Current official NVIDIA sources state or show:

- NVIDIA Developer Program membership enables NVIDIA-hosted NIM API access for development and testing;
- NVIDIA's NIM Developer page describes free NIM API endpoint access for prototyping;
- the exact model page for `deepseek-ai/deepseek-v4-pro-0813` currently shows `Free Endpoint - Available`;
- the exact model example uses base URL `https://integrate.api.nvidia.com/v1`;
- the exact model example uses model ID `deepseek-ai/deepseek-v4-pro-0813`;
- the exact model page reports a 1M-token context window;
- the exact example uses `max_tokens=16384`;
- NVIDIA API Trial Terms restrict trial access to limited trial/internal testing and evaluation and prohibit production use under trial authority;
- Trial Terms allow NVIDIA to impose usage limits and trial-credit limits; no permanent free RPM/RPD or permanent Credits entitlement is assumed.

Authoritative sources:

- https://developer.nvidia.com/nim
- https://build.nvidia.com/deepseek-ai/deepseek-v4-pro-0813
- https://docs.api.nvidia.com/nim/reference/llm-apis
- https://docs.api.nvidia.com/nim/reference/deepseek-ai-deepseek-v4-pro-0813
- https://docs.api.nvidia.com/nim/reference/deepseek-ai-deepseek-v4-pro-0813-infer
- https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf

These are evidence snapshots, not permanent entitlements. Activation-time evidence overrides stale assumptions and must fail closed on conflict.

## 4. Exact provider/model/transport boundary

Only this lineage may be validated:

- provider: NVIDIA-hosted NIM API Catalog;
- provider profile: `provider-profile:nvidia-nim-free-deepseek-v4-pro-0813`;
- provider child: `STUDIO-009P-03`;
- model: `deepseek-ai/deepseek-v4-pro-0813`;
- scheme: HTTPS;
- host: `integrate.api.nvidia.com`;
- base path: `/v1`;
- chat path: `/v1/chat/completions`;
- canonical base URL: `https://integrate.api.nvidia.com/v1`;
- redirects: forbidden;
- caller/model-supplied host/base URL/model: forbidden;
- partner endpoint: forbidden;
- self-hosted endpoint: forbidden;
- third-party gateway/proxy that obscures provider identity: forbidden;
- automatic model substitution/fallback: forbidden.

Provider-generated prose never proves provider/model/account/billing identity.

## 5. Account and credential boundary

Reserved lineage:

- credential profile: `credential-profile:nvidia-nim-api-key`;
- account ref: `account-ref:nvidia-developer-program-owner-account`.

The later real request requires an NVIDIA API key as bearer credential.

For the first connected validation:

- a real key may be created or selected only after V-03 contract merge, offline V-03 implementation, hostile tests and separate Owner connected preflight;
- raw key input must be hidden Owner-interactive, local, session-only and in-memory;
- no ambient `.env` or environment-variable lookup is authorized;
- no CLI-argument secret is authorized;
- no file cache, browser extraction, keychain automation, clipboard automation or remote secret store is authorized;
- the raw key may not be committed, printed, logged, returned, serialized, placed in prompt/model context, trace, evidence, memory, screenshot, command line or shell history;
- tests use synthetic credential suppliers only;
- Owner must prove the chosen key has a current revocation/deletion/invalidation path before the first request.

The dedicated NVIDIA credential bridge must not mutate or reuse Groq/Cloudflare provider-specific bridges as if they were generic.

## 6. Trial/privacy/data boundary

Connected prompts are restricted to:

- PUBLIC;
- synthetic prompts created specifically for validation.

Forbidden:

- private or unreleased GAME canon;
- proprietary source code not separately approved for export;
- credentials/secrets;
- personal data;
- confidential, controlled or sensitive data;
- unreleased assets;
- data without submission rights;
- production workload data.

V-03 does not broaden the P-03 PUBLIC/synthetic-only boundary.

## 7. Zero-cost and entitlement preflight

Before any real API-key input or request, Studio Owner must confirm using current NVIDIA UI/docs:

- the exact model still exposes a NVIDIA-hosted Free Endpoint;
- the selected account can use it without purchasing a subscription or credits;
- no partner endpoint is selected;
- no paid/self-hosted/cloud deployment is selected;
- no production subscription is activated for this track;
- current account-visible free/trial limits or Credits are sufficient for at most three tiny requests;
- no billing-method requirement, purchase, auto-recharge or paid fallback applies to the campaign;
- model/terms have not changed incompatibly.

NVIDIA-granted trial Credits may be consumed by the trial service. Purchased credits and monetary spend remain forbidden.

If free/trial eligibility, remaining entitlement or billing state is absent, exhausted, ambiguous or cannot be proven, do not request/input the key and do not send a request.

## 8. First connected smoke envelope

P-03 retained provider ceilings remain upper bounds:

- input ceiling: 32,768 tokens;
- requested output ceiling: 16,384 tokens;
- timeout ceiling: 60 seconds;
- concurrency: 1;
- automatic retry: 0;
- streaming: disabled;
- tools: disabled.

The first V-03 campaign is intentionally tighter:

- maximum real requests: 3;
- concurrency: exactly 1;
- automatic retries: exactly 0;
- timeout: <=60 seconds;
- estimated input: <=4,096 tokens per request;
- serialized request body: <=32,768 bytes;
- requested completion: <=512 tokens per request;
- response body read: <=131,072 bytes;
- data: PUBLIC/SYNTHETIC only;
- streaming: false;
- tools/functions: none;
- Remote MCP: none;
- code execution: none;
- file search: none;
- URL/browser context: none;
- automatic model fallback: none;
- automatic provider fallback: none;
- MONEY_CEILING=0.

Every real request must be durably reserved in a bounded local campaign ledger before network I/O. A failed request consumes one reservation. No automatic retry is permitted.

A successful smoke may not be repeated merely to improve evidence without fresh Owner authorization.

## 9. Fixed synthetic quality probes

Reachability is not acceptance.

At most three fixed PUBLIC/SYNTHETIC probes may cover:

1. strict structured-output/instruction compliance;
2. bounded reasoning/checking with no external tools;
3. GAME-style synthetic coding or transformation review using invented non-project content.

Acceptance requires the fixed rubric to pass without hidden human correction.

Prompts contain no private GAME canon, unreleased code/assets, personal data, credential, repository secret or raw account data.

## 10. Tool and external-capability denial

V-03 authorizes text-only direct chat completions.

Forbidden:

- tool/function definitions or execution;
- browser/search grounding;
- Remote MCP;
- shell/code execution;
- local/remote file access;
- repository write;
- external publication;
- image/audio;
- embeddings;
- fine-tuning;
- batch;
- third-party routing;
- partner endpoint;
- self-hosted deployment;
- automatic routing/failover;
- persistent worker promotion.

Unexpected tool-call output or evidence of undeclared external execution fails the campaign.

## 11. Safe response/usage evidence

A later implementation may preserve only sanitized evidence needed to prove:

- provider profile;
- exact model ID;
- exact host/path;
- HTTP status and safe Content-Type;
- bounded request count;
- safe provider response/model metadata;
- prompt/completion/total token usage if exposed;
- sanitized quality-rubric result;
- current free/trial preflight evidence reference;
- campaign monetary result after Owner confirmation.

The system must not invent quota, Credits consumed, billable amount or remaining entitlement if NVIDIA does not expose authoritative data.

## 12. Fail-closed normalization

Implementation must safely normalize at minimum:

- HTTP 401/403 -> authentication/authorization failure without secret echo;
- HTTP 422 -> request-validation failure;
- HTTP 429 -> rate-limit/capacity/entitlement failure;
- HTTP 5xx -> provider execution failure;
- timeout -> terminal campaign failure;
- redirect -> terminal host-policy failure;
- wrong host/path/model -> terminal identity failure;
- malformed JSON -> terminal response failure;
- oversized response -> terminal response failure;
- unsafe provider error body -> redacted failure;
- unexpected tool/function-call output -> failure;
- missing free/trial eligibility -> `ZERO_COST_ELIGIBILITY_UNPROVEN`;
- billing/subscription/purchase required -> `PAID_PATH_REQUIRED`.

No failure authorizes automatic retry, paid upgrade, model substitution, endpoint substitution, partner endpoint, provider fallback or scope broadening.

## 13. Live-state ceiling

This V-track may move NVIDIA only:

`DISABLED -> LIVE_VALIDATION_READY -> LIVE_VALIDATED`

It does not authorize:

- LIVE_SHADOW_WORKER;
- LIVE_BOUNDED_WORKER;
- ROUTING_ELIGIBLE;
- automatic routing/failover;
- repository writer claims;
- merge/deploy/publish authority;
- production use.

STUDIO-009E remains automatic routing/failover authority.

STUDIO-009F remains full connected multi-provider studio acceptance.

## 14. Kill and credential lifecycle

Before the first request, implementation must prove a local kill path preventing further NVIDIA calls.

Immediate stop conditions include secret exposure, account/key ambiguity, model/host/path mismatch, Free Endpoint disappearance, paid/subscription/purchase requirement, unexpected redirect, quota/Credit ambiguity, nonzero billable charge, terms drift, data-policy violation or undeclared tool/external-execution signal.

After connected QA and Review, the V-03 validation key must be revoked/deleted/invalidated before final Owner disposition unless an explicit later Owner decision changes that lifecycle. If revocation cannot be proven, V-03 cannot close as accepted.

Rollback remains MANUAL/FAKE. Groq and Cloudflare remain independently governed and are not automatic fallbacks.

## 15. Contract-only boundary

This contract PR must not:

- create/request/display/resolve an NVIDIA API key;
- query private NVIDIA account state;
- call NVIDIA or DeepSeek;
- send HTTPS traffic to `integrate.api.nvidia.com`;
- execute the model;
- consume a real trial request or Credits;
- enable tools;
- enable routing;
- grant worker authority;
- export private GAME data;
- change dependencies;
- spend money.

## 16. Contract acceptance

Requires:

- exact main baseline `eae0b9462bca1c7e3819402219c6225a3f56fb0f`;
- exact seven-path contract allowlist;
- deterministic contract-content/hygiene validation PASS;
- retained live-framework tests >=70;
- retained provider/connectivity focused tests >=548;
- retained full suite >=1053;
- `git diff --check` PASS;
- Rules CI success on immutable contract head;
- zero NVIDIA/account/API-key/model/network/tool/routing activity;
- zero connected execution;
- zero spend;
- separate Studio Owner merge decision.

Only after durable contract merge may the offline V-03 live-transport/smoke implementation begin.

<!-- STUDIO-009V-03-CONTRACT-CHECKPOINT-0001 -->
