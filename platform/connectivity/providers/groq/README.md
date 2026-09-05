# Groq provider integration — STUDIO-009P-01

Status: OFFLINE / SYNTHETIC IMPLEMENTATION ONLY

Contract baseline: `2d2ec86ab5a6f66ffbb102154cff1a8f0d472929`

This directory implements deterministic Groq-specific metadata and normalization for the merged `STUDIO-009P-01` child contract. It does **not** authenticate, resolve a credential, open network transport, call Groq, call a model, execute a tool, route production work, or spend money.

## Frozen first-child scope

- Provider: GroqCloud / Groq API
- Model allowlist: `openai/gpt-oss-120b`
- Canonical future base URL: `https://api.groq.com/openai/v1`
- Data class: `PUBLIC` plus synthetic fixture data only
- ZDR: required before any STUDIO-009F connected pilot
- Money ceiling: integer `0`
- Local tool requests: may be normalized, never executed here
- Built-in tools / Remote MCP / Compound: forbidden by this implementation

## Official evidence snapshot

Verified on 2026-09-03 from Groq documentation:

- Rate limits: 30 RPM / 1,000 RPD / 8,000 TPM / 200,000 TPD for `openai/gpt-oss-120b`
- Rate-limit exhaustion: HTTP 429
- OpenAI-compatible base URL: `https://api.groq.com/openai/v1`
- Local tool calling: execution remains in application code
- Zero Data Retention: available through Groq Data Controls

Authoritative source URLs remain pinned in `tasks/STUDIO-009P-01.md`.

## Safety boundary

The adapter imports no provider SDK and no network client. It never reads environment variables, `.env`, keyrings, browser stores, command lines, or credential values. Historical P-01 statement retained for provenance: "STUDIO-009F remains the only connected activation gate." That statement governed the original offline child. Merged STUDIO-009R-01 plus STUDIO-009V-01 now supersede it only for bounded provider-specific connected validation; STUDIO-009F remains the later full integrated acceptance gate.


## STUDIO-009V-01 bounded connected validation

The merged V-01 contract permits preparation of a direct standard-library HTTPS transport and a session-only Owner-interactive credential bridge. This implementation checkpoint performs no Groq call. The provider remains DISABLED for ordinary connected work; only a later explicit bounded smoke may move it to LIVE_VALIDATED, and routing/worker authority remains unavailable.
