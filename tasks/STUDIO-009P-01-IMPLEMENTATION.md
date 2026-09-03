# STUDIO-009P-01-IMPLEMENTATION â€” Groq offline provider adapter and policy evidence

Status: APPROVED SCOPE â€” NOT EXECUTABLE UNTIL CONTRACT MERGE

Parent: `tasks/STUDIO-009P-01.md`

Planned branch: `agent/studio-009p-01-groq-implementation`

Cost class: ZERO_COST_ONLY

Network/provider runtime authority: NONE

## Exact future implementation scope

After the STUDIO-009P-01 contract PR merges, the implementation branch may create or materially modify only these 20 implementation paths:

1. `platform/connectivity/providers/groq/README.md`
2. `platform/connectivity/providers/groq/provider-profile.json`
3. `platform/connectivity/providers/groq/model-profile-gpt-oss-120b.json`
4. `platform/connectivity/providers/groq/child-contract-evidence.json`
5. `platform/connectivity/providers/groq/transport-policy.json`
6. `platform/connectivity/providers/groq/data-policy.json`
7. `platform/connectivity/providers/groq/quota-policy.json`
8. `platform/connectivity/providers/groq/budget-policy.json`
9. `platform/connectivity/fixtures/009p01/README.md`
10. `platform/connectivity/fixtures/009p01/valid-groq-provider.json`
11. `platform/connectivity/fixtures/009p01/valid-groq-model.json`
12. `platform/connectivity/fixtures/009p01/valid-groq-child-evidence.json`
13. `platform/connectivity/fixtures/009p01/invalid-unapproved-model.json`
14. `platform/connectivity/fixtures/009p01/invalid-host.json`
15. `platform/connectivity/fixtures/009p01/invalid-data-broadening.json`
16. `platform/connectivity/fixtures/009p01/invalid-nonzero-budget.json`
17. `platform/connectivity/fixtures/009p01/invalid-credential-ref.json`
18. `scripts/groq_provider_adapter.py`
19. `tests/test_groq_provider_contract.py`
20. `tests/test_groq_provider_adapter.py`

Only the four existing STUDIO-009P-01 memory paths may additionally update during implementation. Maximum cumulative implementation PR scope is therefore 24 unique paths.

## Implementation boundary

Implementation is deterministic and offline/synthetic only. It may reuse STUDIO-009A/009C/009D canonicalization, secret detection, credential-reference validation, provider-profile/model/evidence schemas, quota/budget normalization, immutable input checks, and safe errors.

`scripts/groq_provider_adapter.py` may normalize provider-specific configuration, request envelopes, synthetic response envelopes, error objects, rate-limit headers, and local tool-call requests. It must not import or call socket, requests, urllib.request, httpx, aiohttp, grpc, websocket, provider SDKs, subprocess provider calls, browser automation, or credential stores; it must not read GROQ_API_KEY or environment/.env secrets; and it must not connect to `api.groq.com`.

Built-in browser search, built-in code execution, Compound, remote MCP, real tool execution, real model calls, and credential resolution are forbidden.

## Required retained checks

- vertical-slice data validation;
- 323 retained focused STUDIO-009A/B/C/D tests before new provider tests;
- full retained 720-test suite before new provider tests;
- provider-specific tests added by this implementation;
- `git diff --check`;
- Rules CI;
- provider/network/credential/store/connector/routing/connected-execution activity = zero;
- spend = zero.

The exact implementation runner must be produced only after this contract merges and must lock the actual merge baseline.