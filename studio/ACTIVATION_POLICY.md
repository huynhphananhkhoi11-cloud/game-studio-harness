# Dynamic Activation Policy

## 1. Canonical scope

This document is the canonical home for role and Cell activation states, minimum-sufficient-team logic, and activation/deactivation conditions.

It governs organizational availability only. It does not implement model selection, provider routing, automatic failover, scheduling software, or infrastructure.

## 2. Core rule

`LARGE ORGANIZATION, SMALL ACTIVE TEAM`

Activate the minimum set of logical roles and Cells reasonably necessary to produce the bounded outcome, validate it at the required risk level, and preserve continuity. Organizational existence never implies current activity.

## 3. Activation states

| State | Meaning | Required durable evidence |
| --- | --- | --- |
| `INACTIVE` | Capability exists but has no current authorized work | Capability or role reference; no active task required |
| `READY` | Scope and prerequisites are sufficient for work to begin, but execution has not started | Task, accepted constraints, inputs, and intended handoff |
| `ACTIVE` | The role or Cell is currently executing a bounded task | Current task, responsible logical role(s), status, and changed-work boundary |
| `BLOCKED` | Safe progress cannot continue because a material dependency, conflict, evidence gap, or authority boundary is unresolved | Blocker, last safe state, impact, and unblock action |
| `HANDOFF` | Work and its durable state are being transferred for continuation, QA, review, or integration | Applicable LEVEL 0/1/2 handoff and receiving role |
| `COMPLETE` | The bounded work satisfies its completion conditions and required checks or verdicts are recorded | Deliverable, checks, verdicts, unresolved items, and next disposition |

These states do not create authority, employment, or permanent staffing. `COMPLETE` describes a task instance; the underlying capability may later return to `READY` or `INACTIVE` for different work.

## 4. Valid lifecycle

Typical transitions are:

```text
INACTIVE → READY → ACTIVE → HANDOFF → COMPLETE → INACTIVE
                     │          │
                     └→ BLOCKED ┘
```

Additional safe transitions are allowed when evidence supports them:

- `READY → INACTIVE` when the need is withdrawn before execution;
- `ACTIVE → COMPLETE` when no separate handoff is required;
- `BLOCKED → ACTIVE` when the recorded blocker is removed;
- `BLOCKED → HANDOFF` when another suitable role can continue;
- `HANDOFF → ACTIVE` when the receiver accepts and continues the same bounded work;
- `COMPLETE → READY` only for a distinct new task or explicitly reopened scope.

State changes must not conceal unfinished work or bypass required independent review.

## 5. Minimum-sufficient-team test

Before activation, answer in order:

1. What bounded outcome and canonical task authorize the work?
2. Which single specialty owns the core deliverable?
3. Does the outcome cross a real domain boundary requiring another specialty?
4. What validation is proportionate to the risk and acceptance criteria?
5. Is independent Review & Integration required by the task, governance, or integration risk?
6. Are dependencies complex enough to require Producer / Coordination?
7. Is scarce shared expertise better borrowed from a Guild than duplicated?
8. Can any proposed role remain inactive without reducing correctness, risk control, or delivery?

If the last answer is yes, keep that role inactive.

## 6. Activation conditions

A logical role or Cell may enter `READY` when:

- a repository-visible task or accepted work item exists;
- scope, non-goals, and canonical references are known;
- required inputs are available or explicitly marked unresolved;
- role boundaries and expected output are clear;
- project-specific context is correctly isolated;
- a handoff or completion target exists.

It enters `ACTIVE` only when work begins. Do not activate a role merely because its department, Guild, or profile exists.

## 7. Risk-appropriate validation

- A low-risk, reversible, single-domain task may need only the authoring specialist's deterministic checks.
- A task needing reproducible falsification adds QA without making QA the author of the same fix it certifies.
- A governance, architecture, integration, historical, or contract-required task adds an independent Review & Integration session.
- A binding or non-reversible trade-off escalates to the Studio Owner.

Review requirements do not make Producer / Coordination a universal approval gate.

## 8. Collaboration while active

Active specialists may communicate and hand off directly. Organizational visibility should be sufficient to expose dependencies and blockers without forcing all communication through one coordinator.

Add Producer / Coordination only when task decomposition, dependency management, scheduling awareness, resource conflict, blocker tracking, or multi-role handoff materially benefits from it.

## 9. Block, handoff, and failover compatibility

When work becomes `BLOCKED`, record the last safe state before reassigning or escalating. When entering `HANDOFF`, use [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) at the level appropriate to risk.

If a runtime is exhausted, unavailable, disabled, or unsuitable, stop safely and hand off. A different suitable runtime may later occupy the same logical role from repository-visible state. This policy does not choose that runtime or automate reassignment.

Private chat history and private chain-of-thought are not activation prerequisites.

## 10. Completion and deactivation

Enter `COMPLETE` only when the bounded outcome, deterministic checks, required QA/review verdicts, unresolved-item record, and downstream handoff are present as applicable.

Then deactivate roles and Cells that no longer have authorized work. Release borrowed Guild capability and unnecessary project context. Persistent activity requires a continuing bounded outcome or demonstrated coordination/context benefit.

## 11. Minimal activation record

Record only the fields necessary for reproducible continuation:

- task and parent scope;
- logical role or Cell;
- current state;
- bounded outcome and changed-work boundary;
- canonical constraints;
- dependencies and blockers;
- checks or verdicts;
- handoff target and next action.

Do not require meetings, daily ceremonies, permanent rosters, or private reasoning logs.

## 12. Runtime neutrality and non-goals

`AGENT ROLE != RUNTIME != MODEL != PROVIDER`

State applies to logical roles and Cells. It does not assign a runtime, model, provider, tool, engine, language, framework, credential, or dependency.
