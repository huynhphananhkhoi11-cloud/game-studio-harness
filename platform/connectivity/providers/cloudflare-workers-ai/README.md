# Cloudflare Workers AI provider child — STUDIO-009P-02 / STUDIO-009V-02

The STUDIO-009P-02 offline/synthetic child remains complete and its provider profile remains `DISABLED`.
STUDIO-009V-02 adds a separately governed bounded connected-validation path for exact model `@cf/nvidia/nemotron-3-120b-a12b` through direct host `api.cloudflare.com` and `/client/v4/accounts/{ACCEPTED_ACCOUNT_ID}/ai/v1/chat/completions`.

Current V-02 envelope: PUBLIC/SYNTHETIC only; max 3 requests; concurrency 1; retry 0; 2,000-Neuron campaign ceiling; money ceiling 0; maximum promotion `LIVE_VALIDATED`.

A dedicated Cloudflare session bridge handles Owner-interactive Account ID/API-token input only after a later Owner connected preflight. The Groq V-01 bridge is not modified.

At this implementation checkpoint the sidecar live state is only `LIVE_VALIDATION_READY`. No real Account ID or API token has been entered and no Cloudflare/model network call has occurred.

AI Gateway, Workers Paid, Unified Billing, prepaid credits, storage, tools, routing/failover, worker authority, deployment and publication remain forbidden.
