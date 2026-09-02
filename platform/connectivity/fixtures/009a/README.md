# STUDIO-009A fixtures

These fixtures exercise the deterministic integration boundary without connecting a repository or AI provider.

- `valid-read-only-boundary.json`: accepted read-only boundary with no writer evidence.
- `valid-branch-write-boundary.json`: accepted isolated branch-write boundary with writer and worktree evidence.
- `valid-threat-assessment.json`: all nine required threats bound to the read-only boundary digest.
- `invalid-*.json`: one fail-closed policy violation per fixture.

All timestamps and `as_of` values are caller-supplied. All money values in valid records are integer zero. Provider identity, credentials, endpoints, network operations, and external execution are deliberately absent.
