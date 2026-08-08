import json, os, tempfile
from .models import PlayerState
def save(state,path):
    d=os.path.dirname(path) or '.'; fd,tmp=tempfile.mkstemp(dir=d,prefix='.tmp_save_',text=True)
    with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(state.to_dict(),f,ensure_ascii=False,sort_keys=True)
    os.replace(tmp,path)
def load(path):
    with open(path,encoding='utf-8') as f: r=json.load(f)
    return PlayerState(**r)
