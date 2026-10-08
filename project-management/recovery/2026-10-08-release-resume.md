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
