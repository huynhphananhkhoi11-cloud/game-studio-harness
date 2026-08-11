# Shared Expert Guilds

## 1. Canonical scope

This document is the canonical home for shared specialist pooling, Guild creation criteria, borrowing and return, project interaction, and inactive conditions.

## 2. Definition

An Expert Guild is a shared capability pool for expertise that is valuable across multiple projects or outcomes but does not need to be duplicated inside every Project Studio or Cell.

A Guild may represent available capability while every associated role is inactive. It is not automatically a department, permanent team, management layer, or executive authority.

Possible future capability areas include historical research, systems design, architecture, performance, accessibility, security, localization, specialist QA, and other high-skill or low-frequency work. This list does not create or activate any Guild.

## 3. When specialist pooling is justified

Pooling is justified when at least one material benefit exists:

- multiple projects need the same scarce expertise;
- the capability has a low duty cycle and permanent duplication would waste resources;
- consistent specialist methods improve correctness or risk control;
- project teams need occasional independent domain review;
- shared learning can be generalized without leaking project-specific state;
- repeated onboarding cost is materially reduced.

Prefer an existing operational role or time-bounded specialist assignment when a separate pool would add no useful capability.

## 4. Criteria for creating a new Guild

A proposal for a new Guild must identify:

- the capability gap;
- evidence of recurring or material demand;
- why existing roles or Cells are insufficient;
- intended project interactions;
- knowledge and project-isolation boundaries;
- activation and inactivity conditions;
- expected reusable outputs, if any;
- overlap with existing Guilds or Platform capabilities;
- rollback or retirement condition.

Creation follows existing governance. A label on an organization chart does not establish a Guild by itself.

## 5. Borrowing a capability

A Project Studio or Cell requests a capability using a bounded record containing:

- requesting project and task;
- capability needed and why;
- required logical role or expertise;
- accepted constraints and relevant canonical references;
- minimum necessary project context;
- deliverable and evidence expectations;
- start, duration, or completion condition;
- handoff and reviewer requirements.

Borrowing activates only the required capability. It does not transfer the whole Guild into the requesting project and does not permanently assign a person, agent, runtime, model, or provider.

## 6. Working relationship

A borrowed specialist:

- works within the requesting task and Project Studio constraints;
- may collaborate directly with Cell members;
- makes only reversible local choices allowed by the applicable role profile;
- preserves evidence provenance and uncertainty;
- receives only context necessary for the outcome;
- returns a repository-visible deliverable and handoff.

The requesting Project Studio retains its project-specific canon and state. The Guild does not become authoritative over the project merely because its expertise is shared.

Producer / Coordination may help with availability, conflicts, blockers, and handoff visibility when coordination load warrants it. It is not a universal request gate.

## 7. Return and release

Return occurs when the requested outcome is complete, blocked beyond the agreed boundary, superseded, or no longer needed.

The return record should include:

- deliverable and checks;
- evidence and concise rationale needed downstream;
- unresolved items and residual risks;
- reusable generic learning, clearly separated from project-specific state;
- next action or receiving role;
- release of project context or access no longer needed.

The logical capability then returns to `READY` or `INACTIVE` under [ACTIVATION_POLICY.md](ACTIVATION_POLICY.md).

## 8. Reuse and project isolation

Guilds may curate generic, non-binding methods, checklists, benchmarks, or evidence indexes when a scoped task authorizes them. Reusable material must retain provenance, limitations, and applicability.

Do not move project canon, accepted project constraints, confidential project context, or binding project state into a shared pool merely for convenience. Shared learning becomes applicable to another project only through explicit evaluation and adoption under that project's scope.

## 9. Conditions for remaining inactive

A Guild remains `INACTIVE` when:

- no current task requires its capability;
- demand is speculative or too low to justify activation;
- an existing role can handle the need without material loss;
- required scope, evidence, or access is missing;
- activation would create unnecessary staffing or ceremony;
- project-isolation risk is not adequately bounded.

An inactive Guild is still an available organizational capability. Inactivity is not failure.

## 10. Authority and runtime neutrality

Guilds do not create binding governance, own project canon, impose shared recommendations on projects, or grant members broader authority than their logical role profiles.

`AGENT ROLE != RUNTIME != MODEL != PROVIDER`

This model does not assign or route runtimes, models, or providers and does not install tools or dependencies.
