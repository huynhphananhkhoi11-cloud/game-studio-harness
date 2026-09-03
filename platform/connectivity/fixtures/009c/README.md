# STUDIO-009C fixtures

These fixtures exercise only credential metadata and deterministic fake-store
planning. No file contains a usable production credential.

Positive fixtures:
- `valid-disabled-profile.json`
- `valid-repository-profile.json`
- `valid-lease-request.json`

Negative fixtures cover embedded secret-field rejection, repository subject
lineage, expiry, revoked-use rejection, missing Owner evidence, scope
broadening, and replay chronology.

`invalid-embedded-secret.json` uses the literal synthetic marker
`NOT_A_REAL_TOKEN_FIXTURE`. The rejection is driven by the forbidden field name,
not by a production-shaped token value.
