# TASK.md — STUDIO-007B memory package

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
  - Implement and verify the accepted zero-cost capability registry and Studio-Owner-recorded manual dispatcher.
allowed_scope: |
  - The thirteen implementation files listed in section 4 of the canonical implementation contract.
  - Material-checkpoint updates to this exact four-record memory package.
non_goals: |
  - Automatic routing, ranking, execution, claims, worktrees, handoffs, failover, provider integration, credentials, external candidates, network services, dependencies, nonzero spend, or Git automation.
  - STUDIO-007C through STUDIO-007F behavior or changes to STUDIO-007A implementation files.

# Responsible role and review

responsible_role: ENGINEERING-01 implements; PRODUCER-01 coordinates
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner

# Acceptance and constraints

acceptance_criteria: tasks/STUDIO-007B-IMPLEMENTATION.md section 9
accepted_constraints: |
  - STUDIO-007A implementation merged by Pull Request #18 at a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f.
  - STUDIO-007B contract merged by Pull Request #19 at 475fb25e8d88c79c84a5fc117c9e8b1614aedfcb.
  - Studio Owner approved bounded vocabulary, evidence-backed internal executors, explicit deterministic expiry, Owner-only dispatch, and zero-cost/no-network operation.
  - AGENTS.md, studio/MEMORY_PROTOCOL.md, studio/HANDOFF_PROTOCOL.md, and accepted governance remain binding.

# Metadata and governance

created_at: 2026-08-29T13:30:00+07:00
authorized_amendments: |
  - Pull Request #19 merged the accepted implementation contract; section 12 authorizes the bounded implementation on agent/studio-007b-manual-dispatch.

# Notes

This package carries Platform Studio operational evidence only. Capability and role records do not authenticate an actor or grant project canon, provider, budget, merge, publication, or execution authority.
