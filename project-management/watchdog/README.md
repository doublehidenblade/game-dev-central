# Watchdog — scoped coordinator decisions

The supported coordinator route is a read-only evaluator over fresh, explicitly
accounted source observations. It identifies authorized next actions and scoped
blockers without writing live state, creating sessions, contacting agents or
triggering Actions/deployments.

Start with [RUNBOOK.md](RUNBOOK.md#supported-coordinator-route-2026-10-09).
The historical automatic loop and queue-delivery paths are quarantined. Do not
run `push_code.py` or use old browser handoff instructions as a bypass.

## Files

- `coordinator.py`: pure validation, task × operation × executor decisions, and
  exact-input receipt revalidation
- `coordinator_cli.py`: explicit JSON-input adapter; stdout only
- `watch.py`: supported aliases route through the shared evaluator before the
  legacy state-writing capture wrapper; retired admission callables fail closed
- `test_rules.py`: synthetic fixtures, no-side-effect integration tests, and
  existing pure state-machine/image regressions
- `fixtures/coordinator-snapshot.json`: dated synthetic shape example, never
  authorization or evidence of live capacity
- `state/` and `releases/`: existing ledgers, unchanged by this decision path
- `STATE_MACHINE.md` and `browser-brief.md`: historical behavior, superseded for
  admission/dispatch by the current runbook

## Commands

`python3 project-management/watchdog/watch.py coordinator-plan --snapshot <file>`

`python3 project-management/watchdog/watch.py idle-defect-check --snapshot <file>`

The plan returns `ACTION_REQUIRED`, `INPUT_REQUIRED`, or scope-bounded `IDLE`.
Permitted alternatives may coexist with warnings; warnings prevent global idle.
Each alternative is bound to its task, operation, executor, owner, full source
SHA, complete input digest and freshness. The runbook documents revalidation.

`python3 project-management/watchdog/test_rules.py` runs the full offline suite.
The coordinator-only standard-library suite is:
`python3 -m unittest discover -s project-management/watchdog -p test_rules.py -v`.

## Boundaries

Actual actions retain existing authorization, ownership and independent
acceptance requirements. Deploy only on Craig's explicit request, including
publication-branch pushes. The $50/month Actions ceiling is not permission or
verified spend. Inspect workflow/publication triggers before ordinary source
pushes and accepted merges. Shuto stays frozen; NEON stays paused/read-only.
Read the [deployment policy](releases/PUSH-PROCEDURE.md#deployment-authorization-and-actions-budget-craig-2026-10-08-1956-utc)
before any publication. This code installs no automatic collector or dispatcher.
