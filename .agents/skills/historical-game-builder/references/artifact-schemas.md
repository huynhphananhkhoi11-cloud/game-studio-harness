# Artifact Schemas

Use these schemas consistently across scene briefs, evidence registers, decision logs, and QA reports.

## Scene Brief

Required fields:

1. **Scene/quest ID** — Stable ID used in filenames, claim IDs, quest catalog, and QA notes.
2. **Current version and source file** — GDD/source version and the file(s) being checked.
3. **Historical date range and place** — Date span and location at the specificity supported by evidence.
4. **Player character and immediate goal** — Who the player controls and what they need now.
5. **Conflict and authority structure** — What blocks the goal and which roles have power to decide, witness, advise, or object.
6. **Core player verbs** — Actions the player performs, such as inspect, compare, ask, choose, wait, or report.
7. **Required gameplay consequence** — Required state change, flag, resource change, unlock, delay, or fail-forward result.
8. **Historical anchors that must remain true** — Claims that cannot be contradicted by writing, gameplay, UI, or art.
9. **Fiction budget** — Characters, dialogue, conflicts, props, or feedback that may be fictional while respecting anchors.
10. **Open research questions** — Unknowns that must remain unresolved or be researched later.
11. **Dependencies on other GDD sections** — Linked quests, variables, mechanics, UI, assets, chronology, terminology, or ending logic.

## Evidence Register CSV

The CSV must use exactly these 12 columns in this order:

```csv
claim_id,scene_id,claim,domain,evidence_level,source_citation,locator,source_url,premise_or_constraint,allowed_use,decision,notes
```

Allowed `evidence_level` values:

- `DIRECT` — The source directly supports the claim at the stated specificity.
- `RECONSTRUCTION` — The claim is a cautious reconstruction from multiple compatible sources or expert synthesis.
- `INFERENCE` — The claim follows from stated premises but is not directly asserted by the source.
- `FICTION` — The element is invented for the game and bounded by historical constraints.
- `UNRESOLVED` — The claim remains unknown, disputed, or unsupported at production specificity.

Allowed `decision` values:

- `KEEP` — Keep the specific content as currently written or planned.
- `CHANGE` — Revise the specific content to fit evidence or design constraints.
- `REMOVE` — Remove the specific content until support exists or because it is wrong for scope.
- `HOLD` — Do not finalize; keep as pending, greybox, research-needed, or production-blocked.

`allowed_use` must say where the claim may appear, such as `player-facing fact`, `production note only`, `visual analogy only`, `fictional plot device`, or `prohibited pending evidence`.

## Decision Log

Each decision record must include:

- **Decision ID** — Stable ID tied to the scene/quest/prop.
- **Original content** — The old content, assumption, or risk being addressed.
- **Revised content** — The approved or proposed replacement.
- **Reason** — Why the change is needed.
- **Evidence claim IDs** — Claim IDs supporting the decision.
- **Affected GDD sections/variables/quests/UI/assets** — Downstream items to patch or verify.
- **Follow-up work** — Research, QA, asset, writing, or implementation tasks still open.

## QA Report

A QA report must include:

- **Scope/files checked** — The exact unit and files reviewed.
- **Evidence gate** — Status and findings for citations, locators, levels, and allowed use.
- **Historical QA** — Fit with time, place, institution, terminology, material culture, and source strength.
- **Narrative QA** — Character authority, motivation, stakes, and overclaim risks.
- **Gameplay QA** — Player verbs, feedback, consequences, fail-forward, and variable effects.
- **Cross-document consistency** — Date, role, term, quest, UI, variable, asset, and GDD alignment.
- **Render/document QA** — Text, prop, UI, and production deliverables are not more specific than evidence.
- **Residual uncertainties and production restrictions** — What remains blocked, greybox, or research-needed.
