# SITU-CH1 Source Authority and Content Promotion

## 1. Canonical scope

This file is the canonical operational home for source relationships, content comparison, historical evidence classifications, and promotion into official project artifacts for `SITU-CH1`.

- `source_relationship`: `CO-EQUAL`
- `official_integrated_gdd`: `NOT_YET_DESIGNATED`
- owner decision: `OWNER_DECISION-SOURCE-001`
- authorizing contract: `tasks/STUDIO-005.md`

## 2. Immutable Owner-created working drafts

| Source ID | Repository path | Baseline Git blob SHA | Status |
| --- | --- | --- | --- |
| `GDD-V22` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v22_Ban_Chi_Tiet_Day_Du.docx` | `a6d6d5519f5fe7b201207a4bfa2cffc1be8ecd3c` | `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` |
| `GDD-V23` | `source/Si_Tu_Hanh_Trinh_Thi_Cu_Chuong_1_GDD_v23_Hieu_Chinh_MQ01.docx` | `e73d3b03a78160f761320184ddbe48f5339d752a` | `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` |

Both drafts were created by the Studio Owner through prior reading, research, reasoning, and design work. They are eligible sources for preservation, copying, adaptation, combination, revision, rejection, or later promotion.

Neither draft automatically supersedes, overrides, corrects, or takes precedence over the other. This rule applies globally and within MQ01A–MQ01D and `DOC01`. Version number, filename, modification date, scope, length, completeness, polish, or the existence of support artifacts does not change this relationship.

The two DOCX files are read-only provenance baselines. Do not edit, replace, rename, move, regenerate, normalize, or resave them. Source immutability does not make either draft historically true or officially accepted.

## 3. Three separate authority layers

| Layer | Question | Valid evidence | Authority limit |
| --- | --- | --- | --- |
| Design provenance | Where did an idea, structure, wording, mechanic, or alternative come from? | Bounded V22/V23 sections and later Owner-created design artifacts | Establishes origin, not historical truth or official acceptance |
| Historical evidence | How strongly is a checkable historical claim supported? | Evidence register, real sources, exact locators, and evidence classifications | Supports or restricts individual claims, not whole-document precedence |
| Official project authority | What is accepted for production and continuity? | Explicit scoped Studio Owner decisions and a designated canonical artifact | Exists only within approved and durably materialized scope |

Evidence may strengthen or weaken a historical claim without choosing an entire GDD. Design provenance may establish authorship without proving historical accuracy. A copied passage does not become official solely because it was copied into another file.

Memory records, artifact maps, filenames, newer versions, recent messages, model recommendations, QA reports, and test success cannot independently create official project authority.

## 4. Bounded content unit

Comparison and promotion operate on one reviewable unit at a time: a quest, scene, mechanic, character role, chronology rule, state variable, dialogue passage, UI term, prop, document, or other explicitly bounded element.

Each unit records:

- unit ID and scope;
- player goal and gameplay function;
- dependencies and affected artifacts;
- non-negotiable Owner intent;
- relevant V22 and V23 locations;
- historical claims and evidence classifications;
- alternatives, conflicts, rationale, uncertainty, and review status.

Silence in one draft is not evidence that the draft rejects content in the other.

## 5. Content comparison and promotion gate

Before a bounded content unit enters an official project artifact, the responsible task must complete every applicable step:

1. **Define the unit and purpose.** Record identity, scope, player goal, gameplay function, dependencies, and non-negotiable Owner intent.
2. **Trace design provenance.** Cite the relevant bounded V22 and V23 locations and any later Owner-created or support artifacts.
3. **Compare alternatives fairly.** Record similarities, differences, omissions, and incompatibilities without choosing by version number, recency, filename, length, polish, convenience, or model preference.
4. **Test internal logic.** Check causality, chronology, character motivation and authority, quest dependencies, state variables, terminology, player actions, feedback, consequences, failure paths, and accepted decisions.
5. **Apply historical evidence classification.** Extract checkable claims and classify each as `DIRECT`, `RECONSTRUCTION`, `INFERENCE`, `FICTION`, or `UNRESOLVED` under `docs/HISTORICAL_CONTENT_SYSTEM.md`.
6. **Preserve playability.** Keep meaningful player action, readable feedback, and fail-forward behavior. Generalize, label, redesign, or use controlled fiction when unsupported specificity would otherwise block the function.
7. **Record recommendation and rationale.** State what is kept, changed, combined, removed, or held; why; supporting claim and decision IDs; affected artifacts; and residual uncertainty.
8. **Perform independent review.** Apply historical, narrative, gameplay, cross-document, delivery, and integration checks proportionate to the unit.
9. **Obtain Studio Owner approval.** A recommendation remains nonbinding until the Studio Owner approves its defined scope.
10. **Materialize durably.** Update the explicitly designated canonical artifact and project decision register through an authorized branch and review artifact.

Passing one step cannot compensate for failing another. If evidence and logic do not support a safe recommendation, preserve the alternatives and record `HOLD` or `UNRESOLVED`. Do not fill the gap with an invented fact or silently declare one draft the winner.

## 6. MQ01 support artifacts and authority limits

| Artifact | Function | Authority limit |
| --- | --- | --- |
| `source/MQ01_evidence_register.csv` | Individual claims, evidence levels, citations, allowed uses, and decisions | Supports or restricts individual claims only |
| `source/MQ01_decision_log.md` | Recorded keep/change/remove/hold reasoning where present | Binding only when an entry has verified Studio Owner acceptance and only within its recorded scope |
| `source/MQ01_scene_brief.md` | Bounded MQ01 scene/quest purpose and design constraints | A design brief, not blanket historical proof or GDD precedence |
| `source/Bao_cao_QA_MQ01.md` | QA findings, conditions, uncertainty, and production restrictions | Review evidence; cannot create canon or infer Studio Owner approval |

The actual status and scope of each record must be inspected. Existence, completeness, a positive QA result, or association with V23 does not elevate V23 or reduce V22.

## 7. `DOC01` boundary

`DOC01` may remain a greybox gameplay object and its gameplay function may be assessed. Final layout, wording, seals, signatures, paper, ink, dimensions, fingerprints, or other period-specific material form must not be locked without separate contemporaneous documentary or material evidence appropriate to time and place.

A legal or administrative rule may support that a document existed, mattered, or served a function. It does not by itself prove visual or material form. Later examples may be labeled `LATER_ANALOGY` for a bounded comparison but cannot be silently transferred backward as contemporary proof.

## 8. Historical evidence and controlled fiction

- `DIRECT`: a cited source directly states or depicts the claim at the written specificity.
- `RECONSTRUCTION`: qualified scholarship reconstructs the claim from evidence.
- `INFERENCE`: a bounded conclusion follows from cited premises; record the inferential step.
- `FICTION`: game-created content; record the historical constraint it must not violate.
- `UNRESOLVED`: evidence is missing, conflicting, or too weak; remove, generalize, relocate, hold, or block factual player-facing use.

For `DIRECT` and `RECONSTRUCTION`, record a real citation, exact locator, and working URL or stable bibliographic identifier. Do not invent a citation, quotation, archival locator, folio, page, image, period form, title, date, material detail, or URL.

The absence of direct evidence does not automatically prohibit playable content. It requires honest classification, constrained fiction or inference, and a production restriction proportionate to uncertainty.

## 9. Stop and escalation conditions

Stop, record `UNRESOLVED`, and request an authorized amendment or decision when:

- a source-authority rule conflicts with an accepted decision;
- a required citation or locator cannot be verified;
- a later-period example is being used as direct proof of an earlier form;
- a character or player action assumes unsupported authority;
- final asset specificity exceeds the evidence level;
- a task attempts to edit either GDD source in place;
- a recommendation would create binding canon without Studio Owner approval;
- safe continuation requires choosing one whole draft by model judgment.

## 10. Initial official state

No integrated official GDD is designated at bootstrap. Existing accepted content-specific decisions, if verified, remain effective only within their recorded scope. STUDIO-005 itself promotes no game content.

