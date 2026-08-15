# RESUME.md — STUDIO-005 re-entry packet

memory_schema_version: 1

task_id: STUDIO-005
package_path: projects/si-tu-chapter-1/memory/tasks/STUDIO-005
canonical_task_contract: tasks/STUDIO-005.md
authorized_contract_amendment: tasks/STUDIO-005-AMENDMENT-001.md
current_state: HANDOFF
last_safe_checkpoint_id: STUDIO-005-CP-0014
required_read_order:
  - AGENTS.md
  - tasks/STUDIO-005.md
  - tasks/STUDIO-005-AMENDMENT-001.md
  - docs/DECISIONS.md
  - studio/MEMORY_PROTOCOL.md
  - projects/si-tu-chapter-1/PROJECT_STUDIO.md
  - projects/si-tu-chapter-1/SOURCE_AUTHORITY.md
  - projects/si-tu-chapter-1/DECISIONS.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/TASK.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/STATE.md
  - projects/si-tu-chapter-1/memory/tasks/STUDIO-005/WORKLOG.md (only entries needed to verify or recover state)

repository_context: game-studio-harness
worktree_context: primary repository worktree
branch: studio-v0.5
last_observed_HEAD: 531235536db678ec93c1f8a11ed4e31bbb0bfeff
durability_state: WORKTREE_ONLY
last_verified_persisted_ref: NONE

expected_worktree_status: |
  - changed_files_attributed_to_task: exactly the 16 implementation paths listed in TASK.md
  - pre_existing_or_unrelated_changed_files: NONE; stop and reconcile if any are observed

completed_summary: |
  - Contract-only commit is verified on the remote branch.
  - Sixteen authorized implementation paths are present in the worktree after Studio Owner approval of Amendment 001.
  - The save-roundtrip test uses a closed destination path and still exercises replacement without changing production save code.
  - The actual v4 handoff contains complete CP-0001 through CP-0008; the provisional QA fixture that stopped at CP-0006 is not the live Windows state.
  - Delivery routing and validator negative cases were corrected within six authorized paths.
  - The checkpoint-mismatch regression test is phase-independent and no longer assumes CP-0010 already exists during the ACTIVE check pass.
  - The v6 failure was caused by changing the Cell state independently of the unchanged Project Studio status; the Cell is now kept at HANDOFF throughout recovery.
  - Deterministic implementation checks: PASS at STUDIO-005-CP-0014.
remaining_summary: |
  - Studio Owner authorization is required before commit, push, or draft Pull Request creation.
  - After that authorization, commit and push the validated implementation, then open a draft Pull Request to `main`.
  - Independent QA-01 must audit the immutable draft Pull Request head.
  - Review & Integration acts only after QA; merge and branch disposition remain Studio Owner decisions.
blockers_and_authority_questions: |
  - NONE
  - official_integrated_gdd: NOT_YET_DESIGNATED
  - No game content or technology selection is authorized by STUDIO-005.
latest_checks: |
  - project studio validator: PASS at STUDIO-005-CP-0014
  - evidence register validator: PASS at STUDIO-005-CP-0014
  - new validator tests and full unit-test discovery: PASS at STUDIO-005-CP-0014
  - source hashes, exact scope, and whitespace: PASS at STUDIO-005-CP-0014

first_verification_actions: |
  - Confirm branch studio-v0.5 and HEAD 531235536db678ec93c1f8a11ed4e31bbb0bfeff before an implementation commit exists; after a later commit, reconcile against its durable reference.
  - Run git status --short --untracked-files=all and preserve any unrelated change.
  - Verify all four records declare memory_schema_version: 1 and reconcile the writer claim.
  - Verify tasks/STUDIO-005.md is unchanged and both GDD Git blob SHAs match SOURCE_AUTHORITY.md.
  - Verify tasks/STUDIO-005-AMENDMENT-001.md and the exact amended test blob before running checks.
  - Run python scripts/validate_project_studio.py.
  - Run python scripts/validate_evidence_register.py source/MQ01_evidence_register.csv.
  - Run python -m unittest discover -s tests -p "test*.py" -v.
  - Run git diff --check and inspect the complete diff before any Git write.
next_implementation_action_after_verification: Obtain explicit Studio Owner authorization to commit and push the validated 16-path implementation and open a draft Pull Request to main; do not invoke official QA before the PR exists.
receiving_role: Studio Owner for delivery authorization
writer_transfer_status: RELEASED

generated_from:
  TASK: TASK.md
  STATE: STATE.md
  WORKLOG: STUDIO-005-CP-0001, STUDIO-005-CP-0002, STUDIO-005-CP-0003, STUDIO-005-CP-0004, STUDIO-005-CP-0005, STUDIO-005-CP-0006, STUDIO-005-CP-0007, STUDIO-005-CP-0008, STUDIO-005-CP-0009, STUDIO-005-CP-0010, STUDIO-005-CP-0011, STUDIO-005-CP-0012, STUDIO-005-CP-0013, STUDIO-005-CP-0014

updated_at: 2026-08-15T15:04:11+07:00

verify_instructions: |
  - The receiver must complete the first verification actions before writing. On mismatch, follow the reconciliation outcomes in studio/MEMORY_PROTOCOL.md and do not overwrite unrelated work or claim authority from memory recency.
