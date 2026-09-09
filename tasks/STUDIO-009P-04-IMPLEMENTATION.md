# STUDIO-009P-04-IMPLEMENTATION - Poolside Laguna S 2.1 offline provider adapter and policy evidence

Status: APPROVED SCOPE - NOT EXECUTABLE UNTIL P-04 CONTRACT MERGE

Parent: `tasks/STUDIO-009P-04.md`

Planned branch: `agent/studio-009p-04-poolside-laguna-s-implementation`

Provider: Poolside standalone hosted inference API

Exact model: `poolside/laguna-s-2.1`

Cost class: ZERO_COST_ONLY

Network/provider runtime authority: NONE

## Exact future implementation scope

Only after the P-04 contract PR is durably merged may the implementation branch create/materially modify these 20 paths:

1. `platform/connectivity/providers/poolside/README.md`
2. `platform/connectivity/providers/poolside/provider-profile.json`
3. `platform/connectivity/providers/poolside/model-profile-laguna-s-2.1.json`
4. `platform/connectivity/providers/poolside/child-contract-evidence.json`
5. `platform/connectivity/providers/poolside/transport-policy.json`
6. `platform/connectivity/providers/poolside/data-policy.json`
7. `platform/connectivity/providers/poolside/quota-policy.json`
8. `platform/connectivity/providers/poolside/budget-policy.json`
9. `platform/connectivity/fixtures/009p04/README.md`
10. `platform/connectivity/fixtures/009p04/valid-poolside-provider.json`
11. `platform/connectivity/fixtures/009p04/valid-poolside-model.json`
12. `platform/connectivity/fixtures/009p04/valid-poolside-child-evidence.json`
13. `platform/connectivity/fixtures/009p04/invalid-unapproved-model.json`
14. `platform/connectivity/fixtures/009p04/invalid-host-or-path.json`
15. `platform/connectivity/fixtures/009p04/invalid-data-broadening.json`
16. `platform/connectivity/fixtures/009p04/invalid-nonzero-budget.json`
17. `platform/connectivity/fixtures/009p04/invalid-credential-ref.json`
18. `scripts/poolside_adapter.py`
19. `tests/test_poolside_provider_contract.py`
20. `tests/test_poolside_provider_adapter.py`

Only the four existing P-04 memory paths may additionally update during implementation.

Maximum cumulative implementation PR scope: 24 unique paths.

## Implementation boundary

Implementation is deterministic/offline/synthetic only and may reuse accepted canonicalization, structural limits, immutable-input, secret detection, credential-reference, provider/model profile, quota/budget, safe-error and MANUAL/FAKE patterns.

`scripts/poolside_adapter.py` may normalize exact configuration, direct-host/path policy, synthetic chat requests/responses, bounded reasoning/output metadata, dynamic free-entitlement evidence metadata, data/budget policy and safe error objects.

It must not:

- import/call network libraries or provider SDKs;
- install/import/execute the `pool` CLI;
- read `POOLSIDE_API_KEY` or `POOLSIDE_TOKEN`;
- read `~/.config/poolside/credentials.json`;
- inspect keychains or secret stores;
- connect to Poolside/Laguna;
- inspect/mutate a Poolside account;
- create/resolve/revoke a real key;
- execute model tools/shell/files/browser/MCP/ACP;
- route/fail over;
- enable production use;
- spend money.

All provider/network/account/credential/store/tool/MCP/ACP/routing/connected-execution activity remains NONE and spend remains ZERO.

## Retained checks

Preserve vertical-slice validation, provider/connectivity focused tests, full suite, `git diff --check`, exact path enforcement, Rules CI, secret hygiene, zero runtime provider activity and zero spend.

## Two-human implementation discipline

Only one writer claim/worktree may own P-04 implementation paths. The second human may review/research read-only. No parallel P-04 or P-05 writer branch. Frozen V-03 remains untouched. Provider role assignment is not frozen; later GAME benchmark evidence decides fit/routing eligibility.

<!-- STUDIO-009P-04-CONTRACT-CHECKPOINT-0001 -->
