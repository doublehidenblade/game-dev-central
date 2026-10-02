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


if __name__ == "__main__":
    print("== Part 1: evidence -> classification ==")
    f1 = test_part1()
    print("== Part 2: classification -> action (real watch.decide_action) ==")
    f2 = test_part2()
    print("== Part 3: hard task-outcome validator (real watch.validate_task_outcome) ==")
    f3 = test_part3()
    total = f1 + f2 + f3
    print(f"\n{total} failures" if total else "\nALL TESTS PASSED")
    sys.exit(1 if total else 0)
