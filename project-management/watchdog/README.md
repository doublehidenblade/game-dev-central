# Watchdog — coding-agent session monitor

Craig's watchdog keeps the coding sessions (Codex + Claude Code, Tokyo Drift 3D)
moving when open work stalls, without spamming him or the sessions. It merges
parked PRs itself (ship = merge to main ONLY; live publish happens only when
Craig asks), dispatches workers to open tasks, and reports a terse heartbeat.

**Everything here is cloud-synced by design** (Craig 2026-10-02, standing rule):
nothing about operating this watchdog may live only on one machine or inside
one agent platform. Scripts, docs, live state, and ledgers all live in this
repo. If you have this link, you can resume.

## Layout

```
project-management/watchdog/
  README.md            this file
  RUNBOOK.md           the ~15-minute loop (what to do, in order)
  STATE_MACHINE.md     session-state → action mapping (full spec)
  browser-brief.md     how to classify live session state (for whoever can
                       observe the Codex/Claude web sessions)
  watch.py             all deterministic logic as subcommands — the loop
                       obeys its verdicts, never re-derives them from prose
  test_rules.py        offline tests for the state machine
  state/               LIVE state, synced every loop (see below)
    state.json             session notes, worker registry, ledgers
    pending_actions.json   queue of browser/steer/dispatch actions
    worker-heartbeats/     worker liveness heartbeats
    liveness-briefs/       replacement briefs for dead workers
    last-check.json        last run watermark
    imagegen_replacement.json
  releases/
    pending.json         merged-but-NOT-live ledger (Craig's next push)
    baselines.json       last-live SHAs per game
    PUSH-PROCEDURE.md    how a live publish runs (only on Craig's ask)
project-management/rules/
  SYSTEM.md, WORKER_BRIEF.md, VALIDATOR_BRIEF.md, VISUAL_BRIEF_TEMPLATE.md
project-management/boards/tokyo-drift-3d.md   the board (source of truth)
```

## Resume from this link (fresh agent takeover)

1. Clone this repo. `cd` to the repo root.
2. You need GitHub API access with repo scope on `game-dev-central` and
   `doublehidenblade/tokyo-drift-3d` (read the board, task files, PRs; merge
   parked PRs; commit state). `watch.py` shells to a `gh api`-compatible CLI:
   set `WATCHDOG_GH_BIN` to yours (default: the Muse github skill path).
   Never commit credentials — they stay in your platform's secure storage.
3. `python3 project-management/watchdog/watch.py state-pull` — sync live
   state from main into your working copy.
4. Read `RUNBOOK.md` and run the loop about every 15 minutes:
   `state-pull` → loop → `state-push "watchdog: sync state"`.
5. **One scheduler at a time.** If a previous scheduler is still running,
   coordinate before starting yours — two writers will conflict on
   `state-push` (it aborts loudly rather than clobber, but you must resolve it).

## What the loop does (short version)

- STEP 0: scripted checks — `liveness` (dead-worker verdicts are code, not
  judgment), `conflicts`, `transitions`, `classification-health`, `board-check`.
- STEP 1: `decide` per session on the last recorded state; queue nudges,
  resumes, rebriefs, failovers, SHIP (merge parked PRs), INSPECT_MERGED.
- DISPATCH CHECK: scripted shortlist of board tasks → queue dispatches.
- STEP 3: always report — terse, grouped, traffic-light (jobs then workers).
- The full procedure, including the Muse-runtime browser handoff duties, is
  in RUNBOOK.md. The deterministic parts are all `watch.py` subcommands.

## Conventions that matter

- The board table is the source of truth for task status; workers touch only
  their own row, via PR.
- `done-pending-verdict` is terminal: implementation verified on main, ONLY
  Craig's phone verdict outstanding. Never re-dispatched, never reopened.
- Live publish happens ONLY on Craig's explicit ask. Merges to main continue
  automatically.
- Task naming: short plain-English defect names, never "td-012"/"PR #12".
- Standing rule: every new lesson/rule/workflow ships its deterministic
  checks as `watch.py` subcommands in the same change; prose-only rules are
  the exception. Tag lessons `[SCRIPTED: watch.py <command>]` or
  `[JUDGMENT-ONLY: why]`.
