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
| ops-coordinator-enforcement-20261009 | Script scoped blockers, task rotation, executor capacity and truthful idle decisions | accepted and merged — PR396 review5471277399; merge39aa747c7f1f35393a316faebd942386579ff913 | dot — coordinator enforcement; one native implementation author, separate independent reviewer | Registration PR393; final PR396 independently accepted and merged at2026-10-09T14:17:33Z; runtime attestation remains unconfirmed; no live collector installed | 2026-10-09 14:17 |

Craig requested scripted enforcement and repository-owned reusable coordinator logic on 2026-10-09. This row registers that bounded central-repository work; it does not register a live implementation worker, accept code or change any existing game task's owner/status.

- **Implementation scope:** one pure decision layer and side-effect-free command entrypoint under `project-management/watchdog/`; fail-closed integration of existing dispatch/eligibility/idle entrypoints in `watch.py`; regression tests in `test_rules.py` with public-safe fixtures; concise usage in this runbook and, only as needed, `COORDINATOR.md`. No new workflow framework. PR143's separate visual-evidence onboarding edits must be preserved if `COORDINATOR.md` changes.
- **Acceptance:** blockers identify their task, operation and executor scope; upload or deployment holds do not silently block authorized implementation, admission or independent verification. Rotation considers those distinct next actions, while preserving explicit stops, denials, ownership and required capability. Native dot capacity is separate from Codex/Claude capacity. Implementation, upload, merge and deployment gates remain separate.
- **Evidence and idle checks:** a complete, fresh source manifest and current exact-head evidence reconcile stale main/PR-body descriptions without overriding explicit holds. Missing, stale or contradictory required inputs fail closed. A shared decision result must reject idle when an authorized, ownership-safe next action and qualified available executor exist; missing inputs cannot return OK. Compatibility entrypoints must not bypass this result.
- **Verification:** replay the overnight failure classes, including scoped publication holds, unavailable Codex with available native capacity, review/admission work, stale-head claims, stopped/owned lanes and malformed/incomplete snapshots. Prove the new entrypoint and integrated aliases do not write state, queues or ledgers, call external dispatch, or contact providers. Exercise old aliases without a verified snapshot and require an input error rather than stale-state approval. Independent exact-head review must cite these checks; documentation alone is not enforcement of any live coordinator.
- **Recommended setup:** frontier native dot author, requested `gpt-6-astra/xhigh`, with Python and isolated fixtures; one initial attempt plus at most one evidence-based correction within two hours, with a separate frontier/xhigh review budget. Native catalog and repository tools are available; the registration originally preceded author startup and did not attest a runtime. Verify the selected author and Python test setup before implementation. Wait for the required tier if unavailable; report scope/ownership conflicts, unsafe entrypoint effects or failed tests without weakening gates. Outcome pending.
- **Attempt amendment — 2026-10-09 13:28 UTC:** the initial candidate `b765a587cd78554d047e06b6bafee9de91c1be7e` and first correction `82a6df52855a3b3a07b9bdc177684214e2946ff0` are retained. [The coordinator's bounded amendment](https://github.com/doublehidenblade/game-dev-central/pull/396#issuecomment-6081855820) authorizes one additional correction for two reproduced read-only routing defects: unrelated unmapped branches blocking exact-head verification, and explicit post-merge verification losing its source. The outer deadline stays 2026-10-09 14:46:40 UTC. No broader retry, weaker acceptance, live operation or merge is authorized by this amendment; independent repaired-head review remains required.
- **Bounded v4 correction — 2026-10-09 14:00 UTC:** v3 `b0b3c8a465c0cfd6b1b03fc87092094dbf29a457` is retained with its changes-required review. [The recorded amendment](https://github.com/doublehidenblade/game-dev-central/pull/396#issuecomment-6082442592) allows only the independently reproduced acceptance-isolation repair: conflicting same-head PASS/FAIL acceptance must retain a separately authorized, explicitly needed independent read-only verification path, while conflict warnings, acceptance/mutation blocks and all source/ownership/capability/stops remain. Both open and merged regression probes are retained. The original 14:46:40 UTC outer deadline and separate exact-head review remain; evidence-feedback framework work is outside this task.
- **Bounded v5 correction — 2026-10-09 14:11 UTC:** v4 `bf4251a0c63464bf91457352e2bd3e504b5904c4` is retained. Independent review reproduced a remaining same-family defect: removing verification from a merged task's needs hid its known same-head conflicting acceptance and could recommend upload or false idle. The coordinator authorized a bounded correction to resolve known immutable source/acceptance independently of the requested operation list, within the original 14:46:40 UTC deadline. The unchanged independent 128-case needs matrix and two-case hold-invariance probe are retained; unrelated operation-specific source requirements are not broadened. Independent exact-head acceptance remains pending.
- **Preflight:** central main `0b4f00e6c5fa810ad2e8e2a94758c9ba60e8a354`; canonical rules, board, registry, log and current state read; all 100 open PR changed-file lists and 322 branch names checked. No open PR changes `RUNBOOK.md`, `watch.py` or `test_rules.py`; PR143 touches `COORDINATOR.md`. The complete tree has no GitHub Actions workflow files. The legacy registry and empty worker ledger are not proof that outside sessions are idle; this reservation grants no game-task takeover.
- **Boundaries:** the original registration changed only this runbook; this candidate implements its bounded read-only enforcement scope. No legacy watcher execution, live queue/state/ledger writes, automatic dispatch, external-agent contact, Actions, deployment, provider/security workaround or stopped-operation retry. Existing td-200/216 upload denials and central PR374/376/368 plus Tokyo PR553 holds stay unchanged. Shuto stays frozen; NEON stays paused. Registration was independently reviewed and merged as PR #393. One scoped native author started 12:46:40 UTC with Python 3.12.14, reverified for the v5 correction; requested model/effort remains distinct from runtime attestation. PR396 received independent exact-head acceptance in review5471277399 and merged as39aa747c7f1f35393a316faebd942386579ff913 at2026-10-09T14:17:33Z. Requested/native selection remains distinct from runtime attestation; no live collector or dispatcher is installed. Later evidence-policy changes require their own independent acceptance; no additional user-approval gate is introduced.

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
The observation age limit is 15 minutes, exclusive, including each review/check
record's `observed_at`; a fresh aggregate receipt cannot refresh an old individual
read. Future or timezone-naive observations are invalid. No `complete=true`, caller-supplied candidate array,
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
  unambiguous current PR and the exact task/PR head must agree. An explicit
  post-merge verification resolves one exact-head merged PR; merged status alone
  is never acceptance
- `branches`: `id`, `task_id` or null for unreconciled work, `head_sha`
- `reviews`: `task_id`, `pr_id`, `head_sha`, `observed_at`, `reviewer_id`, `verdict`,
  optional original `performed_at`, and a `criteria` map of criterion ID to `{result, evidence}`. A passing word
  without every criterion and a nonempty citation is not acceptance
- `checks`: `task_id`, `pr_id`, `head_sha`, `observed_at`, `name`, `result`,
  and optional original `performed_at`.
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
  `resume_task`. An optional, complete selection record adds `selected_model`,
  `selected_effort`, `selection_verified` and `selection_evidence`. This records
  fresh supported catalog/admission evidence, not a model name merely requested
  in a prompt. When `runtime_confirmation_required` is false, matching verified
  selection plus required capabilities can establish readiness while
  `runtime_confirmed: false` and null observed model/effort remain truthful. If
  runtime attestation is required, selection cannot substitute; a known actual
  runtime mismatch cannot be hidden by selected settings. Missing required setup
  evidence yields `INPUT_REQUIRED`, not idle. Unknown native
  capacity is not available capacity; known authorized native capacity is not
  disabled just because Codex is unavailable. External agent contact is unsupported

### Constructing a truthful snapshot with connected reads

This change installs no collector. The coordinator constructs a new JSON object
from its actual connected-source observations; it must run the plan/guard before
its next dispatch or idle report. Passing synthetic fixtures proves tests only,
not adoption of a live loop.

1. Declare the relevant repository scope and read each current full head SHA.
   Read the canonical rules, task/board records, registrations, queues and holds
   at those pins. Enumerate source task IDs before selecting work. Do not omit
   completed/blocked/owned records that are needed to explain known tasks.
2. Use connected GitHub reads to enumerate branches and open PRs through the last
   page, plus each known task-linked closed/merged PR needed for reconciliation.
   Read candidate task files at exact branch/PR heads, PR authors/current heads,
   complete review lists and required check results. Keep all returned task/PR/
   review IDs in the receipt before normalizing candidates. Copy immutable full
   SHAs rather than a title, short SHA or PR-body description.
3. Read the ownership registry and currently available worker/session observations,
   including native work, reserved owners and pending operations. An old empty
   watchdog ledger is not evidence that outside workers are absent. Record
   actual observed native capacity and tools. For a supported native selection,
   copy its verified catalog/admission model and effort into the selection fields,
   cite that observation, and leave runtime identity unconfirmed when unexposed.
   Carry current authenticated asks/authorizations and all stops/denials into
   their separate tables without broadening the authorized action or audience.
4. Record the UTC read time and returned IDs/counts for each constituent source.
   Build each repository/table receipt from those reads: `ok` and `exhausted`
   only when every required constituent succeeded and pagination ended. If any
   required part is unavailable, retain observed IDs and use `partial` or
   `unreadable`; do not fill an empty successful receipt. Never use the test-only
   `coordinator_seal` helper as proof of external completeness.
5. For review/check evidence, preserve the source's original execution/submission
   time in `performed_at` when known. Refresh `observed_at` only after freshly
   retrieving the immutable result and checking its current PR/head applicability.
   Old evidence does not require a rerun just because it is old; old observations
   cannot authorize a merge. Do not rewrite an original performance time.
6. Save this newly constructed object to an ordinary private input file, run the
   supported command above, and resolve the reported missing inputs without
   changing true facts to make it pass. Select one action, refresh observations,
   then run the guard with the selected receipt and exact target. A receipt from
   a different input, owner, head or expired read cannot be reused. Leave live
   state/queues unchanged; any actual authorized assignment is a separate action.

A scope-bounded `IDLE` result must be reported with its repository coverage and
blockers. It is never a claim that all the user's projects, unknown external
sessions or undeclared sources have no work.

### Gates, guarantees and limits

[SCRIPTED: watch.py coordinator-plan] Operations are distinct: `admission`,
`implementation`, `verification`, `upload`, `merge`, `deploy`. Open engineering
work, unfiled asks and review work are derived from accounted records, not a
caller-supplied shortlist. A task's upload/deployment hold cannot silently become
an implementation hold. Required acceptance evidence governs merge separately;
unknown acceptance-only reads do not stop separately authorized coding/admission.
Unrelated unmapped/unknown branches remain a coverage warning, but do not suppress
independently verified read-only verification at an exact open/merged PR head.
All mutation operations still require complete branch and ownership observations.
Explicit `needs: ["verification"]` on a merged task can request post-merge review;
it never restarts implementation, repeats the merge, or treats the merge as
independent acceptance. Missing exact source/readiness facts return
`INPUT_REQUIRED`, including when the rest of the inventory is complete.

Exact full-SHA task/PR/review/check facts reconcile stale ordinary board summaries.
Same-head closed/merged board or terminal PR facts require reconciliation
before an open task can restart implementation; stale source text cannot reopen
completed work. A reviewer must be independent of the task author, PR author and implementation
owner. Failed/incomplete criteria, failed checks, self-review, old-head evidence,
conflicting verdicts and missing inventory cannot produce merge acceptance.
Conflicting same-head PASS/FAIL verdicts remain an acceptance/mutation hold, but
explicit `needs: ["verification"]` can preserve an independently authorized
read-only review to resolve the dispute. That action must still pass every
source, ownership, capability and stop gate; the conflict warning stays visible.
Known exact-head merged source and its acceptance conflicts are reconciled even
when no verification operation is requested. Removing a need cannot clear a hold
or turn conflicting evidence into idle. Missing optional PR linkage does not
create a blanket upload hold; each operation retains its own source requirements.
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
- `python3 project-management/watchdog/test_coordinator_review.py` — unchanged
  32-assertion independent correction/adoption probes, including the two new
  failure classes. Kept separately from the author's regression methods
- `python3 project-management/watchdog/test_coordinator_acceptance_isolation.py`
  — independent 14-case acceptance-versus-review matrix for open and merged PRs
- `python3 project-management/watchdog/test_coordinator_final_guards.py`
  — independent 15-case source, stop, ownership and operation-isolation probes
- `python3 project-management/watchdog/test_coordinator_operation_needs.py`
  — independent 128-case open/merged × all needs subsets × clean/conflicting
  acceptance matrix
- `python3 project-management/watchdog/test_coordinator_hold_invariance.py`
  — independent two-case proof that removing verification cannot erase a hold

The acceptance-isolation and final-guard probe sources were restored from their retained exact review text
after the review workspace was replaced. Rerunning them against the retained v3
head reproduced the original 2/14 and 1/15 failures before this correction; their
restored source bytes are committed unchanged here. They are synthetic regression
evidence, not a live coordinator inventory or independent acceptance of v5.

The new suite denies filesystem access except supplied in-memory CLI reads,
network, subprocesses, state/queue/ledger helpers and legacy verdict capture.
It asserts no input mutation, tests actual CLI/imported aliases, and replays
scoped holds, task rotation, ownership, admission/review, incomplete manifests,
exact-head acceptance, denied routes, requested-versus-observed setup and replay
invalidation. Test-only clocks/fixtures are never live dispatch evidence.

## Evidence-feedback policy integration (2026-10-09)

Read [EVIDENCE_POLICY.md](EVIDENCE_POLICY.md) before constructing an admission or
completion packet. The coordinator independently supplies current authority,
complete canonical rule inventory, task/source scope, ownership/stops and
actor-observation receipts. Worker submissions do not establish authority.
Raw Git commit/tree/blob objects prove immutable artifact membership.

Use `watch.py brief-check --authority <file> --submission <file> --objects <file>`
for admission and `watch.py acceptance-check` with the same arguments for
completion. `evidence-check`, `evidence-checks` and `validator-check` use the
same completion result; exit 2 is missing input, exit 3 is a denied/stopped gate.
No positional/header-only or filename-only route grants acceptance.

Include each task's `{authority, submission, objects}` packet in
`snapshot.evidence_policy[task_id]` before coordinator implementation/upload or
merge decisions. All PR396 source/permission/owner/stop/operation guards remain.
Missing/conflicting completion evidence must not suppress independently
permitted read-only verification; it still blocks acceptance/merge. An unfiled
ask's admission action is registration only, not production implementation.
No workflow dispatch, deployment, external contact or queue/ledger write follows
from a policy result. Explicit human visual/device judgments stay separate.

## Timeout discipline (2026-10-09)

A timeout of the coordinator's own run never waives independent acceptance.

Incident: 2026-10-09, the 11:42 UTC watchdog run timed out and merged PR #610
(td-247 harness + trace evidence) with no validator pass. The post-merge
retro-validator verdict (#613) could not retroactively satisfy the pre-merge
gate, and its all-PASS verdict was overbroad — the per-tick trace lacked the
required source-SHA/Godot/build provenance header — so td-247 had to move back
to in_review for the provenance gap (dot timeout-gate reconciliation,
game-dev-central#358 comment 6085103271).

Rules going forward:

- On a timeout, keep the pending operation BLOCKED and proceed to another
  independently ready task. Never merge first and reconcile later.
- Evidence-only merges are not exempt from independent acceptance.
- Retro-validation is a repair/reconciliation route, never a substitute for
  the pre-merge gate; record that honestly in the task's evidence list.
- Per EVIDENCE_POLICY.md, a gate receipt (authority/submission/objects refs)
  is recorded before every merge decision; the absence of a receipt is itself
  a stop condition.

## Duplicate dispatch after timeout (2026-10-09)

Incident: the 11:42 UTC watchdog run timed out before recording its td-246
worker dispatch. The supervisor, seeing no branch and no record, dispatched a
second td-246 worker. Both workers completed independently: PR #618
(fix/td-246-bust-speed-production) and PR #619 (td-246-bust-evidence, merged
17:15:03Z). The td-246 validator merged #618, which overwrote #619's
`td246_bust_run.log` and task file; it repaired by restoring #619's log as
`godot/qa/td-246/td246_bust_run_619.log`, independently verified both evidence
sets (all criteria PASS under both), and cited both in the verdict
(docs PR #621, 08b03939). No game code was ever at risk (both evidence-only);
nothing was lost.

Rules going forward:

Rules going forward (reconciled 2026-10-09, dot game-dev-central#358):

- A dispatch is not real until it is recorded as a *receipted* admission: the
  authorized route is `watch.py coordinator-plan --snapshot <fresh.json>`
  (see "Supported coordinator route" above), one selected action re-validated
  with `watch.py dispatch-guard --snapshot <fresh.json> --decision <action>`,
  and the decision + dispatch-guard receipt (task, operation, executor, owner,
  full head SHA, UTC timestamps) appended to the coordinator log. The legacy
  `register-worker` and `state-push` admission routes are RETIRED (see
  "Retired routes" above) — do not require them, do not execute them, and do
  not write RUNBOOK instructions that presume them. A dispatch recorded only
  in a scheduler's local memory (or lost to a timeout) has no standing.
- If a run times out before its dispatch receipt exists, the next run assumes
  *unknown* dispatch state and checks actual live state BEFORE any
  re-dispatch: live branches (exhaustive pagination, filtered by task prefix),
  `pulls?head=<branch>`, recent task-file commits, and open PRs. Never
  dispatch a replacement on "no branch seen" or "no record" alone when the
  previous run may have dispatched silently. A dispatch receipt with a live
  branch or open PR is proof of life; its absence is unknown, not idle.
- Heartbeats are a second positive signal, never a death sentence: Craig's
  liveness rule — absence of heartbeat is insufficient to duplicate; a worker
  that IS heartbeating must never be duplicated. Only actual
  session/branch/receipt checks decide lost vs. unknown; never duplicate on
  heartbeat absence alone. (The 2026-10-09 wording "presumed lost after 30
  minutes without heartbeat" is struck.)
- When a duplicate mergeoverwrites a sibling's evidence, restore (never
  delete): keep both evidence sets, verify both, cite both.


## Task-scoped source coverage (isolated repair, 2026-10-09)

The existing `coordinator-plan` / `dispatch-guard` route accepts an optional
`scoped_source` object in the same snapshot. This repairs a source-accounting
circularity: an independently safe filed-task operation need not normalize every
historical task or infer current liveness for every old branch. It does **not**
waive acceptance, current rule acknowledgment, real required checks, ownership,
user stops, denied routes or publication policy. No collector or dispatcher is
installed. Craig's exception admitted only the isolated repair itself.

### Supported scope and honest limits

- Version 1 supports one exact filed-task `implementation`, `verification`,
  `upload` or `merge` operation with one current open/draft PR and candidate
  branch. Unfiled-ask registration, post-merge review and deployment retain the
  existing routes; they cannot be smuggled through this scoped schema.
- A successful scoped action leaves `source_scope.global_coverage: unknown` and
  a visible coverage warning. No scoped-only snapshot can yield global `IDLE`.
  Incomplete global source receipts remain incomplete; do not reseal them as
  complete just to obtain an action.
- Raw branch and open-PR inventories must still be exhaustively enumerated for
  every declared repository. Their full SHA inventory is retained even when
  historical tasks are not normalized. This is bounded *normalization and
  liveness*, not permission to search only a task-name prefix or hide a sibling.
- Normalize only the target in `task_ids`. Multi-task prerequisite graphs fail
  closed in this first version: complete canonical/transitive source proof is
  not implemented, so an owner-free status word cannot imply readiness. Other
  related identities, including a canonical `parent_task` and selected board-row keys,
  must appear in `related_task_ids` for ownership/stop queries. A parent relation
  alone does not assert a completed prerequisite. Canonical `depends_on` and
  `dependencies`, when present, must be empty string-ID lists; a nonempty graph
  or unsupported shape requires canonical/transitive reconciliation outside this
  scoped-v1 route. Source-file dependency/owner regions remain protected.
- Source/dependency/owner-region closure is an authenticated collector and
  independent-review responsibility. The code proves candidate diff coverage,
  named canonical source/rule paths and Git exclusions, and rejects declared
  prerequisite graphs it cannot prove;
  it cannot discover an undisclosed semantic dependency or external session.
  Unknown relevant scope, inability to perform the exact queries, or an
  unresolved owner/queue reservation is a blocker, not an empty successful read.
- Existing source/owner/state guards are retained. Relevant prerequisite
  task/board ownership, unfinished/unknown states, conflicting rows, owner
  records, queued work and holds cannot disappear behind a branch exclusion.
  Branch ancestry is evidence about source bytes, never proof of worker death.
- Table-row scoping is conservative. It supports unique simple first-cell IDs
  in header-led pipe-row blocks, including this board's historical blank-
  separated row blocks. Candidate row keys must exactly equal its real row
  delta. All non-row bytes, each row's context anchor/order and regular-file
  mode are retained. Duplicate IDs, header/context edits, row moves/reordering,
  table creation/deletion or unsupported formats fail closed. There is no
  blanket documentation exemption. Use whole-file scope when appropriate.

### Scoped object contract

Keep the normal version-1 snapshot, its relevant normalized tables and its
truthful global `sources`. Add one `scoped_source` with exactly:

- `version: 1`
- `binding`: exact `task_id`, `repository`, `operation`, `executor_id`,
  `owner_id`, `head_sha` (all SHA values are full lowercase 40-character IDs)
- `base_heads`: exactly the snapshot repository map and current evidence-policy
  `rule_heads`, including cross-repository rule authorities
- `task_ids` (exactly the target), `related_task_ids`: identities described above
- `regions`: `{repository, path, row_keys}` objects. An empty `row_keys` means
  the entire exact file; a trailing slash means an entire directory. Nonempty
  row keys require an exact file. Include every candidate changed path, the
  canonical task, every canonical evidence source path, current rules and all
  additional relevant dependency/owner regions. Rules/tasks cannot use row
  exclusion
- `candidate`: `pr_id`, `branch_id`, `fork_sha`, `base_chain`, `head_chain`.
  The chains go from current base and candidate head to the same proved
  ancestor. Every listed parent edge is verified from hash-checked raw commits
- `inventory`: `branches` and `prs` arrays. Each item has `id`, `repository`,
  `head_sha`, `proof`; PRs also have `branch_id`, `author_id`. Use repository-
  qualified branch IDs. PR IDs retain `owner/repo#number`. Every PR head branch
  must be observed at the identical head; every current base must be represented
- `receipts`: scoped collection receipts below
- `objects`: the existing raw Git object representation used by evidence policy
  (`repository -> SHA -> {type, base64}`). Missing objects never mean absent
  files. All inspected objects are content-hash verified

Inventory proof variants are deliberately not `unrelated: true`:

1. `{"kind":"candidate"}` only for the exact selected branch and current PR
2. `{"kind":"base_ancestor","chain":[...]}` proves the source head is already
   contained by the current base, including the base itself
3. `{"kind":"candidate_ancestor","chain":[...]}` can account for an older
   branch contained by this candidate; never an overlapping open sibling PR
4. `{"kind":"disjoint","fork_sha":"...","base_chain":[...],"head_chain":[...]}`
   proves the fork and computes a complete Git tree diff. Every relevant region
   must be unchanged by that delta, or its entire relevant result must already
   equal the current base (accounting for an already-contained squash result).
   Unknown/overlapping source stays blocked; labels and task-name prefixes do
   not establish disjointness

The candidate's protected source dependencies must also be unchanged between its
fork and current base, or exactly equal its reviewed candidate. Current canonical
rule files that the candidate does not edit are checked at their actual current
base membership instead: the unchanged evidence-policy gate separately requires
current acknowledgment and applicable independent evidence. A rule edit in the
candidate does not receive this treatment. Full-file equivalence includes Git
file mode, not just blob bytes.

### Actual scoped collection receipts

For each required table in every declared repository, provide one receipt with:
`id`, `kind`, `repository`, `source_repository`, `ref_sha`, `observed_at`,
`read_status`, `pagination`, `ids`, `query_digest`, `inventory_digest`,
`records_digest`, `provenance`.

- Perform the exact query represented by `scoped_admission.query(scope)` against
  every relevant constituent. It includes all related task identities,
  prerequisite identities, protected regions, global/wildcard holds and all
  target-owner/target-executor reservations anywhere. The binding retains the
  operation. Do not omit an unknown branch/session/owner or scope a provider
  denial down to one provider. Read-only verification retains its original
  independent-identity requirements
- In `provenance`, identify the actual authenticated sources, their coverage,
  how relevant identities/regions were resolved, and what was inspected. A
  receipt's existence or a fabricated provenance string is not authentication.
  Incomplete/unreadable queries must remain blocked. Source collection and
  identity attestation are the same explicit trust boundary as evidence policy
- `ids` equals the complete raw inventory for branches/PRs, or the complete
  relevant normalized inventory for other tables. Record actual pagination:
  positive `pages_read`, exact `items_seen`, `exhausted: true`, `read_status: ok`
  only after all constituents succeeded. Every relevant record must be retained
- `query_digest` is the canonical digest of that exact query. `records_digest`
  binds the table's normalized records for the receipt repository.
  `scoped_admission.inventory_digest(snapshot, coordinator.TABLES)` binds the
  complete raw inventories, normalized record IDs and collector/source
  identities. The scope and input digests also bind all timestamps and results.
  These helpers calculate hashes; they **do not** collect observations or prove
  coverage. Never use the test-only `seal` helper for a real decision
- Receipts and individual review/check observations must be genuinely retrieved
  within 15 minutes; original performance times remain unchanged. Exactly one
  current trigger policy per repository is required. A second contradictory
  policy cannot be ignored in favor of a safe-looking first row

Malformed scoped input fails the whole scoped request closed; it never falls
back to legacy mutation admission. Existing snapshots without `scoped_source`
retain their prior behavior. All supported aliases and initialized imported
`watch.cmd_*` callables use the same evaluator. Decisions additionally bind
`source_scope_digest` and `source_inventory_digest`. Revalidate using the usual
exact-target `dispatch-guard`; any changed input/receipt/base/head invalidates
an old decision. This remains a recheck, not an atomic distributed lock.

### Module bundle, private inputs and reproduction

Use the repository's complete matching module bundle: `watch.py`,
`coordinator_cli.py`, `coordinator.py`, `scoped_admission.py`, `evidence_policy.py`.
A copied historical standalone `watch.py` does not gain these commands through
a documentation update. At module initialization, canonical `watch.py` wraps
supported/retired `cmd_*` names, and its CLI dispatch selects the same adapters.
Reading an old function body alone misses those wrappers. `review-sweep` remains
a supported read-only alias; retired liveness/transitions/admission routes stay
quarantined. This repair does not modify anyone's private copy or install sync.

Keep actual session, queue, ownership and authority observations in private local
inputs. Do not commit them or an actionable decision receipt. Published fixtures
must be synthetic or bounded already-public source evidence with explicit limits.
The fixtures here include a real immutable PR430 documentation packet replay
inside synthetic surrounding collection; that proves interoperability only.
Its current-rule stale-acknowledgment control still fails. It does not authorize
a current docs merge or claim any game/runtime/visual check.

Additional local commands (no GitHub Actions):

- `python3 -m unittest discover -s project-management/watchdog -p test_scoped_admission.py -v`
- Existing 37 coordinator methods, 53 evidence-policy methods, full legacy
  `test_rules.py`, and all five standalone independent probe scripts above
- See `fixtures/scoped-admission/README.md` for immutable real-source provenance,
  local-input replay and the recorded failing-original/positive controls
