# RESUME.md — STUDIO-005 re-entry packet

memory_schema_version: 1

task_id: STUDIO-005
package_path: projects/si-tu-chapter-1/memory/tasks/STUDIO-005
canonical_task_contract: tasks/STUDIO-005.md
authorized_contract_amendment: tasks/STUDIO-005-AMENDMENT-001.md
current_state: HANDOFF
last_safe_checkpoint_id: STUDIO-005-CP-0015
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
last_observed_HEAD: c22d75a4f3b1cc041cec4370d2571564d3f86744
durability_state: PR
last_verified_persisted_ref: Pull Request #9 at audited implementation head c22d75a4f3b1cc041cec4370d2571564d3f86744

expected_worktree_status: |
  - The 16-path implementation is durable in Draft Pull Request #9.
  - QA01-F001 correction is limited to seven already-authorized governance, memory, validator, and test paths.
  - Resolve the immutable correction commit from Pull Request #9 and its delivery comment; a commit cannot embed its own SHA.

completed_summary: |
  - Contract-only commit is verified on the remote branch.
  - Sixteen authorized implementation paths are present in the worktree after Studio Owner approval of Amendment 001.
  - The save-roundtrip test uses a closed destination path and still exercises replacement without changing production save code.
  - The actual v4 handoff contains complete CP-0001 through CP-0008; the provisional QA fixture that stopped at CP-0006 is not the live Windows state.
  - Delivery routing and validator negative cases were corrected within six authorized paths.
  - The checkpoint-mismatch regression test is phase-independent and no longer assumes CP-0010 already exists during the ACTIVE check pass.
  - The v6 failure was caused by changing the Cell state independently of the unchanged Project Studio status; the Cell is now kept at HANDOFF throughout recovery.
  - Deterministic implementation checks: PASS at STUDIO-005-CP-0014.
  - Draft Pull Request #9 was opened and QA-01 v13 audited implementation head c22d75a4f3b1cc041cec4370d2571564d3f86744.
  - QA-01 v13 ran 67 tests successfully and returned REQUEST CHANGES with the single finding QA01-F001.
  - STUDIO-005-CP-0015 reconciles the delivery and QA records and adds regression coverage against stale pre-delivery memory.
remaining_summary: |
  - Confirm Pull Request #9 current head contains the QA01-F001 correction recorded at STUDIO-005-CP-0015.
  - Independent QA-01 must rerun against that immutable corrected head.
  - Review & Integration acts only after QA; merge and branch disposition remain Studio Owner decisions.
blockers_and_authority_questions: |
  - NONE
  - official_integrated_gdd: NOT_YET_DESIGNATED
  - No game content or technology selection is authorized by STUDIO-005.
latest_checks: |
  - project studio validator: PASS at STUDIO-005-CP-0015
  - evidence register validator: PASS at STUDIO-005-CP-0015
  - validator tests and full unit-test discovery: PASS at STUDIO-005-CP-0015
  - source hashes, exact correction scope, and whitespace: PASS at STUDIO-005-CP-0015

first_verification_actions: |
  - Confirm branch studio-v0.5 and verify the current Pull Request #9 head includes STUDIO-005-CP-0015.
  - Run git status --short --untracked-files=all and preserve any unrelated change.
  - Verify all four records declare memory_schema_version: 1 and reconcile the writer claim.
  - Verify tasks/STUDIO-005.md is unchanged and both GDD Git blob SHAs match SOURCE_AUTHORITY.md.
  - Verify tasks/STUDIO-005-AMENDMENT-001.md and the exact amended test blob before running checks.
  - Run python scripts/validate_project_studio.py.
  - Run python scripts/validate_evidence_register.py source/MQ01_evidence_register.csv.
  - Run python -m unittest discover -s tests -p "test*.py" -v.
  - Run git diff --check and inspect the complete diff before any Git write.
next_implementation_action_after_verification: Rerun independent QA-01 on the immutable corrected Pull Request #9 head; do not begin Review & Integration unless QA approves.
receiving_role: Independent QA-01
writer_transfer_status: RELEASED

generated_from:
  TASK: TASK.md
  STATE: STATE.md
  WORKLOG: STUDIO-005-CP-0001 through STUDIO-005-CP-0015

updated_at: 2026-08-15T16:30:00+07:00

verify_instructions: |
  - The receiver must complete the first verification actions before writing. On mismatch, follow the reconciliation outcomes in studio/MEMORY_PROTOCOL.md and do not overwrite unrelated work or claim authority from memory recency.
