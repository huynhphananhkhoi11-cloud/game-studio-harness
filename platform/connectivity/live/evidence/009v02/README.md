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

## Connected QA PASS

Independent Connected QA reviewed immutable head `a7d8933418d6dbb2102a85b984ecec77f0c0b3a4`.

- QA ref: `qa:connected-cloudflare-v02-a7d8933418d6`;
- result: `PASS`;
- blockers: `0`;
- independent semantic probes: `60`;
- retained tests: `20` smoke / `70` live / `592` focused / `989` total;
- Cloudflare provider calls during QA: `0`;
- Cloudflare network activity during QA: `NONE`;
- Account ID input during QA: `NONE`;
- API-token input during QA: `NONE`;
- provider state remains `LIVE_VALIDATION_READY`;
- no additional real request is authorized.

Connected QA does not promote the provider. The next independent gate is Connected Review & Integration.

<!-- STUDIO-009V-02-CONNECTED-QA-CHECKPOINT-0005D -->

## Connected Review & Integration APPROVE

Independent Connected Review reviewed immutable Connected-QA head `1564c628a8c8312bb028de6c2e329c2674becb51`.

- review ref: `review:connected-cloudflare-v02-1564c628a8c8`;
- result: `APPROVE`;
- blockers: `0`;
- independent semantic/integration probes: `81`;
- retained tests: `20` smoke / `70` live / `592` focused / `989` total;
- Cloudflare provider calls during Review: `0`;
- Cloudflare network activity during Review: `NONE`;
- Account ID input during Review: `NONE`;
- API-token input during Review: `NONE`;
- provider state remains `LIVE_VALIDATION_READY`;
- worker authority remains `NONE`;
- routing authority remains `NONE`;
- no additional real request is authorized.

Review approval is not final provider promotion and is not merge authority. The next gate is explicit Studio Owner final disposition.

<!-- STUDIO-009V-02-CONNECTED-REVIEW-CHECKPOINT-0005E -->

## Owner final disposition — ACCEPT LIVE_VALIDATED

Studio Owner explicitly accepted Cloudflare V-02 after Connected QA PASS and Connected Review APPROVE.

- Owner disposition ref: `owner-disposition:cloudflare-v02-98699b6d605e`;
- final connected-validation ref: `connected-validation:cloudflare-v02`;
- final provider live state: `LIVE_VALIDATED`;
- bounded smoke: exactly `3` requests, concurrency `1`, retry `0`;
- provider-observed Neurons: `35.18`; GAME historical estimate: `37`;
- observed spend: `0 USD`;
- exposed smoke-token revocation: confirmed;
- Connected QA: `PASS`; Connected Review: `APPROVE`;
- worker authority: `NONE`; routing authority: `NONE`; AI Gateway authority: `NONE`;
- additional real-request authority: `NONE`; money ceiling: `0 USD`.

The final `connected-validation.json` uses the exact generic STUDIO-009R schema. Rich smoke/QA/Review history remains durable in prior commits, this README, `quality-evaluation.json`, and task memory.

This checkpoint does not merge PR #64. Owner merge is the next gate.

<!-- STUDIO-009V-02-OWNER-FINAL-DISPOSITION-0005F -->

## Post-merge credential cleanup correction

After PR #64 was merged, Studio Owner reviewed Cloudflare **My Profile → API Tokens** and confirmed the page showed **No API tokens**.

- `GAME-STUDIO-009V-02`: `DELETED`;
- `GAME-STUDIO-009V-02-RETRY`: `DELETED`;
- active V-02 User API validation tokens observed: `NONE`;
- all V-02 validation credentials: `INACTIVE`;
- corrected revocation evidence ref: `revocation:cloudflare-v02-all-validation-tokens-owner-confirmed`;
- final provider state remains `LIVE_VALIDATED`;
- worker/routing/AI Gateway authority remain `NONE`;
- additional real-request authority remains `NONE`;
- money ceiling remains `0 USD`.

The Cloudflare **Global API Key** visible on the page is outside V-02 credential lineage. V-02 did not use, reveal, rotate, or delete that key, and this correction grants it no authority.

This correction changes credential-cleanup evidence only. It does not rerun smoke, call Cloudflare, create a token, broaden provider authority, or alter the validated model/transport/data envelope.

<!-- STUDIO-009V-02-POST-MERGE-CREDENTIAL-CLEANUP-0006B -->
