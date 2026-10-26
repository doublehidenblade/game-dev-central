#!/usr/bin/env python3
"""Regression tests for watch.py's _auto_deregister binding (2026-10-26).

The v1 auto-deregister retired whatever registration sat under a task
when record-pending ran. Dot's review caught the flaw: a task
re-registered for new work after an old PR merged would lose its NEW
worker's registration to a replayed/late record-pending for the old PR.

Binding under test: a registration is retired only when its
dispatched_at predates the PR's real merged_at (fetched via _gh).

Run: python3 tests/test_auto_deregister.py  (exit 0 = all pass)
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
WATCH_DIR = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, WATCH_DIR)  # watch.py imports sibling modules (coordinator_cli)
spec = importlib.util.spec_from_file_location(
    "watch", os.path.join(WATCH_DIR, "watch.py"))
watch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(watch)

MERGED_AT = "2026-10-25T20:00:00Z"  # the "old PR" merge time


def run_case(workers, gh_result=None, gh_raises=False):
    """Run _auto_deregister('td-T', 1105, 'tokyo') against a sandboxed
    state file and a stubbed _gh. Returns (state_after, stdout_text)."""
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump({"workers": workers, "notes": []}, f)
    old_path, old_gh = watch.STATE_PATH, watch._gh
    watch.STATE_PATH = path

    def fake_gh(_path):
        if gh_raises:
            raise RuntimeError("api down")
        return gh_result if gh_result is not None else {"merged_at": MERGED_AT}

    watch._gh = fake_gh
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            watch._auto_deregister("td-T", 1105, "tokyo")
        with open(path) as f:
            return json.load(f), buf.getvalue()
    finally:
        watch.STATE_PATH, watch._gh = old_path, old_gh
        os.unlink(path)


failures = []

# Case A — the normal lifecycle: worker dispatched before its PR merged
# is retired by the merge's record-pending.
state, out = run_case({"td-T": {"kind": "subagent",
                                "dispatched_at": "2026-10-24T03:00:00+00:00"}})
ok = "td-T" not in state["workers"] and "DEREGISTERED td-T" in out
print(("PASS" if ok else "FAIL"), "A: pre-merge registration retired")
if not ok:
    failures.append("A")

# Case B — THE regression: task re-registered for new work AFTER the old
# PR merged; a replayed record-pending for the old PR must not touch it.
state, out = run_case({"td-T": {"kind": "subagent",
                                "dispatched_at": "2026-10-26T00:19:16+00:00"}})
ok = "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out
print(("PASS" if ok else "FAIL"), "B: re-registered worker survives replay")
if not ok:
    failures.append("B")

# Case C — no registration under the task: silent no-op, no crash.
state, out = run_case({})
ok = state["workers"] == {} and "DEREGISTER" not in out
print(("PASS" if ok else "FAIL"), "C: unregistered task is a no-op")
if not ok:
    failures.append("C")

# Case D — the PR lookup fails: keep the registration, report the skip
# (never raise into the merge bookkeeping, never fail silently).
state, out = run_case({"td-T": {"kind": "subagent",
                                "dispatched_at": "2026-10-24T03:00:00+00:00"}},
                      gh_raises=True)
ok = "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out
print(("PASS" if ok else "FAIL"), "D: API failure keeps registration, prints skip")
if not ok:
    failures.append("D")

# Case E — PR not actually merged (merged_at null): the timestamp check
# cannot bind, fall through to the v1 behavior and retire. Documents the
# known edge; record-pending is only ever called for merged PRs.
state, out = run_case({"td-T": {"kind": "subagent",
                                "dispatched_at": "2026-10-24T03:00:00+00:00"}},
                      gh_result={"merged_at": None})
ok = "td-T" not in state["workers"] and "DEREGISTERED td-T" in out
print(("PASS" if ok else "FAIL"), "E: null merged_at falls through to retire")
if not ok:
    failures.append("E")

if failures:
    print("FAILED cases:", ", ".join(failures))
    sys.exit(1)
print("ALL PASS")
