# Run Report — Milestone 2A.1

## Input commit

- Branch: work
- Commit: 5da584b7e54253a6a24c4ba75787e4714bbc7388
- Prior log: `5da584b Add Milestone 2A rules prototype and design specs`; `17e7975 Add Milestone 2A rules prototype and design specs`; `d896cfe Merge pull request #2 from huynhphananhkhoi11-cloud/codex/verify-checkout-before-proceeding`
- Preflight status: no `source/` changes were present before edits.

## Commands run

| Command | Exit code | Notes |
|---|---:|---|
| `git branch --show-current` | 0 | returned `work` |
| `git rev-parse HEAD` | 0 | returned `5da584b7e54253a6a24c4ba75787e4714bbc7388` |
| `git log -3 --oneline` | 0 | recorded above |
| `git status --short` | 0 | clean before edits |
| `python -m prototype.rules.cli validate-data --data-dir data/vertical_slice` | 0 | validator OK |
| `python -m unittest discover -s tests` | 0 | 39 tests |
| `python -m prototype.rules.cli run-scenario --data-dir data/vertical_slice --scenario vertical_slice_smoke --seed 1483` | 0 | scenario completed |
| `python -m prototype.rules.cli save-roundtrip --data-dir data/vertical_slice --seed 1483` | 0 | round-trip OK |
| `python -m prototype.rules.cli batch-simulate --data-dir data/vertical_slice --runs 1000 --seed 1483` | 0 | batch metrics below |

## Batch simulation, 1,000 runs, seed 1483

This is a prototype smoke distribution only and is not a claim that the game is balanced.

| Strategy | Unique finals | Collapse/fail-forward rate | Opportunities drawn | Money min/avg/max | Health min/avg/max | Alertness min/avg/max | Morale min/avg/max | Văn sách XP min/avg/max | Minh sát XP min/avg/max |
|---|---:|---:|---:|---|---|---|---|---|---|
| balanced | 3 | 0.0000 | 9000 | 30/31.97/36 | 82/86.59/100 | 57/57.00/57 | 56/59.83/71 | 38/38.00/38 | 19/19.00/19 |
| overstudy | 6 | 1.0000 | 7000 | 17/19.64/23 | 56/64.47/84 | 2/2.00/2 | 43/49.35/64 | 86/86.00/86 | 0/0.00/0 |
| work_heavy | 5 | 0.0000 | 9000 | 42/44.53/48 | 64/73.86/96 | 66/66.00/66 | 56/63.40/80 | 0/0.00/0 | 19/19.00/19 |

## Remaining limits

- `OWNER_DECISION-XP-STATE-001`: no approved status-to-XP-state classification exists yet.
- DOC01 remains greybox; no layout, wording, seal, fingerprint, signature, paper, ink, or size has been promoted to production fact.
- The batch simulation applies lightweight opportunity effects; it is a deterministic harness, not balance proof.
