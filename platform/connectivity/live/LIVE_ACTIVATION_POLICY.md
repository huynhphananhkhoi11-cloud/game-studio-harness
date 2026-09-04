# GAME Progressive Live Validation Policy — STUDIO-009R-01

Status: OFFLINE FRAMEWORK ONLY
Authority: `tasks/STUDIO-009R-01.md` and `tasks/STUDIO-009R-01-IMPLEMENTATION.md`

## Purpose

This layer validates metadata for progressive provider activation without making provider calls. It separates offline provider acceptance from provider-specific connected validation and from later automatic routing.

## State boundary

`DISABLED -> LIVE_VALIDATION_READY -> LIVE_VALIDATED -> LIVE_SHADOW_WORKER -> LIVE_BOUNDED_WORKER -> ROUTING_ELIGIBLE`

`PAUSED` and `REVOKED` are fail-closed states. Revocation dominates stale approval. `ROUTING_ELIGIBLE` requires explicit later STUDIO-009E authority and cannot be synthesized by this implementation.

The STUDIO-009D `ELIGIBLE` state remains offline onboarding metadata and is not a live state.

## Connected-validation envelope

The first provider-specific connected validation must be separately authorized by a merged STUDIO-009V contract and must remain narrower than ordinary work:

- PUBLIC/SYNTHETIC input only;
- exact provider/model/transport/credential-reference lineage;
- maximum three requests;
- concurrency one;
- automatic retry zero;
- bounded request and output sizes;
- zero spend and no paid fallback;
- transport and model identity verified from accepted metadata, never model text;
- kill-switch and revocation evidence present;
- tools, browser, remote MCP, code execution, search grounding, storage, external write, deployment and publication disabled unless separately contracted.

## Worker modes

`LIVE_SHADOW_WORKER` has no repository write authority. It may return analysis or candidate patch material only through the local harness.

`LIVE_BOUNDED_WORKER` requires an explicit Work Order, existing writer claim, isolated worktree, exact path allowlist and local mediation. It never grants direct-main, merge, deployment, publication, secret access, arbitrary tools or budget increase.

## Quality rule

API success is not a worker-quality pass. Promotion requires provider-specific evaluation of correctness, instruction discipline, structured-output validity, reliability, source recall where applicable and human correction burden. Quota conservation does not justify repeated use of a low-quality provider.

## Runtime prohibition

The generic STUDIO-009R implementation makes zero provider/network/account/credential/tool/routing/Unity calls and spends zero money. It only validates deterministic metadata for later V-track execution.
