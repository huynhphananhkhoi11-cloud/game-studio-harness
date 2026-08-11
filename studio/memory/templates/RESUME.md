# RESUME.md — concise derived re-entry packet template

memory_schema_version: 1

task_id: <TASK-ID>
package_path: <repository-relative path to this package folder>
canonical_task_contract: <path or identifier>
current_state: <READY | ACTIVE | BLOCKED | HANDOFF | COMPLETE | INACTIVE>
last_safe_checkpoint_id: <TASK-ID-CP-####>
required_read_order:
  - AGENTS.md
  - <canonical_task_contract>
  - <accepted decisions and approved specifications referenced by TASK.md>
  - TASK.md
  - STATE.md
  - WORKLOG.md (only entries needed to resolve uncertainty or recover rationale)

repository_context: <repository-relative identifier or repository label; no credential-bearing URL>
worktree_context: <portable worktree label or repository-relative location; no machine-specific absolute path>
branch: <branch or NONE>
last_observed_HEAD: <commit sha or NONE>
durability_state: <WORKTREE_ONLY | COMMITTED_LOCAL | REMOTE_BRANCH | PR | MERGED>
last_verified_persisted_ref: <ref or NONE>

expected_worktree_status: |
  - changed_files_attributed_to_task: <list>
  - pre_existing_or_unrelated_changed_files: <list to preserve>

completed_summary: |
  - <short summary>
remaining_summary: |
  - <short summary>
blockers_and_authority_questions: |
  - <list>
latest_checks: |
  - <check>: <result, evidence reference>

first_verification_actions: |
  - <verify repository/worktree context, branch, HEAD, status, diff, unrelated changes, tests, durability evidence, writer claim, and matching supported schema across all four records>
next_implementation_action_after_verification: <one-sentence next action>
receiving_role: <logical role or Cell>
writer_transfer_status: <CLAIMED | TRANSFER_PENDING | RELEASED | UNKNOWN>

generated_from:
  TASK: TASK.md
  STATE: STATE.md
  WORKLOG: <list of checkpoint ids>

updated_at: <ISO 8601 timestamp with tz>

# Notes

RESUME.md is a concise derived re-entry packet for a receiver. It must be short, actionable, and verified against the canonical task, accepted decisions/specifications, and current repository evidence before the receiver performs any writes. RESUME.md does not replace the Handoff Protocol and must not claim durable sharing (REMOTE_BRANCH/PR/MERGED) without evidence references.

verify_instructions: |
  - The receiver must run the exact `first_verification_actions` before performing writes; if any verification fails, follow the reconciliation steps in studio/MEMORY_PROTOCOL.md.
