# STUDIO-009D - Provider onboarding framework

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - IMPLEMENTATION NOT STARTED

Parent capability: `tasks/STUDIO-009.md`

Dependency: STUDIO-009C closeout merge `bfc48f2080bd654666955ca1ec615ebc27ad83cc`

Primary owner: Studio Owner

Cost class: ZERO_COST

Provider runtime activity: NONE

Network activity: NONE

Connected execution activity: NONE

## Goal

Define a generic, provider-neutral onboarding framework that can validate provider, model, capability, credential-reference, data-export, quota, budget, lifecycle, and child-contract evidence without connecting to or authorizing any real provider.

STUDIO-009D creates the rules and deterministic validation boundary that every later `STUDIO-009P*` real-provider child must satisfy. It does not itself approve OpenAI, Anthropic, Google, xAI, or any other real provider, model, account, endpoint, credential, SDK, CLI, network call, hosted execution, or spend.

## Inherited authority and dependencies

STUDIO-009D consumes and must not replace:

- STUDIO-007F provider-neutral MANUAL/FAKE adapter boundary;
- STUDIO-009A integration boundary and threat model;
- STUDIO-009B repository registry and fail-closed GitHub connector core;
- STUDIO-009C credential broker and metadata-only secret lifecycle;
- STUDIO-007 queue, dispatch, writer claim, worktree, gate, trace, quota, budget, handoff, failover, and provider-adapter contracts;
- Studio Owner authority over provider admission, credentials, budget, activation, merge, deployment, publication, and release.

No provider-onboarding record grants organizational authority.

## 1. Generic provider profile

A provider profile is configuration metadata only. It may describe an onboarding candidate but cannot cause a provider call.

The generic profile must bind at least:

- immutable `provider_profile_id`;
- opaque `provider_identity_ref`;
- opaque `provider_child_contract_ref`;
- opaque `transport_profile_ref`;
- opaque `credential_profile_ref`;
- exact model-profile references;
- exact capability-binding references;
- allowed data classifications;
- export-policy reference;
- quota-policy reference;
- budget-policy reference;
- Owner approval evidence;
- provider kill-switch reference;
- caller-supplied `as_of` and expiry;
- canonical digest.

Provider-specific secrets never appear in the profile.

### Provider lifecycle states

The generic lifecycle is exactly:

- `DISABLED`
- `CANDIDATE`
- `ELIGIBLE`
- `PAUSED`
- `REVOKED`

`ELIGIBLE` means only that deterministic onboarding prerequisites are satisfied. It is not an `ACTIVE` or connected state and does not authorize network use. STUDIO-009D defines no `ACTIVE` state.

`REVOKED` and `PAUSED` dominate eligibility. A revoked profile cannot be reactivated by an event. A fresh accepted child contract and fresh Owner evidence are required for a replacement profile.

## 2. Provider identity and child-contract authority

Real provider identity must come from an accepted `STUDIO-009P*` child contract plus later validated transport metadata. It must never come from model-generated text, prompt content, repository content, a provider response body, or an untrusted caller label.

The generic STUDIO-009D implementation may use only clearly synthetic provider/model/transport identifiers in committed fixtures and tests.

A profile cannot become `ELIGIBLE` unless it binds accepted child-contract evidence. Generic STUDIO-009D evidence may validate structure and lineage only; it cannot fabricate acceptance for a real provider.

## 3. Required `STUDIO-009P*` child contract

Each real-provider child contract must separately define and obtain Studio Owner acceptance for:

1. provider legal/product identity and canonical documentation sources;
2. exact provider/model identifiers and model-version or alias policy;
3. exact transport mechanism and allowlisted host/endpoint identity;
4. authentication mechanism and accepted STUDIO-009C credential-profile lineage;
5. exact capability mapping to the provider-neutral STUDIO-007F adapter boundary;
6. input/output data classifications and provider-specific export policy;
7. provider retention/training/privacy terms relevant to allowed data;
8. request, response, context, file, tool, timeout, and concurrency limits;
9. rate-limit, quota, retry, refusal, timeout, malformed-output, and outage semantics;
10. provider-, currency-, and time-window-specific budget ceiling;
11. transport/provider identity verification evidence;
12. kill switch, provider pause, credential revocation interaction, and rollback to MANUAL/FAKE;
13. incident and secret-exposure response;
14. focused and regression test requirements;
15. independent QA and Review and Integration gates;
16. explicit statement that connected activation remains under STUDIO-009F.

No generic STUDIO-009D record may substitute for a real-provider child contract.

## 4. Model and capability bindings

A model profile and capability binding are metadata-only declarations.

They must:

- bind to one provider profile and accepted child-contract evidence;
- use exact capability IDs and exact model-identity references;
- constrain allowed data classifications;
- constrain bounded input/output limits;
- preserve the provider-neutral request/result contract;
- never broaden repository, credential, data, quota, budget, gate, or Owner authority;
- never claim a capability merely because a model response says it supports one.

Unsupported or uncontracted model/capability combinations fail closed.

## 5. Credential boundary

STUDIO-009D consumes STUDIO-009C credential metadata by reference only.

A provider profile may bind an opaque `credential_profile_ref`, but:

- no raw secret value is accepted;
- no credential lookup is performed;
- no environment variable or `.env` credential is resolved;
- no keyring, Credential Manager, browser credential, vault, KMS, HSM, cloud secret manager, OAuth flow, PAT, API key, refresh token, or private key is accessed;
- credential eligibility alone never authorizes provider execution.

Provider-specific credential purpose/scope must be approved in the applicable `STUDIO-009P*` child.

## 6. Data-export and budget boundary

Data export is deny-by-default.

A provider profile/model/capability combination may only declare classifications explicitly allowed by the accepted child evidence and inherited integration boundary. No generic profile may broaden classification or authority paths.

The monetary ceiling remains integer zero throughout STUDIO-009D implementation. A later provider child may propose a nonzero provider-, currency-, and time-window-specific ceiling, but it has no effect until separately accepted by the Studio Owner.

## 7. Determinism and safe errors

The implementation must reuse accepted canonicalization, structural limits, duplicate-key rejection, finite-number checks, caller-supplied UTC time, immutable input checks, secret detection/redaction, and stable safe-error behavior from STUDIO-009A through STUDIO-009C.

Validation cannot consult system time for acceptance decisions.

Public error messages must not echo untrusted provider/model/account/endpoint/credential values.

## 8. Runtime prohibitions

STUDIO-009D implementation must not:

- import or call provider SDKs or provider CLIs;
- call HTTP, GraphQL, WebSocket, gRPC, browser, or other network transports;
- probe provider endpoints, accounts, organizations, projects, models, quotas, billing, or availability;
- execute a model request;
- resolve a real credential;
- write outside deterministic repository artifacts;
- create routing or live failover;
- activate the STUDIO-009B GitHub transport;
- spend money.

Only deterministic local validation and synthetic fixtures are authorized.

## 9. Failure and rollback

The framework fails closed on:

- missing/ambiguous child-contract evidence;
- provider/model identity mismatch;
- unsupported capability;
- data-policy broadening;
- credential-reference mismatch;
- nonzero budget in STUDIO-009D;
- expired, paused, revoked, or future evidence;
- missing Owner approval;
- duplicate/conflicting identity;
- secret-bearing input;
- scope broadening;
- unsafe or unbounded metadata.

Rollback remains MANUAL/FAKE with real-provider execution absent.

## 10. Acceptance

STUDIO-009D implementation is accepted only after:

- this contract Pull Request is merged first;
- implementation remains within the exact approved path boundary;
- retained baseline of 263 focused / 660 total tests is preserved and coverage increases;
- zero provider/network/credential/store/connector/routing/connected-execution/spend activity;
- Rules CI success on the immutable final implementation head;
- QA-01 PASS;
- Review and Integration APPROVE;
- zero blocking findings;
- separate Studio Owner merge;
- separate memory-only closeout.

Completion of STUDIO-009D authorizes only creation of separately reviewed `STUDIO-009P*` child contracts. It does not authorize any real provider connection.

## 11. Next phase boundary

After STUDIO-009D is complete, the minimum path toward a connected pilot is:

`STUDIO-009P-01` for one real provider -> minimum STUDIO-009E policy routing -> STUDIO-009F connected pilot.

The first real credential enrollment, provider transport, model call, and network-connected execution remain prohibited until the applicable provider child and later activation gates are accepted.