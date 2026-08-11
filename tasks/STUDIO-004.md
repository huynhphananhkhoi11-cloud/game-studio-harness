# STUDIO-004 — Establish Repository-Visible Persistent Memory

## 1. Goal

Establish a lightweight, repository-visible persistent-memory protocol so a suitable AI runtime can safely continue a bounded task after a session ends, a quota is exhausted, a tool becomes unavailable, or work is handed to another logical role.

The protocol is built around four records:

- `TASK` — stable execution identity and authorized task boundary;
- `STATE` — current operational snapshot;
- `WORKLOG` — append-only factual checkpoint history;
- `RESUME` — concise derived re-entry packet.

The memory system must remain runtime/model/provider neutral.

The protocol and templates introduced by this task use `memory_schema_version: 1`. Future automation must consume a declared schema version rather than infer structure from prose or filenames.

This task defines repository documentation and reusable templates only. It does not install a memory service, create a database, add embeddings, connect an AI provider, automate routing or failover, choose a game engine, implement gameplay, or create a real game project.

## 2. Contract Status

Status: `APPROVED`.

Approved by: Studio Owner.

Approval date: `2026-08-11`.

Contract revision: `0.3`.

Revision `0.3` change: correct the scope-validation procedure so the complete nine-file milestone is checked from repository baseline `12d5637`, while the implementation working tree and staged diff are checked against the eight authorized implementation files only.

Pre-amendment contract commit: `ed36920` (`0.2`). Revision `0.3` must be committed on `studio-v0.4` before implementation begins. That clean post-amendment commit becomes the implementation contract baseline; implementation agents must leave `tasks/STUDIO-004.md` unchanged relative to it.

Target memory schema: `1`.

Repository baseline: `main` at merge commit `12d5637`.

Implementation rules:

- implementation agents may read, cite, and validate work against it;
- implementation agents must not modify it;
- implementation agents must not weaken its acceptance criteria;
- implementation agents must not expand their own file scope;
- implementation agents must not treat memory records as authority to override accepted decisions, canon, governance, or the task contract.

If implementation exposes a genuine defect in this contract, report it as `UNRESOLVED` or submit a `CHANGE PROPOSAL` to the Studio Owner. Do not silently rewrite the task.

This approval resolves the documentation protocol only. Tool-backed shared memory, synchronization, automatic failover, retention automation, and schema migration tooling remain unresolved until separately scoped.

## 3. Context

Existing governance, topology, operational roles, and continuity rules already exist in:

- `AGENTS.md`
- `docs/GAME_VISION.md`
- `docs/DECISIONS.md`
- `studio/STUDIO_CONSTITUTION.md`
- `studio/STUDIO_TOPOLOGY.md`
- `studio/PLATFORM_STUDIO.md`
- `studio/PROJECT_STUDIO_TEMPLATE.md`
- `studio/ACTIVATION_POLICY.md`
- `studio/AGENT_REGISTRY.md`
- `studio/MODEL_REGISTRY.md`
- `studio/HANDOFF_PROTOCOL.md`
- the six profiles under `studio/agents/`

STUDIO-001 established governance and runtime-neutral handoff principles.

STUDIO-002 established six reusable logical agent roles.

STUDIO-003 established the hierarchical organization, Project Studio isolation, minimum-sufficient-team logic, dynamic Cells, Expert Guilds, and the Platform Studio capability boundary.

STUDIO-004 makes continuity operational at the documentation layer. It must complement, not replace, the existing Handoff Protocol.

## 4. Problem Statement

Repository evidence is already the required source of continuity, but the repository does not yet define a standard compact package for answering four practical questions:

1. What exactly is this task authorized to do?
2. What is true about the task right now?
3. What material work and checks have occurred?
4. What must the next suitable agent do first to resume safely?

Without a common structure, agents may rely on private chat history, duplicate stale summaries, lose the last safe checkpoint, confuse attempted work with accepted work, or continue from an incorrect branch or diff.

STUDIO-004 addresses this gap without creating an external memory service or a bureaucratic record for every trivial action.

## 5. Architectural Principles

### 5.1 Durable evidence, not hidden memory

Continuity must be recoverable from repository-visible files, Git state, accepted decisions, tests, validators, diffs, commits, and concise evidence.

Private conversation history and private chain-of-thought are never required inputs.

### 5.2 Write less, resume faster

Memory records must preserve only information that materially improves safe continuation, verification, or handoff.

Do not store full chat transcripts, raw model-output dumps, repetitive status narration, or speculative notes that do not affect the task.

### 5.3 One task, one memory package

When persistent memory is activated for a task, that task has one declared memory package containing all four record types.

Do not create competing `STATE` or `RESUME` files for the same task.

### 5.4 One record, one job

- `TASK` defines the stable execution identity and points to the authorized contract.
- `STATE` answers what is true now.
- `WORKLOG` records material events in order.
- `RESUME` tells a receiving agent how to re-enter safely.

No record may silently take over the job of another record.

### 5.5 Memory is allowed to be stale, but not silently trusted

Every receiving agent must compare memory against current repository evidence before writing.

A stale memory record is a recoverable operational defect. It is not permission to ignore Git, tests, accepted decisions, or the current task contract.

### 5.6 Runtime neutrality

`AGENT ROLE != RUNTIME != MODEL != PROVIDER`

The memory format must remain usable when work moves among different sessions, tools, runtimes, models, or providers.

### 5.7 Declared durability, not assumed durability

A file inside a worktree is repository-visible but is not necessarily available to another machine or runtime. Memory must declare its last verified durability state and must not imply that uncommitted or unpushed work has been shared.

Allowed durability states are:

- `WORKTREE_ONLY` — present only in the last observed workspace;
- `COMMITTED_LOCAL` — recorded in local Git history but not verified on a shared remote;
- `REMOTE_BRANCH` — verified on a named shared remote branch or equivalent shared reference;
- `PR` — included in a named pull request or equivalent review artifact;
- `MERGED` — included in an accepted merged reference.

These labels describe evidence availability. They do not authorize Git operations or confer acceptance.

### 5.8 Versioned records

Every live memory record must declare `memory_schema_version`. A receiver must stop and reconcile when the version is missing, unsupported, or inconsistent across the package.

## 6. Authority and Trust Boundaries

### 6.1 Binding authority

The Studio Owner retains final binding and non-reversible authority under `studio/STUDIO_CONSTITUTION.md`.

Memory records do not create a new owner, manager, approver, or executive layer.

### 6.2 Task authority

`TASK.md` is not automatically a new task contract. When an accepted canonical task contract exists, `TASK.md` must reference it and must not weaken, broaden, or replace it.

If the task contract and a memory record conflict, the accepted task contract wins.

### 6.3 Accepted decisions and canon

Memory records may point to accepted decisions, canon, architecture, and constraints. They may not silently modify their status or scope.

A proposed change remains a `PROPOSAL` until the applicable governance accepts it.

### 6.4 Operational assertions

Statements such as “tests pass,” “worktree is clean,” “file completed,” or “PR merged” must be supported by current deterministic evidence or clearly marked as the last observed state with a timestamp and reference.

### 6.5 No authority by recency

A newer `STATE`, `WORKLOG`, or `RESUME` entry does not outrank an accepted decision merely because it is newer.

## 7. Memory Package Model

The reusable package shape is:

```text
<MEMORY_ROOT>/<TASK-ID>/
├── TASK.md
├── STATE.md
├── WORKLOG.md
└── RESUME.md
```

The active context must declare `<MEMORY_ROOT>`.

- Studio-wide work defaults to `studio/memory/tasks/<TASK-ID>/`.
- A future Project Studio defaults to `<PROJECT_NAMESPACE>/memory/tasks/<TASK-ID>/` and must declare that isolated root in its Project Studio record.
- Memory from one Project Studio must not silently become binding or operational state for another Project Studio.
- Parallel subtasks that can change independently must use distinct task IDs and distinct packages.

STUDIO-004 creates templates only. It does not create a live package for a fictional project.

Every live package must also declare:

- `memory_schema_version`;
- package path and canonical task-contract reference;
- current durability state;
- last verified persisted reference, or `NONE` when the package is `WORKTREE_ONLY`;
- last safe checkpoint ID.

Machine-specific absolute paths are not portable task identity. Use repository-relative paths, worktree labels, branch names, and immutable references wherever possible.

### 7.1 Activation threshold

A full memory package is justified when one or more conditions apply:

- work is expected to span multiple sessions;
- another runtime or logical role may need to continue it;
- quota or tool availability creates a meaningful interruption risk;
- the task is blocked and must preserve a last safe state;
- several files or departments are involved;
- the task is architectural, historical, security-sensitive, migration-related, or otherwise high-risk;
- the task contract explicitly requires persistent memory.

A one-session micro-task that ends cleanly does not require a permanent four-file package solely for ceremony. Existing LEVEL 0 handoff remains available.

Once a package is activated, all four files must exist, even when some sections are intentionally minimal or `NOT APPLICABLE`.

## 8. `TASK.md` Semantics

`TASK.md` is the stable execution index for one memory package.

It must contain:

- `memory_schema_version`;
- `task_id`;
- `task_title`;
- `task_type` or risk/handoff level where applicable;
- canonical task-contract path or identifier;
- declared context or Project Studio;
- goal;
- allowed scope;
- explicitly allowed files or scope rule;
- non-goals;
- acceptance-criteria reference;
- relevant accepted constraints and decision references;
- responsible logical role or Cell;
- intended QA/review/handoff target;
- memory-root and package-path declaration;
- creation timestamp and accepted amendment references, if any.

Rules:

- Prefer references to canonical sources over copying large sections.
- Do not record private chain-of-thought.
- Do not broaden scope based on inferred intent.
- Do not rewrite `TASK.md` merely because execution status changes; that belongs in `STATE.md`.
- Any authorized amendment must identify who authorized it, when, and which canonical task or decision record changed.
- If no accepted task contract exists, `TASK.md` remains a scoped execution proposal until the applicable authority accepts the work.

## 9. `STATE.md` Semantics

`STATE.md` is the current operational snapshot. It is intentionally replaceable rather than append-only.

It must contain:

- `memory_schema_version`;
- `task_id`;
- current state: `READY`, `ACTIVE`, `BLOCKED`, `HANDOFF`, `COMPLETE`, or `INACTIVE` where applicable;
- current logical role or Cell;
- branch and worktree or repository context;
- last observed `HEAD` or equivalent immutable reference when Git is used;
- durability state and last verified persisted reference;
- worktree status summary;
- actual changed-file boundary;
- pre-existing or unrelated changed files that must be preserved;
- completed items;
- remaining items;
- blockers and unblock conditions;
- assumptions and unresolved items;
- latest checks and their results;
- last safe checkpoint ID;
- exact next action;
- active-writer claim: logical role or agent ID, claim status, and claim timestamp;
- `updated_at` timestamp with timezone;
- updater identity at the logical-role level.

Rules:

- `STATE.md` describes what is currently believed to be true; it does not preserve history.
- Replace stale fields when material state changes.
- Use explicit values such as `NONE`, `NOT RUN`, `UNKNOWN`, or `UNRESOLVED`; do not leave ambiguity hidden in blank fields.
- A claim about Git or tests must include the last observed evidence reference or be rechecked before use.
- `WORKTREE_ONLY` must not be described as shared, committed, pushed, reviewed, or merged.
- Pre-existing or unrelated changes must not be attributed to the active task or overwritten.
- An active-writer claim is coordination evidence, not an infallible lock. A conflicting or ambiguous claim requires stop-and-reconcile before writes continue.
- `COMPLETE` is not valid when required checks, review, or deliverables remain incomplete.
- `BLOCKED` must preserve the last safe state and a concrete unblock condition.

## 10. `WORKLOG.md` Semantics

`WORKLOG.md` is an append-only factual checkpoint log for material events.

Each entry must contain, as applicable:

- `memory_schema_version` at document level;
- a unique checkpoint ID within the task package;
- timestamp with timezone;
- logical role or agent ID;
- action or checkpoint;
- files or scope affected;
- command, check, source, or evidence reference;
- outcome;
- concise rationale when it is necessary for continuation;
- resulting state or next implication.

Rules:

- Append material checkpoints; do not narrate every click, prompt, or token.
- Record facts about attempted and completed work distinctly.
- Record failed checks and rejected approaches when they materially affect the next action.
- Corrections are appended and linked to the earlier entry; do not silently rewrite history to hide an error.
- Checkpoint IDs must remain stable so `STATE.md` and `RESUME.md` can reference the same last safe point.
- Use checkpoint IDs in the form `<TASK-ID>-CP-####`, increasing within that task package.
- Use ISO 8601 timestamps with an explicit UTC offset.
- Do not store private chain-of-thought, full conversations, secrets, credentials, or unnecessary personal data.
- Do not use “the previous AI said so” as evidence.
- Runtime/model details are optional and should be recorded only when useful for debugging, reproducibility, evaluation, or failover.

## 11. `RESUME.md` Semantics

`RESUME.md` is a concise derived re-entry packet. It is refreshed at a safe checkpoint and may be replaced as the task evolves.

It must contain:

- `memory_schema_version`;
- `task_id` and canonical task-contract reference;
- current state and last safe checkpoint ID;
- required read order;
- branch/worktree and last observed `HEAD`;
- durability state and last verified persisted reference;
- expected worktree status and changed files;
- pre-existing or unrelated changes that the receiver must preserve;
- completed and remaining summary;
- blockers and unresolved authority questions;
- latest relevant checks;
- exact first verification commands or actions;
- exact next implementation action after verification;
- receiving role or handoff target;
- writer-transfer or release status;
- `generated_from` references to `TASK.md`, `STATE.md`, and relevant `WORKLOG.md` entries;
- `updated_at` timestamp with timezone.

Rules:

- `RESUME.md` is a derivative convenience document, not an independent authority source.
- It must remain short enough for a new agent to use before loading optional detail.
- It must never claim a clean worktree, passing check, current branch, or merged state without telling the receiver to verify current evidence.
- It must not imply that `WORKTREE_ONLY` evidence is available outside the last observed workspace.
- It must not duplicate the full task contract, complete worklog, or complete Handoff Protocol.
- When a formal handoff occurs, `RESUME.md` points to the applicable LEVEL 0/1/2 handoff evidence rather than replacing that protocol.

## 12. Lifecycle and Update Triggers

### 12.1 Initialize

When persistent memory is activated:

1. declare the memory root and task ID;
2. create all four files from the templates;
3. link `TASK.md` to the canonical task contract;
4. declare `memory_schema_version`, durability state, and last persisted reference;
5. record the verified initial branch, `HEAD`, worktree status, pre-existing/unrelated changes, and active-writer claim in `STATE.md`;
6. append an initialization checkpoint with a stable checkpoint ID to `WORKLOG.md`;
7. create an immediately actionable `RESUME.md` containing the initial verification actions and first authorized work action.

`RESUME.md` must never begin as an empty or `NOT YET REQUIRED` placeholder. An unexpected interruption can occur before the next planned checkpoint.

### 12.2 During execution

Update `STATE.md` and append `WORKLOG.md` only at material checkpoints, including:

- a scope-relevant deliverable is created or changed;
- a deterministic check changes the task’s confidence or status;
- a blocker appears or is removed;
- responsibility moves to another logical role;
- the branch, worktree, or changed-file boundary materially changes;
- an accepted decision or task amendment changes execution;
- a safe rollback or recovery checkpoint is established.

Before a long-running, destructive, hard-to-reproduce, or interruption-sensitive action, create a material checkpoint when losing the current state would impose meaningful recovery cost. This does not require logging every ordinary command.

### 12.3 Before interruption or handoff

Refresh `STATE.md`, append a final material `WORKLOG.md` entry, and regenerate `RESUME.md` before:

- session end with unfinished work;
- expected quota exhaustion;
- runtime/model/provider replacement;
- tool failure that prevents safe continuation;
- transfer to QA, Review, Integration, or another specialist;
- leaving a dirty worktree for another agent;
- entering `BLOCKED` or `HANDOFF`.

The outgoing writer must mark its writer claim as released or explicitly transferred. If it cannot do so, the receiver treats the claim and all memory after the last safe checkpoint as potentially stale.

### 12.4 Unplanned interruption recovery

When interruption occurs before the outgoing agent can refresh memory, the receiving agent must:

1. treat all memory as last-observed evidence rather than current truth;
2. inspect the repository, branch, `HEAD`, worktree, diff, and relevant checks before writing;
3. preserve pre-existing and unrelated changes;
4. identify the newest checkpoint that is supported by current evidence;
5. append a recovery entry to `WORKLOG.md` rather than rewriting prior history;
6. refresh `STATE.md` and `RESUME.md` with the recovered facts, durability state, writer claim, and remaining uncertainty;
7. enter `BLOCKED` when authorship, scope, secrets, destructive partial work, or accepted authority cannot be reconciled safely.

Recovery must not manufacture a clean checkpoint or claim that unfinished work was completed.

### 12.5 Completion

Before marking `COMPLETE`:

- reconcile memory with current Git and test evidence;
- record required QA/review verdicts;
- state unresolved residual risk;
- record the final disposition, commit, PR, or merge reference when one exists;
- ensure `RESUME.md` does not instruct further implementation unless the task is explicitly reopened.

Completion does not itself authorize commit, push, PR creation, or merge.

The writer claim must be released when the task becomes `COMPLETE` or `INACTIVE`.

### 12.6 Retention and reopening

A completed package remains historical repository evidence unless a separately authorized retention or archival task moves or removes it. STUDIO-004 does not define automated pruning.

A completed package must not return to active use solely because an agent edits `STATE.md`. Reopening requires an authorized task amendment or a new task contract, and the reopening event must be appended to `WORKLOG.md`.

## 13. Reconciliation and Precedence

Before resuming writes, a receiving agent must:

1. read `AGENTS.md`;
2. read the accepted task contract and relevant accepted decisions/specifications;
3. read `TASK.md`, `STATE.md`, and `RESUME.md`;
4. verify `memory_schema_version`, durability state, last persisted reference, last safe checkpoint, and writer claim;
5. inspect the current repository, branch, `HEAD`, worktree status, diff, pre-existing/unrelated changes, and relevant tests/checks;
6. read only the `WORKLOG.md` entries needed to resolve uncertainty or recover rationale;
7. compare memory claims with current deterministic evidence;
8. stop and reconcile any material mismatch before writing.

When evidence conflicts, use the authority order in `studio/STUDIO_CONSTITUTION.md`.

Operationally:

- accepted governance, decisions, canon, task contract, and approved specifications retain their existing authority;
- current Git state, diffs, tests, and validators establish operational evidence but do not silently amend accepted authority;
- `STATE.md` is a current operational claim that must be verified;
- `WORKLOG.md` is historical evidence of observed actions and outcomes;
- `RESUME.md` is a derivative navigation aid.

Never resolve a conflict by selecting whichever memory record is most convenient.

Reconciliation outcomes must be explicit:

- `STALE_MEMORY` — current evidence is clear; append a correction/recovery checkpoint and refresh derived records;
- `UNRELATED_OR_PREEXISTING_CHANGE` — preserve it, exclude it from task ownership, and continue only if scope remains safe;
- `SCOPE_OR_AUTHORITY_CONFLICT` — stop and request the applicable clarification or change proposal;
- `UNSUPPORTED_SCHEMA` — stop until the package is migrated or a compatible reader is used;
- `UNRESOLVED_REPOSITORY_STATE` — enter `BLOCKED` rather than guessing.

## 14. Concurrency and Isolation

### 14.1 Single-writer state

Only one active writer may update a task package’s `STATE.md` and `RESUME.md` at a time.

If parallel work can proceed independently, create distinct child task IDs and memory packages rather than allowing concurrent writers to race on the same current-state files.

Before taking the writer role, a receiving agent must verify the existing claim and record a new claim or an accepted transfer. A claim should include logical role or agent ID, status, and timezone-qualified timestamp.

Allowed writer-claim statuses are:

- `CLAIMED` — one identified writer is active;
- `TRANSFER_PENDING` — the outgoing writer has named an intended receiver, but the receiver has not yet claimed the package;
- `RELEASED` — no writer currently holds the package;
- `UNKNOWN` — an interruption or mismatch prevents a trustworthy ownership conclusion.

Only `CLAIMED` with one unambiguous current writer permits ordinary writes. `TRANSFER_PENDING` and `UNKNOWN` require reconciliation; the receiver records its own `CLAIMED` state only after verification.

This manual claim is not a distributed lock. When two plausible active claims exist, neither writer may resolve the race by overwriting the other; stop and reconcile or split the work into authorized child tasks.

### 14.2 Worklog ownership

Each entry identifies its logical role or agent ID. Parallel child tasks retain separate worklogs until an authorized integration task reconciles them.

### 14.3 Project isolation

Each Project Studio declares its own memory root. Project-specific state, canon, assumptions, and task history must not leak into another project by default.

Shared evidence must retain provenance and scope. Shared memory infrastructure does not create shared project authority.

### 14.4 Integration

An integration task may summarize accepted outputs from child packages, but it must not rewrite their historical worklogs or silently convert proposals into accepted decisions.

### 14.5 Dirty-worktree protection

The current task must distinguish its own changed files from pre-existing or unrelated changes. Agents must not discard, overwrite, stage, attribute, or clean unrelated work merely to make the memory package match an expected state.

If the distinction cannot be established safely, enter `BLOCKED` and preserve the worktree.

## 15. Security, Privacy, and Context Hygiene

Memory records must not contain:

- API keys, OAuth tokens, cookies, credentials, secret URLs, or private keys;
- payment or billing secrets;
- private chain-of-thought;
- full private chat transcripts;
- unnecessary personal or sensitive data;
- copied copyrighted material beyond what the project is permitted to retain;
- large raw logs or model dumps when a concise evidence reference is sufficient;
- unredacted environment dumps or command output that may expose secrets or personal machine data;
- machine-specific absolute user-directory paths when a repository-relative reference or workspace label is sufficient.

Use repository references, redacted summaries, hashes, command names, test results, source citations, and concise rationale instead.

Evidence references must preserve enough detail to reproduce or locate the evidence without copying sensitive output into memory.

If a secret is discovered in memory, stop further propagation, report the exposure, and follow the applicable security and credential-rotation workflow. STUDIO-004 does not implement that workflow.

## 16. Anti-Bureaucracy and Canonical-Home Rule

`ONE RULE → ONE CANONICAL HOME`

Canonical ownership after STUDIO-004:

- persistent-memory lifecycle, schema, durability labels, recovery, retention, and record semantics → `studio/MEMORY_PROTOCOL.md`;
- handoff levels and handoff package requirements → `studio/HANDOFF_PROTOCOL.md`;
- shared governance authority → `studio/STUDIO_CONSTITUTION.md`;
- project-specific memory-root declaration and isolation → `studio/PROJECT_STUDIO_TEMPLATE.md`;
- activation states → `studio/ACTIVATION_POLICY.md`;
- repository-wide agent entry behavior → `AGENTS.md`;
- reusable record structures → `studio/memory/templates/`.

Other documents should link to these rules rather than restating them in full.

Do not require:

- updates after every prompt or command;
- mandatory daily reports or meetings;
- a full package for a trivial task completed safely in one session;
- duplicate status summaries across multiple files;
- retention of irrelevant exploration;
- a coordinator approval for every memory update;
- a new management role to maintain memory.

A record is justified only when it materially improves continuity, correctness, recovery, verification, isolation, or delivery.

## 17. Required Files

The Studio Owner creates and maintains this task contract:

- `tasks/STUDIO-004.md`

Implementation agents must not modify it.

Implementation scope:

Create:

- `studio/MEMORY_PROTOCOL.md`
- `studio/memory/templates/TASK.md`
- `studio/memory/templates/STATE.md`
- `studio/memory/templates/WORKLOG.md`
- `studio/memory/templates/RESUME.md`

Modify:

- `AGENTS.md`
- `studio/HANDOFF_PROTOCOL.md`
- `studio/PROJECT_STUDIO_TEMPLATE.md`

No other repository file may be changed.

Final STUDIO-004 milestone footprint therefore consists of:

- six new files total, including this task contract;
- three existing files modified.

## 18. Required Content by File

### `studio/MEMORY_PROTOCOL.md`

This is the canonical home for:

- memory activation threshold;
- four-record package model;
- `memory_schema_version: 1` and compatibility behavior;
- durability-state labels and the rule that worktree presence is not proof of sharing;
- semantics and authority boundaries of `TASK`, `STATE`, `WORKLOG`, and `RESUME`;
- initialization, checkpoint, interruption, handoff, and completion triggers;
- unplanned-interruption recovery;
- reconciliation with Git, tests, decisions, and task contracts;
- staleness handling;
- active-writer claims, concurrency, and single-writer rules;
- dirty-worktree and unrelated-change protection;
- Project Studio isolation;
- completion retention and authorized reopening;
- security and context-hygiene rules;
- anti-bureaucracy limits.

It must reference existing canonical governance and handoff documents rather than duplicate them.

### `studio/memory/templates/TASK.md`

Must provide reusable placeholders for:

- memory schema version;
- task identity and title;
- canonical contract reference;
- context/Project Studio;
- goal;
- allowed scope and files;
- non-goals;
- accepted constraints and decision references;
- acceptance-criteria reference;
- responsible logical role/Cell;
- review/handoff target;
- memory-root declaration;
- timestamp and authorized amendments.

It must state that the template does not override the canonical task contract.

### `studio/memory/templates/STATE.md`

Must provide reusable placeholders for:

- memory schema version;
- current activation state;
- logical role/Cell;
- branch, worktree, and last observed `HEAD`;
- durability state and last verified persisted reference;
- worktree-status summary, task-attributed changed files, and pre-existing/unrelated changed files;
- completed, remaining, blockers, assumptions, and unresolved items;
- latest checks;
- last safe checkpoint ID;
- exact next action;
- active-writer claim, allowed claim status, and timestamp;
- timezone-qualified timestamp and updater.

It must distinguish current snapshot from historical log.

### `studio/memory/templates/WORKLOG.md`

Must provide an append-only entry structure with:

- memory schema version at document level;
- stable checkpoint ID;
- timestamp;
- logical role/agent ID;
- action or checkpoint;
- scope/files;
- command, check, source, or evidence;
- outcome;
- concise rationale where necessary;
- resulting state or next implication;
- correction-link behavior.

It must explicitly prohibit full transcripts, private chain-of-thought, secrets, and low-value narration.

### `studio/memory/templates/RESUME.md`

Must provide reusable placeholders for:

- memory schema version;
- task/contract identity;
- current state and last safe checkpoint ID;
- required read order;
- branch/worktree/last observed `HEAD`;
- durability state and last verified persisted reference;
- expected worktree state, task-attributed changes, and unrelated/pre-existing changes to preserve;
- completed/remaining summary;
- blockers and unresolved authority questions;
- latest checks;
- first verification actions;
- next implementation action after verification;
- receiving role;
- writer release or transfer status;
- source-memory references;
- timezone-qualified timestamp.

It must state that it is derived, must be verified, and does not replace the Handoff Protocol.

### `AGENTS.md`

Modify only enough to require an agent resuming a task with an activated memory package to:

- follow `studio/MEMORY_PROTOCOL.md`;
- read the canonical task/decisions plus `TASK.md`, `STATE.md`, and `RESUME.md`;
- verify schema version, writer claim, durability state, memory claims, current Git, unrelated changes, and test evidence before writing;
- avoid secrets, transcripts, and private chain-of-thought;
- update memory only at material checkpoints and within task scope.

Do not rewrite unrelated repository instructions.

### `studio/HANDOFF_PROTOCOL.md`

Modify only enough to clarify:

- persistent memory is ongoing operational continuity;
- handoff is a transfer event with LEVEL 0/1/2 requirements;
- `RESUME.md` may point to a handoff but does not replace it;
- interruption and runtime-failure handoffs should refresh the applicable memory package when one is activated;
- unplanned interruption requires evidence-based recovery when the outgoing writer could not refresh or release its claim.

Preserve existing handoff levels, outcomes, role boundaries, and anti-bureaucracy intent.

### `studio/PROJECT_STUDIO_TEMPLATE.md`

Modify only enough to add:

- a declared project-specific memory root;
- the four-record task-package reference;
- the memory schema-version and durability-state requirement;
- project-isolation and provenance rules;
- a note that shared memory infrastructure does not transfer project authority.

Do not create a named project, game, story, canon, engine, provider assignment, or new executive authority.

## 19. Non-Goals

STUDIO-004 must not:

- install tools or dependencies;
- create a database, vector store, knowledge graph, embedding index, cache, or external memory service;
- connect AI providers or accounts;
- create API keys, OAuth flows, credentials, or secrets;
- adopt a particular runtime, model, provider, router, or orchestration framework;
- implement automatic routing, failover, scheduling, synchronization, or background agents;
- create Git hooks, CI workflows, bots, daemons, or validation scripts;
- alter protected-branch or repository permissions;
- choose a game engine, programming language, framework, or gameplay architecture;
- define game vision, mechanics, story, canon, art, audio, economy, or release scope;
- create a real or fictional Project Studio;
- migrate all historical tasks into memory packages;
- create a live memory package merely as an example;
- require memory updates after every interaction;
- make Producer a universal memory gate;
- create a Memory Owner, Project Owner, Project Studio Owner, Platform Studio Owner, or equivalent executive role;
- modify existing STUDIO-002 agent profiles;
- modify this task contract;
- treat this contract as standing authorization to commit, push, open a PR, or merge.

Automation and tool-backed memory may be evaluated only in a later separately scoped milestone.

Git publication remains governed by `AGENTS.md` and the Studio Owner's explicit instruction. A user-authorized feature-branch commit or PR may be used as a review artifact after local validation; no merge is permitted before required independent review and Studio Owner/workflow approval.

## 20. Acceptance Criteria

- [ ] `tasks/STUDIO-004.md` remains unchanged by implementation agents.
- [ ] Exactly five new implementation documents exist: one protocol and four templates.
- [ ] Only `AGENTS.md`, `studio/HANDOFF_PROTOCOL.md`, and `studio/PROJECT_STUDIO_TEMPLATE.md` are modified among pre-existing files.
- [ ] `studio/MEMORY_PROTOCOL.md` is the single canonical home for persistent-memory lifecycle and record semantics.
- [ ] The reusable package contains exactly `TASK.md`, `STATE.md`, `WORKLOG.md`, and `RESUME.md`.
- [ ] Protocol and all four templates declare `memory_schema_version: 1`.
- [ ] `TASK.md` points to authorized scope and cannot override the canonical task contract.
- [ ] `STATE.md` is a replaceable current snapshot rather than historical narration.
- [ ] `STATE.md` distinguishes task-attributed changes from pre-existing or unrelated work and preserves the latter.
- [ ] `STATE.md` records an active-writer claim, durability state, last persisted reference, and last safe checkpoint ID.
- [ ] `WORKLOG.md` is append-only, uses stable checkpoint IDs, and records only material factual checkpoints.
- [ ] `RESUME.md` is concise, derived, and explicitly requires verification.
- [ ] `RESUME.md` is actionable from initialization and is never an empty `NOT YET REQUIRED` placeholder.
- [ ] `WORKTREE_ONLY` is not represented as shared, committed, pushed, reviewed, or merged.
- [ ] Handoff LEVEL 0/1/2 remains canonical in `studio/HANDOFF_PROTOCOL.md`.
- [ ] Persistent memory and handoff are clearly distinguished.
- [ ] Receiving agents must reconcile memory with current Git, tests, accepted decisions, and the task contract before writing.
- [ ] Stale or contradictory memory produces a stop-and-reconcile action rather than silent continuation.
- [ ] Unplanned interruption has an evidence-based recovery procedure that appends history rather than fabricating completion.
- [ ] Missing or unsupported schema versions produce stop-and-reconcile behavior.
- [ ] Runtime/model/provider neutrality is explicit.
- [ ] Private chat history and private chain-of-thought are not required.
- [ ] Secrets, credentials, full transcripts, and unnecessary sensitive data are prohibited.
- [ ] Project Studio memory roots remain isolated.
- [ ] Parallel independent work uses distinct task IDs/packages rather than concurrent `STATE.md` writers.
- [ ] An ambiguous or conflicting active-writer claim blocks writes until reconciled.
- [ ] Writer-claim status uses `CLAIMED`, `TRANSFER_PENDING`, `RELEASED`, or `UNKNOWN` with only one unambiguous `CLAIMED` writer allowed.
- [ ] Memory records do not create binding authority or new executive roles.
- [ ] Studio Owner remains final binding/non-reversible authority.
- [ ] Producer remains coordination-focused and is not a universal memory gate.
- [ ] Micro-tasks are not forced into full persistent-memory ceremony.
- [ ] Completion retention and authorized reopening behavior are explicit.
- [ ] Existing governance, topology, activation states, and six agent profiles remain valid.
- [ ] No runtime, provider, model, tool, dependency, database, engine, language, framework, game, or canon is selected or implemented.
- [ ] No hidden conversation or private reasoning is treated as project truth.
- [ ] No file outside the declared scope is changed.
- [ ] This contract does not itself authorize commit, push, PR creation, or merge; publication follows `AGENTS.md` and explicit Studio Owner instruction.

## 21. Deterministic Content Validation

Before STUDIO-004 may be considered complete, run a fail-fast invariant check in Windows PowerShell 5.1 or later:

```powershell
$ErrorActionPreference = "Stop"

$required = @(
    "studio/MEMORY_PROTOCOL.md",
    "studio/memory/templates/TASK.md",
    "studio/memory/templates/STATE.md",
    "studio/memory/templates/WORKLOG.md",
    "studio/memory/templates/RESUME.md"
)

$missing = $required | Where-Object { -not (Test-Path $_ -PathType Leaf) }
if ($missing) {
    throw "Missing required file(s): $($missing -join ', ')"
}

$mustContain = @{
    "studio/MEMORY_PROTOCOL.md" = @(
        "memory_schema_version",
        "TASK.md", "STATE.md", "WORKLOG.md", "RESUME.md",
        "WORKTREE_ONLY", "COMMITTED_LOCAL", "REMOTE_BRANCH", "PR", "MERGED",
        "unplanned", "single-writer", "retention"
    )
    "studio/memory/templates/TASK.md" = @(
        "memory_schema_version", "task_id", "canonical", "memory"
    )
    "studio/memory/templates/STATE.md" = @(
        "memory_schema_version",
        "READY", "ACTIVE", "BLOCKED", "HANDOFF", "COMPLETE", "INACTIVE",
        "durability", "checkpoint", "writer", "unrelated",
        "CLAIMED", "TRANSFER_PENDING", "RELEASED", "UNKNOWN"
    )
    "studio/memory/templates/WORKLOG.md" = @(
        "memory_schema_version", "checkpoint", "timestamp", "outcome", "correction"
    )
    "studio/memory/templates/RESUME.md" = @(
        "memory_schema_version", "checkpoint", "durability", "verify", "writer"
    )
}

foreach ($path in $mustContain.Keys) {
    $content = Get-Content -Raw -Path $path
    foreach ($token in $mustContain[$path]) {
        if ($content -notmatch [regex]::Escape($token)) {
            throw "Missing required token '$token' in $path"
        }
    }
}

$entryPoints = @(
    "AGENTS.md",
    "studio/HANDOFF_PROTOCOL.md",
    "studio/PROJECT_STUDIO_TEMPLATE.md"
)

foreach ($path in $entryPoints) {
    $content = Get-Content -Raw -Path $path
    if ($content -notmatch [regex]::Escape("MEMORY_PROTOCOL.md")) {
        throw "Missing MEMORY_PROTOCOL.md reference in $path"
    }
}

"PASS: STUDIO-004 deterministic content invariants"
```

Expected final line:

```text
PASS: STUDIO-004 deterministic content invariants
```

Deterministic token checks cannot prove semantic safety. After they pass, inspect suspicious scope- or authority-expanding wording:

```powershell
$paths = @(
    "studio/MEMORY_PROTOCOL.md",
    "studio/memory/templates/TASK.md",
    "studio/memory/templates/STATE.md",
    "studio/memory/templates/WORKLOG.md",
    "studio/memory/templates/RESUME.md",
    "AGENTS.md",
    "studio/HANDOFF_PROTOCOL.md",
    "studio/PROJECT_STUDIO_TEMPLATE.md"
)

Select-String `
    -Path $paths `
    -Pattern "memory.*overrid", `
             "resume.*authoriz", `
             "worklog.*approv", `
             "state.*binding" `
    -CaseSensitive:$false
```

Every result must be manually inspected. Wording that grants memory records binding authority, scope-expansion authority, approval authority, or permission to bypass accepted decisions must be rejected or rewritten. Prohibitive wording is allowed.

## 22. Scope and Diff Validation

Revision `0.3` must already be committed, and the worktree must be clean, before implementation begins. Use separate exact comparisons for:

1. the complete nine-file milestone relative to repository baseline `12d5637`; and
2. the eight implementation files currently changed in the working tree.

```powershell
$ErrorActionPreference = "Stop"
$milestoneBaseline = "12d5637"

$implementationFiles = @(
    "AGENTS.md",
    "studio/HANDOFF_PROTOCOL.md",
    "studio/PROJECT_STUDIO_TEMPLATE.md",
    "studio/MEMORY_PROTOCOL.md",
    "studio/memory/templates/TASK.md",
    "studio/memory/templates/STATE.md",
    "studio/memory/templates/WORKLOG.md",
    "studio/memory/templates/RESUME.md"
)

$milestoneFiles = @($implementationFiles) + @("tasks/STUDIO-004.md")

git cat-file -e "$milestoneBaseline`^{commit}"
if ($LASTEXITCODE -ne 0) {
    throw "Missing milestone baseline commit: $milestoneBaseline"
}

$untracked = @(git ls-files --others --exclude-standard)
if ($LASTEXITCODE -ne 0) { throw "Unable to enumerate untracked files" }

$milestoneDiff = @(git diff --name-only $milestoneBaseline --)
if ($LASTEXITCODE -ne 0) {
    throw "Unable to compare milestone against baseline $milestoneBaseline"
}

$milestoneChanged = @(
    $milestoneDiff
    $untracked
) | Where-Object { $_ } | Sort-Object -Unique

$unexpectedMilestone = $milestoneChanged | Where-Object { $_ -notin $milestoneFiles }
$missingMilestone = $milestoneFiles | Where-Object { $_ -notin $milestoneChanged }

if ($unexpectedMilestone) {
    throw "Out-of-scope milestone file(s): $($unexpectedMilestone -join ', ')"
}
if ($missingMilestone) {
    throw "Expected milestone file(s) absent from baseline diff: $($missingMilestone -join ', ')"
}

$implementationChanged = @(
    @(git diff --name-only)
    @(git diff --cached --name-only)
    $untracked
) | Where-Object { $_ } | Sort-Object -Unique

$unexpectedImplementation = $implementationChanged |
    Where-Object { $_ -notin $implementationFiles }
$missingImplementation = $implementationFiles |
    Where-Object { $_ -notin $implementationChanged }

if ($unexpectedImplementation) {
    throw "Out-of-scope implementation file(s): $($unexpectedImplementation -join ', ')"
}
if ($missingImplementation) {
    throw "Expected implementation file(s) not changed: $($missingImplementation -join ', ')"
}

$contractChanges = @(
    @(git diff --name-only -- "tasks/STUDIO-004.md")
    @(git diff --cached --name-only -- "tasks/STUDIO-004.md")
) | Where-Object { $_ } | Sort-Object -Unique

if ($contractChanges) {
    throw "Implementation modified the approved task contract: $($contractChanges -join ', ')"
}

git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }

"PASS: exact STUDIO-004 milestone and working-tree scope"
```

Expected final line:

```text
PASS: exact STUDIO-004 milestone and working-tree scope
```

Because untracked files are not covered by ordinary `git diff --check`, stage only the eight implementation files after the preceding check. Then run final whitespace and exact staged-scope validation:

```powershell
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }

$cached = @(git diff --cached --name-only) | Where-Object { $_ } | Sort-Object -Unique
$unexpectedCached = $cached | Where-Object { $_ -notin $implementationFiles }
$missingCached = $implementationFiles | Where-Object { $_ -notin $cached }

if ($unexpectedCached) {
    throw "Out-of-scope staged file(s): $($unexpectedCached -join ', ')"
}
if ($missingCached) {
    throw "Expected implementation file(s) not staged: $($missingCached -join ', ')"
}
if ($cached -contains "tasks/STUDIO-004.md") {
    throw "Approved task contract must not be staged by implementation agents"
}

git diff --cached --stat
git status --short

"PASS: exact STUDIO-004 staged implementation scope"
```

Expected final line:

```text
PASS: exact STUDIO-004 staged implementation scope
```

Staging is not authorization to commit. Commit, push, PR creation, and merge remain subject to `AGENTS.md`, explicit Studio Owner instruction, and the review gates below.

## 23. Review Requirements

STUDIO-004 requires independent review before merge.

Preferred path: review the complete staged diff or exported patch before commit.

Fallback path: when an independent reviewer cannot access the local diff, the Studio Owner may explicitly authorize a feature-branch commit, push, and PR solely to create a stable review artifact after deterministic and scope validation pass. This fallback does not authorize merge and does not weaken any acceptance criterion.

In every path:

- the authoring agent instance must not serve as the independent reviewer;
- the reviewer must identify the exact diff, patch, commit, or PR reviewed;
- `APPROVE` must be recorded before merge;
- `REQUEST CHANGES` or `BLOCK` returns the task to authoring without allowing acceptance;
- Studio Owner/workflow approval remains required for merge;
- Git operations still require the explicit authorization required by `AGENTS.md`.

The reviewer must review from the accepted task contract, repository baseline, complete diff, and deterministic evidence rather than relying on the authoring session’s hidden context.

Review should attempt to falsify the implementation by asking:

1. Can a new suitable runtime resume safely without private chat history?
2. Do `TASK`, `STATE`, `WORKLOG`, and `RESUME` each have one distinct job?
3. Can a stale `RESUME.md` override current Git or accepted decisions?
4. Can `TASK.md` silently broaden the canonical task contract?
5. Are attempted work and completed work distinguishable?
6. Are failed checks and blockers preserved honestly?
7. Does `RESUME.md` replace or weaken the Handoff Protocol?
8. Could parallel agents race on the same `STATE.md` or `RESUME.md`?
9. Can an ambiguous writer claim be overwritten rather than reconciled?
10. Can `WORKTREE_ONLY` evidence be mistaken for shared or durable evidence?
11. Can an unexpected interruption be recovered without inventing completion?
12. Are pre-existing or unrelated changes distinguished and protected?
13. Can a missing or unsupported schema version be silently accepted?
14. Can project-specific state leak across Project Studios?
15. Are secrets, transcripts, private chain-of-thought, environment dumps, or personal machine paths invited by any template field?
16. Does the protocol create unnecessary record-keeping for micro-tasks?
17. Did Producer or a new memory role become a universal gate or executive authority?
18. Was any runtime, provider, model, database, tool, engine, language, framework, game, or canon selected?
19. Did implementation modify files outside scope?
20. Are important rules duplicated instead of linked to their canonical homes?

Review outcome:

- `APPROVE`
- `REQUEST CHANGES`
- `BLOCK`

## 24. Definition of Done

STUDIO-004 is complete when:

- the Studio Owner-approved task contract exists at `tasks/STUDIO-004.md`;
- the canonical Persistent Memory Protocol exists;
- all four reusable templates exist, declare `memory_schema_version: 1`, and have distinct responsibilities;
- a future task can declare one isolated memory package;
- a suitable replacement runtime can identify the authorized task, current state, material history, and safe next action from repository-visible evidence;
- memory must be reconciled with Git, tests, accepted decisions, and the task contract before writes resume;
- stale, conflicting, unsupported-version, or unexpectedly interrupted memory has an explicit recovery path;
- durability state distinguishes local worktree evidence from committed, remote, reviewed, or merged evidence;
- writer claims and unrelated-change protection prevent silent overwrite or false attribution;
- the initial `RESUME.md` is actionable from package creation;
- handoff levels and role independence remain intact;
- Project Studio isolation remains intact;
- the protocol remains lightweight and does not burden trivial completed work;
- no secret, private transcript, or private chain-of-thought is required;
- no memory record gains binding authority;
- Studio Owner remains final binding/non-reversible authority;
- no runtime/model/provider/tool/database/engine/language/framework/game/canon decision is introduced;
- deterministic content and scope checks pass;
- independent review returns `APPROVE`;
- no merge occurs before independent `APPROVE` and Studio Owner/workflow approval;
- any pre-review feature-branch commit or PR was explicitly authorized and used only as a stable review artifact;
- the contract itself was not treated as standing authorization for Git publication.
