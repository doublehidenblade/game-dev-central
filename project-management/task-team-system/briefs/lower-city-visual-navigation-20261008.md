# Lower City visual navigation intake — 2026-10-08

Status: documentation only. New td-235/236 are blocked; no runtime author or allowlist is admitted.

## What the inspected frame actually shows

The supplied phone frame shows the pre-acceptance ASAHI RADIO DISPATCH detail screen: Available and Tracking tabs, Take This Gig and Back, followed by a tall text stack. It names Starlight Lounge door (Hoshi-dori / Chidori) and Gate 2 tally office (Gate 2 / Daikoku), a five-road Via string, ¥4,410 bounty, fresh fish on ice, 240 kg, 20 crates, medium durability and 2.5 km distance. A vertical scroll bar is visible. There is no map/path, cargo picture or destination imagery inside the panel. No build version is visible.

Only a cropped sliver of the minimap appears at upper right. The red-target/red-POI overlap is the player's report, not a reproduced screenshot finding. The private original and phone/gallery chrome are not published.

This is a screenshot-grounded intake, not a full flow audit: no taps, scrolling, font contrast measurement, screen-reader test or runtime build identity was verified from that frame.

## Two lanes, with existing owners preserved

1. [td-235: readable minimap target](https://github.com/doublehidenblade/tokyo-drift-3d/blob/docs/td235-236-visual-navigation-intake-20261008/godot/docs/tasks/td-235.md). Small presentation-only candidate: target-specific symbol, contrasting contour/backplate and clear in-view/off-screen shapes. Preferred boundary is MapSheet._draw_target plus target-only helpers. Do not change global MARK because it also colors other map semantics. No menu, input, zoom, shared CSS/DPR, scene, routing or gameplay change is proposed.
2. [td-236: visual briefing and central menu](https://github.com/doublehidenblade/tokyo-drift-3d/blob/docs/td235-236-visual-navigation-intake-20261008/godot/docs/tasks/td-236.md). One coherent future UI author owns the agreed shell/briefing region after handoff. td-215 remains the existing status-access task, td-200/201 own inventory/progression, td-217 owns damage, and td-232 owns payout reports. Those records/owners are not replaced or completed by this intake.

Historical td-203 minimap and td-205 gig-menu acceptance remain intact. This records new readability and navigation requirements, not a rewrite of their verdicts. td-213/214/219/228 repair behavior and existing acceptance limits are protected.

## Visual and interaction direction

- One discoverable MENU entry; icon-plus-English tabs: Map, Inventory, Car Condition, Gigs
- Gigs: Ongoing / Available / Completed filters; list plus selected detail side-by-side on wide screens, list then detail with explicit Back on portrait. Preserve filter, selection and scroll position
- Gig briefing: real road-route preview with distinct pickup/drop-off pins first; recognizable cargo illustration/icon; strong destination names and quoted fare; compact icon/value facts for weight, crates, fragility, time and distance. Secondary exact details remain available without another equal-weight paragraph stack
- Take This Gig accepts only the selected current offer. Selecting a row or map preview does not accept. Ongoing keeps actual phase/destination plus existing confirm-cancel flow
- Completed shows actual completed records with clear outcomes. Failed/cancelled work must never masquerade as success; preserve access to the existing result/retry flow
- Car Condition: clear graphic plus actual labels/values. Do not imply engine/tyre/body components exist when only gig-scoped body telemetry is exposed
- Inventory: actual owned-item grid when authority exists; label client cargo Current load. An unavailable state is honest until inventory is implemented
- Target marker: distinct pin/diamond in view and directional chevron at the edge, with solid light/dark contour or backplate. Shape and short label distinguish it from static POI blocks even in grayscale; it must stay visible at every pulse phase
- Fully opaque surfaces, readable English and CSS-sized controls. No decorative Japanese in controls; Japanese remains environmental art. New pictures represent actual cargo/location data, not fictional destinations

## Verified data prerequisites

Source inspected at live v49 `fa081b42197d50e6adaf202f899146fbffeab725`; the screenshot itself has no visible version.

- GigDispatch.make_offer stores real directed arc IDs in offer.route, with meters, plan_s, limit_s, from/to bays, fare and cargo. CityRouter.route computes connected directed arcs; each arc has geometry points and lane_path builds lane geometry. Use those points, not the lossy Via street-name string. Real pickup/drop-off pins remain distinct from any unverified final access segment
- Current-player-to-pickup only retains via_pickup street names. Do not invent a player GPS line or imply live rerouting. Any future route contract needs explicit owner verification; missing/unreachable geometry yields an honest unavailable state
- Existing cargo dictionaries expose six categories, real weight, crate-size text and durability. They are client cargo, not owned inventory
- GigDispatch keeps a completed count and latest offer/result, not a full completed-job collection. Completed list/history needs an owner-approved record/event contract with stable run identity, duplicate handling and explicit session/persistence semantics. Do not fabricate prior runs
- Body and cargo condition are gig-scoped; _start resets both to100. No persistent vehicle/component-condition claim is supported by that API
- Persistent owned items, suppliers, wallet and capacity remain blocked td-200/201. UI consumes approved read-only contracts and must not invent items, cash, grants or storage

[MapSheet source](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/map_sheet.gd), [GigDispatch source](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/gig_dispatch.gd), [CityRouter source](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/city_router.gd)

## Sequencing and admission gates

1. Independent documentation review and canonical task/board acceptance; fresh reservation check and exact file/region handoff
2. Scope and verify td-235 target-only rendering. It can avoid gig_menu ownership, but shared MapSheet ownership still requires handoff. Serialize future route-renderer edits with it
3. Lock a coherent responsive visual target and the data contracts. Full completed history, persistent inventory and condition remain explicit backend prerequisites, not placeholder data
4. Finish or explicitly hand off td-232 [PR550](https://github.com/doublehidenblade/tokyo-drift-3d/pull/550) before shared gig_menu work. Preserve its exact accepted settlement patch and all remaining visual gates
5. Reconcile [PR549](https://github.com/doublehidenblade/tokyo-drift-3d/pull/549) phone-fit hunks with the then-current composition. Its older whole gig_menu must not overwrite the live MapSheet-based CSS/DPR handling or td-213/232 work
6. Admit one bounded menu/briefing author with exact allowlist and existing status/data-owner handoffs. Do not parallelize writers in gig_menu.gd; do not grant authority over Craig's td-185 assembly/economy or td-217 damage
7. Require exact-head independent review, matched game-only before/after frames, real browser phone CSS/DPR checks, negative controls and input/modal regressions. Headless passes do not establish pixels, gameplay or Craig's phone acceptance

## Reservation and preservation snapshot

Source main `7ed841451ac62cb6138b2dd1f91ad6199d041621`; central main `9707cb939cb8115c53161da3b183d04eefcc9096`. New IDs were absent from these main task/board records and current relevant PR/branch searches. Existing td-234 source [PR552](https://github.com/doublehidenblade/tokyo-drift-3d/pull/552)/central [PR367](https://github.com/doublehidenblade/game-dev-central/pull/367), and td-233 [PR553](https://github.com/doublehidenblade/tokyo-drift-3d/pull/553)/[PR368](https://github.com/doublehidenblade/game-dev-central/pull/368), reserve their IDs and remain separate.

No comprehensive external-worker liveness or duplicate-guard registration is claimed. Existing owner queues were not read. Fresh preflight is still required before dispatch. All existing board rows are preserved byte-for-byte; two blocked rows are appended. No implementation, runtime tests/builds, Actions, merge, deployment, issue comment or external-agent contact. Shuto frozen; NEON paused.

## Recommended setup

Future author and independent reviewer: frontier capability, recommended gpt-6-astra/xhigh; provider-neutral and existing owners preserved. Model catalog observed during intake; implementation runtime, executor and Godot/render/browser readiness are unverified. Use wait_for_required_tier. After separate admission, bound each implementation slice to one initial pass plus one evidence-based correction within two hours, with independent frontier review and all required render/data/input tests reserved in advance. Stop for missing data authority, ownership overlap, excluded-file need, failed review or exhausted bound. No implementation outcome or worker admission is claimed.
