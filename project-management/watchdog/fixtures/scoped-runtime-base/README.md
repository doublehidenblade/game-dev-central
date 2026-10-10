# Scoped runtime composition: offline evidence

Implementation source: `c202855604e4315fa28b5116a8763cd85594bc5d`.
Original scoped source: `6d904f12b2b2aa87e257deb11bd98344c4c1a731`.
The implementation changes only scoped_admission.py, its test file, and scoped
RUNBOOK sections. Existing coordinator/evidence-policy code, inherited tests and
accepted PR449 evidence are unchanged. This directory is new evidence only.

All people, repositories, authority artifacts, collection receipts and snapshots
here are SYNTHETIC. They never authorize a real task, establish live ownership,
or claim gameplay/visual evidence. The author does not accept its own repair.
Independent criterion acceptance is required separately.

## Exact source execution

`execution/C1-...` through `C6-...` follow the pre-registered criterion/check
mapping. Every execution JSON contains the exact command, source head, real UTC
execution time, actor, exit code and complete output. Shared commands are run
once against the exact source and referenced by each applicable criterion.
All 16 registered source paths were checked against the published tree before
the commands ran. No executable fixture/helper file was added; every new test
builder and oracle is inline in `test_scoped_admission.py`.

Results: 62 scoped methods (39 retained + 23 new), 37 coordinator methods,
53 unchanged evidence-policy methods, the legacy suite, and 191 standalone
retained controls. These passing executions establish test results, not C7.

## Original blocker and corrected route

`historical-v1.json` and `historical-v2.json` replay the same synthetic malformed
foreign historical board with valid exact Git objects. The v1 conversion uses
the correct current-rule ancestry chains; it is not broken by an invalid base.
`original-corrected.json` records actual supported coordinator-plan adapter runs:

1. Original code + v1: INPUT_REQUIRED, `unsupported board row identity`
2. Corrected code + v1: identical strict result
3. Corrected code + v2: one ACTION_REQUIRED receipt, global coverage unknown

The v2 positive contains complete independent exact-source context judgments.
The unit suite separately removes/corrupts those judgments and tests no-ID
global/owner/dependency effects, ambiguous/encoded identities, duplicate or
unselected blockers, actual candidate context changes, real whole-file conflicts,
file modes/types/deletion/invalid UTF-8 and missing proof objects. They stay blocked.
The distinct-rule/runtime-head fixture alone demonstrates representation and
interoperability; it is not claimed to reproduce an original v1 failure.

To reproduce the recorded adapter commands, copy the two snapshot JSON files to
`/tmp/scoped-runtime-base-replay-20261010/`, then run each recorded command from
the repository checkout named by its source_head. The command explicitly fixes
synthetic fixture time to 2026-10-09T14:00:00Z; running these old snapshots against
wall-clock time correctly expires them. Use the complete matching five-module
bundle described in RUNBOOK. Commands read snapshots and print results only;
there is no network collector, queue mutation, dispatch, Actions or deployment.

The single reviewed correction binds current owner/reservation/stop applicability
closure and prevents contradictory outer decision labels from hiding structurally
matching BLOCK records. Independent unchanged probes and new inline regressions
cover both same-head identity transfer and composition/context envelope conflicts.
