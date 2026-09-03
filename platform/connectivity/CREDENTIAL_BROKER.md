# CREDENTIAL_BROKER

STUDIO-009C implements a deterministic credential-control core. It does **not**
connect to a production secret store and does not activate GitHub or provider
authentication.

## Trust boundary

The broker accepts credential **metadata only**. `auth_profile_ref`,
`secret_store_ref`, and `secret_locator_ref` are opaque identifiers. They must
never carry, encode, derive, concatenate, or disguise usable authentication
material.

Production credential values are forbidden from Git, prompts, model output,
memory, traces, logs, exceptions, CLI arguments, URLs, environment dumps, and
normalized broker results.

## Profile validation

`validate_credential_profile` enforces an exact metadata shape, bounded input
size/depth/nodes, valid Unicode, finite numbers, immutable canonical digest,
caller-supplied UTC chronology, lifecycle status, maximum lease duration, and
repository lineage.

For repository profiles the caller supplies the raw STUDIO-009B repository
record together with its accepted STUDIO-009A boundary and threat assessment.
STUDIO-009C calls the STUDIO-009B repository validator itself, then requires the
credential profile to match repository identity, record digest,
`auth_profile_ref`, and accepted boundary digest. A caller cannot substitute an
arbitrary "already normalized" dictionary. STUDIO-009C does not widen
repository permissions.

## Lease planning

`plan_credential_lease` binds a usable ACTIVE profile to one task/attempt,
queue/dispatch lineage, gate, trace, quota-budget evidence, Owner evidence,
subject, capability, purpose, caller-supplied time, and bounded replay evidence.
For repository use, the caller supplies the raw STUDIO-009B repository record,
operation envelope, boundary, and threat assessment. STUDIO-009C calls
`github_connector.plan_operation(...)` itself and proves that repository
identity, repository-record digest, operation digest, capability, caller-supplied
`as_of`, and task/attempt/queue/dispatch/writer/worktree/gate/trace/quota lineage
all match the revalidated operation. A caller cannot substitute a handcrafted
transport-plan object or stale operation envelope.

Write-capable GitHub capabilities require writer-claim and worktree evidence.
The monetary ceiling is integer zero. Lease duration is at most 3600 seconds
and can be shorter when the profile expires or reaches its rotation deadline.

Provider-targeted credential use remains unavailable in STUDIO-009C. Provider
identity and use remain gated by STUDIO-009D and provider-specific STUDIO-009P*
contracts.

## Fake broker

`FakeCredentialBroker` uses only an injected `FakeSecretStore`. Synthetic test
objects may exist in process memory, but are not serialized, logged, returned,
persisted, or placed in evidence. There is no production constructor.

Repeated use of the same idempotency key and same request digest returns the
same normalized lease without another fake-store access. Reuse with a different
request digest fails closed.

## Runtime prohibition

The implementation performs no environment credential lookup, `.env` parsing,
OS keychain/Credential Manager access, browser session lookup, token-file
access, cloud vault/KMS/HSM access, GitHub App/PAT/OAuth/SSH integration,
provider SDK/API/CLI use, socket/HTTP/GraphQL call, subprocess credential
retrieval, or system-clock acceptance decision.

Live authentication remains separately gated by later STUDIO-009F activation.
