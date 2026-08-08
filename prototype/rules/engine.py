from .models import StateDelta,DomainEvent
from .loader import records
from .progression import skill_rank, novelty_multiplier
from .economy import apply_job

def clamp(state,data):
    for k,v in data['balance_v0']['variables'].items():
        if v.get('type')=='derived' or k not in state.stats: continue
        if 'min' in v: state.stats[k]=max(v['min'],state.stats[k])
        if 'max' in v: state.stats[k]=min(v['max'],state.stats[k])
    state.stats['money']=max(0,state.stats.get('money',0))

def perform_action(data,state,action_id,quality='normal'):
    acts=records(data,'actions'); jobs=records(data,'jobs'); bal=data['balance_v0']; c=bal['constants']; xpconf=bal['xp']; a=acts[action_id]; d=StateDelta(trace=[f'1 validate {action_id}', '2 reserve time/resource'])
    if state.slot+a['time_slots']>c['routine_max_slots']: raise ValueError('routine day capacity exceeded')
    d.trace.append('3 consume mandatory costs')
    consec=sum(1 for h in state.action_history[-2:] if 'rest' not in h.get('tags',[]))
    cost_mult=1.0
    if consec>=2 and 'rest' not in a.get('tags',[]): cost_mult*=c['overwork_cost_multiplier']; d.events.append(DomainEvent('overwork_modifier',{'multiplier':cost_mult}))
    if state.stats.get('cold'): cost_mult*=c['cold_cost_multiplier']
    for k,v in a.get('costs',{}).items():
        if k=='money': state.stats[k]=state.stats.get(k,0)-v
        else: state.stats[k]=state.stats.get(k,0)+round(v*cost_mult)
    d.trace.append('4 base outcome; 5 modifiers; 6 round; 7 clamp')
    for k,v in a.get('effects',{}).items():
        if k in state.stats: state.stats[k]=state.stats.get(k,0)+v
        else: state.relations[k]=state.relations.get(k,0)+v
    if a.get('job'):
        pay=apply_job(state,jobs[a['job']]); fee=bal['constants']['broker_fee'] if jobs[a['job']].get('broker')=='ba_ba' and state.jobs[a['job']]['mastery']<=jobs[a['job']]['direct_call_mastery'] else 0
        state.stats['money']+=max(0,pay-fee); d.events.append(DomainEvent('job_resolved',{'job':a['job'],'pay':pay,'broker_fee':fee}))
    for sid,base in a.get('xp',{}).items():
        mult=xpconf['quality_multipliers'][quality]*novelty_multiplier(state,action_id,state.day,c['novelty_window_days'],xpconf['novelty_multiplier'])
        gained=round(base*mult); state.skills[sid]['xp']+=gained; state.skills[sid]['rank']=skill_rank(state.skills[sid]['xp'],xpconf['thresholds']); state.skills[sid]['history'].append({'day':state.day,'action':action_id,'xp':gained}); d.events.append(DomainEvent('xp_gained',{'skill':sid,'xp':gained,'multiplier':mult}))
    if 'obligation' in a: state.obligations.append(dict(a['obligation'])); d.events.append(DomainEvent('obligation_added',a['obligation']))
    state.slot+=a['time_slots']; state.action_history.append({'day':state.day,'action_id':action_id,'tags':a.get('tags',[])})
    clamp(state,data)
    if state.stats['health']<=c['collapse_health_threshold'] or state.stats['alertness']<=c['collapse_alertness_threshold']:
        d.events.append(DomainEvent('fail_forward_collapse',{'next':'forced_rest'})); state.slot=c['routine_max_slots']
    d.trace += ['8 thresholds/transitions','9 domain events','10 quest/event triggers','11 telemetry','12 autosave snapshot']
    d.telemetry.append({'event':'action_performed','action':action_id,'day':state.day,'slot':state.slot})
    d.changes=state.to_dict(); return d
