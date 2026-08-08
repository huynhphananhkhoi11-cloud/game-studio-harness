# QA Gates

Each gate may be `PASS`, `CONDITIONAL`, or `BLOCKED`.

- `PASS` — Ready for the current production stage.
- `CONDITIONAL` — Usable only with named restrictions, follow-up, or greybox limits.
- `BLOCKED` — Must not proceed until the blocking issue is resolved or scope is reduced.

## 1. Evidence

Checklist:

- every factual historical assertion has a `claim_id`;
- every `DIRECT` or `RECONSTRUCTION` claim has source citation and locator;
- source-backed `source_url` or identifier is recorded when available;
- `INFERENCE`, `FICTION`, and `UNRESOLVED` are not presented as established historical fact;
- `LATER_ANALOGY` is not converted into contemporaneous proof.

## 2. Historical Fit

Checklist:

- date range, polity, place, institution, role, terminology, and material-culture specificity match the evidence level;
- sources support the stated level of detail;
- existence or legal function of a document is not treated as proof of layout, wording, paper, ink, seals, signatures, fingerprints, or dimensions;
- unresolved claims are held, removed, or reduced in specificity.

## 3. Narrative & Authority

Checklist:

- character roles and authority are plausible within the evidence;
- protagonists do not judge, command, certify, or punish beyond their role;
- dramatic beats do not require false historical certainty;
- creative decisions from the owner are preserved unless evidence or contradictions require change.

## 4. Gameplay

Checklist:

- the player has meaningful verbs, readable feedback, and consequences;
- fail-forward exists when the player fails, refuses, or lacks evidence;
- choices do not silently grant impossible authority;
- variables, resources, flags, and unlocks reflect what the evidence permits.

## 5. GDD/Cross-document Consistency

Checklist:

- dates, roles, terminology, variables, quest IDs, UI labels, assets, and dependencies do not contradict each other;
- changed claims are reflected in decision logs and patch notes;
- affected GDD sections, quest briefs, UI, and prop descriptions are named for follow-up;
- source files protected by scope remain unmodified.

## 6. Delivery

Checklist:

- deliverables are in the expected filenames and schema;
- asset requests are not more specific than evidence level;
- original files and source evidence are not overwritten;
- residual uncertainties and production restrictions are clearly handed off;
- QA status and blocking issues are visible to production owners.
