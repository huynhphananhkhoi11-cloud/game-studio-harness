# SECRET_LIFECYCLE

STUDIO-009C models credential lifecycle as metadata and in-memory simulation
only. It does not rotate, revoke, mint, refresh, delete, or persist a real
credential.

## States

Credential profile states are:

- `DISABLED`
- `ACTIVE`
- `REVOKED`
- `ROTATION_REQUIRED`

Revocation dominates every other state. A revoked profile cannot be re-enabled
by the fake broker. Rotation-required and disabled profiles cannot issue leases.
An ACTIVE profile also becomes unusable when caller-supplied `as_of` reaches
its rotation deadline or expiry.

## Events

Credential lifecycle events contain metadata only and use these actions:

- `DISABLE`
- `ENABLE_ELIGIBLE`
- `REVOKE`
- `ROTATION_REQUIRED`
- `LEASE_ISSUED`
- `LEASE_EXPIRED`

Every event binds the profile identity/digest, optional lease identity,
Owner/control evidence, caller-supplied UTC time, and canonical digest.

## Lease lifetime

A lease is immutable, subject-bound, capability-bound, purpose-bound,
profile-bound, and request-bound. The implementation limit is one hour.
Profile maximum duration, rotation deadline, or profile expiry can make the
effective maximum shorter.

Lease expiry is simulated in memory. It does not trigger a real secret-store
mutation.

## Kill switch and reactivation

Disablement and revocation are fail-closed. Reactivation requires fresh Owner
evidence in a later accepted transition; the fake lifecycle cannot use stale
evidence to reactivate a revoked profile.

## Error and redaction hygiene

Public failures use stable codes with fixed safe messages. Untrusted values and
secret-like material are never echoed. `credential_redaction.py` provides
bounded pattern redaction for synthetic tests; it does not claim cryptographic
memory erasure or secure zeroization.
