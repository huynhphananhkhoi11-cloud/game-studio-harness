# TASK.md â€” STUDIO-007B memory package

memory_schema_version: 1

# Task identity

task_id: STUDIO-007B
task_title: Capability Registry & Manual Dispatcher v1.0
task_type: LEVEL 2 architectural implementation
canonical_task_contract: tasks/STUDIO-007B-IMPLEMENTATION.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-007B
project_studio: NONE

# Goal and scope

goal: |
  - Implement the accepted zero-cost capability registry and Studio-Owner-recorded manual dispatcher after the contract-only Pull Request merges.
allowed_scope: |
  - Contract phase: tasks/STUDIO-007B.md, tasks/STUDIO-007B-IMPLEMENTATION.md, and this exact four-record package.
  - Implementation phase: only the thirteen implementation files listed in section 4 of the canonical implementation contract plus material-checkpoint updates to this package.
non_goals: |
  - Automatic routing, ranking, execution, claims, worktrees, handoffs, failover, provider integration, credentials, external candidates, network services, dependencies, nonzero spend, or Git automation.
  - STUDIO-007C through STUDIO-007F behavior or changes to STUDIO-007A implementation files.

# Responsible role and review

responsible_role: PRODUCER-01 coordinates; ENGINEERING-01 implements after contract merge
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner

# Acceptance and constraints

acceptance_criteria: tasks/STUDIO-007B-IMPLEMENTATION.md section 9
accepted_constraints: |
  - STUDIO-007A implementation merged by Pull Request #18 at a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f.
  - Studio Owner approval on 2026-08-29: bounded vocabulary, evidence-backed internal executors, explicit deterministic expiry, Owner-only dispatch, and zero-cost/no-network operation.
  - AGENTS.md, studio/MEMORY_PROTOCOL.md, studio/HANDOFF_PROTOCOL.md, and accepted governance remain binding.

# Metadata and governance

created_at: 2026-08-29T13:30:00+07:00
authorized_amendments: |
  - Studio Owner authorized preparation of the STUDIO-007B implementation contract on 2026-08-29; implementation authority begins only after the contract-only Pull Request merges.

# Notes

This package carries Platform Studio operational evidence only. Capability and role records do not authenticate an actor or grant project canon, provider, budget, merge, publication, or execution authority.