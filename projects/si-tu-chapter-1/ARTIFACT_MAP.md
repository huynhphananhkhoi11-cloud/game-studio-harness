# SITU-CH1 Artifact Map

## 1. Purpose and status vocabulary

This is the central repository index for `SITU-CH1`. It locates artifacts without copying or moving them. Mapping an artifact preserves discovery and provenance; it does not grant historical truth, official content authority, acceptance, or precedence.

Status values include `IMMUTABLE SOURCE`, `WORKING INPUT`, `EXISTING`, `ACTIVE`, `TEMPLATE`, `UNASSESSED`, `UNKNOWN`, `UNRESOLVED`, and `NONE`.

## 2. Owner-created GDD source baselines

| ID | Path | Type | Status and authority | Provenance / producing task | Review, commit, or PR reference |
| --- | --- | --- | --- | --- | --- |
| `GDD-V22` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v22_Ban_Chi_Tiet_Day_Du.docx` | Owner-created design draft | `IMMUTABLE SOURCE`; `AUTHOR_CREATED_WORKING_DRAFT`; `CO_EQUAL_INPUT`; not integrated official GDD | Studio Owner; prior research and design | Blob `a6d6d5519f5fe7b201207a4bfa2cffc1be8ecd3c`; content review `UNRESOLVED` |
| `GDD-V23` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v23_Hieu_Chinh_MQ01.docx` | Owner-created design draft | `IMMUTABLE SOURCE`; `AUTHOR_CREATED_WORKING_DRAFT`; `CO_EQUAL_INPUT`; not integrated official GDD | Studio Owner; prior research and design | Blob `e73d3b03a78160f761320184ddbe48f5339d752a`; content review `UNRESOLVED` |

Neither row has automatic global or scoped precedence. See `SOURCE_AUTHORITY.md` for bounded comparison and promotion.

## 3. MQ01 research and QA support

| ID | Path | Type | Status and authority | Provenance / producing task | Review, commit, or PR reference |
| --- | --- | --- | --- | --- | --- |
| `MQ01-EVIDENCE` | `source/MQ01_evidence_register.csv` | Evidence register | `EXISTING`; claim-level support only | MQ01 historical-content workflow | Validator: `scripts/validate_evidence_register.py`; acceptance scope must be inspected |
| `MQ01-DECISIONS` | `source/MQ01_decision_log.md` | Content decision log | `EXISTING`; entries bind only if Owner acceptance is verified | MQ01 historical-content workflow | Acceptance reference `UNKNOWN` per entry until inspected |
| `MQ01-BRIEF` | `source/MQ01_scene_brief.md` | Scene/quest brief | `EXISTING`; bounded design brief | MQ01 historical-content workflow | Review reference `UNKNOWN` |
| `MQ01-QA` | `source/Bao_cao_QA_MQ01.md` | QA report | `EXISTING`; review evidence only | MQ01 QA | Does not independently create canon |

## 4. Project governance and continuity

| Path | Type | Status and authority | Provenance / producing task | Review, commit, or PR reference |
| --- | --- | --- | --- | --- |
| `projects/si-tu-chapter-1/PROJECT_STUDIO.md` | Project Studio record | `ACTIVE`; organizational source of project identity and isolation | STUDIO-005 | Contract commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`; implementation PR `NONE` |
| `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md` | Source-authority rule | `ACTIVE`; canonical project operational rule | STUDIO-005 / `OWNER_DECISION-SOURCE-001` | Implementation PR `NONE` |
| `projects/si-tu-chapter-1/DECISIONS.md` | Project decision register | `ACTIVE`; scoped accepted decisions | STUDIO-005 | Approval evidence in contract; implementation PR `NONE` |
| `projects/si-tu-chapter-1/cells/SITU-BASELINE-001.md` | Cell record | `HANDOFF`; temporary bootstrap scope | STUDIO-005 | QA verdict `NONE`; integration verdict `NONE` |
| `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/` | Four-record memory package | `HANDOFF`; operational evidence only | STUDIO-005 | Last checkpoint declared inside package |
| `tasks/STUDIO-005.md` | Accepted task contract | `APPROVED`; binding implementation scope | Studio Owner | Commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff` |
| `tasks/STUDIO-005-AMENDMENT-001.md` | Accepted bounded amendment | `OWNER_APPROVED`; adds the amendment record and Windows-compatible save-roundtrip test to scope | Studio Owner | `WORKTREE_ONLY` until the implementation commit |
| `studio/PROJECT_STUDIO_TEMPLATE.md` | Reusable organizational template | `EXISTING`; template, not project truth | STUDIO-003/004 governance | Commit/reference `UNKNOWN` in this map |
| `studio/MEMORY_PROTOCOL.md` | Persistent-memory protocol | `EXISTING`; canonical studio protocol | STUDIO-004 | Commit/reference `UNKNOWN` in this map |

## 5. Studio-wide rules and historical workflow

| Path or group | Type | Status and authority | Provenance | Review reference |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Repository instructions | `ACTIVE`; repository-wide and project-scoped rules | Studio governance plus STUDIO-005 | Implementation PR `NONE` |
| `docs/GAME_VISION.md` | Vision template | `TEMPLATE`; unfilled fields are not project truth | Repository bootstrap | `UNRESOLVED` |
| `docs/DECISIONS.md` | Studio-wide decision register | `ACTIVE`; do not duplicate as project decisions | Repository governance | `UNKNOWN` |
| `docs/HISTORICAL_CONTENT_SYSTEM.md` | Historical-content system | `ACTIVE`; evidence and QA rules | Historical-game workflow | Existing tests/validator where applicable |
| `.agents/skills/historical-game-builder/` | Repository skill and schemas | `EXISTING`; workflow guidance, not independent canon | Historical-game workflow | `UNKNOWN` |
| `studio/STUDIO_CONSTITUTION.md` | Studio constitution | `ACTIVE`; governance authority | STUDIO-001 | `UNKNOWN` |
| `studio/CELL_MODEL.md`, `studio/ACTIVATION_POLICY.md`, `studio/HANDOFF_PROTOCOL.md` | Cell, activation, handoff rules | `ACTIVE`; canonical studio protocols | STUDIO-003/004 | `UNKNOWN` |

## 6. Derived design, data, code, and evidence

| Path or group | Type | Current status and authority | Provenance / producing task | Review, commit, or PR reference |
| --- | --- | --- | --- | --- |
| `docs/design/` | Derived design specifications | `EXISTING`; working/approved status must be read per file | Milestone 2A and related tasks | `UNKNOWN` per file |
| `data/vertical_slice/` | Prototype content and balance data | `EXISTING`; prototype evidence, not blanket canon | Milestone 2A/2A.2 | Tested by existing suite |
| `prototype/rules/` | Prototype rules code | `EXISTING`; prototype implementation evidence | Milestone 2A/2A.2 | `tests/test_rules_prototype.py` |
| `reports/` | Assumptions, decisions, gaps, QA, run reports, traceability | `EXISTING`; authority varies by artifact | Prior milestones | Inspect each artifact; unknowns remain explicit |
| `scripts/validate_evidence_register.py` | Evidence-register validator | `EXISTING`; structural validation only | Historical-content workflow | `tests/test_validate_evidence_register.py` |
| `scripts/validate_project_studio.py` | Project Studio validator | `ACTIVE`; deterministic structural guard | STUDIO-005 | `tests/test_validate_project_studio.py` |
| `tests/` | Automated test suite and fixtures | `EXISTING`; deterministic operational evidence; save-roundtrip fixture amended for Windows compatibility | Multiple tasks plus STUDIO-005 Amendment 001 | Current run result recorded in task memory/PR |

## 7. External capability register

| Path | Type | Status and authority | Provenance | Review reference |
| --- | --- | --- | --- | --- |
| `studio/EXTERNAL_CAPABILITY_CANDIDATES.md` | Candidate register | `UNASSESSED`; `NOT INSTALLED`; `NO DECISION`; no repository authority | STUDIO-005 | Evaluation deferred to STUDIO-006 |

## 8. Discovery and update rules

- Use this map to locate artifacts; do not assume that the newest filename is authoritative.
- Preserve each artifact's source path and provenance. Do not move existing artifacts to simplify the map.
- Record unknown values as `UNKNOWN`, `UNRESOLVED`, or `NONE`; do not invent review or acceptance references.
- Update this index under an accepted task when artifacts are created, moved by explicit authority, superseded, accepted, or given a durable review reference.
- A map update cannot promote content, amend a decision, or transfer authority.
