#!/usr/bin/env python3
"""Regression tests for watch.py's auto-deregistration binding.

History (all 2026-10-26, dot's supervision reviews): v1 retired
whatever registration sat under a task at record-pending time. v2
bound by chronology but failed open on missing evidence. v3 failed
closed on evidence but its identity check (--session) was optional.
v4 required a completed-assignment identity but stamped it from
whatever registration was current at assign time — including a
"repair" that wrote a reported session onto a session-less
registration — and the shipped repo copy silently lost a helper
function, so the committed tree failed its own tests.

v5: the identity is the LAUNCH-TIME registration itself. assign-pr
records an assignment only when the current registration IS the
completing worker (session present and matching the completion
report, dispatched_at present), and stamps the game's repo as the
assignment scope. Retirement requires the assignment's session and
NONEMPTY dispatched_at snapshot to match the registration exactly,
plus the repo scope, plus the v3 evidence sanity checks.

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
TOKYO_REPO = "doublehidenblade/tokyo-drift-3d"

failures = []


def check(name, ok):
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        failures.append(name)


def asg(session="sess-1", snap=BEFORE, repo=TOKYO_REPO):
    return {"td-T:1105": {"session": session, "repo": repo,
                          "game": "tokyo",
                          "recorded_at": "2026-10-25T21:00:00+00:00",
                          "reg_dispatched_at": snap}}


def reg(session="sess-1", dispatched=BEFORE):
    return {"kind": "subagent", "session": session,
            "dispatched_at": dispatched}


class Sandbox:
    """Sandboxed watch.py state + pending ledger + stubbed _gh."""

    def __init__(self, workers, assignments=None, ledger=None,
                 gh_result=None, gh_raises=False):
        fd, self.state_path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump({"workers": workers,
                       "assignments": assignments or {}, "notes": []}, f)
        self.rel_dir = tempfile.mkdtemp()
        with open(os.path.join(self.rel_dir, "pending.json"), "w") as f:
            json.dump({"pending": ledger or []}, f)
        self._old = (watch.STATE_PATH, watch.RELEASES_DIR, watch._gh)
        watch.STATE_PATH, watch.RELEASES_DIR = self.state_path, self.rel_dir

        def fake_gh(_path):
            if gh_raises:
                raise RuntimeError("api down")
            return gh_result if gh_result is not None else {"merged_at": MERGED_AT}

        watch._gh = fake_gh

    def call(self, fn, args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            fn(args)
        return buf.getvalue()

    def state(self):
        with open(self.state_path) as f:
            return json.load(f)

    def set_workers(self, workers):
        s = self.state()
        s["workers"] = workers
        with open(self.state_path, "w") as f:
            json.dump(s, f)

    def close(self):
        watch.STATE_PATH, watch.RELEASES_DIR, watch._gh = self._old
        os.unlink(self.state_path)
        os.unlink(os.path.join(self.rel_dir, "pending.json"))
        os.rmdir(self.rel_dir)


def run_case(workers, assignments=None, gh_result=None, gh_raises=False,
             game="tokyo", expect_session=None):
    sb = Sandbox(workers, assignments, gh_result=gh_result,
                 gh_raises=gh_raises)
    try:
        out = sb.call(
            lambda a: watch._auto_deregister("td-T", 1105, game,
                                             expect_session), None)
        return sb.state(), out
    finally:
        sb.close()


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

# K3 — assignment with an empty session identity is unbound: survives.
state, out = run_case({"td-T": reg(None, BEFORE2)},
                      assignments=asg(session=None, snap=BEFORE))
check("K3: empty-session assignment keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# K4 — assignment whose repo scope is a different game: survives even
# when called for its own game, and (S4 below) vice versa.
state, out = run_case({"td-T": reg()},
                      assignments=asg(repo="doublehidenblade/neon-drift"))
check("K4: cross-repo assignment keeps registration",
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

# F — assignment with an empty dispatch snapshot is unbound: survives.
state, out = run_case({"td-T": reg()}, assignments=asg(snap=None))
check("F: empty assignment snapshot keeps registration",
      "td-T" in state["workers"] and "DEREGISTER-SKIP td-T" in out)

# G — unknown game cannot resolve a repo: survives.
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
sb = Sandbox({"td-T": reg()}, asg(),
             ledger=[{"game": "tokyo", "task": "td-OTHER", "pr": 1105,
                      "merged_sha": "abc", "merged_at": MERGED_AT,
                      "summary": "x"}])
try:
    out = sb.call(watch.cmd_record_pending,
                  ["tokyo", "td-T", "1105", "abc1234", "s"])
    st = sb.state()
    check("H: ledger task mismatch on dedupe retires nothing",
          "td-T" in st["workers"] and "DEREGISTER-SKIP td-T" in out
          and "PENDING-DEDUPED" in out)
finally:
    sb.close()

# N — v5: assign-pr must NOT repair an unbound registration. A
# session-less registration cannot be bound by a completion report.
sb = Sandbox({"td-T": reg(None, BEFORE)})
try:
    out = sb.call(watch.cmd_assign_pr, ["td-T", "sess-9", "1105", "tokyo"])
    st = sb.state()
    check("N: assign-pr refuses a session-less registration",
          st["assignments"] == {} and st["workers"]["td-T"]["session"] is None
          and "ASSIGN-SKIP td-T" in out)
finally:
    sb.close()

# N2 — assign-pr refuses to overwrite a conflicting assignment.
sb = Sandbox({"td-T": reg("sess-2", BEFORE)}, asg())
try:
    out = sb.call(watch.cmd_assign_pr, ["td-T", "sess-2", "1105", "tokyo"])
    st = sb.state()
    check("N2: assign-pr refuses a conflicting session",
          st["assignments"]["td-T:1105"]["session"] == "sess-1"
          and "ASSIGN-CONFLICT" in out)
finally:
    sb.close()

# N3 — assign-pr happy path: records session + repo + snapshot.
sb = Sandbox({"td-T": reg()})
try:
    out = sb.call(watch.cmd_assign_pr, ["td-T", "sess-1", "1105", "tokyo"])
    a = sb.state()["assignments"].get("td-T:1105", {})
    check("N3: assign-pr records the bound identity",
          a.get("session") == "sess-1" and a.get("repo") == TOKYO_REPO
          and a.get("reg_dispatched_at") == BEFORE
          and "ASSIGNED td-T" in out)
finally:
    sb.close()

# S1 — full sequence: assign-pr -> record-pending retires the worker.
sb = Sandbox({"td-T": reg()})
try:
    sb.call(watch.cmd_assign_pr, ["td-T", "sess-1", "1105", "tokyo"])
    out = sb.call(watch.cmd_record_pending,
                  ["tokyo", "td-T", "1105", "abc1234", "done"])
    st = sb.state()
    check("S1: full assign->record sequence retires the worker",
          "td-T" not in st["workers"] and st["assignments"] == {}
          and "DEREGISTERED td-T" in out)
finally:
    sb.close()

# S2 — full sequence with a replacement registered between assign and
# record: the replacement survives.
sb = Sandbox({"td-T": reg()})
try:
    sb.call(watch.cmd_assign_pr, ["td-T", "sess-1", "1105", "tokyo"])
    sb.set_workers({"td-T": reg("sess-2", BEFORE2)})
    out = sb.call(watch.cmd_record_pending,
                  ["tokyo", "td-T", "1105", "abc1234", "done"])
    st = sb.state()
    check("S2: replacement between assign and record survives",
          "td-T" in st["workers"] and "DEREGISTER-SKIP td-T" in out)
finally:
    sb.close()

# S3 — registration without dispatched_at: assign-pr refuses, and the
# subsequent record-pending retires nothing.
sb = Sandbox({"td-T": {"kind": "subagent", "session": "sess-1"}})
try:
    out1 = sb.call(watch.cmd_assign_pr, ["td-T", "sess-1", "1105", "tokyo"])
    out2 = sb.call(watch.cmd_record_pending,
                   ["tokyo", "td-T", "1105", "abc1234", "done"])
    st = sb.state()
    check("S3: missing snapshot blocks the whole sequence",
          "ASSIGN-SKIP td-T" in out1 and "td-T" in st["workers"]
          and "DEREGISTER-SKIP td-T" in out2)
finally:
    sb.close()

# S4 — cross-repo: assignment bound to tokyo; a record-pending under a
# different game must not retire the registration.
sb = Sandbox({"td-T": reg()})
try:
    sb.call(watch.cmd_assign_pr, ["td-T", "sess-1", "1105", "tokyo"])
    out = sb.call(watch.cmd_record_pending,
                  ["neon", "td-T", "1105", "abc1234", "done"])
    st = sb.state()
    check("S4: cross-repo record-pending keeps registration",
          "td-T" in st["workers"] and "DEREGISTER-SKIP td-T" in out)
finally:
    sb.close()

if failures:
    print("FAILED cases:", ", ".join(failures))
    sys.exit(1)
print("ALL PASS")
