# Platform Studio

## 1. Canonical scope

This document defines the mission, shared-capability boundary, coordination responsibilities, and authority limits of the Platform Studio.

It defines an organizational layer only. It does not select implementations or activate permanent staff.

## 2. Mission

The mission is to make reusable capabilities available across GAME AI Studio while reducing duplicated infrastructure and preserving Project Studio isolation.

The layer exists to coordinate, facilitate, analyze, recommend, and surface gaps. It is not an executive body. Binding and non-reversible matters go to the Studio Owner under [STUDIO_CONSTITUTION.md](STUDIO_CONSTITUTION.md).

## 3. Possible capability categories

Future shared capabilities may include:

- runtime, model, and provider registry support;
- persistent project-memory infrastructure;
- task and handoff infrastructure;
- Git and GitHub workflow support;
- architecture maps;
- benchmarking and evaluation;
- tool and MCP integration;
- routing and failover infrastructure;
- shared automation;
- common development infrastructure.

These are capability categories, not adopted tools or implementation commitments. Any future implementation requires its own scoped task and applicable governance.

## 4. Allowed coordination responsibilities

The layer may:

- maintain visibility over shared-capability demand and capacity;
- coordinate cross-project dependencies and low-risk shared resources;
- identify duplication or compatibility risk;
- analyze trade-offs and recommend options;
- facilitate reuse of approved generic infrastructure or evidence;
- help Project Studios locate an appropriate shared capability or Guild;
- surface governance gaps, project-state leakage, or unresolved conflicts;
- support repository-visible handoffs and continuity.

These actions remain advisory or facilitative unless an existing accepted rule explicitly delegates a reversible in-scope action.

## 5. Authority limits

This layer must not:

- exercise final binding or non-reversible authority;
- settle governance disputes on its own;
- own or silently change project canon;
- impose one project's constraints or state on another;
- turn recommendations into accepted cross-project rules by implication;
- replace the Studio Owner;
- become a universal gate for specialist collaboration;
- grant itself broader authority because it supplies shared infrastructure.

When coordination exposes a binding trade-off, record the options, impact, evidence, and unresolved issue, then escalate it through the Constitution.

## 6. Interaction with Project Studios

A Project Studio may request shared support using a bounded, repository-visible request that identifies:

- the project identity and task;
- the required capability;
- relevant constraints and access boundaries;
- expected output and handoff;
- duration or completion condition;
- risks to project isolation.

The requesting Project Studio keeps its project-specific state and canon. Shared support receives only the context reasonably necessary for the task and returns evidence through the applicable handoff level.

## 7. Interaction with Expert Guilds

The Platform layer may help expose demand, capacity, or cross-project scheduling conflicts for Guild capabilities. Borrowing and return rules remain canonical in [EXPERT_GUILDS.md](EXPERT_GUILDS.md).

Guild participation does not transfer project authority to the shared layer, and generic infrastructure support does not convert a Guild into permanent staff.

## 8. Staffing and activation

This layer may remain partly or entirely inactive when no shared outcome requires work. Roles activate under [ACTIVATION_POLICY.md](ACTIVATION_POLICY.md), using the minimum sufficient team.

Producer / Coordination may maintain visibility when dependencies justify it. Specialists may still communicate directly, and no coordinator is required solely because this layer exists.

## 9. Runtime neutrality and non-goals

Logical responsibilities remain independent of runtime, model, and provider. This document does not assign models, create credentials, adopt dependencies, install tools, implement routing or automatic failover, or select development technology.
