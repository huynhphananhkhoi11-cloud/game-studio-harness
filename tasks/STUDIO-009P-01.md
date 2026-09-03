# STUDIO-009P-01 â€” Groq provider child contract

Status: ACCEPTED â€” CONTRACT ONLY â€” IMPLEMENTATION NOT STARTED

Parent: `tasks/STUDIO-009D.md`

Provider product: GroqCloud / Groq API

Primary owner: Studio Owner

Cost class: ZERO_COST_ONLY

Connected authority: NONE

## Goal

Define the first real-provider child contract for GAME using GroqCloud while preserving the provider-neutral STUDIO-009D boundary. This contract records provider/model/endpoint/auth/data/quota/budget and rollback policy only. It does not connect to Groq, resolve a credential, call a model, enable a built-in tool, route work, or spend money.

## 1. Provider identity

Authoritative product identity: GroqCloud and Groq APIs under the current Groq Services Agreement.

For customers domiciled in Asia under the Groq Services Agreement last modified 2026-06-22, the contracting party is Groq LLC. Connected activation must re-verify the effective contracting party from accepted account domicile and current terms before use.

Authoritative sources:

- https://console.groq.com/docs/legal/services-agreement
- https://console.groq.com/docs/models
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/rate-limits
- https://console.groq.com/docs/your-data
- https://console.groq.com/docs/tool-use/local-tool-calling

Provider profile lineage is reserved as `provider-profile:groq-free-gpt-oss-120b`. Runtime identity must later be proven from accepted configuration plus TLS/HTTP transport metadata; model-generated text is never identity evidence.

## 2. Model identity and version policy

The only model allowed by this first child is exact model ID:

- `openai/gpt-oss-120b`

No alias such as `latest`, no model supplied by a caller, and no second model is allowed. Adding another Groq model requires a later contract amendment or child contract.

Declared capabilities are limited to text generation, reasoning, JSON object/schema output, and provider-returned local function-call requests. Groq built-in browser search, built-in code execution, Compound systems, remote MCP, audio, batch, fine-tuning, LoRA, and any undeclared capability are out of scope.

## 3. Endpoint, host, and transport allowlist

The only provider API base allowed for a future connected phase is:

- scheme: `https`
- host: `api.groq.com`
- base path: `/openai/v1`
- canonical base URL: `https://api.groq.com/openai/v1`

Arbitrary host overrides, redirects to a different host, caller-supplied base URLs, model-supplied endpoints, proxies that change provider identity, HTTP plaintext, WebSocket, gRPC, browser automation, and server-side tool transports are forbidden.

STUDIO-009P-01 implementation itself must not create network transport. Real TLS/HTTP transport remains gated by STUDIO-009F.

## 4. Authentication and credential lineage

Future authentication mechanism: Groq API key carried only as an Authorization bearer credential by an approved transport implementation.

Reserved STUDIO-009C lineage identifier: `credential-profile:groq-api-key`.

The reference does not prove that a real credential exists. Provider eligibility must remain false until a separately approved credential profile/evidence exists. No API key value may appear in repository files, prompts, model output, traces, evidence, logs, exceptions, memory, URLs, screenshots, clipboard automation, or command lines.

This contract does not authorize key creation, enrollment, storage, lease, lookup, rotation, or resolution.

## 5. Capability map

For `openai/gpt-oss-120b`, the maximum declared capability set is:

- `TEXT_GENERATION`
- `REASONING`
- `STRUCTURED_OUTPUT`
- `LOCAL_TOOL_REQUEST`

`LOCAL_TOOL_REQUEST` means the model may later return a structured function-call request. GAME remains solely responsible for allowlisting, validating, denying, or executing any tool. No tool execution is authorized by this child contract.

## 6. Data export, retention, and training policy

Initial connected-pilot data classifications are restricted to `PUBLIC` and synthetic test data only. PRIVATE canon, secrets, credentials, unreleased assets, personal data, confidential project material, and higher classifications are denied until a later Owner decision.

Groq documentation states that inference customer data is not retained by default except limited feature/reliability/abuse circumstances and that Zero Data Retention can be enabled in Data Controls. Before any STUDIO-009F connected pilot, ZDR must be verified enabled for the relevant organization/account and evidence must be recorded without exposing secrets.

If ZDR cannot be verified, the provider remains ineligible for GAME connected execution under this child.

## 7. Quota, rate, timeout, and retry limits

At contract verification time, Groq Free Plan documents `openai/gpt-oss-120b` at:

- 30 requests/minute (RPM)
- 1,000 requests/day (RPD)
- 8,000 tokens/minute (TPM)
- 200,000 tokens/day (TPD)

These are evidence snapshots, not permanent entitlements. Effective GAME ceilings are the lower of the contract ceiling and the current provider/account limit. If the model is removed from Free Plan or the account requires paid billing, eligibility fails closed.

Future implementation must parse rate-limit headers deterministically and normalize 429 responses. Contract ceilings for the first pilot are stricter than provider maxima: concurrency 1, retry count 0 by default, request timeout maximum 60 seconds, maximum input context 32,768 tokens, maximum requested output 8,192 tokens. Any increase requires separate Owner acceptance.

## 8. Budget

Provider: GroqCloud
Currency: USD
Time window: all STUDIO-009P-01 implementation and pilot work until amended
Monetary ceiling: integer zero

No paid Developer plan, purchased credits, auto-recharge, auto-upgrade, pay-as-you-go fallback, or chargeable fallback is authorized. Promotional credit does not broaden authority. If a request would create a charge or requires a billing upgrade, GAME must block the request and fall back to another separately eligible zero-cost path or MANUAL/FAKE.

## 9. Identity verification

Future connected evidence must verify:

- accepted provider profile ID;
- exact model ID `openai/gpt-oss-120b`;
- exact HTTPS host `api.groq.com` and base path `/openai/v1`;
- accepted credential-profile lineage by opaque digest/reference only;
- normalized response metadata and rate-limit headers;
- no redirect or endpoint broadening.

Response prose may never prove provider/model identity.

## 10. Kill switch, pause, and revocation

Studio Owner controls provider pause/revoke. Credential revocation, identity mismatch, paid-only transition, cost anomaly, data-policy failure, unexpected host, or ZDR failure immediately makes the Groq profile ineligible. Resume requires fresh accepted evidence and Owner disposition; stale approvals cannot override revocation.

## 11. Incident response

Fail closed and preserve safe evidence on:

- suspected secret exposure;
- unexpected host/redirect;
- provider/model identity mismatch;
- unauthorized built-in or remote tool request;
- nonzero cost or billing requirement;
- quota anomaly or repeated 429;
- data-retention/ZDR policy mismatch;
- malformed or unsafe provider output;
- provider outage.

Incident records must never contain credential values or unredacted sensitive prompt/output content.

## 12. MANUAL/FAKE rollback

The accepted STUDIO-007F/STUDIO-008 MANUAL/FAKE path remains the no-network regression oracle and mandatory rollback. Groq failure never blocks safe operation of the harness.

## 13. Tests

Provider-specific implementation must use synthetic fixtures first and test at minimum:

- exact provider/model identity;
- unapproved model rejection;
- host/redirect broadening rejection;
- credential-reference mismatch;
- PUBLIC/synthetic-only data policy;
- nonzero budget rejection;
- quota header normalization and 429 handling;
- timeout/refusal/malformed output;
- built-in/remote tool rejection;
- local tool-request envelope without executing tools;
- pause/revocation/kill switch;
- MANUAL/FAKE rollback;
- no network/provider/credential runtime activity.

The retained baseline is 323 focused tests and 720 total tests before STUDIO-009P-01 implementation adds coverage.

## 14. QA and Review

Require independent QA PASS, Review and Integration APPROVE, zero blocking findings, Rules CI success on immutable heads, and a separate Studio Owner merge decision. Contract merge, implementation merge, and closeout are separate checkpoints.

## 15. Connected activation dependency

Merging this child contract or its future offline/synthetic implementation DOES NOT activate Groq. Live authentication, API-key resolution, HTTPS transport, model calls, tool calls, connected execution, and any spend remain gated by STUDIO-009F. STUDIO-009E governs routing/failover policy where applicable.