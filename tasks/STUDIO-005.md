# STUDIO-005 — Bootstrap the Historical Game Project Studio from Co-Equal Working Drafts

## 1. Goal

Create the first real Project Studio in GAME AI Studio for the historical game project developed by the Studio Owner in GDD V22, GDD V23, and the existing MQ01 support artifacts.

The Project Studio identity is:

- `project_studio_id`: `SITU-CH1`
- `project_name`: `Sĩ Tử — Hành Trình Thi Cử — Chương 1`
- `project_namespace`: `projects/si-tu-chapter-1/`
- `project_memory_root`: `projects/si-tu-chapter-1/memory/tasks`

The display name is a repository-management label derived from the source filenames. It is not an accepted final commercial title.

STUDIO-005 creates organizational structure, source-authority rules, a content-promotion gate, an artifact index, one bounded bootstrap Cell, one live persistent-memory package, an external-capability candidate register, and deterministic validation.

STUDIO-005 does not designate an integrated official GDD, rewrite game content, choose technology, install external capabilities, or create gameplay.

## 2. Contract Status

- Status: `APPROVED`
- Approved by: Studio Owner
- Approval date: `2026-08-12`
- Contract revision: `0.2`
- Repository baseline: `main` at `4e5f3ae84724271363b8f098cfeeceda8ffe9b98`
- Implementation branch: `studio-v0.5`
- Target memory schema: `1`
- Source relationship decision: `OWNER_DECISION-SOURCE-001`
- `source_relationship`: `CO-EQUAL`
- `official_integrated_gdd`: `NOT_YET_DESIGNATED`

The Studio Owner has decided that V22 and V23 are co-equal, author-created working design drafts. Neither draft automatically supersedes, overrides, corrects, or takes precedence over the other, including for `MQ01A–MQ01D` and `DOC01`.

The Studio Owner creates and approves this contract. After it is committed as the only change in the first STUDIO-005 commit, implementation agents may read, cite, and validate against it but must not modify it, weaken it, or expand their own scope.

If implementation reveals a genuine contract defect, record `UNRESOLVED` and request an authorized amendment. Do not silently rewrite this file.

## 3. Context and Canonical References

STUDIO-005 operates under:

- `AGENTS.md`
- `docs/GAME_VISION.md`
- `docs/DECISIONS.md`
- `docs/HISTORICAL_CONTENT_SYSTEM.md`
- `studio/STUDIO_CONSTITUTION.md`
- `studio/STUDIO_TOPOLOGY.md`
- `studio/PROJECT_STUDIO_TEMPLATE.md`
- `studio/CELL_MODEL.md`
- `studio/ACTIVATION_POLICY.md`
- `studio/MEMORY_PROTOCOL.md`
- `studio/HANDOFF_PROTOCOL.md`
- the six logical role profiles under `studio/agents/`

STUDIO-003 defined Project Studios as isolated organizational containers and did not create a real project. STUDIO-004 defined repository-visible persistent memory and did not create a live package. STUDIO-005 instantiates both for one existing game project.

## 4. Project and Draft Boundary

GDD V22 and GDD V23 describe one game project, not two Project Studios.

Both files are:

- created by the Studio Owner through prior research, reading, reasoning, and design work;
- valuable working foundations for structure, story, systems, quests, and future development;
- eligible to be preserved, copied, combined, revised, or promoted into later official project artifacts after the gate in Section 7;
- co-equal inputs at the artifact-authority level.

`WORKING_DRAFT` describes their current project-authority status only. It does not imply that the drafts are externally copied, casually invented, low-quality, or unsupported by prior effort.

The version labels `V22` and `V23`, their filenames, their length, their apparent completeness, and their modification dates identify distinct artifacts. None of those facts creates automatic authority or precedence.

A later V24 or another revision of the same game remains inside `SITU-CH1` unless the Studio Owner explicitly creates a different Project Studio. A higher version number alone must never make that later artifact official or authoritative.

At bootstrap:

- no single integrated official GDD baseline is designated;
- no blanket project-wide canon may be inferred from either draft;
- any previously accepted, content-specific Owner decision remains effective only within its recorded scope and status;
- STUDIO-005 itself promotes no game content into official canon.

## 5. Immutable Source Baseline

The following DOCX files are read-only source artifacts for STUDIO-005:

| Source ID | Repository path | Baseline Git blob SHA | Project-authority status |
| --- | --- | --- | --- |
| `GDD-V22` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v22_Ban_Chi_Tiet_Day_Du.docx` | `a6d6d5519f5fe7b201207a4bfa2cffc1be8ecd3c` | `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` |
| `GDD-V23` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v23_Hieu_Chinh_MQ01.docx` | `e73d3b03a78160f761320184ddbe48f5339d752a` | `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` |

STUDIO-005 must not edit, replace, rename, move, regenerate, normalize, or resave either DOCX file. Their Git blob SHAs must remain unchanged at final validation.

Source immutability protects provenance and reproducibility. It does not designate either file as the official GDD, establish historical truth, or grant content precedence.

The following existing MQ01 support artifacts must be mapped and preserved:

- `source/MQ01_evidence_register.csv`
- `source/MQ01_decision_log.md`
- `source/MQ01_scene_brief.md`
- `source/Bao_cao_QA_MQ01.md`

## 6. Three Separate Authority Layers

`projects/si-tu-chapter-1/SOURCE_AUTHORITY.md` is the canonical operational home for the rules in Sections 4 through 8.

The Project Studio must keep these three layers separate:

| Layer | Question answered | Initial authority |
| --- | --- | --- |
| Design provenance | Where did this idea, structure, wording, mechanic, or alternative come from? | V22, V23, and later owner-created design artifacts, cited at bounded section or content-unit level |
| Historical evidence | How strongly is a checkable historical claim supported? | Evidence register, real sources, exact locators, and the classifications `DIRECT`, `RECONSTRUCTION`, `INFERENCE`, `FICTION`, or `UNRESOLVED` |
| Official project authority | What is currently accepted for production and project continuity? | Explicitly accepted Owner decisions plus the canonical artifact designated by those decisions |

Evidence can support or weaken a historical claim without selecting an entire GDD. Design provenance can establish authorship without proving historical truth. A well-supported claim can still require design integration. Text can be copied verbatim from either draft into a later official artifact, but copying alone does not make it official.

Memory records, artifact indexes, filenames, later document versions, recent chat messages, model recommendations, or QA reports do not independently create official canon.

## 7. Content Comparison and Promotion Gate

Content from either draft may be retained unchanged, adapted, combined, rejected, or held. The choice must be made per bounded content unit, not per whole-document preference.

A bounded content unit may be one quest, scene, mechanic, character role, chronology rule, state variable, dialogue passage, UI term, prop, document, or other reviewable design element.

Before a bounded content unit is promoted into an official project artifact, the responsible task must complete all applicable steps below:

1. **Define the unit and its purpose.** Record its ID, scope, player goal, gameplay function, dependencies, and any non-negotiable Owner intent.
2. **Trace provenance.** Identify the relevant V22 and V23 sections, plus any later design or support artifacts. Do not claim that silence in one draft is rejection by that draft.
3. **Compare alternatives fairly.** List material similarities, differences, omissions, and incompatibilities. Do not choose by version number, recency, document length, polish, convenience, or model preference.
4. **Test internal logic.** Check causal coherence, chronology, character motivation and authority, quest dependencies, state variables, terminology, player actions, feedback, consequences, failure paths, and consistency with accepted project decisions.
5. **Apply the historical evidence gate.** Extract checkable claims and classify them under `docs/HISTORICAL_CONTENT_SYSTEM.md`. Factual claims need evidence matching period, polity, institution, object, and specificity. Reconstruction, inference, and fiction remain permitted when honestly classified and constrained.
6. **Preserve playability.** Historical verification must not replace player action. If specificity is unsupported, generalize, label, redesign, or use controlled fiction while preserving the intended gameplay function.
7. **Record the recommendation and rationale.** State what is kept, changed, combined, removed, or held; why it is more coherent; which evidence claims and accepted decisions support it; what artifacts and systems are affected; and what uncertainty remains. Evidence-register decisions must continue to use their approved schema values.
8. **Review independently.** Historical, narrative, gameplay, cross-document, and delivery checks must be performed at the level required by the content task.
9. **Obtain Studio Owner approval.** A recommendation does not become binding or irreversible project canon until the Studio Owner approves its defined scope.
10. **Materialize the decision durably.** Update the designated canonical artifact and project decision register through an authorized branch and review artifact. Chat text alone is not accepted project state.

Passing one criterion cannot compensate for failing another. For example, a historically plausible idea may still fail gameplay or narrative logic; an enjoyable mechanic may still require a clearer fiction label; an Owner-authored passage may still contain an unresolved claim.

When evidence and logic do not support a safe choice, preserve the alternatives and record `HOLD` or `UNRESOLVED`. Do not fill the gap with an invented fact or silently declare one draft the winner.

## 8. MQ01 and `DOC01` Rules

### 8.1 No draft-level precedence

V22 and V23 remain co-equal for `MQ01A–MQ01D` and `DOC01`. V23's title as an MQ01 adjustment and its higher version number do not grant it automatic priority. V22's broader scope or greater continuity does not grant it automatic priority either.

### 8.2 Support-artifact functions

The four existing MQ01 support artifacts have bounded, distinct functions:

| Artifact | Function | Authority limit |
| --- | --- | --- |
| `source/MQ01_evidence_register.csv` | Records individual claims, evidence levels, citations, allowed uses, and decisions | Supports or restricts individual claims; does not elevate an entire GDD |
| `source/MQ01_decision_log.md` | Records prior keep/change/remove/hold reasoning and affected content where present | Binding only for a decision explicitly accepted by the Studio Owner and only within its recorded scope |
| `source/MQ01_scene_brief.md` | Defines the bounded MQ01 scene or quest design unit and its intended function | A design brief, not blanket historical proof or GDD precedence |
| `source/Bao_cao_QA_MQ01.md` | Reports QA findings, conditions, residual uncertainty, and production restrictions | Review evidence; does not independently create canon or Owner approval |

The Project Studio must inspect the actual status and scope of each record. It must not infer acceptance merely because a record exists or a QA result is positive or conditional.

### 8.3 `DOC01` visual and material boundary

`DOC01` may remain a greybox gameplay object and its gameplay function may be evaluated. Its final layout, wording, seals, signatures, paper, ink, dimensions, fingerprints, or other period-specific material form must not be locked without separate contemporaneous documentary or material evidence appropriate to the time and place.

A legal or administrative rule may support that a document existed or mattered. It does not by itself prove the document's visual form.

## 9. Historical Evidence and Controlled Fiction

Historical claims must remain distinguishable as:

- `DIRECT`
- `RECONSTRUCTION`
- `INFERENCE`
- `FICTION`
- `UNRESOLVED`

No Project Studio record, memory record, artifact map, design note, GDD draft, or model output may upgrade `INFERENCE`, `FICTION`, or `UNRESOLVED` into established history.

The absence of direct historical evidence does not automatically prohibit useful game content. It requires an honest classification and a bounded constraint:

- `INFERENCE` identifies the cited premises and inferential step;
- `FICTION` names the historical constraints it must not violate;
- `UNRESOLVED` is removed, generalized, relocated, held, or explicitly blocked from factual player-facing use.

No citation, quotation, archival locator, period form, title, date, material detail, or source URL may be invented.

## 10. Authority and Governance

- Final binding and non-reversible authority remains with the Studio Owner.
- `SITU-CH1` is an organizational container and creates no new owner-level or executive role.
- The six STUDIO-002 logical profiles remain valid.
- A Cell may make reversible, local, in-scope choices only.
- An agent may compare alternatives and recommend a bounded choice; it may not self-approve official canon.
- Accepted content-specific decisions remain scoped; they do not grant whole-document authority.
- Memory records, artifact indexes, later document versions, and recent chat messages do not override accepted decisions or source-authority rules.
- `AGENT ROLE != RUNTIME != MODEL != PROVIDER` remains binding.

The terms `Project Owner`, `Project Studio Owner`, and `Platform Studio Owner` must not be introduced as roles.

## 11. Required Files and Exact Scope

This milestone has exactly 15 authorized new or modified files.

### 11.1 Contract created by the Studio Owner

- `tasks/STUDIO-005.md`

### 11.2 Implementation files to create

- `projects/si-tu-chapter-1/PROJECT_STUDIO.md`
- `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md`
- `projects/si-tu-chapter-1/ARTIFACT_MAP.md`
- `projects/si-tu-chapter-1/DECISIONS.md`
- `projects/si-tu-chapter-1/cells/SITU-BASELINE-001.md`
- `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/TASK.md`
- `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/STATE.md`
- `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/WORKLOG.md`
- `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/RESUME.md`
- `studio/EXTERNAL_CAPABILITY_CANDIDATES.md`
- `scripts/validate_project_studio.py`
- `tests/test_validate_project_studio.py`

### 11.3 Existing files to modify

- `AGENTS.md`
- `README.md`

No other file may be created, modified, deleted, renamed, or moved.

After the contract-only commit, implementation agents have a 14-file change scope and must leave `tasks/STUDIO-005.md` unchanged.

## 12. Required Content by File

### 12.1 `PROJECT_STUDIO.md`

Instantiate `studio/PROJECT_STUDIO_TEMPLATE.md` for `SITU-CH1` and declare:

- the identity and namespace in Section 1;
- the project memory root and package path;
- project scope and explicit exclusions;
- canonical source, decision, artifact, assumptions, architecture, evidence, test, and handoff locations;
- project-specific state isolation;
- Cell `SITU-BASELINE-001`;
- both GDDs as `AUTHOR_CREATED_WORKING_DRAFT` and `CO_EQUAL_INPUT`;
- `official_integrated_gdd: NOT_YET_DESIGNATED`;
- the three authority layers and the content-promotion gate by reference to `SOURCE_AUTHORITY.md`;
- no borrowed Guild or Platform capability as adopted unless explicitly recorded as `NONE` or `NOT YET SELECTED`;
- `LOCKED`, `GUIDED`, and `OPEN` constraints without inventing canon;
- the Studio Owner authority boundary.

Initial status may progress from `READY` to `HANDOFF` or `COMPLETE` only when current repository evidence supports it.

### 12.2 `SOURCE_AUTHORITY.md`

Record Sections 4 through 9 as the canonical operational rules. It must include:

- the two immutable source paths and Git blob SHAs;
- their co-equal, author-created working-draft status;
- an explicit rule that neither draft has automatic global or scoped precedence, including for MQ01 and `DOC01`;
- the separation of design provenance, historical evidence, and official project authority;
- the bounded content-unit comparison and promotion gate;
- the role and authority limit of all four MQ01 support artifacts;
- the initial `NOT_YET_DESIGNATED` integrated official GDD state;
- historical evidence classifications and controlled-fiction rules;
- the `DOC01` greybox and material-evidence boundary.

It must not reduce the drafts to casual reference material, deny their Owner-created provenance, or grant either draft official or historical authority merely from its filename or contents.

### 12.3 `ARTIFACT_MAP.md`

Create a central repository index, not a copy of the artifacts. At minimum map:

- source GDD and MQ01 support artifacts under `source/`;
- derived design documents under `docs/design/`;
- historical-content rules under `docs/` and `.agents/skills/historical-game-builder/`;
- prototype data under `data/vertical_slice/`;
- prototype code under `prototype/rules/`;
- reports and registers under `reports/`;
- tests under `tests/`;
- Project Studio governance, decisions, Cells, memory, and task contracts.

Each entry or grouped entry must expose enough fields to locate the path, identify artifact type, current status and authority, provenance or producing task where known, and review, commit, or PR reference where known. Unknown values must be explicit (`UNKNOWN`, `UNRESOLVED`, or `NONE`), not invented.

The map must distinguish source preservation from content authority and must show both GDDs as co-equal working inputs. No mapped artifact may be moved merely to make the index look cleaner.

### 12.4 `DECISIONS.md`

Create the project-specific decision register for `SITU-CH1`.

Initial accepted decisions may register:

- project identity and one-project treatment of V22 and V23;
- `OWNER_DECISION-SOURCE-001`: both drafts are co-equal, Owner-created working inputs;
- no automatic precedence by version number or scope;
- the separation of provenance, evidence, and official authority;
- `official_integrated_gdd: NOT_YET_DESIGNATED`;
- the bounded promotion gate;
- the `DOC01` greybox and material-evidence boundary.

Each decision entry must state scope, status, authority, rationale, provenance, affected artifacts, approval evidence, and supersession relationship. It must point to `SOURCE_AUTHORITY.md` as the canonical rule rather than duplicate it in full.

Studio-wide decisions remain in their existing canonical homes and must not be copied here as if they were project-specific.

### 12.5 `cells/SITU-BASELINE-001.md`

Define one bounded bootstrap Cell whose outcome is to establish and validate the Project Studio baseline.

Minimum active execution capabilities:

- Producer / Coordination for scope and dependency visibility;
- Narrative / Research for co-equal source treatment, evidence-class integrity, and promotion-gate clarity;
- Engineering for validator and tests.

QA and Review & Integration remain independent handoff and review targets. The Cell does not create permanent staffing, select runtimes, choose between draft content, or continue into gameplay or content revision after the bootstrap outcome.

### 12.6 Persistent-memory package

Create exactly four files at `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/` from the schema-1 templates:

- `TASK.md`
- `STATE.md`
- `WORKLOG.md`
- `RESUME.md`

Requirements:

- every file declares `memory_schema_version: 1`;
- `task_id` is `STUDIO-005`;
- `project_studio` is `SITU-CH1` where that field applies;
- the canonical task contract is `tasks/STUDIO-005.md`;
- the package path and memory root are repository-relative;
- branch, HEAD, durability, persisted reference, writer claim, worktree status, checkpoints, checks, and next actions reflect verified evidence rather than predicted final state;
- initialization starts at `STUDIO-005-CP-0001`;
- `WORKLOG.md` remains append-only;
- `RESUME.md` is actionable from creation and is not an empty placeholder;
- source-authority state records co-equal inputs and no designated integrated official GDD;
- no private transcript, private chain-of-thought, credential, or machine-specific absolute path is stored.

### 12.7 `EXTERNAL_CAPABILITY_CANDIDATES.md`

Register exactly these ten candidate repositories:

1. `https://github.com/obra/superpowers`
2. `https://github.com/anthropics/skills`
3. `https://github.com/mattpocock/skills`
4. `https://github.com/garrytan/gstack`
5. `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
6. `https://github.com/Egonex-AI/Understand-Anything`
7. `https://github.com/addyosmani/agent-skills`
8. `https://github.com/bojieli/ai-agent-book`
9. `https://github.com/msitarzewski/agency-agents`
10. `https://github.com/santifer/career-ops`

For every candidate, record the exact URL, a bounded evaluation purpose, and these safe initial states:

- assessment: `UNASSESSED`;
- license: `NOT REVIEWED` or `UNRESOLVED`;
- security: `NOT REVIEWED`;
- pinned commit or tag: `NONE`;
- compatibility: `UNRESOLVED`;
- installation: `NOT INSTALLED`;
- adoption decision: `NO DECISION`.

Star counts, popularity, marketing claims, or a repository's own safety claims are not acceptance evidence. STUDIO-006 owns evaluation and may later recommend `ADOPT`, `ADAPT`, `REFERENCE`, `DEFER`, or `REJECT`.

### 12.8 Validator and tests

`scripts/validate_project_studio.py` must use only the Python standard library and return a nonzero exit code on failure. It must deterministically check at least:

- required Project Studio files and exact four-file memory package;
- `SITU-CH1` identity, namespace, and schema-1 anchors;
- both immutable GDD Git blob SHAs;
- both GDDs are recorded as `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT`, and free of automatic precedence;
- `official_integrated_gdd: NOT_YET_DESIGNATED`;
- separation of design provenance, historical evidence, and official project authority;
- bounded content-unit promotion requires logic checks, evidence classification, recorded rationale, independent review, Studio Owner approval, and durable canonical update;
- MQ01 support-artifact references and their bounded authority;
- exact ten external candidate URLs and safe initial statuses;
- absence of forbidden owner-level roles in instantiated Project Studio files;
- required artifact-map coverage;
- no positive claim that V22 or V23 automatically supersedes, overrides, corrects, or has priority over the other;
- no claim that draft text becomes official merely by copying, filename, version number, recency, completeness, QA existence, or model judgment;
- no claim that an engine, provider, model, external repository, skill, or dependency has been selected or installed.

The validator should rely on required structured anchors and narrowly defined forbidden positive assertions. It must not mistake an explicit prohibition or a negative test fixture for an authority violation.

`tests/test_validate_project_studio.py` must cover a valid structure and representative failures, including:

- a missing required file;
- an altered source hash;
- inconsistent memory schema;
- unsafe external-candidate status;
- forbidden authority wording;
- one draft asserted as automatically higher authority;
- official status asserted without the promotion and Owner-approval gate.

The validator and tests must not access the network, modify source artifacts, or require a game engine or third-party package.

### 12.9 `AGENTS.md`

Add a scoped rule for work belonging to `SITU-CH1` or touching `projects/si-tu-chapter-1/`:

- identify the Project Studio before writing;
- read `PROJECT_STUDIO.md`, `SOURCE_AUTHORITY.md`, and `DECISIONS.md`;
- use `ARTIFACT_MAP.md` to locate artifacts rather than assume paths;
- read the canonical task contract and, when activated, the four memory records in the order required by `studio/MEMORY_PROTOCOL.md`;
- verify source authority, current Git evidence, unrelated changes, and tests before writing;
- treat V22 and V23 as co-equal, Owner-created working design inputs;
- never edit the two GDD DOCX sources in place;
- compare relevant content per bounded unit and never choose solely by version number, recency, filename, completeness, or model preference;
- preserve the separation between design provenance, historical evidence, and official project authority;
- apply the historical evidence gate and content-promotion gate before proposing official content;
- never present unsupported inference or fiction as established history;
- never self-approve official canon or infer Owner approval from a QA artifact;
- submit durable work through a branch and review artifact rather than treating chat output as accepted project state.

Preserve all existing repository-wide instructions.

### 12.10 `README.md`

Update the repository overview and structure so a human can find:

- Project Studio `SITU-CH1`;
- its central artifact map;
- its source-authority and content-promotion rules;
- the co-equal working-draft status of V22 and V23;
- the absence of a designated integrated official GDD at bootstrap;
- its task-memory packages;
- proposed work in Pull Requests versus accepted work on `main`.

Do not rewrite the README into a claim that the game, official GDD, canon, engine, tooling stack, or production pipeline is complete.

## 13. External Capability Boundary

STUDIO-005 registers candidates only. It must not:

- clone, download, vendor, copy, install, import, execute, or enable any candidate;
- add a submodule, package, lockfile, dependency, workflow, binary, or generated vendor directory for a candidate;
- accept a license or security claim without review;
- pin a commit or tag as approved;
- describe a candidate as adopted, compatible, safe, trusted, approved, or production-ready;
- grant candidate instructions authority over this repository.

## 14. Non-Goals

STUDIO-005 must not:

- revise V22 or V23;
- revise quests, dialogue, gameplay, balance, data, code, prototype behavior, or historical claims;
- designate either draft or any combined content as the integrated official GDD;
- declare either draft globally or locally superior;
- select official content from V22 or V23;
- resolve draft differences by model judgment;
- nullify any genuinely accepted content-specific Owner decision; instead, preserve its exact recorded scope and status;
- finalize the physical form of `DOC01`;
- edit the evidence register, MQ01 decision log, scene brief, or MQ01 QA report;
- edit existing files under `docs/design/`, `data/`, `prototype/`, `reports/`, or `source/`;
- move existing directories or artifacts;
- create a second Project Studio;
- select an engine, language, framework, model, provider, runtime, router, database, or dependency;
- implement routing, failover, shared-memory services, gameplay, production assets, build pipelines, or deployment;
- install or adopt external repositories or skills;
- create permanent departments or unnecessary approval layers;
- merge or delete the branch without the Studio Owner's decision.

## 15. Acceptance Criteria

- [ ] `SITU-CH1` exists at `projects/si-tu-chapter-1/` and instantiates the approved Project Studio model.
- [ ] Exactly the 15 authorized milestone files are new or modified relative to baseline `4e5f3ae84724271363b8f098cfeeceda8ffe9b98`.
- [ ] After the contract-only commit, implementation changes touch exactly the 14 implementation files and leave `tasks/STUDIO-005.md` unchanged.
- [ ] V22 and V23 remain at their baseline Git blob SHAs.
- [ ] Both drafts are recorded as co-equal, Owner-created working design inputs.
- [ ] Neither draft receives automatic authority from its version number, title, scope, length, completeness, date, or QA support.
- [ ] No integrated official GDD is designated by STUDIO-005.
- [ ] The project separates design provenance, historical evidence, and official project authority.
- [ ] The content-promotion gate permits reasoned reuse, copying, combination, revision, or rejection without arbitrary invention.
- [ ] Official promotion requires bounded comparison, logic checks, evidence classification, recorded rationale, independent review, Studio Owner approval, and durable canonical update.
- [ ] MQ01 support artifacts influence only the claims and decisions their records actually support.
- [ ] `DOC01` remains greybox pending separate contemporaneous evidence for its final material form.
- [ ] Existing artifacts are indexed without being moved.
- [ ] Project decisions remain isolated from studio-wide governance.
- [ ] Cell `SITU-BASELINE-001` is bounded, minimally staffed, and hands off to independent QA and Review & Integration.
- [ ] The live memory package contains exactly four files with `memory_schema_version: 1` and evidence-backed current state.
- [ ] The ten external repositories are registered exactly once and all remain unassessed, uninstalled, and undecided.
- [ ] No engine, language, framework, runtime, model, provider, external capability, or dependency is selected or installed.
- [ ] The project validator passes.
- [ ] The existing evidence-register validator passes for `source/MQ01_evidence_register.csv`.
- [ ] The new validator tests pass.
- [ ] The complete existing unit-test suite passes.
- [ ] Scope and whitespace checks pass.
- [ ] Independent QA records `APPROVE` before integration review.
- [ ] Independent Review & Integration records `APPROVE` before merge.
- [ ] The Studio Owner decides whether to merge and whether to delete the branch.

## 16. Deterministic Validation

### 16.1 Contract integrity after the contract-only commit

```powershell
$contractCommit = (git log --diff-filter=A --format=%H -n 1 -- tasks/STUDIO-005.md).Trim()
git diff --exit-code $contractCommit -- tasks/STUDIO-005.md
```

Expected: no output and exit code `0`.

### 16.2 Immutable GDD sources

```powershell
git hash-object source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v22_Ban_Chi_Tiet_Day_Du.docx
git hash-object source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v23_Hieu_Chinh_MQ01.docx
```

Expected:

```text
a6d6d5519f5fe7b201207a4bfa2cffc1be8ecd3c
e73d3b03a78160f761320184ddbe48f5339d752a
```

### 16.3 Validators and tests

```powershell
python scripts/validate_project_studio.py
python scripts/validate_evidence_register.py source/MQ01_evidence_register.csv
python -m unittest tests.test_validate_project_studio -v
python -m unittest discover -s tests -p "test*.py" -v
```

All commands must exit `0`.

### 16.4 Scope and diff

```powershell
git status --short --untracked-files=all
git diff --check
git diff --cached --check
git diff --cached --stat
```

Before implementation files are staged, status must contain only the 14 authorized implementation paths from Section 11.2 and Section 11.3. Final milestone comparison to the baseline must contain only all 15 paths in Section 11.

No implementation commit may be made when scope, source hashes, validator, tests, or whitespace checks fail. The earlier contract-only commit is validated separately under Section 16.1 before implementation begins.

## 17. Review Requirements

QA and Review & Integration must be independent from the implementation writer.

QA attempts to falsify:

1. required-file and exact-scope claims;
2. source immutability and co-equal draft status;
3. absence of hidden V22 or V23 precedence, including within MQ01 and `DOC01`;
4. separation of design provenance, historical evidence, and official project authority;
5. content-promotion logic and Owner-approval boundary;
6. evidence classification and `DOC01` greybox boundary;
7. memory schema, current-state accuracy, and durability claims;
8. external-candidate safety states;
9. validator negative cases and full test results;
10. absence of hidden installation, technology selection, content promotion, or artifact movement.

Review & Integration checks architectural consistency, authority boundaries, source-of-truth placement, duplication, human readability, and whether QA evidence is sufficient.

Allowed verdicts are `APPROVE`, `REQUEST CHANGES`, or `BLOCK`.

Verdicts and evidence must be repository-visible in the STUDIO-005 `WORKLOG.md` and/or the Pull Request. No extra QA report file may be added without an authorized scope amendment.

## 18. Git and Delivery Rules

The delivery sequence is:

1. create and inspect `tasks/STUDIO-005.md`;
2. commit it alone on `studio-v0.5` and verify the remote branch;
3. implement only the 14 authorized implementation files;
4. run deterministic validation;
5. commit and push the validated implementation, then open a draft Pull Request to `main`;
6. obtain independent QA and then Review & Integration verdicts on repository-visible evidence; apply and revalidate any requested changes;
7. the Studio Owner reviews the final `Files changed` and decides whether to merge;
8. only the Studio Owner decides whether the branch is deleted.

Chat output without a repository file and review artifact is a draft, not accepted project state.

## 19. Definition of Done

STUDIO-005 is complete only when the first real Project Studio is repository-visible; V22 and V23 are preserved as co-equal, Owner-created working inputs; source authority and the promotion gate are explicit; no integrated official GDD is falsely designated; all existing project artifacts can be found through the central map; continuity can resume from the four-record package; external capabilities remain safely unassessed; all deterministic checks pass; independent QA and integration review approve; and the Studio Owner accepts the result through the repository workflow.