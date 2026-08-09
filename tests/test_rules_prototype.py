import tempfile, unittest
from prototype.rules.loader import load_data, initial_state
from prototype.rules.validator import validate_data
from prototype.rules.engine import perform_action, clamp
from prototype.rules.progression import skill_rank, novelty_multiplier, state_multiplier
from prototype.rules.scheduler import validate_routine
from prototype.rules.quest_state import transition
from prototype.rules.event_director import draw, eligible
from prototype.rules.economy import can_sell
from prototype.rules.save_system import save, load
DATA='data/vertical_slice'
class RulesTests(unittest.TestCase):
 def setUp(self): self.data=load_data(DATA); self.st=initial_state(DATA)
 def test_data_validation(self): self.assertEqual(validate_data(DATA),[])
 def test_mq01c_present(self): self.assertIn('MQ01C', self.st.quests)
 def test_state_default_invariant(self): self.assertEqual(self.st.stats['health'],82); self.assertEqual(self.st.derived()['stress_internal'],38)
 def test_clamp_money(self): self.st.stats.update(health=200, money=-5); clamp(self.st,self.data); self.assertEqual(self.st.stats['health'],100); self.assertEqual(self.st.stats['money'],0)
 def test_derived_stress(self): self.st.stats['morale']=40; self.assertEqual(self.st.derived()['stress_internal'],60)
 def test_xp_threshold_rounding(self): self.assertEqual(skill_rank(30,self.data['balance_v0']['xp']['thresholds']),2); perform_action(self.data,self.st,'action_study_basic'); self.assertEqual(self.st.skills['skill_van_sach']['xp'],14)
 def test_xp_state_multiplier_explicit_labels(self):
  xpconf=self.data['balance_v0']['xp']
  self.assertEqual(state_multiplier(xpconf,'strained'),0.8); self.assertEqual(state_multiplier(xpconf,'normal'),1.0); self.assertEqual(state_multiplier(xpconf,'rested'),1.1)
  perform_action(self.data,self.st,'action_study_basic',state_label='rested'); self.assertEqual(self.st.skills['skill_van_sach']['xp'],15)
 def test_novelty_window(self): self.st.action_history.append({'day':1,'action_id':'a'}); self.assertEqual(novelty_multiplier(self.st,'a',13,12,1.15),1.0); self.assertEqual(novelty_multiplier(self.st,'a',14,12,1.15),1.15)
 def test_overwork_modifier(self): perform_action(self.data,self.st,'action_study_basic'); perform_action(self.data,self.st,'action_study_basic'); d=perform_action(self.data,self.st,'action_study_basic'); self.assertTrue(any(e.type=='overwork_modifier' for e in d.events))
 def test_routine_limit(self): self.assertEqual(validate_routine(['action_rest']*9,self.data),9); self.assertRaises(ValueError, validate_routine, ['action_rest']*10, self.data)
 def test_quest_transition(self): transition(self.data,self.st,'MQ01A','active'); self.assertEqual(self.st.quests['MQ01A'],'active'); self.assertRaises(ValueError, transition, self.data,self.st,'MQ01A','available')
 def test_event_eligibility(self): cards,log=eligible(self.data,self.st); self.assertTrue(cards); self.assertTrue(log)
 def test_event_draw_seed_group(self): c1,_=draw(self.data,self.st); st2=initial_state(DATA); c2,_=draw(self.data,st2); self.assertEqual([c['id'] for c in c1],[c['id'] for c in c2]); self.assertEqual(len({c['id'] for c in c1}),len(c1)); self.assertEqual(len({c['group'] for c in c1}),len(c1))
 def test_job_pay_mastery_reputation(self): m=self.st.stats['money']; perform_action(self.data,self.st,'action_copyist_job'); self.assertGreater(self.st.stats['money'],m); self.assertGreater(self.st.jobs['job_copyist']['mastery'],0)
 def test_broker_fee_condition(self): perform_action(self.data,self.st,'action_copyist_job'); self.assertEqual(self.st.stats['money'],27)
 def test_item_consumption_quest_sell(self): items={r['id']:r for r in self.data['items']['records']}; self.assertFalse(can_sell(items['item_DOC01_greybox'])); self.assertTrue(can_sell(items['item_rice_ball']))
 def test_obligation(self): perform_action(self.data,self.st,'action_accept_help_vien_ngoai'); self.assertEqual(self.st.obligations[0]['source'],'Vien ngoai stipend'); self.assertEqual(self.st.stats['integrity'],50)
 def test_save_roundtrip(self):
  with tempfile.NamedTemporaryFile(delete=True) as f: save(self.st,f.name); self.assertEqual(self.st.to_dict(),load(f.name).to_dict())

 def test_validator_unknown_unlock(self):
  with tempfile.TemporaryDirectory() as td:
   import shutil,json,pathlib; shutil.copytree(DATA, td, dirs_exist_ok=True); p=pathlib.Path(td)/'quests.json'; d=json.loads(p.read_text()); d['records'][0]['unlocks']=['NOPE']; p.write_text(json.dumps(d)); self.assertTrue(any('unlocks unknown quest' in e for e in validate_data(td)))
 def test_validator_initial_unknown_quest(self):
  with tempfile.TemporaryDirectory() as td:
   import shutil,json,pathlib; shutil.copytree(DATA, td, dirs_exist_ok=True); p=pathlib.Path(td)/'initial_state.json'; d=json.loads(p.read_text()); d['quests']['NOPE']='locked'; p.write_text(json.dumps(d)); self.assertTrue(any('initial_state: unknown quest' in e for e in validate_data(td)))
 def test_validator_dangling_transition_row(self):
  with tempfile.TemporaryDirectory() as td:
   import shutil,json,pathlib; shutil.copytree(DATA, td, dirs_exist_ok=True); p=pathlib.Path(td)/'quests.json'; d=json.loads(p.read_text()); d['records'][0]['transitions']['active']=['completed','missing']; p.write_text(json.dumps(d)); self.assertTrue(any('bad transition target missing' in e for e in validate_data(td)))
 def test_validator_bad_initial_transition(self):
  with tempfile.TemporaryDirectory() as td:
   import shutil,json,pathlib; shutil.copytree(DATA, td, dirs_exist_ok=True); p=pathlib.Path(td)/'quests.json'; d=json.loads(p.read_text()); d['records'][0]['initial_state']='bogus'; p.write_text(json.dumps(d)); self.assertTrue(any('bad initial quest state' in e for e in validate_data(td)))
 def test_mq01_doc01_greybox(self): items={r['id']:r for r in self.data['items']['records']}; self.assertIn('No layout',items['item_DOC01_greybox']['production_lock'])
 def test_self_reliant_continue(self): perform_action(self.data,self.st,'action_market_carry'); self.assertGreaterEqual(self.st.stats['money'],0)
 def test_accept_help_obligation(self): perform_action(self.data,self.st,'action_accept_help_vien_ngoai'); self.assertTrue(self.st.obligations)
 def test_overwork_fail_forward(self):
  self.st.stats['alertness']=20
  events=[]
  for _ in range(3):
   d=perform_action(self.data,self.st,'action_study_basic'); events += [e.type for e in d.events]
   if 'fail_forward_collapse' in events: break
  self.assertIn('fail_forward_collapse',events)
if __name__=='__main__': unittest.main()
