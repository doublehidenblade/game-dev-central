# Worker registry

Who is working on what, right now. One task per worker; never two workers on one task.
Seeded from the agent watchdog state 2026-09-24 00:20 UTC. Entries marked `unverified` were not confirmed in this pass — re-verify before steering.

| Session | Platform | Current task | State (watchdog) | Last seen (UTC) |
|---|---|---|---|---|
| codex:neon-drift | Codex cloud | p3d-060 — relative frame selection for civilian cars | FINISHED (completed diff +269/-39; task page failed to render, no nudge sent) | 2026-09-24 00:20 |
| codex:tokyo-drift-3d | Codex cloud | td-020 — artifact storage quota (task_e_6ab467a3a478832eabc7ded5555f19cd) | unverified — fresh task 2026-09-23, running at 23:58 UTC check | 2026-09-23 23:58 |
| codex:tokyo-drift-3d | Codex cloud | Shuto C1 publish (task_e_6ab436cecab4832eb514c6da1034bf6d) | FINISHED — worker PR blocked by branch protection; cron merged PR #23 | 2026-09-24 00:00 |
| claude-code:tokyo-drift-3d | Claude Code | unverified — was td-010 C1 signs/PBR (PR #38); something merged by cron | WORKING (streaming tool calls) | 2026-09-24 00:00 |
| claude-code:tokyo-drift-3d-textures | Claude Code | imagegen 6 PNGs — STALLED: GEMINI_API_KEY not set, 0/6 done; duplicate-session alert (2 extra live sessions + error-state setup session) | STALLED | 2026-09-23 23:05 |

| codex:td109-sedan | Codex subagent | td-109 — reference-grounded four-door sedan | UNVERIFIED after Muse handoff — branch feat/td-109-dr30-sedan observed, PR not found; session not visible | 2026-09-28 22:04 |
| codex:td110-wedge | Codex subagent | td-110 — reference-grounded orange wedge (`taxi.glb`) | UNVERIFIED after Muse handoff — branch feat/td-109-dr30-sedan observed, PR not found; session not visible | 2026-09-28 22:04 |
| codex:td111-van | Codex subagent | td-111 — reference-grounded compact van | UNVERIFIED after Muse handoff — branch feat/td-109-dr30-sedan observed, PR not found; session not visible | 2026-09-28 22:04 |

| codex `/root/tenjin_worker` | Game-development execution environment; `gpt-6-astra` / `max` requested and accepted by model-selecting dispatch | td-209 — bounded Tenjin live buildings / modular placement; sole implementation author | Author work frozen for independent review: runtime `6f7818b4`, evidence `bcaf46b8`; draft PR489 and whole-city backlog491; no source edits while validator owns verdict. Runtime internals not separately attested | 2026-10-08 00:23 |
| codex `/root/tenjin_validator` | Game-development execution environment; `gpt-6-astra` / `max` requested and accepted by separate model-selecting dispatch; runtime internals unexposed | td-209 — independent acceptance audit; exclusive verdict/report ownership | Reviewing frozen `bcaf46b8` evidence / `6f7818b4` runtime and public QA mirror `8a1f87cd`; no implementation edits, merge, Actions or deployment | 2026-10-08 00:30 |
| codex `/root/tenjin_validator` | Fresh independent Game-development reviewer; `gpt-6-astra` / `max` requested and accepted by model-selecting dispatch; runtime internals unexposed | td-209 — all five canonical criteria; source/evidence/visual/clearance/export audit | Reviewing frozen runtime `6f7818b4` and evidence `bcaf46b8`; owns only new review report/logs and task verdict/status, never implementation fixes. No main edit, merge, Actions or deployment | 2026-10-08 00:23 |

Rules: never nudge a working session; never duplicate a live session; fresh session per task (never accumulate a week of transcript); stale sessions sync/rebase onto main before resuming; stop after 2 identical failures and report.
