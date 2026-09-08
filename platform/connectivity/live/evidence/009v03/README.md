# STUDIO-009V-03 NVIDIA NIM connected-validation evidence

This directory is materialized at the **offline live-implementation** checkpoint.

At this checkpoint:

- `provider-live-state.json` is valid only through `LIVE_VALIDATION_READY`;
- `connected-validation.json` is deliberately `PENDING_REAL_SMOKE`;
- `quality-evaluation.json` is deliberately `PENDING_REAL_SMOKE`;
- no NVIDIA API key, Authorization value, provider error body, private prompt, raw model output, account-private data, or billing-private data may be committed;
- no real NVIDIA request has occurred;
- observed spend is not fabricated;
- routing authority remains absent.

A later Owner connected preflight must re-prove current Free Endpoint / account entitlement / no-paid-path / revocation conditions before any session credential input.

The real smoke is capped at three PUBLIC/SYNTHETIC sequential requests, retry 0, and money ceiling USD 0.
