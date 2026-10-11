# Bounded implementation dispatch — 2026-10-11

Craig requested this **new coordinator mechanism repair**. It does not restart
`ops-stuck-resource-20261011`, transfer any owner, reset a budget, or accept game work.
The [stall audit](../audits/2026-10-11-stall/README.md) explains the failure:
admission and repeated planning were reported without an implementation receipt.

1. **Select from [READY_QUEUE.md](READY_QUEUE.md).** At most five ready entries;
   this first rollout may admit at most three distinct candidates, one per cycle.
   The checked-in rollout limit is **one**, for the parent's independently
   reviewed game-task rollout. Only verified approved Lower City scopes enter.
   Preserve Muse/Craig ownership, frozen Shuto, paused NEON and all acceptance gates.
2. **Reconcile before selection.** The authorized collector supplies the exact
   board commit/blob/row, complete open-PR heads, explicit user-stop sources and
   actual session/queue observations. Bind their receipts to the snapshot digest.
   Use the existing [scoped guard](../watchdog/RUNBOOK.md#task-scoped-source-coverage-isolated-repair-2026-10-09).
   Unknown liveness is a hold; old GitHub activity is not proof of death. Record
   stops/denials persistently; changing executor, branch or a status description
   cannot remove them. The loop has no reset command.
3. **Reserve durably, then execute.** Run [dispatch_loop.py](../watchdog/dispatch_loop.py)
   `cycle --queue project-management/dispatch/READY_QUEUE.md --ledger <authoritative-ATTEMPTS.json>
   --expected-revision <N> --input <private-current-packets.json>`.
   The initial [ATTEMPTS.json](ATTEMPTS.json) preserves known counts and unknowns.
   CAS + file locking + fsync protect one shared backend. Before real use the
   parent must designate one serialized coordinator/backend, persist each revision
   to the canonical source-only handoff and refresh from it. Disposable copies or
   concurrent clones are not authoritative and must not launch. Re-run the existing
   `dispatch-guard` on the returned decision immediately before authorized tools
   create a session. These scripts never create sessions or deliver the legacy queue.
4. **Require proof of implementation.** Record the launch tool's opaque session ID
   (`record`, kind `session`); status stays `admitted`. Within ten minutes, record
   kind `receipt`: actual session/owner/executor, start/write times and the first
   changed code/artifact path with a hash-verified Git citation, based on the admitted
   head and inside the approved write allowlist. Task/board/admission edits are not
   implementation; reviewers must keep them out of that allowlist. Only this receipt
   yields `in_progress`. Persist sanitized references, never private prompts/notes.
5. **Bound attempts and rotate.** `open → ready → admitted → in_progress → in_review
   → validated/rejected/parked`. One initial attempt plus one evidence-based correction
   maximum, including preserved historical attempts. Unknown counts remain `null`
   and block that candidate. Missing receipts count as unsuccessful; live/unknown
   launches retain their reservations until exact liveness reconciliation. Select
   the next independently eligible candidate in the same cycle; never duplicate
   the task, executor or reserved write scope. `validated` needs the existing
   independent exact-head acceptance proof. A failed gate never becomes a pass here.
6. **Escalate precisely.** Empty/blocked queues return `ESCALATION_REQUIRED` with
   every considered candidate's reasons/receipts, never steady `IDLE`. Fix or hand
   off only the named blocker; do not invent work to fill the queue. The separate
   [C1 blocking repair](../tasks/ops-scoped-read-dependency-20261011.json) is proposal
   only; it neither bypasses the guard nor blocks unrelated scopes.

Communication/inspector roles and denied routes stay unchanged. No external-agent
contact, Actions, paid services, credential/security changes, merges or deletion
is authorized by this repair. [Deployment still requires Craig's explicit request](../watchdog/releases/PUSH-PROCEDURE.md#deployment-authorization-and-actions-budget-craig-2026-10-08-1956-utc).
