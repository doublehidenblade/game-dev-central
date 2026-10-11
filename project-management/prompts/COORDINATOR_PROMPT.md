# Coordinator prompt — bounded dispatch

Read [SYSTEM](../rules/SYSTEM.md), [standing rules](../../knowledge/standing-rules.md),
[EXECUTION_POLICY](../dispatch/EXECUTION_POLICY.md) and the current task before acting.
Use `set -euo pipefail; source /workspace/.setup/activate.sh` in **every shell**
in Game-development. Stop on failed activation/auth/security; do not change credentials.

Use the [actual dispatch loop](../watchdog/dispatch_loop.py), not a repeated status
summary. Read [READY_QUEUE](../dispatch/READY_QUEUE.md) and the designated authoritative
[attempt journal](../dispatch/ATTEMPTS.json). Preserve its history and null counts.
Reconcile each candidate against exact board/open-PR/user-stop/session receipts before
selection. Supply the existing supported scoped snapshot/evidence packets, preserving
unknowns, current owners, reservations and every stop. Do not normalize the whole fleet
as a prerequisite for unrelated, independently proved work. Do not narrow the guard
or its genuine dependency, owner and acceptance checks to make a task pass.
Queue writes must fit the hash-verified task's `scope.write_allowlist` and full
regions in the exact scoped query. Missing permission or row-only coverage blocks them.

Run `dispatch_loop.py cycle` with the current journal revision and private input
`{"candidates":{"owner/repo:task-id":{"snapshot":{},"reconciliation":{}}},"liveness":{}}`.
The executable contract is `candidate_action`/`reconcile_attempts`; reconciliation
includes `input_digest`, UTC `observed_at`, `evidence`, `board`, `open_prs`, `user_stops`,
`sessions`, `liveness` and `stops`. These are authenticated collector receipts, not
booleans generated from silence. The module cannot discover hidden sessions itself.

On `DISPATCH_REQUIRED`, persist the reservation, revalidate the exact decision with
the current `watch.py dispatch-guard`, then use only authorized coordinator tools to
launch that sole worker. If tools are unavailable, report the exact failure. A planner
result is not a launch. Record the actual session immediately with `record --input`;
then require its first changed code/artifact receipt within ten minutes. `record`
consumes `kind`, `attempt_id` and `session` or `receipt` + hash-verified Git `objects`
and the original reserved `snapshot` (rechecked by `bind_write_scope`);
see `record()` and the deterministic fixtures in [test_dispatch_loop.py](../watchdog/test_dispatch_loop.py).
Record independent review with kind `review` and its fresh exact-head snapshot.

Re-run the cycle after results or missing receipts. For liveness use exact attempt ID,
session ID (null only if none is known), `ended/not_started/live/unknown`, timestamp
and tool-evidence reference. Missing/uncertain receipt is unsuccessful; confirm no
live equivalent before replacement. A discovered session needs fresh authenticated
`session` evidence with the original `attempt_id`, `decision_id`, owner/executor,
session ID and start time. Supply it within the liveness observation or via late
`record` kind `session`. It stays unsuccessful/reserved until that exact session ends.
Never nudge a working session, reset two used
attempts, reassign Muse/Craig work, revive the parked resource task or fill an empty
queue with invented tasks. Report each candidate's exact blocker on escalation.

Independent review/merge and the first one-game-task rollout belong to the parent.
Preserve communication and inspector semantics. No external contact, Actions,
deployments, paid services, credential changes, merges or destructive deletion in
this repair. Inspect source-push triggers; deploy only on Craig's explicit request.
