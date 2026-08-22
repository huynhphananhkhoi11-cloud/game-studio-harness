# SITU-CH1 Artifact Map

## 1. Purpose and status vocabulary

This is the central repository index for `SITU-CH1`. It locates artifacts without copying or moving them. Mapping an artifact preserves discovery and provenance; it does not grant historical truth, official content authority, acceptance, or precedence.

Status values include `IMMUTABLE SOURCE`, `WORKING INPUT`, `EXISTING`, `ACTIVE`, `COMPLETE`, `TEMPLATE`, `UNASSESSED`, `EVALUATED`, `UNKNOWN`, `UNRESOLVED`, and `NONE`.

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
| `projects/si-tu-chapter-1/PROJECT_STUDIO.md` | Project Studio record | `ACTIVE`; STUDIO-005 bootstrap `COMPLETE`; organizational source of project identity and isolation | STUDIO-005 | Pull Request `#9` merged into `main` as `4e812242c9bc6f96b141e60ff2cf4344bef30ea8` |
| `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md` | Source-authority rule | `ACTIVE`; canonical project operational rule | STUDIO-005 / `OWNER_DECISION-SOURCE-001` | QA-01 v14 `APPROVE`; Pull Request `#9` merged as `4e812242c9bc6f96b141e60ff2cf4344bef30ea8` |
| `projects/si-tu-chapter-1/DECISIONS.md` | Project decision register | `ACTIVE`; scoped accepted decisions | STUDIO-005 | Approval evidence in contract; Pull Request `#9` merged |
| `projects/si-tu-chapter-1/cells/SITU-BASELINE-001.md` | Cell record | `COMPLETE`; temporary bootstrap Cell dissolved | STUDIO-005 | QA-01 v14 `APPROVE`; Review & Integration `APPROVE`; merge commit `4e812242c9bc6f96b141e60ff2cf4344bef30ea8` |
| `projects/si-tu-chapter-1/memory/tasks/STUDIO-005/` | Four-record memory package | `COMPLETE`; operational evidence only | STUDIO-005 | Last checkpoint `STUDIO-005-CP-0016`; Pull Request `#9` merged |
| `tasks/STUDIO-005.md` | Accepted task contract | `APPROVED`; binding implementation scope | Studio Owner | Commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff` |
| `tasks/STUDIO-005-AMENDMENT-001.md` | Accepted bounded amendment | `OWNER_APPROVED`; adds the amendment record and Windows-compatible save-roundtrip test to scope | Studio Owner | Correction head `8212a080f7a22a96a521829d81e00a7763bb2d50`; Pull Request `#9` merged |
| `studio/PROJECT_STUDIO_TEMPLATE.md` | Reusable organizational template | `EXISTING`; template, not project truth | STUDIO-003/004 governance | Commit/reference `UNKNOWN` in this map |
| `studio/MEMORY_PROTOCOL.md` | Persistent-memory protocol | `EXISTING`; canonical studio protocol | STUDIO-004 | Commit/reference `UNKNOWN` in this map |

## 5. Studio-wide rules and historical workflow

| Path or group | Type | Status and authority | Provenance | Review reference |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Repository instructions | `ACTIVE`; repository-wide and project-scoped rules | Studio governance plus STUDIO-005 | Pull Request `#9` merged |
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
| `scripts/validate_project_studio.py` | Project Studio validator | `ACTIVE`; validates both `BASELINE_UNASSESSED` and `EVALUATED` whole-register modes while preserving shared safe states | STUDIO-005 plus `tasks/STUDIO-006-AMENDMENT-001.md` | Validator transition Pull Request `#14` merged as `4258654fddd83b3f7e0d00936c22e3954e321767`; evaluated register PASS at reconciled head `25f46f122023e6d900f87253799dec895e1bf218` |
| `tests/` | Automated test suite and fixtures | `EXISTING`; deterministic operational evidence, including baseline/evaluated transition coverage and Windows-compatible save-roundtrip coverage | Multiple tasks, STUDIO-005 Amendment 001, and STUDIO-006 validator transition | Complete 77-test suite PASS in Rules CI run `31925302692` at reconciled head `25f46f122023e6d900f87253799dec895e1bf218` |

## 7. External capability register — current state

| Path | Type | Status and authority | Provenance | Review reference |
| --- | --- | --- | --- | --- |
| `studio/EXTERNAL_CAPABILITY_CANDIDATES.md` | Candidate register | `EVALUATED`; every candidate remains `NOT INSTALLED` and `NO DECISION`; no repository authority | Registered as `UNASSESSED` by STUDIO-005, then evaluated by STUDIO-006 under the approved contract and amendment | Evaluated register validator PASS at reconciled head `25f46f122023e6d900f87253799dec895e1bf218`; final Pull Request #12 head must be verified from PR metadata |

## 8. STUDIO-006 external-capability evaluation

| Path or evidence | Type | Status and authority | Provenance | Review, commit, or PR reference |
| --- | --- | --- | --- | --- |
| `tasks/STUDIO-006.md` | Accepted task contract | `APPROVED`; evaluation-only authority | Studio Owner | Pull Request `#11` merged into `main` as `0e2d7bab5c7c876338a246be16d46a8f1073b95c` |
| `tasks/STUDIO-006-AMENDMENT-001.md` | Accepted bounded amendment | `APPROVED`; authorizes validator transition only | Studio Owner | Pull Request `#13` merged as `6476b65463815a1f5ccfbb373f8151426d63d8dc` |
| `scripts/validate_project_studio.py` and `tests/test_validate_project_studio.py` | Dual-mode validator transition | `MERGED`; validates baseline and evaluated register modes | STUDIO-006 Amendment 001 implementation | Pull Request `#14` merged as `4258654fddd83b3f7e0d00936c22e3954e321767` |
| `studio/EXTERNAL_CAPABILITY_CANDIDATES.md` | Evaluated candidate register | `EVALUATED`; every candidate remains `NOT INSTALLED` and `NO DECISION` | STUDIO-006 | Pull Request `#12`; reconciled head `25f46f122023e6d900f87253799dec895e1bf218`; final author-correction head must be verified from PR metadata |
| `studio/EXTERNAL_CAPABILITY_EVALUATION.md` | Evidence-based evaluation report | `HANDOFF`; non-binding recommendations only | STUDIO-006 | Ten immutable candidate commits; Pull Request `#12`; Official QA-06 corrections from reconciled head `25f46f122023e6d900f87253799dec895e1bf218` addressed; QA rerun pending final-head CI |
| `projects/si-tu-chapter-1/memory/tasks/STUDIO-006/` | Four-record schema-1 memory package | `HANDOFF`; operational evidence only | STUDIO-006 | Last checkpoint `STUDIO-006-CP-0007`; writer claim `RELEASED` for QA rerun; Pull Request `#12` |
| Rules CI run `31925302692` | Reconciliation verification | `PASS`; `Validate data` and complete 77-test suite passed | Pull Request `#12` at reconciled head | https://github.com/huynhphananhkhoi11-cloud/game-studio-harness/actions/runs/31925302692 |

The report accepts no candidate for use. An `ADOPT` or `ADAPT` recommendation still requires a separate accepted implementation contract before external bytes, instructions, dependencies, hooks, or runtime behavior enter the repository.

## 9. Discovery and update rules

- Use this map to locate artifacts; do not assume that the newest filename is authoritative.
- Preserve each artifact's source path and provenance. Do not move existing artifacts to simplify the map.
- Record unknown values as `UNKNOWN`, `UNRESOLVED`, or `NONE`; do not invent review or acceptance references.
- Update this index under an accepted task when artifacts are created, moved by explicit authority, superseded, accepted, or given a durable review reference.
- A map update cannot promote content, amend a decision, or transfer authority.
