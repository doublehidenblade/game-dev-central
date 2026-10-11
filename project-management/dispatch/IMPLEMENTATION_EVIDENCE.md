# Dispatch repair evidence — 2026-10-11

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
