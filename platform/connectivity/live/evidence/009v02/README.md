# STUDIO-009V-02 connected evidence staging

At this checkpoint `provider-live-state.json` is only `LIVE_VALIDATION_READY`. Connected validation and quality evidence remain pending.
No raw Account ID, API token, Authorization header, provider error body, private prompt, or raw model output may be committed.
No real Cloudflare/provider/model call has occurred. A later bounded smoke requires a separate Studio Owner connected preflight.

## Owner connected preflight checkpoint
Token `GAME-STUDIO-009V-02` was created with Workers AI Read + Workers AI Edit scoped to the selected account. Raw Account ID and token remain local and are not persisted.
Workers AI usage was not observable before first inference, so no headroom value is invented. Workers Free, MONEY_CEILING=0, and fail-closed handling of internal code 3036 remain binding.
This checkpoint authorizes zero real requests.
<!-- STUDIO-009V-02-OWNER-CONNECTED-PREFLIGHT-0003 -->

## Owner bounded-smoke authorization

Studio Owner explicitly authorized the exact V-02 real-smoke envelope:

- maximum real requests: 3;
- concurrency: 1;
- automatic retry: 0;
- campaign neuron ceiling: 2,000;
- money ceiling: 0 USD;
- provider/model/host/data/tool/storage/routing boundaries remain unchanged.

Authorization ref: `owner-authorization:cloudflare-v02-6a38a1fb1c03`.

This checkpoint records authority only. It performs zero Cloudflare calls and does not request or persist the Account ID/API token. The subsequent smoke runner must bind to the immutable authorization head and exact-head Rules CI before hidden credential input.

<!-- STUDIO-009V-02-OWNER-BOUNDED-SMOKE-AUTHORIZATION-0004 -->

## Corrected bounded real-smoke PASS evidence
Campaign `cloudflare-v02-405f777851bb5ca0` completed exactly 3 requests / 3 network successes using `GAME-STUDIO-009V-02-RETRY`.
The preflight evidence had recorded `GAME-STUDIO-009V-02`; Owner later clarified the actual smoke token name. This correction changes token lineage only, not provider/model/request results.
Because the `GAME-STUDIO-009V-02-RETRY` secret appeared in a chat image, Owner revoked it after the smoke before this evidence checkpoint. No token secret, raw Account ID, or raw provider output is persisted.
Reserved Neurons: 1,536; estimated Neurons from returned token usage: 37; quality PASS; human correction 0. Provider-observed Neurons and spend remain UNCONFIRMED. No additional real request is authorized.
<!-- STUDIO-009V-02-SMOKE-EVIDENCE-CORRECTED-0005B -->

## Owner post-smoke Neuron / spend confirmation

Owner-observed provider evidence after the bounded smoke:

- Workers AI provider-observed Neurons today: `35.18`;
- GAME token-usage estimate retained separately: `37`;
- Workers plan: `FREE`;
- Workers Paid: `false`;
- payment method on file: `false`;
- Billable usage page: `NO_DATA`;
- Invoices: `NONE`;
- billable charge observed: `0 USD`;
- observed spend for the V-02 money-ceiling gate: `0 USD`;
- spend basis: `OWNER_OBSERVED_NO_BILLABLE_USAGE_NO_INVOICE_FREE_PLAN_NO_PAYMENT_METHOD`;
- cost-metric display is not reinterpreted or invented: `UNCONFIRMED`.

`35.18` is the provider-observed Neuron value. `37` remains only the GAME estimate from returned token usage. No additional request is authorized.

<!-- STUDIO-009V-02-OWNER-NEURON-SPEND-CONFIRMATION-0005C -->
