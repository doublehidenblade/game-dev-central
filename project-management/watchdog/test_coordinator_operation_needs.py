import copy,itertools,json,sys
import test_rules as T,coordinator as C
ops=['implementation','verification','upload','merge','deploy'];count=0;failed=[]
with T.coordinator_forbid_io():
 for state,conflict in itertools.product(('in_review','merged'),(False,True)):
  for flags in itertools.product((False,True),repeat=len(ops)):
   needs=[op for op,want in zip(ops,flags) if want]
   s=T.coordinator_add_review(T.coordinator_fixture(),True)
   s['tasks'][0].update(status=state,needs=needs);s['board'][0]['status']=state;s['prs'][0]['state']='merged' if state=='merged' else 'open'
   if conflict:
    s['reviews'].append({**copy.deepcopy(s['reviews'][0]),'id':'review-2','reviewer_id':'independent-two','verdict':'fail'});s['prs'][0]['review_ids'].append('review-2')
   s=T.coordinator_seal(s);before=copy.deepcopy(s);r=C.evaluate(s,T.COORDINATOR_NOW);assert before==s
   actual={a['operation'] for a in r['actions']}
   if conflict:
    expected={'verification'} if 'verification' in needs else set()
    okay=actual==expected and any('contradictory same-head' in w for w in r['warnings']) and r['status']==('ACTION_REQUIRED' if expected else 'INPUT_REQUIRED')
   elif state=='in_review':
    expected=(set(needs)&{'implementation','verification','upload'})|{'merge'};okay=actual==expected
   else:
    expected=set(needs)&{'verification','upload'};okay=actual==expected
   count+=1;name=f'{state} conflict={conflict} needs={needs}'
   if not okay:failed.append(name)
   print(('PASS ' if okay else 'FAIL ')+name+(' :: '+json.dumps(dict(status=r['status'],operations=sorted(actual),expected=sorted(expected),warnings=r['warnings']),sort_keys=True) if not okay else ''))
print('TOTAL',count,'FAILURES',len(failed))
sys.exit(bool(failed))
