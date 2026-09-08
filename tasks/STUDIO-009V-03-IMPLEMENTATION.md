# STUDIO-009V-03-IMPLEMENTATION — NVIDIA NIM bounded live transport and connected smoke

## Authorization

Status: APPROVED SCOPE — NOT EXECUTABLE UNTIL STUDIO-009V-03 CONTRACT MERGE

Parent contract: `tasks/STUDIO-009V-03.md`

Provider child: `STUDIO-009P-03`

Provider profile: `provider-profile:nvidia-nim-free-deepseek-v4-pro-0813`

Model: `deepseek-ai/deepseek-v4-pro-0813`

Money ceiling: 0 USD

This file defines future implementation scope only. This contract PR performs no NVIDIA/provider/account/API-key/model/network activity.

## 1. Exact cumulative implementation scope

Only these provider/live/code/test paths may be materially modified or created by the later V-03 implementation:

1. `platform/connectivity/providers/nvidia-nim/README.md`
2. `platform/connectivity/providers/nvidia-nim/data-policy.json`
3. `platform/connectivity/providers/nvidia-nim/quota-policy.json`
4. `platform/connectivity/providers/nvidia-nim/budget-policy.json`
5. `platform/connectivity/providers/nvidia-nim/transport-policy.json`
6. `platform/connectivity/providers/nvidia-nim/live-validation-policy.json`
7. `scripts/nvidia_nim_adapter.py`
8. `scripts/nvidia_nim_live_transport.py`
9. `scripts/nvidia_nim_live_smoke.py`
10. `scripts/nvidia_nim_session_credential_bridge.py`
11. `platform/connectivity/live/evidence/009v03/README.md`
12. `platform/connectivity/live/evidence/009v03/provider-live-state.json`
13. `platform/connectivity/live/evidence/009v03/connected-validation.json`
14. `platform/connectivity/live/evidence/009v03/quality-evaluation.json`
15. `tests/test_nvidia_nim_provider_adapter.py`
16. `tests/test_nvidia_nim_live_transport.py`
17. `tests/test_nvidia_nim_live_smoke.py`
18. `tests/test_nvidia_nim_session_credential_bridge.py`

Only these four V-03 memory files may additionally update:

- `studio/memory/tasks/STUDIO-009V-03/TASK.md`
- `studio/memory/tasks/STUDIO-009V-03/STATE.md`
- `studio/memory/tasks/STUDIO-009V-03/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009V-03/RESUME.md`

Maximum cumulative V-03 implementation PR scope: 22 unique paths.

No generic router, GitHub connector, Groq/Cloudflare provider code, Unity/game code, dependency file, workflow, partner endpoint or unrelated provider is authorized.

## 2. Provider-specific reconciliation

Implementation may reconcile only NVIDIA P-03 provider-specific fields required for V-03 validation.

Maximum promotion is `LIVE_VALIDATED`.

STUDIO-009E remains automatic routing/failover authority.

STUDIO-009F remains full connected studio acceptance.

Historical P-03 evidence remains historical and must not be rewritten.

## 3. Trusted transport

Implement direct standard-library HTTPS/TLS transport to:

`https://integrate.api.nvidia.com/v1/chat/completions`

Requirements:

- exact HTTPS;
- exact host `integrate.api.nvidia.com`;
- exact path `/v1/chat/completions`;
- exact model `deepseek-ai/deepseek-v4-pro-0813`;
- no redirect;
- no proxy/base-url override;
- no arbitrary host/path/model override;
- no partner endpoint;
- no self-hosted endpoint;
- no third-party gateway;
- concurrency 1;
- retry 0;
- timeout <=60 seconds;
- first-campaign input estimate <=4096 tokens;
- request body <=32768 bytes;
- response read <=131072 bytes;
- first-campaign requested completion <=512 tokens;
- streaming false;
- tools/functions absent;
- safe Content-Type handling;
- raw provider body absent from public exceptions.

## 4. Dedicated NVIDIA session credential bridge

Add `scripts/nvidia_nim_session_credential_bridge.py`.

Do not mutate or reuse Groq V-01 or Cloudflare V-02 provider-specific credential bridges as if they were provider-neutral.

The NVIDIA bridge must:

- bind exactly `credential-profile:nvidia-nim-api-key`;
- bind exactly `account-ref:nvidia-developer-program-owner-account`;
- accept raw key only from hidden Owner-interactive local input after connected preflight;
- keep raw key in memory only for the bounded campaign;
- prohibit `.env`, ambient environment variable, CLI argument, file cache, browser extraction, keychain automation, clipboard automation and remote secret store;
- never log, return, serialize, persist or expose raw key;
- support synthetic suppliers only in deterministic tests.

## 5. Bounded smoke ledger

A local ledger must reserve every real request before network I/O.

One Owner-authorized campaign:

- max 3 requests;
- concurrency 1;
- retry 0;
- first-campaign input estimate <=4096 tokens/request;
- completion <=512 tokens/request;
- money ceiling 0.

A failed request consumes its reservation. Unsafe failure ends the campaign.

## 6. Provider-specific hostile tests

Before any real request, deterministic tests must cover at minimum:

- exact host/path/model;
- redirects rejected;
- partner/self-hosted/third-party endpoint rejected;
- API key never logged/serialized/returned;
- no env/CLI/file secret lookup;
- 401/403/422/429/3xx/5xx normalization;
- timeout;
- oversized request/response;
- malformed JSON/Unicode;
- provider error-body redaction;
- wrong model identity;
- request count <=3;
- concurrency rejection;
- retry remains zero;
- tool/function-call rejection;
- Remote MCP/code execution/file search/URL context rejection;
- missing free/trial eligibility fails closed;
- paid/subscription/purchase path fails closed;
- MANUAL/FAKE rollback remains available.

## 7. Owner connected preflight

Before real API-key materialization, Owner must confirm current NVIDIA state:

- exact model still has NVIDIA-hosted Free Endpoint;
- no partner endpoint selected;
- no subscription/paid deployment/purchased credits needed;
- account-visible free/trial entitlement is sufficient for the bounded campaign;
- temporary/revocable key lifecycle is available;
- current terms still permit internal testing/evaluation;
- no paid fallback.

If ambiguous, do not request/input the key.

## 8. Post-smoke gates

After the bounded smoke:

1. materialize sanitized transport/request/model/usage/quality evidence;
2. Owner separately confirms observed billable monetary charge remains USD 0;
3. Connected QA independently reviews immutable smoke evidence;
4. Connected Review/Integration independently reviews immutable QA head;
5. validation API key is revoked/deleted/invalidated and safe revocation evidence is recorded;
6. Owner records final disposition;
7. promotion ceiling remains `LIVE_VALIDATED`;
8. implementation PR remains separate from Owner merge;
9. V-03 closeout remains separate after implementation merge.

No later stage may re-run a successful smoke without fresh Owner authorization.

## 9. Acceptance

Implementation must preserve retained baseline tests and add provider-specific live transport, smoke, bridge and hostile tests.

No real provider request occurs merely to make tests pass.

<!-- STUDIO-009V-03-CONTRACT-CHECKPOINT-0001 -->
