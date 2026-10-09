"""Safe CLI adapter: reads only explicitly supplied JSON; writes only stdout."""
import argparse
import json
from datetime import datetime, timezone

import coordinator

ALIASES = {
    "coordinator-plan", "dispatch-candidates", "dispatch-eligible", "dispatch-guard",
    "idle-defect-check", "all-blocked", "review-sweep", "heartbeat",
}
# These old commands can recommend, produce, consume or authorize an admission
# without the new snapshot contract. Retire them instead of keeping a bypass.
RETIRED = {
    "gate", "check-done", "classify", "decide", "nudge", "resume", "rebrief",
    "failover", "failover-undo", "register-worker", "assign", "liveness",
    "queue-action", "adopt-orphans", "classify-report", "sibling-check",
    "entry-start", "pending-validate", "validator-dispatched", "ship-verify",
    "publish-verify", "audit-task", "validate-task", "transitions",
}


def _load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError("non-finite JSON number")
    with open(path, "r", encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=unique, parse_constant=invalid_constant)


def run(command, argv, at=None):
    if command in RETIRED:
        print(json.dumps({"status": "INPUT_REQUIRED", "reason": "RETIRED_UNGUARDED_ROUTE", "command": command,
                          "next": "Use coordinator-plan with a fresh explicit snapshot; automatic dispatch is disabled"}))
        return 2
    class InputParser(argparse.ArgumentParser):
        def error(self, message):
            raise ValueError(message)
    parser = InputParser(prog="watch.py " + command)
    parser.add_argument("--snapshot")
    parser.add_argument("--decision")
    for key in ("task", "operation", "executor", "owner", "head"):
        parser.add_argument("--" + key)
    try:
        args, extra = parser.parse_known_args(argv)
        if not args.snapshot or extra:
            raise ValueError("--snapshot is required; legacy positional arguments are unsupported")
        snapshot = _load(args.snapshot)
        at = at or datetime.now(timezone.utc)
        # Every alias calls this same evaluator. Never use legacy state fallback.
        result = coordinator.evaluate(snapshot, at)
        if command == "dispatch-guard":
            if not args.decision or not all((args.task, args.operation, args.executor, args.owner, args.head)):
                raise ValueError("guard requires --decision, --task, --operation, --executor, --owner and --head")
            target = dict(task_id=args.task, operation=args.operation, executor_id=args.executor,
                          owner_id=args.owner, head_sha=args.head)
            result = coordinator.revalidate(snapshot, _load(args.decision), target, at)
        elif any((args.decision, args.task, args.operation, args.executor, args.owner, args.head)):
            raise ValueError("target/decision arguments are only supported by dispatch-guard")
    except (OSError, ValueError, TypeError) as exc:
        result = {"status": "INPUT_REQUIRED", "warnings": [str(exc)]}
    print(json.dumps(result, sort_keys=True))
    if result["status"] == "INPUT_REQUIRED":
        return 2
    if result["status"] == "NO_GO" or command == "idle-defect-check" and result["status"] == "ACTION_REQUIRED":
        return 3
    return 0
