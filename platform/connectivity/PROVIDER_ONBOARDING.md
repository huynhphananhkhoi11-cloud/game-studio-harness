# STUDIO-009D Provider Onboarding Framework

STUDIO-009D defines a deterministic, provider-neutral onboarding boundary. It prepares metadata needed by later provider-specific child contracts without connecting to any provider.

## Authority boundary

This framework does not approve or activate a real provider, model, endpoint, account, credential, network transport, routing decision, connected execution, or spend. `ELIGIBLE` means only that metadata is structurally eligible for later provider-specific work.

Every real provider still requires:

1. a separately merged `STUDIO-009P*` child contract;
2. provider-specific implementation and evidence;
3. STUDIO-009E policy routing where applicable; and
4. explicit STUDIO-009F connected-pilot activation.

The Studio Owner remains the final authority.

## Records

### Provider profile

A provider profile binds opaque references for provider identity, transport, credential lineage, data policy, quota policy, zero-budget policy, kill switch, incident response, rollback, Owner approval, allowed data classifications, and allowed capabilities.

Allowed lifecycle states are `CANDIDATE`, `DISABLED`, `ELIGIBLE`, `PAUSED`, `REVOKED`, and `EXPIRED`. `ACTIVE` is forbidden in STUDIO-009D.

### Child-contract evidence

One evidence record binds exactly one provider profile to one `STUDIO-009P*` child identifier. It records Owner acceptance and evidence references for provider identity, transport, credential lineage, model policy, capability policy, data export, quota, budget, kill switch, incident response, and rollback.

Synthetic evidence is distinguished from real-provider evidence. The generic framework never upgrades either class to a connected state.

### Model profile

A model profile binds one opaque model identity/version policy to one provider profile and one child-contract evidence digest. Model data classifications and request/output bounds cannot broaden the parent provider profile.

### Capability binding

A capability binding attaches one declared capability to one accepted model profile. Capability, data classifications, request size, and output size may only narrow existing provider/model scope.

### Eligibility plan

`plan_eligibility` returns immutable metadata only. It can return `ELIGIBLE` or `INELIGIBLE` with a stable refusal code. It never creates transport, resolves credentials, routes work, calls a provider, or authorizes spend.

### Lifecycle events

Metadata-only events are limited to:

- `REGISTER_CANDIDATE`
- `MARK_ELIGIBLE`
- `PAUSE`
- `REVOKE`
- `EXPIRE`

Events cannot create `ACTIVE`, restore a revoked provider, change provider identity, extend expiry, or broaden scope.

## Determinism and safety

- Caller-supplied second-precision UTC is required; no system clock is consulted for acceptance.
- JSON duplicate keys, non-finite numbers, excessive byte/depth/node size, malformed Unicode, unknown fields, secret-like material, and invalid canonical digests fail closed.
- Stable public errors do not echo untrusted values.
- Normalized outputs contain metadata only.
- Money ceiling is exactly integer zero in STUDIO-009D.
- No environment, `.env`, keyring, Credential Manager, browser session, vault/KMS/HSM, provider SDK/API/CLI, HTTP client, socket, subprocess provider call, account discovery, billing discovery, or model call exists in production source.

## Synthetic fixtures

All committed STUDIO-009D fixtures use clearly synthetic, non-routable identities. They are regression evidence only and do not name or authorize a real provider.
