# SITU-CH1 Project Decision Register

This register contains project-specific decisions only. Studio-wide governance remains in its existing canonical files. Full operational rules are referenced rather than duplicated.

## SITU-DEC-001 — One Project Studio

- `scope`: organizational identity and namespace
- `status`: `ACCEPTED`
- `authority`: Studio Owner through approved `tasks/STUDIO-005.md`
- `decision`: V22 and V23 belong to one project, `SITU-CH1`, under `projects/si-tu-chapter-1/`.
- `rationale`: The files describe versions and alternatives within one historical game project, not separate projects.
- `provenance`: GDD filenames, repository context, and STUDIO-005 contract
- `affected_artifacts`: Project Studio files, artifact map, task memory
- `approval_evidence`: `tasks/STUDIO-005.md` at commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `supersedes`: `NONE`

## OWNER_DECISION-SOURCE-001 — Co-equal working drafts

- `scope`: V22, V23, MQ01A–MQ01D, and `DOC01`
- `status`: `ACCEPTED`
- `authority`: Studio Owner
- `decision`: V22 and V23 are `AUTHOR_CREATED_WORKING_DRAFT` and `CO_EQUAL_INPUT` artifacts. Neither has automatic global or scoped precedence.
- `rationale`: Both were created by the Studio Owner through prior research and design; version labels or support artifacts do not decide content quality or authority.
- `provenance`: Studio Owner clarification recorded in the approved STUDIO-005 contract
- `affected_artifacts`: Both GDD sources and all future comparison or integration work
- `approval_evidence`: `tasks/STUDIO-005.md`, Sections 2, 4, 7, and 8; commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `supersedes`: Any unaccepted draft-level precedence assumption; no accepted content-specific decision is nullified

## SITU-DEC-003 — Separate authority layers

- `scope`: all `SITU-CH1` content and evidence work
- `status`: `ACCEPTED`
- `authority`: Studio Owner through approved STUDIO-005 contract
- `decision`: Design provenance, historical evidence, and official project authority are separate layers.
- `rationale`: Authorship does not prove history; evidence does not select an entire draft; copying does not create official acceptance.
- `provenance`: `tasks/STUDIO-005.md`
- `affected_artifacts`: `SOURCE_AUTHORITY.md`, artifact map, later GDD/content tasks
- `approval_evidence`: Contract commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `supersedes`: `NONE`

## SITU-DEC-004 — No integrated official GDD at bootstrap

- `scope`: project-wide content authority at STUDIO-005 bootstrap
- `status`: `ACCEPTED`
- `authority`: Studio Owner
- `decision`: `official_integrated_gdd: NOT_YET_DESIGNATED`.
- `rationale`: STUDIO-005 creates organizational and validation structure; it does not review and promote bounded game content.
- `provenance`: `tasks/STUDIO-005.md`
- `affected_artifacts`: Project Studio record, source authority, README, memory, validators
- `approval_evidence`: Contract commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `supersedes`: `NONE`

## SITU-DEC-005 — Bounded content-promotion gate

- `scope`: any later recommendation to preserve, copy, adapt, combine, reject, hold, or promote content
- `status`: `ACCEPTED`
- `authority`: Studio Owner through approved STUDIO-005 contract
- `decision`: Official promotion requires bounded comparison, provenance, internal-logic checks, historical evidence classification, playability preservation, recorded rationale, independent review, Studio Owner approval, and durable canonical update.
- `rationale`: This permits reasoned reuse from either draft while blocking arbitrary invention and silent precedence.
- `provenance`: `tasks/STUDIO-005.md`, operationalized in `SOURCE_AUTHORITY.md`
- `affected_artifacts`: All future official content artifacts and project decision entries
- `approval_evidence`: Contract commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `supersedes`: `NONE`

## SITU-DEC-006 — `DOC01` greybox and material boundary

- `scope`: `DOC01` gameplay object and any visual/material production specification
- `status`: `ACCEPTED`
- `authority`: Studio Owner through approved STUDIO-005 contract and existing historical-content rules
- `decision`: `DOC01` may remain a greybox gameplay object; final layout, wording, seals, signatures, paper, ink, dimensions, fingerprints, and other period-specific material details remain blocked without appropriate separate contemporaneous evidence.
- `rationale`: Evidence for a document's function or legal importance does not prove its physical form.
- `provenance`: `docs/HISTORICAL_CONTENT_SYSTEM.md`, MQ01 support artifacts, and `tasks/STUDIO-005.md`
- `affected_artifacts`: MQ01/DOC01 design, UI, prop, art, and future GDD content
- `approval_evidence`: Contract commit `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `supersedes`: `NONE`

## Decision use rules

- `SOURCE_AUTHORITY.md` is the canonical operational rule for comparison and promotion.
- Later entries must state scope, status, authority, rationale, provenance, affected artifacts, approval evidence, and supersession.
- A proposal, QA result, test pass, memory checkpoint, chat message, or newer filename does not become an accepted decision by itself.
- Binding changes require Studio Owner authority and durable repository evidence.

