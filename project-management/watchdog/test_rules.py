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
    # in_review flip -> explicit-word JOBS line with defect name + task link.
    check("in_review flip job",
          any("🟢 OPEN — assigned · [td-137](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-137.md) Split/merge: Shuto interchange" in l
              for l in out))
    # validated flip -> alert, NOT a job (outcome 1, closed).
    check("validated flip alerts", "! td-140: in_review → validated — notify Craig" in out)
    check("validated flip not a job", not any("td-140" in l and l.startswith(("🟢", "🟡", "🔴")) for l in out if "JOBS" not in l and "td-140 —" in l))
    # blocked flip with human keyword -> explicit words, not a digit.
    check("blocked flip words",
          any(l.startswith("🔴 BLOCKED — needs you · [td-119]") and "blocked: blocked on Craig" in l for l in out))
    # queued dispatch -> explicit-word job with defect name.
    check("dispatch action job",
          any("🟢 OPEN — assigned · [td-141]" in l and "Traffic fleet tripo rebuild" in l and "dispatch-codex" in l for l in out))
    # pending: unreported -> job line; reported -> count only.
    check("pending unreported job",
          any("🟢 OPEN — assigned · [PR #274](https://github.com/doublehidenblade/tokyo-drift-3d/pull/274)" in l for l in out))
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
          any(l.startswith("🟡 OPEN — no worker · [td-054]") and "Multiplayer online" in l
              for l in out3))
    check("fallback owned words",
          any(l.startswith("🟢 OPEN — assigned · [td-139]") and "(Muse)" in l
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
    check("fallback cap", sum(1 for l in out4 if l.startswith("🟡 OPEN — no worker")) == 6
          and "…and 2 more open on the board" in out4)
    # Five-outcome set (Craig 2026-09-25, words per 2026-10-04): HELD pending
    # (merged, evidence rejected) is open-and-assigned, never closed.
    pending_held = [{"game": "tokyo", "pr": 282, "task": "td-137",
                     "status": "HELD", "hold_reason": "inspector rejected",
                     "reported": False}]
    out6 = watch.build_heartbeat({"sessions": {}}, {}, [], [], pending_held,
                                  None)
    check("held pending words",
          any(l.startswith("🔴 OPEN — assigned · [PR #282]") for l in out6))
    # Every JOBS line states its outcome explicitly in words with color
    # coding — no bare digits.
    import re as _re
    _oc = (r"^([🟢🔴] OPEN — assigned|🟡 OPEN — (assigned|no worker)|"
           r"🔴 BLOCKED — (needs you|external|unclear)) · ")
    for tag, oo in (("main", out), ("fallback", out3), ("held", out6)):
        jobs = "\n".join(oo).split("JOBS")[1].split("PENDING")[0].splitlines()
        job_lines = [l for l in jobs if l and not l.startswith("(")]
        check(f"outcome words {tag}",
              all(_re.match(_oc, l) for l in job_lines)
              and len(job_lines) > 0)
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
          any(l.startswith("🟡 OPEN — no worker") and "td-040" in l for l in out5))
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


def test_part9():
    """Part 9: evidence cheat-checks (real watch._find_duplicate_images,
    watch._pair_findings, watch._is_tiny). Deterministic audits for the
    hourly task-evidence inspector."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails += 1

    # Duplicate frames: same bytes under two names (the td-137 ch2150 case —
    # one frame reused as evidence for two criteria).
    d = watch._find_duplicate_images([
        ("c1/td137-criterion-1-after.png", "aaa"),
        ("c3/td137-criterion-3-after.png", "aaa"),
        ("c1/other.png", "bbb"),
    ])
    check("same bytes two names -> one dup group",
          list(d.values()) == [["c1/td137-criterion-1-after.png",
                                "c3/td137-criterion-3-after.png"]])
    check("no dups -> empty",
          watch._find_duplicate_images([("a.png", "aaa"), ("b.png", "bbb")]) == {})
    # Same path twice is not a duplicate (re-listed dir), only distinct paths.
    check("same path twice -> not flagged",
          watch._find_duplicate_images([("a.png", "aaa"), ("a.png", "aaa")]) == {})

    # Pair findings: after without before.
    m = watch._pair_findings(["x-after.png", "y-before.png", "y-after.png"])
    check("after without before -> flagged", m == ["x-after.png"])
    check("complete pairs -> clean",
          watch._pair_findings(["y-before.png", "y-after.PNG"]) == [])
    check("case-insensitive stems", watch._pair_findings(
        ["TD-1-Before.png", "td-1-after.png"]) == [])

    # Tiny images.
    check("399px max dim -> tiny", watch._is_tiny(399, 200))
    check("400px max dim -> ok", not watch._is_tiny(400, 200))
    check("large -> ok", not watch._is_tiny(1920, 1080))
    return fails


def test_part10():
    """Part 10: EVIDENCE-VOID dark-void heuristic (real
    watch._void_dark_fraction, watch._is_void_suspect). td-171: flags
    Blender dark-studio void renders as VOID-SUSPECT for the hourly
    task-evidence-inspector's vision pass — triage flag, never a verdict."""
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails += 1

    from PIL import Image
    import io

    def png_bytes(color, size=(100, 100), lit_frac=0.0):
        im = Image.new("RGB", size, color)
        if lit_frac:
            import random
            random.seed(7)
            px = im.load()
            n = int(size[0] * size[1] * lit_frac)
            for _ in range(n):
                px[random.randrange(size[0]),
                   random.randrange(size[1])] = (200, 180, 120)
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        return buf.getvalue()

    # Void-render profile: near-black navy backdrop (luminance ~20), like the
    # td-119 criterion-1 void pair (measured darkfrac 0.85/0.88 on real files).
    df = watch._void_dark_fraction(png_bytes((13, 20, 41)))
    check("void backdrop -> darkfrac ~1.0", df is not None and df > 0.95)
    check("void backdrop -> suspect", watch._is_void_suspect(df))

    # In-engine night street profile: dark sky but lit windows/road —
    # replicates td-119-criterion-3-after (measured 0.67 on the real file).
    df2 = watch._void_dark_fraction(png_bytes((13, 20, 41), lit_frac=0.35))
    check("night street -> darkfrac ~0.65",
          df2 is not None and 0.55 < df2 < 0.75)
    check("night street -> not suspect", not watch._is_void_suspect(df2))

    # Threshold boundary behavior.
    check("0.80 -> suspect", watch._is_void_suspect(0.80))
    check("0.79 -> not suspect", not watch._is_void_suspect(0.79))
    check("None -> not suspect", not watch._is_void_suspect(None))

    # Garbage bytes -> None, never a crash.
    check("bad bytes -> None",
          watch._void_dark_fraction(b"not an image") is None)
    return fails



# Public-safe replay fixtures and integration tests for the supported coordinator.
import copy
import contextlib
import io
import json
import pathlib
import socket
import subprocess
import unittest
from unittest import mock
import coordinator
import coordinator_cli

COORDINATOR_NOW = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
COORDINATOR_REPO = "example/game"
COORDINATOR_HEAD = "1" * 40


def coordinator_seal(snapshot):
    """Synthetic source receipts for tests ONLY; not a production collector."""
    snapshot["sources"] = []
    for repo, head in snapshot["repositories"].items():
        for table in coordinator.TABLES:
            ids = [r["id"] for r in snapshot[table] if r["repository"] == repo]
            snapshot["sources"].append({
                "id": repo + ":" + table, "kind": table, "repository": repo,
                "source_repository": repo, "ref_sha": head,
                "observed_at": snapshot["observed_at"], "read_status": "ok",
                "pagination": {"pages_read": 1, "items_seen": len(ids), "exhausted": True},
                "ids": ids})
    return snapshot


def coordinator_fixture():
    repo, head = COORDINATOR_REPO, COORDINATOR_HEAD
    snapshot = {"version": 1, "observed_at": COORDINATOR_NOW.isoformat(),
                "repositories": {repo: "0" * 40}, "sources": [],
                **{kind: [] for kind in coordinator.TABLES}}
    snapshot["policies"] = [{"id": "policy", "repository": repo, "triggers_checked": True,
        "push_runs_actions": False, "push_deploys": False,
        "merge_runs_actions": False, "merge_deploys": False}]
    snapshot["tasks"] = [{"id": "task-a", "repository": repo, "head_sha": head,
        "status": "open", "owner_id": None, "project": "sample", "author_id": "author",
        "needs": [], "criteria": ["criterion-1"], "required_checks": ["unit"],
        "requirements": {op: {"capabilities": [op], "model": "frontier-example",
            "effort": "high", "runtime_confirmation_required": True}
            for op in coordinator.OPERATIONS[1:]}}]
    snapshot["board"] = [{k: snapshot["tasks"][0][k] for k in ("id", "repository", "head_sha", "status", "owner_id")}]
    snapshot["branches"] = [{"id": "task-a-branch", "repository": repo, "task_id": "task-a", "head_sha": head}]
    snapshot["requests"] = [{"id": "approved-work", "repository": repo, "task_id": "*", "project": "*",
        "operations": list(coordinator.OPERATIONS), "executors": ["*"], "kind": "standing",
        "state": "active", "authority_verified": True, "evidence": "Synthetic authorized source receipt"}]
    snapshot["executors"] = [{"id": "native", "repository": repo, "owner_id": "reviewer",
        "kind": "native", "state": "available", "capabilities": list(coordinator.OPERATIONS),
        "observed_model": "frontier-example", "observed_effort": "high", "runtime_confirmed": True,
        "resume_task": None}]
    return coordinator_seal(snapshot)


def coordinator_add_review(snapshot, accepted=False):
    repo, head = COORDINATOR_REPO, COORDINATOR_HEAD
    snapshot["tasks"][0]["status"] = "in_review"
    pr = {"id": repo + "#1", "repository": repo, "task_id": "task-a", "head_sha": head,
          "author_id": "author", "state": "open", "review_ids": [], "check_ids": []}
    snapshot["prs"] = [pr]
    if accepted:
        pr["review_ids"] = ["review-1"]
        pr["check_ids"] = ["check-1"]
        snapshot["reviews"] = [{"id": "review-1", "repository": repo, "task_id": "task-a",
            "pr_id": pr["id"], "head_sha": head, "observed_at": COORDINATOR_NOW.isoformat(),
            "reviewer_id": "independent-validator", "verdict": "pass",
            "criteria": {"criterion-1": {"result": "pass", "evidence": "qa/synthetic-unit-report.txt"}}}]
        snapshot["checks"] = [{"id": "check-1", "repository": repo, "task_id": "task-a",
            "pr_id": pr["id"], "head_sha": head, "observed_at": COORDINATOR_NOW.isoformat(),
            "name": "unit", "result": "pass"}]
    return coordinator_seal(snapshot)


@contextlib.contextmanager
def coordinator_forbid_io(reads=None):
    """Legacy operation-layer unit fixtures only; not production evidence proof.

    The PR396 fixture has deliberately fake SHAs. Isolate the newly added proof
    boundary here while preserving every original ownership/stop/operation
    assertion. Unmocked end-to-end proof and route tests live in
    test_evidence_policy.py; there is no production skip flag or test identity.
    """
    def read_only(path, mode="r", *args, **kwargs):
        if mode == "r" and reads is not None and path in reads:
            return io.StringIO(reads[path])
        raise AssertionError("forbidden filesystem access")
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(coordinator, "_policy_gate", side_effect=lambda snapshot, task, operation, at:
            {"status": "ACCEPTABLE" if operation == "completion" else "ADMISSIBLE", "issues": []}))
        stack.enter_context(mock.patch("builtins.open", side_effect=read_only))
        for path in ("socket.socket", "socket.create_connection", "subprocess.Popen", "subprocess.run",
                     "urllib.request.urlopen", "os.makedirs", "os.mkdir", "os.remove", "os.unlink",
                     "os.rename", "os.replace", "os.system", "pathlib.Path.write_text", "pathlib.Path.write_bytes"):
            stack.enter_context(mock.patch(path, side_effect=AssertionError("forbidden external effect")))
        for name in ("load_state", "save_state", "_load_pending_actions", "_save_pending_actions", "_gh", "_gh_api", "get", "_build_replacement_brief", "_capture_verdicts", "_record_verdict"):
            stack.enter_context(mock.patch.object(watch, name, side_effect=AssertionError("forbidden legacy effect")))
        yield


class CoordinatorEnforcementTests(unittest.TestCase):
    def evaluate(self, snapshot=None, at=COORDINATOR_NOW):
        snapshot = snapshot if snapshot is not None else coordinator_fixture()
        original = copy.deepcopy(snapshot)
        with coordinator_forbid_io():
            result = coordinator.evaluate(snapshot, at)
        self.assertEqual(snapshot, original, "evaluation mutated its input")
        return result

    def actions(self, snapshot, operation=None):
        return [a for a in self.evaluate(snapshot)["actions"] if operation is None or a["operation"] == operation]

    def test_available_native_survives_codex_capacity_block(self):
        s = coordinator_fixture()
        codex = {**s["executors"][0], "id": "codex", "owner_id": "codex-owner", "kind": "codex", "state": "unavailable"}
        s["executors"].insert(0, codex)
        s["blockers"] = [{"id": "quota", "repository": COORDINATOR_REPO, "task_id": "*",
            "operations": ["*"], "executors": ["codex"], "kind": "capacity", "reason": "quota exhausted"}]
        result = self.evaluate(coordinator_seal(s))
        self.assertEqual([a["executor_id"] for a in result["actions"]], ["native"])
        self.assertEqual(result["status"], "ACTION_REQUIRED")

    def test_scoped_publication_holds_do_not_block_code_or_second_task(self):
        s = coordinator_fixture()
        s["tasks"][0]["needs"] = ["upload", "deploy"]
        second = copy.deepcopy(s["tasks"][0]); second["id"] = "task-b"
        s["tasks"].append(second)
        s["board"].append({k: second[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
        s["branches"].append({**s["branches"][0], "id": "task-b-branch", "task_id": "task-b"})
        s["blockers"] = [{"id": "hold-a", "repository": COORDINATOR_REPO, "task_id": "task-a",
            "operations": ["*"], "executors": ["*"], "kind": "hold", "reason": "task hold"},
            {"id": "upload-hold", "repository": COORDINATOR_REPO, "task_id": "task-b",
            "operations": ["upload", "deploy"], "executors": ["*"], "kind": "hold", "reason": "publication hold"}]
        self.assertEqual([(a["task_id"], a["operation"]) for a in self.actions(coordinator_seal(s))], [("task-b", "implementation")])

    def test_unfiled_ask_is_admission_without_implementation_candidate(self):
        s = coordinator_fixture()
        s["tasks"].clear(); s["board"].clear(); s["branches"].clear()
        s["requests"] = [{**s["requests"][0], "id": "unfiled-ask", "task_id": None,
                           "kind": "ask", "project": "sample", "operations": ["admission"]}]
        actions = self.actions(coordinator_seal(s))
        self.assertEqual([(a["task_id"], a["operation"]) for a in actions], [("request:unfiled-ask", "admission")])

    def test_unfiled_admission_holds_are_task_scoped(self):
        s = coordinator_fixture()
        s["tasks"].clear(); s["board"].clear(); s["branches"].clear()
        template = {**s["requests"][0], "task_id": None, "kind": "ask",
                    "project": "sample", "operations": ["admission"]}
        s["requests"] = [{**template, "id": "ask-a"}, {**template, "id": "ask-b"}]
        s["blockers"] = [{"id": "admission-hold", "repository": COORDINATOR_REPO,
            "task_id": "request:ask-a", "operations": ["admission"], "executors": ["*"],
            "kind": "hold", "reason": "admission dependency"}]
        self.assertEqual([a["task_id"] for a in self.actions(coordinator_seal(s))], ["request:ask-b"])

    def test_review_pending_and_stale_board_produce_exact_head_verification(self):
        result = self.evaluate(coordinator_add_review(coordinator_fixture()))
        self.assertEqual(result["actions"][0]["operation"], "verification")
        self.assertEqual(result["actions"][0]["head_sha"], COORDINATOR_HEAD)
        self.assertTrue(result["reconciliations"])

    def test_implementation_owner_preserved_independent_review_available(self):
        s = coordinator_add_review(coordinator_fixture())
        s["tasks"][0]["owner_id"] = "author"; s["tasks"][0]["needs"] = ["implementation"]
        s["board"][0]["owner_id"] = "author"
        s["executors"].append({**s["executors"][0], "id": "author-executor", "owner_id": "author", "state": "busy"})
        s["owners"] = [{"id": "owner", "repository": COORDINATOR_REPO, "task_id": "task-a",
            "operation": "implementation", "owner_id": "author", "executor_id": "author-executor", "state": "active"}]
        actions = self.actions(coordinator_seal(s))
        self.assertEqual([(a["operation"], a["executor_id"]) for a in actions], [("verification", "native")])

    def test_owned_continuation_requires_existing_exact_executor(self):
        s = coordinator_fixture()
        s["tasks"][0]["owner_id"] = s["board"][0]["owner_id"] = "reviewer"
        s["owners"] = [{"id": "owner", "repository": COORDINATOR_REPO, "task_id": "task-a",
            "operation": "implementation", "owner_id": "reviewer", "executor_id": "native", "state": "active"}]
        self.assertFalse(self.actions(coordinator_seal(s)))
        s["executors"][0]["resume_task"] = "task-a"
        self.assertTrue(self.actions(s))

    def test_native_unknown_or_requested_model_is_not_attestation(self):
        for changes in ({"state": "unknown"}, {"runtime_confirmed": False},
                        {"observed_model": "weaker-example"}, {"observed_effort": "low"},
                        {"capabilities": []}):
            with self.subTest(changes=changes):
                s = coordinator_fixture(); s["executors"][0].update(changes)
                self.assertFalse(self.actions(s))
        s = coordinator_fixture(); s["executors"][0]["requested_model"] = "frontier-example"
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")

    def test_acceptance_is_independent_complete_and_exact(self):
        base = coordinator_add_review(coordinator_fixture(), accepted=True)
        self.assertEqual([a["operation"] for a in self.actions(base)], ["merge"])
        mutations = [lambda s: s["reviews"][0].update(head_sha="2"*40),
                     lambda s: s["reviews"][0].update(reviewer_id="author"),
                     lambda s: s["reviews"][0].update(criteria={}),
                     lambda s: s["reviews"][0]["criteria"]["criterion-1"].update(evidence=""),
                     lambda s: s["reviews"][0]["criteria"]["criterion-1"].update(result="fail"),
                     lambda s: s["checks"][0].update(head_sha="2"*40),
                     lambda s: s["checks"][0].update(result="fail")]
        for mutation in mutations:
            s = copy.deepcopy(base); mutation(s)
            self.assertFalse(self.actions(s, "merge"))

    def test_terminal_board_and_merged_pr_do_not_restart_completed_work(self):
        for status in ("closed", "merged"):
            s = coordinator_fixture(); s["board"][0]["status"] = status
            result = self.evaluate(s)
            self.assertFalse(result["actions"])
            self.assertEqual(result["status"], "INPUT_REQUIRED")
        s = coordinator_fixture()
        s["prs"] = [{"id": COORDINATOR_REPO + "#1", "repository": COORDINATOR_REPO,
            "task_id": "task-a", "head_sha": COORDINATOR_HEAD, "author_id": "author",
            "state": "merged", "review_ids": [], "check_ids": []}]
        result = self.evaluate(coordinator_seal(s))
        self.assertFalse(result["actions"])
        self.assertEqual(result["status"], "INPUT_REQUIRED")
        s["tasks"][0]["status"] = "merged"
        s["tasks"][0]["needs"] = ["implementation", "upload"]
        result = self.evaluate(s)
        self.assertEqual([a["operation"] for a in result["actions"]], ["upload"])
        self.assertTrue(result["warnings"])
        s = coordinator_add_review(coordinator_fixture(), True)
        s["tasks"][0].update(status="merged", needs=["implementation"])
        s["reviews"][0]["verdict"] = "fail"
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        self.assertFalse(self.actions(s))

    def test_terminal_conflict_does_not_suppress_other_verified_task(self):
        s = coordinator_fixture(); second = copy.deepcopy(s["tasks"][0]); second["id"] = "task-b"
        s["tasks"].append(second)
        s["board"].append({k: second[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
        s["branches"].append({**s["branches"][0], "id": "task-b-branch", "task_id": "task-b"})
        s["board"][0]["status"] = "merged"
        result = self.evaluate(coordinator_seal(s))
        self.assertEqual([a["task_id"] for a in result["actions"]], ["task-b"])
        self.assertTrue(result["warnings"])

    def test_individual_read_freshness_is_separate_from_old_evidence_date(self):
        base = coordinator_add_review(coordinator_fixture(), True)
        for table in ("reviews", "checks"):
            base[table][0]["performed_at"] = (COORDINATOR_NOW - timedelta(days=2)).isoformat()
        original = copy.deepcopy(base)
        self.assertEqual([a["operation"] for a in self.actions(base)], ["merge"])
        self.assertEqual(base, original, "old performed_at must not be rewritten")
        for table in ("reviews", "checks"):
            for age in (timedelta(days=2), timedelta(minutes=15)):
                s = copy.deepcopy(base)
                # Keep this counterexample valid under the original schema too:
                # it must fail for stale reads, not for an unknown optional field.
                for kind in ("reviews", "checks"):
                    s[kind][0].pop("performed_at")
                s[table][0]["observed_at"] = (COORDINATOR_NOW - age).isoformat()
                result = self.evaluate(s)
                self.assertFalse(result["actions"])
                self.assertEqual(result["status"], "INPUT_REQUIRED")
            s = copy.deepcopy(base); s[table][0]["observed_at"] = (COORDINATOR_NOW - timedelta(minutes=5)).isoformat()
            action = self.actions(s)[0]
            self.assertEqual(action["expires_at"], (COORDINATOR_NOW + timedelta(minutes=10)).isoformat())
            target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
            with coordinator_forbid_io():
                self.assertEqual(coordinator.revalidate(s, action, target, COORDINATOR_NOW + timedelta(minutes=10))["status"], "NO_GO")
        s = copy.deepcopy(base)
        s["reviews"].append({**copy.deepcopy(s["reviews"][0]), "id": "review-2"})
        s["prs"][0]["review_ids"].append("review-2")
        s["reviews"][0]["observed_at"] = (COORDINATOR_NOW - timedelta(minutes=5)).isoformat()
        self.assertEqual([a["operation"] for a in self.actions(coordinator_seal(s))], ["merge"])
        s = copy.deepcopy(base); s["checks"][0]["performed_at"] = (COORDINATOR_NOW + timedelta(seconds=1)).isoformat()
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")

    def test_stale_acceptance_read_keeps_unrelated_coding_available(self):
        s = coordinator_add_review(coordinator_fixture(), True)
        second = copy.deepcopy(s["tasks"][0]); second.update(id="task-b", status="open")
        s["tasks"].append(second)
        s["board"].append({k: second[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
        s["branches"].append({**s["branches"][0], "id": "task-b-branch", "task_id": "task-b"})
        s["reviews"][0]["observed_at"] = (COORDINATOR_NOW - timedelta(days=2)).isoformat()
        result = self.evaluate(coordinator_seal(s))
        self.assertEqual([(a["task_id"], a["operation"]) for a in result["actions"]], [("task-b", "implementation")])
        self.assertTrue(result["warnings"])

    def test_supported_native_selection_does_not_claim_runtime_attestation(self):
        s = coordinator_fixture(); requirement = s["tasks"][0]["requirements"]["implementation"]
        requirement.update(model="gpt-6-astra", effort="xhigh", runtime_confirmation_required=False)
        ex = s["executors"][0]
        ex.update(observed_model=None, observed_effort=None, runtime_confirmed=False,
                  selected_model="gpt-6-astra", selected_effort="xhigh", selection_verified=True,
                  selection_evidence="Synthetic current supported catalog plus admitted exact selection")
        self.assertEqual([a["operation"] for a in self.actions(s)], ["implementation"])
        self.assertFalse(ex["runtime_confirmed"])
        self.assertIsNone(ex["observed_model"])
        requirement["runtime_confirmation_required"] = True
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        requirement["runtime_confirmation_required"] = False
        for key in ("selected_model", "selected_effort", "selection_verified", "selection_evidence"):
            ex.pop(key)
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        ex.update(selected_model="gpt-6-astra", selected_effort="xhigh",
                  selection_verified=False, selection_evidence="Requested only")
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        ex.update(selection_verified=True, selection_evidence="Verified catalog/admission", selected_model="weaker-model")
        self.assertFalse(self.actions(s))
        ex.update(selected_model="gpt-6-astra", runtime_confirmed=True,
                  observed_model="weaker-model", observed_effort="xhigh")
        self.assertFalse(self.actions(s), "known runtime mismatch must not be hidden by selection")
        ex.update(runtime_confirmed=False, observed_model=None, observed_effort=None, capabilities=[])
        self.assertFalse(self.actions(s), "selection is no substitute for tools")

    def test_conflicting_same_head_reviews_require_reconciliation(self):
        s = coordinator_add_review(coordinator_fixture(), accepted=True)
        s["reviews"].append({**copy.deepcopy(s["reviews"][0]), "id": "review-2", "verdict": "fail"})
        s["prs"][0]["review_ids"].append("review-2")
        result = self.evaluate(coordinator_seal(s))
        self.assertFalse(result["actions"])
        self.assertEqual(result["status"], "INPUT_REQUIRED")

    def disputed_review(self, state):
        s = coordinator_add_review(coordinator_fixture(), accepted=True)
        s["tasks"][0].update(status=state, needs=["verification", "implementation", "upload", "merge", "deploy"])
        s["board"][0]["status"] = state
        s["prs"][0]["state"] = "merged" if state == "merged" else "open"
        s["reviews"].append({**copy.deepcopy(s["reviews"][0]), "id": "review-2",
                              "reviewer_id": "another-independent-validator", "verdict": "fail"})
        s["prs"][0]["review_ids"].append("review-2")
        return coordinator_seal(s)

    def test_disputed_acceptance_preserves_explicit_review_only(self):
        for state in ("in_review", "merged"):
            with self.subTest(state=state):
                s = self.disputed_review(state)
                result = self.evaluate(s)
                self.assertEqual([a["operation"] for a in result["actions"]], ["verification"])
                self.assertEqual(result["status"], "ACTION_REQUIRED")
                self.assertTrue(any("contradictory same-head" in w for w in result["warnings"]))
                self.assertFalse(coordinator.acceptance(s["tasks"][0], s["prs"][0], s)[0])
                for blocked in result["blocked"]:
                    self.assertIn("ACCEPTANCE_RECONCILIATION_REQUIRED", blocked["reasons"])
                blocked_ops = {b["operation"] for b in result["blocked"]}
                self.assertTrue({"upload", "merge", "deploy"} <= blocked_ops)
                if state == "in_review":
                    self.assertIn("implementation", blocked_ops)

    def test_known_conflict_survives_removal_of_verification_need(self):
        for state in ("in_review", "merged"):
            for needs in ([], ["upload"], ["implementation", "upload", "merge", "deploy"]):
                with self.subTest(state=state, needs=needs):
                    s = self.disputed_review(state)
                    s["tasks"][0]["needs"] = needs
                    result = self.evaluate(s)
                    self.assertFalse(result["actions"])
                    self.assertEqual(result["status"], "INPUT_REQUIRED")
                    self.assertTrue(any("contradictory same-head" in w for w in result["warnings"]))

    def test_disputed_review_retains_source_owner_capability_and_stop_gates(self):
        mutations = {
            "authorization": lambda s: s["requests"][0]["operations"].remove("verification"),
            "author": lambda s: s["executors"][0].update(owner_id="author"),
            "capability": lambda s: s["executors"][0]["capabilities"].remove("verification"),
            "ownership": lambda s: s["board"][0].update(owner_id="another-owner"),
            "owner-read": lambda s: next(r for r in s["sources"] if r["kind"] == "owners").update(read_status="unreadable"),
            "source-read": lambda s: next(r for r in s["sources"] if r["kind"] == "prs").update(read_status="unreadable"),
            "stale-review": lambda s: s["reviews"][0].update(observed_at=(COORDINATOR_NOW - timedelta(minutes=16)).isoformat()),
            "board-stop": lambda s: s["board"][0].update(status="paused"),
            "cancelled": lambda s: s["requests"][0].update(state="cancelled"),
        }
        for state in ("in_review", "merged"):
            for case, mutate in mutations.items():
                with self.subTest(state=state, case=case):
                    s = self.disputed_review(state); mutate(s)
                    result = self.evaluate(s)
                    self.assertFalse(result["actions"])
                    self.assertEqual(result["status"], "INPUT_REQUIRED")
            for kind in ("stop", "denial", "security"):
                s = self.disputed_review(state)
                s["blockers"] = [{"id": "review-hold", "repository": COORDINATOR_REPO,
                    "task_id": "task-a", "operations": ["verification"], "executors": ["*"],
                    "kind": kind, "reason": "Explicit read-only verification restriction"}]
                self.assertFalse(self.actions(coordinator_seal(s)))

    def test_disputed_review_is_scoped_and_receipts_still_revalidate(self):
        for state in ("in_review", "merged"):
            s = self.disputed_review(state)
            second = copy.deepcopy(s["tasks"][0]); second.update(id="task-b", status="open", needs=[])
            s["tasks"].append(second)
            s["board"].append({k: second[k] for k in ("id", "repository", "head_sha", "status", "owner_id")})
            s["branches"].append({**s["branches"][0], "id": "task-b-branch", "task_id": "task-b"})
            result = self.evaluate(coordinator_seal(s))
            self.assertEqual([(a["task_id"], a["operation"]) for a in result["actions"]],
                             [("task-a", "verification"), ("task-b", "implementation")])
            action = result["actions"][0]
            target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
            with coordinator_forbid_io():
                self.assertEqual(coordinator.revalidate(s, action, target, COORDINATOR_NOW)["status"], "GO")
                s["reviews"][1]["criteria"]["criterion-1"]["evidence"] = "qa/changed-review.txt"
                self.assertEqual(coordinator.revalidate(s, action, target, COORDINATOR_NOW)["status"], "NO_GO")

    def test_manifest_omissions_and_unreadability_never_claim_idle(self):
        mutations = [lambda s: s.pop("sources"), lambda s: s.update(sources=[]),
                     lambda s: s["sources"][2]["pagination"].update(exhausted=False),
                     lambda s: s["sources"][2].update(read_status="unreadable"),
                     lambda s: s["sources"][2]["ids"].append("omitted-task"),
                     lambda s: s.update(complete=True), lambda s: s.update(candidates=[]),
                     lambda s: s["board"].clear()]
        for mutation in mutations:
            s = coordinator_fixture(); mutation(s)
            result = self.evaluate(s)
            self.assertEqual(result["status"], "INPUT_REQUIRED")
            self.assertFalse(result["actions"])

    def test_complete_empty_scope_is_no_work_only_with_all_receipts(self):
        s = coordinator_fixture(); s["tasks"].clear(); s["board"].clear(); s["branches"].clear()
        self.assertEqual(self.evaluate(coordinator_seal(s))["status"], "IDLE")
        s["sources"].pop()
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")

    def test_safe_action_coexists_with_unrelated_unknown_scope(self):
        s = coordinator_fixture()
        s["repositories"]["example/unobserved-game"] = "3" * 40
        result = self.evaluate(s)
        self.assertEqual(result["status"], "ACTION_REQUIRED")
        self.assertEqual(len(result["actions"]), 1)
        self.assertTrue(result["warnings"])

    def test_unknown_acceptance_does_not_stop_separately_authorized_code(self):
        s = coordinator_fixture()
        next(src for src in s["sources"] if src["kind"] == "reviews")["read_status"] = "unreadable"
        result = self.evaluate(s)
        self.assertEqual(result["status"], "ACTION_REQUIRED")
        self.assertEqual(result["actions"][0]["operation"], "implementation")
        self.assertTrue(result["warnings"])
        s = coordinator_add_review(s, True)
        next(src for src in s["sources"] if src["kind"] == "reviews")["read_status"] = "unreadable"
        self.assertFalse(self.actions(s, "merge"))

    def test_bad_times_sha_repository_duplicate_and_review_omission(self):
        mutations = [lambda s: s.update(observed_at="2026-10-09T12:00:00"),
                     lambda s: s.update(observed_at="malformed"),
                     lambda s: s.update(observed_at="2026-10-09T12:01:00Z"),
                     lambda s: s["sources"][0].update(observed_at="2026-10-09T12:01:00Z"),
                     lambda s: s["tasks"][0].update(head_sha="1"*7),
                     lambda s: s["tasks"][0].update(repository="wrong/repository"),
                     lambda s: s["sources"][0].update(ref_sha="2"*40),
                     lambda s: s["tasks"].append(copy.deepcopy(s["tasks"][0])),
                     lambda s: s["sources"].append(copy.deepcopy(s["sources"][0]))]
        for mutation in mutations:
            s = coordinator_fixture(); mutation(s)
            self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        self.assertEqual(self.evaluate(coordinator_fixture(), COORDINATOR_NOW + timedelta(minutes=16))["status"], "INPUT_REQUIRED")
        s = coordinator_add_review(coordinator_fixture(), True); s["reviews"].clear()
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        s = coordinator_add_review(coordinator_fixture(), True); s["reviews"][0]["pr_id"] = "example/elsewhere#1"
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")

    def test_stops_denials_cancellation_and_frozen_projects_preserved(self):
        for kind in ("hold", "stop", "cancelled", "denial", "security"):
            s = coordinator_fixture()
            s["blockers"] = [{"id": "stop", "repository": COORDINATOR_REPO, "task_id": "task-a",
                "operations": ["implementation"], "executors": ["*"], "kind": kind, "reason": "explicit stop"}]
            self.assertFalse(self.actions(coordinator_seal(s)))
        s = coordinator_fixture(); s["requests"].append({**s["requests"][0], "id": "cancelled", "task_id": "task-a", "state": "cancelled"})
        self.assertFalse(self.actions(coordinator_seal(s)))
        for project in ("shuto", "neon-drift"):
            s = coordinator_fixture(); s["tasks"][0]["project"] = project
            self.assertFalse(self.actions(s))
        s = coordinator_fixture(); s["tasks"][0]["status"] = "cancelled"
        self.assertFalse(self.actions(s))

    def test_frozen_unfiled_ask_and_board_stops_cannot_be_laundered(self):
        s = coordinator_fixture()
        s["tasks"].clear(); s["board"].clear(); s["branches"].clear()
        s["requests"] = [{**s["requests"][0], "id": "ask", "task_id": None,
                           "kind": "ask", "project": "shuto", "operations": ["admission"]}]
        self.assertFalse(self.actions(coordinator_seal(s)))
        for status in ("cancelled", "paused", "done-pending-verdict"):
            s = coordinator_fixture(); s["board"][0]["status"] = status
            result = self.evaluate(s)
            self.assertFalse(result["actions"])
            self.assertEqual(result["status"], "INPUT_REQUIRED")

    def test_unknown_branch_and_ownership_conflicts_require_reconciliation(self):
        s = coordinator_fixture(); s["branches"][0]["task_id"] = None
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")
        s = coordinator_fixture(); s["board"][0]["owner_id"] = "unreconciled-owner"
        self.assertFalse(self.actions(s))
        s = coordinator_fixture(); s["tasks"][0]["status"] = "blocked"
        s["tasks"][0]["needs"] = ["implementation"]
        self.assertEqual(self.evaluate(s)["status"], "INPUT_REQUIRED")

    def test_denial_cannot_be_narrowed_to_evade_on_another_executor(self):
        s = coordinator_fixture()
        s["blockers"] = [{"id": "denied", "repository": COORDINATOR_REPO, "task_id": "task-a",
            "operations": ["implementation"], "executors": ["native"], "kind": "denial", "reason": "denied"}]
        self.assertEqual(self.evaluate(coordinator_seal(s))["status"], "INPUT_REQUIRED")

    def test_unknown_branches_do_not_block_exact_read_only_review(self):
        s = coordinator_add_review(coordinator_fixture(), True)
        s["tasks"][0]["needs"] = ["verification", "implementation", "upload", "merge"]
        s["branches"].append({"id": "unmapped", "repository": COORDINATOR_REPO,
                              "task_id": None, "head_sha": "e" * 40})
        result = self.evaluate(coordinator_seal(s))
        self.assertEqual([a["operation"] for a in result["actions"]], ["verification"])
        self.assertTrue(result["warnings"])
        for table in ("owners", "prs"):
            bad = copy.deepcopy(s)
            next(src for src in bad["sources"] if src["kind"] == table)["read_status"] = "unreadable"
            self.assertFalse(self.actions(bad), "readonly exception must retain ownership/source gates")
        s["blockers"] = [{"id": "review-stop", "repository": COORDINATOR_REPO,
            "task_id": "task-a", "operations": ["verification"], "executors": ["*"],
            "kind": "stop", "reason": "explicit verification stop"}]
        self.assertFalse(self.actions(coordinator_seal(s)))

    def test_post_merge_verification_resolves_source_without_reacceptance(self):
        s = coordinator_add_review(coordinator_fixture())
        s["tasks"][0].update(status="merged", needs=["verification", "implementation", "merge"])
        s["board"][0]["status"] = "merged"; s["prs"][0]["state"] = "merged"
        result = self.evaluate(coordinator_seal(s))
        self.assertEqual([a["operation"] for a in result["actions"]], ["verification"])
        self.assertEqual(result["actions"][0]["head_sha"], s["prs"][0]["head_sha"])
        self.assertTrue(result["warnings"], "duplicate implementation remains rejected")
        s["executors"][0]["owner_id"] = "author"
        self.assertFalse(self.actions(s), "post-merge work still requires independence")

    def test_missing_post_merge_source_never_returns_false_idle(self):
        base = coordinator_add_review(coordinator_fixture())
        base["tasks"][0].update(status="merged", needs=["verification"])
        base["board"][0]["status"] = "merged"; base["prs"][0]["state"] = "merged"
        for mutation in (lambda s: s["prs"][0].update(head_sha="e" * 40),
                         lambda s: s["prs"][0].update(state="closed"),
                         lambda s: s["prs"].clear()):
            s = copy.deepcopy(base); mutation(s)
            result = self.evaluate(coordinator_seal(s))
            self.assertFalse(result["actions"])
            self.assertEqual(result["status"], "INPUT_REQUIRED")
        s = coordinator_fixture();s["tasks"][0]["needs"] = ["verification"]
        s["blockers"] = [{"id": "code-hold", "repository": COORDINATOR_REPO,
            "task_id": "task-a", "operations": ["implementation"], "executors": ["*"],
            "kind": "hold", "reason": "hold code"}]
        result = self.evaluate(coordinator_seal(s))
        self.assertEqual(result["status"], "INPUT_REQUIRED")
        self.assertTrue(any("exact review source" in warning for warning in result["warnings"]))

    def test_publication_triggers_and_deploy_never_granted_by_code_permission(self):
        s = coordinator_fixture(); s["tasks"][0]["needs"] = ["upload", "deploy"]
        s["policies"][0]["push_runs_actions"] = True
        self.assertEqual([a["operation"] for a in self.actions(s)], ["implementation"])
        s = coordinator_add_review(coordinator_fixture(), True); s["policies"][0]["merge_deploys"] = True
        self.assertFalse(self.actions(s, "merge"))

    def test_decision_replay_is_bound_to_target_owner_sha_inputs_and_freshness(self):
        base = coordinator_fixture(); action = self.actions(base)[0]
        target = {k: action[k] for k in ("task_id", "operation", "executor_id", "owner_id", "head_sha")}
        with coordinator_forbid_io():
            self.assertEqual(coordinator.revalidate(base, action, target, COORDINATOR_NOW)["status"], "GO")
            self.assertEqual(coordinator.revalidate(base, action, {**target, "operation": "upload"}, COORDINATOR_NOW)["status"], "NO_GO")
            self.assertEqual(coordinator.revalidate(base, action, target, COORDINATOR_NOW + timedelta(minutes=16))["status"], "NO_GO")
        for mutate in (lambda s: s["executors"][0].update(owner_id="changed"),
                       lambda s: s["tasks"][0].update(head_sha="2"*40),
                       lambda s: s["requests"][0].update(state="cancelled"),
                       lambda s: s["tasks"][0].update(owner_id="someone")):
            s = copy.deepcopy(base); mutate(s)
            with coordinator_forbid_io():
                self.assertEqual(coordinator.revalidate(s, action, target, COORDINATOR_NOW)["status"], "NO_GO")

    def test_all_cli_aliases_use_shared_evaluator_and_never_capture_state(self):
        s = coordinator_fixture(); action = self.actions(s)[0]
        reads = {"snapshot.json": json.dumps(s), "decision.json": json.dumps(action)}
        for command in coordinator_cli.ALIASES:
            args = ["--snapshot", "snapshot.json"]
            if command == "dispatch-guard":
                args += ["--decision", "decision.json", "--task", action["task_id"],
                         "--operation", action["operation"], "--executor", action["executor_id"],
                         "--owner", action["owner_id"], "--head", action["head_sha"]]
            with self.subTest(command=command), coordinator_forbid_io(reads), \
                    mock.patch.object(coordinator, "evaluate", wraps=coordinator.evaluate) as shared, \
                    mock.patch.object(coordinator_cli, "datetime") as clock, \
                    mock.patch.object(sys, "argv", ["watch.py", command] + args), \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                clock.now.return_value = COORDINATOR_NOW
                with self.assertRaises(SystemExit) as exit_info:
                    watch.main()
                self.assertEqual(exit_info.exception.code, 3 if command == "idle-defect-check" else 0)
                self.assertTrue(shared.called, "alias bypassed shared evaluator")
                self.assertIn(json.loads(stdout.getvalue())["status"], {"ACTION_REQUIRED", "GO"})

    def test_aliases_without_snapshot_and_retired_routes_fail_closed(self):
        for command in coordinator_cli.ALIASES | coordinator_cli.RETIRED:
            for route in ("main", "callable"):
                with self.subTest(command=command, route=route), coordinator_forbid_io(), \
                        mock.patch.object(sys, "argv", ["watch.py", command]), \
                        contextlib.redirect_stdout(io.StringIO()) as stdout:
                    with self.assertRaises(SystemExit) as exit_info:
                        if route == "main":
                            watch.main()
                        else:
                            getattr(watch, "cmd_" + command.replace("-", "_"))([])
                    self.assertEqual(exit_info.exception.code, 2)
                    self.assertEqual(json.loads(stdout.getvalue())["status"], "INPUT_REQUIRED")

    def test_cli_malformed_options_are_structured_input_required(self):
        for command in coordinator_cli.ALIASES:
            with coordinator_forbid_io(), contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(coordinator_cli.run(command, ["--snapshot"], COORDINATOR_NOW), 2)
                self.assertEqual(json.loads(out.getvalue())["status"], "INPUT_REQUIRED")

    def test_cli_rejects_malformed_duplicate_json_without_legacy_fallback(self):
        for data in ("{", '{"version":1,"version":1}', '{"version":NaN}'):
            with coordinator_forbid_io({"bad.json": data}), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(coordinator_cli.run("coordinator-plan", ["--snapshot", "bad.json"], COORDINATOR_NOW), 2)


def test_part11():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CoordinatorEnforcementTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return len(result.failures) + len(result.errors)



def test_part12():
    """flagship-waiting timestamp handling (2026-10-10 independent review of
    PR461, residual P2 defects): unknown waiting-since age must not establish
    the 48h threshold (no parked=999h false positive), and naive timestamps
    must be normalized to UTC consistently instead of crashing on
    aware-minus-naive subtraction. Exercises the REAL
    watch.cmd_flagship_waiting with stubbed board/task-file/state."""
    import io
    from contextlib import redirect_stdout
    from datetime import datetime, timezone, timedelta
    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails += 1

    TASK_FILE = "## Dispatch recommendation\nRecommended model: flagship\nEffort: L\n"

    def run(rows, task_files, notes):
        def fake_board(game):
            return rows

        def fake_task_file(repo_full, path):
            task = path.rsplit("/", 1)[-1].replace(".md", "")
            return task_files.get(task, "")

        def fake_state():
            return {"workers": {}, "sessions": {}, "notes": notes}

        old = (watch._board_rows, watch._task_file_text, watch.load_state)
        watch._board_rows = fake_board
        watch._task_file_text = fake_task_file
        watch.load_state = fake_state
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                watch.cmd_flagship_waiting(["tokyo-drift-3d"])
            return buf.getvalue()
        finally:
            (watch._board_rows, watch._task_file_text,
             watch.load_state) = old

    def row(task, last_update):
        return {"task": task, "defect": "x", "status": "open — placeholder",
                "prefix": "open", "owner": "\u2014", "pr": "",
                "last_update": last_update}

    now = datetime.now(timezone.utc)
    naive_10h = (now - timedelta(hours=10)).replace(tzinfo=None).isoformat()
    aware_50h = (now - timedelta(hours=50)).isoformat()
    naive_50h = (now - timedelta(hours=50)).replace(tzinfo=None).isoformat()
    aware_10h = (now - timedelta(hours=10)).isoformat()

    flagship = {"td-991": TASK_FILE, "td-992": TASK_FILE, "td-993": TASK_FILE,
                "td-994": TASK_FILE, "td-995": TASK_FILE, "td-996": TASK_FILE,
                "td-997": TASK_FILE}

    # P2 #1: unknown age (empty / em-dash / invalid Last update, no state
    # note) must not establish the 48h threshold.
    for tid, lu in (("td-991", ""), ("td-992", "\u2014"),
                    ("td-993", "not-a-date")):
        try:
            out = run([row(tid, lu)], flagship, {})
            crashed = False
        except Exception as e:  # noqa: BLE001
            out, crashed = "", True
            print(f"  exception: {e!r}")
        check(f"P2#1 {tid} no crash", not crashed)
        check(f"P2#1 {tid} no FLAGSHIP-WAITING verdict",
              f"FLAGSHIP-WAITING {tid}" not in out)
        check(f"P2#1 {tid} no parked=999h", "parked=999h" not in out)
        check(f"P2#1 {tid} reported as unknown-age",
              f"FLAGSHIP-UNKNOWN-AGE {tid}" in out)

    # P2 #2: naive state-note timestamp must not crash (normalized to UTC).
    try:
        out = run([row("td-994", "")],
                  flagship,
                  {"td-994 waiting-for-flagship":
                   {"ts": naive_10h, "note": "waiting-for-flagship"}})
        crashed = False
    except Exception as e:  # noqa: BLE001
        out, crashed = "", True
        print(f"  exception: {e!r}")
    check("P2#2 naive state-note ts no crash", not crashed)
    check("P2#2 10h-old naive note not parked",
          "FLAGSHIP-WAITING td-994" not in out)

    # Naive board last-update normalized to UTC: 50h-old naive date parks.
    try:
        out = run([row("td-995", naive_50h)], flagship, {})
        crashed = False
    except Exception as e:  # noqa: BLE001
        out, crashed = "", True
        print(f"  exception: {e!r}")
    check("naive board last_update no crash", not crashed)
    check("naive 50h-old board date parks",
          "FLAGSHIP-WAITING td-995 parked=50h" in out)

    # Positive control: aware 50h-old last-update parks with real hours.
    out = run([row("td-996", aware_50h)], flagship, {})
    check("aware 50h-old last-update parks",
          "FLAGSHIP-WAITING td-996 parked=50h" in out)

    # Recency control: aware 10h-old last-update is not parked.
    out = run([row("td-997", aware_10h)], flagship, {})
    check("aware 10h-old last-update not parked",
          "FLAGSHIP-WAITING td-997" not in out)

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
    print("== Part 9: evidence cheat-checks (duplicates, pairs, tiny) ==")
    f9 = test_part9()
    print("== Part 10: EVIDENCE-VOID dark-void heuristic ==")
    f10 = test_part10()
    print("== Part 11: scoped coordinator enforcement and no-side-effect CLI ==")
    f11 = test_part11()
    print("== Part 12: flagship-waiting timestamp handling (real watch.cmd_flagship_waiting) ==")
    f12 = test_part12()
    total = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8 + f9 + f10 + f11 + f12
    print(f"\n{total} failures" if total else "\nALL TESTS PASSED")
    sys.exit(1 if total else 0)
