# Historical RUNBOOK admission evidence

Source: `bec73fbfdb6d6a4fdcf920065ff2ce30a925e304:project-management/watchdog/RUNBOOK.md`; Git blob `e90c226df5d17f39fd6f878dbb61c68f754982e8`.
These are excerpts from the already-read immutable local source, not new observations, changed rules or a rerun. Original line numbers are retained.

## Original lines 183–218

```text
183: ## Supported coordinator route (2026-10-09)
184: 
185: [SCRIPTED: watch.py coordinator-plan] The supported route is a read-only decision
186: cycle over an explicit snapshot. It does **not** run the old watcher, write live
187: state, claim ownership, create sessions, deliver queues, contact providers, merge,
188: upload, trigger Actions, or deploy. A permitted action is a scoped recommendation
189: for the authorized coordinator, not proof an action happened or new permission.
190: 
191: 1. Read the current task sources, board, ownership registry, live worker/session
192:    observations, pending queue, requests, holds, branches, PRs and review/check
193:    evidence. Exhaust pagination. Include all known task/PR IDs, not a shortlist.
194:    Reconcile identities and preserve unknowns rather than converting them to idle.
195: 2. Normalize those observations using the version-1 contract below. Keep live
196:    snapshots private if their source data is private. Do not commit private
197:    prompts, session URLs, tokens, or internal notes. Reusable code and synthetic
198:    fixtures belong in this repository.
199: 3. Run `python3 project-management/watchdog/watch.py coordinator-plan --snapshot <snapshot.json>`.
200:    `ACTION_REQUIRED` means at least one scoped next action exists; report/use an
201:    authorized alternative instead of claiming global idle. `INPUT_REQUIRED`
202:    means required observations are missing, contradictory or stale. `IDLE` means
203:    no permitted action was found **within the declared, fully accounted scope**;
204:    inspect `blocked` to see why, rather than assuming tasks are complete.
205: 4. The `actions` list contains alternatives, **not a concurrent dispatch batch**.
206:    Select one, retain its complete JSON object, and refresh observations before
207:    the action. Revalidate with:
208: 
209:    `python3 project-management/watchdog/watch.py dispatch-guard --snapshot <fresh.json> --decision <selected-action.json> --task <id> --operation <operation> --executor <id> --owner <identity> --head <full-sha>`
210: 
211:    Any input, owner, source, permission, hold, target or freshness change invalidates
212:    the receipt. Re-plan after a changed observation or completed action. Revalidation
213:    does not execute the action, reserve a worker, authorize an upload target, or
214:    replace the existing confirmation, workflow-trigger and release checks.
215: 5. Report useful results and scoped blockers. Do not wait on one blocked task
216:    while another authorized action exists. Admission of an unfiled ask and an
217:    independent review are work too. Retain acceptance and publication holds.
218: 
```

## Original lines 253–272

```text
253: Each source receipt contains `id`, `kind` (table name), `repository` (subject
254: scope), `source_repository` (origin), `ref_sha` (origin repository pin),
255: `observed_at`, `read_status` (`ok`, `partial`, `unreadable`), `pagination`
256: (`pages_read`, `items_seen`, `exhausted`), and explicitly enumerated `ids`.
257: Repository-level pins describe the observation context; task/branch/PR/review
258: records additionally pin the actual candidate/evidence head. A source receipt
259: aggregates **all** necessary reads for that kind: for example, ownership includes
260: registry, sessions, reservations and known outside workers, not just one empty
261: legacy ledger. `requests` includes current asks and authorized routine-work scope;
262: `blockers` includes current stops, denials, release/packet holds and cancellations.
263: If any constituent read fails or pagination is unfinished, mark the aggregate
264: partial/unreadable. Do not assert an empty successful source when it was unread.
265: 
266: IDs and item counts must match normalized records exactly. Board and task-file
267: inventories must reconcile; every PR lists its exact `review_ids` and `check_ids`,
268: which must match the review/check arrays. All related records must refer to the
269: same task, repository and PR. Unknown/unmapped branches require reconciliation.
270: The observation age limit is 15 minutes, exclusive, including each review/check
271: record's `observed_at`; a fresh aggregate receipt cannot refresh an old individual
272: read. Future or timezone-naive observations are invalid. No `complete=true`, caller-supplied candidate array,
```

## Original lines 377–420

```text
377: ### Gates, guarantees and limits
378: 
379: [SCRIPTED: watch.py coordinator-plan] Operations are distinct: `admission`,
380: `implementation`, `verification`, `upload`, `merge`, `deploy`. Open engineering
381: work, unfiled asks and review work are derived from accounted records, not a
382: caller-supplied shortlist. A task's upload/deployment hold cannot silently become
383: an implementation hold. Required acceptance evidence governs merge separately;
384: unknown acceptance-only reads do not stop separately authorized coding/admission.
385: Unrelated unmapped/unknown branches remain a coverage warning, but do not suppress
386: independently verified read-only verification at an exact open/merged PR head.
387: All mutation operations still require complete branch and ownership observations.
388: Explicit `needs: ["verification"]` on a merged task can request post-merge review;
389: it never restarts implementation, repeats the merge, or treats the merge as
390: independent acceptance. Missing exact source/readiness facts return
391: `INPUT_REQUIRED`, including when the rest of the inventory is complete.
392: 
393: Exact full-SHA task/PR/review/check facts reconcile stale ordinary board summaries.
394: Same-head closed/merged board or terminal PR facts require reconciliation
395: before an open task can restart implementation; stale source text cannot reopen
396: completed work. A reviewer must be independent of the task author, PR author and implementation
397: owner. Failed/incomplete criteria, failed checks, self-review, old-head evidence,
398: conflicting verdicts and missing inventory cannot produce merge acceptance.
399: Conflicting same-head PASS/FAIL verdicts remain an acceptance/mutation hold, but
400: explicit `needs: ["verification"]` can preserve an independently authorized
401: read-only review to resolve the dispute. That action must still pass every
402: source, ownership, capability and stop gate; the conflict warning stays visible.
403: Known exact-head merged source and its acceptance conflicts are reconciled even
404: when no verification operation is requested. Removing a need cannot clear a hold
405: or turn conflicting evidence into idle. Missing optional PR linkage does not
406: create a blanket upload hold; each operation retains its own source requirements.
407: No reconciliation clears an explicit hold. Shuto stays frozen, NEON paused,
408: `td-054` no-redispatch and preservation PR `#253` never-merge remain enforced.
409: Deployment is always directed to the separate explicitly requested release flow;
410: this adapter cannot authorize or execute it. Actual uploads still require the
411: approved payload/destination and existing transmission checks.
412: 
413: Each action binds task, operation, executor, owner, repository, full candidate
414: SHA, authorizing record IDs, canonical input digest and expiry. A changed input
415: invalidates a prior receipt, even if a human thinks the change is harmless.
416: The guard is a recheck, not an atomic lock: external changes after checking still
417: require normal ownership/target verification immediately before action.
418: 
419: The collector is a trust boundary. Schema/accounting validation cannot prove a
420: caller disclosed every external conversation, supplied authentic evidence, or
```

## Original lines 480–501

```text
480: ## Evidence-feedback policy integration (2026-10-09)
481: 
482: Read [EVIDENCE_POLICY.md](EVIDENCE_POLICY.md) before constructing an admission or
483: completion packet. The coordinator independently supplies current authority,
484: complete canonical rule inventory, task/source scope, ownership/stops and
485: actor-observation receipts. Worker submissions do not establish authority.
486: Raw Git commit/tree/blob objects prove immutable artifact membership.
487: 
488: Use `watch.py brief-check --authority <file> --submission <file> --objects <file>`
489: for admission and `watch.py acceptance-check` with the same arguments for
490: completion. `evidence-check`, `evidence-checks` and `validator-check` use the
491: same completion result; exit 2 is missing input, exit 3 is a denied/stopped gate.
492: No positional/header-only or filename-only route grants acceptance.
493: 
494: Include each task's `{authority, submission, objects}` packet in
495: `snapshot.evidence_policy[task_id]` before coordinator implementation/upload or
496: merge decisions. All PR396 source/permission/owner/stop/operation guards remain.
497: Missing/conflicting completion evidence must not suppress independently
498: permitted read-only verification; it still blocks acceptance/merge. An unfiled
499: ask's admission action is registration only, not production implementation.
500: No workflow dispatch, deployment, external contact or queue/ledger write follows
501: from a policy result. Explicit human visual/device judgments stay separate.
```

## Original lines 580–589

```text
580: ### Supported scope and honest limits
581: 
582: - Version 1 supports one exact filed-task `implementation`, `verification`,
583:   `upload` or `merge` operation with one current open/draft PR and candidate
584:   branch. Unfiled-ask registration, post-merge review and deployment retain the
585:   existing routes; they cannot be smuggled through this scoped schema.
586: - A successful scoped action leaves `source_scope.global_coverage: unknown` and
587:   a visible coverage warning. No scoped-only snapshot can yield global `IDLE`.
588:   Incomplete global source receipts remain incomplete; do not reseal them as
589:   complete just to obtain an action.
```

