# External Capability Candidate Register

## 1. Boundary

STUDIO-006 records a read-only evaluation of the ten candidates registered by STUDIO-005. Evaluation is not installation, adoption, trust, license acceptance, security approval, or authority over this repository. Recommendations remain non-binding until a separate Studio Owner-approved implementation contract exists.

Every candidate retains the same safe state:

- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`
- repository authority: `NONE`

The detailed method, evidence, trade-offs, and limitations are in `studio/EXTERNAL_CAPABILITY_EVALUATION.md`.

## CANDIDATE-01 — obra/superpowers

- URL: https://github.com/obra/superpowers
- bounded evaluation purpose: Assess workflow patterns for disciplined agent planning, execution, and review without importing instructions or code.
- assessment: `EVALUATED`
- evaluated reference: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- immutable reference: https://github.com/obra/superpowers/commit/b36e0829c6d0140e93cfef2ca599b1b07d4a7797
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; no SECURITY policy found in the evaluated tree; session-start command hook and automatic context injection are present
- compatibility: `CONDITIONAL`; useful planning, TDD, debugging, and review patterns overlap current governance and its automatic instructions cannot receive authority
- recommendation: `ADAPT`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-01--obrasuperpowers`
- evidence limitation: Static read-only inspection only; no installation, hook execution, or behavioral testing.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-02 — anthropics/skills

- URL: https://github.com/anthropics/skills
- bounded evaluation purpose: Assess reusable skill-package structure and documentation patterns without granting repository authority.
- assessment: `EVALUATED`
- evaluated reference: `f6656c1256d5a8adfa37db9110046ef20bac644c`
- immutable reference: https://github.com/anthropics/skills/commit/f6656c1256d5a8adfa37db9110046ef20bac644c
- license: `MIXED`; many examples use Apache-2.0 while document skills contain source-available restrictions
- security: `CONDITIONAL`; no repository SECURITY policy found in the evaluated tree and several skill folders contain executable scripts
- compatibility: `CONDITIONAL`; the folder and SKILL.md pattern is relevant, but the implementation is Claude-oriented and license boundaries differ by skill
- recommendation: `REFERENCE`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-02--anthropicsskills`
- evidence limitation: License conclusions are per inspected files, not a blanket license for the repository.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-03 — mattpocock/skills

- URL: https://github.com/mattpocock/skills
- bounded evaluation purpose: Assess narrowly scoped developer-skill organization and handoff clarity.
- assessment: `EVALUATED`
- evaluated reference: `8b78b531ab965735c5dc74f6f7a219e1e37326df`
- immutable reference: https://github.com/mattpocock/skills/commit/8b78b531ab965735c5dc74f6f7a219e1e37326df
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; no SECURITY policy found; setup guidance reads Git configuration and writes repository instruction and documentation files
- compatibility: `CONDITIONAL`; narrow composable patterns are useful but issue-tracker and documentation setup overlaps accepted GAME governance
- recommendation: `ADAPT`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-03--mattpocockskills`
- evidence limitation: Prompt-driven behavior was inspected as text and not executed.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-04 — garrytan/gstack

- URL: https://github.com/garrytan/gstack
- bounded evaluation purpose: Assess multi-role software workflow concepts and review boundaries.
- assessment: `EVALUATED`
- evaluated reference: `008dd65b1fc3df8af618408f5aea37a24dcea411`
- immutable reference: https://github.com/garrytan/gstack/commit/008dd65b1fc3df8af618408f5aea37a24dcea411
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `HIGH INTEGRATION SURFACE`; browser automation, network/tunnel packages, telemetry, setup scripts, filesystem writes, deployment and credential-adjacent workflows are visible; no root SECURITY policy found
- compatibility: `CONDITIONAL FOR CONCEPTS ONLY`; full installation is Claude/Bun-centered and conflicts with runtime neutrality and existing authority boundaries
- recommendation: `REFERENCE`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-04--garrytangstack`
- evidence limitation: Large repository; evaluation covers registered workflow purpose and material entry surfaces, not every executable path.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-05 — nextlevelbuilder/ui-ux-pro-max-skill

- URL: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- bounded evaluation purpose: Assess future UI/UX review heuristics for possible adaptation under a separate task.
- assessment: `EVALUATED`
- evaluated reference: `a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5`
- immutable reference: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/commit/a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; SECURITY policy covers installer/search-script risks; npm CLI and Python scripts create a supply-chain and write surface
- compatibility: `UNRESOLVED FOR CURRENT PROJECT STAGE`; project prerequisite remains unresolved because GAME has defined neither a UI target nor an engine, platform, or production UI direction
- recommendation: `DEFER`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-05--nextlevelbuilderui-ux-pro-max-skill`
- evidence limitation: Design-quality claims were not benchmarked and executable components were not run.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-06 — Egonex-AI/Understand-Anything

- URL: https://github.com/Egonex-AI/Understand-Anything
- bounded evaluation purpose: Assess repository-understanding concepts and traceability support without executing external code.
- assessment: `EVALUATED`
- evaluated reference: `32944829e7a63a9fa9c55d811d7f98a9530c6a6a`
- immutable reference: https://github.com/Egonex-AI/Understand-Anything/commit/32944829e7a63a9fa9c55d811d7f98a9530c6a6a
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; SECURITY policy states local project reads and `.ua/` writes; installer clones and creates links; analysis uses LLM and static-analysis dependencies
- compatibility: `UNRESOLVED`; traceability is relevant but whole-repository analysis, token use, data exposure, and generated state need a separate privacy and architecture decision
- recommendation: `DEFER`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-06--egonex-aiunderstand-anything`
- evidence limitation: Local-only and no-phone-home statements are maintainer claims not independently execution-tested here.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-07 — addyosmani/agent-skills

- URL: https://github.com/addyosmani/agent-skills
- bounded evaluation purpose: Assess documented engineering-agent practices and quality gates.
- assessment: `EVALUATED`
- evaluated reference: `df1edb2e05487d0aa6d93c747141e0aed1187f25`
- immutable reference: https://github.com/addyosmani/agent-skills/commit/df1edb2e05487d0aa6d93c747141e0aed1187f25
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; no SECURITY policy found; session-start hook, shell scripts, command definitions, and declared read/write capability are present
- compatibility: `CONDITIONAL`; quality-gate patterns are useful but substantially overlap current contracts, QA, handoff, and review roles
- recommendation: `ADAPT`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-07--addyosmaniagent-skills`
- evidence limitation: No hook, command, or evaluation fixture was executed.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-08 — bojieli/ai-agent-book

- URL: https://github.com/bojieli/ai-agent-book
- bounded evaluation purpose: Assess conceptual references for agent architecture and coordination terminology.
- assessment: `EVALUATED`
- evaluated reference: `4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94`
- immutable reference: https://github.com/bojieli/ai-agent-book/commit/4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94
- license: `APACHE-2.0 VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; no SECURITY policy found; the repository includes many executable experiments, dependencies, provider endpoints, and API-key configuration examples
- compatibility: `PASS FOR CONCEPTUAL REFERENCE`; executable experiments are outside the registered need and runtime-neutral boundary
- recommendation: `REFERENCE`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-08--bojieliai-agent-book`
- evidence limitation: The book and experiments are large and multilingual; no factual or technical claim from the book is adopted as project truth by this evaluation.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-09 — msitarzewski/agency-agents

- URL: https://github.com/msitarzewski/agency-agents
- bounded evaluation purpose: Assess role-profile patterns while preserving GAME AI Studio authority and runtime neutrality.
- assessment: `EVALUATED`
- evaluated reference: `ebe9c99acb5c96f9468de368d8bead775387d1a7`
- immutable reference: https://github.com/msitarzewski/agency-agents/commit/ebe9c99acb5c96f9468de368d8bead775387d1a7
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `CONDITIONAL`; SECURITY policy distinguishes Markdown profiles from executable installation/conversion scripts and warns about prompt injection
- compatibility: `CONDITIONAL FOR REFERENCE ONLY`; numerous role personas overlap the six accepted logical profiles and cannot override Studio topology or authority
- recommendation: `REFERENCE`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-09--msitarzewskiagency-agents`
- evidence limitation: Individual profile quality was sampled only for structural relevance; the full roster was not behavior-tested.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## CANDIDATE-10 — santifer/career-ops

- URL: https://github.com/santifer/career-ops
- bounded evaluation purpose: Assess operational documentation patterns that may improve task continuity and evidence visibility.
- assessment: `EVALUATED`
- evaluated reference: `22cbe88e0a39394020a334901c0ce37b0faedfcb`
- immutable reference: https://github.com/santifer/career-ops/commit/22cbe88e0a39394020a334901c0ce37b0faedfcb
- license: `MIT VERIFIED AT EVALUATED REFERENCE`
- security: `HIGH DATA AND EXECUTION SURFACE`; SECURITY policy covers scripts, dashboard and templates; npm postinstall downloads Chromium and workflows process personal CV/job data and network sources
- compatibility: `FAIL FOR REGISTERED PURPOSE`; the job-search domain is remote from game-studio task continuity and existing memory/handoff protocols already cover the bounded need
- recommendation: `REJECT`
- report anchor: `studio/EXTERNAL_CAPABILITY_EVALUATION.md#candidate-10--santifercareer-ops`
- evidence limitation: Rejection is scoped to GAME AI Studio's registered continuity purpose, not a general quality judgment about the project.
- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`

## 2. Evaluation and stop rules

- Popularity, stars, marketing claims, and self-reported safety are not acceptance evidence.
- STUDIO-006 used public read-only GitHub repository, tree, file, commit, and advisory views at the references above.
- No candidate was cloned, downloaded as a repository/archive, installed, imported, vendored, executed, enabled, or granted authority.
- A zero published-advisory observation on the evaluation date is not proof of safety.
- `ADOPT` or `ADAPT` recommendations do not authorize implementation. Any implementation requires a separate accepted contract, exact scope, security/license controls, tests, rollback, review, and Studio Owner approval.
