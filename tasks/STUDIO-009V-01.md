# STUDIO-009V-01 — Groq bounded connected validation contract

Status: ACCEPTED — CONTRACT ONLY — CONNECTED EXECUTION NOT AUTHORIZED UNTIL MERGE

Parent: `tasks/STUDIO-009.md`

Provider parent: `tasks/STUDIO-009P-01.md`

Progressive-live authority: `tasks/STUDIO-009R-01.md`

Primary owner: Studio Owner

Cost class: ZERO_COST_ONLY

Money ceiling: `0 USD`

## 1. Purpose

Authorize a narrowly bounded first connected-validation track for the already-complete Groq offline child without granting normal worker authority, automatic routing, repository write authority, deployment authority, publication authority, or nonzero spend.

This contract exists because STUDIO-009R-01 separated provider-specific connected validation from final STUDIO-009F integrated acceptance.

The contract itself makes zero Groq/API/model/credential calls. Connected authority becomes usable only after this contract is durably merged and the separately bounded implementation is prepared and verified.

## 2. Durable prerequisites

The implementation must fail closed unless all of the following remain true:

- STUDIO-009P-01 Groq offline closeout is durable through PR #52 merge `1b75f250169ccdab3e2d67cbac4047253792c4a7`;
- STUDIO-009R-01 progressive live framework and closeout are durable through PR #58 merge `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`;
- the generic live gate/evidence framework remains accepted and unweakened;
- the Groq provider profile remains exactly `provider-profile:groq-free-gpt-oss-120b`;
- the provider child remains exactly `STUDIO-009P-01`;
- the credential lineage remains exactly `credential-profile:groq-api-key`;
- `MONEY_CEILING=0`.

Any mismatch requires a new Owner decision before a real request.

## 3. Current official provider evidence snapshot

Evidence re-verified on 2026-09-05 from Groq official documentation:

- model ID: `openai/gpt-oss-120b`;
- API base URL: `https://api.groq.com/openai/v1`;
- first connected endpoint: `POST /openai/v1/chat/completions`;
- Free Plan limits for this model: 30 RPM, 1,000 RPD, 8,000 TPM, 200,000 TPD;
- rate-limit responses use HTTP 429 and Groq exposes rate-limit headers;
- inference customer data is not retained by default except limited reliability/abuse circumstances;
- Zero Data Retention is available to customers through Data Controls;
- Groq distinguishes the Free tier from the paid Developer tier; upgrading to Developer requires a payment method and usage is billed;
- `openai/gpt-oss-120b` supports browser search/code execution, so those capabilities must be explicitly denied for this first validation.

Authoritative sources:

- https://console.groq.com/docs/model/openai/gpt-oss-120b
- https://console.groq.com/docs/rate-limits
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/api-reference
- https://console.groq.com/docs/your-data
- https://console.groq.com/docs/billing-faqs
- https://console.groq.com/docs/tool-use/local-tool-calling
- https://console.groq.com/docs/tool-use/built-in-tools
- https://console.groq.com/docs/legal/services-agreement

These are evidence snapshots, not permanent entitlements. The implementation must fail closed if current provider/account evidence conflicts with them.

## 4. Exact provider/model/transport boundary

Only the following connected lineage is authorized:

- provider: GroqCloud / Groq API;
- provider profile: `provider-profile:groq-free-gpt-oss-120b`;
- provider child: `STUDIO-009P-01`;
- model: `openai/gpt-oss-120b`;
- scheme: HTTPS;
- host: `api.groq.com`;
- base path: `/openai/v1`;
- endpoint: `/openai/v1/chat/completions`;
- transport: direct TLS/HTTP from the local trusted harness process;
- redirects: forbidden;
- proxy/host override: forbidden;
- alternate model or endpoint: forbidden.

Response prose is never identity evidence. The trusted transport must compare accepted configuration with the actual target host and provider response metadata, including the response `model` field when returned.

## 5. Account and zero-cost preflight

Before the first real request, the Studio Owner must explicitly confirm in Groq Console that:

- the organization/account used by the key is currently on the Free tier;
- no paid Developer-tier use is being intentionally invoked for this validation;
- no paid fallback, auto-upgrade, purchased credit, recharge, or chargeable service tier is authorized;
- ZDR is enabled in Data Controls for the relevant account/organization.

If tier or ZDR status is ambiguous, the smoke does not run.

The smoke must not use Groq paid Flex processing. It must use the ordinary Free-tier path only.

After the bounded smoke, the Owner must confirm observed charge/spend remains zero. Any observed nonzero charge fails the V-track and immediately returns the provider to fail-closed disposition.

## 6. Credential boundary

Credential lineage is fixed to `credential-profile:groq-api-key`.

For this first V-track, the only authorized secret-source mode is an Owner-interactive, session-only, in-memory handoff after accepted credential-lease metadata has been validated.

Rules:

- no API key in repository files, task/memory/evidence files, prompts, model output, logs, traces, exceptions, URLs, command lines, or screenshots;
- no environment-variable lookup;
- no `.env` lookup;
- no filesystem token/key cache;
- no browser-session extraction;
- no OS keychain/keyring/Credential Manager lookup;
- no cloud secret manager/vault/KMS;
- no automated clipboard extraction;
- no secret persistence after the local validation process exits;
- tests inject synthetic secret suppliers only;
- the real smoke asks the Owner through a hidden interactive input and never echoes the value.

This is a narrowly accepted V-01 session bridge, not a general production credential-store selection.

## 7. First-smoke request envelope

The entire initial V-01 connected smoke is capped at three real requests total.

Hard ceilings:

- request count: maximum 3;
- concurrency: exactly 1;
- automatic retry: exactly 0;
- request timeout: maximum 30 seconds;
- serialized request body: maximum 8,192 bytes;
- response body read: maximum 65,536 bytes;
- requested completion: maximum 256 tokens per request;
- input classification: PUBLIC/SYNTHETIC only;
- currency: USD;
- spend: exactly zero.

No automatic second attempt is authorized after an unsafe failure. Any later retry campaign requires a fresh Owner disposition.

## 8. Tool and external-capability denial

For every V-01 request:

- `tool_choice` must be `none`;
- no local function/tool definitions;
- no browser search;
- no built-in code execution;
- no Remote MCP;
- no Compound system;
- no documents/file context;
- no URL context;
- no search grounding;
- no provider storage;
- no batch/fine-tuning/LoRA;
- no external write or publication.

The transport must reject a response that indicates `tool_calls`, `executed_tools`, unexpected citations/search execution, alternate model use, or any other undeclared external capability.

## 9. Synthetic quality probes

API reachability alone is not acceptance.

The first smoke may use up to three fixed PUBLIC/SYNTHETIC probes covering:

1. strict structured-output compliance;
2. deterministic instruction discipline and bounded reasoning;
3. GAME-style transformation/checking with a fully synthetic payload.

The prompts and expected rubrics must contain no private GAME canon, unreleased asset, personal data, credential, or repository secret.

Promotion requires:

- every issued request receives an acceptable transport response;
- exact provider/model/host lineage remains valid;
- no forbidden tool/external capability is observed;
- required structured output validates;
- no secret-like material appears in sanitized evidence;
- human correction burden for these fixed smoke probes is zero;
- connected QA returns PASS;
- Review and Integration returns APPROVE;
- Studio Owner records the final V-01 disposition.

## 10. Live-state ceiling

This V-track may move Groq only as far as:

`DISABLED -> LIVE_VALIDATION_READY -> LIVE_VALIDATED`

It does not authorize:

- `LIVE_SHADOW_WORKER`;
- `LIVE_BOUNDED_WORKER`;
- `ROUTING_ELIGIBLE`;
- automatic routing or failover;
- repository writer claims;
- deployment/publication.

Worker promotion requires a later explicit contract/gate. Automatic routing remains STUDIO-009E authority.

## 11. Evidence and secret hygiene

Durable connected evidence may contain only sanitized metadata, digests, bounded counters, response identity metadata, quota headers normalized to safe values, quality scores, gate references, and Owner/QA/Review references.

Do not persist raw Authorization headers, API-key values, raw provider error bodies, private prompts, or unbounded raw model output.

Provider error text is untrusted. Public failures use stable safe codes and do not echo provider bodies or secret-bearing headers.

## 12. Kill, pause, and revocation

Before any real request the implementation must prove a local kill path that prevents additional calls.

Immediate fail-closed conditions include:

- Owner cancellation;
- wrong host/redirect;
- wrong model;
- tier/payment ambiguity;
- ZDR ambiguity/failure;
- secret exposure;
- unexpected tool/external execution;
- request/response ceiling breach;
- nonzero spend;
- malformed/oversized response;
- repeated/automatic request behavior;
- provider/account policy mismatch.

On failure, Groq remains or returns to `DISABLED`/`PAUSED` as appropriate. Stale approval cannot override revocation.

## 13. Implementation boundary

The separately accepted `tasks/STUDIO-009V-01-IMPLEMENTATION.md` controls implementation paths.

The implementation may introduce one narrowly trusted Groq HTTPS transport and one session-only credential bridge. Generic routing, repository connectivity, Unity, other providers, provider SDK installation, and nonzero-budget capability remain out of scope.

## 14. Contract-only boundary

This contract PR must not:

- resolve or request a real API key;
- open a Groq connection;
- call a model;
- create a real provider evidence result;
- enable Groq worker/routing authority;
- modify production live transport code;
- change dependencies;
- spend money.

Contract acceptance is documentation/memory only.

## 15. Acceptance

Contract acceptance requires:

- exact main baseline `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`;
- exact seven-path contract allowlist;
- retained deterministic data validation PASS;
- 70 live-framework tests PASS;
- 477 focused connectivity/provider tests PASS;
- 874 total retained tests PASS;
- `git diff --check` PASS;
- Rules CI success on the immutable contract head;
- zero Groq/provider/model/credential runtime activity;
- zero connected execution;
- zero spend;
- separate Studio Owner merge decision.

Only after this contract is durably merged may the implementation/connected-smoke track begin.
