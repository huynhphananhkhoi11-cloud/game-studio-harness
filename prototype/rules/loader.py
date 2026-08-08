import json, pathlib
from .models import PlayerState
FILES=['balance_v0','actions','skills','jobs','items','opportunities','quests','scenarios']
def load_json(p):
    with open(p,'r',encoding='utf-8') as f: return json.load(f)
def load_data(data_dir):
    base=pathlib.Path(data_dir); d={k:load_json(base/(k+'.json')) for k in FILES}; d['initial_state']=load_json(base/'initial_state.json'); return d
def initial_state(data_dir):
    raw=load_json(pathlib.Path(data_dir)/'initial_state.json')
    return PlayerState(raw['schema_version'],raw['day'],raw['slot'],raw['seed'],raw['stats'],raw['relations'],raw['skills'],raw['jobs'],raw['items'],raw['quests'],raw['obligations'],raw['flags'])
def records(data,name): return {r['id']:r for r in data[name]['records']}
