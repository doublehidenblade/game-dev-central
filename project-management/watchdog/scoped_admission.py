"""Proof-bound source coverage for ONE filed-task operation; no I/O or dispatch.

Git objects prove exclusions, not freshness or external identity. Authenticated
collectors remain responsible for exhaustive branch/PR reads and the stated
region/identity queries against every ownership, queue and stop source. A scope
receipt is never a claim of repository-wide liveness or permission to act.
"""
from datetime import timedelta
import re

import evidence_policy as ep


class ScopeError(ValueError):
    pass


def need(condition, detail):
    if not condition:
        raise ScopeError(detail)


def fields(value, keys, where):
    need(isinstance(value, dict) and set(value) == set(keys.split()),
         where + ": unexpected or missing fields")


def names(value, where, nonempty=False):
    need(isinstance(value, list) and all(isinstance(x, str) and x for x in value)
         and len(value) == len(set(value)) and (value or not nonempty),
         where + ": unique nonempty strings required")


def chain(store, repo, values, descendant, ancestor):
    """A supplied path must prove every parent edge; no ancestry boolean."""
    names(values, "ancestry path", True)
    need(values[0] == descendant and values[-1] == ancestor,
         "ancestry path endpoints differ")
    for i, head in enumerate(values):
        _, parents = store.commit(repo, head)
        if i + 1 < len(values):
            need(values[i + 1] in parents, "unproved ancestry edge")


def changed_paths(store, repo, before, after):
    """Complete structural diff; identical subtrees need no downloaded blobs."""
    left, _ = store.commit(repo, before)
    right, _ = store.commit(repo, after)
    changes = set()

    def walk(a, b, prefix):
        if a == b:
            return
        aa = store.tree(repo, a) if a else {}
        bb = store.tree(repo, b) if b else {}
        for name in sorted(set(aa) | set(bb)):
            x, y = aa.get(name), bb.get(name)
            if x == y:
                continue
            path = prefix + name
            if (x is None or x[0] == b"40000") and (y is None or y[0] == b"40000"):
                walk(x[1] if x else None, y[1] if y else None, path + "/")
            elif x and x[0] == b"40000" or y and y[0] == b"40000":
                # Type changes overlap the entire path, not just one child.
                changes.add(path)
            else:
                changes.add(path)
    walk(left, right, "")
    return changes


def leaf(store, repo, head, path):
    """None means a proved absent path, never a missing proof object."""
    tree, _ = store.commit(repo, head)
    parts = ep.path_parts(path)
    for i, part in enumerate(parts):
        entries = store.tree(repo, tree)
        if part not in entries:
            return None
        mode, oid = entries[part]
        if i < len(parts) - 1:
            need(mode == b"40000", "region path crosses a non-directory")
            tree = oid
        else:
            need(mode in (b"100644", b"100755"), "region is not a regular file")
            return mode, oid


def blob(store, repo, head, path):
    entry = leaf(store, repo, head, path)
    return entry[1] if entry else None


def board_rows(raw):
    """Recognize header-led pipe-row blocks, preserving non-data-row bytes.

    A row-region proof supports only simple unique ASCII first-cell keys. A
    changed header, separator, section context, duplicate key or unsupported row
    cannot be dismissed as an unrelated row. This is not a Markdown interpreter.
    """
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)
    rows, skeleton = {}, []
    row_number, in_rows, have_header = 0, False, False
    separator = re.compile(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
    for i, line in enumerate(lines):
        is_header = (line.startswith("|") and i + 1 < len(lines) and
                     separator.fullmatch(lines[i + 1].strip()))
        is_separator = separator.fullmatch(line.strip()) and i and lines[i - 1].startswith("|")
        if is_header or is_separator:
            have_header = True
            in_rows = False
            skeleton.append(line)
            continue
        # The canonical board contains blank-separated pipe-row blocks without
        # repeated headers. Preserve each block's identity and all separators;
        # recognizing these rows does not permit movement between blocks.
        if have_header and line.startswith("|"):
            cells = line.rstrip("\r\n").split("|")
            key = cells[1].strip() if len(cells) > 2 else ""
            need(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key), "unsupported board row identity")
            need(key not in rows, "duplicate board row identity")
            if not in_rows:
                row_number = 0
            in_rows = True
            # Anchor to the preserved non-row prefix, including empty tables.
            # Counting only populated blocks would miss moves into an empty
            # historical/paused table that precedes/follows the same headers.
            rows[key] = (len(skeleton), row_number, line)
            row_number += 1
        else:
            in_rows = False
            skeleton.append(line)
    need(rows, "row proof contains no recognized table rows")
    return rows, "".join(skeleton)


def row_delta(store, repo, before, after, path):
    left_entry, right_entry = leaf(store, repo, before, path), leaf(store, repo, after, path)
    need(left_entry and right_entry and left_entry[0] == right_entry[0], "row proof cannot change file mode")
    aa, bb = left_entry[1], right_entry[1]
    need(aa is not None and bb is not None, "row proof cannot create/delete a table")
    left, left_context = board_rows(store.read(repo, aa, "blob"))
    right, right_context = board_rows(store.read(repo, bb, "blob"))
    need(left_context == right_context, "board non-row context changed")
    return {key for key in set(left) | set(right) if left.get(key) != right.get(key)}


def path_overlap(path, region):
    root = region["path"].rstrip("/")
    return path == root or path.startswith(root + "/") or root.startswith(path + "/")


def region_equal(store, repo, before, after, region):
    if region["row_keys"]:
        return not (row_delta(store, repo, before, after, region["path"]) & set(region["row_keys"]))
    if region["path"].endswith("/"):
        return not any(path_overlap(path, region) for path in changed_paths(store, repo, before, after))
    return leaf(store, repo, before, region["path"]) == leaf(store, repo, after, region["path"])


def query(scope):
    """Exact query each collector must actually perform, not a task-name prefix."""
    return {"binding": scope["binding"], "base_heads": scope["base_heads"],
            "regions": scope["regions"], "task_ids": scope["related_task_ids"],
            "dependency_task_ids": scope["task_ids"],
            "include_global_and_wildcard_holds": True,
            "include_any_owner_touching_regions": True,
            "include_all_target_owner_and_executor_reservations": True}


def inventory_digest(snapshot, tables):
    """Bind raw refs, normalized inventories and the source/collector identities.

    Omit receipt digest fields to avoid self-reference. The complete scope and
    input digests additionally bind every observation, result and timestamp.
    """
    scope = snapshot["scoped_source"]
    return ep.digest({"raw_sources": scope["inventory"],
        "record_ids": {kind: [r["id"] for r in snapshot[kind]] for kind in tables},
        "collectors": [{k: r[k] for k in ("id", "kind", "repository", "source_repository", "ref_sha", "provenance")}
                       for r in scope["receipts"]]})


def verify(snapshot, at, tables, sources_for):
    """Return an exact-action receipt or fail the entire scoped request closed."""
    scope = snapshot["scoped_source"]
    fields(scope, "version binding base_heads task_ids related_task_ids regions candidate inventory receipts objects", "scoped source")
    need(type(scope["version"]) is int and scope["version"] == 1, "unsupported scoped version")
    binding = scope["binding"]
    fields(binding, "task_id repository operation executor_id owner_id head_sha", "scoped binding")
    need(binding["operation"] in {"implementation", "verification", "upload", "merge"},
         "scoped coverage supports filed-task source operations only")
    ep.full_sha(binding["head_sha"])
    need(scope["base_heads"] == snapshot["repositories"], "scoped base heads changed")
    repo = binding["repository"]
    need(repo in scope["base_heads"], "scoped repository missing")
    names(scope["task_ids"], "relevant task IDs", True)
    names(scope["related_task_ids"], "related ownership-query task IDs", True)
    need(set(scope["task_ids"]) <= set(scope["related_task_ids"]), "ownership query omits prerequisite task")
    need(binding["task_id"] in scope["task_ids"], "target missing from task closure")
    need(scope["task_ids"] == [binding["task_id"]],
         "multi-task prerequisite graphs require canonical transitive proof; unsupported in scoped v1")
    need(set(scope["task_ids"]) == {t["id"] for t in snapshot["tasks"]},
         "every relevant task must be normalized, without a candidate-only shortlist")
    task = next(t for t in snapshot["tasks"] if t["id"] == binding["task_id"])
    need(task["head_sha"] == binding["head_sha"] and task["repository"] == repo,
         "scoped task head/repository mismatch")
    executor = next((e for e in snapshot["executors"] if e["id"] == binding["executor_id"]), None)
    need(executor and executor["owner_id"] == binding["owner_id"] and executor["repository"] == repo,
         "scoped executor/owner mismatch")
    for rr in scope["base_heads"]:
        need(len([p for p in snapshot["policies"] if p["repository"] == rr]) == 1,
             "exactly one current policy record required for scoped source")
    packet = snapshot.get("evidence_policy", {}).get(task["id"])
    need(isinstance(packet, dict), "filed scoped task requires canonical evidence-policy packet")
    authority = packet["authority"]
    # Scope coverage never replaces evidence-policy admission or acceptance.
    need(authority["rule_heads"] == scope["base_heads"], "scope and current rule heads differ")
    store = ep.GitObjects(scope["objects"])
    evidence_store = ep.GitObjects(packet["objects"])
    canonical = evidence_store.json(authority["task_ref"])
    need(canonical.get("id") == task["id"], "wrong canonical scoped task")
    if canonical.get("parent_task") is not None:
        need(isinstance(canonical["parent_task"], str) and canonical["parent_task"] in scope["related_task_ids"],
             "ownership query omits canonical parent task")
    for key in ("depends_on", "dependencies"):
        if key in canonical:
            names(canonical[key], "canonical " + key)
            need(not canonical[key], "canonical prerequisite graph unsupported in scoped v1; retain hold")
    regions = scope["regions"]
    need(isinstance(regions, list) and regions, "protected source/dependency/owner regions required")
    seen = set()
    for region in regions:
        fields(region, "repository path row_keys", "protected region")
        need(region["repository"] in scope["base_heads"], "unaccounted region repository")
        ep.path_parts(region["path"].rstrip("/"))
        names(region["row_keys"], "row keys")
        need(set(region["row_keys"]) <= set(scope["related_task_ids"]), "ownership query omits protected row identity")
        need(not region["row_keys"] or not region["path"].endswith("/"), "rows need exact file")
        key = (region["repository"], region["path"])
        need(key not in seen, "duplicate protected path")
        seen.add(key)
    # Include canonical task/evidence source and all current rules. A selected
    # table row may narrow a source file only after candidate row-only proof.
    required = {(repo, authority["task_ref"]["path"])}
    for policy in canonical.get("evidence_policy", {}).values():
        required.update((repo, p) for p in policy["source_paths"])
    required.update((r["ref"]["repository"], r["ref"]["path"]) for r in authority["rules"])
    for rr, path in required:
        need(any(r["repository"] == rr and (r["path"] == path or
                 r["path"].endswith("/") and path.startswith(r["path"])) for r in regions),
             "scope omits canonical source/rule path: " + path)
    # Rules and the canonical task cannot be narrowed to selected table rows.
    fixed = {(repo, authority["task_ref"]["path"])} | {
        (r["ref"]["repository"], r["ref"]["path"]) for r in authority["rules"]}
    rule_paths = set()
    for rule in authority["rules"]:
        ref = rule["ref"]
        need(ref["commit"] == scope["base_heads"][ref["repository"]] and
             blob(store, ref["repository"], ref["commit"], ref["path"]) == ref["blob"],
             "current rule membership differs from scoped base")
        evidence_store.citation(ref)
        rule_paths.add((ref["repository"], ref["path"]))
    need(not any(r["row_keys"] and (r["repository"], r["path"]) in fixed for r in regions),
         "canonical rule/task cannot use row exclusion")
    candidate = scope["candidate"]
    fields(candidate, "pr_id branch_id fork_sha base_chain head_chain", "candidate proof")
    current_prs = [p for p in snapshot["prs"] if p["task_id"] == task["id"] and p["state"] == "open"]
    need(len(current_prs) == 1 and current_prs[0]["id"] == candidate["pr_id"] and
         current_prs[0]["head_sha"] == binding["head_sha"], "candidate must be the one normalized current task PR")
    need(any(b["id"] == candidate["branch_id"] and b["repository"] == repo and
             b["task_id"] == task["id"] and b["head_sha"] == binding["head_sha"] for b in snapshot["branches"]),
         "candidate branch must retain normalized task ownership")
    chain(store, repo, candidate["base_chain"], scope["base_heads"][repo], candidate["fork_sha"])
    chain(store, repo, candidate["head_chain"], binding["head_sha"], candidate["fork_sha"])
    delta = changed_paths(store, repo, candidate["fork_sha"], binding["head_sha"])
    for region in regions:
        if region["row_keys"]:
            need(region["repository"] == repo and region["path"] in delta and
                 row_delta(store, repo, candidate["fork_sha"], binding["head_sha"], region["path"]) == set(region["row_keys"]),
                 "row scope must match the complete actual candidate row delta")
        if region["repository"] == repo:
            # Rules are independently pinned to CURRENT base membership and the
            # unchanged policy gate checks acknowledgment/review applicability.
            # An old branch that does not edit a rule does not revert that rule
            # on merge. Other source dependencies still require equivalence.
            if (repo, region["path"]) in rule_paths and region["path"] not in delta:
                continue
            need(region_equal(store, repo, candidate["fork_sha"], scope["base_heads"][repo], region) or
                 region_equal(store, repo, binding["head_sha"], scope["base_heads"][repo], region),
                 "protected current-base dependency diverged from reviewed candidate: " + region["path"])
    for path in delta:
        protected = [r for r in regions if r["repository"] == repo and path_overlap(path, r)]
        need(protected, "candidate delta outside protected regions: " + path)
        for region in protected:
            if region["row_keys"]:
                need(path == region["path"] and row_delta(store, repo, candidate["fork_sha"],
                     binding["head_sha"], path) <= set(region["row_keys"]),
                     "candidate changes unprotected board rows")
    fields(scope["inventory"], "branches prs", "raw source inventory")
    accounted, overlaps = [], []
    for kind in ("branches", "prs"):
        entries = scope["inventory"][kind]
        need(isinstance(entries, list), "raw inventory must be a list")
        ids = set()
        for item in entries:
            fields(item, "id repository head_sha proof" + (" branch_id author_id" if kind == "prs" else ""), "raw " + kind)
            need(isinstance(item["id"], str) and item["id"] and item["id"] not in ids, "duplicate raw source ID")
            ids.add(item["id"])
            rr, head = item["repository"], item["head_sha"]
            need(rr in scope["base_heads"], "raw source outside repository coverage")
            ep.full_sha(head)
            store.commit(rr, head)
            proof = item["proof"]
            need(isinstance(proof, dict) and "kind" in proof, "branch/PR proof required")
            selected = item["id"] == candidate["pr_id" if kind == "prs" else "branch_id"] and rr == repo
            if selected:
                fields(proof, "kind", "selected proof")
                need(proof["kind"] == "candidate" and head == binding["head_sha"], "selected source head differs")
                if kind == "prs":
                    need(item["branch_id"] == candidate["branch_id"], "candidate PR branch differs")
                accounted.append(item["id"])
                continue
            if proof["kind"] == "base_ancestor":
                fields(proof, "kind chain", "contained source proof")
                chain(store, rr, proof["chain"], scope["base_heads"][rr], head)
                accounted.append(item["id"])
                continue
            if proof["kind"] == "candidate_ancestor" and kind == "branches" and rr == repo:
                fields(proof, "kind chain", "contained branch proof")
                chain(store, rr, proof["chain"], binding["head_sha"], head)
                accounted.append(item["id"])
                continue
            fields(proof, "kind fork_sha base_chain head_chain", "disjoint proof")
            need(proof["kind"] == "disjoint", "unknown source exclusion proof")
            chain(store, rr, proof["base_chain"], scope["base_heads"][rr], proof["fork_sha"])
            chain(store, rr, proof["head_chain"], head, proof["fork_sha"])
            changes = changed_paths(store, rr, proof["fork_sha"], head)
            for region in (r for r in regions if r["repository"] == rr):
                if not any(path_overlap(p, region) for p in changes):
                    continue
                # Prove the region unchanged on this branch, or prove its full
                # relevant result already present at the current base (squash).
                if not (region_equal(store, rr, proof["fork_sha"], head, region) or
                        region_equal(store, rr, scope["base_heads"][rr], head, region)):
                    overlaps.append(item["id"] + ":" + region["path"])
            accounted.append(item["id"])
        selected_id = candidate["pr_id" if kind == "prs" else "branch_id"]
        need(selected_id in ids, "selected source absent from complete raw inventory")
        if kind == "branches":
            for rr, base in scope["base_heads"].items():
                need(any(i["repository"] == rr and i["head_sha"] == base for i in entries),
                     "current repository base absent from raw branch inventory")
        for row in snapshot[kind]:
            match = next((i for i in entries if i["id"] == row["id"]), None)
            need(match and match["repository"] == row["repository"] and match["head_sha"] == row["head_sha"],
                 "normalized source omitted/changed in raw inventory")
            if kind == "prs":
                need(row["state"] == "open" and match["author_id"] == row["author_id"], "current PR author/state differs")
    # Every PR's head branch must be observed at the same immutable head.
    for pr in scope["inventory"]["prs"]:
        need(any(b["id"] == pr["branch_id"] and b["repository"] == pr["repository"] and
                 b["head_sha"] == pr["head_sha"] for b in scope["inventory"]["branches"]),
             "raw PR branch missing or changed")
    source_digest = inventory_digest(snapshot, tables)
    query_digest = ep.digest(query(scope))
    need(isinstance(scope["receipts"], list), "scoped source receipts required")
    times, seen = {}, set()
    for receipt in scope["receipts"]:
        fields(receipt, "id kind repository source_repository ref_sha observed_at read_status pagination ids query_digest inventory_digest records_digest provenance", "scoped receipt")
        key = (receipt["repository"], receipt["kind"])
        need(key not in times and key[0] in scope["base_heads"] and key[1] in tables, "duplicate/unknown scoped source")
        need(isinstance(receipt["id"], str) and receipt["id"] and receipt["id"] not in seen, "duplicate receipt identity")
        seen.add(receipt["id"])
        need(receipt["source_repository"] in scope["base_heads"] and receipt["ref_sha"] == scope["base_heads"][receipt["source_repository"]], "scoped source head changed")
        need(receipt["query_digest"] == query_digest and receipt["inventory_digest"] == source_digest, "scoped query/inventory changed")
        records = [r for r in snapshot[key[1]] if r["repository"] == key[0]]
        need(receipt["records_digest"] == ep.digest(records), "scoped normalized records changed")
        raw = scope["inventory"][key[1]] if key[1] in ("branches", "prs") else snapshot[key[1]]
        expected_ids = {r["id"] for r in raw if r["repository"] == key[0]}
        names(receipt["ids"], "scoped receipt IDs")
        need(set(receipt["ids"]) == expected_ids, "scoped source inventory omission")
        fields(receipt["pagination"], "pages_read items_seen exhausted", "scoped pagination")
        pg = receipt["pagination"]
        need(type(pg["pages_read"]) is int and pg["pages_read"] > 0 and type(pg["items_seen"]) is int and
             pg["items_seen"] == len(expected_ids) and pg["exhausted"] is True and receipt["read_status"] == "ok",
             "incomplete scoped source read/pagination")
        observed = ep.utc(receipt["observed_at"])
        need(timedelta(0) <= at - observed < timedelta(minutes=15) and observed <= ep.utc(snapshot["observed_at"]), "stale/future scoped source")
        need(isinstance(receipt["provenance"], str) and receipt["provenance"].strip(), "authenticated collection provenance required")
        for row in records:
            if "observed_at" in row:
                row_time = ep.utc(row["observed_at"])
                need(timedelta(0) <= at - row_time < timedelta(minutes=15) and row_time <= observed, "stale/future scoped record")
        times[key] = observed
    required = set(sources_for[binding["operation"]])
    if task["status"] in {"in_review", "validated"} and binding["operation"] == "implementation":
        required.add("reviews")
    # Branch/PR exclusion proof always needs full raw enumeration, including
    # when the older read-only route could safely omit branch coverage.
    required |= {"branches", "prs"}
    need(all((rr, kind) in times for rr in scope["base_heads"] for kind in required), "missing scoped source receipt")
    need(not overlaps, "overlapping or unresolved source: " + ", ".join(sorted(set(overlaps))))
    need(set(scope["task_ids"]) == {b["id"] for b in snapshot["board"]}, "scoped board/task mismatch")
    for dependency in snapshot["tasks"]:
        if dependency["id"] == binding["task_id"]:
            continue
        board = next(b for b in snapshot["board"] if b["id"] == dependency["id"])
        need(all(board[k] == dependency[k] for k in ("repository", "head_sha", "status", "owner_id")),
             "relevant dependency board/task reconciliation required")
        need(dependency["owner_id"] is None and dependency["status"] in {"merged", "validated", "closed"},
             "relevant dependency task/board ownership or unfinished state retained: " + dependency["id"])
    for row in snapshot["owners"]:
        if row["task_id"] != binding["task_id"] and row["state"] != "released":
            raise ScopeError("relevant dependency owner retained: " + row["id"])
    for row in snapshot["queue"]:
        if row["task_id"] != binding["task_id"]:
            raise ScopeError("relevant dependency queue retained: " + row["id"])
    for row in snapshot["blockers"]:
        if row["task_id"] not in {binding["task_id"], "*"}:
            raise ScopeError("relevant dependency hold retained: " + row["id"])
    return {"binding": binding, "inventory_digest": source_digest,
            "scope_digest": ep.digest(scope), "accounted_source_ids": sorted(accounted),
            "expires_at": min(times[rr, kind] for rr in scope["base_heads"] for kind in required) + timedelta(minutes=15)}
