# Tokyo Drift 3D — task board

Source of task truth: `godot/docs/tasks/td-*.md` in `doublehidenblade/tokyo-drift-3d`.
One defect = one task. A task closes ONLY when its exact defect is fixed and verified — never because siblings were fixed.

Board seeded 2026-09-23. Statuses marked `unverified` were not confirmed against a live session or merged PR — re-verify before acting.

Live site: https://doublehidenblade.github.io/tokyo-drift-3d-web/

> ID COLLISION WARNING: historical NEON records use bare `td-021`–`td-026`; Shuto records use `td-021-shuto`–`td-026-shuto` for the same numbers (Tokyo internal IDs td-021–026). Bare `td-027+` are Tokyo. Never overwrite historical NEON entries.

| Task | Defect (Craig's wording) | Status | Owner | Last update |
|---|---|---|---|---|
| td-020 | Artifact storage quota blocks CI artifact uploads (infra rework) | in_progress — fresh Codex task `task_e_6ab467a3a478832eabc7ded5555f19cd` created 2026-09-23, running at last check 23:58 UTC; scope: verify actual quota state first, CI-only fix, open PR, do not merge | codex:tokyo-drift-3d | 2026-09-23 23:58 UTC |
| td-021 | Rail/parapet contact is unrecoverable (Craig's blocker #1) | fixed_pending_verify — PR #41 merged 2026-09-23 (rail-wall-recovery); needs fixed-build evidence + Craig's phone verdict | unverified | 2026-09-23 |
| td-022 | Buildings/roads clipping into the drivable surface (systemic) | fixed_pending_verify (physical-block half only — see task file Fix section) | unverified | 2026-09-23 |
| td-023 | Track end is a huge wall; replace with checkerboard finish gate | fixed_pending_verify | unverified | 2026-09-23 |
| td-024 | Road merge/ramp geometry plainly wrong (systemic) | open (unverified beyond task file) | — | 2026-09-23 |
| td-025 | Shared kit: road texture, pause menu, traffic, trees inherit into Shuto | open (unverified; split owed per one-bug-one-task) | — | 2026-09-23 |
| td-026 | Shuto load time much longer; split into a second URL | open (unverified) | — | 2026-09-23 |
| td-027 | Shuto C1 is auto-drive only; add controls and menus | open (unverified; split owed) | — | 2026-09-23 |
| td-028 | Shuto C1 completion: texture the scene, add traffic | open (unverified; split owed) | — | 2026-09-23 |
| td-029 | Start button click freezes ~8 seconds after load | open (unverified) | — | 2026-09-23 |
| td-030 | Cut out-of-view buildings to reduce load (careful map study) | open (unverified) | — | 2026-09-23 |
| td-031 | Game end: keep driving in auto-drive with orbiting camera instead of abrupt stop | open (unverified) | — | 2026-09-23 |

Related: Shuto C1 publish — Codex Tokyo's publish runs completed 2026-09-23 but nothing shipped (branch-protection required checks blocked the worker's PR attempt); the cron later merged Shuto C1 PR #23. Verify live before claiming shipped.
