#!/usr/bin/env python3
"""Unit tests for watch.py cmd_liveness ownership-safety rules (td-310/td-311).

History (td-310): cmd_liveness's Signal C (cloud-session classification)
only runs when a registration carries a session id. For a session-less
registration (session=None, e.g. registered with '-'), fresh_observation
stayed True, so two consecutive cycles with no heartbeat file and no
fresh GitHub evidence advanced quiet_cycles QUIET(1) -> DEAD: the
registration was deleted and a replacement dispatch-subagent was queued
in pending_actions.json — with no ended-session receipt of any kind.
Absence of evidence was treated as a fresh observation of death, but for
a session-less registration the checker has NO channel that could observe
the session ending. Reproduced by td-218 (2026-11-15: registered
session=null, quiet_cycles=1; the next sync proclaimed it DEAD and queued
a replacement nobody authorized).

Fix td-310 (cmd_liveness only; _worker_evidence is td-308, untouched):
1. Session-less + no life signs is NOT a fresh observation: STALE with a
   reason naming the missing ended-session receipt, counter frozen,
   registration kept, no replacement queued. Alive paths (fresh
   heartbeat / fresh GitHub evidence) and the terminal-status DROPPED
   path are unchanged.
2. DEAD replacement queueing respects the dispatch denylist (built the
   same way _dispatch_rows builds it: state dispatch_denylist,
   list-or-dict, plus the td-054 default). A denylisted worker whose
   death WAS observed through a session channel is still proclaimed
   DEAD, noted, and dropped — only the replacement is not queued.

Residual (td-311, Dot's FLEET-019 review): the td-310 fix left the
session-backed path unsafe. Signal C treated only a fresh WORKING
classification as alive and only marked the observation not-fresh when
the classification was stale/missing — so a FRESH STALLED or UNKNOWN
classification left fresh_observation=True, quiet_cycles incremented,
and after 2 cycles the worker was proclaimed DEAD, dropped, and a
replacement queued. A fresh STALLED/UNKNOWN is not an ended-session
receipt. The old test (b) in this file expected that unsafe transition.

Fix td-311 (cmd_liveness only): a fresh classification advances the
quiet counter toward DEAD only when it is itself a positive
ended-session receipt — a fresh DEAD classification. A fresh STALLED,
UNKNOWN, or any other non-terminal classification is NOT a fresh
observation of death: STALE with a reason naming the missing
ended-session receipt, counter frozen, registration kept, no
replacement queued. Test (b) now expects the safe behaviour; tests
(b2)/(b4) add the UNKNOWN and other-non-terminal regressions, and
test (b3) is the positive control: a fresh DEAD classification still
goes QUIET(1) -> DEAD with a replacement queued. The denylist tests
(e)/(e2)/(e3) now reach DEAD through the DEAD-classification receipt,
so the denylist behaviour itself is unchanged.

Run: python3 test_liveness_caller.py  (exit 0 = all pass)
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from datetime import timedelta
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _load_watch_unwrapped():
    """Load watch.py's real cmd_liveness for testing.

    On game-dev-central main, watch.py's import-time tail replaces the
    globals cmd_liveness (and the other ALIASES | RETIRED commands) with
    coordinator_cli retired-route stubs — the CLI route is retired, but
    the cmd_liveness function itself is the code under test here (it is
    the operational function in the local runtime copy). Loading a
    private copy of the module with an empty coordinator_cli stub keeps
    the real function reachable without touching sys.modules['watch']
    or the real coordinator_cli for any other test module.
    """
    stub = types.ModuleType("coordinator_cli")
    stub.ALIASES = set()
    stub.RETIRED = set()
    stub.EVIDENCE_COMMANDS = {}
    stub.run = lambda *a, **k: 2
    stub.run_evidence = lambda *a, **k: 2
    saved = sys.modules.get("coordinator_cli")
    sys.modules["coordinator_cli"] = stub
    try:
        spec = importlib.util.spec_from_file_location(
            "watch_td311_liveness",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "watch.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        if saved is not None:
            sys.modules["coordinator_cli"] = saved
        else:
            sys.modules.pop("coordinator_cli", None)


watch = _load_watch_unwrapped()

REPO = "tokyo-drift-3d"


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def worker(task, session=None, quiet=0, dispatched_days_ago=2):
    return {
        "kind": "subagent",
        "session": session,
        "repo": REPO,
        "task_file": f"godot/docs/tasks/{task}.md",
        "dispatched_at": iso(watch.now() - timedelta(days=dispatched_days_ago)),
        "quiet_cycles": quiet,
        "last_verdict": "registered",
    }


class LivenessHarness(unittest.TestCase):
    """cmd_liveness against a fully sandboxed state / ledger / heartbeat dir.

    load_state/save_state run for real against a temp STATE_PATH;
    STATE_DIR (pending_actions.json), the heartbeat dir, the GitHub
    evidence call, the task-status call, and the replacement-brief
    builder are all sandboxed or mocked — nothing touches live state.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="td310-liveness-")
        self.hb_dir = os.path.join(self.tmp, "worker-heartbeats")
        os.makedirs(self.hb_dir)
        self.state_path = os.path.join(self.tmp, "state.json")
        self.pa_path = os.path.join(self.tmp, "pending_actions.json")
        self.evidence_result = (False, ["no fresh evidence"], [])
        self.task_status = None
        self.state = {"workers": {}, "sessions": {}, "notes": []}
        self._write_state()
        self._write_pa({"actions": [], "notes": []})
        self._patches = [
            mock.patch.object(watch, "STATE_PATH", self.state_path),
            mock.patch.object(watch, "STATE_DIR", self.tmp),
            mock.patch.object(watch, "LIVENESS_HEARTBEAT_DIR", self.hb_dir),
            mock.patch.object(watch, "_task_status_on_main",
                              side_effect=lambda repo, tf: self.task_status),
            mock.patch.object(watch, "_worker_evidence",
                              side_effect=lambda *a: self.evidence_result),
            mock.patch.object(watch, "_build_replacement_brief",
                              side_effect=lambda task, tf, salvage:
                              (os.path.join(self.tmp, f"{task}-brief.md"),
                               f"brief for {task}")),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()

    # -- sandbox helpers ----------------------------------------------------
    def _write_state(self):
        with open(self.state_path, "w") as f:
            json.dump(self.state, f)

    def _write_pa(self, pa):
        with open(self.pa_path, "w") as f:
            json.dump(pa, f)

    def read_state(self):
        with open(self.state_path) as f:
            return json.load(f)

    def read_pa(self):
        with open(self.pa_path) as f:
            return json.load(f)

    def set_workers(self, workers, sessions=None, denylist=None):
        self.state = {"workers": workers, "sessions": sessions or {},
                      "notes": []}
        if denylist is not None:
            self.state["dispatch_denylist"] = denylist
        self._write_state()

    def fresh_classification(self, session, classification):
        return {session: {
            "last_classification": classification,
            "last_classification_ts": iso(watch.now()),
        }}

    def run_liveness(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            watch.cmd_liveness()
        return buf.getvalue()

    # -- (a) td-218 reproduction ---------------------------------------------
    def test_a_sessionless_no_life_signs_stale_twice_never_dead(self):
        # td-218 snapshot: session=null, quiet_cycles=1, dispatched long ago.
        self.set_workers({"td-218": worker("td-218", session=None, quiet=1)})
        for _ in range(2):
            out = self.run_liveness()
            self.assertTrue(out.startswith("STALE td-218"), out)
            self.assertIn("session-less registration", out)
            self.assertIn("no ended-session receipt", out)
            st = self.read_state()
            self.assertIn("td-218", st["workers"],
                          "session-less registration must NOT be dropped")
            self.assertEqual(st["workers"]["td-218"]["quiet_cycles"], 1,
                             "quiet_cycles must never advance on STALE")
            self.assertEqual(st["workers"]["td-218"]["last_verdict"], "stale")
            self.assertEqual(self.read_pa()["actions"], [],
                             "no replacement may be queued for a STALE worker")

    # -- (b) fresh STALLED is NOT an ended-session receipt (td-311) -----------
    def test_b_session_backed_fresh_stalled_stale_never_dead(self):
        # td-311 / Dot's FLEET-019 criterion: a session-backed registration
        # with a FRESH STALLED classification and no ended-session receipt
        # must NOT go QUIET -> DEAD. (The td-310 version of this test
        # expected exactly that unsafe transition; it is flipped here.)
        # STALLED is not a receipt: the counter stays frozen, the
        # registration is kept, and nothing is queued — across repeated
        # cycles, starting from quiet_cycles=1, the point where one more
        # quiet cycle under the old code proclaimed DEAD immediately.
        task = "td-900"
        self.set_workers(
            {task: worker(task, session="sess-b", quiet=1)},
            sessions=self.fresh_classification("sess-b", "STALLED"))
        for _ in range(3):
            out = self.run_liveness()
            self.assertTrue(out.startswith(f"STALE {task}"), out)
            self.assertIn("fresh STALLED classification", out)
            self.assertIn("no ended-session receipt", out)
            st = self.read_state()
            self.assertIn(task, st["workers"],
                          "fresh-STALLED registration must NOT be dropped")
            self.assertEqual(st["workers"][task]["quiet_cycles"], 1,
                             "quiet_cycles must never advance without a receipt")
            self.assertEqual(st["workers"][task]["last_verdict"], "stale")
            self.assertEqual(self.read_pa()["actions"], [],
                             "no replacement may be queued for a STALE worker")

    # -- (b2) fresh UNKNOWN is NOT an ended-session receipt (td-311) ----------
    def test_b2_session_backed_fresh_unknown_stale_never_dead(self):
        # UNKNOWN means the classifier could not determine the session
        # state — it is not a receipt that the session ended. Same safe
        # behaviour as STALLED, across repeated cycles.
        task = "td-906"
        self.set_workers(
            {task: worker(task, session="sess-u", quiet=1)},
            sessions=self.fresh_classification("sess-u", "UNKNOWN"))
        for _ in range(3):
            out = self.run_liveness()
            self.assertTrue(out.startswith(f"STALE {task}"), out)
            self.assertIn("fresh UNKNOWN classification", out)
            self.assertIn("no ended-session receipt", out)
            st = self.read_state()
            self.assertIn(task, st["workers"],
                          "fresh-UNKNOWN registration must NOT be dropped")
            self.assertEqual(st["workers"][task]["quiet_cycles"], 1)
            self.assertEqual(st["workers"][task]["last_verdict"], "stale")
            self.assertEqual(self.read_pa()["actions"], [])

    # -- (b3) fresh DEAD classification IS the receipt: DEAD path preserved ---
    def test_b3_session_backed_fresh_dead_quiet_then_dead_queued(self):
        # Positive control: a fresh DEAD classification itself reports the
        # session ended, so it IS a positive ended-session receipt — the
        # existing QUIET(1) -> DEAD + replacement-queued behaviour is
        # preserved for exactly this case.
        task = "td-907"
        self.set_workers(
            {task: worker(task, session="sess-d")},
            sessions=self.fresh_classification("sess-d", "DEAD"))
        out1 = self.run_liveness()
        self.assertTrue(out1.startswith(f"QUIET(1) {task}"), out1)
        self.assertIn("ended-session receipt", out1)
        out2 = self.run_liveness()
        self.assertTrue(out2.startswith(f"DEAD {task}"), out2)
        self.assertIn("replacement queued", out2)
        st = self.read_state()
        self.assertNotIn(task, st["workers"])
        self.assertTrue(any("proclaimed DEAD" in n for n in st["notes"]))
        actions = self.read_pa()["actions"]
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["type"], "dispatch-subagent")
        self.assertEqual(actions[0]["task"], task)

    # -- (b4) other fresh non-terminal classifications: also not receipts -----
    def test_b4_other_fresh_nonterminal_classifications_stale(self):
        # FINISHED / OUT_OF_TOKENS / LOGIN_BLOCKED have their own flows
        # (SHIP / FAILOVER / REPORT_LOGIN in decide_action); none of them
        # is a liveness ended-session receipt, so liveness must not
        # proclaim DEAD, drop, or queue a replacement for any of them.
        for i, cls in enumerate(("FINISHED", "OUT_OF_TOKENS", "LOGIN_BLOCKED")):
            with self.subTest(classification=cls):
                task = f"td-91{i}"
                session = f"sess-{cls.lower()}"
                self.set_workers(
                    {task: worker(task, session=session, quiet=1)},
                    sessions=self.fresh_classification(session, cls))
                self._write_pa({"actions": [], "notes": []})
                for _ in range(2):
                    out = self.run_liveness()
                    self.assertTrue(out.startswith(f"STALE {task}"), out)
                    self.assertIn("no ended-session receipt", out)
                    st = self.read_state()
                    self.assertIn(task, st["workers"])
                    self.assertEqual(st["workers"][task]["quiet_cycles"], 1)
                    self.assertEqual(self.read_pa()["actions"], [])

    # -- (c) session-less + fresh heartbeat -> ALIVE ---------------------------
    def test_c_sessionless_fresh_heartbeat_alive_counter_reset(self):
        task = "td-902"
        self.set_workers({task: worker(task, session=None, quiet=1)})
        with open(os.path.join(self.hb_dir, f"{task}.json"), "w") as f:
            json.dump({"ts": iso(watch.now()), "current_step": "working"}, f)
        out = self.run_liveness()
        self.assertTrue(out.startswith(f"ALIVE {task}"), out)
        st = self.read_state()
        self.assertEqual(st["workers"][task]["quiet_cycles"], 0)
        self.assertEqual(st["workers"][task]["last_verdict"], "alive")

    # -- (d) session-less + fresh GitHub evidence -> ALIVE ---------------------
    def test_d_sessionless_fresh_github_evidence_alive(self):
        task = "td-903"
        self.set_workers({task: worker(task, session=None, quiet=1)})
        self.evidence_result = (True, [f"branch worker/{task}-fix 1 ahead"], [])
        out = self.run_liveness()
        self.assertTrue(out.startswith(f"ALIVE {task}"), out)
        st = self.read_state()
        self.assertIn(task, st["workers"])
        self.assertEqual(st["workers"][task]["quiet_cycles"], 0)

    # -- (e) denylisted session-backed DEAD: dropped, NO replacement -----------
    def test_e_denylisted_dead_recorded_dropped_no_replacement(self):
        # td-311: DEAD is reached through the fresh DEAD classification —
        # the positive ended-session receipt. The denylist behaviour
        # itself (DEAD recorded and dropped, replacement NOT queued) is
        # the td-310 behaviour, unchanged.
        task = "td-901"
        self.set_workers(
            {task: worker(task, session="sess-e", quiet=1)},
            sessions=self.fresh_classification("sess-e", "DEAD"),
            denylist={task: "gated: test denylist entry"})
        out = self.run_liveness()
        self.assertTrue(out.startswith(f"DEAD {task}"), out)
        self.assertIn("NOT queued", out)
        self.assertIn("dispatch denylist", out)
        st = self.read_state()
        self.assertNotIn(task, st["workers"],
                         "an observed death still drops the registry entry")
        self.assertTrue(any("proclaimed DEAD" in n and "NOT queued" in n
                            for n in st["notes"]), st["notes"])
        self.assertEqual(self.read_pa()["actions"], [],
                         "denylisted task must NOT get a replacement queued")

    def test_e2_td054_default_denylist_no_replacement(self):
        # The td-054 default applies even with no state denylist entry,
        # exactly as _dispatch_rows applies it.
        task = "td-054"
        self.set_workers(
            {task: worker(task, session="sess-054", quiet=1)},
            sessions=self.fresh_classification("sess-054", "DEAD"))
        out = self.run_liveness()
        self.assertTrue(out.startswith(f"DEAD {task}"), out)
        self.assertIn("NOT queued", out)
        self.assertEqual(self.read_pa()["actions"], [])

    def test_e3_list_form_denylist_no_replacement(self):
        task = "td-904"
        self.set_workers(
            {task: worker(task, session="sess-l", quiet=1)},
            sessions=self.fresh_classification("sess-l", "DEAD"),
            denylist=[task])
        out = self.run_liveness()
        self.assertTrue(out.startswith(f"DEAD {task}"), out)
        self.assertIn("NOT queued", out)
        self.assertEqual(self.read_pa()["actions"], [])

    # -- terminal-status DROPPED path unchanged for session-less workers -------
    def test_f_sessionless_terminal_status_dropped(self):
        task = "td-905"
        self.set_workers({task: worker(task, session=None, quiet=1)})
        self.task_status = "done"
        out = self.run_liveness()
        self.assertTrue(out.startswith(f"DROPPED {task}"), out)
        self.assertNotIn(task, self.read_state()["workers"])
        self.assertEqual(self.read_pa()["actions"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
