STUDIO-003 — Establish Hierarchical Studio Topology
Goal
Evolve GAME AI Studio from a flat set of specialist roles into a scalable hierarchical organization that can support:
•	one parent GAME AI Studio;
•	a shared Platform Studio;
•	multiple future Project Studios;
•	dynamic cross-functional Cells;
•	Shared Expert Guilds.
The topology must remain runtime/model/provider neutral.
This task defines organizational structure only.
It does NOT install tools, connect AI providers, implement routing, select a game engine, define gameplay, or create a real game project.
Contract Status
This file is the Studio Owner-authored task contract.
Implementation agents may:
•	read this file;
•	cite this file;
•	validate their work against this file.
Implementation agents must NOT:
•	modify this file;
•	weaken its acceptance criteria;
•	expand their own scope;
•	reinterpret forbidden authority roles into equivalent new roles.
If implementation reveals a genuine problem in this task contract, report it as UNRESOLVED or propose a change to the Studio Owner.
Do not silently rewrite the task.
Context
Existing governance and operational roles already exist in:
•	AGENTS.md
•	docs/GAME_VISION.md
•	docs/DECISIONS.md
•	studio/STUDIO_CONSTITUTION.md
•	studio/ORG_CHART.md
•	studio/AGENT_REGISTRY.md
•	studio/MODEL_REGISTRY.md
•	studio/HANDOFF_PROTOCOL.md
•	studio/agents/PRODUCER-01.md
•	studio/agents/GAME-DESIGN-01.md
•	studio/agents/NARRATIVE-RESEARCH-01.md
•	studio/agents/ENGINEERING-01.md
•	studio/agents/QA-01.md
•	studio/agents/REVIEW-INTEGRATION-01.md
STUDIO-001 established shared governance.
STUDIO-002 established reusable logical agent roles.
STUDIO-003 defines how those roles can be organized at scale without permanently binding organizational roles to particular AI runtimes or models.
Architectural Principle
LARGE ORGANIZATION, SMALL ACTIVE TEAM
The studio may define many possible capabilities without activating all agents for every task.
Organizational capability does not imply permanent active workforce.
A large topology is acceptable. A large active team for every task is not.
For each task, activate only the minimum set of roles reasonably necessary to:
1.	produce the outcome;
2.	validate the outcome;
3.	satisfy risk-appropriate review requirements.
Target Topology
GAME AI STUDIO
│
├── Platform Studio
│
├── Project Studios
│   └── Dynamic Cross-Functional Cells
│
└── Shared Expert Guilds
This is the organizational topology.
It is NOT a requirement that every component be permanently staffed or active.
1. GAME AI Studio
GAME AI Studio is the parent organizational layer.
It owns studio-wide governance and shared organizational standards already established by existing governance documents.
It may contain multiple future Project Studios while allowing them to remain isolated where appropriate.
GAME AI Studio does not imply that one AI agent must control the entire organization.
The Studio Owner remains the existing final binding authority defined by current governance.
2. Platform Studio
Platform Studio provides shared capabilities that multiple Project Studios, Cells, or specialists may use.
Future capability categories MAY include:
•	runtime/model/provider registry;
•	persistent project memory;
•	task and handoff infrastructure;
•	Git/GitHub workflow;
•	architecture maps;
•	benchmarking and evaluation;
•	tools and MCP integration;
•	routing and failover;
•	shared automation;
•	common development infrastructure.
These are capability categories only.
STUDIO-003 must NOT:
•	select implementations for them;
•	install tools;
•	connect providers;
•	create API keys;
•	define runtime routing logic;
•	adopt specific dependencies.
Platform Studio is a coordination and shared-capability layer.
It is NOT a second executive authority.
3. Project Studios
A Project Studio is an organizational container for one future game or project.
A Project Studio MAY contain:
•	project-specific context;
•	project-specific tasks;
•	project-specific decisions;
•	project-specific canon;
•	project-specific architecture;
•	project-specific state;
•	project-specific Cells.
A Project Studio may use shared Platform capabilities and borrow specialists from Expert Guilds.
A Project Studio does NOT automatically create a new owner or executive role.
STUDIO-003 must not create a real Project Studio for an actual or fictional game.
Only a reusable template may be defined.
4. Dynamic Cross-Functional Cells
Cells are small working units formed around a concrete outcome.
A Cell may be formed around:
•	a feature;
•	a subsystem;
•	a milestone;
•	a content stream;
•	a research question;
•	an integration task;
•	another clearly bounded outcome.
Cells should be cross-functional when the outcome requires multiple specialties.
Examples of possible Cell labels MAY include:
•	Gameplay Cell;
•	World & Content Cell;
•	Presentation Cell;
•	Release Cell.
These are examples only. They are not mandatory permanent departments.
Cells should:
•	activate only required roles;
•	operate within accepted constraints;
•	collaborate directly where appropriate;
•	produce a bounded outcome;
•	hand off evidence/state;
•	dissolve or become inactive when no longer needed.
Detailed Cell lifecycle belongs canonically in studio/CELL_MODEL.md.
5. Shared Expert Guilds
Expert Guilds are shared capability pools for specialist expertise that does not need to be duplicated inside every Project Studio or Cell.
Possible future expertise MAY include:
•	historical research;
•	systems design;
•	architecture;
•	performance;
•	accessibility;
•	security;
•	localization;
•	specialist QA;
•	other high-skill or low-frequency capabilities.
A Guild is not automatically an active team.
A Guild may exist as an available capability while all its roles remain inactive.
Detailed Guild rules belong canonically in studio/EXPERT_GUILDS.md.
6. Existing Operational Roles
The six STUDIO-002 operational profiles remain valid:
•	Producer / Coordination
•	Game Design
•	Narrative & Research
•	Engineering
•	QA
•	Review & Integration
STUDIO-003 reorganizes how roles may be deployed.
It does not invalidate, replace, or permanently reassign those profiles.
Future additional roles may be proposed through governance when actual workload or specialization justifies them.
Do not create roles merely to imitate the organization chart of a large human company.
7. Role Independence
AGENT ROLE != RUNTIME != MODEL != PROVIDER
An organizational role must not be permanently bound to:
•	Grok;
•	Claude;
•	Copilot;
•	GPT;
•	DeepSeek;
•	Gemini;
•	any other current or future runtime/model/provider.
A suitable runtime may occupy a logical role when selected by future runtime policy.
Runtime selection and failover implementation are outside STUDIO-003.
8. Dynamic Activation
The topology must support role/cell states such as:
•	INACTIVE
•	READY
•	ACTIVE
•	BLOCKED
•	HANDOFF
•	COMPLETE
These states describe work availability or lifecycle. They do not create new authority.
The detailed activation policy belongs canonically in studio/ACTIVATION_POLICY.md.
Activate the minimum sufficient team.
Do not activate an agent merely because its department, Cell, Guild, or role exists.
9. Direct Collaboration
Specialists must not be forced to communicate through Producer for every interaction.
Direct collaboration and handoff MAY occur where appropriate, including:
•	Design ↔ Engineering;
•	Design ↔ Narrative;
•	Engineering ↔ QA;
•	Research ↔ Review;
•	other justified cross-functional interactions.
Producer maintains:
•	coordination visibility;
•	priorities;
•	dependencies;
•	blockers;
•	scheduling awareness;
•	low-risk resource coordination.
Producer is NOT:
•	a universal communication proxy;
•	a mandatory approval gate for every specialist decision;
•	a replacement for Studio Owner;
•	a source of new binding governance authority.
10. Project Isolation
The topology must allow multiple future Project Studios without silently mixing their binding state.
Project-specific items must be capable of remaining isolated, including:
•	canon;
•	project decisions;
•	project architecture;
•	tasks;
•	assumptions;
•	state;
•	constraints;
•	code or content ownership where applicable.
Shared infrastructure does not automatically make a decision from Project A binding on Project B.
Shared evidence or shared capabilities may be reused where appropriate, but reuse does not silently transfer project-specific authority.
11. Runtime Failover Compatibility
STUDIO-003 does not implement runtime failover.
However, its organizational topology must remain compatible with future failover.
If one runtime becomes:
•	exhausted;
•	rate-limited;
•	unavailable;
•	disabled;
•	unsuitable;
another suitable runtime must eventually be able to occupy the same logical role using repository-visible state.
No organizational rule may require inaccessible private chat history or private chain-of-thought from the previous runtime.
12. No Hidden Context Dependency
Organizational continuity must rely on durable project evidence such as:
•	task contracts;
•	accepted decisions;
•	repository state;
•	handoffs;
•	tests;
•	diffs;
•	documented architecture;
•	concise rationale;
•	evidence.
Do not require private chain-of-thought.
Do not make a previous AI conversation the only source of project truth.
13. Information Architecture Principle
ONE RULE → ONE CANONICAL HOME
A rule should have one primary canonical document.
Other documents should reference that rule rather than repeatedly redefine it.
Examples:
•	overall organizational relationships → studio/STUDIO_TOPOLOGY.md
•	Platform boundaries → studio/PLATFORM_STUDIO.md
•	Project Studio template → studio/PROJECT_STUDIO_TEMPLATE.md
•	Cell lifecycle → studio/CELL_MODEL.md
•	Guild behavior → studio/EXPERT_GUILDS.md
•	activation states and minimum-team logic → studio/ACTIVATION_POLICY.md
•	shared handoff rules → existing studio/HANDOFF_PROTOCOL.md
•	shared governance authority → existing studio/STUDIO_CONSTITUTION.md
Detail is welcome when it adds unique operational information.
Do not reduce useful detail merely to minimize line count.
Do not increase document length through duplicated explanations, unnecessary ceremonies, or company-like bureaucracy.
14. Authority Invariants
14.1 Binding authority
The existing role with final binding/non-reversible authority is:
•	Studio Owner
STUDIO-003 must not invent another owner-level authority.
14.2 Forbidden authority roles
The following roles must NOT exist:
•	Project Owner
•	Project Studio Owner
•	Platform Studio Owner
Do not create equivalent replacement roles under different names merely to bypass this restriction.
A Project Studio is an organizational container.
Platform Studio is a shared-capability and coordination layer.
Neither automatically creates a new executive authority.
14.3 Specialists and Cells
Specialists/Cells MAY:
•	make reversible local in-scope decisions;
•	execute within accepted constraints;
•	explore within OPEN/GUIDED scope;
•	surface blockers;
•	create proposals;
•	hand off work.
Specialists/Cells MUST NOT:
•	create binding governance decisions;
•	silently override accepted decisions;
•	silently override accepted canon;
•	grant themselves broader authority.
14.4 Producer
Producer MAY:
•	coordinate priorities;
•	manage dependencies;
•	manage blockers;
•	coordinate scheduling;
•	coordinate low-risk resource allocation;
•	maintain visibility across work;
•	facilitate handoffs.
Producer MUST NOT:
•	become a universal approval gate;
•	obtain binding governance authority by implication;
•	silently change project canon;
•	silently override specialist ownership;
•	replace Studio Owner.
14.5 Platform Studio
Platform Studio MAY:
•	provide shared capabilities;
•	coordinate cross-project dependencies;
•	coordinate shared resources;
•	surface governance gaps;
•	analyze trade-offs;
•	recommend options;
•	facilitate shared infrastructure.
Platform Studio MUST NOT:
•	become a second executive authority;
•	approve binding governance decisions;
•	resolve binding governance disputes;
•	make binding cross-project decisions on its own;
•	own project canon;
•	silently impose project-specific decisions on other projects.
If coordination requires a binding or non-reversible decision:
escalate to Studio Owner.
14.6 Project Studios
A Project Studio MAY:
•	maintain project-specific context;
•	maintain project-specific state;
•	organize Cells;
•	borrow shared specialists;
•	use Platform capabilities;
•	contain project-specific decisions and canon.
A Project Studio does NOT automatically create:
•	a Project Owner;
•	a Project Studio Owner;
•	a new executive authority.
15. Anti-Bureaucracy Rule
Do not create organizational mechanisms solely because they resemble a professional human company.
Avoid unnecessary additions such as:
•	mandatory daily meetings;
•	meeting schedules;
•	Day 1 / Day 2-to-N ceremonies;
•	quarterly reviews;
•	redundant approval ladders;
•	excessive escalation tiers;
•	management rituals;
•	organizational health bureaucracy;
•	permanent staffing requirements without demonstrated need.
A mechanism is justified only when it materially improves:
•	coordination;
•	correctness;
•	specialization;
•	context isolation;
•	risk control;
•	cognitive load;
•	delivery.
16. Required Files
The Studio Owner creates and maintains this task contract:
•	tasks/STUDIO-003.md
Implementation agents must not modify it.
Implementation scope:
Create
•	studio/STUDIO_TOPOLOGY.md
•	studio/PLATFORM_STUDIO.md
•	studio/PROJECT_STUDIO_TEMPLATE.md
•	studio/CELL_MODEL.md
•	studio/EXPERT_GUILDS.md
•	studio/ACTIVATION_POLICY.md
Modify
•	studio/ORG_CHART.md
No other file may be changed.
Final STUDIO-003 milestone footprint therefore consists of:
•	seven new files total, including this task contract;
•	one existing file modified: studio/ORG_CHART.md.
17. Required Content by File
studio/STUDIO_TOPOLOGY.md
•	parent organizational map;
•	relationship between Platform Studio, Project Studios, Cells, and Expert Guilds;
•	high-level ownership boundaries;
•	high-level interaction model.
Do not duplicate detailed operational rules belonging to later files.
studio/PLATFORM_STUDIO.md
•	Platform Studio mission;
•	shared-capability boundaries;
•	allowed coordination responsibilities;
•	prohibited authority expansion;
•	interaction with Project Studios and Guilds.
Do not select tools, implement runtime routing, assign models, or create executive authority.
studio/PROJECT_STUDIO_TEMPLATE.md
•	identity;
•	project scope;
•	project-specific references;
•	project-specific state;
•	active Cells;
•	borrowed Guild capabilities;
•	project constraints.
It must NOT create a named game, invent sample canon, invent a specific fictional project, or create Project Owner/Project Studio Owner.
studio/CELL_MODEL.md
•	Cell purpose;
•	formation criteria;
•	minimum composition;
•	lightweight operation;
•	collaboration;
•	handoff;
•	blocked state;
•	completion;
•	dissolution/inactivation.
Cells must remain outcome-oriented, cross-functional when needed, temporary or persistent only when justified, and minimally staffed.
studio/EXPERT_GUILDS.md
•	what a Guild is;
•	when specialist pooling is justified;
•	borrowing/return concept;
•	interaction with Cells/Projects;
•	criteria for creating a new Guild;
•	conditions for keeping a Guild inactive.
Guilds are capability pools, not mandatory active departments.
studio/ACTIVATION_POLICY.md
•	INACTIVE
•	READY
•	ACTIVE
•	BLOCKED
•	HANDOFF
•	COMPLETE
It must define minimum sufficient team, explain when roles/Cells activate or deactivate, and must not implement provider/model routing.
studio/ORG_CHART.md
•	Update only enough to show that the six existing STUDIO-002 logical roles can now operate inside the hierarchical topology.
Preserve the six operational role profiles and do not rewrite existing governance unnecessarily.
18. Non-Goals
STUDIO-003 must NOT:
•	install tools;
•	install dependencies;
•	create API keys;
•	connect AI providers;
•	adopt OpenCode;
•	adopt Kilo;
•	adopt LiteLLM;
•	adopt OmniRoute;
•	adopt Promptfoo;
•	adopt Serena;
•	implement runtime routing;
•	implement automatic failover;
•	choose an engine;
•	choose a programming language;
•	choose a framework;
•	define gameplay;
•	define story canon;
•	create a real game project;
•	create a fictional example project that could be mistaken for project truth;
•	create art/audio pipelines;
•	assign permanent models/providers to roles;
•	create unnecessary active agents;
•	modify existing STUDIO-002 agent profiles;
•	modify this task contract;
•	commit;
•	push;
•	merge;
•	open a PR.
Tool/runtime evaluation belongs to later milestones.
19. Acceptance Criteria
☐ tasks/STUDIO-003.md remains unchanged by implementation agents.
☐ Exactly six new implementation documents exist under studio/.
☐ Only studio/ORG_CHART.md is modified among pre-existing files.
☐ Parent GAME AI Studio is clearly defined.
☐ Platform Studio is clearly defined.
☐ Project Studios are clearly defined.
☐ Dynamic cross-functional Cells are clearly defined.
☐ Shared Expert Guilds are clearly defined.
☐ Existing six STUDIO-002 operational profiles remain valid.
☐ LARGE ORGANIZATION, SMALL ACTIVE TEAM is preserved.
☐ Minimum-sufficient-team principle is explicit.
☐ AGENT ROLE != RUNTIME != MODEL != PROVIDER is preserved.
☐ Producer remains coordination-focused.
☐ Platform Studio does not gain binding executive authority.
☐ Studio Owner remains final binding/non-reversible authority.
☐ Project-specific state can remain isolated.
☐ Direct specialist collaboration remains possible.
☐ Runtime failover compatibility is preserved conceptually.
☐ No runtime/provider/tool is adopted.
☐ No engine/language/framework is selected.
☐ No game/canon is invented.
☐ No hidden chat history or private chain-of-thought is required.
☐ No unnecessary human-company ceremony becomes mandatory.
☐ Rules have clear canonical homes and avoid unnecessary duplication.
20. Deterministic Authority Validation
Before STUDIO-003 may be considered complete, run deterministic searches.
The allowed implementation files must contain ZERO occurrences of:
•	Project Owner
•	Project Studio Owner
•	Platform Studio Owner
Search:
$paths = @(
    "studio\STUDIO_TOPOLOGY.md",
    "studio\PLATFORM_STUDIO.md",
    "studio\PROJECT_STUDIO_TEMPLATE.md",
    "studio\CELL_MODEL.md",
    "studio\EXPERT_GUILDS.md",
    "studio\ACTIVATION_POLICY.md",
    "studio\ORG_CHART.md"
)

Select-String `
    -Path $paths `
    -Pattern "Project Owner",
             "Project Studio Owner",
             "Platform Studio Owner" `
    -CaseSensitive:$false
Expected result:
(no output)
Also inspect suspicious authority wording:
Select-String `
    -Path $paths `
    -Pattern "Platform.*resolv",
             "Platform.*approv",
             "Platform.*decid" `
    -CaseSensitive:$false
Any result that gives Platform Studio final binding/governance authority must be rejected or rewritten.
Platform Studio may coordinate, surface, facilitate, analyze, or recommend.
Binding/non-reversible authority remains with Studio Owner.
21. Scope Validation
Run:
git status --short --untracked-files=all
Expected milestone scope:
 M studio/ORG_CHART.md
?? studio/ACTIVATION_POLICY.md
?? studio/CELL_MODEL.md
?? studio/EXPERT_GUILDS.md
?? studio/PLATFORM_STUDIO.md
?? studio/PROJECT_STUDIO_TEMPLATE.md
?? studio/STUDIO_TOPOLOGY.md
?? tasks/STUDIO-003.md
No other changed file is allowed.
22. Diff Validation
Before staging:
git diff --check
Because newly created untracked files are not included in normal git diff, final whitespace validation must also occur after staging.
After staging:
git diff --cached --check
git diff --cached --stat
git status --short
No commit may occur until scope and content review pass.
23. Review Requirements
STUDIO-003 requires independent review before commit/PR.
Review should attempt to falsify the implementation by checking:
4.	Did any new authority role appear?
5.	Did Platform gain binding authority?
6.	Did Producer become a universal gate?
7.	Were existing STUDIO-002 roles invalidated?
8.	Did project-specific state leak across Project Studios?
9.	Did any runtime/model/provider become permanently bound to a role?
10.	Was unnecessary bureaucracy introduced?
11.	Is important information duplicated across multiple canonical files?
12.	Was a game, engine, language, framework, or provider chosen?
13.	Did implementation modify files outside scope?
Review outcome:
•	APPROVE
•	REQUEST CHANGES
•	BLOCK
24. Definition of Done
STUDIO-003 is complete when:
•	the hierarchical topology is documented;
•	authority invariants pass deterministic validation;
•	all six implementation documents exist;
•	studio/ORG_CHART.md is updated consistently;
•	existing governance and STUDIO-002 profiles remain valid;
•	organizational capability can scale without requiring a large permanently active workforce;
•	Project Studios can remain isolated;
•	Cells can activate dynamically;
•	Guilds can provide shared expertise;
•	Platform Studio remains a shared-capability/coordination layer rather than a second executive authority;
•	Studio Owner retains final binding authority;
•	no game or technology decision has been introduced;
•	no runtime/tool/provider has been installed or adopted;
•	independent review passes;
•	no commit or PR has occurred before review.
