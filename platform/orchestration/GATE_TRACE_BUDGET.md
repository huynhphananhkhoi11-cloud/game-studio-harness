# Gate, Trace, Quota, and Budget Contract

STUDIO-007E provides a deterministic, read-only boundary for deciding whether an orchestration attempt may continue. Records contain safe references and digests only; credentials and secret-like values are rejected.

## Gate authority

| Gate | Required role |
|---|---|
| Scope, evidence, quota, secret safety, focused tests, regression | `ENGINEERING` |
| QA acceptance | `QA` |
| Review and integration | `REVIEW_INTEGRATION` |
| Owner decision | `STUDIO_OWNER` |

An evaluator ID identifies the actor. It never substitutes for the required role. Implementation work requires all technical gates plus QA and review gates to be `PASS`. The studio owner retains external merge authority.

## Immutable artifact identity

Every gate and trace event binds to the same repository, 40-character commit SHA, SHA-256 artifact digest, and sorted repository-relative changed-path set. Trace events form a consecutive, append-only chain using canonical SHA-256 predecessor digests.

## Zero-cost quota

Defaults are three attempts, 7,200 elapsed seconds, 25 changed paths, 2,097,152 output bytes, and zero monetary budget/spend. Only the studio owner may extend time, path, or output limits with a bounded, effective amendment. Attempts and money cannot be amended. Exceeding a limit produces `PAUSE`.

## Determinism and safety

Validation requires an explicit UTC `as_of` timestamp and never reads the system clock. The validator performs no network, provider, billing, Git, subprocess, or execution operation, and does not mutate its input.

## Commands

```text
python scripts/orchestration_gate_trace_budget.py validate-gate FILE --as-of TIMESTAMP
python scripts/orchestration_gate_trace_budget.py validate-budget FILE --as-of TIMESTAMP
python scripts/orchestration_gate_trace_budget.py validate-bundle FILE --as-of TIMESTAMP
python scripts/orchestration_gate_trace_budget.py evaluate-attempt FILE --as-of TIMESTAMP
python scripts/orchestration_gate_trace_budget.py explain-boundary
```
