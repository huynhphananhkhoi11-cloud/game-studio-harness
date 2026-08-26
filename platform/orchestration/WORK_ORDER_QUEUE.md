# Work Order & Producer Queue v1.0

STUDIO-007A provides a zero-cost, provider-neutral intake envelope and a local
file-backed queue. Queue data records work; it does not grant approval,
authentication, execution, review, merge, or publication authority.

## Storage layout

```text
<queue-root>/
  work-orders/<work-order-id>.json
  events/<work-order-id>.jsonl
```

Each JSON snapshot is the current state of one work order. Each JSONL file is
the ordered, append-only logical history for that work order. The first event
uses `null` as its explicit `prior_state` and `DRAFT` as `next_state`.

The ordered queue is derived from validated snapshots. Higher `priority` comes
first, followed by earlier `created_at`, followed by lexical `work_order_id`.
No mutable index or database is authoritative.

## Authority boundary

- `PRODUCER-01` creates `DRAFT`, advances `READY` to `CLAIMABLE`, blocks active
  intake states with a reason, and returns `BLOCKED` to `DRAFT`.
- `STUDIO_OWNER` alone advances `DRAFT` to `READY` or cancels an active intake
  state.
- `CLAIMED`, `QA_PENDING`, `OWNER_PENDING`, and `DONE` are recognized but
  reserved. STUDIO-007A rejects every transition into or out of them.

Actor IDs and role labels are evidence claims. They are not authentication.
Repository review and the Studio Owner remain the authority boundary.

## Integrity and safety

- Schema version is `1`; timestamps are ISO 8601 UTC with a `Z` suffix.
- Monetary budget is exactly `0`.
- Paths are repository-relative and cannot escape the repository.
- Transition history is checked for identity, ordering, authority, state
  continuity, replay, and snapshot-digest reconciliation.
- Objective, path scope, prohibitions, and budget cannot be escalated during a
  transition.
- Writes use temporary sibling files and `os.replace`. A partial or interrupted
  update fails later validation and is never reported as a valid transition.
- The CLI performs no network, provider, credential, Git, deletion, or paid
  action.

## CLI

Run `python scripts/orchestration_queue.py --help` for complete arguments.

```text
create-draft  create a validated DRAFT and its initial event
validate      validate a queue root without changing it
list          print the deterministic derived queue without changing it
transition    append one authorized active transition and update its snapshot
```

Schemas document the record shapes. The standard-library validator is the
enforcement implementation; no JSON Schema package is required.
