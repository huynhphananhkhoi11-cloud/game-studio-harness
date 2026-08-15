# Cell SITU-BASELINE-001 — Project Studio Baseline

## 1. Formation record

- `cell_id`: `SITU-BASELINE-001`
- `parent_scope`: Project Studio `SITU-CH1`
- `task_contract`: `tasks/STUDIO-005.md`
- `authorized_amendment`: `tasks/STUDIO-005-AMENDMENT-001.md`
- `state`: `HANDOFF`
- `handoff_level`: `LEVEL 2 — historical / architectural`
- `memory_package`: `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/`
- `bounded_outcome`: Establish and deterministically validate the first real Project Studio baseline without changing game content or selecting technology.

## 2. Canonical references

- `AGENTS.md`
- `tasks/STUDIO-005.md`
- `tasks/STUDIO-005-AMENDMENT-001.md`
- `studio/STUDIO_CONSTITUTION.md`
- `studio/PROJECT_STUDIO_TEMPLATE.md`
- `studio/CELL_MODEL.md`
- `studio/ACTIVATION_POLICY.md`
- `studio/MEMORY_PROTOCOL.md`
- `studio/HANDOFF_PROTOCOL.md`
- `docs/HISTORICAL_CONTENT_SYSTEM.md`
- `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md`

## 3. Minimum sufficient composition

| Execution capability | Bounded responsibility | State |
| --- | --- | --- |
| Producer / Coordination | Maintain exact 16-file amended implementation scope, dependency visibility, checkpoints, and handoff readiness | `HANDOFF` |
| Narrative / Research | Preserve co-equal source treatment, authority-layer separation, evidence classifications, and `DOC01` limits | `HANDOFF` |
| Engineering | Implement the validator, tests, exact file structure, and deterministic checks | `HANDOFF` |

QA and Review & Integration are independent handoff recipients, not implementation authors or permanent Cell members. No runtime, model, or provider is assigned to a logical capability.

## 4. Authorized deliverables

The Cell may create or modify only the 16 implementation paths authorized by `tasks/STUDIO-005.md`, Section 11, together with `tasks/STUDIO-005-AMENDMENT-001.md`. The amendment permits a bounded Windows-compatibility repair in `tests/test_rules_prototype.py`; it does not permit changes to prototype rules. The Cell must leave `tasks/STUDIO-005.md`, both GDD DOCX files, MQ01 support artifacts, design content, prototype data, and prototype rules unchanged.

## 5. Accepted constraints

- V22 and V23 are co-equal, Owner-created working design inputs.
- No integrated official GDD is designated.
- No content unit is selected, promoted, rewritten, or rejected by this bootstrap Cell.
- Design provenance, historical evidence, and official project authority remain separate.
- `DOC01` final material form remains blocked pending appropriate evidence.
- External capabilities remain unassessed, uninstalled, and undecided.
- Engine, language, framework, runtime, model, provider, router, database, dependency, and production pipeline remain unselected.

## 6. Dependencies and blockers

| Dependency | Required evidence | Current state |
| --- | --- | --- |
| Contract durability | Remote branch contains contract commit | `VERIFIED`: `studio-v0.5@531235536db678ec93c1f8a11ed4e31bbb0bfeff` |
| GDD immutability | Exact Git blob SHAs | `VERIFIED AT INITIALIZATION`; recheck before commit |
| Exact scope | Git status/diff contains only authorized paths | `PASS at STUDIO-005-CP-0014` |
| Deterministic tests | Validators and unit-test suite exit 0 | `PASS at STUDIO-005-CP-0014` |
| Durable delivery | Authorized commit, push, and draft Pull Request | `PENDING STUDIO OWNER AUTHORIZATION` |
| Independent QA | Repository-visible verdict on immutable draft Pull Request head | `PENDING AFTER DRAFT PR` |
| Review & Integration | Repository-visible verdict after QA | `PENDING` |

Enter `BLOCKED` if source hashes change, scope expands, evidence/canon authority conflicts, writer state cannot be reconciled, or any required check fails.

## 7. Handoff targets

1. Obtain explicit Studio Owner authorization for the delivery operation; the correction itself does not authorize Git writes.
2. After authorization, commit and push the validated 16-path implementation, then open a draft Pull Request to `main`.
3. QA independently audits the immutable draft Pull Request head and attempts to falsify scope, source immutability, co-equal status, authority separation, memory accuracy, external-candidate safety, and validator negative cases.
4. Review & Integration acts only after QA and checks architectural consistency, authority boundaries, source-of-truth placement, duplication, readability, and evidence sufficiency.
5. The Studio Owner reviews the final Pull Request and decides merge and branch disposition.

Allowed independent verdicts are `APPROVE`, `REQUEST CHANGES`, or `BLOCK`.

## 8. Completion and dissolution

The Cell may enter `COMPLETE` only when all deliverables exist, deterministic checks pass, QA and Review & Integration approve, residual risks are explicit, and a downstream disposition is recorded. It then dissolves or becomes `INACTIVE`.

The Cell may not persist into gameplay implementation, content comparison, GDD integration, external-capability evaluation, or permanent staffing without a new accepted task.
