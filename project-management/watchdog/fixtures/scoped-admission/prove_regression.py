"""Offline before/after scope regression; original code must match its Git blob."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import coordinator
from test_scoped_admission import docs_case, NOW

p = argparse.ArgumentParser()
p.add_argument('--original', required=True)
args = p.parse_args()
raw = Path(args.original).read_bytes()
blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
assert blob == '1e87c500bd8c7890d59e2e83dc614c0d58bbb6b9', 'wrong original source'
spec = importlib.util.spec_from_file_location('scoped_original_coordinator', args.original)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
snapshot = docs_case()['snapshot']
before = original.evaluate(snapshot, NOW)
after = coordinator.evaluate(snapshot, NOW)
assert before['status'] == 'INPUT_REQUIRED' and not before['actions']
assert after['status'] == 'ACTION_REQUIRED' and len(after['actions']) == 1
assert after['source_scope']['global_coverage'] == 'unknown'
print(json.dumps({'original_blob': blob, 'original': before['status'], 'repaired': after['status'],
                  'global_coverage': 'unknown', 'result': 'PASS', 'live_authorization': False}))
