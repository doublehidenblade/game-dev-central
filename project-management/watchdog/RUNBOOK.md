# Watchdog runbook — the ~15-minute loop

Run from the repo root (`game-dev-central`). All paths below are repo-relative
unless stated otherwise. This is the portable version of the loop; the
deterministic decisions are all `watch.py` subcommands — obey their verdicts,
never re-derive them from prose.

## Loop wrapper (every run)

1. `python3 project-management/watchdog/watch.py state-pull` — sync live
   state from main into your working copy. (First-ever run: the files may not
   exist in the repo yet; your local state seeds them.)
2. Run the loop below.
3. `python3 project-management/watchdog/watch.py state-push "watchdog: sync state"`
   — commit changed state/ledgers to main. Aborts loudly on a moved ref
   (another writer); never force-push it.

**One scheduler at a time.** Two concurrent loops will conflict on
`state-push`. If you are taking over from another scheduler, make sure it is
stopped first.

## Platform notes

- The MAIN-AGENT HANDOFF DUTIES at the bottom were written for Muse (browser
  tasks, subagents, the 15-min cron). On another platform, implement the
  equivalent: something must (a) observe the Codex/Claude web sessions and
  report classifications, and (b) deliver queued nudges/steers/dispatches.
  The queue schema (`state/pending_actions.json`) and ledger commands are
  platform-independent — only the delivery mechanism differs.
- You need GitHub API access (repo scope). Set `WATCHDOG_GH_BIN` to a
  `gh api`-compatible CLI if you are not on Muse.

---
Every ~15 minutes, run Craig's coding-agent watchdog for Codex (Tokyo Drift 3D) and Claude Code (Tokyo Drift). Monitoring with conditional recovery. The run never modifies game code. It DOES merge parked PRs itself (ship = merge to main ONLY — live publish happens only when Craig asks, 2026-09-27): a finished session with an unmerged PR gets merged by the run once its build is clean — CI is after-the-fact verification, NOT a deploy gate (whoever gets to a parked PR first ships it — no steering the worker to ship). Never nudge a working session. Never create a duplicate live session. Full state machine: project-management/watchdog/STATE_MACHINE.md.

NEON DRIFT FREEZE (Craig 2026-09-29 — SUPERSEDES all NEON instructions below): neon-drift repo is ARCHIVED (read-only); pseudo-3D paused indefinitely. All effort is Tokyo Drift 3D. Therefore: SKIP codex:neon-drift entirely (no decide/classify/dispatch/heartbeat line); NEVER dispatch p3d-* tasks or todoNNN READMEs; NEVER open PRs against doublehidenblade/neon-drift (writes will fail); IGNORE the NEON board in DISPATCH CHECK and JOBS; NEON browser-brief PART 1 env is dead — fresh classification covers Codex Tokyo + Claude Code only. Any "NEON DRIFT" mention below is struck through. Frozen demo stays live at https://doublehidenblade.github.io/neon-drift-web/ (do not touch).

ARCHITECTURE (structural fix 2026-09-24): the browser-task dispatch BLOCKS the worker, so no timer, budget, or "do not wait" prose can ever fire. Therefore THIS JOB NEVER SPAWNS, STEERS, PEEKS, OR CLOSES BROWSER TASKS — not for classification, not for nudges, not for anything. If you are the worker reading this: do not touch the browser, ever. All browser work happens in the MAIN AGENT's turn on the handoff (see MAIN-AGENT HANDOFF DUTIES at the bottom — not for you). This run is pure shell + github API + heartbeat.

MAX-PARALLELIZATION (Craig 2026-09-23, standing rule): parallelize ALL open tasks as long as conflict risk is minimal. Multiple workers MAY be active on the same repo/game at once, each on a different task — no one-game-one-agent assumption, no hard cap. Agents self-resolve merge conflicts; any worker resuming a stale session syncs master first. Never two workers on the same task file.

CONTEXT MIGRATION (Craig 2026-09-23): when a stalled/dead session is replaced by ANY route, the replacement must NOT redo finished work. Before spawning it: (1) read the old session's last messages/task activity for what it completed and where it stopped; (2) check its branch via the github skill for commits not yet on main. Fold both into the replacement's brief as "already done — do not redo; continue from X". If the old session is expected back soon (token refill, transient stall with known return) AND migration is expensive: do NOT replace it — set a runonce cron to re-check/wake it at the expected return time, and record the expectation in the session note.

BLOCKED-WORK DISCIPLINE (Craig 2026-09-23): when a worker's last message says it is blocked, READ that message first — never nudge blind. (1) Blocked on something only Craig can unblock (his API key, login, external quota/account): `watch.py block <session> <blocker-key> <reason>`, PARK it, and surface to Craig exactly once per blocker — `watch.py blocker-surfaced <session> <blocker-key>` prints SURFACE (first time) or SUPPRESSED; surface only on SURFACE. (2) Blocker is resolvable (missing env var, wrong branch, CI error with known fix): queue a steer via `watch.py queue-action` with the exact resolution. (3) Same block repeated with no new information: reconcile — real block or loop? Park it or convince it to resume with a concrete next step. Never nudge just to watch it no-op again.

STEP 0 — DETERMINISTIC CHECKS (Craig 2026-10-02: every check is a watch.py subcommand — obey verdicts, never re-derive them). Run in order with `python3 project-management/watchdog/watch.py`:
1. `liveness` — BEFORE the decide pass. One verdict per registered worker: ALIVE / QUIET(n) / GRACE / STALE / DROPPED / DEAD — authoritative, never override with your own reading of the same data. Report every verdict line in the WORKERS section. On DEAD the script has already queued a `dispatch-subagent` entry for the main agent to deliver; DEAD printed but no such entry in pending_actions.json → say so loudly. Registration is the dispatch proof: dispatchers run `register-worker <task> <subagent|codex|claude> <session|-> <repo> <task-file>`; run `deregister-worker <task> <reason>` when its work is merged or handed off. Unregistered workers are invisible. ([JUDGMENT-ONLY] override, 2026-10-02: suppress a script-queued replacement ONLY on direct, fresher aliveness evidence the script can't see — then drop the queued entry, record why in state.json notes, and repair the signal. Never suppress on a re-reading of the script's own signals.)
2. `conflicts` — duplicate task ownership. Exit 3 = CONFLICT: stop, surface, never dispatch over it.
3. `transitions` — the SYSTEM.md board-watcher as code. FLIP lines: `in_review` → dispatch validator; `validated`/`rejected`/`blocked` → notify Craig.
4. `classification-health` — prints STALE-RUNS=n for the DEGRADED WATCHDOG ALARM (main agent ANDs it with the in-flight browser check).
5. `board-check tokyo-drift-3d` — board hygiene (>6-cell rows, unparseable rows, active workers with empty Owner).

STANDING SCRIPTIFICATION RULE (Craig 2026-10-02): every future 'remember to' / lesson / rule / workflow addition must ship its deterministic checks as watch.py subcommands in the same change; prose-only rules are the exception, not the default. Tag new lessons [SCRIPTED: watch.py <command>] or [JUDGMENT-ONLY: why].

STEP 1 — Decide and act on the LAST RECORDED state first (fast; no browser needed). For each session (codex:tokyo-drift-3d, claude-code:tokyo-drift-3d), run `watch.py decide <session>` — prints ACTION, never touches timestamps. Nudge/failover guards enforced in code. Queue via `watch.py queue-action '<json>'` (dedupes on type+session); never dispatch anything yourself.
- NOTHING → do nothing.
- NUDGE → if the last message reports a known blocker, `watch.py blocker-surfaced <session> <blocker-key>` first: SUPPRESSED → apply BLOCKED-WORK DISCIPLINE, do NOT nudge. Else queue `{"type":"nudge-codex"|"nudge-claude","session":<session>,"target_task_url":<from decide>}`.
- RESUME → queue `{"type":"resume-codex"|"resume-claude","session":<session>,"target_workspace":<from decide>}`.
- REBRIEF → queue `{"type":"steer-codex"|"steer-claude","session":<session>,"message":<rebried steer text>}`.
- FAILOVER → read FAILOVER_TARGET + BRIEF from decide. Sibling target: `watch.py sibling-check <session>` first — STEER-BLOCKED (sibling WORKING) → route to a Muse subagent instead; STEER-OK → queue `{"type":"steer-codex"|"steer-claude","session":<sibling>,"message":<BRIEF>,"failover":true}`, then `watch.py failover <session>` (if the steer later can't be sent, `watch.py failover-undo <session>`). MUSE_SUBAGENT target (or sibling unavailable): spawn a Muse subagent per SYSTEM.md — brief links SYSTEM.md, names repo + task file, grants github skill, states transcript-is-noise / task-file+evidence-are-truth / never merge-publish; apply CONTEXT MIGRATION; then `watch.py failover <session>`. Notify Craig ONLY if the failover itself could not be executed.
- REPORT_LOGIN → `watch.py loginfail <session>`.
- SHIP → ship the parked PR yourself via the github skill (`bin/gh api`), no browser. (1) `watch.py ship-verify <session>` — NEVER merge on the SHIP label alone: merge only SHIP-VERIFIED; SHIP-BLOCKED (denylist, e.g. #253) never merges; SHIP-STALE = nothing parked. (2) `watch.py ci-report <owner>/<repo> <head-sha>` — CI is after-the-fact verification, NOT a deploy gate; merge once the build is clean. Failed/pending checks → pull failed steps + annotations (`bin/gh api GET /repos/<o>/<r>/check-runs/<id>/annotations`): real build failure → steer with the exact error NOW; infra noise (artifact-quota failures, all substantive steps green) → file rework per one-bug-one-task, merge anyway; conflicted branch → rebase via git-database API (blobs → tree on current main → commit → update branch ref), then merge. (3) Draft PR → mark ready via GraphQL: POST https://api.github.com/graphql {"query":"mutation { markPullRequestReadyForReview(input: {pullRequestId: \"<node_id>\"}) { pullRequest { isDraft } } }"} (REST ready_for_review 404s; PATCH {"draft":false} does NOT undraft). (4) Squash-merge: `bin/gh api PUT /repos/<o>/<r>/pulls/<N>/merge '{"merge_method":"squash"}'` (PUT, not POST). (5) No publish workflows, no live-site check — live only on Craig's ask. `watch.py record-pending <game> <task-id> <pr> <merge-sha> "<summary>"` (dedupes on pr). (6) `watch.py merged <session> cron`. Auth/permission error → do NOT retry-loop; surface failure + PR number in the final message, move on.
- INSPECT_MERGED → `watch.py status` for merged_by; read the merged diff (PR from INSPECT_NOTE); `watch.py evidence-audit <task>`. Missing/invalid pairs → `watch.py session-alive <session>`: ALIVE → steer the worker (`{"type":"steer-codex"|"steer-claude","session":<session>,"message":"For task <id>, commit before/after pairs for EVERY visual criterion: <task-id>-<criterion-N>-before.png / -after.png, same camera angle, under the task's QA folder, and record the paths per criterion in the task file's evidence list. Missing valid pairs: <list>. Do not set in_review until every visual criterion has one."}`); GONE → spawn a Muse subagent per SYSTEM.md to SCAVENGE evidence only (never merges/publishes). Queue `{"type":"screenshots","session":<session>,"pr":<N>}` for inspected screenshots. Report to Craig: what changed, who shipped it (worker or cron — say plainly), remaining work, evidence recovery route, screenshots note. Then: gaps/regressions → new task(s) per one-bug-one-task; stalled post-merge work → queue a steer. `watch.py inspected <session>` (one report per shipped PR).

DISPATCH CHECK (Craig 2026-09-24 — the watchdog dispatches, not just watches; verdict/CI never block implementation). After the decide pass, run the scripted shortlist — never grep the board by hand: `watch.py dispatch-eligible`, `watch.py dispatch-candidates` (applies the SKIP-DONE RULE, drops owned tasks and the dispatch denylist), `watch.py owners`. Priority: Tokyo by board order (NEON is archived). For a salvage-carrying task, `watch.py salvage <owner>/<repo> <task>` and fold the output into the brief as done-work-not-to-redo. Then queue via `watch.py queue-action '{"type":"dispatch-codex"|"dispatch-claude","session":<session>,"env":"tokyo-drift-3d","task":<task-id>,"task_file":<path>,"brief":<WORKER_BRIEF.md with [TASK_ID]/[TASK_FILE_PATH] filled plus context/salvage>}'` (dedupes; STEP 0 `conflicts` enforces it). Record the assignment in the session note.

ALL-BLOCKED ESCALATION (Craig 2026-09-23, standing rule): if `watch.py all-blocked` prints ALL-BLOCKED True — every live session STALLED/DEAD/OUT_OF_TOKENS/LOGIN_BLOCKED, none WORKING, no viable sibling — do NOT grind through the nudge/cooldown ladder. Apply CONTEXT MIGRATION, then spawn Muse subagents immediately on the highest-priority open briefs per project-management/rules/SYSTEM.md — one subagent per task, never two on the same task file (brief links SYSTEM.md, names repo + task file, grants github skill, states transcript-is-noise / task-file+evidence-are-truth / never merge-publish). Record them in the session notes. The subagent is the last resort; it does not merge or publish.

STEP 2 — REMOVED 2026-09-24 (structural fix): fresh browser classification is dispatched by the MAIN AGENT on the handoff turn (see MAIN-AGENT HANDOFF DUTIES), never by this job. There is no STEP 2 here.

BUDGET CHECK (Craig 2026-09-27 — ask BEFORE the Actions budget fills, never after it blocks): on Muse, once per run, run `python3 ~/workspace/github-billing/check_budget.py`. On other platforms, skip (no billing access). Level OK → say nothing about billing. ALERT_WARN or ALERT_HIT → put the budget ask FIRST in the final message: "GitHub Actions at $X of your $Y budget (Z%) — raise it? (Settings → Billing → Budgets and alerts)". On ALERT_HIT add: "Paid Actions usage is stopped until you raise it." Never change the budget yourself. The script dedupes alerts per month.

STEP 3 — ALWAYS report, every run (Craig 2026-09-23: he wants a heartbeat, never silence). Terse, GROUPED, TRAFFIC-LIGHT: two sections, jobs then workers. Omit jobs with no change unless the list would be empty. `watch.py pending-report`: merged-but-not-live items get exactly one REPORT line, then only the COUNT line — never repeated open/assigned noise. After reporting an item, `watch.py pending-reported <pr>` to stamp it.

TASK NAMING (Craig 2026-09-25): name every job by a short plain-English defect name (from the task file's defect summary when none is established), reused across runs. PR numbers stay only as the PR link's label, never as the job headline.

INSPECTION OUTCOMES (Craig 2026-09-25 — CLOSED SET, ENFORCED): every inspected task ends in EXACTLY ONE of these five states — never "open and idle", never "waiting for next cycle", never "queued/unassigned" without a reason. If a task cannot be placed, the run is broken: fire the degraded-watchdog alarm loudly.
1. closed — defect fixed and verified (screenshot evidence inspected for visual tasks), OR superseded/duplicated with the reason on the board.
2. open and assigned — a NAMED worker owns it now: a cloud session, a dispatched task, a live subagent, or the run's SHIP path (parked PR = assigned to SHIP; merged-not-live = in pending.json, published only on Craig's ask).
3. open but no available worker — genuinely no capacity: every session blocked/dead/out-of-tokens/login-blocked AND no viable subagent route (ALL-BLOCKED ESCALATION must have fired first). Name what's missing and why. Token-refill wait is NOT outcome 3 — default is handoff to another worker (outcome 2); refill-wait with wake timer is the narrow exception (refill soon AND context too large to migrate, both in the session note).
4. blocked on human — ONLY Craig can unblock (login, API key, purchase approval, physical action). Name the exact action. Park it; surface once per blocker.
5. blocked on external — third-party/service outage nobody here can fix. Park with reason + re-check timer; re-probe, never nudge workers over it.

FOLD-IN RULES (edge cases that map into the five): "stalled, nudge queued" / "steer queued" → 2 (the queued action IS the assignment). "finished, PR parked" → 2 (owned by the SHIP action). "merged, not yet live" → 2. "waiting on token refill" → 2 by default (outcome 3 with wake timer only as the narrow exception above). "dead, no recovery route" → 3 (ALL-BLOCKED ESCALATION must have fired first). "superseded by a kill order / duplicate" → 1 (closed, reason on the board).

JOBS — open tasks with activity or needing eyes this run. Board table in doublehidenblade/game-dev-central (project-management/boards/tokyo-drift-3d.md — NEON archived) is the SOURCE OF TRUTH; fetch via the github skill. Cross-check session notes for owners. Every JOBS line carries its outcome number (outcome 1 never appears).
- 🟢 2 — open and assigned — task, worker, and PR if any
- 🟡 3 — open but no available worker — missing capacity and why handoff wasn't possible
- 🔴 4 — blocked on human — the exact action Craig must take
- 🔴 5 — blocked on external — the dependency and re-check plan

WORKERS — one line per known agent: own subagents plus the cloud sessions (codex:tokyo-drift-3d, claude-code:tokyo-drift-3d).
- 🟢 working — what task it's on
- 🟡 idle / stalled — available, or queued for nudge this run. IDLE-WITH-ASSIGNABLE-WORK IS A RUN DEFECT: idle only when every open task is outcome 3/4/5. Verify with `watch.py idle-defect-check` (DEFECT <session> <task> exits 3 when an idle session has assignable work; else OK).
- 🔴 out of tokens / dead / login-blocked — plus the recovery

INLINE LINKS (Craig 2026-09-24): every JOBS line links its task file and PR; every WORKERS line links its live session. Generate URLs with `watch.py links <session>` and paste them verbatim — never guess a URL; link plainly if none is on record.

VERDICT/CI FRAMING (Craig 2026-09-24): Craig's phone verdict is QA closure only — it NEVER blocks implementation, and CI is after-the-fact verification, never a deploy gate. Never report a job as "awaiting Craig's verdict" or "waiting on verification/CI": verdict-only work does not appear in JOBS; remaining implementation shows its inspection outcome (2/3/4/5). NOTIFY-worthy events first (nudge queued, resume queued, parked PR shipped, merged PR inspected and reported, login failure, subagent spawned, merge conflict self-resolved, dispatch queued), then the two grouped sections. This is the run's final message and it always goes out.

DEGRADED WATCHDOG ALARM: STATE_AGE_MIN > ~45 min means no fresh classification yet — say so plainly (e.g. "classifications 90 min old, fresh check in flight"), not as failure. If classifications stay stale for 3+ consecutive runs AND no classification task is in flight, say so loudly: the main-agent dispatch path may be broken. A watchdog that can see but not act must say so loudly, never finish silently.

MERGE CONFLICTS (Craig 2026-10-02, standing rule): merge conflicts are the agent's to resolve — rebase the worker's branch onto current main via the github skill git-database API (create blobs, build tree on main, commit, update the branch ref), resolve conflicts, and push. Never ask Craig; he never merges or pushes himself. Force-push only to the worker's own feature branch, never main.

NEVER-SHIP DENYLIST (Craig 2026-10-01): `NEVER_SHIP_PRS` lives in watch.py — `ship-verify` prints SHIP-BLOCKED for denylisted PRs (e.g. PR #253, the td-138 round-3 preservation branch) even when open. The cron merges only SHIP-VERIFIED PRs.

MAIN-AGENT HANDOFF DUTIES (not for the cron worker — for the main agent turn that receives this run's handoff):
1. Deliver or skip the heartbeat per the delivery rules (Craig wants it every run).
2. Read project-management/watchdog/state/pending_actions.json. For each entry, delegate ONE browser task with browser-brief.md ACTION MODE for its type, passing the entry's fields (nudge/resume/steer-codex/claude: target_task_url / target_workspace / message):
   - dispatch-codex: new Codex cloud task in the entry's env, title "<task> — <short defect>", brief VERBATIM in the composer.
   - dispatch-claude: open the session URL, brief VERBATIM in the Prompt box; re-verify idle first (if WORKING, pop with NO_ACTION_WORKING + record why).
   - screenshots: capture the PR's changed-area screenshots from the live -web site, eyeball before reporting.
   - dispatch-subagent: spawn ONE Muse subagent, brief VERBATIM as first message (do not edit); then `watch.py register-worker <task> subagent - <repo> <task_file>`; pop the entry.
   On ACTION_DONE / STEER_DONE: matching ledger command (nudge|resume|rebrief|failover <session>) + pop. On NO_ACTION_WORKING: `watch.py entry-attempt <type> <session>` (3 attempts → dropped + SURFACE → tell Craig). Before starting: `watch.py entry-start <type> <session>` (refuses concurrent same-session entries). `watch.py pending-validate` anytime.
3. Fresh classification: check browser.list_tasks for an in-flight "READ-ONLY classification run" task. If none, spawn ONE browser task with instruction = "READ-ONLY classification run. ACTION MODE is NOT enabled." + full contents of project-management/watchdog/browser-brief.md PART 1 and PART 2 (skip neon-drift env — archived) + this TIME LIMIT block verbatim: "TIME LIMIT: you have 5 minutes total from the moment you start. Never spend more than ~90 seconds on any single page load — if a page is blank or still loading after that, reload once; if it still does not render, mark that environment/session PENDING and move on. At the 5-minute mark, STOP and report immediately: PARTIAL lines for every environment/session you classified, PENDING for the rest. A partial report on time beats a complete report late." The task must not type into any composer, must not attempt or wait on login pages or CAPTCHAs — report LOGIN_BLOCKED for that product and move on.
4. When a classification report handoff arrives (its own turn): save the report lines to a file and run `watch.py classify-report <file>` — it parses the fixed-format CODEX/CLAUDE lines and runs check-done + classify per line (no manual transcription). Then end the turn quietly with no user-visible message for routine classifications.
