import copy,json,sys
from datetime import timedelta
import test_rules as T,coordinator as C
count=0;failed=[]
def ck(name,truth,r):
 global count
 count+=1;print(('PASS ' if truth else 'FAIL ')+name+((' :: '+json.dumps(r,sort_keys=True)) if not truth else ''))
 if not truth:failed.append(name)
def ev(s):
 before=copy.deepcopy(s);r=C.evaluate(s,T.COORDINATOR_NOW);assert before==s;return r
def merged():
 s=T.coordinator_add_review(T.coordinator_fixture());s['tasks'][0].update(status='merged',needs=['verification']);s['board'][0]['status']='merged';s['prs'][0]['state']='merged';s['branches']=[]
 return T.coordinator_seal(s)
def ops(r):return [a['operation'] for a in r['actions']]
with T.coordinator_forbid_io():
 s=merged();r=ev(s);ck('merged PR independently corroborates source after branch deletion',ops(r)==['verification'],r)
 for failure in ('wronghead','missingpr','closedpr','twoexactmerged','selfreview','ownerunknown','prsreadfail','stops','denial'):
  s=merged()
  if failure=='wronghead':s['prs'][0]['head_sha']='e'*40
  if failure=='missingpr':s['prs']=[]
  if failure=='closedpr':s['prs'][0]['state']='closed'
  if failure=='twoexactmerged':s['prs'].append({**s['prs'][0],'id':T.COORDINATOR_REPO+'#2'})
  if failure=='selfreview':s['executors'][0]['owner_id']='author'
  if failure=='stops' or failure=='denial':s['blockers']=[dict(id='hold',repository=T.COORDINATOR_REPO,task_id='task-a',operations=['verification'],executors=['*'],kind='stop' if failure=='stops' else 'denial',reason='user stopped or denied review')]
  s=T.coordinator_seal(s)
  if failure=='ownerunknown':next(r for r in s['sources'] if r['kind']=='owners')['read_status']='unreadable'
  if failure=='prsreadfail':next(r for r in s['sources'] if r['kind']=='prs')['read_status']='unreadable'
  r=ev(s);ck('merged review retains '+failure,not r['actions'] and (failure not in ('selfreview','stops','denial') or True),r)
 for branchfailure in ('unmapped','partial','missing'):
  s=T.coordinator_add_review(T.coordinator_fixture(),True);s['tasks'][0]['needs']=['implementation','verification','upload','merge','deploy']
  if branchfailure=='unmapped':s['branches'].append(dict(id='unknown',repository=T.COORDINATOR_REPO,task_id=None,head_sha='f'*40))
  s=T.coordinator_seal(s)
  if branchfailure=='partial':next(r for r in s['sources'] if r['kind']=='branches')['read_status']='partial'
  if branchfailure=='missing':s['sources']=[r for r in s['sources'] if r['kind']!='branches']
  r=ev(s);ck('branch '+branchfailure+' exception remains verification-only',ops(r)==['verification'] and bool(r['warnings']),r)
 s=merged();s['tasks'][0]['needs']=['verification','implementation','merge'];r=ev(s);ck('postmerge no duplicate merge or coding',ops(r)==['verification'] and bool(r['warnings']),r)
 # Disputed same-head acceptance: fresh pass and fail should be resolvable by an independent read-only reviewer.
 s=T.coordinator_add_review(T.coordinator_fixture(),True);s['tasks'][0].update(status='merged',needs=['verification']);s['board'][0]['status']='merged';s['prs'][0]['state']='merged'
 s['reviews'].append({**copy.deepcopy(s['reviews'][0]),'id':'second-review','reviewer_id':'second-independent-reviewer','verdict':'fail'});s['prs'][0]['review_ids'].append('second-review')
 r=ev(T.coordinator_seal(s));ck('disputed postmerge acceptance permits fresh independent verification',ops(r)==['verification'] and bool(r['warnings']),r)
print('TOTAL',count,'FAILURES',len(failed),failed)
sys.exit(bool(failed))
