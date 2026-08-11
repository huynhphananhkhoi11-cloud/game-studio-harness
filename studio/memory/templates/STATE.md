# STATE.md — memory package current snapshot template

memory_schema_version: 1

# Package identity and repository context

task_id: <TASK-ID>
package_path: <repository-relative path to this package folder>
canonical_task_contract: <path or identifier>
state: <READY | ACTIVE | BLOCKED | HANDOFF | COMPLETE | INACTIVE>
logical_role: <current logical role or Cell>
repository_context: <repository-relative identifier or repository label; no credential-bearing URL>
worktree_context: <portable worktree label or repository-relative location; no machine-specific absolute path>
branch: <branch name or NONE>
last_observed_HEAD: <commit sha or NONE>
durability_state: <WORKTREE_ONLY | COMMITTED_LOCAL | REMOTE_BRANCH | PR | MERGED>
last_verified_persisted_ref: <ref or NONE>

# Worktree and change boundary
worktree_status_summary: |
  - changed_files_attributed_to_task: <list of files the task is explicitly changing>
  - pre_existing_or_unrelated_changed_files: <list of files that must be preserved>

# Progress and state
completed: |
  - <completed items>
remaining: |
  - <remaining items>
blockers: |
  - <blocker and concrete unblock condition>
assumptions: |
  - <explicit assumptions>
unresolved_items: |
  - <unresolved items>

# Checks, checkpoints, and next action
latest_checks: |
  - <check name>: <result and evidence reference>

last_safe_checkpoint_id: <TASK-ID-CP-####>
exact_next_action: <one-sentence next action>

# Active writer claim (coordination evidence, not a distributed lock)
active_writer_claim:
  status: <CLAIMED | TRANSFER_PENDING | RELEASED | UNKNOWN>
  writer: <logical role or agent id>
  claim_timestamp: <ISO 8601 timestamp with tz>
  transfer_intent: <optional: intended receiver id or NONE>

updated_at: <ISO 8601 timestamp with tz>
updater: <logical role or cell>

# Notes

STATE.md is a replaceable current snapshot and not an append-only log. Use explicit values (NONE, NOT_RUN, UNKNOWN, UNRESOLVED) rather than blanks. Distinguish task-attributed changed files from pre-existing/unrelated changes; do not overwrite or attribute unrelated work to this task. Before writing, verify the repository and worktree contexts and all four records' schema versions under studio/MEMORY_PROTOCOL.md.
