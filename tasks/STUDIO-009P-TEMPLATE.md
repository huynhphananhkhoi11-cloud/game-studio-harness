# STUDIO-009P-* — Real Provider Child Contract Template

Status: TEMPLATE ONLY — GRANTS NO PROVIDER AUTHORITY

Parent: `tasks/STUDIO-009D.md`

A real provider MUST receive a separately reviewed and merged child contract based on this template before provider-specific implementation is authorized.

## 1. Provider identity

Record:

- child task identifier `STUDIO-009P-*`;
- authoritative provider legal/product identity;
- authoritative source references;
- immutable provider-profile lineage;
- method for proving runtime provider/transport identity independently from model-generated text.

## 2. Model identity and version policy

Specify exact allowed model identifiers and whether versions are pinned, allowlisted, or otherwise bounded. Undefined model aliases are forbidden.

## 3. Endpoint, host, and transport allowlist

Specify exact endpoint/host/region/transport classes. Redirect broadening, arbitrary hosts, user-supplied endpoints, and model-supplied endpoints are forbidden.

## 4. Authentication and credential lineage

Specify the approved authentication mechanism and exact STUDIO-009C `credential_profile_ref` lineage. No credential value may appear in repository files, prompts, model output, traces, evidence, logs, exceptions, memory, URLs, or command lines.

## 5. Capability map

Map each provider/model combination to explicit capabilities. Undeclared capabilities fail closed.

## 6. Data export, retention, and training policy

Specify allowed data classifications; residency/export constraints; retention; logging; provider training/use policy; and any content classes that must never leave the local boundary.

## 7. Quota, rate, timeout, and retry limits

Specify deterministic ceilings for request size, output size, rate, concurrency, timeout, retry count, and replay/idempotency behavior.

## 8. Budget

Specify provider, currency, time window, and exact monetary ceiling. Until separately approved by the Studio Owner, the ceiling remains integer zero.

## 9. Identity verification

Define how provider identity, model identity, endpoint/transport identity, and response lineage are verified from accepted configuration and transport metadata rather than model-generated text.

## 10. Kill switch, pause, and revocation

Define Owner-controlled pause/kill/revoke actions and the evidence required to resume. Revocation dominates stale approvals.

## 11. Incident response

Define secret exposure, unexpected host, identity mismatch, unauthorized capability, cost anomaly, data-policy violation, and provider outage response.

## 12. MANUAL/FAKE rollback

The accepted STUDIO-007F/STUDIO-008 MANUAL/FAKE path must remain a no-network fallback and regression oracle.

## 13. Tests

Require provider-specific focused tests plus the complete retained regression suite. Tests must include malformed/hostile metadata, identity mismatch, data-policy broadening, credential mismatch, quota/budget enforcement, pause/revocation, kill switch, replay, timeout/failure, and rollback.

## 14. QA and Review

Require independent QA PASS, Review and Integration APPROVE, zero blocking findings, and a separate Studio Owner merge decision.

## 15. Progressive connected-validation dependency

Merging a `STUDIO-009P-*` child contract, offline implementation, QA record, Review record, or closeout DOES NOT activate a provider.

After STUDIO-009R-01 is durably accepted, a provider that has completed its P-child offline lifecycle may receive a separately reviewed and merged `STUDIO-009V-*` / provider-specific live-extension contract. Only that V-track may authorize the bounded credential/network/model activity needed for provider-specific connected validation.

Initial connected validation must remain PUBLIC/SYNTHETIC, zero-cost, exact-provider/model/host bounded, concurrency 1, automatic retry 0, and tool/browser/remote-MCP/code-execution/search/storage disabled unless the V contract explicitly and separately narrows those controls.

A successful V-track does not authorize automatic routing. STUDIO-009E governs automatic routing/failover and may select only separately validated providers that are explicitly routing-eligible. STUDIO-009F remains the full integrated connected-studio acceptance gate.

No P child, V child, router, adapter, reviewer, evaluator, AI, or provider can self-authorize merge, deployment, publication, data-policy broadening, or nonzero spend.
