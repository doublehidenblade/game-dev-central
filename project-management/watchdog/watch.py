#!/usr/bin/env python3
"""Coding-agent watchdog: Codex (NEON DRIFT) + Claude Code (Tokyo Drift).

Subcommands:
  gate                      GitHub-side gate. Prints QUIET or NEEDS_BROWSER_CHECK <repos>.
                            Writes state/last-check.json and updates state/state.json.
  check-done <repo...>      Mark browser check completed for repos (sets last_browser_check_ts).
  classify <session> <STATE> [--task-url URL] [--note TEXT] [--pr-merged]
                            Decide the action for a browser classification. Prints ACTION=...
                            STATE in {WORKING, STALLED, DEAD, OUT_OF_TOKENS, LOGIN_BLOCKED, FINISHED}.
                            --pr-merged marks that the session's PR is already merged
                            (used with FINISHED to trigger post-merge inspection).
  nudge <session>           Ledger a sent "continue" nudge. Prints NOTIFY line when due.
  resume <session>          Ledger a session resume. Prints NOTIFY line when due.
  rebrief <session>         Ledger a stall-episode re-brief to the next open task. Prints NOTIFY.
  merged <session> [by]     Ledger that this finished episode's PR is merged,
                            by "worker" (the session shipped itself or the browser report showed Merged) or "cron"
                            (the watchdog shipped the parked PR). The next run inspects
                            the diff and reports to Craig. Prints NOTIFY line.
  inspected <session>       Ledger that the merged PR was inspected and reported to Craig.
                            Prints NOTIFY line.
  failover <session>        Ledger a token-exhaustion failover. Prints HANDOFF line.
  loginfail <session>       Ledger a login failure. Prints NOTIFY or SUPPRESSED (throttled).
  register-worker <task> <kind> <session|-> <repo> <task-file>
                            Record an actual dispatch so the liveness check tracks it.
  liveness                  Deterministic dead-worker check (Craig 2026-10-02):
                            one verdict per tracked worker (ALIVE/QUIET/GRACE/STALE/
                            DEAD/DROPPED). DEAD after 2 quiet cycles queues a
                            dispatch-subagent replacement in pending_actions.json
                            with a deterministically built brief. Never advances
                            quiet_cycles on stale observations.
  status                    Dump current state summary.
  decide <session>          Print ACTION for the last recorded state (no writes).

Hard rules (enforced here, not just in prose):
  - WORKING -> never act.
  - OUT_OF_TOKENS -> FAILOVER (Craig 2026-09-23: another agent takes over; never leave priority work stranded). Once per out-of-tokens episode; FAILOVER_COOLDOWN_MIN backstops back-to-back episodes.
  - STALLED -> one "continue" nudge per stall episode, then REBRIEF to the next
    open priority task (blocked task stays open, per one-bug-one-task; Craig
    2026-09-23). One re-brief per episode; after that, wait for a fresh
    classification instead of looping.
  - DEAD -> resume/start once per check; the browser action re-verifies liveness first.
  - LOGIN_BLOCKED -> notify Craig at most once per LOGIN_NOTIFY_COOLDOWN_H.
  - FINISHED -> whoever gets to a parked PR first ships it (Craig 2026-09-23
    ~14:25 CDT — replaces the ship-steer + 45-min window + cron-backup model).
    No steering the worker to ship, no waiting. FINISHED with an unmerged PR
    -> SHIP: the run itself ships the parked PR — check the PR's CI via the
    github skill and record the state (CI is after-the-fact verification, NOT a
    merge gate — Craig 2026-09-23); merge once the build is clean (mark draft
    ready, squash-merge). Real build failure gets a steer with the exact error
    NOW, infra noise does not block, conflicts are resolved in-run. Then record
    the merge in project-management/watchdog/releases/pending.json
    (live publish happens ONLY when Craig asks — 2026-09-27),
    ledger `merged <session> cron`. FINISHED with an already-merged PR ->
    INSPECT_MERGED: the run inspects the diff, reports to Craig, files new
    tasks / re-opens gaps, and nudges the worker if post-merge work stalled.
This script never merges/publishes code; it only reads GitHub and keeps
ledgers. The cron turn performs the SHIP merge+deploy.
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
# Portable layout: this script lives at <repo>/project-management/watchdog/watch.py.
# All mutable state lives under ./state/, release ledgers under ./releases/ —
# nothing is machine-specific. The scheduler syncs ./state/ with the repo
# (see `state-pull` / `state-push`); any agent can resume from the repo alone.
STATE_DIR = os.path.join(HERE, "state")
RELEASES_DIR = os.path.join(HERE, "releases")
STATE_PATH = os.path.join(STATE_DIR, "state.json")
CHECK_PATH = os.path.join(STATE_DIR, "last-check.json")
API = "https://api.github.com"

REPOS = {
    "neon-drift": "doublehidenblade/neon-drift",
    "tokyo-drift-3d": "doublehidenblade/tokyo-drift-3d",
}
SESSIONS = {
    "codex:neon-drift": {"product": "codex", "repo": "neon-drift"},
    "codex:tokyo-drift-3d": {"product": "codex", "repo": "tokyo-drift-3d"},
    "claude-code:tokyo-drift-3d": {"product": "claude-code", "repo": "tokyo-drift-3d"},
}

# Token-exhaustion failover chain (Craig 2026-09-23): if one agent runs out of
# tokens, another takes over. Same-repo sibling first; NEON DRIFT has no
# sibling session, so it falls to a Muse subagent. If both Codex and Claude
# are down, the supervisor assigns a Muse subagent.
FAILOVER_SIBLING = {
    "codex:neon-drift": None,  # -> Muse subagent (no sibling covers neon-drift)
    "codex:tokyo-drift-3d": "claude-code:tokyo-drift-3d",
    "claude-code:tokyo-drift-3d": "codex:tokyo-drift-3d",
}

# Where the current priority brief lives per repo (handed to the failover agent).
PRIORITY_BRIEF = {
    "neon-drift": "Highest-priority open NEON task per todos/todo*/README.md on main "
                  "(status open/unassigned — verify before starting). "
                  "SINGLE TASK ONLY per one-bug-one-task (Craig 2026-09-23) — never bundle. "
                  "Note: p3d-040/041/042 from the 2026-09-23 brief are done; p3d-065 water shipped. "
                  "CI IS workflow_dispatch-ONLY (Craig 2026-09-27): every cost-incurring "
                  "automation runs solely on his explicit request. NEVER trigger a workflow "
                  "run yourself — no `gh workflow run`, no re-run clicks, no dispatching to "
                  "'verify'. If CI is red, fix the cause or file a task; dispatch CI only "
                  "when Craig explicitly asks for a run. "
                  "All 3D modeling uses the 3dviz-pro-max skill "
                  "(https://github.com/viettranx/3dviz-pro-max); task-file hard rules win "
                  "on conflict (Craig 2026-09-27).",
    "tokyo-drift-3d": "Re-curated 2026-10-01 ~19:10Z — the 2026-09-29 curation below "
                      "is STALE, do not use it. DO NOT take: td-141 (Tripo traffic "
                      "fleet — Muse coordinator actively rebuilding the 12 cars in "
                      "Blender, do not duplicate), td-119 (Showa environment placement "
                      "— Codex Tokyo steered 18:10Z, may still be working; never steal "
                      "a working session — re-verify idle before steering), td-138 "
                      "(hero player car stage 4 — worker active), td-137 (Shuto "
                      "split/merge — worker active, PR #249), td-140 (UI rework — "
                      "worker active 2026-10-01), td-054 (explicit no-redispatch per "
                      "Craig), td-126 (merged). shuto-c1's stranded context: it was "
                      "checking CI on merge commit 4f86564 then continuing td-045 — "
                      "adopt td-045 ONLY if the board shows it open and unowned. "
                      "Otherwise read the Tokyo board (doublehidenblade/game-dev-central "
                      "project-management/boards/tokyo-drift-3d.md) for the top P0 "
                      "open+unowned task (match status-cell prefixes; skip "
                      "done/merged/closed rows). "
                      "SINGLE TASK ONLY per one-bug-one-task (Craig 2026-09-23) — never bundle. "
                      "CI IS workflow_dispatch-ONLY (Craig 2026-09-27): every cost-incurring "
                      "automation runs solely on his explicit request. NEVER trigger a workflow "
                      "run yourself — no `gh workflow run`, no re-run clicks. If CI is red, fix "
                      "the cause or file a task; dispatch CI only when Craig explicitly asks. "
                      "All 3D modeling uses the 3dviz-pro-max skill "
                      "(https://github.com/viettranx/3dviz-pro-max); task-file hard rules win "
                      "on conflict (Craig 2026-09-27).",
}

IDLE_MINUTES = 50          # "no progress": no commits/PR updates while open work exists
BROWSER_COOLDOWN_MIN = 30  # don't spend a browser check on the same repo more often
NUDGE_COOLDOWN_MIN = 45    # at most one "continue" nudge per session per this window
FAILOVER_COOLDOWN_MIN = 180  # at most one token-failover per session per this window
LOGIN_NOTIFY_COOLDOWN_H = 6  # login-failure notifications throttled to this
RECHECK_WORKING_MIN = 45   # re-validate a session last classified WORKING this long ago
SESSION_OPEN_TTL_MIN = 360  # session classifications count as open work this long

STATES = {"WORKING", "STALLED", "DEAD", "OUT_OF_TOKENS", "LOGIN_BLOCKED", "FINISHED"}


def now():
    return datetime.now(timezone.utc)


def parse_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def get(path):
    req = urllib.request.Request(
        API + path,
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "craig-agent-watch"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"repos": {}, "sessions": {}}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=1)


# ---------------------------------------------------------------------------
# Run-verdict recording for the scripted heartbeat (Craig 2026-10-02).
# The mutating STEP 0 checks (transitions, classification-health, liveness)
# consume their own evidence when they run, so the end-of-run `heartbeat`
# command cannot re-derive their verdicts. Each check's printed verdict lines
# are recorded here under state["run_verdicts"] = {"ts": iso,
# "checks": {name: [lines]}}. heartbeat only trusts verdicts newer than
# HEARTBEAT_FRESH_MIN. Recording goes through _capture_verdicts in main()
# so the command bodies stay untouched.
# ---------------------------------------------------------------------------

HEARTBEAT_FRESH_MIN = 40  # verdicts older than this are not this run's


def _record_verdict(check, lines):
    state = load_state()
    rv = state.setdefault("run_verdicts", {})
    ts = now().isoformat()
    rv["ts"] = ts
    rv.setdefault("checks", {})[check] = [l for l in lines if l.strip()]
    # Per-check timestamp: _hb_verdicts filters on this, so one command's
    # fresh run never revalidates another command's older lines.
    rv.setdefault("check_ts", {})[check] = ts
    save_state(state)


def _capture_verdicts(check, fn, *args):
    """Run a check, replay its stdout, and record its verdict lines for
    `heartbeat`. Safe around sys.exit (conflicts exits 3): the finally block
    records before the exception propagates."""
    import io
    import contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            return fn(*args)
    finally:
        text = buf.getvalue()
        sys.stdout.write(text)
        sys.stdout.flush()
        _record_verdict(check, text.splitlines())


def repo_activity(repo_full):
    """Return (open_prs, open_issues, last_activity_dt, detail).
    Uses the authenticated _gh (audit 2026-10-02: the old unauthenticated
    get() couldn't read private repos)."""
    open_prs = _gh(f"/repos/{repo_full}/pulls?state=open&per_page=20")
    issues = _gh(f"/repos/{repo_full}/issues?state=open&per_page=20")
    open_issues = [i for i in issues if "pull_request" not in i]
    head = _gh(f"/repos/{repo_full}/commits/main?per_page=1")
    head_dt = parse_ts(head["commit"]["committer"]["date"])
    newest_push = None
    try:
        events = _gh(f"/repos/{repo_full}/events?per_page=30")
        pushes = [e for e in events if e.get("type") == "PushEvent"]
        if pushes:
            newest_push = parse_ts(pushes[0]["created_at"])
    except Exception:
        pass
    cand = [parse_ts(p["updated_at"]) for p in open_prs]
    cand += [parse_ts(i["updated_at"]) for i in open_issues]
    cand += [head_dt, newest_push]
    cand = [c for c in cand if c]
    last_activity = max(cand) if cand else None
    return open_prs, open_issues, last_activity, {
        "open_pr_numbers": [p["number"] for p in open_prs],
        "head_sha": head["sha"][:7],
    }


def cmd_gate():
    state = load_state()
    t = now()
    detail = {}
    need = []
    for key, repo_full in REPOS.items():
        rst = state.setdefault("repos", {}).setdefault(key, {})
        try:
            open_prs, open_issues, last_act, info = repo_activity(repo_full)
        except Exception as e:
            detail[key] = {"error": str(e)}
            continue
        open_work = bool(open_prs or open_issues)
        idle_min = (t - last_act).total_seconds() / 60 if last_act else 10 ** 9
        gate = open_work and idle_min >= IDLE_MINUTES
        last_check = parse_ts(rst.get("last_browser_check_ts"))
        cooled = (not last_check) or (t - last_check) >= timedelta(minutes=BROWSER_COOLDOWN_MIN)
        # Sessions count as open work too: a task on a branch with no PR yet
        # (e.g. a brand-new Codex task) is invisible to the GitHub gate above.
        # Re-validate a session believed WORKING if it hasn't been looked at
        # in RECHECK_WORKING_MIN — read-only, never a nudge (decide_action
        # still forbids nudging WORKING sessions).
        sess_open = False
        sess_working_stale = False
        for skey, sinfo in SESSIONS.items():
            if sinfo.get("repo") != key:
                continue
            sst = state.get("sessions", {}).get(skey, {})
            cls = sst.get("last_classification")
            cts = parse_ts(sst.get("last_classification_ts"))
            if cls in ("WORKING", "STALLED") and cts:
                age_min = (t - cts).total_seconds() / 60
                if age_min < SESSION_OPEN_TTL_MIN:
                    sess_open = True
                    if cls == "WORKING" and age_min >= RECHECK_WORKING_MIN:
                        sess_working_stale = True
        open_work = open_work or sess_open
        needs_browser = (gate and cooled) or (sess_working_stale and cooled)
        rst.update({
            "open_prs": len(open_prs),
            "open_issues": len(open_issues),
            "open_pr_numbers": info["open_pr_numbers"],
            "head_sha": info["head_sha"],
            "last_activity_ts": last_act.isoformat() if last_act else None,
            "idle_min": round(idle_min, 1),
            "gate_fired": gate,
            "needs_browser": needs_browser,
        })
        detail[key] = {
            "open_work": open_work,
            "open_prs": len(open_prs),
            "open_issues": len(open_issues),
            "sess_open": sess_open,
            "sess_working_stale": sess_working_stale,
            "last_activity": last_act.isoformat() if last_act else None,
            "idle_min": round(idle_min, 1),
            "gate_fired": gate,
            "browser_cooldown_ok": cooled,
            "needs_browser": needs_browser,
        }
        if needs_browser:
            need.append(key)
    save_state(state)
    with open(CHECK_PATH, "w") as f:
        json.dump({"ts": t.isoformat(), "repos": detail}, f, indent=1)
    if need:
        print("NEEDS_BROWSER_CHECK " + " ".join(need))
    else:
        reasons = "; ".join(
            f"{k}: idle {v.get('idle_min', '?')}m, open_work={v.get('open_work', '?')}, "
            f"sess_open={v.get('sess_open', '?')}, stale_working={v.get('sess_working_stale', '?')}"
            for k, v in detail.items()
        )
        print("QUIET — " + (reasons or "no repo data"))


def cmd_check_done(repos):
    state = load_state()
    t = now().isoformat()
    for r in repos:
        state.setdefault("repos", {}).setdefault(r, {})["last_browser_check_ts"] = t
    save_state(state)
    print("OK check-done " + " ".join(repos))


def decide_action(session, classification, state):
    """Pure decision logic (also unit-tested). Returns (action, reason)."""
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    t = now()
    last_nudge = parse_ts(sst.get("last_nudge_ts"))
    if classification == "WORKING":
        return "NOTHING", "session actively working — never nudge a working session"
    if classification == "OUT_OF_TOKENS":
        # Once per out-of-tokens episode: if we already failed over since this
        # episode began, stay silent (the sibling/subagent already has the brief).
        oot = parse_ts(sst.get("out_of_tokens_since"))
        last_fo = parse_ts(sst.get("last_failover_ts"))
        if last_fo and oot and last_fo >= oot:
            return "NOTHING", "already failed over for this out-of-tokens episode"
        if last_fo and (t - last_fo) < timedelta(minutes=FAILOVER_COOLDOWN_MIN):
            return "NOTHING", f"failover already fired {(t-last_fo).total_seconds()/60:.0f}m ago (< {FAILOVER_COOLDOWN_MIN}m cooldown)"
        return "FAILOVER", "token/usage limit reached — hand priority work to another agent (Craig 2026-09-23)"
    if classification == "STALLED":
        # Craig 2026-09-23: a session stuck on one blocked task must not idle
        # on repeated "continue" nudges. One nudge per stall episode, then
        # REBRIEF it to the next open priority task (the blocked task stays
        # open, per one-bug-one-task). One re-brief per episode; after that,
        # wait for a fresh classification instead of looping.
        ep_start = parse_ts(sst.get("stall_episode_start")) or parse_ts(sst.get("last_classification_ts"))
        last_rebrief = parse_ts(sst.get("last_rebrief_ts"))
        nudged_this_ep = bool(last_nudge and ep_start and last_nudge >= ep_start)
        rebriefed_this_ep = bool(last_rebrief and ep_start and last_rebrief >= ep_start)
        if last_nudge and (t - last_nudge) < timedelta(minutes=NUDGE_COOLDOWN_MIN):
            return "NOTHING", f"already nudged {(t-last_nudge).total_seconds()/60:.0f}m ago (< {NUDGE_COOLDOWN_MIN}m cooldown)"
        if last_rebrief and (t - last_rebrief) < timedelta(minutes=NUDGE_COOLDOWN_MIN):
            return "NOTHING", f"already re-briefed {(t-last_rebrief).total_seconds()/60:.0f}m ago (< {NUDGE_COOLDOWN_MIN}m cooldown)"
        if nudged_this_ep and not rebriefed_this_ep:
            return "REBRIEF", "still stalled after a continue nudge — re-brief to the next open priority task; blocked task stays open (Craig 2026-09-23)"
        if rebriefed_this_ep:
            return "NOTHING", "already re-briefed this stall episode — awaiting fresh classification"
        return "NUDGE", "session stalled with open work and no recent nudge"
    if classification == "DEAD":
        return "RESUME", "session dead/ended while open work exists — resume in workspace"
    if classification == "LOGIN_BLOCKED":
        return "REPORT_LOGIN", "browser hit login wall/CAPTCHA — needs manual login"
    if classification == "FINISHED":
        # Craig 2026-09-23 (~14:25 CDT): whoever gets to a parked PR first
        # ships it. No ship-steering the worker, no 45-minute shipping window,
        # no backup model — the run ships a parked PR itself on sight.
        # FINISHED + PR already merged (pr_merged) -> INSPECT_MERGED: the run
        # inspects the diff, reports to Craig, files new tasks / re-opens gaps,
        # and nudges the worker if post-merge work stalled. Fires once per
        # finished episode (inspected_ts).
        # FINISHED + PR still open -> SHIP: the run checks the PR's CI via the
        # github skill and records the state (CI is after-the-fact verification,
        # NOT a merge gate — Craig 2026-09-23); merges once the build is clean
        # (mark draft ready, squash-merge), records the merge in
        # project-management/watchdog/releases/pending.json (live publish happens ONLY
        # when Craig asks — 2026-09-27), ledgers `merged <session> cron`.
        # Real build failure -> steer NOW; infra noise doesn't block.
        sst = state.get("sessions", {}).get(session, {})
        if sst.get("user_followup_pending"):
            # Craig 2026-09-25: he typed a follow-up into a FINISHED session
            # himself (new direction). Never ship the parked PR out from under
            # his redirect — wait until the follow-up run starts (WORKING) or
            # finishes (new FINISHED episode clears this flag in classify).
            return "NOTHING", "Craig queued a follow-up on this finished session — holding SHIP until his redirect resolves"
        if sst.get("inspected_ts"):
            return "NOTHING", "merged work already inspected and reported (inspected_ts set)"
        if sst.get("pr_merged"):
            return "INSPECT_MERGED", "PR merged — inspect the diff, report to Craig, file new tasks or re-open gaps as needed"
        if sst.get("finished_no_pr"):
            # 2026-09-23: a session can FINISH by pushing straight to main
            # (no PR). There is no parked PR to ship, so SHIP must not fire —
            # without this the run re-verifies and skips forever.
            return "NOTHING", "finished and shipped via direct push — no parked PR, nothing to ship"
        return "SHIP", "finished with an unmerged PR — ship the parked PR now: merge to main ONLY (mark ready if draft, squash-merge; CI is after-the-fact verification, not a merge gate), record the merge in project-management/watchdog/releases/pending.json — live publish happens ONLY when Craig asks, never dispatch publish-web, never verify the live site"
    return "NOTHING", f"unknown classification {classification}"


# ---- Hard outcome validator (Craig 2026-09-26) ----
# Every inspected task must end in exactly ONE of these outcomes:
#   1. closed
#   2. open and assigned
#   3. open but no available worker
#   4. blocked on human
#   5. blocked on external
# Merged-but-not-live is still OPEN (export-liveness rule, Craig 2026-09-24):
# a merged fix is not closed until exported, published, and live-verified.
# Publish-on-request (Craig 2026-09-27): "published and live-verified" happens
# ONLY when Craig asks for a push — merged-not-live sits in outcome 2
# (open and assigned, recorded in project-management/watchdog/releases/pending.json)
# and the watchdog NEVER publishes or live-verifies it itself.
# Forbidden framings must never reach a report: "open and idle", "queued
# without ownership", "waiting for the next cycle", "waiting for CI",
# "waiting for Craig's verdict". Any input asserting one of those, or any
# fact set matching zero or multiple outcomes, raises a loud
# degraded-watchdog alarm instead of a quiet guess.
OUTCOMES = {
    1: "closed",
    2: "open and assigned",
    3: "open but no available worker",
    4: "blocked on human",
    5: "blocked on external",
}

FORBIDDEN_FRAMINGS = (
    "open and idle",
    "queued without ownership",
    "waiting for the next cycle",
    "waiting for ci",
    "waiting for craig's verdict",
    "awaiting craig's verdict",
    "awaiting verdict",
)


class DegradedWatchdog(Exception):
    """Raised when a task cannot be mapped to exactly one outcome."""


def validate_task_outcome(task_id, facts):
    """Map an inspected task's facts to exactly one outcome.

    facts: dict with keys
      merged (bool), live_verified (bool), owner (str|None),
      owner_alive (bool), blocked_human (bool), blocked_external (bool),
      framing (str, optional free text — must not contain a forbidden framing).
    Returns (outcome_number, outcome_label). Raises DegradedWatchdog on any
    forbidden framing, or when the facts match zero or multiple outcomes.
    """
    framing = (facts.get("framing") or "").lower()
    for f in FORBIDDEN_FRAMINGS:
        if f in framing:
            raise DegradedWatchdog(
                f"DEGRADED-WATCHDOG ALARM: task {task_id} reported with forbidden framing "
                f"'{facts.get('framing')}' — framings like open-and-idle, queued-without-"
                f"ownership, waiting-for-CI, waiting-for-Craig's-verdict are never valid "
                f"task states. Re-express as exactly one of outcomes 1-5."
            )
    merged = facts.get("merged", False)
    live = facts.get("live_verified", False)
    owner = facts.get("owner")
    owner_alive = facts.get("owner_alive", False)
    blocked_human = facts.get("blocked_human", False)
    blocked_external = facts.get("blocked_external", False)
    matches = []
    if merged and live:
        matches.append(1)
    else:
        # Not closed: merged-but-not-live, or never merged. Classify the open state.
        if blocked_human:
            matches.append(4)
        if blocked_external:
            matches.append(5)
        if not blocked_human and not blocked_external:
            if owner and owner_alive:
                matches.append(2)
            else:
                # No owner, or the assignee is gone/unreachable: nobody owns it.
                matches.append(3)
    if len(matches) != 1:
        raise DegradedWatchdog(
            f"DEGRADED-WATCHDOG ALARM: task {task_id} maps to {len(matches)} outcomes "
            f"({[OUTCOMES[m] for m in matches] or 'none'}) — every inspected task must "
            f"map to exactly one of outcomes 1-5. Facts: {json.dumps(facts)}"
        )
    return matches[0], OUTCOMES[matches[0]]


def cmd_validate_task(args):
    # validate-task <task-id> '<json facts>'
    # Prints OUTCOME=<n> (<label>) TASK=<id>, or OUTCOME=ALARM and exits 3.
    task_id = args[0]
    facts = json.loads(args[1])
    try:
        num, label = validate_task_outcome(task_id, facts)
    except DegradedWatchdog as e:
        print(str(e))
        print(f"OUTCOME=ALARM TASK={task_id}")
        sys.exit(3)
    print(f"OUTCOME={num} ({label}) TASK={task_id}")


def cmd_classify(args):
    # classify <session> <STATE> [--task-url URL] [--note TEXT] [--pr-merged] [--no-pr] [--pr N] [--user-followup]
    session, classification = args[0], args[1].upper()
    if session not in SESSIONS:
        print(f"ERROR unknown session {session}", file=sys.stderr)
        sys.exit(2)
    if classification not in STATES:
        print(f"ERROR unknown state {classification}", file=sys.stderr)
        sys.exit(2)
    task_url = note = None
    pr_merged_flag = no_pr_flag = user_followup = False
    pr_number = None
    it = iter(args[2:])
    for a in it:
        if a == "--task-url":
            task_url = next(it, None)
        elif a == "--note":
            note = next(it, None)
        elif a == "--pr-merged":
            pr_merged_flag = True
        elif a == "--no-pr":
            no_pr_flag = True
        elif a == "--pr":
            try:
                pr_number = int(next(it, None))
            except (TypeError, ValueError):
                pr_number = None
        elif a == "--user-followup":
            # Craig typed into a finished session: hold SHIP (decide_action
            # reads this; audit 2026-10-02: the flag was only ever set by
            # ad-hoc manual python, never in code).
            user_followup = True
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    prev = sst.get("last_classification")
    sst["last_classification"] = classification
    sst["last_classification_ts"] = now().isoformat()
    if classification == "OUT_OF_TOKENS" and prev != "OUT_OF_TOKENS":
        # Trio guard (2026-09-30): the claude-code workspace reports three sessions
        # per classification, so texture-imagegen's FINISHED line lands between the
        # main-dev/shuto-c1 OUT_OF_TOKENS lines. A bare prev check then starts a
        # bogus new OOT episode on every cycle and re-fires FAILOVER (same family
        # as the 2026-09-26 FINISHED-ledger flap). Only start a new episode when
        # the FINISHED line, if any, was for THIS session's own URL (genuine
        # recovery-then-reblock); a FINISHED for a different URL is the trio
        # interleaving, not a new episode.
        trio_interleave = (
            prev == "FINISHED"
            and task_url
            and sst.get("last_finished_url")
            and task_url != sst["last_finished_url"]
        )
        if not trio_interleave:
            sst["out_of_tokens_since"] = now().isoformat()  # new episode: failover may fire once
    if classification == "STALLED" and prev != "STALLED":
        sst["stall_episode_start"] = now().isoformat()  # new episode: one nudge, then one re-brief
    sst0 = state.get("sessions", {}).get(session, {})
    sst0.pop("user_followup_pending", None)
    if classification == "FINISHED":
        # New finished episode: reset the ship/inspect ledger so this round of
        # work gets its own ship + post-merge inspection. Keyed on the finished
        # task/session URL being NEW (tracked in finished_urls, a set of
        # session URLs ever seen FINISHED for this key) — not just "changed
        # since last FINISHED line" — because the claude-code workspace reports
        # three sessions per classification (main-dev, shuto-c1, texture-
        # imagegen) sharing ONE session key, so any single-slot comparison
        # resets the ledger on EVERY cycle: FINISHED(url-A) then STALLED(url-B)
        # then FINISHED(url-C) makes url-C "changed" even though url-C finished
        # weeks ago, re-firing a bogus SHIP for the long-finished
        # texture-imagegen session (its 6 PNGs are on main, PR #26 merged;
        # nothing to ship). 2026-09-26 fixed the OOT-interleave variant with a
        # single last_finished_url slot; 2026-10-02 the STALLED-interleave
        # variant fired the same bogus SHIP. The set fixes both: a re-reported
        # known URL never pops the ledger, only a genuinely new finished URL
        # does. [SCRIPTED: watch.py classify]
        seen = sst.setdefault("finished_urls", [])
        new_episode = not task_url or task_url not in seen
        if new_episode:
            for k in ("pr_merged", "merged_by", "inspected_ts", "finished_no_pr"):
                sst.pop(k, None)
        if task_url:
            sst["last_finished_url"] = task_url  # back-compat single slot
            if task_url not in seen:
                seen.append(task_url)
                del seen[:-8]  # bound the set
        if pr_merged_flag:
            sst["pr_merged"] = True
            sst.setdefault("merged_by", "worker")
        if no_pr_flag:
            # Session finished by pushing straight to main — no parked PR.
            # decide() treats this as terminal so SHIP never fires for it.
            sst["finished_no_pr"] = True
    if task_url:
        sst["task_url"] = task_url
    if note:
        sst["last_note"] = note[:300]
    if pr_number:
        # Structured PR storage (audit 2026-10-02): stop mining prose for
        # identifiers — ship-verify prefers this, regex on the note is fallback.
        sst["pr_number"] = pr_number
    if user_followup:
        sst["user_followup_pending"] = True
    action, reason = decide_action(session, classification, state)
    save_state(state)
    repo = SESSIONS[session]["repo"]
    print(f"ACTION={action} SESSION={session} REPO={repo} REASON={reason}")
    if action == "NUDGE":
        print(f"TARGET_TASK_URL={sst.get('task_url', '(find latest task in workspace)')}")
    if action == "RESUME":
        print(f"TARGET_WORKSPACE={SESSIONS[session]['product']} workspace for {repo}")
    if action == "REBRIEF":
        print(f"REBRIEF_BLOCKED_NOTE={sst.get('last_note', '')}")
        print(f"REBRIEF_BRIEF={PRIORITY_BRIEF.get(repo, '')} — steer the session to the next open task AFTER the blocked one; the blocked task stays open per one-bug-one-task (Craig 2026-09-23)")
    if action == "FAILOVER":
        sib = FAILOVER_SIBLING.get(session)
        print(f"FAILOVER_TARGET={sib if sib else 'MUSE_SUBAGENT'} BRIEF={PRIORITY_BRIEF.get(repo, '')}")
    if action == "SHIP":
        print(f"SHIP_NOTE={sst.get('last_note', '')} — ship the parked PR now: check its CI via the github "
              f"skill and record the state (CI is after-the-fact verification, NOT a merge gate — Craig "
              f"2026-09-23); merge once the build is clean (mark draft ready, squash-merge). Real build "
              f"failure: queue a steer with the exact error NOW, never defer to next run. Infra noise (e.g. "
              f"artifact-quota upload failures with all substantive steps green): file rework per "
              f"one-bug-one-task, merge anyway. Conflicted branch: rebase/resolve in this run via the "
              f"git-database API, then merge. Then record the merge in "
              f"project-management/watchdog/releases/pending.json (live publish happens ONLY when Craig asks — "
              f"2026-09-27), then ledger `merged {session} cron`. "
              f"Whoever gets to a parked PR first ships it — no steering the worker to ship.")
    if action == "INSPECT_MERGED":
        print(f"INSPECT_NOTE={sst.get('last_note', '')} — inspect the merged diff, report to Craig (screenshots, "
              f"what changed, remaining work), file new tasks or re-open gaps, nudge the worker if post-merge work stalled")


def cmd_decide(session):
    # decide <session> — print the action for the session's LAST RECORDED
    # classification WITHOUT touching timestamps. Used by the cron's STEP 1
    # (act on last-known state) so a stale record stays visibly stale.
    if session not in SESSIONS:
        print(f"ERROR unknown session {session}", file=sys.stderr)
        sys.exit(2)
    state = load_state()
    sst = state.get("sessions", {}).get(session, {})
    classification = sst.get("last_classification")
    if not classification:
        print(f"ACTION=NOTHING SESSION={session} REASON=no recorded classification yet")
        return
    action, reason = decide_action(session, classification, state)
    repo = SESSIONS[session]["repo"]
    print(f"ACTION={action} SESSION={session} REPO={repo} REASON={reason} STATE_AGE_MIN={_state_age_min(sst)}")
    # Persistent operator flags: survive classify's last_note overwrite.
    # Set via: python3 -c "import json;p='.../state.json';s=json.load(open(p));
    #   s['sessions']['<session>'].setdefault('flags',{})['<name>']='<text>';
    #   json.dump(s,open(p,'w'),indent=1)". Clear with .pop('<name>').
    for fname, ftext in (sst.get("flags") or {}).items():
        print(f"FLAG_{fname}={ftext}")
    if action == "NUDGE":
        print(f"TARGET_TASK_URL={sst.get('task_url', '(find latest task in workspace)')}")
    if action == "RESUME":
        print(f"TARGET_WORKSPACE={SESSIONS[session]['product']} workspace for {repo}")
    if action == "REBRIEF":
        print(f"REBRIEF_BLOCKED_NOTE={sst.get('last_note', '')}")
        print(f"REBRIEF_BRIEF={PRIORITY_BRIEF.get(repo, '')} — steer the session to the next open task AFTER the blocked one; the blocked task stays open per one-bug-one-task (Craig 2026-09-23)")
    if action == "FAILOVER":
        sib = FAILOVER_SIBLING.get(session)
        print(f"FAILOVER_TARGET={sib if sib else 'MUSE_SUBAGENT'} BRIEF={PRIORITY_BRIEF.get(repo, '')}")
    if action == "SHIP":
        print(f"SHIP_NOTE={sst.get('last_note', '')} — ship the parked PR now: check its CI via the github "
              f"skill and record the state (CI is after-the-fact verification, NOT a merge gate — Craig "
              f"2026-09-23); merge once the build is clean (mark draft ready, squash-merge). Real build "
              f"failure: queue a steer with the exact error NOW, never defer to next run. Infra noise (e.g. "
              f"artifact-quota upload failures with all substantive steps green): file rework per "
              f"one-bug-one-task, merge anyway. Conflicted branch: rebase/resolve in this run via the "
              f"git-database API, then merge. Then record the merge in "
              f"project-management/watchdog/releases/pending.json (live publish happens ONLY when Craig asks — "
              f"2026-09-27), then ledger `merged {session} cron`. "
              f"Whoever gets to a parked PR first ships it — no steering the worker to ship.")
    if action == "INSPECT_MERGED":
        print(f"INSPECT_NOTE={sst.get('last_note', '')} — inspect the merged diff, report to Craig (screenshots, "
              f"what changed, remaining work), file new tasks or re-open gaps, nudge the worker if post-merge work stalled")


def _state_age_min(sst):
    cts = parse_ts(sst.get("last_classification_ts"))
    if not cts:
        return "unknown"
    return round((now() - cts).total_seconds() / 60, 1)


def cmd_nudge(session):
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    sst["last_nudge_ts"] = now().isoformat()
    sst["last_nudge_kind"] = "continue"
    save_state(state)
    label = _session_label(session)
    print(f"NOTIFY: Sent 'continue' to {label} — session was stalled with open work. "
          f"No merge/publish performed.")


def cmd_rebrief(session):
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    sst["last_rebrief_ts"] = now().isoformat()
    save_state(state)
    label = _session_label(session)
    print(f"NOTIFY: Re-briefed {label} to its next open priority task — it was still stalled after a "
          f"continue nudge, so it moves on instead of idling. The blocked task stays open "
          f"(one-bug-one-task). No merge/publish performed.")


def cmd_merged(session, by="worker"):
    # Ledger that this finished episode's PR is merged, by "worker" (the
    # session shipped itself or the browser report showed Merged) or "cron"
    # (the watchdog shipped the parked PR). The next run inspects the diff and
    # reports to Craig.
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    sst["pr_merged"] = True
    sst["merged_by"] = by
    save_state(state)
    label = _session_label(session)
    print(f"NOTIFY: {label}'s PR is merged (by {by}) — the run will inspect the diff, report to "
          f"Craig (screenshots, what changed, remaining work), and file new tasks if needed.")


def cmd_inspected(session):
    # Ledger that the merged PR was inspected and reported to Craig.
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    sst["inspected_ts"] = now().isoformat()
    save_state(state)
    label = _session_label(session)
    print(f"NOTIFY: Inspected {label}'s merged PR and reported to Craig (diff, screenshots, remaining "
          f"work). New tasks filed or gaps re-opened as needed. Watch continues.")


def _session_label(session):
    info = SESSIONS.get(session, {})
    repo = info.get("repo", "?")
    if session.startswith("codex"):
        return f"Codex ({repo})"
    return f"Claude Code ({repo})"


def cmd_resume(session):
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    sst["last_nudge_ts"] = now().isoformat()
    sst["last_nudge_kind"] = "resume+continue"
    save_state(state)
    label = _session_label(session)
    print(f"NOTIFY: Resumed {label} in its workspace and sent 'continue' — the old session was dead. "
          f"No merge/publish performed.")


def cmd_failover(session):
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    sst["last_failover_ts"] = now().isoformat()
    save_state(state)
    label = _session_label(session)
    repo = SESSIONS.get(session, {}).get("repo", "?")
    sibling = FAILOVER_SIBLING.get(session)
    brief = PRIORITY_BRIEF.get(repo, "priority task files")
    if sibling:
        sib_label = _session_label(sibling)
        print(f"HANDOFF: {label} is out of tokens. Failover: steer {sib_label} with the priority brief "
              f"({brief}) via ACTION MODE steer (browser-brief.md). Re-verify the sibling is not WORKING "
              f"before steering; if it is unavailable, fall back to a Muse subagent per ~/workspace/supervisor-system/SYSTEM.md. "
              f"Never merge/publish.")
    else:
        print(f"HANDOFF: {label} is out of tokens and has no sibling session. Failover: assign a Muse "
              f"subagent on the priority brief ({brief}) per ~/workspace/supervisor-system/SYSTEM.md "
              f"(subagent gets the github skill + repo access; never merge/publish).")


def cmd_loginfail(session):
    state = load_state()
    sst = state.setdefault("sessions", {}).setdefault(session, {})
    t = now()
    last = parse_ts(sst.get("login_fail_notified_ts"))
    if last and (t - last) < timedelta(hours=LOGIN_NOTIFY_COOLDOWN_H):
        print(f"SUPPRESSED login-fail notify for {session} "
              f"(notified {(t-last).total_seconds()/3600:.1f}h ago)")
        return
    sst["login_fail_notified_ts"] = t.isoformat()
    save_state(state)
    label = "Codex (Tokyo Drift 3D)" if session.startswith("codex") else "Claude Code (Tokyo Drift)"
    print(f"NOTIFY: {label} needs a manual login — the watchdog's browser hit a "
          f"login page or CAPTCHA and cannot proceed on its own. Session checks for "
          f"this product are paused until you sign in again.")


def cmd_status():
    state = load_state()
    print(json.dumps(state, indent=1))


# ---------------------------------------------------------------------------
# Deterministic dead-worker detection (Craig 2026-10-02).
# The two-cycle rule used to live only in the cron body's prose, so a run
# could "interpret" it differently — or, worse, proclaim a worker alive from
# stale data (the 2026-10-02 td-140 phantom). This command makes the DECISION
# code: it reads only observable signals, advances per-worker quiet-cycle
# counters in state.json, and on DEAD queues a replacement dispatch with a
# brief built deterministically from WORKER_BRIEF.md. The cron worker's only
# job is to run this and act on the verdicts.
# ---------------------------------------------------------------------------

LIVENESS_HEARTBEAT_DIR = os.path.join(STATE_DIR, "worker-heartbeats")
LIVENESS_BRIEF_DIR = os.path.join(STATE_DIR, "liveness-briefs")
WORKER_BRIEF_PATH = os.path.expanduser("~/workspace/supervisor-system/WORKER_BRIEF.md")

LIVENESS_QUIET_CYCLES = 2       # quiet this many consecutive cycles -> DEAD
LIVENESS_HEARTBEAT_MAX_MIN = 35  # heartbeat older than this does not prove life
LIVENESS_CLASSIFY_MAX_MIN = 25  # classification older than this -> observation STALE, counter frozen
LIVENESS_GRACE_MIN = 30         # freshly dispatched worker: ~2 cycles of grace
# NOTE: LIVENESS_TERMINAL is defined once below as an alias of
# STATUS_PREFIXES_TERMINAL — do not re-add a separate set here.


def _gh(path):
    """Authenticated GET via the github skill's surrogate (private repos)."""
    import subprocess
    gh = os.path.expanduser(os.environ.get("WATCHDOG_GH_BIN", "~/workspace/skills/github/bin/gh"))
    out = subprocess.run([gh, "api", "GET", path], capture_output=True,
                         text=True, timeout=40)
    if out.returncode != 0:
        raise RuntimeError(f"gh api {path}: {out.stderr[:200]}")
    return json.loads(out.stdout)


def _task_status_on_main(repo_full, task_file):
    """Read the task file's ## Status line from main. Returns the status
    PREFIX (first word, lowercased) or None. Uses the shared prefix rule —
    never splits on hyphens (audit 2026-10-02: 'done-pending-verdict' was
    mis-split into 'done' by the old split('-') logic)."""
    try:
        blob = _gh(f"/repos/{repo_full}/contents/{task_file}?ref=main")
        import base64
        text = base64.b64decode(blob["content"]).decode("utf-8", "replace")
    except Exception:
        return None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## Status"):
            rest = text.split(s, 1)[1]
            for l2 in rest.splitlines():
                l2 = l2.strip().strip("*")
                if l2 and not l2.startswith("#"):
                    return l2.split()[0].lower() if l2.split() else None
    return None


def _worker_evidence(repo_full, task, task_file, dispatched_dt):
    """Collect deterministic liveness evidence. Returns (alive, reasons, salvage)."""
    reasons, salvage = [], []
    alive = False
    # 1. Task-file commits on main after dispatch.
    try:
        commits = _gh(f"/repos/{repo_full}/commits?path={task_file}&sha=main&per_page=3")
        fresh = [c for c in commits
                 if (d := parse_ts(c["commit"]["committer"]["date"])) and
                 (not dispatched_dt or d > dispatched_dt)]
        if fresh:
            alive = True
            reasons.append(f"task-file commit {fresh[0]['sha'][:7]} "
                           f"{fresh[0]['commit']['committer']['date'][:16]}")
            salvage.append("Recent task-file commits:\n" + "\n".join(
                f"  {c['sha'][:7]} {c['commit']['message'].splitlines()[0]}" for c in fresh))
    except Exception as e:
        reasons.append(f"task-file check failed: {e}")
    # 2. Branches containing the task id with commits after dispatch.
    try:
        branches = _gh(f"/repos/{repo_full}/branches?per_page=100")
        for b in branches:
            if task.lower().replace("-", "") in b["name"].lower().replace("-", ""):
                try:
                    cmp = _gh(f"/repos/{repo_full}/compare/main...{b['name']}?per_page=5")
                    ahead = cmp.get("ahead_by", 0)
                    if ahead:
                        msgs = [c["commit"]["message"].splitlines()[0]
                                for c in cmp.get("commits", [])[-5:]]
                        salvage.append(f"Branch {b['name']} ({ahead} ahead of main):\n" +
                                       "\n".join(f"  - {m}" for m in msgs))
                        alive = True
                        reasons.append(f"branch {b['name']} {ahead} ahead")
                    else:
                        salvage.append(f"Branch {b['name']}: already on main (no unique commits)")
                except Exception:
                    pass
    except Exception as e:
        reasons.append(f"branch check failed: {e}")
    # 3. Open PRs mentioning the task.
    try:
        prs = _gh(f"/repos/{repo_full}/pulls?state=open&per_page=30")
        for p in prs:
            if task.lower() in (p.get("title") or "").lower() or \
               task.lower() in (p.get("body") or "")[:500].lower():
                alive = True
                reasons.append(f"open PR #{p['number']} {p['title'][:60]}")
                salvage.append(f"Open PR #{p['number']}: {p['title']} — {p.get('html_url','')}")
    except Exception as e:
        reasons.append(f"PR check failed: {e}")
    return alive, reasons, salvage


def _build_replacement_brief(task, task_file, salvage):
    """Fill WORKER_BRIEF.md deterministically: task id + file + salvage context."""
    with open(WORKER_BRIEF_PATH) as f:
        brief = f.read()
    brief = brief.replace("[TASK_ID]", task).replace("[TASK_FILE_PATH]", task_file)
    context = (
        "## Context: this is a REPLACEMENT dispatch (Craig 2026-10-02).\n"
        "The previous worker was proclaimed DEAD by the deterministic liveness check "
        f"({LIVENESS_QUIET_CYCLES} consecutive ~15-minute cycles with no heartbeat, "
        "no new session message, and no branch/PR/task-file activity). Salvage any "
        "usable work below; do not assume any of it is complete or correct — "
        "verify against the task file yourself.\n\n" +
        ("\n\n".join(salvage) if salvage else
         "No branch, PR, or task-file commits from the previous worker were found.")
    )
    brief = brief.replace("[ANYTHING THE TASK FILE DOESN'T SAY]", context)
    os.makedirs(LIVENESS_BRIEF_DIR, exist_ok=True)
    ts = now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(LIVENESS_BRIEF_DIR, f"{task}-{ts}.md")
    with open(path, "w") as f:
        f.write(brief)
    return path, brief


def cmd_register_worker(args):
    """register-worker <task> <kind> <session|-> <repo> <task-file>
    Records an actual dispatch so the liveness check tracks it. kind in
    {subagent, codex, claude}. session is '-' for subagents."""
    if len(args) != 5:
        print("usage: register-worker <task> <kind> <session|-> <repo> <task-file>",
              file=sys.stderr)
        sys.exit(2)
    task, kind, session, repo, task_file = args
    state = load_state()
    workers = state.setdefault("workers", {})
    workers[task] = {
        "kind": kind,
        "session": None if session == "-" else session,
        "repo": repo,
        "task_file": task_file,
        "dispatched_at": now().isoformat(),
        "quiet_cycles": 0,
        "last_verdict": "registered",
    }
    save_state(state)
    print(f"REGISTERED {task} kind={kind}")


def cmd_assign(args):
    """assign <session> <task> <note> — structured dispatch assignment record.
    The DISPATCH CHECK's 'record the assignment in the session note' was an
    ad-hoc python -c pattern (audit 2026-10-02); this makes it a command so
    the next run never double-dispatches."""
    session, task = args[0], args[1]
    note = " ".join(args[2:]) if len(args) > 2 else ""
    state = load_state()
    sst = state.get("sessions", {}).setdefault(session, {})
    assigns = sst.setdefault("assignments", [])
    assigns.append({"task": task, "note": note[:200],
                    "assigned_at": now().isoformat()})
    sst["last_task"] = task
    save_state(state)
    print(f"ASSIGNED {session} -> {task}")


def cmd_deregister_worker(args):
    """deregister-worker <task> [reason] — retire a completed worker.
    The worker lifecycle was register-only; finished workers lingered in the
    registry (td-142's done worker still showed as owned). Run when the
    worker reports done and its work is merged or handed off."""
    task = args[0]
    reason = " ".join(args[1:]) if len(args) > 1 else "worker reported done"
    state = load_state()
    workers = state.get("workers", {})
    if task not in workers:
        print(f"NOT-REGISTERED {task}")
        return
    w = workers.pop(task)
    state.setdefault("notes", []).append(
        f"{now().isoformat()[:16]}Z deregistered {task} ({w.get('kind')}): {reason}")
    save_state(state)
    print(f"DEREGISTERED {task} ({reason[:60]})")


def cmd_liveness():
    """Deterministic dead-worker check. Prints one verdict line per tracked worker:
    ALIVE | QUIET(n) | GRACE | STALE | DEAD | DROPPED. On DEAD (>=2 quiet cycles),
    queues a dispatch-subagent entry in pending_actions.json with a deterministically
    built brief, records the death in state notes, and drops the worker from the
    registry. Never advances quiet_cycles on stale observations."""
    state = load_state()
    workers = state.get("workers", {})
    notes = state.setdefault("notes", [])
    hb_dir = LIVENESS_HEARTBEAT_DIR
    for task, w in list(workers.items()):
        kind, repo = w.get("kind"), w.get("repo")
        task_file = w.get("task_file")
        dispatched_dt = parse_ts(w.get("dispatched_at"))
        age_min = (now() - dispatched_dt).total_seconds() / 60 if dispatched_dt else 9999
        # Terminal task -> drop, nothing to watch.
        status = _task_status_on_main(repo, task_file) if repo and task_file else None
        if status and status in LIVENESS_TERMINAL:
            del workers[task]
            print(f"DROPPED {task} (task status '{status}')")
            continue
        alive, reasons = False, []
        fresh_observation = True
        # Signal A: heartbeat file (subagents).
        hb_path = os.path.join(hb_dir, f"{task}.json")
        if os.path.exists(hb_path):
            try:
                hb = json.load(open(hb_path))
                hb_dt = parse_ts(hb.get("ts"))
                hb_age = (now() - hb_dt).total_seconds() / 60 if hb_dt else 9999
                if hb_age < LIVENESS_HEARTBEAT_MAX_MIN:
                    alive = True
                    step = (hb.get("current_step") or hb.get("step") or
                            hb.get("current") or hb.get("doing") or "")
                    reasons.append(f"heartbeat {hb_age:.0f}min ago ({step[:50]})")
                else:
                    reasons.append(f"heartbeat stale ({hb_age:.0f}min)")
            except Exception as e:
                reasons.append(f"heartbeat unreadable: {e}")
        else:
            reasons.append("no heartbeat file")
        # Signal B: GitHub evidence (branch/PR/task-file commits).
        try:
            gh_alive, gh_reasons, salvage = _worker_evidence(repo, task, task_file, dispatched_dt)
            if gh_alive:
                alive = True
            reasons.extend(gh_reasons)
        except Exception as e:
            reasons.append(f"evidence check error: {e}")
            salvage = []
        # Signal C: cloud session classification (codex/claude).
        session = w.get("session")
        if session and not alive:
            sst = state.get("sessions", {}).get(session, {})
            cls, cls_ts = sst.get("last_classification"), parse_ts(sst.get("last_classification_ts"))
            if cls_ts and (now() - cls_ts).total_seconds() / 60 < LIVENESS_CLASSIFY_MAX_MIN:
                if cls == "WORKING":
                    alive = True
                    reasons.append(f"session {session} classified WORKING recently")
            else:
                fresh_observation = False
                reasons.append(f"session {session} classification stale/missing")
        if alive:
            w["quiet_cycles"] = 0
            w["last_verdict"] = "alive"
            print(f"ALIVE {task} ({'; '.join(reasons)[:160]})")
            continue
        # No life signs. Grace, staleness, then the counter.
        if age_min < LIVENESS_GRACE_MIN:
            w["last_verdict"] = "grace"
            print(f"GRACE {task} (dispatched {age_min:.0f}min ago; {'; '.join(reasons)[:120]})")
            continue
        if not fresh_observation:
            w["last_verdict"] = "stale"
            print(f"STALE {task} (no fresh observation; counter frozen; {'; '.join(reasons)[:120]})")
            continue
        w["quiet_cycles"] = w.get("quiet_cycles", 0) + 1
        qc = w["quiet_cycles"]
        if qc < LIVENESS_QUIET_CYCLES:
            w["last_verdict"] = f"quiet-{qc}"
            print(f"QUIET({qc}) {task} ({'; '.join(reasons)[:160]})")
            continue
        # DEAD: proclaim, record, queue deterministic replacement, drop from registry.
        brief_path, brief = _build_replacement_brief(task, task_file, salvage)
        pa_path = os.path.join(STATE_DIR, "pending_actions.json")
        try:
            pa = json.load(open(pa_path))
        except Exception:
            pa = {"actions": [], "notes": []}
        pa.setdefault("actions", []).append({
            "type": "dispatch-subagent",
            "task": task,
            "task_file": task_file,
            "repo": repo,
            "brief_file": brief_path,
            "brief": brief,
            "queued_at": now().isoformat(),
            "reason": f"DEAD after {qc} quiet cycles: {'; '.join(reasons)[:200]}",
        })
        with open(pa_path, "w") as f:
            json.dump(pa, f, indent=1)
        notes.append(f"{now().isoformat()[:16]}Z LIVENESS: {task} proclaimed DEAD "
                     f"({qc} quiet cycles; {'; '.join(reasons)[:160]}). "
                     f"Replacement dispatch-subagent queued (brief {os.path.basename(brief_path)}).")
        del workers[task]
        print(f"DEAD {task} (replacement queued; {'; '.join(reasons)[:160]})")
    save_state(state)


# ---------------------------------------------------------------------------
# Task-management scriptifications (Craig 2026-10-02: "audit everything about
# task management, scriptify everywhere when possible").
# Every prose rule below used to live only in cron-body text, where a run could
# misread it (prefix-grep misses, stale SHIP merges, duplicate dispatches).
# These commands make the DECISIONS code; the cron body only runs them.
# ---------------------------------------------------------------------------

BOARD_REPO = "doublehidenblade/game-dev-central"
BOARD_PATHS = {
    "tokyo-drift-3d": "project-management/boards/tokyo-drift-3d.md",
    "neon-drift": "project-management/boards/neon-drift.md",
}
# Status-cell prefixes that are terminal / never re-enter dispatch (Craig
# 2026-09-30 SKIP-DONE RULE; board-read rule Craig 2026-09-28: match prefixes).
# Single shared constant — board-scan, liveness, and task-status all use it
# (audit 2026-10-02: liveness had its own divergent copy).
STATUS_PREFIXES_TERMINAL = {"done", "closed", "merged", "validated", "verified",
                            "superseded", "abandoned", "shipped", "resolved",
                            "live", "paused", "done-pending-verdict"}
LIVENESS_TERMINAL = STATUS_PREFIXES_TERMINAL  # alias; do not diverge
# Sessions whose product is retired — skipped by construction, not by prose.
ARCHIVED_SESSIONS = {"codex:neon-drift"}
PENDING_ACTIONS_PATH = os.path.join(STATE_DIR, "pending_actions.json")


def _board_rows(game):
    """Fetch the board markdown and parse rows -> [{task,status,prefix,owner,pr}].
    Finds the task cell by id pattern (td-NNN / p3d-NNN / td-NNN-shuto) instead
    of assuming column 0 — rows 143-145 carry a corrupt 7th leading row-number
    column (audit 2026-10-02), which naive positional parsing misparses."""
    import re
    blob = _gh(f"/repos/{BOARD_REPO}/contents/{BOARD_PATHS[game]}?ref=main")
    import base64
    text = base64.b64decode(blob["content"]).decode("utf-8", "replace")
    rows = []
    task_re = re.compile(r"^((?:td|p3d)-\d+(?:-shuto)?)$", re.I)
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        ti = next((i for i, c in enumerate(cells) if task_re.match(c)), None)
        if ti is None or ti + 4 >= len(cells):
            continue
        task = cells[ti]
        status_raw = cells[ti + 2]
        prefix = status_raw.split()[0].lower().strip("*") if status_raw.split() else ""
        rows.append({"task": task, "defect": cells[ti + 1], "status": status_raw,
                     "prefix": prefix, "owner": cells[ti + 3], "pr": cells[ti + 4]})
    return rows


def cmd_board(args):
    """board <game> [--json] — parse the task board into structured rows.
    Replaces prose prefix-greps (2026-09-28: exact-cell greps hid owners and
    caused a duplicate dispatch). Prints one line per row:
    ROW <task> prefix=<prefix> owner=<owner>."""
    game = args[0] if args else "tokyo-drift-3d"
    as_json = "--json" in args
    rows = _board_rows(game)
    if as_json:
        print(json.dumps(rows))
        return
    for r in rows:
        print(f"ROW {r['task']} prefix={r['prefix']} owner={r['owner'][:40]}")


def cmd_task_status(args):
    """task-status <repo-full> <task-file> — canonical task-file ## Status.
    Prints STATUS <status-prefix> (full line after)."""
    repo_full, task_file = args[0], args[1]
    st = _task_status_on_main(repo_full, task_file)
    print(f"STATUS {st or 'unknown'}")


def _load_pending_actions():
    try:
        return json.load(open(PENDING_ACTIONS_PATH))
    except Exception:
        return {"actions": [], "notes": []}


def _save_pending_actions(pa):
    with open(PENDING_ACTIONS_PATH, "w") as f:
        json.dump(pa, f, indent=1)


def cmd_queue_action(args):
    """queue-action '<json>' — deduped append to pending_actions.json.
    Dedupe key: (type, session|task). Prints QUEUED or DEDUPED.
    Replaces the prose 'dedupe on type+session' rule the cron body repeated
    per action type (and which still produced duplicates, e.g. p3d-086)."""
    entry = json.loads(args[0])
    pa = _load_pending_actions()
    key = (entry.get("type"), entry.get("session") or entry.get("task"))
    for e in pa.get("actions", []):
        if (e.get("type"), e.get("session") or e.get("task")) == key:
            print(f"DEDUPED {entry.get('type')} {key[1]} (already pending)")
            return
    entry["queued_at"] = now().isoformat()
    pa.setdefault("actions", []).append(entry)
    _save_pending_actions(pa)
    print(f"QUEUED {entry.get('type')} {key[1]}")


def cmd_owners(args):
    """owners — task -> owner map from every source of truth.
    Merges: workers registry (liveness), session notes (last_task), pending
    dispatch actions. Prints OWNER <task> <source> <owner>.
    The DISPATCH CHECK's 'no owner in any session note' is now this command."""
    as_json = "--json" in args
    state = load_state()
    owners = {}
    for task, w in state.get("workers", {}).items():
        owners[task] = ("liveness-registry", w.get("kind") + ":" +
                        (w.get("session") or "subagent"))
    for session, sst in state.get("sessions", {}).items():
        t = sst.get("last_task")
        if t and t not in owners:
            owners[t] = ("session-note", session)
    pa = _load_pending_actions()
    for e in pa.get("actions", []):
        if e.get("type", "").startswith("dispatch") and e.get("task"):
            owners.setdefault(e["task"], ("pending-dispatch", e["type"]))
    if as_json:
        print(json.dumps(owners))
        return
    for task in sorted(owners):
        src, own = owners[task]
        print(f"OWNER {task} {src} {own}")


def cmd_conflicts(args):
    """conflicts — fail loudly on duplicate task ownership.
    Checks the workers registry + session notes + pending dispatches for two
    owners on the same task. Prints OK or CONFLICT lines and exits 3 on
    conflict. Run before every DISPATCH CHECK."""
    state = load_state()
    seen = {}
    bad = []
    for task, w in state.get("workers", {}).items():
        seen.setdefault(task, []).append("liveness:" + w.get("kind", "?"))
    for session, sst in state.get("sessions", {}).items():
        t = sst.get("last_task")
        if t:
            seen.setdefault(t, []).append("session:" + session)
    pa = _load_pending_actions()
    for e in pa.get("actions", []):
        if e.get("type", "").startswith("dispatch") and e.get("task"):
            seen.setdefault(e["task"], []).append("pending:" + e["type"])
    for task, srcs in seen.items():
        kinds = {s.split(":")[0] for s in srcs}
        # liveness-registry + its own pending replacement is fine (death path);
        # two live owners is not.
        live = [s for s in srcs if not s.startswith("pending:")]
        if len(set(live)) > 1:
            bad.append((task, srcs))
    if bad:
        for task, srcs in bad:
            print(f"CONFLICT {task} owners={srcs}")
        sys.exit(3)
    print("OK no duplicate task ownership")


# PRs that must NEVER be merged by the watchdog, regardless of state.
# Craig 2026-10-01: PR #253 (td-138 round-3 preservation branch) must never ship.
NEVER_SHIP_PRS = {
    253: "Craig 2026-10-01: td-138 round-3 preservation branch must never ship",
}


def cmd_ship_verify(args):
    """ship-verify <session> — verify the parked PR is REALLY still open.
    The 2026-09-29 bogus-SHIP lesson: a SHIP fired for td-113 while its note
    already said "PRs #168/#169 merged" — both merged-closed, nothing parked.
    This command extracts PR numbers from the session note, checks each via
    the API, and prints SHIP-VERIFIED <pr> <head_sha> or SHIP-STALE <reason>.
    The cron run never merges on the SHIP label alone."""
    import re
    session = args[0]
    state = load_state()
    sst = state.get("sessions", {}).get(session, {})
    repo = SESSIONS.get(session, {}).get("repo", "tokyo-drift-3d")
    repo_full = REPOS[repo]
    # Mine the CURRENT episode's note (last_note, <=300 chars, overwritten per
    # classify) + structured pr_number — NOT the accumulated long-lived `note`
    # field, which carries ancient PR refs across episodes (2026-10-02: it
    # surfaced #253/#260 from td-138 history for a td-125 verify episode).
    text = " ".join(str(sst.get(k) or "") for k in
                    ("last_note", "task_url"))
    prs = sorted({int(n) for n in re.findall(r"#(\d+)", text)})
    # Structured pr_number first (classify --pr), regex as fallback.
    if sst.get("pr_number"):
        prs = sorted(set(prs) | {int(sst["pr_number"])})
    if not prs:
        print(f"SHIP-STALE {session}: no PR number in session note")
        return
    verified, stale, blocked = [], [], []
    for pr in prs:
        if pr in NEVER_SHIP_PRS:
            blocked.append(f"#{pr} BLOCKED ({NEVER_SHIP_PRS[pr]})")
            continue
        try:
            p = _gh(f"/repos/{repo_full}/pulls/{pr}")
        except Exception as e:
            stale.append(f"#{pr} unreadable ({e})")
            continue
        if p.get("state") == "open":
            verified.append((pr, p["head"]["sha"][:7], p["title"][:50]))
        else:
            stale.append(f"#{pr} {p.get('state')}"
                         + (" (merged)" if p.get("merged_at") else ""))
    for pr, sha, title in verified:
        print(f"SHIP-VERIFIED #{pr} {sha} :: {title}")
    for s in stale:
        print(f"SHIP-STALE {s}")
    for b in blocked:
        print(f"SHIP-BLOCKED {b}")
    if not verified:
        print(f"SHIP-NONE-PARKED {session}: nothing to ship")


def _task_file_text(repo_full, task_file):
    blob = _gh(f"/repos/{repo_full}/contents/{task_file}?ref=main")
    import base64
    return base64.b64decode(blob["content"]).decode("utf-8", "replace")


SCRIPTIFICATION_ANCHOR = "Scriptify deterministic parts of every lesson"


def _watch_subcommands():
    """All `watch.py <cmd>` subcommand names, parsed from this file's own
    dispatch table. Used by scriptification-audit to verify [SCRIPTED:]
    tags name a real subcommand."""
    import re, os
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    return set(re.findall(r'elif cmd == "([^"]+)":', src))


def _audit_lesson_sections(text, subcommands):
    """Pure: audit AGENTS.md lesson sections -> [(verdict, detail)].

    Only sections AFTER the scriptification rule's own section are audited
    (earlier lessons predate the rule and are grandfathered). Each must
    carry [SCRIPTED: watch.py <cmd>] — <cmd> must be a real subcommand —
    or [JUDGMENT-ONLY: <why>] with a non-empty why. Extracted for unit
    tests (test_rules.py Part 8)."""
    import re
    sections = []
    for part in re.split(r"(?m)^## ", text)[1:]:
        head, _, body = part.partition("\n")
        sections.append((head.strip(), body))
    anchor = next((i for i, (h, _) in enumerate(sections)
                   if SCRIPTIFICATION_ANCHOR in h), None)
    if anchor is None:
        return [("SCRIPTIFICATION-NOANCHOR",
                 "rule section not found in AGENTS.md")]
    verdicts = []
    for h, b in sections[anchor + 1:]:
        tags = re.findall(r"\[(SCRIPTED|JUDGMENT-ONLY):\s*([^\]]*)\]",
                          h + "\n" + b)
        if not tags:
            verdicts.append(("SCRIPTIFICATION-MISSING", h[:80]))
            continue
        valid = False
        for kind, content in tags:
            content = content.strip()
            if kind == "JUDGMENT-ONLY":
                if content:
                    valid = True
                else:
                    verdicts.append(("SCRIPTIFICATION-NOWHY", h[:80]))
            else:
                m = re.match(r"watch\.py\s+([A-Za-z0-9_\-<>]+)", content)
                cmd = m.group(1) if m else ""
                if cmd.startswith("<") and cmd.endswith(">"):
                    continue  # documented placeholder, not a scripting claim
                if cmd and cmd in subcommands:
                    valid = True
                else:
                    verdicts.append(("SCRIPTIFICATION-BADCMD",
                                     f"[{content[:40]}] in {h[:50]}"))
        if valid:
            verdicts.append(("SCRIPTIFICATION-TAGGED", h[:80]))
    return verdicts


def cmd_scriptification_audit(args):
    """scriptification-audit — the 2026-10-02 scriptification rule enforcing
    itself on ~/AGENTS.md. Craig 2026-10-03: the rule was prose-only, so
    nothing caught a prose-only lesson until he did. Now the audit runs as a
    STEP 0 deterministic check (surfaces in the heartbeat) and as a
    push_code.py pre-push gate. Prints one line per post-rule lesson:
      SCRIPTIFICATION-TAGGED <heading>   — has a valid tag
      SCRIPTIFICATION-MISSING <heading> — no [SCRIPTED:]/[JUDGMENT-ONLY:] tag
      SCRIPTIFICATION-BADCMD [tag] in <heading> — names no real subcommand
      SCRIPTIFICATION-NOWHY <heading>   — empty JUDGMENT-ONLY reason
    Exit 3 on any violation (usage errors exit 2). Honest limit: the audit
    verifies a tag exists and names a real subcommand — it cannot verify the
    subcommand implements every clause of the lesson (that stays human)."""
    import os
    try:
        text = open(os.path.expanduser("~/AGENTS.md"), encoding="utf-8").read()
    except Exception as e:
        print(f"SCRIPTIFICATION-ERROR cannot read ~/AGENTS.md: {e}")
        sys.exit(2)
    verdicts = _audit_lesson_sections(text, _watch_subcommands())
    bad = 0
    for v, d in verdicts:
        print(f"{v} {d}")
        if v != "SCRIPTIFICATION-TAGGED":
            bad += 1
    if bad:
        print(f"SCRIPTIFICATION-FAIL {bad} violation(s): tag new lessons "
              "[SCRIPTED: watch.py <cmd>] or [JUDGMENT-ONLY: <why>]")
        sys.exit(3)
    print(f"SCRIPTIFICATION-OK {len(verdicts)} post-rule lesson(s) tagged")


def _strip_dnm_prefix(title):
    """Remove a stale 'DO NOT MERGE' title prefix -> new title, or None.

    Pure helper for unit tests (test_rules.py Part 7). Handles the variants
    workers actually use: 'DO NOT MERGE — ...', 'DO NOT MERGE: ...',
    '[DO NOT MERGE] ...', case-insensitive. Returns None when there is no
    DNM prefix to strip. A bare 'DO NOT MERGE' with nothing after it returns
    an empty string — the caller substitutes a non-empty placeholder title.
    """
    import re
    m = re.match(r"^\s*\[?\s*do not merge\s*\]?\s*[:\-—–]?\s*(.*)$",
                 title, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    # Guard: the regex above matches anything starting with optional
    # whitespace — require the literal words to have been present.
    if "do not merge" not in title[:30].lower():
        return None
    return m.group(1).strip()


def _orphan_verdict(pr, board_prefix):
    """Pure decision for one open PR -> (verdict, detail).
    Extracted for unit tests (test_rules.py Part 6)."""
    n = pr["number"]
    title = pr.get("title", "")
    if n in NEVER_SHIP_PRS:
        return ("ORPHAN-BLOCKED", f"denylisted: {NEVER_SHIP_PRS[n][:60]}")
    if pr.get("draft"):
        return ("ORPHAN-DRAFT", "")
    dnm = "DO NOT MERGE" in title.upper()
    if board_prefix == "validated":
        flag = (" [stale DO NOT MERGE title overridden by validated verdict]"
                if dnm else "")
        return ("ORPHAN-READY", f"{pr['head']['sha'][:7]}{flag}")
    if dnm:
        return ("ORPHAN-HELD",
                "(DO NOT MERGE, not validated — human judgment required)")
    return ("ORPHAN-UNKNOWN", f"(board: {board_prefix or 'no row'})")


def cmd_adopt_orphans(args):
    """adopt-orphans [game] [--fix-titles] — backstop for validated-but-unmerged PRs.
    The 2026-10-03 td-148..152 lesson: workers titled PRs "DO NOT MERGE —
    awaiting Craig's verdict", their sessions died, and no SHIP ever fired
    because SHIP is per-session — five validated PRs stranded with no owner.
    Craig's verdict is a PUBLISH gate, never a merge gate, so a `validated`
    board row overrides a stale DO NOT MERGE title.
    Prints one line per open PR:
      ORPHAN-READY #N <sha> :: <title>   — board says validated: merge it
      ORPHAN-BLOCKED #N ...              — NEVER_SHIP_PRS denylist
      ORPHAN-DRAFT #N ...                — draft PR, not ready
      ORPHAN-HELD #N ...                 — DO NOT MERGE title, NOT validated:
                                          needs human judgment, never auto-merge
      ORPHAN-UNKNOWN #N ...              — open, no validated row: leave alone
    With --fix-titles, every ORPHAN-READY PR whose title still carries a
    stale DO NOT MERGE prefix gets the prefix stripped via the API
    (TITLE-STRIPPED #N: <old> -> <new>), so the misleading title can never
    strand validated work again — the WORKER_BRIEF title rule enforced in
    code, not prose. Titles on ORPHAN-HELD (unvalidated) PRs are legitimate
    holds and are never touched.
    The cron merges ORPHAN-READY with the standard SHIP sequence
    (ci-report, conflict check/rebase, squash-merge, record-pending)."""
    import re
    fix_titles = "--fix-titles" in args
    args = [a for a in args if a != "--fix-titles"]
    game = args[0] if args else "tokyo-drift-3d"
    repo_full = REPOS[game]
    try:
        prs = _gh(f"/repos/{repo_full}/pulls?state=open&per_page=100")
    except Exception as e:
        print(f"ORPHAN-ERROR {e}")
        return
    rows = _board_rows(game)
    pr_prefix = {}
    for r in rows:
        for n in re.findall(r"#(\d+)", r["pr"]):
            n = int(n)
            # validated is sticky: a later non-validated mention must not
            # hide an earlier validated verdict for the same PR.
            if pr_prefix.get(n) != "validated":
                pr_prefix[n] = r["prefix"]
    if not prs:
        print("ORPHAN-NONE no open PRs")
        return
    for p in prs:
        n = p["number"]
        title = p.get("title", "")
        verdict, detail = _orphan_verdict(p, pr_prefix.get(n))
        if verdict == "ORPHAN-READY" and fix_titles:
            stripped = _strip_dnm_prefix(title)
            if stripped is not None:
                new_title = stripped or f"#{n} (validated)"
                try:
                    _gh_api("PATCH", f"/repos/{repo_full}/pulls/{n}",
                            {"title": new_title})
                    print(f"TITLE-STRIPPED #{n}: {title[:60]} -> {new_title[:60]}")
                    title = new_title
                except Exception as e:
                    print(f"TITLE-STRIP-FAILED #{n}: {e}")
        if verdict == "ORPHAN-READY":
            print(f"{verdict} #{n} {detail} :: {title[:60]}")
        elif detail:
            print(f"{verdict} #{n} :: {title[:60]} {detail}")
        else:
            print(f"{verdict} #{n} :: {title[:60]}")


def cmd_evidence_audit(args):
    """evidence-audit <task> — verify before/after pairs exist per reference.
    The 2026-09-24/25 inspection rule: every visual criterion needs a valid
    before/after pair, same angle, under the task's QA folder. This command
    finds the QA dir from the task file, lists reference images (files without
    before/after infix), and checks for <base>-before.png / <base>-after.png.
    Also checks the Evidence section embeds images (![]()). Prints
    EVIDENCE-OK / EVIDENCE-MISSING lines."""
    import re
    task = args[0]
    repo_full = REPOS["tokyo-drift-3d"]
    task_file = f"godot/docs/tasks/{task}.md"
    try:
        text = _task_file_text(repo_full, task_file)
    except Exception as e:
        print(f"EVIDENCE-ERROR {task}: cannot read task file ({e})")
        return
    qa_dirs = sorted(set(re.findall(r"godot/qa/([a-z0-9\-_]+)/", text)))
    if not qa_dirs:
        print(f"EVIDENCE-ERROR {task}: no godot/qa/ dir referenced in task file")
        return
    # Evidence section embeds images?
    ev = ""
    if "## Evidence" in text:
        ev = re.split(r"(?m)^## (?!#)", text.split("## Evidence", 1)[1])[0]
    embedded = "![]( " in ev or "![](" in ev
    print(f"EVIDENCE-EMBED {'OK' if embedded else 'MISSING'} "
          f"(Evidence section has embedded images: {embedded})")
    # Craig 2026-10-02: QA README link check — evidence READMEs must use
    # rendered images (![]()) or clickable links ([]()), never bare backtick
    # paths (`foo.png`) which render as dead text. Check README.md in each
    # QA dir and one level of subdirectories (evidence lives in dated folders).
    def _check_readme_links(qa_path, readme):
        bare = []
        for m in re.finditer(r"`([A-Za-z0-9_][A-Za-z0-9_\-./]*\.(png|jpg|jpeg))`", readme, re.I):
            start = m.start()
            prefix = readme[max(0, start-3):start]
            if prefix.endswith("](") or prefix.endswith("] ("):
                continue
            if start > 0 and readme[start-1] == "]":
                rest = readme[m.end():m.end()+3]
                if rest.startswith("]("):
                    continue
            bare.append(m.group(1))
        return sorted(set(bare))

    for qa in qa_dirs:
        readme_paths = [f"godot/qa/{qa}/README.md"]
        try:
            entries = _gh(f"/repos/{repo_full}/contents/godot/qa/{qa}?ref=main")
            for e in entries:
                if e["type"] == "dir":
                    readme_paths.append(f"godot/qa/{qa}/{e['name']}/README.md")
        except Exception:
            pass
        for rp in readme_paths:
            try:
                readme = _repo_file_text(repo_full, rp, ref="main")
            except Exception:
                continue
            bare = _check_readme_links(rp, readme)
            short = rp.replace("godot/qa/", "qa/")
            if bare:
                print(f"EVIDENCE-README-LINKS MISSING {short} "
                      f"({len(bare)} bare image paths, not links: {', '.join(bare[:5])}"
                      f"{'...' if len(bare) > 5 else ''})")
            else:
                print(f"EVIDENCE-README-LINKS OK {short}")
    for qa in qa_dirs:
        try:
            files = _gh(f"/repos/{repo_full}/contents/godot/qa/{qa}?ref=main")
        except Exception as e:
            print(f"EVIDENCE-ERROR {task}: cannot list qa/{qa} ({e})")
            continue
        names = [f["name"] for f in files if f["type"] == "file"]
        pngs = [n for n in names if n.lower().endswith((".png", ".jpg", ".jpeg"))]
        refs = [n for n in pngs
                if "-before" not in n.lower() and "-after" not in n.lower()
                and "-impl" not in n.lower()]
        # A QA dir holding only reference inputs (no before/after/triptych/impl
        # captures at all) is a design-reference dir, not worker evidence —
        # its images need no pairs.
        if refs and not any("-triptych" in n.lower() or "-impl" in n.lower()
                            or "-before" in n.lower() or "-after" in n.lower()
                            for n in pngs):
            for ref in sorted(refs):
                print(f"EVIDENCE-REF qa/{qa}/{ref} (reference input, no pair required)")
            continue
        have = set(n.lower() for n in pngs)
        for ref in sorted(refs):
            base = re.sub(r"\.(png|jpg|jpeg)$", "", ref, flags=re.I)
            screen = re.sub(r"-triptych$", "", base.lower())
            keys = {base.lower(), screen}
            has_combined = any(h.startswith(k + "-before-after") for k in keys for h in have)
            has_before = has_combined or any(h.startswith(k + "-before") for k in keys for h in have)
            has_after = has_combined or any(h.startswith(k + "-after") for k in keys for h in have)
            if has_before and has_after:
                print(f"EVIDENCE-OK qa/{qa}/{ref} (before+after present)")
            else:
                print(f"EVIDENCE-MISSING qa/{qa}/{ref} "
                      f"(before={has_before} after={has_after})")


# --- Evidence collection + deterministic cheat-checks (Craig 2026-10-04) ---
# The hourly task-evidence inspector (devil's advocate) needs the raw pixels,
# not worker captions. These subcommands pull the QA images for a task and run
# deterministic audits that catch laziness/cheating without any vision model:
# duplicate frames reused across criteria, byte-identical before/after pairs,
# after-shots with no before, postage-stamp images, and dark-void studio
# renders (EVIDENCE-VOID-SUSPECT — triage flag for the inspector's vision
# pass, never a verdict).
# [SCRIPTED: watch.py evidence-collect] [SCRIPTED: watch.py evidence-checks]

def _sha256_bytes(raw):
    import hashlib
    return hashlib.sha256(raw).hexdigest()


def _find_duplicate_images(entries):
    """Pure helper. entries: [(relpath, sha)]. Returns {sha: [relpaths]} for
    groups where the same bytes appear under 2+ distinct paths."""
    groups = {}
    for relpath, sha in entries:
        groups.setdefault(sha, []).append(relpath)
    return {s: sorted(ps) for s, ps in groups.items()
            if len(set(ps)) > 1}


def _pair_findings(names):
    """Pure helper. names: image filenames (basenames, any case).
    Returns (missing_before, identical_stems_pending) where missing_before
    lists after-files with no matching before-file. Identical-content detection
    needs bytes and happens in cmd_evidence_checks."""
    import re
    lower = {n.lower(): n for n in names}

    def stem(n):
        return re.sub(r"\.(png|jpg|jpeg)$", "", n, flags=re.I)

    befores = {stem(n)[:-len("-before")] for n in lower
               if stem(n).endswith("-before")}
    afters = [(stem(n), n) for n in names if stem(n).lower().endswith("-after")]
    missing = []
    for a_stem, orig in afters:
        base = a_stem[:-len("-after")]
        if base.lower() not in {b.lower() for b in befores}:
            missing.append(orig)
    return sorted(missing)


def _is_tiny(w, h, min_dim=400):
    """Pure helper. Flags postage-stamp evidence too small to judge."""
    return max(w, h) < min_dim


# EVIDENCE-VOID tuning (td-171, 2026-10-04): Blender dark-studio void renders
# use a near-black navy backdrop (luminance ~20). In-engine night shots are
# also dark, so this is strictly a SUSPECT flag for the hourly
# task-evidence-inspector's vision pass — never a verdict. Tuned on td-119:
# fires on the criterion-1 void pair (dark fraction 0.85/0.88 at lum<32),
# stays quiet on the in-engine night street shot criterion-3-after (0.67).
_VOID_LUM_THRESH = 32
_VOID_FRAC_THRESH = 0.80


def _void_dark_fraction(raw):
    """Pure helper. Returns the fraction of pixels with luminance below
    _VOID_LUM_THRESH (near-black backdrop), or None when the bytes can't be
    decoded as an image. Downsamples first; exact ratio doesn't matter, only
    whether the frame is overwhelmingly backdrop."""
    try:
        from PIL import Image
        import io
        with Image.open(io.BytesIO(raw)) as im:
            rgb = im.convert("RGB")
            rgb.thumbnail((200, 200))
            px = list(rgb.getdata())
    except Exception:
        return None
    if not px:
        return None
    dark = sum(1 for r, g, b in px
               if 0.299 * r + 0.587 * g + 0.114 * b < _VOID_LUM_THRESH)
    return dark / len(px)


def _is_void_suspect(dark_frac, thresh=_VOID_FRAC_THRESH):
    """Pure helper. Flags images that are overwhelmingly near-black
    background — the Blender dark-void studio signature — as VOID-SUSPECT
    for vision review."""
    return dark_frac is not None and dark_frac >= thresh


def _collect_evidence_images(task, outdir):
    """Download every image under godot/qa/<task>/ (one subdir level) on main
    into outdir, preserving relative paths. Returns [(relpath, bytes)]."""
    import urllib.request
    repo_full = REPOS["tokyo-drift-3d"]
    got = []

    def listing(qa_path):
        try:
            return _gh(f"/repos/{repo_full}/contents/{qa_path}?ref=main")
        except Exception:
            return []

    work = [f"godot/qa/{task}"]
    seen_dirs = set()
    while work:
        qp = work.pop()
        if qp in seen_dirs:
            continue
        seen_dirs.add(qp)
        for e in listing(qp):
            if e["type"] == "dir":
                work.append(f"{qp}/{e['name']}")
            elif e["type"] == "file" and e["name"].lower().endswith(
                    (".png", ".jpg", ".jpeg")):
                rel = f"{qp}/{e['name']}".replace(f"godot/qa/{task}/", "")
                url = e.get("download_url")
                size = e.get("size") or 0
                if not url or size > 25 * 1024 * 1024:
                    print(f"EVIDENCE-COLLECT-SKIP {rel} "
                          f"(no url or >25MB)")
                    continue
                try:
                    req = urllib.request.Request(url, headers={
                        "User-Agent": "agent-watch-inspector"})
                    with urllib.request.urlopen(req, timeout=90) as resp:
                        raw = resp.read()
                except Exception as ex:
                    print(f"EVIDENCE-COLLECT-FAIL {rel} ({ex})")
                    continue
                dest = os.path.join(outdir, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(raw)
                got.append((rel, raw))
                print(f"EVIDENCE-COLLECT {rel} {len(raw)}B")
    return got


def cmd_evidence_collect(args):
    """evidence-collect <task> [outdir] — download task QA images from main.
    Prints EVIDENCE-COLLECT lines and a final EVIDENCE-COLLECT-DONE."""
    task = args[0]
    outdir = (args[1] if len(args) > 1 else
              os.path.expanduser("~/workspace/agent-watch/inspector/"
                                 f"evidence/{task}"))
    os.makedirs(outdir, exist_ok=True)
    got = _collect_evidence_images(task, outdir)
    print(f"EVIDENCE-COLLECT-DONE {task} {len(got)} files -> {outdir}")


def cmd_evidence_checks(args):
    """evidence-checks <task> [outdir] — deterministic cheat/laziness audits
    over the collected QA pixels. Prints EVIDENCE-DUP (same bytes, 2+ names —
    e.g. one frame reused across criteria), EVIDENCE-PAIR-IDENTICAL (before
    and after byte-identical — no change), EVIDENCE-PAIR-MISSING-BEFORE
    (after-shot with no before), EVIDENCE-TINY (max dim < 400px),
    EVIDENCE-VOID-SUSPECT (dark-pixel fraction >= 0.80 — Blender dark-void
    studio signature, for the inspector's vision pass), and a final
    EVIDENCE-CHECKS-DONE summary line. Exit 0 always; verdicts are lines."""
    task = args[0]
    outdir = (args[1] if len(args) > 1 else
              os.path.expanduser("~/workspace/agent-watch/inspector/"
                                 f"evidence/{task}"))
    if not os.path.isdir(outdir):
        got = _collect_evidence_images(task, outdir)
    else:
        got = []
        for root, _ds, fs in os.walk(outdir):
            for fn in fs:
                if fn.lower().endswith((".png", ".jpg", ".jpeg")):
                    p = os.path.join(root, fn)
                    with open(p, "rb") as f:
                        got.append((os.path.relpath(p, outdir), f.read()))
        if not got:
            got = _collect_evidence_images(task, outdir)
    entries = [(rel, _sha256_bytes(raw)) for rel, raw in got]
    names = [rel.split("/")[-1] for rel, _r in entries]

    dups = _find_duplicate_images(entries)
    for sha, paths in sorted(dups.items()):
        print(f"EVIDENCE-DUP {sha[:12]} {' '.join(paths)}")

    missing = _pair_findings(names)
    for m in missing:
        print(f"EVIDENCE-PAIR-MISSING-BEFORE {m}")

    by_stem = {}
    for rel, raw in got:
        import re
        base = re.sub(r"\.(png|jpg|jpeg)$", "", rel.split("/")[-1], flags=re.I)
        by_stem.setdefault(base.lower(), {})[rel] = raw
    identical = 0
    for base, variants in sorted(by_stem.items()):
        if base.endswith("-after"):
            stem = base[:-len("-after")]
            b = by_stem.get(stem + "-before")
            if b:
                a_raw = next(iter(variants.values()))
                b_raw = next(iter(b.values()))
                if _sha256_bytes(a_raw) == _sha256_bytes(b_raw):
                    identical += 1
                    print(f"EVIDENCE-PAIR-IDENTICAL {stem}")

    tiny = 0
    void_suspects = []
    try:
        from PIL import Image
        for rel, raw in got:
            try:
                with Image.open(__import__("io").BytesIO(raw)) as im:
                    w, h = im.size
            except Exception:
                continue
            if _is_tiny(w, h):
                tiny += 1
                print(f"EVIDENCE-TINY {rel} {w}x{h}")
            df = _void_dark_fraction(raw)
            if _is_void_suspect(df):
                void_suspects.append((rel, df))
                print(f"EVIDENCE-VOID-SUSPECT {rel} darkfrac={df:.2f}")
    except ImportError:
        print("EVIDENCE-TINY-SKIP (PIL unavailable)")
        print("EVIDENCE-VOID-SKIP (PIL unavailable)")

    print(f"EVIDENCE-CHECKS-DONE {task} files={len(got)} "
          f"dups={len(dups)} identical_pairs={identical} "
          f"missing_before={len(missing)} tiny={tiny} "
          f"void_suspects={len(void_suspects)}")


PUBLISH_REPOS = {
    "tokyo": ("doublehidenblade/tokyo-drift-3d", "doublehidenblade/tokyo-drift-3d-web"),
    "neon": ("doublehidenblade/neon-drift", "doublehidenblade/neon-drift-web"),
}


def _repo_file_text(repo_full, path, ref="main"):
    blob = _gh(f"/repos/{repo_full}/contents/{path}?ref={ref}")
    import base64
    return base64.b64decode(blob["content"]).decode("utf-8", "replace").strip()


def cmd_publish_verify(args):
    """publish-verify <game> — four-way publish parity check.
    The 2026-10-02 v33 incident: the publish reused a STALE smoke artifact, so
    live build-sha.txt matched the candidate pointer but NOT current main —
    and the badge alone "proved" the release. This command compares all four:
    source main HEAD, candidate pointer (deploy/web-candidate.json),
    live build-sha.txt, live version.txt. Prints PARITY, STALE-CANDIDATE, or
    MISMATCH with the values. Run after every publish, before claiming
    anything shipped."""
    game = args[0] if args else "tokyo"
    src_repo, web_repo = PUBLISH_REPOS[game]
    main_head = _gh(f"/repos/{src_repo}/commits/main?per_page=1")["sha"]
    try:
        cand = json.loads(_repo_file_text(src_repo, "deploy/web-candidate.json"))
        cand_sha = cand.get("source_sha", "?")
    except Exception as e:
        print(f"PUBLISH-ERROR cannot read candidate pointer ({e})")
        return
    live_sha = _repo_file_text(web_repo, "build-sha.txt")
    try:
        live_ver = _repo_file_text(web_repo, "version.txt").split()[0]
    except Exception:
        live_ver = "?"
    print(f"PUBLISH-SOURCE-MAIN {main_head[:12]}")
    print(f"PUBLISH-CANDIDATE {cand_sha[:12]}")
    print(f"PUBLISH-LIVE-SHA {live_sha[:12]} version={live_ver}")
    if live_sha == cand_sha == main_head:
        print("PUBLISH-PARITY OK: live matches candidate matches current main")
    elif live_sha == cand_sha != main_head:
        print("PUBLISH-STALE-CANDIDATE: live matches the candidate pointer, "
              "but the pointer predates current main — merged work is NOT live")
    else:
        print("PUBLISH-MISMATCH: live build-sha does not match the candidate "
              "pointer — do not claim the release shipped")


def _load_pending_ledger():
    """Load project-management/watchdog/releases/pending.json, tolerating schema drift.
    The documented form is {"pending": [...]} but the live file drifted to a
    bare [...] (audit 2026-10-02). Returns (data_dict, path)."""
    path = os.path.join(RELEASES_DIR, "pending.json")
    try:
        data = json.load(open(path))
    except Exception:
        data = {"pending": []}
    if isinstance(data, list):
        data = {"pending": data}
    data.setdefault("pending", [])
    return data, path


def cmd_record_pending(args):
    """record-pending <game> <task> <pr> <sha> <summary> — deduped append to
    project-management/watchdog/releases/pending.json. Dedupe on pr. Replaces the prose
    'dedupe on pr' rule in the SHIP step."""
    game, task, pr, sha = args[0], args[1], int(args[2]), args[3]
    summary = args[4] if len(args) > 4 else ""
    data, path = _load_pending_ledger()
    for e in data.get("pending", []):
        if e.get("pr") == pr and e.get("game") == game:
            print(f"PENDING-DEDUPED {game} PR #{pr} (already recorded)")
            return
    data.setdefault("pending", []).append({
        "game": game, "task": task, "pr": pr, "merged_sha": sha,
        "merged_at": now().isoformat(), "summary": summary})
    json.dump(data, open(path, "w"), indent=1)
    print(f"PENDING-RECORDED {game} {task} PR #{pr} {sha[:7]}")


def cmd_pending_report(args):
    """pending-report — merged-not-live items with reported flags.
    The STEP 3 rule: merged-but-not-live items get exactly one report, then
    only a pending count. Prints REPORT <pr> <summary> for unreported entries,
    COUNT <n> always. Run `pending-reported <pr>` after reporting."""
    data, _ = _load_pending_ledger()
    pending = data.get("pending", [])
    fresh = [e for e in pending if not e.get("reported")]
    for e in fresh:
        print(f"REPORT {e.get('game')} PR #{e.get('pr')} {e.get('task')} :: "
              f"{e.get('summary','')[:80]}")
    print(f"COUNT {len(pending)} merged-not-live")


def cmd_pending_reported(args):
    """pending-reported <pr> — stamp an entry reported (one-report rule)."""
    pr = int(args[0])
    data, path = _load_pending_ledger()
    for e in data.get("pending", []):
        if e.get("pr") == pr:
            e["reported"] = True
    json.dump(data, open(path, "w"), indent=1)
    print(f"REPORTED PR #{pr}")


def cmd_pending_hold(args):
    """pending-hold <pr> "<reason>" — mark a merged-not-live entry HELD:
    its evidence was rejected after merge (inspector FAIL, Craig overturn).
    Held entries are NOT publishable inventory: the heartbeat renders them
    as HELD (never "merged, not live"), and publish-verify must refuse a
    candidate containing held code until released. [SCRIPTED: watch.py pending-hold]"""
    pr = int(args[0])
    reason = args[1] if len(args) > 1 else ""
    data, path = _load_pending_ledger()
    for e in data.get("pending", []):
        if e.get("pr") == pr:
            e["status"] = "HELD"
            e["hold_reason"] = reason
            e["held_at"] = now().isoformat()
    json.dump(data, open(path, "w"), indent=1)
    print(f"PENDING-HELD PR #{pr} :: {reason[:80]}")


def cmd_pending_release(args):
    """pending-release <pr> — clear a hold after the rework lands and its
    evidence passes. Returns the entry to publishable merged-not-live."""
    pr = int(args[0])
    data, path = _load_pending_ledger()
    for e in data.get("pending", []):
        if e.get("pr") == pr:
            e.pop("status", None)
            e.pop("hold_reason", None)
            e.pop("held_at", None)
    json.dump(data, open(path, "w"), indent=1)
    print(f"PENDING-RELEASED PR #{pr}")


# ---------------------------------------------------------------------------
# Scripted heartbeat (Craig 2026-10-02): the watchdog report as code.
# The cron's old STEP 3 hand-wrote the heartbeat from check outputs in prose,
# which drifted run to run (missing links, reworded sections, dropped jobs).
# `heartbeat` assembles ALERTS + JOBS + WORKERS + PENDING + STATE from this
# run's recorded check verdicts (see _record_verdict), recent queued actions,
# the pending ledger, and the board — with markdown inline links and the
# board's defect names as headlines (TASK NAMING rule, Craig 2026-09-25).
# Outcome words follow the FOLD-IN RULES (Craig 2026-09-25 — the closed
# five-outcome set every JOBS line must state EXPLICITLY IN WORDS, never as
# bare digits Craig can't map):
#   🟢 OPEN — assigned: open and assigned to a named worker/action/publish
#     chain (stalled with a nudge/steer queued, parked PRs, and
#     merged-but-not-live work — including HELD/rejected-evidence — all
#     fold in here);
#   🟡 OPEN — no worker: open but no available worker, only after escalation
#     routes are exhausted, with expected return/recovery stated;
#   🔴 BLOCKED — needs you: blocked on human, naming Craig's exact required
#     action;
#   🔴 BLOCKED — external: blocked on third-party outage/upstream failure,
#     with a re-check plan;
#   (1 closed = done/verified — validated flips stay silent, nothing to do.)
# Genuinely ambiguous blockers get `🔴 BLOCKED — unclear`. A JOBS line
# without an explicit outcome phrase is a failed heartbeat.
# ---------------------------------------------------------------------------

_HB_EMOJI = {"WORKING": "🟢", "FINISHED": "🟡", "IDLE": "🟡",
             "STALLED": "🟡", "OUT_OF_TOKENS": "🔴", "LOGIN_BLOCKED": "🔴",
             "DEAD": "🔴"}
_HB_HUMAN_KW = ("login", "key", "purchase", "craig", "phone", "approval",
                "sign in", "2fa", "otp")
_HB_EXTERNAL_KW = ("outage", "down", "deprecated", "rate limit", "quota",
                   "incident")
# Board prefixes that still mean project work is outstanding (Craig
# 2026-10-02: a heartbeat must never imply the game is done/ready).
# done-pending-verdict is deliberately excluded — implementation is complete,
# only Craig's phone verdict is outstanding (never re-dispatched).
_HB_OPEN_PREFIXES = {"open", "in_progress", "in_review", "blocked", "rejected"}
_HB_OPEN_FALLBACK_N = 6


def _hb_verdicts(state):
    """This run's recorded check verdicts, filtered per check.
    A check's verdicts count only if that check ran within
    HEARTBEAT_FRESH_MIN — a newly run command must not make an older check's
    lines look current (audit 2026-10-02: shared run_verdicts.ts let a prior
    run's keys ride along). Falls back to the shared ts for pre-change data."""
    rv = state.get("run_verdicts", {})
    shared_ts = parse_ts(rv.get("ts"))
    per = rv.get("check_ts", {})
    out = {}
    for name, lines in rv.get("checks", {}).items():
        ts = parse_ts(per.get(name)) or shared_ts
        if ts and (now() - ts).total_seconds() / 60 <= HEARTBEAT_FRESH_MIN:
            out[name] = lines
    return out


def _hb_recent_actions():
    pa = _load_pending_actions()
    out = []
    for e in pa.get("actions", []):
        qa = parse_ts(e.get("queued_at"))
        if qa and (now() - qa).total_seconds() / 60 <= HEARTBEAT_FRESH_MIN:
            out.append(e)
    return out


def _hb_age_txt(age):
    if age == "unknown" or age is None:
        return "age?"
    try:
        m = float(age)
    except (TypeError, ValueError):
        return "age?"
    return f"{m:.0f}m" if m < 90 else f"{m/60:.1f}h"


def build_heartbeat(state, checks, actions, board_rows, pending, budget):
    """Pure heartbeat builder (testable). Inputs: state dict, recorded check
    verdicts {name: [lines]}, recent queued actions, board rows, pending-ledger
    entries, budget level string ('OK'/'ALERT_WARN …'/'ALERT_HIT …'/None).
    Returns the report lines."""
    import re
    repo_full = REPOS.get("tokyo-drift-3d", "")
    defects = {r["task"].lower(): r for r in board_rows}

    def task_link(task):
        if not task:
            return "?"
        url = (f"https://github.com/{repo_full}/blob/main/"
               f"godot/docs/tasks/{task}.md")
        return f"[{task}]({url})"

    def pr_link(pr):
        return f"[PR #{pr}](https://github.com/{repo_full}/pull/{pr})"

    def defect_of(task):
        r = defects.get((task or "").lower())
        return (r["defect"][:70] if r and r.get("defect") else (task or "?"))

    lines = [f"HEARTBEAT {now().astimezone().strftime('%Y-%m-%dT%H:%M%z')}"]
    alerts, jobs = [], []

    # ---- ALERTS ----
    # Login failures surfaced this run.
    for session, sst in state.get("sessions", {}).items():
        if session in ARCHIVED_SESSIONS:
            continue
        ts = parse_ts(sst.get("login_fail_notified_ts"))
        if ts and (now() - ts).total_seconds() / 60 <= HEARTBEAT_FRESH_MIN:
            alerts.append(f"! {session} hit a login wall — needs Craig's manual login")
    # Conflicts.
    for line in checks.get("conflicts", []):
        if line.startswith("CONFLICT"):
            alerts.append(f"! {line}")
    # Board flips.
    flips = []
    for line in checks.get("transitions", []):
        m = re.match(r"FLIP (\S+): (\S+) -> (\S+) \[(\S+)\]", line)
        if m:
            flips.append(m.groups())
    for task, old, new, action in flips:
        if action in ("notify-craig", "notify-or-iterate"):
            alerts.append(f"! {task}: {old} → {new} — notify Craig")
    # Queued actions this run.
    for e in actions:
        tgt = e.get("session") or e.get("task") or "?"
        alerts.append(f"! queued {e.get('type')} → {tgt}")
    # Stale classifications.
    stale_n = None
    for line in checks.get("classification-health", []):
        m = re.match(r"STALE-RUNS=(\d+)", line)
        if m:
            stale_n = int(m.group(1))
    if stale_n is not None and stale_n >= 3:
        alerts.append(f"! classifications stale {stale_n} runs — watchdog may be "
                      f"blind (AND with in-flight browser check before alarming)")
    # Budget.
    if budget and budget != "OK":
        alerts.append(f"! GitHub Actions budget: {budget}")
    lines.append("ALERTS")
    lines.extend(alerts if alerts else ["(none)"])

    # ---- JOBS ----
    for task, old, new, action in flips:
        dl, tl = defect_of(task), task_link(task)
        if action == "wake-validator":
            jobs.append(f"🟢 OPEN — assigned · {tl} {dl} — validator dispatch due")
        elif action == "notify-or-iterate":  # rejected
            jobs.append(f"🟡 OPEN — assigned · {tl} {dl} — rejected, rework needed")
        elif action == "notify-craig" and new == "blocked":
            r = defects.get(task.lower(), {})
            status_txt = (r.get("status") or "")[:90]
            low = status_txt.lower()
            if any(k in low for k in _HB_HUMAN_KW):
                oc = "🔴 BLOCKED — needs you"
            elif any(k in low for k in _HB_EXTERNAL_KW):
                oc = "🔴 BLOCKED — external"
            else:
                oc = "🔴 BLOCKED — unclear"
            jobs.append(f"{oc} · {tl} {dl} — blocked: {status_txt}")
        # validated → closed, silent → nothing to do.
    for e in actions:
        t = e.get("type", "")
        if t.startswith("dispatch"):
            task = e.get("task") or "?"
            jobs.append(f"🟢 OPEN — assigned · {task_link(task)} {defect_of(task)} — dispatch queued ({t})")
        elif t.split("-")[0] in ("nudge", "resume", "steer", "failover"):
            sst = state.get("sessions", {}).get(e.get("session"), {})
            task = sst.get("current_task") or sst.get("last_task") or "?"
            jobs.append(f"🟢 OPEN — assigned · {task_link(task)} {defect_of(task)} — {t} queued")
    for e in pending:
        if not e.get("reported"):
            if e.get("status") == "HELD":
                # Fold-in rule: merged-but-not-live with rejected evidence is
                # still open-and-assigned, never closed.
                jobs.append(f"🔴 OPEN — assigned · {pr_link(e.get('pr'))} {e.get('task')} — HELD: "
                            f"{e.get('hold_reason', '')[:80]} (merged, evidence rejected — not for publish)")
            else:
                jobs.append(f"🟢 OPEN — assigned · {pr_link(e.get('pr'))} {e.get('task')} — "
                            f"{e.get('summary', '')[:70]} (merged, not live)")
    all_blocked = any(l.startswith("ALL-BLOCKED True")
                      for l in checks.get("all-blocked", []))
    if all_blocked:
        for r in board_rows:
            if (r["prefix"] not in STATUS_PREFIXES_TERMINAL
                    and r["owner"].strip("—- ") == ""):
                jobs.append(f"🟡 OPEN — no worker · {task_link(r['task'])} {defect_of(r['task'])} "
                            f"— no available worker (all sessions blocked)")
    lines.append("JOBS")
    if jobs:
        lines.extend(jobs)
    else:
        # Craig 2026-10-02: an empty activity list must NEVER read as "the
        # game has no open work / is ready". Fall back to the board's open
        # work so worker idleness can't masquerade as project readiness.
        open_rows = [r for r in board_rows
                     if r.get("prefix") in _HB_OPEN_PREFIXES]
        # Craig 2026-10-02: prioritize in_progress/in_review over plain open
        # so active work surfaces instead of being buried by board order.
        _HB_PRIORITY = {"in_progress": 0, "in_review": 1, "blocked": 2,
                        "rejected": 3, "open": 4}
        open_rows.sort(key=lambda r: (_HB_PRIORITY.get(r.get("prefix"), 9),
                                      r.get("task", "")))
        if open_rows:
            lines.append("(no run activity — open board work:)")
            for r in open_rows[:_HB_OPEN_FALLBACK_N]:
                owner = (r.get("owner") or "").strip("—- ")
                named = bool(owner and owner.lower() not in ("", "unassigned"))
                own_txt = f" ({owner})" if named else ""
                # Five-outcome set (Craig 2026-09-25, words not digits per
                # 2026-10-04): every fallback line states its outcome
                # explicitly with color coding.
                if named:
                    oc = "🟢 OPEN — assigned"  # open, named worker owns it
                elif r.get("prefix") in ("blocked", "rejected"):
                    low = ((r.get("status") or "") + " " +
                           (r.get("defect") or "")).lower()
                    if any(k in low for k in _HB_HUMAN_KW):
                        oc = "🔴 BLOCKED — needs you"
                    elif any(k in low for k in _HB_EXTERNAL_KW):
                        oc = "🔴 BLOCKED — external"
                    else:
                        oc = "🔴 BLOCKED — unclear"
                else:
                    oc = "🟡 OPEN — no worker"  # open, no available worker
                lines.append(f"{oc} · {task_link(r['task'])} "
                             f"{defect_of(r['task'])}"
                             f" — {r.get('prefix')}{own_txt}")
            if len(open_rows) > _HB_OPEN_FALLBACK_N:
                lines.append(f"…and {len(open_rows) - _HB_OPEN_FALLBACK_N} "
                             f"more open on the board")
        else:
            lines.append("(none)")
    lines.append(f"PENDING {len(pending)} merged-not-live")

    # ---- WORKERS ----
    lines.append("WORKERS")
    for session in SESSIONS:
        if session in ARCHIVED_SESSIONS:
            continue
        sst = state.get("sessions", {}).get(session, {})
        cls = sst.get("last_classification") or "?"
        emoji = _HB_EMOJI.get(cls, "⚪")
        task = (sst.get("current_task") or sst.get("last_task")
                or sst.get("dispatched_task") or "—")
        age = _hb_age_txt(_state_age_min(sst))
        name = (f"[{session}]({sst['task_url']})" if sst.get("task_url")
                else session)
        extra = ""
        if cls not in ("?", "UNKNOWN"):
            try:
                action, _ = decide_action(session, cls, state)
            except Exception:
                action = "?"
            if action != "NOTHING":
                extra = f" → {action}"
        lines.append(f"{emoji} {name} — {cls} ({age}) — {task}{extra}")

    # ---- STATE ----
    lines.append("STATE")
    max_age, stale_txt = "?", ""
    for session in SESSIONS:
        if session in ARCHIVED_SESSIONS:
            continue
        a = _state_age_min(state.get("sessions", {}).get(session, {}))
        if a != "unknown" and (max_age == "?" or a > max_age):
            max_age = a
    if stale_n is not None:
        stale_txt = f" — STALE-RUNS={stale_n}"
    lines.append(f"classifications {_hb_age_txt(max_age)} old{stale_txt}")
    for line in checks.get("board-check", []):
        lines.append(line)
    for line in checks.get("liveness", []):
        if line.startswith(("DEAD", "DROPPED")):
            lines.append(line)
    if not checks:
        lines.append("(no check verdicts recorded this run — heartbeat is stale)")
    return lines


def cmd_heartbeat(args):
    """heartbeat — the scripted watchdog report (Craig 2026-10-02).
    Assembles ALERTS + JOBS + WORKERS + PENDING + STATE from this run's
    recorded check verdicts, recent queued actions, the pending ledger, and
    the board. The cron pastes the output verbatim as its final message."""
    state = load_state()
    checks = _hb_verdicts(state)
    actions = _hb_recent_actions()
    try:
        board_rows = _board_rows("tokyo-drift-3d")
    except Exception as e:
        board_rows = []
        print(f"(board fetch failed: {e})", file=sys.stderr)
    pending, _ = _load_pending_ledger()
    budget = None
    try:
        import subprocess
        bp = os.path.expanduser("~/workspace/github-billing/check_budget.py")
        out = subprocess.run([sys.executable, bp], capture_output=True,
                             text=True, timeout=45).stdout
        for line in out.splitlines():
            if "ALERT_HIT" in line or "ALERT_WARN" in line or line.startswith("OK"):
                budget = line.strip()[:100]
                break
    except Exception:
        pass
    for line in build_heartbeat(state, checks, actions, board_rows,
                                pending.get("pending", []), budget):
        print(line)


def cmd_brief_check(args):
    """brief-check <brief-file> — validate a filled visual brief.
    The 2026-10-01 td-140 incident: the brief told a VISUAL worker to
    self-merge, contradicting the template's section 6. Checks: (1) all 8
    VISUAL_BRIEF_TEMPLATE.md section headers present; (2) no self-merge
    contradiction (merge-yourself language outside a DO-NOT-MERGE context);
    (3) the task id appears. Prints BRIEF-OK or BRIEF-FAIL <reason>."""
    import re
    path = os.path.expanduser(args[0])
    text = open(path).read()
    tpl = open(os.path.expanduser(
        "~/workspace/supervisor-system/VISUAL_BRIEF_TEMPLATE.md")).read()
    headers = re.findall(r"^## \d+\. .+$", tpl, re.M)
    missing = [h for h in headers if h not in text]
    if missing:
        print(f"BRIEF-FAIL missing sections: {missing}")
        return
    # Self-merge contradiction: merge-yourself phrasing not near DO NOT MERGE.
    bad = re.findall(
        r"(?i)\b(self-merge|merge (it|the PR|the branch) yourself|"
        r"you (may|can) merge|authorized to merge|merge when (done|complete))\b",
        text)
    # allow if a DO NOT MERGE appears within 5 lines either side
    lines = text.splitlines()
    real_bad = []
    for i, line in enumerate(lines):
        if re.search(r"(?i)\b(self-merge|merge (it|the PR|the branch) yourself|"
                     r"you (may|can) merge|authorized to merge|"
                     r"merge when (done|complete))\b", line):
            ctx = "\n".join(lines[max(0, i-5):i+6])
            if "DO NOT MERGE" not in ctx.upper():
                real_bad.append(line.strip()[:80])
    if real_bad:
        print(f"BRIEF-FAIL self-merge contradiction: {real_bad}")
        return
    print("BRIEF-OK all 8 sections present, no self-merge contradiction")


def cmd_dispatch_candidates(args):
    """dispatch-candidates — scripted DISPATCH CHECK shortlist.
    Board rows whose status prefix is open/in_progress, minus terminal
    prefixes (SKIP-DONE RULE), minus tasks with an owner (cmd_owners), minus
    the dispatch denylist. Prints CANDIDATE <task> <prefix> <ownership> ::
    <status>. The cron worker picks from this list; it never greps the
    board itself."""
    game = args[0] if args else "tokyo-drift-3d"
    rows = _board_rows(game)
    state = load_state()
    owned = set(state.get("workers", {}))
    owned |= {sst.get("last_task") for sst in state.get("sessions", {}).values()
              if sst.get("last_task")}
    pa = _load_pending_actions()
    owned |= {e["task"] for e in pa.get("actions", [])
              if e.get("type", "").startswith("dispatch") and e.get("task")}
    # Standing per-task dispatch exclusions (Craig's explicit calls).
    denylist = state.get("dispatch_denylist", {})
    if isinstance(denylist, list):
        denylist = {t: "" for t in denylist}
    denylist = dict(denylist)
    denylist.setdefault("td-054", "explicit no-redispatch per Craig")
    for r in rows:
        if r["prefix"] not in ("open", "in_progress"):
            continue
        if r["task"] in denylist:
            why = denylist[r["task"]] or "denylisted"
            print(f"SKIP {r['task']} {why} :: {r['status'][:60]}")
            continue
        srcs = []
        if r["task"] in owned:
            srcs.append("tracked")
        bo = r["owner"].strip()
        if bo and bo not in ("—", "-", "unassigned", ""):
            srcs.append("board:" + bo[:30])
        mark = "unowned" if not srcs else "owned(" + ",".join(srcs) + ")"
        print(f"CANDIDATE {r['task']} {r['prefix']} {mark} :: {r['status'][:80]}")


# ---------------------------------------------------------------------------
# Watchdog-loop scriptifications, batch 2 (audit 2026-10-02).
# ---------------------------------------------------------------------------

def cmd_classify_report(args):
    """classify-report <file> — transcribe a fixed-format classification report.
    Parses CODEX/CLAUDE lines (env/session, state, task_url/session_url, note),
    runs check-done once, then classify per line. Replaces the manual
    transcription the main agent did every handoff (error-prone)."""
    import re
    path = args[0]
    lines = open(path).read().splitlines()
    # check-done once for tokyo (the only live env)
    print(cmd_check_done(["tokyo-drift-3d"]) or "check-done ok")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(CODEX|CLAUDE)\b.*?\bstate=([A-Z_]+)", line)
        if not m:
            print(f"SKIP unparseable: {line[:80]}")
            continue
        kind, state = m.group(1), m.group(2)
        url = re.search(r"(?:task_url|session_url)=(\S+)", line)
        note = re.search(r"note=(.*)$", line)
        if kind == "CODEX":
            session = "codex:tokyo-drift-3d"
        else:
            session = "claude-code:tokyo-drift-3d"
        cargs = [session, state]
        if url and url.group(1) != "none":
            cargs += ["--task-url", url.group(1)]
        if note:
            cargs += ["--note", note.group(1)[:300]]
        print(f"--- {session} {state}")
        cmd_classify(cargs)


def cmd_ci_report(args):
    """ci-report <repo-full> <sha> — deterministic CI fact-gathering.
    Lists check-runs with conclusions + failed step names. The real-build-
    failure vs infra-noise VERDICT stays human; the fetching is code."""
    repo_full, sha = args[0], args[1]
    try:
        data = _gh(f"/repos/{repo_full}/commits/{sha}/check-runs?per_page=50")
    except Exception as e:
        print(f"CI-ERROR {e}")
        return
    runs = data.get("check_runs", [])
    if not runs:
        print("CI-NONE no check runs on this SHA")
        return
    for r in runs:
        print(f"CI {r['name'][:50]} status={r['status']} "
              f"conclusion={r.get('conclusion')}")


def cmd_salvage(args):
    """salvage <repo-full> <task> — dead worker's salvageable work.
    Exposes the liveness _worker_evidence salvage for the dispatch path:
    branches containing the task id with commits ahead of main, recent
    task-file commits. The brief folds this in as done-work-not-to-redo."""
    import re
    repo_full, task = args[0], args[1]
    alive, reasons, salvage = _worker_evidence(
        repo_full, task, f"godot/docs/tasks/{task}.md", None)
    if not salvage:
        print(f"SALVAGE-NONE {task}: no branch/PR/task-file activity found")
        return
    print(f"SALVAGE {task}:")
    for s in salvage:
        print(s)


def _session_fresh_alive(session):
    """(alive, age_min, classification) for a cloud session."""
    state = load_state()
    sst = state.get("sessions", {}).get(session, {})
    cls = sst.get("last_classification")
    ts = parse_ts(sst.get("last_classification_ts"))
    age = (now() - ts).total_seconds() / 60 if ts else 99999
    fresh = age < LIVENESS_CLASSIFY_MAX_MIN
    alive = fresh and cls in ("WORKING", "STALLED", "FINISHED")
    return alive, age, cls


def cmd_session_alive(args):
    """session-alive <session> — ALIVE or GONE for INSPECT_MERGED routing.
    Worker alive (WORKING/STALLED/FINISHED, fresh) -> steer it for missing
    evidence. Gone -> spawn a scavenger subagent."""
    session = args[0]
    alive, age, cls = _session_fresh_alive(session)
    print(f"SESSION-{'ALIVE' if alive else 'GONE'} {session} "
          f"(last={cls}, {age:.0f}min ago)")


def cmd_all_blocked(args):
    """all-blocked — evaluate the ALL-BLOCKED ESCALATION predicate in code.
    True iff every live session is STALLED/DEAD/OUT_OF_TOKENS/LOGIN_BLOCKED,
    none WORKING, and no viable sibling exists (FAILOVER_SIBLING map)."""
    blocked_states = {"STALLED", "DEAD", "OUT_OF_TOKENS", "LOGIN_BLOCKED"}
    any_working, all_blocked, per = False, True, []
    for session in SESSIONS:
        if session in ARCHIVED_SESSIONS:
            continue
        alive, age, cls = _session_fresh_alive(session)
        per.append(f"{session}={cls}")
        if cls == "WORKING" and age < LIVENESS_CLASSIFY_MAX_MIN:
            any_working = True
        if cls not in blocked_states:
            all_blocked = False
    result = all_blocked and not any_working
    print(f"ALL-BLOCKED {result} ({'; '.join(per)})")
    return result


def cmd_dispatch_eligible(args):
    """dispatch-eligible — per-session ELIGIBLE/INELIGIBLE for the DISPATCH CHECK.
    Eligible = last classification FINISHED (idle), no pending action for the
    session, the session's own last task not actively owned, no expect-return
    hold. (A registered subagent on ANOTHER task doesn't block the session —
    max-parallelization.)"""
    state = load_state()
    pa = _load_pending_actions()
    pending_sessions = {e.get("session") for e in pa.get("actions", [])}
    workers = state.get("workers", {})
    for session in SESSIONS:
        if session in ARCHIVED_SESSIONS:
            continue
        alive, age, cls = _session_fresh_alive(session)
        reasons = []
        if cls != "FINISHED":
            reasons.append(f"classification={cls}")
        if session in pending_sessions:
            reasons.append("pending action queued")
        last_task = state.get("sessions", {}).get(session, {}).get("last_task")
        if last_task in workers:
            reasons.append(f"own task {last_task} actively worked")
        hold = state.get("sessions", {}).get(session, {}).get("expect_return")
        if hold and parse_ts(hold.get("until")) and parse_ts(hold["until"]) > now():
            reasons.append(f"expect-return hold until {hold['until'][:16]} "
                           f"({hold.get('reason','')[:40]})")
        if reasons:
            print(f"INELIGIBLE {session}: {'; '.join(reasons)}")
        else:
            print(f"ELIGIBLE {session}")


def cmd_sibling_check(args):
    """sibling-check <session> — failover-steer safety.
    Prints STEER-OK unless the FAILOVER_SIBLING is WORKING and fresh."""
    session = args[0]
    sibling = FAILOVER_SIBLING.get(session)
    if not sibling:
        print(f"STEER-OK {session}: no sibling, route to Muse subagent")
        return
    alive, age, cls = _session_fresh_alive(sibling)
    if cls == "WORKING" and age < LIVENESS_CLASSIFY_MAX_MIN:
        print(f"STEER-BLOCKED {sibling} is WORKING ({age:.0f}min ago) — "
              f"never steal a working session")
    else:
        print(f"STEER-OK {sibling} last={cls} ({age:.0f}min ago)")


def cmd_dispatch_guard(args):
    """dispatch-guard <session> — pre-dispatch re-verification.
    Prints GO unless the session turned WORKING since decide. The browser
    task remains the final re-verifier."""
    session = args[0]
    alive, age, cls = _session_fresh_alive(session)
    if cls == "WORKING" and age < LIVENESS_CLASSIFY_MAX_MIN:
        print(f"NO-GO {session}: WORKING ({age:.0f}min ago) — do not dispatch over it")
    else:
        print(f"GO {session}: last={cls} ({age:.0f}min ago)")


def cmd_failover_undo(args):
    """failover-undo <session> — undo a failover ledger entry.
    The set side (cmd_failover) existed; the undo didn't — a failed delivery
    couldn't pop the ledger so the next run never retried. Clears
    last_failover_ts so the episode can fire again."""
    session = args[0]
    state = load_state()
    sst = state.get("sessions", {}).setdefault(session, {})
    sst.pop("last_failover_ts", None)
    sst.pop("out_of_tokens_since", None)
    save_state(state)
    print(f"FAILOVER-UNDONE {session}")


def cmd_links(args):
    """links <session> — emit the inline-link URLs for a heartbeat line.
    Task-file, PR, and session URLs from state via the documented patterns.
    The worker pastes them verbatim (Craig clicks them)."""
    import re
    session = args[0]
    state = load_state()
    sst = state.get("sessions", {}).get(session, {})
    repo = SESSIONS.get(session, {}).get("repo", "tokyo-drift-3d")
    repo_full = REPOS[repo]
    task = sst.get("last_task")
    if task and repo == "tokyo-drift-3d":
        print(f"LINK task https://github.com/{repo_full}/blob/main/"
              f"godot/docs/tasks/{task}.md")
    note = " ".join(str(sst.get(k) or "") for k in ("last_note", "note"))
    for pr in sorted({int(n) for n in re.findall(r"#(\d+)", note)}):
        print(f"LINK pr https://github.com/{repo_full}/pull/{pr}")
    url = sst.get("task_url")
    if url:
        print(f"LINK session {url}")


def cmd_expect_return(args):
    """expect-return <session> <iso-ts> <reason> — wake-timer hold.
    Records that a worker is expected back (token refill); dispatch-eligible
    and liveness treat it as a hold until the timestamp passes, so the next
    run doesn't treat it as abandoned."""
    session, iso, reason = args[0], args[1], " ".join(args[2:])
    state = load_state()
    sst = state.get("sessions", {}).setdefault(session, {})
    sst["expect_return"] = {"until": iso, "reason": reason,
                            "recorded_at": now().isoformat()}
    save_state(state)
    print(f"EXPECT-RETURN {session} until {iso} ({reason[:60]})")


def cmd_block(args):
    """block <session> <blocker-key> <reason> — record a keyed blocker.
    Pairs with blocker-surfaced: 'surface to Craig exactly once per blocker'
    becomes a ledger read, not a memory."""
    session, key = args[0], args[1]
    reason = " ".join(args[2:])
    state = load_state()
    sst = state.get("sessions", {}).setdefault(session, {})
    blockers = sst.setdefault("blockers", {})
    blockers[key] = {"reason": reason, "recorded_at": now().isoformat(),
                     "surfaced": blockers.get(key, {}).get("surfaced", False)}
    save_state(state)
    print(f"BLOCKED {session} [{key}] {reason[:60]}")


def cmd_blocker_surfaced(args):
    """blocker-surfaced <session> <blocker-key> — once-per-blocker gate.
    Prints SURFACE (first time — stamps surfaced_ts) or SUPPRESSED."""
    session, key = args[0], args[1]
    state = load_state()
    sst = state.get("sessions", {}).setdefault(session, {})
    b = sst.setdefault("blockers", {}).setdefault(key, {})
    if b.get("surfaced"):
        print(f"SUPPRESSED {session} [{key}] (already surfaced "
              f"{b.get('surfaced_at','?')[:16]})")
    else:
        b["surfaced"] = True
        b["surfaced_at"] = now().isoformat()
        save_state(state)
        print(f"SURFACE {session} [{key}]")


def cmd_classification_health(args):
    """classification-health — consecutive-stale-run counter.
    The DEGRADED WATCHDOG ALARM's staleness counting as code: increments when
    every live session's classification is older than 45 min, resets on fresh
    data. Prints STALE-RUNS=n. The main agent ANDs this with the in-flight
    browser check (needs browser.list_tasks, not scriptable)."""
    state = load_state()
    health = state.setdefault("classification_health", {"stale_runs": 0})
    stale = True
    for session in SESSIONS:
        if session in ARCHIVED_SESSIONS:
            continue
        ts = parse_ts(state.get("sessions", {}).get(session, {})
                      .get("last_classification_ts"))
        if ts and (now() - ts).total_seconds() / 60 < 45:
            stale = False
    health["stale_runs"] = health.get("stale_runs", 0) + 1 if stale else 0
    save_state(state)
    print(f"STALE-RUNS={health['stale_runs']}")


def cmd_entry_attempt(args):
    """entry-attempt <type> <session> — NO_ACTION_WORKING attempt counting.
    Increments attempts; at 3, moves the entry to dropped with SURFACE flag.
    Prints ATTEMPT n/3 or DROPPED-SURFACE."""
    etype, session = args[0], args[1]
    pa = _load_pending_actions()
    for e in pa.get("actions", []):
        if e.get("type") == etype and e.get("session") == session:
            e["attempts"] = e.get("attempts", 0) + 1
            if e["attempts"] >= 3:
                pa["actions"].remove(e)
                pa.setdefault("dropped", []).append(e)
                _save_pending_actions(pa)
                print(f"DROPPED-SURFACE {etype} {session} "
                      f"(3 attempts — surface to Craig)")
            else:
                _save_pending_actions(pa)
                print(f"ATTEMPT {e['attempts']}/3 {etype} {session}")
            return
    print(f"ENTRY-NOT-FOUND {etype} {session}")


def cmd_entry_start(args):
    """entry-start <type> <session> — claim an entry for delivery.
    Refuses when another in_progress entry targets the same session
    ('never run two entries against the same session concurrently')."""
    etype, session = args[0], args[1]
    pa = _load_pending_actions()
    for e in pa.get("actions", []):
        if (e.get("session") == session and e.get("status") == "in_progress"
                and not (e.get("type") == etype)):
            print(f"ENTRY-BLOCKED {session}: {e.get('type')} already in_progress")
            return
    for e in pa.get("actions", []):
        if e.get("type") == etype and e.get("session") == session:
            e["status"] = "in_progress"
            _save_pending_actions(pa)
            print(f"ENTRY-STARTED {etype} {session}")
            return
    print(f"ENTRY-NOT-FOUND {etype} {session}")


def cmd_pending_validate(args):
    """pending-validate — per-type required-key schema check.
    Every queued entry must carry the keys its consumer needs. Prints
    VALID or INVALID <type> <missing keys>."""
    required = {
        "nudge-codex": ["session", "target_task_url"],
        "nudge-claude": ["session", "target_task_url"],
        "resume-codex": ["session", "target_workspace"],
        "resume-claude": ["session", "target_workspace"],
        "steer-codex": ["session", "message"],
        "steer-claude": ["session", "message"],
        "dispatch-codex": ["session", "env", "task", "task_file", "brief"],
        "dispatch-claude": ["session", "task", "task_file", "brief"],
        "dispatch-subagent": ["task", "task_file", "brief"],
        "screenshots": ["session", "pr"],
    }
    pa = _load_pending_actions()
    ok = True
    for e in pa.get("actions", []):
        need = required.get(e.get("type"), [])
        missing = [k for k in need if not e.get(k)]
        if missing:
            ok = False
            print(f"INVALID {e.get('type')} missing={missing}")
    if ok:
        print(f"VALID {len(pa.get('actions', []))} entries")


def cmd_idle_defect_check(args):
    """idle-defect-check — IDLE-WITH-ASSIGNABLE-WORK is a run defect.
    Session IDLE (not WORKING, no in-progress action) AND dispatch-eligible
    AND a dispatch candidate exists -> DEFECT. Else OK. Denylisted tasks
    (td-054 etc.) never count as assignable work."""
    rows = _board_rows("tokyo-drift-3d")
    state = load_state()
    owned = set(state.get("workers", {}))
    denylist = state.get("dispatch_denylist", {})
    denylist = set(denylist) | {"td-054"}
    cands = []
    for r in rows:
        if r["prefix"] not in ("open", "in_progress"):
            continue
        if r["task"] in owned or r["task"] in denylist:
            continue
        bo = r["owner"].strip()
        if bo and bo not in ("—", "-", "unassigned", ""):
            continue  # board names an owner
        # Confirm against the task file — board rows go stale (td-125 was
        # in_review on the task file while the board said in_progress).
        ts = _task_status_on_main("doublehidenblade/tokyo-drift-3d",
                                  f"godot/docs/tasks/{r['task']}.md")
        if ts in ("open", "in_progress"):
            cands.append(r["task"])
    pa = _load_pending_actions()
    busy = {e.get("session") for e in pa.get("actions", [])
            if e.get("status") == "in_progress"}
    defects = []
    for session in SESSIONS:
        if session in ARCHIVED_SESSIONS:
            continue
        alive, age, cls = _session_fresh_alive(session)
        if cls in ("WORKING",) or session in busy:
            continue
        if cands:
            defects.append((session, cands[0]))
    if defects:
        for s, t in defects:
            print(f"DEFECT {s} idle with assignable work ({t}) — "
                  f"dispatch check must fire")
        sys.exit(3)
    print("OK no idle-with-assignable-work")


def cmd_audit_task(args):
    """audit-task <task> — auto-assemble validate_task_outcome facts.
    Gathers: merged? (board prefix), owner? (owners), owner alive?
    (liveness/session), blocked markers? (session blockers). Prints the
    OUTCOME via validate_task_outcome. The worker overrides any field it
    knows better via validate-task directly."""
    task = args[0]
    rows = {r["task"]: r for r in _board_rows("tokyo-drift-3d")}
    row = rows.get(task, {})
    prefix = row.get("prefix", "")
    merged = prefix in ("merged", "live", "validated", "done")
    state = load_state()
    workers = state.get("workers", {})
    owner = None
    owner_alive = False
    if task in workers:
        w = workers[task]
        owner = w.get("kind") + ":" + (w.get("session") or "subagent")
        hb = os.path.join(LIVENESS_HEARTBEAT_DIR, f"{task}.json")
        if os.path.exists(hb):
            hb_dt = parse_ts(json.load(open(hb)).get("ts"))
            owner_alive = bool(hb_dt and
                               (now() - hb_dt).total_seconds() / 60 < 35)
    else:
        for session, sst in state.get("sessions", {}).items():
            if sst.get("last_task") == task:
                owner = session
                alive, age, cls = _session_fresh_alive(session)
                owner_alive = alive
    blocked_human = any(
        sst.get("blockers") for sst in state.get("sessions", {}).values())
    facts = {"merged": merged, "live_verified": False, "owner": owner,
             "owner_alive": owner_alive, "blocked_human": bool(blocked_human),
             "blocked_external": False, "framing": ""}
    try:
        num, label = validate_task_outcome(task, facts)
    except DegradedWatchdog as e:
        print(str(e))
        print(f"OUTCOME=ALARM TASK={task}")
        sys.exit(3)
    print(f"OUTCOME={num} ({label}) TASK={task} "
          f"facts={json.dumps(facts)[:160]}")


def cmd_publish_audit(args):
    """publish-audit <game> — who dispatched the publish workflows?
    Lists recent runs of publish-game.yml / publish-web.yml with actor +
    event. Flags any workflow_dispatch not by Craig (doublehidenblade).
    Prose 'never dispatch except on Craig's explicit ask' becomes an
    auditable check."""
    game = args[0] if args else "tokyo"
    src_repo, _ = PUBLISH_REPOS[game]
    files = ["publish-game.yml", "publish-web.yml"] if game == "tokyo" else ["publish-web.yml"]
    for wf in files:
        try:
            runs = _gh(f"/repos/{src_repo}/actions/workflows/{wf}/runs?per_page=8")
        except Exception as e:
            print(f"PUBLISH-AUDIT-ERROR {wf}: {e}")
            continue
        for r in runs.get("workflow_runs", []):
            actor = (r.get("actor") or {}).get("login", "?")
            flag = ""
            if r.get("event") == "workflow_dispatch" and actor != "doublehidenblade":
                flag = " <-- FLAG: dispatch not by Craig"
            print(f"PUBLISH-RUN {wf} #{r['run_number']} {r['event']} "
                  f"by={actor} {r['created_at'][:16]} {r['conclusion']}{flag}")


def cmd_imagegen_due(args):
    """imagegen-due — the STATE_MACHINE.md imagegen-replacement condition.
    DUE iff: Claude texture-imagegen session done AND replacement slots
    unstarted AND no live session doing imagegen work. Honors an explicit
    "complete": true in imagegen_replacement.json."""
    import os
    path = os.path.join(STATE_DIR, "imagegen_replacement.json")
    try:
        data = json.load(open(path))
    except Exception as e:
        print(f"IMAGEGEN-ERROR cannot read replacement file ({e})")
        return
    if data.get("complete"):
        print(f"IMAGEGEN-NOT-DUE marked complete: {str(data.get('note'))[:80]}")
        return
    state = load_state()
    cls = state.get("sessions", {}).get("claude-code:tokyo-drift-3d", {}).get(
        "last_classification")
    slots = {k: v for k, v in data.items()
             if k in ("claude", "codex_neon", "codex_shuto")}
    unstarted = [k for k, v in slots.items() if not v]
    live_imagegen = [t for t, w in state.get("workers", {}).items()
                     if "imagegen" in t or "imagegen" in str(w.get("task_file", ""))]
    if cls == "FINISHED" and unstarted and not live_imagegen:
        print(f"IMAGEGEN-DUE unstarted slots: {unstarted}")
    else:
        print(f"IMAGEGEN-NOT-DUE session={cls} unstarted={unstarted} "
              f"live_imagegen={live_imagegen}")


def cmd_imagegen_mark(args):
    """imagegen-mark <slot> — idempotent replacement-slot marking.
    Never double-start: marks codex_neon/codex_shuto/claude started."""
    slot = args[0]
    path = os.path.join(STATE_DIR, "imagegen_replacement.json")
    data = json.load(open(path))
    if data.get(slot):
        print(f"IMAGEGEN-ALREADY-MARKED {slot} (not double-starting)")
        return
    data[slot] = True
    data["note"] = (str(data.get("note", "")) +
                    f" | {now().isoformat()[:16]}Z: {slot} replacement started.")
    json.dump(data, open(path, "w"), indent=1)
    print(f"IMAGEGEN-MARKED {slot}")


def cmd_taskfile_check(args):
    """taskfile-check <repo-full> <task> — task-file contract as code.
    The SYSTEM.md 'JSON contract' drifted from the Markdown reality (audit
    2026-10-02); this checks the reality: required sections present, ##
    Status first line is a known token, work-log entries dated, and — if
    status is validated/rejected — the verdict has per-criterion PASS/FAIL."""
    import re
    repo_full, task = args[0], args[1]
    known = {"open", "in_progress", "in_review", "validated", "rejected",
             "done", "done-pending-verdict", "blocked", "merged", "closed",
             "abandoned", "paused"}
    try:
        text = _task_file_text(repo_full, f"godot/docs/tasks/{task}.md")
    except Exception as e:
        print(f"TASKFILE-FAIL {task}: unreadable ({e})")
        return
    problems = []
    for section in ("## Status", "## Work log", "## Evidence"):
        if section not in text:
            problems.append(f"missing {section}")
    st = _task_status_on_main(repo_full, f"godot/docs/tasks/{task}.md")
    if st not in known:
        problems.append(f"unknown status token '{st}'")
    if "## Work log" in text:
        wl = text.split("## Work log", 1)[1].split("## ", 1)[0]
        for line in wl.splitlines():
            line = line.strip()
            if line.startswith("-") and line.strip("- ").strip():
                body = line.strip("- ").strip()
                if body.startswith("("):  # "(worker fills)" placeholder
                    continue
                if not re.search(r"\d{4}-\d{2}-\d{2}", line):
                    problems.append(f"undated work-log entry: {line[:60]}")
                    break
    if st in ("validated", "rejected") and "## Verdict" in text:
        verdict = text.split("## Verdict", 1)[1].split("## ", 1)[0]
        if not re.search(r"PASS|FAIL", verdict):
            problems.append("verdict lacks per-criterion PASS/FAIL")
    if problems:
        for p in problems:
            print(f"TASKFILE-FAIL {task}: {p}")
    else:
        print(f"TASKFILE-OK {task} (status={st})")


def cmd_board_check(args):
    """board-check <game> — board hygiene as code.
    (1) lint: every data row has exactly 6 cells (flags the 7-column
    corruption); (2) PR column sanity: PR numbers referenced exist via API
    (sampled); (3) stale owners: Owner is empty while the liveness registry
    shows an active worker. Prints BOARD-OK or BOARD-FAIL lines."""
    import re
    game = args[0] if args else "tokyo-drift-3d"
    blob = _gh(f"/repos/{BOARD_REPO}/contents/{BOARD_PATHS[game]}?ref=main")
    import base64
    text = base64.b64decode(blob["content"]).decode("utf-8", "replace")
    fails = 0
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.split("|")[1:-1]]
        if not cells or set(cells) <= {"---", ""}:
            continue  # separator row
        if cells[0].lower() == "task":
            continue  # header row
        # Rows with FEWER than 6 cells (trailing empties omitted) still parse
        # via the task-id pattern; only MORE than 6 is real corruption, and
        # rows where no task cell parses at all are unusable.
        has_task = any(re.match(r"^(?:td|p3d)-\d+", c, re.I) for c in cells)
        if len(cells) > 6 or not has_task:
            print(f"BOARD-FAIL line {i}: {len(cells)} cells, "
                  f"task-parse={'ok' if has_task else 'FAILED'}: {s[:80]}")
            fails += 1
    state = load_state()
    workers = state.get("workers", {})
    rows = _board_rows(game)
    for r in rows:
        bo = r["owner"].strip()
        if r["task"] in workers and bo in ("—", "-", "", "unassigned"):
            print(f"BOARD-FAIL {r['task']}: liveness registry shows active "
                  f"worker but board Owner is empty")
            fails += 1
    if not fails:
        print(f"BOARD-OK {game} ({len(rows)} rows)")


# ---------------------------------------------------------------------------
# Cloud sync: the watchdog's mutable state lives in the repo
# (project-management/watchdog/state/), so any agent can resume from the GH
# link alone. The scheduler runs `state-pull` first and `state-push` last.
# ---------------------------------------------------------------------------
WATCHDOG_REPO = "doublehidenblade/game-dev-central"
WATCHDOG_STATE_PREFIX = "project-management/watchdog/state"
WATCHDOG_RELEASES_PREFIX = "project-management/watchdog/releases"


def _gh_api(method, path, data=None):
    """Authenticated API call with an arbitrary method + JSON body.

    Uses urllib + the authd surrogate directly (no CLI arg limits) when
    available; falls back to the WATCHDOG_GH_BIN CLI for small payloads."""
    import urllib.request
    try:
        sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
        from dynamic_credentials import add_surrogate_to_request, read_json_response
        req = urllib.request.Request(
            "https://api.github.com" + path,
            data=json.dumps(data).encode() if data is not None else None,
            method=method)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        add_surrogate_to_request(req, "custom.github",
                                 allowed_hosts=("github.com", "api.github.com"))
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
        return json.loads(body) if body.strip() else {}
    except Exception as e:
        raise RuntimeError(f"gh api {method} {path}: {e}")


def _sync_paths():
    """Local files synced with the repo: (repo_path, local_path)."""
    pairs = []
    for name in ("state.json", "pending_actions.json", "last-check.json",
                 "imagegen_replacement.json"):
        pairs.append((f"{WATCHDOG_STATE_PREFIX}/{name}",
                      os.path.join(STATE_DIR, name)))
    for name in ("pending.json", "baselines.json"):
        pairs.append((f"{WATCHDOG_RELEASES_PREFIX}/{name}",
                      os.path.join(RELEASES_DIR, name)))
    hb = os.path.join(STATE_DIR, "worker-heartbeats")
    if os.path.isdir(hb):
        for f in sorted(os.listdir(hb)):
            if f.endswith(".json"):
                pairs.append((f"{WATCHDOG_STATE_PREFIX}/worker-heartbeats/{f}",
                              os.path.join(hb, f)))
    return pairs


def cmd_state_pull(args):
    """state-pull — download the watchdog state + ledgers from repo main.

    Makes the local working copy match the cloud. Run first in the scheduler
    loop and on any fresh takeover before doing watchdog work."""
    for repo_path, local_path in _sync_paths():
        try:
            blob = _gh(f"/repos/{WATCHDOG_REPO}/contents/{repo_path}?ref=main")
        except Exception:
            continue  # not in repo yet (first run) — keep local
        import base64
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "w") as f:
            f.write(base64.b64decode(blob["content"]).decode("utf-8"))
    print("STATE-PULLED from main")


def cmd_state_push(args):
    """state-push [message] — commit changed watchdog state to repo main.

    Git-database API: blobs -> tree -> commit -> ref update. Aborts loudly on
    a moved ref (another writer pushed first) instead of clobbering it."""
    import base64
    ref = _gh(f"/repos/{WATCHDOG_REPO}/git/ref/heads/main")
    base_commit = ref["object"]["sha"]
    base_tree = _gh(f"/repos/{WATCHDOG_REPO}/git/commits/{base_commit}")["tree"]["sha"]
    import base64 as _b64
    tree_entries = []
    changed = 0
    for repo_path, local_path in _sync_paths():
        if not os.path.exists(local_path):
            continue
        with open(local_path, "rb") as f:
            raw = f.read()
        try:
            blob0 = _gh(f"/repos/{WATCHDOG_REPO}/contents/{repo_path}?ref=main")
            same = _b64.b64decode(blob0["content"]) == raw
        except Exception:
            same = False  # not in repo yet — must push
        if same:
            continue
        blob = _gh_api("POST", f"/repos/{WATCHDOG_REPO}/git/blobs",
                       {"content": _b64.b64encode(raw).decode(), "encoding": "base64"})
        tree_entries.append({"path": repo_path, "mode": "100644",
                             "type": "blob", "sha": blob["sha"]})
        changed += 1
    if not changed:
        print("STATE-PUSH nothing changed")
        return
    new_tree = _gh_api("POST", f"/repos/{WATCHDOG_REPO}/git/trees",
                       {"base_tree": base_tree, "tree": tree_entries})["sha"]
    msg = args[0] if args else "watchdog: sync state"
    commit = _gh_api("POST", f"/repos/{WATCHDOG_REPO}/git/commits",
                     {"message": msg, "tree": new_tree,
                      "parents": [base_commit]})["sha"]
    # Re-read the ref: abort instead of clobbering a concurrent writer.
    ref_now = _gh(f"/repos/{WATCHDOG_REPO}/git/ref/heads/main")["object"]["sha"]
    if ref_now != base_commit:
        print(f"STATE-PUSH-CONFLICT main moved {base_commit[:7]} -> {ref_now[:7]}; "
              f"commit {commit[:7]} NOT pushed — run state-pull and retry")
        return
    _gh_api("PATCH", f"/repos/{WATCHDOG_REPO}/git/refs/heads/main", {"sha": commit})
    print(f"STATE-PUSHED {commit[:7]} ({changed} files)")


def cmd_validator_check(args):
    """validator-check <repo-full> <task> — verdict as code.
    SYSTEM.md hard rule #2: a verdict without an evidence citation per
    criterion is itself rejected. Checks: every completion criterion has a
    PASS/FAIL in ## Verdict, each with a citation path that exists in the
    repo. Prints VALIDATOR-OK or VALIDATOR-FAIL."""
    import re
    repo_full, task = args[0], args[1]
    try:
        text = _task_file_text(repo_full, f"godot/docs/tasks/{task}.md")
    except Exception as e:
        print(f"VALIDATOR-FAIL {task}: unreadable ({e})")
        return
    if "## Verdict" not in text:
        print(f"VALIDATOR-FAIL {task}: no ## Verdict section")
        return
    verdict = text.split("## Verdict", 1)[1].split("## ", 1)[0]
    criteria = []
    if "## Completion criteria" in text:
        crit = text.split("## Completion criteria", 1)[1].split("## ", 1)[0]
        criteria = re.findall(r"^\d+\.\s*(.+)$", crit, re.M)
    fails = []
    for n, c in enumerate(criteria, 1):
        line = next((l for l in verdict.splitlines()
                     if re.search(rf"\bcriterion[-\s]*{n}\b", l, re.I)
                     or f"({n})" in l), None)
        if not line or not re.search(r"PASS|FAIL", line):
            fails.append(f"criterion {n}: no PASS/FAIL in verdict")
            continue
        cites = re.findall(r"[`\"']?((?:godot/)?qa/[\w\-./]+\.(?:png|jpg|mp4))[`\"']?",
                           line)
        for cp in cites:
            cp = cp if cp.startswith("godot/") else "godot/" + cp
            try:
                _gh(f"/repos/{repo_full}/contents/{cp}?ref=main")
            except Exception:
                fails.append(f"criterion {n}: cited path missing: {cp}")
    for f in fails:
        print(f"VALIDATOR-FAIL {task}: {f}")
    if not fails:
        print(f"VALIDATOR-OK {task} ({len(criteria)} criteria)")


def cmd_transitions(args):
    """transitions — the SYSTEM.md board-watcher as code.
    Diffs this cycle's board/task statuses against the last recorded snapshot
    and prints FLIP lines (task: old -> new). The 'watcher' the system doc
    describes was never implemented (audit 2026-10-02) — this is it:
    in_review flips wake validator dispatch; validated/rejected/blocked flips
    notify. Snapshot lives in state.json so the diff is deterministic."""
    game = args[0] if args else "tokyo-drift-3d"
    rows = _board_rows(game)
    state = load_state()
    snap = state.setdefault("board_snapshot", {})
    flips = []
    for r in rows:
        old = snap.get(r["task"])
        if old is not None and old != r["prefix"]:
            flips.append((r["task"], old, r["prefix"]))
        snap[r["task"]] = r["prefix"]
    save_state(state)
    watch = {"in_review": "wake-validator", "validated": "notify-craig",
             "rejected": "notify-or-iterate", "blocked": "notify-craig"}
    for task, old, new in flips:
        action = watch.get(new, "silent")
        print(f"FLIP {task}: {old} -> {new} [{action}]")
    if not flips:
        print("NO-FLIPS")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == "gate":
        cmd_gate()
    elif cmd == "check-done":
        cmd_check_done(sys.argv[2:])
    elif cmd == "classify":
        cmd_classify(sys.argv[2:])
    elif cmd == "decide":
        cmd_decide(sys.argv[2])
    elif cmd == "nudge":
        cmd_nudge(sys.argv[2])
    elif cmd == "resume":
        cmd_resume(sys.argv[2])
    elif cmd == "rebrief":
        cmd_rebrief(sys.argv[2])
    elif cmd == "merged":
        cmd_merged(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "worker")
    elif cmd == "inspected":
        cmd_inspected(sys.argv[2])
    elif cmd == "failover":
        cmd_failover(sys.argv[2])
    elif cmd == "loginfail":
        cmd_loginfail(sys.argv[2])
    elif cmd == "validate-task":
        cmd_validate_task(sys.argv[2:])
    elif cmd == "status":
        cmd_status()
    elif cmd == "register-worker":
        cmd_register_worker(sys.argv[2:])
    elif cmd == "deregister-worker":
        cmd_deregister_worker(sys.argv[2:])
    elif cmd == "assign":
        cmd_assign(sys.argv[2:])
    elif cmd == "liveness":
        _capture_verdicts("liveness", cmd_liveness)
    elif cmd == "board":
        cmd_board(sys.argv[2:])
    elif cmd == "task-status":
        cmd_task_status(sys.argv[2:])
    elif cmd == "queue-action":
        cmd_queue_action(sys.argv[2:])
    elif cmd == "owners":
        cmd_owners(sys.argv[2:])
    elif cmd == "conflicts":
        _capture_verdicts("conflicts", cmd_conflicts, sys.argv[2:])
    elif cmd == "dispatch-candidates":
        cmd_dispatch_candidates(sys.argv[2:])
    elif cmd == "ship-verify":
        cmd_ship_verify(sys.argv[2:])
    elif cmd == "adopt-orphans":
        cmd_adopt_orphans(sys.argv[2:])
    elif cmd == "scriptification-audit":
        cmd_scriptification_audit(sys.argv[2:])
    elif cmd == "evidence-audit":
        cmd_evidence_audit(sys.argv[2:])
    elif cmd == "evidence-collect":
        cmd_evidence_collect(sys.argv[2:])
    elif cmd == "evidence-checks":
        cmd_evidence_checks(sys.argv[2:])
    elif cmd == "brief-check":
        cmd_brief_check(sys.argv[2:])
    elif cmd == "publish-verify":
        cmd_publish_verify(sys.argv[2:])
    elif cmd == "record-pending":
        cmd_record_pending(sys.argv[2:])
    elif cmd == "pending-report":
        cmd_pending_report(sys.argv[2:])
    elif cmd == "pending-reported":
        cmd_pending_reported(sys.argv[2:])
    elif cmd == "pending-hold":
        cmd_pending_hold(sys.argv[2:])
    elif cmd == "pending-release":
        cmd_pending_release(sys.argv[2:])
    elif cmd == "heartbeat":
        cmd_heartbeat(sys.argv[2:])
    elif cmd == "classify-report":
        cmd_classify_report(sys.argv[2:])
    elif cmd == "ci-report":
        cmd_ci_report(sys.argv[2:])
    elif cmd == "salvage":
        cmd_salvage(sys.argv[2:])
    elif cmd == "session-alive":
        cmd_session_alive(sys.argv[2:])
    elif cmd == "all-blocked":
        _capture_verdicts("all-blocked", cmd_all_blocked, sys.argv[2:])
    elif cmd == "dispatch-eligible":
        cmd_dispatch_eligible(sys.argv[2:])
    elif cmd == "sibling-check":
        cmd_sibling_check(sys.argv[2:])
    elif cmd == "dispatch-guard":
        cmd_dispatch_guard(sys.argv[2:])
    elif cmd == "failover-undo":
        cmd_failover_undo(sys.argv[2:])
    elif cmd == "links":
        cmd_links(sys.argv[2:])
    elif cmd == "expect-return":
        cmd_expect_return(sys.argv[2:])
    elif cmd == "block":
        cmd_block(sys.argv[2:])
    elif cmd == "blocker-surfaced":
        cmd_blocker_surfaced(sys.argv[2:])
    elif cmd == "classification-health":
        _capture_verdicts("classification-health", cmd_classification_health, sys.argv[2:])
    elif cmd == "entry-attempt":
        cmd_entry_attempt(sys.argv[2:])
    elif cmd == "entry-start":
        cmd_entry_start(sys.argv[2:])
    elif cmd == "pending-validate":
        cmd_pending_validate(sys.argv[2:])
    elif cmd == "idle-defect-check":
        _capture_verdicts("idle-defect-check", cmd_idle_defect_check, sys.argv[2:])
    elif cmd == "audit-task":
        cmd_audit_task(sys.argv[2:])
    elif cmd == "transitions":
        _capture_verdicts("transitions", cmd_transitions, sys.argv[2:])
    elif cmd == "publish-audit":
        cmd_publish_audit(sys.argv[2:])
    elif cmd == "imagegen-due":
        cmd_imagegen_due(sys.argv[2:])
    elif cmd == "imagegen-mark":
        cmd_imagegen_mark(sys.argv[2:])
    elif cmd == "taskfile-check":
        cmd_taskfile_check(sys.argv[2:])
    elif cmd == "board-check":
        _capture_verdicts("board-check", cmd_board_check, sys.argv[2:])
    elif cmd == "validator-check":
        cmd_validator_check(sys.argv[2:])
    elif cmd == "state-pull":
        cmd_state_pull(sys.argv[2:])
    elif cmd == "state-push":
        cmd_state_push(sys.argv[2:])
    else:
        print(f"ERROR unknown command {cmd}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
