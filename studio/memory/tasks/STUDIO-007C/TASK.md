# TASK.md - STUDIO-007C memory package

memory_schema_version: 1

task_id: STUDIO-007C
task_title: Writer Claim, worktree & durable handoff v1.0
task_type: LEVEL 2 architectural implementation
canonical_task_contract: tasks/STUDIO-007C-IMPLEMENTATION.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-007C
project_studio: NONE

goal: |
  Implement and verify the accepted zero-cost writer-claim, worktree-record, and durable-handoff validators after the contract-only Pull Request merges.

allowed_scope: |
  - Contract phase: tasks/STUDIO-007C.md, tasks/STUDIO-007C-IMPLEMENTATION.md, and this exact four-record memory package.
  - Implementation phase after contract merge: the sixteen implementation paths in section 4 of the canonical contract.
  - Material-checkpoint updates to this exact memory package.

non_goals: |
  - Automatic Git or filesystem worktree operations, execution, routing, failover, provider integration, credentials, network access, dependencies, external code, nonzero spending, publication, or deployment.
  - STUDIO-007D through STUDIO-007F or modifications to STUDIO-007A/STUDIO-007B implementation files.

responsible_role: PRODUCER-01 coordinates contract; ENGINEERING-01 implements only after contract merge
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner

acceptance_criteria: tasks/STUDIO-007C-IMPLEMENTATION.md section 10

accepted_constraints: |
  - STUDIO-007A and STUDIO-007B are accepted, implemented, reviewed, merged, and retained.
  - One writer per overlapping path scope.
  - Active implementation writer claims use a 24-hour lease; unfinished work requires pre-expiry renewal or a new Owner-authorized claim after expiry.
  - Same-writer renewal only before expiry; expiry does not transfer authority.
  - Studio Owner alone records overlap exceptions in v1.0.
  - Git automation remains prohibited.
  - AGENTS.md, studio/MEMORY_PROTOCOL.md, studio/HANDOFF_PROTOCOL.md, and accepted governance remain binding.

created_at: 2026-08-29T17:33:00+07:00

authorized_amendments: |
  - Studio Owner accepted the bounded STUDIO-007C decisions on 2026-08-29.
  - Implementation remains unauthorized until the contract-only Pull Request merges.
  - Studio Owner authorized a 24-hour ENGINEERING-01 implementation writer claim after PR #22 merged.

notes: |
  This package carries Platform Studio operational evidence only. Claim, worktree, and handoff records do not authenticate actors or grant project truth, merge, provider, budget, publication, or execution authority.
