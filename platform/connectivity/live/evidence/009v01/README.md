# STUDIO-009V-01 connected evidence staging

This directory is the sanitized evidence staging area for Groq V-01.

At the offline implementation checkpoint:

- `provider-live-state.json` is valid only through `LIVE_VALIDATION_READY`;
- `connected-validation.json` is deliberately `PENDING_REAL_SMOKE` and is not valid connected evidence;
- `quality-evaluation.json` is deliberately pending;
- no API key, raw Authorization header, raw provider error body, private prompt, or raw model output may be committed here.

A later bounded smoke may update these files only after the Studio Owner confirms Free tier and ZDR, supplies the key through hidden session-only input, and the smoke remains within the merged V-01 envelope.

## Failed authentication campaign and fresh retry authorization

- Failed campaign: `groq-v01-782697ab855de1bd`
- Implementation head: `c50469518be364476aee0ded221eabe7dab2f878`
- Reserved/attempted requests: `1`
- Failed slot: `1` / `STRUCTURED_OUTPUT`
- Result: `AUTH_FAILED`
- Automatic retry: `0`
- Remaining requests in failed campaign are NOT authorized.
- API key value persisted: `false`
- Raw provider output persisted: `false`
- Observed spend: `UNCONFIRMED`
- Studio Owner acknowledged the failed campaign.
- Studio Owner confirmed the failed key was revoked.
- Studio Owner confirmed a new key was created in `Default Project`.
- Studio Owner authorized one fresh retry campaign under the same 3-request / concurrency-1 / retry-0 / zero-money envelope.
- Provider live state remains `LIVE_VALIDATION_READY`.
<!-- STUDIO-009V-01-RETRY1-AUTHORIZATION-0003A -->
