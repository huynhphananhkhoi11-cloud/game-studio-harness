# STUDIO-009A-IMPLEMENTATION - Deterministic integration-boundary validator

## 1. Purpose

Authorize one deterministic, read-only validator for the STUDIO-009A integration boundary and threat model.

This document is an implementation contract, not runtime connection code. Its contract-only Pull Request must merge before any implementation path below is created.

## 2. Approval and baseline

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-09-01
- Parent capability: `tasks/STUDIO-009A.md`
- Verified dependency baseline: STUDIO-008 closeout merge `d69a613dc50b59dcded83189d38d5e86ff9d70e6`
- Contract branch: `agent/studio-009a-contract`
- Planned implementation branch: `agent/studio-009a-boundary-validator`
- Cost class: `ZERO_COST`
- External activity: `NONE`

## 3. Normative records

### 3.1 Integration boundary record

Schema v1 uses an exact allowlist and binds:

- `schema_version`, `boundary_id`, `task_id`, `created_at`, and caller-supplied `as_of`;
- `repository` with stable `repository_id`, immutable `revision`, `access_tier`, normalized `allowed_paths`, normalized `denied_paths`, and a safe `auth_profile_ref` only;
- `data_policy` with allowed classifications and explicit instruction-authority paths;
- `provider_request` with a generic capability ID, data classification, and a provider-profile reference only;
- `control_evidence` references for queue, dispatch, writer claim when write-capable, gate, trace, quota/budget, adapter, Owner approval, and threat assessment;
- `money_ceiling` fixed to integer zero for this phase;
- `canonical_digest` computed from all other allowlisted fields.

The record contains no URL with embedded authentication, endpoint, account, model-generated provider identity, credential value, token, secret, environment variable, or free-form extension map.

### 3.2 Threat assessment record

Schema v1 binds one boundary digest to an exact set of assessed threats. Every required threat has a stable ID, zone transition, decision, controls, and evidence references.

Required threat IDs:

- `T-PROMPT-INJECTION`
- `T-SECRET-LEAKAGE`
- `T-UNAUTHORIZED-WRITE`
- `T-SUPPLY-CHAIN-EXECUTION`
- `T-COST-RUNAWAY`
- `T-DUPLICATE-WORK`
- `T-WEBHOOK-SPOOF-REPLAY`
- `T-PROVIDER-IDENTITY-CONFUSION`
- `T-OWNER-GATE-BYPASS`

Each decision is exactly `MITIGATED` or `NOT_APPLICABLE`. `ACCEPTED_RISK`, free-form waivers, missing threats, duplicate threats, or evidence-free mitigation fail closed.

### 3.3 Validation result

The validator returns a new normalized result containing a stable status, error codes, canonical boundary digest, canonical threat digest, and validated identity references. It never returns or logs input secrets and never mutates input objects or fixture bytes.

## 4. Exact implementation scope

The future implementation branch may create exactly these nineteen paths:

1. `platform/connectivity/CONNECTION_BOUNDARY.md`
2. `platform/connectivity/THREAT_MODEL.md`
3. `platform/connectivity/schemas/integration-boundary.schema.json`
4. `platform/connectivity/schemas/threat-assessment.schema.json`
5. `platform/connectivity/fixtures/009a/valid-read-only-boundary.json`
6. `platform/connectivity/fixtures/009a/valid-branch-write-boundary.json`
7. `platform/connectivity/fixtures/009a/valid-threat-assessment.json`
8. `platform/connectivity/fixtures/009a/invalid-prompt-injection.json`
9. `platform/connectivity/fixtures/009a/invalid-secret-field.json`
10. `platform/connectivity/fixtures/009a/invalid-path-traversal.json`
11. `platform/connectivity/fixtures/009a/invalid-default-branch-write.json`
12. `platform/connectivity/fixtures/009a/invalid-provider-identity.json`
13. `platform/connectivity/fixtures/009a/invalid-nonzero-budget.json`
14. `platform/connectivity/fixtures/009a/invalid-missing-control-evidence.json`
15. `platform/connectivity/fixtures/009a/invalid-missing-threat.json`
16. `platform/connectivity/fixtures/009a/invalid-extra-field.json`
17. `scripts/connectivity_boundary.py`
18. `tests/test_connectivity_boundary.py`
19. `platform/connectivity/fixtures/009a/README.md`

The implementation may also materially update only these four existing memory paths:

- `studio/memory/tasks/STUDIO-009A/TASK.md`
- `studio/memory/tasks/STUDIO-009A/STATE.md`
- `studio/memory/tasks/STUDIO-009A/WORKLOG.md`
- `studio/memory/tasks/STUDIO-009A/RESUME.md`

Maximum implementation Pull Request scope: 23 changed paths. Renames, generated files, binary files, dependency changes, workflow changes, and changes outside this list are prohibited.

## 5. Required validation behavior

- Reject missing and extra fields at every controlled object level.
- Reject secret-like keys and credential-bearing values recursively.
- Normalize and validate repository-relative POSIX paths; reject absolute paths, `..`, empty segments, backslashes, control characters, and denied-path overlap.
- Require `READ_ONLY` when no valid writer-claim evidence exists; write tiers require writer-claim, worktree, and Owner evidence references.
- Reject default-branch, admin, settings, deletion, workflow, deployment, publication, and release authority.
- Validate all required threat IDs exactly once and bind them to the canonical boundary digest.
- Require all money fields to be integer zero; booleans are not valid integers.
- Validate ISO 8601 UTC chronology using caller-supplied `as_of`; never read the system clock.
- Canonicalize JSON before SHA-256 hashing and prove key-order-stable results.
- Leave caller objects and fixture bytes unchanged on success and failure.
- Produce stable error codes without echoing secret-bearing values.

## 6. Required checks

The implementation must run:

```text
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_connectivity_boundary -v
python -m unittest discover -s tests -p 'test*.py' -v
git diff --check
```

The retained baseline is 397 passing tests from STUDIO-008. Implementation must not reduce this count.

Focused tests must cover every valid and invalid fixture, exact allowlists, nested allowlists, path normalization and overlap, classifications, instruction authority, threat completeness, control evidence, digest stability, chronology, zero-cost typing, secret rejection, input immutability, no clock, no subprocess, no Git, no filesystem mutation, no network, and no provider/credential activity.

## 7. Review gates

Before merge, one immutable implementation head requires:

- Rules CI success;
- independent QA PASS;
- independent Review and Integration APPROVE;
- proof of the exact 23-path maximum scope;
- proof that no repository, credential, provider, network, or spend was activated;
- Studio Owner merge decision.

Implementation and closeout use separate Pull Requests. No script or validator may merge either Pull Request.

## 8. Later-phase boundary

STUDIO-009A acceptance does not authorize STUDIO-009B through STUDIO-009F. Each later phase requires a separate accepted contract. Every real provider additionally requires its own `STUDIO-009P*` child contract with provider identity, threat review, credential lifecycle, data policy, budget, incident response, tests, and rollback.
