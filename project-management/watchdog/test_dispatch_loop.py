"""Deterministic offline tests. All sessions, collectors and projects are synthetic.

Positive dispatch goes through the REAL scoped/evidence guard, not a mocked GO.
"""
from copy import deepcopy
from datetime import timedelta
import json
import multiprocessing
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import coordinator as co
import dispatch_loop as loop
import evidence_policy as ep
import test_evidence_policy as evidence
import test_scoped_admission as scoped
from test_evidence_policy import NOW


def fixture(repo="example/evidence-policy", executor="native"):
    with patch.object(evidence, "REPO", repo), patch.object(scoped, "REPO", repo):
        case = scoped.docs_case()
    s = case["snapshot"]
    t = s["tasks"][0]
    t.update(project="lower-city", status="open", needs=["implementation"])
    s["board"][0]["status"] = "open"
    s["requests"][0]["project"] = "lower-city"
    s["executors"][0].update(id=executor, owner_id="worker-A", resume_task="ops-docs")
    s["scoped_source"]["binding"].update(operation="implementation", owner_id="worker-A", executor_id=executor)
    s["evidence_policy"]["ops-docs"]["authority"]["status"] = "open"
    scoped.seal(s)
    c = dict(repository=repo, task_id="ops-docs", state="ready", write_paths=["src/"], receipts=["SYNTHETIC approved task"])
    return case, c, packet(s)


def packet(s):
    return {"snapshot": s, "reconciliation": {
        "input_digest": co.digest(s), "observed_at": NOW.isoformat(), "evidence": "SYNTHETIC collector result",
        "board": "exact board commit/blob/row", "open_prs": "complete exact PR-head inventory",
        "user_stops": "explicit user-stop read", "sessions": "authorized tool session inventory",
        "liveness": "clear", "stops": []}}


def ledger_for(*candidates):
    return dict(version=1, revision=0, history={loop.key(c): {
        "prior_attempts": 0, "state": "open", "receipts": ["SYNTHETIC complete zero-attempt history"]}
        for c in candidates}, events=[])


def queue_for(*candidates):
    return dict(version=1, rollout_limit=3, ready=list(candidates), blocked=[])


def liveness(attempt, state, at=NOW + timedelta(minutes=11), session=None):
    return {attempt["attempt_id"]: dict(attempt_id=attempt["attempt_id"], session_id=session, state=state,
        observed_at=at.isoformat(), evidence="SYNTHETIC exact launch request and session reconciliation")}


def write_receipt(case, attempt):
    w = case["world"]
    w.file("src/feature.gd", "extends Node\n")
    head = w.commit(case["head"])
    ref = w.ref(head, "src/feature.gd")
    return {"kind": "receipt", "attempt_id": attempt["attempt_id"], "objects": w.objects,
            "receipt": dict(observed_at=NOW.isoformat(), evidence="SYNTHETIC authenticated write tool result",
                session_id="session-1", session_evidence="SYNTHETIC launch tool response",
                executor_id="native", owner_id="worker-A", started_at=NOW.isoformat(), written_at=NOW.isoformat(), first_write=ref)}


def race(path, queue, packets, result_queue):
    try:
        r = loop.transaction(path, 0, lambda ledger: loop.cycle(queue, ledger, packets, {}, NOW))
        result_queue.put(r["status"])
    except ValueError:
        result_queue.put("STALE")


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.case, self.c, self.p = fixture()
        self.q, self.l = queue_for(self.c), ledger_for(self.c)
        self.packets = {loop.key(self.c): self.p}
        # Every implementation/receipt proof is local; tests cannot open sockets.
        self.network = patch("socket.socket", side_effect=AssertionError("offline test attempted network"))
        self.network.start()
        self.addCleanup(self.network.stop)

    def cycle(self, at=NOW, observations=None):
        return loop.cycle(self.q, self.l, self.packets, observations or {}, at)

    def test_guarded_selection_and_no_duplicate_across_restart(self):
        result = self.cycle()
        self.assertEqual(result["status"], "DISPATCH_REQUIRED", result)
        self.assertEqual(result["attempt"]["state"], "admitted")
        self.l = json.loads(json.dumps(self.l))
        self.assertEqual(self.cycle()["status"], "ESCALATION_REQUIRED")
        self.assertEqual(len(loop.attempts(self.l)), 1)

    def test_stop_before_selection_is_retained_when_omitted_later(self):
        self.p["reconciliation"]["stops"] = ["PR374@exact-head R4 stop"]
        self.assertIn("R4 stop", json.dumps(self.cycle()))
        self.assertFalse(loop.attempts(self.l))
        self.p["reconciliation"]["stops"] = []
        self.assertEqual(self.cycle()["status"], "ESCALATION_REQUIRED")

    def test_real_guard_stops_denials_owners_queue_and_acceptance_stay_binding(self):
        for kind in ("stop", "denial", "security", "owner", "queue", "evidence"):
            with self.subTest(kind=kind):
                case, c, _ = fixture()
                s = case["snapshot"]
                if kind in {"stop", "denial", "security"}:
                    s["blockers"] = [dict(id="hold", repository=c["repository"], task_id=c["task_id"],
                        operations=["implementation"], executors=["*"], kind=kind, reason="explicit restriction")]
                elif kind == "owner":
                    s["owners"] = [dict(id="foreign", repository=c["repository"], task_id=c["task_id"],
                        operation="implementation", owner_id="Muse", executor_id="native", state="active")]
                elif kind == "queue":
                    s["queue"] = [dict(id="existing", repository=c["repository"], task_id=c["task_id"],
                        operation="implementation", owner_id="worker-A", executor_id="native", state="pending", head_sha=s["tasks"][0]["head_sha"])]
                else:
                    s["evidence_policy"]["ops-docs"]["submission"]["acknowledgment"]["rules"] = []
                scoped.seal(s)
                r = loop.cycle(queue_for(c), ledger_for(c), {loop.key(c): packet(s)}, {}, NOW)
                self.assertEqual(r["status"], "ESCALATION_REQUIRED", r)

    def test_frozen_projects_and_unknown_history(self):
        for project in ("shuto", "neon-drift"):
            s = deepcopy(self.p["snapshot"])
            s["tasks"][0]["project"] = project
            self.assertEqual(loop.cycle(self.q, self.l, {loop.key(self.c): packet(s)}, {}, NOW)["status"], "ESCALATION_REQUIRED")
        self.l["history"][loop.key(self.c)]["prior_attempts"] = None
        self.assertIn("never infer zero", json.dumps(self.cycle()))

    def test_initial_plus_one_correction_cap_survives_changed_executor_and_head(self):
        first = self.cycle()["attempt"]
        at = NOW + timedelta(minutes=11)
        self.assertIn("correction requires", json.dumps(self.cycle(at, liveness(first, "not_started"))))
        self.c["correction"] = dict(evidence="new launcher failure evidence", changed_approach="verified launch adapter")
        second = self.cycle(at)["attempt"]
        # Reconciliation at a later pass stays fresh without resealing production facts.
        at2 = NOW + timedelta(minutes=12)
        loop.append(self.l, "missing_receipt", second, "rejected", at2, unsuccessful=True, released=True,
                    reason="SYNTHETIC known launch failure", evidence="SYNTHETIC failed tool response")
        self.assertIn("exhausted", json.dumps(self.cycle(at2)))
        self.assertEqual(len(loop.attempts(self.l)), 2)
        self.c["correction"]["changed_approach"] = "different model, branch or failure label"
        self.assertIn("exhausted", json.dumps(self.cycle(at2)))

    def test_missing_receipt_rotates_after_confirmed_nonlaunch(self):
        first = self.cycle()["attempt"]
        _, second, p = fixture("example/second", "native-2")
        self.q["ready"].append(second)
        self.l["history"].update(ledger_for(second)["history"])
        self.packets[loop.key(second)] = p
        result = self.cycle(NOW + timedelta(minutes=11), liveness(first, "not_started"))
        self.assertEqual(result["attempt"]["key"], loop.key(second), result)
        self.assertTrue(loop.attempts(self.l)[0]["unsuccessful"])

    def test_unknown_liveness_is_failure_but_cannot_replace_session(self):
        first = self.cycle()["attempt"]
        self.c["correction"] = dict(evidence="new evidence", changed_approach="new approach")
        result = self.cycle(NOW + timedelta(minutes=11))
        self.assertEqual(result["status"], "ESCALATION_REQUIRED")
        a = loop.attempts(self.l)[0]
        self.assertTrue(a["unsuccessful"])
        self.assertFalse(a["released"])
        self.assertEqual(a["state"], "parked")
        result = self.cycle(NOW + timedelta(minutes=12), liveness(first, "ended", NOW + timedelta(minutes=12)))
        self.assertEqual(result["status"], "DISPATCH_REQUIRED", result)

    def test_actual_session_and_changed_git_artifact_required(self):
        a = self.cycle()["attempt"]
        event = write_receipt(self.case, a)
        for mutation in (lambda e: e["receipt"].update(session_id=""),
                         lambda e: e["receipt"].update(first_write=self.case["world"].ref(self.case["head"], "doc.md")),
                         lambda e: e.update(objects={}),
                         lambda e: e["receipt"].update(owner_id="foreign")):
            bad = deepcopy(event); mutation(bad)
            with self.assertRaises((ValueError, ep.PolicyError)):
                loop.record(self.l, bad, NOW)
        r = loop.record(self.l, event, NOW)
        self.assertEqual(r["state"], "in_progress")
        self.assertEqual(self.cycle()["status"], "ESCALATION_REQUIRED")

    def test_old_or_self_declared_acceptance_cannot_validate_new_code(self):
        a = self.cycle()["attempt"]
        loop.record(self.l, write_receipt(self.case, a), NOW)
        with self.assertRaises(ValueError):
            loop.record(self.l, dict(kind="review", attempt_id=a["attempt_id"], snapshot=self.p["snapshot"],
                                   state="validated", evidence="author claims success"), NOW)

    def test_missing_receipt_never_becomes_success_from_late_artifact(self):
        a = self.cycle()["attempt"]
        self.cycle(NOW + timedelta(minutes=11))
        with self.assertRaises(ValueError):
            loop.record(self.l, write_receipt(self.case, a), NOW + timedelta(minutes=11))

    def test_launch_without_write_is_not_implementation_and_preserves_session(self):
        a = self.cycle()["attempt"]
        receipt = write_receipt(self.case, a)["receipt"]
        session = {k: v for k, v in receipt.items() if k not in {"first_write", "written_at"}}
        result = loop.record(self.l, dict(kind="session", attempt_id=a["attempt_id"], session=session), NOW)
        self.assertEqual(result["state"], "admitted")
        self.assertEqual(loop.attempts(self.l)[0]["session"]["session_id"], "session-1")
        with self.assertRaises(ValueError):
            self.cycle(NOW + timedelta(minutes=11), liveness(a, "not_started"))
        r = self.cycle(NOW + timedelta(minutes=11), liveness(a, "live", session="session-1"))
        self.assertEqual(r["status"], "ESCALATION_REQUIRED")
        self.assertFalse(loop.attempts(self.l)[0]["released"])

    def test_same_executor_cannot_take_unrelated_replacement_until_reconciled(self):
        self.cycle()
        _, second, p = fixture("example/second", "native")
        self.q["ready"].append(second)
        self.l["history"].update(ledger_for(second)["history"])
        self.packets[loop.key(second)] = p
        self.assertIn("unreleased reservation", json.dumps(self.cycle()))
        self.assertEqual(len(loop.attempts(self.l)), 1)

    def test_empty_queue_has_exact_candidate_escalation(self):
        self.q["ready"] = []
        self.q["blocked"] = [dict(repository=self.c["repository"], task_id="td-197",
            reasons=["PR374 R4 authoring/publication stopped"], receipts=["PR374@93645f303a9193344224cf69722a2d0251c4b2f7"])]
        r = self.cycle()
        self.assertEqual(r["status"], "ESCALATION_REQUIRED")
        self.assertEqual(r["candidates"], self.q["blocked"])
        self.assertEqual(self.l["events"], [])

    def test_queue_limits_and_expired_or_changed_reconciliation(self):
        self.q["rollout_limit"] = 4
        with self.assertRaises(ValueError): self.cycle()
        self.q["rollout_limit"] = 3
        self.p["snapshot"]["requests"][0]["evidence"] = "changed user request"
        self.assertIn("snapshot changed", json.dumps(self.cycle()))
        self.p = packet(self.p["snapshot"]); self.packets[loop.key(self.c)] = self.p
        self.assertIn("stale", json.dumps(self.cycle(NOW + timedelta(minutes=16))))
        self.q["ready"] = [deepcopy(self.c) for _ in range(6)]
        with self.assertRaises(ValueError): self.cycle()

    def test_compare_and_swap_persistence_race_allows_only_one_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ATTEMPTS.json"
            path.write_text(json.dumps(self.l))
            context = multiprocessing.get_context("fork")
            results = context.Queue()
            workers = [context.Process(target=race, args=(path, self.q, self.packets, results)) for _ in range(2)]
            for worker in workers: worker.start()
            for worker in workers:
                worker.join(10)
                self.assertEqual(worker.exitcode, 0)
            self.assertEqual(sorted(results.get(timeout=2) for _ in workers), ["DISPATCH_REQUIRED", "STALE"])
            saved = json.loads(path.read_text())
            self.assertEqual(saved["history"], self.l["history"])
            self.assertEqual(saved["revision"], 1)
            self.assertEqual(len(loop.attempts(saved)), 1)


if __name__ == "__main__":
    unittest.main()
