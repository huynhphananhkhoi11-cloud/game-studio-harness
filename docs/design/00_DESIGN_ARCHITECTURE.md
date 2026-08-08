# Milestone 2A Design Architecture

## Inputs and priority
- GDD v22 DOCX SHA256 `e288157e6e83af4ffe5e70dec6808f442dcd47ba3f05a9367e156ff13c01a679` is a major design input, not immutable final truth.
- GDD v23 DOCX is used only for MQ01A-MQ01D and DOC01 corrections supported by `source/MQ01_evidence_register.csv`, `source/MQ01_scene_brief.md`, `source/MQ01_decision_log.md`, and `source/Bao_cao_QA_MQ01.md`.
- `docs/GAME_VISION.md` and `docs/DECISIONS.md` are templates/empty decision log; no engine choice is recorded.

## Method sources applied
MDA is used to connect desired emotion to dynamics, mechanics, feedback, telemetry and playtest questions. Unity production planning is applied as layered source-of-truth gates. Unreal Data Driven Gameplay, Godot Resources and ink inform data-first content records without choosing an engine. Godot signals inform domain-event style boundaries; Godot saving informs atomic save/recovery policy. Machinations informs pools/sources/sinks/converters. Xbox XAG 101/107/114 inform readable text, remappable input and UI context. GDC playtesting warns telemetry must not replace observation. GDC branching-on-a-budget informs rejoin/choice-memory. GDC historian guidance is treated as method only, not Đại Việt evidence.

## Layer contracts
| Layer | Player purpose | Inputs | Outputs | Readers | Sole writer | Events | Dependencies | Fail-forward | Source of truth | DoD |
|---|---|---|---|---|---|---|---|---|---|---|
| Player Experience & Design Pillars | Preserve life-before-exam pressure with dignity. | GDD v22 pillars. | Pillar IDs, MDA matrix. | All disciplines. | Design director. | pillar_changed | none | mark OWNER_DECISION. | this file + traceability matrix | Each feature maps to a pillar. |
| Story/Narrative Bible | Keep Chapter 1 dramatic arc coherent. | GDD v22 story, v23 MQ01 deltas. | arcs, character truths. | quest/UI/QA. | Narrative lead. | arc_revealed | historical evidence | unresolved claims become greybox. | `01_STORY_QUEST_SYSTEM_MAP.md` | No silent v22/v23 conflict. |
| Quest, Scene & Dialogue System | Turn story into playable verbs. | scene briefs, quests JSON. | state reads/writes, beats. | engine, UI, QA. | Quest system. | quest_transition | story, data | fail/skipped rejoin. | `data/vertical_slice/quests.json` | every transition logged. |
| Core Loop & Time Scheduler | Make nine-canh Nếp legible. | actions, balance. | reservations, routine summary. | engine/UI. | scheduler. | routine_resolved | state, events | refund/cancel rules. | `02_RULES...` + scheduler.py | no routine >9 slots. |
| Player State, Progression & Status Effects | Show health/alertness/morale consequences. | initial_state, balance. | clamped state, XP. | all systems. | engine pipeline. | xp_gained/status_threshold | scheduler | collapse triggers forced rest. | balance_v0.json | stress derived only. |
| Jobs, Economy, Items & Obligations | Avoid single Viên ngoại path. | jobs/items/actions. | money ledger, mastery, obligations. | engine/UI/telemetry. | economy. | job_resolved/obligation_added | state | safety-net work. | jobs/items JSON | quest items cannot sell. |
| Opportunity/Event Director | Offer three cards, choose one. | opportunities, state, seed. | eligible cards + explanation log. | UI/engine. | event_director. | opportunity_drawn | RNG state | fallback fewer cards with reason. | opportunities.json | deterministic draw. |
| Document Investigation & Exam Systems | Make documents playable without overclaim. | MQ01 evidence. | greybox evidence actions. | quest/UI. | document system. | evidence_pinned | history gate | conclusion capped to “needs comparison”. | MQ01 files + content spec | DOC01 not final asset. |
| UX/UI Interaction Contract | Define click/command/feedback. | state, quests, actions. | screen contracts. | UI implementation. | UI command adapter only. | ui_command_requested | all systems | disabled reason visible. | `04_UX...` | keyboard/controller/text scaling covered. |
| Content Data & Technical Contract | Keep prototype data-driven. | all JSON. | schemas/validator. | tools/runtime. | content pipeline. | data_validated | design specs | invalid data blocks mutation. | `03_CONTENT...` | validator passes. |
| Save, Telemetry, Playtest & QA | Reproducible tests and observation. | state/events. | save files, event dictionary. | QA/design. | save/telemetry modules. | autosave_written | engine | atomic recovery. | `05_SAVE...` | round-trip exact. |
| Historical Evidence & Controlled Fiction | Prevent fake certainty. | evidence register, QA. | claim classes/restrictions. | writers/art/UI. | historical reviewer. | claim_status_changed | all content | lower specificity/hold. | `docs/HISTORICAL_CONTENT_SYSTEM.md` + MQ01 register | every historical claim has claim ID. |

## MDA matrix
| Pillar | Aesthetics / feeling | Dynamics | Mechanics/feedback | Telemetry/playtest question |
|---|---|---|---|---|
| Đời sống trước công danh | pressured but not helpless | tradeoffs between study, work, rest | nine-canh routine, status costs, summary top five deltas | Do players explain why they rested/worked? `routine_resolved` |
| Chữ nghĩa có trọng lượng | curiosity and caution | inspect before claiming | DOC01 greybox compare, conclusion cap | Do players overclaim? `mq01_conclusion_selected` |
| Trưởng thành qua lao động | earned competence | repeat jobs/study for rank/mastery | XP thresholds, job mastery unlock direct-call | Does progress feel visible by day 18? `xp_gained` |
| Ân nghĩa không miễn phí | gratitude with unease | accept/refuse/repay aid | obligation ledger and callbacks | Do players understand obligation terms? `obligation_added` |
| Fail-forward có phẩm giá | setback with future | recover after collapse/failure | forced rest, quest failed->completed rejoin | Do players feel punished or guided? interview + `fail_forward_collapse` |
