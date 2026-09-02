# STUDIO-009B fixtures

These fixtures exercise the deterministic repository registry and disabled
GitHub connector. They are test data only and do not contain usable
credentials or authorize a live repository connection.

Positive fixtures:
- `valid-disabled-repository.json`
- `valid-read-only-repository.json`
- `valid-pr-write-operation.json`

Negative fixtures:
- `invalid-embedded-credential.json`
- `invalid-unapproved-repository.json`
- `invalid-default-branch-write.json`
- `invalid-path-escape.json`
- `invalid-mutable-revision.json`
- `invalid-missing-owner-evidence.json`
- `invalid-unsafe-github-url.json`

The write-operation fixture is bound in tests to a deterministic PR_WRITE
variant of the accepted STUDIO-009A write boundary. No network transport is
created or invoked.
