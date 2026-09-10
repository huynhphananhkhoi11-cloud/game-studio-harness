# Poolside direct provider profile — STUDIO-009P-04

This directory is the deterministic OFFLINE/SYNTHETIC implementation of the merged P-04 contract.

Provider: Poolside standalone hosted inference API
Exact model: `poolside/laguna-s-2.1`
Direct candidate base URL: `https://inference.poolside.ai/v1`
Chat path: `/v1/chat/completions`

Runtime state is deliberately `DISABLED`; model state is `DECLARED`; child evidence is `SYNTHETIC`.

This implementation performs no Poolside account/API-key lookup, no network request, no `pool` CLI execution, no tool/MCP/ACP/shell/file/browser/repository-write action, no routing/failover, and no spend.

Initial connected data authority remains PUBLIC/SYNTHETIC only. Current public free availability is dynamic (`Free to use for a limited time`) and must be re-proven at a separately merged V-04 connected preflight. Training opt-out does not broaden GAME data authority.

Rollback remains MANUAL/FAKE. V-03 NVIDIA remains independently frozen.
<!-- STUDIO-009P-04-IMPLEMENTATION-CHECKPOINT-0002 -->


## STUDIO-009V-04 offline live-validation readiness

V-04 contract merge: `a7beb556d19da1397cceb09431d47848e69c5b12`.

This provider remains not connected. The offline live implementation materializes only direct HTTPS transport code, a session-only Owner-interactive credential bridge, a durable three-request campaign ledger and kill switch, fixed PUBLIC/SYNTHETIC probes, `LIVE_VALIDATION_READY` policy/evidence placeholders, and deterministic hostile tests.

At this checkpoint:

- provider profile remains `DISABLED`;
- historical P-04 policy/config evidence remains unchanged;
- connected execution remains false;
- `pool` CLI remains disabled;
- tools/MCP/ACP/shell/file/browser/repository write/routing remain disabled;
- current account-level USD 0 eligibility must be re-proved at Owner connected preflight;
- a server-side validation-key revocation/deletion/invalidation path must be proved before key input;
- no Poolside API key has been created/input by this implementation;
- no Poolside/Laguna request has occurred;
- spend remains USD 0.

Passing offline tests does not authorize a provider call.

<!-- STUDIO-009V-04-OFFLINE-LIVE-IMPLEMENTATION-CHECKPOINT-0002 -->
