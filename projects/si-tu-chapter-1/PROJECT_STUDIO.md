# Project Studio — SITU-CH1

## 1. Identity

- `project_studio_id`: `SITU-CH1`
- `project_name`: `Sĩ Tử — Hành Trình Thi Cử — Chương 1`
- `status`: `HANDOFF`
- `repository_or_namespace`: `projects/si-tu-chapter-1/`
- `created_from_task`: `STUDIO-005`
- `binding_authority_reference`: `studio/STUDIO_CONSTITUTION.md`
- `project_memory_root`: `projects/si-tu-chapter-1/memory/tasks`
- `memory_task_package`: `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/`
- `memory_schema_requirement`: `memory_schema_version: 1`
- `official_integrated_gdd`: `NOT_YET_DESIGNATED`

This is one organizational container for one historical game project. It creates no additional owner-level or executive role. Final binding and non-reversible authority remains with the Studio Owner.

## 2. Intended outcome and boundary

The Project Studio provides an isolated, repository-visible home for project governance, source authority, decisions, artifact discovery, bounded Cells, task memory, and handoff evidence.

### In scope at bootstrap

- instantiate the `SITU-CH1` Project Studio;
- preserve and map the two Owner-created GDD working drafts;
- establish operational source-authority and content-promotion rules;
- index existing project artifacts without moving them;
- activate Cell `SITU-BASELINE-001` for the bounded STUDIO-005 baseline;
- create one schema-1 persistent-memory package;
- register external capabilities as unassessed candidates only;
- provide deterministic validation and tests.

### Out of scope

- selecting, combining, or rewriting game content from V22 or V23;
- designating an integrated official GDD or project-wide canon;
- changing quests, dialogue, gameplay, balance, historical claims, or source artifacts;
- finalizing `DOC01` beyond its greybox boundary;
- choosing an engine, language, framework, model, provider, runtime, router, database, dependency, or production pipeline;
- installing or adopting an external capability;
- creating another Project Studio.

### Completion boundary

The bootstrap outcome is complete only after all STUDIO-005 deliverables and deterministic checks exist, independent QA and Review & Integration record `APPROVE`, and the Studio Owner decides the merge disposition. Project development may continue under later accepted tasks without keeping the bootstrap Cell active.

## 3. Source relationship and authority state

| Source | Path | Git blob SHA | Design status | Project authority |
| --- | --- | --- | --- | --- |
| `GDD-V22` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v22_Ban_Chi_Tiet_Day_Du.docx` | `a6d6d5519f5fe7b201207a4bfa2cffc1be8ecd3c` | `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` | Not an integrated official GDD |
| `GDD-V23` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v23_Hieu_Chinh_MQ01.docx` | `e73d3b03a78160f761320184ddbe48f5339d752a` | `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` | Not an integrated official GDD |

V22 and V23 are co-equal inputs. Neither receives automatic global or scoped precedence from version number, filename, date, length, completeness, apparent polish, or MQ01 support artifacts. Relevant content is compared per bounded content unit under `SOURCE_AUTHORITY.md`.

The Project Studio keeps three authority layers separate:

1. design provenance;
2. historical evidence;
3. official project authority.

Copying, preserving, adapting, or combining draft text does not by itself make that text official. Promotion requires the full gate in `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md`, including Studio Owner approval and durable canonical materialization.

## 4. Canonical project references

| Reference type | Canonical repository path or identifier | Status |
| --- | --- | --- |
| Task contracts | `tasks/STUDIO-005.md`, `tasks/STUDIO-005-AMENDMENT-001.md`, and later accepted `tasks/` contracts | `STUDIO-005 AND AMENDMENT 001 OWNER_APPROVED` |
| Game/project vision | `docs/GAME_VISION.md` | `TEMPLATE / UNRESOLVED` |
| Studio-wide decisions | `docs/DECISIONS.md` | `CANONICAL STUDIO-WIDE LOCATION` |
| Project decisions | `projects/si-tu-chapter-1/DECISIONS.md` | `ACTIVE REGISTER` |
| Source and content authority | `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md` | `CANONICAL PROJECT RULE` |
| Artifact discovery | `projects/si-tu-chapter-1/ARTIFACT_MAP.md` | `CENTRAL INDEX` |
| Design architecture | `docs/design/00_DESIGN_ARCHITECTURE.md` | `EXISTING DERIVED DESIGN ARTIFACT` |
| Assumptions and unresolved items | `reports/ASSUMPTION_REGISTER.md`, project decisions, and task memory | `SCOPED; SEE ARTIFACT MAP` |
| Historical evidence system | `docs/HISTORICAL_CONTENT_SYSTEM.md` | `CANONICAL STUDIO RULE` |
| MQ01 evidence and QA | Four mapped artifacts under `source/` | `BOUNDED SUPPORT` |
| Tests and validators | `scripts/`, `tests/`, and `reports/` | `SEE ARTIFACT MAP` |
| Handoff | STUDIO-005 memory package and Pull Request | `LEVEL 2 REQUIRED` |

Repository-visible evidence is the continuity source. Private chat history and private chain-of-thought are not required inputs.

## 5. Project-specific state and isolation

| State category | Canonical location | Isolation rule |
| --- | --- | --- |
| Official content authority | `SOURCE_AUTHORITY.md` plus a future explicitly designated canonical artifact | No integrated official GDD at bootstrap |
| Accepted project decisions | `DECISIONS.md` | Applies only within recorded scope |
| Architecture and derived design | `docs/design/` as indexed | Reuse requires explicit provenance and scope |
| Tasks and milestones | `tasks/` plus project memory packages | Project work is attributed to `SITU-CH1` |
| Assumptions and unresolved items | Mapped reports, decisions, and task memory | Unknowns remain explicit |
| Constraints | `SOURCE_AUTHORITY.md`, `DECISIONS.md`, accepted task contracts | Not inherited by another project implicitly |
| Code and content ownership | Existing repository paths mapped in `ARTIFACT_MAP.md` | No artifact moves at bootstrap |
| Current operational state | `projects/si-tu-chapter-1/memory/tasks/<TASK-ID>/` | Verified before every write |

Shared infrastructure or evidence does not transfer canon, decisions, scope, acceptance, or active-writer ownership across Project Studios.

## 6. Active Cell

| Cell ID | Bounded outcome | Required execution capabilities | State | Independent handoff targets | Completion condition |
| --- | --- | --- | --- | --- | --- |
| `SITU-BASELINE-001` | Establish and validate the Project Studio baseline | Producer / Coordination; Narrative / Research; Engineering | `HANDOFF` | QA, then Review & Integration | Contract scope, checks, verdicts, and handoff evidence complete |

The Cell record is `projects/si-tu-chapter-1/cells/SITU-BASELINE-001.md`. It is temporary and may not continue into content selection, gameplay implementation, or permanent staffing.

## 7. Borrowed Guild capabilities

| Guild or capability | Need | Status | Return condition |
| --- | --- | --- | --- |
| `NONE` | No Guild capability is required to instantiate the baseline | `NOT YET SELECTED` | Reassess only under a later accepted task |

No external repository registered by STUDIO-005 is adopted, installed, trusted, or granted authority.

## 8. Platform capabilities used

| Capability category | Bounded use | Status | Data boundary |
| --- | --- | --- | --- |
| Repository-visible governance and Git evidence | Store task, decisions, memory, diffs, tests, and review evidence | Existing repository capability only; implementation `NOT YET SELECTED` | `SITU-CH1` state remains in its namespace |

This record does not select a platform implementation, runtime, model, provider, or router.

## 9. Project constraints

### LOCKED

- V22 and V23 are Owner-created `AUTHOR_CREATED_WORKING_DRAFT` and `CO_EQUAL_INPUT` artifacts.
- Neither draft has automatic global or scoped precedence, including for MQ01 and `DOC01`.
- `official_integrated_gdd: NOT_YET_DESIGNATED`.
- The two GDD DOCX files are immutable at their recorded Git blob SHAs.
- Design provenance, historical evidence, and official project authority remain separate.
- Historical claims use `DIRECT`, `RECONSTRUCTION`, `INFERENCE`, `FICTION`, or `UNRESOLVED` honestly.
- Final `DOC01` material form remains blocked pending appropriate contemporaneous evidence.
- Binding and non-reversible authority remains with the Studio Owner.

### GUIDED

- Specialists may compare, preserve, copy, adapt, combine, reject, or hold bounded content units when they follow the promotion gate.
- Reversible local organization and validation choices may be made within accepted task scope.

### OPEN

- Future integrated GDD structure and title;
- future content recommendations after bounded comparison;
- engine, language, framework, model, provider, runtime, router, database, dependency, and production pipeline;
- external capability evaluation under a later accepted task.

### Explicit exclusions

- no self-approved canon;
- no invented historical citation, quote, locator, form, title, or URL;
- no silent source precedence;
- no source-file edit or artifact relocation;
- no external-capability installation or adoption.

## 10. Interaction, review, and authority

- The six STUDIO-002 logical profiles retain their existing boundaries.
- Producer / Coordination supports dependencies and visibility but is not a universal approval gate.
- QA and Review & Integration remain independent from the implementation writer.
- A specialist or Cell may recommend a bounded choice but may not self-approve official project content.
- A chat recommendation, memory record, filename, QA report, or model output cannot create official canon.
- `AGENT ROLE != RUNTIME != MODEL != PROVIDER` remains binding.

## 11. Isolation and reuse checklist

- [x] Project-specific state has declared canonical locations.
- [x] V22 and V23 are mapped as co-equal working inputs.
- [x] No state from another project is silently binding here.
- [x] Shared evidence must retain provenance, scope, and acceptance status.
- [x] The repository-relative memory root is declared.
- [x] The STUDIO-005 package contains exactly four schema-1 records.
- [x] Runtime replacement can resume from repository-visible evidence.
- [x] Shared memory infrastructure is not treated as a transfer of project authority.
- [ ] Independent QA verdict recorded.
- [ ] Independent Review & Integration verdict recorded.
- [ ] Studio Owner merge disposition recorded.
