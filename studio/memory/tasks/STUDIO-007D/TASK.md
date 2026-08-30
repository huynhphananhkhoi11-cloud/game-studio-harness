# TASK.md - STUDIO-007D memory package

memory_schema_version: 1

task_id: STUDIO-007D
task_title: Simulated failover state machine v1.0
task_type: LEVEL 2 architectural implementation
canonical_task_contract: tasks/STUDIO-007D-IMPLEMENTATION.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-007D
project_studio: NONE

goal: |
  Implement and verify deterministic zero-cost failover-state, attempt-lineage, and simulated-transition validators after the contract-only Pull Request merges.

allowed_scope: |
  - Contract phase: tasks/STUDIO-007D.md, tasks/STUDIO-007D-IMPLEMENTATION.md, and this exact four-record memory package.
  - Implementation phase after contract merge: the sixteen paths in section 4 of the canonical contract.
  - Material-checkpoint updates to this exact memory package.

non_goals: |
  - Real failover, provider/model calls, network, credentials, execution, automatic retry or reassignment, Git/worktree mutation, dependencies, deletion, publication, deployment, or nonzero spending.
  - STUDIO-007E or STUDIO-007F and modifications to STUDIO-007A through STUDIO-007C implementation paths.

responsible_role: PRODUCER-01 coordinates contract; ENGINEERING-01 implements only after contract merge
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner
acceptance_criteria: tasks/STUDIO-007D-IMPLEMENTATION.md section 10

accepted_constraints: |
  - STUDIO-007A through STUDIO-007C are accepted, implemented, reviewed, merged, and retained.
  - Accepted failure classes are bounded to six values.
  - Maximum attempts per work order is 3.
  - STUDIO_OWNER gate is required for reassignment, evidence-exception resume, and abort.
  - A safe checkpoint cannot be waived.
  - AGENTS.md, studio/MEMORY_PROTOCOL.md, studio/HANDOFF_PROTOCOL.md, and accepted governance remain binding.

created_at: 2026-08-30T16:36:42+07:00
authorized_amendments: |
  - Studio Owner accepted the bounded STUDIO-007D decisions on 2026-08-30.
  - Implementation was authorized when contract PR #25 merged at c00dea3a8adc97f5b38e715aaf6c1c4759cca0fc.
  - Implementation PR #26 passed Rules CI, QA-01, and Review and Integration, then merged at e273862609608decf7069429ccb075caac1547f2 on 2026-08-30.

notes: |
  Failover records are operational evidence only. They do not authenticate actors or grant execution, project truth, QA acceptance, merge, provider, budget, publication, or deployment authority.
