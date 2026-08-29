# RESUME.md — STUDIO-007B re-entry packet

memory_schema_version: 1

task_id: STUDIO-007B
package_path: studio/memory/tasks/STUDIO-007B
canonical_task_contract: tasks/STUDIO-007B-IMPLEMENTATION.md
current_state: IMPLEMENTATION_PREPARED
last_safe_checkpoint_id: STUDIO-007B-CP-0004
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
  - WORKLOG.md entries STUDIO-007B-CP-0001 through STUDIO-007B-CP-0004

repository_context: game-studio-harness
worktree_context: primary repository worktree
branch: agent/studio-007b-manual-dispatch
last_observed_HEAD: 475fb25e8d88c79c84a5fc117c9e8b1614aedfcb
durability_state: WORKTREE_ONLY
last_verified_persisted_ref: 475fb25e8d88c79c84a5fc117c9e8b1614aedfcb

expected_worktree_status: |
  - changed_files_attributed_to_task: exactly thirteen new implementation files and four modified records under studio/memory/tasks/STUDIO-007B/.
  - pre_existing_or_unrelated_changed_files: NONE.

completed_summary: |
  - Pull Request #19 merged the accepted contract; the bounded STUDIO-007B implementation package was prepared and 21 focused tests passed.
remaining_summary: |
  - Apply to the verified branch, run every required repository check, inspect the exact diff, then commit/push only on explicit Studio Owner direction.
blockers_and_authority_questions: |
  - Application must stop if branch, HEAD, cleanliness, scope, or memory schema differs.
  - Final merge remains exclusively the Studio Owner decision after independent QA and integration review.
latest_checks: |
  - Preparation workspace: all JSON parse checks PASS; 21 focused dispatch tests PASS.

first_verification_actions: |
  - Confirm branch agent/studio-007b-manual-dispatch, HEAD 475fb25e8d88c79c84a5fc117c9e8b1614aedfcb, and a clean worktree.
  - Apply exactly thirteen new implementation files and replace exactly these four memory records.
  - Run data validation, retained queue tests, focused dispatcher tests, full discovery, git diff --check, and exact-scope verification.
next_implementation_action_after_verification: Review the exact seventeen-file diff; do not commit, push, open a Pull Request, or merge until explicitly authorized.
receiving_role: ENGINEERING-01
writer_transfer_status: CLAIMED by ENGINEERING-01; transfer to QA-01 only after one immutable implementation head exists

generated_from:
  TASK: TASK.md
  STATE: STATE.md
  WORKLOG: STUDIO-007B-CP-0001 through STUDIO-007B-CP-0004

updated_at: 2026-08-29T14:00:00+07:00

verify_instructions: |
  - If branch, HEAD, exact scope, schema, claim, authority, or worktree evidence differs, stop and follow reconciliation in studio/MEMORY_PROTOCOL.md.
