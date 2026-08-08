---
name: historical-game-builder
description: Use when researching, designing, revising, or QA-auditing a historical game's GDD, quest, scene, dialogue, prop, chronology, terminology, authority structure, or mechanic, especially when the work must distinguish direct evidence, reconstruction, inference, fiction, and unresolved claims.
---

# Historical Game Builder

Use this skill for one bounded unit at a time: one scene, quest chain, prop, mechanic, terminology rule, chronology question, or historical question. Do not turn one request into a rewrite of the whole GDD unless the user explicitly asks for that scope.

## Required workflow

1. **Define the unit.** State the scene/quest/prop/mechanic/question ID, source files, current version, player-facing purpose, and production target.
2. **Extract checkable claims.** Split historical assertions, material-culture assumptions, institutional roles, dates, place names, dialogue facts, and gameplay consequences into claim-sized items.
3. **Research claim by claim only when allowed.** If the task forbids research, use only supplied sources and mark unsupported claims at lower certainty.
4. **Classify every claim.** Use `DIRECT`, `RECONSTRUCTION`, `INFERENCE`, `FICTION`, or `UNRESOLVED`; do not present inference, fiction, or unresolved material as settled history.
5. **Pass the evidence gate.** Ensure each factual assertion has a claim ID, source-backed claims have citation and locator, and later analogies are not back-projected.
6. **Revise in layers.** Change the Evidence Register first, then world/terminology rules, then quest brief and gameplay consequence, then treatment/dialogue/UI/prop description.
7. **Audit independently.** Apply the QA gates after revision and record remaining uncertainty and production restrictions.

Keep the project owner's existing creative decisions unless evidence, source limits, or internal contradictions require a proposed change. Prefer narrower wording, lower specificity, or safer gameplay framing over invented certainty.

## Required outputs for substantial work

For meaningful scene/quest/prop/mechanic work, produce or update:

- scene brief;
- evidence register;
- decision log;
- revised patch for the relevant GDD/quest/world files;
- QA report.

## References and templates

Read the relevant reference file completely before acting:

- `references/artifact-schemas.md` for required schemas and field definitions.
- `references/source-and-evidence-standard.md` before sourcing, classifying, or comparing historical claims.
- `references/qa-gates.md` before approving or blocking a patch.

Use these templates for new artifacts:

- `assets/scene_brief_template.md`
- `assets/evidence_register_template.csv`
- `assets/decision_log_template.md`
- `assets/qa_report_template.md`

## Stop conditions

Stop, lower the claim level, or request/recommend more evidence when any condition applies:

- no citation, quote, locator, URL, DOI, identifier, date, office title, procedure, artifact form, or translation can be verified from allowed sources;
- a source supports existence or function but not material form, wording, layout, seal, signature, fingerprint, size, ink, or paper;
- evidence belongs to a later period and can only be labeled `LATER_ANALOGY`, not proof for the earlier setting;
- sources conflict and no stronger source resolves the conflict;
- a gameplay beat would grant a character authority that the evidence does not support;
- an asset request is more specific than the evidence level allows;
- source files are protected by task scope and would need modification to pass.

When blocked, state what evidence would unblock the claim and propose a historically safer gameplay alternative if possible. Do not embed MQ01-specific conclusions as universal rules for every quest; use MQ01 only as a calibration example when the current repository asks for it.
