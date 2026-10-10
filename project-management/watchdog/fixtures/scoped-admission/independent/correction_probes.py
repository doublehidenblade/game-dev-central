"""Independent bounded-correction controls: rule authority vs write conflicts."""
import copy, sys
sys.path.insert(0,sys.argv[1])
import coordinator as C, test_scoped_admission as F

failed=[];count=0
def case(explicit=False):
    c=F.docs_case();s=c['snapshot']
    s['scoped_source']['regions']=[r for r in s['scoped_source']['regions'] if r['path']!='rules.md']
    if explicit:s['scoped_source']['regions'].append(dict(repository=F.REPO,path='rules.md',row_keys=[]))
    F.seal(s)
    return c
def result(name,c,want,reason=None):
    global count
    count+=1;s=c['snapshot'];before=copy.deepcopy(s);F.seal(s);r=C.evaluate(s,F.NOW)
    good=bool(r['actions'])==want and (want or r['status']!='IDLE')
    if reason:good=good and reason in ' '.join(r['warnings'])
    print(('PASS ' if good else 'FAIL ')+name)
    if not good:failed.append(name);print(r)

c=case();result('rule-only current authority need not be write region',c,True)
c=case();F.add_branch(c,{'rules.md':'Unmerged future rule proposal'},pr=True);result('known rule-only proposal does not block immutable current rule reader',c,True)
c=case(True);F.add_branch(c,{'rules.md':'Unmerged future rule proposal'},pr=True);result('explicit rule dependency region still blocks proposal',c,False,'overlapping')
c=case();F.add_branch(c,{'rules.md':'Proposed rule','doc.md':'Actual candidate-path conflict'},pr=True);result('mixed rule and actual write proposal still blocks',c,False,'overlapping')
c=case();F.add_branch(c,{'board.md':c['board'].replace('# Board','# Changed ownership context')},pr=True);result('real-shaped PR377 non-row board context still blocks',c,False,'context')
c=case();F.add_branch(c,{'doc.md':'Different same-task source bytes'},pr=True);result('real-shaped PR533 same task-file writer still blocks',c,False,'overlapping')
c=case();c['snapshot']['evidence_policy']['ops-docs']['authority']['rules'][0]['ref']['blob']='f'*40;result('read-only canonical rule still requires exact current blob',c,False)
c=case();s=c['snapshot'];s['evidence_policy']['ops-docs']['submission']['acknowledgment']['rules'][0]['ref']['blob']='f'*40;result('changed author rule acknowledgment still blocks',c,False)
c=case();F.add_branch(c,{'rules.md':'Unmerged proposal'},pr=True);s=c['snapshot'];s['owners']=[dict(id='owner',repository=F.REPO,task_id='ops-docs',operation='merge',owner_id='coordinator-A',executor_id='native',state='unknown')];result('rule-only proposal cannot hide relevant unknown owner',c,False)
c=case();F.add_branch(c,{'rules.md':'Unmerged proposal'},pr=True);s=c['snapshot'];s['blockers']=[dict(id='denial',repository=F.REPO,task_id='*',operations=['*'],executors=['*'],kind='denial',reason='Retained')];result('rule-only proposal cannot hide wildcard denial',c,False)

def candidate_rule_writer():
    c=case(True);s=c['snapshot'];w=c['world']
    w.file('rules.md','Candidate also proposes a rule change')
    head=w.commit(c['head'])
    for row in (s['tasks'][0],s['board'][0],s['prs'][0],s['branches'][0],s['scoped_source']['binding']):row['head_sha']=head
    for kind in ('branches','prs'):
        for row in s['scoped_source']['inventory'][kind]:
            if row['proof']['kind']=='candidate':row['head_sha']=head
    s['scoped_source']['candidate']['head_chain']=[head,c['head'],c['source'],c['base']]
    s['evidence_policy']['ops-docs']['authority']['candidate']['artifact_head']=head
    s['tasks'][0]['needs']=['verification'];s['scoped_source']['binding']['operation']='verification'
    return c
c=candidate_rule_writer();result('candidate rule writer positive control before competing proposal',c,True)
c=candidate_rule_writer();F.add_branch(c,{'rules.md':'Competing unmerged rule change'},pr=True);result('candidate rule writer keeps genuine rule overlap hold',c,False,'overlapping')
c=candidate_rule_writer();c['snapshot']['scoped_source']['regions']=[r for r in c['snapshot']['scoped_source']['regions'] if r['path']!='rules.md'];result('candidate rule write cannot omit its protected path',c,False)

print('TOTAL',count,'FAILURES',len(failed),failed)
sys.exit(bool(failed))
