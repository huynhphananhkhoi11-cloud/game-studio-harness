def transition(data,state,qid,target):
    q=next(r for r in data['quests']['records'] if r['id']==qid); cur=state.quests.get(qid,q.get('initial_state'))
    if target not in q['transitions'].get(cur,[]): raise ValueError(f'Illegal quest transition {qid} {cur}->{target}')
    state.quests[qid]=target; return {'quest':qid,'from':cur,'to':target}
