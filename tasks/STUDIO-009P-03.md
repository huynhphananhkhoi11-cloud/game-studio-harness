# STUDIO-009P-03 - NVIDIA-hosted NIM provider child contract

Status: ACCEPTED SCOPE - CONTRACT ONLY - IMPLEMENTATION NOT STARTED

Parent: `tasks/STUDIO-009D.md`

Provider product: NVIDIA-hosted NIM API Catalog trial endpoint

Selected model candidate: `deepseek-ai/deepseek-v4-pro-0813`

Primary owner: Studio Owner

Cost class: ZERO_COST_ONLY

Usage class: INTERNAL_TESTING_EVALUATION_ONLY

Connected authority: NONE

## Goal

Define the third real-provider child contract for GAME using the NVIDIA-hosted NIM API Catalog with exact model `deepseek-ai/deepseek-v4-pro-0813`, while preserving STUDIO-009D and the accepted progressive-live STUDIO-009R-01 / STUDIO-009V* boundary.

This contract records provider/model/transport/authentication/data/quota/budget/failure/rollback policy only. It does not create or resolve an NVIDIA API key, call NVIDIA or DeepSeek, query account state, execute a model/tool, enable routing, create a persistent worker, or spend money.

STUDIO-009P-01 Groq and STUDIO-009P-02 Cloudflare remain independently accepted. Their V-01/V-02 results are not broadened by this child.

## 1. Provider identity and authoritative sources

Authoritative provider-facing product: NVIDIA-hosted NIM API endpoint exposed through the NVIDIA API Catalog.

Authoritative sources re-verified for this contract on 2026-09-08:

- https://developer.nvidia.com/nim
- https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317
- https://build.nvidia.com/deepseek-ai/deepseek-v4-pro-0813
- https://build.nvidia.com/deepseek-ai/deepseek-v4-pro-0813/modelcard
- https://docs.api.nvidia.com/nim/reference/llm-apis
- https://docs.api.nvidia.com/nim/reference/deepseek-ai-deepseek-v4-pro-0813
- https://docs.api.nvidia.com/nim/reference/deepseek-ai-deepseek-v4-pro-0813-infer
- https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf

Provider profile lineage:

`provider-profile:nvidia-nim-free-deepseek-v4-pro-0813`

Runtime identity must later be proven from accepted configuration plus validated HTTPS transport metadata. Model-generated prose is never provider/model identity evidence.

NVIDIA currently describes Developer Program NIM API access as free access for prototyping/research/development/testing. NVIDIA API Trial Terms restrict trial use to internal testing/evaluation and not production unless separate production/subscription terms apply. This child is therefore non-production.

## 2. Exact model identity and version policy

Only exact model ID:

`deepseek-ai/deepseek-v4-pro-0813`

No `latest`, preview alias, provider-selected substitute, caller-supplied model, automatic migration, catalog fallback, or second model.

Current official evidence records:

- `Free Endpoint - Available`;
- DeepSeek AI model identity;
- text input / text output;
- 1,000,000-token context;
- intended text generation, reasoning, coding and agentic workflows;
- OpenAI-compatible chat completions;
- NVIDIA API reference `max_tokens` range 1..16384.

The 1M provider context is evidence, not a GAME request allowance. Initial GAME connected validation remains deliberately much smaller.

Declared provider-neutral capabilities for this first child:

- `TEXT_GENERATION`
- `REASONING`

Coding/repository work is a workload class, not a new authority capability.

Although the model is described as agentic/tool-use capable, this child does NOT authorize tool calling/execution, browser, MCP, code execution, shell execution, file writes, image/audio, embeddings, fine-tuning, batch, or undeclared capability.

## 3. Transport allowlist

Future connected transport candidate:

- scheme: `https`
- host: `integrate.api.nvidia.com`
- base path: `/v1`
- chat endpoint: `/v1/chat/completions`
- canonical base URL: `https://integrate.api.nvidia.com/v1`

Arbitrary host overrides, cross-host redirects, caller/model-supplied URLs, partner endpoints, self-hosted endpoints, third-party gateways, HTTP plaintext, WebSocket, gRPC, browser automation, or proxy routes that obscure provider identity are forbidden.

P-03 implementation remains offline/synthetic. Real HTTPS activity requires separately merged STUDIO-009V-03 authority.

## 4. Authentication and credential lineage

Future NVIDIA-hosted authentication: NVIDIA API key as bearer credential through an approved transport only.

Reserved STUDIO-009C lineage:

`credential-profile:nvidia-nim-api-key`

Reserved account reference:

`account-ref:nvidia-developer-program-owner-account`

These refs do not prove any account/key exists.

P-03 authorizes no NVIDIA account creation, Developer Program enrollment, API-key creation/display/storage/lookup/lease/rotation/revocation, or environment-variable resolution.

No raw key may appear in repository files, Git history, prompts, outputs, traces, evidence, screenshots, worklogs, memory, URLs, command lines, stdout/stderr, exceptions, or clipboard automation.

## 5. Data policy and trial privacy boundary

Initial future connected-validation data is restricted to:

- `PUBLIC`
- synthetic prompts created for validation

Forbidden:

- PRIVATE project canon;
- unreleased GDD/game content;
- proprietary source code not separately approved for export;
- credentials/secrets;
- confidential/controlled/sensitive information;
- personal data;
- payment/health/sensitive research data;
- unreleased assets;
- data without submission rights.

Current NVIDIA API Trial Terms prohibit confidential/controlled/sensitive information and personal data unless expressly permitted. They also state that session/error metrics are collected and that User Content and Generated Content may be collected to improve NVIDIA products/services, including AI models, plus security/fraud/abuse monitoring.

Therefore NVIDIA NIM trial access is not eligible for PRIVATE/unreleased GAME data under P-03.

## 6. Trial/free entitlement and quota policy

Current evidence:

- exact model page lists `Free Endpoint - Available`;
- NVIDIA Developer Program/FAQ describes free hosted NIM API access for prototyping/testing;
- API Catalog trial rate limits vary by model and concurrent load;
- effective limits must be checked from the account UI.

GAME must not invent a permanent free RPM/RPD entitlement.

Initial future V-03 smoke ceilings proposed by P-03:

- maximum real requests: 3;
- concurrency: 1;
- automatic retries: 0;
- timeout: 60 seconds maximum;
- GAME input ceiling: 32,768 tokens;
- requested output ceiling: 16,384 tokens;
- streaming: disabled;
- tools: disabled;
- automatic model fallback: disabled;
- automatic provider fallback: disabled until STUDIO-009E.

Before each connected smoke, current free/trial eligibility and account-visible limits must be re-verified. If free access is absent/exhausted/uncertain, requires billing/subscription, or cannot be proven, fail closed.

HTTP 429/capacity/limit failure does not authorize retry escalation, payment, alternate model, or alternate endpoint.

## 7. Budget

Provider: NVIDIA-hosted NIM API Catalog

Currency: USD

Time window: all STUDIO-009P-03 and later V-03 work until amended

Monetary ceiling: integer zero

Authorized class: no-cost Developer Program/API Catalog trial for internal testing/evaluation only.

Forbidden: paid subscription, chargeable partner endpoint, paid cloud deployment, purchased credits, auto-recharge, paid fallback, billable request, and production use under trial authority.

If exact endpoint/model requires payment or production subscription, mark provider ineligible. No automated upgrade.

## 8. Failure normalization

Future adapter must safely normalize at minimum:

- HTTP 429 -> rate-limit/capacity fail-closed state;
- HTTP 401/403 -> authentication/authorization failure without secret echo;
- HTTP 422 -> request validation failure;
- HTTP 500 -> provider execution failure;
- timeout/abort -> fail closed;
- malformed response -> fail closed;
- unexpected redirect/host -> fail closed;
- model mismatch -> fail closed;
- missing free/trial eligibility -> `ZERO_COST_ELIGIBILITY_UNPROVEN`;
- billing/subscription required -> `PAID_PATH_REQUIRED`.

No error authorizes automatic retry, paid upgrade, model/endpoint substitution, or scope broadening.

## 9. Identity verification

A later V-03 evidence packet must verify:

- accepted provider profile ID;
- exact model `deepseek-ai/deepseek-v4-pro-0813`;
- exact host `integrate.api.nvidia.com`;
- exact `/v1/chat/completions` path;
- opaque credential lineage;
- current Free Endpoint / Developer Program trial eligibility;
- trial-only boundary;
- bounded request count;
- safe response/transport metadata sufficient for identity evidence;
- observed billable spend remains USD 0.

Provider-generated text never proves identity or billing state.

## 10. Kill switch, revocation and rollback

Studio Owner retains pause/revoke authority.

Credential revocation, identity mismatch, endpoint/model deprecation, free/trial uncertainty, billing requirement, data-policy failure, unexpected host, secret exposure, nonzero spend, or incompatible terms change makes the provider ineligible.

Rollback remains STUDIO-007F/STUDIO-008 MANUAL/FAKE. Groq/Cloudflare remain separately governed; P-03 does not auto-fail over to them.

## 11. Two-human operating compatibility

GAME is operated by two humans, but this child does not rewrite Studio Owner governance.

- only one active writer branch/claim may modify P-03 authoritative paths;
- the second human may perform read-only provider research/review while P-03 write work is active;
- no parallel P-03 implementation writer branch;
- raw credentials are never shared through Git/chat/task memory/screenshots/committed files;
- P-04/P-05 research may be read-only, but P-03 creates no P-04/P-05 authority;
- provider/model role stays benchmark-driven and is not hard-coded to a worker role.

Any two-person approval/merge/budget/canon authority change requires separate governance amendment.

## 12. Incident response

Fail closed on suspected key exposure, host/model mismatch, nonzero cost, account/trial uncertainty, data-policy violation, malformed output, outage/rate limit, unauthorized tool request, or terms/license change. Preserve only safe evidence; never raw credentials or confidential prompt/output content.

## 13. Offline implementation dependency

Merging P-03 authorizes only bounded offline/synthetic implementation in `tasks/STUDIO-009P-03-IMPLEMENTATION.md`.

Offline implementation must create deterministic policy/config artifacts, synthetic fixtures, adapter validation and tests without provider/network/account/credential/model/tool/routing/spend activity.

## 14. Tests and acceptance

Offline implementation must test exact provider/model identity, unapproved model rejection, host/path/redirect rejection, credential-ref mismatch, PUBLIC/synthetic-only data policy, PRIVATE/confidential/personal-data rejection, nonzero budget rejection, unproven quota fail-closed behavior, malformed/timeout/error normalization, tool rejection, kill switch, MANUAL/FAKE rollback, immutable input, and zero runtime provider activity.

Acceptance requires contract merge before implementation, exact path scope, retained regression suite, independent QA PASS, Review and Integration APPROVE, zero blockers, Rules CI success, separate Owner merge, and memory-only closeout.

## 15. Connected-validation dependency

P-03 merge/offline completion do NOT activate NVIDIA NIM.

A separate `STUDIO-009V-03` contract must merge before any NVIDIA account/key resolution, HTTPS request, model call or quota consumption.

V-03 cannot grant automatic routing, persistent worker authority, production use, private-data export, tool execution, merge/deploy/publish authority, or nonzero spend.

Automatic routing/failover remains STUDIO-009E. Full connected multi-provider acceptance remains STUDIO-009F.