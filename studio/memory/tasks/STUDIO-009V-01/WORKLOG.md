# STUDIO-009V-01 WORKLOG

memory_schema_version: 1

task_id: STUDIO-009V-01
package_path: studio/memory/tasks/STUDIO-009V-01
canonical_task_contract: tasks/STUDIO-009V-01.md

## 2026-09-05 — Contract preparation

- Durable STUDIO-009P-01 offline closeout merge verified at `1b75f250169ccdab3e2d67cbac4047253792c4a7`.
- Durable STUDIO-009R-01 closeout merge verified at `11c2c2d4a35f37c5712376a3e7b16ca22d848bc7`.
- Current Groq official evidence re-verified for `openai/gpt-oss-120b`, `api.groq.com/openai/v1`, Free Plan limits, ZDR, billing-tier behavior, and supported tool capabilities.
- Contract keeps `MONEY_CEILING=0`.
- First smoke is bounded to max 3 requests, concurrency 1, retry 0, PUBLIC/SYNTHETIC only, no tools/browser/code/MCP/search/storage/external write.
- V-01 promotion ceiling is `LIVE_VALIDATED`; no worker or routing authority is granted.
- Contract preparation performs no Groq/provider/model/credential runtime activity and no spend.

## 2026-09-05 — Offline V-01 implementation checkpoint

- Contract PR #59 merged at `2b811d7ac64e88c396f691cec940ec68784b1457`.
- Reconciled Groq provider-specific activation policy from historical STUDIO-009F-only wording to the merged V-01 bounded-validation gate while preserving P-01 historical provenance.
- Added standard-library HTTPS transport, session-only hidden credential bridge, bounded smoke orchestrator, pending sanitized evidence staging, and deterministic hostile tests.
- No real API key was requested or resolved.
- No Groq/provider/model network request was executed.
- Provider live state is only `LIVE_VALIDATION_READY`.
- New tests: 48; retained live framework: 70; focused: 525; total: 922.
- MONEY_CEILING=0; provider/network/credential/routing/connected activity NONE; spend ZERO.
- Next gate is a separate Studio Owner Free-tier/ZDR connected preflight. The implementation Pull Request must remain unmerged until connected smoke, QA, Review, and Owner disposition complete.
<!-- STUDIO-009V-01-IMPLEMENTATION-CHECKPOINT-0002 -->

## 2026-09-05 — Connected-preflight hardening before first real request

- Independent review of PR #60 kept it unmerged.
- Hardened the smoke so every network request requires a caller-supplied durable reservation before I/O; a failed/crashed run therefore cannot safely reset the three-request campaign.
- Removed the premature `observed_spend=0` claim. Observed spend remains unknown until the Studio Owner checks Groq account evidence after the smoke.
- Added required Owner confirmation that `openai/gpt-oss-120b` is permitted for the active organization.
- Explicitly disables returned reasoning content with `include_reasoning=false`; no reasoning format is sent for GPT-OSS.
- Fixed stale STATE remaining-actions text from the already-merged contract stage.
- No real API key was requested; no Groq call occurred; live state remains `LIVE_VALIDATION_READY`.
- New tests now total 50 over pre-V-01 baseline; focused 527; total 924.
<!-- STUDIO-009V-01-PREFLIGHT-HARDENING-0002A -->

## 2026-09-05 — Failed auth campaign reviewed; RETRY1 authorized

- Durable local ledger `groq-v01-782697ab855de1bd` was reviewed.
- Exactly one request slot was reserved and attempted.
- Slot 1 (`STRUCTURED_OUTPUT`) failed with safe code `AUTH_FAILED`.
- Concurrency remained 1 and automatic retry remained 0.
- No API key value or raw provider output was persisted.
- The failed campaign is terminal; its remaining two slots are not authorized for use.
- Studio Owner acknowledged the failure, revoked the failed key, created a new key in `Default Project`, and authorized one fresh retry campaign.
- RETRY1 preserves max 3 requests, concurrency 1, retry 0, PUBLIC/SYNTHETIC only, `MONEY_CEILING=0`.
- Provider live state remains `LIVE_VALIDATION_READY`.
- Observed spend remains `UNCONFIRMED`.
- No Groq/provider/model request occurred during this authorization checkpoint.
<!-- STUDIO-009V-01-RETRY1-AUTHORIZATION-0003A -->

## 2026-09-05 — RETRY1 bounded Groq connected smoke

- RETRY1 used the fresh Owner authorization checkpoint after the prior one-request `AUTH_FAILED` campaign; the old key was revoked and a new key was created in `Default Project`.
- Campaign `groq-v01-retry1-ac2943edca636f95` reserved every request durably before network I/O.
- Exactly 3 real PUBLIC/SYNTHETIC requests were issued sequentially.
- Concurrency was 1; automatic retry was 0.
- Exact model and transport identity gates passed.
- Fixed smoke quality probes passed with zero human correction.
- No raw model output or API key value was persisted to repository evidence.
- Provider live state remains `LIVE_VALIDATION_READY`.
- Observed spend is deliberately `UNCONFIRMED` until Studio Owner checks Groq Usage/Billing.
- No additional request is authorized. PR #60 remains unmerged.
<!-- STUDIO-009V-01-RETRY1-SMOKE-CHECKPOINT-0003B -->

## 2026-09-05 — Owner spend confirmation

- RETRY1 smoke had already completed with 3/3 quality-pass requests; no additional Groq request was made in this checkpoint.
- Studio Owner re-confirmed the active Groq account remains on the `FREE` tier.
- Groq Usage displayed `<0.01 USD` for `openai/gpt-oss-120b - on_demand`; this literal sub-cent usage-cost metric is preserved and is not rewritten as zero.
- Studio Owner confirmed no billable charge / amount due / paid-tier charge was observed.
- `observed_spend=0` is scoped to billable charge observed by the Owner.
- Provider live state remains `LIVE_VALIDATION_READY`; no routing or worker authority is granted.
- Next gate is independent Connected QA against the immutable spend-confirmed head.
<!-- STUDIO-009V-01-OWNER-SPEND-CONFIRMATION-0003C -->

## 2026-09-05 — Independent Connected QA

- Immutable spend-confirmed head reviewed: `2b803e9e6ad3e1e75432f61aefa161a1a9e64595`.
- QA result: `PASS`; blockers: `0`.
- Independent probes: `60`.
- Tests: `70` live / `527` focused / `924` total.
- Verified exact Groq/model/transport lineage, three-request RETRY1 envelope, cumulative four-request V-01 history, model/transport identity, PUBLIC-only classification, no paid fallback, secret/raw-output hygiene, zero automatic retry, and zero billable charge on Free tier.
- Preserved the literal `<0.01 USD` provider usage-cost metric as nonzero usage accounting while keeping observed billable spend at `0 USD`.
- No provider/Groq/model request, API-key input, routing, tool execution, MCP, or external capability occurred during QA.
- Provider live state remains `LIVE_VALIDATION_READY`.
- Next gate: independent Connected Review.
<!-- STUDIO-009V-01-CONNECTED-QA-CHECKPOINT-0003D -->

## 2026-09-05 — Independent Connected Review and Integration

- Immutable Connected-QA head reviewed: `1f31119f7f5d00db781f5fc60653312dfa25c7d3`.
- Review result: `APPROVE`; blockers: `0`.
- Independent review/integration probes: `80`.
- Tests: `70` live / `527` focused / `924` total.
- Confirmed the exact 20-path implementation scope and all live lineage/ceiling/budget/security constraints remain intact.
- Confirmed Connected QA reference `qa:connected-groq-v01-2b803e9e6ad3` is bound to immutable spend-confirmed head `2b803e9e6ad3e1e75432f61aefa161a1a9e64595` with 60 probes PASS.
- Confirmed RETRY1 used three successful requests after one separately authorized failed authentication campaign; cumulative V-01 history remains four real attempts without automatic retry.
- Confirmed account tier `FREE`, literal usage cost `<0.01 USD`, and observed billable charge `0 USD`.
- No Groq/provider/model request, API-key input, routing, external tool, MCP, deployment, publication, or nonzero billable spend occurred during Review.
- Provider remains `LIVE_VALIDATION_READY`.
- Next gate: Owner revocation of the temporary RETRY1 key plus final Owner disposition and LIVE_VALIDATED materialization.
<!-- STUDIO-009V-01-CONNECTED-REVIEW-CHECKPOINT-0003E -->

## 2026-09-05 — Studio Owner final V-01 disposition

- Immutable Connected-Review head accepted: `bfc08b636c79f6346cc2f63fc689f4551ed89799`.
- Studio Owner confirmed the temporary RETRY1 Groq API key was deleted/revoked from `Default Project`.
- Studio Owner final disposition: `ACCEPT_LIVE_VALIDATED`.
- Owner disposition ref: `owner-disposition:groq-v01-bfc08b636c79`.
- Revocation evidence ref: `revocation:groq-v01-retry1-key-owner-confirmed`.
- QA remained `PASS`; Review remained `APPROVE`; blockers remained `0`.
- Final `connected-validation.json` is an exact generic STUDIO-009R bound-evidence record; the prior rich staging record remains recoverable in immutable Git history.
- Provider state is materialized as `LIVE_VALIDATED` in PR #60 only; durability still requires manual Owner merge.
- Worker and routing authority remain `NONE`; STUDIO-009E/STUDIO-009F authority is not granted.
- No additional Groq/provider/model request, API-key input, routing, MCP, tool execution, deployment, publication, or nonzero billable spend occurred.
- Final tests: `70` live / `527` focused / `924` total.
<!-- STUDIO-009V-01-OWNER-DISPOSITION-CHECKPOINT-0003F -->

## 2026-09-05 — Merged V-01 implementation closeout

- Implementation PR #60 merged at `c1d640663d63c854fc6e2356837e7ad03ad83723` from final disposition head `bcab0d23ce6eed40dcbf2edd2c619d30e066506b`.
- Groq V-01 connected-validation result is `LIVE_VALIDATED`.
- Connected QA remained `PASS`; Connected Review remained `APPROVE`; Owner disposition remained `ACCEPT_LIVE_VALIDATED`.
- RETRY1 temporary API key was revoked before final disposition and no persistent Groq key is created by this closeout.
- Historical V-01 connected activity remains four total real attempts: one terminal `AUTH_FAILED` request in the failed campaign plus three successful RETRY1 smoke requests.
- Final validation evidence: 70 live tests / 527 focused / 924 total.
- Closeout itself performs zero provider calls, zero Groq network activity, zero API-key input, and zero additional billable spend.
- Groq keeps `LIVE_VALIDATED` only; worker authority `NONE`; routing authority `NONE`; no additional real request is authorized.
- Closeout becomes durable only after separate Studio Owner merge.
- Next after durable closeout: STUDIO-009V-02 Cloudflare connected-validation contract research.
<!-- STUDIO-009V-01-CLOSEOUT-CHECKPOINT-0004 -->
