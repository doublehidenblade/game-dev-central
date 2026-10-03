#!/usr/bin/env python3
"""Offline tests for the agent-watch state machine.

Part 1: evidence -> classification mapping. This mirrors browser-brief.md's rules
as an executable spec (the real classification runs in the browser task). Each
case is a dict of observed page evidence; classify_evidence() must map it to the
state the brief defines.

Part 2: classification -> action mapping. Uses the REAL decide_action() from
watch.py, so the enforced rules are tested, not a copy.
"""
import sys, os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch


def classify_evidence(ev):
    """Executable spec of browser-brief.md PART 1+2 rules."""
    if ev.get("login_wall"):
        return "LOGIN_BLOCKED"
    if ev.get("product") == "codex":
        if ev.get("usage_limit_banner"):
            return "OUT_OF_TOKENS"
        if ev.get("final_status") == "Merged" and ev.get("retry_button"):
            # Craig 2026-09-23 (~14:07 CDT): the worker merges its own PR when
            # CI is green — "Merged" is FINISHED work, not DEAD. The run will
            # inspect the merged diff and report to Craig.
            return "FINISHED"
        if ev.get("final_status") in ("Failed", "Cancelled") and ev.get("retry_button"):
            return "DEAD"
        if ev.get("working_banner") and ev.get("thinking") and ev.get("cancel_button") and ev.get("live_log"):
            return "WORKING"
        if ev.get("task_unfinished") and not ev.get("live_log") and ev.get("composer_idle"):
            return "STALLED"
        return "UNKNOWN"
    if ev.get("product") == "claude-code":
        if ev.get("usage_pct", 0) >= 99 or ev.get("context_exhausted"):
            return "OUT_OF_TOKENS"
        if ev.get("session_ended"):
            return "DEAD"
        if ev.get("running") and ev.get("streaming") and ev.get("stop_button"):
            return "WORKING"
        if ev.get("session_exists") and not ev.get("streaming") and ev.get("prompt_idle"):
            return "STALLED"
        return "UNKNOWN"
    return "UNKNOWN"


EVIDENCE_CASES = [
    # Observed live 2026-09-22 ~01:23 CDT — Codex neon-drift "Continue autonomously"
    ({"product": "codex", "working_banner": True, "thinking": True,
      "cancel_button": True, "live_log": True}, "WORKING"),
    # Observed live 2026-09-22 ~01:26 CDT — Claude Code tokyo-drift-3d session
    ({"product": "claude-code", "running": True, "streaming": True,
      "stop_button": True}, "WORKING"),
    # Codex failed task seen 2026-09-22 ("Verify GitHub authentication setup")
    ({"product": "codex", "final_status": "Failed", "retry_button": True}, "DEAD"),
    # Codex merged task — worker ships its own PR (Craig 2026-09-23 ~14:07 CDT)
    ({"product": "codex", "final_status": "Merged", "retry_button": True}, "FINISHED"),
    # "Usage nearing limit" banner seen on Codex 2026-09-22
    ({"product": "codex", "usage_limit_banner": True}, "OUT_OF_TOKENS"),
    # Claude Code 5-hour limit exhausted
    ({"product": "claude-code", "session_exists": True, "usage_pct": 100,
      "prompt_idle": True}, "OUT_OF_TOKENS"),
    # Stalled: unfinished, silent, idle composer
    ({"product": "codex", "task_unfinished": True, "live_log": False,
      "composer_idle": True}, "STALLED"),
    ({"product": "claude-code", "session_exists": True, "streaming": False,
      "prompt_idle": True}, "STALLED"),
    # Login walls
    ({"product": "codex", "login_wall": True}, "LOGIN_BLOCKED"),
    ({"product": "claude-code", "login_wall": True}, "LOGIN_BLOCKED"),  # incl. unreadable hCaptcha
]


def fresh_state():
    return {"repos": {}, "sessions": {}}


def test_part1():
    fails = 0
    for ev, want in EVIDENCE_CASES:
        got = classify_evidence(ev)
        ok = got == want
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} evidence->{want}: got {got}  {ev}")
    return fails


def test_part2():
    fails = 0
    cases = [
        # (session, classification, state_setup, want_action)
        ("codex:neon-drift", "WORKING", {}, "NOTHING"),
        ("codex:neon-drift", "OUT_OF_TOKENS", {}, "FAILOVER"),
        ("claude-code:tokyo-drift-3d", "WORKING", {}, "NOTHING"),
        ("claude-code:tokyo-drift-3d", "OUT_OF_TOKENS", {}, "FAILOVER"),
        ("codex:neon-drift", "STALLED", {}, "NUDGE"),
        ("claude-code:tokyo-drift-3d", "STALLED", {}, "NUDGE"),
        ("codex:neon-drift", "DEAD", {}, "RESUME"),
        ("claude-code:tokyo-drift-3d", "DEAD", {}, "RESUME"),
        ("codex:neon-drift", "LOGIN_BLOCKED", {}, "REPORT_LOGIN"),
    ]
    for session, cls, setup, want in cases:
        st = fresh_state()
        st["sessions"][session] = dict(setup)
        action, reason = watch.decide_action(session, cls, st)
        ok = action == want
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} {session} {cls}->{want}: got {action} ({reason})")
    # nudge cooldown: nudged 10 min ago, still stalled -> NOTHING
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "last_nudge_ts": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "STALLED", st)
    ok = action == "NOTHING"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} cooldown (nudged 10m ago, STALLED)->NOTHING: got {action} ({reason})")
    # nudge cooldown expired: nudged 60 min ago, still stalled -> NUDGE again
    st["sessions"]["codex:neon-drift"] = {
        "last_nudge_ts": (datetime.now(timezone.utc) - timedelta(minutes=60)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "STALLED", st)
    ok = action == "NUDGE"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} cooldown expired (nudged 60m ago, STALLED)->NUDGE: got {action} ({reason})")
    # failover cooldown: fired 10 min ago, still out of tokens -> NOTHING
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "last_failover_ts": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "OUT_OF_TOKENS", st)
    ok = action == "NOTHING"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} failover cooldown (fired 10m ago, OUT_OF_TOKENS)->NOTHING: got {action} ({reason})")
    # failover cooldown expired: fired 200 min ago -> FAILOVER again
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "last_failover_ts": (datetime.now(timezone.utc) - timedelta(minutes=200)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "OUT_OF_TOKENS", st)
    ok = action == "FAILOVER"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} failover cooldown expired (fired 200m ago)->FAILOVER: got {action} ({reason})")
    # already failed over this episode -> NOTHING (no re-steer spam)
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "out_of_tokens_since": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
        "last_failover_ts": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "OUT_OF_TOKENS", st)
    ok = action == "NOTHING"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} already failed over this episode->NOTHING: got {action} ({reason})")
    # new episode after an old failover -> FAILOVER again
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "out_of_tokens_since": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(),
        "last_failover_ts": (datetime.now(timezone.utc) - timedelta(minutes=200)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "OUT_OF_TOKENS", st)
    ok = action == "FAILOVER"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} new episode after old failover->FAILOVER: got {action} ({reason})")

    # REBRIEF (Craig 2026-09-23): stalled, nudged 60m ago within this episode
    # (episode started 90m ago), cooldown expired -> REBRIEF, not another NUDGE
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "stall_episode_start": (datetime.now(timezone.utc) - timedelta(minutes=90)).isoformat(),
        "last_nudge_ts": (datetime.now(timezone.utc) - timedelta(minutes=60)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "STALLED", st)
    ok = action == "REBRIEF"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} stalled+nudged this episode, cooldown over->REBRIEF: got {action} ({reason})")
    # REBRIEF cooldown: rebriefed 10m ago, still stalled -> NOTHING
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "stall_episode_start": (datetime.now(timezone.utc) - timedelta(minutes=90)).isoformat(),
        "last_nudge_ts": (datetime.now(timezone.utc) - timedelta(minutes=80)).isoformat(),
        "last_rebrief_ts": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "STALLED", st)
    ok = action == "NOTHING"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} rebrief cooldown (rebriefed 10m ago)->NOTHING: got {action} ({reason})")
    # Already re-briefed this episode, cooldown expired -> NOTHING (no rebrief loop)
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "stall_episode_start": (datetime.now(timezone.utc) - timedelta(minutes=200)).isoformat(),
        "last_nudge_ts": (datetime.now(timezone.utc) - timedelta(minutes=190)).isoformat(),
        "last_rebrief_ts": (datetime.now(timezone.utc) - timedelta(minutes=60)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "STALLED", st)
    ok = action == "NOTHING"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} already rebriefed this episode->NOTHING: got {action} ({reason})")
    # Nudge from a PREVIOUS episode does not count: episode started 30m ago,
    # nudge was 60m ago (before the episode) -> NUDGE, fresh episode gets its nudge
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "stall_episode_start": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
        "last_nudge_ts": (datetime.now(timezone.utc) - timedelta(minutes=60)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "STALLED", st)
    ok = action == "NUDGE"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} nudge was previous episode->NUDGE: got {action} ({reason})")

    # FINISHED + unmerged PR -> SHIP (Craig 2026-09-23 ~14:25 CDT: whoever
    # gets to a parked PR first ships it — no ship-steering, no shipping
    # window, no backup model; the run ships it on sight when CI is green)
    st = fresh_state()
    action, reason = watch.decide_action("codex:neon-drift", "FINISHED", st)
    ok = action == "SHIP"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} finished->SHIP: got {action} ({reason})")
    # FINISHED + pr_merged -> INSPECT_MERGED (run inspects the diff, reports to
    # Craig, files new tasks or re-opens gaps)
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {"pr_merged": True}
    action, reason = watch.decide_action("codex:neon-drift", "FINISHED", st)
    ok = action == "INSPECT_MERGED"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} finished+pr_merged->INSPECT_MERGED: got {action} ({reason})")
    # FINISHED + inspected_ts set -> NOTHING (no re-flag after inspection)
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {"pr_merged": True, "inspected_ts": "2026-09-23T19:00:00+00:00"}
    action, reason = watch.decide_action("codex:neon-drift", "FINISHED", st)
    ok = action == "NOTHING"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} finished+inspected_ts->NOTHING: got {action} ({reason})")
    # FINISHED + stale legacy ship-steer ledger keys -> SHIP (old keys are
    # ignored under the ship-on-sight rule)
    st = fresh_state()
    st["sessions"]["codex:neon-drift"] = {
        "last_ship_steer_ts": (datetime.now(timezone.utc) - timedelta(minutes=20)).isoformat(),
        "ship_steer_failed_ts": (datetime.now(timezone.utc) - timedelta(minutes=60)).isoformat(),
        "last_merge_backup_ts": (datetime.now(timezone.utc) - timedelta(minutes=20)).isoformat()}
    action, reason = watch.decide_action("codex:neon-drift", "FINISHED", st)
    ok = action == "SHIP"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} finished+legacy ship ledger keys->SHIP: got {action} ({reason})")
    return fails


def test_part3():
    """Hard outcome validator (Craig 2026-09-26): every inspected task maps
    to exactly one of outcomes 1-5. Uses the REAL watch.validate_task_outcome."""
    fails = 0

    def check(task_id, facts, want=None, want_alarm=False):
        nonlocal fails
        try:
            num, label = watch.validate_task_outcome(task_id, facts)
            if want_alarm:
                fails += 1
                print(f"FAIL {task_id}: expected ALARM, got outcome {num} ({label})")
            elif num != want:
                fails += 1
                print(f"FAIL {task_id}: expected outcome {want}, got {num} ({label})")
            else:
                print(f"PASS {task_id} -> outcome {num} ({label})")
        except watch.DegradedWatchdog as e:
            if want_alarm:
                print(f"PASS {task_id} -> ALARM raised")
            else:
                fails += 1
                print(f"FAIL {task_id}: unexpected ALARM: {e}")

    # 1 closed: merged + live-verified.
    check("p3d-096", {"merged": True, "live_verified": True}, want=1)
    # merged but not live -> still open; live owner -> 2.
    check("td-058", {"merged": True, "live_verified": False,
                     "owner": "codex:tokyo-drift-3d", "owner_alive": True}, want=2)
    # merged, not live, no owner -> 3.
    check("td-x", {"merged": True, "live_verified": False}, want=3)
    # open, live owner -> 2.
    check("p3d-092", {"merged": False, "owner": "codex:neon-drift",
                      "owner_alive": True}, want=2)
    # open, owner dead -> 3 (nobody owns it).
    check("p3d-095", {"merged": False, "owner": "codex:neon-drift",
                      "owner_alive": False}, want=3)
    # open, no owner at all -> 3.
    check("p3d-088", {"merged": False}, want=3)
    # blocked on human only -> 4.
    check("td-y", {"merged": False, "blocked_human": True}, want=4)
    # blocked on external only -> 5.
    check("td-z", {"merged": False, "blocked_external": True}, want=5)
    # blocked on BOTH human and external -> multiple outcomes -> ALARM.
    check("td-both", {"merged": False, "blocked_human": True,
                      "blocked_external": True}, want_alarm=True)
    # Forbidden framings -> ALARM, never a quiet mapping.
    for framing in ("open and idle", "queued without ownership",
                    "waiting for the next cycle", "waiting for CI",
                    "waiting for Craig's verdict", "awaiting verdict"):
        check("td-framing", {"merged": False, "owner": "codex:tokyo-drift-3d",
                             "owner_alive": True, "framing": framing},
              want_alarm=True)
    return fails


def test_part4():
    """Scripted heartbeat (Craig 2026-10-02): build_heartbeat assembles
    ALERTS + JOBS + WORKERS + PENDING + STATE from recorded verdicts, queued
    actions, the pending ledger, and board rows — with inline links, defect
    names as headlines, and fold-in-rule outcome numbers."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        if not cond:
            fails += 1
            print(f"  FAIL {name}")

    state = {"sessions": {
        "codex:tokyo-drift-3d": {
            "last_classification": "WORKING",
            "last_classification_ts": "2026-10-02T18:00:00+00:00",
            "current_task": "td-119",
            "task_url": "https://chatgpt.com/codex/cloud/tasks/T1"},
        "claude-code:tokyo-drift-3d": {
            "last_classification": "FINISHED",
            "last_classification_ts": "2026-10-02T17:00:00+00:00",
            "last_task": "td-140",
            "task_url": "https://claude.ai/code/session/S1"},
    }}
    checks = {
        "transitions": ["FLIP td-137: open -> in_review [wake-validator]",
                        "FLIP td-140: in_review -> validated [notify-craig]",
                        "FLIP td-119: open -> blocked [notify-craig]"],
        "classification-health": ["STALE-RUNS=3"],
        "conflicts": ["OK no duplicate task ownership"],
        "board-check": ["BOARD-OK tokyo-drift-3d (142 rows)"],
    }
    actions = [{"type": "dispatch-codex", "task": "td-141",
                "queued_at": "2026-10-02T18:05:00+00:00"}]
    rows = [
        {"task": "td-137", "defect": "Split/merge: Shuto interchange",
         "status": "in_review", "prefix": "in_review", "owner": "", "pr": ""},
        {"task": "td-119", "defect": "Showa environment models",
         "status": "blocked on Craig: approve sign purchase", "prefix": "blocked",
         "owner": "", "pr": ""},
        {"task": "td-141", "defect": "Traffic fleet tripo rebuild",
         "status": "open", "prefix": "open", "owner": "", "pr": ""},
    ]
    pending = [
        {"game": "tokyo", "pr": 274, "task": "td-119",
         "summary": "Shuto salvage merge", "reported": False},
        {"game": "tokyo", "pr": 273, "task": "td-140",
         "summary": "UI rework", "reported": True},
    ]
    out = watch.build_heartbeat(state, checks, actions, rows, pending, "OK")
    text = "\n".join(out)

    # Sections present, in order.
    secs = ["HEARTBEAT", "ALERTS", "JOBS", "WORKERS", "STATE"]
    idx = [text.find(s) for s in secs]
    check("sections in order", all(i >= 0 for i in idx) and idx == sorted(idx))
    # in_review flip -> outcome-2 JOBS line with defect name + task link.
    check("in_review flip job",
          any("🟢 2 [td-137](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-137.md) Split/merge: Shuto interchange" in l
              for l in out))
    # validated flip -> alert, NOT a job (outcome 1, closed).
    check("validated flip alerts", "! td-140: in_review → validated — notify Craig" in out)
    check("validated flip not a job", not any("td-140" in l and l.startswith(("🟢", "🟡", "🔴")) for l in out if "JOBS" not in l and "td-140 —" in l))
    # blocked flip with human keyword -> outcome 4.
    check("blocked flip outcome 4",
          any(l.startswith("🔴 4 [td-119]") and "blocked: blocked on Craig" in l for l in out))
    # queued dispatch -> outcome-2 job with defect name.
    check("dispatch action job",
          any("🟢 2 [td-141]" in l and "Traffic fleet tripo rebuild" in l and "dispatch-codex" in l for l in out))
    # pending: unreported -> job line; reported -> count only.
    check("pending unreported job",
          any("🟢 2 [PR #274](https://github.com/doublehidenblade/tokyo-drift-3d/pull/274)" in l for l in out))
    check("pending reported not a job",
          not any("[PR #273]" in l for l in out if l.startswith("🟢")))
    check("pending count", "PENDING 2 merged-not-live" in out)
    # stale-runs=3 -> degraded-watchdog alert.
    check("stale alert", any("classifications stale 3 runs" in l for l in out))
    # workers: emoji by classification, session link, task.
    check("worker working",
          any("🟢 [codex:tokyo-drift-3d](https://chatgpt.com/codex/cloud/tasks/T1) — WORKING" in l and "td-119" in l for l in out))
    check("worker finished",
          any("🟡 [claude-code:tokyo-drift-3d](https://claude.ai/code/session/S1) — FINISHED" in l for l in out))
    # board-check verdict carried into STATE.
    check("state board line", "BOARD-OK tokyo-drift-3d (142 rows)" in out)
    # Empty run: no alerts/jobs, stale verdicts ignored.
    out2 = watch.build_heartbeat({"sessions": {}}, {}, [], [], [], None)
    t2 = "\n".join(out2)
    check("quiet run", "(none)" in t2 and "PENDING 0 merged-not-live" in t2
          and "(no check verdicts recorded this run — heartbeat is stale)" in t2)
    # Open-work fallback (Craig 2026-10-02): empty run activity must never
    # read as "no open work / game is ready". Open board rows surface under
    # JOBS with defect names; done-pending-verdict is excluded (done work).
    rows_open = [
        {"task": "td-054", "defect": "Multiplayer online", "status": "open",
         "prefix": "open", "owner": "", "pr": ""},
        {"task": "td-139", "defect": "QA round 2", "status": "in_review",
         "prefix": "in_review", "owner": "Muse", "pr": "243"},
        {"task": "td-140", "defect": "UI rework", "status": "done-pending-verdict",
         "prefix": "done-pending-verdict", "owner": "", "pr": "273"},
    ]
    out3 = watch.build_heartbeat({"sessions": {}}, {}, [], rows_open, [], None)
    t3 = "\n".join(out3)
    check("open fallback shown",
          any(l.startswith("⬜ [td-054]") and "Multiplayer online" in l
              for l in out3))
    check("fallback owner shown",
          any("td-139" in l and "(Muse)" in l for l in out3))
    check("done-pending-verdict excluded",
          "td-140" not in t3.split("JOBS")[1].split("PENDING")[0])
    check("fallback header",
          "(no run activity — open board work:)" in t3)
    check("fallback not bare none",
          not any(l == "(none)" for l in
                  t3.split("JOBS")[1].split("PENDING")[0].splitlines()))
    # Cap: 8 open rows -> 6 lines + overflow count.
    many = [{"task": f"td-{100 + i}", "defect": f"d{i}", "status": "open",
             "prefix": "open", "owner": "", "pr": ""} for i in range(8)]
    out4 = watch.build_heartbeat({"sessions": {}}, {}, [], many, [], None)
    check("fallback cap", sum(1 for l in out4 if l.startswith("⬜")) == 6
          and "…and 2 more open on the board" in out4)
    # All-blocked fallback (Craig 2026-10-02): done-pending-verdict is
    # TERMINAL (only Craig's verdict outstanding) — it must never surface
    # as "no available worker" work when every session is blocked.
    rows_ab = [
        {"task": "td-022", "defect": "Buildings clipping",
         "status": "done-pending-verdict 2026-09-30",
         "prefix": "done-pending-verdict", "owner": "", "pr": ""},
        {"task": "td-040", "defect": "webgl-smoke fails",
         "status": "blocked 2026-09-30",
         "prefix": "blocked", "owner": "", "pr": ""},
    ]
    checks_ab = {"all-blocked": ["ALL-BLOCKED True "
                                 "(codex:tokyo-drift-3d=LOGIN_BLOCKED; "
                                 "claude-code:tokyo-drift-3d=LOGIN_BLOCKED)"]}
    out5 = watch.build_heartbeat({"sessions": {}}, checks_ab, [], rows_ab, [], None)
    jobs5 = "\n".join(out5).split("JOBS")[1].split("PENDING")[0]
    check("all-blocked dpv excluded", "td-022" not in jobs5)
    check("all-blocked blocked row shown",
          any(l.startswith("🟡 3") and "td-040" in l for l in out5))
    return fails


def test_part5():
    """Verdict freshness (Craig 2026-10-02): _hb_verdicts trusts each check's
    own recording time — a fresh command must not revalidate older keys from
    a prior run."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        if not cond:
            fails += 1
            print(f"  FAIL {name}")

    now = watch.now()
    fresh = (now - timedelta(minutes=5)).isoformat()
    stale = (now - timedelta(minutes=120)).isoformat()
    state = {"run_verdicts": {
        "ts": fresh,  # shared ts bumped by the fresh check
        "checks": {"transitions": ["NO-FLIPS"],
                   "classification-health": ["STALE-RUNS=9"]},
        "check_ts": {"transitions": fresh,
                     "classification-health": stale},
    }}
    got = watch._hb_verdicts(state)
    check("fresh check kept", got.get("transitions") == ["NO-FLIPS"])
    check("stale check dropped", "classification-health" not in got)
    # Old-format data (no per-check ts) falls back to the shared ts.
    state2 = {"run_verdicts": {
        "ts": fresh,
        "checks": {"conflicts": ["OK no duplicate task ownership"]}}}
    check("legacy shared-ts fallback",
          watch._hb_verdicts(state2).get("conflicts")
          == ["OK no duplicate task ownership"])
    state3 = {"run_verdicts": {
        "ts": stale,
        "checks": {"conflicts": ["OK no duplicate task ownership"]}}}
    check("legacy stale dropped", watch._hb_verdicts(state3) == {})
    check("empty state", watch._hb_verdicts({}) == {})
    return fails


def test_part6():
    """adopt-orphans verdicts (real watch._orphan_verdict).
    The 2026-10-03 td-148..152 lesson: a `validated` board row overrides a
    stale DO NOT MERGE title — Craig's verdict is a publish gate, never a
    merge gate. Unvalidated DO NOT MERGE stays HELD for human judgment."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails += 1

    def pr(n, title, draft=False):
        return {"number": n, "title": title, "draft": draft,
                "head": {"sha": "abc1234def5678"}}

    # The exact td-149 case: validated + stale DO NOT MERGE title -> READY
    v, d = watch._orphan_verdict(
        pr(288, "DO NOT MERGE — td-149: traffic cars overlay turning wheels"),
        "validated")
    check("validated + DO NOT MERGE title -> ORPHAN-READY", v == "ORPHAN-READY")
    check("stale-title flag noted", "stale DO NOT MERGE title" in d)

    # Validated without the stale title -> READY, no flag
    v, d = watch._orphan_verdict(pr(285, "td-150: retro loading screen art"),
                                 "validated")
    check("validated, clean title -> ORPHAN-READY", v == "ORPHAN-READY")
    check("no stale-title flag when title clean", "stale" not in d)

    # DO NOT MERGE but NOT validated -> HELD, never auto-merge
    v, d = watch._orphan_verdict(
        pr(292, "DO NOT MERGE — td-101: Blender vegetation kit v2"),
        "in_review")
    check("unvalidated DO NOT MERGE -> ORPHAN-HELD", v == "ORPHAN-HELD")

    # Denylist beats everything, even validated
    v, d = watch._orphan_verdict(pr(253, "td-138 round 3 preservation"),
                                 "validated")
    check("denylisted PR -> ORPHAN-BLOCKED even if validated",
          v == "ORPHAN-BLOCKED")

    # Drafts never merge
    v, d = watch._orphan_verdict(
        {"number": 159, "title": "TD108: rebuild hero coupe", "draft": True,
         "head": {"sha": "abc1234def5678"}}, "validated")
    check("draft -> ORPHAN-DRAFT even if validated", v == "ORPHAN-DRAFT")

    # Open, no validated row, clean title -> UNKNOWN (leave alone)
    v, d = watch._orphan_verdict(pr(289, "td-150: validator verdict"), None)
    check("no board row -> ORPHAN-UNKNOWN", v == "ORPHAN-UNKNOWN")
    v, d = watch._orphan_verdict(pr(244, "td-110: rebuild orange wedge"),
                                 "in_progress")
    check("in_progress -> ORPHAN-UNKNOWN", v == "ORPHAN-UNKNOWN")

    # Case-insensitivity: lowercase "do not merge" still counts
    v, d = watch._orphan_verdict(pr(282, "td-137: split/merge (do not merge)"),
                                 "in_review")
    check("lowercase do not merge -> ORPHAN-HELD", v == "ORPHAN-HELD")
    return fails


def test_part7():
    """Part 7: _strip_dnm_prefix — stale DO NOT MERGE title repair."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails += 1

    s = watch._strip_dnm_prefix
    check("em-dash variant stripped",
          s("DO NOT MERGE \u2014 awaiting Craig's verdict")
          == "awaiting Craig's verdict")
    check("colon variant stripped",
          s("DO NOT MERGE: td-148 traffic fleet") == "td-148 traffic fleet")
    check("bracket variant stripped",
          s("[DO NOT MERGE] td-149 wheels") == "td-149 wheels")
    check("lowercase stripped", s("do not merge - foo") == "foo")
    check("bare DNM -> empty string", s("DO NOT MERGE") == "")
    check("clean title untouched",
          s("td-150: validator verdict") is None)
    check("DNM mid-title untouched",
          s("td-137: split/merge (do not merge)") is None)
    check("missing space variant untouched",
          s("DONOTMERGE foo") is None)
    return fails


def test_part8():
    """Part 8: _audit_lesson_sections — the scriptification rule on itself."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails += 1

    subs = {"heartbeat", "adopt-orphans", "evidence-audit",
            "scriptification-audit"}
    base = ("# AGENTS.md\n\n## Scriptify deterministic parts of every lesson/rule/workflow "
            "(Craig 2026-10-02 \u2014 standing rule)\nEvery lesson ships checks as subcommands.\n")

    def verdicts(sections):
        return watch._audit_lesson_sections(base + sections, subs)

    def kinds(v):
        return [k for k, _ in v]

    # Grandfathering: pre-rule lessons are not audited
    v = watch._audit_lesson_sections(
        "# AGENTS.md\n\n## Old lesson (2026-09-27)\nNo tags at all.\n" + base.split("# AGENTS.md\n\n", 1)[1],
        subs)
    check("pre-rule untagged lesson grandfathered",
          kinds(v) == [])

    # Valid SCRIPTED tag naming a real subcommand
    v = verdicts("\n## New thing (Craig 2026-10-03) [SCRIPTED: watch.py heartbeat]\nBody.\n")
    check("valid SCRIPTED tag passes", kinds(v) == ["SCRIPTIFICATION-TAGGED"])

    # Missing tag
    v = verdicts("\n## New thing (Craig 2026-10-03)\nProse only, no tag.\n")
    check("missing tag -> SCRIPTIFICATION-MISSING",
          kinds(v) == ["SCRIPTIFICATION-MISSING"])

    # SCRIPTED naming a nonexistent subcommand
    v = verdicts("\n## New thing (Craig 2026-10-03) [SCRIPTED: watch.py mind-reader]\nBody.\n")
    check("bad subcommand -> SCRIPTIFICATION-BADCMD",
          kinds(v) == ["SCRIPTIFICATION-BADCMD"])

    # Documented placeholder <cmd> is not a scripting claim — skipped
    v = verdicts("\n## New thing (Craig 2026-10-03) [SCRIPTED: watch.py scriptification-audit]\n"
                 "Format is [SCRIPTED: watch.py <cmd>].\n")
    check("placeholder <cmd> skipped, real tag passes",
          kinds(v) == ["SCRIPTIFICATION-TAGGED"])

    # Empty JUDGMENT-ONLY reason
    v = verdicts("\n## New thing (Craig 2026-10-03) [JUDGMENT-ONLY:]\nBody.\n")
    check("empty why -> SCRIPTIFICATION-NOWHY",
          kinds(v) == ["SCRIPTIFICATION-NOWHY"])

    # Valid JUDGMENT-ONLY with a why
    v = verdicts("\n## New thing (Craig 2026-10-03) [JUDGMENT-ONLY: chat formatting, not scriptable]\nBody.\n")
    check("JUDGMENT-ONLY with why passes",
          kinds(v) == ["SCRIPTIFICATION-TAGGED"])

    # Tag in body (not heading) also counts
    v = verdicts("\n## New thing (Craig 2026-10-03)\nFix [SCRIPTED: watch.py adopt-orphans] did it.\n")
    check("tag in section body counts",
          kinds(v) == ["SCRIPTIFICATION-TAGGED"])

    # Missing anchor -> NOANCHOR, not silent pass
    v = watch._audit_lesson_sections("## Something\nNo rule here.\n", subs)
    check("missing anchor -> SCRIPTIFICATION-NOANCHOR",
          kinds(v) == ["SCRIPTIFICATION-NOANCHOR"])
    return fails


if __name__ == "__main__":
    print("== Part 1: evidence -> classification ==")
    f1 = test_part1()
    print("== Part 2: classification -> action (real watch.decide_action) ==")
    f2 = test_part2()
    print("== Part 3: hard task-outcome validator (real watch.validate_task_outcome) ==")
    f3 = test_part3()
    print("== Part 4: scripted heartbeat (real watch.build_heartbeat) ==")
    f4 = test_part4()
    print("== Part 5: verdict freshness (real watch._hb_verdicts) ==")
    f5 = test_part5()
    print("== Part 6: adopt-orphans verdicts (real watch._orphan_verdict) ==")
    f6 = test_part6()
    print("== Part 7: DNM title strip (real watch._strip_dnm_prefix) ==")
    f7 = test_part7()
    print("== Part 8: scriptification audit (real watch._audit_lesson_sections) ==")
    f8 = test_part8()
    total = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8
    print(f"\n{total} failures" if total else "\nALL TESTS PASSED")
    sys.exit(1 if total else 0)
