# STUDIO-009B-IMPLEMENTATION - Deterministic repository registry and disabled GitHub connector core

## 1. Purpose

Authorize one deterministic repository-registry validator and one fail-closed GitHub connector core with an injected fake transport.

This is an implementation contract. Its contract-only Pull Request must merge before any implementation path below is created. The implementation must not contact GitHub or activate credentials.

## 2. Approval and baseline

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-09-02
- Parent capability: `tasks/STUDIO-009B.md`
- Verified dependency baseline: STUDIO-009A closeout merge `b6b31a225f38422cbb15c762f4dcc2e2e731b39c`
- Contract branch: `agent/studio-009b-contract`
- Planned implementation branch: `agent/studio-009b-repository-connector`
- Cost class: `ZERO_COST`
- Connector runtime activity: `NONE`
- Credential activity: `NONE`

## 3. Normative implementation

### 3.1 Repository registry validator

Schema v1 validates exact repository records defined by `tasks/STUDIO-009B.md`, binds each record to accepted STUDIO-009A evidence, detects duplicate/conflicting identities, normalizes safe fields, and returns stable error codes without mutating input.

### 3.2 Connector request planner

The planner accepts only a validated active repository record plus an exact operation envelope. It resolves effective access without broadening the record, rejects denied operations before transport, and emits a new immutable transport plan.

### 3.3 Disabled connector core

The connector core accepts an injected transport interface. Production/live transport constructors are absent. Tests use only a deterministic in-memory fake that records normalized plans and returns bounded fixtures.

The core normalizes and verifies responses against requested repository identity, operation, path/ref scope, immutable revisions, idempotency key, and size limits. It cannot merge, approve, execute repository content, or alter authority.

## 4. Exact implementation scope

The future implementation branch may create exactly these twenty paths:

1. `platform/connectivity/REPOSITORY_REGISTRY.md`
2. `platform/connectivity/GITHUB_CONNECTOR.md`
3. `platform/connectivity/schemas/repository-record.schema.json`
4. `platform/connectivity/schemas/github-operation.schema.json`
5. `platform/connectivity/schemas/github-result.schema.json`
6. `platform/connectivity/fixtures/009b/valid-disabled-repository.json`
7. `platform/connectivity/fixtures/009b/valid-read-only-repository.json`
8. `platform/connectivity/fixtures/009b/valid-pr-write-operation.json`
9. `platform/connectivity/fixtures/009b/invalid-embedded-credential.json`
10. `platform/connectivity/fixtures/009b/invalid-unapproved-repository.json`
11. `platform/connectivity/fixtures/009b/invalid-default-branch-write.json`
12. `platform/connectivity/fixtures/009b/invalid-path-escape.json`
13. `platform/connectivity/fixtures/009b/invalid-mutable-revision.json`
14. `platform/connectivity/fixtures/009b/invalid-missing-owner-evidence.json`
15. `platform/connectivity/fixtures/009b/invalid-unsafe-github-url.json`
16. `platform/connectivity/fixtures/009b/README.md`
17. `scripts/repository_registry.py`
18. `scripts/github_connector.py`
19. `tests/test_repository_registry.py`
20. `tests/test_github_connector.py`

The implementation may materially update only these four memory records:

- `studio/memory/tasks/STUDIO-009B/TASK.md`
- `studio/memory/tasks/STUDIO-009B/STATE.md`
- `studio/memory/tasks/STUDIO-009B/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009B/RESUME.md`

Maximum implementation Pull Request scope: 24 changed paths. Renames, binary/generated files, dependencies, workflows, live transports, credential files, and changes outside this list are prohibited.

## 5. Required behavior

- Reject missing and extra fields at every controlled object level.
- Reuse the accepted STUDIO-009A canonicalization, path, chronology, secret, and structural limits rather than creating a weaker duplicate.
- Require one unique validated repository identity and immutable registration revision.
- Pin host to `github.com`; reject user-info, query, fragment, alternate ports, IP literals, Unicode/confusable host forms, and off-host redirects.
- Enforce access tier, default-branch denial, exact branch namespace, path scope, data classification, and instruction authority.
- Require writer claim and worktree evidence for write operations.
- Require Owner, gate, trace, queue, dispatch, boundary, threat, and zero-budget evidence.
- Enforce bounded payload, file count, pagination, timeout, and response size using integer-only limits.
- Bind every request and result to canonical SHA-256 digests and caller-supplied UTC `as_of`.
- Reject stale/replayed idempotency evidence or return one prior normalized result without repeating transport.
- Validate response repository identity, operation, refs, paths, and immutable revisions.
- Return stable error codes without echoing secrets or untrusted content.
- Never mutate caller objects or fixture bytes.
- Never read system clock, environment credentials, Git configuration, credential helpers, filesystem repositories, or network state.
- Never import or call socket, HTTP, GraphQL, subprocess, Git, GitHub CLI, SDK, keyring, or provider code.
- Never merge, approve, deploy, publish, release, or spend.

## 6. Required checks

```text
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_connectivity_boundary tests.test_repository_registry tests.test_github_connector -v
python -m unittest discover -s tests -p 'test*.py' -v
git diff --check
```

The retained baseline is 456 passing tests from STUDIO-009A. Implementation must not reduce it.

Focused tests must cover every valid/invalid fixture, exact/nested allowlists, duplicate keys, JSON size/depth/Unicode/number safety, repository identity, URL pinning, access tiers, protected/default branch denial, path/ref scope, immutable revisions, classifications, instruction authority, control evidence, canonical digests, chronology, idempotency/replay, response mismatch, fake-transport call count, input immutability, and the complete no-external-activity boundary.

## 7. Review gates

Before merge, one immutable implementation head requires:

- Rules CI success;
- independent QA PASS;
- independent Review and Integration APPROVE;
- proof of the exact 24-path maximum scope;
- proof that no live transport, repository connection, credential, provider, network call, or spend was activated;
- Studio Owner merge decision.

Implementation and closeout use separate Pull Requests. No script or validator may merge either Pull Request.

## 8. Later-phase boundary

STUDIO-009B acceptance does not authorize credentials, live transport, webhooks, AI providers, routing, or connected execution. STUDIO-009C and every later phase require separate accepted contracts. Real GitHub activation remains gated by STUDIO-009C and STUDIO-009F.
