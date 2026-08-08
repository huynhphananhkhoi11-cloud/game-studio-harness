import argparse,json,tempfile,os
from .loader import load_data,initial_state,records
from .validator import validate_data
from .engine import perform_action
from .scheduler import validate_routine
from .event_director import draw
from .simulation import run_scenario,batch
from .save_system import save,load

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
    for c in ['validate-data','show-state','list-actions','perform-action','build-routine','resolve-routine','draw-opportunities','run-scenario','batch-simulate','save-roundtrip']:
        sp=sub.add_parser(c); sp.add_argument('--data-dir',default='data/vertical_slice'); sp.add_argument('--seed',type=int,default=1483); sp.add_argument('--scenario',default='vertical_slice_smoke'); sp.add_argument('--runs',type=int,default=10); sp.add_argument('actions',nargs='*')
    a=p.parse_args(); data=load_data(a.data_dir); st=initial_state(a.data_dir); st.seed=a.seed
    if a.cmd=='validate-data':
        e=validate_data(a.data_dir); print('OK' if not e else '\n'.join(e)); raise SystemExit(1 if e else 0)
    if a.cmd=='show-state': print(json.dumps(st.to_dict(),ensure_ascii=False,indent=2))
    elif a.cmd=='list-actions': print('\n'.join(records(data,'actions')))
    elif a.cmd=='perform-action': print(json.dumps(perform_action(data,st,a.actions[0]).changes,ensure_ascii=False,indent=2))
    elif a.cmd in ['build-routine','resolve-routine']:
        acts=a.actions or ['action_study_basic','action_copyist_job','action_rest']*3; print(json.dumps({'slots':validate_routine(acts,data),'actions':acts},ensure_ascii=False));
        if a.cmd=='resolve-routine':
            summary=[]
            for x in acts: summary += [e.type for e in perform_action(data,st,x).events]
            print(json.dumps({'state':st.to_dict(),'top_changes':summary[:5]},ensure_ascii=False))
    elif a.cmd=='draw-opportunities':
        cards,log=draw(data,st); print(json.dumps({'cards':[c['id'] for c in cards],'log':log},ensure_ascii=False,indent=2))
    elif a.cmd=='run-scenario': print(json.dumps(run_scenario(a.data_dir,a.scenario,a.seed).to_dict(),ensure_ascii=False,indent=2))
    elif a.cmd=='batch-simulate': print(json.dumps(batch(a.data_dir,a.runs,a.seed),ensure_ascii=False,indent=2))
    elif a.cmd=='save-roundtrip':
        fd,path=tempfile.mkstemp(); os.close(fd); save(st,path); st2=load(path); os.remove(path); print('OK' if st.to_dict()==st2.to_dict() else 'FAIL')
if __name__=='__main__': main()
