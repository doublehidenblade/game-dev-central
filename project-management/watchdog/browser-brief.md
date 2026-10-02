# Browser brief — coding-agent session watchdog

You are checking the health of Craig's two AI coding sessions. This is READ-ONLY
classification unless the "ACTION MODE" section at the bottom is explicitly enabled
by the run that hands you this brief. The browser task itself never merges
code, never publishes, never changes repository settings: merges happen in
the main run via the github skill — you only type instructions to the
session. Never type into any
composer except in ACTION MODE.

## Logins

Both sites already have saved logins and an active browser session. Reuse them.
If you land on a login page, a re-auth prompt, or a CAPTCHA/bot check: STOP. Do
not attempt to solve anything, do not wait on it — report LOGIN_BLOCKED for that
product and move on to the other product. (The claude.ai magic-link flow can show
an hCaptcha whose image is unreadable to automation.)

## PART 1 — Codex (Tokyo Drift 3D only — NEON DRIFT archived 2026-09-29, do NOT open or classify it)

1. Open https://chatgpt.com/codex/cloud
2. Check ONE environment only: **tokyo-drift-3d** (repo doublehidenblade/tokyo-drift-3d — this one builds the Shuto Expressway C1 map). The **neon-drift** env is archived and retired; never open it, never classify it, never type into its composer.
3. For the tokyo-drift-3d environment, open its most recent task and classify it:
   - **WORKING** — shows "Working on your task" banner AND "Thinking" status AND
     a loading progressbar AND a "Cancel task" button AND a live terminal log
     (log lines are recent/appearing). The task list shows "Thinking" for it.
   - **FINISHED** — the task's run completed (completed/finished status, completed
     diff shown, idle composer). This is DONE, not stalled — never nudge or
     resume a finished task. If the final status literally says "Merged", the
     worker already shipped its own PR — still report FINISHED, and put the
     merged PR number/title in the note so the run inspects it and reports to Craig.
   - **STALLED** — a task exists and is not finished (no "Failed"/
     "Cancelled" final status, no completed diff shown) but there is no activity:
     no "Working on your task" banner, no live log movement, an idle composer
     waiting with nothing happening. Do NOT call a task "stalled" just because
     its last run finished — a finished run with a completed diff is done, not stalled.
   - **DEAD** — a final status is shown ("Failed after Ns", "Cancelled")
     with a "Retry" button instead of "Cancel task". A task whose final status
     is "Merged" is NOT dead — that is a finished worker that shipped its own
     work; classify it FINISHED.
   - **OUT_OF_TOKENS** — a "Usage nearing limit" banner or usage-limit messaging
     is visible; the session cannot take more work right now.
4. Report one line, in this exact format:
   `CODEX env=tokyo-drift-3d state=<WORKING|STALLED|DEAD|OUT_OF_TOKENS|LOGIN_BLOCKED|FINISHED> task_url=<full task URL or "none"> note=<one line: task title, age, what you saw>`

## PART 2 — Claude Code (Tokyo Drift)

1. Open https://claude.ai/code
2. In the Recents list, find the session for the **tokyo-drift-3d** workspace
   (workspace label "Default tokyo-drift-3d", repo doublehidenblade/tokyo-drift-3d).
3. Open the most recent session in that workspace and classify it:
   - **WORKING** — "Running" in the Recents list AND a "Currently streaming
     message" block with live tool calls AND a "Stop" button next to the Prompt box.
   - **FINISHED** — the session is idle, its last message is complete, and the
     agent signaled the task done (summary shown). DONE, not stalled — never
     nudge or resume a finished session.
   - **STALLED** — a session exists but nothing is streaming: no "Running"
     indicator, no live tool calls, the last message is complete and the Prompt
     box sits idle with open work pending.
   - **DEAD** — the session ended/errored with no way to continue in it.
   - **OUT_OF_TOKENS** — usage shows at/near 100% of the 5-hour limit or the
     context window is exhausted; the session cannot take more work right now.
4. Report, in this exact format:
   `CLAUDE state=<WORKING|STALLED|DEAD|OUT_OF_TOKENS|LOGIN_BLOCKED|FINISHED> session_url=<full session URL or "none"> note=<one line>`

## Duplicate-session guard

When listing tasks/sessions, note whether MORE THAN ONE live session exists for
the same workspace. EXCEPTION (Craig-authorized 2026-09-22, corrected same day):
the tokyo-drift-3d workspace legitimately has THREE live sessions — the main dev
session (branch td016-texture-request-and-td018-occlusion), a Shuto Expressway C1
loop map session (Craig-ordered; idle awaiting his design answers), and a
texture-imagegen session (chat title contains "texture imagegen", owns ONLY the
6 PNGs under godot/assets/pbr/stylized/). Do NOT report this trio as an
unauthorized duplicate and never try to close one. Classify all three: emit
three lines, `CLAUDE ... note=main-dev`, `CLAUDE ... note=shuto-c1`, and
`CLAUDE ... note=texture-imagegen`. Any FOURTH live session is still a duplicate
to report.
If you ever see two live sessions elsewhere, report it in the note — the recovery
rules below must never create a second live session.

---

## STEER / UNBLOCK MODE (Craig-permitted, 2026-09-22)

Craig gave the watchdog standing permission to steer the coding agents in conversation and to unblock them when a permission/settings issue is what is actually stopping them. Use this mode only when the obstacle is a permission or a settings flag, not for routine progress:

- **Unblock on the agent's behalf:** navigate to the page that grants the permission and grant it.
  Examples: on github.com open the repo/org settings to open up browser use for the agent; in ChatGPT or Claude settings, enable the permission the agent is asking for.
- **Steer in conversation:** type a short, specific instruction in the session's composer explaining what was fixed or what to do next. Leave a working session alone — this is "mostly not needed if they are still working."

Keep the same boundaries: never merge code, never publish, never change repository settings beyond granting the agent its own access, never solve the game's code yourself through this route. Report any unblock/steer action to Craig in the run's final message.

ACTION MODE is enabled with one of: ACTION=nudge-codex | ACTION=resume-codex |
ACTION=nudge-claude | ACTION=resume-claude | ACTION=steer-codex |
ACTION=steer-claude, plus a target URL or workspace.

Hard rules for every action: re-verify the session is still in the stated state
before acting (if it is now WORKING, do nothing and report NO_ACTION_WORKING).
Never create a second live session — check the task list / Recents first.
Type exactly `continue` and nothing else. After sending, confirm the session
accepted it (composer cleared / new run started) and report ACTION_DONE.

- **nudge-codex**: open the target task URL. If still STALLED, type `continue`
  in the composer textbox at the bottom ("Request changes or ask a question") and send.
- **resume-codex**: on https://chatgpt.com/codex/cloud, re-check the task list —
  if a live task exists in the target environment, do nothing (NO_ACTION_WORKING).
  Otherwise start a NEW Codex task in the target environment and send `continue`.
  The ACTION names the environment: ACTION=resume-codex env=tokyo-drift-3d (neon-drift is archived — never resume it).
- **nudge-claude**: open the target session URL. If still STALLED, type `continue`
  in the "Prompt" textbox and send.
- **resume-claude**: on https://claude.ai/code, re-check Recents — if a live
  session exists for tokyo-drift-3d, do nothing (NO_ACTION_WORKING). Otherwise
  resume/start Claude Code, select the tokyo-drift-3d workspace, and send `continue`.
- **steer-codex**: FAILOVER steering (Craig 2026-09-23 — a sibling session ran out
  of tokens; this sibling takes over its priority work). Open the target task URL.
  If the session is currently WORKING (live run in progress), do nothing and
  report NO_ACTION_WORKING — never steal a working session. Otherwise type the
  provided MESSAGE verbatim in the composer and send. Report STEER_DONE.
- **steer-claude**: FAILOVER steering (Craig 2026-09-23 — a sibling session ran out
  of tokens; this sibling takes over its priority work). Open the target session
  URL. If the session is currently streaming/working, do nothing and report
  NO_ACTION_WORKING — never steal a working session. Otherwise type the provided
  MESSAGE verbatim in the "Prompt" box and send. Report STEER_DONE.
