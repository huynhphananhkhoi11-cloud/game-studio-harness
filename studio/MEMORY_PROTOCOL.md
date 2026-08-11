# Persistent Memory Protocol — studio/MEMORY_PROTOCOL.md

memory_schema_version: 1

This document is the canonical operational protocol required by STUDIO-004. It is the single authoritative reference for the lifecycle, responsibilities, and operational invariants of repository-visible persistent memory packages. It complements, and does not replace, the canonical governance, activation, handoff, and Project Studio documents (see references).

This protocol prescribes:
- the exact four-record package and each record's distinct responsibility;
- activation thresholds and the LEVEL 0 exception for clean one-session micro-tasks;
- initialization, material checkpoints, planned interruption, handoff, unplanned recovery, completion, retention, and authorized reopening;
- evidence requirements and invalid combinations for durability labels;
- writer-claim lifecycle and single-writer rules;
- reconciliation outcomes and required actions for common failure classes;
- security, context hygiene, and portability constraints.

Package shape and canonical responsibilities

A memory package lives at <MEMORY_ROOT>/<TASK-ID>/ and contains exactly:
- TASK.md — stable task identity and authorized scope reference. Records the canonical contract pointer, allowed scope, non-goals, responsible role, review/handoff target, memory_root, package_path, creation timestamp, and authorized amendment list. TASK.md is an execution index and must not be used as a current-state record or to expand accepted authority.
- STATE.md — replaceable current operational snapshot. Records repository/worktree context, branch, last observed HEAD, durability evidence, changed-file boundary, unrelated/pre-existing changes, completed/remaining items, blockers, assumptions, unresolved items, checks, last safe checkpoint ID, exact next action, and an active-writer claim. STATE.md is authoritative only as an operational claim and must be verified against current evidence before acting.
- WORKLOG.md — append-only material checkpoint history. Each entry records a stable checkpoint ID, timestamp, actor, action, scope/files, commands/checks, evidence references, outcome (attempted, failed, partial, completed, reviewed, accepted, observed), concise rationale (when necessary), resulting state/implication, and correction links to earlier checkpoints.
- RESUME.md — concise derived re-entry packet. Summarizes current state, last safe checkpoint, read order, first verification commands, next implementation action, receiving role, writer-transfer/release status, and generated-from references to TASK.md, STATE.md, and relevant WORKLOG entries. RESUME.md is convenience only and must not replace the Handoff Protocol.

Schema compatibility and stop conditions

- This protocol supports `memory_schema_version: 1`. Every live TASK.md, STATE.md, WORKLOG.md, and RESUME.md in one package must declare that same supported version.
- A missing, blank, unsupported, or inconsistent version anywhere in the four-record package is `UNSUPPORTED_SCHEMA`. The receiver must stop before writing any package or task file and request an authorized migration, a compatible reader, or human reconciliation.
- A receiver must not infer a version from filenames or prose, update only one record to force agreement, or silently reinterpret fields from another version.
- A future schema migration must preserve the prior package as evidence and record its authority and result as an append-only WORKLOG checkpoint; this protocol does not authorize or automate such a migration.

Durability labels and evidence semantics

Declared durability labels:
- WORKTREE_ONLY — present only in the observed workspace; not evidence of sharing.
- COMMITTED_LOCAL — committed in the local Git history but not verified on a shared remote.
- REMOTE_BRANCH — pushed/verified on a named shared remote branch or equivalent shared reference.
- PR — included in a named pull request or equivalent review artifact; evidence must include the PR identifier and head ref.
- MERGED — included in an accepted merged reference; provide the merge commit or canonical reference.

Rules and invalid combinations:
- A package must declare its durability_state and the last_verified_persisted_ref (or NONE for WORKTREE_ONLY).
- WORKTREE_ONLY + "last_verified_persisted_ref: <remote>" is invalid; do not assert remote evidence when only a worktree was observed.
- COMMITTED_LOCAL requires a local commit ref; claiming REMOTE_BRANCH/PR/MERGED without matching remote/PR/merge evidence is invalid.
- PR and MERGED are distinct: PR indicates review artifact; MERGED indicates accepted integration. Do not conflate them.

Important: durability labels describe evidence availability only. They do not grant acceptance, approval, or authorization to perform Git operations.

Activation thresholds and LEVEL 0 exception

Activate a full four-file package when one or more of the following apply:
- work spans multiple sessions or roles;
- another runtime or logical role may need to continue it;
- quota or tool availability creates meaningful interruption risk;
- the task is blocked or plans destructive operations requiring a restore point;
- several files or departments are involved;
- the task is architectural, historical, security-sensitive, migration-related, or high-risk;
- the task contract explicitly requires persistent memory.

LEVEL 0 exception: a one-session micro-task that ends cleanly does not require activating a four-file package. LEVEL 0 handoffs remain the lightweight default for trivial reversible work. When a package is justified, all four files must be created; minimal or NOT_APPLICABLE content is acceptable for fields that do not apply.

Initialization, checkpoints, and update triggers

On activation/initialization:
1. declare memory_root and task_id in TASK.md;
2. create TASK.md, STATE.md, WORKLOG.md, and RESUME.md from templates;
3. declare memory_schema_version, durability_state, and last_verified_persisted_ref in STATE.md;
4. record repository context: branch, last_observed_HEAD, worktree summary, and pre-existing/unrelated changes;
5. append an initialization checkpoint to WORKLOG.md with a stable checkpoint ID;
6. populate RESUME.md with exact verification actions and the first authorized work action.

During execution, update STATE.md and append to WORKLOG.md only at material checkpoints, such as:
- creation or modification of a scope-relevant deliverable;
- deterministic checks that change confidence or state;
- new blockers or resolved blockers;
- responsibility transfer to another role;
- change in branch, worktree, or changed-file boundary;
- accepted decision or authorised task amendment;
- establishment of a safe rollback or recovery checkpoint.

Before planned interruption or handoff, refresh STATE.md, append a final material WORKLOG entry, regenerate RESUME.md, and attempt to release or transfer the writer claim. If the outgoing writer cannot release or refresh the claim, record the failure explicitly in WORKLOG and include guidance for evidence-based recovery.

Unplanned interruption and recovery

When an interruption prevents the outgoing writer from refreshing memory:
1. treat all memory as last-observed evidence rather than current truth;
2. inspect repository: branch, HEAD, worktree status, diffs, and relevant checks deterministically;
3. preserve pre-existing and unrelated changes;
4. identify the newest checkpoint supported by current evidence;
5. append a recovery entry to WORKLOG.md linking to the chosen checkpoint and describing verification steps performed;
6. refresh STATE.md and RESUME.md with the recovered facts, durability state, claim status, and remaining uncertainties;
7. enter BLOCKED when authorship, scope, secrets, destructive partial work, or accepted authority cannot be reconciled safely.

Recovery must be append-only. Do not rewrite history, manufacture completion evidence, or remove prior checkpoints.

Writer-claim lifecycle and concurrency

Writer-claim states and semantics:
- CLAIMED — one identified writer currently holds the active claim and is authorized to update STATE.md and RESUME.md.
- TRANSFER_PENDING — the outgoing writer has named an intended receiver; the receiver must verify before recording CLAIMED.
- RELEASED — no active writer claim; a new claimant may record CLAIMED after verifying current evidence.
- UNKNOWN — claim state cannot be reliably determined due to interruption, conflicting evidence, or missing context.

Rules:
- Only one unambiguous CLAIMED writer permits ordinary writes. Multiple simultaneous CLAIMED claims are a conflict that requires stop-and-reconcile.
- TRANSFER_PENDING does not permit the receiver to unilaterally write STATE.md until it verifies the transfer and records CLAIMED.
- Conflicting claims, simultaneous writers, or racing attempts must be resolved by creating child task packages or by manual reconciliation; do not resolve by overwriting another writer's history.
- The writer-claim lifecycle must be recorded in STATE.md and appended/annotated in WORKLOG.md as material checkpoints.

Reconciliation outcomes and required actions

When comparing memory to current evidence, receiving agents must decide and record one of the following outcomes and take the associated action:
- STALE_MEMORY — memory fields are contradicted by current evidence. Append a correction or recovery checkpoint to WORKLOG and refresh STATE.md/RESUME.md.
- UNRELATED_OR_PREEXISTING_CHANGE — preserve that change and exclude it from task ownership. Document files and continue only when scope remains safe.
- SCOPE_OR_AUTHORITY_CONFLICT — stop and request clarification or file a Change Proposal. Do not proceed.
- UNSUPPORTED_SCHEMA — a version is missing, blank, unsupported, or inconsistent across the four records; stop before writing and require an authorized migration, compatible reader, or human reconciliation.
- UNRESOLVED_REPOSITORY_STATE — enter BLOCKED and preserve the last safe state.

Distinguish attempted, completed, accepted, and failed work

- Attempted work: record as an entry in WORKLOG with outcome `attempted` or `partial`.
- Completed work: record with `completed` and cite deterministic evidence (commit, PR, test results) where applicable.
- Accepted work: include reviewer verdicts, QA/Integration results, PR/merge references, or explicit acceptance recorded in WORKLOG and STATE.md.
- Failed checks: record failures with evidence and resulting implications for next action.

Completion, QA evidence, and writer release

Before marking STATE.md `COMPLETE`:
- reconcile memory with current Git state, tests, validators, and accepted decisions;
- record required QA or review evidence with references (e.g., PR number, commit, QA report);
- state unresolved residual risks and the final disposition (commit, PR, merge reference or NONE);
- ensure RESUME.md does not instruct further implementation unless the task is formally reopened;
- append a completion checkpoint to WORKLOG and release the writer claim.

`COMPLETE` is invalid while any required check, review, or deliverable remains incomplete.

Retention and authorized reopening

- A completed package remains historical repository evidence in its declared memory root. Completion does not authorize pruning, deletion, relocation, compaction, or history rewriting.
- Only a separately authorized retention or archival task may move or remove a completed package. That task must preserve repository provenance and any references needed to locate the retained history. STUDIO-004 defines no automatic pruning policy.
- Editing STATE.md alone cannot reactivate a completed or inactive package. Reopening requires an authorized amendment to the canonical task contract or a new accepted task contract that explicitly identifies the package and reopened scope.
- On reopening, first verify the four-record schema, current repository/worktree evidence, accepted authority, and writer claim. Then append a reopening checkpoint to WORKLOG.md that cites the authorization, preserve the earlier completion checkpoint, update TASK.md's authorized amendment reference when applicable, acquire one verified CLAIMED writer, and refresh STATE.md and RESUME.md.
- If reopening authority or compatibility cannot be verified, leave the package COMPLETE or INACTIVE and enter the applicable stop-and-reconcile outcome; do not manufacture active work.

BLOCKED behavior and protections

Enter BLOCKED when safe continuation is impossible due to unresolved authorship, scope, secret exposure, destructive partial work, accepted-authority conflict, or unrecoverable repository state. When BLOCKED:
- preserve the last safe checkpoint and the full worktree state;
- append a BLOCKED checkpoint describing why and what minimal evidence is needed to unblock;
- do not attempt destructive cleanup or history rewriting to manufacture a resolvable state.

Append-only recovery and dirty-worktree protection

- Recovery must be append-only: append corrective checkpoints rather than rewriting or erasing history.
- Do not stage, commit, or discard unrelated or pre-existing work solely to make the memory package match the expected state. Preserve provenance.

Project Studio isolation and provenance

- Each Project Studio must declare its memory_root in PROJECT_STUDIO_TEMPLATE.md. Packages under one memory_root do not grant authority to other projects.
- Shared memory infrastructure may carry repository evidence, but it does not transfer project authority, canon, decisions, scope, acceptance status, or active-state ownership.
- Evidence intentionally reused across Project Studios must retain its source Project Studio, task/package path, checkpoint or immutable reference, scope, and acceptance status.
- Integration tasks may summarize accepted outputs from child packages but must not rewrite their worklogs or covertly change their acceptance status.

Security and context hygiene

- Prohibit secrets, credentials, private transcripts, or sensitive machine-specific data in memory files.
- Avoid machine-specific absolute paths; prefer repository-relative paths, branch names, and immutable refs.
- Evidence references should enable reproduction without copying sensitive output into memory.

Authority, precedence, and neutrality

- Accepted governance, Studio Owner directions, accepted decisions, canon, approved specifications, and the canonical task contract retain precedence. Memory records are operational evidence and cannot amend authority.
- Git diffs, commits, tests, and validators are deterministic operational evidence; memory cannot override them by recency.
- The protocol is runtime/model/provider neutral; it does not require or select any runtime, model, or provider.

References

See the canonical governance and handoff documents for binding rules and handoff levels: studio/STUDIO_CONSTITUTION.md, studio/HANDOFF_PROTOCOL.md, studio/PROJECT_STUDIO_TEMPLATE.md, studio/ACTIVATION_POLICY.md, and AGENTS.md.
