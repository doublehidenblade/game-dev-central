import copy,json,sys
import test_rules as T,coordinator as C
failures=0
with T.coordinator_forbid_io():
 for needs in (['verification','upload'],['upload']):
  s=T.coordinator_add_review(T.coordinator_fixture(),True)
  s['tasks'][0].update(status='merged',needs=needs);s['board'][0]['status']='merged';s['prs'][0]['state']='merged'
  s['reviews'].append({**copy.deepcopy(s['reviews'][0]),'id':'review-2','reviewer_id':'another-independent-reviewer','verdict':'fail'});s['prs'][0]['review_ids'].append('review-2')
  result=C.evaluate(T.coordinator_seal(s),T.COORDINATOR_NOW)
  okay=not any(a['operation']=='upload' for a in result['actions']) and any('contradictory same-head' in w for w in result['warnings'])
  failures+=not okay
  print(('PASS ' if okay else 'FAIL ')+repr(needs)+' :: '+json.dumps(result,sort_keys=True))
print('TOTAL 2 FAILURES',failures)
sys.exit(bool(failures))
