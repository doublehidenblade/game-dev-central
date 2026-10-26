#!/usr/bin/env python3
"""Regression tests for watch.py's _auto_deregister binding (2026-10-26).

v1 retired whatever registration sat under a task when record-pending
ran. Dot's reviews of v1 and v2 established the bar: chronology is not
identity, and missing evidence is not permission — retirement must FAIL
CLOSED. v3 retires only when every check positively binds the
registration to the PR: the ledger's recorded task matches (dedupe
verifies, never trusts the caller), a supplied --session matches the
registration's session exactly, dispatched_at exists and parses, the
game resolves to a repo, merged_at exists and parses, and
dispatched_at predates merged_at.

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
BEFORE = "2026-10-24T03:00:00+00:00"  # dispatched before the merge
AFTER = "2026-10-26T00:19:16+00:00"  # dispatched after the merge

failures = []


def check(name, ok):
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        failures.append(name)


def run_case(workers, gh_result=None, gh_raises=False, game="tokyo",
             expect_session=None):
    """Run _auto_deregister against a sandboxed state file and a stubbed
    _gh. Returns (state_after, stdout_text)."""
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
            watch._auto_deregister("td-T", 1105, game, expect_session)
        with open(path) as f:
            return json.load(f), buf.getvalue()
    finally:
        watch.STATE_PATH, watch._gh = old_path, old_gh
        os.unlink(path)


REG_BEFORE = {"td-T": {"kind": "subagent", "session": "sess-1",
                       "dispatched_at": BEFORE}}

# A — the normal lifecycle: worker dispatched before its PR merged is
# retired by the merge's record-pending.
state, out = run_case(dict(REG_BEFORE))
check("A: pre-merge registration retired",
      "td-T" not in state["workers"] and "DEREGISTERED td-T" in out)

# B — the v1 regression: task re-registered for new work AFTER the old
# PR merged; a replayed record-pending for the old PR must not touch it.
state, out = run_case({"td-T": {"kind": "subagent", "session": "sess-2",
                                "dispatched_at": AFTER}})
check("B: re-registered worker survives replay",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# C — no registration under the task: silent no-op, no crash.
state, out = run_case({})
check("C: unregistered task is a no-op",
      state["workers"] == {} and "DEREGISTER" not in out)

# D — the PR lookup fails: keep the registration, report the skip
# (never raise into the merge bookkeeping, never fail silently).
state, out = run_case(dict(REG_BEFORE), gh_raises=True)
check("D: API failure keeps registration, prints skip",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# E — REVERSED from v2 (dot's review): a null merged_at is missing
# evidence, not permission. The registration must SURVIVE.
state, out = run_case(dict(REG_BEFORE), gh_result={"merged_at": None})
check("E: null merged_at keeps registration (fail closed)",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# F — a registration with no parseable dispatched_at cannot be bound to
# the PR: survives.
state, out = run_case({"td-T": {"kind": "subagent", "session": "sess-1"}})
check("F: missing dispatched_at keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# G — an unknown game cannot resolve a repo to verify the merge:
# survives.
state, out = run_case(dict(REG_BEFORE), game="atlantis")
check("G: unknown game keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# I — session binding: the caller names the merging worker's session; a
# registration carrying a different session is not that worker: survives.
state, out = run_case(dict(REG_BEFORE), expect_session="sess-OTHER")
check("I: session mismatch keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# J — session binding, matching: retires.
state, out = run_case(dict(REG_BEFORE), expect_session="sess-1")
check("J: session match retires registration",
      "td-T" not in state["workers"] and "DEREGISTERED td-T" in out)


# H — dedupe must verify the ledger task, never trust the caller's.
# The ledger records PR #1105 under td-OTHER; a record-pending call
# naming td-T must retire nothing.
def run_cmd_case():
    state_fd, state_path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(state_fd, "w") as f:
        json.dump({"workers": dict(REG_BEFORE), "notes": []}, f)
    rel_dir = tempfile.mkdtemp()
    with open(os.path.join(rel_dir, "pending.json"), "w") as f:
        json.dump({"pending": [{"game": "tokyo", "task": "td-OTHER",
                                "pr": 1105, "merged_sha": "abc",
                                "merged_at": MERGED_AT, "summary": "x"}]}, f)
    old = (watch.STATE_PATH, watch.RELEASES_DIR, watch._gh)
    watch.STATE_PATH, watch.RELEASES_DIR = state_path, rel_dir
    watch._gh = lambda _p: {"merged_at": MERGED_AT}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            watch.cmd_record_pending(["tokyo", "td-T", "1105", "abc1234", "s"])
        with open(state_path) as f:
            return json.load(f), buf.getvalue()
    finally:
        watch.STATE_PATH, watch.RELEASES_DIR, watch._gh = old
        os.unlink(state_path)
        os.unlink(os.path.join(rel_dir, "pending.json"))
        os.rmdir(rel_dir)


state, out = run_cmd_case()
check("H: ledger task mismatch on dedupe retires nothing",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out
      and "PENDING-DEDUPED" in out)

if failures:
    print("FAILED cases:", ", ".join(failures))
    sys.exit(1)
print("ALL PASS")
