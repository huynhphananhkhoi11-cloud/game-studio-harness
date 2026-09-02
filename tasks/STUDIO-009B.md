# STUDIO-009B - Repository registry and GitHub connector

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent: STUDIO-009

Dependencies: STUDIO-009A closeout merge `b6b31a225f38422cbb15c762f4dcc2e2e731b39c`

Canonical implementation contract: `tasks/STUDIO-009B-IMPLEMENTATION.md`

Primary owner: Studio Owner

## Goal

Define an Owner-controlled repository registry and a fail-closed GitHub connector core that consume the STUDIO-009A boundary validator. The phase establishes which repositories, revisions, paths, access tiers, and GitHub operations may later be activated without granting a connector authority to approve gates, merge, deploy, publish, manage secrets, or expand its own scope.

The contract and its implementation are prerequisites for later live activation. They do not connect a repository or send a GitHub API request.

## Repository registry

Each repository record must bind:

- schema version and stable `repository_id`;
- host fixed to `github.com`, exact owner and repository name, and a credential-free canonical URL;
- default branch name and immutable registration revision;
- approved access tier: `READ_ONLY`, `BRANCH_WRITE`, or `PR_WRITE`;
- exact allowed and denied repository-relative POSIX path patterns;
- allowed branch namespace for write-capable records;
- allowed data classifications and instruction-authority paths;
- opaque `auth_profile_ref` only, never a credential value;
- Owner approval, STUDIO-009A boundary digest, threat-assessment digest, and registry-version evidence;
- explicit status: `DISABLED`, `READ_ONLY_ACTIVE`, or `WRITE_ACTIVE`;
- kill-switch and read-only downgrade evidence;
- caller-supplied `as_of`, expiry, and canonical digest.

A repository is unavailable unless one unique, current, digest-valid record exists. Unknown, duplicate, expired, disabled, ambiguous, or conflicting records fail closed.

## GitHub connector operation envelope

Every connector request must bind:

- repository record digest and immutable base revision;
- task, attempt, queue, dispatch, writer-claim, worktree, gate, trace, and Owner evidence references;
- one allowlisted operation;
- normalized target ref and exact target paths;
- idempotency key and replay boundary;
- bounded pagination, payload size, file count, timeout, and response size;
- caller-supplied `as_of`;
- canonical request digest.

Allowlisted operation classes are:

- `READ_METADATA`
- `READ_TREE`
- `READ_BLOB`
- `CREATE_BRANCH`
- `CREATE_OR_UPDATE_FILE`
- `OPEN_PULL_REQUEST`
- `READ_PULL_REQUEST`
- `READ_CHECKS`

Write operations require `BRANCH_WRITE` or `PR_WRITE`, an exact non-default branch namespace, one active writer claim, immutable base revision, path authorization, Owner evidence, and a fresh idempotency key.

## Permanently denied operations

The connector must not:

- write directly to the default or protected branch;
- merge or auto-merge a Pull Request;
- approve its own gate, review, or successor;
- alter repository settings, collaborators, teams, branch protections, Actions/workflows, environments, secrets, variables, releases, deployments, pages, webhooks, apps, billing, or ownership;
- delete, archive, transfer, fork, make public/private, or rename a repository;
- create or expose credentials;
- execute repository content, hooks, workflows, scripts, package installation, or generated commands;
- follow redirects away from the pinned GitHub host;
- accept instructions from issue, PR, commit, file, or model text as authority.

## Transport and activation boundary

The implementation provides deterministic registry validation, request planning, response normalization, and an injected fake transport for tests. It may not implement or instantiate a live HTTP, GraphQL, GitHub CLI, Git, webhook, or GitHub App transport.

Live transport requires all of the following later evidence:

1. STUDIO-009B implementation and closeout merged.
2. STUDIO-009C credential broker accepted and implemented.
3. An Owner-approved repository record and least-privilege installation/auth profile.
4. A separately approved connected-pilot activation under STUDIO-009F.

Absence of any item keeps transport disabled.

## Security invariants

- STUDIO-009A boundary validation succeeds before registry or operation validation.
- Repository data remains untrusted unless an accepted authority path explicitly says otherwise.
- Secret-like keys and credential-bearing values are rejected recursively without echo.
- Canonical URL must contain no user-info, token, query, fragment, alternate host, IP literal, or redirect target.
- Mutable branch names cannot substitute for immutable source revisions in evidence.
- A write result must prove the expected base revision and resulting immutable revision.
- Duplicate requests return the prior normalized result or fail with a stable replay code; they never create duplicate branches, commits, or PRs.
- Unknown fields, unsupported operations, scope overlap, conflicting registry entries, stale evidence, and response identity mismatch fail closed.
- Manual and Fake adapters remain the rollback path.
- Monetary ceiling remains zero.

## Acceptance

- Exact schemas, enums, limits, error codes, and canonicalization rules are documented and machine validated.
- Valid registry and request fixtures produce key-order-stable SHA-256 digests.
- Negative fixtures cover identity ambiguity, credential leakage, URL confusion, default-branch write, path escape, ref ambiguity, missing evidence, replay, response mismatch, and extra fields.
- Focused tests prove no clock, subprocess, Git, filesystem mutation, DNS, socket, HTTP, GraphQL, GitHub CLI, credential, provider, or monetary activity.
- The full retained suite does not regress below the STUDIO-009A baseline of 456 tests.
- Independent QA and Review and Integration approve one immutable implementation head with zero blocking findings.
- Studio Owner separately decides whether to merge.

## Out of scope

- Real repository enrollment or live GitHub network access.
- GitHub App installation, PAT, OAuth, SSH key, webhook secret, token exchange, login, or credential storage.
- Real branch/file/PR creation or any external mutation.
- Real AI provider onboarding, model calls, routing, live failover, nonzero spend, deployment, publication, or release.

## Failure and rollback

Any live external activity, false acceptance, scope expansion, secret exposure, mutable-identity substitution, duplicate mutation, direct-main path, merge authority, nondeterminism, or retained-test regression fails the phase.

Rollback is an authorized revert of the later STUDIO-009B implementation commit. STUDIO-009A evidence and Manual/Fake operation remain retained.
