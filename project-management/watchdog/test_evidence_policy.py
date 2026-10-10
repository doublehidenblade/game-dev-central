"""Offline adversarial evidence-policy tests. Fixtures use real Git object hashes."""
import base64
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import unittest
from unittest.mock import patch

import evidence_policy as ep

NOW = datetime(2026, 10, 9, 14, 0, tzinfo=timezone.utc)
STAMP = "2026-10-09T14:00:00Z"
REPO = "example/evidence-policy"


class World:
    def __init__(self):
        self.objects = {REPO: {}}
        self.files = {}

    def object(self, kind, content):
        raw = content.encode() if isinstance(content, str) else content
        oid = hashlib.sha1(kind.encode() + b" " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.objects[REPO][oid] = {"type": kind, "base64": base64.b64encode(raw).decode()}
        return oid

    def file(self, path, content):
        raw = json.dumps(content, sort_keys=True).encode() if isinstance(content, (dict, list)) else content
        self.files[path] = self.object("blob", raw)
        return self.files[path]

    def commit(self, parent=None):
        nested = {}
        for path, oid in self.files.items():
            cursor = nested
            parts = path.split("/")
            for part in parts[:-1]:
                cursor = cursor.setdefault(part, {})
            cursor[parts[-1]] = oid
        def tree(entries):
            raw = b""
            for name, value in sorted(entries.items(), key=lambda kv: kv[0] + ("/" if isinstance(kv[1], dict) else "")):
                mode, oid = ("40000", tree(value)) if isinstance(value, dict) else ("100644", value)
                raw += f"{mode} {name}".encode() + b"\0" + bytes.fromhex(oid)
            return self.object("tree", raw)
        body = f"tree {tree(nested)}\n" + (f"parent {parent}\n" if parent else "")
        body += "author Fixture <fixture@example.invalid> 1791554400 +0000\ncommitter Fixture <fixture@example.invalid> 1791554400 +0000\n\nOffline test fixture\n"
        return self.object("commit", body)

    def ref(self, head, path):
        store = ep.GitObjects(self.objects)
        return {"repository": REPO, "commit": head, "path": path, "blob": store.blob_at(REPO, head, path)}


def make_case(visual=False, task_transform=None, historical=False):
    w = World()
    checks = [] if visual else [{"id": "unit", "command": ["python3", "test_source.py"]}]
    task = {"id": "ops-example", "completion_criteria": [{"id": "C1", "criterion": "Fix every mapped instance", "verification": "Inspect original exact-head evidence"}],
            "evidence_policy": {"C1": {"applicability": "required", "rationale": "Canonical task requires this criterion", "rule_id": "R1", "instances": ["instance-A"],
                        "source_paths": ["src/source.py"], "build": {"id": "test-build", "variant": "test", "environment": "python-3.12"}, "visual": visual, "checks": checks}}}
    task["evidence_rule_inventory"] = [{"id": "R1", "repository": REPO, "path": "rules.md"}]
    if task_transform:
        task_transform(task)
    w.file("task.json", task)
    w.file("rules.md", "# R1\nEvery applicable criterion needs independent inspection.\n")
    w.file("src/source.py", "assert True\n")
    w.file("broken.json", {"defect": "missing evidence", "code": "MISSING_EVIDENCE"})
    source = w.commit()
    task_ref, rule_ref = w.ref(source, "task.json"), w.ref(source, "rules.md")
    policy = task["evidence_policy"].get("C1", {})
    build = policy.get("build")
    execution = {"check_id": "unit", "command": ["python3", "test_source.py"], "exit_code": 0, "output": "1 test passed; asserted mapped instance-A invariant", "source_head": source,
                 "build": build, "performed_at": STAMP, "actor_id": "test-observer"}
    if visual:
        w.file("qa/before.png", b"\x89PNG\r\n\x1a\nfixture-before-pixels")
        w.file("qa/after.png", b"\x89PNG\r\n\x1a\nfixture-after-pixels")
    else:
        w.file("qa/test.json", execution)
    artifact = w.commit(source)
    paths = ["qa/before.png", "qa/after.png"] if visual else ["qa/test.json"]
    evidence = []
    for i, path in enumerate(paths):
        item = {"id": "E" + str(i), "criterion_id": "C1", "instances": ["instance-A"], "type": "image" if visual else "log", "ref": w.ref(artifact, path),
                "source_head": source, "build": build, "performed_at": STAMP, "check_id": None if visual else "unit"}
        if visual:
            item["pair"] = {"role": "before" if i == 0 else "after", "camera": "locked-camera-instance-A"}
        evidence.append(item)
    candidate = source
    if historical:
        w.file("unrelated.txt", "new text outside relevant scope\n")
        candidate = w.commit(artifact)
        artifact = candidate
    authority = {"version": 1, "observed_at": STAMP, "rule_heads": {REPO: source}, "rules": [{"id": "R1", "ref": rule_ref}], "task_ref": task_ref,
                 "candidate": {"repository": REPO, "implementation_head": candidate, "artifact_head": artifact},
                 "principals": {"author": "worker-A", "coordinator": "coordinator-A", "reviewer": "reviewer-B", "human": "Craig" if visual else None},
                 "owner_id": "worker-A", "status": "in_review", "stopped": False, "exclusions": {}, "attestations": [], "findings": [], "decisions": []}
    submission = {"acknowledgment": {"task_id": task["id"], "author_id": "worker-A", "rules": deepcopy(authority["rules"])},
                  "plans": {"C1": {"method": "Run exact local assertion and inspect result" if not visual else "Direct matched per-instance before/after pixel review plus Craig's phone judgment",
                             "artifacts": [({"path": path, "type": "image", "instances": ["instance-A"], "pair": {"role": "before" if i == 0 else "after", "camera": "locked-camera-instance-A"}} if visual else
                                            {"path": path, "type": "log", "check_id": "unit"}) for i, path in enumerate(paths)],
                             "source_paths": ["src/source.py"], "build": build, "coverage": ["instance-A"], "reviewer_id": "reviewer-B"}},
                  "evidence": evidence}
    case = {"world": w, "authority": authority, "submission": submission, "source": source, "task": task, "execution": execution}
    if not visual:
        attest(case, "execution", evidence[0]["ref"], "test-observer")
    else:
        for item in evidence:
            attest(case, "capture", item["ref"], "capture-observer")
            authority["attestations"][-1]["binding"] = deepcopy({k: item[k] for k in ("source_head", "build", "performed_at", "criterion_id", "instances")})
    install_verdict(case, "review")
    if visual:
        install_verdict(case, "human")
    return case


def attest(case, kind, ref, actor):
    case["authority"]["attestations"].append({"kind": kind, "ref": deepcopy(ref), "actor_id": actor, "observed_at": STAMP,
                                            "provenance": "Authenticated test collector record; synthetic fixture identity"})


def make_verdict(case, kind):
    a, s = case["authority"], case["submission"]
    criteria = {}
    for cid, p in case["task"]["evidence_policy"].items():
        if p["applicability"] != "required" or kind == "human" and not p["visual"]:
            continue
        items = [e for e in s["evidence"] if e["criterion_id"] == cid]
        decision = {"decision": "PASS", "rationale": "Original evidence inspected and mapped instance checked", "citations": [e["ref"] for e in items], "evidence_ids": [e["id"] for e in items]}
        if p["visual"]:
            decision["visual_inspection"] = {"method": "human_device" if kind == "human" else "direct_pixel_inspection", "matched_pairs": True, "nonempty": True, "meaningful": True, "after_resolves_defect": True}
        criteria[cid] = decision
    return {"task_id": case["task"]["id"], "candidate_head": a["candidate"]["implementation_head"], "actor_id": a["principals"]["reviewer" if kind == "review" else "human"],
            "authority_digest": ep.acceptance_binding(a), "evidence_digest": ep.digest(s["evidence"]), "performed_at": STAMP, "criteria": criteria}


def install_verdict(case, kind, transform=None):
    w, a, s = case["world"], case["authority"], case["submission"]
    verdict = make_verdict(case, kind)
    if transform:
        transform(verdict)
    path = f"qa/{kind}-verdict.json"
    w.file(path, verdict)
    head = w.commit(a["candidate"]["artifact_head"])
    ref = w.ref(head, path)
    a["candidate"]["artifact_head"] = head
    s["verdict" if kind == "review" else "human_verdict"] = ref
    attest(case, kind, ref, verdict["actor_id"])
    return verdict


def replace_execution(case, transform):
    w, a, s = case["world"], case["authority"], case["submission"]
    log = deepcopy(case["execution"])
    transform(log)
    w.file("qa/test.json", log)
    head = w.commit(a["candidate"]["artifact_head"])
    a["candidate"]["artifact_head"] = head
    s["evidence"][0]["ref"] = w.ref(head, "qa/test.json")
    attest(case, "execution", s["evidence"][0]["ref"], log.get("actor_id", "test-observer"))
    install_verdict(case, "review")


def finding(case, fid="F1"):
    f = {"id": fid, "repository": REPO, "head": case["source"], "observed_at": STAMP, "task_id": "ops-example", "criterion_id": "C1", "evidence": [case["world"].ref(case["source"], "broken.json")],
         "code": "MISSING_EVIDENCE", "coverage": ["instance-A"], "limitations": []}
    f["fingerprint"] = ep.finding_fingerprint(f)
    return f


def decision(case, kind="existing_rule", transform=None, filename="decision.json"):
    a, w = case["authority"], case["world"]
    f = a["findings"][0]
    detail = {"rule_id": "R1", "rule_ref": a["rules"][0]["ref"]} if kind == "existing_rule" else {
        "task_id": "ops-example", "criterion_ids": ["C1"], "instances": ["instance-A"], "required_action": "Inspect the missing artifact", "required_evidence": "Committed exact-head log", "blocks": ["completion"]}
    d = {"id": "D1", "actor_id": "coordinator-A", "finding_ids": [f["id"]], "fingerprints": [f["fingerprint"]], "kind": kind,
         "rationale": "The recorded failure is already covered by the current rule", "citations": f["evidence"], "detail": detail}
    if transform:
        transform(d)
    w.file(filename, d)
    head = w.commit(a["candidate"]["artifact_head"])
    ref = w.ref(head, filename)
    a["candidate"]["artifact_head"] = head
    a["decisions"].append(ref)
    attest(case, "decision", ref, d["actor_id"])
    return d


class EvidencePolicyTests(unittest.TestCase):
    def result(self, c, operation="completion"):
        fn = ep.evaluate_admission if operation == "admission" else ep.evaluate_completion
        return fn(c["authority"], c["submission"], c["world"].objects, NOW)

    def denied(self, c, operation="completion", code=None):
        result = self.result(c, operation)
        self.assertNotIn(result["status"], {"ACCEPTABLE", "ADMISSIBLE"}, result)
        self.assertEqual(result["mutations"], [])
        if code:
            self.assertEqual(result["issues"][0]["code"], code, result)
        return result

    def test_positive_exact_source_and_evidence_only_descendants(self):
        c = make_case()
        self.assertNotEqual(c["authority"]["candidate"]["artifact_head"], c["source"])
        self.assertEqual(self.result(c, "admission")["status"], "ADMISSIBLE")
        result = self.result(c)
        self.assertEqual(result["status"], "ACCEPTABLE", result)
        self.assertEqual(result["gates"], {"author": "PASS", "test_evidence": "BOUND", "independent_review": "PASS", "human_visual": "NOT_APPLICABLE"})

    def test_historical_evidence_with_actual_scope_equivalence(self):
        c = make_case(historical=True)
        self.assertNotEqual(c["submission"]["evidence"][0]["source_head"], c["authority"]["candidate"]["implementation_head"])
        self.assertEqual(self.result(c)["status"], "ACCEPTABLE")

    def test_rules_inventory_and_revision_negatives(self):
        mutations = [lambda c: c["authority"].update(rules=[]),
                     lambda c: c["authority"]["rule_heads"].update({REPO: "a" * 40}),
                     lambda c: c["submission"]["acknowledgment"].update(rules=[]),
                     lambda c: c["submission"]["acknowledgment"]["rules"][0]["ref"].update(blob="f" * 40),
                     lambda c: c["authority"]["rules"][0]["ref"].update(commit="main"),
                     lambda c: c["authority"].update(observed_at="2026-10-09T13:00:00Z"),
                     lambda c: c["submission"].pop("acknowledgment")]
        for i, mutate in enumerate(mutations):
            with self.subTest(i=i):
                c = make_case(); mutate(c); self.denied(c, "admission")

    def test_worker_cannot_narrow_authoritative_rules(self):
        c = make_case()
        c["authority"]["rules"].append({"id": "R2", "ref": deepcopy(c["authority"]["rules"][0]["ref"])})
        self.denied(c, "admission", "UNKNOWN_RULES")

    def test_plan_negatives(self):
        changes = [lambda c: c["submission"].update(plans={}),
                   lambda c: c["submission"]["plans"]["C1"].update(method=" "),
                   lambda c: c["submission"]["plans"]["C1"].update(artifacts=[]),
                   lambda c: c["submission"]["plans"]["C1"].update(source_paths=[]),
                   lambda c: c["submission"]["plans"]["C1"].update(coverage=[]),
                   lambda c: c["submission"]["plans"]["C1"].update(build={"id": "other"}),
                   lambda c: c["submission"]["plans"]["C1"].update(reviewer_id="worker-A"),
                   lambda c: c["submission"]["plans"]["C1"].update(extra="ignored?"),
                   lambda c: c["submission"]["plans"]["C1"].update(artifacts=[{"path": "../local.log", "type": "log"}])]
        for i, mutate in enumerate(changes):
            with self.subTest(i=i):
                c = make_case(); mutate(c); self.denied(c, "admission")

    def test_empty_criteria_and_applicability_never_pass(self):
        changes = [lambda t: t.update(completion_criteria=[]),
                   lambda t: t.update(evidence_policy={}),
                   lambda t: t["evidence_policy"]["C1"].update(rationale=""),
                   lambda t: t["evidence_policy"]["C1"].update(applicability="not_applicable"),
                   lambda t: t["evidence_policy"]["C1"].update(instances=[]),
                   lambda t: t["evidence_policy"]["C1"].update(rule_id="unknown")]
        for i, transform in enumerate(changes):
            with self.subTest(i=i):
                c = make_case(task_transform=transform)
                self.denied(c, "admission")

    def test_no_publication_hold_dependency(self):
        c = make_case()
        # Authority has no publication channel. An unrelated deploy hold must
        # stay in the coordinator's operation-specific decision layer.
        self.assertEqual(self.result(c, "admission")["status"], "ADMISSIBLE")
        c["authority"]["findings"] = [finding(c)]
        decision(c, "task_limitation")
        self.assertEqual(self.result(c, "admission")["status"], "ADMISSIBLE")
        self.denied(c, code="TASK_LIMITATION")

    def test_missing_evidence_and_partial_coverage(self):
        for mutate in [lambda c: c["submission"].update(evidence=[]),
                       lambda c: c["submission"]["evidence"][0].update(criterion_id="C9"),
                       lambda c: c["submission"]["evidence"][0].update(instances=[]),
                       lambda c: c["submission"]["evidence"][0].update(instances=["other"]),
                       lambda c: c["submission"]["plans"]["C1"]["artifacts"].append({"path": "qa/absent.log", "type": "log"})]:
            c = make_case(); mutate(c); self.denied(c)

    def test_raw_commit_tree_blob_proof_not_metadata(self):
        for kind in ("commit", "tree", "blob"):
            with self.subTest(kind=kind):
                c = make_case()
                oid = next(k for k, v in c["world"].objects[REPO].items() if v["type"] == kind)
                c["world"].objects[REPO][oid]["base64"] = base64.b64encode(b"forged").decode()
                self.denied(c)
        c = make_case()
        c["submission"]["evidence"][0]["ref"]["commit"] = "a" * 40
        self.denied(c, code="INACCESSIBLE_OBJECT")

    def test_inaccessible_uncommitted_wrong_blob_path_and_repository(self):
        mutations = [lambda r: r.update(path="qa/local-only.log"), lambda r: r.update(blob="a" * 40),
                     lambda r: r.update(repository="other/repository"), lambda r: r.update(commit="deadbeef"),
                     lambda r: r.update(commit="main"), lambda r: r.update(path="/absolute.png")]
        for mutate in mutations:
            c = make_case(); mutate(c["submission"]["evidence"][0]["ref"]); self.denied(c)

    def test_changed_source_invalidates_evidence_only_claim(self):
        c = make_case(); w = c["world"]; a = c["authority"]
        w.file("src/source.py", "raise RuntimeError('changed source')\n")
        a["candidate"]["artifact_head"] = w.commit(a["candidate"]["artifact_head"])
        self.denied(c, code="SOURCE_CHANGED")

    def test_historical_source_change_is_not_metadata_equivalence(self):
        c = make_case(historical=True); w = c["world"]; a = c["authority"]
        w.file("src/source.py", "new source\n")
        source = w.commit(a["candidate"]["artifact_head"])
        a["candidate"].update(implementation_head=source, artifact_head=source)
        install_verdict(c, "review")
        self.denied(c, code="STALE_EVIDENCE")

    def test_changed_current_canonical_criteria_invalidates_review(self):
        c = make_case(); w = c["world"]; a = c["authority"]
        t = deepcopy(c["task"]); t["completion_criteria"][0]["criterion"] = "Different criterion"
        w.file("task.json", t); a["candidate"]["artifact_head"] = w.commit(a["candidate"]["artifact_head"])
        self.denied(c, code="TASK_CHANGED")

    def test_evidence_only_task_log_change_is_allowed(self):
        c = make_case(); w = c["world"]; a = c["authority"]
        t = deepcopy(c["task"]); t["work_log"] = ["record evidence; criterion scope unchanged"]
        w.file("task.json", t); a["candidate"]["artifact_head"] = w.commit(a["candidate"]["artifact_head"])
        self.assertEqual(self.result(c)["status"], "ACCEPTABLE")

    def test_evidence_replaced_at_tip_is_not_accepted(self):
        c = make_case(); w = c["world"]; a = c["authority"]
        w.file("qa/test.json", {"claim": "new unreviewed evidence"})
        a["candidate"]["artifact_head"] = w.commit(a["candidate"]["artifact_head"])
        self.denied(c, code="EVIDENCE_CHANGED")

    def test_wrong_build_variant_environment(self):
        for key in ("id", "variant", "environment"):
            c = make_case()
            c["submission"]["evidence"][0]["build"] = {**c["submission"]["evidence"][0]["build"], key: "wrong"}
            self.denied(c, code="BUILD_MISMATCH")

    def test_execution_must_be_real_bound_successful_observation(self):
        mutations = [lambda log: log.update(exit_code=1), lambda log: log.pop("exit_code"),
                     lambda log: log.update(command=["echo", "PASS"]), lambda log: log.update(output=""),
                     lambda log: log.update(source_head="a" * 40), lambda log: log.update(check_id="other"),
                     lambda log: log.update(build={"id": "forged"})]
        for i, mutate in enumerate(mutations):
            with self.subTest(i=i):
                c = make_case(); replace_execution(c, mutate); self.denied(c)

    def test_unattested_execution_is_not_a_claimed_boolean(self):
        c = make_case(); c["authority"]["attestations"] = [r for r in c["authority"]["attestations"] if r["kind"] != "execution"]
        self.denied(c, code="UNATTESTED_ACTOR")

    def test_unmapped_or_missing_required_checks(self):
        c = make_case(); c["submission"]["evidence"][0]["check_id"] = None
        self.denied(c, code="UNPLANNED_EVIDENCE")
        c = make_case(task_transform=lambda t: t["evidence_policy"]["C1"]["checks"].append({"id": "second", "command": ["python3", "other.py"]}))
        self.denied(c, code="INCOMPLETE_PLAN")

    def test_missing_and_unattested_independent_verdict(self):
        c = make_case(); c["submission"].pop("verdict"); self.denied(c, code="MISSING_VERDICT")
        c = make_case(); c["authority"]["attestations"] = [r for r in c["authority"]["attestations"] if r["kind"] != "review"]
        self.denied(c, code="UNATTESTED_ACTOR")

    def test_verdict_negative_table(self):
        mutations = [lambda v: v.update(candidate_head="a" * 40), lambda v: v.update(actor_id="worker-A"),
                     lambda v: v.update(criteria={}), lambda v: v["criteria"]["C1"].update(citations=[]),
                     lambda v: v["criteria"]["C1"].update(evidence_ids=[]), lambda v: v["criteria"]["C1"].update(decision="FAIL"),
                     lambda v: v["criteria"]["C1"].update(decision="PENDING"), lambda v: v.update(authority_digest="old"),
                     lambda v: v.update(evidence_digest="old"), lambda v: v["criteria"]["C1"].update(rationale="")]
        for i, mutate in enumerate(mutations):
            with self.subTest(i=i):
                c = make_case(); install_verdict(c, "review", mutate); self.denied(c)

    def test_conflicting_authenticated_actor_receipts_fail_closed(self):
        c = make_case(); attest(c, "review", c["submission"]["verdict"], "worker-A")
        self.denied(c, code="ACTOR_CONFLICT")

    def test_visual_explicit_independent_and_human_pass(self):
        c = make_case(visual=True)
        self.assertEqual(self.result(c)["status"], "ACCEPTABLE", self.result(c))

    def test_human_missing_pending_rejected_not_inferred_from_green(self):
        c = make_case(visual=True); c["submission"].pop("human_verdict")
        result = self.denied(c, code="HUMAN_PENDING")
        self.assertEqual(result["gates"]["independent_review"], "PASS")
        self.assertEqual(result["gates"]["human_visual"], "PENDING")
        for status in ("PENDING", "FAIL"):
            c = make_case(visual=True); install_verdict(c, "human", lambda v: v["criteria"]["C1"].update(decision=status))
            self.denied(c, code="HUMAN_PENDING")

    def test_numeric_diff_or_ci_is_not_visual_judgment(self):
        for kind in ("review", "human"):
            c = make_case(visual=True)
            install_verdict(c, kind, lambda v: v["criteria"]["C1"]["visual_inspection"].update(method="numeric_diff"))
            self.denied(c, code="VISUAL_JUDGMENT_REQUIRED")

    def test_visual_identical_wrong_empty_or_unmatched_pairs(self):
        for mutate in [lambda c: c["submission"]["evidence"][1]["pair"].update(camera="different"),
                       lambda c: c["submission"]["evidence"][1]["pair"].update(role="before"),
                       lambda c: c["submission"]["evidence"].pop()]:
            c = make_case(visual=True); mutate(c); self.denied(c)
        c = make_case(visual=True)
        install_verdict(c, "review", lambda v: v["criteria"]["C1"]["visual_inspection"].update(after_resolves_defect=False))
        self.denied(c, code="VISUAL_JUDGMENT_REQUIRED")

    def test_stops_and_owner_do_not_change(self):
        for state in ep.STOPPED:
            c = make_case(); c["authority"]["status"] = state
            self.assertEqual(self.denied(c)["status"], "STOPPED")
            self.assertEqual(self.denied(c, "admission")["status"], "STOPPED")
        c = make_case(); c["authority"]["stopped"] = True
        self.denied(c, code="STOPPED")
        c = make_case(); c["authority"]["owner_id"] = "another-live-owner"
        self.denied(c, "admission", "OWNER_CONFLICT")

    def test_reconcile_existing_rule_duplicate_replay_is_idempotent(self):
        c = make_case(); a = c["authority"]; a["findings"] = [finding(c)]
        decision(c)
        r = ep.reconcile_findings(a, c["world"].objects, NOW)
        self.assertEqual(r["status"], "RECORDED", r)
        a["findings"].append(deepcopy(a["findings"][0])); a["decisions"].append(deepcopy(a["decisions"][0]))
        r2 = ep.reconcile_findings(a, c["world"].objects, NOW)
        self.assertEqual(r["reconciliations"], r2["reconciliations"])
        self.assertEqual(r2["mutations"], [])

    def test_reconcile_unresolved_changed_same_id_conflicting_decisions(self):
        c = make_case(); a = c["authority"]; a["findings"] = [finding(c)]
        self.denied(c, "admission", "UNRESOLVED_FINDING")
        decision(c)
        a["findings"].append({**deepcopy(a["findings"][0]), "observed_at": "2026-10-09T13:59:00Z"})
        self.denied(c, "admission", "FINDING_CONFLICT")
        c = make_case(); a = c["authority"]; a["findings"] = [finding(c)]
        decision(c); decision(c, "task_limitation", filename="other-decision.json")
        self.denied(c, "admission", "DECISION_CONFLICT")

    def test_missing_finding_fields_or_fingerprint_fail(self):
        for key in ("id", "head", "coverage", "limitations", "evidence", "criterion_id"):
            c = make_case(); f = finding(c); f.pop(key); c["authority"]["findings"] = [f]
            self.denied(c, "admission")
        c = make_case(); f = finding(c); f["fingerprint"] = "wrong"; c["authority"]["findings"] = [f]
        self.denied(c, "admission", "FINGERPRINT_MISMATCH")

    def test_inspector_cannot_reconcile_or_broaden_limitation(self):
        c = make_case(); c["authority"]["findings"] = [finding(c)]
        decision(c, transform=lambda d: d.update(actor_id="inspector"))
        self.denied(c, "admission", "INSPECTOR_MUTATION")
        c = make_case(); c["authority"]["findings"] = [finding(c)]
        decision(c, "task_limitation", lambda d: d["detail"].update(task_id="all-games"))
        self.denied(c, "admission", "UNBOUNDED_LIMITATION")

    def test_stale_existing_rule_cannot_reconcile(self):
        c = make_case(); c["authority"]["findings"] = [finding(c)]
        decision(c, transform=lambda d: d["detail"].update(rule_ref={**d["detail"]["rule_ref"], "blob": "f" * 40}))
        self.denied(c, "admission", "STALE_RULE")

    def test_unknown_decision_kind_does_not_repair_or_create_tasks(self):
        c = make_case(); c["authority"]["findings"] = [finding(c)]
        decision(c, transform=lambda d: d.update(kind="create_repair_task"))
        self.denied(c, "admission", "UNRESOLVED_FINDING")

    def test_no_io_no_subprocess_no_network_and_no_input_mutation(self):
        c = make_case(); before = ep.digest({"authority": c["authority"], "submission": c["submission"], "objects": c["world"].objects})
        denied = AssertionError("pure evaluator attempted I/O or mutation")
        with patch("builtins.open", side_effect=denied), patch.object(Path, "write_text", side_effect=denied), \
                patch("os.open", side_effect=denied), patch.object(subprocess, "Popen", side_effect=denied), \
                patch.object(subprocess, "run", side_effect=denied), patch.object(socket, "socket", side_effect=denied):
            first = self.result(c)
            second = self.result(c)
            self.assertEqual(first, second)
            self.assertEqual(first["status"], "ACCEPTABLE")
        self.assertEqual(before, ep.digest({"authority": c["authority"], "submission": c["submission"], "objects": c["world"].objects}))

    def test_malformed_input_does_not_throw_or_vacuously_pass(self):
        for value in (None, [], {}, {"version": float("nan")}, "claim PASS"):
            result = ep.evaluate_completion(value, {}, {}, NOW)
            self.assertEqual(result["status"], "INPUT_REQUIRED")
        c = make_case(); c["submission"]["acknowledgment"]["rules"] = [None]
        self.denied(c, "admission")

    def test_fixture_is_reproducible_and_matches_checked_in_bytes(self):
        path = Path(__file__).parent / "fixtures/evidence-policy/positive.json"
        if path.exists():
            packet = json.loads(path.read_text())
            c = make_case()
            self.assertEqual(packet, {"authority": c["authority"], "submission": c["submission"], "objects": c["world"].objects, "evaluated_at": STAMP})
            self.assertEqual(ep.evaluate_completion(packet["authority"], packet["submission"], packet["objects"], NOW)["status"], "ACCEPTABLE")


    def test_canonical_rule_inventory_cannot_be_narrowed_in_both_inputs(self):
        c = make_case(task_transform=lambda t: t["evidence_rule_inventory"].append({"id": "R2", "repository": REPO, "path": "other.md"}))
        self.denied(c, "admission", "UNKNOWN_RULES")

    def test_build_capture_requires_authenticated_exact_binding(self):
        c = make_case(visual=True)
        c["authority"]["attestations"] = [r for r in c["authority"]["attestations"] if r["kind"] != "capture"]
        self.denied(c, code="CAPTURE_UNBOUND")
        c = make_case(visual=True)
        next(r for r in c["authority"]["attestations"] if r["kind"] == "capture")["binding"]["build"]["variant"] = "wrong"
        self.denied(c, code="CAPTURE_UNBOUND")

    def test_execution_cannot_postdate_its_observation(self):
        c = make_case()
        next(r for r in c["authority"]["attestations"] if r["kind"] == "execution")["observed_at"] = "2026-10-09T13:59:00Z"
        self.denied(c, code="STALE_READ")

    def test_reordered_authority_lists_are_deterministic(self):
        c = make_case(visual=True)
        before = self.result(c)
        c["authority"]["attestations"].reverse()
        self.assertEqual(before, self.result(c))


def guideline_case():
    c = make_case(); a, w = c["authority"], c["world"]
    old_rule = deepcopy(a["rules"][0]["ref"])
    w.file("rules.md", "# R1\nRequire source-bound evidence before admission and completion; missing evidence fails.\n")
    w.file("regression.py", "def check(record):\n    assert record.get('evidence'), 'MISSING_EVIDENCE'\n")
    new_rules = w.commit(a["candidate"]["artifact_head"])
    a["candidate"]["artifact_head"] = new_rules
    current = w.ref(new_rules, "rules.md")
    a["rules"] = [{"id": "R1", "ref": current}]; a["rule_heads"][REPO] = new_rules
    c["submission"]["acknowledgment"]["rules"] = deepcopy(a["rules"])
    delta = {"before": old_rule, "after": current, "incident": "Missing artifact was previously claimed complete"}
    w.file("delta.json", delta)
    delta_head = w.commit(new_rules)
    delta_ref = w.ref(delta_head, "delta.json")
    broken_ref = w.ref(c["source"], "broken.json")
    ns = {}; exec(ep.GitObjects(w.objects).citation(w.ref(new_rules, "regression.py")), ns)
    try:
        ns["check"](ep.GitObjects(w.objects).json(broken_ref))
        exit_code, observed = 0, "unexpected PASS"
    except AssertionError as exc:
        exit_code, observed = 1, "AssertionError: " + str(exc)
    log = {"actor_id": "regression-observer", "command": ["python3", "regression.py", "broken.json"], "broken_fixture": broken_ref,
           "assertion": w.ref(new_rules, "regression.py"), "rule_delta": delta_ref, "exit_code": exit_code, "failure_code": "MISSING_EVIDENCE",
           "observed_output": observed, "performed_at": STAMP}
    w.file("regression-log.json", log); log_head = w.commit(delta_head)
    log_ref = w.ref(log_head, "regression-log.json")
    a["candidate"]["artifact_head"] = log_head
    attest(c, "execution", log_ref, "regression-observer")
    a["findings"] = [finding(c)]
    detail = {"incident": delta["incident"], "invariant": "Missing source-bound evidence must fail every admission route", "contexts": ["completion", "admission"],
              "rule_id": "R1", "previous_rule": old_rule, "delta_ref": delta_ref, "regression_ref": log_ref}
    decision(c, transform=lambda d: d.update(kind="reusable_guideline", detail=detail))
    return c


def coordinator_packet(case, state="in_review"):
    """Genuine raw-object proof fixture for production coordinator routes."""
    import coordinator as co
    a = case["authority"]; a["status"] = state
    head = a["candidate"]["artifact_head"]; source = a["candidate"]["implementation_head"]
    task_id = case["task"]["id"]
    snapshot = {"version": 1, "observed_at": STAMP, "repositories": {REPO: head}, "sources": [], **{key: [] for key in co.TABLES}}
    task = {"id": task_id, "repository": REPO, "head_sha": head, "status": state, "owner_id": "worker-A", "project": "example",
            "author_id": "worker-A", "needs": [], "criteria": ["C1"], "required_checks": ["unit"],
            "requirements": {op: {"capabilities": [op], "model": None, "effort": None, "runtime_confirmation_required": False} for op in co.OPERATIONS[1:]}}
    snapshot["tasks"] = [task]; snapshot["board"] = [{key: task[key] for key in ("id", "repository", "head_sha", "status", "owner_id")}]
    snapshot["branches"] = [{"id": "branch", "repository": REPO, "task_id": task_id, "head_sha": head}]
    snapshot["policies"] = [{"id": "policy", "repository": REPO, "triggers_checked": True, "push_runs_actions": False, "push_deploys": False, "merge_runs_actions": False, "merge_deploys": False}]
    snapshot["requests"] = [{"id": "authorized", "repository": REPO, "task_id": task_id, "project": "example", "operations": list(co.OPERATIONS), "executors": ["*"],
                             "kind": "explicit", "state": "active", "authority_verified": True, "evidence": "Synthetic fixture explicit authorization"}]
    snapshot["executors"] = [{"id": "native", "repository": REPO, "owner_id": "worker-A" if state == "in_progress" else "reviewer-B", "kind": "native", "state": "available",
                              "capabilities": list(co.OPERATIONS), "observed_model": None, "observed_effort": None, "runtime_confirmed": False, "resume_task": task_id if state == "in_progress" else None}]
    snapshot["prs"] = [{"id": REPO + "#1", "repository": REPO, "task_id": task_id, "head_sha": head, "author_id": "worker-A", "state": "open", "review_ids": ["review"], "check_ids": ["unit"]}]
    snapshot["reviews"] = [{"id": "review", "repository": REPO, "task_id": task_id, "pr_id": REPO + "#1", "head_sha": source, "observed_at": STAMP,
                            "reviewer_id": "reviewer-B", "verdict": "pass", "criteria": {"C1": {"result": "pass", "evidence": "qa/review-verdict.json"}}}]
    snapshot["checks"] = [{"id": "unit", "repository": REPO, "task_id": task_id, "pr_id": REPO + "#1", "head_sha": source, "observed_at": STAMP, "name": "unit", "result": "pass"}]
    snapshot["evidence_policy"] = {task_id: {"authority": a, "submission": case["submission"], "objects": case["world"].objects}}
    for table in co.TABLES:
        ids = [r["id"] for r in snapshot[table]]
        snapshot["sources"].append({"id": table, "kind": table, "repository": REPO, "source_repository": REPO, "ref_sha": head, "observed_at": STAMP,
                                    "read_status": "ok", "pagination": {"pages_read": 1, "items_seen": len(ids), "exhausted": True}, "ids": ids})
    return snapshot


class EvidenceIntegrationTests(unittest.TestCase):
    result = EvidencePolicyTests.result
    denied = EvidencePolicyTests.denied
    # These tests deliberately do not use the PR396 test-only _policy_gate mock.
    def test_reusable_guideline_executes_failure_and_records_bound_delta(self):
        c = guideline_case()
        r = ep.reconcile_findings(c["authority"], c["world"].objects, NOW)
        self.assertEqual(r["status"], "RECORDED", r)
        self.assertEqual(r["reconciliations"][0]["kind"], "reusable_guideline")
        self.assertEqual(self.result(c, "admission")["status"], "ADMISSIBLE")

    def test_regression_booleans_wrong_fixture_and_unrelated_failure_reject(self):
        for field, value in (("exit_code", 0), ("failure_code", "UNRELATED"), ("observed_output", ""), ("broken_fixture", None)):
            c = guideline_case(); a, w = c["authority"], c["world"]
            dref = a["decisions"][0]; d = ep.GitObjects(w.objects).json(dref)
            log = ep.GitObjects(w.objects).json(d["detail"]["regression_ref"])
            log[field] = value if field != "broken_fixture" else w.ref(c["source"], "rules.md")
            w.file("wrong-regression.json", log); head = w.commit(a["candidate"]["artifact_head"])
            ref = w.ref(head, "wrong-regression.json"); attest(c, "execution", ref, "regression-observer")
            d["detail"]["regression_ref"] = ref
            w.file("wrong-decision.json", d); head = w.commit(head); a["candidate"]["artifact_head"] = head
            ref = w.ref(head, "wrong-decision.json"); a["decisions"] = [ref]; attest(c, "decision", ref, "coordinator-A")
            self.denied(c, "admission")

    def test_same_source_conflicting_verdict_cannot_choose_convenient_pass(self):
        c = make_case(); install_verdict(c, "review", lambda v: v["criteria"]["C1"].update(decision="FAIL"))
        install_verdict(c, "review")
        self.denied(c, code="CONFLICTING_VERDICT")

    def test_all_real_aliases_use_shared_policy_and_exit_nonzero(self):
        import contextlib, io
        import coordinator_cli as cli
        import watch
        c = make_case()
        reads = {"authority.json": json.dumps(c["authority"]), "submission.json": json.dumps(c["submission"]), "objects.json": json.dumps(c["world"].objects)}
        def reader(path, mode="r", **kwargs):
            self.assertEqual(mode, "r"); return io.StringIO(reads[path])
        args = ["--authority", "authority.json", "--submission", "submission.json", "--objects", "objects.json"]
        for command, operation in cli.EVIDENCE_COMMANDS.items():
            for route in ("main", "callable"):
                with self.subTest(command=command, route=route), patch("builtins.open", side_effect=reader), patch.object(cli, "datetime") as clock, \
                        patch("sys.argv", ["watch.py", command] + args), contextlib.redirect_stdout(io.StringIO()) as output:
                    clock.now.return_value = NOW
                    with self.assertRaises(SystemExit) as exit_info:
                        watch.main() if route == "main" else getattr(watch, "cmd_" + command.replace("-", "_"))(args)
                    self.assertEqual(exit_info.exception.code, 0, output.getvalue())
                    self.assertEqual(json.loads(output.getvalue())["operation"], operation)
            for badargs in ([], ["positional-legacy-input"], ["--authority"]):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    code = cli.run_evidence(command, badargs, NOW)
                self.assertEqual(code, 2); self.assertEqual(json.loads(output.getvalue())["status"], "INPUT_REQUIRED")
        c["submission"]["evidence"] = []; reads["submission.json"] = json.dumps(c["submission"])
        for command in ("evidence-check", "evidence-checks", "validator-check", "acceptance-check"):
            with patch("builtins.open", side_effect=reader), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(cli.run_evidence(command, args, NOW), 3)
                self.assertEqual(json.loads(output.getvalue())["issues"][0]["code"], "MISSING_EVIDENCE")

    def test_production_coordinator_and_guard_require_full_policy(self):
        import coordinator as co
        c = make_case(); snapshot = coordinator_packet(c)
        result = co.evaluate(snapshot, NOW)
        self.assertEqual([x["operation"] for x in result["actions"]], ["merge"], result)
        action = result["actions"][0]; target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
        self.assertEqual(co.revalidate(snapshot, action, target, NOW)["status"], "GO")
        # Evidence-only artifact tip can differ from original reviewed source.
        self.assertNotEqual(action["head_sha"], snapshot["reviews"][0]["head_sha"])
        snapshot["evidence_policy"].clear()
        result = co.evaluate(snapshot, NOW)
        self.assertNotIn("merge", [x["operation"] for x in result["actions"]], result)
        self.assertIn("verification", [x["operation"] for x in result["actions"]], result)
        self.assertEqual(co.revalidate(snapshot, action, target, NOW)["status"], "NO_GO")
        self.assertFalse(co.acceptance(snapshot["tasks"][0], snapshot["prs"][0], snapshot, NOW)[0])

    def test_production_admission_no_packet_or_partial_plan_denies(self):
        import coordinator as co
        c = make_case(); snapshot = coordinator_packet(c, "in_progress")
        self.assertIn("implementation", [x["operation"] for x in co.evaluate(snapshot, NOW)["actions"]])
        c["submission"]["plans"] = {}
        result = co.evaluate(snapshot, NOW)
        self.assertFalse(result["actions"], result)
        self.assertEqual(result["status"], "INPUT_REQUIRED")
        snapshot.pop("evidence_policy")
        self.assertFalse(co.evaluate(snapshot, NOW)["actions"])

    def test_production_coordinator_scope_binding_and_stops(self):
        import coordinator as co
        for mutate in [lambda c: c["authority"]["candidate"].update(artifact_head=c["source"]),
                       lambda c: c["authority"].update(stopped=True), lambda c: c["authority"].update(owner_id="other"),
                       lambda c: c["submission"]["evidence"][0]["build"].update(variant="wrong")]:
            c = make_case(); snapshot = coordinator_packet(c); mutate(c)
            result = co.evaluate(snapshot, NOW)
            self.assertNotIn("merge", [x["operation"] for x in result["actions"]], result)
            # The explicit independent read-only route remains available.
            self.assertIn("verification", [x["operation"] for x in result["actions"]], result)

    def test_production_aliases_cannot_reuse_legacy_evidence_strings(self):
        import contextlib, io
        import coordinator_cli as cli
        c = make_case(); snapshot = coordinator_packet(c); snapshot.pop("evidence_policy")
        for command in cli.ALIASES - {"dispatch-guard"}:
            with patch("builtins.open", return_value=io.StringIO(json.dumps(snapshot))), contextlib.redirect_stdout(io.StringIO()) as out:
                cli.run(command, ["--snapshot", "current.json"], NOW)
            result = json.loads(out.getvalue())
            self.assertNotIn("merge", [x["operation"] for x in result["actions"]])
            self.assertIn("verification", [x["operation"] for x in result["actions"]])


    def test_current_failed_check_blocks_with_or_without_finding_or_new_review(self):
        for add_finding in (False, True):
            for refresh_review in (False, True):
                with self.subTest(finding=add_finding, fresh_review=refresh_review):
                    c = make_case(); a, w = c['authority'], c['world']
                    failed = deepcopy(c['execution']); failed.update(exit_code=1, output='FAILED: mapped instance-A invariant broken')
                    w.file('qa/new-failure.json', failed); head = w.commit(a['candidate']['artifact_head'])
                    a['candidate']['artifact_head'] = head; ref = w.ref(head, 'qa/new-failure.json')
                    attest(c, 'execution', ref, 'test-observer')
                    if add_finding:
                        f = {'id': 'F-current-failed-execution', 'repository': REPO, 'head': head, 'observed_at': STAMP,
                             'task_id': 'ops-example', 'criterion_id': 'C1', 'evidence': [ref], 'code': 'FAILED_CHECK', 'coverage': ['instance-A'], 'limitations': []}
                        f['fingerprint'] = ep.finding_fingerprint(f); a['findings'] = [f]
                        decision(c, 'existing_rule')
                    if refresh_review:
                        install_verdict(c, 'review')
                    self.denied(c, code='CURRENT_CHECK_FAILED')

    def test_new_findings_invalidate_old_review_and_need_explicit_inspection(self):
        c = make_case(); c['authority']['findings'] = [finding(c)]; decision(c)
        self.denied(c, code='STALE_VERDICT')
        install_verdict(c, 'review')
        self.denied(c, code='UNREVIEWED_FINDING')
        def inspected(v):
            v['criteria']['C1']['finding_ids'] = ['F1']
            v['criteria']['C1']['citations'] += c['authority']['findings'][0]['evidence']
        install_verdict(c, 'review', inspected)
        self.assertEqual(self.result(c)['status'], 'ACCEPTABLE')

    def test_impossible_admission_plans_are_rejected(self):
        c = make_case(); c['submission']['plans']['C1']['artifacts'][0]['type'] = 'document'
        self.denied(c, 'admission', 'INCOMPLETE_PLAN')
        c = make_case(visual=True); c['submission']['plans']['C1']['artifacts'] = c['submission']['plans']['C1']['artifacts'][:1]
        self.denied(c, 'admission', 'VISUAL_PAIR_REQUIRED')
        c = make_case(visual=True, task_transform=lambda t:t['evidence_policy']['C1'].update(checks=[{'id':'pixel-guard','command':['python3','guard.py']}]))
        self.denied(c, 'admission', 'INCOMPLETE_PLAN')

    def test_visual_images_and_numeric_check_can_complete_together(self):
        c = make_case(visual=True, task_transform=lambda t:t['evidence_policy']['C1'].update(checks=[{'id':'pixel-guard','command':['python3','guard.py']}]))
        a,w,s = c['authority'],c['world'],c['submission']
        log = deepcopy(c['execution']); log.update(check_id='pixel-guard',command=['python3','guard.py'])
        w.file('qa/guard.json',log); head = w.commit(a['candidate']['artifact_head']); a['candidate']['artifact_head'] = head
        ref = w.ref(head,'qa/guard.json');attest(c,'execution',ref,'test-observer')
        s['plans']['C1']['artifacts'].append({'path':'qa/guard.json','type':'log','check_id':'pixel-guard'})
        s['evidence'].append({'id':'E-guard','criterion_id':'C1','instances':['instance-A'],'type':'log','ref':ref,'source_head':c['source'],
                              'build':log['build'],'performed_at':STAMP,'check_id':'pixel-guard'})
        install_verdict(c,'review');install_verdict(c,'human')
        self.assertEqual(self.result(c,'admission')['status'],'ADMISSIBLE')
        self.assertEqual(self.result(c)['status'],'ACCEPTABLE',self.result(c))

    def test_actual_completion_alias_denies_unselected_current_failed_log(self):
        import contextlib,io
        import coordinator_cli as cli
        c=make_case();a,w=c['authority'],c['world'];failed=deepcopy(c['execution']);failed['exit_code']=1
        w.file('qa/unselected-failure.json',failed);head=w.commit(a['candidate']['artifact_head']);a['candidate']['artifact_head']=head
        attest(c,'execution',w.ref(head,'qa/unselected-failure.json'),'test-observer')
        reads={'authority':json.dumps(a),'submission':json.dumps(c['submission']),'objects':json.dumps(w.objects)}
        for command in ('acceptance-check','validator-check','evidence-check','evidence-checks'):
            with patch('builtins.open',side_effect=lambda path,*args,**kwargs:io.StringIO(reads[path])),contextlib.redirect_stdout(io.StringIO()) as out:
                code=cli.run_evidence(command,['--authority','authority','--submission','submission','--objects','objects'],NOW)
            self.assertEqual(code,3);self.assertEqual(json.loads(out.getvalue())['issues'][0]['code'],'CURRENT_CHECK_FAILED')



if __name__ == "__main__":
    unittest.main(verbosity=2)
