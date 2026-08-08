# Balance Baseline

Command: `python -m prototype.rules.cli batch-simulate --data-dir data/vertical_slice --runs 1000 --seed 1483`.

```json
{
  "balanced": {
    "money_avg": 30,
    "health_avg": 82,
    "alertness_avg": 57,
    "morale_avg": 56,
    "van_sach_xp_avg": 38,
    "minh_sat_xp_avg": 19,
    "copyist_mastery_avg": 9,
    "obligation_avg": 0
  },
  "overstudy": {
    "money_avg": 17,
    "health_avg": 56,
    "alertness_avg": 2,
    "morale_avg": 43,
    "van_sach_xp_avg": 86,
    "minh_sat_xp_avg": 0,
    "copyist_mastery_avg": 0,
    "obligation_avg": 0
  },
  "work_heavy": {
    "money_avg": 42,
    "health_avg": 64,
    "alertness_avg": 66,
    "morale_avg": 56,
    "van_sach_xp_avg": 0,
    "minh_sat_xp_avg": 19,
    "copyist_mastery_avg": 9,
    "obligation_avg": 0
  }
}
```

Interpretation: this is not proof of balance. It only shows initial outliers/questions: overstudy preserves money but reduces health/alertness/morale; work-heavy improves money and copyist mastery while tiring Lâm; balanced route lands between them. Playtest must observe whether players understand why these outcomes occur.
