# Dynamic Cross-Functional Cell Model

## 1. Canonical scope

This document is the canonical home for Cell purpose, formation, composition, lightweight operation, handoff, completion, and dissolution.

Activation-state definitions remain canonical in [ACTIVATION_POLICY.md](ACTIVATION_POLICY.md). Shared handoff formats remain canonical in [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md).

## 2. Definition and purpose

A Cell is a small working unit formed around one concrete, bounded outcome. It may address a feature, subsystem, milestone, content stream, research question, integration task, or another clearly defined result.

A Cell is cross-functional only when the outcome needs multiple specialties. It is not a permanent department, an authority tier, or a reason to activate every available role.

## 3. Formation criteria

Form a Cell when all of the following are true:

1. A repository-visible task defines a bounded outcome and acceptance criteria.
2. Coordinated work by two or more specialties materially improves delivery, correctness, or risk control; otherwise assign the task directly to one role.
3. The relevant project or studio-wide scope is explicit.
4. Accepted constraints and canonical references are identifiable.
5. The expected handoff, reviewer need, and completion condition are known or explicitly marked unresolved.

Do not form a Cell solely to imitate a department chart, add ceremony, or keep idle roles busy.

## 4. Formation record

A Cell record should contain only what downstream work needs:

- `cell_id`;
- bounded outcome;
- parent scope: Project Studio or studio-wide task;
- task contract and canonical references;
- required logical roles;
- current state;
- accepted constraints and non-goals;
- deliverables and acceptance criteria;
- dependency or blocker list;
- handoff and reviewer target;
- completion and dissolution condition.

The record must not permanently assign a runtime, model, or provider to a logical role.

## 5. Minimum composition

Use the minimum sufficient team:

- one responsible specialist may be enough for a single-domain, low-risk outcome;
- add a second specialty only when the outcome crosses a real domain boundary;
- add QA when acceptance needs reproducible falsification beyond the author's checks;
- add independent Review & Integration when risk, governance, integration, or the task contract requires it;
- add Producer / Coordination only when dependency load, scheduling, blockers, or multi-role visibility justify it;
- borrow a Guild capability only when required expertise is scarce, specialized, or inefficient to duplicate.

The six STUDIO-002 profiles remain unchanged. Cell membership is a temporary task assignment, not a new role or promotion.

## 6. Lightweight operating loop

1. Confirm outcome, scope, canonical references, and acceptance criteria.
2. Activate only required roles under the activation policy.
3. Work directly across specialties where useful.
4. Keep decisions, evidence, diffs, tests, blockers, and current state repository-visible at the handoff level appropriate to risk.
5. Stop or enter `BLOCKED` when proceeding would violate scope or require unresolved binding authority.
6. Produce the bounded deliverable and deterministic checks.
7. Enter `HANDOFF` for required QA, review, or downstream integration.
8. Enter `COMPLETE`, then dissolve or become `INACTIVE` when no continuing outcome justifies activity.

No daily meeting, recurring ceremony, or mandatory reporting ladder is implied.

## 7. Collaboration

Cell members may collaborate directly, including Design with Engineering, Design with Narrative, Engineering with QA, and Research with Review.

Producer / Coordination may maintain visibility over priorities, dependencies, blockers, scheduling awareness, and low-risk resource coordination. It is not the mandatory channel for specialist communication and does not replace specialist authority inside accepted scope.

When roles disagree, use accepted constraints, deterministic evidence, domain evidence, and risk-appropriate review. Binding or non-reversible trade-offs go to the Studio Owner.

## 8. Blocked state

A Cell enters `BLOCKED` when a missing input, contradictory accepted rule, unavailable required capability, scope violation, unresolved evidence problem, or binding trade-off prevents safe progress.

The Cell must record:

- what is blocked;
- the last safe completed state;
- affected deliverables;
- evidence or reproduction where applicable;
- who or what can unblock it;
- the smallest useful next action.

Being blocked does not authorize silent scope expansion or weakened acceptance criteria.

## 9. Handoff

Use LEVEL 0, 1, or 2 from the existing handoff protocol based on risk. A Cell handoff identifies the Cell, task, parent scope, changed artifacts, checks, decisions or assumptions, blockers, remaining work, and next recipient.

Private chain-of-thought is never required. Another suitable runtime must be able to resume a logical role from the task, repository state, evidence, and handoff.

## 10. Completion

A Cell may enter `COMPLETE` when:

- its bounded deliverable exists;
- acceptance checks have run and results are visible;
- required QA or independent review has a recorded verdict;
- unresolved items and residual risks are explicit;
- project-specific state remains in its correct namespace;
- a downstream handoff exists when needed.

Completion of a Cell does not itself accept a binding change or authorize merge.

## 11. Dissolution, inactivation, and persistence

After completion, dissolve the working unit or mark it `INACTIVE`. Release borrowed Guild capability and remove project context that is no longer required.

A Cell may persist across multiple tasks only when a continuing bounded outcome, stable coordination need, or material context cost justifies it. Persistence must not become permanent staffing by default.

Reactivation requires a new or continuing repository-visible outcome and a fresh minimum-team check.

## 12. Authority and non-goals

Cells may execute accepted work and make reversible local choices within scope. They do not create binding governance, override accepted canon, expand their own authority, select organizational technology, or create a real project through this model.
