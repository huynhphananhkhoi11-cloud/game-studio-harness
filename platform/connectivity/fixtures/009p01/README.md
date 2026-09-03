# STUDIO-009P-01 synthetic fixtures

All fixtures in this directory are synthetic public metadata.

They contain no credential values and trigger no network/provider activity.

- `valid-*`: contract/profile/model metadata that remains DISABLED/DECLARED.
- `invalid-*`: one-boundary negative fixtures for provider-specific fail-closed tests.

The exact model allowlist is `openai/gpt-oss-120b`; any other model is invalid for this child even if Groq offers it elsewhere.
