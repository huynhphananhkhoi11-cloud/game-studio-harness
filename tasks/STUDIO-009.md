# STUDIO-009 - Connected repositories and multi-AI activation

Status: ACCEPTED - PHASED IMPLEMENTATION AUTHORIZED - CONNECTIONS NOT ACTIVATED

Parent roadmap: GAME AI Studio post-v1.0 activation

Dependencies: STUDIO-001 through STUDIO-008 are merged and retained

Primary owner: Studio Owner

## Goal

Extend the accepted Manual/Fake v1.0 control plane so separately approved repositories and real AI providers can participate through explicit, least-privilege boundaries without gaining authority to approve gates, write outside scope, merge, deploy, publish, or spend beyond an Owner-approved ceiling.

STUDIO-009 is an activation program, not one all-powerful connector. Repository access, credential handling, provider onboarding, routing/failover, and connected-pilot acceptance remain separable controls with independent evidence and rollback.

## Phased structure

1. `STUDIO-009A` - integration boundary and threat model.
2. `STUDIO-009B` - repository registry and GitHub connector.
3. `STUDIO-009C` - credential broker and secret lifecycle.
4. `STUDIO-009D` - provider onboarding framework.
5. `STUDIO-009P*` - one child contract per real provider.
6. `STUDIO-009E` - policy routing and live failover.
7. `STUDIO-009F` - connected pilot, acceptance, and closeout.

Each phase requires its contract to merge before its implementation paths are created. Provider-specific work cannot be authorized by the generic STUDIO-009D framework alone.

## Inherited capabilities

- STUDIO-001 through STUDIO-004 provide governance, roles, topology, handoff, and persistent memory.
- STUDIO-005 and STUDIO-006 provide source/evidence authority plus deterministic evaluation and review.
- STUDIO-007 provides queue, dispatch, writer claims, worktrees, durable handoff, failover, gates, trace, budgets, and the provider-neutral adapter boundary.
- STUDIO-008 provides the accepted deterministic Manual/Fake pilot and rollback baseline.

STUDIO-009 must consume those contracts. It must not create a parallel queue, authority system, memory protocol, gate system, or merge path.

## Program-wide invariants

- The Studio Owner retains the final approve/reject and merge decision.
- Direct writes to protected/default branches are forbidden.
- One attempt has at most one active writer claim for its authorized path scope.
- Repository, path, data, provider, capability, credential, quota, budget, and time boundaries are allowlisted and fail closed.
- Repository content is untrusted data unless an accepted authority document explicitly grants instruction authority.
- Secrets remain outside repository, prompt, model output, trace, evidence, exception text, and memory records.
- Real provider identity is derived from accepted configuration and validated transport metadata, never from model-generated text.
- Monetary ceiling is zero until the Owner accepts a provider-, currency-, and time-window-specific nonzero amount.
- Manual and Fake adapters remain available as the no-network rollback path.
- No adapter, dispatcher, router, evaluator, reviewer, or AI can self-authorize a successor, gate, merge, deployment, publication, or budget increase.

## Full acceptance target

Full connected multi-provider acceptance requires:

- at least two Owner-approved repository records, each with a real immutable identity and explicit access tier;
- at least two real provider adapters, each onboarded through its own accepted child contract;
- zero unauthorized writes, direct-main writes, AI merge attempts, secret exposures, duplicate writers, duplicate outputs, and gate bypasses;
- complete material transition trace and durable handoff lineage;
- deterministic reconciliation of repository, provider, credential, quota, budget, gate, and result evidence;
- demonstrated kill switch, credential revocation, provider pause, repository read-only downgrade, and rollback to Manual/Fake;
- independent QA PASS, Review and Integration APPROVE, and a separate Studio Owner disposition.

A single-provider or read-only result may be accepted only with explicit limitations. It is not equivalent to full connected multi-provider acceptance.

## Current authorization boundary

STUDIO-009A and STUDIO-009B are complete. Only STUDIO-009C contract work is currently active. This authorizes specification and memory records only: no credential value, secret-store access, GitHub App installation/token minting, PAT, OAuth flow, SSH key use, live repository transport, webhook, provider SDK/API/CLI, model call, routing, connected execution, network call, nonzero spend, external write, deployment, or release is authorized.

## Owner decisions deferred to later contracts

- the identity and URL of every repository beyond `game-studio-harness`;
- GitHub authentication mechanism and installation scope;
- runner and sandbox environment;
- credential store and rotation/revocation mechanism;
- provider/model/transport identity for each `STUDIO-009P*` child;
- provider-specific data export policy;
- provider-, currency-, and time-window-specific monetary ceilings;
- final connected-pilot disposition.

## Failure and rollback

Any phase that expands scope without accepted authority, leaks a secret, permits direct-main or unauthorized writes, creates duplicate work, bypasses a gate, fabricates provider identity, exceeds a ceiling, or loses immutable lineage fails closed.

Rollback is phase-local where possible and always preserves accepted contracts and evidence. The minimum safe fallback is repository write disabled, real providers paused/revoked, money ceiling zero, and Manual/Fake-only operation.