# STUDIO-009V-01 connected evidence staging

This directory is the sanitized evidence staging area for Groq V-01.

At the offline implementation checkpoint:

- `provider-live-state.json` is valid only through `LIVE_VALIDATION_READY`;
- `connected-validation.json` is deliberately `PENDING_REAL_SMOKE` and is not valid connected evidence;
- `quality-evaluation.json` is deliberately pending;
- no API key, raw Authorization header, raw provider error body, private prompt, or raw model output may be committed here.

A later bounded smoke may update these files only after the Studio Owner confirms Free tier and ZDR, supplies the key through hidden session-only input, and the smoke remains within the merged V-01 envelope.
