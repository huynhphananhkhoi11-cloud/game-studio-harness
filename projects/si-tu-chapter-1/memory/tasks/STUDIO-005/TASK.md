# TASK.md — STUDIO-005 execution index

memory_schema_version: 1

# Task identity

task_id: STUDIO-005
task_title: Bootstrap the historical game Project Studio from co-equal working drafts
task_type: LEVEL 2 — historical / architectural
canonical_task_contract: tasks/STUDIO-005.md
authorized_contract_amendment: tasks/STUDIO-005-AMENDMENT-001.md
memory_root: projects/si-tu-chapter-1/memory/tasks
package_path: projects/si-tu-chapter-1/memory/tasks/STUDIO-005
project_studio: SITU-CH1

# Goal and scope

goal: |
  - Instantiate and validate the SITU-CH1 Project Studio while preserving V22 and V23 as co-equal, Owner-created working design inputs.
allowed_scope: |
  - projects/si-tu-chapter-1/PROJECT_STUDIO.md
  - projects/si-tu-chapter-1/SOURCE_AUTHORITY.md
  - projects/si-tu-chapter-1/ARTIFACT_MAP.md
  - projects/si-tu-chapter-1/DECISIONS.md
  - projects/si-tu-chapter-1/cells/SITU-BASELINE-001.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/TASK.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/STATE.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/WORKLOG.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/RESUME.md
  - studio/EXTERNAL_CAPABILITY_CANDIDATES.md
  - scripts/validate_project_studio.py
  - tests/test_validate_project_studio.py
  - AGENTS.md
  - README.md
  - tasks/STUDIO-005-AMENDMENT-001.md
  - tests/test_rules_prototype.py
non_goals: |
  - Do not modify tasks/STUDIO-005.md after its contract-only commit.
  - Do not modify, move, rename, normalize, or resave either GDD DOCX source or any MQ01 support artifact.
  - Do not select, combine, rewrite, promote, or reject game content from V22 or V23.
  - Do not designate an integrated official GDD or finalize DOC01 material form.
  - Do not choose technology or install/adopt external capabilities.
  - Do not modify prototype/rules/save_system.py or any other production code; Amendment 001 authorizes only the exact Windows-compatible test fixture repair.
  - Do not commit, push, open a Pull Request, merge, or delete a branch without the separately authorized workflow step.

# Responsible role and review

responsible_role: Cell SITU-BASELINE-001
review_target: Independent QA-01, then independent REVIEW-INTEGRATION-01, then Studio Owner

# Acceptance and constraints

acceptance_criteria: tasks/STUDIO-005.md Sections 15–19
accepted_constraints: |
  - studio/STUDIO_CONSTITUTION.md
  - studio/PROJECT_STUDIO_TEMPLATE.md
  - studio/CELL_MODEL.md
  - studio/ACTIVATION_POLICY.md
  - studio/MEMORY_PROTOCOL.md
  - studio/HANDOFF_PROTOCOL.md
  - docs/HISTORICAL_CONTENT_SYSTEM.md
  - OWNER_DECISION-SOURCE-001 in tasks/STUDIO-005.md
  - tasks/STUDIO-005-AMENDMENT-001.md

# Metadata and governance

created_at: 2026-08-12T12:00:37+07:00
authorized_amendments: |
  - STUDIO-005-AMENDMENT-001: Studio Owner approved Option A on 2026-08-12; adds tasks/STUDIO-005-AMENDMENT-001.md and tests/test_rules_prototype.py, for exactly 16 implementation paths total.

# Notes

This file is the stable execution index. Dynamic state belongs in STATE.md, material checkpoints belong in WORKLOG.md, and re-entry instructions belong in RESUME.md. This package cannot broaden the approved task contract or create official game content.
