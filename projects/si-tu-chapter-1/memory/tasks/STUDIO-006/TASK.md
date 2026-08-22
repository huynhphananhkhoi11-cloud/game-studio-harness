# TASK.md — STUDIO-006 execution index

memory_schema_version: 1

# Task identity

task_id: STUDIO-006
task_title: Evidence-based external capability evaluation
task_type: LEVEL 2 — security / dependency / architectural evaluation
canonical_task_contract: tasks/STUDIO-006.md
authorized_contract_amendment: tasks/STUDIO-006-AMENDMENT-001.md
memory_root: projects/si-tu-chapter-1/memory/tasks
package_path: projects/si-tu-chapter-1/memory/tasks/STUDIO-006
project_studio: SITU-CH1

# Goal and scope

goal: |
  - Evaluate exactly ten STUDIO-005 external capability candidates through public read-only evidence and provide one non-binding recommendation per candidate.
allowed_scope: |
  - studio/EXTERNAL_CAPABILITY_CANDIDATES.md
  - studio/EXTERNAL_CAPABILITY_EVALUATION.md
  - projects/si-tu-chapter-1/ARTIFACT_MAP.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-006/TASK.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-006/STATE.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-006/WORKLOG.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-006/RESUME.md
non_goals: |
  - Do not modify tasks/STUDIO-006.md after its contract merge.
  - Do not clone, download as a repository/archive, install, import, vendor, execute, enable, or grant authority to a candidate.
  - Do not add dependencies, workflows, hooks, binaries, models, providers, runtimes, routers, frameworks, engines, or platforms.
  - Do not change GDD sources, historical claims, gameplay, prototype code/data, MQ01 artifacts, or completed STUDIO-005 memory.
  - Do not convert recommendations into adoption decisions.
  - Do not merge the evaluation Pull Request from the delivery script.

# Responsible role and review

responsible_role: STUDIO-006-EVALUATION
review_target: Independent QA-06, then independent REVIEW-INTEGRATION-06, then Studio Owner

# Acceptance and constraints

acceptance_criteria: tasks/STUDIO-006.md Sections 10–13
accepted_constraints: |
  - AGENTS.md
  - studio/STUDIO_CONSTITUTION.md
  - studio/MEMORY_PROTOCOL.md
  - studio/HANDOFF_PROTOCOL.md
  - projects/si-tu-chapter-1/PROJECT_STUDIO.md
  - projects/si-tu-chapter-1/SOURCE_AUTHORITY.md
  - projects/si-tu-chapter-1/DECISIONS.md
  - Pull Request #11 merged as 0e2d7bab5c7c876338a246be16d46a8f1073b95c
  - tasks/STUDIO-006-AMENDMENT-001.md approved and merged through Pull Request #13 as 6476b65463815a1f5ccfbb373f8151426d63d8dc
  - validator transition Pull Request #14 merged as 4258654fddd83b3f7e0d00936c22e3954e321767

# Metadata and governance

created_at: 2026-08-15T22:17:34+07:00
authorized_amendments: tasks/STUDIO-006-AMENDMENT-001.md

# Notes

This stable index cannot broaden the contract. Dynamic state belongs in STATE.md, material checkpoints in WORKLOG.md, and re-entry instructions in RESUME.md.
