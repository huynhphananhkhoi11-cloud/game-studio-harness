# GAME AI Studio — Hierarchical Topology

## 1. Canonical scope

This document is the canonical home for the studio-wide organizational map, the relationships among its layers, and their high-level boundaries.

Detailed rules live in:

- [PLATFORM_STUDIO.md](PLATFORM_STUDIO.md) for shared-capability boundaries;
- [PROJECT_STUDIO_TEMPLATE.md](PROJECT_STUDIO_TEMPLATE.md) for isolated project containers;
- [CELL_MODEL.md](CELL_MODEL.md) for Cell formation and lifecycle;
- [EXPERT_GUILDS.md](EXPERT_GUILDS.md) for shared specialist pools;
- [ACTIVATION_POLICY.md](ACTIVATION_POLICY.md) for activation states and minimum-team logic;
- [STUDIO_CONSTITUTION.md](STUDIO_CONSTITUTION.md) for binding authority and governance;
- [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) for durable work transfer.

## 2. Architectural principles

`LARGE ORGANIZATION, SMALL ACTIVE TEAM`

The organization may define many available capabilities without keeping every role, Cell, or Guild active. Each outcome uses only the minimum sufficient team needed to produce it and apply risk-appropriate validation.

`AGENT ROLE != RUNTIME != MODEL != PROVIDER`

Organizational placement never permanently binds a logical role to an AI runtime, model, or provider.

## 3. Parent map

```text
GAME AI Studio
├── Platform Studio
├── Project Studios
│   └── Dynamic Cross-Functional Cells
└── Shared Expert Guilds
```

This is a capability topology, not a permanent staffing plan. The Studio Owner retains the final binding and non-reversible authority established by the Constitution; the map creates no additional executive layer.

## 4. Organizational relationships

| Component | Organizational purpose | High-level boundary | Canonical detail |
| --- | --- | --- | --- |
| GAME AI Studio | Parent layer for shared governance and organizational standards | Does not imply control by one agent instance | This file and the Constitution |
| Platform Studio | Supplies reusable capabilities and cross-project coordination | Has no binding governance authority and owns no project canon | `PLATFORM_STUDIO.md` |
| Project Studio | Isolates the context and state of one future project | Is a container, not an additional executive layer | `PROJECT_STUDIO_TEMPLATE.md` |
| Cell | Forms the smallest useful working unit around a bounded outcome | Uses only required roles and stays within accepted constraints | `CELL_MODEL.md` |
| Expert Guild | Makes specialist capability available across projects | Is a capability pool, not a mandatory active department | `EXPERT_GUILDS.md` |

The six STUDIO-002 profiles remain reusable logical roles. They may be activated in an appropriate organizational context without changing their existing missions, limits, or independence requirements.

## 5. High-level interaction model

1. A repository-visible task identifies a bounded outcome and its project or studio-wide scope.
2. The relevant container activates the minimum sufficient roles, forming a Cell only when coordinated multi-role work is useful.
3. Shared capabilities may be requested from the Platform layer, and specialist capability may be borrowed from a Guild.
4. Specialists may collaborate directly within scope. Producer / Coordination maintains visibility where coordination is needed but is not a universal proxy or approval gate.
5. Work ends with repository-visible evidence and a risk-appropriate handoff or review.
6. Roles and Cells deactivate when their current outcome no longer needs them.

Shared support does not transfer project-specific authority. Binding or non-reversible matters escalate through the Constitution to the Studio Owner.

## 6. Project isolation

Each Project Studio must be able to keep its own canon, accepted project decisions, architecture, tasks, assumptions, constraints, state, and code/content ownership separate from every other project.

Reusable evidence or infrastructure may cross project boundaries only when its scope and provenance are explicit. A project-specific rule does not become binding elsewhere merely because it uses shared infrastructure.

## 7. Continuity and failover compatibility

The topology is compatible with future runtime failover but does not implement it. Another suitable runtime must be able to occupy the same logical role from durable project evidence when the previous runtime is unavailable or unsuitable.

Continuity therefore depends on task contracts, accepted decisions, repository state, diffs, tests, handoffs, documented architecture, concise rationale, and evidence. Private chat history and private chain-of-thought are never required sources of project truth.

## 8. Authority boundaries

- The Studio Owner retains final binding and non-reversible authority.
- Organizational containers and capability pools do not create additional executive authority.
- Specialists and Cells may make reversible local choices inside accepted scope.
- Producer / Coordination manages visibility, priorities, dependencies, blockers, scheduling awareness, and low-risk resource coordination when needed.
- Direct specialist collaboration remains allowed.
- Governance gaps and binding trade-offs are surfaced, not silently settled by a support layer or specialist.

## 9. Non-goals

This topology does not select or install tools, providers, runtimes, models, dependencies, engines, languages, or frameworks. It does not implement routing or failover and does not define a real game, project, gameplay system, or canon.
