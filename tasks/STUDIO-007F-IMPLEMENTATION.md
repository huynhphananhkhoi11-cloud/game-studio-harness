# STUDIO-007F-IMPLEMENTATION - Provider-neutral adapter v1.0

## 1. Purpose

Authorize one bounded, zero-cost implementation of normalized adapter request/result validation plus deterministic `manual` and `fake` adapters.

This document is an implementation contract, not runtime code. Its contract-only Pull Request must merge before any implementation path below is created.

## 2. Approval and baseline

- Status: APPROVED - IMPLEMENTATION NOT STARTED
- Approved by: Studio Owner
- Approval date: 2026-08-31
- Parent capability: `tasks/STUDIO-007F.md`
- Verified dependency baseline: STUDIO-007E closeout merge `2e0c661e438cc901e5a9f40e95357b2419e2665a`
- Contract branch: `agent/studio-007f-contract`
- Planned implementation branch: `agent/studio-007f-provider-adapter`
- Cost class: `ZERO_COST`

## 3. Normative semantics

### 3.1 Request

Schema v1 requests must use an exact allowlist and bind `request_id`, `work_order_id`, `attempt_number`, `adapter_type`, `capability_id`, `correlation_id`, immutable repository/artifact identity, safe input references, required gate/trace/budget evidence references, `created_at`, and caller-supplied `as_of`.

`adapter_type` is exactly `MANUAL` or `FAKE`. Missing fields, extra fields, duplicate identifiers, malformed references, future evidence, mismatched work-order/attempt/artifact lineage, an undeclared capability, or evidence that does not prove the required gates fail closed.

### 3.2 Capability

A capability record is an allowlisted declaration, not authority. It binds an ID and adapter type to accepted input/output kinds and one deterministic operation. v1.0 operations are limited to:

- `NORMALIZE_MANUAL_RESULT`
- `SIMULATE_SUCCESS`
- `SIMULATE_REFUSAL`
- `SIMULATE_TIMEOUT`
- `SIMULATE_FAILURE`

Capabilities cannot grant scope, gate approval, retry, failover, successor selection, merge, publication, deployment, credentials, network, or spend.

### 3.3 Result

Schema v1 results bind `result_id`, the exact request/work-order/attempt/adapter/capability/correlation/artifact identity, one terminal status, safe output and evidence references, integer usage counters, error class, optional handoff reference, and explicit completion time.

Statuses are `SUCCESS`, `REFUSED`, `TIMEOUT`, and `FAILURE`. Error classes are `NONE`, `REFUSAL`, `TIMEOUT`, `MALFORMED_OUTPUT`, and `ADAPTER_FAILURE`. `SUCCESS` requires `NONE`; all other statuses require their compatible non-`NONE` class. Monetary usage is always zero.

Results do not approve quality gates or authorize continuation. Any result may still be rejected by later gate, quota, QA, review, or Owner evidence.

### 3.4 Adapter behavior

- `manual` only validates and normalizes caller-supplied evidence; it performs no work.
- `fake` chooses an outcome only from the declared fixture scenario and returns canonical deterministic bytes for identical canonical inputs.
- Neither adapter reads environment credentials, system time, network state, provider configuration, Git state, or hidden files.
- Neither adapter invokes subprocesses, network APIs, SDKs, billing, or repository mutations.
- Inputs remain byte-for-byte unchanged after both success and failure.

### 3.5 Security and provider neutrality

Secret-like field names or credential-bearing values, private-key material, bearer authorization, access/refresh tokens, passwords, session cookies, embedded authentication, provider/model/account/endpoint fields, network capabilities, and nonzero monetary values fail closed.

Provider-specific extension fields are not reserved in v1.0. A future real provider requires a new owner-accepted contract and cannot enter through fixture or configuration substitution.

## 4. Exact implementation scope

The implementation branch may create exactly these nineteen paths:

1. `platform/orchestration/PROVIDER_ADAPTER.md`
2. `platform/orchestration/schemas/adapter-request.schema.json`
3. `platform/orchestration/schemas/adapter-result.schema.json`
4. `platform/orchestration/schemas/adapter-capability.schema.json`
5. `platform/orchestration/fixtures/007f/manual/valid-request.json`
6. `platform/orchestration/fixtures/007f/manual/valid-success-result.json`
7. `platform/orchestration/fixtures/007f/manual/valid-refusal-result.json`
8. `platform/orchestration/fixtures/007f/fake/valid-success-result.json`
9. `platform/orchestration/fixtures/007f/fake/valid-timeout-result.json`
10. `platform/orchestration/fixtures/007f/fake/valid-failure-result.json`
11. `platform/orchestration/fixtures/007f/invalid-undeclared-capability.json`
12. `platform/orchestration/fixtures/007f/invalid-scope-expansion.json`
13. `platform/orchestration/fixtures/007f/invalid-mismatched-correlation.json`
14. `platform/orchestration/fixtures/007f/invalid-provider-field.json`
15. `platform/orchestration/fixtures/007f/invalid-credential-field.json`
16. `platform/orchestration/fixtures/007f/invalid-network-capability.json`
17. `platform/orchestration/fixtures/007f/invalid-malformed-result.json`
18. `scripts/orchestration_provider_adapter.py`
19. `tests/test_orchestration_provider_adapter.py`

The implementation may also materially update only these four existing memory paths:

- `studio/memory/tasks/STUDIO-007F/TASK.md`
- `studio/memory/tasks/STUDIO-007F/STATE.md`
- `studio/memory/tasks/STUDIO-007F/WORKLOG.md`
- `studio/memory/tasks/STUDIO-007F/RESUME.md`

Maximum implementation Pull Request scope: 23 changed paths. Any additional path requires a new accepted contract.

## 5. Required validation

Focused tests must cover exact schema allowlists; canonical serialization; request/result/capability identity; capability declaration; manual normalization; fake determinism; all terminal statuses; status/error compatibility; correlation and artifact lineage; gate/trace/budget evidence linkage; safe references; zero monetary usage; secret/provider/network rejection; input immutability; future-time rejection; no system clock; and prohibition of network, SDK, subprocess, Git, credential, approval, merge, and execution behavior.

The implementation must run:

```text
python -m prototype.rules.cli validate-data --data-dir data/vertical_slice
python -m unittest tests.test_orchestration_provider_adapter -v
python -m unittest discover -s tests -p 'test*.py' -v
git diff --check
```

The retained baseline is 252 passing tests from STUDIO-007E. Implementation must not reduce this count, and all newly added focused tests must pass.

## 6. Review gates

Before merge, one immutable implementation head requires:

- Rules CI success;
- independent QA PASS;
- independent Review and Integration APPROVE;
- proof of exact 23-path maximum scope and zero-cost/provider-neutral behavior;
- Studio Owner merge decision.

Implementation and closeout use separate Pull Requests. No script in this package merges either Pull Request.

## 7. Real-provider change control

Any real provider, model, endpoint, account, SDK, credential, network access, paid quota, billing integration, hosted telemetry, or production execution requires a separate contract containing ownership, threat review, credential lifecycle, least privilege, budget ceilings, data handling, test plan, incident response, and rollback.
