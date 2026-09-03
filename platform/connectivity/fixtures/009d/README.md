# STUDIO-009D synthetic fixtures

These fixtures contain provider-neutral synthetic metadata only.

- `valid-disabled-provider.json` — synthetically valid DISABLED provider profile.
- `valid-eligible-provider.json` — synthetically valid ELIGIBLE provider profile. ELIGIBLE is not connected/live.
- `valid-model-profile.json` — synthetic model profile bound to the valid eligible provider and child evidence.
- `valid-child-contract-evidence.json` — synthetic STUDIO-009P child evidence.
- `invalid-provider-identity.json` — rejects a non-opaque URL-like provider identity.
- `invalid-model-scope.json` — broadens data classification beyond the provider profile.
- `invalid-data-policy-broadening.json` — requests a classification not allowed by the provider profile.
- `invalid-credential-profile.json` — child evidence points at a different credential profile.
- `invalid-nonzero-budget.json` — violates the STUDIO-009D integer-zero monetary ceiling.
- `invalid-missing-child-contract.json` — demonstrates eligibility refusal when child evidence is absent.

No fixture identifies a real provider, model, endpoint, credential, account, or routable transport.
