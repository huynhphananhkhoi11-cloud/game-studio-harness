# STUDIO-008 - Zero-cost system pilot and v1.0 acceptance

Status: ACCEPTED - IMPLEMENTATION CONTRACT APPROVED - PILOT NOT STARTED

Parent roadmap: GAME AI Studio Blueprint v1.0

Dependencies: STUDIO-001 through STUDIO-007, including the reconciled STUDIO-007 milestone, are merged and retained

Primary owner: Studio Owner

Canonical implementation contract: tasks/STUDIO-008-IMPLEMENTATION.md

## Goal

Prove the retained zero-cost Manual/Fake operating model end to end. STUDIO-008 is the final v1.0 system pilot and acceptance check. It does not add a new organizational Studio, topology, authority layer, memory system, provider stack, or production release capability.

## Entry conditions

- STUDIO-007A through STUDIO-007F are independently merged and reconciled.
- Manual remains the human-controlled adapter and Fake remains deterministic with zero network activity.
- No provider SDK, credential, account, paid service, or nonzero budget is active.
- Queue, dispatch, writer/worktree/handoff, failover, gate/trace/budget, and provider-adapter rollback evidence is retained.

## Required pilot scenarios

### P01 - Research handoff

Produce source references, limitations, a durable handoff, and zero-cost evidence. Research output cannot promote itself to canon or gain write authority.

### P02 - Engineering work

Prove a valid claim, isolated worktree, deterministic repository change, focused tests, retained regression, allowed paths, and durable handoff.

### P03 - Simulated failover

Prove the old attempt safe-stops, a human explicitly approves reassignment, the new attempt continues from durable evidence, and no duplicate writer or output exists.

### P04 - Writer conflict

Prove an overlapping claim fails closed with CLAIM_SCOPE_CONFLICT and preserves complete trace evidence.

### P05 - QA failure and correction

Prove correction uses a new attempt and that approval bound to an earlier immutable head cannot authorize the corrected head.

### P06 - Owner gate

Prove both approve and reject paths. No adapter, dispatcher, evaluator, or agent can bypass the Studio Owner decision.

## Acceptance thresholds

- All 6 scenarios pass.
- Replaying the same canonical bundle produces the same results and digests.
- Unauthorized writes: 0.
- Duplicate writers: 0.
- Duplicate outputs: 0.
- Gate bypasses: 0.
- Durable handoff coverage for material transitions: 100 percent.
- Trace coverage for material transitions: 100 percent.
- Paid, provider, network, and credential activity: 0.
- Manual rollback is demonstrated for every retained capability.

## Owner disposition

The final report records exactly one disposition:

- ACCEPT_V1_0
- ACCEPT_WITH_LIMITATIONS
- REQUEST_CHANGES
- REJECT_V1_0

ACCEPT_V1_0 means only that the Manual/Fake zero-cost v1.0 boundary is accepted. It does not authorize a real provider, credential, network call, spend, deployment, store submission, or release.

## Out of scope

- Game-engine integration, release dry-run, deployment, publication, store submission, or player telemetry.
- Real model/provider calls, SDKs, accounts, credentials, network access, billing, or nonzero cost.
- New topology, memory protocol, authority, automatic merge, automatic owner approval, or automatic rollback.

## Failure and rollback

Any missing scenario, nondeterministic replay, unsafe write, duplicate writer/output, gate bypass, incomplete durable evidence, secret/provider activity, or nonzero spend fails the pilot. Rollback removes only the later STUDIO-008 implementation through an authorized revert; earlier accepted contracts and evidence remain intact.
