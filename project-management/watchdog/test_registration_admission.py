"""Offline candidate-specific registration proofs; all collection is SYNTHETIC."""
from copy import deepcopy
from datetime import timedelta
import json
import unittest
from unittest.mock import patch

import coordinator as co
import evidence_policy as ep
import registration_admission as reg
from test_evidence_policy import World, NOW, REPO
import test_scoped_admission as scoped

REQUEST = "request:register-child"


def seal(snapshot, activity=()):
    """Synthetic authenticated collector: complete current catalog, never live proof."""
    scope = snapshot["registration_source"]
    query = reg.inspect_candidate(snapshot)["query"]
    reads = {kind: dict(records=deepcopy(snapshot[kind]), pages_read=1, items_seen=len(snapshot[kind]),
                        exhausted=True, read_status="ok") for kind in reg.READS if kind not in {"catalog", "activity"}}
    for kind, rows in (("activity", list(activity)), ("catalog", [{k: r[k] for k in ("id", "repository", "kind", "head_sha")} for r in activity])):
        reads[kind] = dict(records=deepcopy(rows), pages_read=1, items_seen=len(rows), exhausted=True, read_status="ok")
    scope["collection"] = dict(query=query, reads=reads)
    scope["attestation"] = dict(collector_id="coordinator-A", observed_at=NOW.isoformat(), query_digest=ep.digest(query),
                                records_digest=ep.digest(reads), evidence="SYNTHETIC independent authenticated source response")
    return snapshot


def fixture(markdown=False, future=False):
    w = World()
    parent = dict(id="parent", owner="coordinator-A", status="blocked", assigned_worker=None,
                  dependencies=["dependency"], completion_criteria=[{"check": "Preserve full production criteria"}],
                  ask={"by": "Craig", "scope": "metadata only"}, constraints=["No runtime activation"],
                  evidence=[], verdict=None, work_log=[])
    dependency = dict(parent, id="dependency", dependencies=[], owner="dependency-owner")
    parent_path = "docs/parent.md" if markdown else "docs/parent.json"
    parent_bytes = "# Parent\n\n```json\n" + json.dumps(parent, indent=2) + "\n```\n" if markdown else parent
    w.file(parent_path, parent_bytes); w.file("docs/dependency.json", dependency)
    w.file("board.md", "| Task | Title | Status | Owner |\n|---|---|---|---|\n| parent | Parent | blocked | coordinator-A |\n| dependency | Dependency | blocked | dependency-owner |\n")
    w.file("rules.md", "# Rules\nIndependent document review required.\n")
    journal = dict(version=1, revision=0, history={REPO + ":dependency": dict(prior_attempts=2, state="parked", receipts=["SYNTHETIC exhausted production allocation"])}, events=[])
    w.file("project-management/dispatch/ATTEMPTS.json", journal)
    base = w.commit()
    base_files = deepcopy(w.files)
    template = scoped.docs_case()["snapshot"]["evidence_policy"]["ops-docs"]
    task = ep.GitObjects(template["objects"]).json(template["authority"]["task_ref"])
    task.update(id="registration", parent_task="parent", kind="documentation_acceptance_binding", runtime_allowlist=[],
                dependencies=[], depends_on=[], scope_amendment=dict(source_parent=base, permitted_new_paths=["docs/registration.json", "docs/proof.md"], frozen_reviewed_local_paths=[]))
    task["evidence_rule_inventory"] = [dict(id="R1", repository=REPO, path="rules.md")]
    task["evidence_policy"]["C1"]["source_paths"] = ["docs/proof.md"]
    if markdown:
        task["scope_amendment"]["frozen_reviewed_local_paths"] = [parent_path]
        w.file(parent_path, parent_bytes + "\n## Registration appendix\nPreserve all original production criteria.\n")
    if future:
        task["scope_amendment"]["permitted_new_paths"].append("docs/component.json")
        w.file("docs/component.json", dict(id="component",parent_task="parent",parent_dependency_retained=["dependency"],runtime_allowlist=["src/future.gd"]))
    w.file("docs/registration.json", task); w.file("docs/proof.md", "Exact subordinate document evidence; no runtime implementation.\n")
    source = w.commit(base)
    authority = deepcopy(template["authority"])
    authority.update(rule_heads={REPO: base}, rules=[dict(id="R1", ref=w.ref(base, "rules.md"))],
                     task_ref=w.ref(source, "docs/registration.json"), candidate=dict(repository=REPO, implementation_head=source, artifact_head=source))
    submission = deepcopy(template["submission"])
    submission["acknowledgment"].update(task_id="registration", rules=deepcopy(authority["rules"]))
    submission["plans"]["C1"].update(source_paths=["docs/proof.md"], artifacts=[dict(path="docs/proof.md", type="document")])
    item = submission["evidence"][0]
    item.update(ref=w.ref(source, "docs/proof.md"), source_head=source)
    verdict = dict(task_id="registration", candidate_head=source, actor_id="reviewer-B", authority_digest=ep.acceptance_binding(authority),
                   evidence_digest=ep.digest(submission["evidence"]), performed_at=NOW.isoformat(), criteria={"C1": dict(decision="PASS", rationale="Independent document inspection", citations=[item["ref"]], evidence_ids=[item["id"]])})
    w.file("docs/review.json", verdict)
    head = w.commit(source)
    authority["candidate"]["artifact_head"] = head
    submission["verdict"] = w.ref(head, "docs/review.json")
    authority["attestations"] = [dict(kind="review", ref=submission["verdict"], actor_id="reviewer-B", observed_at=NOW.isoformat(), provenance="SYNTHETIC authenticated independent review")]
    result = ep.evaluate_completion(authority, submission, w.objects, NOW)
    assert result["status"] == "ACCEPTABLE", result
    s = dict(version=1, observed_at=NOW.isoformat(), repositories={REPO: base}, sources=[], **{k: [] for k in co.TABLES})
    s["policies"] = [dict(id="source-policy", repository=REPO, triggers_checked=True, push_runs_actions=False, push_deploys=False, merge_runs_actions=False, merge_deploys=False)]
    for doc in (parent, dependency):
        t = dict(id=doc["id"], repository=REPO, head_sha=base, status=doc["status"], owner_id=doc["owner"],
                 project="lower-city", author_id=doc["owner"], needs=[], criteria=["production"], required_checks=["independent"], requirements={})
        s["tasks"].append(t); s["board"].append({k: t[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
    s["requests"] = [dict(id="register-child", repository=REPO, task_id=None, project="lower-city", operations=["admission"], executors=["native"], kind="ask", state="active", authority_verified=True, evidence="SYNTHETIC Craig registration request")]
    s["executors"] = [dict(id="native", repository=REPO, owner_id="coordinator-A", kind="native", state="available", capabilities=["admission"], observed_model=None, observed_effort=None, runtime_confirmed=False, resume_task=REQUEST)]
    s["evidence_policy"] = {"registration": dict(authority=authority, submission=submission, objects=w.objects)}
    s["registration_source"] = dict(version=1, binding=dict(task_id=REQUEST, repository=REPO, operation="admission", executor_id="native", owner_id="coordinator-A", head_sha=base),
        document_id="registration", parent_ref=w.ref(base,parent_path), dependency_refs=[w.ref(base,"docs/dependency.json")], board_ref=w.ref(base,"board.md"),
        journal_ref=w.ref(base,"project-management/dispatch/ATTEMPTS.json"), collection={}, attestation={}, coexistence=[],
        allocation=dict(request_id=REQUEST, operation="admission", limit=1, used=0, evidence="SYNTHETIC known unused single metadata-registration allocation; production budget untouched"))
    w.base_files = base_files
    return w, seal(s)


def activity(kind="pr", state="open", path="docs/parent.json", task_ids=None):
    return dict(id="foreign-source", repository=REPO, kind=kind, state=state, head_sha="f" * 40 if kind in {"pr", "branch"} else None,
                task_ids=task_ids if task_ids is not None else [], regions=[dict(repository=REPO,path=path,row_keys=[])], owner_id="foreign-owner")


def coexistence(snapshot, row, source_base):
    inspected = reg.inspect_candidate(snapshot)
    return dict(source_digest=ep.digest(row),query_digest=ep.digest(inspected["query"]),
        candidate_head=inspected["query"]["candidate"]["artifact_head"],source_base=source_base,
        owner_id="coordinator-A",approved_by="coordinator-A",observed_at=NOW.isoformat(),
        owner_evidence="SYNTHETIC authenticated lane owner",approval_evidence="SYNTHETIC explicit serialized document coexistence approval")


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.w, self.s = fixture()
        self.network = patch("socket.socket", side_effect=AssertionError("offline test attempted network"))
        self.network.start(); self.addCleanup(self.network.stop)

    def result(self, snapshot=None, at=NOW):
        s = self.s if snapshot is None else snapshot
        before = deepcopy(s)
        result = co.evaluate(s, at)
        self.assertEqual(s, before)
        return result

    def assert_blocked(self, s=None, at=NOW):
        r = self.result(s, at)
        self.assertFalse(r["actions"], r)
        self.assertNotEqual(r["status"], "IDLE", r)
        return r

    def test_unfiled_registration_ignores_659_unassigned_historical_rows_only(self):
        self.s["branches"] = [dict(id=f"historical-{i}", repository=REPO, task_id=None, head_sha="e" * 40) for i in range(659)]
        r = self.result()
        self.assertEqual([(a["task_id"],a["operation"]) for a in r["actions"]], [(REQUEST,"admission")], r)
        self.assertEqual(r["source_scope"]["global_coverage"], "unknown")
        self.assertEqual(self.s["sources"], [])
        self.assertEqual(len([w for w in r["warnings"] if 'branch not reconciled' in w]), 659)
        self.assertEqual(self.s["tasks"][0]["status"],"blocked")

    def test_current_disjoint_sources_need_no_task_mapping(self):
        seal(self.s, [activity(path="unrelated/art.png"), activity(kind="branch",state="active",path="unrelated/code.gd") | {"id":"unpublished-other"}])
        self.assertEqual(self.result()["status"],"ACTION_REQUIRED")

    def test_relevant_overlap_unknown_scope_and_liveness_hold(self):
        for kind,state in (("pr","open"),("branch","active"),("branch","unknown"),("session","live"),("session","unknown"),("reservation","pending")):
            with self.subTest(kind=kind,state=state):
                seal(self.s,[activity(kind=kind,state=state)])
                self.assertIn("overlap retained",str(self.assert_blocked()))
        row=activity(path="unrelated/file");row["regions"]=None
        seal(self.s,[row]);self.assertIn("unknown live/source scope",str(self.assert_blocked()))

    def test_omitted_matching_source_not_caller_shortlist_completeness(self):
        seal(self.s,[activity()])
        reads=self.s["registration_source"]["collection"]["reads"]
        reads["activity"]["records"]=[];reads["activity"]["items_seen"]=0
        self.assertIn("changed/shortened",str(self.assert_blocked()))
        # Even an independently refreshed response cannot omit a retained catalog item.
        self.s["registration_source"]["attestation"]["records_digest"]=ep.digest(reads)
        self.assertIn("omitted/changed current source",str(self.assert_blocked()))
        s=deepcopy(self.s)
        s["prs"]=[dict(id=REPO+"#7",repository=REPO,task_id="parent",head_sha="d"*40,
                       author_id="foreign-owner",state="open",review_ids=[],check_ids=[])]
        seal(s,[])
        self.assertIn("known open PR omitted/changed",str(self.assert_blocked(s)))
        seal(s,[activity() | dict(id=REPO+"#7",head_sha="f"*40)])
        self.assertIn("known open PR omitted/changed",str(self.assert_blocked(s)))

    def test_query_cannot_drop_parent_dependency_global_stop_or_unpublished_scope(self):
        for key in ("task_ids","regions","include_global_stops","include_unpublished","include_unknown"):
            s=deepcopy(self.s);q=s["registration_source"]["collection"]["query"]
            q[key]=[] if isinstance(q[key],list) else False
            s["registration_source"]["attestation"]["query_digest"]=ep.digest(q)
            self.assertIn("query changed or narrowed",str(self.assert_blocked(s)))

    def test_global_stop_denial_owner_and_reservation_are_not_historical_exclusions(self):
        for kind in ("stop","denial","security"):
            s=deepcopy(self.s);s["blockers"]=[dict(id="hold",repository=REPO,task_id="*",operations=["admission"],executors=["*"],kind=kind,reason="Craig restriction")]
            seal(s);self.assertIn("hold retained",str(self.assert_blocked(s)))
        s=deepcopy(self.s);s["owners"]=[dict(id="owner",repository=REPO,task_id="parent",operation="implementation",owner_id="coordinator-A",executor_id="native",state="unknown")]
        seal(s);self.assertIn("owner retained",str(self.assert_blocked(s)))
        s=deepcopy(self.s);s["queue"]=[dict(id="q",repository=REPO,task_id=REQUEST,operation="admission",owner_id="coordinator-A",executor_id="native",head_sha=s["repositories"][REPO],state="pending")]
        seal(s);self.assertIn("queued/reserved",str(self.assert_blocked(s)))

    def test_dependency_parent_and_candidate_identity_preserved(self):
        for mutate in (lambda s:s["registration_source"].update(dependency_refs=[]),
                       lambda s:s["tasks"][0].update(owner_id="Muse"),
                       lambda s:s["board"][0].update(status="validated"),
                       lambda s:s["registration_source"].update(parent_ref=s["registration_source"]["dependency_refs"][0])):
            s=deepcopy(self.s);mutate(s);self.assert_blocked(s)

    def test_finite_allocation_and_stale_mutated_receipt_fail_closed(self):
        for used in (None,1,2,-1):
            s=deepcopy(self.s);s["registration_source"]["allocation"]["used"]=used
            seal(s);self.assertIn("allocation required",str(self.assert_blocked(s)))
        self.assertIn("stale/future",str(self.assert_blocked(at=NOW+timedelta(minutes=15))))
        s=deepcopy(self.s);s["requests"][0]["evidence"]="changed request"
        self.assertIn("omitted/changed relevant",str(self.assert_blocked(s)))

    def test_existing_row_and_existing_task_collisions(self):
        s=deepcopy(self.s);s["tasks"].append(dict(s["tasks"][0],id="registration"));s["board"].append(dict(s["board"][0],id="registration"))
        self.assertIn("collision",str(self.assert_blocked(s)))
        s=deepcopy(self.s);s["registration_source"]["document_id"]="parent"
        self.assert_blocked(s)

    def test_independent_acceptance_and_source_triggers_stay_required(self):
        s=deepcopy(self.s);s["evidence_policy"]["registration"]["authority"]["attestations"]=[]
        self.assertIn("independent documentary acceptance",str(self.assert_blocked(s)))
        s=deepcopy(self.s);s["policies"][0]["push_runs_actions"]=True;seal(s)
        self.assertIn("trigger/publication hold",str(self.assert_blocked(s)))

    def test_registration_decision_replay_changed_allocation_head_or_expiry_is_no_go(self):
        r=self.result();self.assertTrue(r["actions"],r)
        decision=r["actions"][0]
        target={k:decision[k] for k in ("task_id","operation","executor_id","owner_id","head_sha")}
        self.assertEqual(co.revalidate(self.s,decision,target,NOW)["status"],"GO")
        s=deepcopy(self.s);s["registration_source"]["allocation"]["used"]=1;seal(s)
        self.assertEqual(co.revalidate(s,decision,target,NOW)["status"],"NO_GO")
        self.assertEqual(co.revalidate(self.s,decision,target,NOW+timedelta(minutes=15))["status"],"NO_GO")
        target["operation"]="implementation"
        self.assertEqual(co.revalidate(self.s,decision,target,NOW)["status"],"NO_GO")

    def test_exact_same_owner_disjoint_appendix_coexistence(self):
        w,s=fixture(markdown=True)
        w.files=deepcopy(w.base_files)
        base=s["repositories"][REPO]
        raw=ep.GitObjects(w.objects).citation(s["registration_source"]["parent_ref"]).decode()
        w.file("docs/parent.md",raw.replace("# Parent", "# Parent direction correction"))
        head=w.commit(base)
        row=activity(path="docs/parent.md",task_ids=["parent"]) | dict(head_sha=head,owner_id="coordinator-A")
        seal(s,[row]);self.assertIn("overlap retained",str(self.assert_blocked(s)))
        s["registration_source"]["coexistence"]=[coexistence(s,row,base)]
        self.assertEqual(self.result(s)["status"],"ACTION_REQUIRED")
        for field,value in (("owner_id","Muse"),("approved_by","Muse"),("candidate_head","f"*40),("source_digest","stale"),("observed_at",(NOW-timedelta(minutes=15)).isoformat())):
            changed=deepcopy(s);changed["registration_source"]["coexistence"][0][field]=value
            self.assert_blocked(changed)
        # An approval for the PR never releases a separate uncertain session.
        seal(s,[row,activity(kind="session",state="unknown",path="docs/parent.md")])
        self.assertIn("overlap retained",str(self.assert_blocked(s)))

    def test_coexistence_cannot_hide_append_boundary_changed_criteria_or_extra_write(self):
        for variant in ("append", "criteria", "omitted", "future"):
            with self.subTest(variant=variant):
                w,s=fixture(markdown=True,future=True);w.files=deepcopy(w.base_files);base=s["repositories"][REPO]
                raw=ep.GitObjects(w.objects).citation(s["registration_source"]["parent_ref"]).decode()
                if variant=="append":raw+="\nConflicting appendix\n"
                elif variant=="criteria":raw=raw.replace("Preserve full production criteria","Weaken production criteria")
                else:raw=raw.replace("# Parent", "# Corrected parent")
                w.file("docs/parent.md",raw)
                if variant in {"omitted","future"}:w.file("src/future.gd","Actual conflicting future source\n")
                row=activity(path="docs/parent.md",task_ids=["parent"]) | dict(head_sha=w.commit(base),owner_id="coordinator-A")
                if variant=="future":row["regions"].append(dict(repository=REPO,path="src/future.gd",row_keys=[]))
                seal(s,[row]);s["registration_source"]["coexistence"]=[coexistence(s,row,base)]
                self.assert_blocked(s)

    def test_future_source_paths_and_dependency_stops_cannot_be_omitted(self):
        _,s=fixture(future=True)
        seal(s,[activity(path="src/future.gd")]);self.assertIn("overlap retained",str(self.assert_blocked(s)))
        _,s=fixture()
        stop=dict(s["requests"][0],id="dependency-stop",task_id="dependency",state="cancelled")
        s["requests"].append(stop);seal(s)
        self.assertIn("dependency user stop",str(self.assert_blocked(s)))

    def test_missing_canonical_rows_unknown_empty_scope_and_bad_states_fail_closed(self):
        s=deepcopy(self.s);s["board"]=[];self.assert_blocked(s)
        for change in (dict(regions=[],task_ids=[]),dict(state="probably_idle"),dict(regions=[dict(repository="wrong/repo",path="safe",row_keys=[])])):
            s=deepcopy(self.s);seal(s,[activity(path="unrelated/file") | change]);self.assert_blocked(s)

    def test_source_parent_difference_is_not_an_unrelated_candidate_deletion(self):
        w,s=fixture();scope=s["registration_source"];base=s["repositories"][REPO]
        w.files=deepcopy(w.base_files);w.file("docs/unrelated.json",dict(id="unrelated"));current=w.commit(base)
        s["repositories"][REPO]=current;scope["binding"]["head_sha"]=current
        for ref in [scope["parent_ref"],*scope["dependency_refs"],scope["board_ref"],scope["journal_ref"]]:ref["commit"]=current
        for row in s["tasks"]+s["board"]:row["head_sha"]=current
        proof=reg.inspect_candidate(s)
        self.assertEqual(proof["canonical_disjoint_changes"],["docs/unrelated.json"])
        self.assertNotIn("docs/unrelated.json",proof["write_paths"])
        w.file("docs/proof.md","New canonical collision\n");collision=w.commit(current)
        s["repositories"][REPO]=collision;scope["binding"]["head_sha"]=collision
        for ref in [scope["parent_ref"],*scope["dependency_refs"],scope["board_ref"],scope["journal_ref"]]:ref["commit"]=collision
        for row in s["tasks"]+s["board"]:row["head_sha"]=collision
        self.assertIn("canonical changes overlap",str(self.assert_blocked(s)))

    def test_pending_document_worker_requires_exact_current_ended_session(self):
        w,s=fixture(markdown=True);w.files=deepcopy(w.base_files);base=s["repositories"][REPO]
        raw=ep.GitObjects(w.objects).citation(s["registration_source"]["parent_ref"]).decode()
        w.file("docs/parent.md",raw.replace('"assigned_worker": null','"assigned_worker": "old-worker"'))
        row=activity(path="docs/parent.md",task_ids=["parent"]) | dict(head_sha=w.commit(base),owner_id="coordinator-A")
        seal(s,[row]);s["registration_source"]["coexistence"]=[coexistence(s,row,base)]
        self.assertIn("needs current ended receipt",str(self.assert_blocked(s)))
        for state,owner in (("unknown","coordinator-A"),("live","coordinator-A"),("ended","foreign-owner")):
            seal(s,[row,activity(kind="session",state=state,path="docs/parent.md") | dict(id="old-worker",owner_id=owner)])
            self.assert_blocked(s)
        seal(s,[row,activity(kind="session",state="ended",path="docs/parent.md") | dict(id="old-worker",owner_id="coordinator-A")])
        self.assertEqual(self.result(s)["status"],"ACTION_REQUIRED")

    def test_frozen_projects_and_wrong_route_never_admit(self):
        for project in ("shuto", "neon-drift"):
            s=deepcopy(self.s);s["requests"][0]["project"]=project;seal(s)
            self.assertIn("PROJECT_FROZEN",str(self.assert_blocked(s)))
        for operation in ("implementation","upload","merge","deploy"):
            s=deepcopy(self.s);s["registration_source"]["binding"]["operation"]=operation
            self.assert_blocked(s)


if __name__ == "__main__":
    unittest.main()
