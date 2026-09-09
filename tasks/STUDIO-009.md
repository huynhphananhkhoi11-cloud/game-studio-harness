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
## STUDIO-009P-03 NVIDIA NIM provider-child contract checkpoint

STUDIO-009V-02 Cloudflare connected validation is durably COMPLETE through closeout merge cbcdd527fc549ccf474667661244e452bdcfc5a5; worker/routing/AI-Gateway authority remains NONE and spend remains zero.

The V-02 closeout resumes at STUDIO-009P-03_PROVIDER_ONBOARDING_PLANNING and selected no provider itself.

The Studio Owner has selected NVIDIA-hosted NIM as the third provider-child contract track, exact candidate model deepseek-ai/deepseek-v4-pro-0813.

P-03 is specification-only: no NVIDIA account/API-key/network/model/tool/routing/worker/production-use authority; money ceiling zero; PUBLIC/synthetic only.

Only after durable P-03 contract merge may bounded offline/synthetic implementation be created. Real NVIDIA validation requires separately accepted STUDIO-009V-03. Automatic routing/failover remains STUDIO-009E and full connected acceptance remains STUDIO-009F.

Poolside P/V-04 and OpenCode P/V-05 remain future planning tracks with no authority from P-03.

Next gate: separate Studio Owner merge of the P-03 contract Pull Request.
<!-- STUDIO-009P-03-CONTRACT-CHECKPOINT-0001 -->

## STUDIO-009V-03 NVIDIA NIM connected-validation contract checkpoint

STUDIO-009P-03 NVIDIA NIM is durably COMPLETE through implementation merge `ac04040f40f544d70db10dba975481b7da5930ea` and closeout merge `eae0b9462bca1c7e3819402219c6225a3f56fb0f`. Exact model remains `deepseek-ai/deepseek-v4-pro-0813`; connected provider, credential, tool and routing authority remain NONE and spend remains zero.

STUDIO-009V-03 is now the provider-specific connected-validation contract track for the completed NVIDIA P-03 child.

The V-03 contract may authorize only a later bounded NVIDIA-hosted Free Endpoint validation with promotion ceiling `LIVE_VALIDATED`: maximum three PUBLIC/SYNTHETIC real requests, concurrency 1, retry 0, first-campaign input estimate <=4096 tokens/request, requested output <=512 tokens/request, no tools, no partner endpoint, no production use and money ceiling zero.

The contract PR itself authorizes no NVIDIA API-key creation/input, no private account probing, no NVIDIA/DeepSeek/model/network call, no real trial request/Credit consumption, no routing/worker promotion and no spend.

Automatic routing/failover remains STUDIO-009E authority. Full connected studio acceptance remains STUDIO-009F.

Next gate: separate Studio Owner merge of the V-03 contract Pull Request.
<!-- STUDIO-009V-03-CONTRACT-CHECKPOINT-0001 -->

## STUDIO-009V-03 post-merge account-verification freeze checkpoint

STUDIO-009V-03 offline live-validation implementation is durably merged through PR #71 at `f124a51e792b66eba363b069108754f99edc1c79` from reviewed head `c9a66ae01e9c7a57e4a67b846ce43c187edde6ed`.

The connected phase remains unexecuted. Owner inspection of `build.nvidia.com` confirmed the exact `deepseek-ai/deepseek-v4-pro-0813` Free API endpoint and exact NVIDIA-hosted base URL are visible, but NVIDIA account verification currently blocks API access because SMS OTP verification is not completing.

V-03 is therefore frozen at `LIVE_VALIDATION_READY` before Owner connected preflight. No NVIDIA API key has been created for GAME; no real NVIDIA request has been sent; connected-validation and quality evidence remain `PENDING_REAL_SMOKE`; worker/tool/routing authority remain NONE; spend remains zero.

This freeze does not grant connected authority. V-03 may resume only after the Owner can prove account verification/API access, current zero-cost eligibility, no paid/billing requirement for the bounded campaign, and a credential revocation path.

While V-03 is frozen, STUDIO-009P-04 Poolside provider-child planning may become the next authoritative provider write track. P-04 receives no NVIDIA authority and must preserve the one-writer rule. STUDIO-009E routing and STUDIO-009F full acceptance remain later gates.

Next gate for V-03: `WAIT_NVIDIA_ACCOUNT_VERIFICATION_THEN_OWNER_CONNECTED_PREFLIGHT`.
Next provider write track: `STUDIO-009P-04_CONTRACT`.
<!-- STUDIO-009V-03-ACCOUNT-VERIFICATION-FREEZE-CHECKPOINT-0006 -->

## STUDIO-009P-04 Poolside / Laguna S 2.1 provider child contract checkpoint

STUDIO-009V-03 NVIDIA connected preflight remains durably frozen on account verification. The freeze checkpoint authorizes `STUDIO-009P-04_CONTRACT` as the next provider write track without granting any NVIDIA connected authority.

STUDIO-009P-04 defines Poolside's direct standalone hosted inference path with exact model `poolside/laguna-s-2.1`, exact candidate base URL `https://inference.poolside.ai/v1`, PUBLIC/SYNTHETIC-only data, dynamic `Free to use for a limited time` evidence, and money ceiling zero.

The P-04 contract itself authorizes no Poolside account/API-key creation or resolution, no Poolside/Laguna network/model call, no `pool` CLI, no tools/MCP/ACP, no third-party gateway, no local/self-hosted inference, no routing/worker promotion, no private GAME export, and no spend.

Poolside Terms permit Content use for training unless opted out; therefore P-04 remains PUBLIC/SYNTHETIC-only regardless of future Training Opt-Out status. The `pool` CLI is intentionally outside the initial provider/model evaluation because it can persist credentials and exercise repository/tool/MCP capabilities.

After contract merge only, P-04 may proceed to its exact offline/synthetic implementation scope. A separate STUDIO-009V-04 contract is required before any real Poolside connection.

Automatic routing/failover remains STUDIO-009E authority. Full connected acceptance remains STUDIO-009F.

Next gate: separate Studio Owner review and merge of the P-04 contract Pull Request.
<!-- STUDIO-009P-04-CONTRACT-CHECKPOINT-0001 -->


## STUDIO-009V-04 Poolside / Laguna S 2.1 bounded connected-validation contract checkpoint

P-04 is durably COMPLETE after implementation PR #74 and closeout PR #75.

V-04 is the next provider-connected contract track for the direct Poolside standalone path:

- provider profile: `provider-profile:poolside-direct-laguna-s-2.1`;
- child: `STUDIO-009P-04`;
- model: `poolside/laguna-s-2.1`;
- direct base: `https://inference.poolside.ai/v1`;
- first campaign maximum: 3 requests, concurrency 1, retry 0;
- PUBLIC/SYNTHETIC only;
- `pool` CLI/tools/MCP/ACP/routing remain forbidden;
- money ceiling remains USD 0;
- V-03 NVIDIA remains frozen at account verification;
- P-05 OpenCode remains non-authoritative while V-04 is active.

This contract checkpoint performs no Poolside account/key/provider/model/network/CLI/tool/MCP/ACP/routing activity.

Contract merge authorizes only the separate offline V-04 live-transport implementation. A real request remains forbidden until offline implementation + QA + Review and a separate Owner connected preflight prove current zero-cost eligibility and server-side validation-key revocation/deletion/invalidation.

Next gate: `VERIFY_V04_CONTRACT_PR_AND_RULES_CI`.

<!-- STUDIO-009V-04-CONTRACT-CHECKPOINT-0001 -->
