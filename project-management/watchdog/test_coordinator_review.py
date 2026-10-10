import copy,contextlib,io,json,sys
from datetime import timedelta
from unittest import mock
import test_rules as T,coordinator as C,coordinator_cli as CLI,watch as W
N=T.COORDINATOR_NOW
checks=[]
def check(name,yes,result=None):
 checks.append(bool(yes));print(('PASS ' if yes else 'FAIL ')+name+((' :: '+json.dumps(result,sort_keys=True)) if not yes else ''))
def ev(s,at=N):
 old=copy.deepcopy(s);r=C.evaluate(s,at);assert s==old;return r
def ops(r):return [(a['task_id'],a['operation'],a['executor_id']) for a in r['actions']]
def base():
 s=T.coordinator_fixture();req=s['tasks'][0]['requirements']['implementation']
 req.update(model='gpt-6-astra',effort='xhigh',runtime_confirmation_required=False)
 s['executors'][0].update(observed_model=None,observed_effort=None,runtime_confirmed=False,selected_model='gpt-6-astra',selected_effort='xhigh',selection_verified=True,selection_evidence='Synthetic verified supported launch selection, Python/Godot inspected')
 return s
with T.coordinator_forbid_io():
 s=base();r=ev(s);check('verified native selection available without false runtime',ops(r)==[('task-a','implementation','native')] and not s['executors'][0]['runtime_confirmed'],r)
 s=base();s['tasks'][0]['requirements']['implementation']['runtime_confirmation_required']=True;r=ev(s);check('required runtime attestation not substituted',r['status']=='INPUT_REQUIRED' and not r['actions'],r)
 for case in ('none','unverified','incomplete','noevidence','wrongmodel','wrongeffort','toolmissing','actualmismatch'):
  s=base();ex=s['executors'][0]
  if case=='none':
   for k in ('selected_model','selected_effort','selection_verified','selection_evidence'):ex.pop(k)
  if case=='unverified':ex['selection_verified']=False
  if case=='incomplete':ex.pop('selected_effort')
  if case=='noevidence':ex['selection_evidence']=' '
  if case=='wrongmodel':ex['selected_model']='gpt-other'
  if case=='wrongeffort':ex['selected_effort']='low'
  if case=='toolmissing':ex['capabilities']=[]
  if case=='actualmismatch':ex.update(runtime_confirmed=True,observed_model='gpt-other',observed_effort='xhigh')
  r=ev(s);check('selection rejects '+case,not r['actions'] and (case not in ('none','unverified','incomplete','noevidence') or r['status']=='INPUT_REQUIRED'),r)
 s=base();r=ev(s);a=r['actions'][0];target={k:a[k] for k in ('task_id','operation','executor_id','owner_id','head_sha')}
 s['executors'][0]['selection_evidence']='Different later supported launch observation';check('selection evidence change invalidates receipt',C.revalidate(s,a,target,N)['status']=='NO_GO')
 s=T.coordinator_add_review(T.coordinator_fixture(),True)
 for table in ('reviews','checks'):s[table][0]['performed_at']=(N-timedelta(days=200)).isoformat()
 original=copy.deepcopy(s);r=ev(s);check('old immutable evidence freshly observed accepted',ops(r)==[('task-a','merge','native')] and s==original,r)
 for table in ('reviews','checks'):
  s=copy.deepcopy(original);s[table][0]['observed_at']=(N-timedelta(minutes=14)).isoformat();r=ev(s)
  check('record expiry limits receipt '+table,r['actions'][0]['expires_at']==(N+timedelta(minutes=1)).isoformat(),r)
  a=r['actions'][0];target={k:a[k] for k in ('task_id','operation','executor_id','owner_id','head_sha')}
  check('record exact expiry NO_GO '+table,C.revalidate(s,a,target,N+timedelta(minutes=1))['status']=='NO_GO')
  s=copy.deepcopy(original);s[table][0]['observed_at']=(N+timedelta(seconds=1)).isoformat();r=ev(s);check('future individual observation rejects '+table,r['status']=='INPUT_REQUIRED',r)
  s=copy.deepcopy(original);s[table][0]['performed_at']=(N+timedelta(seconds=1)).isoformat();r=ev(s);check('performed after read rejects '+table,r['status']=='INPUT_REQUIRED',r)
 # Concrete adoption cases
 s=T.coordinator_add_review(T.coordinator_fixture())
 s['branches'].append(dict(id='unmapped-unrelated-branch',repository=T.COORDINATOR_REPO,task_id=None,head_sha='e'*40))
 r=ev(T.coordinator_seal(s));check('unmapped unrelated branch does not block exact-head read-only review',ops(r)==[('task-a','verification','native')] and bool(r['warnings']),r)
 s=T.coordinator_add_review(T.coordinator_fixture());s['tasks'][0].update(status='merged',needs=['verification']);s['board'][0].update(status='merged');s['prs'][0]['state']='merged'
 r=ev(T.coordinator_seal(s));check('explicit post-merge exact-head verification remains actionable',ops(r)==[('task-a','verification','native')],r)
 # Document existing behavior where a stopped completed lane must not block another.
 s=T.coordinator_fixture();b=copy.deepcopy(s['tasks'][0]);b['id']='task-b';s['tasks'].append(b);s['board'].append({k:b[k] for k in ('id','repository','head_sha','status','owner_id')});s['branches'].append({**s['branches'][0],'id':'b','task_id':'task-b'});s['board'][0]['status']='merged'
 r=ev(T.coordinator_seal(s));check('terminal contradiction retains independent safe lane',[(a['task_id'],a['operation']) for a in r['actions']]==[('task-b','implementation')] and bool(r['warnings']),r)
 s=T.coordinator_fixture();s['tasks'][0].update(status='merged',needs=['implementation']);s['board'][0]['status']='merged';r=ev(s);check('merged task cannot request duplicate implementation',not r['actions'] and r['status']=='INPUT_REQUIRED',r)
 for cmd in sorted(CLI.ALIASES):
  with contextlib.redirect_stdout(io.StringIO()) as out:
   code=CLI.run(cmd,['--snapshot'],N)
  check('malformed parser JSON '+cmd,code==2 and json.loads(out.getvalue())['status']=='INPUT_REQUIRED')
print('TOTAL',len(checks),'FAILURES',len(checks)-sum(checks))
sys.exit(not all(checks))
