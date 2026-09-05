# STUDIO-009V-02 connected evidence staging

At this checkpoint `provider-live-state.json` is only `LIVE_VALIDATION_READY`. Connected validation and quality evidence remain pending.
No raw Account ID, API token, Authorization header, provider error body, private prompt, or raw model output may be committed.
No real Cloudflare/provider/model call has occurred. A later bounded smoke requires a separate Studio Owner connected preflight.

## Owner connected preflight checkpoint
Token `GAME-STUDIO-009V-02` was created with Workers AI Read + Workers AI Edit scoped to the selected account. Raw Account ID and token remain local and are not persisted.
Workers AI usage was not observable before first inference, so no headroom value is invented. Workers Free, MONEY_CEILING=0, and fail-closed handling of internal code 3036 remain binding.
This checkpoint authorizes zero real requests.
<!-- STUDIO-009V-02-OWNER-CONNECTED-PREFLIGHT-0003 -->
