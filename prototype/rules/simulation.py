from statistics import mean
from .loader import initial_state, load_data, records
from .engine import perform_action
from .event_director import draw
STRATS={'balanced':['action_study_basic','action_copyist_job','action_rest']*3,'overstudy':['action_study_basic']*9,'work_heavy':['action_market_carry','action_copyist_job','action_rest']*3}
def run_scenario(data_dir,scenario,seed):
    data=load_data(data_dir); st=initial_state(data_dir); st.seed=seed
    scen=records(data,'scenarios')[scenario]
    for cmd in scen['commands']:
        d=perform_action(data,st,cmd)
        cards,_=draw(data,st,count=1)
        apply_opportunities(st,cards)
        if any(e.type=='fail_forward_collapse' for e in d.events): break
    return st
def apply_opportunities(st,cards):
    for card in cards:
        st.flags['opportunity_draw_count']=st.flags.get('opportunity_draw_count',0)+1
        for k,v in card.get('effects',{}).items():
            if k in st.stats: st.stats[k]+=v
            elif k in st.relations: st.relations[k]+=v
            else: st.flags[k]=v
def dist(vals):
    return {'min':min(vals),'avg':round(mean(vals),2),'max':max(vals)}
def batch(data_dir,runs,seed):
    data=load_data(data_dir); out={}
    for name,cmds in STRATS.items():
        finals=[]; collapses=0
        for i in range(runs):
            st=initial_state(data_dir); st.seed=seed+i
            for cmd in cmds:
                d=perform_action(data,st,cmd)
                cards,_=draw(data,st,count=1)
                apply_opportunities(st,cards)
                if any(e.type=='fail_forward_collapse' for e in d.events): collapses+=1; break
            finals.append(st)
        sigs={(s.stats['money'],s.stats['health'],s.stats['alertness'],s.stats['morale'],s.skills['skill_van_sach']['xp'],s.skills['skill_minh_sat']['xp'],s.slot) for s in finals}
        out[name]={
            'unique_final_results':len(sigs),'collapse_fail_forward_rate':round(collapses/runs,4),'opportunities_drawn':sum(s.flags.get('opportunity_draw_count',0) for s in finals),
            'money':dist([s.stats['money'] for s in finals]),'health':dist([s.stats['health'] for s in finals]),'alertness':dist([s.stats['alertness'] for s in finals]),'morale':dist([s.stats['morale'] for s in finals]),
            'van_sach_xp':dist([s.skills['skill_van_sach']['xp'] for s in finals]),'minh_sat_xp':dist([s.skills['skill_minh_sat']['xp'] for s in finals]),
            'copyist_mastery_avg':round(mean(s.jobs['job_copyist']['mastery'] for s in finals),2),'obligation_avg':round(mean(len(s.obligations) for s in finals),2)}
    return out
