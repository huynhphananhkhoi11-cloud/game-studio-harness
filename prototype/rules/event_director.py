import random, operator
OPS={'>=':operator.ge,'<=':operator.le,'>':operator.gt,'<':operator.lt,'==':operator.eq}
def ok(cond,state):
    for op,fn in OPS.items():
        if op in cond:
            a,b=cond.split(op); val=state.stats.get(a.strip(), state.relations.get(a.strip(),0)); return fn(val,int(b))
    return False
def eligible(data,state,day=None):
    out=[]; log=[]; day=day or state.day
    for o in data['opportunities']['records']:
        good=o['days'][0]<=day<=o['days'][1] and all(ok(c,state) for c in o.get('conditions',[])) and (not o.get('one_shot') or o['id'] not in state.drawn_opportunities)
        log.append(f"{o['id']} {'eligible' if good else 'ineligible'}")
        if good: out.append(o)
    return out,log
def draw(data,state,count=None,allow_same_group=False):
    rng=random.Random(state.seed+state.day); count=count or data['balance_v0']['constants']['opportunity_draw_count']; pool,log=eligible(data,state); picked=[]; groups=set()
    while pool and len(picked)<count:
        total=sum(o['weight'] for o in pool); x=rng.uniform(0,total); acc=0; choice=pool[-1]
        for o in pool:
            acc+=o['weight']
            if x<=acc: choice=o; break
        pool=[o for o in pool if o['id']!=choice['id']]
        if not allow_same_group and choice['group'] in groups: continue
        picked.append(choice); groups.add(choice['group'])
    state.drawn_opportunities += [p['id'] for p in picked if p.get('one_shot')]
    return picked,log
