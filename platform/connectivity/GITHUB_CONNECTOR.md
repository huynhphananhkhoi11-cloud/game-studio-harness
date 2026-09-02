# STUDIO-009B Disabled GitHub Connector Core

## Purpose

This module implements deterministic request planning, injected-transport
execution, response verification, and in-memory idempotency reuse. It contains
no live HTTP, GraphQL, Git, GitHub CLI, SDK, webhook, credential, provider, or
network transport constructor.

## Allowlisted operations

- `READ_METADATA`
- `READ_TREE`
- `READ_BLOB`
- `CREATE_BRANCH`
- `CREATE_OR_UPDATE_FILE`
- `OPEN_PULL_REQUEST`
- `READ_PULL_REQUEST`
- `READ_CHECKS`

All other operations fail closed. In particular, merge/auto-merge, repository
administration, settings, collaborators, teams, protections, workflows,
environments, secrets, variables, releases, deployments, pages, webhooks,
apps, billing, ownership, delete/archive/transfer/fork/visibility/rename,
credential creation, and execution of repository content are outside this
core.

## Planning

A request is accepted only after its repository record and STUDIO-009A
boundary/threat evidence validate. Planning verifies repository identity and
record digest, immutable base SHA, access tier/status, default/protected branch
denial, exact branch namespace, exact/nested path allowlists, data
classification, instruction authority, writer/worktree evidence for writes,
Owner/gate/trace/queue/dispatch/zero-budget evidence, integer-only limits,
caller-supplied UTC chronology, idempotency window, and canonical request
digest.

The resulting `TransportPlan` is a frozen dataclass. It carries only normalized
bounded fields and the opaque auth-profile reference; no credential value is
accepted.

## Injected transport and replay

`DisabledGitHubConnector` requires an object exposing `execute(plan)`. Tests use
a deterministic in-memory recording fake. The core has no live transport
factory. A repeated idempotency key with the same canonical request returns a
copy of the prior normalized result without another transport call. Reusing a
key for a different request fails with `IDEMPOTENCY_CONFLICT`.

## Result verification

Results must match repository identity, repository-record digest, operation,
request digest, idempotency key, base revision, target ref/path scope and
caller `as_of`; response size is bounded and revisions must be immutable.
File-update results must prove a new immutable revision. Read results must
remain bound to the requested immutable revision.

This implementation does not activate GitHub connectivity. Real transport
remains gated by STUDIO-009C and the separately approved STUDIO-009F connected
pilot.
