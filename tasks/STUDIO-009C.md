# STUDIO-009C - Credential broker and secret lifecycle

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent: STUDIO-009

Dependencies: STUDIO-009B closeout merge `32942ac4db312884ab2f2184a3f899e363d61058`

Canonical implementation contract: `tasks/STUDIO-009C-IMPLEMENTATION.md`

Primary owner: Studio Owner

Cost class: ZERO_COST

Live credential activity: NONE

## Goal

Define and later implement an Owner-controlled credential broker and secret lifecycle boundary that can bind the opaque `auth_profile_ref` produced by STUDIO-009B to narrowly scoped, time-bounded credential-use authority without exposing secret material to repository content, prompts, model outputs, memory, traces, evidence, logs, exceptions, or unrelated processes.

STUDIO-009C is a credential-control phase. It is not a live secret-store activation, not a GitHub authentication decision, not provider onboarding, and not a connected execution pilot.

## Inherited authority

STUDIO-009C consumes and must not weaken:

- STUDIO-009A trust boundaries, canonicalization, structural limits, secret detection, path safety, caller-supplied chronology, threat evidence, and zero-cost rule;
- STUDIO-009B repository identity, access tier, path/branch scope, operation envelope, immutable revision, Owner evidence, idempotency, replay, and disabled injected-transport connector;
- STUDIO-007 queue, dispatch, writer/worktree, gate, trace, quota/budget, adapter, failover, and handoff controls;
- Studio Owner final authority over credential enrollment, activation, revocation, rotation, repository/provider access, merge, release, and spend.

No credential record, lease, broker, transport, provider, repository content, model output, or automation can create authority that is not already present in accepted Owner evidence.

## Secret-material boundary

Secret material includes any usable authentication value or value from which usable authentication can be recovered, including tokens, passwords, API keys, private keys, signed session material, refresh credentials, authorization codes, cookies, or equivalent bearer material.

The following are metadata only and MUST NOT contain, encode, concatenate, derive, or disguise secret material:

- `credential_profile_id`;
- `auth_profile_ref`;
- `secret_store_ref`;
- `secret_locator_ref`;
- `credential_lease_id`;
- `credential_event_id`;
- canonical digests, evidence references, task/attempt references, and trace references.

Secret material is forbidden from:

- Git history, repository files, fixtures, generated artifacts, task contracts, and persistent memory;
- prompts, model context, model responses, agent messages, review comments, and evaluation evidence;
- logs, traces, worklogs, exceptions, error strings, command lines, URLs, process arguments, environment dumps, and telemetry;
- connector request/result schemas and durable handoff objects.

A future trusted transport may receive credential material only through a separately accepted broker-to-transport interface under an active lease. STUDIO-009C implementation itself remains fake/injected and carries no production secret.

## Credential profile v1

The implementation must validate exact credential-profile metadata with, at minimum:

- stable `credential_profile_id` and opaque `auth_profile_ref`;
- `subject_type` and exact `subject_ref`;
- generic credential class and opaque authentication-scheme reference;
- opaque `secret_store_ref` and `secret_locator_ref`;
- allowed capability/purpose scope;
- repository record binding when the subject is a repository;
- Owner approval, boundary, gate/trace, kill-switch, and lifecycle evidence;
- status, not-before, expiry, rotation deadline, maximum lease duration, and caller-supplied `as_of`;
- canonical SHA-256 digest.

Profile status is fail-closed and limited to:

- `DISABLED`;
- `ACTIVE`;
- `REVOKED`;
- `ROTATION_REQUIRED`.

A provider-targeted profile may be represented as metadata for schema neutrality but cannot become usable until the applicable STUDIO-009D and STUDIO-009P* contracts are accepted.

## Lease request and lease result

A credential-use request must bind one validated active profile to one bounded purpose and one accepted execution lineage. It must include:

- task and attempt;
- queue and dispatch;
- writer/worktree evidence when the requested downstream operation can write;
- gate, trace, quota/budget, and Owner approval;
- subject identity and profile digest;
- repository record and operation digest when repository access is involved;
- requested lease duration;
- caller-supplied UTC `as_of`;
- bounded idempotency/replay evidence;
- canonical digest.

The broker may emit only metadata describing a lease. A lease must be immutable, time-bounded, purpose-bound, subject-bound, and profile-bound. It must never contain the secret value.

Maximum implementation lease duration is one hour. Shorter profile or request limits win. Expired, not-yet-valid, revoked, rotation-required, disabled, replayed, conflicting, or broadened requests fail closed.

## Lifecycle rules

The deterministic lifecycle model must cover:

1. profile validation;
2. disabled-to-active eligibility planning;
3. lease planning and in-memory lease accounting;
4. lease expiry;
5. revocation;
6. rotation-required state;
7. kill-switch disablement;
8. reactivation only with fresh Owner evidence.

Implementation state changes are simulated/in-memory only. They do not mutate a real credential store.

Revocation and kill switch dominate every other state. Rotation cannot silently extend expiry, scope, or Owner approval. Reusing a lease/idempotency key for different scope fails closed.

## Redaction and error hygiene

Every public failure is a stable code plus a fixed safe message. Errors must not echo untrusted input, secret-like values, locators, URLs containing user-info, environment content, or raw transport/store responses.

Redaction utilities may receive synthetic test strings in memory, but no committed fixture may contain a usable credential.

The implementation must prove that secret-like values do not appear in normalized results, exceptions, durable evidence, or memory.

## Store and runtime boundary

STUDIO-009C implementation is deterministic and injected-store-only.

Allowed:

- pure validation;
- immutable request/lease planning;
- in-memory fake store and fake lease accounting;
- synthetic redaction tests;
- canonical digests and bounded metadata.

Forbidden:

- environment-variable credential lookup;
- `.env` parsing for credential values;
- OS keychain/keyring/Credential Manager access;
- browser profile/session access;
- filesystem private-key/token cache access;
- cloud secret manager, vault, HSM, KMS, GitHub App, OAuth, PAT, SSH, provider key, or SDK integration;
- socket, HTTP, GraphQL, GitHub CLI, provider CLI/API, subprocess-based credential retrieval, or network transport;
- writing a credential value to disk, Git, stdout/stderr, trace, evidence, or memory;
- minting, refreshing, rotating, revoking, or deleting any real credential.

## Repository and provider separation

STUDIO-009C does not change repository authorization from STUDIO-009B and does not modify the disabled GitHub connector core.

An active repository credential profile is necessary but not sufficient for live GitHub access. Live GitHub transport still requires a separately Owner-approved repository/auth profile and STUDIO-009F activation.

Provider credentials do not authorize a provider. Provider identity, model/capability policy, endpoint/transport, data export, quota, and spend remain under STUDIO-009D, STUDIO-009P*, STUDIO-009E, and STUDIO-009F.

## Fail-closed conditions

At minimum, reject:

- embedded secret material or secret-like key fields;
- unknown/extra/missing nested fields;
- invalid Unicode, non-finite numbers, excessive depth/nodes/bytes;
- mutable or ambiguous subject identity;
- unknown or conflicting profile identity;
- subject/profile/repository digest mismatch;
- disabled, revoked, expired, future, or rotation-required profile;
- missing Owner/gate/trace/queue/dispatch/budget evidence;
- missing writer/worktree evidence for write-bound credential use;
- nonzero monetary ceiling;
- overlong lease or broadened capability/purpose;
- stale/replayed/conflicting idempotency;
- system-clock-derived acceptance decisions;
- input mutation;
- any attempt to serialize, log, return, or persist secret material.

## Acceptance

STUDIO-009C implementation is accepted only if:

- its contract Pull Request merges before implementation paths are created;
- exact implementation scope matches `tasks/STUDIO-009C-IMPLEMENTATION.md`;
- all new and retained tests pass with the retained full-suite baseline never below 551;
- no production secret store, credential, network, repository transport, provider, routing, connected execution, or spend is activated;
- independent QA-01 returns PASS;
- Review and Integration returns APPROVE with zero blocking findings on one immutable head;
- Studio Owner separately decides implementation merge;
- a separate memory-only closeout Pull Request is merged before STUDIO-009D implementation begins.

## Later activation boundary

STUDIO-009C acceptance does not authorize live GitHub authentication, provider authentication, secret-store connectivity, provider calls, routing, or connected execution.

Real secret-store selection and credential enrollment require explicit Owner decisions. Real GitHub connectivity remains gated by STUDIO-009F. Provider use additionally requires STUDIO-009D and provider-specific STUDIO-009P* contracts.