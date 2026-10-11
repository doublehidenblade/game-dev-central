"""Bounded execution handoff. No network, worker launch, or legacy queue writes.

The coordinator supplies authenticated observations and executes returned handoffs
with its authorized tools. This journal is a single-writer, single-filesystem
backend; separate clones are NOT a distributed dispatch lock.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import fcntl
import json
import os
from pathlib import Path
import tempfile

import coordinator as co
from coordinator_cli import _load
import evidence_policy as ep
import scoped_admission as sa

MAX_QUEUE = 5
MAX_ROLLOUT = 3
RECEIPT_WINDOW = timedelta(minutes=10)
STATES = {"open", "ready", "admitted", "in_progress", "in_review", "validated", "rejected", "parked"}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def key(candidate):
    return candidate["repository"] + ":" + candidate["task_id"]


def fresh(receipt, at):
    need(timedelta(0) <= at - co.utc(receipt["observed_at"]) < co.MAX_AGE,
         "missing, stale or future observation")
    need(isinstance(receipt["evidence"], str) and receipt["evidence"].strip(), "evidence reference required")


def validate(queue, ledger):
    need(queue["version"] == ledger["version"] == 1, "unsupported schema")
    need(type(queue["rollout_limit"]) is int and 1 <= queue["rollout_limit"] <= MAX_ROLLOUT,
         "first rollout permits at most three candidates")
    need(isinstance(queue["ready"], list) and len(queue["ready"]) <= MAX_QUEUE, "ready queue exceeds five")
    ids = [key(c) for c in queue["ready"] + queue["blocked"]]
    need(len(ids) == len(set(ids)), "duplicate candidate identity")
    for c in queue["ready"]:
        need(c["state"] == "ready", "queue entries must be explicitly ready")
        need(c["write_paths"] and len(c["write_paths"]) == len(set(c["write_paths"])), "write allowlist required")
        for path in c["write_paths"]:
            ep.path_parts(path.rstrip("/"))
    for c in queue["blocked"]:
        need(c["reasons"] and c["receipts"], "blocked candidate needs exact reasons and receipts")
    need(type(ledger["revision"]) is int and ledger["revision"] == len(ledger["events"]), "journal revision mismatch")
    for baseline in ledger["history"].values():
        count = baseline["prior_attempts"]
        need(count is None or type(count) is int and count >= 0, "unknown history must remain null")
        need(baseline["receipts"] and baseline["state"] in STATES, "history needs source receipts and state")
    attempts = {}
    for n, event in enumerate(ledger["events"], 1):
        need(event["revision"] == n and event["state"] in STATES, "invalid journal event")
        need(event["kind"] in {"hold", "reserve", "session", "receipt", "review", "missing_receipt", "liveness_reconciled"},
             "unknown journal event")
        if event["kind"] == "hold":
            need(event["state"] == "parked" and event["reasons"] and event["receipts"], "invalid retained stop")
        elif event["kind"] == "reserve":
            need(event["attempt_id"] not in attempts, "duplicate attempt ID")
            attempts[event["attempt_id"]] = event
        else:
            need(event["attempt_id"] in attempts and event["key"] == attempts[event["attempt_id"]]["key"],
                 "event has no matching reservation")


def append(ledger, kind, attempt, state, at, **data):
    ledger["revision"] += 1
    event = dict(revision=ledger["revision"], kind=kind, key=attempt["key"],
                 attempt_id=attempt["attempt_id"], state=state, at=at.isoformat(), **data)
    ledger["events"].append(event)
    return event


def attempts(ledger):
    result = {}
    for event in ledger["events"]:
        if event["kind"] == "hold":
            continue
        if event["kind"] == "reserve":
            result[event["attempt_id"]] = dict(event, reserved_at=event["at"], released=False,
                                              unsuccessful=False, receipt=None, session=None)
        else:
            result[event["attempt_id"]].update(event)
    return list(result.values())


def reconcile_attempts(ledger, observations, at):
    """Timeout is failure to prove implementation, never proof of worker death."""
    for attempt in attempts(ledger):
        if attempt["released"]:
            continue
        observation = observations.get(attempt["attempt_id"])
        clear = False
        if observation:
            fresh(observation, at)
            need(observation["attempt_id"] == attempt["attempt_id"], "liveness targets another attempt")
            session_id = (attempt["session"] or attempt["receipt"] or {}).get("session_id")
            need(observation["session_id"] == session_id, "liveness session mismatch")
            need(observation["state"] in {"ended", "not_started", "live", "unknown"}, "invalid liveness")
            need(observation["state"] != "not_started" or session_id is None, "known session cannot be not_started")
            clear = observation["state"] in {"ended", "not_started"}
        expired = at >= co.utc(attempt["receipt_due"])
        if attempt["receipt"] is None and expired and not attempt["unsuccessful"]:
            append(ledger, "missing_receipt", attempt, "rejected" if clear else "parked", at,
                   unsuccessful=True, released=clear, evidence=observation,
                   reason="No verified session and first-write receipt by deadline")
        elif clear and (attempt["unsuccessful"] or attempt["state"] in {"in_review", "validated", "rejected", "parked"}):
            append(ledger, "liveness_reconciled", attempt, attempt["state"], at,
                   released=True, evidence=observation)


def overlaps(left, right):
    return any(a == b or a.endswith("/") and b.startswith(a) or
               b.endswith("/") and a.startswith(b) for a in left for b in right)


def candidate_action(candidate, packet, at):
    snapshot, receipt = packet["snapshot"], packet["reconciliation"]
    fresh(receipt, at)
    need(receipt["input_digest"] == co.digest(snapshot), "reconciliation is not bound to this snapshot")
    for source in ("board", "open_prs", "user_stops", "sessions"):
        need(isinstance(receipt[source], str) and receipt[source].strip(), source + " receipt required")
    need(receipt["stops"] == [], "explicit stop: " + str(receipt["stops"]))
    need(receipt["liveness"] == "clear", "reconcile uncertain/live session before replacement")
    task = next(t for t in snapshot["tasks"] if t["id"] == candidate["task_id"] and t["repository"] == candidate["repository"])
    need(task["project"] == "lower-city", "only approved Lower City implementation belongs in this queue")
    plan = co.evaluate(snapshot, at)
    actions = [a for a in plan["actions"] if a["task_id"] == candidate["task_id"] and
               a["repository"] == candidate["repository"] and a["operation"] == "implementation"]
    if not actions:
        reasons = [b for b in plan["blocked"] if b["task_id"] == candidate["task_id"]]
        raise ValueError(json.dumps({"guard_blockers": reasons, "warnings": plan["warnings"]}, sort_keys=True))
    action = actions[0]
    target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
    need(co.revalidate(snapshot, action, target, at)["status"] == "GO", "final guard failed")
    return action, receipt


def cycle(queue, ledger, packets, observations, at):
    validate(queue, ledger)
    reconcile_attempts(ledger, observations, at)
    escalations = deepcopy(queue["blocked"])
    current = attempts(ledger)
    active = [a for a in current if not a["released"]]
    rollout = {a["key"] for a in current}
    for candidate in queue["ready"]:
        task_key = key(candidate)
        try:
            # Stop/source reconciliation precedes selection, even for previously ready tasks.
            need(task_key in packets, "fresh board/open-PR/user-stop/session packet missing")
            packet = packets[task_key]
            snapshot, reconciliation = packet["snapshot"], packet["reconciliation"]
            fresh(reconciliation, at)
            need(reconciliation["input_digest"] == co.digest(snapshot), "stop reconciliation snapshot changed")
            stops = list(reconciliation["stops"])
            stops.extend(b["kind"] + ":" + b["id"] + ":" + b["reason"] for b in snapshot["blockers"]
                         if b["repository"] == candidate["repository"] and b["task_id"] in {candidate["task_id"], "*"}
                         and b["kind"] in {"stop", "denial", "security"} and
                         ("implementation" in b["operations"] or "*" in b["operations"]))
            stops.extend("cancelled request:" + r["id"] for r in snapshot["requests"]
                         if r["repository"] == candidate["repository"] and r["task_id"] in {candidate["task_id"], "*"}
                         and r["state"] == "cancelled" and "implementation" in r["operations"])
            held = [e for e in ledger["events"] if e["kind"] == "hold" and e["key"] == task_key]
            if stops and not any(e["reasons"] == stops for e in held):
                held.append(append(ledger, "hold", {"key": task_key, "attempt_id": None}, "parked", at,
                                   reasons=stops, receipts=[reconciliation["user_stops"]]))
            need(not held, "retained explicit stop/denial: " + str([e["reasons"] for e in held]))
            action, receipt = candidate_action(candidate, packets[task_key], at)
            history = ledger["history"].get(task_key)
            need(history is not None and history["prior_attempts"] is not None,
                 "historical attempt count unknown; never infer zero")
            need(history["state"] not in {"parked", "validated", "in_review", "in_progress", "admitted"},
                 "historical stop/ownership/acceptance retained: " + history["state"])
            previous = [a for a in current if a["key"] == task_key]
            count = history["prior_attempts"] + len(previous)
            need(count < 2, "initial plus one correction exhausted")
            need(not previous or previous[-1]["unsuccessful"], "prior implementation needs independent review; no redispatch")
            if count:
                correction = candidate.get("correction") or {}
                need(correction.get("evidence") and correction.get("changed_approach"), "correction requires new evidence and changed approach")
            need(task_key in rollout or len(rollout) < queue["rollout_limit"], "first rollout candidate limit reached")
            for other in active:
                need(other["key"] != task_key and other["decision"]["executor_id"] != action["executor_id"] and
                     (other["decision"]["repository"] != action["repository"] or
                      not overlaps(other["write_paths"], candidate["write_paths"])),
                     "unreleased reservation: " + other["attempt_id"] + "; reconcile liveness, never duplicate")
            identity = {"key": task_key, "attempt_id": task_key + ":" + str(count + 1)}
            event = append(ledger, "reserve", identity, "admitted", at, decision=action,
                           reconciliation=receipt, write_paths=candidate["write_paths"],
                           correction=candidate.get("correction"), receipt_due=(at + RECEIPT_WINDOW).isoformat())
            return {"status": "DISPATCH_REQUIRED", "attempt": event, "escalations": escalations,
                    "next": "Persist the journal; revalidate exact decision immediately before authorized coordinator launch. Admission is not implementation."}
        except (ValueError, KeyError, TypeError, StopIteration, ep.PolicyError) as exc:
            escalations.append({"repository": candidate["repository"], "task_id": candidate["task_id"],
                                "reasons": [str(exc)], "receipts": candidate.get("receipts", [])})
    if not escalations:
        escalations = [{"task_id": "queue", "reasons": ["No verified eligible approved candidates registered"],
                        "receipts": ["READY_QUEUE.md"]}]
    return {"status": "ESCALATION_REQUIRED", "candidates": escalations,
            "reservations": [{"attempt_id": a["attempt_id"], "state": a["state"], "released": a["released"]}
                             for a in attempts(ledger)], "next": "Resolve only the named blocker with its owner; do not report steady IDLE."}


def record(ledger, event, at):
    attempt = next(a for a in attempts(ledger) if a["attempt_id"] == event["attempt_id"])
    need(not any(e["kind"] == "hold" and e["key"] == attempt["key"] for e in ledger["events"]),
         "retained stop; recording cannot restart this attempt")
    if event["kind"] == "session":
        need(attempt["state"] == "admitted" and attempt["session"] is None and not attempt["unsuccessful"],
             "session already recorded or attempt unavailable")
        session = event["session"]
        fresh(session, at)
        need(session["session_id"] and session["session_evidence"], "actual launch tool receipt required")
        need(all(session[k] == attempt["decision"][k] for k in ("executor_id", "owner_id")), "wrong session owner/executor")
        need(co.utc(attempt["reserved_at"]) <= co.utc(session["started_at"]) <= at <= co.utc(attempt["receipt_due"]),
             "session outside reserved receipt window")
        append(ledger, "session", attempt, "admitted", at, session=session)
    elif event["kind"] == "receipt":
        need(attempt["state"] == "admitted" and not attempt["unsuccessful"], "receipt cannot revive a failed/stopped attempt")
        need(at <= co.utc(attempt["receipt_due"]), "late receipt requires liveness reconciliation, not a new attempt")
        receipt = event["receipt"]
        fresh(receipt, at)
        for field in ("session_id", "session_evidence"):
            need(isinstance(receipt[field], str) and receipt[field].strip(), "actual session receipt required")
        decision = attempt["decision"]
        need(all(receipt[k] == decision[k] for k in ("executor_id", "owner_id")), "wrong session owner/executor")
        need(attempt["session"] is None or attempt["session"]["session_id"] == receipt["session_id"], "first write names another session")
        need(co.utc(attempt["reserved_at"]) <= co.utc(receipt["started_at"]) <= co.utc(receipt["written_at"]) <= at,
             "first write must occur in the admitted session")
        ref = receipt["first_write"]
        need(ref["repository"] == decision["repository"] and
             any(ref["path"] == p or p.endswith("/") and ref["path"].startswith(p) for p in attempt["write_paths"]),
             "first write is outside the admitted implementation/artifact allowlist")
        store = ep.GitObjects(event["objects"])
        store.citation(ref)
        need(store.ancestor(ref["repository"], decision["head_sha"], ref["commit"]), "write is not based on admitted source")
        need(sa.blob(store, ref["repository"], decision["head_sha"], ref["path"]) != ref["blob"],
             "unchanged artifact/admission is not implementation")
        append(ledger, "receipt", attempt, "in_progress", at, receipt=receipt)
    elif event["kind"] == "review":
        need(attempt["receipt"] and not attempt["unsuccessful"], "review requires actual implementation receipt")
        snapshot = event["snapshot"]
        _, sources, _ = co.validate(snapshot, at)
        task = next(t for t in snapshot["tasks"] if key({"repository": t["repository"], "task_id": t["id"]}) == attempt["key"])
        pr = next(p for p in snapshot["prs"] if p["task_id"] == task["id"] and p["head_sha"] == task["head_sha"] and p["state"] == "open")
        need(all(sources[task["repository"], kind][0] for kind in ("tasks", "board", "prs", "reviews")),
             "review source observations incomplete/stale")
        proof = snapshot["evidence_policy"][task["id"]]
        store = ep.GitObjects(proof["objects"])
        need(store.ancestor(task["repository"], attempt["receipt"]["first_write"]["commit"], task["head_sha"]),
             "review predates this implementation receipt")
        state = event["state"]
        need(state in {"in_review", "validated", "rejected"}, "unsupported review state")
        accepted, rejected, conflicting = co.acceptance(task, pr, snapshot, at)
        need(state != "validated" or accepted and not conflicting, "independent exact-head acceptance required")
        need(state != "rejected" or rejected, "independent failure evidence required")
        need(state != "in_review" or task["status"] == "in_review", "canonical review transition required")
        need(event["evidence"], "review receipt required")
        append(ledger, "review", attempt, state, at, unsuccessful=state == "rejected",
               evidence=event["evidence"], input_digest=co.digest(snapshot))
    else:
        raise ValueError("unsupported event; there is no reset command")
    return {"status": "RECORDED", "attempt_id": attempt["attempt_id"], "state": ledger["events"][-1]["state"]}


def transaction(path, expected_revision, operation):
    """CAS and fsync before returning any handoff; crashed writes retain old data."""
    path = Path(path)
    with path.with_suffix(path.suffix + ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger = _load(path)
        need(ledger["revision"] == expected_revision, "stale ledger revision; reload before any dispatch")
        before = deepcopy(ledger)
        result = operation(ledger)
        need(ledger["history"] == before["history"] and ledger["events"][:len(before["events"])] == before["events"],
             "historical attempts cannot be rewritten")
        if ledger != before:
            with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, prefix=".dispatch-", delete=False) as stream:
                json.dump(ledger, stream, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
                temporary = stream.name
            os.replace(temporary, path)
            fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        return {**result, "revision": ledger["revision"]}


def load_queue(path):
    text = Path(path).read_text()
    need(text.count("```json\n") == 1, "READY_QUEUE needs one canonical JSON block")
    return ep.load_json(text.split("```json\n", 1)[1].split("```", 1)[0].encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["cycle", "record"])
    parser.add_argument("--queue", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--expected-revision", type=int, required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        queue, packet = load_queue(args.queue), _load(args.input)
        at = datetime.now(timezone.utc)
        def operation(ledger):
            validate(queue, ledger)
            return cycle(queue, ledger, packet["candidates"], packet["liveness"], at) if args.command == "cycle" else record(ledger, packet, at)
        result = transaction(args.ledger, args.expected_revision, operation)
    except (OSError, ValueError, KeyError, TypeError, StopIteration, ep.PolicyError) as exc:
        result = {"status": "INPUT_REQUIRED", "reason": str(exc)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"DISPATCH_REQUIRED", "RECORDED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
