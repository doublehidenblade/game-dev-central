# Agent session watchdog — state machine

## ARCHITECTURE (2026-09-24 — structural fix after seven consecutive 1200s cron timeouts)
The cron worker NEVER touches the browser: the browser-task dispatch blocked the worker, so no instruction-based cutoff could ever fire. Split design:
- **Cron worker** (`agent-session-watch`): pure shell + GitHub API. Runs `watch.py decide` per session, ships parked PRs itself, spawns Muse subagents for failover/all-blocked, queues browser-needing actions (nudge/resume/steer/screenshots) into `hidden_files/pending_actions.json`, and always emits the STEP 3 heartbeat. Never spawns browser tasks.
- **Main agent** (on each watchdog handoff turn): executes pending_actions.json entries via ACTION MODE browser tasks, dispatches ONE fresh "READ-ONLY classification run" browser task per cycle if none is in flight, and records arriving classification reports via `watch.py check-done` + `watch.py classify`. See the cron body's MAIN-AGENT HANDOFF DUTIES — that section is authoritative.

Watches Craig's coding sessions and nudges them only when open work has
stalled. Read-only by default; writes are limited to a single `continue` nudge,
a session resume, a steer message typed into the session's own composer, or —
as a last resort only — the cron merging a finished PR the worker failed to
ship (Craig 2026-09-23 ~14:45 CDT). Whoever gets to a parked PR first ships it —
no steering the worker to ship, no 45-minute window: the run ships it itself
once the build is clean — CI is after-the-fact verification per Craig 2026-09-23 ~15:03 CDT
(deploy is never gated on CI green; his own playtest is part of testing).
and deploys its OWN PR once the build is clean, then moves on — never the main agent,
never the watchdog — and the worker must NOT wait for the cron.

## Products

| # | Product | URL | Workspace | Repo |
|---|---------|-----|-----------|------|
| 1 | Codex | https://chatgpt.com/codex/cloud | `neon-drift` | doublehidenblade/neon-drift |
| 2 | Claude Code | https://claude.ai/code | `Default tokyo-drift-3d` | doublehidenblade/tokyo-drift-3d |

## Pipeline

```
every 15 min
  └─ watch.py gate                      (GitHub API, cheap)
       ├─ QUIET  → stop, say nothing
       └─ NEEDS_BROWSER_CHECK <repos>
            └─ browser task (PART 1+2 of browser-brief.md, READ-ONLY)
                 └─ per session: WORKING | STALLED | DEAD | OUT_OF_TOKENS | LOGIN_BLOCKED | FINISHED
                      └─ watch.py classify  → ACTION
                           ├─ NOTHING        → stop, heartbeat only
                           ├─ NUDGE          → browser task (ACTION MODE nudge-*) → watch.py nudge → notify Craig
                           ├─ REBRIEF         → browser task (ACTION MODE steer-*) re-briefs session to next open task → watch.py rebrief → notify Craig (Craig 2026-09-23: blocked workers move on; blocked task stays open)
                           ├─ RESUME         → browser task (ACTION MODE resume-*) → watch.py resume → notify Craig
                           ├─ SHIP          → the RUN ships the parked PR itself via the github skill once the build is clean (Craig 2026-09-23 ~14:45 CDT: whoever gets to a parked PR first ships it; never steer the worker to ship). CI is after-the-fact verification (Craig 2026-09-23 ~15:03 CDT): CI red/pending does NOT block the merge — in the SAME run, pull the failed steps/annotations, distinguish a real build failure (steer the worker with the exact error now) from infra noise (file as rework per one-bug-one-task), and resolve branch conflicts in the same run then merge. Craig 2026-09-23: see the issue, address it right away — never defer to 're-check next run'.
                           ├─ INSPECT_MERGED → run inspects the merged diff and reports to Craig (screenshots, what changed, remaining work); files new tasks or re-opens gaps; nudges the worker if post-merge work stalled → watch.py inspected
                           └─ REPORT_LOGIN   → watch.py loginfail → notify Craig (throttled 6h)
```

## Gate (GitHub side)

Per repo, from the GitHub API:
- **open work** = open PRs > 0 OR open issues > 0
- **last activity** = max(open PR `updated_at`, open issue `updated_at`,
  newest push event on any branch, newest `main` commit)
- **no progress** = last activity ≥ 50 minutes ago (`IDLE_MINUTES`)

`NEEDS_BROWSER_CHECK` only when: open work AND no progress for ≥ 50 min AND no
browser check in the last 30 min (`BROWSER_COOLDOWN_MIN`). Otherwise `QUIET`.

## Session states (browser evidence → classification)

### Codex (`/codex/cloud/tasks/task_e_<uuid>`)

| State | Evidence |
|-------|----------|
| WORKING | "Working on your task" banner + "Thinking" + loading progressbar + "Cancel task" + live terminal log |
| FINISHED | Task shows a completed/finished run with a completed diff and an idle composer — done, not stalled. A task whose final status literally says "Merged" is FINISHED, not dead: the worker shipped its own PR, and the run inspects the diff and reports to Craig. |
| STALLED | Task unfinished (no final status) but no banner, no log movement, idle composer — genuinely stuck, not merely finished |
| DEAD | Final status "Failed after Ns" / "Cancelled" + "Retry" button |
| OUT_OF_TOKENS | "Usage nearing limit" banner or usage-limit messaging |
| LOGIN_BLOCKED | Login page / re-auth / CAPTCHA — stop, do not attempt |

### Claude Code (`/code/session_<id>`)

| State | Evidence |
|-------|----------|
| WORKING | "Running" in Recents + "Currently streaming message" + live tool calls + "Stop" button |
| STALLED | Session exists, nothing streaming, last message complete, Prompt idle — open work pending, agent has NOT signaled done |
| FINISHED | Session idle, last message complete, agent signaled the task done (summary shown) — done, not stalled |
| DEAD | Session ended/errored, cannot continue in it |
| OUT_OF_TOKENS | ~100% of 5-hour limit or context window exhausted |
| LOGIN_BLOCKED | Login page / re-auth / CAPTCHA (incl. unreadable hCaptcha) — stop, do not attempt |

## Actions (`watch.py classify` enforces)

| Classification | Action | Guard |
|----------------|--------|-------|
| WORKING | NOTHING | hard: never nudge a working session |
| OUT_OF_TOKENS | FAILOVER | hard: hand priority work to sibling session or Muse subagent (Craig 2026-09-23); once per out-of-tokens episode (`out_of_tokens_since`), 180m cooldown backstops back-to-back episodes |
| STALLED | NUDGE — send `continue` once per stall episode, then REBRIEF (Craig 2026-09-23) | NUDGE: at most 1 per 45 min per session (`NUDGE_COOLDOWN_MIN`); action task re-verifies stalled-ness first. REBRIEF: if still STALLED after the episode's nudge, steer the session to the next open priority task — the blocked task stays open per one-bug-one-task. One re-brief per stall episode; after that, wait for a fresh classification. |
| DEAD | RESUME — start/resume session in workspace, send `continue` | action task checks task list / Recents first; never create a duplicate live session |
| LOGIN_BLOCKED | REPORT_LOGIN | notify Craig, throttled to once per 6 h |
| FINISHED (PR unmerged) | SHIP — the RUN ships the parked PR itself via the github skill once the build is clean (Craig 2026-09-23 ~14:45 CDT: whoever gets to it first ships it; do NOT steer the worker to ship). CI is after-the-fact (Craig 2026-09-23 ~15:03 CDT): CI red/pending does NOT block the merge — in the SAME run, pull the failed steps/annotations, distinguish a real build failure (steer the worker with the exact error now) from infra noise (file as rework per one-bug-one-task), and resolve branch conflicts in the same run then merge. Craig 2026-09-23: see the issue, address it right away — never defer to 're-check next run'. | fires once per finished episode (pr_merged ledgered by `watch.py merged <session> cron`) |
| FINISHED (PR already merged) | INSPECT_MERGED — the run inspects the merged diff and reports to Craig (inspected screenshots, what changed, remaining work; who shipped it: `merged_by` = worker or cron); files new tasks or re-opens gaps if the merge left problems; nudges the worker if post-merge work stalled | once per finished episode (inspected_ts ledgered); then NOTHING |
| FINISHED (no PR — pushed straight to main) | NOTHING — terminal: there is no parked PR to ship, so SHIP must not fire. `classify ... --no-pr` records `finished_no_pr` for the episode (reset on each new FINISHED episode). | nothing to ledger; the episode is closed |

Exception (Craig-authorized 2026-09-22, corrected same day): the
tokyo-drift-3d workspace legitimately runs THREE live Claude sessions — main-dev
(branch td016-texture-request-and-td018-occlusion), Shuto Expressway C1 loop map
(Craig-ordered; idle awaiting his 9 design answers), and texture-imagegen (title
contains "texture imagegen", owns ONLY the 6 PNGs under
godot/assets/pbr/stylized/). Never "fix" this set; classify all three each run.
Any fourth live session is still an unauthorized duplicate.

## Imagegen session replacement (standing instruction, Craig 2026-09-22)

Craig verified the Gemini key works end-to-end in the Claude texture-imagegen
session (proxy injects the real key; GEMINI_API_KEY placeholder is set in the
env). Standing order:

- WHEN the Claude texture-imagegen session is done (finished/ended, not merely
  stalled) AND `hidden_files/imagegen_replacement.json` shows replacements not
  yet started → the main agent starts fresh sessions for texture/imagegen work:
  1. New Claude session in workspace `Default tokyo-drift-3d` (GEMINI_API_KEY
     placeholder env var + proxy credential already configured), GH repo
     `doublehidenblade/tokyo-drift-3d` attached.
  2. New Codex task in env `neon-drift` (GEMINI_API_KEY already in env),
     repo `doublehidenblade/neon-drift`.
  3. New Codex task in env `tokyo-drift-3d` (GEMINI_API_KEY already in env),
     repo `doublehidenblade/tokyo-drift-3d` (shuto express work).
- New sessions are started via browser tasks on claude.ai / chatgpt.com/codex,
  each with a proper task brief (texture/imagegen scope). Per the imagegen flow,
  briefs tell sessions to consume Muse-generated committed mocks; in-session
  Gemini only if a mock is unusable. They are
  Craig-ordered, so they are NOT unauthorized duplicates — but still check
  first: do not start a replacement in an env where a live session is already
  doing texture/imagegen work.
- After starting each, mark it in `hidden_files/imagegen_replacement.json`
  (`claude`, `codex_neon`, `codex_shuto`) so the 15-min watch never double-starts.
- The watch itself does not start sessions; it surfaces the texture-imagegen
  session's finished state in its handoff so the main agent can act.
  Flag: `IMAGEGEN_REPLACEMENT_DUE`.

## Notification policy

Craig hears about the watchdog only when it *did* something or is blocked:
- `continue` nudge sent → short message naming the session
- session resumed → short message naming the session
- PR shipped by the run (SHIP) → short message naming the session and the PR ("shipped parked PR #N")
- merged PR inspected → the full post-merge report (inspected screenshots, what changed, remaining work, any new tasks filed)
- login failure → "needs a manual login", ≤ 1 per 6 h

Everything else (QUIET gate, WORKING checks, cooldown-suppressed nudges) is silent.
The GitHub watch's no-change silence is preserved: this cron never reports "all quiet".

## Files

- `watch.py` — gate, decisions, ledgers
- `browser-brief.md` — verbatim browser-task instructions (classification + action mode)
- `hidden_files/state.json` — per-repo activity, per-session classification/nudge/login ledgers
- `hidden_files/last-check.json` — latest gate detail
- `hidden_files/imagegen_replacement.json` — which Craig-ordered imagegen replacement sessions have been started (never double-start)
- `test_rules.py` — offline executable spec of the evidence→state and state→action rules
