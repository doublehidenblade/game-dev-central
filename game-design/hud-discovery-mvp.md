# Tokyo Drift HUD and discovery MVP

> Researched: 2026-10-07 by dot design research. Design before implementation. For Craig and the existing feature owners. This is a published draft proposal, not a shipped feature or a runtime acceptance verdict.

## Recommended direction

Use a compact analog instrument panel around a clear driving view. Japanese belongs on the buildings and physical objects. HUD information appears in the player's selected language, with a translated place name when looking at or arriving at a place. No permanent Japanese/English double-labels on every control.

Keep cash, speed and fuel continuously visible during driving. Keep vehicle, cargo and load accessible through a permanent status icon; promote each to a visible warning only when action is needed. This reconciles “always accessible” with warnings-only secondary instruments without hiding essential state. Offer an optional pinned full-status row, not a second HUD implementation.

The distinguishing details are an enamel/brass instrument fascia, clear pedal silhouettes, a folded-map icon, one Japanese-police-inspired wanted emblem with three lamps, and a satisfying stamped delivery receipt. All panels are opaque. No translucent brown cards, tiny bilingual paragraphs or general cyberpunk decoration.

## What the current sources actually contain

- Research snapshot of game main is `9d4a88490c41f86e8d34e1c2c6f142838de20c73`; PR446 is `64ccf666847499c076edaffcebf2ca303f462a8f`; PR457 is `827e058c6e11e8bb923b9fefa7471227bae59a40`. Both PRs are open drafts at inspection.
- Cash is already displayed in PR457 FuelHud: `FUEL %.2f km · ¥%d`, using FuelService's balance. This is a visibility/publication gap, not missing cash functionality. Preserve one wallet authority; do not introduce a HUD-owned balance.
- Main GigDispatch already has cargo weight values (15–320 kg in its cargo catalogue). These are metadata, not proof of a complete aggregate load/capacity/handling system.
- Main BODY is real impact-derived information held in GigDispatch, reset for a gig. It does not produce a chassis-wreck event. A persistent vehicle condition system is still a separate contract. The HUD must never claim the current BODY number is that system.
- Muse owns td-203 map/minimap, td-204 health and td-205 gig menu/settlement. dot's existing td-200 covers persistent ownership, carried goods and discovered suppliers; td-201 covers workshop/reveal UI. Use these tasks before inventing a duplicate discovery/save system.
- The Fuel-versus-menu repair is already independently reported as passing. Its published composition evidence separately reports 772 native and 772 browser assertions with retained renderer failures. Do not conflate those scopes or redo that narrow overlap patch as the new design.
- Open unrelated composition defects remain: expanded landscape minimap intercepts GAS release; DamageBar's clipped stripe triangulation fails. The new layout must include these as explicit regressions, not quietly label the overall build clean.

## Layout and interaction contract

### Driving

Top edge: compact cash at left; fuel range with pump icon; speed in km/h in the instrument cluster; pause at the far edge. Keep currency and units legible. Fuel remains estimated road range; do not imply remaining route distance or guaranteed reachability.

Left edge: current gig objective in one line with time beneath, expandable through the existing GigMenu. Right edge: Muse's minimap in a reserved dock, collapse/expand through the same map renderer. Map expansion is explicit, never triggered by releasing a pedal beneath it.

Bottom: existing steering controls and two pedal buttons. Gas is a long ribbed accelerator; brake is a visibly wider pedal pad. Preserve familiar physical placement and independent multi-touch. Text explanations belong in hover/focus help and the first-use lesson, not on every frame. Icons require accessible names.

The center driving corridor stays clear. A context cue sits above the driving controls, never over the vehicle or horizon. All interactive targets are at least 44 screen pixels in the smallest supported layout; moving driving controls should be larger. Reserve the actual hit rectangles, including padding, not just painted bounds. Text scales in screen pixels, not only design-canvas units.

### Secondary status

A single always-present car/status button reveals car condition, cargo condition, and carried weight/capacity. Healthy axes have quiet icons; no cargo explicitly reads “No cargo,” never “100% cargo.” Values unavailable from an authority read unavailable, not a fabricated healthy value.

- Damage: retain existing damaged/critical thresholds and the existing critical-before-failure guarantee. Damaged produces a brief change notice and small persistent warning; critical keeps its value and action visible until resolved. Cargo and car use different silhouettes.
- Weight: when healthy, details show `240 / 300 kg` as an example, not a hardcoded starter capacity. At overload the load icon turns red and the exact ratio stays visible with “Overloaded · slower, harder to steer.” Red is supplemented by the warning shape and words.
- Cash and fuel update from existing authority signals. A payout animates the existing balance, never awards money from the animation.
- Desktop hover and keyboard focus reveal concise labels. Phone first encounters teach one control at a time while parked or paused; repeat help remains available in status/help. No tutorial grabs steering during a chase.

### One presentation owner per state

Specify shared reserved zones and priorities before styling individual cards. Only the coordinator assembly changes global placement. Feature owners provide content and state, not competing relocation heuristics.

Arrest owns the center while its sequence runs; hold ordinary settlement presentation until release without delaying the actual gig settlement. Payment owns a paused confirmation sheet. Full map, gig menu and status details use one active sheet with explicit Back/Close. Changing orientation must cancel or safely preserve a held touch, never reinterpret its release as a different action. Normal driving inputs do not leak through any sheet.

## Shop recognition and discovery

Use the existing artbook's distance hierarchy: silhouette and light first, fine signs near the shop. A garage should read as an open service bay with tires and a hoist; a fuel stop as a canopy and mechanical pump; a market as noren, crates and cold-room frontage. Vary recognizable silhouettes within Claude's asset direction, rather than placing the same floating label on generic boxes.

1. **Unseen:** no permanent named map marker. A quest lead can show a coarse lead or address, explicitly distinct from discovering a shop or knowing its inventory.
2. **Looking/approaching:** one short localized name and service icon for the best visible candidate. Use camera-facing/visibility and entrance association, not proximity through a wall. Stabilize the candidate to avoid flicker. Translation need not replace or duplicate the actual sign.
3. **Arrived:** inside the real service area and sufficiently slow, show the existing interaction button and verb. No automatic purchase or service. Discovery itself does not require payment.
4. **Discovered:** emit one stable POI-ID event, save it, and show “Added to map” once. Muse's map consumes the same record and category icon. Leaving, failure, arrest and reload do not remove it.

For suppliers, retain td-200's physical pull-in requirement: seeing the facade can reveal its name, but entering the service area establishes discovery. Discovery reveals the place, not all future blueprints, prices or stock. td-201's prerequisite rules still apply.

Permanent means across reloads, not merely until the scene resets. Current fuel/cash are run-scoped. Reuse td-200's planned versioned discovery field or agree one narrow shared persistence contract; do not secretly create a second wallet/save authority. If storage fails, retain session discovery and disclose that it could not be saved. Browser data clearing and a deliberate profile reset are separate from ordinary “fresh run.”

## Wanted indicator grounded in Japanese references

The Tokyo Metropolitan Police flag specification dates to Showa 40 (1965) and defines a white sun emblem with 20 rays. Its official drawing was inspected. This is a documented Japanese police reference, not a Western five-point sheriff star. The modern MPD uniform insignia was also inspected; use it only as a recognition reference, not evidence of a Showa-period uniform.

**Preferred mock:** one compact fictional KMTED sunburst-like medallion enclosing the artbook's existing split-flap roundel, followed by three rectangular instrument lamps. The medallion is an adaptation for this fictional force, not an “authentic Japanese badge.” Keep the original faction roundel identifiable. Do not duplicate three badges or introduce official agency wording.

At level 0 the cluster is quiet and compact. Levels 1–3 illuminate one to three segments and briefly show the corresponding existing runtime state in the selected language. Add a restrained beacon/dispatch cue and a short reason after an offense. Clearing shows one confirmation, then returns to the quiet state. Never imply roadblocks, bribes, seizure trucks or other lore mechanics exist merely because the artbook names them.

**Canon reconciliation:** the artbook text specifies municipal blue roundels and amber beacons. The actual inspected `impl-kmted-cruiser.png` visibly has red roof lamps. Record this text/image discrepancy; a HUD design task must not silently repaint Claude's cruiser or rewrite faction canon. Real Tokyo police red-light and black/white-car references establish recognition cues, not a mandate to replace the fictional putty-gray/blue livery. Compare the preferred medallion mock with a simpler beacon-plus-roundel option before implementing.

## Delivery success should feel earned

Reuse GigMenu's settlement authority and actions. A successful delivery gets a quick opaque “DELIVERED” stamp/snap, a short mechanical chime, and a count-up to the exact settled payout. Then show a compact receipt: payout and any actual bonus/condition deduction, plus the recommended next gig. Cash confirms the same increment. Do not invent bonuses absent from the result data.

Keep “Take next,” “All gigs,” and “Close.” No auto-accept, no timeout that removes the receipt, no duplicate payout on reopen. The initial celebration may finish quickly; the receipt persists. Arrest/failure never plays success effects. Reduced-motion mode uses a static stamp and final amount. Celebration motion does not use transparency or obscure live pedals.

## Weight MVP and later inventory

MVP reads an aggregate carried mass and vehicle capacity. Include client cargo and owned supply packs once each. Permit overload, keep the red warning visible, and apply monotonic, bounded penalties through the existing vehicle capability/controller contract. Suggested tuning experiments: no penalty up to capacity; progressive acceleration/top-speed reduction and less responsive handling beyond it. Validate feel with the real car; do not add random steering or rewrite the controller. Capacity and penalty curves are tuneable data, not numbers invented by the HUD.

Loading must display the resulting weight and penalty before confirmation, but weight alone cannot block it under this brief. Any separate physical-space rule must be explicit. Clear load/penalties on actual unload, not on opening/closing UI or settling an unrelated transaction.

Later scope, explicitly deferred: physical slots, item placement, weight distribution, center of gravity, shifting or falling cargo. Preserve item/mass IDs for that extension. Do not build rigid-body cargo simulation for this MVP.

## Proposed work split (not assignments)

1. **Design and composition contract:** one owner prepares responsive state mocks, icon/text rules, reserved bounds and presentation priority. No implementation until these are inspected. No new task numbers assumed here.
2. **dot Fuel/Wanted presentation:** adapt the existing owned FuelHud and WantedHud to the agreed slots and icon style; expose read-only balance/range/wanted data. Do not touch Muse map/gig/health or Claude assets in this slice.
3. **Pending Muse coordination — map and gig surfaces:** map icon/dock, discovery-marker consumer, concise objective, secondary health presentation and rewarding settlement. Keep the GAS hit-test defect and DamageBar rendering defect separately tracked under their respective owners.
4. **dot td-200/201 discovery and load:** stable POI discovery/persistence and aggregate load/capability contract, reconciled with garage suppliers and prerequisites. Serialize GigDispatch schema/assembly edits through its owner; a display worker must not independently modify the same file.
5. **Pending Claude coordination — shop assets:** readable facade silhouettes and Japanese physical signage within existing assets. Provide a short data-facing POI/entrance/sign spec, not parallel shop models from dot.
6. **Independent integration reviewer:** pinned combination, before/after cameras, real browser input and phone verdict. Work split is a recommendation; no outside agent was contacted and no code was written in this pass.

## Mock set and acceptance

Create six labelled design states over real current Lower City camera frames: calm driving; two critical conditions plus overload; shop approach/arrival; first discovery plus map; wanted 1/3 and 3/3; successful delivery. Check each in 844×390 and 390×844, plus one desktop composition. Use actual artbook references; mark generated images as design mocks, never runtime proof. Inspect icon recognition and Japanese glyphs at final display size. Preserve opacity and deliberate symmetry.

Acceptance must establish:

- Cash/speed/fuel readable and continuously present while driving; every secondary value one action away; critical states promoted correctly with no false healthy data.
- No persistent bilingual double labels; Japanese signs preserved; contextual translations accurate and stable; no tofu glyphs.
- Pedal holds/releases and steering multi-touch cannot open map/menu, including orientation changes and controls becoming visible mid-gesture. A broken-baseline test must fail at the existing GAS overlap coordinate.
- All sheet permutations preserve pause ownership, Back/Close, input isolation and arrest timing; no duplicate settlement or debit.
- First visit emits once, revisits do not spam, through-wall proximity does not discover, and discovered markers survive restart/reload using the same POI ID.
- At equal car/input/road conditions, increased overload monotonically lowers the intended performance; unloading restores it; aggregate mass matches cargo and supplies with no double-count.
- Success payout animation equals the authoritative result and current balance; next gig is explicit; failure/arrest cannot show success.
- Actual full-resolution captures are inspected. Godot 4.7.2 native and browser tests are separate from physical-phone performance and Craig's final visual verdict. Retained baseline errors remain disclosed.

## Sources

Repository sources inspected on 2026-10-07:

- [Artbook identity and KMTED design](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/gig-city-retrofutur-identity.md)
- [Factions chapter and existing roundel](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/art-book/factions/chapter.md)
- [Lower City silhouette hierarchy](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/art-book/lower-city/chapter.md)
- [Showa grounding](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/art-book/showa-grounding.md) and [Japanese text audit](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/art-book/text-audit.md)
- Inspected artbook pixels: [KMTED](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/art-book/factions/impl-kmted-cruiser.png) and [Kotobuki garage](https://github.com/doublehidenblade/game-dev-central/blob/main/game-design/art-book/lower-city/mock-kotobuki.png)
- [Standing rules](https://github.com/doublehidenblade/game-dev-central/blob/main/knowledge/standing-rules.md), [current task board](https://github.com/doublehidenblade/game-dev-central/blob/main/project-management/boards/tokyo-drift-3d.md)
- [PR446](https://github.com/doublehidenblade/tokyo-drift-3d/pull/446), [PR457](https://github.com/doublehidenblade/tokyo-drift-3d/pull/457), [FuelHud balance display](https://github.com/doublehidenblade/tokyo-drift-3d/blob/827e058c6e11e8bb923b9fefa7471227bae59a40/godot/scripts/lower_city/fuel_hud.gd#L284-L299)
- [Pinned composition proof](https://github.com/doublehidenblade/tokyo-drift-3d-web/tree/2ef7e2ece8331c3835f60dc4c04a3d2633d9fd34/qa/td-206/composition). Inspected local copies of arrest, settlement, repaired Fuel/next-gig, map/GAS overlap and portrait fuel confirmation screenshots; fixture scenes are not new live-play evidence.
- Main tasks [td-203 map](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-203.md), [td-204 health](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-204.md), [td-205 gig menu](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-205.md), [td-200 inventory/save](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-200.md), [td-201 workshop discovery](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-201.md)

Authoritative police references:

- [Tokyo Metropolitan Police flag specification, Showa 40](https://www.reiki.metro.tokyo.lg.jp/reiki/reiki_honbun/g101RG00002176.html): documented 20-ray sun emblem; official drawing inspected
- [MPD uniform emblem explanation](https://www.keishicho.metro.tokyo.lg.jp/book/mamechishiki/mame01/): modern uniform emblem image inspected; not asserted as a Showa-era design
- [MPD police-box and patrol-car history](https://www.keishicho.metro.tokyo.lg.jp/about_mpd/shokai/pipo/webpb/koban_qa.html): red-light symbol; national black/white patrol-car scheme in Showa 30
