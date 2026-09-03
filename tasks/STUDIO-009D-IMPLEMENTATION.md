# STUDIO-009D-IMPLEMENTATION - Deterministic provider onboarding framework

## Authorization

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-09-03
- Parent capability: `tasks/STUDIO-009D.md`
- Verified dependency baseline: STUDIO-009C closeout merge `bfc48f2080bd654666955ca1ec615ebc27ad83cc`
- Contract branch: `agent/studio-009d-contract`
- Planned implementation branch: `agent/studio-009d-provider-onboarding`
- Cost class: ZERO_COST
- Provider runtime activity: NONE
- Network activity: NONE
- Credential runtime activity: NONE
- Connected execution activity: NONE

This implementation contract becomes executable only after the STUDIO-009D contract Pull Request merges. Until then, no implementation path below may be created.

## 1. Exact implementation scope

The implementation branch may create or materially modify only these 21 implementation paths:

1. `platform/connectivity/PROVIDER_ONBOARDING.md`
2. `tasks/STUDIO-009P-TEMPLATE.md`
3. `platform/connectivity/schemas/provider-profile.schema.json`
4. `platform/connectivity/schemas/provider-model.schema.json`
5. `platform/connectivity/schemas/provider-capability-binding.schema.json`
6. `platform/connectivity/schemas/provider-child-contract-evidence.schema.json`
7. `platform/connectivity/schemas/provider-onboarding-event.schema.json`
8. `platform/connectivity/fixtures/009d/valid-disabled-provider.json`
9. `platform/connectivity/fixtures/009d/valid-eligible-provider.json`
10. `platform/connectivity/fixtures/009d/valid-model-profile.json`
11. `platform/connectivity/fixtures/009d/valid-child-contract-evidence.json`
12. `platform/connectivity/fixtures/009d/invalid-provider-identity.json`
13. `platform/connectivity/fixtures/009d/invalid-model-scope.json`
14. `platform/connectivity/fixtures/009d/invalid-data-policy-broadening.json`
15. `platform/connectivity/fixtures/009d/invalid-credential-profile.json`
16. `platform/connectivity/fixtures/009d/invalid-nonzero-budget.json`
17. `platform/connectivity/fixtures/009d/invalid-missing-child-contract.json`
18. `platform/connectivity/fixtures/009d/README.md`
19. `scripts/provider_onboarding.py`
20. `tests/test_provider_onboarding.py`
21. `tests/test_provider_contract.py`

Only these four existing memory files may also be materially updated:

- `studio/memory/tasks/STUDIO-009D/TASK.md`
- `studio/memory/tasks/STUDIO-009D/STATE.md`
- `studio/memory/tasks/STUDIO-009D/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009D/RESUME.md`

Maximum cumulative implementation Pull Request scope: exactly the authorized subset, never more than 25 unique changed paths.

Renames, binaries, generated build products, dependency changes, workflow changes, provider SDKs, live transports, real credentials, real provider configuration, routing, and unrelated edits are prohibited.

## 2. Required implementation behavior

### 2.1 Provider-profile validator

Implement an exact-schema, provider-neutral validator that:

- reuses STUDIO-009A canonicalization, secret detection, structural limits, chronology, finite-number, and input-mutation controls;
- reuses STUDIO-009C safe secret/reference boundaries;
- validates opaque provider, transport, credential, policy, Owner, kill-switch, model, and capability references without resolving them;
- enforces exact lifecycle state;
- enforces caller-supplied UTC chronology and expiry;
- rejects duplicate/conflicting provider identities;
- rejects secret-bearing or unbounded metadata;
- produces normalized metadata only.

No production provider constructor or transport may exist.

### 2.2 Child-contract evidence validator

Implement deterministic child-contract evidence validation that:

- binds one provider profile to exactly one `STUDIO-009P*` child identifier;
- binds Owner acceptance evidence;
- binds provider-identity, transport, credential, model, capability, data-export, quota, budget, kill-switch, incident-response, and rollback evidence references;
- distinguishes synthetic test evidence from real-provider evidence;
- rejects missing, conflicting, stale, future, revoked, or broadened evidence;
- cannot itself mark a real provider connected or active.

### 2.3 Model-profile and capability-binding validator

Implement exact validators that:

- bind every model to one provider profile and child-contract evidence;
- bind every capability to one accepted model profile;
- constrain data classifications and bounded request/output metadata;
- reject undeclared model/capability combinations;
- reject provider/model identity derived from model output or untrusted content;
- preserve provider-neutral STUDIO-007F request/result authority boundaries.

### 2.4 Eligibility planner

Implement a deterministic immutable onboarding eligibility plan.

The planner may return only metadata such as `ELIGIBLE`, `INELIGIBLE`, or stable refusal codes. It must never:

- call a provider;
- resolve a credential;
- create a network request;
- create a routing decision;
- authorize spend;
- claim that a provider is live.

`ELIGIBLE` requires a non-revoked profile, accepted child-contract evidence, exact model/capability bindings, Owner evidence, zero-budget evidence for STUDIO-009D, and caller-supplied non-expired chronology.

### 2.5 Lifecycle event normalization

Normalize metadata-only events for:

- `REGISTER_CANDIDATE`
- `MARK_ELIGIBLE`
- `PAUSE`
- `REVOKE`
- `EXPIRE`

Events bind profile identity/digest, child-contract evidence where applicable, Owner/control evidence, caller-supplied time, and canonical digest.

Events cannot broaden scope, change provider identity, extend expiry, restore a revoked profile, create `ACTIVE`, or authorize a real connection.

## 3. Exact schema requirements

All controlled objects and nested objects use exact fields with `additionalProperties: false` or equivalent implementation checks.

Schemas must not define raw-secret fields.

Provider/model/transport identifiers in generic committed fixtures must be clearly synthetic and non-routable. Generic STUDIO-009D schemas may carry opaque identity references, but real provider-specific values require a later accepted child contract.

No free-form arbitrary metadata bag is allowed.

## 4. `STUDIO-009P-TEMPLATE.md`

The committed template must require each real-provider child to specify, at minimum:

- real provider identity and authoritative sources;
- exact model identities/version policy;
- endpoint/host/transport allowlist;
- auth mechanism and credential-profile lineage;
- capability map;
- data-export/retention/training policy;
- quota/rate/timeout/retry limits;
- budget ceiling with provider/currency/time window;
- provider/transport identity verification;
- kill switch/pause/revocation;
- incident response;
- MANUAL/FAKE rollback;
- focused/regression tests;
- QA and Review gates;
- explicit STUDIO-009F activation dependency.

The template itself grants no provider authority.

## 5. Required fixtures and negative coverage

Committed fixtures are synthetic metadata only.

Focused tests must cover at least:

- every positive/negative fixture;
- duplicate JSON keys;
- unknown/missing nested fields;
- byte/depth/node/Unicode/non-finite-number bounds;
- profile identity and duplicate/conflicting identity;
- synthetic-vs-real child evidence handling;
- missing child-contract evidence;
- model/provider lineage;
- undeclared capability;
- data classification broadening;
- credential-profile reference mismatch;
- missing Owner approval;
- paused/revoked/expired/future evidence;
- zero-budget enforcement;
- no `ACTIVE` lifecycle state;
- no secret value in normalized output;
- stable safe errors with no untrusted echo;
- input/fixture immutability;
- no system-clock acceptance;
- no environment/keyring/filesystem credential lookup;
- no network/subprocess/provider SDK/CLI activity.

## 6. Source/runtime prohibitions

Production source under this implementation must not import or call:

- `socket`, `requests`, `urllib.request`, HTTP/GraphQL/WebSocket/gRPC clients;
- provider SDK/API clients;
- provider CLIs through subprocess;
- account/model/billing discovery;
- environment-variable or `.env` credential resolution;
- keyring, Credential Manager, browser credential/session APIs;
- vault/secret-manager/KMS/HSM SDKs;
- system clock functions for acceptance decisions.

Tests may invoke local Python tooling only. No external/network process is permitted.

## 7. Required checks

At minimum:

```powershell
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_connectivity_boundary tests.test_repository_registry tests.test_github_connector tests.test_credential_broker tests.test_credential_redaction tests.test_provider_onboarding tests.test_provider_contract -v
python -m unittest discover -s tests -p 'test*.py' -v
git diff --check
```

The retained full-suite baseline before STUDIO-009D implementation is 660 tests. The implementation must increase coverage without reducing retained behavior.

## 8. Review gates

Before implementation merge:

- contract Pull Request merged;
- one immutable implementation head;
- Rules CI success on that head;
- exact cumulative path allowlist, maximum 25;
- zero provider/network/credential/store/connector/routing/connected-execution/spend activity;
- independent QA-01 PASS;
- independent Review and Integration APPROVE;
- zero blocking findings;
- separate Studio Owner merge decision.

Implementation and closeout use separate Pull Requests. No script, validator, adapter, provider, router, reviewer, connector, or AI may merge either Pull Request.

## 9. Later-phase boundary

STUDIO-009D implementation does not approve a real provider, real model, real endpoint, real credential, provider SDK, provider account, network call, or model call.

Each real provider requires a separately merged `STUDIO-009P*` child contract and later provider-specific implementation. Policy routing remains STUDIO-009E. Connected activation remains STUDIO-009F. Monetary ceiling remains integer zero during STUDIO-009D.