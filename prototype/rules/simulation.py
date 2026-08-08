from statistics import mean
from .loader import initial_state, load_data, records
from .engine import perform_action
STRATS={'balanced':['action_study_basic','action_copyist_job','action_rest']*3,'overstudy':['action_study_basic']*9,'work_heavy':['action_market_carry','action_copyist_job','action_rest']*3}
def run_scenario(data_dir,scenario,seed):
    data=load_data(data_dir); st=initial_state(data_dir); st.seed=seed
    scen=records(data,'scenarios')[scenario]
    for cmd in scen['commands']:
        d=perform_action(data,st,cmd)
        if any(e.type=='fail_forward_collapse' for e in d.events): break
    return st
def batch(data_dir,runs,seed):
    data=load_data(data_dir); out={}
    for name,cmds in STRATS.items():
        finals=[]
        for i in range(runs):
            st=initial_state(data_dir); st.seed=seed+i
            for cmd in cmds:
                d=perform_action(data,st,cmd)
                if any(e.type=='fail_forward_collapse' for e in d.events): break
            finals.append(st)
        out[name]={'money_avg':round(mean(s.stats['money'] for s in finals),2),'health_avg':round(mean(s.stats['health'] for s in finals),2),'alertness_avg':round(mean(s.stats['alertness'] for s in finals),2),'morale_avg':round(mean(s.stats['morale'] for s in finals),2),'van_sach_xp_avg':round(mean(s.skills['skill_van_sach']['xp'] for s in finals),2),'minh_sat_xp_avg':round(mean(s.skills['skill_minh_sat']['xp'] for s in finals),2),'copyist_mastery_avg':round(mean(s.jobs['job_copyist']['mastery'] for s in finals),2),'obligation_avg':round(mean(len(s.obligations) for s in finals),2)}
    return out
