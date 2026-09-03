# STUDIO-009P-02-IMPLEMENTATION - Cloudflare Workers AI offline provider adapter and policy evidence

Status: APPROVED SCOPE - NOT EXECUTABLE UNTIL CONTRACT MERGE

Parent: `tasks/STUDIO-009P-02.md`

Planned branch: `agent/studio-009p-02-cloudflare-implementation`

Cost class: ZERO_COST_ONLY

Network/provider runtime authority: NONE

## Exact future implementation scope

After the STUDIO-009P-02 contract PR merges, the implementation branch may create or materially modify only these 20 implementation paths:

1. `platform/connectivity/providers/cloudflare-workers-ai/README.md`
2. `platform/connectivity/providers/cloudflare-workers-ai/provider-profile.json`
3. `platform/connectivity/providers/cloudflare-workers-ai/model-profile-nemotron-3-super.json`
4. `platform/connectivity/providers/cloudflare-workers-ai/child-contract-evidence.json`
5. `platform/connectivity/providers/cloudflare-workers-ai/transport-policy.json`
6. `platform/connectivity/providers/cloudflare-workers-ai/data-policy.json`
7. `platform/connectivity/providers/cloudflare-workers-ai/quota-policy.json`
8. `platform/connectivity/providers/cloudflare-workers-ai/budget-policy.json`
9. `platform/connectivity/fixtures/009p02/README.md`
10. `platform/connectivity/fixtures/009p02/valid-cloudflare-provider.json`
11. `platform/connectivity/fixtures/009p02/valid-cloudflare-model.json`
12. `platform/connectivity/fixtures/009p02/valid-cloudflare-child-evidence.json`
13. `platform/connectivity/fixtures/009p02/invalid-unapproved-model.json`
14. `platform/connectivity/fixtures/009p02/invalid-host-or-account-path.json`
15. `platform/connectivity/fixtures/009p02/invalid-data-broadening.json`
16. `platform/connectivity/fixtures/009p02/invalid-nonzero-budget.json`
17. `platform/connectivity/fixtures/009p02/invalid-credential-or-account-ref.json`
18. `scripts/cloudflare_workers_ai_adapter.py`
19. `tests/test_cloudflare_provider_contract.py`
20. `tests/test_cloudflare_provider_adapter.py`

Only the four existing STUDIO-009P-02 memory paths may additionally update during implementation.

Maximum cumulative implementation PR scope is therefore 24 unique paths.

## Implementation boundary

Implementation is deterministic and offline/synthetic only.

It may reuse STUDIO-009A/009C/009D canonicalization, secret detection, credential-reference validation, provider-profile/model/evidence schemas, quota/budget normalization, immutable input checks, and safe errors.

`scripts/cloudflare_workers_ai_adapter.py` may normalize provider-specific configuration, endpoint templates, request envelopes, synthetic response envelopes, error objects, quota evidence, and local function-call requests.

It must not:

- import or call socket, requests, urllib.request, httpx, aiohttp, grpc, websocket, Cloudflare/provider SDKs, or browser automation;
- invoke subprocesses for provider/account/token discovery;
- read `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, environment/.env secrets, credential stores, or OS keychains;
- connect to `api.cloudflare.com`;
- create, mutate, or inspect a Cloudflare account;
- create/resolve/revoke a Cloudflare API token;
- enable AI Gateway, Unified Billing, prepaid credits, storage services, or a paid Workers plan;
- call a real model or execute a tool.

All provider, network, account, credential, store, routing, tool, connected-execution, and spend activity must remain zero.

## Required retained checks

- vertical-slice data validation;
- retained 362 focused tests before new STUDIO-009P-02 provider tests;
- retained 759-test full suite before new provider tests;
- provider-specific tests added by implementation;
- `git diff --check`;
- Rules CI;
- exact allowed-path enforcement;
- provider/network/account/credential/store/tool/MCP/routing/connected-execution activity = zero;
- spend = zero.

The exact implementation runner must be produced only after this contract merges and must lock the actual merge baseline.
