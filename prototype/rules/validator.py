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
    for a in loaded.get('actions',{}).get('records',[]):
        if a.get('time_slots',0)<1 or a.get('time_slots',0)>9: errors.append(f'{a["id"]}: bad time')
        for s in a.get('xp',{}):
            if s not in skills: errors.append(f'{a["id"]}: unknown skill {s}')
        if a.get('job') and a['job'] not in jobs: errors.append(f'{a["id"]}: unknown job')
    for q in loaded.get('quests',{}).get('records',[]):
        for k, vs in q.get('transitions',{}).items():
            if k not in QUEST_STATES: errors.append(f'{q["id"]}: bad quest state')
            for v in vs:
                if v not in QUEST_STATES: errors.append(f'{q["id"]}: bad transition target')
        for it in q.get('items',[]):
            if it not in items: errors.append(f'{q["id"]}: unknown item {it}')
    for o in loaded.get('opportunities',{}).get('records',[]):
        for c in o.get('conditions',[]):
            var=re.split(r'[<>=!]+',c)[0].strip()
            if var not in KNOWN_VARS: errors.append(f'{o["id"]}: unknown condition var {var}')
    b=loaded.get('balance_v0',{}).get('variables',{})
    for k,v in b.items():
        if 'min' in v and not (v['min']<=v['default']<=v['max']): errors.append(f'{k}: default outside range')
    return errors
