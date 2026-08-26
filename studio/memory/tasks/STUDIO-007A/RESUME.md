# RESUME.md — STUDIO-007A re-entry packet

memory_schema_version: 1

task_id: STUDIO-007A
package_path: studio/memory/tasks/STUDIO-007A
canonical_task_contract: tasks/STUDIO-007A-IMPLEMENTATION.md
current_state: ACTIVE
last_safe_checkpoint_id: STUDIO-007A-CP-0002
required_read_order:
  - AGENTS.md
  - docs/DECISIONS.md
  - tasks/STUDIO-007.md
  - tasks/STUDIO-007A.md
  - tasks/STUDIO-007A-IMPLEMENTATION.md
  - studio/MEMORY_PROTOCOL.md
  - TASK.md
  - STATE.md
  - WORKLOG.md entries STUDIO-007A-CP-0001 through STUDIO-007A-CP-0002

repository_context: game-studio-harness
worktree_context: primary repository worktree
branch: agent/studio-007a-contract
last_observed_HEAD: e04a933e2c0dd18438822f4c9fdabd2f6af9c4e5
durability_state: WORKTREE_ONLY
last_verified_persisted_ref: NONE

expected_worktree_status: |
  - changed_files_attributed_to_task: exactly the six contract and memory files recorded in STATE.md.
  - pre_existing_or_unrelated_changed_files: NONE expected; preserve and stop if observed.

completed_summary: |
  - Owner approval and the bounded zero-cost implementation contract are recorded.
remaining_summary: |
  - Verify, commit, push, review, and merge the contract-only package before implementation.
blockers_and_authority_questions: |
  - Runtime implementation is prohibited until the contract-only Pull Request merges.
latest_checks: |
  - Pull Request #16 and baseline e04a933e2c0dd18438822f4c9fdabd2f6af9c4e5 verified.
  - Six-file scope and whitespace still require verification in the receiving worktree.

first_verification_actions: |
  - Run git branch --show-current, git rev-parse HEAD, git status --short --branch, git diff --stat, and git diff --check.
  - Verify all four records declare memory_schema_version 1 and one unambiguous CLAIMED writer.
next_implementation_action_after_verification: Commit and push only the six-file contract package for independent review; do not create implementation files.
receiving_role: REVIEW-INTEGRATION-01
writer_transfer_status: CLAIMED

generated_from:
  TASK: TASK.md
  STATE: STATE.md
  WORKLOG: STUDIO-007A-CP-0001, STUDIO-007A-CP-0002

updated_at: 2026-08-26T11:26:06+07:00

verify_instructions: |
  - If branch, HEAD, scope, schema, writer claim, or worktree evidence differs, stop and follow reconciliation in studio/MEMORY_PROTOCOL.md.
