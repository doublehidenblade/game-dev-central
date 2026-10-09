"""Bounded nonvisual PR452 document assertions; no network or external writes.

Run from the repository root. These structural assertions do not replace
independent semantic review or coordinator merge-guard receipts.
"""
import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re

RUNBOOK = Path('project-management/watchdog/RUNBOOK.md')
START = '## Implementation-first Lower City priorities (Craig, 2026-10-09)'
END = '## Coordinator engineering registration — 2026-10-09 12:44 UTC'
BASE_BLOB = '5b661ec6bd75305f73b583b243f686885cfbc624'
ORDER = [217,218,231,195,220,200,197,198,199,201,213,214,219,223,224,212,233,234,185,215,216,222,221,228,226,235,237,236,229,230,248,186,245,192,232,243,225,227,187,238,249,202]

def section(text):
    assert text.count(START) == 1 and text.count(END) == 1
    a, b = text.index(START), text.index(END)
    assert a < b
    return a, b, text[a:b]

def check(text, criterion):
    a, b, new = section(text)
    rows = [line for line in new.splitlines() if re.match(r'\| \d+ \| (High|Medium|Low) \|', line)]
    if criterion == 'C1':
        assert len(rows) == 42
        assert [int(re.search(r'\[td-(\d+)\]', line).group(1)) for line in rows] == ORDER
        assert [int(line.split('|')[1].strip()) for line in rows] == list(range(1,43))
        assert Counter(line.split('|')[2].strip() for line in rows) == {'High':19,'Medium':13,'Low':10}
        for line, task in zip(rows, ORDER):
            assert f'https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-{task}.md' in line
        assert 'They are not 42 unimplemented features' in new
    elif criterion == 'C2':
        required = ['Browser / phone / visual-evidence follow-up is LOW',
          'required acceptance checks and independent verification still gate source',
          'On Craig\'s explicit deployment request', 'disclose failed and unrun checks',
          'not a\n  deployment request, merge acceptance or permission to run Actions',
          'No board or task status is changed here.', 'Shuto stays frozen and NEON paused.',
          'no free/debt recovery is authorized', 'quoted, exactly-once paid recovery',
          'Existing runtime lacks those providers; do not invent them.',
          'Missing providers are implementation dependencies, not browser',
          'STOPPED: prior admission explicitly aborted.']
        # The concrete-defect distinction is a semantic review point backed by
        # these exact persisted phrases, not an automatic gameplay verdict.
        required += ['mesh-index defects, so those repairs remain Medium implementation work.',
                     'publication first', 'author remains frozen']
        for phrase in required:
            assert phrase in new, phrase
        terminal = next(x for x in rows if '[td-238]' in x)
        assert '| Low |' in terminal and 'LOW / PARKED' in terminal
        assert 'Leave terminal and parser work parked.' in terminal
    elif criterion == 'C3':
        original = (text[:a] + text[b:]).encode()
        blob = hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest()
        assert blob == BASE_BLOB, blob
        for private in ('/workspace/', 'codex://', 'task_e_', 'session_id'):
            assert private not in new, private
        assert '[canonical board](../boards/tokyo-drift-3d.md)' in new
        assert '[existing deployment procedure](releases/PUSH-PROCEDURE.md)' in new
    else:
        raise AssertionError(criterion)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--criterion', choices=['C1','C2','C3'], required=True)
    args = p.parse_args()
    text = RUNBOOK.read_bytes().decode('utf-8')
    check(text, args.criterion)
    if args.criterion == 'C1':
        broken = text.replace('| 1 | High |', '| 1 | Low |', 1)
    elif args.criterion == 'C2':
        broken = text.replace('Leave terminal and parser work parked.', 'Start terminal now.', 1)
    else:
        broken = text.replace('# Watchdog runbook', '# Changed unrelated runbook', 1)
    try:
        check(broken, args.criterion)
    except AssertionError:
        pass
    else:
        raise AssertionError('negative control unexpectedly passed')
    print(f'{args.criterion} PASS: actual document assertions; negative control rejected; no runtime or merge acceptance claimed')

if __name__ == '__main__':
    main()
