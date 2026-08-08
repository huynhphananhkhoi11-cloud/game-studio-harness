def skill_rank(xp, thresholds):
    rank=1
    for name,val in sorted(thresholds.items(), key=lambda kv: kv[1]):
        if xp>=val: rank=int(name.split('_')[-1])
    return rank
def novelty_multiplier(state, action_id, day, window, mult):
    for h in reversed(state.action_history):
        if h['action_id']==action_id and day-h['day']<=window: return 1.0
    return mult
