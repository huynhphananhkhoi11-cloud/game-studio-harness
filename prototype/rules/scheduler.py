def validate_routine(actions, data):
    amap={r['id']:r for r in data['actions']['records']}; slots=sum(amap[a]['time_slots'] for a in actions)
    if slots>data['balance_v0']['constants']['routine_max_slots']: raise ValueError('Routine exceeds nine canh')
    return slots
