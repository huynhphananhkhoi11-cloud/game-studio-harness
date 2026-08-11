# WORKLOG.md — append-only checkpoint log template

memory_schema_version: 1

task_id: <TASK-ID>
package_path: <repository-relative path to this package folder>
canonical_task_contract: <path or identifier>

# Each entry example

- checkpoint_id: <TASK-ID-CP-0001>
  timestamp: <ISO 8601 timestamp with tz>
  actor: <logical role or agent id>
  action: <description of action or checkpoint>
  scope_files: <files or globs>
  command_or_check: <command or check name and reference>
  evidence_reference: <commit/ref/PR or NONE>
  outcome: <attempted | failed | partial | completed | reviewed | accepted | observed>
  rationale: <concise rationale when necessary>
  resulting_state: <state or implication>
  correction_of: <checkpoint_id or NONE>

# Rules: append-only; use stable checkpoint IDs; record only material factual checkpoints.
# Record attempted, failed, partial, completed, reviewed, and accepted outcomes distinctly.
# Corrections append and reference the corrected checkpoint rather than rewriting earlier entries.
# Do not record secrets, private chain-of-thought, full transcripts, or low-value narration.
