# STUDIO-002 — Create Operational Profiles for Six AI Agents

## Goal
Create six reusable operational AI-agent profiles so any suitable runtime/model can enter one role and work from repository evidence without relying on private chat history.

`AGENT ROLE != RUNTIME != MODEL != PROVIDER`

## Context
Shared governance already exists in:
- `AGENTS.md`
- `studio/STUDIO_CONSTITUTION.md`
- `studio/ORG_CHART.md`
- `studio/AGENT_REGISTRY.md`
- `studio/MODEL_REGISTRY.md`
- `studio/HANDOFF_PROTOCOL.md`
- `docs/GAME_VISION.md`
- `docs/DECISIONS.md`

## Scope
Create exactly:
- `tasks/STUDIO-002.md`
- `studio/agents/PRODUCER-01.md`
- `studio/agents/GAME-DESIGN-01.md`
- `studio/agents/NARRATIVE-RESEARCH-01.md`
- `studio/agents/ENGINEERING-01.md`
- `studio/agents/QA-01.md`
- `studio/agents/REVIEW-INTEGRATION-01.md`

## Non-Goals
Do not choose engine/language/framework/dependencies; define game vision or canon; assign permanent models/providers; implement gameplay; install/download tools; create secrets; modify existing governance; commit/push/merge.

## Shared Principles

### LOCKED / GUIDED / OPEN
- **LOCKED:** follow accepted constraints during execution; agents may still open a `CHANGE PROPOSAL`.
- **GUIDED:** intent exists, but specialists may choose reversible local solutions, prototype and compare alternatives.
- **OPEN:** no binding decision exists; specialists may research, benchmark, experiment and propose freely.

### Reversible Decisions
Agents may autonomously make reversible, local, in-scope choices that do not contradict accepted decisions, alter canon, create major dependencies/costs, or materially constrain other departments.

### Creative Freedom
Agents may challenge weak assumptions, propose alternatives, prototype, compare multiple references, explain trade-offs, and reject poor approaches when evidence supports it.

### Historical Integrity
When relevant, use:
- `FACT`
- `INTERPRETATION`
- `ASSUMPTION`
- `UNRESOLVED`
- `FICTIONALIZATION`
- `PROPOSAL`

Historical fictionalization is allowed when clearly identified internally. Historical claims must not be invented or presented with false certainty.

### No Hidden Context Dependency
Use task, repo, accepted decisions, diff, tests, evidence, concise rationale and handoff. Do not require another AI's private chain-of-thought.

## Acceptance Criteria
- [ ] Exactly seven allowed files.
- [ ] Six operational profiles.
- [ ] Producer is not a creative approval bottleneck.
- [ ] Game Design retains high creative autonomy.
- [ ] Narrative & Research protects historical truth while permitting responsible fictionalization.
- [ ] Engineering has high local implementation autonomy without silently changing intent.
- [ ] QA tries to falsify deliverables and does not self-certify its own fixes.
- [ ] Review is independent from the authoring session.
- [ ] Runtime/model/provider neutrality is explicit.
- [ ] Handoffs use LEVEL 0 / 1 / 2 based on risk.
- [ ] No existing file modified.

## Verification
```powershell
git status --short --untracked-files=all
git diff --stat
```

Before commit, after staging:
```powershell
git diff --cached --check
```

## Definition of Done
The seven files pass scope review and independent content review, and Studio Owner approves them for commit/PR.
