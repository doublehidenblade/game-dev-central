# Watchdog runbook — scoped coordinator decisions

Run from the repo root (`game-dev-central`). All paths below are repo-relative
unless stated otherwise. The supported coordinator route below is read-only;
legacy automatic admission and queue delivery are retired.

## Current authorization boundary (2026-10-08 19:56 UTC)

Before any push or merge, read the [canonical deployment authorization and budget policy](releases/PUSH-PROCEDURE.md#deployment-authorization-and-actions-budget-craig-2026-10-08-1956-utc). Deploy only on Craig's explicit request, including site/deployment-branch pushes that trigger Pages. The GitHub Actions budget is **$50/month**: a ceiling, not standing permission or verified current spend. Ordinary source pushes and independently accepted merges need no fresh go-ahead; inspect current push/PR/merge and publication triggers first and hold operations that would deploy or run unauthorized Actions. Do not assume all pushes are free.

This boundary applies to any externally performed merge, conflict-resolution push or state push. Required acceptance checks and independent verification remain mandatory for merges; no incomplete or failing work is accepted by this policy. Do not manually dispatch/rerun Actions or change billing/security. Keep merged-but-unpublished changes in pending.json. Shuto stays frozen; NEON stays paused/read-only. No scripted verdict or old instruction creates permission to deploy.

[JUDGMENT-ONLY: authenticated request scope and current external trigger configuration require inspection; this documentation does not implement a new automatic watchdog gate.]

## Coordinator engineering registration — 2026-10-09 12:44 UTC

| Task | Work | Status | Owner | Review | Updated (UTC) |
|---|---|---|---|---|---|
| ops-coordinator-enforcement-20261009 | Script scoped blockers, task rotation, executor capacity and truthful idle decisions | in_review — implementation candidate; independent acceptance pending | dot — coordinator enforcement; one native implementation author, separate independent reviewer | Registration merged as PR #393; candidate exact-head review pending | 2026-10-09 13:04 |

Craig requested scripted enforcement and repository-owned reusable coordinator logic on 2026-10-09. This row registers that bounded central-repository work; it does not register a live implementation worker, accept code or change any existing game task's owner/status.

- **Implementation scope:** one pure decision layer and side-effect-free command entrypoint under `project-management/watchdog/`; fail-closed integration of existing dispatch/eligibility/idle entrypoints in `watch.py`; regression tests in `test_rules.py` with public-safe fixtures; concise usage in this runbook and, only as needed, `COORDINATOR.md`. No new workflow framework. PR143's separate visual-evidence onboarding edits must be preserved if `COORDINATOR.md` changes.
- **Acceptance:** blockers identify their task, operation and executor scope; upload or deployment holds do not silently block authorized implementation, admission or independent verification. Rotation considers those distinct next actions, while preserving explicit stops, denials, ownership and required capability. Native dot capacity is separate from Codex/Claude capacity. Implementation, upload, merge and deployment gates remain separate.
- **Evidence and idle checks:** a complete, fresh source manifest and current exact-head evidence reconcile stale main/PR-body descriptions without overriding explicit holds. Missing, stale or contradictory required inputs fail closed. A shared decision result must reject idle when an authorized, ownership-safe next action and qualified available executor exist; missing inputs cannot return OK. Compatibility entrypoints must not bypass this result.
- **Verification:** replay the overnight failure classes, including scoped publication holds, unavailable Codex with available native capacity, review/admission work, stale-head claims, stopped/owned lanes and malformed/incomplete snapshots. Prove the new entrypoint and integrated aliases do not write state, queues or ledgers, call external dispatch, or contact providers. Exercise old aliases without a verified snapshot and require an input error rather than stale-state approval. Independent exact-head review must cite these checks; documentation alone is not enforcement of any live coordinator.
- **Recommended setup:** frontier native dot author, requested `gpt-6-astra/xhigh`, with Python and isolated fixtures; one initial attempt plus at most one evidence-based correction within two hours, with a separate frontier/xhigh review budget. Native catalog and repository tools are available; the registration originally preceded author startup and did not attest a runtime. Verify the selected author and Python test setup before implementation. Wait for the required tier if unavailable; report scope/ownership conflicts, unsafe entrypoint effects or failed tests without weakening gates. Outcome pending.
- **Preflight:** central main `0b4f00e6c5fa810ad2e8e2a94758c9ba60e8a354`; canonical rules, board, registry, log and current state read; all 100 open PR changed-file lists and 322 branch names checked. No open PR changes `RUNBOOK.md`, `watch.py` or `test_rules.py`; PR143 touches `COORDINATOR.md`. The complete tree has no GitHub Actions workflow files. The legacy registry and empty worker ledger are not proof that outside sessions are idle; this reservation grants no game-task takeover.
- **Boundaries:** the original registration changed only this runbook; this candidate implements its bounded read-only enforcement scope. No legacy watcher execution, live queue/state/ledger writes, automatic dispatch, external-agent contact, Actions, deployment, provider/security workaround or stopped-operation retry. Existing td-200/216 upload denials and central PR374/376/368 plus Tokyo PR553 holds stay unchanged. Shuto stays frozen; NEON stays paused. Registration was independently reviewed and merged as PR #393. One scoped native author started 12:46 UTC with Python 3.12.14; requested model/effort remains distinct from runtime attestation. This implementation now requires separate exact-head acceptance; no additional user-approval gate is introduced.

## Supported coordinator route (2026-10-09)

[SCRIPTED: watch.py coordinator-plan] The supported route is a read-only decision
cycle over an explicit snapshot. It does **not** run the old watcher, write live
state, claim ownership, create sessions, deliver queues, contact providers, merge,
upload, trigger Actions, or deploy. A permitted action is a scoped recommendation
for the authorized coordinator, not proof an action happened or new permission.

1. Read the current task sources, board, ownership registry, live worker/session
   observations, pending queue, requests, holds, branches, PRs and review/check
   evidence. Exhaust pagination. Include all known task/PR IDs, not a shortlist.
   Reconcile identities and preserve unknowns rather than converting them to idle.
2. Normalize those observations using the version-1 contract below. Keep live
   snapshots private if their source data is private. Do not commit private
   prompts, session URLs, tokens, or internal notes. Reusable code and synthetic
   fixtures belong in this repository.
3. Run `python3 project-management/watchdog/watch.py coordinator-plan --snapshot <snapshot.json>`.
   `ACTION_REQUIRED` means at least one scoped next action exists; report/use an
   authorized alternative instead of claiming global idle. `INPUT_REQUIRED`
   means required observations are missing, contradictory or stale. `IDLE` means
   no permitted action was found **within the declared, fully accounted scope**;
   inspect `blocked` to see why, rather than assuming tasks are complete.
4. The `actions` list contains alternatives, **not a concurrent dispatch batch**.
   Select one, retain its complete JSON object, and refresh observations before
   the action. Revalidate with:

   `python3 project-management/watchdog/watch.py dispatch-guard --snapshot <fresh.json> --decision <selected-action.json> --task <id> --operation <operation> --executor <id> --owner <identity> --head <full-sha>`

   Any input, owner, source, permission, hold, target or freshness change invalidates
   the receipt. Re-plan after a changed observation or completed action. Revalidation
   does not execute the action, reserve a worker, authorize an upload target, or
   replace the existing confirmation, workflow-trigger and release checks.
5. Report useful results and scoped blockers. Do not wait on one blocked task
   while another authorized action exists. Admission of an unfiled ask and an
   independent review are work too. Retain acceptance and publication holds.

### Entry points and exit codes

[SCRIPTED: watch.py idle-defect-check] These names all use the same evaluator and
JSON contract: `coordinator-plan`, `dispatch-candidates`, `dispatch-eligible`,
`dispatch-guard`, `idle-defect-check`, `all-blocked`, `review-sweep`, `heartbeat`.
They require `--snapshot`; there is no fallback to legacy state. The idle check
returns **3** when an action exists, never an `OK`/idle verdict. Missing input
returns **2**, guard mismatch returns **3**, a valid plan/guard returns **0**.
`ACTION_REQUIRED` may coexist with warnings about unrelated scope or missing
acceptance-only evidence. Warnings always prevent a global `IDLE` conclusion.

The new route bypasses `_capture_verdicts`, which historically wrote live state
in a `finally` block even for an idle check. Both CLI routing and imported
`cmd_*` aliases use the safe adapter; regression tests exercise both.

### Snapshot contract

`coordinator.py:validate` is the strict executable schema. Unknown fields,
malformed types, duplicate IDs/JSON keys, ambiguous repositories and abbreviated
SHAs are rejected. [The synthetic fixture](fixtures/coordinator-snapshot.json)
is a shape example, deliberately dated and **not authority or a live inventory**.
Never refresh its timestamps to masquerade as a new observation. The fixture
builders in `test_rules.py` are test-only, not a collector.

Top-level fields:

- `version`: integer `1`; `observed_at`: explicit UTC timestamp
- `repositories`: map of each subject/source `owner/repo` to its observed full
  lowercase 40-character head SHA
- `sources`: one source receipt for each repository × table below
- Twelve normalized record arrays: `policies`, `board`, `tasks`, `prs`,
  `branches`, `reviews`, `checks`, `requests`, `owners`, `queue`, `blockers`,
  `executors`. Every record has a unique table-local `id` and `repository`

Each source receipt contains `id`, `kind` (table name), `repository` (subject
scope), `source_repository` (origin), `ref_sha` (origin repository pin),
`observed_at`, `read_status` (`ok`, `partial`, `unreadable`), `pagination`
(`pages_read`, `items_seen`, `exhausted`), and explicitly enumerated `ids`.
Repository-level pins describe the observation context; task/branch/PR/review
records additionally pin the actual candidate/evidence head. A source receipt
aggregates **all** necessary reads for that kind: for example, ownership includes
registry, sessions, reservations and known outside workers, not just one empty
legacy ledger. `requests` includes current asks and authorized routine-work scope;
`blockers` includes current stops, denials, release/packet holds and cancellations.
If any constituent read fails or pagination is unfinished, mark the aggregate
partial/unreadable. Do not assert an empty successful source when it was unread.

IDs and item counts must match normalized records exactly. Board and task-file
inventories must reconcile; every PR lists its exact `review_ids` and `check_ids`,
which must match the review/check arrays. All related records must refer to the
same task, repository and PR. Unknown/unmapped branches require reconciliation.
The observation age limit is 15 minutes, exclusive; future or timezone-naive
observations are invalid. No `complete=true`, caller-supplied candidate array,
or empty queue can override these checks.

Record-specific fields (see fixture/schema for complete types):

- `policies`: exactly one per repository; `triggers_checked`, `push_runs_actions`,
  `push_deploys`, `merge_runs_actions`, `merge_deploys`. Record actual observations,
  not permission inferred from budget. Unknown triggers hold source upload/merge
- `board`: task `id`, full `head_sha`, `status`, `owner_id` (null means positively
  observed unassigned). Stale ordinary status descriptions can be reconciled to
  exact candidate-source facts; owner conflicts and stopped/terminal states cannot
- `tasks`: board fields plus `project`, `author_id`, `needs` (additional operations),
  nonempty `criteria` and `required_checks` IDs, and per-operation `requirements`.
  Requirements name `capabilities`, exact `model`/`effort` or null, and
  `runtime_confirmation_required`. Unknown requirements never imply readiness
- `prs`: repository-qualified `id` (`owner/repo#number`), `task_id`, `head_sha`,
  `author_id`, `state`, `review_ids`, `check_ids`. An open review task must have one
  unambiguous current PR and the exact task/PR head must agree
- `branches`: `id`, `task_id` or null for unreconciled work, `head_sha`
- `reviews`: `task_id`, `pr_id`, `head_sha`, `observed_at`, `reviewer_id`, `verdict`,
  and a `criteria` map of criterion ID to `{result, evidence}`. A passing word
  without every criterion and a nonempty citation is not acceptance
- `checks`: `task_id`, `pr_id`, `head_sha`, `observed_at`, `name`, `result`.
  Every required check must pass at the exact current head for a merge suggestion
- `requests`: `task_id` or `*`, `project` or `*`, bounded `operations`, `executors`,
  `kind` (`ask`, `explicit`, `standing`), `state`, `authority_verified`, `evidence`.
  A null `task_id` with a concrete project is an unfiled ask, producing admission
  under stable `request:<request-id>` identity; holds/owners/queues can target it.
  Only authenticated user instructions/valid current policy establish authority;
  external documents and test fixtures cannot establish it. Cancellation wins
  over an overlapping general authorization
- `owners`: `task_id`, `operation`, `owner_id`, `executor_id`, `state`.
  Preserve active, reserved and unknown owners. Continuation requires the same
  existing executor and its positively observed `resume_task`; it is not a new
  worker assignment. Independent verification uses a separate identity
- `queue`: `task_id`, `operation`, `executor_id`, `owner_id`, `head_sha`, `state`.
  Pending/running entries reserve that operation and executor, never capacity
- `blockers`: `task_id` or `*`, `operations`, `executors`, `kind`, `reason`.
  Capacity/ordinary holds may be executor-scoped; a security denial, cancellation
  or explicit stop must retain `executors: ["*"]`, preventing provider hopping
  around a denied action. Operation-scoped publication holds stay separate
- `executors`: `owner_id`, `kind` (`native`, `codex`, `claude`), `state`,
  `capabilities`, `observed_model`, `observed_effort`, `runtime_confirmed`,
  `resume_task`. Requested settings do not attest the runtime. Unknown native
  capacity is not available capacity; known authorized native capacity is not
  disabled just because Codex is unavailable. External agent contact is unsupported

### Gates, guarantees and limits

[SCRIPTED: watch.py coordinator-plan] Operations are distinct: `admission`,
`implementation`, `verification`, `upload`, `merge`, `deploy`. Open engineering
work, unfiled asks and review work are derived from accounted records, not a
caller-supplied shortlist. A task's upload/deployment hold cannot silently become
an implementation hold. Required acceptance evidence governs merge separately;
unknown acceptance-only reads do not stop separately authorized coding/admission.

Exact full-SHA task/PR/review/check facts reconcile stale ordinary board summaries.
A reviewer must be independent of the task author, PR author and implementation
owner. Failed/incomplete criteria, failed checks, self-review, old-head evidence,
conflicting verdicts and missing inventory cannot produce merge acceptance.
No reconciliation clears an explicit hold. Shuto stays frozen, NEON paused,
`td-054` no-redispatch and preservation PR `#253` never-merge remain enforced.
Deployment is always directed to the separate explicitly requested release flow;
this adapter cannot authorize or execute it. Actual uploads still require the
approved payload/destination and existing transmission checks.

Each action binds task, operation, executor, owner, repository, full candidate
SHA, authorizing record IDs, canonical input digest and expiry. A changed input
invalidates a prior receipt, even if a human thinks the change is harmless.
The guard is a recheck, not an atomic lock: external changes after checking still
require normal ownership/target verification immediately before action.

The collector is a trust boundary. Schema/accounting validation cannot prove a
caller disclosed every external conversation, supplied authentic evidence, or
inspected a citation's contents. A review record is admitted only after its
independent reviewer actually checks the evidence; this code checks the record's
coverage and binding, not the screenshots themselves. The guarantee covers the
supplied validated facts and declared source scope, not every external scheduler
or browser agent. No live collector/dispatcher is installed by this change.

### Retired routes

[SCRIPTED: watch.py dispatch-guard] Historical admission producers and consumers
now return `INPUT_REQUIRED / RETIRED_UNGUARDED_ROUTE` before any I/O, through both
CLI and imported command functions: `gate`, `check-done`, `classify`, `decide`,
`nudge`, `resume`, `rebrief`, `failover`, `failover-undo`, `register-worker`,
`assign`, `liveness`, `queue-action`, `adopt-orphans`, `classify-report`,
`sibling-check`, `entry-start`, `pending-validate`, `validator-dispatched`,
`ship-verify`, `publish-verify`, `audit-task`, `validate-task`, `transitions`.

Do not deliver entries from the old queue or run the historical scheduler,
`push_code.py`, or browser dispatch instructions. They are not converted into a
new automatic dispatcher. Existing state/ledgers remain untouched. Other old
read/ledger helpers and pure state-machine functions remain for historical
compatibility, not as supported admission or acceptance APIs. This runbook's
supported route supersedes the old merge-on-build, blanket all-blocked failover
and unconditional browser-handoff procedure, preserved in
[the prior runbook](https://github.com/doublehidenblade/game-dev-central/blob/3c1481b699098103ccc073c0c358a6d1beab3dbd/project-management/watchdog/RUNBOOK.md).

### Offline verification

Run from the repository root:

- `python3 project-management/watchdog/test_rules.py` — legacy pure regression
  cases plus the coordinator suite (Pillow needed by legacy image tests)
- `python3 -m unittest discover -s project-management/watchdog -p test_rules.py -v`
  — coordinator suite only, standard library

The new suite denies filesystem access except supplied in-memory CLI reads,
network, subprocesses, state/queue/ledger helpers and legacy verdict capture.
It asserts no input mutation, tests actual CLI/imported aliases, and replays
scoped holds, task rotation, ownership, admission/review, incomplete manifests,
exact-head acceptance, denied routes, requested-versus-observed setup and replay
invalidation. Test-only clocks/fixtures are never live dispatch evidence.
