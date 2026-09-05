# STUDIO-009V-01-IMPLEMENTATION — Groq bounded live transport and connected smoke

## Authorization

- Status: APPROVED SCOPE — NOT EXECUTABLE UNTIL STUDIO-009V-01 CONTRACT MERGE
- Parent contract: `tasks/STUDIO-009V-01.md`
- Provider child: `STUDIO-009P-01`
- Provider profile: `provider-profile:groq-free-gpt-oss-120b`
- Model: `openai/gpt-oss-120b`
- Cost class: ZERO_COST_ONLY
- Money ceiling: 0 USD

No real Groq credential/network/model activity is authorized until the V-01 contract Pull Request is durably merged.

## 1. Exact cumulative implementation scope

Only these sixteen implementation/evidence/test paths may be created or materially modified:

1. `platform/connectivity/providers/groq/README.md`
2. `platform/connectivity/providers/groq/transport-policy.json`
3. `platform/connectivity/providers/groq/data-policy.json`
4. `platform/connectivity/providers/groq/live-validation-policy.json`
5. `scripts/groq_provider_adapter.py`
6. `scripts/session_credential_bridge.py`
7. `scripts/groq_live_transport.py`
8. `scripts/groq_live_smoke.py`
9. `platform/connectivity/live/evidence/009v01/README.md`
10. `platform/connectivity/live/evidence/009v01/provider-live-state.json`
11. `platform/connectivity/live/evidence/009v01/connected-validation.json`
12. `platform/connectivity/live/evidence/009v01/quality-evaluation.json`
13. `tests/test_groq_provider_adapter.py`
14. `tests/test_session_credential_bridge.py`
15. `tests/test_groq_live_transport.py`
16. `tests/test_groq_live_smoke.py`

Only these four task-memory files may additionally be updated:

- `studio/memory/tasks/STUDIO-009V-01/TASK.md`
- `studio/memory/tasks/STUDIO-009V-01/STATE.md`
- `studio/memory/tasks/STUDIO-009V-01/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009V-01/RESUME.md`

Maximum cumulative implementation Pull Request scope: 20 unique paths.

No generic routing code, repository connector, Unity/game code, Cloudflare code, dependency file, workflow, or unrelated path is authorized.

## 2. Reconcile pre-009R Groq policy

The existing Groq offline files still contain historical `STUDIO-009F_ONLY` connected-activation values from before STUDIO-009R-01.

Implementation must reconcile only the Groq provider-specific policy needed for V-01 so that:

- offline P-01 evidence remains historical and valid;
- real connected validation is authorized only by merged `STUDIO-009V-01`;
- ordinary worker/routing authority remains unavailable;
- STUDIO-009F remains required for full integrated studio acceptance.

No silent global rewrite of generic activation policy is allowed.

## 3. Session credential bridge

Implement a narrow provider-neutral session bridge used by V-01.

Production behavior:

- receives validated credential lease metadata first;
- obtains the Groq API key only from hidden Owner-interactive input in the local process;
- never reads environment variables, `.env`, keychains, browser storage, files, CLI arguments, or remote stores;
- never logs/serializes/returns the secret;
- exposes the secret only to the trusted transport call boundary;
- performs best-effort in-memory lifetime minimization;
- supports an injected synthetic supplier for tests;
- fails closed outside an interactive Owner-authorized run.

This bridge is not a persistent secret store.

## 4. Trusted Groq HTTPS transport

Implement the live transport without adding a third-party dependency.

Preferred primitive: Python standard-library TLS/HTTP with explicit certificate verification.

Hard requirements:

- exact host `api.groq.com`;
- exact path `/openai/v1/chat/completions`;
- HTTPS only;
- no redirect following;
- no arbitrary proxy/base URL;
- no caller-supplied model;
- exact `openai/gpt-oss-120b`;
- `tool_choice: "none"`;
- no tools/documents/search/storage;
- `citation_options: "disabled"` when accepted by the endpoint;
- concurrency 1;
- retry 0;
- timeout <= 30s;
- request <= 8,192 serialized bytes;
- response body read <= 65,536 bytes;
- requested completion <= 256 tokens;
- safe Content-Type handling;
- provider response body never included in public exception text.

A 3xx, unexpected host/model, oversized body, unsafe field, 401/403, 429, 5xx, or malformed response must yield a stable fail-closed result with no automatic retry.

## 5. Connected smoke orchestrator

The real smoke may execute only when all of the following are proven in-process:

- merged V-01 contract ref;
- exact P-01 closeout ref;
- exact R-01 closeout ref;
- accepted Groq provider/model/transport/data/budget lineage;
- Owner Free-tier confirmation;
- Owner ZDR confirmation;
- accepted zero monetary ceiling;
- active bounded credential-lease metadata;
- local kill switch armed;
- PUBLIC/SYNTHETIC probe set loaded;
- request counter initially zero.

Maximum real requests across the initial smoke: three.

Any failure stops further automatic calls.

## 6. Evidence materialization

Raw live responses stay temporary and noncanonical.

Only sanitized evidence may be committed, covering:

- live-state lineage;
- connected-validation lineage;
- exact request count;
- model/transport verification;
- safe rate-limit/quota metadata;
- zero-spend Owner confirmation;
- kill/revoke evidence;
- quality scores;
- connected QA/Review/Owner references;
- canonical digests.

Evidence files may be finalized at material QA/Review checkpoints while remaining within the exact cumulative path scope.

## 7. Tests before any real request

Before the smoke, local deterministic tests must cover at minimum:

- session secret never logged/serialized/returned;
- environment/CLI/file secret lookup forbidden;
- exact host/path/model;
- redirect rejection;
- TLS/HTTP boundary;
- 401/403/429/3xx/5xx normalization;
- timeout;
- oversized request/response;
- malformed JSON/Unicode/non-finite values;
- provider error-body redaction;
- response model mismatch;
- rate-limit header parsing;
- retry remains zero;
- request counter never exceeds three;
- concurrent request rejection;
- `tool_choice=none`;
- tool call/executed tool/citation/search rejection;
- Free-tier/ZDR preflight required;
- nonzero spend rejection;
- kill/pause/revoke dominance;
- generic provider-live gate lineage;
- input immutability;
- Manual/Fake fallback remains available.

No unit test may call Groq or any external network.

Retained pre-V-01 baseline is 874 total tests. Implementation must add coverage without reducing retained behavior.

## 8. Connected quality gate

The bounded smoke uses up to three fixed PUBLIC/SYNTHETIC probes.

`LIVE_VALIDATED` requires:

- every issued request accepted by the transport gate;
- exact model/host identity;
- no forbidden tool/external capability;
- all required structured outputs valid;
- quality rubric PASS;
- zero human correction on the fixed smoke outputs;
- zero observed spend;
- connected QA PASS;
- Review and Integration APPROVE;
- Studio Owner disposition.

HTTP 200 alone is insufficient.

## 9. Promotion ceiling

V-01 ends at `LIVE_VALIDATED` at most.

The implementation must not create:

- shadow-worker authority;
- bounded-worker repository write authority;
- routing eligibility;
- STUDIO-009E rules;
- STUDIO-009F full acceptance.

## 10. QA / Review / Owner merge

Before implementation merge:

- one immutable implementation/connected evidence head;
- exact cumulative maximum 20 paths;
- Rules CI success;
- independent connected QA PASS;
- independent Review and Integration APPROVE;
- zero blocking findings;
- no secret evidence;
- request count <= 3;
- retry 0;
- concurrency 1;
- observed spend 0;
- separate Studio Owner merge decision.

Implementation, QA, Review, Owner merge, and closeout remain separate checkpoints. No AI or script may self-merge.
