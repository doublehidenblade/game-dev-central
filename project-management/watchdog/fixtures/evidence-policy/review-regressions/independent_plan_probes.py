import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'candidate/project-management/watchdog'))
import evidence_policy as ep
import test_evidence_policy as f

def run(label,c):
 r=ep.evaluate_admission(c['authority'],c['submission'],c['world'].objects,f.NOW)
 print(label,json.dumps(r,sort_keys=True))
 Path(__file__).with_name(label+'.packet.json').write_text(json.dumps({'authority':c['authority'],'submission':c['submission'],'objects':c['world'].objects},indent=2))

c=f.make_case();c['submission']['plans']['C1']['artifacts'][0]['type']='document';run('required-command-document-only-plan',c)
c=f.make_case(visual=True);c['submission']['plans']['C1']['artifacts']=c['submission']['plans']['C1']['artifacts'][:1];run('visual-one-image-plan',c)
c=f.make_case(visual=True,task_transform=lambda t:t['evidence_policy']['C1'].update(checks=[{'id':'pixel-guard','command':['python3','guard.py']}]))
run('visual-with-required-command-plan',c)
