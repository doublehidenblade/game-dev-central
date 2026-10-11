# Dispatch repair evidence — 2026-10-11

## Owner-directed additional correction — pending independent acceptance

Independent review [rejected head 8d070716](https://github.com/doublehidenblade/game-dev-central/pull/472#issuecomment-6112364709)
for two reproduced defects. Craig then requested finishing/merging/pulling this
existing PR; the parent delegated **one additional bounded correction** of those
findings. The [same canonical task](../tasks/ops-dispatch-handoff-20261011.json)
records that allocation and retains the original initial attempt and correction.
This allocation does not reset any gameplay or parked-resource history.

- `bind_write_scope` now requires every queue write path to fit both the pinned,
  hash-verified canonical task's `scope.write_allowlist` and a full-file/directory
  region in the exact guarded snapshot. It verifies canonical scope is unchanged
  at the admitted head. Row-only coverage cannot authorize an entire file. The
  reservation retains that binding and copies its paths; first-write recording
  rechecks the original reserved snapshot/decision and the same binding. Old
  unbound reservations fail closed; they are not rewritten or inferred safe.
- `record_session` can append authenticated discovery of the original launch
  after timeout, via `cycle` liveness or late `record` kind `session`. Discovery
  must bind the original attempt/decision, owner, executor, session and start
  window. It preserves unsuccessful status, consumed attempt and reservation,
  including retained stops. Only the exact discovered session's `ended`
  observation releases its reservation; live/unknown never does. Null-session
  `ended` is rejected; authenticated `not_started` remains limited to no known
  session. Recovery does not make a late first-write receipt successful.

**Verification:** [24 focused tests](evidence/additional-correction-tests.log) PASS;
retained coordinator/evidence/scoped suites PASS **37/53/62**; standalone retained
acceptance/final-guard/hold/operation/review checks PASS **14/15/2/128/32**; historical
`test_rules.py` reports ALL TESTS PASSED. [Machine results and source/log hashes](ADDITIONAL_CORRECTION_TEST_RESULTS.json)
bind the evidence to the corrected code and test files. Tests use synthetic
authenticated observations and real unmodified guards, with sockets disabled.

The [same negative regressions against rejected head 8d070716](evidence/reviewed-head-reproductions.log)
produce two scope assertion failures (reservation and receipt) and the late-live
session mismatch error. The [initial additional-correction red run](evidence/additional-correction-before.log)
is also retained. During the single correction allocation, a focused test first
failed because its artifact builder mutated its admission snapshot; the helper
now copies the synthetic Git world. No production guard or assertion was relaxed.

The actual CLI still returns eight exact candidate escalations with an unchanged
scratch journal. READY_QUEUE, ATTEMPTS, audit originals, core/scoped/evidence
guards, prior tests, board, workers, legacy state and parked resource task remain
unchanged by this correction. No saved automation was changed.

Before this source update, current main `424e441bc69a924bda8b992c77374e1cfb9823ad`
and the PR had no `.github` files; GitHub reported zero workflows and
`has_pages: false`. The main advance since the original PR base changes only
`project-management/watchdog/state/state.json`, outside this repair. The source
update stays on the same branch/PR and preserves the rejected head as an ancestor.

Parent integration: independently accept the **new exact PR head**, recheck current
push/merge triggers, then merge using an exact-head match. In the existing clean
`/workspace/game-dev-central` checkout (branch `work` at `b880784` when inspected),
fetch `origin main` and fast-forward with `git merge --ff-only origin/main`; stop
if local work/divergence appears. Do not reset, force-push or delete another lane.
Parent retains the accepted merge and first one-game-task rollout. Authenticated
fresh collection and one durable serialized authoritative journal remain required
for live adoption; review recording still requires complete fresh task/board/PR/
review observations. No author merge, launch, Actions or deployment occurred.

## Original candidate history — retained

Implemented [dispatch_loop.py](../watchdog/dispatch_loop.py) (331 lines) and
[15 deterministic tests](../watchdog/test_dispatch_loop.py). This is coordinator
mechanism code, **not gameplay implementation**. No game worker was launched.
The author used one implementation and one correction; independent acceptance
and the first one-game-task rollout remain with the parent.

| Verification | Result / retained evidence |
| --- | --- |
| Real scoped/evidence-guard selection, stop before selection, retained denials, ownership/queue gates | PASS in [dispatch tests](evidence/dispatch-tests.log) |
| Initial + one correction cap, unknown history, missing receipt rotation, uncertain/live session holds, no duplicates | PASS in the same 15-test suite |
| Actual session + changed content-addressed Git artifact; launch alone stays admitted; stale acceptance rejected | PASS; synthetic authenticated observations only, no live-launch claim |
| Two independent processes, one shared journal revision | One reservation/handoff, one stale-revision rejection |
| Core coordinator / evidence / scoped suites | 37 / 53 / 62 tests PASS |
| Retained acceptance isolation / final guards / hold invariance / operation needs / review scripts | 14 / 15 / 2 / 128 / 32 checks PASS; no prior assertions changed |
| Historical full `test_rules.py` script | ALL TESTS PASSED |
| Actual CLI against checked-in empty queue and scratch copy of journal | [ESCALATION_REQUIRED](EMPTY_QUEUE_RESULT.json), eight exact candidate blockers; journal unchanged |

[TEST_RESULTS.json](TEST_RESULTS.json) records exact commands, logs and hashes.
The initial focused run had 12 passes and one test-only missing-import error;
its [original log](evidence/initial-tests.log) is retained. The single correction
fixed that import and tightened launch/session evidence tests. Broad unittest
discovery encountered five legacy scripts' successful `sys.exit(False)` calls;
the [harness limitation](evidence/discovery-harness-limitation.log) is retained.
Each script then passed when run directly in its existing supported mode.

Canonical audit base: `19617c6afd961fdcc3142a00613b30a8d470787e`.
The independent parent comparison found 71 of 72 originals matching and only
`td197-stall-audit-evidence-20261011/provenance/r4-interfaces.json` missing.
Recovered the actual supplied garage-archive original in the audit-only commit preceding this repair:
12,042 bytes; Git blob `b49f2481584294ec61aff54200c16e3e732da6f0`;
SHA-256 `c2c28368b09e9e79ead0f84ff8ccd778eff1d67fb7507aca7eb2492191ecba82`.
All 72 audit-manifest entries now match their bytes/hashes. No missing companion
source was reconstructed; no private notes or broader evidence archive was copied.

Ownership/source inspection: no repository `.agents/skills` or AGENTS file was
present in central; `/workspace/.agents` was empty. Read canonical SYSTEM,
standing rules, worker-selection/durability policy, runbook, board and registry.
102 open central PRs were checked with changed paths; none reserved this mechanism
code. The protected board and other owners' lanes remain untouched. 243 game PRs
were enumerated for the bounded candidate checks. Current game source pin:
`b617aa71cc411b55191f0edec4310b515deb4569`.

C1 read/exclusive-write coupling is precisely filed in
[ops-scoped-read-dependency-20261011](../tasks/ops-scoped-read-dependency-20261011.json).
`scoped_admission.py` and its acceptance tests are unchanged. The separate parked
resource task remains parked, with unknown historical count preserved.

Before source push, GitHub reported central `has_pages: false`, zero Actions
workflows and no `.github` files at main. Source push and draft-PR creation therefore
have no observed repository Actions/Pages trigger. No workflow, deployment, merge,
external-agent contact, paid service, credential or security operation was performed.

Limits: this is a single authoritative shared-file journal, not a distributed
lease across clones. Collector/session assertions must come from authorized tools;
the module cannot authenticate a hidden session itself. Parent must designate and
persist the authoritative backend before live adoption. Saved automations are
unchanged. The queue stays empty until an actual approved candidate's scope,
history and liveness are verified; failed acceptance and deployment stops stay binding.
