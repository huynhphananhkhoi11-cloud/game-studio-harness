# STUDIO-009P-02 - Cloudflare Workers AI provider child contract

Status: ACCEPTED - CONTRACT ONLY - IMPLEMENTATION NOT STARTED

Parent: `tasks/STUDIO-009D.md`

Provider product: Cloudflare Workers AI

Primary owner: Studio Owner

Cost class: ZERO_COST_ONLY

Connected authority: NONE

## Goal

Define the second real-provider child contract for GAME using Cloudflare Workers AI with NVIDIA Nemotron 3 Super while preserving the provider-neutral STUDIO-009D boundary.

This contract records provider/model/endpoint/authentication/data/quota/budget/failure/rollback policy only. It does not create a Cloudflare account, discover an account ID, create or resolve an API token, call Workers AI, enable AI Gateway, execute a model or tool, route work, or spend money.

STUDIO-009P-01 Groq remains an independently accepted provider child. This child does not replace or broaden Groq authority.

## 1. Provider identity

Authoritative provider product: Cloudflare Workers AI.

Authoritative provider/model sources verified for this contract on 2026-09-03:

- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/workers-ai/platform/limits/
- https://developers.cloudflare.com/workers-ai/platform/errors/
- https://developers.cloudflare.com/workers-ai/platform/data-usage/
- https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/
- https://developers.cloudflare.com/workers-ai/get-started/rest-api/
- https://developers.cloudflare.com/workers-ai/models/nemotron-3-120b-a12b/
- https://developers.cloudflare.com/changelog/post/2026-07-28-models-require-workers-paid/

Provider profile lineage is reserved as:

`provider-profile:cloudflare-workers-ai-free-nemotron-3-super`

Runtime provider identity must later be proven from accepted configuration plus validated HTTPS transport metadata. Model-generated text is never provider identity evidence.

The first connected pilot under this child requires Workers Free eligibility. A paid Workers plan, prepaid AI Gateway credits, Unified Billing, or another chargeable path does not satisfy this zero-cost child unless a later Owner-approved amendment explicitly changes the budget contract.

## 2. Model identity and version policy

The only model allowed by this child is exact Cloudflare model ID:

`@cf/nvidia/nemotron-3-120b-a12b`

No `latest` alias, caller-supplied model, automatic model migration, second model, catalog fallback, or provider-selected substitute is allowed.

At contract verification time Cloudflare documents this model as:

- Cloudflare-hosted;
- text generation;
- reasoning supported;
- function calling supported;
- current model-page context window: 256,000 tokens.

The older 2026-03-11 Cloudflare launch changelog described a 32,000-token context window. Because provider documentation can evolve, the current model page is the contract snapshot, but STUDIO-009F must re-verify the exact model identity, current context specification, Free-plan eligibility, and applicable terms before any connected execution.

Declared GAME capability set is limited to:

- `TEXT_GENERATION`
- `REASONING`
- `LOCAL_TOOL_REQUEST`

`LOCAL_TOOL_REQUEST` means the provider may return a structured function-call request. GAME remains solely responsible for allowlisting, validating, denying, or executing any local tool. No tool execution is authorized by this child.

Embedding, image, audio, batch, fine-tuning, LoRA, AI Search, AI Gateway routing, third-party-provider routing, browser search, remote MCP, code execution, storage services, and undeclared capabilities are out of scope.

## 3. Endpoint, account, host, and transport allowlist

The only future connected transport selected by this child is the Cloudflare Workers AI OpenAI-compatible chat-completions endpoint.

Required transport identity:

- scheme: `https`
- host: `api.cloudflare.com`
- fixed prefix: `/client/v4/accounts/`
- accepted account identifier: resolved only from approved configuration at STUDIO-009F
- fixed suffix: `/ai/v1`
- chat endpoint: `/chat/completions`

Canonical future base URL template:

`https://api.cloudflare.com/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1`

The raw Cloudflare Account ID is not authorized to be hard-coded in repository files, prompts, model output, evidence prose, or memory. Runtime configuration may resolve it only after STUDIO-009F accepts the corresponding account identity evidence.

Arbitrary hosts, redirects to another host, caller/model-supplied account IDs or base URLs, `/ai-gateway/` routes, third-party provider routes, plaintext HTTP, WebSocket, gRPC, browser automation, and server-side tool transports are forbidden.

STUDIO-009P-02 implementation itself must not create network transport. Real HTTPS transport remains gated by STUDIO-009F.

## 4. Authentication and credential lineage

Future authentication mechanism: Cloudflare API token carried only as an Authorization bearer credential by an approved transport implementation.

Reserved STUDIO-009C lineage identifier:

`credential-profile:cloudflare-workers-ai-api-token`

Reserved account identity reference:

`account-ref:cloudflare-workers-ai-owner-account`

These references do not prove that a real account identifier or credential exists.

Cloudflare documentation currently instructs REST API users to use a Cloudflare Account ID and API token. Current documentation also requires Workers AI permissions; exact minimum permissions must be re-verified at activation time and unrelated permissions must not be granted merely for GAME.

No API-token value or raw account identifier may appear in repository files, prompts, model output, traces, evidence prose, logs, exceptions, memory, URLs, screenshots, clipboard automation, or command lines.

This contract does not authorize account discovery, API-token creation, enrollment, storage, lease, lookup, rotation, revocation calls, or resolution.

## 5. Data export, training, storage, and logging policy

Initial connected-pilot data classification is restricted to:

- `PUBLIC`
- synthetic test data

PRIVATE canon, credentials, secrets, unreleased assets, personal data, confidential project material, and higher classifications are denied under this child.

Cloudflare currently states that Workers AI Customer Content is owned by the customer, is not made available to other Cloudflare customers, and is not used to train Workers AI models or improve Cloudflare or third-party services without explicit consent.

Cloudflare also states that Customer Content may be stored when a storage service such as R2, KV, Durable Objects, or Vectorize is used with Workers AI. Therefore the first child forbids such storage paths.

AI Gateway logging, caching, analytics, Unified Billing, prepaid credits, and third-party provider routing are also out of scope for the first connected pilot.

If current data terms, storage behavior, model license, account configuration, or logging behavior cannot be verified before STUDIO-009F, this provider remains ineligible.

## 6. Free quota and operational ceilings

Cloudflare Workers AI currently documents:

- Workers Free allocation: 10,000 Neurons per day at no charge;
- reset: 00:00 UTC;
- further operations fail when the free allocation is exhausted;
- Workers Paid can bill usage above the free allocation;
- some models require a paid billing method.

At contract verification time, `@cf/nvidia/nemotron-3-120b-a12b` remains listed as available on Workers Free.

Current model unit conversion snapshot:

- 45,455 Neurons per 1,000,000 input tokens;
- 136,364 Neurons per 1,000,000 output tokens.

These are evidence snapshots, not permanent entitlements.

GAME ceilings for the first future connected pilot are stricter:

- account plan requirement: Workers Free;
- daily GAME ceiling: 8,000 Neurons;
- concurrency: 1;
- retry count: 0;
- request timeout maximum: 60 seconds;
- maximum input tokens requested/accepted by GAME: 16,384;
- maximum output tokens requested by GAME: 4,096;
- automatic quota increase: forbidden.

The 8,000-Neuron GAME ceiling intentionally leaves a safety margin below the current 10,000-Neuron provider free allocation.

If reliable quota/metering evidence is unavailable, the provider fails closed rather than assuming free capacity remains.

## 7. Error and failover policy

Provider-specific implementation must deterministically normalize at minimum:

- HTTP 429 / internal `3036`: free allocation exhausted -> `FREE_QUOTA_EXHAUSTED`;
- HTTP 429 / internal `3040`: out of capacity -> `CAPACITY_UNAVAILABLE`;
- HTTP 403 / internal `5035`: model requires Workers Paid -> `PAID_PLAN_REQUIRED`;
- invalid or missing model identity -> fail closed;
- timeout or aborted request -> fail closed;
- malformed response -> fail closed.

No condition above authorizes an automatic retry, paid upgrade, prepaid credit use, AI Gateway fallback, model substitution, or scope increase.

Eligible failover is only to another separately accepted zero-cost GAME provider through later STUDIO-009E policy, or to MANUAL/FAKE.

## 8. Budget

Provider: Cloudflare Workers AI

Currency: USD

Time window: all STUDIO-009P-02 implementation and pilot work until amended

Monetary ceiling: integer zero

Authorized billing class: Workers Free only

Forbidden:

- Workers Paid activation for this child;
- chargeable usage above free allocation;
- prepaid AI Gateway credits;
- Unified Billing;
- auto-recharge;
- auto-upgrade;
- paid-only models;
- promotional or prepaid credit as authority;
- chargeable third-party fallback.

If the selected model becomes paid-only, the account becomes unable to guarantee zero-cost execution, or a request would require payment, the provider becomes ineligible and GAME must fail closed.

## 9. Identity verification

Future connected evidence must verify:

- accepted provider profile ID;
- exact model ID `@cf/nvidia/nemotron-3-120b-a12b`;
- exact HTTPS host `api.cloudflare.com`;
- exact OpenAI-compatible Workers AI path template;
- accepted account identity reference by opaque evidence;
- accepted credential-profile lineage by opaque digest/reference only;
- Workers Free eligibility;
- model remains Free-plan eligible;
- current data and license terms;
- no redirect, AI Gateway, account, endpoint, or model broadening.

Response prose may never prove provider/model/account identity.

## 10. Kill switch, pause, and revocation

Studio Owner controls provider pause/revoke.

Any of the following immediately makes this profile ineligible:

- credential revocation or suspected exposure;
- account identity mismatch;
- provider/model identity mismatch;
- model deprecation/removal;
- model becomes paid-only;
- Workers Free eligibility cannot be proven;
- unexpected host/path/redirect;
- AI Gateway or billing broadening;
- quota anomaly;
- data-policy or model-license change;
- connected execution cannot prove monetary ceiling zero.

Resume requires fresh accepted evidence and Owner disposition. Stale approvals cannot override revocation or a paid-only transition.

## 11. Incident response

Fail closed and preserve safe evidence on:

- suspected secret or account-identifier exposure;
- unexpected host, account path, or redirect;
- provider/model identity mismatch;
- unauthorized tool request or execution;
- nonzero cost or billing requirement;
- free quota exhaustion;
- out-of-capacity response;
- model deprecation;
- data-policy or license mismatch;
- malformed or unsafe provider output;
- provider outage.

Incident records must never contain credential values, raw account identifiers, or unredacted sensitive prompt/output content.

## 12. MANUAL/FAKE rollback

The accepted STUDIO-007F/STUDIO-008 MANUAL/FAKE path remains the no-network regression oracle and mandatory rollback.

Cloudflare failure, quota exhaustion, capacity loss, paid-only transition, model removal, or account ineligibility must never block safe operation of the harness.

## 13. Tests

Provider-specific implementation must use synthetic fixtures first and test at minimum:

- exact provider/model identity;
- unapproved model rejection;
- model alias/substitution rejection;
- host/path/account broadening rejection;
- credential-reference and account-reference mismatch;
- PUBLIC/synthetic-only data policy;
- storage/AI-Gateway/billing broadening rejection;
- nonzero budget rejection;
- Workers Paid and prepaid-credit rejection;
- free quota ceiling behavior;
- `3036`, `3040`, and `5035` normalization;
- timeout/refusal/malformed output;
- local tool-request envelope without executing tools;
- pause/revocation/kill switch;
- model becomes paid-only/deprecated;
- MANUAL/FAKE rollback;
- no network/provider/credential/account-discovery runtime activity.

The retained post-STUDIO-009P-01 baseline is:

- 362 focused tests;
- 759 total tests.

## 14. QA and Review

Require:

- independent QA PASS;
- Review and Integration APPROVE;
- zero blocking findings;
- Rules CI success on immutable heads;
- separate Studio Owner merge decision.

Contract merge, offline implementation merge, and closeout remain separate checkpoints.

## 15. Connected activation dependency

Merging this child contract or its future offline/synthetic implementation DOES NOT activate Cloudflare Workers AI.

Live account-ID resolution, API-token resolution, HTTPS transport, Workers AI calls, model calls, tool calls, quota consumption, routing, connected execution, and any spend remain gated by STUDIO-009F.

STUDIO-009E governs future capability/quota/cost/data routing and failover where applicable.

Until STUDIO-009F explicitly accepts a connected pilot, provider state must remain disabled/ineligible for real execution.
