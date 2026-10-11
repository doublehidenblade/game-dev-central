"""One unfiled subordinate DOCUMENT registration, never runtime or publication.

The authorized collector must perform the exact inclusive query below against
current source, owner, session (including unpublished work), reservation and stop
sources. Hash bindings detect changed/shortened responses, not forged collectors.
Historical branch-to-task mappings are neither queried nor treated as liveness.
This module is read-only. The existing coordinator guard revalidates its decision.
"""
from datetime import timedelta
import difflib

import evidence_policy as ep
import scoped_admission as sa

need = sa.need
fields = sa.fields
PARENT_FIELDS = ("id", "status", "owner", "assigned_worker", "dependencies", "depends_on",
                 "completion_criteria", "ask", "constraints", "evidence", "verdict", "work_log")
READS = ("policies", "tasks", "board", "requests", "owners", "queue", "blockers", "executors", "catalog", "activity")


def task_document(store, ref):
    raw = store.citation(ref)
    if ref["path"].endswith(".md"):
        need(b"```json\n" in raw, "canonical task JSON block missing")
        raw = raw.split(b"```json\n", 1)[1].split(b"```", 1)[0]
    value = ep.load_json(raw)
    need(isinstance(value, dict) and isinstance(value.get("id"), str), "canonical task ID missing")
    return value


def current_ref(ref, heads):
    need(heads.get(ref["repository"]) == ref["commit"], "canonical source pin changed: " + ref["path"])


def named_session(document, repository):
    worker = document.get("assigned_worker")
    need(worker is None or isinstance(worker, str) and worker.strip() == worker and bool(worker),
         "unsupported named worker identity: " + document["id"])
    if worker is not None:
        need(isinstance(document["owner"], str) and document["owner"], "named worker owner is unknown")
        return dict(repository=repository, task_id=document["id"], session_id=worker, owner_id=document["owner"])


def require_ended_sessions(expected, activity):
    for session in expected:
        need(any(row["kind"] == "session" and row["repository"] == session["repository"] and
                 row["id"] == session["session_id"] and row["state"] == "ended" and
                 row["owner_id"] == session["owner_id"] and session["task_id"] in row["task_ids"] for row in activity),
             "named document session needs current ended receipt: " + session["task_id"] + ":" + session["session_id"])


def inspect_candidate(snapshot):
    """Immutable source inspection only; this result is NOT admission authority."""
    scope = snapshot["registration_source"]
    fields(scope, "version binding document_id parent_ref dependency_refs board_ref journal_ref collection attestation allocation coexistence", "registration source")
    need(scope["version"] == 1, "unsupported registration version")
    binding = scope["binding"]
    fields(binding, "task_id repository operation executor_id owner_id head_sha", "registration binding")
    need(binding["operation"] == "admission" and binding["task_id"].startswith("request:"), "only unfiled registration supported")
    heads, repo = snapshot["repositories"], binding["repository"]
    need(heads[repo] == binding["head_sha"], "registration base changed")
    request = next((r for r in snapshot["requests"] if "request:" + r["id"] == binding["task_id"]), None)
    need(request and request["repository"] == repo and request["task_id"] is None and request["kind"] == "ask",
         "genuinely unfiled ask required")
    packet = snapshot["evidence_policy"][scope["document_id"]]
    authority, submission = packet["authority"], packet["submission"]
    store = ep.GitObjects(packet["objects"])
    proposal = store.json(authority["task_ref"])
    ref, candidate = authority["task_ref"], authority["candidate"]
    need(ref["repository"] == repo == candidate["repository"] and proposal["id"] == scope["document_id"], "wrong subordinate identity")
    need(proposal.get("kind") == "documentation_acceptance_binding" and proposal.get("runtime_allowlist") == [],
         "registration is metadata only; no runtime writes admitted")
    need(sa.blob(store, repo, heads[repo], ref["path"]) is None, "subordinate task already exists at canonical base")
    need(sa.blob(store, repo, candidate["artifact_head"], ref["path"]) == ref["blob"], "subordinate proposal changed after review pin")
    need(not any(t["id"] == proposal["id"] for t in snapshot["tasks"] + snapshot["board"]), "existing task/row collision")
    parent_ref = scope["parent_ref"]
    current_ref(parent_ref, heads)
    parent = task_document(store, parent_ref)
    need(parent_ref["repository"] == repo and proposal["parent_task"] == parent["id"], "real parent identity required")
    need(parent["owner"] == authority["principals"]["coordinator"] == binding["owner_id"], "parent ownership cannot transfer through registration")
    parent_candidate = task_document(store, {**parent_ref, "commit": candidate["artifact_head"],
        "blob": store.blob_at(repo, candidate["artifact_head"], parent_ref["path"])})
    need(all(parent.get(k) == parent_candidate.get(k) for k in PARENT_FIELDS), "parent identity/dependencies/criteria/history changed")

    # Preserve the entire declared prerequisite chain, without pretending blocked
    # production dependencies are complete merely to register a document.
    related = {parent["id"]: parent}
    for dependency_ref in scope["dependency_refs"]:
        current_ref(dependency_ref, heads)
        dep = task_document(store, dependency_ref)
        need(dep["id"] not in related and dependency_ref["repository"] == repo, "duplicate/wrong-repository dependency")
        need(sa.leaf(store, repo, dependency_ref["commit"], dependency_ref["path"]) ==
             sa.leaf(store, repo, candidate["artifact_head"], dependency_ref["path"]),
             "canonical dependency must remain byte-identical: " + dep["id"])
        related[dep["id"]] = dep
    seen, pending = set(), [parent["id"]]
    while pending:
        tid = pending.pop()
        if tid in seen:
            continue
        need(tid in related, "canonical dependency omitted: " + tid)
        seen.add(tid)
        for field in ("dependencies", "depends_on"):
            dependencies = related[tid].get(field, [])
            sa.names(dependencies, "canonical " + field)
            pending.extend(dependencies)
    need(seen == set(related), "unrelated or omitted dependency records")
    named_sessions = [session for tid in sorted(related) if (session := named_session(related[tid], repo)) is not None]
    need(proposal.get("dependencies") == proposal.get("depends_on") == [], "subordinate adds unsupported execution dependencies")
    for tid, document in related.items():
        task = next((t for t in snapshot["tasks"] if t["id"] == tid and t["repository"] == repo), None)
        board = next((b for b in snapshot["board"] if b["id"] == tid and b["repository"] == repo), None)
        need(task and board and task["head_sha"] == board["head_sha"] == heads[repo] and
             task["owner_id"] == board["owner_id"] == document["owner"] and
             task["status"] == board["status"] == document["status"], "canonical parent/dependency owner or status omitted")

    board_ref, journal_ref = scope["board_ref"], scope["journal_ref"]
    current_ref(board_ref, heads); current_ref(journal_ref, heads)
    rows, _ = sa.board_rows(store.citation(board_ref))
    need(parent["id"] in rows and proposal["id"] not in rows, "canonical parent row missing or subordinate row already exists")
    cells = [v.strip() for v in rows[parent["id"]][2].strip().split("|")[1:-1]]
    need(len(cells) >= 4 and cells[3] == parent["owner"] and cells[2].split()[0] == parent["status"], "canonical parent board owner/status changed")
    journal = store.json(journal_ref)
    need(journal_ref["path"] == "project-management/dispatch/ATTEMPTS.json", "canonical attempt journal required")
    import dispatch_loop
    dispatch_loop.validate(dict(version=1, rollout_limit=1, ready=[], blocked=[]), journal)

    amendment = proposal["scope_amendment"]
    source_parent = amendment["source_parent"]
    ep.full_sha(source_parent)
    need(store.ancestor(repo, source_parent, heads[repo]) and
         store.ancestor(repo, source_parent, candidate["artifact_head"]), "unproved candidate source parent")
    delta = sorted(sa.changed_paths(store, repo, source_parent, candidate["artifact_head"]))
    sa.names(amendment["permitted_new_paths"], "declared new metadata paths")
    sa.names(amendment["frozen_reviewed_local_paths"], "frozen reviewed metadata paths")
    for path in amendment["permitted_new_paths"]:
        need(sa.leaf(store, repo, source_parent, path) is None and sa.leaf(store, repo, heads[repo], path) is None,
             "declared new metadata path already exists: " + path)
    need(set(amendment["frozen_reviewed_local_paths"]) <= {parent_ref["path"]}, "only the intact parent can be an existing-file edit")
    need(all(path == parent_ref["path"] or
             sa.leaf(store, repo, source_parent, path) is None and sa.leaf(store, repo, heads[repo], path) is None for path in delta),
         "registration cannot rewrite any other existing file")
    permitted = set(amendment["permitted_new_paths"] + amendment["frozen_reviewed_local_paths"])
    permitted.update(r["path"] for r in authority["decisions"] if r["repository"] == repo)
    permitted.add(submission["verdict"]["path"])
    prefix = parent_ref["path"].rsplit("/", 1)[0] + "/"
    need(delta and set(delta) <= permitted and all(p.startswith(prefix) and p.endswith((".json", ".md")) for p in delta),
         "candidate delta outside exact metadata scope")
    need(all((sa.leaf(store, repo, candidate["artifact_head"], p) or (None,))[0] == b"100644" for p in delta),
         "registration cannot delete files or add executable metadata")
    original_parent = store.citation(parent_ref)
    candidate_parent = store.read(repo, store.blob_at(repo, candidate["artifact_head"], parent_ref["path"]), "blob")
    need(candidate_parent == original_parent or parent_ref["path"].endswith(".md") and
         candidate_parent.startswith(original_parent), "registration may only append to the intact parent document")
    regions = [{"repository": repo, "path": p, "row_keys": []} for p in delta]
    for ref in [parent_ref, *scope["dependency_refs"]]:
        region = {"repository": ref["repository"], "path": ref["path"], "row_keys": []}
        if region not in regions:
            regions.append(region)
    identities = set(related) | {binding["task_id"], proposal["id"]}
    # Future paths are overlap-query scope only, never a registration write grant.
    for path in delta:
        if path.endswith(".json"):
            doc = store.json({"repository": repo, "commit": candidate["artifact_head"], "path": path,
                              "blob": store.blob_at(repo, candidate["artifact_head"], path)})
            if isinstance(doc, dict) and doc.get("runtime_allowlist"):
                need(doc.get("parent_task") == parent["id"] and doc.get("parent_dependency_retained") == parent.get("dependencies", []),
                     "future component loses real parent/dependencies")
                identities.add(doc["id"])
                sa.names(doc["runtime_allowlist"], "future runtime query paths", True)
                for path in doc["runtime_allowlist"]:
                    ep.path_parts(path)
                    regions.append({"repository": repo, "path": path, "row_keys": []})
    regions.append({"repository": board_ref["repository"], "path": board_ref["path"], "row_keys": [parent["id"], proposal["id"]]})
    drift = sa.changed_paths(store, repo, source_parent, heads[repo])
    need(not any(sa.path_overlap(path, region) for path in drift for region in regions if region["repository"] == repo),
         "canonical changes overlap candidate/parent/dependency/future scope")
    query = {"binding": binding, "candidate": candidate, "task_ids": sorted(identities),
             "repositories": heads, "regions": sorted(regions, key=lambda r: (r["repository"], r["path"])),
             "allocation_digest": ep.digest(scope["allocation"]),
             "include_global_stops": True, "include_unpublished": True, "include_unknown": True,
             "source_mode": "all current open PRs and active/unknown branches, sessions and reservations; no historical task mapping"}
    if named_sessions:
        query["named_sessions"] = named_sessions
    return {"query": query, "packet": packet, "journal": journal, "document": proposal,
            "parent": parent, "write_paths": delta, "canonical_disjoint_changes": sorted(drift), "named_sessions": named_sessions}


def compatible_document_pr(row, disposition, inspected, scope, at):
    """Exact same-owner serialization of disjoint document regions, never liveness."""
    import coordinator as co
    fields(disposition, "source_digest query_digest candidate_head source_base owner_id approved_by observed_at owner_evidence approval_evidence", "document coexistence")
    query, packet = inspected["query"], inspected["packet"]
    need(disposition["source_digest"] == ep.digest(row) and disposition["query_digest"] == ep.digest(query) and
         disposition["candidate_head"] == query["candidate"]["artifact_head"], "coexistence source/candidate/query changed")
    need(row["kind"] == "pr" and row["state"] == "open", "coexistence cannot release a session/reservation/unknown branch")
    owner = inspected["parent"]["owner"]
    need(owner == row["owner_id"] == disposition["owner_id"] == disposition["approved_by"] == scope["binding"]["owner_id"] and
         all(isinstance(disposition[k], str) and disposition[k].strip() for k in ("owner_evidence", "approval_evidence")),
         "explicit same-owner serialized coexistence required; no ownership transfer")
    need(timedelta(0) <= at - ep.utc(disposition["observed_at"]) < co.MAX_AGE, "stale/future coexistence approval")
    store, repo, base = ep.GitObjects(packet["objects"]), row["repository"], disposition["source_base"]
    # This deliberately narrow route supports one-parent documentary PRs. The
    # complete tree diff prevents a disposition hiding an additional write.
    need(store.commit(repo, row["head_sha"])[1] == [base], "coexistence requires exact single-commit source parent")
    changes = sa.changed_paths(store, repo, base, row["head_sha"])
    expected = [{"repository": repo, "path": p, "row_keys": []} for p in sorted(changes)]
    need(row["regions"] == expected, "coexistence must retain the complete source delta")
    reads = {r["path"]: r for r in [scope["parent_ref"], *scope["dependency_refs"]]}
    pending_sessions = []
    for path in changes:
        protected = [r for r in query["regions"] if r["repository"] == repo and sa.path_overlap(path, r)]
        if not protected:
            continue
        need(path in reads and all(r["path"] == path for r in protected), "coexistence overlaps new metadata/future/board scope")
        original = store.citation(reads[path])
        base_ref = dict(repository=repo, commit=base, path=path, blob=store.blob_at(repo, base, path))
        baseline = store.citation(base_ref)
        other_ref = dict(repository=repo, commit=row["head_sha"], path=path, blob=store.blob_at(repo, row["head_sha"], path))
        other = store.citation(other_ref)
        canonical_task, pending_task = task_document(store, reads[path]), task_document(store, other_ref)
        need(canonical_task["owner"] == owner and all(canonical_task.get(k) == pending_task.get(k)
             for k in ("id", "owner", "dependencies", "depends_on", "completion_criteria")),
             "coexistence cannot change dependency ownership or acceptance criteria")
        for document in (canonical_task, pending_task):
            session = named_session(document, repo)
            if session is not None and session not in pending_sessions:
                pending_sessions.append(session)
        if path in inspected["write_paths"]:
            need(path == scope["parent_ref"]["path"] and path.endswith(".md"), "only the intact parent's appendix can share a write path")
            before, current, after = [raw.splitlines(keepends=True) for raw in (baseline, original, other)]
            unchanged = [op for op in difflib.SequenceMatcher(None, before, current, autojunk=False).get_opcodes() if op[0] == "equal"]
            for tag, start, end, _, _ in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
                if tag == "equal":
                    continue
                # Map each actual PR hunk through unchanged canonical text.
                # Later canonical appendices are not PR deletions. Ambiguous or
                # overlapping edits, including the append boundary, stay held.
                need(any(a <= start <= end < b and c + end - a < len(current)
                         for _, a, b, c, d in unchanged), "source changes intersect canonical edits or candidate appendix boundary")
        # Read-only prerequisites may have pending same-owner amendments; no
        # bytes are imported and no task/dependency/status/acceptance is changed.
    return {"pending_session_ids": sorted({s["session_id"] for s in pending_sessions}), "named_sessions": pending_sessions}


def verify(snapshot, at):
    import coordinator as co
    import dispatch_loop
    inspected = inspect_candidate(snapshot)
    scope, query = snapshot["registration_source"], inspected["query"]
    binding = scope["binding"]
    collection, receipt = scope["collection"], scope["attestation"]
    fields(receipt, "collector_id observed_at query_digest records_digest evidence", "authenticated scoped collection")
    fields(collection, "query reads", "scoped collection response")
    need(collection["query"] == query and receipt["query_digest"] == ep.digest(query), "inclusive candidate query changed or narrowed")
    need(receipt["records_digest"] == ep.digest(collection["reads"]), "scoped response changed/shortened after collection")
    need(receipt["collector_id"] == inspected["packet"]["authority"]["principals"]["coordinator"] and
         isinstance(receipt["evidence"], str) and receipt["evidence"].strip(), "authenticated coordinator collection required")
    observed = ep.utc(receipt["observed_at"])
    need(timedelta(0) <= at - observed < co.MAX_AGE and observed <= co.utc(snapshot["observed_at"]), "stale/future scoped collection")
    need(set(collection["reads"]) == set(READS), "inclusive source query missing a required source")
    for kind, read in collection["reads"].items():
        fields(read, "records pages_read items_seen exhausted read_status", "scoped source result")
        need(type(read["pages_read"]) is int and read["pages_read"] > 0 and
             read["items_seen"] == len(read["records"]) and read["exhausted"] is True and read["read_status"] == "ok",
             "incomplete scoped source read: " + kind)
        if kind not in {"catalog", "activity"}:
            need(read["records"] == snapshot[kind], "omitted/changed relevant source records: " + kind)
    catalog = collection["reads"]["catalog"]["records"]
    activity = collection["reads"]["activity"]["records"]
    # The complete source catalog and overlap observations are separate reads.
    # A caller cannot present only chosen candidates as the catalog's result.
    catalog_ids = set()
    for item in catalog:
        fields(item, "id repository kind head_sha", "current source catalog entry")
        identity = (item["repository"], item["kind"], item["id"])
        need(identity not in catalog_ids, "duplicate current source identity")
        catalog_ids.add(identity)
        matches = [r for r in activity if (r["repository"], r["kind"], r["id"]) == identity]
        need(len(matches) == 1 and matches[0]["head_sha"] == item["head_sha"], "omitted/changed current source: " + item["id"])
    need(catalog_ids == {(r["repository"], r["kind"], r["id"]) for r in activity}, "current source catalog/result mismatch")
    need(all(any(r["repository"] == p["repository"] and r["kind"] == "pr" and r["id"] == p["id"] and
                     r["head_sha"] == p["head_sha"] for r in catalog) for p in snapshot["prs"] if p["state"] == "open"),
         "known open PR omitted/changed in current source catalog")
    need(isinstance(scope["coexistence"], list), "coexistence receipts must be a list")
    used_dispositions = []
    for row in activity:
        fields(row, "id repository kind state head_sha task_ids regions owner_id", "current overlap result")
        need(row["kind"] in {"branch", "pr", "session", "reservation"}, "unknown overlap source kind")
        states = {"branch": {"active", "unknown"}, "pr": {"open"},
                  "session": {"live", "unknown", "ended"}, "reservation": {"pending", "unknown"}}
        need(row["state"] in states[row["kind"]], "unknown/unsupported current source state")
        need(row["repository"] in snapshot["repositories"], "current source repository unaccounted")
        if row["kind"] in {"branch", "pr"}:
            ep.full_sha(row["head_sha"])
        if row["regions"] is None or row["task_ids"] is None:
            raise sa.ScopeError("unknown live/source scope retained: " + row["id"])
        sa.names(row["task_ids"], "activity task identities")
        need(isinstance(row["regions"], list) and (row["regions"] or row["task_ids"]), "empty live/source scope is unknown")
        relevant = bool(set(row["task_ids"]) & set(query["task_ids"]))
        for region in row["regions"]:
            fields(region, "repository path row_keys", "activity region")
            need(region["repository"] == row["repository"], "activity region repository mismatch")
            ep.path_parts(region["path"].removesuffix("/"))
            sa.names(region["row_keys"], "activity row identities")
            for protected in query["regions"]:
                if region["repository"] == protected["repository"] and sa.path_overlap(region["path"], protected):
                    if region["path"] != protected["path"] or not region["row_keys"] or not protected["row_keys"] or set(region["row_keys"]) & set(protected["row_keys"]):
                        relevant = True
        dispositions = [d for d in scope["coexistence"] if d.get("source_digest") == ep.digest(row)]
        need(len(dispositions) <= 1, "duplicate coexistence disposition")
        compatible = False
        if relevant and dispositions:
            proof = compatible_document_pr(row, dispositions[0], inspected, scope, at)
            require_ended_sessions(proof["named_sessions"], activity)
            compatible = True
            used_dispositions.extend(dispositions)
        need(not relevant or compatible or row["state"] == "ended" and row["kind"] == "session",
             "relevant live/open/unknown overlap retained: " + row["id"])
    need(len(used_dispositions) == len(scope["coexistence"]), "unmatched/stale coexistence disposition")
    require_ended_sessions(inspected["named_sessions"], activity)
    for row in snapshot["owners"]:
        if row["task_id"] in query["task_ids"] or row["executor_id"] == binding["executor_id"]:
            need(row["task_id"] == binding["task_id"] or row["state"] == "released", "relevant parent/dependency owner retained: " + row["id"])
    need(not any(row["task_id"] in query["task_ids"] or row["executor_id"] == binding["executor_id"] for row in snapshot["queue"]),
         "relevant queued/reserved work retained")
    for row in snapshot["blockers"]:
        if row["task_id"] in ["*", *query["task_ids"]] and ("admission" in row["operations"] or "*" in row["operations"]):
            raise sa.ScopeError("relevant/global hold retained: " + row["id"] + ":" + row["reason"])
    for row in snapshot["requests"]:
        if row["task_id"] in ["*", *query["task_ids"]] and row["state"] == "cancelled" and "admission" in row["operations"]:
            raise sa.ScopeError("parent/dependency user stop retained: " + row["id"])
    for policy in snapshot["policies"]:
        need(policy["triggers_checked"] and not any(policy[k] for k in ("push_runs_actions", "push_deploys", "merge_runs_actions", "merge_deploys")),
             "source trigger/publication hold")
    for event in inspected["journal"]["events"]:
        if event["kind"] == "hold" and event["key"].split(":", 1)[-1] in query["task_ids"]:
            raise sa.ScopeError("canonical journal hold retained: " + event["key"])
    for attempt in dispatch_loop.attempts(inspected["journal"]):
        if not attempt["released"] and (attempt["key"].split(":", 1)[-1] in query["task_ids"] or
                attempt["decision"]["executor_id"] == binding["executor_id"] or
                any(r["repository"] == attempt["decision"]["repository"] and
                    any(sa.path_overlap(p, r) for p in attempt["write_paths"]) for r in query["regions"])):
            raise sa.ScopeError("canonical journal reservation retained: " + attempt["attempt_id"])
    allocation = scope["allocation"]
    fields(allocation, "request_id operation limit used evidence", "registration-only allocation")
    need(allocation["request_id"] == binding["task_id"] and allocation["operation"] == "admission" and
         type(allocation["used"]) is int and type(allocation["limit"]) is int and
         0 <= allocation["used"] < allocation["limit"] <= 2 and allocation["evidence"],
         "finite evidenced registration allocation required; no unknown/zero inference or gameplay reset")
    packet = inspected["packet"]
    need(packet["authority"]["rule_heads"] == snapshot["repositories"], "current rule applicability pins changed")
    verdict = ep.evaluate_completion(packet["authority"], packet["submission"], packet["objects"], at)
    need(verdict["status"] == "ACCEPTABLE", "independent documentary acceptance required: " + str(verdict.get("issues", [])))
    observations = [observed, ep.utc(packet["authority"]["observed_at"])] + [ep.utc(d["observed_at"]) for d in scope["coexistence"]]
    return {"binding": binding, "scope_digest": ep.digest(scope), "inventory_digest": receipt["records_digest"],
            "expires_at": min(observations) + co.MAX_AGE}
