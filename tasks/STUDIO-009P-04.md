# STUDIO-009P-04 - Poolside direct Laguna S 2.1 provider child contract

Status: ACCEPTED SCOPE - CONTRACT ONLY - IMPLEMENTATION NOT STARTED

Parent: `tasks/STUDIO-009D.md`

Provider product: Poolside standalone hosted inference API

Selected model candidate: `poolside/laguna-s-2.1`

Primary owner: Studio Owner

Cost class: ZERO_COST_ONLY

Usage class: INTERNAL_TESTING_EVALUATION_ONLY

Connected authority: NONE

## Goal

Define the fourth real-provider child contract for GAME using Poolside's direct hosted inference endpoint with exact model `poolside/laguna-s-2.1`.

This contract records provider/model/transport/authentication/data/quota/budget/failure/rollback policy only. It does not create a Poolside account or API key, call Poolside or Laguna, install or execute the `pool` CLI, execute a model/tool, enable routing, create a persistent worker, export private GAME content, or spend money.

STUDIO-009V-03 NVIDIA connected validation remains frozen at account verification and is not modified or resumed by P-04. P-04 becomes the next authoritative provider write track only because the durable V-03 freeze checkpoint explicitly permits `STUDIO-009P-04_CONTRACT`.

## 1. Provider identity and authoritative sources

Authoritative provider-facing product for this child: Poolside standalone cloud inference exposed from the current public Poolside model page.

Authoritative sources re-verified for this contract on 2026-09-09:

- https://poolside.ai/models
- https://poolside.ai/blog/introducing-laguna-s-2-1
- https://platform.poolside.ai/
- https://docs.poolside.ai/cli/install
- https://docs.poolside.ai/cli/cli-reference
- https://poolside.ai/legal/eula
- https://poolside.ai/legal/acceptable-use-policy
- https://poolside.ai/legal/privacy

Provider profile lineage:

`provider-profile:poolside-direct-laguna-s-2.1`

Reserved credential lineage:

`credential-profile:poolside-api-key`

Reserved account reference:

`account-ref:poolside-owner-account`

These references are metadata only and do not prove that an account, entitlement, or credential exists.

Current public Poolside model evidence states that Laguna S 2.1 is free to use for a limited time through Poolside's OpenAI-compatible chat API. Free-for-limited-time is dynamic availability evidence, not a permanent free entitlement.

## 2. Exact model identity and version policy

Only exact model ID:

`poolside/laguna-s-2.1`

No `latest`, provider-selected substitute, Laguna M.1, Laguna XS 2.1, OpenRouter alias, third-party alias, automatic migration, or caller-supplied model.

Current official model evidence records:

- Laguna S 2.1;
- 118B total parameters;
- 8B activated parameters per token;
- Mixture-of-Experts architecture;
- model support up to 1M context;
- agentic coding and long-horizon work focus;
- thinking and no-thinking modes;
- max thinking enabled by default in Poolside's release description;
- no public low/medium/high effort control in the release description;
- OpenAI-compatible chat API.

The 1M model context is evidence, not a GAME request allowance and not proof that every free hosted route exposes the full 1M window. V-04 must verify actual direct-endpoint/account limits before connected execution.

Declared provider-neutral capabilities for the initial P-04 child:

- `TEXT_GENERATION`
- `REASONING`

Coding/software-engineering is a workload class to benchmark later, not automatic worker authority.

Although Laguna is trained for agentic coding and Poolside offers tool-capable harnesses, P-04 authorizes no tool calls, shell, file access, code execution, browser, MCP, ACP, repository mutation, external action, or agent loop.

## 3. Exact transport allowlist

Future connected transport candidate for this child:

- scheme: `https`
- host: `inference.poolside.ai`
- base path: `/v1`
- chat endpoint: `/v1/chat/completions`
- canonical base URL: `https://inference.poolside.ai/v1`

This identity follows Poolside's current standalone public model example using the OpenAI client with base URL `https://inference.poolside.ai/v1` and model `poolside/laguna-s-2.1`.

Explicitly out of scope:

- tenant/on-premise Poolside deployment endpoints such as deployment-specific `/openai/v1`;
- OpenRouter;
- Baseten;
- Vercel AI Gateway;
- Kilo;
- any other gateway/aggregator;
- local/self-hosted Laguna weights;
- HTTP plaintext;
- arbitrary host/path override;
- redirect to another host;
- browser automation;
- WebSocket/gRPC;
- provider-selected endpoint substitution.

P-04 implementation remains offline/synthetic. Real HTTPS activity requires a separately merged `STUDIO-009V-04` connected-validation contract.

## 4. Authentication and credential boundary

Future standalone authentication candidate: Poolside API key used as Bearer authentication only through an approved direct transport.

Reserved credential profile:

`credential-profile:poolside-api-key`

Reserved account reference:

`account-ref:poolside-owner-account`

P-04 authorizes no Poolside account creation, login, API-key creation/display/copy/storage/lookup/lease/rotation/revocation, environment-variable lookup, keychain lookup, browser credential extraction, or credential-file access.

No raw key may appear in repository files, Git history, prompts, model outputs, traces, evidence, screenshots, memory, URLs, command lines, stdout/stderr, exceptions, or clipboard automation.

Poolside documentation states that the `pool` CLI can store credentials in `~/.config/poolside/credentials.json` and can also resolve `POOLSIDE_API_KEY`/`POOLSIDE_TOKEN`. Therefore the initial P-04/V-04 path must not install or use `pool` for authentication or execution. A later separate harness evaluation may consider `pool` only under explicit authority.

## 5. Data, retention and training boundary

Initial future connected-validation data is restricted to:

- `PUBLIC`;
- synthetic prompts created only for validation.

Forbidden:

- PRIVATE project canon;
- unreleased GDD/game content;
- proprietary source code not separately approved for export;
- credentials/secrets;
- confidential or sensitive information;
- personal data;
- regulated payment/health/government-ID data;
- unreleased assets;
- data without submission rights.

Poolside Terms of Use state that Content may be used to provide, maintain, improve and develop Poolside offerings, including model training, unless the user opts out. Direct Site users may use Training Opt-Out in User Settings. The Terms also state that Feedback-linked or safety-review content may still be used in specified cases.

Therefore P-04 remains PUBLIC/SYNTHETIC-only whether or not an account later enables Training Opt-Out. Enabling opt-out does not broaden GAME data authority. Initial connected validation must not submit feedback/ratings.

## 6. Free entitlement, quota and dynamic-limit policy

Current official public evidence:

- Laguna S 2.1 is described as `Free to use for a limited time`;
- standalone API key access is offered through Poolside's platform;
- no permanent GAME-specific RPM/RPD/token quota is established by this contract;
- Poolside Terms allow fees for certain Products/features and fee changes.

GAME must not infer unlimited or permanent free access.

A later V-04 connected preflight must prove current account-level zero-cost eligibility before key creation/input or any request. If free access is absent, expired, exhausted, unclear, requires payment/billing/subscription, or cannot be proven, fail closed.

Proposed maximum first-campaign envelope for later V-04:

- maximum real requests: 3;
- concurrency: 1;
- automatic retries: 0;
- timeout: 60 seconds maximum;
- estimated input: <= 4,096 tokens/request;
- requested completion: <= 1,024 tokens/request;
- request body: <= 32,768 bytes;
- response body: <= 131,072 bytes;
- streaming: disabled;
- tools/functions: disabled;
- MCP/ACP: disabled;
- shell/code/file/browser/URL execution: disabled;
- automatic provider/model fallback: disabled;
- monetary ceiling: USD 0.

V-04 may tighten these limits. Any broadening requires explicit accepted authority.

## 7. Budget

Provider: Poolside standalone hosted inference API

Currency: USD

Time window: all STUDIO-009P-04 and later V-04 work until amended

Monetary ceiling: integer zero

Authorized class: only a currently provable no-cost Poolside hosted route for bounded internal testing/evaluation.

Forbidden:

- paid endpoint;
- subscription purchase;
- credit purchase;
- billing-method requirement for the bounded GAME campaign;
- auto-recharge;
- third-party paid gateway;
- paid fallback;
- billable request;
- self-hosted infrastructure spend attributed to P-04;
- production use under this authority.

If the exact direct endpoint/model requires payment or zero-cost status cannot be proven, mark connected validation ineligible.

## 8. Failure normalization

Future adapter/live transport must safely normalize at minimum:

- HTTP 401/403 -> authentication/authorization failure without secret echo;
- HTTP 404 -> endpoint/model not found, fail closed;
- HTTP 422 -> request validation failure;
- HTTP 429 -> rate-limit/capacity failure;
- HTTP 5xx -> provider execution failure;
- timeout/abort -> fail closed;
- malformed JSON/schema -> fail closed;
- unexpected redirect/host -> fail closed;
- exact model mismatch -> fail closed;
- unexpected external capability/tool output -> fail closed;
- missing current free eligibility -> `ZERO_COST_ELIGIBILITY_UNPROVEN`;
- billing/payment required -> `PAID_PATH_REQUIRED`;
- terms/data-policy drift -> fail closed.

No failure authorizes retry escalation, payment, alternate model, alternate endpoint, gateway substitution, tool activation, or scope broadening.

## 9. Identity and connected evidence

A later V-04 evidence packet must verify:

- accepted provider profile ID;
- exact model `poolside/laguna-s-2.1`;
- exact host `inference.poolside.ai`;
- exact `/v1/chat/completions` path;
- opaque credential lineage;
- current no-cost entitlement;
- bounded request count;
- allowed PUBLIC/SYNTHETIC data;
- safe transport/model metadata sufficient for identity;
- observed billable spend remains USD 0.

Model-generated prose is never provider/model/billing identity evidence.

## 10. Kill switch, credential revocation and rollback

Studio Owner retains pause/revoke authority.

Before any real V-04 request, an account-level key revocation/deletion path must be proven. Local CLI `logout` or deletion of a local credential file is not sufficient evidence of server-side key revocation.

Credential exposure, provider/model/endpoint mismatch, free-entitlement uncertainty, paid requirement, data-policy failure, terms drift, unexpected tool execution, or nonzero spend makes connected validation ineligible.

Rollback remains STUDIO-007F/STUDIO-008 MANUAL/FAKE. Groq, Cloudflare and frozen NVIDIA remain separately governed and are not automatic fallbacks.

## 11. Poolside CLI and agent-harness boundary

P-04 intentionally evaluates the model/provider separately from Poolside's agent harness.

The `pool` CLI can operate on repositories, files, terminal commands, tools, MCP servers, secrets, and stored credentials. None of those capabilities are authorized by this child.

P-04 and initial V-04 therefore use direct text-only API semantics only. This avoids conflating:

- model quality;
- Poolside agent-harness quality;
- tool permission behavior;
- repository mutation;
- credential persistence.

If GAME later wants to evaluate `pool`, that is a distinct harness/tool-capability task after provider/model evidence exists.

## 12. Model limitations relevant to later benchmark design

Poolside's Laguna S 2.1 release describes known limitations including:

- possible tool-schema overfitting in third-party harnesses;
- nested-tool argument formatting failures;
- longer-than-expected thinking/overthinking.

These are evidence for benchmark design, not grounds to reject the model now. Since P-04 tools are disabled, initial offline implementation must treat tool-capable behavior as denied. Later GAME-specific benchmark evidence decides whether Laguna S 2.1 fits coding, reasoning, review, or other roles.

No provider self-description directly assigns a GAME worker role.

## 13. Two-human operating compatibility

GAME is operated by two humans while preserving one authoritative writer track.

- only one writer branch/claim may modify P-04 authoritative paths;
- the second human may conduct read-only research/review;
- no parallel P-04 implementation writer branch;
- no parallel P-05 authoritative write branch while P-04 is active;
- V-03 remains frozen and receives no writes from P-04;
- raw credentials are never shared through Git/chat/task memory/screenshots/committed files;
- provider/model role remains benchmark-driven.

## 14. Incident response

Fail closed on suspected key exposure, host/model mismatch, nonzero cost, free-entitlement uncertainty, data-policy violation, malformed output, outage/rate limit, unexpected capability/tool output, or terms/license change.

Preserve only safe evidence. Never preserve raw credentials or confidential prompt/output content.

## 15. Offline implementation dependency

Merging P-04 authorizes only bounded offline/synthetic implementation in `tasks/STUDIO-009P-04-IMPLEMENTATION.md`.

Offline implementation must create deterministic policy/config artifacts, synthetic fixtures, adapter validation and tests without Poolside provider/network/account/credential/model/tool/routing/spend activity.

## 16. Tests and acceptance

Offline implementation must test exact provider/model identity, model substitution rejection, host/path/gateway rejection, credential-ref mismatch, PUBLIC/SYNTHETIC-only data policy, private/confidential/sensitive-data rejection, nonzero budget rejection, dynamic/free entitlement fail-closed behavior, malformed/timeout/error normalization, tool/CLI/harness rejection, kill switch, MANUAL/FAKE rollback, immutable input, and zero runtime provider activity.

Acceptance requires contract merge before implementation, exact path scope, retained regression suite, independent QA PASS, Review and Integration APPROVE, zero blockers, Rules CI success, separate Owner merge, and memory-only closeout.

## 17. Connected-validation dependency

P-04 contract merge/offline completion do NOT activate Poolside.

A separate `STUDIO-009V-04` contract must merge before any Poolside account/key resolution, HTTPS request, model call, quota consumption, or connected evidence.

V-04 cannot grant automatic routing, persistent worker authority, production use, private-data export, `pool` CLI execution, tool/MCP/ACP execution, merge/deploy/publish authority, or nonzero spend.

Automatic routing/failover remains STUDIO-009E. Full connected multi-provider acceptance remains STUDIO-009F.

<!-- STUDIO-009P-04-CONTRACT-CHECKPOINT-0001 -->
