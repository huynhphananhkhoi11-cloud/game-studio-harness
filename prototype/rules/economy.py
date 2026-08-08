def apply_job(state, job):
    st=state.jobs[job['id']]; st['mastery']+=job.get('mastery_gain',0); st['reputation']+=job.get('reputation_gain',0); return job.get('base_pay',0)
def can_sell(item): return not item.get('quest_item',False)
