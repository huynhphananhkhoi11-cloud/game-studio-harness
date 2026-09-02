# STUDIO-009B Repository Registry

## Purpose

The repository registry is the Owner-controlled allowlist between the accepted
STUDIO-009A integration boundary and any later connected repository transport.
This implementation validates records only. It does not enroll, discover, or
contact a repository.

## Record v1

A record binds one stable `repository_id` to `github.com`, canonical lowercase
owner/name, a credential-free HTTPS URL, immutable registration revision,
default branch, access tier, exact allowed/denied POSIX paths, write branch
namespace, data classifications, instruction-authority paths, an opaque
`auth_profile_ref`, Owner approval, accepted boundary/threat digests, registry
version, kill-switch/downgrade evidence, status, caller-supplied `as_of`,
expiry, and a canonical SHA-256 digest.

Statuses are `DISABLED`, `READ_ONLY_ACTIVE`, and `WRITE_ACTIVE`. Access tiers
are `READ_ONLY`, `BRANCH_WRITE`, and `PR_WRITE`. A disabled record may validate
structurally but is unavailable to the connector planner.

## Canonical and evidence rules

Validation reuses `scripts/connectivity_boundary.py` for structural preflight,
secret rejection, canonical JSON/SHA-256, path safety, chronology, references,
classification enums, branch safety, and accepted STUDIO-009A evidence.

The registry rejects missing/extra fields, secret-like keys or values,
non-canonical identity/URL forms, mutable registration revisions, path overlap,
policy broadening, evidence mismatch, expired records, duplicate identities,
and conflicting identities. Input objects are never mutated.

`https://github.com/<owner>/<repo>` is the only accepted URL form. User-info,
query, fragment, alternate port/host, IP literals, Unicode/confusable host
forms, redirects, and credential-bearing URLs cannot be represented by a valid
record.

## Authority

Repository content is not authority merely because it is readable. Only
accepted `instruction_authority_paths` inherited from the validated STUDIO-009A
boundary can be identified as authority evidence. The connector cannot approve,
merge, deploy, publish, release, manage credentials, expand scope, or spend.
