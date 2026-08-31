# Provider-neutral adapter v1.0

STUDIO-007F defines a deterministic evidence boundary between validated orchestration records and an executor-shaped adapter. It does not connect an executor or provider.

## Authority boundary

Adapter records never grant authority. An adapter cannot change work-order scope, approve a gate, select a successor, retry, fail over, merge, publish, deploy, reveal credentials, use a network, or authorize spend. Results remain subject to STUDIO-007E gates, QA, Review and Integration, and the Studio Owner.

## Supported adapters

### MANUAL

`MANUAL` with `NORMALIZE_MANUAL_RESULT` validates and canonicalizes a result supplied by a human-controlled process. It performs no underlying work and has no hidden fallback.

### FAKE

`FAKE` accepts exactly one declared simulation operation: success, refusal, timeout, or failure. Its result is derived only from canonical request/capability bytes and caller-supplied `as_of`. Identical inputs produce identical canonical output. It never sleeps or consults the system clock.

## Records

### Capability

A capability declares one adapter type, one operation, accepted reference kinds, produced reference kinds, deterministic behavior, `ZERO_COST`, `network_access: false`, and an empty authority list. It is evidence of an allowlist, not actor authentication.

The runtime enforces that allowlist: every request input must map to a declared input kind, every capability must declare `RESULT_REFERENCE`, and a non-null handoff requires `HANDOFF_REFERENCE`.

### Request

A request binds one work order and attempt to:

- a declared adapter capability;
- one correlation ID;
- immutable repository, commit, and artifact digest identity;
- safe input references;
- scope, integrity, quota, and secret-safety gate references;
- trace and budget references;
- explicit creation and `as_of` times.

The `as_of` value is supplied by the caller and must match the request. Validation never reads current time.

`trace_reference` is bound to the request correlation ID and `budget_reference` is bound to the work-order ID. A safe-looking reference for another identity fails closed.

### Result

A result repeats the exact request identity and records one terminal status:

| Status | Compatible error class |
| --- | --- |
| `SUCCESS` | `NONE` |
| `REFUSED` | `REFUSAL` |
| `TIMEOUT` | `TIMEOUT` |
| `FAILURE` | `MALFORMED_OUTPUT` or `ADAPTER_FAILURE` |

Success requires output evidence. Non-success results cannot claim output references. Usage counters must agree with the records, remain within the inherited 2 MiB output ceiling, and keep monetary usage at zero.

## Safe references

Only normalized references using `artifact`, `evidence`, `gate`, `trace`, `budget`, `handoff`, or `fixture` schemes are accepted. URLs, traversal, backslashes, query strings, fragments, control characters, secrets, provider fields, account fields, endpoint fields, and model fields are rejected.

## Determinism and immutability

- Canonical JSON uses UTF-8, sorted keys, and compact separators.
- Digests are lowercase SHA-256 with a `sha256:` prefix.
- Validation and simulation use deep-copy checks to prove inputs remain unchanged.
- JSON loading rejects duplicate keys, hidden input files, oversized input, and non-canonical timestamps.
- A supplied `FAKE` result must byte-match the result derived from its declared operation; changing its status, identity, evidence, counters, or output is rejected.
- No subprocess, network library, provider SDK, Git command, environment credential, filesystem write, or billing call is used.

## CLI

```text
python scripts/orchestration_provider_adapter.py validate-bundle --input <fixture.json> --as-of <UTC-Z>
python scripts/orchestration_provider_adapter.py normalize-manual --input <fixture.json> --as-of <UTC-Z>
python scripts/orchestration_provider_adapter.py run-fake --input <fixture.json> --as-of <UTC-Z>
python scripts/orchestration_provider_adapter.py digest --input <fixture.json>
```

All successful output is canonical JSON on stdout. Contract violations return exit code 1 and a bounded error on stderr.

## Real-provider prohibition

Provider names, models, endpoints, accounts, credentials, tokens, network access, paid quota, billing, and hosted execution are outside v1.0. A real provider requires a separately owner-accepted contract, threat review, credential lifecycle, budget controls, focused and regression tests, incident response, and rollback.
