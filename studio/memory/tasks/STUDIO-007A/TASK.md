# TASK.md — STUDIO-007A memory package

memory_schema_version: 1

# Task identity

task_id: STUDIO-007A
task_title: Work Order & Producer Queue v1.0
task_type: LEVEL 2 architectural implementation
canonical_task_contract: tasks/STUDIO-007A-IMPLEMENTATION.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-007A
project_studio: NONE

# Goal and scope

goal: |
  - Implement the accepted zero-cost work-order envelope and file-backed Producer Queue after the contract-only Pull Request merges.
allowed_scope: |
  - Contract phase: tasks/STUDIO-007A.md, tasks/STUDIO-007A-IMPLEMENTATION.md, and this exact four-record package.
  - Implementation phase: only the twelve implementation files listed in section 4 of the canonical implementation contract plus material-checkpoint updates to this package.
non_goals: |
  - STUDIO-007B through STUDIO-007F behavior.
  - AI/provider integration, credentials, external candidates, network services, dependencies, nonzero spend, or automatic Git operations.

# Responsible role and review

responsible_role: PRODUCER-01 coordinates; ENGINEERING-01 implements after contract merge
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner

# Acceptance and constraints

acceptance_criteria: tasks/STUDIO-007A-IMPLEMENTATION.md section 9
accepted_constraints: |
  - tasks/STUDIO-007.md merged by Pull Request #16 at e04a933e2c0dd18438822f4c9fdabd2f6af9c4e5.
  - Studio Owner approval on 2026-08-26: JSON records, Python standard library, zero-cost file queue, Owner-only READY/CANCELLED authority, and reserved downstream states.
  - AGENTS.md, studio/MEMORY_PROTOCOL.md, and studio/HANDOFF_PROTOCOL.md remain binding.

# Metadata and governance

created_at: 2026-08-26T11:26:06+07:00
authorized_amendments: |
  - Studio Owner authorized the STUDIO-007A implementation contract on 2026-08-26; no implementation authority exists before its contract-only Pull Request merges.

# Notes

This package carries Platform Studio operational evidence only. It grants no project canon, provider, credential, budget, merge, or publication authority.
