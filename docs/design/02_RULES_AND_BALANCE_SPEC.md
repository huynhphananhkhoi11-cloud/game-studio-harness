# Rules and Balance Spec

Canonical variables live in `data/vertical_slice/balance_v0.json`: health, alertness, morale, satiety, cold, money, integrity, derived stress_internal, relations, skills, job mastery, items, quests, obligations. Status is SPECIFIED when inherited consistently, PLAYTEST ASSUMPTION for numeric tuning, OWNER_DECISION where final design authority is needed. All numeric defaults/ranges/round/clamp/save/telemetry are centralized in balance or initial_state.

## Resolution pipeline
Validate command/preconditions; reserve time/resource; consume costs; compute base outcome; apply modifiers in order `cold -> overwork -> quality -> novelty -> state`; round nearest int except money floor; clamp; detect thresholds; emit events; evaluate quest/event triggers; create telemetry; autosave snapshot.

## Formulas and tests
| System | Formula | Pseudocode | Normal | Threshold | Edge/error | Test |
|---|---|---|---|---|---|---|
| Nếp | `sum(action.time_slots) <= 9` | sum slots, reject if > cap | 9 slots OK | 10 rejects | story-locked routine OWNER_DECISION | `test_routine_limit` |
| Status cost | `delta = round(base_cost * cold * overwork)` | apply negative costs then clamp | -8 alertness | 3rd continuous non-rest uses 1.5 | clamps 0-100 | `test_overwork_modifier`, `test_clamp` |
| stress_internal | `100 - morale` | never save duplicate | morale 62 => 38 | morale 0 => 100 | morale clamp first | `test_derived_stress` |
| XP | `round(base * quality * novelty * state)` | add XP, recompute rank, no spend | 12*1.15=14 | 30 XP rank 2 | unknown skill invalid data | `test_xp_threshold_rounding` |
| Novelty | `1.15 if no same action in prior 12 days else 1.0` | scan action history | first study bonus | day+12 no bonus | day+13 bonus | `test_novelty_window` |
| Job pay | `money += max(0, base_pay - broker_fee)` | apply mastery/rep then pay | copyist 5-2=3 | mastery > direct unlock no fee | insufficient stat blocks later | `test_job_pay_mastery_reputation` |
| Item sell/use | `quest_item => cannot sell` | reject sale if quest flag | rice sell allowed | DOC01 blocked | unknown item invalid | `test_quest_item_not_sellable` |
| Opportunity draw | weighted without replacement and group uniqueness | deterministic RNG seed | 3 groups | fewer if not enough | log ineligible reasons | `test_event_draw_seed` |
| Quest state | target in transitions[current] | raise on illegal | available->active | failed->completed rejoin | completed->active blocked | `test_quest_transition` |
| Obligation | source+due required; integrity unaffected by creation | append ledger | Viên ngoại creates debt | due day shown | missing source invalid future | `test_obligation` |
| Exam/ending | `ending = fate > eligibility > rank > obligation > moral > coda > route` | contract only | pass route | clean record hard cap | no full exam code 2A | traceability QA |

## System notes
A day contains three canh; a Nếp contains three days/nine canh. Travel is an action cost in later data; slice actions consume one slot. Story/exam locked days block builder. Interruptions refund unspent slots unless event consumes them. Pure routine bonus is a playtest assumption applied only after three planned days with no forced interrupt.

Health, alertness and morale are displayed; satiety/cold are hidden support variables. Collapse is fail-forward forced rest, never game over. Relationships do not add exam points. Integrity changes only from concrete action cost, not moral-sounding dialogue. Obligations require source, due, repayment/refusal path and callback. Event director uses seeded deterministic weighted selection without replacement and avoids three cards from the same group unless explicitly overridden. Exam/ending remain interface contracts for Milestone 2A.
