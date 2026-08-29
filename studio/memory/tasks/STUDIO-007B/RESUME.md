# RESUME.md â€” STUDIO-007B re-entry packet

memory_schema_version: 1

task_id: STUDIO-007B
package_path: studio/memory/tasks/STUDIO-007B
canonical_task_contract: tasks/STUDIO-007B-IMPLEMENTATION.md
current_state: CONTRACT_PREPARED
last_safe_checkpoint_id: STUDIO-007B-CP-0002
required_read_order:
  - AGENTS.md
  - docs/GAME_VISION.md
  - docs/DECISIONS.md
  - tasks/STUDIO-007.md
  - tasks/STUDIO-007B.md
  - tasks/STUDIO-007B-IMPLEMENTATION.md
  - platform/orchestration/WORK_ORDER_QUEUE.md
  - studio/MEMORY_PROTOCOL.md
  - TASK.md
  - STATE.md
  - WORKLOG.md entries STUDIO-007B-CP-0001 through STUDIO-007B-CP-0002

repository_context: game-studio-harness
worktree_context: primary repository worktree
branch: agent/studio-007b-capability-dispatcher
last_observed_HEAD: a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f
durability_state: WORKTREE_ONLY
last_verified_persisted_ref: NONE

expected_worktree_status: |
  - changed_files_attributed_to_task: exactly tasks/STUDIO-007B.md, tasks/STUDIO-007B-IMPLEMENTATION.md, and four records under studio/memory/tasks/STUDIO-007B/.
  - pre_existing_or_unrelated_changed_files: NONE.

completed_summary: |
  - STUDIO-007A merge evidence and the clean baseline were verified; the bounded 007B contract-only package was prepared.
remaining_summary: |
  - Apply and verify the package, run checks, then commit/push only on explicit Owner direction and submit a contract-only Pull Request.
blockers_and_authority_questions: |
  - Runtime implementation remains prohibited until the contract-only Pull Request merges.
latest_checks: |
  - Baseline branch agent/studio-007b-capability-dispatcher at a8c4979dbedf827f1d9d9ff4570b37e0ae214c6f: clean by Studio Owner evidence.

first_verification_actions: |
  - Run git branch --show-current, git rev-parse HEAD, git status --short --branch, git status --porcelain=v1 --untracked-files=all, git diff --stat, and git diff --check.
  - Confirm exactly six scoped files and memory_schema_version 1 in all four memory records.
  - Run data validation and the complete existing test suite.
next_implementation_action_after_verification: Review the exact contract diff; do not create runtime files, commit, push, or merge without the applicable authorization.
receiving_role: PRODUCER-01
writer_transfer_status: CLAIMED by PRODUCER-01

generated_from:
  TASK: TASK.md
  STATE: STATE.md
  WORKLOG: STUDIO-007B-CP-0001 through STUDIO-007B-CP-0002

updated_at: 2026-08-29T13:30:00+07:00

verify_instructions: |
  - If branch, HEAD, exact scope, schema, claim, authority, or worktree evidence differs, stop and follow reconciliation in studio/MEMORY_PROTOCOL.md.