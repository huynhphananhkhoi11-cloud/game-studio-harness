# STUDIO-009C-IMPLEMENTATION - Deterministic credential broker and fake secret lifecycle

## Authorization

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-09-03
- Parent capability: `tasks/STUDIO-009C.md`
- Verified dependency baseline: STUDIO-009B closeout merge `32942ac4db312884ab2f2184a3f899e363d61058`
- Contract branch: `agent/studio-009c-contract`
- Planned implementation branch: `agent/studio-009c-credential-broker`
- Cost class: ZERO_COST
- Credential runtime activity: NONE
- Secret-store activity: NONE
- Connector runtime activity: NONE
- Provider activity: NONE

This implementation contract becomes executable only after the STUDIO-009C contract Pull Request merges. Until then, no implementation path below may be created.

## 1. Exact implementation scope

The implementation branch may create or materially modify only these 21 implementation paths:

1. `platform/connectivity/CREDENTIAL_BROKER.md`
2. `platform/connectivity/SECRET_LIFECYCLE.md`
3. `platform/connectivity/schemas/credential-profile.schema.json`
4. `platform/connectivity/schemas/credential-request.schema.json`
5. `platform/connectivity/schemas/credential-lease.schema.json`
6. `platform/connectivity/schemas/credential-event.schema.json`
7. `platform/connectivity/fixtures/009c/valid-disabled-profile.json`
8. `platform/connectivity/fixtures/009c/valid-repository-profile.json`
9. `platform/connectivity/fixtures/009c/valid-lease-request.json`
10. `platform/connectivity/fixtures/009c/invalid-embedded-secret.json`
11. `platform/connectivity/fixtures/009c/invalid-subject-mismatch.json`
12. `platform/connectivity/fixtures/009c/invalid-expired-profile.json`
13. `platform/connectivity/fixtures/009c/invalid-revoked-profile.json`
14. `platform/connectivity/fixtures/009c/invalid-missing-owner-evidence.json`
15. `platform/connectivity/fixtures/009c/invalid-scope-broadening.json`
16. `platform/connectivity/fixtures/009c/invalid-replay-request.json`
17. `platform/connectivity/fixtures/009c/README.md`
18. `scripts/credential_broker.py`
19. `scripts/credential_redaction.py`
20. `tests/test_credential_broker.py`
21. `tests/test_credential_redaction.py`

Only these four existing memory files may also be materially updated:

- `studio/memory/tasks/STUDIO-009C/TASK.md`
- `studio/memory/tasks/STUDIO-009C/STATE.md`
- `studio/memory/tasks/STUDIO-009C/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009C/RESUME.md`

Maximum cumulative implementation Pull Request scope: exactly the authorized subset, never more than 25 unique changed paths.

Renames, binaries, generated build products, dependencies, workflow changes, live secret-store connectors, credential values, provider SDKs, network transports, and unrelated edits are prohibited.

## 2. Required implementation behavior

### 2.1 Credential profile validator

Implement an exact-schema validator for credential-profile metadata.

It must:

- reuse accepted STUDIO-009A canonicalization, secret detection, structural limits, references, chronology, finite-number, and input-mutation controls;
- bind repository-targeted profiles to accepted STUDIO-009B repository identity and record digest;
- validate opaque auth/store/locator references without resolving them;
- enforce exact lifecycle state and caller-supplied time;
- reject duplicates/conflicts and scope broadening;
- produce normalized metadata only;
- never return or accept a production secret value.

### 2.2 Credential-use request planner

Accept only a validated usable profile plus an exact credential-use request.

It must:

- bind task/attempt/queue/dispatch/gate/trace/quota-budget/Owner evidence;
- bind writer/worktree evidence for write-capable repository use;
- bind repository record and operation digest where applicable;
- enforce capability/purpose scope without broadening;
- enforce integer-only lease duration at or below 3600 seconds and the profile maximum;
- enforce caller-supplied UTC chronology;
- enforce deterministic idempotency and replay rules;
- emit an immutable lease plan containing no secret.

### 2.3 Deterministic fake broker

Provide an injected fake store/broker interface only.

The fake may:

- hold synthetic non-production secret objects in memory during a test;
- count store accesses;
- simulate lease issue, reuse, expiry, revocation, rotation-required, and kill-switch behavior.

The fake must not:

- read environment variables or credential files;
- contact any operating-system credential service or external secret manager;
- write synthetic secret material to disk, stdout/stderr, memory records, or normalized results;
- provide a production constructor.

### 2.4 Redaction and safe errors

Implement deterministic redaction/error hygiene that:

- prevents secret-like material from appearing in public exceptions/results;
- uses stable error codes and fixed safe messages;
- does not echo untrusted fields or values;
- is bounded for bytes, depth, nodes, and string processing;
- does not claim cryptographic memory erasure or secure zeroization that Python cannot prove.

### 2.5 Lifecycle event normalization

Lifecycle events are metadata-only and must bind:

- profile identity/digest;
- lease identity where applicable;
- action (`DISABLE`, `ENABLE_ELIGIBLE`, `REVOKE`, `ROTATION_REQUIRED`, `LEASE_ISSUED`, `LEASE_EXPIRED`);
- Owner/control evidence;
- caller-supplied time;
- canonical digest.

Events cannot reactivate a revoked profile, expand scope, extend expiry, or bypass fresh Owner evidence.

## 3. Exact schema requirements

All controlled objects and nested objects use exact fields with `additionalProperties: false` or equivalent implementation checks.

Schemas must reject secret-bearing fields and must not define a field that carries a raw credential.

Reference-like values are opaque identifiers only. No schema may accept URL user-info, bearer strings, private-key text, token-shaped material, or unbounded arbitrary metadata.

## 4. Required fixtures and negative coverage

The committed fixtures are metadata-only. `invalid-embedded-secret.json` may contain a clearly synthetic non-usable marker sufficient to exercise secret-field rejection; it must not contain a token/key that resembles a usable production credential.

Focused tests must cover at least:

- every positive/negative fixture;
- duplicate JSON keys;
- unknown/missing nested fields;
- input byte/depth/node/Unicode/non-finite-number limits;
- profile identity and duplicate/conflicting identity;
- repository subject and digest lineage;
- auth/store/locator reference format;
- disabled/revoked/expired/future/rotation-required profiles;
- allowed capability/purpose scope;
- write evidence requirements;
- Owner/gate/trace/queue/dispatch/zero-budget evidence;
- caller-supplied time and no system clock;
- lease maximum and profile maximum;
- idempotency, replay, and conflict;
- kill switch and revocation dominance;
- input and fixture immutability;
- safe errors and redaction;
- fake store call count;
- no secret value in normalized output;
- no environment/keyring/filesystem/network/subprocess/provider activity.

## 5. Source/runtime prohibitions

Production source under this implementation must not import or call live credential/runtime facilities such as:

- `socket`, `requests`, `urllib.request`, HTTP/GraphQL clients;
- `subprocess` for credential retrieval;
- `keyring`, Windows Credential Manager, browser credential/session APIs;
- cloud vault/secret-manager/KMS/HSM SDKs;
- GitHub App, OAuth, PAT, SSH, provider SDK/API/CLI clients;
- environment-variable or `.env` credential resolution;
- system clock functions for acceptance decisions.

Tests may use standard-library subprocess only when required to invoke a local CLI under test, but no external/network process is permitted.

## 6. Required checks

At minimum:

```powershell
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_connectivity_boundary tests.test_repository_registry tests.test_github_connector tests.test_credential_broker tests.test_credential_redaction -v
python -m unittest discover -s tests -p 'test*.py' -v
git diff --check
```

The retained full-suite baseline before STUDIO-009C implementation is 551 tests. The implementation must increase coverage without reducing retained behavior.

## 7. Review gates

Before implementation merge:

- contract Pull Request merged;
- one immutable implementation head;
- Rules CI success on that head;
- exact cumulative path allowlist, maximum 25;
- zero live credential/store/connector/provider/network/routing/connected-execution/spend activity;
- independent QA-01 PASS;
- independent Review and Integration APPROVE;
- zero blocking findings;
- separate Studio Owner merge decision.

Implementation and closeout use separate Pull Requests. No script, broker, validator, reviewer, connector, provider, or AI may merge either Pull Request.

## 8. Later-phase boundary

STUDIO-009C implementation does not select or enroll a real credential, secret store, GitHub auth mechanism, or provider credential. It does not activate the STUDIO-009B connector.

STUDIO-009D/provider child contracts remain required for real providers. STUDIO-009F remains required for connected activation. Monetary ceiling remains integer zero unless a later explicit Owner contract changes it.