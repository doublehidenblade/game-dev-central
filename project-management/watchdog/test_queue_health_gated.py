#!/usr/bin/env python3
"""Unit tests for watch.py Craig-gated dispatch classification (td-313).

Defect: `_dispatch_rows` classified a board row solely by ownership and
the dispatch denylist. The Craig-gated story-layer spec row td-285
(status: "open — spec/design only; no implementation until Craig
approves the gig-city world bible", owner unassigned) therefore came
out "unowned", `queue-health` counted it as the sole dispatchable
candidate (QUEUE-HEALTH OK workers=0 candidates=1 vision_remaining=9),
and QUEUE-EMPTY-VISION-DUE never fired — the never-idle vision
breakdown never ran while vision work remained. The same gate existed
on the vision side: story-layer is the only not_started checklist
item and its notes say GATED / BLOCKED-ON-CRAIG, so a DUE line naming
the first not_started item would have named the gated item itself.

Fix (td-313, _dispatch_rows + cmd_queue_health only):
1. A board row whose status text carries a Craig gate or a spec-only
   marker is classified "SKIP <gated reason>", never "unowned" — a
   general status-text rule (Craig gate phrases / spec-only phrases),
   not a td-285 special case.
2. The queue-health DUE selection skips gated vision items the same
   way: it names the first not_started UNGATED item, else the first
   ungated remaining item, and never a gated item.

td-315 extension (same file): the td-313 DUE fallback reconciled the
selected vision item only against the Craig gate. Two gaps remained:
1. Selected-item ownership was not reconciled: police-wanted's
   follow-up rows td-220/221/222 are open, owned, and carry 'no new
   worker; coordination queue' restrictions, yet DUE printed
   unqualified — a consumer reading it as a fresh-breakdown trigger
   would dispatch duplicate police work against those owners. The
   fallback now annotates DUE as already-owned / review-only when the
   selected item's follow-up rows already cover it (DUE itself is
   preserved as a review signal, never suppressed).
2. A plain 'STOP: do not dispatch' marker in a board row's status was
   recognized nowhere: a STOP-marked unowned row still read 'unowned'.
   _dispatch_rows now SKIPs STOP-marked rows (general word-token text
   rule, like the Craig-gate rule).

Run: python3 test_queue_health_gated.py  (exit 0 = all pass)
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _load_watch_unwrapped():
    """Load watch.py's real _dispatch_rows / cmd_queue_health.

    Same pattern as test_liveness_caller.py: on game-dev-central main,
    watch.py's import-time tail replaces some CLI command globals with
    coordinator_cli retired-route stubs. _dispatch_rows and
    cmd_queue_health are not themselves retired routes, but loading
    with an empty coordinator_cli stub keeps every function reachable
    exactly as written, without touching the real coordinator_cli.
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
            "watch_td313_queue_health",
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

TD285_STATUS = ("open — spec/design only; no implementation until Craig "
                "approves the gig-city world bible")


def board_text(rows):
    """rows: [(task, status, owner)] -> board markdown _parse_board_rows reads."""
    lines = ["| Task | Defect | Status | Owner | PR | Updated |",
             "|---|---|---|---|---|---|"]
    for task, status, owner in rows:
        lines.append(f"| {task} | defect for {task} | {status} | {owner} | — | 2026-11-16 |")
    return "\n".join(lines) + "\n"


def classify(rows, state=None, pa=None):
    parsed = watch._parse_board_rows(board_text(rows))
    return watch._dispatch_rows(parsed, state or {"workers": {}, "sessions": {}},
                                pa if pa is not None else {"actions": [], "notes": []})


def marks_by_task(classified):
    return {task: mark for task, _prefix, mark, _status in classified}


class GatedBoardRowTests(unittest.TestCase):
    def test_a_td285_gated_row_is_skip_not_unowned(self):
        out = classify([("td-285", TD285_STATUS, "unassigned")])
        self.assertEqual(len(out), 1)
        task, prefix, mark, _status = out[0]
        self.assertEqual(task, "td-285")
        self.assertTrue(mark.startswith("SKIP"), mark)
        self.assertIn("gated", mark.lower())
        self.assertIn("craig", mark.lower())
        candidates = sum(1 for *_x, m, _s in
                         [(t, p, mk, s) for t, p, mk, s in out] if m == "unowned")
        self.assertEqual(candidates, 0)

    def test_a_gated_variants_are_skip(self):
        variants = [
            ("td-901", "open — gated on Craig: do not dispatch", "unassigned"),
            ("td-902", "open — BLOCKED-ON-CRAIG; awaiting his approval", "unassigned"),
            ("td-903", "open — spec only; no implementation until Craig approves it", "unassigned"),
            ("td-904", "open — spec/design only", "unassigned"),
        ]
        marks = marks_by_task(classify(variants))
        for task, _status, _owner in variants:
            self.assertTrue(marks[task].startswith("SKIP"), (task, marks[task]))

    def test_b_genuinely_unowned_ungated_row_still_candidate(self):
        out = classify([("td-910", "open — ready to implement", "unassigned")])
        self.assertEqual(out[0][2], "unowned")

    def test_b_craig_mention_without_gate_is_not_gated(self):
        # A plain Craig mention (a verdict note, a direct order) is not a
        # gate: only gate phrasing / spec-only markers may SKIP a row.
        out = classify([("td-911", "open — filed under Craig's direct order; ready", "unassigned")])
        self.assertEqual(out[0][2], "unowned")

    def test_no_other_classification_changes(self):
        rows = [
            ("td-054", "open — two-renderer acceptance", "unassigned"),
            ("td-912", "open — ready", "Muse worker"),
            ("td-913", "in_progress — working", "unassigned"),
        ]
        # td-913 is unowned-but-in_progress with a tracked worker below.
        state = {"workers": {"td-913": {}}, "sessions": {}}
        marks = marks_by_task(classify(rows, state=state))
        self.assertTrue(marks["td-054"].startswith("SKIP"), marks["td-054"])
        self.assertIn("no-redispatch", marks["td-054"])
        self.assertTrue(marks["td-912"].startswith("owned("), marks["td-912"])
        self.assertTrue(marks["td-913"].startswith("owned("), marks["td-913"])


STORY_LAYER = {
    "id": "story-layer",
    "name": "Story layer: scripted missions layered on generic gigs",
    "status": "not_started",
    "notes": ("GATED: no implementation until he approves it. "
              "BLOCKED-ON-CRAIG 2026-10-26: breakdown filed as spec-only "
              "task td-285; no implementation (and no dispatch) until "
              "Craig approves the world bible."),
}
UNGATED_NOT_STARTED = {
    "id": "ungated-feature",
    "name": "Ungated feature",
    "status": "not_started",
    "notes": "Ready to break down.",
}
UNGATED_IN_PROGRESS = {
    "id": "police-wanted",
    "name": "Police and wanted system",
    "status": "in_progress",
    "notes": "Core system merged; defect tail still open.",
}
WORLD_INSPECTOR = {
    "id": "world-inspector",
    "name": "World Inspector",
    "status": "in_progress",
    "notes": "Breakdown filed 2026-10-26 under Craig's direct order.",
}


class VisionGateTests(unittest.TestCase):
    def test_vision_item_gated_detection(self):
        self.assertTrue(watch._vision_item_gated(STORY_LAYER))
        self.assertFalse(watch._vision_item_gated(UNGATED_NOT_STARTED))
        self.assertFalse(watch._vision_item_gated(UNGATED_IN_PROGRESS))
        # Craig mention alone (direct order) must not read as a gate.
        self.assertFalse(watch._vision_item_gated(WORLD_INSPECTOR))


class QueueHealthDueTests(unittest.TestCase):
    def run_queue_health(self, board_rows, checklist_items):
        tmp = tempfile.mkdtemp(prefix="td313-qh-")
        state_dir = os.path.join(tmp, "state")
        os.makedirs(state_dir)
        with open(os.path.join(state_dir, "state.json"), "w") as f:
            json.dump({"workers": {}, "sessions": {}}, f)
        with open(os.path.join(state_dir, "pending_actions.json"), "w") as f:
            json.dump({"actions": [], "notes": []}, f)
        board_file = os.path.join(tmp, "board.md")
        with open(board_file, "w") as f:
            f.write(board_text(board_rows))
        checklist = os.path.join(tmp, "vision.json")
        with open(checklist, "w") as f:
            json.dump({"items": checklist_items}, f)
        buf = io.StringIO()
        with redirect_stdout(buf):
            watch.cmd_queue_health(["tokyo-drift-3d", "--state-dir", state_dir,
                                    "--board-file", board_file,
                                    "--checklist", checklist])
        return buf.getvalue().strip()

    def test_c_due_skips_gated_vision_item_names_ungated_not_started(self):
        out = self.run_queue_health(
            [("td-285", TD285_STATUS, "unassigned")],
            [UNGATED_IN_PROGRESS, STORY_LAYER, UNGATED_NOT_STARTED])
        self.assertEqual(
            out, "QUEUE-EMPTY-VISION-DUE ungated-feature :: Ungated feature")

    def test_c_due_fallback_names_ungated_remaining_not_gated(self):
        out = self.run_queue_health(
            [("td-285", TD285_STATUS, "unassigned")],
            [UNGATED_IN_PROGRESS, STORY_LAYER])
        self.assertTrue(out.startswith("QUEUE-EMPTY-VISION-DUE police-wanted"), out)
        self.assertNotIn("story-layer", out)

    def test_gated_board_row_alone_does_not_block_due(self):
        # Before the fix this board (sole row = gated td-285) printed
        # QUEUE-HEALTH OK candidates=1 and DUE never fired.
        out = self.run_queue_health(
            [("td-285", TD285_STATUS, "unassigned")],
            [UNGATED_NOT_STARTED])
        self.assertTrue(out.startswith("QUEUE-EMPTY-VISION-DUE"), out)

    def test_ungated_candidate_still_reports_ok(self):
        out = self.run_queue_health(
            [("td-910", "open — ready to implement", "unassigned")],
            [UNGATED_NOT_STARTED])
        self.assertEqual(
            out, "QUEUE-HEALTH OK workers=0 candidates=1 vision_remaining=1")


class StopMarkerTests(unittest.TestCase):
    def test_d_stop_row_is_skip_never_unowned(self):
        out = classify([("td-920", "open — STOP: do not dispatch; "
                                   "held by the coordinator", "unassigned")])
        self.assertEqual(len(out), 1)
        task, _prefix, mark, _status = out[0]
        self.assertEqual(task, "td-920")
        self.assertTrue(mark.startswith("SKIP"), mark)
        self.assertIn("STOP", mark)
        self.assertNotEqual(mark, "unowned")

    def test_d_stop_variants_skip_and_non_markers_do_not(self):
        variants = [
            ("td-921", "open — stop. Do not dispatch this row.", "unassigned"),
            ("td-922", "open — STOP — no dispatch until the lane reopens", "unassigned"),
            ("td-923", "in_progress — STOP: never dispatch a second worker", "unassigned"),
        ]
        marks = marks_by_task(classify(variants))
        for task, _status, _owner in variants:
            self.assertTrue(marks[task].startswith("SKIP"), (task, marks[task]))
        # 'stop' as a substring or as an ordinary word, with no dispatch
        # prohibition, is NOT a STOP marker.
        negatives = [
            ("td-924", "open — bus stop signage is missing; ready", "unassigned"),
            ("td-925", "open — unstoppable regression in the stopgap build; ready", "unassigned"),
            ("td-926", "open — do not dispatch yet; awaiting art", "unassigned"),
        ]
        marks = marks_by_task(classify(negatives))
        for task, _status, _owner in negatives:
            self.assertEqual(marks[task], "unowned", (task, marks[task]))


POLICE_WANTED = {
    "id": "police-wanted",
    "name": "Police and wanted system: crimes raise the wanted level, "
            "cops pursue and arrest",
    "status": "in_progress",
    "task": "td-195",
    "notes": "Core system merged; defect tail still open (cop collision "
             "td-195, cop spawn placement td-274, wanted HUD evidence "
             "td-245).",
    "source": "GAME_DESIGN.md section 4; police system tasks td-190+",
}
POLICE_FOLLOWUPS = [
    ("td-220", "open — no new worker; coordination queue; no parallel "
               "dot police implementation", "Muse police lanes td-188/190/192"),
    ("td-221", "open — no new worker; coordination queue; cones excluded "
               "from dot map-access lane", "Muse police/map lanes td-190/203"),
    ("td-222", "open — no new worker; coordination queue; countdown not "
               "claimed under active dot repair",
     "Muse td-190 wanted owner / dot presentation coordination"),
]


class DueOwnershipTests(unittest.TestCase):
    def run_queue_health(self, board_rows, checklist_items):
        tmp = tempfile.mkdtemp(prefix="td315-qh-")
        state_dir = os.path.join(tmp, "state")
        os.makedirs(state_dir)
        with open(os.path.join(state_dir, "state.json"), "w") as f:
            json.dump({"workers": {}, "sessions": {}}, f)
        with open(os.path.join(state_dir, "pending_actions.json"), "w") as f:
            json.dump({"actions": [], "notes": []}, f)
        board_file = os.path.join(tmp, "board.md")
        with open(board_file, "w") as f:
            f.write(board_text(board_rows))
        checklist = os.path.join(tmp, "vision.json")
        with open(checklist, "w") as f:
            json.dump({"items": checklist_items}, f)
        buf = io.StringIO()
        with redirect_stdout(buf):
            watch.cmd_queue_health(["tokyo-drift-3d", "--state-dir", state_dir,
                                    "--board-file", board_file,
                                    "--checklist", checklist])
        return buf.getvalue().strip()

    def test_a_owned_followups_yield_already_owned_review_only_due(self):
        out = self.run_queue_health(
            POLICE_FOLLOWUPS + [("td-285", TD285_STATUS, "unassigned")],
            [POLICE_WANTED, STORY_LAYER])
        # DUE is preserved as a review signal naming the same item...
        self.assertTrue(
            out.startswith("QUEUE-EMPTY-VISION-DUE police-wanted"), out)
        # ...but qualified already-owned / review-only, naming the
        # covering follow-up rows — never an unqualified DUE.
        self.assertIn("ALREADY-OWNED", out)
        self.assertIn("review-only", out)
        for task in ("td-220", "td-221", "td-222"):
            self.assertIn(task, out)
        self.assertNotIn("story-layer", out)

    def test_a_linked_task_row_owned_also_covers(self):
        out = self.run_queue_health(
            [("td-195", "in_progress — defect tail being fixed",
              "Muse worker")],
            [POLICE_WANTED])
        self.assertTrue(
            out.startswith("QUEUE-EMPTY-VISION-DUE police-wanted"), out)
        self.assertIn("ALREADY-OWNED", out)
        self.assertIn("td-195", out)

    def test_a_unowned_unrestricted_followup_does_not_cover(self):
        # The linked task's own row is open, unowned and unrestricted:
        # nothing covers the item, so DUE stays a plain signal.
        out = self.run_queue_health(
            [("td-195", "open — ready to implement", "unassigned")],
            [dict(POLICE_WANTED, notes="Core merged.", source="")])
        # td-195 unowned counts as a candidate, so queue-health is OK,
        # not DUE at all — coverage must not be invented either way.
        self.assertTrue(out.startswith("QUEUE-HEALTH OK"), out)
        self.assertIn("candidates=1", out)

    def test_b_unowned_unrestricted_selected_item_plain_due(self):
        out = self.run_queue_health(
            [("td-285", TD285_STATUS, "unassigned")],
            [UNGATED_NOT_STARTED, STORY_LAYER])
        self.assertEqual(
            out, "QUEUE-EMPTY-VISION-DUE ungated-feature :: Ungated feature")
        self.assertNotIn("ALREADY-OWNED", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
