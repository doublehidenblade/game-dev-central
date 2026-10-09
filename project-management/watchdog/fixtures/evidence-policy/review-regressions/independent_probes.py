import sys,json
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'candidate/project-management/watchdog'))
import evidence_policy as ep
import test_evidence_policy as f

def result(c): return ep.evaluate_completion(c['authority'],c['submission'],c['world'].objects,f.NOW)

c=f.make_case();print('positive',result(c)['status'])
a,w,s=c['authority'],c['world'],c['submission']
failed=deepcopy(c['execution']);failed.update(exit_code=1,output='FAILED: mapped instance-A invariant broken')
w.file('qa/new-failure.json',failed)
head=w.commit(a['candidate']['artifact_head']);a['candidate']['artifact_head']=head
ref=w.ref(head,'qa/new-failure.json');f.attest(c,'execution',ref,'test-observer')
finding={'id':'F-current-failed-execution','repository':f.REPO,'head':head,'observed_at':f.STAMP,'task_id':'ops-example','criterion_id':'C1','evidence':[ref],'code':'FAILED_CHECK','coverage':['instance-A'],'limitations':[]}
finding['fingerprint']=ep.finding_fingerprint(finding);a['findings']=[finding]
f.decision(c,'existing_rule')
print('same-source authenticated failure plus existing-rule disposition:',json.dumps(result(c),sort_keys=True))
Path(__file__).with_name('contradictory-current-failure.packet.json').write_text(json.dumps({'authority':a,'submission':s,'objects':w.objects},indent=2))
