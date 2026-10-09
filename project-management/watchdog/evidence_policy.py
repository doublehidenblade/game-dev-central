"""Deterministic, read-only evidence gates. No I/O, clock reads or state changes.

The caller owns authenticated collection of the *authority* argument. A worker
submission cannot choose current rules, task scope, stops, or reviewer identity.
Raw Git objects prove immutable commit/tree/path/blob membership, not the truth
of an author's claims. Independent inspected verdicts remain mandatory.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import json
import re
from datetime import datetime, timedelta

VERSION = 1
MAX_AGE = timedelta(minutes=15)
SHA = re.compile(r"[0-9a-f]{40}\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
STOPPED = {"paused", "cancelled", "abandoned", "closed", "done-pending-verdict"}


class PolicyError(ValueError):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}")


def require(test, code, detail):
    if not test:
        raise PolicyError(code, detail)


def fields(value, required, where, optional=""):
    names, opt = set(required.split()), set(optional.split())
    require(isinstance(value, dict) and names <= set(value) <= names | opt,
            "MALFORMED", f"{where}: expected {required}; optional {optional}")


def text(value, where):
    require(isinstance(value, str) and bool(value.strip()), "MALFORMED", f"{where}: nonempty text required")


def strings(value, where, nonempty=True):
    require(isinstance(value, list) and (not nonempty or bool(value)), "MALFORMED", f"{where}: list required")
    for x in value:
        text(x, where)
    require(len(set(value)) == len(value), "MALFORMED", f"{where}: duplicate value")


def full_sha(value):
    require(isinstance(value, str) and SHA.fullmatch(value), "UNPINNED", "full lowercase Git SHA required")


def utc(value):
    require(isinstance(value, str), "MALFORMED", "UTC timestamp required")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PolicyError("MALFORMED", "invalid timestamp") from exc
    require(dt.tzinfo is not None and dt.utcoffset() == timedelta(0), "MALFORMED", "explicit UTC required")
    return dt


def fresh(value, at):
    observed = utc(value)
    require(timedelta(0) <= at - observed <= MAX_AGE, "STALE_READ", "authority/receipt collection must be current")


def digest(value):
    try:
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise PolicyError("MALFORMED", "JSON-compatible finite input required") from exc
    return hashlib.sha256(raw).hexdigest()


def load_json(raw):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, "MALFORMED", "duplicate JSON key")
            result[k] = v
        return result
    def constant(_):
        raise PolicyError("MALFORMED", "non-finite JSON")
    try:
        return json.loads(raw, object_pairs_hook=unique, parse_constant=constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PolicyError("MALFORMED", "invalid UTF-8 JSON document") from exc


def path_parts(path):
    text(path, "path")
    parts = path.split("/")
    require(all(p not in ("", ".", "..") and "\x00" not in p and "\\" not in p for p in parts),
            "UNSAFE_PATH", "repository-relative regular path required")
    return parts


def ref_key(ref):
    fields(ref, "repository commit path blob", "citation")
    require(isinstance(ref["repository"], str) and REPOSITORY.fullmatch(ref["repository"]), "MALFORMED", "repository required")
    full_sha(ref["commit"])
    full_sha(ref["blob"])
    path_parts(ref["path"])
    return (ref["repository"], ref["commit"], ref["path"], ref["blob"])


class GitObjects:
    """Offline content-addressed proof, including the commit-to-tree link.

    objects[repository][sha] = {type: blob|tree|commit, base64: raw Git payload}.
    These are payload bytes (without the ``type size\\0`` hashing header).
    A named path or a collector's boolean is never proof of committed content.
    """
    def __init__(self, objects):
        require(isinstance(objects, dict), "MALFORMED", "object database required")
        self.objects = objects

    def read(self, repository, sha, kind):
        full_sha(sha)
        entry = self.objects.get(repository, {}).get(sha)
        require(entry is not None, "INACCESSIBLE_OBJECT", f"missing {kind} {repository}@{sha}")
        fields(entry, "type base64", "Git object")
        require(entry["type"] == kind, "OBJECT_TYPE", f"expected {kind}")
        try:
            raw = base64.b64decode(entry["base64"], validate=True)
        except (ValueError, TypeError, binascii.Error) as exc:
            raise PolicyError("MALFORMED", "invalid object encoding") from exc
        actual = hashlib.sha1(kind.encode() + b" " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        require(actual == sha, "OBJECT_HASH", f"unverified {kind} bytes")
        return raw

    def commit(self, repository, sha):
        raw = self.read(repository, sha, "commit")
        header = raw.split(b"\n\n", 1)[0].splitlines()
        trees = [x[5:].decode("ascii", "replace") for x in header if x.startswith(b"tree ")]
        parents = [x[7:].decode("ascii", "replace") for x in header if x.startswith(b"parent ")]
        require(len(trees) == 1, "MALFORMED", "commit must name one tree")
        for item in trees + parents:
            full_sha(item)
        return trees[0], parents

    def tree(self, repository, sha):
        raw = self.read(repository, sha, "tree")
        entries = {}
        while raw:
            try:
                prefix, remainder = raw.split(b"\x00", 1)
                mode, name = prefix.split(b" ", 1)
                name = name.decode("utf-8")
                require(len(remainder) >= 20, "MALFORMED", "short tree entry")
                oid, raw = remainder[:20].hex(), remainder[20:]
            except (ValueError, UnicodeDecodeError) as exc:
                raise PolicyError("MALFORMED", "invalid tree object") from exc
            require(len(path_parts(name)) == 1 and name not in entries, "MALFORMED", "duplicate/invalid tree name")
            require(mode in (b"40000", b"100644", b"100755", b"120000", b"160000"), "MALFORMED", "unknown tree mode")
            entries[name] = (mode, oid)
        return entries

    def blob_at(self, repository, commit, path):
        tree, _ = self.commit(repository, commit)
        parts = path_parts(path)
        for i, part in enumerate(parts):
            entries = self.tree(repository, tree)
            require(part in entries, "UNCOMMITTED_PATH", f"{path} not committed at {commit}")
            mode, oid = entries[part]
            if i < len(parts) - 1:
                require(mode == b"40000", "UNSAFE_PATH", "path crosses non-tree")
                tree = oid
            else:
                require(mode in (b"100644", b"100755"), "UNSAFE_PATH", "regular blob required; no symlinks/submodules")
                return oid
        raise PolicyError("UNSAFE_PATH", "empty path")

    def citation(self, ref):
        repository, commit, path, blob = ref_key(ref)
        require(self.blob_at(repository, commit, path) == blob, "BLOB_MISMATCH", f"citation blob differs at {path}")
        raw = self.read(repository, blob, "blob")
        require(bool(raw.strip()), "EMPTY_EVIDENCE", f"empty committed evidence {path}")
        return raw

    def json(self, ref):
        return load_json(self.citation(ref))

    def ancestor(self, repository, before, after):
        pending, seen = [after], set()
        while pending:
            head = pending.pop()
            if head == before:
                self.commit(repository, head)
                return True
            if head not in seen:
                seen.add(head)
                _, parents = self.commit(repository, head)
                pending.extend(parents)
        return False

    def equal_scope(self, repository, before, after, paths):
        strings(paths, "relevant source paths")
        return all(self.blob_at(repository, before, p) == self.blob_at(repository, after, p) for p in paths)


def citations(value, store):
    require(isinstance(value, list) and bool(value), "NO_CITATIONS", "nonempty inspected citations required")
    keys = [ref_key(r) for r in value]
    require(len(keys) == len(set(keys)), "MALFORMED", "duplicate citation")
    for ref in value:
        store.citation(ref)
    return set(keys)


def _authority(authority, objects, at):
    require(isinstance(at, datetime) and at.tzinfo is not None and at.utcoffset() == timedelta(0), "MALFORMED", "evaluation clock must be explicit UTC")
    fields(authority, "version observed_at rule_heads rules task_ref candidate principals owner_id status stopped exclusions attestations findings decisions", "authority")
    require(type(authority["version"]) is int and authority["version"] == VERSION, "MALFORMED", "unsupported version")
    fresh(authority["observed_at"], at)
    store = GitObjects(objects)
    heads, rules = authority["rule_heads"], authority["rules"]
    require(isinstance(heads, dict) and bool(heads), "UNKNOWN_RULES", "current rule head inventory required")
    require(isinstance(rules, list) and bool(rules), "UNKNOWN_RULES", "complete applicable rule inventory required")
    index = {}
    for rule in rules:
        fields(rule, "id ref", "rule")
        text(rule["id"], "rule ID")
        require(rule["id"] not in index, "MALFORMED", "duplicate rule ID")
        ref = rule["ref"]
        ref_key(ref)
        require(heads.get(ref["repository"]) == ref["commit"], "STALE_RULE", "rule is not bound to observed current authoritative head")
        store.citation(ref)
        index[rule["id"]] = ref
    require(set(heads) == {r["ref"]["repository"] for r in rules}, "UNKNOWN_RULES", "unaccounted authoritative rule repository")
    task = store.json(authority["task_ref"])
    require(isinstance(task, dict), "MALFORMED", "task document must be JSON object")
    text(task.get("id"), "task ID")
    inventory = task.get("evidence_rule_inventory")
    require(isinstance(inventory, list) and bool(inventory), "UNKNOWN_RULES", "canonical task must name its complete applicable rule inventory")
    inventory_keys = []
    for rule in inventory:
        fields(rule, "id repository path", "canonical rule inventory")
        inventory_keys.append((rule["id"], rule["repository"], rule["path"]))
    require(len(set(inventory_keys)) == len(inventory_keys) and set(inventory_keys) == {(r["id"], r["ref"]["repository"], r["ref"]["path"]) for r in rules},
            "UNKNOWN_RULES", "authority/acknowledgment cannot narrow canonical applicable rules")
    criteria = task.get("completion_criteria")
    require(isinstance(criteria, list) and bool(criteria), "ZERO_CRITERIA", "no parsed acceptance criteria")
    ids = []
    for c in criteria:
        require(isinstance(c, dict), "MALFORMED", "criterion object required")
        for key in ("id", "criterion", "verification"):
            text(c.get(key), f"criterion {key}")
        ids.append(c["id"])
    require(len(set(ids)) == len(ids), "MALFORMED", "duplicate criterion ID")
    policies = task.get("evidence_policy")
    require(isinstance(policies, dict) and set(policies) == set(ids), "APPLICABILITY_REQUIRED", "explicit policy for every canonical criterion required")
    require(isinstance(authority["exclusions"], dict), "MALFORMED", "exclusions must be authoritative map")
    require(set(authority["exclusions"]) <= set(ids), "MALFORMED", "unknown exclusion criterion")
    for cid, policy in policies.items():
        fields(policy, "applicability rationale rule_id instances source_paths build visual checks", f"policy {cid}")
        text(policy["rationale"], "applicability rationale")
        require(policy["rule_id"] in index, "UNKNOWN_RULE", "applicability rule not current")
        require(policy["applicability"] in ("required", "not_applicable"), "APPLICABILITY_REQUIRED", "explicit applicability required")
        require(type(policy["visual"]) is bool, "MALFORMED", "visual flag must be Boolean")
        strings(policy["instances"], "all claimed instances")
        strings(policy["source_paths"], "relevant source scope")
        for p in policy["source_paths"]:
            path_parts(p)
        require(isinstance(policy["checks"], list), "MALFORMED", "required checks list needed")
        check_ids = set()
        for check in policy["checks"]:
            fields(check, "id command", "required check")
            text(check["id"], "check ID")
            strings(check["command"], "required command")
            require(check["id"] not in check_ids, "MALFORMED", "duplicate check ID")
            check_ids.add(check["id"])
        if policy["build"] is not None:
            fields(policy["build"], "id variant environment", "build binding")
            for key in policy["build"]:
                text(policy["build"][key], "build " + key)
        if policy["applicability"] == "not_applicable":
            exclusion = authority["exclusions"].get(cid)
            require(isinstance(exclusion, dict), "UNSUPPORTED_EXCLUSION", f"{cid} lacks independent authoritative exclusion")
            fields(exclusion, "rationale rule_id citation", "exclusion")
            require(exclusion["rationale"] == policy["rationale"] and exclusion["rule_id"] == policy["rule_id"], "UNSUPPORTED_EXCLUSION", "exclusion scope/authority mismatch")
            store.citation(exclusion["citation"])
        else:
            require(cid not in authority["exclusions"], "CONTRADICTORY_APPLICABILITY", "required criterion has exclusion")
    required = {cid for cid, p in policies.items() if p["applicability"] == "required"}
    require(bool(required), "ZERO_APPLICABLE_CRITERIA", "all-excluded tasks require explicit human reconciliation; never automatic PASS")
    candidate = authority["candidate"]
    fields(candidate, "repository implementation_head artifact_head", "candidate")
    require(candidate["repository"] == authority["task_ref"]["repository"], "SOURCE_MISMATCH", "task and candidate repository differ")
    for key in ("implementation_head", "artifact_head"):
        full_sha(candidate[key])
        store.commit(candidate["repository"], candidate[key])
    current_task = store.json({**authority["task_ref"], "commit": candidate["artifact_head"],
                              "blob": store.blob_at(candidate["repository"], candidate["artifact_head"], authority["task_ref"]["path"])})
    require(all(current_task.get(k) == task.get(k) for k in ("id", "completion_criteria", "evidence_policy", "evidence_rule_inventory")),
            "TASK_CHANGED", "canonical criterion scope changed after pinned task revision")
    principals = authority["principals"]
    fields(principals, "author coordinator reviewer human", "principals")
    for key in ("author", "coordinator", "reviewer"):
        text(principals[key], key)
    require(principals["reviewer"] != principals["author"], "SELF_REVIEW", "independent reviewer required")
    require(principals["human"] is None or isinstance(principals["human"], str) and principals["human"].strip(), "MALFORMED", "human identity invalid")
    text(authority["owner_id"], "owner")
    text(authority["status"], "status")
    require(type(authority["stopped"]) is bool, "MALFORMED", "explicit stop state required")
    require(isinstance(authority["attestations"], list), "MALFORMED", "attestation collection required")
    for receipt in authority["attestations"]:
        fields(receipt, "kind ref actor_id observed_at provenance", "authenticated receipt", "binding")
        require(receipt["kind"] in ("review", "human", "execution", "decision", "capture"), "MALFORMED", "receipt kind invalid")
        ref_key(receipt["ref"])
        text(receipt["actor_id"], "authenticated actor")
        text(receipt["provenance"], "authenticated collection source")
        fresh(receipt["observed_at"], at)
    for cid, exclusion in authority["exclusions"].items():
        judgment = store.json(exclusion["citation"])
        fields(judgment, "kind task_id criterion_id actor_id rationale rule_id", "exclusion decision")
        require(judgment["kind"] == "criterion_exclusion" and judgment["task_id"] == task["id"] and judgment["criterion_id"] == cid,
                "UNSUPPORTED_EXCLUSION", "exclusion decision does not match canonical scope")
        require(judgment["actor_id"] == principals["coordinator"] and judgment["actor_id"] != principals["author"],
                "UNSUPPORTED_EXCLUSION", "worker cannot exclude own criterion")
        require(judgment["rationale"] == exclusion["rationale"] and judgment["rule_id"] == exclusion["rule_id"], "UNSUPPORTED_EXCLUSION", "exclusion decision rationale differs")
        _receipt(authority, "decision", exclusion["citation"], judgment["actor_id"])
    return store, task, policies, required, index


def _receipt(authority, kind, ref, actor, performed_at=None, binding=None):
    matches = [r for r in authority["attestations"] if r["kind"] == kind and ref_key(r["ref"]) == ref_key(ref)]
    require(bool(matches), "UNATTESTED_ACTOR", f"no authenticated {kind} observation")
    require(all(r["actor_id"] == actor for r in matches), "ACTOR_CONFLICT", "receipt actor mismatch")
    if binding is not None:
        require(all(r.get("binding") == binding for r in matches), "CAPTURE_UNBOUND", "authenticated capture does not bind source/build/instance provenance")
    if performed_at is not None:
        require(utc(performed_at) <= min(utc(r["observed_at"]) for r in matches), "STALE_READ", "execution/judgment postdates authenticated observation")


def finding_fingerprint(finding):
    """Stable for a repeated observation, with exact source/evidence provenance."""
    return digest({k: finding[k] for k in ("repository", "head", "task_id", "criterion_id", "code", "evidence", "coverage", "limitations")})


def _reconcile(authority, store, task, rules, at):
    findings, decisions = authority["findings"], authority["decisions"]
    require(isinstance(findings, list) and isinstance(decisions, list), "MALFORMED", "findings/decisions lists required")
    unique, by_fingerprint, chosen = {}, {}, {}
    for f in findings:
        fields(f, "id fingerprint repository head observed_at task_id criterion_id evidence code coverage limitations", "finding")
        text(f["id"], "finding ID")
        full_sha(f["head"])
        require(utc(f["observed_at"]) <= at, "MALFORMED", "finding is future-dated")
        require(f["task_id"] == task["id"] and f["criterion_id"] in task["evidence_policy"], "UNMAPPED_FINDING", "finding has unknown task/criterion")
        text(f["code"], "failure code")
        strings(f["coverage"], "finding coverage")
        strings(f["limitations"], "read limitations", nonempty=False)
        require(set(f["coverage"]) <= set(task["evidence_policy"][f["criterion_id"]]["instances"]), "UNMAPPED_FINDING", "unknown instance")
        citations(f["evidence"], store)
        require(all(r["repository"] == f["repository"] and r["commit"] == f["head"] for r in f["evidence"]), "SOURCE_MISMATCH", "finding evidence is not observed source")
        require(f["fingerprint"] == finding_fingerprint(f), "FINGERPRINT_MISMATCH", "failure fingerprint differs")
        require(f["id"] not in unique or unique[f["id"]] == f, "FINDING_CONFLICT", "same finding ID changed payload")
        unique[f["id"]] = f
        by_fingerprint.setdefault(f["fingerprint"], []).append(f["id"])
    for dref in decisions:
        d = store.json(dref)
        fields(d, "id actor_id finding_ids fingerprints kind rationale citations detail", "reconciliation decision")
        text(d["id"], "decision ID")
        require(d["actor_id"] == authority["principals"]["coordinator"], "INSPECTOR_MUTATION", "only designated coordinator can record decisions")
        _receipt(authority, "decision", dref, d["actor_id"])
        strings(d["finding_ids"], "decision findings")
        strings(d["fingerprints"], "decision fingerprints")
        require(set(d["finding_ids"]) <= set(unique), "UNMAPPED_DECISION", "decision references absent finding")
        require(set(d["fingerprints"]) == {unique[i]["fingerprint"] for i in d["finding_ids"]}, "FINGERPRINT_MISMATCH", "decision lost finding provenance")
        text(d["rationale"], "decision rationale")
        citations(d["citations"], store)
        detail = d["detail"]
        if d["kind"] == "existing_rule":
            fields(detail, "rule_id rule_ref", "existing rule")
            require(rules.get(detail["rule_id"]) == detail["rule_ref"], "STALE_RULE", "decision must cite exact current rule")
        elif d["kind"] == "task_limitation":
            fields(detail, "task_id criterion_ids instances required_action required_evidence blocks", "task limitation")
            require(detail["task_id"] == task["id"], "UNBOUNDED_LIMITATION", "limitation must stay on task")
            strings(detail["criterion_ids"], "limited criteria")
            strings(detail["instances"], "limited instances")
            require(set(detail["criterion_ids"]) == {unique[i]["criterion_id"] for i in d["finding_ids"]}, "UNBOUNDED_LIMITATION", "limitation criterion scope differs")
            require(set(detail["instances"]) == set().union(*(set(unique[i]["coverage"]) for i in d["finding_ids"])), "UNBOUNDED_LIMITATION", "limitation instance scope differs")
            text(detail["required_action"], "required action")
            text(detail["required_evidence"], "required evidence")
            strings(detail["blocks"], "blocked gates")
            require(set(detail["blocks"]) <= {"admission", "completion"}, "MALFORMED", "limitation gates invalid")
        elif d["kind"] == "reusable_guideline":
            fields(detail, "incident invariant contexts rule_id previous_rule delta_ref regression_ref", "reusable guideline")
            text(detail["incident"], "recorded incident")
            text(detail["invariant"], "generalized invariant")
            strings(detail["contexts"], "generalization contexts")
            require(len(detail["contexts"]) >= 2, "UNJUSTIFIED_GUIDELINE", "frequency alone is insufficient; distinct contexts required")
            require(detail["rule_id"] in rules, "UNKNOWN_RULE", "authoritative rule delta required")
            previous = detail["previous_rule"]
            current = rules[detail["rule_id"]]
            store.citation(previous)
            require(previous["repository"] == current["repository"] and previous["path"] == current["path"] and previous["blob"] != current["blob"], "NO_RULE_DELTA", "rule content must actually change")
            require(store.ancestor(previous["repository"], previous["commit"], current["commit"]), "NO_RULE_DELTA", "previous rule is not an ancestor of current rule")
            delta = store.json(detail["delta_ref"])
            fields(delta, "before after incident", "rule delta")
            require(delta["before"] == previous and delta["after"] == current and delta["incident"] == detail["incident"], "NO_RULE_DELTA", "delta is not bound to the authoritative change")
            regression = store.json(detail["regression_ref"])
            fields(regression, "actor_id command broken_fixture assertion rule_delta exit_code failure_code observed_output performed_at", "regression execution")
            _receipt(authority, "execution", detail["regression_ref"], regression["actor_id"], regression["performed_at"])
            text(regression["actor_id"], "execution observer")
            strings(regression["command"], "executed regression command")
            store.citation(regression["broken_fixture"])
            store.citation(regression["assertion"])
            require(regression["command"] == ["python3", regression["assertion"]["path"], regression["broken_fixture"]["path"]],
                    "REGRESSION_UNBOUND", "regression command must execute the cited assertion on the cited broken fixture")
            require(regression["rule_delta"] == detail["delta_ref"], "REGRESSION_UNBOUND", "regression must bind rule delta")
            require(any(ref_key(regression["broken_fixture"]) in {ref_key(r) for r in unique[i]["evidence"]} for i in d["finding_ids"]), "REGRESSION_UNBOUND", "broken fixture is not recorded incident evidence")
            require(type(regression["exit_code"]) is int and regression["exit_code"] != 0, "VACUOUS_REGRESSION", "recorded broken fixture must fail")
            require(regression["failure_code"] in {unique[i]["code"] for i in d["finding_ids"]}, "REGRESSION_UNBOUND", "wrong failure class")
            text(regression["observed_output"], "actual failing output")
            require(utc(regression["performed_at"]) <= at, "MALFORMED", "future regression")
        else:
            raise PolicyError("UNRESOLVED_FINDING", "unknown/unresolved reconciliation decision")
        for fid in d["finding_ids"]:
            signature = digest(d)
            require(fid not in chosen or chosen[fid][0] == signature, "DECISION_CONFLICT", "contradictory decisions for finding")
            chosen[fid] = (signature, d, dref)
    require(set(chosen) == set(unique), "UNRESOLVED_FINDING", "every observed finding needs explicit reconciliation")
    # Equivalent observations cannot receive different dispositions under different IDs.
    for ids in by_fingerprint.values():
        dispositions = {digest({k: chosen[i][1][k] for k in ("kind", "rationale", "detail")}) for i in ids}
        require(len(dispositions) == 1, "DECISION_CONFLICT", "duplicate failure has conflicting reconciliation")
    return [{"finding_id": fid, "fingerprint": unique[fid]["fingerprint"], "decision_id": chosen[fid][1]["id"],
             "kind": chosen[fid][1]["kind"], "decision_ref": chosen[fid][2],
             "blocks": chosen[fid][1]["detail"].get("blocks", [])}
            for fid in sorted(unique)]


def _base(authority, submission, objects, at, operation):
    store, task, policies, required, rules = _authority(authority, objects, at)
    require(not authority["stopped"] and authority["status"] not in STOPPED, "STOPPED", "explicit stop/terminal state retained; no owner transfer or redispatch")
    require(authority["owner_id"] == authority["principals"]["author"], "OWNER_CONFLICT", "existing owner must remain designated author")
    reconciled = _reconcile(authority, store, task, rules, at)
    require(not any(operation in r["blocks"] for r in reconciled), "TASK_LIMITATION", f"recorded task limitation blocks {operation}")
    require(isinstance(submission, dict), "MALFORMED", "submission object required")
    ack = submission.get("acknowledgment")
    require(isinstance(ack, dict), "MISSING_ACKNOWLEDGMENT", "worker acknowledgment required")
    fields(ack, "task_id author_id rules", "acknowledgment")
    require(ack["task_id"] == task["id"] and ack["author_id"] == authority["principals"]["author"], "ACKNOWLEDGMENT_MISMATCH", "wrong task/author acknowledgment")
    expected = [{"id": k, "ref": v} for k, v in sorted(rules.items())]
    require(isinstance(ack["rules"], list) and sorted(ack["rules"], key=lambda r: r.get("id", "")) == expected,
            "STALE_ACKNOWLEDGMENT", "acknowledge entire current rule inventory with exact commit/blob revisions")
    plans = submission.get("plans")
    require(isinstance(plans, dict) and set(plans) == required, "INCOMPLETE_PLAN", "exactly one concrete plan per applicable canonical criterion required")
    for cid, plan in plans.items():
        p = policies[cid]
        fields(plan, "method artifacts source_paths build coverage reviewer_id", f"plan {cid}")
        text(plan["method"], "evidence method")
        require(isinstance(plan["artifacts"], list) and bool(plan["artifacts"]), "INCOMPLETE_PLAN", "artifact path/type plan required")
        seen, planned_checks, planned_images = set(), set(), []
        checks = {c["id"] for c in p["checks"]}
        for artifact in plan["artifacts"]:
            fields(artifact, "path type", "planned artifact", "check_id instances pair")
            path_parts(artifact["path"])
            require(artifact["type"] in {"assertion", "log", "diff", "document", "image"}, "INCOMPLETE_PLAN", "appropriate artifact type required")
            require(artifact["path"] not in seen, "INCOMPLETE_PLAN", "duplicate artifact path")
            seen.add(artifact["path"])
            if artifact["type"] in {"log", "assertion"}:
                require(artifact.get("check_id") in checks, "INCOMPLETE_PLAN", "planned execution must identify a required canonical check")
                planned_checks.add(artifact["check_id"])
            else:
                require(artifact.get("check_id") is None, "INCOMPLETE_PLAN", "non-execution artifact cannot satisfy a required check")
            if p["visual"] and artifact["type"] == "image":
                strings(artifact.get("instances"), "planned visual instance")
                require(len(artifact["instances"]) == 1 and artifact["instances"][0] in p["instances"], "INCOMPLETE_PLAN", "planned image must name exactly one canonical instance")
                fields(artifact.get("pair"), "role camera", "planned visual pair")
                require(artifact["pair"]["role"] in {"before", "after"}, "INCOMPLETE_PLAN", "planned pair role required")
                text(artifact["pair"]["camera"], "planned matched camera")
                planned_images.append(artifact)
            else:
                require("pair" not in artifact and "instances" not in artifact, "INCOMPLETE_PLAN", "pair fields only apply to planned visual images")
        require(planned_checks == checks, "INCOMPLETE_PLAN", "every required command needs a planned log/assertion artifact")
        if p["visual"]:
            for instance in p["instances"]:
                pair = [a for a in planned_images if a["instances"] == [instance]]
                require(len(pair) == 2 and {a["pair"]["role"] for a in pair} == {"before", "after"} and len({a["pair"]["camera"] for a in pair}) == 1,
                        "VISUAL_PAIR_REQUIRED", "plan needs a matched before/after artifact pair for every instance")
        strings(plan["source_paths"], "planned source scope")
        strings(plan["coverage"], "planned instance coverage")
        require(set(plan["source_paths"]) == set(p["source_paths"]) and set(plan["coverage"]) == set(p["instances"]), "INCOMPLETE_PLAN", "plan narrows canonical source or instance coverage")
        require(plan["build"] == p["build"], "BUILD_MISMATCH", "planned source/build/variant/environment differs")
        require(plan["reviewer_id"] == authority["principals"]["reviewer"], "SELF_REVIEW", "designated independent reviewer required")
        require(not p["visual"] or any(a["type"] == "image" for a in plan["artifacts"]), "INCOMPLETE_PLAN", "visual plan requires matched image evidence")
    return store, task, policies, required, reconciled


def _authority_digest(authority):
    try:
        normalized = dict(authority)
        for key in ("rules", "findings", "decisions", "attestations"):
            if isinstance(normalized.get(key), list):
                normalized[key] = sorted(normalized[key], key=digest)
        return digest(normalized)
    except (PolicyError, TypeError, ValueError):
        return None


def _result(operation, authority, status, issues=(), gates=None, reconciled=()):
    return {"version": VERSION, "operation": operation, "status": status,
            "authority_digest": _authority_digest(authority), "issues": list(issues),
            "gates": gates or {}, "reconciliations": list(reconciled),
            "mutations": [], "limitations": ["Authenticated collection and identity attestations are caller responsibilities; this evaluator never fetches, dispatches, changes ownership or accepts work on its own."]}


def _failure(operation, authority, exc, gates=None):
    status = "STOPPED" if exc.code == "STOPPED" else "INPUT_REQUIRED" if exc.code in {"MALFORMED", "UNKNOWN_RULES", "STALE_READ", "INACCESSIBLE_OBJECT", "APPLICABILITY_REQUIRED"} else "NO_GO"
    return _result(operation, authority, status, [{"code": exc.code, "detail": exc.detail}], gates)


def evaluate_admission(authority, submission, objects, at):
    """Check only admission. Unrelated deployment/publication holds are not inputs."""
    try:
        _, _, _, _, reconciled = _base(authority, submission, objects, at, "admission")
        return _result("admission", authority, "ADMISSIBLE", gates={"admission": "PASS"}, reconciled=reconciled)
    except (PolicyError, KeyError, TypeError, AttributeError) as exc:
        if not isinstance(exc, PolicyError):
            exc = PolicyError("MALFORMED", str(exc))
        return _failure("admission", authority, exc, {"admission": "FAIL"})


def _source_bound(store, authority, policies, required):
    candidate = authority["candidate"]
    repo, source, artifact = candidate["repository"], candidate["implementation_head"], candidate["artifact_head"]
    require(store.ancestor(repo, source, artifact), "SOURCE_MISMATCH", "artifact tip must descend from reviewed implementation")
    for cid in required:
        require(store.equal_scope(repo, source, artifact, policies[cid]["source_paths"]), "SOURCE_CHANGED", f"{cid}: evidence-only commit changed relevant source")


def _evidence(authority, submission, store, policies, required, at):
    items = submission.get("evidence")
    require(isinstance(items, list) and bool(items), "MISSING_EVIDENCE", "committed evidence required")
    found, index = {cid: set() for cid in required}, {}
    checks_seen = {cid: set() for cid in required}
    candidate = authority["candidate"]
    repo, source = candidate["repository"], candidate["implementation_head"]
    for item in items:
        fields(item, "id criterion_id instances type ref source_head build performed_at check_id", "evidence", "pair")
        text(item["id"], "evidence ID")
        require(item["id"] not in index, "MALFORMED", "duplicate evidence ID")
        cid = item["criterion_id"]
        require(cid in required, "UNMAPPED_EVIDENCE", "evidence does not map applicable criterion")
        strings(item["instances"], "evidence instances")
        require(set(item["instances"]) <= set(policies[cid]["instances"]), "UNMAPPED_EVIDENCE", "unknown defect instance")
        require(item["type"] in {a["type"] for a in submission["plans"][cid]["artifacts"] if a["path"] == item["ref"].get("path")}, "UNPLANNED_EVIDENCE", "artifact path/type not in admitted plan")
        planned = next(a for a in submission["plans"][cid]["artifacts"] if a["path"] == item["ref"]["path"])
        require(planned.get("check_id") == item["check_id"], "UNPLANNED_EVIDENCE", "execution check differs from admitted artifact plan")
        store.citation(item["ref"])
        require(item["ref"]["repository"] == repo, "SOURCE_MISMATCH", "evidence repository differs")
        require(store.ancestor(repo, item["ref"]["commit"], candidate["artifact_head"]), "UNCOMMITTED_PATH", "evidence not in candidate history")
        require(store.blob_at(repo, candidate["artifact_head"], item["ref"]["path"]) == item["ref"]["blob"], "EVIDENCE_CHANGED", "evidence was changed after cited revision")
        full_sha(item["source_head"])
        require(store.ancestor(repo, item["source_head"], source), "SOURCE_MISMATCH", "evidence source is not candidate/ancestor")
        require(store.equal_scope(repo, item["source_head"], source, policies[cid]["source_paths"]), "STALE_EVIDENCE", "historical evidence source scope differs")
        require(item["build"] == policies[cid]["build"], "BUILD_MISMATCH", "wrong build, variant or environment")
        require(utc(item["performed_at"]) <= at, "MALFORMED", "evidence execution is future-dated")
        if item["type"] in {"log", "assertion"}:
            spec = {c["id"]: c["command"] for c in policies[cid]["checks"]}
            require(item["check_id"] in spec, "UNMAPPED_CHECK", "execution must map a required canonical check")
            execution = store.json(item["ref"])
            fields(execution, "check_id command exit_code output source_head build performed_at actor_id", "execution log")
            require(execution["check_id"] == item["check_id"] and execution["command"] == spec[item["check_id"]],
                    "CHECK_MISMATCH", "log is from a different command/check")
            require(type(execution["exit_code"]) is int and execution["exit_code"] == 0, "FAILED_CHECK", "required command did not pass")
            text(execution["output"], "observed check output")
            text(execution["actor_id"], "execution observer")
            require(all(execution[k] == item[k] for k in ("source_head", "build", "performed_at")),
                    "SOURCE_MISMATCH", "execution provenance differs from evidence manifest")
            _receipt(authority, "execution", item["ref"], execution["actor_id"], execution["performed_at"])
            checks_seen[cid].add(item["check_id"])
        else:
            require(item["check_id"] is None, "UNMAPPED_CHECK", "non-execution artifact cannot satisfy command check")
            if policies[cid]["visual"] or item["build"] is not None:
                captures = [r for r in authority["attestations"] if r["kind"] == "capture" and ref_key(r["ref"]) == ref_key(item["ref"])]
                require(bool(captures), "CAPTURE_UNBOUND", "source/build-dependent artifacts need authenticated capture provenance")
                binding = {k: item[k] for k in ("source_head", "build", "performed_at", "criterion_id", "instances")}
                _receipt(authority, "capture", item["ref"], captures[0]["actor_id"], item["performed_at"], binding)

        if policies[cid]["visual"] and item["type"] == "image":
            require(len(item["instances"]) == 1, "VISUAL_PAIR_REQUIRED", "visual evidence must identify one defect instance")
            fields(item.get("pair"), "role camera", "visual pair")
            require(item["pair"]["role"] in {"before", "after"}, "VISUAL_PAIR_REQUIRED", "pair role missing")
            text(item["pair"]["camera"], "matched camera")
            require(item["instances"] == planned["instances"] and item["pair"] == planned["pair"], "UNPLANNED_EVIDENCE", "visual instance/camera/role differs from admitted plan")
        else:
            require("pair" not in item, "MALFORMED", "nonvisual evidence has visual pair metadata")
        found[cid].update(item["instances"])
        index[item["id"]] = item
    for cid in required:
        require(found[cid] == set(policies[cid]["instances"]), "PARTIAL_COVERAGE", f"{cid}: missing claimed instances")
        require(checks_seen[cid] == {c["id"] for c in policies[cid]["checks"]}, "MISSING_CHECK", "all required command checks need actual successful execution logs")
        actual_paths = {item["ref"]["path"] for item in items if item["criterion_id"] == cid}
        require(actual_paths == {a["path"] for a in submission["plans"][cid]["artifacts"]}, "MISSING_EVIDENCE", "every planned artifact must be accounted for")
        if policies[cid]["visual"]:
            for instance in policies[cid]["instances"]:
                pair = [x for x in items if x["criterion_id"] == cid and instance in x["instances"] and x["type"] == "image"]
                require(len(pair) == 2 and {x["pair"]["role"] for x in pair} == {"before", "after"} and len({x["pair"]["camera"] for x in pair}) == 1,
                        "VISUAL_PAIR_REQUIRED", f"{cid}/{instance}: matched before/after pair required")
                require(len({x["ref"]["blob"] for x in pair}) == 2, "IDENTICAL_VISUAL_PAIR", "before and after bytes are identical")
    return index



def _current_execution_gate(authority, store, policies, required, at):
    candidate = authority["candidate"]
    regression_refs = {ref_key(d["detail"]["regression_ref"]) for d in (store.json(ref) for ref in authority["decisions"]) if d["kind"] == "reusable_guideline"}
    for receipt in authority["attestations"]:
        if receipt["kind"] != "execution" or receipt["ref"]["repository"] != candidate["repository"]:
            continue
        record = store.json(receipt["ref"])
        require(isinstance(record, dict), "MALFORMED", "authenticated execution observation must be structured")
        # Generalization regressions deliberately fail on a cited broken fixture;
        # their distinct schema is validated during reconciliation, not confused
        # with a check of the current candidate implementation.
        if "check_id" not in record:
            require(ref_key(receipt["ref"]) in regression_refs, "CURRENT_CHECK_INCOMPLETE", "unmapped execution cannot be reclassified as a regression")
            require(set(record) == {"actor_id", "command", "broken_fixture", "assertion", "rule_delta", "exit_code", "failure_code", "observed_output", "performed_at"},
                    "CURRENT_CHECK_INCOMPLETE", "unknown execution observation cannot be silently ignored")
            continue
        fields(record, "check_id command exit_code output source_head build performed_at actor_id", "observed required-check execution")
        _receipt(authority, "execution", receipt["ref"], record["actor_id"], record["performed_at"])
        for cid in required:
            checks = {check["id"]: check["command"] for check in policies[cid]["checks"]}
            if record["check_id"] not in checks or record["build"] != policies[cid]["build"]:
                continue
            full_sha(record["source_head"])
            # A failure only stops this criterion when actual relevant source is
            # the same. A real corrective source change can invalidate old logs.
            if not store.equal_scope(candidate["repository"], record["source_head"], candidate["implementation_head"], policies[cid]["source_paths"]):
                continue
            require(record["command"] == checks[record["check_id"]], "CURRENT_CHECK_CONFLICT", "current required-check observation names a different command")
            require(type(record["exit_code"]) is int and record["exit_code"] == 0, "CURRENT_CHECK_FAILED", "authenticated failure of an applicable current required check remains unresolved")
            text(record["output"], "observed current check output")


def _verdict(authority, submission, store, policies, required, evidence, kind, at):
    ref = submission.get("verdict" if kind == "review" else "human_verdict")
    require(ref is not None, "MISSING_VERDICT" if kind == "review" else "HUMAN_PENDING", f"explicit {kind} verdict required")
    verdict = store.json(ref)
    fields(verdict, "task_id candidate_head actor_id authority_digest evidence_digest performed_at criteria", f"{kind} verdict")
    actor = authority["principals"]["reviewer" if kind == "review" else "human"]
    require(actor is not None and verdict["actor_id"] == actor and actor != authority["principals"]["author"], "SELF_REVIEW", "designated independent actor required")
    _receipt(authority, kind, ref, actor, verdict["performed_at"])
    task_id = submission["acknowledgment"]["task_id"]
    # Do not cherry-pick a convenient PASS when the authenticated current
    # observation set contains a same-source rejection or pending judgment.
    for receipt in authority["attestations"]:
        if receipt["kind"] != kind or ref_key(receipt["ref"]) == ref_key(ref):
            continue
        other = store.json(receipt["ref"])
        require(isinstance(other, dict), "MALFORMED", "review observation must be structured")
        if other.get("task_id") == task_id and other.get("candidate_head") == authority["candidate"]["implementation_head"]:
            require(other.get("actor_id") == receipt["actor_id"], "ACTOR_CONFLICT", "review observation actor differs")
            decisions = other.get("criteria")
            require(isinstance(decisions, dict) and set(decisions) == (required if kind == "review" else {c for c in required if policies[c]["visual"]}),
                    "CONFLICTING_VERDICT", "incomplete current review requires reconciliation")
            require(all(isinstance(d, dict) and d.get("decision") == "PASS" for d in decisions.values()),
                    "CONFLICTING_VERDICT", "same-source FAIL/PENDING judgment remains unresolved")
    require(verdict["task_id"] == task_id, "UNMAPPED_VERDICT", "verdict names another task")
    require(verdict["candidate_head"] == authority["candidate"]["implementation_head"], "STALE_VERDICT", "verdict must name full reviewed implementation head")
    # The verdict cannot hash itself, the containing evidence commit or fresh
    # collection timestamps. Pin only task/rule/source scope and evidence inputs.
    require(verdict["authority_digest"] == acceptance_binding(authority), "STALE_VERDICT", "task/rule/source applicability changed")
    require(verdict["evidence_digest"] == digest(submission["evidence"]), "STALE_VERDICT", "evidence manifest changed after inspection")
    require(utc(verdict["performed_at"]) <= at, "MALFORMED", "future verdict")
    criteria = verdict["criteria"]
    expected = required if kind == "review" else {c for c in required if policies[c]["visual"]}
    require(isinstance(criteria, dict) and bool(criteria) and set(criteria) == expected, "PARTIAL_VERDICT", "exactly one judgment per applicable criterion required")
    for cid, decision in criteria.items():
        fields(decision, "decision rationale citations evidence_ids", "criterion judgment", "visual_inspection finding_ids")
        text(decision["rationale"], "inspection rationale")
        require(decision["decision"] in {"PASS", "FAIL", "PENDING"}, "MALFORMED", "explicit decision required")
        require(decision["decision"] == "PASS", "REJECTED_VERDICT" if kind == "review" else "HUMAN_PENDING", "pending/rejected judgments cannot become automatic acceptance")
        seen = citations(decision["citations"], store)
        strings(decision["evidence_ids"], "inspected evidence IDs")
        current_findings = {f["id"]: f for f in authority["findings"] if f["criterion_id"] == cid}
        finding_ids = decision.get("finding_ids", [])
        strings(finding_ids, "reviewed finding IDs", nonempty=False)
        require(set(finding_ids) == set(current_findings), "UNREVIEWED_FINDING", "independent judgment must account for every observed finding")
        require({ref_key(r) for f in current_findings.values() for r in f["evidence"]} <= seen, "UNREVIEWED_FINDING", "review must inspect the finding's original evidence as well as claimed resolution")
        expected_ids = {eid for eid, item in evidence.items() if item["criterion_id"] == cid}
        require(set(decision["evidence_ids"]) == expected_ids, "PARTIAL_VERDICT", "review must inspect every claimed instance/artifact")
        require({ref_key(evidence[e]["ref"]) for e in expected_ids} <= seen, "NO_CITATIONS", "inspection citations must include actual mapped evidence")
        if policies[cid]["visual"]:
            inspect = decision.get("visual_inspection")
            fields(inspect, "method matched_pairs nonempty meaningful after_resolves_defect", "explicit visual judgment")
            require(inspect["method"] in ({"human_device"} if kind == "human" else {"direct_pixel_inspection"}), "VISUAL_JUDGMENT_REQUIRED", "numeric diffs/CI cannot stand in for direct visual inspection")
            require(all(inspect[k] is True for k in ("matched_pairs", "nonempty", "meaningful", "after_resolves_defect")), "VISUAL_JUDGMENT_REQUIRED", "explicit inspected quality judgments required")
    return verdict


def _unique_records(records):
    return [value for _, value in sorted({digest(value): value for value in records}.items())]


def acceptance_binding(authority):
    """Stable across evidence/verdict-only descendants and fresh collection reads."""
    return digest({"rules": sorted([{"id": r["id"], "repository": r["ref"]["repository"], "path": r["ref"]["path"], "blob": r["ref"]["blob"]} for r in authority["rules"]], key=lambda r: r["id"]), "task_ref": authority["task_ref"],
                   "implementation_head": authority["candidate"]["implementation_head"],
                   "principals": authority["principals"], "exclusions": authority["exclusions"],
                   "findings": _unique_records(authority["findings"]),
                   "decisions": _unique_records(authority["decisions"]),
                   "observations": _unique_records([{k: r[k] for k in ("kind", "ref", "actor_id", "binding") if k in r}
                       for r in authority["attestations"] if r["kind"] not in {"review", "human"}])})


def evaluate_completion(authority, submission, objects, at):
    gates = {"author": "PENDING", "test_evidence": "PENDING", "independent_review": "PENDING", "human_visual": "PENDING"}
    try:
        store, task, policies, required, reconciled = _base(authority, submission, objects, at, "completion")
        gates["author"] = "PASS"
        gates["human_visual"] = "PENDING" if any(policies[c]["visual"] for c in required) else "NOT_APPLICABLE"
        _source_bound(store, authority, policies, required)
        _current_execution_gate(authority, store, policies, required, at)
        evidence = _evidence(authority, submission, store, policies, required, at)
        gates["test_evidence"] = "BOUND"
        _verdict(authority, submission, store, policies, required, evidence, "review", at)
        gates["independent_review"] = "PASS"
        if any(policies[c]["visual"] for c in required):
            _verdict(authority, submission, store, policies, required, evidence, "human", at)
            gates["human_visual"] = "PASS"
        else:
            gates["human_visual"] = "NOT_APPLICABLE"
        return _result("completion", authority, "ACCEPTABLE", gates=gates, reconciled=reconciled)
    except (PolicyError, KeyError, TypeError, AttributeError) as exc:
        if not isinstance(exc, PolicyError):
            exc = PolicyError("MALFORMED", str(exc))
        return _failure("completion", authority, exc, gates)


def reconcile_findings(authority, objects, at):
    try:
        store, task, _, _, rules = _authority(authority, objects, at)
        reconciled = _reconcile(authority, store, task, rules, at)
        return _result("reconciliation", authority, "RECORDED", reconciled=reconciled)
    except (PolicyError, KeyError, TypeError, AttributeError) as exc:
        if not isinstance(exc, PolicyError):
            exc = PolicyError("MALFORMED", str(exc))
        return _failure("reconciliation", authority, exc)
