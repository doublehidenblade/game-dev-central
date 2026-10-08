# Lower City visual navigation intake — 2026-10-08

Status: documentation only. New td-235/236/237 are blocked; no runtime author or allowlist is admitted.

## What the inspected frame actually shows

The supplied phone frame shows the pre-acceptance ASAHI RADIO DISPATCH detail screen: Available and Tracking tabs, Take This Gig and Back, followed by a tall text stack. It names Starlight Lounge door (Hoshi-dori / Chidori) and Gate 2 tally office (Gate 2 / Daikoku), a five-road Via string, ¥4,410 bounty, fresh fish on ice, 240 kg, 20 crates, medium durability and 2.5 km distance. A vertical scroll bar is visible. There is no map/path, cargo picture or destination imagery inside the panel. No build version is visible.

Only a cropped sliver of the minimap appears at upper right. The red-target/red-POI overlap is the player's report, not a reproduced screenshot finding. The private original and phone/gallery chrome are not published.

This is a screenshot-grounded intake, not a full flow audit: no taps, scrolling, font contrast measurement, screen-reader test or runtime build identity was verified from that frame.

## Coordinated lanes, with existing owners preserved

1. [td-235: readable minimap target](https://github.com/doublehidenblade/tokyo-drift-3d/blob/docs/td235-236-visual-navigation-intake-20261008/godot/docs/tasks/td-235.md). Small presentation-only candidate: target-specific symbol, contrasting contour/backplate and clear in-view/off-screen shapes. Preferred boundary is MapSheet._draw_target plus target-only helpers. Do not change global MARK because it also colors other map semantics. No menu, input, zoom, shared CSS/DPR, scene, routing or gameplay change is proposed.
2. [td-236: visual briefing, editable route planning and central menu](https://github.com/doublehidenblade/tokyo-drift-3d/blob/docs/td235-236-visual-navigation-intake-20261008/godot/docs/tasks/td-236.md). One coherent future UI author owns the agreed shell/briefing region after handoff. td-215 remains the existing status-access task, td-200/201 own inventory/progression, td-217 owns damage, and td-232 owns payout reports. Those records/owners are not replaced or completed by this intake.

3. [td-237: synchronized itinerary and destination cues](https://github.com/doublehidenblade/tokyo-drift-3d/blob/docs/td235-236-visual-navigation-intake-20261008/godot/docs/tasks/td-237.md). One shared navigation model and typed AR/world-cue lane, proposed from the explicit follow-up. td-236 edits and renders this model; it does not own another route store. td-235 remains display-only. All runtime scope stays blocked pending review and exact handoffs.

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
- Current-player-to-pickup only retains via_pickup street names. The follow-up now explicitly requests editable route planning and real player-to-next-stop geometry, superseding the initial static-preview-only restriction. td-237 must provide the single validated directed-arc/layer/entrance contract; td-236 consumes it. Missing/unreachable segments remain honestly unavailable, and no straight-line GPS path is invented
- Existing cargo dictionaries expose six categories, real weight, crate-size text and durability. They are client cargo, not owned inventory
- GigDispatch keeps a completed count and latest offer/result, not a full completed-job collection. Completed list/history needs an owner-approved record/event contract with stable run identity, duplicate handling and explicit session/persistence semantics. Do not fabricate prior runs
- Body and cargo condition are gig-scoped; _start resets both to100. No persistent vehicle/component-condition claim is supported by that API
- Persistent owned items, suppliers, wallet and capacity remain blocked td-200/201. UI consumes approved read-only contracts and must not invent items, cash, grants or storage

[MapSheet source](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/map_sheet.gd), [GigDispatch source](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/gig_dispatch.gd), [CityRouter source](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/city_router.gd)

## Editable itinerary and AR follow-up — 2026-10-08

The player reports a visitor reached the minimap pickup location but missed the painted parking box. This has not been reproduced in new screenshots. The requested improvement includes current player facing, editable POI detours, compact through-environment flags with live distance, close-range light-column/arrival cues, custom-stop auto-clear/advance, and threshold-driven fuel/repair icons.

### Single synchronized itinerary

- Exactly one revisioned model owns default/edited routes and active custom stop. Briefing, map, minimap and world cues subscribe to identical stop IDs, world anchors, route geometry and revision
- Required pickup/drop-off remain ordered and owner-controlled. Custom POIs/stops may be added, reordered or removed within valid mission legs. Preview/Apply/Cancel and stale-revision handling belong to one edit transaction; selecting an offer never accepts it
- Actual CityRouter arcs and verified POI bay/service entrances define every leg. nearest_arc skips ramps by default, so layer-aware validation must cover ramps/bridges/trench explicitly. Invalid/unreachable edits retain the last valid plan; do not invent access connectors
- Player location and facing use the real vehicle basis, not velocity or camera bearing. Direct-distance labels use actual 3D player-to-anchor distance; road distance, when shown, is separately labelled
- Custom arrival checks the active stop's 3D surface/layer, clears its cue from every surface atomically and advances once. Repeated frames, same-XZ wrong-deck passes, high-speed crossing, overlap, teleport/recovery and edits cannot chain-consume stops
- Mission entry merely prompts LOAD/UNLOAD. Flags persist through loading/unloading and advance only on the authoritative pickup-completed phase or delivery outcome. No proximity acceptance, mission completion, payout or service payment
- Route edits cannot reset/extend deadlines, change fare/settlement/damage or grant time. Preserve current pause semantics and compare at equal unpaused elapsed time

### Typed compact cues and real arrival area

Use distinct custom/pickup/drop-off/fuel/repair symbols plus short English distance labels and solid contrasting outlines. Through-environment means the marker can render over occluding geometry, not that the environment becomes transparent. Off-screen/behind-camera cues remain within safe areas and do not intercept driving touches.

Close to a target, a bounded light-column-like/emissive beacon plus ground-area cue must identify its real bay or valid arrival surface without hiding the car/road. Source confirms CitySigns._gig_bays draws a heading-aligned 2.6 m by 9 m painted box at the actual at/h position. GigDispatch's valid interaction envelope is different: currently 7 m horizontal radius, less than 2.5 m height difference and below 2.2 m/s, followed by explicit LOAD/UNLOAD. Preserve both envelopes; do not resize gameplay rules to match marker art.

### Fuel, condition and repair truth

FuelService.range_snapshot exposes actual range and low_range; the effective starter FuelProfile threshold is currently 2.5 km. Real FuelStation objects expose service_position, road_arc and layer-aware contains_car. Fuel icons may reveal those real services; no automatic waypoint insertion, route mutation, refill, tow or charge.

Condition warnings must use the existing owner's valid numeric vehicle-health scope and an admitted configurable display threshold. Current car_hp is gig-scoped, cargo_hp is not vehicle health, and FuelService's wreck-event hook is not a numeric-health provider. CityDressing repair-bay scenery is not a repair-service registry. Until a real repair provider/entrance exists, show a truthful advisory/unavailable-service state rather than inventing a repair map pin. Test threshold boundaries, hysteresis, stale/unavailable state and recovery without changing economy or damage thresholds.

[CitySigns bays](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/city_signs.gd), [FuelService](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/fuel_service.gd), [FuelStation](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/fuel_station.gd)

## Sequencing and admission gates

1. Independent source/board review, canonical acceptance and fresh reservation check. Agree td-237's one-model contract, real layer/entrance data and mission/service/health ownership first
2. Complete td-235 as the small target-display prerequisite, then explicitly hand off the renderer region. Do not expand it into an itinerary or create competing minimap writers
3. Admit one bounded td-237 navigation/cue author only after exact scope and assembly adapters are handed off. Use sequential, separately reviewed slices; data/arrival tests precede rendered cue acceptance
4. td-236 then consumes the stable itinerary API for current-facing and POI route editing. Its shared gig_menu work still waits for td-232 [PR550](https://github.com/doublehidenblade/tokyo-drift-3d/pull/550), [PR549](https://github.com/doublehidenblade/tokyo-drift-3d/pull/549) phone-fit and td-215 handoffs. Preserve exact current MapSheet CSS/DPR behavior; never overlay an older whole file
5. Existing owners deliver any missing authoritative status/history/repair/inventory interfaces; these tasks cannot manufacture those capabilities or take over td-185/215/217/200/201
6. Independent exact-composition review covers synchronized edits, actual facing, typed AR/near cues, distance, layer-aware once-only custom arrival, mission completion boundaries, fuel/condition warning states, unchanged economy/deadlines and relevant input/modal regressions. Require matched game-only rendered/browser evidence and Craig's phone verdict

## Reservation and preservation snapshot

Source main `7ed841451ac62cb6138b2dd1f91ad6199d041621`; central main `9707cb939cb8115c53161da3b183d04eefcc9096`. New IDs were absent from these main task/board records and current relevant PR/branch searches. Existing td-234 source [PR552](https://github.com/doublehidenblade/tokyo-drift-3d/pull/552)/central [PR367](https://github.com/doublehidenblade/game-dev-central/pull/367), and td-233 [PR553](https://github.com/doublehidenblade/tokyo-drift-3d/pull/553)/[PR368](https://github.com/doublehidenblade/game-dev-central/pull/368), reserve their IDs and remain separate.

No comprehensive external-worker liveness or duplicate-guard registration is claimed. Fresh preflight is still required before dispatch. The extension is reconciled with source main fe2bb9f8251586a8fd793aea2535d822ed8f0941 and central main 70a99e09aec85f52b2f93b19ac080579d780f83a, preserving the merged td-234 reservation. td-237 was absent from current main task/board, matching branch and relevant open-PR scans. Existing board rows are preserved byte-for-byte; three blocked intake rows are appended. No implementation, runtime tests/builds, Actions, merge, deployment, issue comment or external-agent contact. Shuto frozen; NEON paused.

## Recommended setup

Future author and independent reviewer: frontier capability, recommended gpt-6-astra/xhigh; provider-neutral and existing owners preserved. Model catalog observed during intake; implementation runtime, executor and Godot/render/browser readiness are unverified. Use wait_for_required_tier. After separate admission, bound each implementation slice to one initial pass plus one evidence-based correction within two hours, with independent frontier review and all required render/data/input tests reserved in advance. Stop for missing data authority, ownership overlap, excluded-file need, failed review or exhausted bound. No implementation outcome or worker admission is claimed.
