"""Offline scoped-source regressions using hash-verified Git objects.

All generated people, repositories and collection receipts here are SYNTHETIC.
No fixture seal is evidence of a real external read or live permission.
"""
import contextlib
import base64
import gzip
import hashlib
from pathlib import Path
from copy import deepcopy
from datetime import timedelta
import io
import json
import socket
import subprocess
import unittest
from unittest.mock import patch

import coordinator as co
import coordinator_cli as cli
import evidence_policy as ep
import scoped_admission as sa
import watch
from test_evidence_policy import World, REPO, NOW, STAMP


def seal(snapshot):
    """TEST ONLY: simulate all completed collector queries after a fixture edit."""
    scope = snapshot["scoped_source"]
    scope["receipts"] = []
    for repo, head in snapshot["repositories"].items():
        for kind in co.TABLES:
            rows = [r for r in snapshot[kind] if r["repository"] == repo]
            raw = scope["inventory"][kind] if kind in ("branches", "prs") else snapshot[kind]
            ids = [r["id"] for r in raw if r["repository"] == repo]
            scope["receipts"].append({"id": repo + ":" + kind, "kind": kind,
                "repository": repo, "source_repository": repo, "ref_sha": head,
                "observed_at": STAMP, "read_status": "ok", "ids": ids,
                "pagination": {"pages_read": 1, "items_seen": len(ids), "exhausted": True},
                "query_digest": ep.digest(sa.query(scope)),
                "inventory_digest": ep.digest(scope["inventory"]), "records_digest": ep.digest(rows),
                "provenance": "SYNTHETIC fixture: all named scoped sources observed; never live authority"})
    for receipt in scope["receipts"]:
        receipt["inventory_digest"] = sa.inventory_digest(snapshot, co.TABLES)
    return snapshot


def docs_case(task_transform=None, rule_paths=("rules.md",), candidate_rule_edit=False):
    w = World()
    task_id = "ops-docs"
    task = {"id": task_id, "completion_criteria": [{"id": "C1", "criterion": "Document one scoped decision", "verification": "Inspect the exact document and board diff"}],
            "evidence_rule_inventory": [{"id": "R" + str(i + 1), "repository": REPO, "path": p} for i, p in enumerate(rule_paths)],
            "evidence_policy": {"C1": {"applicability": "required", "rationale": "Documentary criterion", "rule_id": "R1", "instances": ["doc-decision"],
                "source_paths": ["doc.md", "board.md"], "build": None, "visual": False, "checks": []}}}
    if task_transform:
        task_transform(task)
    w.file("task.json", task)
    for path in rule_paths:
        w.file(path, "# Rules\nIndependent document review required.\n")
    board = "# Board\n\n| Task | State |\n|---|---|\n| ops-docs | open |\n| unrelated | open |\n\nContext remains unchanged.\n"
    w.file("board.md", board)
    w.file("doc.md", "Before scoped decision\n")
    base = w.commit()
    base_files = deepcopy(w.files)
    w.file("board.md", board.replace("ops-docs | open", "ops-docs | in_review"))
    w.file("doc.md", "After: scope and independent review are explicit.\n")
    if candidate_rule_edit:
        w.file(rule_paths[0], "# Candidate rule edit\nIndependent review still required.\n")
    source = w.commit(base)
    authority = {"version": 1, "observed_at": STAMP, "rule_heads": {REPO: base},
        "rules": [{"id": "R" + str(i + 1), "ref": w.ref(base, p)} for i, p in enumerate(rule_paths)], "task_ref": w.ref(source, "task.json"),
        "candidate": {"repository": REPO, "implementation_head": source, "artifact_head": source},
        "principals": {"author": "worker-A", "coordinator": "coordinator-A", "reviewer": "reviewer-B", "human": None},
        "owner_id": "worker-A", "status": "in_review", "stopped": False, "exclusions": {}, "attestations": [], "findings": [], "decisions": []}
    item = {"id": "document-proof", "criterion_id": "C1", "instances": ["doc-decision"], "type": "document",
        "ref": w.ref(source, "doc.md"), "source_head": source, "build": None, "performed_at": STAMP, "check_id": None}
    submission = {"acknowledgment": {"task_id": task_id, "author_id": "worker-A", "rules": deepcopy(authority["rules"])},
        "plans": {"C1": {"method": "Inspect document and exact board-row diff", "artifacts": [{"path": "doc.md", "type": "document"}],
            "source_paths": deepcopy(task["evidence_policy"]["C1"]["source_paths"]), "build": None, "coverage": ["doc-decision"], "reviewer_id": "reviewer-B"}}, "evidence": [item], "human_verdict": None}
    verdict = {"task_id": task_id, "candidate_head": source, "actor_id": "reviewer-B",
        "authority_digest": ep.acceptance_binding(authority), "evidence_digest": ep.digest(submission["evidence"]), "performed_at": STAMP,
        "criteria": {"C1": {"decision": "PASS", "rationale": "Original documentary evidence inspected", "citations": [item["ref"]], "evidence_ids": [item["id"]]}}}
    w.file("qa/review.json", verdict)
    head = w.commit(source)
    authority["candidate"]["artifact_head"] = head
    submission["verdict"] = w.ref(head, "qa/review.json")
    authority["attestations"] = [{"kind": "review", "ref": submission["verdict"], "actor_id": "reviewer-B", "observed_at": STAMP,
        "provenance": "SYNTHETIC authenticated fixture review; not external acceptance"}]
    check = ep.evaluate_completion(authority, submission, w.objects, NOW)
    assert check["status"] == "ACCEPTABLE", check
    snapshot = {"version": 1, "observed_at": STAMP, "repositories": {REPO: base}, "sources": [], **{k: [] for k in co.TABLES}}
    snapshot["policies"] = [{"id": "policy", "repository": REPO, "triggers_checked": True,
        "push_runs_actions": False, "push_deploys": False, "merge_runs_actions": False, "merge_deploys": False}]
    normalized = {"id": task_id, "repository": REPO, "head_sha": head, "status": "in_review", "owner_id": "worker-A", "author_id": "worker-A", "project": "docs",
        "needs": [], "criteria": ["C1"], "required_checks": ["evidence-policy:acceptance-check"],
        "requirements": {op: {"capabilities": [op], "model": None, "effort": None, "runtime_confirmation_required": False} for op in co.OPERATIONS[1:]}}
    snapshot["tasks"] = [normalized]
    snapshot["board"] = [{k: normalized[k] for k in ("id", "repository", "head_sha", "status", "owner_id")}]
    pr_id, branch_id = REPO + "#1", REPO + ":refs/heads/docs"
    snapshot["prs"] = [{"id": pr_id, "repository": REPO, "task_id": task_id, "head_sha": head, "author_id": "worker-A", "state": "open", "review_ids": ["review"], "check_ids": ["check"]}]
    snapshot["branches"] = [{"id": branch_id, "repository": REPO, "task_id": task_id, "head_sha": head}]
    snapshot["reviews"] = [{"id": "review", "repository": REPO, "task_id": task_id, "pr_id": pr_id, "head_sha": source,
        "observed_at": STAMP, "performed_at": STAMP, "reviewer_id": "reviewer-B", "verdict": "pass", "criteria": {"C1": {"result": "pass", "evidence": "qa/review.json"}}}]
    snapshot["checks"] = [{"id": "check", "repository": REPO, "task_id": task_id, "pr_id": pr_id, "head_sha": head,
        "observed_at": STAMP, "performed_at": STAMP, "name": "evidence-policy:acceptance-check", "result": "pass"}]
    snapshot["requests"] = [{"id": "authorized-source", "repository": REPO, "task_id": task_id, "project": "docs", "operations": list(co.OPERATIONS),
        "executors": ["*"], "kind": "standing", "state": "active", "authority_verified": True, "evidence": "SYNTHETIC user authorization fixture"}]
    snapshot["executors"] = [{"id": "native", "repository": REPO, "owner_id": "coordinator-A", "kind": "native", "state": "available",
        "capabilities": list(co.OPERATIONS), "observed_model": None, "observed_effort": None, "runtime_confirmed": False, "resume_task": None}]
    snapshot["evidence_policy"] = {task_id: {"authority": authority, "submission": submission, "objects": w.objects}}
    snapshot["scoped_source"] = {"version": 1,
        "binding": {"task_id": task_id, "repository": REPO, "operation": "merge", "executor_id": "native", "owner_id": "coordinator-A", "head_sha": head},
        "base_heads": {REPO: base}, "task_ids": [task_id], "related_task_ids": [task_id],
        "regions": [{"repository": REPO, "path": p, "row_keys": [task_id] if p == "board.md" else []} for p in ("doc.md", "board.md", "task.json", "qa/")],
        "candidate": {"pr_id": pr_id, "branch_id": branch_id, "fork_sha": base, "base_chain": [base], "head_chain": [head, source, base]},
        "inventory": {"branches": [
            {"id": REPO + ":refs/heads/main", "repository": REPO, "head_sha": base, "proof": {"kind": "base_ancestor", "chain": [base]}},
            {"id": branch_id, "repository": REPO, "head_sha": head, "proof": {"kind": "candidate"}}],
            "prs": [{"id": pr_id, "repository": REPO, "head_sha": head, "branch_id": branch_id, "author_id": "worker-A", "proof": {"kind": "candidate"}}]},
        "receipts": [], "objects": w.objects}
    return {"snapshot": seal(snapshot), "world": w, "base": base, "source": source, "head": head, "base_files": base_files, "board": board}


def add_branch(case, changes, pr=False, name="another"):
    w, s = case["world"], case["snapshot"]
    w.files = deepcopy(case["base_files"])
    for path, content in changes.items():
        w.file(path, content)
    head = w.commit(case["base"])
    branch_id = REPO + ":refs/heads/" + name
    proof = {"kind": "disjoint", "fork_sha": case["base"], "base_chain": [case["base"]], "head_chain": [head, case["base"]]}
    s["scoped_source"]["inventory"]["branches"].append({"id": branch_id, "repository": REPO, "head_sha": head, "proof": proof})
    if pr:
        s["scoped_source"]["inventory"]["prs"].append({"id": REPO + "#2", "repository": REPO, "head_sha": head, "branch_id": branch_id, "author_id": "another-worker", "proof": deepcopy(proof)})
    seal(s)
    return head


class ScopedAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.case = docs_case()
        self.s = self.case["snapshot"]

    def result(self):
        return co.evaluate(self.s, NOW)

    def assert_allowed(self):
        result = self.result()
        self.assertEqual(result["status"], "ACTION_REQUIRED", result)
        self.assertEqual(len(result["actions"]), 1, result)
        self.assertEqual(result["source_scope"]["global_coverage"], "unknown")
        return result["actions"][0]

    def assert_blocked(self):
        result = self.result()
        self.assertFalse(result["actions"], result)
        self.assertNotEqual(result["status"], "IDLE", result)
        return result

    def test_docs_only_actual_policy_check_positive(self):
        self.assertEqual(self.case["world"].objects, self.s["scoped_source"]["objects"])
        self.assert_allowed()
        self.assertEqual(self.s["tasks"][0]["required_checks"], ["evidence-policy:acceptance-check"])

    # Real PR143 changes precisely these four canonical rule paths. The Git
    # object graphs and ownership receipts below are synthetic controls, not
    # current live inventory or proof that PR143's author released ownership.
    RULE_PROPOSAL_PATHS = ("COORDINATOR.md", "project-management/rules/SYSTEM.md",
                          "project-management/rules/VALIDATOR_BRIEF.md",
                          "project-management/rules/WORKER_BRIEF.md")

    def rule_proposal_case(self, **kwargs):
        self.case = docs_case(rule_paths=self.RULE_PROPOSAL_PATHS, **kwargs)
        self.s = self.case["snapshot"]
        add_branch(self.case, {p: "# A separate proposed rule change\n" for p in self.RULE_PROPOSAL_PATHS},
                   pr=True, name="pr143-shaped-proposal")

    def test_pr143_shaped_read_only_authority_proposal_is_disjoint(self):
        self.rule_proposal_case()
        self.assert_allowed()
        # Every rule remains an exact current-base membership and receipt pin.
        packet = self.s["evidence_policy"]["ops-docs"]
        self.assertEqual(len(packet["authority"]["rules"]), 4)
        for rule in packet["authority"]["rules"]:
            self.assertEqual(rule["ref"]["commit"], self.case["base"])

    def test_rule_proposal_never_exempts_explicit_dependency_regions(self):
        for path in self.RULE_PROPOSAL_PATHS:
            with self.subTest(path=path):
                self.rule_proposal_case()
                self.s["scoped_source"]["regions"].append({"repository": REPO, "path": path, "row_keys": []})
                seal(self.s)
                self.assert_blocked()

    def test_rule_source_dependency_cannot_be_omitted_or_declared_unrelated(self):
        self.rule_proposal_case(task_transform=lambda t: t["evidence_policy"]["C1"]["source_paths"].append("COORDINATOR.md"))
        self.assert_blocked()  # Canonical source dependency omitted from regions.
        self.s["scoped_source"]["regions"].append({"repository": REPO, "path": "COORDINATOR.md", "row_keys": []})
        seal(self.s)
        self.assert_blocked()  # Now its actual competing source delta is visible.

    def test_candidate_rule_write_requires_region_and_blocks_competing_writer(self):
        self.case = docs_case(rule_paths=self.RULE_PROPOSAL_PATHS, candidate_rule_edit=True)
        self.s = self.case["snapshot"]
        self.assert_blocked()  # Computed candidate delta cannot hide a rule edit.
        self.s["scoped_source"]["regions"].append({"repository": REPO, "path": "COORDINATOR.md", "row_keys": []})
        seal(self.s)
        self.assert_allowed()
        add_branch(self.case, {"COORDINATOR.md": "# Competing rule edit\n"}, pr=True)
        self.assert_blocked()

    def test_read_only_rule_proposal_keeps_rule_freshness_and_membership_guards(self):
        for mode in ("blob", "commit", "missing-object", "stale-ack", "stale-receipt"):
            with self.subTest(mode=mode):
                self.rule_proposal_case()
                packet = self.s["evidence_policy"]["ops-docs"]
                rule = packet["authority"]["rules"][0]["ref"]
                if mode == "blob": rule["blob"] = "f" * 40
                if mode == "commit": rule["commit"] = self.case["head"]
                if mode == "missing-object": del self.s["scoped_source"]["objects"][REPO][rule["blob"]]
                if mode == "stale-ack": packet["submission"]["acknowledgment"]["rules"][0]["ref"]["commit"] = self.case["head"]
                if mode == "stale-receipt": self.s["scoped_source"]["receipts"][0]["observed_at"] = (NOW - timedelta(hours=1)).isoformat()
                self.assert_blocked()

    def test_rule_proposal_keeps_relevant_owner_queue_and_wildcard_stops(self):
        for kind in ("owners", "queue", "blockers"):
            with self.subTest(kind=kind):
                self.rule_proposal_case()
                if kind == "owners":
                    self.s[kind].append({"id": "rule-owner", "repository": REPO, "task_id": "ops-docs", "operation": "merge", "owner_id": "another-worker", "executor_id": "native", "state": "unknown"})
                elif kind == "queue":
                    self.s[kind].append({"id": "rule-queue", "repository": REPO, "task_id": "ops-docs", "operation": "merge", "owner_id": "another-worker", "executor_id": "native", "head_sha": self.case["head"], "state": "pending"})
                else:
                    self.s[kind].append({"id": "rule-stop", "repository": REPO, "task_id": "*", "executors": ["*"], "kind": "stop", "reason": "SYNTHETIC global stop", "operations": ["merge"]})
                seal(self.s)
                self.assert_blocked()

    def test_actual_public_rule_proposal_and_true_overlap_predicates(self):
        root = Path(__file__).parent / "fixtures/scoped-admission"
        manifest = json.loads((root / "rule-proposal-controls.json").read_text())
        raw = gzip.decompress(base64.b64decode((root / "rule-proposal-objects.json.gz.b64").read_text()))
        self.assertEqual(hashlib.sha256(raw).hexdigest(), manifest["uncompressed_sha256"])
        store = ep.GitObjects(json.loads(raw))
        for case in manifest["controls"]:
            rr, fork, head, base = (case[k] for k in ("repository", "fork", "head", "base"))
            if case["full_delta"]:
                self.assertEqual(sorted(sa.changed_paths(store, rr, fork, head)), case["changed_paths"])
            if case["pr"] == 143:
                # These actual four changed rule paths are absent from this
                # docs task's actual source/write regions. Their current-base
                # authority pins remain verified by the full-route tests.
                docs = [{"repository": rr, "path": "project-management/tasks/td-218-docs-admission/", "row_keys": []},
                        {"repository": rr, "path": "project-management/boards/tokyo-drift-3d.md", "row_keys": ["td-218"]}]
                self.assertFalse(any(sa.path_overlap(p, r) for p in case["changed_paths"] for r in docs))
            for region, expected in zip(case["regions"], case["expected"]):
                if "error" in expected:
                    with self.assertRaisesRegex(sa.ScopeError, expected["error"]):
                        sa.region_equal(store, rr, fork, head, region)
                else:
                    self.assertFalse(sa.region_equal(store, rr, fork, head, region))
                    self.assertFalse(sa.region_equal(store, rr, base, head, region))

    def test_old_global_missing_coverage_stays_blocked(self):
        self.s.pop("scoped_source")
        self.assert_blocked()

    def test_scoped_empty_work_never_global_idle(self):
        self.s["tasks"][0]["status"] = "paused"
        self.s["board"][0]["status"] = "paused"
        self.s["evidence_policy"]["ops-docs"]["authority"]["status"] = "paused"
        seal(self.s)
        self.assertEqual(self.assert_blocked()["status"], "INPUT_REQUIRED")

    def test_proved_disjoint_branch_and_pr_need_no_historical_task_normalization(self):
        add_branch(self.case, {"unrelated/game.py": "historical unrelated source"}, pr=True)
        self.assert_allowed()

    def test_ancestor_branch_does_not_need_task_id(self):
        self.s["scoped_source"]["inventory"]["branches"].append({"id": REPO + ":archive", "repository": REPO, "head_sha": self.case["source"],
            "proof": {"kind": "candidate_ancestor", "chain": [self.case["head"], self.case["source"]]}})
        seal(self.s)
        self.assert_allowed()

    def test_relevant_branch_blocks(self):
        add_branch(self.case, {"doc.md": "a live overlapping edit"})
        self.assertIn("overlapping", " ".join(self.assert_blocked()["warnings"]))

    def test_sibling_pr_cannot_hide_behind_task_name(self):
        add_branch(self.case, {"doc.md": "overlapping unrelated-name branch"}, pr=True, name="totally-unrelated-title")
        self.assert_blocked()

    def test_unknown_branch_proof_fails_closed(self):
        add_branch(self.case, {"unrelated.txt": "unrelated"})
        self.s["scoped_source"]["inventory"]["branches"][-1]["proof"] = {"kind": "unrelated", "unrelated": True}
        seal(self.s)
        self.assert_blocked()

    def test_forged_ancestry_edge_fails(self):
        add_branch(self.case, {"unrelated.txt": "unrelated"})
        row = self.s["scoped_source"]["inventory"]["branches"][-1]
        row["proof"] = {"kind": "base_ancestor", "chain": [self.case["base"], row["head_sha"]]}
        seal(self.s)
        self.assert_blocked()

    def test_relevant_file_and_row_mode_changes_are_not_disjoint(self):
        for path in ("doc.md", "board.md"):
            with self.subTest(path=path):
                case = docs_case()
                w, s, base = case["world"], case["snapshot"], case["base"]
                store = ep.GitObjects(w.objects)
                tree, _ = store.commit(REPO, base)
                entries = store.tree(REPO, tree)
                entries[path] = (b"100755", entries[path][1])
                raw = b"".join(mode + b" " + name.encode() + b"\0" + bytes.fromhex(oid)
                               for name, (mode, oid) in sorted(entries.items()))
                changed_tree = w.object("tree", raw)
                head = w.object("commit", "tree " + changed_tree + "\nparent " + base + "\n\nSynthetic mode change\n")
                s["scoped_source"]["inventory"]["branches"].append({"id": REPO + ":mode-change", "repository": REPO, "head_sha": head,
                    "proof": {"kind": "disjoint", "fork_sha": base, "base_chain": [base], "head_chain": [head, base]}})
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_shared_board_disjoint_row_allowed(self):
        add_branch(self.case, {"board.md": self.case["board"].replace("unrelated | open", "unrelated | in_progress")}, pr=True)
        self.assert_allowed()

    def test_shared_board_target_row_blocks(self):
        add_branch(self.case, {"board.md": self.case["board"].replace("ops-docs | open", "ops-docs | blocked")}, pr=True)
        self.assert_blocked()

    def test_shared_board_context_and_duplicates_block(self):
        for text in [self.case["board"].replace("# Board", "# Changed authority"), self.case["board"] + "\n| Task | State |\n|---|---|\n| ops-docs | duplicate |\n"]:
            with self.subTest(text=text):
                case = docs_case()
                add_branch(case, {"board.md": text})
                self.assertFalse(co.evaluate(case["snapshot"], NOW)["actions"])

    def test_candidate_scope_cannot_omit_path_or_row(self):
        for remove in ["doc.md", "task.json", "qa/"]:
            with self.subTest(remove=remove):
                s = deepcopy(self.s)
                s["scoped_source"]["regions"] = [r for r in s["scoped_source"]["regions"] if r["path"] != remove]
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])
        next(r for r in self.s["scoped_source"]["regions"] if r["path"] == "board.md")["row_keys"] = ["unrelated"]
        seal(self.s)
        self.assert_blocked()

    def test_every_receipt_missing_partial_stale_or_query_changed_blocks(self):
        for kind in co.TABLES:
            for bad in ("missing", "partial", "stale", "query", "inventory", "records", "pagination"):
                with self.subTest(kind=kind, bad=bad):
                    s = deepcopy(self.s)
                    r = next(x for x in s["scoped_source"]["receipts"] if x["kind"] == kind)
                    if bad == "missing": s["scoped_source"]["receipts"].remove(r)
                    if bad == "partial": r["read_status"] = "partial"
                    if bad == "stale": r["observed_at"] = (NOW - timedelta(minutes=15)).isoformat()
                    if bad in {"query", "inventory", "records"}: r[bad + "_digest"] = "changed"
                    if bad == "pagination": r["pagination"]["exhausted"] = False
                    self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_unknown_owner_and_queue_are_retained_even_when_branch_contained(self):
        owner = {"id": "owner", "repository": REPO, "task_id": "ops-docs", "operation": "merge", "owner_id": "coordinator-A", "executor_id": "native", "state": "unknown"}
        self.s["owners"] = [owner]
        seal(self.s)
        self.assert_blocked()
        self.s["owners"] = []
        self.s["queue"] = [{"id": "queue", "repository": REPO, "task_id": "ops-docs", "operation": "merge", "executor_id": "native", "owner_id": "coordinator-A", "head_sha": self.case["head"], "state": "pending"}]
        seal(self.s)
        self.assert_blocked()

    def test_provider_denial_stop_and_global_hold_remain(self):
        for kind in ("hold", "stop", "denial", "security", "cancelled"):
            for tid in ("ops-docs", "*"):
                with self.subTest(kind=kind, tid=tid):
                    s = deepcopy(self.s)
                    s["blockers"] = [{"id": "block", "repository": REPO, "task_id": tid, "operations": ["merge"], "executors": ["*"], "kind": kind, "reason": "Retained user decision"}]
                    seal(s)
                    self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_required_checks_never_empty_missing_failed_or_invented(self):
        for mode in ("empty", "missing", "failed", "different"):
            with self.subTest(mode=mode):
                s = deepcopy(self.s)
                if mode == "empty": s["tasks"][0]["required_checks"] = []
                if mode == "missing": s["checks"] = []; s["prs"][0]["check_ids"] = []
                if mode == "failed": s["checks"][0]["result"] = "fail"
                if mode == "different": s["checks"][0]["name"] = "fake-unit-test"
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_independent_proof_cannot_be_replaced_by_pass_word(self):
        for mode in ("no-proof", "self-review", "failed", "stale-ack"):
            with self.subTest(mode=mode):
                s = deepcopy(self.s)
                if mode == "no-proof": s["evidence_policy"]["ops-docs"]["submission"]["verdict"] = None
                if mode == "self-review": s["reviews"][0]["reviewer_id"] = "worker-A"
                if mode == "failed": s["reviews"][0]["verdict"] = "fail"
                if mode == "stale-ack": s["evidence_policy"]["ops-docs"]["submission"]["acknowledgment"]["rules"][0]["ref"]["commit"] = self.case["source"]
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_decision_binds_candidate_base_owner_rules_inventory_and_receipt(self):
        action = self.assert_allowed()
        target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
        self.assertEqual(co.revalidate(self.s, action, target, NOW)["status"], "GO")
        mutations = [lambda s: s["tasks"][0].update(head_sha=self.case["source"]),
            lambda s: s["repositories"].update({REPO: self.case["source"]}),
            lambda s: s["executors"][0].update(owner_id="someone-else"),
            lambda s: s["evidence_policy"]["ops-docs"]["authority"]["rules"][0]["ref"].update(blob="f" * 40),
            lambda s: s["scoped_source"]["inventory"]["branches"][0].update(head_sha=self.case["source"]),
            lambda s: s["scoped_source"]["receipts"][0].update(provenance="changed receipt")]
        for mutate in mutations:
            s = deepcopy(self.s); mutate(s)
            self.assertEqual(co.revalidate(s, action, target, NOW)["status"], "NO_GO")
        self.assertEqual(co.revalidate(self.s, action, target, NOW + timedelta(minutes=15))["status"], "NO_GO")

    def test_invalid_scope_never_falls_back_to_complete_legacy_sources(self):
        from test_rules import coordinator_seal
        coordinator_seal(self.s)
        self.s["scoped_source"]["unexpected"] = True
        self.assert_blocked()

    def test_all_cli_and_imported_supported_aliases_share_result_without_io(self):
        action = self.assert_allowed()
        args = ["--snapshot", "snapshot.json"]
        guard = args + ["--decision", "decision.json", "--task", "ops-docs", "--operation", "merge", "--executor", "native", "--owner", "coordinator-A", "--head", self.case["head"]]
        original = deepcopy(self.s)
        class FrozenClock:
            @staticmethod
            def now(tz):
                return NOW
        with patch.object(cli, "_load", side_effect=lambda p: self.s if p == "snapshot.json" else action), \
             patch.object(cli, "datetime", FrozenClock), \
             patch("builtins.open", side_effect=AssertionError("unexpected filesystem read")), \
             patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
             patch.object(subprocess, "run", side_effect=AssertionError("dispatch forbidden")):
            for alias in cli.ALIASES:
                argv = guard if alias == "dispatch-guard" else args
                for imported in (False, True):
                    with self.subTest(alias=alias, imported=imported), contextlib.redirect_stdout(io.StringIO()) as out:
                        try:
                            if imported:
                                code = getattr(watch, "cmd_" + alias.replace("-", "_"))(argv) or 0
                            else:
                                code = cli.run(alias, argv, NOW)
                        except SystemExit as stop:
                            code = stop.code
                        result = json.loads(out.getvalue())
                        self.assertEqual(result["status"], "GO" if alias == "dispatch-guard" else "ACTION_REQUIRED")
                        self.assertEqual(code, 3 if alias == "idle-defect-check" else 0)
                        if alias != "dispatch-guard":
                            self.assertEqual(result["actions"], [action])
        self.assertEqual(self.s, original)

    def test_duplicate_trigger_policy_cannot_use_first_safe_record(self):
        second = deepcopy(self.s["policies"][0])
        second.update(id="conflicting-policy", merge_runs_actions=True)
        self.s["policies"].append(second)
        seal(self.s)
        self.assert_blocked()

    def test_supported_operation_positives_and_deploy_not_supported(self):
        for operation in ("implementation", "verification", "upload", "merge"):
            with self.subTest(operation=operation):
                s = deepcopy(self.s)
                s["scoped_source"]["binding"]["operation"] = operation
                s["tasks"][0]["needs"] = [operation]
                if operation == "implementation":
                    s["tasks"][0]["status"] = s["board"][0]["status"] = "in_progress"
                    s["evidence_policy"]["ops-docs"]["authority"]["status"] = "in_progress"
                    s["executors"][0].update(owner_id="worker-A", resume_task="ops-docs")
                    s["scoped_source"]["binding"]["owner_id"] = "worker-A"
                seal(s)
                result = co.evaluate(s, NOW)
                self.assertEqual([a["operation"] for a in result["actions"]], [operation], result)
        self.s["scoped_source"]["binding"]["operation"] = "deploy"
        seal(self.s)
        self.assert_blocked()

    def test_relevant_dependency_owner_queue_or_hold_blocks(self):
        other = deepcopy(self.s["tasks"][0])
        other.update(id="dependency", status="paused")
        self.s["tasks"].append(other)
        self.s["board"].append({k: other[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
        self.s["scoped_source"]["task_ids"].append("dependency")
        self.s["scoped_source"]["related_task_ids"].append("dependency")
        for table, row in [
            ("owners", {"id": "dependency-owner", "repository": REPO, "task_id": "dependency", "operation": "implementation", "owner_id": "coordinator-A", "executor_id": "native", "state": "reserved"}),
            ("queue", {"id": "dependency-queue", "repository": REPO, "task_id": "dependency", "operation": "implementation", "executor_id": "native", "owner_id": "coordinator-A", "head_sha": self.case["head"], "state": "running"}),
            ("blockers", {"id": "dependency-stop", "repository": REPO, "task_id": "dependency", "operations": ["*"], "executors": ["*"], "kind": "stop", "reason": "Retain dependent owner's stop"})]:
            with self.subTest(table=table):
                s = deepcopy(self.s)
                s[table] = [row]
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_dependency_board_task_owner_cannot_disappear_from_owner_table(self):
        other = deepcopy(self.s["tasks"][0])
        other.update(id="dependency", status="in_progress", owner_id="another-worker")
        self.s["tasks"].append(other)
        self.s["board"].append({k: other[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
        self.s["scoped_source"]["task_ids"].append("dependency")
        self.s["scoped_source"]["related_task_ids"].append("dependency")
        seal(self.s)
        self.assert_blocked()

    def test_unproved_prerequisite_graphs_fail_even_with_owner_free_status(self):
        for key in ("depends_on", "dependencies"):
            with self.subTest(key=key):
                case = docs_case(lambda t: t.update({key: ["hidden-prerequisite"]}))
                self.assertFalse(co.evaluate(case["snapshot"], NOW)["actions"])
        other = deepcopy(self.s["tasks"][0])
        other.update(id="dependency", status="validated", owner_id=None)
        self.s["tasks"].append(other)
        self.s["board"].append({k: other[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
        self.s["scoped_source"]["task_ids"].append("dependency")
        self.s["scoped_source"]["related_task_ids"].append("dependency")
        seal(self.s)
        self.assert_blocked()

    def test_declared_dependency_region_cannot_be_hidden_as_disjoint(self):
        self.s["scoped_source"]["regions"].append({"repository": REPO, "path": "dependency/", "row_keys": []})
        add_branch(self.case, {"dependency/shared.py": "changed prerequisite source"})
        self.assert_blocked()

    def test_closed_current_task_and_original_frozen_holds_are_retained(self):
        for mode in ("cancelled", "done-pending-verdict", "shuto", "neon-drift", "td-054", "preservation"):
            with self.subTest(mode=mode):
                s = deepcopy(self.s)
                if mode in ("cancelled", "done-pending-verdict"):
                    s["board"][0]["status"] = mode
                elif mode in ("shuto", "neon-drift"):
                    s["tasks"][0]["project"] = mode
                    s["requests"][0]["project"] = mode
                elif mode == "preservation":
                    old, new = REPO + "#1", REPO + "#253"
                    s["prs"][0]["id"] = new
                    s["reviews"][0]["pr_id"] = s["checks"][0]["pr_id"] = new
                    s["scoped_source"]["candidate"]["pr_id"] = new
                    s["scoped_source"]["inventory"]["prs"][0]["id"] = new
                else:
                    # td-054's existing implementation gate is also covered by
                    # the unchanged inherited suite; a scoped binding cannot
                    # relabel this canonical task to impersonate it.
                    s["scoped_source"]["binding"]["task_id"] = "td-054"
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_unrequested_actions_or_triggered_publication_remain_blocked(self):
        for mode in ("unauthorized", "cancelled", "actions", "deployment", "unverified-trigger"):
            with self.subTest(mode=mode):
                s = deepcopy(self.s)
                if mode == "unauthorized": s["requests"][0]["operations"] = ["verification"]
                if mode == "cancelled": s["requests"][0]["state"] = "cancelled"
                if mode == "actions": s["policies"][0]["merge_runs_actions"] = True
                if mode == "deployment": s["policies"][0]["merge_deploys"] = True
                if mode == "unverified-trigger": s["policies"][0]["triggers_checked"] = False
                seal(s)
                self.assertFalse(co.evaluate(s, NOW)["actions"])

    def test_board_reorder_or_table_move_is_not_disjoint(self):
        two = "# Active\n\n| Task | State |\n|---|---|\n| ops-docs | open |\n| unrelated | open |\n\n# History\n\n| Task | State |\n|---|---|\n| archived | old |\n"
        swapped = two.replace("| ops-docs | open |", "SWAP").replace("| archived | old |", "| ops-docs | open |").replace("SWAP", "| archived | old |")
        reordered = two.replace("| ops-docs | open |\n| unrelated | open |", "| unrelated | open |\n| ops-docs | open |")
        self.assertNotEqual(sa.board_rows(two.encode()), sa.board_rows(swapped.encode()))
        self.assertNotEqual(sa.board_rows(two.encode()), sa.board_rows(reordered.encode()))
        active = "# Active\n\n| Task | State |\n|---|---|\n"
        historical = "# Historical\n\n| Task | State |\n|---|---|\n"
        row = "| ops-docs | open |\n"
        self.assertNotEqual(sa.board_rows((active + row + "\n" + historical).encode()),
                            sa.board_rows((active + "\n" + historical + row).encode()))

    def test_current_base_dependency_change_blocks(self):
        w = self.case["world"]
        w.files = deepcopy(self.case["base_files"])
        w.file("doc.md", "new main dependency incompatible with old branch")
        new_base = w.commit(self.case["base"])
        self.s["repositories"][REPO] = new_base
        self.s["scoped_source"]["base_heads"][REPO] = new_base
        self.s["evidence_policy"]["ops-docs"]["authority"]["rule_heads"][REPO] = new_base
        self.s["evidence_policy"]["ops-docs"]["authority"]["rules"][0]["ref"]["commit"] = new_base
        self.s["scoped_source"]["candidate"]["base_chain"] = [new_base, self.case["base"]]
        main = self.s["scoped_source"]["inventory"]["branches"][0]
        main.update(head_sha=new_base, proof={"kind": "base_ancestor", "chain": [new_base]})
        seal(self.s)
        self.assertIn("current-base dependency", " ".join(self.assert_blocked()["warnings"]))


def runtime_decision(case, record, path, replace_kind=None):
    """SYNTHETIC independent-collector artifact, never a live receipt builder."""
    w, s = case["world"], case["snapshot"]
    a = s["evidence_policy"]["ops-docs"]["authority"]
    saved = deepcopy(w.files)
    w.files = deepcopy(case["source_files"])
    w.file(path, record)
    commit = w.commit(case["source"])
    ref = w.ref(commit, path)
    w.files = saved
    if replace_kind:
        a["attestations"] = [r for r in a["attestations"] if r.get("binding", {}).get("kind") != replace_kind]
    a["attestations"].append({"kind": "decision", "ref": ref, "actor_id": record["actor_id"],
        "observed_at": STAMP, "provenance": "SYNTHETIC independent context/source inspection",
        "binding": {"kind": record["kind"], "digest": ep.digest(record)}})
    return ref


def runtime_designation(case):
    s = case["snapshot"]; scope = s["scoped_source"]; c = scope["composition"]
    record = {"kind": "runtime-composition", "task_id": "ops-docs", "actor_id": "coordinator-A",
        "performed_at": STAMP, "binding": deepcopy(scope["binding"]),
        "composition": {k: c[k] for k in ("repository", "target_ref", "head_sha", "request_id")},
        "candidate": {k: deepcopy(scope["candidate"][k]) for k in ("pr_id", "branch_id", "target")},
        "request_digest": ep.digest(s["requests"][0]), "decision": "DESIGNATED",
        "rationale": "SYNTHETIC independently designated fixed runtime for this exact operation"}
    c["designation_ref"] = runtime_decision(case, record, "authority/composition.json", "runtime-composition")


def runtime_review(case):
    w, s = case["world"], case["snapshot"]
    packet = s["evidence_policy"]["ops-docs"]; a, submission = packet["authority"], packet["submission"]
    item = submission["evidence"][0]
    record = {"task_id": "ops-docs", "candidate_head": case["source"], "actor_id": "reviewer-B",
        "authority_digest": ep.acceptance_binding(a), "evidence_digest": ep.digest(submission["evidence"]),
        "performed_at": STAMP, "criteria": {"C1": {"decision": "PASS", "rationale": "SYNTHETIC original evidence inspected",
        "citations": [item["ref"]], "evidence_ids": [item["id"]]}}}
    saved = deepcopy(w.files); w.files = deepcopy(case["source_files"])
    w.file("authority/review.json", record); commit = w.commit(case["source"])
    submission["verdict"] = w.ref(commit, "authority/review.json"); w.files = saved
    a["attestations"] = [r for r in a["attestations"] if r["kind"] != "review"]
    a["attestations"].append({"kind": "review", "ref": submission["verdict"], "actor_id": "reviewer-B",
        "observed_at": STAMP, "provenance": "SYNTHETIC authenticated independent completion inspection"})


def runtime_case():
    case = docs_case(); w, s = case["world"], case["snapshot"]
    board = "# Board\n\n| Task | State |\n|---|---|\n| unrelated | open |\n\nContext remains unchanged.\n"
    w.files = deepcopy(case["base_files"]); w.file("board.md", board)
    composition = w.commit(); base_files = deepcopy(w.files)
    w.file("rules.md", "# Current rules\nIndependent inspection remains mandatory.\n")
    w.file("other-main.txt", "Unrelated current-main work\n"); rules_head = w.commit(composition)
    w.files = deepcopy(base_files)
    task = ep.GitObjects(w.objects).json(w.ref(composition, "task.json"))
    descriptor = {"repository": REPO, "target_ref": "refs/heads/runtime", "head_sha": composition,
                  "request_id": "authorized-source"}
    task["runtime_composition"] = descriptor
    w.file("task.json", task); w.file("doc.md", "After: independently reviewed bounded runtime repair.\n")
    w.file("board.md", board.replace("| unrelated | open |\n", "| unrelated | open |\n| ops-docs | in_review |\n"))
    source = w.commit(composition)
    case.update(base=composition, source=source, head=source, base_files=base_files, source_files=deepcopy(w.files), board=board)
    packet = s["evidence_policy"]["ops-docs"]; a, submission = packet["authority"], packet["submission"]
    a.update(rule_heads={REPO: rules_head}, rules=[{"id": "R1", "ref": w.ref(rules_head, "rules.md")}],
             task_ref=w.ref(source, "task.json"), candidate={"repository": REPO, "implementation_head": source, "artifact_head": source}, attestations=[])
    submission["acknowledgment"]["rules"] = deepcopy(a["rules"])
    submission["evidence"][0].update(ref=w.ref(source, "doc.md"), source_head=source)
    s["repositories"] = {REPO: rules_head}
    for table in ("tasks", "board", "prs", "branches", "checks", "reviews"):
        for row in s[table]: row["head_sha"] = source
    s["requests"][0]["executors"] = ["native"]
    scope = s["scoped_source"]
    scope.update(version=2, base_heads={REPO: rules_head}, composition={**descriptor, "designation_ref": None}, context_assessments=[])
    scope["binding"]["head_sha"] = source
    target = {"repository": REPO, "ref": descriptor["target_ref"], "head_sha": composition}
    scope["candidate"].update(fork_sha=composition, base_chain=[composition], head_chain=[source, composition], target=target)
    scope["inventory"]["branches"] = [
        {"id": REPO + ":refs/heads/main", "repository": REPO, "head_sha": rules_head,
         "proof": {"kind": "disjoint", "fork_sha": composition, "base_chain": [composition], "head_chain": [rules_head, composition]}},
        {"id": REPO + ":refs/heads/runtime", "repository": REPO, "head_sha": composition,
         "proof": {"kind": "base_ancestor", "chain": [composition]}},
        {"id": scope["candidate"]["branch_id"], "repository": REPO, "head_sha": source, "proof": {"kind": "candidate"}}]
    scope["inventory"]["prs"][0].update(head_sha=source, target=deepcopy(target))
    runtime_designation(case); runtime_review(case); seal(s)
    return case


def runtime_foreign(case, board=None, pr=True):
    w, s = case["world"], case["snapshot"]
    w.files = deepcopy(case["base_files"])
    w.file("board.md", board or case["board"].replace("# Board", "# Historical layout\nArchived prose")
           .replace("| unrelated | open |", "| **old row** | open |"))
    head = w.commit(case["base"])
    branch_id = REPO + ":refs/heads/foreign"
    proof = {"kind": "disjoint", "fork_sha": case["base"], "base_chain": [case["base"]], "head_chain": [head, case["base"]]}
    s["scoped_source"]["inventory"]["branches"].append({"id": branch_id, "repository": REPO, "head_sha": head, "proof": proof})
    if pr:
        s["scoped_source"]["inventory"]["prs"].append({"id": REPO + "#2", "repository": REPO,
            "head_sha": head, "branch_id": branch_id, "author_id": "foreign-worker", "proof": deepcopy(proof)})
    seal(s)
    return head


def runtime_context(case, transform=None):
    s = case["snapshot"]; scope = s["scoped_source"]; w = case["world"]
    region = next(r for r in scope["regions"] if r["path"] == "board.md")
    store = ep.GitObjects(w.objects); refs = []
    a = s["evidence_policy"]["ops-docs"]["authority"]
    a["attestations"] = [r for r in a["attestations"] if r.get("binding", {}).get("kind") != "foreign-row-context"]
    for kind in ("branches", "prs"):
        for item in scope["inventory"][kind]:
            if item["head_sha"] != scope["inventory"]["branches"][-1]["head_sha"] or item["proof"]["kind"] != "disjoint": continue
            left, right = sa.leaf(store, REPO, case["base"], "board.md"), sa.leaf(store, REPO, item["head_sha"], "board.md")
            if not left or not right: continue
            bound = sa.context_binding(scope, item, kind, region, case["base"], case["base"], left, right, s)
            spans = sa.context_spans(store.read(REPO, left[1], "blob").decode(), store.read(REPO, right[1], "blob").decode())
            record = {"kind": "foreign-row-context", "task_id": "ops-docs", "actor_id": "reviewer-B", "performed_at": STAMP,
                "binding": deepcopy(bound), "spans": [{**x, "effects": {k: "outside_scope" for k in ("task", "dependency", "owner", "global_stop")},
                "rationale": "SYNTHETIC full changed span inspected: unrelated archived layout only"} for x in spans],
                "identity": {"classification": "unambiguous_foreign", "rationale": "SYNTHETIC all raw identities inspected, none can denote the protected task"},
                "decision": "OUTSIDE_SCOPE", "rationale": "SYNTHETIC independent full source/context and global-owner closure judgment"}
            if transform: transform(record)
            refs.append(runtime_decision(case, record, "authority/context-" + kind + ".json"))
    scope["context_assessments"] = refs
    runtime_review(case); seal(s)


class RuntimeCompositionTests(unittest.TestCase):
    def setUp(self):
        self.case = runtime_case(); self.s = self.case["snapshot"]

    def allowed(self):
        result = co.evaluate(self.s, NOW)
        self.assertEqual(result["status"], "ACTION_REQUIRED", result)
        self.assertEqual(len(result["actions"]), 1, result)
        self.assertEqual(result["source_scope"]["global_coverage"], "unknown")
        return result["actions"][0]

    def blocked(self):
        result = co.evaluate(self.s, NOW)
        self.assertFalse(result["actions"], result)
        self.assertNotEqual(result["status"], "IDLE", result)
        return result

    def test_current_rules_and_runtime_heads_remain_distinct_positive(self):
        self.assertNotEqual(self.s["repositories"][REPO], self.case["base"])
        self.allowed()
        a = self.s["evidence_policy"]["ops-docs"]["authority"]
        self.assertEqual(a["rule_heads"], self.s["repositories"])

    def test_missing_forged_stale_or_self_composition_designation(self):
        for mode in ("missing", "unattested", "self", "stale", "bad-binding", "BLOCK", "duplicate"):
            with self.subTest(mode=mode):
                self.setUp(); a = self.s["evidence_policy"]["ops-docs"]["authority"]
                r = next(x for x in a["attestations"] if x["kind"] == "decision")
                if mode == "missing": self.s["scoped_source"]["composition"]["designation_ref"] = None
                if mode == "unattested": a["attestations"].remove(r)
                if mode == "self": r["actor_id"] = "worker-A"
                if mode == "stale": r["observed_at"] = (NOW - timedelta(minutes=15)).isoformat()
                if mode == "bad-binding": r["binding"]["digest"] = "invented"
                if mode == "duplicate": a["attestations"].append(deepcopy(r))
                if mode == "BLOCK":
                    d = ep.GitObjects(self.case["world"].objects).json(r["ref"]); d["decision"] = "BLOCK"
                    runtime_decision(self.case, d, "authority/blocked.json", "runtime-composition")
                seal(self.s); self.blocked()

    def test_exact_task_request_executor_target_ref_and_ancestry_binding(self):
        mutations = [lambda s: s["requests"][0].update(task_id="*"),
            lambda s: s["requests"][0].update(executors=["*"]),
            lambda s: s["requests"][0].update(authority_verified=False),
            lambda s: s["requests"][0].update(state="cancelled"),
            lambda s: s["scoped_source"]["candidate"]["target"].update(ref="refs/heads/same-sha-wrong-ref"),
            lambda s: s["scoped_source"]["inventory"]["prs"][0]["target"].update(ref="refs/heads/retargeted"),
            lambda s: s["scoped_source"]["inventory"]["branches"].pop(1),
            lambda s: s["scoped_source"]["inventory"]["branches"][1].update(head_sha=self.case["source"]),
            lambda s: s["scoped_source"]["candidate"].update(head_chain=[self.case["source"], s["repositories"][REPO], self.case["base"]]),
            lambda s: s["scoped_source"]["composition"].update(head_sha=self.case["source"])]
        for i, mutate in enumerate(mutations):
            with self.subTest(i=i):
                self.setUp(); mutate(self.s); seal(self.s); self.blocked()

    def test_composition_conflicts_cannot_hide_in_outer_envelope(self):
        for field, value in (("task_id", "different-task"), ("kind", "runtime-composition-unknown")):
            with self.subTest(field=field):
                self.setUp(); self.allowed()
                a = self.s["evidence_policy"]["ops-docs"]["authority"]
                receipt = next(r for r in a["attestations"] if r.get("binding", {}).get("kind") == "runtime-composition")
                record = ep.GitObjects(self.case["world"].objects).json(receipt["ref"])
                record.update(decision="BLOCK"); record[field] = value
                runtime_decision(self.case, record, "authority/composition-conflict.json")
                runtime_review(self.case); seal(self.s); self.blocked()

    def test_foreign_historical_context_requires_real_independent_closure(self):
        runtime_foreign(self.case); self.blocked()
        runtime_context(self.case); self.allowed()

    def test_no_literal_id_global_owner_or_dependency_effect_blocks(self):
        for effect in ("global_stop", "owner", "dependency", "task"):
            with self.subTest(effect=effect):
                self.setUp()
                runtime_foreign(self.case, self.case["board"] + "All native implementation is stopped; shared owner reserved.\n")
                runtime_context(self.case, lambda d: d["spans"][0]["effects"].update({effect: "applicable"}))
                self.blocked()

    def test_incomplete_ambiguous_stale_forged_and_worker_context_assessments(self):
        mutations = [lambda d: d.update(spans=[]), lambda d: d.update(decision="BLOCK"),
            lambda d: d.update(decision="unknown"), lambda d: d.update(actor_id="worker-A"),
            lambda d: d["identity"].update(classification="ambiguous"),
            lambda d: d["spans"][0].update(before_digest="forged"),
            lambda d: d["spans"][0]["effects"].update(global_stop="unknown"),
            lambda d: d["binding"]["source"].update(comparison_base="f" * 40),
            lambda d: d["binding"].update(related_task_ids=[])]
        for i, mutate in enumerate(mutations):
            with self.subTest(i=i):
                self.setUp(); runtime_foreign(self.case); runtime_context(self.case, mutate); self.blocked()
        self.setUp(); runtime_foreign(self.case); runtime_context(self.case)
        a = self.s["evidence_policy"]["ops-docs"]["authority"]
        next(r for r in a["attestations"] if r.get("binding", {}).get("kind") == "foreign-row-context")["observed_at"] = (NOW - timedelta(minutes=15)).isoformat()
        self.blocked()

    def test_duplicate_or_unselected_conflicting_context_never_cherry_picked(self):
        for decision in ("OUTSIDE_SCOPE", "BLOCK", "unknown"):
            with self.subTest(decision=decision):
                self.setUp(); runtime_foreign(self.case); runtime_context(self.case)
                a = self.s["evidence_policy"]["ops-docs"]["authority"]
                receipt = next(r for r in a["attestations"] if r.get("binding", {}).get("kind") == "foreign-row-context")
                d = ep.GitObjects(self.case["world"].objects).json(receipt["ref"])
                d["decision"] = decision
                runtime_decision(self.case, d, "authority/unselected.json")
                runtime_review(self.case); seal(self.s); self.blocked()

    def test_structurally_matching_conflicts_cannot_hide_in_outer_envelope(self):
        for field, value in (("task_id", "different-task"), ("kind", "foreign-row-context-unknown")):
            with self.subTest(field=field):
                self.setUp(); runtime_foreign(self.case); runtime_context(self.case); self.allowed()
                a = self.s["evidence_policy"]["ops-docs"]["authority"]
                receipt = next(r for r in a["attestations"] if r.get("binding", {}).get("kind") == "foreign-row-context")
                record = ep.GitObjects(self.case["world"].objects).json(receipt["ref"])
                record.update(decision="BLOCK"); record[field] = value
                runtime_decision(self.case, record, "authority/conflicting-envelope.json")
                runtime_review(self.case); seal(self.s); self.blocked()

    def test_protected_literal_encoded_duplicate_and_ambiguous_id_never_excluded(self):
        for text in ("ops-docs", "ops&#45;docs", "ops%2Ddocs", "ops\\-docs", "ops\\u002ddocs",
                     "| ops-docs | open |\n| ops-docs | duplicate |"):
            with self.subTest(text=text):
                self.setUp(); runtime_foreign(self.case, self.case["board"] + text + "\n")
                runtime_context(self.case); self.blocked()

    def test_context_source_mode_missing_object_and_whole_file_conflicts_remain(self):
        self.setUp(); runtime_foreign(self.case); runtime_context(self.case)
        scope = self.s["scoped_source"]; region = next(r for r in scope["regions"] if r["path"] == "board.md")
        region["row_keys"] = []; seal(self.s); self.blocked()
        self.setUp(); head = runtime_foreign(self.case); runtime_context(self.case)
        oid = sa.blob(ep.GitObjects(self.case["world"].objects), REPO, head, "board.md")
        del self.case["world"].objects[REPO][oid]; self.blocked()

    def test_foreign_file_deletion_type_mode_and_invalid_utf8_fail_closed(self):
        for mode in ("delete", "100755", "120000", "40000", "utf8"):
            with self.subTest(mode=mode):
                self.setUp(); old = runtime_foreign(self.case, pr=False)
                w = self.case["world"]; store = ep.GitObjects(w.objects)
                if mode in ("delete", "utf8"):
                    if mode == "delete": del w.files["board.md"]
                    else: w.file("board.md", b"\xff invalid UTF-8\n")
                    head = w.commit(self.case["base"])
                else:
                    tree, _ = store.commit(REPO, old)
                    raw = store.read(REPO, tree, "tree").replace(b"100644 board.md\0", mode.encode() + b" board.md\0")
                    new_tree = w.object("tree", raw)
                    head = w.object("commit", store.read(REPO, old, "commit").replace(tree.encode(), new_tree.encode(), 1))
                item = self.s["scoped_source"]["inventory"]["branches"][-1]
                item["head_sha"] = head; item["proof"]["head_chain"] = [head, self.case["base"]]
                seal(self.s); result = self.blocked()
                expected = {"delete": "create/delete", "100755": "mode", "120000": "regular file",
                            "40000": "regular file", "utf8": "utf-8"}[mode]
                self.assertIn(expected, " ".join(result["warnings"]).lower())

    def test_unselected_context_cannot_hide_behind_strict_equal_row_proof(self):
        runtime_foreign(self.case, self.case["board"].replace("unrelated | open", "unrelated | closed"))
        self.allowed()  # Existing exact row-only proof needs no semantic fallback.
        runtime_context(self.case, lambda d: d.update(decision="BLOCK"))
        self.s["scoped_source"]["context_assessments"] = []
        runtime_review(self.case); seal(self.s); self.blocked()

    def test_actual_main_and_sibling_whole_file_conflicts_are_not_excluded(self):
        for source in ("main", "sibling"):
            with self.subTest(source=source):
                self.setUp(); w = self.case["world"]; scope = self.s["scoped_source"]
                w.files = deepcopy(self.case["base_files"])
                w.file("doc.md", "Conflicting actual protected source\n")
                if source == "main":
                    old = self.s["repositories"][REPO]
                    w.file("rules.md", ep.GitObjects(w.objects).read(REPO, sa.blob(ep.GitObjects(w.objects), REPO, old, "rules.md"), "blob"))
                    head = w.commit(self.case["base"])
                    self.s["repositories"][REPO] = head; scope["base_heads"][REPO] = head
                    a = self.s["evidence_policy"]["ops-docs"]["authority"]
                    a["rule_heads"][REPO] = head; a["rules"][0]["ref"] = w.ref(head, "rules.md")
                    self.s["evidence_policy"]["ops-docs"]["submission"]["acknowledgment"]["rules"] = deepcopy(a["rules"])
                    item = scope["inventory"]["branches"][0]
                    item["head_sha"] = head; item["proof"]["head_chain"] = [head, self.case["base"]]
                else:
                    add_branch(self.case, {"doc.md": "Conflicting actual protected source\n"}, pr=True)
                runtime_review(self.case); seal(self.s)
                self.assertIn("overlapping", " ".join(self.blocked()["warnings"]))

    def test_candidate_context_remains_strict_with_v2_foreign_fallback_enabled(self):
        w = self.case["world"]; w.files = deepcopy(self.case["source_files"])
        w.file("board.md", self.case["board"].replace("# Board", "# Changed candidate context")
               .replace("| unrelated | open |", "| unrelated | open |\n| ops-docs | in_review |"))
        head = w.commit(self.case["base"]); self.case.update(source=head, head=head, source_files=deepcopy(w.files))
        packet = self.s["evidence_policy"]["ops-docs"]; a = packet["authority"]
        a.update(task_ref=w.ref(head, "task.json"), candidate={"repository": REPO, "implementation_head": head, "artifact_head": head})
        packet["submission"]["evidence"][0].update(ref=w.ref(head, "doc.md"), source_head=head)
        for table in ("tasks", "board", "branches", "prs", "checks", "reviews"):
            for row in self.s[table]: row["head_sha"] = head
        scope = self.s["scoped_source"]; scope["binding"]["head_sha"] = head
        scope["candidate"]["head_chain"] = [head, self.case["base"]]
        scope["inventory"]["branches"][-1]["head_sha"] = head; scope["inventory"]["prs"][0]["head_sha"] = head
        runtime_designation(self.case); runtime_review(self.case); seal(self.s)
        self.assertIn("non-row context changed", " ".join(self.blocked()["warnings"]))

    def test_each_v2_operation_keeps_setup_independence_and_publication_gates(self):
        for operation in ("implementation", "verification", "upload", "merge"):
            with self.subTest(operation=operation):
                self.setUp(); scope = self.s["scoped_source"]
                scope["binding"]["operation"] = operation
                self.s["tasks"][0]["needs"] = [operation]
                if operation == "implementation":
                    self.s["tasks"][0]["status"] = "open"; self.s["board"][0]["status"] = "open"
                    self.s["executors"][0]["resume_task"] = "ops-docs"
                    self.s["executors"][0]["owner_id"] = "worker-A"; scope["binding"]["owner_id"] = "worker-A"
                    self.s["evidence_policy"]["ops-docs"]["authority"]["status"] = "open"
                runtime_designation(self.case); runtime_review(self.case); seal(self.s); self.allowed()
                self.s["tasks"][0]["requirements"][operation]["runtime_confirmation_required"] = True
                seal(self.s); self.blocked()
                self.s["tasks"][0]["requirements"][operation]["runtime_confirmation_required"] = False
                if operation in ("merge", "upload"):
                    self.s["policies"][0][("merge" if operation == "merge" else "push") + "_runs_actions"] = True
                elif operation == "verification":
                    self.s["tasks"][0]["author_id"] = "coordinator-A"
                else:
                    self.s["tasks"][0]["project"] = "shuto"
                seal(self.s); self.blocked()

    def test_context_exclusion_never_releases_owner_queue_or_global_stop(self):
        for kind in ("owners", "queue", "blockers"):
            with self.subTest(kind=kind):
                self.setUp(); runtime_foreign(self.case); runtime_context(self.case)
                if kind == "owners": self.s[kind] = [{"id": "owner", "repository": REPO, "task_id": "ops-docs", "operation": "merge", "owner_id": "other", "executor_id": "native", "state": "unknown"}]
                if kind == "queue": self.s[kind] = [{"id": "queue", "repository": REPO, "task_id": "ops-docs", "operation": "merge", "owner_id": "other", "executor_id": "native", "head_sha": self.case["source"], "state": "pending"}]
                if kind == "blockers": self.s[kind] = [{"id": "global", "repository": REPO, "task_id": "*", "operations": ["*"], "executors": ["*"], "kind": "stop", "reason": "SYNTHETIC global stop"}]
                seal(self.s); self.blocked()

    def test_independent_owner_transfer_probe_invalidates_context_assessment(self):
        # Independent review's unchanged same-head author/owner transfer probe.
        runtime_foreign(self.case, self.case["board"] + "\nWorker-C work is stopped across all tasks.\n")
        runtime_context(self.case); self.allowed()
        citations = deepcopy(self.s["scoped_source"]["context_assessments"])
        packet = self.s["evidence_policy"]["ops-docs"]
        self.s["tasks"][0].update(author_id="Worker-C", owner_id="Worker-C")
        self.s["board"][0]["owner_id"] = "Worker-C"
        packet["authority"]["principals"]["author"] = "Worker-C"
        packet["authority"]["owner_id"] = "Worker-C"
        packet["submission"]["acknowledgment"]["author_id"] = "Worker-C"
        runtime_review(self.case); seal(self.s)
        self.assertEqual(self.s["scoped_source"]["context_assessments"], citations)
        self.assertIn("source/scope assessment changed", " ".join(self.blocked()["warnings"]))

    def test_changed_owner_and_queue_closure_require_fresh_context_judgment(self):
        for kind in ("owners", "queue"):
            with self.subTest(kind=kind):
                self.setUp(); runtime_foreign(self.case); runtime_context(self.case); self.allowed()
                if kind == "owners":
                    self.s[kind] = [{"id": "released", "repository": REPO, "task_id": "ops-docs", "operation": "implementation", "owner_id": "coordinator-A", "executor_id": "native", "state": "released"}]
                else:
                    self.s[kind] = [{"id": "reservation", "repository": REPO, "task_id": "ops-docs", "operation": "verification", "owner_id": "coordinator-A", "executor_id": "native", "head_sha": self.case["source"], "state": "pending"}]
                runtime_review(self.case); seal(self.s)
                self.assertIn("source/scope assessment changed", " ".join(self.blocked()["warnings"]))

    def test_v2_still_needs_current_ack_real_checks_and_independent_acceptance(self):
        for mode in ("ack", "missing-check", "failed-check", "invented-check", "self-review", "missing-verdict"):
            with self.subTest(mode=mode):
                self.setUp(); packet = self.s["evidence_policy"]["ops-docs"]
                if mode == "ack": packet["submission"]["acknowledgment"]["rules"][0]["ref"]["commit"] = self.case["base"]
                if mode == "missing-check": self.s["checks"] = []; self.s["prs"][0]["check_ids"] = []
                if mode == "failed-check": self.s["checks"][0]["result"] = "fail"
                if mode == "invented-check": self.s["checks"][0]["name"] = "invented"
                if mode == "self-review": self.s["reviews"][0]["reviewer_id"] = "worker-A"
                if mode == "missing-verdict": packet["submission"]["verdict"] = None
                seal(self.s); self.blocked()

    def test_guard_binds_every_new_source_context_and_time_input(self):
        runtime_foreign(self.case); runtime_context(self.case); action = self.allowed()
        target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
        self.assertEqual(co.revalidate(self.s, action, target, NOW)["status"], "GO")
        for mutate in (lambda s: s["scoped_source"]["candidate"]["target"].update(ref="refs/heads/new"),
                       lambda s: s["scoped_source"]["context_assessments"].clear(),
                       lambda s: s["requests"][0].update(evidence="changed request"),
                       lambda s: s["scoped_source"]["related_task_ids"].append("other")):
            s = deepcopy(self.s); mutate(s); seal(s)
            self.assertNotEqual(co.revalidate(s, action, target, NOW)["status"], "GO")
        self.assertNotEqual(co.revalidate(self.s, action, target, NOW + timedelta(minutes=15))["status"], "GO")

    def test_v2_actual_supported_cli_and_imported_aliases_no_io(self):
        runtime_foreign(self.case); runtime_context(self.case); action = self.allowed()
        args = ["--snapshot", "snapshot.json"]
        guard = args + ["--decision", "decision.json", "--task", "ops-docs", "--operation", "merge", "--executor", "native", "--owner", "coordinator-A", "--head", self.case["source"]]
        original = deepcopy(self.s)
        def load(path): return deepcopy(action if path == "decision.json" else self.s)
        with patch.object(cli, "_load", side_effect=load), patch.object(cli, "datetime") as clock, \
             patch("builtins.open", side_effect=AssertionError("unexpected file access")), \
             patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
             patch.object(subprocess, "run", side_effect=AssertionError("dispatch forbidden")):
            clock.now.return_value = NOW
            for alias in cli.ALIASES:
                for imported in (False, True):
                    with self.subTest(alias=alias, imported=imported), contextlib.redirect_stdout(io.StringIO()) as out:
                        try:
                            argv = guard if alias == "dispatch-guard" else args
                            code = (getattr(watch, "cmd_" + alias.replace("-", "_"))(argv) or 0) if imported else cli.run(alias, argv, NOW)
                        except SystemExit as stop: code = stop.code
                        self.assertEqual(json.loads(out.getvalue())["status"], "GO" if alias == "dispatch-guard" else "ACTION_REQUIRED")
                        self.assertEqual(code, 3 if alias == "idle-defect-check" else 0)
        self.assertEqual(self.s, original)

    def test_malformed_v2_never_falls_back_and_v1_no_scope_remain_strict(self):
        self.s["scoped_source"]["composition"]["extra"] = True; self.blocked()
        s = docs_case()["snapshot"]
        s["scoped_source"]["version"] = 2
        self.assertFalse(co.evaluate(s, NOW)["actions"])
        s.pop("scoped_source")
        self.assertFalse(co.evaluate(s, NOW)["actions"])


if __name__ == "__main__":
    unittest.main()
