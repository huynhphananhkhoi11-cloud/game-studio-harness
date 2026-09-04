# STUDIO-009R deterministic live-validation fixtures

These fixtures are synthetic metadata only. They do not name or authorize a real provider, endpoint, credential, account, model call, routing decision, Unity action, or spend.

- `valid-live-validation-ready.json`: accepted offline lineage ready for a later V-track contract.
- `valid-live-validated.json`: synthetic representation of accepted connected-validation evidence.
- `valid-shadow-worker.json`: synthetic live shadow-worker state with no repository write authority.
- `invalid-unmerged-offline.json`: missing durable offline merge.
- `invalid-private-data.json`: broadens data beyond a PUBLIC-only parent policy.
- `invalid-nonzero-budget.json`: violates the zero-cost invariant.
- `invalid-routing-before-009e.json`: attempts routing eligibility without STUDIO-009E authority.
- `invalid-revoked-provider.json`: revoked state used to prove revocation dominance.
