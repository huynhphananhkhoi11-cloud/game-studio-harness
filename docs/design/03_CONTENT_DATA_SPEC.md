# Content Data Spec

Vertical slice data is limited to days 1-18 in `data/vertical_slice/`. Required files are `initial_state.json`, `balance_v0.json`, `actions.json`, `skills.json`, `jobs.json`, `items.json`, `opportunities.json`, `quests.json`, and `scenarios.json`.

Every record has stable `id`, `schema_version`, `source_reference`, and `design_status`. JSON stores identifiers and scalar parameters, not prose scenes or executable logic. Shared playtest numbers live in `balance_v0.json`; data records may refer to those values or contain record-specific costs/pay that are also listed in the assumption register.

The Python standard-library validator checks UTF-8 JSON, unique IDs, enum status, variable ranges, quest transitions, action time/cost sanity, referenced skill/job/item IDs, opportunity condition variables, and basic magic-number containment by requiring common constants in balance.
