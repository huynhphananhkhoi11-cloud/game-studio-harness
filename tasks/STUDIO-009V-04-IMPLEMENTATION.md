# STUDIO-009V-04-IMPLEMENTATION — Poolside bounded live transport and connected smoke

## Authorization

Status: APPROVED SCOPE — NOT EXECUTABLE UNTIL STUDIO-009V-04 CONTRACT MERGE

Parent contract: `tasks/STUDIO-009V-04.md`

Provider child: `STUDIO-009P-04`

Provider profile: `provider-profile:poolside-direct-laguna-s-2.1`

Model: `poolside/laguna-s-2.1`

Money ceiling: 0 USD

This file defines future implementation scope only. This contract PR performs no Poolside/provider/account/API-key/model/network/CLI/tool/MCP/ACP/routing activity.

## 1. Exact cumulative implementation scope

Only these provider/live/code/test paths may be materially modified or created by the later V-04 implementation:

1. `platform/connectivity/providers/poolside/README.md`
2. `platform/connectivity/providers/poolside/data-policy.json`
3. `platform/connectivity/providers/poolside/quota-policy.json`
4. `platform/connectivity/providers/poolside/budget-policy.json`
5. `platform/connectivity/providers/poolside/transport-policy.json`
6. `platform/connectivity/providers/poolside/live-validation-policy.json`
7. `scripts/poolside_adapter.py`
8. `scripts/poolside_live_transport.py`
9. `scripts/poolside_live_smoke.py`
10. `scripts/poolside_session_credential_bridge.py`
11. `platform/connectivity/live/evidence/009v04/README.md`
12. `platform/connectivity/live/evidence/009v04/provider-live-state.json`
13. `platform/connectivity/live/evidence/009v04/connected-validation.json`
14. `platform/connectivity/live/evidence/009v04/quality-evaluation.json`
15. `tests/test_poolside_provider_adapter.py`
16. `tests/test_poolside_live_transport.py`
17. `tests/test_poolside_live_smoke.py`
18. `tests/test_poolside_session_credential_bridge.py`

Only these four V-04 memory files may additionally update:

- `studio/memory/tasks/STUDIO-009V-04/TASK.md`
- `studio/memory/tasks/STUDIO-009V-04/STATE.md`
- `studio/memory/tasks/STUDIO-009V-04/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009V-04/RESUME.md`

Maximum cumulative V-04 implementation PR scope: 22 unique paths.

No generic router, GitHub connector, Groq/Cloudflare/NVIDIA provider code, Unity/game code, dependency file, workflow, third-party gateway or unrelated provider is authorized.

## 2. Provider-specific reconciliation

Implementation may reconcile only Poolside P-04 provider-specific fields required for V-04 validation.

Maximum promotion is `LIVE_VALIDATED`.

STUDIO-009E remains automatic routing/failover authority.
STUDIO-009F remains full connected studio acceptance.
Historical P-04 evidence remains historical and must not be rewritten.

## 3. Trusted direct transport

Implement direct standard-library HTTPS/TLS transport to:

`https://inference.poolside.ai/v1/chat/completions`

Requirements:

- exact HTTPS;
- exact host `inference.poolside.ai`;
- exact path `/v1/chat/completions`;
- exact model `poolside/laguna-s-2.1`;
- no redirect;
- no arbitrary host/path/model override;
- no gateway;
- no enterprise/deployment endpoint;
- no local/self-hosted endpoint;
- concurrency 1;
- retry 0;
- timeout <=60 seconds;
- first-campaign input estimate <=4096 tokens;
- request body <=32768 bytes;
- response read <=131072 bytes;
- completion <=1024 tokens;
- streaming false;
- tools/functions absent;
- safe Content-Type handling;
- raw provider body absent from public exceptions.

## 4. Dedicated Poolside session credential bridge

Add `scripts/poolside_session_credential_bridge.py`.

The bridge must:

- bind exactly `credential-profile:poolside-api-key`;
- bind exactly `account-ref:poolside-owner-account`;
- accept raw key only from hidden Owner-interactive local input after connected preflight;
- keep raw key in memory only for the bounded campaign;
- prohibit `.env`, ambient env lookup, CLI argument, credential-file read, Poolside CLI, browser extraction, keychain automation, clipboard automation and remote secret store;
- never log, return, serialize, persist or expose raw key;
- support synthetic suppliers only in deterministic tests.

## 5. Bounded smoke ledger

One Owner-authorized campaign:

- max 3 requests;
- concurrency 1;
- retry 0;
- input estimate <=4096 tokens/request;
- completion <=1024 tokens/request;
- request body <=32768 bytes;
- response read <=131072 bytes;
- money ceiling 0.

Every request is reserved before network I/O. Failed requests consume reservations. Unsafe failure ends the campaign.

## 6. Provider-specific hostile tests

Before real request, deterministic tests must cover at minimum:

- exact host/path/model;
- redirect rejected;
- gateway/enterprise/local endpoint rejected;
- API key never logged/serialized/returned;
- no env/CLI/file/keychain/clipboard secret lookup;
- 401/403/404/422/429/3xx/5xx normalization;
- timeout;
- oversized request/response;
- malformed JSON/Unicode;
- provider error-body redaction;
- wrong model identity;
- request count <=3;
- concurrency rejection;
- retry remains zero;
- tool/function rejection;
- MCP/ACP/shell/file/browser/URL/repository-write rejection;
- missing zero-cost eligibility fails closed;
- billing/subscription/payment path fails closed;
- server-side revocation path unproven fails closed;
- Terms/data-policy drift fails closed;
- MANUAL/FAKE rollback remains available.

## 7. Owner connected preflight

Before raw key materialization or real request, Owner must confirm current Poolside state:

- exact direct model/endpoint still available;
- account-level no-cost eligibility for the bounded campaign;
- no mandatory billing/payment/subscription;
- a server-side key revoke/delete/invalidate path;
- current Terms/data policy remain compatible;
- no gateway/enterprise/local route selected;
- no paid fallback.

If ambiguous, do not create/input/use the key.

## 8. Post-smoke gates

After the bounded smoke:

1. materialize only sanitized identity/transport/request/usage/quality evidence;
2. Owner confirms observed monetary charge remains USD 0;
3. Connected QA reviews immutable smoke evidence;
4. Connected Review/Integration reviews immutable QA head;
5. validation key is revoked/deleted/invalidated server-side and safe evidence recorded;
6. Owner records final disposition;
7. promotion ceiling remains `LIVE_VALIDATED`;
8. implementation PR remains separate from Owner merge;
9. V-04 closeout remains separate after implementation merge.

No successful smoke may be re-run without fresh Owner authorization.

## 9. Acceptance

Implementation must preserve the retained baseline tests and add Poolside-specific live transport, smoke, credential bridge and hostile tests.

No real provider request occurs merely to make tests pass.

<!-- STUDIO-009V-04-CONTRACT-CHECKPOINT-0001 -->
