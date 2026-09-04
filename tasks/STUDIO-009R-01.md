# STUDIO-009R-01 — Progressive Live Activation Amendment

Status: ACCEPTED — CONTRACT ONLY — IMPLEMENTATION NOT STARTED

Parent: `tasks/STUDIO-009.md`

Primary owner: Studio Owner

Cost class: ZERO_COST

## 1. Purpose

Amend STUDIO-009 so a provider that has completed its separately accepted `STUDIO-009P-*` contract, offline/synthetic implementation, independent QA, Review and Integration, and Studio Owner merge may proceed through a separately accepted provider-specific connected-validation track before STUDIO-009F.

This amendment separates **provider-specific connected validation** from **full integrated studio acceptance**.

It does not activate any provider, resolve any credential, create any network request, select any future provider/model, create automatic routing, authorize nonzero spend, create a Unity/game repository, or change the Studio Owner's final authority.

## 2. Why the amendment is required

The current parent and provider template were written for a late-connect lifecycle in which STUDIO-009F was the only connected activation gate. That rule prevents GAME from learning whether an already accepted offline provider is actually reachable, zero-cost, identity-correct, quota-compatible, and useful until the end of STUDIO-009.

GAME now adopts a cloud-first, progressive-validation lifecycle while retaining fail-closed governance and the Manual/Fake regression path.

No runner, credential, provider, or API call may bypass the old rule before this amendment becomes durable through merge.

## 3. Revised provider lifecycle

The accepted lifecycle after this amendment is:

`P-CONTRACT -> Owner merge -> OFFLINE IMPLEMENTATION -> QA -> REVIEW -> Owner merge -> V-CONTRACT -> Owner merge -> BOUNDED CONNECTED SMOKE -> CONNECTED QA/REVIEW -> Owner closeout -> explicit live worker mode -> STUDIO-009E routing eligibility -> STUDIO-009F full integrated acceptance`

Rules:

- every real provider still requires its own accepted `STUDIO-009P-*` child;
- every connected validation requires a separate `STUDIO-009V-*` child or provider-specific live-extension contract;
- a `P-*` merge never implies connected authority;
- a `V-*` contract cannot exist before the corresponding offline implementation, QA, Review, and Owner merge are durable;
- provider identity, model identity, host/transport identity, credential lineage, data class, quota, budget, and kill-switch evidence remain exact and fail closed;
- STUDIO-009E controls automatic routing/failover only after providers are independently validated and explicitly routing-eligible;
- STUDIO-009F remains the full end-to-end multi-provider/multi-repository acceptance gate, not the first API-call gate.

## 4. Progressive live states

The live layer introduced by later implementation must distinguish at least these states:

- `DISABLED` — offline metadata/adapter may exist; no real credential resolution, network, or model call.
- `LIVE_VALIDATION_READY` — offline implementation, QA, Review, and Owner merge are durable; a separate connected-validation contract is still required before network use.
- `LIVE_VALIDATED` — bounded real endpoint/model/credential-lineage validation passed with accepted zero-cost evidence. This state does not broaden the provider's accepted data classifications.
- `LIVE_SHADOW_WORKER` — may receive explicitly selected work within accepted data policy and return analysis or candidate patches into temporary evidence; no repository credential, commit, push, merge, deployment, publication, or direct canonical write.
- `LIVE_BOUNDED_WORKER` — may participate only in an explicit Work Order through the existing STUDIO-007 writer-claim/worktree/path boundary; provider output remains mediated by the local harness and never grants direct-main or merge authority.
- `ROUTING_ELIGIBLE` — may be selected automatically only by accepted STUDIO-009E policy after quality, data, quota, cost, and reliability gates pass.
- `PAUSED` / `REVOKED` — immediately ineligible. Revocation dominates stale approvals.

These states are not interchangeable with the STUDIO-009D offline onboarding states. The later live implementation must maintain an explicit boundary between offline eligibility and connected authority.

## 5. First connected-validation safety envelope

The first connected validation for any provider must be narrower than normal work:

- PUBLIC/SYNTHETIC prompts only;
- exactly one accepted provider/model/host/transport lineage;
- maximum 3 real requests in the initial smoke;
- concurrency exactly 1;
- automatic retry exactly 0;
- bounded request/output sizes defined by the provider-specific V contract;
- credential values never appear in repository files, prompts, model output, traces, evidence, logs, exceptions, memory, URLs, or command lines;
- transport/model identity must be verified from accepted configuration and transport metadata, not model-generated claims;
- quota/rate/capacity evidence must be captured when exposed by the provider;
- observed spend must remain zero and no paid fallback, credit purchase, auto-recharge, paid tier, or billing broadening is allowed;
- browser, remote MCP, provider tools, code execution, search grounding, URL context, storage, external write, deployment, and publication are disabled unless separately contracted;
- kill switch and credential revocation evidence are required before the provider can be considered live-validated;
- any unexpected redirect/host, model mismatch, data-policy violation, secret exposure, paid-plan requirement, or unauthorized tool/path request fails closed.

## 6. Quality-first worker gate

HTTP success is not sufficient for worker authority.

Before promotion from `LIVE_VALIDATED` to `LIVE_SHADOW_WORKER` or `LIVE_BOUNDED_WORKER`, provider-specific evaluation must measure usefulness for GAME tasks, including correctness, instruction discipline, relevant-source recall where applicable, structured-output validity, reliability, and human correction burden.

Quota conservation must not justify repeatedly using a provider that fails accepted quality gates. No unbounded automatic retry loop is authorized by this amendment.

## 7. P-01 and P-02 disposition

- STUDIO-009P-01 Groq is already COMPLETE through merged offline closeout. This amendment permits a later `STUDIO-009V-01` / equivalent live-extension contract; it does not activate Groq by itself.
- STUDIO-009P-02 Cloudflare Workers AI is already COMPLETE through merged offline closeout. This amendment permits a later `STUDIO-009V-02` / equivalent live-extension contract; it does not activate Cloudflare by itself.
- both providers remain DISABLED for connected execution until their own V-track authority becomes durable.

## 8. Future P-03+ provider slots

This amendment does **not** select or reserve the identity of P-03, P-04, P-05, or any later provider/model.

Historical planning documents, chat decisions, candidate lists, benchmarks, or provider popularity do not grant provider authority. Each future provider/model must be revalidated against current official evidence and accepted through its own `STUDIO-009P-*` contract.

## 9. STUDIO-009E after the amendment

STUDIO-009E becomes the automatic policy-routing and failover layer over already validated providers. It may consume immutable connected-validation evidence but may select only providers explicitly marked `ROUTING_ELIGIBLE` by accepted policy.

STUDIO-009E must not convert mere API reachability into routing authority and must retain MANUAL/FAKE as the deterministic zero-network fallback.

## 10. STUDIO-009F after the amendment

STUDIO-009F becomes full integrated studio acceptance covering the real queue/dispatcher, context, repository, provider, routing/failover, writer-claim/worktree, handoff, QA, Review, trace, kill switch, rollback, and Owner disposition path.

Provider calls may already have been independently validated before STUDIO-009F, but STUDIO-009F remains required before GAME can claim full connected multi-provider acceptance.

## 11. Contract-only boundary

This contract PR may modify only the exact amendment/reconciliation paths authorized by the runner.

It must not create the later live runtime, schemas, validators, fixtures, provider transports, provider SDKs, credential resolution, network calls, routing code, Unity integration, game-production code, or nonzero budget.

The separately accepted `tasks/STUDIO-009R-01-IMPLEMENTATION.md` controls later offline implementation scope.

## 12. Acceptance

Contract acceptance requires:

- exact main baseline verification;
- exact contract path allowlist;
- retained deterministic tests PASS;
- `git diff --check` PASS;
- Rules CI success on the immutable contract head;
- no provider/network/account/credential/store/tool/routing/connected-execution activity;
- spend = ZERO;
- separate Studio Owner decision to merge the contract PR.

The contract becomes durable only when merged.
