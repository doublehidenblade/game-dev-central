"""Actual read-only CLI processes with fresh, explicitly synthetic fixtures."""
import datetime, hashlib, json, os, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root))
import test_scoped_admission as F, coordinator as C, coordinator_cli as CLI
F.NOW=datetime.datetime.now(datetime.timezone.utc)
F.STAMP=F.NOW.isoformat()
case=F.docs_case();snapshot=case['snapshot'];action=C.evaluate(snapshot,F.NOW)['actions'][0]
work=pathlib.Path(sys.argv[2]).resolve();work.mkdir(exist_ok=True)
snapshot_path=work/'synthetic-cli-snapshot.json';decision_path=work/'synthetic-cli-decision.json'
snapshot_path.write_text(json.dumps(snapshot));decision_path.write_text(json.dumps(action))
def hashes():return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
before=hashes(); count=0; failed=[]
for alias in sorted(CLI.ALIASES | CLI.RETIRED):
    args=[sys.executable,str(root/'watch.py'),alias]
    if alias in CLI.ALIASES:
        args+=['--snapshot',str(snapshot_path)]
    if alias=='dispatch-guard':
        args+=['--decision',str(decision_path),'--task',action['task_id'],'--operation',action['operation'],'--executor',action['executor_id'],'--owner',action['owner_id'],'--head',action['head_sha']]
    result=subprocess.run(args,cwd=work,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=10)
    expected=('INPUT_REQUIRED',2) if alias in CLI.RETIRED else ('GO',0) if alias=='dispatch-guard' else ('ACTION_REQUIRED',3 if alias=='idle-defect-check' else 0)
    try:got=json.loads(result.stdout)
    except Exception:got={}
    good=(got.get('status'),result.returncode)==expected
    if alias in CLI.RETIRED:good=good and got.get('reason')=='RETIRED_UNGUARDED_ROUTE'
    if alias in CLI.ALIASES-{'dispatch-guard'}:good=good and got.get('actions')==[action]
    count+=1;print(('PASS ' if good else 'FAIL ')+alias)
    if not good:failed.append(alias);print(result.stdout,result.stderr)
same=hashes()==before
count+=1;print(('PASS ' if same else 'FAIL ')+'source/state filesystem unchanged')
if not same:failed.append('filesystem unchanged')
print('TOTAL',count,'FAILURES',len(failed),failed)
sys.exit(bool(failed))
