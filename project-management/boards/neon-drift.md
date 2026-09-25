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
| p3d-060 (todo133) | todo133 | civilian sprite view by relative player distance | open | — | 2026-09-25 |
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
| p3d-075 (todo148) | todo148 | arch bridge as short tunnel (tunnel interim) | open | — | 2026-09-25 |
| p3d-076 (todo149) | todo149 | building sides not to perspective | open | — | 2026-09-25 |
| p3d-077 (todo150) | todo150 | START banner: raise to overhang height, center the START text | open | — | 2026-09-25 |
| p3d-078 (todo151) | todo151 | player car collides with road rail too prematurely (collision-box inaccuracy) | open | — | 2026-09-25 |
| p3d-079 (todo152) | todo152 | collision spark and nitro collect spark too small | open | — | 2026-09-25 |
| p3d-080 (todo153) | todo153 | roadblock/cone hit animation (break off / fly off) with new sprites | in_review | — | 2026-09-25 |
| p3d-081 (todo154) | todo154 | player speed +30%, opponent speed +15% | open | — | 2026-09-25 |
| p3d-082 (todo155) | todo155 | distinct race opponent car sprites vs civilian cars (start-grid car variety) | open | — | 2026-09-25 |
| p3d-083 (todo156) | todo156 | split/merge fork not readable in gameplay | open — unassigned | — | 2026-09-25 |
| p3d-084 (todo157) | todo157 | feature banners look like floating debug boxes | open — unassigned | — | 2026-09-25 |
| p3d-085 (todo158) | todo158 | water must extend vertically toward the horizon in perspective (follow-up to p3d-074) | merged | — | 2026-09-25 |
| p3d-086 (todo159) | todo159 | roadside walls grey not blue (fix wall sprite texture, not canvas) | open | — | 2026-09-25 |
| p3d-087 (todo160) | todo160 | dirt terrain brown not blue (fix dirt sprite texture, not canvas) | merged | — | 2026-09-25 |
| p3d-088 (todo161) | todo161 | refresh stale harbor-desktop-linux.png snapshot after p3d-085 water projection (CI red on main) | open | — | 2026-09-25 |
| p3d-089 (todo162) | todo162 | investigate city CPU render p95 regression after p3d-085 (31.7ms vs 25ms budget) | open | — | 2026-09-25 |
| p3d-090 (todo163) | todo163 | land terrain renders blue in some parts (phone QA 2026-09-24) | merged (PR #53 squash-merged by cron 2026-09-25T06:46Z, sha d5eed4f8; publish-web dispatch… | — | 2026-09-25 |
| p3d-091 (todo164) | todo164 | land and water don't stretch to the horizon in some parts (phone QA 2026-09-24) | merged (PR #54 squash-merged by cron 2026-09-25T08:05Z, sha a95321ff; terrain/water projec… | — | 2026-09-25 |
| p3d-092 (todo165) | todo165 | terrain and water sprites look horizontally stretched (phone QA 2026-09-24) | open | — | 2026-09-25 |
| p3d-093 (todo166) | todo166 | other car sprites not showing sides when next to player (phone QA 2026-09-24) | merged — PR #56 (cron ship 2026-09-25, all 67 correctness/visual CI cases pass; CPU-only f… | — | 2026-09-25 |
| p3d-094 (todo167) | todo167 | other cars run over obstacles without reacting or dodging (phone QA 2026-09-24) | open | — | 2026-09-25 |
| p3d-095 (todo168) | todo168 | building sides still dead horizontal instead of 3D perspective (phone QA 2026-09-24) | open | — | 2026-09-25 |
| p3d-096 (todo169) | todo169 | start sign still too low and in the way (phone QA 2026-09-24) | open | — | 2026-09-25 |
| p3d-097 (todo170) | todo170 | bridge-exit CPU p95 perf check is flaky on CI (infra noise, not a game regression) | open | — | 2026-09-25 |
| p3d-098 (todo171) | todo171 | PR #56 after-evidence shows rear sprite, not side sprite (Craig QA 2026-09-25) | open | — | 2026-09-25 |
| p3d-099 (todo172) | todo172 | further car renders on top of the player car (Craig QA 2026-09-25) | open | — | 2026-09-25 |

Related (not a task file): bridge **128-2** (wires/poles too thin) — `fixed_pending_verify` in qa-registry, still visible on Craig's live screenshot 2026-09-23 09:42 CDT after PR #19. Do not close without Craig's phone verdict.

QA 2026-09-24: Craig could not verify p3d-060 on his phone — overtaken cars disappear into the back too quickly when passed (p3d-063 defect, open). p3d-060 closure blocked on his verdict until p3d-063 fixed. Player car was NOT part of the p3d-060 fix — p3d-070 filed for the 12-view player sprite.

Priority order (Craig 2026-09-23): civilian-car sprite/traffic cluster (p3d-060..064) → visual fixes (p3d-065..068 + bridge 128-2) → p3d-069 neon complex roads.
