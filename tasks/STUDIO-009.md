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
5. `STUDIO-009P*` - one child contract per real provider, with offline/synthetic implementation first.
6. `STUDIO-009R-01` - one-time progressive live-activation governance amendment.
7. `STUDIO-009V*` - one separately accepted provider-specific connected-validation track after the corresponding P child is durably complete offline.
8. `STUDIO-009E` - automatic policy routing and failover across separately validated, routing-eligible providers.
9. `STUDIO-009F` - full connected multi-provider/multi-repository studio acceptance and closeout.

Each contract must merge before the implementation or connected authority it governs is created. Provider-specific work cannot be authorized by the generic STUDIO-009D framework alone. A merged P child never implies connected authority; a separately merged V-track contract is required before real provider authentication/network/model activity.

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

STUDIO-009A through STUDIO-009D are complete.

STUDIO-009P-01 Groq is COMPLETE through merged offline implementation and closeout. Its real provider remains DISABLED for connected execution until a separately accepted provider-specific V-track authorizes bounded connected validation.

STUDIO-009P-02 Cloudflare Workers AI is COMPLETE through merged offline/synthetic implementation and closeout. Its exact offline model allowlist remains `@cf/nvidia/nemotron-3-120b-a12b`. Its real provider remains DISABLED for connected execution until a separately accepted provider-specific V-track authorizes bounded connected validation.

STUDIO-009R-01 is COMPLETE through merged closeout PR #58 at `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`. Its generic progressive-live framework is durable and grants no provider authority by itself.

STUDIO-009V-01 is the next provider-specific track for Groq. Its contract may authorize a later bounded PUBLIC/SYNTHETIC connected smoke only after the V-01 contract itself is durably merged. Until then Groq remains connected `DISABLED`. STUDIO-009V-02 Cloudflare remains a later separate track. Automatic provider selection remains prohibited until STUDIO-009E.

STUDIO-009E remains the automatic routing/failover phase over separately validated and routing-eligible providers. STUDIO-009F remains the full connected studio acceptance gate, not the first provider-call gate.

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

## STUDIO-009V-02 Cloudflare connected-validation contract checkpoint

STUDIO-009V-01 Groq is COMPLETE through durable closeout merge `6bdb1daa9b2dee65a3262da8caf8c3ce42a4ac46` and remains `LIVE_VALIDATED` with worker/routing authority `NONE`.

STUDIO-009V-02 is now the provider-specific connected-validation contract track for the already-complete Cloudflare Workers AI P-02 child.

The V-02 contract reconciles the post-STUDIO-009R architecture without rewriting historical P-02 evidence: the later implementation may authorize bounded Cloudflare connected validation only through `STUDIO-009V-02_ONLY`, with promotion ceiling `LIVE_VALIDATED`. Automatic routing/failover remains STUDIO-009E authority and full connected studio acceptance remains STUDIO-009F.

The contract PR itself authorizes no Account ID/API-token input, no Cloudflare/model/network call, no AI Gateway, no tool/storage activity and no spend.

Next gate: separate Studio Owner merge of the V-02 contract PR.
<!-- STUDIO-009V-02-CONTRACT-CHECKPOINT-0001 -->

## STUDIO-009V-02 credential bridge scope correction

After V-02 contract merge, implementation preflight established that the existing `scripts/session_credential_bridge.py` is Groq V-01-specific rather than provider-neutral.

V-02 therefore authorizes a dedicated Cloudflare session credential bridge and dedicated tests instead of mutating or misusing the accepted Groq bridge. This is a scope correction only; Cloudflare connected authority, money ceiling, live-state ceiling, worker/routing authority and AI Gateway prohibition are unchanged.

No Cloudflare/account/token/network/model activity is authorized by this correction.

<!-- STUDIO-009V-02-CREDENTIAL-BRIDGE-CORRECTION-0001A -->
