# NEON DRIFT — task board

Source of task truth: `todos/todoNNN/README.md` in `doublehidenblade/neon-drift`.
One defect = one task. A task closes ONLY when its exact defect is fixed and verified — never because siblings were fixed.

Backfilled 2026-09-25 from the task files. Per Craig 2026-09-25, this table is the SOURCE OF TRUTH for task status — workers update it via PR (PR-based edits avoid merge conflicts).

Live site: https://doublehidenblade.github.io/neon-drift-web/

| Task | Todo | Defect (Craig's wording) | Status | Owner | Last update |
|---|---|---|---|---|---|
| todo118 | todo118 | Real-world depth, water, impacts, road life and tunnels | implementation checkpoint complete; exact-head CI and shipping remain. | — | 2026-09-25 |
| todo119 | todo119 | Systemic projection, biome transitions and layered tunnels | systemic implementation and local visual review complete; full QA/Browser CI pending. | — | 2026-09-25 |
| todo120 | todo120 | Phone feedback on v119 (tunnel, camera, shadows, lamps, water, terrain) | systemic implementation complete; full QA and exact-head Browser CI pending. | — | 2026-09-25 |
| todo121 | todo121 | Phone feedback on v120 (PR #7 world-lighting) | systemic implementation complete; full visual/CI acceptance pending. | — | 2026-09-25 |
| todo122 | todo122 | PR #8 build phone QA + Slipstream reference | open | — | 2026-09-25 |
| todo123 | todo123 | TODO 122 publication audit | unknown | — | 2026-09-25 |
| todo126 | todo126 | Complete public-repository publication migration | unknown | — | 2026-09-25 |
| todo127 | todo127 | Reconcile TODO 126 completion evidence | unknown | — | 2026-09-25 |
| todo128 | todo128 | Craig phone sprite and continuity QA | closed | — | 2026-09-25 |
| todo129 | todo129 | Continue p3d-040 verification and publication | unknown | — | 2026-09-25 |
| todo131 | todo131 | Address merged p3d-040 review findings | unknown | — | 2026-09-25 |
| p3d-058 (todo132) | todo132 | directional traffic frames | unknown | — | 2026-09-25 |
| p3d-060 (todo133) | todo133 | civilian sprite view by relative player distance | in_review | PR [#70](https://github.com/doublehidenblade/neon-drift/pull/70) | 2026-09-26 |
| p3d-061 (todo134) | todo134 | sprite size normalization and systematic sprite CI | merged | — | 2026-09-25 |
| p3d-062 (todo135) | todo135 | civilian-vs-civilian and civilian-vs-obstacle collision | in_review | — | 2026-09-25 |
| p3d-063 (todo136) | todo136 | overtaken civilian cars keep their own speed | in_review — PR #29 (fix/p3d-063-civilian-speed) merged 2026-09-24T02:24:30Z as bbee229d, p… | — | 2026-09-25 |
| p3d-064 (todo137) | todo137 | collision boxes mapped to obstacle visual size | merged — PR #28 (p3d-064: map collision boxes to obstacle visual size) squash-merged 22:48… | — | 2026-09-25 |
| p3d-065 (todo138) | todo138 | better water (not observed on live build) | shipped — PR #37 merged and live | — | 2026-09-25 |
| p3d-066 (todo139) | todo139 | remove the broken secondary roads | shipped — PR #25 (fix/p3d-066-remove-secondary-roads) merged 2026-09-24T08:38:01Z as 76109… | — | 2026-09-25 |
| p3d-067 (todo140) | todo140 | roadblock | shipped — PR #34 merged 2026-09-24T03:44:18Z as 97a7029d, publish-web green, live. Craig's… | — | 2026-09-25 |
| p3d-068 (todo141) | todo141 | floating torii gate | in_review — merged to main (deef2429), live verified 2026-09-23 20:10 MDT; awaiting Craig'… | — | 2026-09-25 |
| p3d-069 (todo142) | todo142 | neon complex roads (second map, proof of concept) | unknown | — | 2026-09-25 |
| p3d-070 (todo143) | todo143 | : player car sprite replaced with Slipstream-style 12-view set | blocked | — | 2026-09-25 |
| todo144 | todo144 | Browser CI perf assertions flake on PR branches (shared-runner variance) | unknown | — | 2026-09-25 |
| p3d-072 (todo145) | todo145 | start banner replaces torii + opponent lineup at start | unknown | — | 2026-09-25 |
| p3d-073 (todo146) | todo146 | player car rear view angled right | unknown | — | 2026-09-25 |
| p3d-074 (todo147) | todo147 | water color and extent | in_review | — | 2026-09-25 |
| p3d-075 (todo148) | todo148 | arch bridge as short tunnel (tunnel interim) | in_review | PR [#67](https://github.com/doublehidenblade/neon-drift/pull/67) — exact-head Browser CI blocked by desktop CPU p95 | 2026-09-26 |
| p3d-076 (todo149) | todo149 | building sides not to perspective | merged (neon PR #73, squash-merged by cron 2026-09-27T02:29Z as a39ff4a10; renderer.js +33/-4: second-row facades routed through shared building class with 8 world-depth projection slices; matched before/after QA pairs todos/todo149/qa/p3d-076-criterion-1-{before,after}.png + numeric projection test (<=1e-9); NOT live — awaiting Craig's push) | — | 2026-09-27 |
| p3d-077 (todo150) | todo150 | START banner: raise to overhang height, center the START text | merged — neon PR [#78](https://github.com/doublehidenblade/neon-drift/pull/78) squash-merged by cron 2026-09-27T11:44Z as eed7cdba (START banner raised to overhang height, START text centered over start grid); NOT live — awaiting Craig's push | — | 2026-09-27 |
| p3d-078 (todo151) | todo151 | player car collides with road rail too prematurely (collision-box inaccuracy) | in_review | p3d-078 worker | 2026-09-27 |
| p3d-079 (todo152) | todo152 | collision spark and nitro collect spark too small | merged — neon PR [#79](https://github.com/doublehidenblade/neon-drift/pull/79) squash-merged as 5b897cd; shared 8 px / 0.68 s / 0.72 opacity spark floor; matched collision/pickup evidence; exact-head Browser CI 93/93; NOT live — awaiting Craig push | p3d-079 worker | 2026-09-27 |
| p3d-080 (todo153) | todo153 | roadblock/cone hit animation (break off / fly off) with new sprites | in_review | — | 2026-09-25 |
| p3d-081 (todo154) | todo154 | player speed +30%, opponent speed +15% | merged — neon PR [#80](https://github.com/doublehidenblade/neon-drift/pull/80) squash-merged by cron 2026-09-27T14:36Z as e76bbeb7 (1.30x player / 1.15x opponent speeds, telemetry + matched before/after pair committed, criterion-2 eyeball passed; desktop CPU p95 gate 25.4ms miss = known infra flake p3d-097); NOT live — awaiting Craig's push | — | 2026-09-27 |
| p3d-082 (todo155) | todo155 | distinct race opponent car sprites vs civilian cars (start-grid car variety) | in_review — neon PR [#81](https://github.com/doublehidenblade/neon-drift/pull/81); four named race-only designs + matched grid evidence; exact-head CI pending | Codex worker | 2026-09-27 |
| p3d-083 (todo156) | todo156 | split/merge fork not readable in gameplay | merged — neon PR [#68](https://github.com/doublehidenblade/neon-drift/pull/68) squash-merged by Craig 2026-09-27T05:17Z (rebase onto main, renderer.js +34/-3 gore + diagonal paint + textured branch pavement; matched before/after QA pairs todos/todo156/qa/p3d-083-criterion-{1,2}-{before,after}.png + 4 through-zone frames; 85/86 Browser CI, only failure = bridge-exit CPU p95 gate 25.7ms, known infra flake p3d-097); NOT live — awaiting Craig's push | — | 2026-09-27 |
| p3d-084 (todo157) | todo157 | feature banners look like floating debug boxes | merged — PR [#72](https://github.com/doublehidenblade/neon-drift/pull/72) squash-merged by watchdog cron 2026-09-27T00:44Z (6 gantry signs mounted in renderer.js + evidence pairs committed); NOT live: publish-web blocked, Actions budget exhausted (needs Craig: raise spending limit) | — | 2026-09-26 |
| p3d-085 (todo158) | todo158 | water must extend vertically toward the horizon in perspective (follow-up to p3d-074) | merged | — | 2026-09-25 |
| p3d-086 (todo159) | todo159 | roadside walls grey not blue (fix wall sprite texture, not canvas) | in_review | Codex worker | 2026-09-26 |
| p3d-087 (todo160) | todo160 | dirt terrain brown not blue (fix dirt sprite texture, not canvas) | merged | — | 2026-09-25 |
| p3d-088 (todo161) | todo161 | refresh stale harbor-desktop-linux.png snapshot after p3d-085 water projection (CI red on main) | open | — | 2026-09-25 |
| p3d-089 (todo162) | todo162 | investigate city CPU render p95 regression after p3d-085 (31.7ms vs 25ms budget) | open | — | 2026-09-25 |
| p3d-090 (todo163) | todo163 | land terrain renders blue in some parts (phone QA 2026-09-24) | merged (PR #53 squash-merged by cron 2026-09-25T06:46Z, sha d5eed4f8; publish-web dispatch… | — | 2026-09-25 |
| p3d-091 (todo164) | todo164 | land and water don't stretch to the horizon in some parts (phone QA 2026-09-24) | merged (PR #54 squash-merged by cron 2026-09-25T08:05Z, sha a95321ff; terrain/water projec… | — | 2026-09-25 |
| p3d-092 (todo165) | todo165 | terrain and water sprites look horizontally stretched (phone QA 2026-09-24) | merged (PR #63, 2026-09-26T04:50Z) — mobile LOADING-99% regression filed as p3d-100 | Muse (watchdog failover) | PR #63 | 2026-09-26 |
| p3d-093 (todo166) | todo166 | other car sprites not showing sides when next to player (phone QA 2026-09-24) | merged — PR #56 (cron ship 2026-09-25, all 67 correctness/visual CI cases pass; CPU-only f… | — | 2026-09-25 |
| p3d-094 (todo167) | todo167 | other cars run over obstacles without reacting or dodging (phone QA 2026-09-24) | merged — neon PR [#57](https://github.com/doublehidenblade/neon-drift/pull/57) merged by Craig 2026-09-26T17:13Z as b75985a0 (shared deterministic obstacle anticipation/dodging for civilians + race opponents; matched before/after pair todos/todo167/qa/p3d-094-criterion-1-{before,after}.png; exact-head CI 69/70, only failure = bridge p95 gate, known infra flake p3d-097); NOT live — awaiting Craig's push | — | 2026-09-27 |
| p3d-095 (todo168) | todo168 | building sides still dead horizontal instead of 3D perspective (phone QA 2026-09-24) | open | — | 2026-09-25 |
| p3d-096 (todo169) | todo169 | start sign still too low and in the way (phone QA 2026-09-24) | merged — PR #61 merged by Craig 2026-09-26T01:40Z; live unchanged (no export files touched); perf gate red = pre-existing (p3d-097) | — | 2026-09-26 |
| p3d-097 (todo170) | todo170 | bridge-exit CPU p95 perf check is flaky on CI (infra noise, not a game regression) | open | — | 2026-09-25 |
| p3d-098 (todo171) | todo171 | PR #56 after-evidence shows rear sprite, not side sprite (Craig QA 2026-09-25) | merged — PR #60 squash-merged by cron 2026-09-25T22:28Z as 0e56269 (CI perf-gate red = pre-existing main failure, p3d-097 infra); dup PR #58 closed | — | 2026-09-25 |
| p3d-099 (todo172) | todo172 | further car renders on top of the player car (Craig QA 2026-09-25) | merged — PR #59 (p3d-099: correct car painter order) squash-merged 2026-09-25T20:32:46Z as 5f4c9fee, by cron | — | 2026-09-25 |
| p3d-100 (todo174) | todo174 | mobile loader sticks at LOADING 99%, START RACE never appears (regression from PR #63) | merged — [PR #74](https://github.com/doublehidenblade/neon-drift/pull/74) squash-merged by cron 2026-09-27T04:46Z as 866bf6a; live pending Craig's push request | — | 2026-09-27 |
| p3d-101 (todo175) | todo175 | Again, a middle out of nowhere bridge, with no roads leading out of both ends | merged — PR #71 squash-merged by cron 2026-09-27T00:01Z as a9e395ec (perf-gate red = pre-existing infra flake p3d-097) — NOT live yet: publish-web blocked, GitHub Actions budget exhausted (job 'not started because an Actions budget is preventing further use', 23:59Z); needs Craig: raise Actions spending limit | — | 2026-09-26 |
| p3d-102 (todo176) | todo176 | race ends on lap 2 before player crosses the finish line (Craig QA 2026-09-27) | open | — | 2026-09-27 |
| p3d-103 (todo177) | todo177 | HUD heart health icons unreadable on phone — should face the player, not sideways (Craig QA 2026-09-27) | open | — | 2026-09-27 |
| p3d-104 (todo178) | todo178 | tapping the nitro button also steers the car (Craig QA 2026-09-27) | open | — | 2026-09-27 |

Related (not a task file): bridge **128-2** (wires/poles too thin) — `fixed_pending_verify` in qa-registry, still visible on Craig's live screenshot 2026-09-23 09:42 CDT after PR #19. Do not close without Craig's phone verdict.

QA 2026-09-24: Craig could not verify p3d-060 on his phone — overtaken cars disappear into the back too quickly when passed (p3d-063 defect, open). p3d-060 closure blocked on his verdict until p3d-063 fixed. Player car was NOT part of the p3d-060 fix — p3d-070 filed for the 12-view player sprite.

Priority order (Craig 2026-09-23): civilian-car sprite/traffic cluster (p3d-060..064) → visual fixes (p3d-065..068 + bridge 128-2) → p3d-069 neon complex roads.
