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
| td-054 | Online multiplayer: 2–4 player integration test | open — Codex task created & started 2026-09-26 20:09Z for FRESH full acceptance (signaling restored; prior Phase-3 probe failures td-062..td-065 merged live) | Codex Tokyo | [task](https://chatgpt.com/codex/cloud/tasks/task_e_6ab8263c22c0832eb73a9535eee7b3e2) | 2026-09-26 |
| td-055 | Player car speed increase (top_speed_scale 1.0 → 1.3) | done | Muse | — | 2026-09-25 |
| td-056 | Perf: harbor map stutters on start and on bridge (Shuto does not) | merged 2026-09-25 (PR #84) | — | PR #84 | 2026-09-26 |
| td-057 | Signaling wire-key mismatch: server speaks t, client speaks type — converge on one key | merged 2026-09-26 (PR #90) — live verify pending under td-059 | — | PR #90 | 2026-09-26 |
| td-058 | net.gd never answers server ping — peers reaped after ~60s | merged 2026-09-26 (PR #89, 01:11Z) — heartbeat pong, live-verified under td-059 | Codex | PR #89 | 2026-09-26 |
| td-059 | Multiplayer button missing on the live site — PUBLISHED 2026-09-26 (de15deec), LIVE-VERIFIED: button visible, rooms XEB67Y/BQ5VRJ created, 2-player join w/ peer-joined, 75s+ survival (4 heartbeats), WebRTC SDP/ICE flowing, +30% speed (1.3) live | done | Muse | PR #96 | 2026-09-26 |
| td-060 | webgl-smoke "Verify ordinary loading and immediate race entry" fails repo-wide: entry.mjs hard-coded tap (360,607) hits SHUTO C1 after the MULTIPLAYER button shifted the menu layout | merged 2026-09-26 (PR #95, 05:20Z) — keyboard-shortcut race entry; PR #94 closed unmerged | Muse (watchdog failover) | PR #95 | 2026-09-26 |
| td-061 | Can't enter driver name on mobile (typing fails) — RANDOM-name workaround + native HTML input overlay | merged 2026-09-26 (PR #98, d5fd3886, Craig); LIVE — publish-web 16:37Z success, build-sha 1d419b48 | Muse | PR #98 | 2026-09-26 |
| td-062 | Net crashes every frame after a rejected join (null _socket in _process) | merged 2026-09-26 (PR #101, 689751da, Craig); LIVE — publish-web 16:37Z, build-sha 1d419b48 — live 2-client verification pending | Craig | PR #101 | 2026-09-26 |
| td-063 | begin_race RPC calls a function that doesn't exist (joiner stuck in lobby on race start) | merged 2026-09-26 (PR #103, c0d21048, Craig); LIVE — publish-web 16:37Z, build-sha 1d419b48 — live 2-client acceptance pending | Craig | PR #103 | 2026-09-26 |
| td-064 | Signaling server can't match joiners to hosts ("room not found" on a live room; Fly split-brain) | merged 2026-09-26 (PR #102, dda5df67, Craig); signaling DEPLOYED — deploy-signaling success 15:28Z — live join verification pending | Craig | PR #102 | 2026-09-26 |
| td-065 | Net node may not survive the scene change to mp_race (kicks back to menu) | verified no-change-needed (Net already autoload); rode with PR #103 — LIVE in build-sha 1d419b48 — live verification pending | Craig | PR #103 | 2026-09-26 |
| td-066 | Touch controls dead on mobile in multiplayer race (left/right tap does nothing) | merged 2026-09-26 (PR #105, 15:49Z, Craig); LIVE — publish-web 16:37Z, build-sha 1d419b48 — TouchControls kept in MP race, hidden on results/host-left | Craig | PR #105 | 2026-09-26 |
| td-067 | Multiplayer race loads the empty base map instead of the bridge map | merged 2026-09-26 (PR #106, 15:49Z, Craig); LIVE — publish-web 16:37Z, build-sha 1d419b48 — mp_race instances harbor_slice.tscn, 8 slice checkpoints | Craig | PR #106 | 2026-09-26 |
| td-068 | Deploy signaling server: "Enforce single instance" step fails, redeploys go out unhealthchecked (td-064 step; 2/2 runs fail) | done 2026-09-26 (PR #107, 8e73ded8): replaced Nomad-era `flyctl scale count 1` with machines-aware enforcement; green on main (run 36252065438), all 6 steps incl. health check success | Muse subagent | PR #107 | 2026-09-26 |
| td-069 | Multiplayer: each player picks their own car color (at least 4 colors) | merged 2026-09-26 (PR #108, 637a7c70, Craig); LIVE — publish-game 18:15Z, source f04f59d (validation run 36258663381) — 6-color picker on HOST/JOIN, signaling sync with server-side duplicate reassignment | Muse subagent | PR #108 | 2026-09-26 |
| td-070 | iPhone Safari: tapping room-code field on JOIN never opens the keyboard | merged 2026-09-26 (PR #109, f04f59d, Craig); LIVE — publish-game 18:15Z, source f04f59d (validation run 36258663381) — pre-created native <input> per LineEdit (tap lands on real input, iOS raises keyboard natively); real-iPhone verification pending Craig's phone (td-071 blocks join-flow test) | Muse subagent | PR #109 | 2026-09-26 |
| td-071 | Signaling server unreachable (Fly.io trial ended, org suspended ~16:52Z) — create/join/WebSocket dead | closed 2026-09-26: billing restored, suspension lifted, signaling LIVE — /health 200 verified 19:57Z; host/create flow unblocked | Craig | — | 2026-09-26 |
| td-072 | Android Chrome: typing into DRIVER NAME / ROOM CODE still fails (native overlay never created — .get()/.set() on JavaScriptObject; Craig 2026-09-26: "the typing still isnt resolved") | LIVE 2026-09-26 21:05Z — published (run 36271664534, source 4257c4014a2d, validation run 36268334491); native HTML input overlay fix; Craig phone-testing on Android Chrome | Muse subagent | PR #110 | 2026-09-26 |
| td-073 | JOIN: list available rooms so joining needs no typing (Craig's workaround for the td-072 typing defect) | done — PR tokyo-drift-3d#111 merged 2026-09-26, published live per Craig's publish-first order (build ce5abf6); smoke verification after-the-fact | Muse | tokyo-drift-3d#111 | 2026-09-26 |
| td-074 | JOIN with empty/invalid room code starts solo game instead of error | in_progress | Codex worker | fix/td-074-invalid-join | 2026-09-26 |
| td-075 | "Quit to room" quits to main menu; need room lobby page with player list | LIVE 2026-09-26 22:27Z — PR #115 merged (cron ship, build clean); publish-game run 36276274917 green, live build-sha 3ba3db94 | worker-td-075 | tokyo-drift-3d#115 | 2026-09-26 |
| td-076 | Multiplayer: show player name above car in their color | in_review — PR #117 draft (feat/td-076-nameplates): billboarded nameplates in td-069 color, before/after evidence committed, 4 screenshots eyeballed | Muse subagent | tokyo-drift-3d#117 | 2026-09-26 |
| td-077 | Multiplayer: no traffic / AI cars | open — filed 2026-09-26 from Craig's phone QA | unassigned | — | 2026-09-26 |
| td-078 | Multiplayer: no nitro / hearts pickups | open — filed 2026-09-26 from Craig's phone QA | unassigned | — | 2026-09-26 |
| td-079 | Host starts race but joiner stuck on "waiting for host to start" — race must not start until all players loaded | in_review | Codex worker | Source PR #114; local ready-gate and two-client protocol evidence green, CI/live validation pending | 2026-09-26 |
| td-080 | Client-side multiplayer debug info (copyable) | in_progress | Codex worker | Folded into td-079 source PR #114 per Craig | 2026-09-26 |
| td-081 | Server-side room event logging | in_progress | Codex worker | Folded into td-079 source PR #114 per Craig | 2026-09-26 |
| td-082 | Multiplayer POS: each player sees their own race position (1st/2nd/3rd/4th) | in_progress | Codex worker | cloud task_e_6ab841087f24832ea1eb84c65915a191 — own-position HUD (not leaderboard), compatible with td-076 name labels | 2026-09-26 |
| td-083 | Multiplayer end-of-race rank screen: finishing order, total times, DNF, race-again/quit | in_review | Codex worker | tokyo-drift-3d#116 | 2026-09-26 |
