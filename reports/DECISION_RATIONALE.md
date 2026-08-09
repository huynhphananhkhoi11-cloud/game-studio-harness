# Decision Rationale — Milestone 2A.1

## XP state multiplier

- Decision: implement `XP = round(base × quality × novelty × state)` in code and tests.
- Rationale: rules spec and balance data already define `state_multipliers`, while the previous engine omitted them.
- Limit: no approved rule maps health/alertness/morale to `strained`, `normal`, or `rested`.
- Owner decision: `OWNER_DECISION-XP-STATE-001` remains open; the resolver defaults to `normal` and accepts explicit labels for tests/scenarios.

## MQ01C

- Decision: add MQ01C to data because the existing MQ01 evidence register contains MQ01C-specific support as controlled fiction, including temporary deferral by the local official and optional poem branch.
- Rationale: this fixes the MQ01B unlock dangling reference without inventing new historical details.
- Production lock: DOC01 remains greybox; unresolved material-culture specifics remain blocked.

## Batch simulation

- Decision: keep balanced, overstudy, and work_heavy strategies, but draw one seeded opportunity after each executed action and apply only data-defined effects.
- Rationale: previous 1,000-run batch was deterministic per strategy and could not test seed-sensitive variation.
- Limit: the result is a prototype smoke distribution, not a balance claim.
