# Tokyo Drift 3D — task board

Source of task truth: `godot/docs/tasks/td-*.md` in `doublehidenblade/tokyo-drift-3d`.
One defect = one task. A task closes ONLY when its exact defect is fixed and verified — never because siblings were fixed.

Backfilled 2026-09-25 from the task files. 2026-09-25 reprioritization (Craig): online competitive play on the 3D base map is the sole priority. All non-multiplayer rows are paused/stashed. td-050–td-054 are the multiplayer milestone; td-055 done. Per Craig 2026-09-25, this table is the SOURCE OF TRUTH for task status — workers update it via PR (PR-based edits avoid merge conflicts).

Live site: https://doublehidenblade.github.io/tokyo-drift-3d-web/

> ID COLLISION WARNING: historical NEON records use bare `td-021`–`td-026`; Shuto records use `td-021-shuto`–`td-026-shuto` for the same numbers (Tokyo internal IDs td-021–026). Bare `td-027+` are Tokyo. Never overwrite historical NEON entries.

| Task | Defect (Craig's wording) | Status | Owner | PR | Last update |
|---|---|---|---|---|---|
| td-001 | Stitch assembly: HWx3 + connector + BSx3 + bridge in Godot | done | — | — | 2026-09-25 |
| td-002 | Drive integration: vehicle + waypoints + lap logic on stitched world | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-003 | Stitch verification: 7-angle screenshots + drive-through | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-004 | Stitch report to Craig with public links | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-005 | Bay Strait visual polish: starry sky + ground plane + water | done | — | — | 2026-09-25 |
| td-006 | Stitch visual polish: lighting + connector proof + BS ground fix | abandoned | — | — | 2026-09-25 |
| td-007 | Combined bridge-centerpiece scene: harbor -> 90deg ramp -> bridge -> commercial | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-008 | Living city, material response and dependable phone driving | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-009 | Grounded world, stable manual steering and stronger race-car art | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-010 | Finish td009 acceptance and guard manual curved-road steering | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-011 | Immediate race entry, recovery, Tokyo street detail and native review | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-012 | Anime expressway: painted 2D city backdrop, occluded near field | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-013 | Reflection coverage, turn dressing, AI art pass, finish state, tuning menu | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-014 | Live-site confirmed; art, finish/opponents, containment, roads, perf, audio | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-020 | Artifact storage quota blocks CI artifact uploads (infra rework) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-021 | Rail/parapet contact is unrecoverable (Craig's blocker #1) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-022 | Buildings/roads clipping into the drivable surface (systemic) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-023 | Track end is a huge wall; replace with checkerboard finish gate | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-024 | Road merge/ramp geometry plainly wrong (systemic) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-025 | Shared kit: road texture, pause menu, traffic, trees inherit into Shuto | MERGED 2026-09-24 (PR #45, merge 5d0ddad by main agent via Git Data API fallback — normal… | — | — | 2026-09-25 |
| td-026 | Shuto load time much longer; split into a second URL | LIVE 2026-09-25 ~06:24Z — second URL https://doublehidenblade.github.io/tokyo-drift-3d-shu… | — | — | 2026-09-25 |
| td-027 | Shuto C1 is auto-drive only; add controls and menus | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-028 | Shuto C1 completion: texture the scene, add traffic | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-029 | Start button click freezes ~8 seconds after load | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-030 | Cut out-of-view buildings to reduce load (careful map study) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-031 | Game end: keep driving in auto-drive with orbiting camera instead of abrupt stop | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-032 | Loading screen: show "30M/502M downloaded" during the download step | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-033 | Rail collision box doesn't match the car model (visual clipping into rail) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-034 | webgl-smoke "Verify prepared entry" step fails intermittently with no printed error | merged 2026-09-25 (PR #77, squash 7a80d63d0049, shipped by cron) — all 17 smoke tests rout… | — | — | 2026-09-25 |
| td-035 | asymmetric near-head-on rail recovery: left-side hit stalls at 0.13 m/s vs right-side 13.56 m/s | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-036 | publish merged td-033/td-035 rail fixes | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-037 | fix WebGL smoke resource leak (blocks td-024 publish) | merged (PR #62, worker doublehidenblade 2026-09-25T04:16Z; test-harness audio-stop fix, no… | — | — | 2026-09-25 |
| td-038 | Harbor base map has no texture except road and bridge | merged — PR #65 merged 2026-09-24T23:33:14Z, published via #66, live record #67 | — | — | 2026-09-25 |
| td-039 | Big building in the middle of the Shuto road | merged (PR #64, watchdog cron 2026-09-24; conflict with main self-resolved) — inspected +… | — | — | 2026-09-25 |
| td-040 | webgl-smoke "Verify prepared entry and local crash recovery" fails repo-wide | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-041 | player car reverted back to self driving (phone QA 2026-09-24) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-042 | opponent cars hitting walls, bad navigation (phone QA 2026-09-24) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | Codex | — | 2026-09-25 |
| td-043 | pause menu missing items, buttons too small (phone QA 2026-09-24) | merged (PR #75 squash-merged 2026-09-25 10:13Z by watchdog cron; live via publish-web — im… | — | — | 2026-09-25 |
| td-044 | 3 roads still clipping into the Shuto road (phone QA 2026-09-24) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-045 | textures, props, signages to fill the Shuto scene (phone QA 2026-09-24) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-046 | Shuto second URL never published: publish-game.yml fails on stale candidate pointer | merged 2026-09-25 ~10:40Z — recovery-record PR #72 merged by watchdog cron; live screensho… | — | — | 2026-09-25 |
| td-047 | Shuto road network regressed: splits/merges/overpass gone, stub roads cut off mid-air (phone QA 2026-09-25) | merged — PR #79 squash-merged by cron 2026-09-25T18:1xZ as 4a36d33 (CI green export+smoke)… | — | — | 2026-09-25 |
| td-048 | Shuto C1 section-end road visibly terminates mid-air in player view (Craig QA 2026-09-25) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |
| td-049 | player car too large; shrink to opponent car size (phone QA 2026-09-25) | paused 2026-09-25 — Craig reprioritized to online multiplayer; stashed, resume later | — | — | 2026-09-25 |

Related: Shuto C1 publish — the second Shuto URL (https://doublehidenblade.github.io/tokyo-drift-3d-shuto-web/) is live per td-026. Verify live before claiming shipped.
| td-050 | Online multiplayer: signaling server (room codes + WebRTC signaling) | merged 2026-09-25 (PR #81) | — | PR #81 | 2026-09-26 |
| td-051 | Online multiplayer: Godot WebRTC netcode core (Net autoload) | merged 2026-09-25 (PR #82) | — | PR #82 | 2026-09-26 |
| td-052 | Online multiplayer: lobby UI (host room / join by code) | merged 2026-09-25 (PR #83) | — | PR #83 | 2026-09-26 |
| td-053 | Online multiplayer: race replication (cars, laps, countdown, results) | merged 2026-09-25 (PR #85) | — | PR #85 | 2026-09-26 |
| td-054 | Online multiplayer: 2–4 player integration test (queued behind signaling deploy) | in_progress | watchdog-subagent (refired 2026-09-26T08:35Z) | — | 2026-09-26 |
| td-055 | Player car speed increase (top_speed_scale 1.0 → 1.3) | done | Muse | — | 2026-09-25 |
| td-056 | Perf: harbor map stutters on start and on bridge (Shuto does not) | merged 2026-09-25 (PR #84) | — | PR #84 | 2026-09-26 |
| td-057 | Signaling wire-key mismatch: server speaks t, client speaks type — converge on one key | merged 2026-09-26 (PR #90) — live verify pending under td-059 | — | PR #90 | 2026-09-26 |
| td-058 | net.gd never answers server ping — peers reaped after ~60s | merged 2026-09-26 (PR #89, 01:11Z) — heartbeat pong, live-verified under td-059 | Codex | PR #89 | 2026-09-26 |
| td-059 | Multiplayer button missing on the live site — PUBLISHED 2026-09-26 (de15deec), LIVE-VERIFIED: button visible, rooms XEB67Y/BQ5VRJ created, 2-player join w/ peer-joined, 75s+ survival (4 heartbeats), WebRTC SDP/ICE flowing, +30% speed (1.3) live | done | Muse | PR #96 | 2026-09-26 |
| td-060 | webgl-smoke "Verify ordinary loading and immediate race entry" fails repo-wide: entry.mjs hard-coded tap (360,607) hits SHUTO C1 after the MULTIPLAYER button shifted the menu layout | merged 2026-09-26 (PR #95, 05:20Z) — keyboard-shortcut race entry; PR #94 closed unmerged | Muse (watchdog failover) | PR #95 | 2026-09-26 |
