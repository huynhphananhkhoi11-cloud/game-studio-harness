# Project Studio — Reusable Template

## 1. Purpose

A Project Studio is an isolated organizational container for one future project. This template records the minimum durable context needed to organize work without creating a new executive role or binding a logical role to a runtime.

Copy and complete this template only under a future project-creation task. Do not treat placeholders as accepted project truth.

## 2. Identity

- `project_studio_id`: `<UNASSIGNED>`
- `project_name`: `<UNASSIGNED>`
- `status`: `<PROPOSED | READY | ACTIVE | BLOCKED | HANDOFF | COMPLETE | INACTIVE>`
- `repository_or_namespace`: `<UNASSIGNED>`
- `created_from_task`: `<TASK-ID>`
- `binding_authority_reference`: `studio/STUDIO_CONSTITUTION.md`

The container does not create an additional owner-level or executive position. Final binding and non-reversible authority remains with the Studio Owner.

## 3. Project scope

### Intended outcome

`<Describe the bounded purpose of this project without inventing unaccepted canon.>`

### In scope

- `<PROJECT-SPECIFIC ITEM>`

### Out of scope

- `<EXPLICIT NON-GOAL>`

### Completion boundary

`<State how the Project Studio knows its organizational purpose is complete or inactive.>`

## 4. Project-specific references

| Reference type | Canonical repository path or identifier | Status |
| --- | --- | --- |
| Task contracts | `<PATH>` | `<PROPOSED / ACCEPTED / SUPERSEDED>` |
| Game/project vision | `<PATH>` | `<STATUS>` |
| Accepted project decisions | `<PATH>` | `<STATUS>` |
| Canon or content authority | `<PATH OR NOT APPLICABLE>` | `<STATUS>` |
| Project architecture | `<PATH>` | `<STATUS>` |
| Assumptions and unresolved items | `<PATH>` | `<STATUS>` |
| Tests and evidence | `<PATH>` | `<STATUS>` |
| Handoffs | `<PATH OR WORKFLOW LOCATION>` | `<STATUS>` |

Repository-visible references are the source of continuity. Private conversation history and private chain-of-thought are not required inputs.

## 5. Project-specific state

| State category | Canonical location | Isolation rule |
| --- | --- | --- |
| Canon | `<PATH>` | Does not bind another project |
| Accepted project decisions | `<PATH>` | Applies only within declared scope |
| Architecture | `<PATH>` | Shared only through explicit reuse |
| Tasks and milestones | `<PATH>` | Namespaced to this project |
| Assumptions / unresolved | `<PATH>` | Provenance remains attached |
| Constraints | `<PATH>` | Not inherited by another project implicitly |
| Code/content ownership | `<PATH OR RULE>` | Boundary is explicit |
| Current operational state | `<PATH>` | Updated through durable handoff |

## 6. Active Cells

Use [CELL_MODEL.md](CELL_MODEL.md) and [ACTIVATION_POLICY.md](ACTIVATION_POLICY.md). Do not create a Cell merely to mirror a permanent department.

| Cell ID | Bounded outcome | Required logical roles | State | Handoff target | Completion condition |
| --- | --- | --- | --- | --- | --- |
| `<CELL-ID>` | `<OUTCOME>` | `<MINIMUM SUFFICIENT SET>` | `<STATE>` | `<TARGET>` | `<CONDITION>` |

## 7. Borrowed Guild capabilities

Use [EXPERT_GUILDS.md](EXPERT_GUILDS.md). Record capabilities rather than permanent staffing commitments.

| Guild or capability | Need | Scope and duration | Project context exposed | Return condition |
| --- | --- | --- | --- | --- |
| `<CAPABILITY>` | `<JUSTIFICATION>` | `<BOUNDARY>` | `<MINIMUM NECESSARY CONTEXT>` | `<HANDOFF / COMPLETE / RELEASE>` |

Borrowed specialists work within this project's accepted constraints. Participation does not make shared infrastructure or another project authoritative here.

## 8. Platform capabilities used

Use [PLATFORM_STUDIO.md](PLATFORM_STUDIO.md). Listing a capability here does not select an implementation.

| Capability category | Bounded use | Project data boundary | Exit or replacement condition |
| --- | --- | --- | --- |
| `<CATEGORY>` | `<USE>` | `<BOUNDARY>` | `<CONDITION>` |

## 9. Project constraints

### LOCKED

- `<ACCEPTED CONSTRAINT AND CANONICAL REFERENCE>`

### GUIDED

- `<INTENT WITH LOCAL REVERSIBLE FREEDOM>`

### OPEN

- `<UNDECIDED AREA AVAILABLE FOR RESEARCH OR PROPOSAL>`

### Explicit exclusions

- `<PROHIBITED OR DEFERRED ITEM>`

## 10. Interaction and authority

- The six STUDIO-002 profiles remain valid and retain their existing boundaries.
- Specialists may collaborate directly across roles when useful.
- Producer / Coordination is activated only when coordination load justifies it and is not a universal gate.
- Reversible, local, in-scope choices stay with the responsible specialist or Cell.
- Binding or non-reversible matters escalate to the Studio Owner.
- Review independence follows the Constitution and the existing Review & Integration profile.

## 11. Isolation and reuse checklist

- [ ] Project-specific state has a declared canonical location.
- [ ] No state from another project is silently binding here.
- [ ] Shared evidence retains provenance and scope.
- [ ] Shared capabilities receive only necessary project context.
- [ ] Cross-project reuse is explicit and reversible where practical.
- [ ] Runtime replacement can resume from repository-visible evidence.

## 12. Non-goals of this template

This template does not create a real or fictional game, canon, engine, language, framework, dependency, provider assignment, runtime-routing rule, staffing commitment, or additional executive authority.
