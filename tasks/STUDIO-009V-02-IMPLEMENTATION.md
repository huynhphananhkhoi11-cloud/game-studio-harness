# STUDIO-009V-02-IMPLEMENTATION — Cloudflare bounded live transport and connected smoke

## Authorization

Status: APPROVED SCOPE — NOT EXECUTABLE UNTIL STUDIO-009V-02 CONTRACT MERGE

Parent contract: `tasks/STUDIO-009V-02.md`

Provider child: `STUDIO-009P-02`

Provider profile: `provider-profile:cloudflare-workers-ai-free-nemotron-3-super`

Model: `@cf/nvidia/nemotron-3-120b-a12b`

Money ceiling: 0 USD

This file defines future implementation scope only. This contract PR performs no Cloudflare/provider/account/token/model call.

## 1. Exact cumulative implementation scope

Only these provider/live/code/test paths may be materially modified or created by the later V-02 implementation:

1. `platform/connectivity/providers/cloudflare-workers-ai/README.md`
2. `platform/connectivity/providers/cloudflare-workers-ai/data-policy.json`
3. `platform/connectivity/providers/cloudflare-workers-ai/quota-policy.json`
4. `platform/connectivity/providers/cloudflare-workers-ai/budget-policy.json`
5. `platform/connectivity/providers/cloudflare-workers-ai/transport-policy.json`
6. `platform/connectivity/providers/cloudflare-workers-ai/live-validation-policy.json`
7. `scripts/cloudflare_workers_ai_adapter.py`
8. `scripts/cloudflare_live_transport.py`
9. `scripts/cloudflare_live_smoke.py`
10. `platform/connectivity/live/evidence/009v02/README.md`
11. `platform/connectivity/live/evidence/009v02/provider-live-state.json`
12. `platform/connectivity/live/evidence/009v02/connected-validation.json`
13. `platform/connectivity/live/evidence/009v02/quality-evaluation.json`
14. `tests/test_cloudflare_provider_adapter.py`
15. `tests/test_cloudflare_live_transport.py`
16. `tests/test_cloudflare_live_smoke.py`

Only these four task-memory files may additionally update:

- `studio/memory/tasks/STUDIO-009V-02/TASK.md`
- `studio/memory/tasks/STUDIO-009V-02/STATE.md`
- `studio/memory/tasks/STUDIO-009V-02/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009V-02/RESUME.md`

Maximum cumulative implementation PR scope: 20 unique paths.

No generic router, AI Gateway configuration, GitHub connector, Unity/game code, dependency file, workflow or unrelated provider is authorized.

## 2. Legacy-policy reconciliation

The implementation must explicitly reconcile Cloudflare P-02 historical `STUDIO-009F_ONLY` activation values to V-02 validation authority without rewriting historical evidence semantics.

Provider-specific live validation becomes `STUDIO-009V-02_ONLY`.

STUDIO-009E remains automatic routing/failover authority.

STUDIO-009F remains full connected studio acceptance.

## 3. Trusted transport

Implement direct standard-library HTTPS/TLS transport to:

`https://api.cloudflare.com/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1/chat/completions`

Requirements:

- exact HTTPS host;
- accepted account identifier supplied only after Owner preflight;
- exact model `@cf/nvidia/nemotron-3-120b-a12b`;
- no redirect;
- no proxy/base-url override;
- no AI Gateway header or route;
- no arbitrary account/model override;
- concurrency 1;
- retry 0;
- timeout <=30s;
- request <=8192 bytes;
- response read <=65536 bytes;
- completion <=256 tokens;
- safe Content-Type handling;
- provider body absent from public exceptions.

## 4. Session account/token handoff

Reuse the accepted provider-neutral session credential bridge for the API token without ambient secret lookup.

The Cloudflare-specific smoke may collect the Account ID through an Owner-interactive local input only after preflight, but it must not persist or print the raw Account ID.

Tests use synthetic account/token suppliers only.

No `.env`, environment variable, CLI argument, filesystem key cache, browser extraction, keychain or remote secret store is authorized for V-02.

## 5. Bounded smoke ledger

A durable local ledger must reserve each real request before network I/O.

One Owner-authorized campaign:

- max 3 requests;
- concurrency 1;
- retry 0;
- campaign neuron ceiling 2,000;
- daily GAME ceiling 8,000;
- money ceiling 0.

Any unsafe failure stops the campaign.

## 6. Provider-specific hostile tests

Before any real request, deterministic tests must cover at minimum:

- exact host/base-path/account path/model;
- account ID not persisted or printed;
- token never logged/serialized/returned;
- no environment/CLI/file secret lookup;
- no AI Gateway route/header;
- no storage/logging/caching broadening;
- 401/403/429/3xx/5xx normalization;
- Cloudflare `3036`, `3040`, `5035`;
- timeout;
- oversized request/response;
- malformed JSON/Unicode;
- provider error-body redaction;
- wrong model identity;
- request counter <=3;
- neuron campaign ceiling;
- concurrency rejection;
- retry remains zero;
- tool/function-call rejection;
- paid-plan-required fail closed;
- MANUAL/FAKE rollback remains available.

## 7. Owner connected preflight

Before credential/account materialization, Owner must confirm current Cloudflare state:

- Workers Free suitable for Workers AI;
- exact model remains free-eligible;
- current free-neuron headroom is sufficient;
- no Workers Paid path;
- no prepaid AI Gateway credits;
- no Unified Billing;
- API token permission configuration follows current official Workers AI guidance;
- no paid fallback.

If ambiguous, do not request the token or Account ID.

## 8. Post-smoke evidence and gates

After the bounded smoke:

1. materialize sanitized request/model/transport/quality evidence;
2. Owner separately confirms neuron usage and billable charge;
3. Connected QA independently reviews immutable evidence;
4. Connected Review and Integration independently reviews immutable QA head;
5. temporary V-02 token is revoked/deleted;
6. Owner records final disposition;
7. promotion ceiling is `LIVE_VALIDATED`;
8. implementation PR remains separate from Owner merge;
9. closeout remains separate after implementation merge.

No later stage may re-run the successful smoke without fresh Owner authorization.

## 9. Acceptance tests

The implementation must preserve the current baseline and add provider-specific live tests without reducing retained coverage. Exact counts are determined by the implementation contract checkpoint and then frozen for QA/Review.

No real provider request occurs merely to make tests pass.

<!-- STUDIO-009V-02-CONTRACT-CHECKPOINT-0001 -->
