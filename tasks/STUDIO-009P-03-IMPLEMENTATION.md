# STUDIO-009P-03-IMPLEMENTATION - NVIDIA NIM offline provider adapter and policy evidence

Status: APPROVED SCOPE - NOT EXECUTABLE UNTIL P-03 CONTRACT MERGE

Parent: `tasks/STUDIO-009P-03.md`

Planned branch: `agent/studio-009p-03-nvidia-nim-implementation`

Provider: NVIDIA-hosted NIM API Catalog

Exact model: `deepseek-ai/deepseek-v4-pro-0813`

Cost class: ZERO_COST_ONLY

Network/provider runtime authority: NONE

## Exact future implementation scope

Only after the P-03 contract PR is durably merged may the implementation branch create/materially modify these 20 paths:

1. `platform/connectivity/providers/nvidia-nim/README.md`
2. `platform/connectivity/providers/nvidia-nim/provider-profile.json`
3. `platform/connectivity/providers/nvidia-nim/model-profile-deepseek-v4-pro-0813.json`
4. `platform/connectivity/providers/nvidia-nim/child-contract-evidence.json`
5. `platform/connectivity/providers/nvidia-nim/transport-policy.json`
6. `platform/connectivity/providers/nvidia-nim/data-policy.json`
7. `platform/connectivity/providers/nvidia-nim/quota-policy.json`
8. `platform/connectivity/providers/nvidia-nim/budget-policy.json`
9. `platform/connectivity/fixtures/009p03/README.md`
10. `platform/connectivity/fixtures/009p03/valid-nvidia-nim-provider.json`
11. `platform/connectivity/fixtures/009p03/valid-nvidia-nim-model.json`
12. `platform/connectivity/fixtures/009p03/valid-nvidia-nim-child-evidence.json`
13. `platform/connectivity/fixtures/009p03/invalid-unapproved-model.json`
14. `platform/connectivity/fixtures/009p03/invalid-host-or-path.json`
15. `platform/connectivity/fixtures/009p03/invalid-data-broadening.json`
16. `platform/connectivity/fixtures/009p03/invalid-nonzero-budget.json`
17. `platform/connectivity/fixtures/009p03/invalid-credential-ref.json`
18. `scripts/nvidia_nim_adapter.py`
19. `tests/test_nvidia_nim_provider_contract.py`
20. `tests/test_nvidia_nim_provider_adapter.py`

Only the four existing P-03 memory paths may additionally update during implementation. Maximum cumulative implementation PR scope: 24 unique paths.

## Implementation boundary

Implementation is deterministic/offline/synthetic only and may reuse accepted canonicalization, structural limits, immutable-input, secret detection, credential-reference, provider/model profile, quota/budget, safe-error and MANUAL/FAKE patterns.

`scripts/nvidia_nim_adapter.py` may normalize exact configuration, host/path policy, synthetic chat requests/responses, reasoning/output limits, dynamic quota evidence metadata, data/budget policy and safe error objects.

It must not import/call network libraries/provider SDKs, read `NVIDIA_API_KEY` or real secrets, inspect credential stores, connect to NVIDIA/DeepSeek, inspect/mutate an NVIDIA account, create/resolve/revoke a real key, execute model tools, route/fail over, enable production use, or spend money.

All provider/network/account/credential/store/tool/MCP/routing/connected-execution activity remains NONE and spend remains ZERO.

## Retained checks

Preserve vertical-slice validation, retained provider/connectivity focused tests, full suite, new P-03 tests, `git diff --check`, exact path enforcement, Rules CI, secret hygiene, zero runtime provider activity and zero spend.

## Two-human implementation discipline

Only one writer claim/worktree may own P-03 implementation paths. The second human may review/research read-only. No parallel P-03 writer branch. Provider role assignment is not frozen; later GAME benchmark evidence decides fit/routing eligibility.