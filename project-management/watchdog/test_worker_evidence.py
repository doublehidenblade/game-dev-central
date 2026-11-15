#!/usr/bin/env python3
"""Unit tests for watch.py _worker_evidence freshness rules (td-308).

History: _worker_evidence had no recency bound. td-218 (registered
2026-10-12, no heartbeat) stayed ALIVE forever on a branch whose newest
unique commit predated its dispatch, and td-217 stayed ALIVE because
hourly inspector-report PRs mention every task id in their body. Fix:
LIVENESS_EVIDENCE_MAX_MIN = 180 bounds every signal; branch evidence
must be post-dispatch AND fresh; report-only PRs never count.

Run: python3 test_worker_evidence.py  (exit 0 = all pass)
"""
import os
import sys
import unittest
from datetime import timedelta
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch

REPO = "doublehidenblade/tokyo-drift-3d"
TASK = "td-999"
TASK_FILE = "godot/docs/tasks/td-999.md"


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def commit(dt, msg="work"):
    return {"sha": "abcdef1234567890",
            "commit": {"committer": {"date": iso(dt)}, "message": msg}}


class WorkerEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.now = watch.now()
        self.dispatched = self.now - timedelta(days=10)
        self.commits = []    # task-file commits on main
        self.branches = []   # branch list
        self.compare = {}    # branch name -> compare payload
        self.prs = []        # open PRs

    def fake_gh(self, path):
        if "/commits?path=" in path:
            return self.commits
        if "/branches?" in path:
            return self.branches
        if "/compare/" in path:
            name = path.split("main...", 1)[1].split("?")[0]
            return self.compare[name]
        if "/pulls?" in path:
            return self.prs
        raise AssertionError(f"unexpected _gh path: {path}")

    def evidence(self):
        with mock.patch.object(watch, "_gh", side_effect=self.fake_gh):
            return watch._worker_evidence(REPO, TASK, TASK_FILE, self.dispatched)

    def add_branch(self, newest_dt, name="worker/td-999-fix"):
        self.branches = [{"name": name}]
        self.compare = {name: {"ahead_by": 1, "commits": [commit(newest_dt)]}}

    # --- Signal 2: branches -------------------------------------------------
    def test_old_pre_dispatch_branch_not_alive_salvage_kept(self):
        self.add_branch(self.dispatched - timedelta(days=1))
        alive, reasons, salvage = self.evidence()
        self.assertFalse(alive)
        self.assertTrue(any("worker/td-999-fix" in s for s in salvage),
                        f"salvage must still record the branch: {salvage}")

    def test_stale_post_dispatch_branch_not_alive(self):
        self.add_branch(self.now - timedelta(days=2))
        alive, _, salvage = self.evidence()
        self.assertFalse(alive)
        self.assertTrue(any("worker/td-999-fix" in s for s in salvage))

    def test_fresh_post_dispatch_branch_alive(self):
        self.add_branch(self.now - timedelta(minutes=10))
        alive, reasons, _ = self.evidence()
        self.assertTrue(alive)
        self.assertTrue(any("branch" in r for r in reasons))

    # --- Signal 3: open PRs ---------------------------------------------------
    def test_inspector_report_pr_mention_not_alive(self):
        self.prs = [{"number": 42, "title": "Inspector report 2026-11-15",
                     "body": "liveness unchanged (td-999 stale heartbeat)",
                     "updated_at": iso(self.now - timedelta(minutes=5)),
                     "html_url": "https://example.invalid/pr/42",
                     "head": {"ref": "inspector/report-2026-11-15"}}]
        alive, _, _ = self.evidence()
        self.assertFalse(alive)

    def test_fresh_worker_pr_mention_alive(self):
        self.prs = [{"number": 43, "title": "td-999: implement the fix",
                     "body": "Fix for td-999.",
                     "updated_at": iso(self.now - timedelta(minutes=5)),
                     "html_url": "https://example.invalid/pr/43",
                     "head": {"ref": "worker/td-999-fix"}}]
        alive, reasons, _ = self.evidence()
        self.assertTrue(alive)
        self.assertTrue(any("open PR #43" in r for r in reasons))

    def test_stale_worker_pr_mention_not_alive(self):
        self.prs = [{"number": 44, "title": "td-999: implement the fix",
                     "body": "Fix for td-999.",
                     "updated_at": iso(self.now - timedelta(days=3)),
                     "html_url": "https://example.invalid/pr/44",
                     "head": {"ref": "worker/td-999-fix"}}]
        alive, _, _ = self.evidence()
        self.assertFalse(alive)

    # --- Signal 1: task-file commits ------------------------------------------
    def test_old_task_file_commit_not_alive(self):
        # After dispatch, but far older than LIVENESS_EVIDENCE_MAX_MIN.
        self.commits = [commit(self.now - timedelta(days=2))]
        alive, _, _ = self.evidence()
        self.assertFalse(alive)

    def test_fresh_task_file_commit_alive(self):
        self.commits = [commit(self.now - timedelta(minutes=10))]
        alive, reasons, _ = self.evidence()
        self.assertTrue(alive)
        self.assertTrue(any("task-file commit" in r for r in reasons))


if __name__ == "__main__":
    unittest.main(verbosity=2)
