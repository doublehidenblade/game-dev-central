#!/usr/bin/env python3
"""Regression tests for watch.py's auto-deregistration binding.

History (all 2026-10-26, dot's supervision reviews): v1 retired
whatever registration sat under a task at record-pending time. v2
bound by chronology (dispatched_at < merged_at) but failed open on
missing evidence. v3 failed closed on evidence and verified the
ledger task, but its identity check (--session) was optional, so the
default path still deleted on chronology alone — including a
replacement worker dispatched before the old PR merged. v4 is
identity-first: retirement requires a completed-assignment identity
(assign-pr, recorded from the worker's own completion report) that
matches the registration's session AND the dispatched_at snapshot
taken when the assignment was recorded; the assignment is consumed
on use. The v3 evidence checks remain as sanity, all fail-closed.

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
BEFORE2 = "2026-10-24T09:30:00+00:00"  # also before, different instance
AFTER = "2026-10-26T00:19:16+00:00"  # dispatched after the merge

failures = []


def check(name, ok):
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        failures.append(name)


def asg(session="sess-1", snap=BEFORE):
    return {"td-T:1105": {"session": session,
                          "recorded_at": "2026-10-25T21:00:00+00:00",
                          "reg_dispatched_at": snap,
                          "reg_session": session}}


def reg(session="sess-1", dispatched=BEFORE):
    return {"kind": "subagent", "session": session,
            "dispatched_at": dispatched}


def run_case(workers, assignments=None, gh_result=None, gh_raises=False,
             game="tokyo", expect_session=None):
    """Run _auto_deregister against a sandboxed state file and a stubbed
    _gh. Returns (state_after, stdout_text)."""
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump({"workers": workers, "assignments": assignments or {},
                   "notes": []}, f)
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


# A — the normal lifecycle, identity recorded: the completing worker's
# registration is retired and the assignment is consumed.
state, out = run_case({"td-T": reg()}, assignments=asg())
check("A: assigned worker retired, assignment consumed",
      "td-T" not in state["workers"] and "td-T:1105" not in state["assignments"]
      and "DEREGISTERED td-T" in out)

# B — re-registered after the old PR merged (v1/v2 regression): survives.
state, out = run_case({"td-T": reg("sess-2", AFTER)}, assignments=asg())
check("B: re-registered worker survives replay",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# K — dot's v4 case: a replacement dispatched BEFORE the old PR merged.
# Chronology alone would retire it; identity must not.
state, out = run_case({"td-T": reg("sess-2", BEFORE2)}, assignments=asg())
check("K: pre-merge replacement survives on identity",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# K2 — no assignment on record at all: absent identity skips, even with
# perfect chronology and a matching session name.
state, out = run_case({"td-T": reg()}, assignments=None)
check("K2: absent assignment identity keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# K3 — session-less replacement registration: the dispatched_at snapshot
# from assignment time distinguishes the instance.
state, out = run_case({"td-T": reg(None, BEFORE2)},
                      assignments=asg(session=None, snap=BEFORE))
check("K3: snapshot mismatch keeps session-less replacement",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# C — no registration under the task: silent no-op, no crash.
state, out = run_case({}, assignments=asg())
check("C: unregistered task is a no-op",
      state["workers"] == {} and "DEREGISTER" not in out)

# D — the PR lookup fails: keep the registration, report the skip.
state, out = run_case({"td-T": reg()}, assignments=asg(), gh_raises=True)
check("D: API failure keeps registration, prints skip",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# E — null merged_at is missing evidence, not permission: survives.
state, out = run_case({"td-T": reg()}, assignments=asg(),
                      gh_result={"merged_at": None})
check("E: null merged_at keeps registration (fail closed)",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# F — registration with no parseable dispatched_at: survives.
state, out = run_case({"td-T": {"kind": "subagent", "session": "sess-1"}},
                      assignments=asg(snap=None))
check("F: missing dispatched_at keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# G — unknown game cannot resolve a repo to verify the merge: survives.
state, out = run_case({"td-T": reg()}, assignments=asg(), game="atlantis")
check("G: unknown game keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# I — caller-supplied --session disagrees with the assignment: survives.
state, out = run_case({"td-T": reg()}, assignments=asg(),
                      expect_session="sess-OTHER")
check("I: caller session mismatch keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# J — caller-supplied --session matches the assignment: retires.
state, out = run_case({"td-T": reg()}, assignments=asg(),
                      expect_session="sess-1")
check("J: caller session match retires registration",
      "td-T" not in state["workers"] and "DEREGISTERED td-T" in out)


# H — dedupe must verify the ledger task, never trust the caller's.
# The ledger records PR #1105 under td-OTHER; a record-pending call
# naming td-T must retire nothing.
def run_cmd_case(fn, args, workers, assignments, ledger_entries):
    state_fd, state_path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(state_fd, "w") as f:
        json.dump({"workers": workers, "assignments": assignments,
                   "notes": []}, f)
    rel_dir = tempfile.mkdtemp()
    with open(os.path.join(rel_dir, "pending.json"), "w") as f:
        json.dump({"pending": ledger_entries}, f)
    old = (watch.STATE_PATH, watch.RELEASES_DIR, watch._gh)
    watch.STATE_PATH, watch.RELEASES_DIR = state_path, rel_dir
    watch._gh = lambda _p: {"merged_at": MERGED_AT}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            fn(args)
        with open(state_path) as f:
            return json.load(f), buf.getvalue()
    finally:
        watch.STATE_PATH, watch.RELEASES_DIR, watch._gh = old
        os.unlink(state_path)
        os.unlink(os.path.join(rel_dir, "pending.json"))
        os.rmdir(rel_dir)


state, out = run_cmd_case(
    watch.cmd_record_pending, ["tokyo", "td-T", "1105", "abc1234", "s"],
    {"td-T": reg()}, asg(),
    [{"game": "tokyo", "task": "td-OTHER", "pr": 1105,
      "merged_sha": "abc", "merged_at": MERGED_AT, "summary": "x"}])
check("H: ledger task mismatch on dedupe retires nothing",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out
      and "PENDING-DEDUPED" in out)

# N — assign-pr: records the identity, repairs a session-less
# registration from the completion report, and refuses conflicts.
state, out = run_cmd_case(
    watch.cmd_assign_pr, ["td-T", "sess-9", "1105"],
    {"td-T": reg(None, BEFORE)}, {},
    [])
check("N: assign-pr records identity and repairs session",
      state["assignments"].get("td-T:1105", {}).get("session") == "sess-9"
      and state["workers"]["td-T"]["session"] == "sess-9"
      and "ASSIGNED td-T" in out)

state, out = run_cmd_case(
    watch.cmd_assign_pr, ["td-T", "sess-2", "1105"],
    {"td-T": reg()}, asg(), [])
check("N2: assign-pr refuses a conflicting session",
      state["assignments"]["td-T:1105"]["session"] == "sess-1"
      and "ASSIGN-CONFLICT" in out)

if failures:
    print("FAILED cases:", ", ".join(failures))
    sys.exit(1)
print("ALL PASS")
