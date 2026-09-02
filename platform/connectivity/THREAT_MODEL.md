# STUDIO-009A Threat Model

## Trust zones

- `OWNER_CONTROL`: accepted decisions, contracts, and Owner gates.
- `STUDIO_CONTROL_PLANE`: queue, dispatch, claims, gates, trace, budget, adapter normalization, and boundary validation.
- `REPOSITORY_CONTENT`: repository and collaboration content; untrusted for instruction authority by default.
- `EXECUTION_SANDBOX`: future isolated runner/worktree with bounded paths, commands, and network.
- `EXTERNAL_PROVIDER`: future separately contracted provider boundary.
- `SECRET_STORE`: future external secret store; secret values never enter boundary evidence.

## Required threats

Every assessment contains each ID exactly once:

| Threat ID | Risk | Minimum control intent |
| --- | --- | --- |
| `T-PROMPT-INJECTION` | Repository content attempts to override accepted authority | Instruction-authority classification; untrusted-content default; no free-form authority |
| `T-SECRET-LEAKAGE` | Secret appears in prompt, result, log, diff, exception, or evidence | Reference-only credentials; recursive secret rejection; revocation in later phase |
| `T-UNAUTHORIZED-WRITE` | Write outside repo/path/tier or to default branch | Registry boundary; writer claim; isolated worktree; Owner gate |
| `T-SUPPLY-CHAIN-EXECUTION` | Repository or tool content triggers code | No execution in 009A; later pinned dependency and sandbox controls |
| `T-COST-RUNAWAY` | Retry/context/call creates unapproved spend | Integer-zero ceiling; later reservation and settlement controls |
| `T-DUPLICATE-WORK` | Two writers or outputs race | Single writer claim; attempt identity; idempotency; durable handoff |
| `T-WEBHOOK-SPOOF-REPLAY` | Forged or replayed external event | No webhook in 009A; later signature and delivery replay controls |
| `T-PROVIDER-IDENTITY-CONFUSION` | Model/provider self-identifies or changes capability | Accepted profile reference and validated transport metadata only |
| `T-OWNER-GATE-BYPASS` | AI/router merges or approves itself | Owner decision remains outside provider authority |

## Assessment semantics

Each threat decision is exactly `MITIGATED` or `NOT_APPLICABLE`, with one or more stable control IDs and evidence references. `ACCEPTED_RISK`, waiver text, missing or duplicate threats, missing evidence, unknown zones, extra fields, digest mismatch, and future-dated assessment fail closed.

An assessment is valid only when its boundary ID and canonical boundary digest match a separately valid boundary record. Validation does not mean the integration is activated; it means the supplied design evidence is internally consistent under STUDIO-009A.
