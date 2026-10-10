import copy,json,sys
import test_rules as T,coordinator as C
results=[]
with T.coordinator_forbid_io():
 for state in ('in_review','merged'):
  for case in ('pass_plus_fail','empty_criteria','partial_criteria','self_review','failed_check','old_head_review','no_reviews'):
   s=T.coordinator_add_review(T.coordinator_fixture(),True)
   s['tasks'][0].update(status=state,needs=['verification']);s['board'][0]['status']=state;s['prs'][0]['state']='merged' if state=='merged' else 'open'
   if case=='pass_plus_fail':
    s['reviews'].append({**copy.deepcopy(s['reviews'][0]),'id':'second-review','reviewer_id':'other-independent','verdict':'fail'});s['prs'][0]['review_ids'].append('second-review')
   if case=='empty_criteria':s['reviews'][0]['criteria']={}
   if case=='partial_criteria':s['tasks'][0]['criteria'].append('missing-criterion')
   if case=='self_review':s['reviews'][0]['reviewer_id']='author'
   if case=='failed_check':s['checks'][0]['result']='fail'
   if case=='old_head_review':s['reviews'][0]['head_sha']='e'*40
   if case=='no_reviews':s['reviews']=[];s['prs'][0]['review_ids']=[]
   r=C.evaluate(T.coordinator_seal(s),T.COORDINATOR_NOW)
   okay=any(a['operation']=='verification' for a in r['actions']) and not any(a['operation']=='merge' for a in r['actions'])
   results.append(okay);print(('PASS ' if okay else 'FAIL ')+state+':'+case+(' :: '+json.dumps(r,sort_keys=True) if not okay else ''))
print('TOTAL',len(results),'FAILURES',len(results)-sum(results))
sys.exit(not all(results))
