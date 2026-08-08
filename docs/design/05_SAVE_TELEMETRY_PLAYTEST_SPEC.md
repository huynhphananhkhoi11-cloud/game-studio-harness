# Save, Telemetry and Playtest Spec

Save schema version is `2A.v0`. Persistent state: day, slot, seed, stats except derived values, relations, skills XP/rank/history, jobs mastery/reputation, item counts, quest states, obligations, flags, action history and drawn one-shot opportunities. Derived state such as `stress_internal = 100 - morale` is recomputed after load.

Autosave occurs after routine/quest decision; decision-save occurs before irreversible choices; manual save is allowed outside mutation pipeline. Saves write to a temp file then atomic replace. If load fails, keep previous good save and show recovery error. Migration policy: schema bump requires explicit migration function and QA round-trip fixture. Deterministic seed is saved and every random draw derives from seed plus stable context.

Telemetry dictionary: `action_performed`, `routine_built`, `routine_resolved`, `opportunity_drawn`, `job_resolved`, `xp_gained`, `obligation_added`, `quest_transition`, `mq01_evidence_inspected`, `mq01_conclusion_selected`, `fail_forward_collapse`, `save_loaded`, `settings_changed`. Metrics map to playtest questions: Do players understand costs? Do they overclaim evidence? Does self-reliant route remain viable? Does obligation feel fair? Does fail-forward feel dignified? Telemetry supports but never replaces observation/interview.
