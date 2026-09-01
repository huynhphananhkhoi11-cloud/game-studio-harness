
# STUDIO-008 zero-cost pilot acceptance

This capability validates supplied evidence only. It does not execute orchestration.

## Pilot paths

- P01 proves sourced research, limitations, durable handoff, no canon self-promotion, and no write authority.
- P02 proves one valid claim, isolated worktree evidence, allowed paths, focused tests, and retained regression.
- P03 proves safe-stop, explicit human reassignment approval, new-attempt completion, and no duplicate writer/output.
- P04 proves overlapping writer scope fails closed with `CLAIM_SCOPE_CONFLICT` and creates no output.
- P05 proves correction uses a new attempt/head and old approval cannot authorize the corrected head.
- P06 proves both Studio Owner approve and reject paths and rejects bypass evidence.

## Deterministic boundary

Input is canonical JSON plus caller-supplied `as_of`. Validation is read-only, uses SHA-256 canonical digests, and leaves evidence unchanged. System time, Git, subprocesses, sockets, provider SDKs, environment credentials, file mutation, dispatch, retries, merge, deployment, publication, and spend are outside the runtime.

## Acceptance

Acceptance requires six of six scenarios, both P06 paths, deterministic replay, zero unauthorized writes, zero duplicate writers/outputs, zero gate bypasses, complete durable handoff and trace coverage, zero provider/network/credential/spend activity, and manual rollback evidence for every path.

The validator emits PASS evidence only. Final disposition remains a separate Studio Owner decision and may be `ACCEPT_V1_0`, `ACCEPT_WITH_LIMITATIONS`, `REQUEST_CHANGES`, or `REJECT_V1_0`.

## Rollback

Revert the STUDIO-008 implementation commit and remove only the twenty implementation paths authorized by the contract. Earlier contracts and STUDIO-001 through STUDIO-007 remain retained.
