# STUDIO-009R-01-IMPLEMENTATION — Progressive Live Validation Framework

## Authorization

- Status: APPROVED — IMPLEMENTATION NOT STARTED
- Parent contract: `tasks/STUDIO-009R-01.md`
- Planned implementation branch: `agent/studio-009r-01-implementation`
- Cost class: ZERO_COST
- Provider runtime activity: NONE
- Network activity: NONE
- Credential runtime activity: NONE
- Connected execution activity: NONE

This implementation contract becomes executable only after the STUDIO-009R-01 contract Pull Request is merged. Until then, none of the implementation paths below may be created or materially modified.

## 1. Exact implementation scope

The implementation branch may create or materially modify only these 17 implementation paths:

1. `platform/connectivity/live/LIVE_ACTIVATION_POLICY.md`
2. `platform/connectivity/live/provider-live-state.schema.json`
3. `platform/connectivity/live/connected-validation.schema.json`
4. `platform/connectivity/live/worker-mode-policy.schema.json`
5. `platform/connectivity/live/fixtures/009r/README.md`
6. `platform/connectivity/live/fixtures/009r/valid-live-validation-ready.json`
7. `platform/connectivity/live/fixtures/009r/valid-live-validated.json`
8. `platform/connectivity/live/fixtures/009r/valid-shadow-worker.json`
9. `platform/connectivity/live/fixtures/009r/invalid-unmerged-offline.json`
10. `platform/connectivity/live/fixtures/009r/invalid-private-data.json`
11. `platform/connectivity/live/fixtures/009r/invalid-nonzero-budget.json`
12. `platform/connectivity/live/fixtures/009r/invalid-routing-before-009e.json`
13. `platform/connectivity/live/fixtures/009r/invalid-revoked-provider.json`
14. `scripts/provider_live_gate.py`
15. `scripts/provider_live_evidence.py`
16. `tests/test_provider_live_gate.py`
17. `tests/test_provider_live_evidence.py`

Only these four existing memory files may also be materially updated:

- `studio/memory/tasks/STUDIO-009R-01/TASK.md`
- `studio/memory/tasks/STUDIO-009R-01/STATE.md`
- `studio/memory/tasks/STUDIO-009R-01/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009R-01/RESUME.md`

Maximum cumulative implementation Pull Request scope: 21 unique changed paths.

No provider-specific transport, SDK, real endpoint call, account discovery, real credential value, routing implementation, workflow change, dependency change, Unity/game code, or unrelated edit is authorized.

## 2. Required implementation behavior

### 2.1 Live-state validator

Implement an exact deterministic validator for the live-state contract introduced by STUDIO-009R-01.

It must:

- consume only accepted immutable references and caller-supplied chronology;
- bind one live-state record to one already accepted provider child/profile lineage;
- reject any transition that skips required offline merge, QA, Review, Owner, V-contract, or connected-evidence prerequisites;
- prevent data-class, capability, provider/model/host, quota, budget, or time broadening;
- make `PAUSED` and `REVOKED` dominate stale approvals;
- prohibit `ROUTING_ELIGIBLE` without explicit later STUDIO-009E authority.

### 2.2 Connected-validation evidence validator

Implement deterministic evidence validation for a later provider-specific V-track.

It may validate metadata describing bounded real calls, but this generic STUDIO-009R implementation itself must make zero real calls.

Required evidence fields must cover provider/model/transport lineage, credential reference lineage, accepted data class, request/output ceilings, request count, concurrency, retry count, transport/model identity verification, quota/capacity evidence when available, zero-cost evidence, kill-switch evidence, revocation evidence, connected QA/Review references, and Owner disposition.

### 2.3 Worker-mode policy validator

Implement exact policy validation for `LIVE_SHADOW_WORKER` and `LIVE_BOUNDED_WORKER`.

- Shadow mode has no repository write authority.
- Bounded mode must require an explicit Work Order, existing STUDIO-007 writer claim, isolated worktree, exact allowed paths, and local mediation.
- No worker mode may grant merge, direct-main, deployment, publication, budget increase, secret access, or arbitrary tool/network authority.
- Routing eligibility remains unavailable before STUDIO-009E.

### 2.4 Stable refusal codes

Provide stable fail-closed refusal codes for at least:

- offline child not durably merged;
- missing QA/Review/Owner evidence;
- missing V-contract authority;
- data-class broadening;
- provider/model/host mismatch;
- credential-lineage mismatch;
- request/concurrency/retry ceiling breach;
- nonzero spend or paid fallback;
- missing kill/revoke evidence;
- paused/revoked provider;
- routing requested before STUDIO-009E;
- unauthorized writer/path/tool authority.

### 2.5 Determinism and secret safety

Reuse the accepted STUDIO-009A/C/D canonicalization, structural limits, secret detection/redaction, stable public errors, caller-supplied UTC, no-system-clock acceptance, and input immutability controls where applicable.

## 3. Required tests

Focused tests must include positive and hostile/negative cases for every live state and transition, duplicate JSON keys, unknown fields, malformed Unicode, non-finite numbers, byte/depth/node limits, chronology, digest mismatch, data broadening, identity mismatch, secret-like material, nonzero budget, retry/concurrency broadening, missing kill switch, revocation dominance, premature routing, and writer/path broadening.

The retained full-suite baseline before implementation is 804 tests. Implementation must increase coverage without reducing retained behavior.

## 4. Source/runtime prohibitions

Production code added by this implementation must not import or call:

- `socket`, `requests`, `urllib.request`, HTTP/GraphQL/WebSocket/gRPC clients;
- provider SDKs or provider CLIs;
- environment, `.env`, keyring, Credential Manager, browser session, vault/KMS/HSM credential lookup;
- account/model/billing discovery;
- system clock for acceptance decisions;
- subprocess for provider/network execution;
- GitHub write/merge/deploy APIs;
- Unity Editor, Unity MCP, game repository, or game build tooling.

Tests may use local deterministic Python only. Network/provider activity must remain zero.

## 5. Required checks

At minimum:

```powershell
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_connectivity_boundary tests.test_repository_registry tests.test_github_connector tests.test_credential_broker tests.test_credential_redaction tests.test_provider_onboarding tests.test_provider_contract tests.test_groq_provider_contract tests.test_groq_provider_adapter tests.test_cloudflare_provider_contract tests.test_cloudflare_provider_adapter tests.test_provider_live_gate tests.test_provider_live_evidence -v
python -m unittest discover -s tests -p 'test*.py' -v
git diff --check
```

## 6. Review gates

Before implementation merge:

- STUDIO-009R-01 contract PR merged;
- one immutable implementation head;
- exact cumulative path allowlist, maximum 21;
- Rules CI success on that head;
- zero provider/network/account/credential/store/tool/routing/connected-execution/spend activity;
- independent QA PASS;
- independent Review and Integration APPROVE;
- zero blocking findings;
- separate Studio Owner merge decision.

Implementation and closeout remain separate checkpoints. No AI, adapter, validator, reviewer, provider, router, or script may self-merge.

## 7. Later boundary

This implementation creates the generic **offline validation framework only**. It still does not authorize Groq, Cloudflare, or any other provider to connect.

After this implementation is merged and closed out, provider-specific `STUDIO-009V-01`, `STUDIO-009V-02`, and later V-track contracts may be authored. Real network/credential/model activity remains prohibited until the corresponding V contract is durably merged.
