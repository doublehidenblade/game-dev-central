"""Read the immutable supplied td201 archive; never refresh its observations.

Usage: python3 replay_td201.py ARCHIVE --central-git EXISTING_CENTRAL_CHECKOUT
Outputs a sanitized source-scope result, not a live admission/launch assertion.
No network, source write, task filing, journal mutation or historical sweep.
"""
import argparse
import base64
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import coordinator as co
import evidence_policy as ep
import registration_admission as reg

ARCHIVE_SHA256 = "35b6a2bde4d1506c0b4de7779d34bb7932959f858a21f326610e9d2f943dff87"
SOURCE = "4c5381ab698a15ebbd947906843ffd311055d87f"
TOKYO = "doublehidenblade/tokyo-drift-3d"
CENTRAL = "doublehidenblade/game-dev-central"


def prepare(archive, central_git):
    raw = Path(archive).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ARCHIVE_SHA256, "Archive differs from supplied version1"
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        load = lambda name: json.loads(z.read(name))
        objects = load("objects-complete.json")
        authority = load("authority-with-authenticated-review.PENDING_FRESH_AUTHORITY.json")
        submission = load("submission-with-committed-verdict.json")
        remaining = load("remaining-task-specific-inputs.json")
        family = load("six-task-family-facts-preserved.json")
        with zipfile.ZipFile(io.BytesIO(z.read("prior-checkpoint/td201-registration-checkpoint-2216.zip"))) as old:
            branches = json.loads(old.read("tokyo-branch-accounting.json"))
    heads = authority["rule_heads"]
    assert authority["candidate"]["artifact_head"] == SOURCE
    # Retained canonical task bytes prove dependencies without new branch reads.
    for fact in family.values():
        raw = fact["source_text"].encode()
        oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert oid == fact["ref"]["blob"]
        objects[TOKYO][oid] = dict(type="blob", base64=base64.b64encode(raw).decode())

    def central_ref(path):
        head = heads[CENTRAL]
        def add(oid, kind):
            raw = subprocess.check_output(["git", "-C", central_git, "cat-file", kind, oid])
            assert hashlib.sha1(kind.encode() + b" " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == oid
            objects[CENTRAL][oid] = dict(type=kind, base64=base64.b64encode(raw).decode())
            return raw
        raw = add(head,"commit")
        tree = raw.splitlines()[0].split()[1].decode()
        parts = path.split("/")
        for i, part in enumerate(parts):
            add(tree,"tree")
            mode, oid = ep.GitObjects(objects).tree(CENTRAL, tree)[part]
            if i < len(parts)-1:
                assert mode == b"40000"; tree=oid
            else:
                add(oid,"blob")
        return dict(repository=CENTRAL,commit=head,path=path,blob=oid)

    store = ep.GitObjects(objects)
    parent = reg.task_document(store,family["td-201"]["ref"])
    closure, pending = {}, ["td-201"]
    while pending:
        tid = pending.pop()
        if tid in closure: continue
        document = reg.task_document(store,family[tid]["ref"])
        closure[tid]=document
        pending.extend(document.get("dependencies",[]) + document.get("depends_on",[]))
    s = dict(version=1, observed_at=authority["observed_at"], repositories=heads, sources=[], **{kind:[] for kind in co.TABLES})
    for tid, doc in closure.items():
        task=dict(id=tid,repository=TOKYO,head_sha=heads[TOKYO],status=doc["status"],owner_id=doc["owner"],
                  project="lower-city",author_id=doc["owner"],needs=[],criteria=[f"parent-C{i+1}" for i in range(len(doc["completion_criteria"]))],required_checks=["original-parent-acceptance"],requirements={})
        s["tasks"].append(task);s["board"].append({k:task[k] for k in ("id","repository","head_sha","status","owner_id")})
    request = remaining["request"]["derived_identity"]
    s["requests"]=[dict(id=request.removeprefix("request:"),repository=TOKYO,task_id=None,project="lower-city",operations=["admission"],executors=["dot"],kind="ask",state="active",authority_verified=False,evidence="Frozen handoff explicitly requires fresh registration authority; no freshness invented")]
    s["executors"]=[dict(id="dot",repository=TOKYO,owner_id="dot",kind="native",state="unknown",capabilities=["admission"],observed_model=None,observed_effort=None,runtime_confirmed=False,resume_task=request)]
    for repo in heads:
        s["policies"].append(dict(id=repo+":policy",repository=repo,triggers_checked=False,push_runs_actions=False,push_deploys=False,merge_runs_actions=False,merge_deploys=False))
    # Unnormalized historical identities remain unknown. Original nonexclusive
    # associations stay in the unchanged Library archive, not rewritten as owners.
    s["branches"]=[dict(id=TOKYO+":refs/heads/"+b["branch"],repository=TOKYO,task_id=None,head_sha=b["head_sha"]) for b in branches]
    document_id="td-201-source-document-admission"
    s["evidence_policy"]={document_id:dict(authority=authority,submission=submission,objects=objects)}
    s["registration_source"]=dict(version=1,binding=dict(task_id=request,repository=TOKYO,operation="admission",executor_id="dot",owner_id="dot",head_sha=heads[TOKYO]),document_id=document_id,
        parent_ref=family["td-201"]["ref"],dependency_refs=[family[k]["ref"] for k in sorted(closure) if k!="td-201"],
        board_ref=central_ref("project-management/boards/tokyo-drift-3d.md"),journal_ref=central_ref("project-management/dispatch/ATTEMPTS.json"),
        collection={},attestation={},coexistence=[],allocation=dict(request_id=request,operation="admission",limit=1,used=None,evidence="Existing document correction consumed; current registration usage has not been authenticated"))
    return s, remaining, len(branches)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive");parser.add_argument("--central-git",required=True)
    parser.add_argument("--coexistence-proof",default=str(Path(__file__).with_name("td201-pr455-coexistence.json")))
    args=parser.parse_args()
    s,remaining,count=prepare(args.archive,args.central_git)
    original=deepcopy(s)
    inspected=reg.inspect_candidate(s)
    assert s==original
    packet=s["evidence_policy"][s["registration_source"]["document_id"]]
    coexistence=json.loads(Path(args.coexistence_proof).read_text())
    for repo, objects in coexistence["objects"].items():
        packet["objects"].setdefault(repo,{}).update(objects)
    s["registration_source"]["coexistence"]=[coexistence["disposition"]]
    compatible=reg.compatible_document_pr(coexistence["activity"],coexistence["disposition"],inspected,
        s["registration_source"],co.utc(coexistence["observed_at"]))
    # Preserve actual timestamps: at freeze time, aggregate authority is stale.
    at=co.utc("2026-10-11T22:35:17.588922+00:00")
    evidence=ep.evaluate_completion(packet["authority"],packet["submission"],packet["objects"],at)
    result=co.evaluate(s,at)
    assert not result["actions"] and evidence["status"]!="ACCEPTABLE"
    print(json.dumps(dict(archive_sha256=ARCHIVE_SHA256,candidate=SOURCE,immutable_candidate_scope="PASS",
        historical_rows=count,historical_task_mapping_required=False,write_paths=inspected["write_paths"],
        preserved_parent={k:inspected["parent"].get(k) for k in ("id","owner","status","dependencies","assigned_worker")},
        protected_task_ids=inspected["query"]["task_ids"],future_and_document_region_count=len(inspected["query"]["regions"]),
        canonical_disjoint_changes=inspected["canonical_disjoint_changes"],
        pr455_document_regions="COMPATIBLE at recorded approval, with pending session receipts retained",
        pr455_approval_observed_at=coexistence["observed_at"],pr455_pending_sessions=compatible["pending_session_ids"],
        documentary_authority_unchanged=True,documentary_authority_result=evidence["status"],documentary_issues=evidence.get("issues",[]),
        real_guard_status=result["status"],real_guard_warnings=result["warnings"],live_admission_claimed=False,
        preserved_known_overlap=remaining["live_overlap"]["retained"][0],remaining_inputs=["fresh authenticated candidate-scope catalog/observations, including PR455 and exact named historical session","current source-trigger, stop, owner, queue and session receipts","current finite registration allocation (not a new source-correction/runtime allocation)","fresh authentic documentary authority and review applicability"]),indent=2))


if __name__=="__main__":main()
