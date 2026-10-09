"""Independent adversarial source-scope review. Synthetic data; never authority."""
import copy, contextlib, io, json, pathlib, sys
from datetime import timedelta
from unittest.mock import patch

sys.path.insert(0, sys.argv[1])
import coordinator as C, coordinator_cli as CLI, scoped_admission as S
import test_scoped_admission as F

count = 0
failures = []
def check(name, condition, detail=None):
    global count
    count += 1
    print(('PASS ' if condition else 'FAIL ') + name)
    if not condition:
        failures.append(name)
        if detail is not None: print(json.dumps(detail, sort_keys=True, default=str))

def ev(s):
    before = copy.deepcopy(s)
    result = C.evaluate(s, F.NOW)
    assert before == s, 'mutated snapshot'
    return result

def probe(name, mutate, allowed=False, reseal=True):
    case = F.docs_case(); s = case['snapshot']
    mutate(s, case)
    if reseal: F.seal(s)
    try:
        result = ev(s)
        check(name, bool(result['actions']) == allowed and (allowed or result['status'] != 'IDLE'), result)
    except Exception as exc:
        check(name + ' uncaught exception', False, repr(exc))

probe('unmodified document-only production policy', lambda s,c:None, True)
row='| task-a | reserved |\n'
section1='# Active\n| Task | State |\n|---|---|\n'
section2='# Historical\n| Task | State |\n|---|---|\n'
check('row movement into empty semantic table detected',S.board_rows((section1+row+'\n'+section2).encode())!=S.board_rows((section1+'\n'+section2+row).encode()))
for operation in ('implementation','verification','upload','merge'):
    def setup(s,c,op=operation):
        s['tasks'][0]['needs']=[op]
        s['scoped_source']['binding']['operation']=op
        if op=='implementation':
            s['executors'][0].update(owner_id='worker-A',resume_task='ops-docs')
            s['scoped_source']['binding']['owner_id']='worker-A'
    probe('positive exact '+operation, setup, True)
    for kind in ('stop','denial','security','cancelled'):
        def stop(s,c,op=operation,kind=kind):
            setup(s,c,op)
            s['blockers']=[dict(id='halt',repository=F.REPO,task_id='*',operations=['*'],executors=['*'],kind=kind,reason='retained')]
        probe(operation+' retains '+kind,stop)

for state in ('unknown','busy','unavailable'):
    probe('executor '+state, lambda s,c,state=state:s['executors'][0].update(state=state))
probe('executor capabilities absent',lambda s,c:s['executors'][0].update(capabilities=[]))
probe('authority request cancelled',lambda s,c:s['requests'][0].update(state='cancelled'))
probe('authority request unverified',lambda s,c:s['requests'][0].update(authority_verified=False))
probe('authority wrong operation',lambda s,c:s['requests'][0].update(operations=['verification']))
probe('authority wrong executor',lambda s,c:s['requests'][0].update(executors=['nonexistent']))
probe('task owner and board disagree',lambda s,c:s['board'][0].update(owner_id='another-owner'))
for mode in ('task-owner','board-owner','unknown-state','paused-state'):
    def dependency(s,c,mode=mode):
        dep=copy.deepcopy(s['tasks'][0])
        dep.update(id='dependent-task',head_sha=c['base'],status='in_progress',owner_id=None,author_id='another-worker',needs=[])
        if mode=='task-owner':dep['owner_id']='another-worker'
        if mode=='unknown-state':dep['status']='unknown'
        if mode=='paused-state':dep['status']='paused'
        board={k:dep[k] for k in ('id','repository','head_sha','status','owner_id')}
        if mode=='board-owner':board['owner_id']='another-worker'
        s['tasks'].append(dep);s['board'].append(board)
        s['scoped_source']['task_ids'].append(dep['id'])
        if 'related_task_ids' in s['scoped_source']:
            s['scoped_source']['related_task_ids'].append(dep['id'])
    probe('relevant dependency '+mode,dependency)
for state in ('paused','cancelled','done-pending-verdict'):
    probe('board retains '+state,lambda s,c,state=state:s['board'][0].update(status=state))
for kind in ('shuto','neon-drift'):
    probe('frozen '+kind,lambda s,c,kind=kind:s['tasks'][0].update(project=kind))
for k in ('triggers_checked','merge_runs_actions','merge_deploys'):
    probe('publication '+k,lambda s,c,k=k:s['policies'][0].update({k:k!='triggers_checked'}))
probe('zero policies',lambda s,c:s.update(policies=[]))
probe('two conflicting policies',lambda s,c:s['policies'].append({**s['policies'][0],'id':'unsafe','merge_deploys':True}))

for table in ('reviews','checks'):
    for bad in ('missing','fail','pending','stale','future','head'):
        def mutate(s,c,table=table,bad=bad):
            if bad=='missing':
                s[table]=[];s['prs'][0]['review_ids' if table=='reviews' else 'check_ids']=[]
            elif bad in ('fail','pending'):s[table][0]['verdict' if table=='reviews' else 'result']=bad
            elif bad=='stale':s[table][0]['observed_at']=(F.NOW-timedelta(minutes=15)).isoformat();s[table][0].pop('performed_at')
            elif bad=='future':s[table][0]['observed_at']=(F.NOW+timedelta(seconds=1)).isoformat()
            else:s[table][0]['head_sha']=c['base']
        probe(table+' '+bad,mutate)
probe('contradictory current review',lambda s,c:(s['reviews'].append({**copy.deepcopy(s['reviews'][0]),'id':'contrary','reviewer_id':'reviewer-C','verdict':'fail'}),s['prs'][0]['review_ids'].append('contrary')))
probe('contradictory current check',lambda s,c:(s['checks'].append({**s['checks'][0],'id':'contrary','result':'fail'}),s['prs'][0]['check_ids'].append('contrary')))

for key in ('task_id','operation','executor_id','owner_id','head_sha'):
    case=F.docs_case();s=case['snapshot'];action=ev(s)['actions'][0]
    target={k:action[k] for k in ('task_id','operation','executor_id','owner_id','head_sha')}
    target[key]='other' if key!='head_sha' else 'f'*40
    check('guard rejects wrong '+key,C.revalidate(s,action,target,F.NOW)['status']=='NO_GO')
case=F.docs_case();s=case['snapshot'];action=ev(s)['actions'][0]
target={k:action[k] for k in ('task_id','operation','executor_id','owner_id','head_sha')}
check('guard rejects extra target fields',C.revalidate(s,action,{**target,'repository':F.REPO},F.NOW)['status']=='NO_GO')
check('guard expires exactly at15minutes',C.revalidate(s,action,target,F.NOW+timedelta(minutes=15))['status']=='NO_GO')

for mode in ('missing-object','altered-object','no-query','receipt-extra','receipt-duplicate','inventory-missing','unknown-proof','normalized-head'):
    def mutate(s,c,mode=mode):
        scope=s['scoped_source']
        if mode=='missing-object':scope['objects']=[]
        elif mode=='altered-object':
            scope['objects']=copy.deepcopy(scope['objects'])
            scope['objects'][F.REPO][c['head']]['base64']='YWx0ZXJlZA=='
        elif mode=='no-query':scope['receipts'][0]['query_digest']=''
        elif mode=='receipt-extra':scope['receipts'][0]['unrelated']=True
        elif mode=='receipt-duplicate':scope['receipts'].append(copy.deepcopy(scope['receipts'][0]))
        elif mode=='inventory-missing':scope['inventory']['branches']=scope['inventory']['branches'][:1]
        elif mode=='unknown-proof':scope['inventory']['branches'][0]['proof']={'kind':'unrelated','unrelated':True}
        elif mode=='normalized-head':s['branches'][0]['head_sha']=c['source']
    probe(mode,mutate,reseal=False)

for name,changes,want in [
    ('disjoint file',{'other.txt':'safe'},True),
    ('sibling source overlap',{'doc.md':'unsafe'},False),
    ('sibling dependency overlap',{'rules.md':'unsafe'},False),
    ('row-only unrelated change',{'board.md':F.docs_case()['board'].replace('unrelated | open','unrelated | paused')},True),
    ('target row ownership change',{'board.md':F.docs_case()['board'].replace('ops-docs | open','ops-docs | other-owner')},False),
    ('table header scope change',{'board.md':F.docs_case()['board'].replace('# Board','# Stopped')},False),
]:
    def overlap(s,c,changes=changes,name=name):
        # A genuine explicitly declared dependency remains protected. Canonical
        # rule authority alone is a read-only version pin after the correction.
        if name=='sibling dependency overlap' and not any(r['path']=='rules.md' for r in s['scoped_source']['regions']):
            s['scoped_source']['regions'].append(dict(repository=F.REPO,path='rules.md',row_keys=[]))
        F.add_branch(c,changes,pr=True)
    probe(name,overlap,want)

for path in ('doc.md','board.md'):
    def mode_change(s,c,path=path):
        w=c['world'];store=F.ep.GitObjects(w.objects)
        tree,_=store.commit(F.REPO,c['base'])
        raw=store.read(F.REPO,tree,'tree')
        newtree=w.object('tree',raw.replace(('100644 '+path+'\0').encode(),('100755 '+path+'\0').encode()))
        head=w.object('commit',f'tree {newtree}\nparent {c["base"]}\nauthor Fixture <fixture@example.invalid> 1791554400 +0000\ncommitter Fixture <fixture@example.invalid> 1791554400 +0000\n\nMode test\n')
        proof=dict(kind='disjoint',fork_sha=c['base'],base_chain=[c['base']],head_chain=[head,c['base']])
        s['scoped_source']['inventory']['branches'].append(dict(id=F.REPO+':refs/heads/mode',repository=F.REPO,head_sha=head,proof=proof))
    probe('relevant file mode overlap '+path,mode_change)

print('TOTAL',count,'FAILURES',len(failures),failures)
sys.exit(bool(failures))
