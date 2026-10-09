"""Read-only coordinator decisions over a validated, explicitly scoped snapshot.

This module does not collect facts, dispatch, write state, or confer permission.
The collector must supply fresh authenticated observations; see RUNBOOK.md.
"""
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone

VERSION = 1
MAX_AGE = timedelta(minutes=15)
OPERATIONS = ("admission", "implementation", "verification", "upload", "merge", "deploy")
TABLES = ("policies", "board", "tasks", "prs", "branches", "reviews", "checks",
          "requests", "owners", "queue", "blockers", "executors")
FROZEN = {"shuto", "neon-drift"}
# Incomplete acceptance evidence must not stop independently authorized coding
# or admission. It still forbids a global idle conclusion.
BASE_SOURCES = set(TABLES) - {"reviews", "checks"}
SOURCES_FOR = {op: BASE_SOURCES | ({"reviews", "checks"} if op == "merge" else
                                  {"reviews"} if op == "verification" else set())
               for op in OPERATIONS}
# Independently pinned read-only review does not mutate branch ownership or
# source. Unreconciled branches remain warnings and still gate all mutations.
SOURCES_FOR["verification"] = (BASE_SOURCES - {"branches"}) | {"reviews"}
SHA = re.compile(r"[0-9a-f]{40}\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")


class InputError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InputError(message)


def fields(value, names, where, optional=""):
    required = set(names.split())
    allowed = required | set(optional.split())
    require(isinstance(value, dict) and required <= set(value) <= allowed,
            f"{where}: expected fields {names}" + (f"; optional {optional}" if optional else ""))


def strings(value, where, allowed=None, nonempty=False):
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value),
            f"{where}: expected string list")
    require(len(value) == len(set(value)), f"{where}: duplicate IDs")
    require(not nonempty or value, f"{where}: empty")
    require(allowed is None or set(value) <= set(allowed), f"{where}: unknown value")


def utc(value):
    require(isinstance(value, str), "timestamp must be UTC text")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InputError("invalid timestamp") from exc
    require(dt.tzinfo is not None and dt.utcoffset() == timedelta(0),
            "timestamp must have explicit UTC timezone")
    return dt


def sha(value):
    require(isinstance(value, str) and SHA.fullmatch(value), "full lowercase SHA required")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()


def _requirements(value):
    require(isinstance(value, dict) and set(value) <= set(OPERATIONS), "invalid requirements")
    for req in value.values():
        fields(req, "capabilities model effort runtime_confirmation_required", "requirements")
        strings(req["capabilities"], "capabilities", nonempty=True)
        for key in ("model", "effort"):
            require(req[key] is None or isinstance(req[key], str) and req[key], f"invalid {key}")
        require(type(req["runtime_confirmation_required"]) is bool, "invalid confirmation requirement")


def validate(snapshot, at):
    """Validate shape and cross-accounting. Incomplete reads are scoped warnings.

    A source's IDs must equal its normalized records, even for partial reads.
    The reader's pagination receipts are evidence, not a boolean 'complete' flag.
    No finite manifest can prove an undisclosed outside source does not exist.
    """
    require(isinstance(at, datetime) and at.tzinfo is not None and
            at.utcoffset() == timedelta(0), "evaluation clock must be UTC")
    fields(snapshot, "version observed_at repositories sources " + " ".join(TABLES), "snapshot")
    require(type(snapshot["version"]) is int and snapshot["version"] == VERSION, "unsupported version")
    observed = utc(snapshot["observed_at"])
    require(observed <= at, "snapshot is future-dated")
    require(isinstance(snapshot["repositories"], dict) and snapshot["repositories"], "repository scope required")
    repos = snapshot["repositories"]
    for repo, head in repos.items():
        require(REPOSITORY.fullmatch(repo), "invalid repository scope")
        sha(head)
    index = {}
    for table in TABLES:
        require(isinstance(snapshot[table], list), f"{table}: list required")
        index[table] = {}
        for record in snapshot[table]:
            require(isinstance(record, dict), f"{table}: record required")
            rid, repo = record.get("id"), record.get("repository")
            require(isinstance(rid, str) and rid and rid != "*" and rid not in index[table], f"{table}: invalid/duplicate ID")
            require(table != "tasks" or not rid.startswith("request:"), "reserved admission task ID")
            require(repo in repos, f"{table}/{rid}: wrong repository")
            index[table][rid] = record
    for row in snapshot["policies"]:
        fields(row, "id repository triggers_checked push_runs_actions push_deploys merge_runs_actions merge_deploys", "policy")
        require(all(type(row[k]) is bool for k in row if k not in ("id", "repository")), "policy flags must be booleans")
    for table in ("board", "tasks"):
        for row in snapshot[table]:
            names = "id repository head_sha status owner_id"
            if table == "tasks":
                names += " project author_id needs criteria required_checks requirements"
            fields(row, names, table)
            sha(row["head_sha"])
            require(row["owner_id"] is None or isinstance(row["owner_id"], str) and row["owner_id"], "invalid owner")
            require(row["status"] in {"open", "in_progress", "in_review", "validated", "rejected", "blocked", "merged", "closed", "cancelled", "paused", "done-pending-verdict", "unknown"}, "unknown task status")
            if table == "tasks":
                require(isinstance(row["project"], str) and row["project"], "project required")
                require(isinstance(row["author_id"], str) and row["author_id"], "author required")
                strings(row["needs"], "task needs", OPERATIONS[1:])
                strings(row["criteria"], "acceptance criteria", nonempty=True)
                strings(row["required_checks"], "required checks", nonempty=True)
                _requirements(row["requirements"])
    for row in snapshot["prs"]:
        fields(row, "id repository task_id head_sha author_id state review_ids check_ids", "PR")
        sha(row["head_sha"])
        require(re.fullmatch(re.escape(row["repository"]) + r"#[1-9][0-9]*", row["id"]), "PR ID must include correct repository")
        require(row["state"] in {"open", "merged", "closed"}, "invalid PR state")
        require(isinstance(row["author_id"], str) and row["author_id"], "PR author required")
        strings(row["review_ids"], "PR review IDs")
        strings(row["check_ids"], "PR check IDs")
    for row in snapshot["branches"]:
        fields(row, "id repository task_id head_sha", "branch")
        sha(row["head_sha"])
    for table in ("reviews", "checks"):
        for row in snapshot[table]:
            names = "id repository task_id pr_id head_sha observed_at"
            names += " reviewer_id verdict criteria" if table == "reviews" else " name result"
            fields(row, names, table, optional="performed_at")
            sha(row["head_sha"])
            row_observed = utc(row["observed_at"])
            require(row_observed <= observed, f"{table} observation exceeds snapshot time")
            if row.get("performed_at") is not None:
                require(utc(row["performed_at"]) <= row_observed, f"{table} performance time exceeds observation")
            if table == "checks":
                require(isinstance(row["name"], str) and row["name"] and row["result"] in {"pass", "fail", "pending"}, "invalid check")
            else:
                require(isinstance(row["reviewer_id"], str) and row["reviewer_id"], "reviewer required")
                require(row["verdict"] in {"pass", "fail", "pending"}, "invalid verdict")
                require(isinstance(row["criteria"], dict), "criterion map required")
                for criterion in row["criteria"].values():
                    fields(criterion, "result evidence", "criterion")
                    require(criterion["result"] in {"pass", "fail", "pending"} and isinstance(criterion["evidence"], str), "invalid criterion")
    for row in snapshot["requests"]:
        fields(row, "id repository task_id project operations executors kind state authority_verified evidence", "request")
        require(isinstance(row["project"], str) and row["project"], "request project scope required")
        require(row["task_id"] is not None or row["project"] != "*", "unfiled ask needs explicit project scope")
        strings(row["operations"], "request operations", OPERATIONS, nonempty=True)
        strings(row["executors"], "request executors", nonempty=True)
        require(row["kind"] in {"ask", "explicit", "standing"} and row["state"] in {"active", "cancelled"}, "invalid request")
        require(type(row["authority_verified"]) is bool and isinstance(row["evidence"], str) and row["evidence"], "request authority evidence required")
        require(row["task_id"] is not None or row["kind"] == "ask", "only an unfiled ask may omit task")
    for row in snapshot["owners"]:
        fields(row, "id repository task_id operation owner_id executor_id state", "owner")
        require(row["operation"] in OPERATIONS and row["state"] in {"active", "reserved", "unknown", "released"}, "invalid ownership")
        require(isinstance(row["owner_id"], str) and row["owner_id"], "owner identity required")
    for row in snapshot["queue"]:
        fields(row, "id repository task_id operation executor_id owner_id head_sha state", "queue")
        sha(row["head_sha"])
        require(row["operation"] in OPERATIONS and row["state"] in {"pending", "running"}, "invalid queued operation")
        require(isinstance(row["owner_id"], str) and row["owner_id"], "queue owner required")
    for row in snapshot["blockers"]:
        fields(row, "id repository task_id operations executors kind reason", "blocker")
        strings(row["operations"], "blocker operations", (*OPERATIONS, "*"), nonempty=True)
        strings(row["executors"], "blocker executors", nonempty=True)
        require(row["kind"] in {"hold", "capacity", "stop", "cancelled", "denial", "security"}, "invalid blocker kind")
        require(isinstance(row["reason"], str) and row["reason"], "blocker reason required")
        # A denied action cannot be retried through a different provider.
        if row["kind"] in {"denial", "security", "stop", "cancelled"}:
            require(row["executors"] == ["*"], "hard stops/denials must retain cross-executor scope")
    for row in snapshot["executors"]:
        fields(row, "id repository owner_id kind state capabilities observed_model observed_effort runtime_confirmed resume_task", "executor", optional="selected_model selected_effort selection_verified selection_evidence")
        require(row["kind"] in {"native", "codex", "claude"}, "unsupported executor (external agent contact not admitted)")
        require(row["state"] in {"available", "busy", "unavailable", "unknown"}, "invalid capacity")
        require(isinstance(row["owner_id"], str) and row["owner_id"], "executor owner required")
        strings(row["capabilities"], "executor capabilities")
        require(type(row["runtime_confirmed"]) is bool, "runtime confirmation must be boolean")
        for key in ("observed_model", "observed_effort"):
            require(row[key] is None or isinstance(row[key], str) and row[key], "invalid observed setup")
        require(not row["runtime_confirmed"] or row["observed_model"] is not None and row["observed_effort"] is not None, "confirmed runtime needs observed model and effort")
        selection_keys = {"selected_model", "selected_effort", "selection_verified", "selection_evidence"}
        if selection_keys.intersection(row):
            require(selection_keys <= set(row), "selection record must include model, effort, verification and evidence")
            require(type(row["selection_verified"]) is bool and isinstance(row["selection_evidence"], str), "invalid selection verification")
            for key in ("selected_model", "selected_effort"):
                require(row[key] is None or isinstance(row[key], str) and row[key], "invalid selected setup")
            require(not row["selection_verified"] or row["selected_model"] and row["selected_effort"] and row["selection_evidence"].strip(), "verified selection needs exact supported setup and evidence")
    # Unfiled asks have stable admission identities too, so they can retain
    # their own owner/queue/hold rather than forcing a global admission stop.
    task_scopes = {r["id"]: r["repository"] for r in snapshot["tasks"]}
    task_scopes.update({"request:" + r["id"]: r["repository"] for r in snapshot["requests"] if r["task_id"] is None})
    # Cross-references are repository-qualified, not short IDs or SHA prefixes.
    for table in ("prs", "branches", "reviews", "checks", "owners", "queue", "blockers", "requests"):
        for row in snapshot[table]:
            tid = row["task_id"]
            if tid is None and table in {"requests", "branches"} or tid == "*" and table in {"requests", "blockers"}:
                continue
            scopes = task_scopes if table in {"owners", "queue", "blockers", "requests"} else {k: v["repository"] for k, v in index["tasks"].items()}
            require(tid in scopes and scopes[tid] == row["repository"], f"{table}: unknown/wrong-repository task")
    for table in ("owners", "queue"):
        for row in snapshot[table]:
            ex = index["executors"].get(row["executor_id"])
            require(ex and ex["repository"] == row["repository"] and ex["owner_id"] == row["owner_id"], f"{table}: unknown/conflicting executor")
    for row in snapshot["executors"]:
        require(row["resume_task"] is None or row["resume_task"] in task_scopes and task_scopes[row["resume_task"]] == row["repository"], "invalid resume task")
    for table in ("requests", "blockers"):
        for row in snapshot[table]:
            require(all(e == "*" or e in index["executors"] and index["executors"][e]["repository"] == row["repository"] for e in row["executors"]), "unknown/wrong-repository executor scope")
    for table in ("reviews", "checks"):
        for row in snapshot[table]:
            pr = index["prs"].get(row["pr_id"])
            require(pr and pr["repository"] == row["repository"] and pr["task_id"] == row["task_id"], f"{table}: wrong PR/task/repository")
    for pr in snapshot["prs"]:
        for table, key in (("reviews", "review_ids"), ("checks", "check_ids")):
            require(set(pr[key]) == {r["id"] for r in snapshot[table] if r["pr_id"] == pr["id"]}, f"PR {table} inventory omission")
    require(isinstance(snapshot["sources"], list), "source manifest required")
    sources, warnings, seen = {}, [], set()
    for src in snapshot["sources"]:
        fields(src, "id kind repository source_repository ref_sha observed_at read_status pagination ids", "source")
        require(isinstance(src["id"], str) and src["id"] and src["id"] not in seen, "duplicate/invalid source ID")
        seen.add(src["id"])
        key = (src["repository"], src["kind"])
        require(src["kind"] in TABLES and src["repository"] in repos and src["source_repository"] in repos and key not in sources, "duplicate/unknown source scope")
        sha(src["ref_sha"])
        require(src["ref_sha"] == repos[src["source_repository"]], "source pin disagrees with repository scope")
        dt = utc(src["observed_at"])
        require(dt <= observed, "source observation exceeds snapshot time")
        require(src["read_status"] in {"ok", "unreadable", "partial"}, "invalid read status")
        fields(src["pagination"], "pages_read items_seen exhausted", "pagination")
        pg = src["pagination"]
        require(type(pg["pages_read"]) is int and pg["pages_read"] >= 0 and type(pg["items_seen"]) is int and pg["items_seen"] >= 0 and type(pg["exhausted"]) is bool, "invalid pagination receipt")
        strings(src["ids"], "source IDs")
        expected = {r["id"] for r in snapshot[src["kind"]] if r["repository"] == src["repository"]}
        problems = []
        if set(src["ids"]) != expected or pg["items_seen"] != len(src["ids"]):
            problems.append("inventory accounting mismatch")
        if src["read_status"] != "ok" or not pg["exhausted"] or pg["pages_read"] < 1:
            problems.append("incomplete read/pagination")
        if at - dt >= MAX_AGE:
            problems.append("stale observation")
        sources[key] = (not problems, dt)
        warnings.extend(f"{src['repository']}:{src['kind']}: {p}" for p in problems)
    for repo in repos:
        for table in TABLES:
            if (repo, table) not in sources:
                sources[repo, table] = (False, observed)
                warnings.append(f"{repo}:{table}: missing source manifest")
        if len([p for p in snapshot["policies"] if p["repository"] == repo]) != 1:
            sources[repo, "policies"] = (False, observed)
            warnings.append(f"{repo}: exactly one current policy record required")
        board = {r["id"] for r in snapshot["board"] if r["repository"] == repo}
        tasks = {r["id"] for r in snapshot["tasks"] if r["repository"] == repo}
        if board != tasks:
            sources[repo, "tasks"] = (False, observed)
            warnings.append(f"{repo}: board/task inventory mismatch")
    # A fresh aggregate receipt cannot launder an expired individual read.
    # Immutable evidence may have been performed long ago; observed_at is the
    # fresh read/applicability check and is deliberately distinct.
    receipt_times = {key: value[1] for key, value in sources.items()}
    for table in ("reviews", "checks"):
        for row in snapshot[table]:
            key = (row["repository"], table)
            valid, source_time = sources[key]
            row_time = utc(row["observed_at"])
            require(row_time <= receipt_times[key], f"{table} observation exceeds source receipt")
            if at - row_time >= MAX_AGE:
                valid = False
                warnings.append(f"{row['repository']}:{table}:{row['id']}: stale record observation")
            sources[key] = (valid, min(source_time, row_time))
    if at - observed >= MAX_AGE:
        warnings.append("stale snapshot")
    return index, sources, warnings


def acceptance(task, pr, snapshot):
    """Independent acceptance at the exact current source head, never a prefix."""
    reviews = [r for r in snapshot["reviews"] if r["pr_id"] == pr["id"] and r["head_sha"] == pr["head_sha"]]
    authors = {task["author_id"], pr["author_id"], task["owner_id"]} | {o["owner_id"] for o in snapshot["owners"] if o["task_id"] == task["id"] and o["operation"] == "implementation" and o["state"] != "released"}
    independent = [r for r in reviews if r["reviewer_id"] not in authors]
    failed = any(r["verdict"] == "fail" or any(c["result"] == "fail" for c in r["criteria"].values()) for r in independent)
    passed = any(r["verdict"] == "pass" and set(r["criteria"]) == set(task["criteria"]) and all(c["result"] == "pass" and c["evidence"].strip() for c in r["criteria"].values()) for r in independent)
    checks = [c for c in snapshot["checks"] if c["pr_id"] == pr["id"] and c["head_sha"] == pr["head_sha"]]
    checks_pass = all(any(c["name"] == name and c["result"] == "pass" for c in checks) and not any(c["name"] == name and c["result"] != "pass" for c in checks) for name in task["required_checks"])
    return passed and not failed and checks_pass, failed, passed and failed


def evaluate(snapshot, at):
    """Return every permitted alternative, scoped blockers, and coverage warnings."""
    result = {"version": VERSION, "status": "INPUT_REQUIRED", "actions": [], "blocked": [], "warnings": [], "reconciliations": []}
    try:
        index, sources, warnings = validate(snapshot, at)
        result["input_digest"] = digest(snapshot)
    except (InputError, TypeError, ValueError) as exc:
        result["warnings"] = [str(exc)]
        return result
    result["warnings"] = warnings
    opportunities = []
    for task in snapshot["tasks"]:
        repo, tid = task["repository"], task["id"]
        task_prs = [p for p in snapshot["prs"] if p["task_id"] == tid]
        prs = [p for p in task_prs if p["state"] == "open"]
        if task["status"] == "unknown":
            warnings.append(f"{tid}: unknown task state")
            continue
        if task["status"] in {"closed", "cancelled", "paused", "done-pending-verdict"}:
            continue
        terminal_prs = [p for p in task_prs if p["state"] in {"merged", "closed"} and p["head_sha"] == task["head_sha"]]
        if terminal_prs and task["status"] != "merged":
            warnings.append(f"{tid}: same-head terminal PR requires task reconciliation")
            continue
        if task["status"] == "merged" and prs:
            warnings.append(f"{tid}: merged task conflicts with an open PR")
            continue
        if len(prs) > 1 or prs and prs[0]["head_sha"] != task["head_sha"]:
            warnings.append(f"{tid}: contradictory current task/PR heads")
            continue
        pr = prs[0] if prs else None
        if task["status"] == "merged" and "verification" in task["needs"]:
            merged_sources = [p for p in task_prs if p["state"] == "merged" and p["head_sha"] == task["head_sha"]]
            if len(merged_sources) == 1:
                pr = merged_sources[0]
            else:
                warnings.append(f"{tid}: post-merge verification needs one exact merged PR source")
        observed_heads = {snapshot["repositories"][repo]} | {b["head_sha"] for b in snapshot["branches"] if b["task_id"] == tid}
        if pr:
            observed_heads.add(pr["head_sha"])
        if task["head_sha"] not in observed_heads:
            warnings.append(f"{tid}: source head not corroborated by repository/branch/PR")
            continue
        if task["status"] == "blocked" and (not task["needs"] or not any(b["task_id"] in {tid, "*"} and b["repository"] == repo for b in snapshot["blockers"])):
            warnings.append(f"{tid}: blocked task lacks operation accounting")
            continue
        accepted, rejected, conflicting = acceptance(task, pr, snapshot) if pr else (False, False, False)
        if conflicting:
            warnings.append(f"{tid}: contradictory same-head review verdicts")
            continue
        board = index["board"].get(tid)
        if board and (board["status"] in {"cancelled", "paused", "done-pending-verdict"} or
                      board["status"] in {"closed", "merged"} and board["head_sha"] == task["head_sha"] and board["status"] != task["status"]):
            warnings.append(f"{tid}: board stop/terminal state requires reconciliation")
            continue
        if board and (board["status"] != task["status"] or board["head_sha"] != task["head_sha"]):
            result["reconciliations"].append({"task_id": tid, "head_sha": task["head_sha"], "reason": "exact source task/PR facts supersede stale board descriptions; holds unchanged"})
        needs = set(task["needs"])
        if task["status"] == "merged" and "implementation" in needs:
            warnings.append(f"{tid}: merged task cannot restart implementation without reconciliation")
            needs.remove("implementation")
        if task["status"] != "merged" and (task["status"] in {"open", "in_progress", "rejected"} or rejected):
            needs.add("implementation")
        if task["status"] in {"in_review", "validated"} and not rejected:
            needs.add("merge" if accepted else "verification")
        if task["status"] in {"in_review", "validated"} and not pr:
            warnings.append(f"{tid}: review state has no current open PR")
        for operation in OPERATIONS:
            if operation in needs:
                opportunities.append((tid, repo, task["head_sha"], operation, task, pr, accepted))
    for request in snapshot["requests"]:
        if request["task_id"] is None and request["state"] == "active":
            opportunities.append(("request:" + request["id"], request["repository"], snapshot["repositories"][request["repository"]], "admission", None, None, False))
    for branch in snapshot["branches"]:
        if branch["task_id"] is None:
            warnings.append(f"{branch['repository']}:{branch['id']}: branch not reconciled to a task")
            key = (branch["repository"], "branches")
            sources[key] = (False, sources[key][1])
    for queued in snapshot["queue"]:
        queued_task = index["tasks"].get(queued["task_id"])
        expected_head = queued_task["head_sha"] if queued_task else snapshot["repositories"][queued["repository"]]
        if queued["head_sha"] != expected_head:
            warnings.append(f"{queued['task_id']}: queued source head changed; reservation retained")
    for owner in snapshot["owners"]:
        if owner["state"] == "unknown":
            warnings.append(f"{owner['task_id']}: ownership unknown")
    for request in snapshot["requests"]:
        if request["state"] == "active" and not request["authority_verified"]:
            warnings.append(f"{request['id']}: request authority unverified")
    for ex in snapshot["executors"]:
        if ex["state"] == "unknown":
            warnings.append(f"{ex['id']}: capacity unknown")
    for tid, repo, head, operation, task, pr, accepted in opportunities:
        for ex in [e for e in snapshot["executors"] if e["repository"] == repo]:
            reasons = []
            # Complete safety/ownership scope is mandatory. Acceptance-only
            # unknowns do not block separately authorized implementation/admission.
            required_sources = SOURCES_FOR[operation]
            if task and task["status"] in {"in_review", "validated"} and operation == "implementation":
                required_sources = required_sources | {"reviews"}
            missing = sorted(kind for kind in required_sources if not sources[repo, kind][0])
            if missing:
                reasons.append("INPUT_REQUIRED: " + ",".join(missing))
            project = task["project"] if task else next(r["project"] for r in snapshot["requests"] if tid == "request:" + r["id"])
            repo_name = repo.rsplit("/", 1)[-1].lower()
            if project in FROZEN or repo_name in FROZEN or repo_name.startswith("shuto-"):
                reasons.append("PROJECT_FROZEN")
            if task and tid == "td-054" and operation == "implementation":
                reasons.append("EXPLICIT_NO_REDISPATCH")
            if pr and pr["id"].endswith("#253") and operation == "merge":
                reasons.append("PRESERVATION_PR_HOLD")
            if ex["state"] != "available":
                reasons.append("CAPACITY_" + ex["state"].upper())
            req = task["requirements"].get(operation) if task else {"capabilities": ["admission"], "model": None, "effort": None, "runtime_confirmation_required": False}
            if req is None:
                reasons.append("INPUT_REQUIRED: operation requirements")
                warnings.append(f"{tid}:{operation}: requirements missing")
            else:
                if not set(req["capabilities"]) <= set(ex["capabilities"]):
                    reasons.append("MISSING_CAPABILITY")
                if req["runtime_confirmation_required"] and not ex["runtime_confirmed"]:
                    reasons.append("RUNTIME_UNCONFIRMED")
                    warnings.append(f"{tid}:{ex['id']}: runtime unconfirmed")
                setup_required = any(req[k] is not None for k in ("model", "effort"))
                # Confirmed runtime evidence wins over selected settings. When
                # attestation is not required, a verified supported selection
                # can establish admission readiness without inventing runtime ID.
                prefix = "observed_" if ex["runtime_confirmed"] else "selected_"
                setup_verified = ex["runtime_confirmed"] or (not req["runtime_confirmation_required"] and ex.get("selection_verified", False))
                if setup_required and not setup_verified:
                    reasons.append("INPUT_REQUIRED: setup selection/runtime evidence")
                    warnings.append(f"{tid}:{ex['id']}: required setup readiness unknown")
                elif setup_required and any(req[k] is not None and req[k] != ex.get(prefix + k) for k in ("model", "effort")):
                    reasons.append("REQUIRED_SETUP_MISMATCHED")
            matches = [r for r in snapshot["requests"] if r["repository"] == repo and r["project"] in {project, "*"} and (r["task_id"] in {tid, "*"} or tid == "request:" + r["id"])]
            authorized = [r for r in matches if r["state"] == "active" and r["authority_verified"] and operation in r["operations"] and ("*" in r["executors"] or ex["id"] in r["executors"])]
            if not authorized:
                reasons.append("NO_AUTHORIZATION")
            if any(r["state"] == "cancelled" and operation in r["operations"] for r in matches):
                reasons.append("USER_CANCELLED")
            for block in snapshot["blockers"]:
                if block["repository"] == repo and block["task_id"] in {tid, "*"} and (operation in block["operations"] or "*" in block["operations"]) and (ex["id"] in block["executors"] or "*" in block["executors"]):
                    reasons.append(f"{block['kind'].upper()}:{block['id']}:{block['reason']}")
            owners = [o for o in snapshot["owners"] if o["task_id"] == tid and o["state"] != "released"]
            relevant_owners = [o for o in owners if o["operation"] == operation]
            if len({(o["owner_id"], o["executor_id"]) for o in relevant_owners}) > 1:
                reasons.append("OWNERSHIP_CONFLICT")
            if any(o["state"] == "unknown" or o["owner_id"] != ex["owner_id"] or o["executor_id"] != ex["id"] or ex["resume_task"] != tid for o in relevant_owners):
                reasons.append("ALREADY_OWNED_OR_OWNERSHIP_UNKNOWN")
            if operation == "implementation" and task and task["owner_id"] and (task["owner_id"] != ex["owner_id"] or ex["resume_task"] != tid):
                reasons.append("TASK_OWNER_RESERVED")
            if board := index["board"].get(tid):
                if board["owner_id"] != (task or {}).get("owner_id"):
                    reasons.append("OWNERSHIP_RECONCILIATION_REQUIRED")
            if any(o["executor_id"] == ex["id"] and o["task_id"] != tid and o["state"] != "released" for o in snapshot["owners"]):
                reasons.append("EXECUTOR_OWNS_OTHER_TASK")
            if any(q["task_id"] == tid and q["operation"] == operation for q in snapshot["queue"]):
                reasons.append("OPERATION_ALREADY_QUEUED")
            if any(q["executor_id"] == ex["id"] for q in snapshot["queue"]):
                reasons.append("EXECUTOR_ALREADY_QUEUED")
            if operation == "verification" and task and ex["owner_id"] in ({task["author_id"], task["owner_id"], (pr or {}).get("author_id")} | {o["owner_id"] for o in owners if o["operation"] == "implementation"}):
                reasons.append("INDEPENDENT_REVIEW_REQUIRED")
            if operation == "verification" and pr is None:
                reasons.append("INPUT_REQUIRED: exact review source")
            if operation == "merge" and (not pr or pr["state"] != "open" or task["status"] == "merged" or not accepted):
                reasons.append("EXACT_HEAD_ACCEPTANCE_REQUIRED")
            policy = next((p for p in snapshot["policies"] if p["repository"] == repo), None)
            if operation in {"upload", "merge"} and (not policy or not policy["triggers_checked"] or policy[("push" if operation == "upload" else "merge") + "_runs_actions"] or policy[("push" if operation == "upload" else "merge") + "_deploys"]):
                reasons.append("TRIGGER_OR_PUBLICATION_HOLD")
            if operation == "deploy":
                # Deployment remains outside this read-only coordinator's dispatch
                # capabilities, even with a recorded request. Use the release flow.
                reasons.append("DEPLOY_REQUIRES_SEPARATE_EXPLICIT_REQUEST_FLOW")
            binding = {"task_id": tid, "repository": repo, "operation": operation,
                       "executor_id": ex["id"], "owner_id": ex["owner_id"], "head_sha": head}
            if reasons:
                warnings.extend(f"{tid}:{operation}:{ex['id']}: {reason}" for reason in reasons if reason.startswith("INPUT_REQUIRED:"))
                unresolved = {"OWNERSHIP_CONFLICT", "OWNERSHIP_RECONCILIATION_REQUIRED"}
                if unresolved.intersection(reasons):
                    warnings.append(f"{tid}:{operation}:{ex['id']}: ownership reconciliation required")
                result["blocked"].append({**binding, "reasons": sorted(set(reasons))})
                continue
            expiry = min(sources[repo, k][1] for k in required_sources) + MAX_AGE
            decision = {**binding, "input_digest": result["input_digest"], "expires_at": expiry.isoformat(),
                        "authorization_ids": sorted(r["id"] for r in authorized)}
            decision["decision_id"] = digest(decision)
            result["actions"].append(decision)
    result["warnings"] = sorted(set(warnings))
    result["status"] = "ACTION_REQUIRED" if result["actions"] else "INPUT_REQUIRED" if warnings else "IDLE"
    return result


def revalidate(snapshot, decision, target, at):
    """A decision is an expiring receipt, not a reusable bearer permission."""
    result = evaluate(snapshot, at)
    if not isinstance(target, dict):
        return {"status": "NO_GO", "reason": "target required", "evaluation": result}
    match = next((a for a in result["actions"] if a == decision and all(a.get(k) == v for k, v in target.items())), None)
    required = {"task_id", "operation", "executor_id", "owner_id", "head_sha"}
    if set(target) != required or match is None:
        return {"status": "NO_GO", "reason": "missing, changed, expired or wrong-target decision", "evaluation": result}
    return {"status": "GO", "decision": match, "evaluation": result}
