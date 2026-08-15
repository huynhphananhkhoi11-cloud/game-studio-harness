# STUDIO-006 — External Capability Evaluation

## 1. Identity, baseline, and decision boundary

- Task: `STUDIO-006`
- Contract: `tasks/STUDIO-006.md`
- Contract merge: Pull Request `#11`, merge commit `0e2d7bab5c7c876338a246be16d46a8f1073b95c`
- Evaluation branch: `agent/studio-006-evaluation`
- Evaluation date: `2026-08-15`
- Candidate count: exactly `10`
- External installation state: `NOT INSTALLED`
- External adoption state: `NO DECISION`

This report provides non-binding evidence and recommendations for a future Studio Owner decision. It does not install, adopt, import, copy, vendor, execute, enable, or grant authority to any candidate. An `ADOPT` or `ADAPT` recommendation would still require a separate accepted implementation contract.

## 2. Method and read-only boundary

The evaluation used public GitHub repository metadata, immutable commit pages, commit-addressed file views, commit-addressed recursive tree views, license files, security policies, manifests, installation scripts, hooks, and the public repository-advisory API. Candidate code, hooks, installers, examples, and tests were not run. Candidate repositories and archives were not cloned or downloaded.

For each candidate, the evaluation:

1. resolved the default branch to one full commit SHA on `2026-08-15`;
2. inspected the repository tree at that SHA;
3. inspected the README, license boundary, security-policy presence, material manifests, installers, hooks, and executable entry surfaces relevant to the registered purpose;
4. recorded maintenance as a dated observation, not a quality proxy;
5. assessed all eleven dimensions from the contract; and
6. assigned exactly one of `ADOPT`, `ADAPT`, `REFERENCE`, `DEFER`, or `REJECT`.

The public advisory API returned zero published repository advisories for each candidate when inspected on `2026-08-15`. This is only an observation about that endpoint at that time. It is not proof that a repository is secure, vulnerability-free, comprehensively audited, or safe to execute.

### Author-side validation boundary

The existing `scripts/validate_project_studio.py` is a STUDIO-005 baseline guard. Its candidate-state rules deliberately require the original register values `UNASSESSED`, `NOT REVIEWED`, `NONE`, and `UNRESOLVED`; applying those assertions to this evaluated register would directly contradict the approved STUDIO-006 deliverables. The validator and complete 71-test suite were therefore run against an isolated archive of immutable `origin/main`, where their STUDIO-005 baseline and fixture assertions remain applicable. The changed STUDIO-006 register and report were checked separately for the fixed ten-candidate set, canonical URL identity, full immutable references, eleven dimensions, recommendation vocabulary, evidence limitations, and the preserved `NOT INSTALLED` and `NO DECISION` states. Five validator-fixture tests that copy the evaluated register and then demand the STUDIO-005 state are not applicable to this STUDIO-006 transition. This applicability distinction follows Sections 12 and 13 of `tasks/STUDIO-006.md`; it does not weaken or modify the protected validator or tests.

## 3. Recommendation summary

| Group | Candidates | Meaning |
| --- | --- | --- |
| Selective adaptation worth a later contract | `CANDIDATE-01`, `CANDIDATE-03`, `CANDIDATE-07` | Borrow narrowly bounded workflow or quality-gate patterns; do not install wholesale. |
| Conceptual reference only | `CANDIDATE-02`, `CANDIDATE-04`, `CANDIDATE-08`, `CANDIDATE-09` | Cite or learn from the material without importing its runtime, role authority, or executable surface. |
| Revisit after project prerequisites exist | `CANDIDATE-05`, `CANDIDATE-06` | Potential value exists, but current UI, privacy, architecture, and integration decisions are insufficient. |
| Unsuitable for the registered purpose | `CANDIDATE-10` | Domain distance and data/execution surface exceed the limited continuity value. |

No candidate is recommended for immediate installation or adoption.

## CANDIDATE-01 — obra/superpowers

### Evidence snapshot

- Identity and immutable reference: [`obra/superpowers@b36e0829c6d0140e93cfef2ca599b1b07d4a7797`](https://github.com/obra/superpowers/commit/b36e0829c6d0140e93cfef2ca599b1b07d4a7797), default-branch commit dated `2026-08-12T16:53:21Z`.
- Function: the [commit-addressed README](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md) describes a composable planning, specification, TDD, debugging, review, worktree, and subagent methodology across multiple agent harnesses.
- License: the [MIT license](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/LICENSE) permits use and modification subject to its notice and disclaimer.
- Execution surface: [`hooks/hooks.json`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/hooks.json) registers a synchronous session-start command, and [`hooks/session-start`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/session-start) injects skill instructions into session context. The [package manifest](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/package.json) declares runtime bootstrap and agent integrations.
- Security evidence: no `SECURITY` file was found in the [immutable tree](https://api.github.com/repos/obra/superpowers/git/trees/b36e0829c6d0140e93cfef2ca599b1b07d4a7797?recursive=1); [published advisory query](https://api.github.com/repos/obra/superpowers/security-advisories?state=published&per_page=100) returned zero on the evaluation date.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS` | Planning, TDD, debugging, verification, review, and branch-completion patterns directly match the registered purpose. |
| Functional overlap | `CONDITIONAL` | Much of the workflow overlaps accepted contracts, memory, QA, handoff, and review processes. |
| Authority compatibility | `CONDITIONAL` | Automatic bootstrap language and self-triggering workflow instructions cannot override `AGENTS.md` or Studio Owner authority. |
| Runtime neutrality | `CONDITIONAL` | Multiple harnesses are supported, but installation and hook behavior remain harness-specific. |
| License | `PASS` | MIT verified at the evaluated commit. |
| Security | `CONDITIONAL` | Session hooks execute commands and inject context; no repository security policy was found. |
| Maintenance | `PASS` | The evaluated default-branch commit was three days old at evaluation; recency is not treated as quality. |
| Integration cost | `HIGH` | Wholesale use would duplicate governance and require resolving hooks, naming, review flow, and branch authority. |
| Data and privacy | `CONDITIONAL` | Skills operate on repository/session context; optional visual or external integrations require separate review. |
| Reversibility | `PASS FOR TEXTUAL ADAPTATION` | A separately written bounded checklist can be removed without making project truth depend on the candidate. |
| Net value | `POSITIVE IF NARROWLY BOUNDED` | Selected verification and debugging patterns add value; full bootstrap does not. |

Recommendation: `ADAPT` selected planning, debugging, verification, and review ideas only under a later exact-scope contract. Confidence: `HIGH`. Limitation: static inspection did not execute hooks or test cross-harness behavior.

## CANDIDATE-02 — anthropics/skills

### Evidence snapshot

- Identity and immutable reference: [`anthropics/skills@f6656c1256d5a8adfa37db9110046ef20bac644c`](https://github.com/anthropics/skills/commit/f6656c1256d5a8adfa37db9110046ef20bac644c), commit dated `2026-08-13T18:09:54Z`.
- Function: the [README](https://github.com/anthropics/skills/blob/f6656c1256d5a8adfa37db9110046ef20bac644c/README.md) defines self-contained skill folders with `SKILL.md`, scripts, and resources, while the [template](https://github.com/anthropics/skills/blob/f6656c1256d5a8adfa37db9110046ef20bac644c/template/SKILL.md) shows minimal frontmatter. The repository points the normative specification to an external site from its [spec stub](https://github.com/anthropics/skills/blob/f6656c1256d5a8adfa37db9110046ef20bac644c/spec/agent-skills-spec.md).
- License: licensing is not uniform. An example skill contains [Apache-2.0](https://github.com/anthropics/skills/blob/f6656c1256d5a8adfa37db9110046ef20bac644c/skills/algorithmic-art/LICENSE.txt), while the document skill contains [source-available restrictions](https://github.com/anthropics/skills/blob/f6656c1256d5a8adfa37db9110046ef20bac644c/skills/docx/LICENSE.txt).
- Execution surface: the [immutable tree](https://api.github.com/repos/anthropics/skills/git/trees/f6656c1256d5a8adfa37db9110046ef20bac644c?recursive=1) contains Python, shell, JavaScript, requirements files, document-processing tools, web testing, and artifact-building scripts.
- Security evidence: no repository `SECURITY` file was found in that tree; [published advisory query](https://api.github.com/repos/anthropics/skills/security-advisories?state=published&per_page=100) returned zero on the evaluation date.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS` | Self-contained folders, metadata, instructions, scripts, and resources are directly relevant to skill-package structure. |
| Functional overlap | `CONDITIONAL` | GAME already has repository and platform skills; the value is pattern comparison rather than another catalog. |
| Authority compatibility | `CONDITIONAL` | Skill instructions remain subordinate; production Claude implementation details cannot become repository governance. |
| Runtime neutrality | `FAIL FOR WHOLESALE USE` | The repository explicitly demonstrates Anthropic/Claude skills, even though the structural pattern is portable. |
| License | `CONDITIONAL` | Per-folder review is mandatory because Apache and restrictive source-available terms coexist. |
| Security | `CONDITIONAL` | Executable scripts exist and no repository security policy was found. |
| Maintenance | `PASS` | The evaluated commit was recent; external specification drift remains possible. |
| Integration cost | `MEDIUM TO HIGH` | Per-skill license, dependency, instruction, and script review would be required. |
| Data and privacy | `CONDITIONAL` | Document and web skills may process user files or external services; behavior differs by skill. |
| Reversibility | `PASS FOR REFERENCE` | Structural lessons can be cited without copying restricted material. |
| Net value | `POSITIVE AS REFERENCE` | The minimal schema and packaging pattern are useful; mixed licensing blocks blanket reuse. |

Recommendation: `REFERENCE` the package anatomy and specification concepts only. Confidence: `HIGH`. Limitation: no blanket license conclusion applies across the repository.

## CANDIDATE-03 — mattpocock/skills

### Evidence snapshot

- Identity and immutable reference: [`mattpocock/skills@8b78b531ab965735c5dc74f6f7a219e1e37326df`](https://github.com/mattpocock/skills/commit/8b78b531ab965735c5dc74f6f7a219e1e37326df), commit dated `2026-08-13T09:06:21Z`.
- Function: the [README](https://github.com/mattpocock/skills/blob/8b78b531ab965735c5dc74f6f7a219e1e37326df/README.md) emphasizes small, composable, model-neutral engineering skills, including handoff, triage, review, research, TDD, and documentation.
- License: [MIT](https://github.com/mattpocock/skills/blob/8b78b531ab965735c5dc74f6f7a219e1e37326df/LICENSE).
- Execution/write surface: the [package manifest](https://github.com/mattpocock/skills/blob/8b78b531ab965735c5dc74f6f7a219e1e37326df/package.json) has development tooling; the [setup skill](https://github.com/mattpocock/skills/blob/8b78b531ab965735c5dc74f6f7a219e1e37326df/skills/engineering/setup-matt-pocock-skills/SKILL.md) reads Git and instruction files, asks configuration questions, and writes repository docs and agent instructions.
- Security evidence: no `SECURITY` file was found in the [immutable tree](https://api.github.com/repos/mattpocock/skills/git/trees/8b78b531ab965735c5dc74f6f7a219e1e37326df?recursive=1); [published advisory query](https://api.github.com/repos/mattpocock/skills/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS` | Narrow handoff, triage, research, and review skills match the registered purpose. |
| Functional overlap | `CONDITIONAL` | Handoff, task state, issue handling, and ADR practices overlap accepted studio protocols. |
| Authority compatibility | `CONDITIONAL` | Setup can edit AGENTS/CLAUDE and repository docs; those writes require GAME-specific authority. |
| Runtime neutrality | `PASS AT CONCEPT LEVEL` | README claims model portability, while packaging still includes Claude and agent-specific paths. |
| License | `PASS` | MIT verified. |
| Security | `CONDITIONAL` | No policy found; some skills include shell scripts and Git/issue operations. |
| Maintenance | `PASS` | Recent evaluated commit and explicit versioned package metadata. |
| Integration cost | `MEDIUM` | Selective rewriting can fit current conventions; wholesale setup would collide with existing files. |
| Data and privacy | `CONDITIONAL` | Research and issue-tracker skills may access repository and external tracker data. |
| Reversibility | `PASS` | Bounded rewritten patterns can remain independent of the source runtime. |
| Net value | `POSITIVE IF SELECTIVE` | Small-skill design and explicit handoff prompts can improve clarity without replacing governance. |

Recommendation: `ADAPT` selected narrow handoff, triage, and code-review patterns after removing repository-writing assumptions. Confidence: `HIGH`. Limitation: prompt behavior was not executed.

## CANDIDATE-04 — garrytan/gstack

### Evidence snapshot

- Identity and immutable reference: [`garrytan/gstack@008dd65b1fc3df8af618408f5aea37a24dcea411`](https://github.com/garrytan/gstack/commit/008dd65b1fc3df8af618408f5aea37a24dcea411), commit dated `2026-08-15T05:02:07Z`.
- Function: the [README](https://github.com/garrytan/gstack/blob/008dd65b1fc3df8af618408f5aea37a24dcea411/README.md) presents a Claude Code-centered virtual software team with planning, design, review, QA, browser, security, release, and deployment roles.
- License: [MIT](https://github.com/garrytan/gstack/blob/008dd65b1fc3df8af618408f5aea37a24dcea411/LICENSE).
- Execution surface: the [manifest](https://github.com/garrytan/gstack/blob/008dd65b1fc3df8af618408f5aea37a24dcea411/package.json) requires Bun and includes browser automation, Puppeteer, Playwright, SOCKS, ngrok, model SDKs, and many executable scripts. The [setup script](https://github.com/garrytan/gstack/blob/008dd65b1fc3df8af618408f5aea37a24dcea411/setup) builds binaries, links or copies skills, writes host directories, and supports team auto-update behavior.
- Security evidence: the repository contains extensive security-related code and tests but no root `SECURITY` policy in the [immutable tree](https://api.github.com/repos/garrytan/gstack/git/trees/008dd65b1fc3df8af618408f5aea37a24dcea411?recursive=1); [published advisory query](https://api.github.com/repos/garrytan/gstack/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS FOR CONCEPTS` | Role-separated planning, review, QA, security, and release concepts match the registered purpose. |
| Functional overlap | `HIGH` | The virtual team substantially duplicates Studio topology, six logical profiles, QA, review, memory, and handoff. |
| Authority compatibility | `FAIL FOR WHOLESALE USE` | Setup and skills can alter instructions, commit, ship, deploy, browse, and auto-update beyond the accepted authority model. |
| Runtime neutrality | `FAIL` | Primary workflow is Claude Code and Bun centered despite some Codex support. |
| License | `PASS` | MIT verified. |
| Security | `CONDITIONAL/HIGH SURFACE` | Browser, tunnels, telemetry, network, binaries, filesystem writes, and credential-adjacent deployment features materially increase risk. |
| Maintenance | `PASS` | Active at evaluation, but breadth and fast change increase review burden. |
| Integration cost | `VERY HIGH` | Governance conflict resolution, dependency review, browser isolation, secrets policy, and training would be substantial. |
| Data and privacy | `HIGH RISK WITHOUT CONTROLS` | Browser sessions, cookies, repository context, telemetry, tunnels, and deployment connections may expose sensitive state. |
| Reversibility | `CONDITIONAL` | Conceptual reference is reversible; team-mode hooks and generated state would be harder to remove safely. |
| Net value | `LOW FOR INSTALLATION; MODERATE FOR REFERENCE` | Concepts are useful, but full-stack duplication and risk exceed benefit. |

Recommendation: `REFERENCE` role boundaries and review questions only; do not install or reproduce the stack. Confidence: `HIGH`. Limitation: the large executable surface was scoped to material entry points, not exhaustively audited.

## CANDIDATE-05 — nextlevelbuilder/ui-ux-pro-max-skill

### Evidence snapshot

- Identity and immutable reference: [`nextlevelbuilder/ui-ux-pro-max-skill@a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/commit/a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5), commit dated `2026-08-13T17:08:23Z`.
- Function: the [README](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5/README.md) describes searchable UI styles, design-system reasoning, accessibility checks, stack guidance, Python search tools, and a multi-agent CLI installer.
- License: [MIT](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5/LICENSE).
- Execution surface: the [CLI manifest](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5/cli/package.json) declares an npm binary, dependencies, Python validation, shell smoke tests, TypeScript build, and Playwright development tests.
- Security evidence: [SECURITY.md](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5/SECURITY.md) explicitly covers arbitrary execution, path traversal, unsafe writes, and npm supply-chain issues; [published advisory query](https://api.github.com/repos/nextlevelbuilder/ui-ux-pro-max-skill/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS FOR FUTURE UI REVIEW` | Accessibility, layout, interaction, and design-system heuristics could support a later UI task. |
| Functional overlap | `LOW TO MEDIUM` | Current GAME governance has no equivalent design catalog, but no production UI decision exists. |
| Authority compatibility | `CONDITIONAL` | Recommendations must remain advisory and cannot select a framework, visual canon, or platform. |
| Runtime neutrality | `CONDITIONAL` | The content supports several agents, but CLI paths and stack guidance are runtime/tool specific. |
| License | `PASS` | MIT verified. |
| Security | `CONDITIONAL` | A meaningful policy exists; installer and search scripts still require code and supply-chain review. |
| Maintenance | `PASS` | Recent commit and declared release/security support for latest version only. |
| Integration cost | `MEDIUM` | Static heuristics could be extracted later; CLI adoption adds Node/Python and file-write surfaces. |
| Data and privacy | `LOW FOR STATIC REFERENCE; CONDITIONAL FOR CLI` | Static catalog reading is bounded; generators and external font/icon refresh flows may use network or project data. |
| Reversibility | `PASS FOR CHECKLIST ADAPTATION` | A later project-owned checklist could be removed or replaced. |
| Net value | `UNRESOLVED NOW` | Value depends on a future platform, art direction, accessibility target, and UI production need. |

Recommendation: `DEFER` until a UI/UX production contract defines platform, stack, art direction, and acceptance criteria. Confidence: `HIGH`. Limitation: no design-output benchmark was performed.

## CANDIDATE-06 — Egonex-AI/Understand-Anything

### Evidence snapshot

- Identity and immutable reference: [`Egonex-AI/Understand-Anything@32944829e7a63a9fa9c55d811d7f98a9530c6a6a`](https://github.com/Egonex-AI/Understand-Anything/commit/32944829e7a63a9fa9c55d811d7f98a9530c6a6a), commit dated `2026-08-11T14:13:36Z`.
- Function: the [README](https://github.com/Egonex-AI/Understand-Anything/blob/32944829e7a63a9fa9c55d811d7f98a9530c6a6a/README.md) describes multi-agent repository analysis, static parsing, knowledge graphs, search, tours, and diff impact analysis. It states that the graph is written under `.ua/` or a legacy project directory.
- License: [MIT](https://github.com/Egonex-AI/Understand-Anything/blob/32944829e7a63a9fa9c55d811d7f98a9530c6a6a/LICENSE).
- Execution surface: the [manifest](https://github.com/Egonex-AI/Understand-Anything/blob/32944829e7a63a9fa9c55d811d7f98a9530c6a6a/package.json) uses pnpm, TypeScript, tree-sitter builds, and dashboard packages. The [PowerShell installer](https://github.com/Egonex-AI/Understand-Anything/blob/32944829e7a63a9fa9c55d811d7f98a9530c6a6a/install.ps1) clones or updates the repository and writes user skill links/junctions.
- Security evidence: [SECURITY.md](https://github.com/Egonex-AI/Understand-Anything/blob/32944829e7a63a9fa9c55d811d7f98a9530c6a6a/SECURITY.md) states local project reads and graph writes, no phone-home behavior, and dashboard path controls; [published advisory query](https://api.github.com/repos/Egonex-AI/Understand-Anything/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS` | Graph and impact-analysis concepts could improve repository understanding and traceability. |
| Functional overlap | `CONDITIONAL` | Existing artifact maps and memory already provide human-auditable traceability without code analysis. |
| Authority compatibility | `CONDITIONAL` | Generated summaries and graphs are derived evidence, not project authority or truth. |
| Runtime neutrality | `CONDITIONAL` | Multiple agents and local models are mentioned, but LLM analysis and plugin integration remain runtime-dependent. |
| License | `PASS` | MIT verified. |
| Security | `CONDITIONAL/HIGH READ SCOPE` | The tool reads the codebase, writes generated state, runs parsers/dashboard code, and may invoke LLM providers. |
| Maintenance | `PASS` | Active at evaluation; architecture and data formats may still evolve. |
| Integration cost | `HIGH` | Requires dependency, generated-artifact, privacy, token-cost, ignore-policy, and truth-authority decisions. |
| Data and privacy | `HIGH DECISION NEED` | Whole-repository content may be processed by a configured model; local mode reduces but does not eliminate operational review. |
| Reversibility | `CONDITIONAL` | `.ua/` state can likely be removed, but workflows may become dependent on generated graphs. |
| Net value | `UNRESOLVED` | Current repository size and existing maps do not yet justify the surface. |

Recommendation: `DEFER` until repository scale and a separate privacy/architecture contract justify a controlled pilot. Confidence: `HIGH`. Limitation: maintainer security claims were not execution-tested.

## CANDIDATE-07 — addyosmani/agent-skills

### Evidence snapshot

- Identity and immutable reference: [`addyosmani/agent-skills@df1edb2e05487d0aa6d93c747141e0aed1187f25`](https://github.com/addyosmani/agent-skills/commit/df1edb2e05487d0aa6d93c747141e0aed1187f25), commit dated `2026-08-14T18:50:27Z`.
- Function: the [README](https://github.com/addyosmani/agent-skills/blob/df1edb2e05487d0aa6d93c747141e0aed1187f25/README.md) maps specifications, planning, incremental implementation, testing, review, performance, simplification, and shipping to skills and commands.
- License: [MIT](https://github.com/addyosmani/agent-skills/blob/df1edb2e05487d0aa6d93c747141e0aed1187f25/LICENSE).
- Execution surface: [`hooks/hooks.json`](https://github.com/addyosmani/agent-skills/blob/df1edb2e05487d0aa6d93c747141e0aed1187f25/hooks/hooks.json) registers a session-start shell command. The [Codex plugin manifest](https://github.com/addyosmani/agent-skills/blob/df1edb2e05487d0aa6d93c747141e0aed1187f25/.codex-plugin/plugin.json) declares interactive read/write capability and a full spec-to-ship workflow.
- Security evidence: no repository `SECURITY` policy was found in the [immutable tree](https://api.github.com/repos/addyosmani/agent-skills/git/trees/df1edb2e05487d0aa6d93c747141e0aed1187f25?recursive=1); [published advisory query](https://api.github.com/repos/addyosmani/agent-skills/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS` | Engineering quality gates and lifecycle practices directly match the registered purpose. |
| Functional overlap | `HIGH` | Specifications, plans, tests, QA, review, and shipping overlap existing Studio profiles and protocols. |
| Authority compatibility | `CONDITIONAL` | Automatic skill routing and ship commands cannot self-authorize changes or merge. |
| Runtime neutrality | `CONDITIONAL` | Many platforms are documented, but plugin/hook mechanisms differ and some integrations copy instructions. |
| License | `PASS` | MIT verified. |
| Security | `CONDITIONAL` | Session hook, shell scripts, command definitions, and read/write capability require review; no policy found. |
| Maintenance | `PASS` | Recent evaluated commit and explicit plugin version. |
| Integration cost | `MEDIUM TO HIGH` | Selected checklist adaptation is manageable; whole lifecycle integration would duplicate governance. |
| Data and privacy | `CONDITIONAL` | Browser, source-driven research, and repository-write skills can access code and external resources. |
| Reversibility | `PASS FOR ADAPTED CHECKLISTS` | Project-owned quality gates can remain detached from the source plugin. |
| Net value | `POSITIVE IF NARROW` | Security, observability, definition-of-done, and review patterns can strengthen existing gates. |

Recommendation: `ADAPT` selected quality-gate and checklist concepts under existing QA and review authority. Confidence: `HIGH`. Limitation: hooks, commands, and eval fixtures were not executed.

## CANDIDATE-08 — bojieli/ai-agent-book

### Evidence snapshot

- Identity and immutable reference: [`bojieli/ai-agent-book@4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94`](https://github.com/bojieli/ai-agent-book/commit/4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94), commit dated `2026-08-15T12:26:36Z`.
- Function: the [README](https://github.com/bojieli/ai-agent-book/blob/4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94/README.md) presents ten chapters and many experiments covering context, memory, tools, coding agents, interaction, evaluation, planning, multi-agent systems, and applications.
- License: [Apache-2.0](https://github.com/bojieli/ai-agent-book/blob/4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94/LICENSE).
- Execution surface: the [immutable tree](https://api.github.com/repos/bojieli/ai-agent-book/git/trees/4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94?recursive=1) contains thousands of book, build, experiment, dependency, and provider files. [`.env.example`](https://github.com/bojieli/ai-agent-book/blob/4c16eb47b9c1ae2b3e1b5db44f51ffd130f06b94/.env.example) documents local and remote model providers plus multiple API-key variables.
- Security evidence: no repository `SECURITY` policy was found in the immutable tree; [published advisory query](https://api.github.com/repos/bojieli/ai-agent-book/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS FOR CONCEPTS` | Context, memory, tools, planning, multi-agent coordination, and evaluation are relevant reference subjects. |
| Functional overlap | `CONDITIONAL` | GAME already defines operational versions of several concepts; the book may add terminology and alternatives. |
| Authority compatibility | `PASS FOR REFERENCE` | Educational claims remain sources to assess, not governance or decisions. |
| Runtime neutrality | `PASS FOR TEXT; FAIL FOR MANY EXPERIMENTS` | Concepts span providers, while experiments require specific languages, models, endpoints, or keys. |
| License | `PASS` | Apache-2.0 verified. |
| Security | `CONDITIONAL` | Large executable experiment surface and provider-key configuration; no security policy found. |
| Maintenance | `PASS` | Active and multilingual at evaluation; translations may lag the source language. |
| Integration cost | `LOW FOR CITATION; VERY HIGH FOR CODE` | Reading selected chapters is low cost; adopting experiments would require separate evaluation. |
| Data and privacy | `LOW FOR STATIC READING; HIGHER FOR EXPERIMENTS` | Remote-provider experiments may transmit prompts/data and require credentials. |
| Reversibility | `PASS` | Citations do not create runtime dependency. |
| Net value | `POSITIVE AS REFERENCE` | Useful conceptual map without needing executable adoption. |

Recommendation: `REFERENCE` selected conceptual chapters and terminology only. Confidence: `HIGH`. Limitation: the evaluation does not validate the book's technical claims or translations and does not authorize experiments.

## CANDIDATE-09 — msitarzewski/agency-agents

### Evidence snapshot

- Identity and immutable reference: [`msitarzewski/agency-agents@ebe9c99acb5c96f9468de368d8bead775387d1a7`](https://github.com/msitarzewski/agency-agents/commit/ebe9c99acb5c96f9468de368d8bead775387d1a7), commit dated `2026-08-06T13:29:46Z`.
- Function: the [README](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/README.md) describes a large roster of specialized, personality-driven, deliverable-focused role profiles, including game-development roles and integrations for many agent tools.
- License: [MIT](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/LICENSE).
- Execution surface: the [installer](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/install.sh) copies or links generated profiles to user and project configuration directories for many tools; conversion and memory-integration scripts also exist.
- Security evidence: [SECURITY.md](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/SECURITY.md) distinguishes Markdown prompts from executable shell scripts and asks reviewers to check prompt injection; [published advisory query](https://api.github.com/repos/msitarzewski/agency-agents/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `PASS FOR ROLE-PROFILE STUDY` | Role identity, mission, deliverable, and success-metric patterns match the registered purpose. |
| Functional overlap | `VERY HIGH` | The large roster overlaps Studio topology, logical profiles, Guild concepts, and task Cells. |
| Authority compatibility | `CONDITIONAL` | Persona instructions cannot create roles, permissions, canon, or approval gates in GAME. |
| Runtime neutrality | `CONDITIONAL` | Many tools are supported through generated integrations, but each installation target has different semantics. |
| License | `PASS` | MIT verified. |
| Security | `CONDITIONAL` | Markdown is non-executable, but prompt injection and install/convert scripts remain material risks. |
| Maintenance | `PASS` | Active at evaluation with a very large and growing roster. |
| Integration cost | `HIGH` | Mapping hundreds of profiles to six logical roles and removing conflicting authority would be costly. |
| Data and privacy | `LOW FOR STATIC READING; CONDITIONAL FOR INTEGRATIONS` | Profile reading is bounded; memory and tool integrations may write user/project configuration. |
| Reversibility | `PASS FOR REFERENCE` | Structural ideas can be cited without installing profiles. |
| Net value | `MODERATE AS REFERENCE` | Profile anatomy is useful; importing the roster would add duplication and ambiguity. |

Recommendation: `REFERENCE` role-profile anatomy and selected game-role examples only. Confidence: `HIGH`. Limitation: this is not a quality review of every profile.

## CANDIDATE-10 — santifer/career-ops

### Evidence snapshot

- Identity and immutable reference: [`santifer/career-ops@22cbe88e0a39394020a334901c0ce37b0faedfcb`](https://github.com/santifer/career-ops/commit/22cbe88e0a39394020a334901c0ce37b0faedfcb), commit dated `2026-08-15T07:32:00Z`.
- Function: the [README](https://github.com/santifer/career-ops/blob/22cbe88e0a39394020a334901c0ce37b0faedfcb/README.md) describes an AI job-search system for offer evaluation, CV generation, portal scanning, batch processing, tracking, company research, and application assistance.
- License: [MIT](https://github.com/santifer/career-ops/blob/22cbe88e0a39394020a334901c0ce37b0faedfcb/LICENSE).
- Execution surface: the [manifest](https://github.com/santifer/career-ops/blob/22cbe88e0a39394020a334901c0ce37b0faedfcb/package.json) exposes many Node commands, network/model dependencies, browser automation, and a postinstall that downloads Chromium with system dependencies. The [setup guide](https://github.com/santifer/career-ops/blob/22cbe88e0a39394020a334901c0ce37b0faedfcb/docs/SETUP.md) clones the project, installs dependencies, ingests CV/profile details, scans job sites, writes reports/PDFs, and tracks applications.
- Security evidence: [SECURITY.md](https://github.com/santifer/career-ops/blob/22cbe88e0a39394020a334901c0ce37b0faedfcb/SECURITY.md) covers command injection, traversal, SSRF, dashboard, templates, configuration, and secrets; [published advisory query](https://api.github.com/repos/santifer/career-ops/security-advisories?state=published&per_page=100) returned zero.

### Dimension findings

| Dimension | Result | Finding |
| --- | --- | --- |
| Bounded relevance | `FAIL` | Job-search operations are remote from game-studio continuity; only generic tracking/documentation ideas overlap. |
| Functional overlap | `HIGH FOR THE LIMITED VALUE` | Memory, worklog, resume, handoff, artifact map, and PR evidence already provide continuity. |
| Authority compatibility | `CONDITIONAL` | Its agent modes and write workflows cannot become GAME authority. |
| Runtime neutrality | `CONDITIONAL` | Many agent CLIs are supported, but Node, Go, Playwright, browser, and provider integrations are concrete runtime choices. |
| License | `PASS` | MIT verified. |
| Security | `HIGH SURFACE` | Browser automation, network sources, command scripts, provider calls, downloads, local dashboard, and PDF generation are present. |
| Maintenance | `PASS` | Active at evaluation; this does not increase relevance. |
| Integration cost | `VERY HIGH RELATIVE TO BENEFIT` | Extracting generic operations would add review burden without improving the existing protocol materially. |
| Data and privacy | `HIGH` | CVs, contact details, career preferences, job pages, tracking data, and model/browser flows are core to the product. |
| Reversibility | `CONDITIONAL` | Static documentation ideas are reversible; installed data workflows and browser dependencies are not trivial. |
| Net value | `NEGATIVE FOR REGISTERED PURPOSE` | Domain mismatch and risk exceed marginal continuity value. |

Recommendation: `REJECT` for GAME AI Studio task-continuity use. Confidence: `HIGH`. Limitation: the decision is purpose-specific and is not a general judgment of career-ops quality.

## 4. Cross-candidate comparison

### Overlap and complementary value

| Cluster | Candidates | Existing GAME capability | Evidence-based conclusion |
| --- | --- | --- | --- |
| Full development workflow | 01, 03, 04, 07 | Contracts, task scope, memory, handoff, QA, independent review, PR/Owner merge | High overlap. Prefer selected patterns from 01, 03, and 07; treat 04 as conceptual reference. |
| Skill packaging | 01, 02, 03, 05, 07 | Repository skills plus platform skill/plugin mechanisms | Candidate 02 is the clearest structural reference, but mixed licensing requires per-folder controls. |
| Role topology | 04, 09 | Six logical profiles, Project Studios, Cells, Guilds, Platform layer | Do not import parallel authority systems. Use only terminology or profile-format ideas. |
| UI/UX intelligence | 05 | No accepted production UI stack or art direction | Potentially complementary but premature; defer. |
| Repository knowledge graph | 06 | Artifact map and persistent memory | Potential future complement at larger scale, but privacy and generated-truth boundaries are unresolved. |
| Agent theory and experiments | 08 | Existing studio governance and runtime neutrality | Useful educational reference; experiments are not dependencies. |
| Operational continuity | 10 | Four-file memory package, WORKLOG, RESUME, artifact map, Git/PR evidence | Candidate is domain-mismatched and adds disproportionate personal-data and execution risk. |

### Risk and cost ordering

- Lowest-risk use: cite static concepts from candidates 02, 08, and 09 without copying or execution.
- Manageable under a later exact contract: rewrite selected patterns from candidates 01, 03, and 07 into project-owned, runtime-neutral checks.
- Requires prerequisite decisions: candidate 05 needs UI/art/platform scope; candidate 06 needs privacy, generated-artifact, model, cost, and architecture scope.
- Highest integration surface: candidates 04 and 10 because of browser/network/deployment or personal-data workflows; candidate 04 retains conceptual value, while candidate 10 does not meet its registered purpose.

### Duplication control

No candidate should introduce a second constitution, task authority, memory truth, role hierarchy, QA chain, merge authority, or automatic instruction source. Any later adaptation must map to existing canonical paths, remove self-authorizing language, preserve runtime neutrality, and remain reversible.

## 5. Residual uncertainties

- Static inspection cannot establish runtime safety, prompt compliance, absence of vulnerabilities, or behavior under adversarial repository content.
- Repository state and published advisories can change after the evaluated commits and date.
- Candidate 02 requires license review per individual skill before any copying or adaptation.
- Candidate 05 lacks an approved GAME UI platform, stack, art direction, and benchmark target.
- Candidate 06 lacks an approved privacy boundary, model/provider decision, generated-artifact policy, token budget, and pilot acceptance criteria.
- No technical claim in candidate 08's book or translations was independently adjudicated.
- No recommendation creates installation or adoption authority.

## 6. Final boundary and next decision

The evaluation is complete as research evidence only. Every candidate remains:

- installation: `NOT INSTALLED`
- adoption decision: `NO DECISION`
- repository authority: `NONE`

No candidate was cloned, downloaded as a repository/archive, installed, imported, copied, vendored, executed, enabled, or granted authority during STUDIO-006. Independent QA must verify completeness, immutable references, source traceability, recommendation vocabulary, exact file scope, and prohibited-action compliance before Review & Integration and Studio Owner merge disposition.
