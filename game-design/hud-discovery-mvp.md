# Tokyo Drift HUD and discovery MVP

> Researched: 2026-10-07 by dot design research. Revised after Craig’s desktop, minimap, police-symbol and payout-report feedback. Design before implementation. For Craig and the existing feature owners. This is a proposal, not a shipped feature or a runtime acceptance verdict.

## Latest direction takes precedence

Craig’s latest feedback supersedes the earlier opaque driving-HUD treatment, large desktop touch-oriented text, permanent desktop pedals, and medallion-plus-lamps wanted proposal. Use a clear, background-free driving overlay with small readable desktop text; use the supplied Japanese police symbol itself as the repeated wanted-level marker. This is an explicit UI exception to the older general opaque-rendering rule. World geometry still follows its existing material rules. Do not solve the HUD request with a large transparent or opaque card that still obscures the road.

Source: Craig’s message `Sentinel_458257ab5d688191ba02eeeb40310146`. The corrected visual boards are a separate mock deliverable. Craig’s actual police reference was inspected for this revision: a gold circular center with distinct long pointed sun rays. Its silhouette is the shape authority; no new board is claimed as runtime proof.

## Recommended direction

Use a compact analog instrument panel around a clear driving view. Japanese belongs on the buildings and physical objects. HUD information appears in the player's selected language, with a translated place name when looking at or arriving at a place. No permanent Japanese/English double-labels on every control.

Keep cash, speed and fuel continuously visible during driving. Keep vehicle, cargo and load accessible through a permanent status icon; promote each to a visible warning only when action is needed. This reconciles “always accessible” with warnings-only secondary instruments without hiding essential state. Offer an optional pinned full-status row, not a second HUD implementation.

The distinguishing details are precise instrument-like type, a compact always-visible minimap, repeated recognizable Japanese police symbols, bold green money, and a satisfying graded delivery receipt. Driving HUD labels and icons have no filled backing. Use a restrained text outline or shadow for contrast, tested against bright and dark streets. Analog character comes from typography and interaction, not a dashboard slab blocking the view. Touch pedal silhouettes appear only in the mobile/touch layout.

## What the current sources actually contain

- Tokyo main was rechecked at 15:52 UTC and remains `9d4a88490c41f86e8d34e1c2c6f142838de20c73`. The earlier inspected PR446/457 heads remain the design evidence pins, not a new runtime acceptance. Central design PR344 merged as `60a4f56f80bf15ca55105da4da6712b7dd091e2b`; worker-selection policy PR345 merged as `4a074eff99fffd93fda4ea5d8d6ef13d2794e9ae`. This revision updates the existing design, not a second plan.
- Cash is already displayed in PR457 FuelHud: `FUEL %.2f km · ¥%d`, using FuelService's balance. This is a visibility/publication gap, not missing cash functionality. Preserve one wallet authority; do not introduce a HUD-owned balance.
- Main GigDispatch already has cargo weight values (15–320 kg in its cargo catalogue). These are metadata, not proof of a complete aggregate load/capacity/handling system.
- Main BODY is real impact-derived information held in GigDispatch, reset for a gig. It does not produce a chassis-wreck event. A persistent vehicle condition system is still a separate contract. The HUD must never claim the current BODY number is that system.
- Muse owns td-203 map/minimap, td-204 health and td-205 gig menu/settlement. dot's existing td-200 covers persistent ownership, carried goods and discovered suppliers; td-201 covers workshop/reveal UI. Use these tasks before inventing a duplicate discovery/save system.
- The Fuel-versus-menu repair is already independently reported as passing. Its published composition evidence separately reports 772 native and 772 browser assertions with retained renderer failures. Do not conflate those scopes or redo that narrow overlap patch as the new design.
- Open unrelated composition defects remain: expanded landscape minimap intercepts GAS release; DamageBar's clipped stripe triangulation fails. The new layout must include these as explicit regressions, not quietly label the overall build clean.

## Layout and interaction contract

### Desktop and browser driving

Use a true desktop layout, not an enlarged phone canvas. No steering arrows, gas/brake touch buttons or empty reserved pedal space on desktop. Show a first-run keyboard lesson before the first drive: W or Up accelerates, A/D or Left/Right steer, S or Down brakes/reverses according to the actual controller mapping. Verify that exact mapping before shipping the lesson; do not teach an unsupported action. Dismiss once, keep Help available, and do not repeat every scene load. Keyboard/mouse are the desktop default; a phone running a browser still gets touch controls. Avoid a browser-versus-native rule that misclassifies mobile web.

Use approximately 16–18 screen-pixel desktop labels and 20–24 pixel key values as mock starting points, then inspect at real 1280×720 and 1920×1080 sizes. These are not mandatory phone sizes. Keep keyboard focus affordances and hover help, but do not apply the phone’s 44-pixel target minimum to every desktop text label.

Top left: bold green cash (`¥10,510`), with compact objective/time below. Place small fuel range and speed near the lower edge or in another stable corner without a backing card. Fuel is estimated road range, never a guarantee of reaching a destination. Use a single localized label only when an icon needs teaching.

Top right: an always-visible compact minimap, approximately 160–200 desktop screen pixels across as a mock starting point. It shows actual roads, N/E/S/W, the player position and facing wedge, and the current pickup/drop-off destination bearing. Keep north fixed and rotate the player wedge so current facing is clear. An off-map arrow carries target bearing; do not invent a GPS route line or road-route ETA. When there is no gig, compass/player tracking remain. Clicking the minimap opens the existing large map; Close/Escape returns to the same mini view. A separate MAP text card or map icon is not a substitute for this visible map. Do not collapse it to an icon by default. The map’s own small geographic field is necessary content, not a larger decorative HUD backing.

Wanted symbols sit in a compact row clear of the map and objective. Leave the center, horizon and vehicle silhouette unobstructed. The shop context cue is one brief line near the lower center, not a panel.

### Mobile and touch driving

Keep larger, thumb-safe text and existing steering controls with two pedal silhouettes. Gas is a long ribbed accelerator; brake is a wider pad. Preserve physical placement and independent multi-touch. First-encounter teaching is short and parked/paused; never steal live steering. The minimap remains visible with N/E/S/W, facing and destination bearing, and tapping it opens the same large map.

Mobile interactive targets remain at least 44 screen pixels; driving controls should be larger. Reserve actual hit rectangles including padding. No expanded minimap region may cover gas/brake targets. On mixed-input devices, allow explicit touch controls or a stable device/input setting; a stray touch must not suddenly rearrange the HUD during a drive.

### Secondary status

A single always-present car/status button reveals car condition, cargo condition, and carried weight/capacity. Healthy axes have quiet icons; no cargo explicitly reads “No cargo,” never “100% cargo.” Values unavailable from an authority read unavailable, not a fabricated healthy value.

- Damage: retain existing damaged/critical thresholds and the existing critical-before-failure guarantee. Damaged produces a brief change notice and small persistent warning; critical keeps its value and action visible until resolved. Cargo and car use different silhouettes.
- Weight: when healthy, details show `240 / 300 kg` as an example, not a hardcoded starter capacity. At overload the load icon turns red and the exact ratio stays visible with “Overloaded · slower, harder to steer.” Red is supplemented by the warning shape and words.
- Cash is always bold green during driving and updates from the existing authority, including spends and payouts. Contrast comes from a fine outline, not a background card. Fuel updates from its own authority. A payout animates the existing balance, never awards money from the animation.
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

## Wanted symbols from Craig’s police reference

Use the recognizably reproduced Japanese police symbol from Craig’s supplied image as each of the three wanted-level markers. This explicitly replaces the earlier proposed combined KMTED medallion and rectangular lamps. Do not simplify it into a generic star, gear, flower or invented crest; inspect the original and test the distinctive ray/sun shape at actual display size. Preserve three existing runtime levels: active symbols are clearly filled/high-contrast, inactive markers quiet outlines. At zero, keep the row minimal. Color is not the only indication.

The supplied image controls the silhouette. The design researcher inspected the supplied reference as an authoring input; the image is not included in this documentation-only revision. Before implementation, the mock owner must obtain that exact supplied image rather than infer it from this description. Preserve its center-to-ray proportions and distinct pointed silhouette. The mock owner must include a side-by-side comparison at final icon size. Historical corroboration remains useful: the official Tokyo Metropolitan Police flag specification dates to Showa 40 (1965) and defines a 20-ray sun emblem. That does not establish that every supplied police emblem is the same historical design, or that its image is automatically licensed for reuse. Use an original, faithful UI rendering of the recognizable symbol with documented source, not an unsupported claim of an official or licensed asset.

Short localized crime/clear notices can appear briefly. No constant bilingual WANTED panel. Replacing symbols does not change police escalation, collisions or arrest. Do not infer unimplemented lore mechanics from the icon count. Claude’s faction roundel and cruiser livery remain their own asset work; the amber-beacon text versus red-lamp artwork discrepancy remains recorded rather than silently resolved by this HUD task.

## Delivery grading and itemized payout

A delivery is a success even when it is late. “DELIVERED” must never be red: use cream/green and a brief stamp/snap with a mechanical chime. Money is bold green. Red outcome headings are for WASTED, BUSTED, OUT OF GAS and genuine failure. A late successful delivery gets a clear “Late by 0:20” grade/deduction, not an erroneous red failure title.

Show separate grades for cargo condition and delivery time. Time grading appears only for timed contracts. Untimed contracts say “Time: Not rated” or omit the time row; they have no deadline, timing bonus or late deduction. Preserve readable raw facts alongside grades: condition percent, actual delivery duration, target duration and lateness when applicable. Initial grade proposal for owner review: cargo A at 90–100%, B at 75–<90%, C at 50–<75%, D above 0–<50%; zero condition is a failed delivery. Timed delivery A on time, B up to 30 seconds late, C over 30 up to 60 seconds late, D beyond 60 seconds. These grade thresholds are new configurable presentation design, not existing runtime facts, and grades must not apply an extra money multiplier.

The expanded receipt itemizes base fare, time bonus or late deduction, cargo damage deduction, explicit rounding adjustment if needed, and net payout. Show the resulting wallet balance separately from the payout. Display deductions neutrally/amber with minus signs; keep DELIVERED and credited money distinct. The small automatic receipt can show the two grades plus net payout and an explicit “Details” expansion; do not cover the driving view with the full breakdown. Never hide the only route to the itemized report. User-opened report/details may occupy a compact readable surface, but need no broad full-screen dim or decorative background. Keep the minimap visible while the automatic summary is present.

Keep the existing Take next, All gigs and Close flow; no auto-accept or timeout. Expanded report content must remain available through the existing last-result lifecycle. Arrest/failure never plays success effects. Reduced motion shows the final stamp and amount immediately. No duplicate payment on report reopen or animation replay.

### Actual source contract and minimum change

The inspected `GigDispatch._physics_process` already allows `time_left` to go negative and still enables UNLOAD. Cargo at zero fails; simply reaching a deadline does not. `_settle` already computes a timing multiplier and cargo-condition multiplier and credits `earnings` once. Current tuning offers up to +25% for time left; lateness decreases its multiplier to 0.30 over 60 seconds. This is a timing floor, not a guaranteed 30% of the base payout after damage. Keep those mechanics unless the economy owner deliberately revises them; no new late-failure logic is needed.

Every generated offer currently has `limit_s`; there is no explicit timed/untimed contract. Add a deliberate `is_timed` field (existing offers migrate/default to true). Untimed flow does not present or deduct a countdown, uses timing factor 1, has no timing reward/penalty and reports time grade as not applicable. Preserve `clock(time_left, cargo_hp, car_hp)` compatibility or version its consumers together; do not break health/fuel integrations by changing the signal casually. Track actual elapsed delivery time explicitly from the end of loading to the accepted UNLOAD interaction, matching the existing deadline stop point; `started_ms` currently begins at gig acceptance and must not be mislabeled delivery time.

Current result fields are `ok`, `reason`, `fare`, `timing`, `condition`, `total`, `time_used`, `limit`, `late`, and `hits`. `timing` and `condition` are rounded for output, but `total` uses the unrounded multipliers and rounds to ¥10. Therefore GigMenu must not reconstruct money deductions from the existing rounded factors.

The owner should extend the single authoritative result with `is_timed`, exact measured duration/lateness, cargo condition, both grades (time nullable), and signed integer-yen line items: `base_fare_yen`, `time_adjustment_yen`, `cargo_adjustment_yen`, `rounding_adjustment_yen`, `net_payout_yen`. Sum of line items equals the credited payout exactly. Preserve current total calculation during this reporting change. Derive the line items inside `_settle` from its full-precision calculation, then assign any integer/¥10 residue to the explicit rounding line. Do not silently change the order of rounding or compound timing/damage twice. Failure results must not expose a positive payable subtotal without a clearly offset final failure outcome; simplest is no success payout receipt on failure.

Source-grounded illustrative receipt: base ¥6,000, cargo 85% (proposed grade B), 45 seconds late (proposed grade C). Existing timing factor is 0.475. Rows: +¥6,000 base, −¥3,150 late, −¥428 cargo, −¥2 rounding, net +¥2,420. With an illustrative prior wallet ¥5,000, resulting cash is ¥7,420. These are example data and proposed report rounding fields, not a runtime capture; they preserve the source’s exact final payout. A prettier mock must not substitute milder deductions without a separate economy decision.

Muse owns this coupled GigDispatch/GameConfig/GigMenu change. Fuel consumes the existing earnings/balance authority; td-200’s future persistent wallet consumes the once-only settlement contract. Do not add a UI balance, extra reward writer or second settlement event. Add a stable settlement identity when the owning persistence contract needs one; do not fake replay-safety by hiding a button.

## Weight MVP and later inventory

MVP reads an aggregate carried mass and vehicle capacity. Include client cargo and owned supply packs once each. Permit overload, keep the red warning visible, and apply monotonic, bounded penalties through the existing vehicle capability/controller contract. Suggested tuning experiments: no penalty up to capacity; progressive acceleration/top-speed reduction and less responsive handling beyond it. Validate feel with the real car; do not add random steering or rewrite the controller. Capacity and penalty curves are tuneable data, not numbers invented by the HUD.

Loading must display the resulting weight and penalty before confirmation, but weight alone cannot block it under this brief. Any separate physical-space rule must be explicit. Clear load/penalties on actual unload, not on opening/closing UI or settling an unrelated transaction.

Later scope, explicitly deferred: physical slots, item placement, weight distribution, center of gravity, shifting or falling cargo. Preserve item/mass IDs for that extension. Do not build rigid-body cargo simulation for this MVP.

## Proposed work split (not assignments)

1. **Design and composition contract:** one owner prepares responsive state mocks, icon/text rules, reserved bounds and presentation priority. No implementation until these are inspected. No new task numbers assumed here.
2. **dot Fuel/Wanted presentation:** adapt the existing owned FuelHud and WantedHud to the agreed slots and icon style; expose read-only balance/range/wanted data. Do not touch Muse map/gig/health or Claude assets in this slice.
3. **Pending Muse coordination — map and gig surfaces:** persistent minimap/destination bearing/cardinals/click-expand, discovery-marker consumer, concise objective, secondary health presentation, and coupled authoritative grading/itemized settlement. Keep the GAS hit-test defect and DamageBar rendering defect separately tracked under their respective owners.
4. **dot td-200/201 discovery and load:** stable POI discovery/persistence and aggregate load/capability contract, reconciled with garage suppliers and prerequisites. Serialize GigDispatch schema/assembly edits through its owner; a display worker must not independently modify the same file.
5. **Pending Claude coordination — shop assets:** readable facade silhouettes and Japanese physical signage within existing assets. Provide a short data-facing POI/entrance/sign spec, not parallel shop models from dot.
6. **Independent integration reviewer:** pinned combination, before/after cameras, real browser input and phone verdict. Work split is a recommendation; no outside agent was contacted and no code was written in this pass.

## Mock set and acceptance

Create labelled design states over real current Lower City camera frames: calm desktop driving with no pedals; mobile driving in both orientations; critical conditions plus overload; shop approach/arrival; first discovery plus map; supplied-symbol wanted levels 1/3 and 3/3; on-time, late and untimed delivery reports; genuine adverse outcome. Check touch layouts at 844×390 and 390×844 and desktop at 1280×720 and 1920×1080. Keep the minimap present on normal driving and automatic-result boards. Use actual artbook/reference images; label generated overlays as design mocks, never runtime proof. Inspect symbol recognition, text contrast and Japanese glyphs at final size. Preserve deliberate symmetry; follow the latest background-free HUD direction.

Acceptance must establish:

- Cash/speed/fuel readable and continuously present while driving; every secondary value one action away; critical states promoted correctly with no false healthy data.
- No persistent bilingual double labels; Japanese signs preserved; contextual translations accurate and stable; no tofu glyphs.
- Pedal holds/releases and steering multi-touch cannot open map/menu, including orientation changes and controls becoming visible mid-gesture. A broken-baseline test must fail at the existing GAS overlap coordinate.
- All sheet permutations preserve pause ownership, Back/Close, input isolation and arrest timing; no duplicate settlement or debit.
- First visit emits once, revisits do not spam, through-wall proximity does not discover, and discovered markers survive restart/reload using the same POI ID.
- At equal car/input/road conditions, increased overload monotonically lowers the intended performance; unloading restores it; aggregate mass matches cargo and supplies with no double-count.
- Desktop has no steering/pedal overlay, has a dismissible first-run keyboard tutorial, and keeps legible smaller text. Mobile browser retains touch controls. Normal HUD has no filled backing; bold green cash and supplied-symbol wanted markers match the inspected mock.
- Minimap stays visible with actual roads/cardinals/player facing/destination bearing, updates across pickup/drop-off, and click/tap opens the existing large map. Closing restores it without an extra route/map system.
- Success payout animation equals the authoritative result and current balance; next gig is explicit; failure/arrest cannot show success. DELIVERED never uses red. Cargo and timed-only time grades are present; late delivery is accepted with the exact deduction; untimed delivery has no timing modifier. Integer report rows sum exactly to the paid total, including rounding, across boundary cases and repeated report opens.
- Actual full-resolution captures are inspected. Godot 4.7.2 native and browser tests are separate from physical-phone performance and Craig's final visual verdict. Retained baseline errors remain disclosed.

## Recommended setup for the coupled change

Apply the merged worker-selection policy. Recommend a frontier model at high effort for responsive hierarchy and owner-contract design; use max for the coupled gig/economy/persistence implementation and independent acceptance audit. Candidate exact setup is `gpt-6-astra` high for UI direction and max for the coupled result/settlement work, subject to the target executor’s current supported catalog. Provider choice is otherwise neutral. Muse is the owning route, not proof of any underlying model.

Fallback is `wait_for_required_tier`. Cheap attempts: none for the coupled change. Do not replace the owner or downgrade because quota is unavailable. Read-only source/reference preparation can continue. Runtime model, effort, tools, budget and available quota remain unconfirmed here; the dispatcher records the actual check before production admission. Reserve one coherent implementation pass, one evidence-based correction, and a separate frontier max audit. If the correction still fails, stop for a new owner-approved plan rather than retry weak variants. Escalate immediately for missing tools, changed payout arithmetic, mismatched schemas, replay risk or cross-owner edits.

Required tools: Godot 4.7.2, the real Lower City scene and pinned owner branches, native and browser capture, keyboard/multi-touch tests, and ability to inspect final-resolution pixels. Verification budget includes arithmetic boundary/rounding tests, timed/untimed and late-success flows, settlement replay checks, input-mode/layout permutations, and independent visual review. No worker admission, model runtime attestation or cost claim is made by this design. Actual outcome remains pending implementation and acceptance.

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

Revision sources re-read at 15:52 UTC:

- [GigDispatch at inspected main](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/scripts/lower_city/gig_dispatch.gd): negative timer accepted; settlement formula and rounded result fields
- [GameConfig at inspected main](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/scripts/game_config.gd): timing/damage tuning
- [GigMenu at inspected main](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/scripts/lower_city/gig_menu.gd): existing result/next-gig surface shows total but no itemized grades
- [Merged design PR344](https://github.com/doublehidenblade/game-dev-central/pull/344), [merged worker policy PR345](https://github.com/doublehidenblade/game-dev-central/pull/345), [setup policy](https://github.com/doublehidenblade/game-dev-central/blob/4a074eff99fffd93fda4ea5d8d6ef13d2794e9ae/project-management/rules/WORKER_SELECTION_POLICY.md)

Authoritative police references:

- [Tokyo Metropolitan Police flag specification, Showa 40](https://www.reiki.metro.tokyo.lg.jp/reiki/reiki_honbun/g101RG00002176.html): documented 20-ray sun emblem; official drawing inspected
- [MPD uniform emblem explanation](https://www.keishicho.metro.tokyo.lg.jp/book/mamechishiki/mame01/): modern uniform emblem image inspected; not asserted as a Showa-era design
- [MPD police-box and patrol-car history](https://www.keishicho.metro.tokyo.lg.jp/about_mpd/shokai/pipo/webpb/koban_qa.html): red-light symbol; national black/white patrol-car scheme in Showa 30
