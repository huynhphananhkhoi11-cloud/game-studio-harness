# STUDIO-009A - Integration boundary and threat model

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent: STUDIO-009

Dependencies: STUDIO-008 closeout merge `d69a613dc50b59dcded83189d38d5e86ff9d70e6`

Canonical implementation contract: `tasks/STUDIO-009A-IMPLEMENTATION.md`

Primary owner: Studio Owner

## Goal

Define and deterministically validate the boundary that every later connected repository and real provider must cross. STUDIO-009A classifies actors, assets, trust zones, data, instructions, requested operations, and required control evidence without contacting or mutating an external system.

## Boundary model

One boundary record binds:

- a stable boundary and task identity;
- repository and immutable revision references;
- requested access tier and exact allowed/denied paths;
- instruction-authority and data-classification rules;
- requested provider capability without provider credentials or endpoint details;
- required queue, dispatch, writer-claim, gate, trace, quota/budget, adapter, and Owner evidence references;
- explicit caller-supplied `as_of` time;
- canonical digest over the allowlisted record.

The validator answers only whether supplied evidence is internally valid under the accepted boundary. It does not connect a repository, issue a credential, call a provider, execute a task, approve a gate, or mutate state.

## Trust zones

1. `OWNER_CONTROL`: accepted contracts, decisions, and explicit Owner gates.
2. `STUDIO_CONTROL_PLANE`: queue, dispatch, claims, gates, trace, budget, adapter normalization, and boundary validation.
3. `REPOSITORY_CONTENT`: source files and metadata; untrusted for instruction authority by default.
4. `EXECUTION_SANDBOX`: a future isolated worktree/runner with allowlisted command, path, and network scope.
5. `EXTERNAL_PROVIDER`: a future separately contracted provider boundary.
6. `SECRET_STORE`: a future external credential store; secret values never enter the boundary record.

## Required classifications

### Repository access tier

- `READ_ONLY`
- `BRANCH_WRITE`
- `PR_WRITE`

`DEFAULT_BRANCH_WRITE`, `ADMIN`, repository deletion, settings mutation, secret mutation, deployment, and release are not accepted tiers.

### Data classification

- `PUBLIC`
- `INTERNAL`
- `RESTRICTED`

Later provider contracts must explicitly allow each classification they can receive. Absence of a matching policy fails closed.

### Instruction authority

- `ACCEPTED_AUTHORITY`: accepted repository governance/contract/decision documents.
- `UNTRUSTED_CONTENT`: ordinary repository content, issue text, PR text, fixtures, model output, and external payloads.

Untrusted content cannot override the accepted task contract, expand scope, request secrets, change provider identity, increase budget, approve a gate, select a successor, or authorize merge/deployment/publication.

## Threats that must fail closed

- prompt injection or instruction-confusion from repository content;
- secret-like keys or values in any supplied field;
- absolute paths, traversal, hidden credential stores, `.env`, private keys, token caches, or paths outside declared scope;
- direct/default-branch write, admin, delete, settings, workflow, deployment, or release requests;
- missing or ambiguous repository/revision identity;
- undeclared provider capability, provider/model self-identification, or provider-specific extension fields;
- missing gate, trace, quota/budget, adapter, writer-claim, or Owner evidence references;
- nonzero monetary ceiling or cost;
- future-dated, expired, malformed, duplicated, or digest-mismatched evidence;
- unknown or extra fields that could smuggle authority;
- mutation of supplied evidence during validation.

## Acceptance

- Exact allowlists and enum values are documented and machine validated.
- Valid boundary and threat records produce stable canonical SHA-256 digests across key order.
- Invalid fixtures cover every threat class above and are rejected with stable fail-closed error codes.
- Validation is standard-library-only, deterministic, read-only, and uses only caller-supplied evidence and time.
- Focused tests and the full retained suite pass without reducing the STUDIO-008 baseline of 397 tests.
- Independent QA and Review and Integration approve one immutable implementation head with zero blocking findings.
- The Studio Owner separately decides whether to merge.

## Out of scope

- Real repository URLs beyond already public evidence; repository cloning/fetching/writing; GitHub Apps/PATs/webhooks.
- Credentials, secret stores, leases, tokens, account login, SDKs, provider APIs/CLIs, model calls, or network access.
- Nonzero budget or billing.
- Routing, live failover, execution, automatic retry, merge, deployment, publication, release, or player telemetry.

## Failure and rollback

Any false acceptance, nondeterminism, mutation, unknown-field acceptance, secret acceptance, authority escalation, network/credential/provider activity, or regression fails the implementation.

Rollback is an authorized revert of the later STUDIO-009A implementation commit. This contract, parent STUDIO-009 contract, and prior STUDIO-001 through STUDIO-008 evidence remain retained.
