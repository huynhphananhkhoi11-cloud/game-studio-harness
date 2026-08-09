import json, pathlib, re
VALID_STATUS={'SPECIFIED','NEEDS_DETAIL','NEEDS_PLAYTEST','INTERNAL_CONFLICT','HISTORICAL_REVIEW','OWNER_DECISION','REMOVE_CANDIDATE','PLAYTEST_ASSUMPTION'}
QUEST_STATES={'locked','available','active','completed','failed','expired','skipped'}
KNOWN_VARS={'health','alertness','morale','satiety','cold','money','integrity','mentor_trust','village_reputation','relation_tin','relation_hao','relation_vien_ngoai'}
def validate_data(data_dir):
    base=pathlib.Path(data_dir); errors=[]; loaded={}
    for p in base.glob('*.json'):
        try:
            txt=p.read_text(encoding='utf-8'); loaded[p.stem]=json.loads(txt)
        except Exception as e: errors.append(f'{p}: invalid UTF-8/JSON {e}')
    ids={}
    for name,obj in loaded.items():
        recs=obj.get('records',[])
        for r in recs:
            if r.get('id') in ids: errors.append(f'duplicate id {r.get("id")}')
            ids[r.get('id')]=name
            if r.get('design_status') not in VALID_STATUS: errors.append(f'{r.get("id")}: bad status')
            for req in ('schema_version','source_reference'):
                if req not in r: errors.append(f'{r.get("id")}: missing {req}')
    skills={r['id'] for r in loaded.get('skills',{}).get('records',[])}; jobs={r['id'] for r in loaded.get('jobs',{}).get('records',[])}; items={r['id'] for r in loaded.get('items',{}).get('records',[])}
    quests={r['id']:r for r in loaded.get('quests',{}).get('records',[])}
    for a in loaded.get('actions',{}).get('records',[]):
        if a.get('time_slots',0)<1 or a.get('time_slots',0)>9: errors.append(f'{a["id"]}: bad time')
        for s in a.get('xp',{}):
            if s not in skills: errors.append(f'{a["id"]}: unknown skill {s}')
        if a.get('job') and a['job'] not in jobs: errors.append(f'{a["id"]}: unknown job')
        if a.get('requires_quest') and a['requires_quest'] not in quests: errors.append(f'{a["id"]}: unknown required quest {a["requires_quest"]}')
    for qid,q in quests.items():
        if q.get('initial_state') not in QUEST_STATES: errors.append(f'{qid}: bad initial quest state')
        if q.get('initial_state') not in q.get('transitions',{}): errors.append(f'{qid}: initial state missing transition row')
        for u in q.get('unlocks',[]):
            if u not in quests: errors.append(f'{qid}: unlocks unknown quest {u}')
        for k, vs in q.get('transitions',{}).items():
            if k not in QUEST_STATES: errors.append(f'{qid}: bad quest state {k}')
            for v in vs:
                if v not in QUEST_STATES: errors.append(f'{qid}: bad transition target {v}')
                if v not in q.get('transitions',{}): errors.append(f'{qid}: transition target missing row {v}')
        for it in q.get('items',[]):
            if it not in items: errors.append(f'{qid}: unknown item {it}')
    for qid,state in loaded.get('initial_state',{}).get('quests',{}).items():
        if qid not in quests: errors.append(f'initial_state: unknown quest {qid}')
        elif state not in QUEST_STATES: errors.append(f'initial_state: bad state {qid}={state}')
        elif state not in quests[qid].get('transitions',{}): errors.append(f'initial_state: {qid} state has no transition row {state}')
    for o in loaded.get('opportunities',{}).get('records',[]):
        for c in o.get('conditions',[]):
            var=re.split(r'[<>=!]+',c)[0].strip()
            if var not in KNOWN_VARS: errors.append(f'{o["id"]}: unknown condition var {var}')
    b=loaded.get('balance_v0',{}).get('variables',{})
    for k,v in b.items():
        if 'min' in v and not (v['min']<=v['default']<=v['max']): errors.append(f'{k}: default outside range')
    return errors
