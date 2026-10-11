# Tokyo Drift first playtest release resume handoff

> Researched: 2026-10-08 by game-development coordination
> Source inspection: 03:32–03:35 UTC, 2026-10-08 (23:32–23:35 EDT, 2026-10-07)

**Release remains held.** Implementation and independent review are paused pending an available approved worker. Preserve current owners and required model/tool standards; do not start duplicate work or substitute a lower tier. This is an isolated evidence handoff, not an acceptance verdict, dispatch, board update, merge or deployment.

Craig approved an earlier first preview once the current gigs, HUD, traffic, Tenjin/Kamome buildings and download fixes pass, with unfinished districts disclosed. Whole-city completion is not required first. The CI waiver applies only to this playtest; it does not waive failed acceptance or authorize Actions. Physical-phone acceptance comes from the preview. [Current release-scope record](https://github.com/doublehidenblade/tokyo-drift-3d/blob/3d1f592fad58324bc2e752fc35a5a02f39527655/deploy/chunked/RELEASE_PLAN.md)

## Verified remote pins

All listed Tokyo PRs were open/draft and unmerged at inspection. SHA means the remote evidence/head commit unless labelled runtime/product. Retain both: evidence commits are not interchangeable with tested game source.

| Work | Remote head | Runtime or product |
| --- | --- | --- |
| [Tenjin #489](https://github.com/doublehidenblade/tokyo-drift-3d/pull/489) | `0b2652bc86b6824444af277fdb34af5bdd981066` | `6f7818b45cd09ade3ca621354ce4eb116050a66b` |
| [Kamome #494](https://github.com/doublehidenblade/tokyo-drift-3d/pull/494) | `09eb9455def0a27ece9f93f4946b739dc03cf712` | `f05048b12c176f9443cfc77e3a1bfb1ec19f62cf` |
| [HUD integration #498](https://github.com/doublehidenblade/tokyo-drift-3d/pull/498) | `067e4c620d8f41910a0e4d219e258e95e45ff19a` | `ea7f3cf4d616b79533a48ccca1e4560f2bc2674f` |
| [Asset repair #486](https://github.com/doublehidenblade/tokyo-drift-3d/pull/486) | `fb1f53af6241f9af486a6565faf49acfe773f52b` | `aeb5d8b367a41ec68905f2c86c47002628bdce73` |
| Asset repair integration branch | `fd1d674266335f49fa9486fbff0a6ddae757865f` | `de4a4f03f5295b7b7e163c84bb41d7ba1684d2f5` |
| [Packaging #496](https://github.com/doublehidenblade/tokyo-drift-3d/pull/496) | `3d1f592fad58324bc2e752fc35a5a02f39527655` | `6c4d2942334837c4bfeea26fc6fb11037d9d6ad6` |
| [Older assembly #488](https://github.com/doublehidenblade/tokyo-drift-3d/pull/488) | `2227f71e784f581d11ace8f90e7201fbb59b1f63` | `8e7caeb1209c0d47dfea3ac57308e693a00b3983` |

Kamome's frozen author evidence is `dd0fe14672a92990193194741b5fc5580040fafc`; the newer remote head contains its independent verdict. Its PR body still describes review as pending, so use the committed review below.

HUD #498's [pinned integration record](https://github.com/doublehidenblade/tokyo-drift-3d/blob/067e4c620d8f41910a0e4d219e258e95e45ff19a/godot/qa/td-211/source-pins.json) combines:
- Claude [#497](https://github.com/doublehidenblade/tokyo-drift-3d/pull/497) `145cd528b40c4c396e7c0999dde493a345cf8dd6`, runtime `c3515628a5bd63d50234191bf112d113311f0372`
- Fuel [#457](https://github.com/doublehidenblade/tokyo-drift-3d/pull/457) `827e058c6e11e8bb923b9fefa7471227bae59a40`
- Fuel HUD [#483](https://github.com/doublehidenblade/tokyo-drift-3d/pull/483) `d48a5dcba6b4e7f66b292ccf6610200595f88d5e`
- Systems [#446](https://github.com/doublehidenblade/tokyo-drift-3d/pull/446) `64ccf666847499c076edaffcebf2ca303f462a8f`
- Integration base `1848378c136f102f3369605f090c2dd47c642679`; source main remains `9d4a88490c41f86e8d34e1c2c6f142838de20c73`

These are distinct dependency stacks. #488 still contains the older assets and HUD and is not the final combined candidate.

## What passed and what did not

- **Tenjin: independently passed its five bounded criteria.** 77 lots; focused 82/82 and ramps 25/25. The [independent report](https://github.com/doublehidenblade/tokyo-drift-3d-web/blob/6654e32d3769836076e312cd42db10ad816c0218/qa/td-209/REVIEW.md) retains inherited console/sign/drive failures and physical-phone limits. This is not whole-game acceptance.
- **Kamome: independently passed its six bounded criteria.** The [committed verdict](https://github.com/doublehidenblade/tokyo-drift-3d/blob/09eb9455def0a27ece9f93f4946b739dc03cf712/godot/qa/td-210/REVIEW.md) covers 345 lots, including 50 documented visibility exceptions, rather than claiming unobscured facade proof for those exceptions. Independent checks reproduced 20/20, Tenjin 82/82 and ramps 25/25. Median construction rose 4,110→5,626 ms and static allocation 309,098,122→377,103,143 bytes. Both strict ordinary runs still fail with 48 inherited errors; seven sign trips and drive leg nine fail, with only nine of 21 planned drive legs emitted. The 112,557,688-byte pack is not the final combined release pack.
- **Asset repair: prior independent bounded PASS relayed by the coordinator.** Wheel speed, steering sign and deferred AnimeLook repair passed at the listed repaired heads: 45/45 versus 13 old failures, wheel-travel ratio 0.997, 27/27 systems and 956/956 Forge checks. [Committed secondary record](https://github.com/doublehidenblade/tokyo-drift-3d/blob/3d1f592fad58324bc2e752fc35a5a02f39527655/reviews/chunked-delivery-20261007/README.md#parent-supplied-bounded-asset-repair-review). The original independent raw report has no public URL; this pass did not rerun it. The same 26 menu-resource errors remain unresolved and unwaived.
- **HUD integration: author-passed focused checks; independent acceptance pending.** [Frozen handoff](https://github.com/doublehidenblade/tokyo-drift-3d/blob/067e4c620d8f41910a0e4d219e258e95e45ff19a/godot/qa/td-211/README.md) reports per-engine 398/398 HUD, 23/23 rotation/input, 170/170 paid modal and 138/138 drive/recovery assertions. It reports the portrait NITRO/font and paid-recovery lesson corrections. Staged settlement displays are not driven deliveries. Real police arrests defeated full-gig autopilot checks; a run timed out, build is 33/34, and direct-script CrimeBus/Nil failures persist. Full production entry/reload, independent exact-head and physical-phone acceptance are pending.
- **Packaging: author corrected three P2s; not independently accepted.** [Correction record](https://github.com/doublehidenblade/tokyo-drift-3d/blob/3d1f592fad58324bc2e752fc35a5a02f39527655/reviews/chunked-delivery-20261007/p2-correction/README.md) reports 4/4 package and 12/12 focused checks for real Wasm timeout cancellation, executable selector validation and HTTP-body cancellation. Focused independent re-review was interrupted and remains pending. The earlier full matrix belongs to the previous head. Its Tenjin test pack still has older city errors and is not final Kamome/HUD/repaired-asset assembly. Chunking solves the blob-delivery constraint; it does not establish a mobile-memory improvement.

## Minimal path to the first preview

1. When an approved worker is available, resume the existing independent packaging and HUD reviews against these exact heads. Do not rerun completed district implementation or weaken failed tests. Retain raw failures and require source-cited verdicts.
2. In the existing assembly ownership, combine reviewed final Kamome/Tenjin, HUD/Claude/Fuel/systems and repaired-asset pins with the accepted packaging product. Reconcile overlapping ancestry once; preserve Fuel JSON inclusion and selective asset exclusions. Record the final runtime, evidence/tree/importer/export hashes and both actual packs.
3. Validate that final assembly through ordinary production entry, actual steering/braking/collision, traffic/pedestrians/police, a real gig accept→pickup→delivery→payout loop, failure/recovery, Fuel quote/cancel/payment, map/pause/resume, run-state/reload and Shuto. Resolve release-blocking failures with their current owners. Isolated fixture PASS counts do not close this gate.
4. After required reviews and final acceptance checks pass, obtain the coordinator's release signal under Craig's conditional preview approval. Use the [supported static-chunk plan](https://github.com/doublehidenblade/tokyo-drift-3d/blob/3d1f592fad58324bc2e752fc35a5a02f39527655/deploy/chunked/RELEASE_PLAN.md), preserve immutable rollback versions and galleries, and verify both real HTTPS origins, every served inventory hash, reconstructed PCK, selected manifests/source/version and ordinary browser behavior. Do not trigger Actions or bypass the stopped Pages-administration access path.
5. Send inspected screenshots, changes, risks, unfinished districts and the verified play links as **for Craig to check**. Record physical-phone appearance/performance after that playtest; do not manufacture a pre-release phone PASS.

No new districts, cosmetics or weather belong ahead of this release. [Whole-city #491](https://github.com/doublehidenblade/tokyo-drift-3d/issues/491) remains open, including Chidori, Kotobuki, Daikoku, Shinkai, North Rail Depots and bespoke T2/Paper Exchange.

## Live identity and preserved boundaries

HTTPS reads during 03:34–03:35 UTC confirmed both [main deployment](https://doublehidenblade.github.io/tokyo-drift-3d-web/deployment.json) and [Shuto deployment](https://doublehidenblade.github.io/tokyo-drift-3d-shuto-web/deployment.json), and both build-sha.txt files, return source `4ecd2089c1b292c11c70b7e9701f77df39cca044`. Main version.txt returns v46; Shuto version.txt remains 404. This is identity evidence only, not fresh gameplay or phone acceptance. The historical manifest/HTML hash discrepancy remains a release-plan limitation; no full served-file hash audit was performed here.

Central base `b07dbc8638a0029603dd0b0b66c60e2124e2fe94` was read with [rules](https://github.com/doublehidenblade/game-dev-central/blob/b07dbc8638a0029603dd0b0b66c60e2124e2fe94/project-management/rules/SYSTEM.md), [board](https://github.com/doublehidenblade/game-dev-central/blob/b07dbc8638a0029603dd0b0b66c60e2124e2fe94/project-management/boards/tokyo-drift-3d.md), worker registry, coordinator log and release pending/baseline ledger. Registry/log observations and v29/v34 release baselines are historical; they do not prove present worker liveness or current publication.

Muse/Claude ownership is preserved. NEON stays paused. Central [#347](https://github.com/doublehidenblade/game-dev-central/pull/347) at `81e3fc0493dcadeb8e8595f325641c4178e60e9d` and Tokyo [#479](https://github.com/doublehidenblade/tokyo-drift-3d/pull/479) at `212e28b096d2b7d024cc47c4b3bcaddd543c74e1` remain draft and untouched. [Truck brief #351](https://github.com/doublehidenblade/game-dev-central/pull/351) remains separate; mock-upload approval holds stay in place and no 3D implementation is claimed. [Weather #352](https://github.com/doublehidenblade/game-dev-central/pull/352) merged as documentation only at `4c9ab36c959f278a374ad0f73229c0298f7e80a4`, with execution disabled.

This document changes no active board, reservation, registry, log, release ledger, runtime, owner controls or worker state.

## 2026-10-08 06:03 UTC — dot-cloud preparation checkpoint

This append-only checkpoint supersedes the earlier blanket paused/review-pending description only where evidence below advances it. **Release is still held.** This is progress recording, not full acceptance, an owner reassignment, or a release signal.

- Remote recheck at 06:02 UTC: HUD #498 remains `067e4c620d8f41910a0e4d219e258e95e45ff19a`, packaging #496 remains `3d1f592fad58324bc2e752fc35a5a02f39527655`, Kamome #494 remains `09eb9455def0a27ece9f93f4946b739dc03cf712`; all remain open. Tokyo main remains `9d4a88490c41f86e8d34e1c2c6f142838de20c73`.
- **Independent HUD: bounded PASS.** Fresh headless presentation 43/43, menu 25/25, touch 31/31 and lesson 30/30 total 129 checks, all exit 0 with no ERROR/SCRIPT ERROR/WARNING. Separate real-scene geometry is **46/50**, not green: four invisible slack-strip overlaps reproduce in the controls-only baseline and remain inherited P3. Source/evidence audit is separately 34/34. Reviewed authored pixels corroborate portrait NITRO/font, visible TAKE and lesson corrections; no fresh independent browser or physical-phone execution is claimed. Raw full-gig arrests/timeout, broad build 33/34 and prior renderer errors are preserved.
- **Independent packaging: source and bounded Node checks only.** Package suite 4/4; executable-selector controls 5; synthetic native-Fetch transport evidence comprises 11 saved checks plus 10 corrected remaining-case checks, **21 distinct checks**, without double-counting reruns or calling the interrupted first run a full pass. Corrected HTTP-error bodies close; corrected Wasm timeout occurs at 60,003.95 ms with zero live body before disposal and no reopened server request. Synthetic recovery is not a browser reload or actual oversized Godot startup. Browser launch/socket and browser-to-session loopback failures remain environmental blockers; the 48 inherited author fixture errors (26 menu + 22 city) remain unwaived.
- **Independent combined-candidate legal delivery: bounded functional PASS.** An isolated, unchanged copy drove default Asahi HQ → Starlight pickup → Gate 2: 2.923 km, 218.7/255 seconds delivery clock, 100% cargo, zero hits/crime/arrest/recovery, credited payout ¥4,570 and run-scoped Fuel balance ¥5,000 → ¥9,570. A QA-only driver supplied real throttle/steering and yielded to real traffic/pedestrians; no actors, police, collisions, dispatch or Fuel constraints were disabled, and no teleports/manual settlement were used. All 2,517 pre-existing files remained hash-identical. This uses 85.7647% of the limit and **does not pass the original 85% upper challenge gate or four-run full suite**. Earlier arrested/timed-out attempts remain retained. No runtime error preceded settlement; shutdown resource/RID leaks remain in raw evidence. It is headless input/physics evidence, not menu, graphics, browser or phone acceptance.
- **Both new combined packs exported locally, exit 0, independently rehashed here.** Base: 112,573,080 bytes, SHA256 `81697c34b95dafdd7e6713c878833330686c0a10ae8efe94034b3b6ea9475046`. Shuto: 99,677,672 bytes, SHA256 `9474bff79d68c0d8d40c8b8be3e92c5bd3b3ec52b96de332a58753fddff0c795`. Construction preserves the HUD source pin with bounded district/repaired-asset overlays and corrected packaging; these local exports are not a committed, accepted or served release. Export success does not replace pack dependency closure, native-OpenGL district checks or browser acceptance.
- Five canceled non-shipping files remain omitted: the preset-excluded td186 bus GLB and four ignored car-source .blend files. No retry or alternate transfer was performed for these files. Do not claim a complete source checkout or full Forge validation.
- **Private 32 MiB transfer probe remains unknown/pending**, per coordinator at this checkpoint: the create_blob attempt pending since 05:42 has no confirmed upload or ref change. Expected Git blob is `46c22e2da32bb58cfa5d6240a983807d667b56cd`; no retry. Earlier 05:36 readback was absent, but it does not decide the later pending attempt. This is not an established GitHub size-limit failure or a successful transfer.
- **Live identity only:** coordinator's fresh HTTPS checks at 06:02:19–06:02:47 UTC found both deployment manifests HTTP 200 at source `4ecd2089c1b292c11c70b7e9701f77df39cca044`, published timestamp 2026-10-07T04:33:28.167Z; main build marker/version remain that SHA/v46. Shuto build marker/version were not yet freshly confirmed in this checkpoint; earlier 03:34–03:35 evidence remains historical. These reads do not establish fresh live gameplay acceptance.

Evidence provenance: independently authored local reports were read in full before this summary. They are not uploaded here and have no new public evidence URL. SHA256 identities: HUD report `41bcd7b002bc795516fcd8d93f08035ce71b63b9d36303f37d88198fa77984ef`; packaging report `68c6e383b143a34ad7a5b7c1a7ab9a995118b0e8d6597198e1217e638eb23f88`; legal-delivery report `1eb45809505d8907cdea0c9cac245342a41fd2c8ef5e4f4f53463325b35ab08e` and machine result `b6f4981180cf82c64ea3ddfb03321a5fb030680748731f93aa8fbe5c82159790`. Existing exact-head source/evidence links above remain the remote anchors; local counts are explicitly separate from committed author evidence.

Next gate remains independently accepted combined runtime/pack/browser behavior and verified actual-origin delivery under the conditional preview scope. Preserve all raw failures, rollback versions and owner boundaries. This checkpoint changes only this existing draft-PR handoff file; no active board, registry, coordinator log, release ledger, game source, Actions, merge or deployment is changed.

## 2026-10-08 06:12 UTC — reproducible candidate and pack-audit handoff

Verification-only continuation. No merge, Actions, game deployment or publication authorization is added. Previous history and unmet browser/release gates remain in force.

### Exact reconstruction without transferring private binaries

Use an isolated verification checkout of `doublehidenblade/tokyo-drift-3d` at HUD base `067e4c620d8f41910a0e4d219e258e95e45ff19a`. Preserve every other base path. Apply only the 26 exact path/blob replacements below, plus the separate QA fixture and packaging files. Each resulting overlay file was Git-blob-hash-checked against the prepared candidate, and every overlay blob was read successfully from the repository at 06:11 UTC. These are existing source bytes, not a new gameplay implementation.

Source aliases:
- K = Kamome `09eb9455def0a27ece9f93f4946b739dc03cf712`; district scope derives from its delta against older assembly `2227f71e784f581d11ace8f90e7201fbb59b1f63`, preserving reviewed Tenjin.
- A = repaired assets `fb1f53af6241f9af486a6565faf49acfe773f52b`; repair scope derives from its delta against main `9d4a88490c41f86e8d34e1c2c6f142838de20c73`.
- G = pedestrian integration glue `fd1d674266335f49fa9486fbff0a6ddae757865f`.

Do not merge whole older ancestry over the HUD/Fuel/systems base. For an available authenticated repository checkout, `git show <full-ref>:<path>` provides each exact file; compare `git hash-object <file>` with the table before testing. The traffic result originally constructed as a narrow three-way combination is already byte-identical to K's existing blob `a96fddd...`; use the listed exact bytes without inventing another merge.

| Repository-relative path | Source | Expected Git blob |
| --- | --- | --- |
| `godot/export_presets.cfg` | K | `4d9e9adb3f4a30ec34612197be9c867a7e2c234a` |
| `godot/scenes/pedestrian_manager.tscn` | G | `d1d71de044aa286c1ef1bb51739ec71971c0f1e7` |
| `godot/scenes/td186/td186_car_taxi.tscn` | A | `1a7c752652cea507120ec14b8ebd98f0a1cfbcc8` |
| `godot/scenes/td186/td186_pedestrian.tscn` | A | `bcbfd3fe2b9742d9964ff1c32e2eb0141f878bb8` |
| `godot/scripts/lower_city/city_dressing.gd` | K | `f19fc062ca1cdbbdbb472f38d99d2e2caa0e3f72` |
| `godot/scripts/lower_city/city_kamome_buildings.gd` | K | `2c4f3b107e73e45a8416a3dfa57bc9e655f16624` |
| `godot/scripts/lower_city/city_kit_batch.gd` | K | `b31fba57f719c1058981cb494a1e480b2e4e97a3` |
| `godot/scripts/lower_city/city_kit_instances.gd` | K | `163d3be10b020f679af7c9c989510e0306b0487c` |
| `godot/scripts/lower_city/city_tenjin_buildings.gd` | K | `a3b77b009e8ce63e7ba510da31622b81f7bd93b1` |
| `godot/scripts/lower_city/lower_city_world.gd` | K | `6c40d58333752ab0632fd2eba33f1478d2a2c18a` |
| `godot/scripts/slice/anime_look.gd` | A | `dd0ccff62bed524d2ee54d26550562e9cbedddda` |
| `godot/scripts/td186/td186_car_model.gd` | A | `b9fbd58833a95572f3e084122c86546220184625` |
| `godot/scripts/td186/td186_car_model.gd.uid` | A | `30289b9c2bc2ff10313689161b8a3eb17c57dd72` |
| `godot/scripts/td186/td186_pedestrian.gd` | A | `fe14ebd7aa4b945e987c5d1b4fc86c2a2c9cfc3e` |
| `godot/scripts/td186/td186_pedestrian.gd.uid` | A | `f66eb2956d8abfb131755618a162c0fb500012fd` |
| `godot/scripts/traffic/city_traffic.gd` | K | `a96fdddceae0511715f22d5187093f0228feb7cf` |
| `godot/tools/qa/kamome_eave_geometry.gd` | K | `b95f4a500dc3b84b8cb826cb458fc5f93346d088` |
| `godot/tools/td186/capture_city_slice.gd` | A | `b8ea85ea526c09763e75d633b3ba61ccc5832e67` |
| `godot/tools/td186/capture_city_slice.gd.uid` | A | `8a7b10fedd0aa5ee9db3f5af16ee45197336848c` |
| `godot/tools/td186/td186_test_input.gd` | A | `9c35aecc639a396e929ed7b7e68f9065af6c7d7b` |
| `godot/tools/td186/td186_test_input.gd.uid` | A | `28b05cc555970cc66d4ef115a3e27b2efb07df2a` |
| `godot/tools/td186/test_td186_city_slice.gd` | A | `b12ed6e9123a10009fce8420c663e1b12448accd` |
| `godot/tools/td186/test_td186_city_slice.gd.uid` | A | `05930f91aa9433032737656a3df9e51cb5dd75fe` |
| `godot/tools/test_kamome_buildings.gd` | K | `7c9cec4f1ce8b916d4278ae946d933e09214ddca` |
| `godot/tools/test_lower_city_build.gd` | K | `cec2d469c1ace418d1a629725c7b271cb85f5faf` |
| `godot/tools/test_tenjin_buildings.gd` | K | `725da113ed673b3b17400e8d20b415352cc29689` |

Add QA-only `godot/qa/td-209/baseline-world.json` from K: Git blob `a2f01dc0654889faf1172a3cab39fa64857da6e7`, 71,458 bytes. This is supporting test data, not a runtime change.

Copy the following packaging files from `3d1f592fad58324bc2e752fc35a5a02f39527655`:
- `deploy/chunked/README.md`: `c30255d417fbb8b57cfb91f1e00ab5aaae33f611`
- `deploy/chunked/RELEASE_PLAN.md`: `270a5bb00f14be2b129793ab26b7482b47f46e66`
- `deploy/chunked/browser.test.mjs`: `c5b198a5b696975048f1193b01a52deb7f0d8360`
- `deploy/chunked/loader.js`: `67f1b5295defae043f437399bb95530e13145985`
- `deploy/chunked/p2-correction.test.mjs`: `6e582a797ba0b7a12dfabec09e1a37398817c3f9`
- `deploy/chunked/package.mjs`: `6b7586715f08cac8a2af4c30269b95bfd3550b2e`
- `deploy/chunked/package.test.mjs`: `713549b1458f7b7f50d231fb390f42245d4eab25`
- `deploy/chunked/shuto.test.mjs`: `1795b98b76e158ce2373a39c95e737774b778cb1`

### Import, export and verification boundaries

Use exact Godot `4.7.2.stable.official.ed1daf0bf` and matching 4.7.2 web templates; use the pinned repository bootstrap checksums rather than the installed 4.6.3 engine. Isolate HOME and XDG_DATA_HOME/XDG_CONFIG_HOME/XDG_CACHE_HOME consistently so template lookup finds that version. A normal clean 4.7.2 headless editor import succeeded here without native texture-recovery fixtures; none was needed or used. Preserve authored assets/import recipes. If another environment fails, retain its raw output and diagnose instead of silently changing import semantics.

Export preset `Web` from the base copy and `Web Shuto` from a separate otherwise-identical copy. Shuto's sole project.godot change is `run/main_scene="res://scenes/main_menu.tscn"` → `run/main_scene="res://scenes/shuto_c1/shuto_c1.tscn"`. Invoke the exact engine with `--headless --path <project> --export-release "<preset>" <output>/index.html`; retain import/export logs and hash actual resulting files. Previous pack sizes/hashes above identify these prepared exports, not a guarantee that another importer environment reproduces bytes. Record any new byte identity honestly; never relabel a different pack.

The cloud preparation's five canceled, non-shipping source gaps remain disclosed. Do not retry those canceled downloads or use another route to bypass the cancellation. If the continuation already has a complete authorized checkout, retain its existing non-shipping source files rather than deleting them to imitate the cloud omissions. A local reconstructed candidate is not a source commit: no final combined source commit exists in this handoff.

### New independently inspectable pack facts and status corrections

The actual prepared PCKs were mounted from an empty project and audited: base **1,328/1,328 readable, hash-indexed files; 115/115 GLB models load**; Shuto **1,164/1,164 files; 97/97 GLB models load**. Final audit logs contain zero errors/warnings. Base Fuel stations JSON SHA256 `2112bb609d6f4a02339cc400f870b729709f6cf5f745a71e1133633fe95c79db` matches pinned source; its starter coupe resource remap exists, all four repaired pedestrians and taxi load. The canceled bus is absent; Shuto excludes Lower City and td186 paths. The first audit's guessed optional JSON-path fixture error remains retained; the corrected final audit checks the actual stations JSON and starter_coupe.tres.remap. This establishes pack readability/resource closure for the checked paths, not ordinary menu/gameplay, native-OpenGL district geometry, WebGL/browser, phone or release acceptance.

The private 32 MiB create_blob attempt was interrupted without a response at approximately 06:05 UTC; expected object `46c22e2da32bb58cfa5d6240a983807d667b56cd` returned 404 in the 06:06 read-only check. No upload/ref change is confirmed, no retry is made, and the underlying cause remains unknown. No GitHub API size-limit failure was demonstrated; do not call the publication path ready.

Coordinator's 06:03 UTC fresh Shuto build marker returns the same `4ecd2089c1b292c11c70b7e9701f77df39cca044`; Shuto version.txt remains 404. This updates the earlier pending identity read only. No new live gameplay QA or deployment occurred.

Reproduction correction, 06:13 UTC: the preparation lead confirms the actual retained packs used **--export-debug**, not --export-release. To reproduce those artifacts, use `--headless --path <project> --export-debug "Web" <output>/index.html`, and `--export-debug "Web Shuto"` for the isolated Shuto copy. The preceding release-mode command is not the retained-artifact recipe. Exact engine/template bootstrap source is `scripts/bootstrap-godot.sh` at the HUD base. Standard import command is `--headless --path <project> --editor --quit`. Native GPU/OpenGL remains required for meaningful Kamome geometry readback.
