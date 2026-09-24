# NEON DRIFT — task board

Source of task truth: `todos/todoNNN/README.md` in `doublehidenblade/neon-drift`.
One defect = one task. A task closes ONLY when its exact defect is fixed and verified — never because siblings were fixed.

Board seeded 2026-09-23. Statuses marked `unverified` were not confirmed against a live session or merged PR — re-verify before acting.

Live site: https://doublehidenblade.github.io/neon-drift-web/

| Task | Todo | Defect (Craig's wording) | Status | Owner | Last update |
|---|---|---|---|---|---|
| p3d-060 | todo133 | civilian sprite view by relative player distance | in_review — codex:neon-drift finished per watchdog 2026-09-24 00:20 UTC (completed diff +269/-39); claimed PR #23 — re-verify before shipping | codex:neon-drift (task_e_6ab459d96adc832eaa6e357d4a997fd1) | 2026-09-24 00:20 UTC |
| p3d-061 | todo134 | sprite size normalization and systematic sprite CI | open — queued behind p3d-060 (likely sprite-file collision) | — | 2026-09-23 |
| p3d-062 | todo135 | civilian-vs-civilian and civilian-vs-obstacle collision | open — dispatch round 2026-09-23 unverified (no confirmed worker) | unverified | 2026-09-23 |
| p3d-063 | todo136 | overtaken civilian cars keep their own speed | open — dispatch round 2026-09-23 unverified | unverified | 2026-09-23 |
| p3d-064 | todo137 | collision boxes mapped to obstacle visual size | open — dispatch round 2026-09-23 unverified | unverified | 2026-09-23 |
| p3d-065 | todo138 | better water (not observed on live build) | open — dispatch round 2026-09-23 unverified | unverified | 2026-09-23 |
| p3d-066 | todo139 | remove the broken secondary roads | open — dispatch round 2026-09-23 unverified | unverified | 2026-09-23 |
| p3d-067 | todo140 | roadblock | open — dispatch round 2026-09-23 unverified (capture on live first, then ground physically or remove) | unverified | 2026-09-23 |
| p3d-068 | todo141 | floating torii gate | open — dispatch round 2026-09-23 unverified | unverified | 2026-09-23 |
| p3d-070 | todo143 | player car sprite replaced with Slipstream-style 12-view set (Craig: prioritized) | open — filed 2026-09-24, awaiting dispatch | — | 2026-09-24 |
| p3d-069 | todo142 | neon complex roads (second map, proof of concept) | open — GATED: only after civilian-car cluster + visual fixes (p3d-062..068, bridge 128-2) are fixed and verified | — | 2026-09-23 |

Related (not a task file): bridge **128-2** (wires/poles too thin) — `fixed_pending_verify` in qa-registry, still visible on Craig's live screenshot 2026-09-23 09:42 CDT after PR #19. Included in the 2026-09-23 dispatch round (unverified). Do not close without Craig's phone verdict.

QA 2026-09-24: Craig could not verify p3d-060 on his phone — overtaken cars disappear into the back too quickly when passed (p3d-063 defect, open). p3d-060 closure blocked on his verdict until p3d-063 fixed. Player car was NOT part of the p3d-060 fix — p3d-070 filed for the 12-view player sprite.

Priority order (Craig 2026-09-23): civilian-car sprite/traffic cluster (p3d-060..064) → visual fixes (p3d-065..068 + bridge 128-2) → p3d-069 neon complex roads.
