# HUD and discovery MVP revised execution plan

> 2026-10-07, revised for Craig’s latest desktop, minimap, police-symbol and delivery-report feedback. Update the existing merged design/plan, not a new parallel feature queue. No production code or external-agent contact in this revision.

## Direction now locked by feedback

Use smaller desktop text, no desktop steering/pedal overlay, and a first-use WASD/arrow-key lesson. Mobile including mobile browsers keeps thumb-safe touch controls. Normal driving HUD has no filled background blocking the world; fine text outlines provide contrast. Bold green money stays visible.

Keep the actual minimap continuously visible with N/E/S/W, player facing and destination bearing. Click/tap opens the existing large map; map icon alone does not satisfy the request. Repeat Craig’s supplied police sun-ray symbol as the three wanted markers; remove the earlier invented medallion/three-lamp proposal. The latest user direction supersedes the old opaque driving-HUD and desktop phone-scale proposals.

DELIVERED uses green/cream. BUSTED, WASTED, OUT OF GAS and genuine failure use red. Successful deliveries show cargo grade and timed-only time grade, plus an accessible, clearly itemized payout report. Late delivery remains acceptable with its money deduction.

Read the revised [design brief](../../../game-design/hud-discovery-mvp.md), [standing rules](../../../knowledge/standing-rules.md), [SYSTEM](../../rules/SYSTEM.md) and [worker selection policy](../../rules/WORKER_SELECTION_POLICY.md). The latest explicit UI exception applies without another design-choice question. Independent mock inspection still precedes implementation.

## Current ownership and reuse

The [central board](../../boards/tokyo-drift-3d.md) and the following existing task files were read at publication. Recheck them and live workers immediately before runtime admission.

- [td-200](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-200.md): dot-owned atomic inventory, persistent wallet/ownership, carried packs, discovered suppliers and aggregate client/supply load. Extend this contract; never create another discovery database, wallet, save service or inventory implementation.
- [td-201](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-201.md): dot-owned workshop and prerequisite-aware reveal UI. Early discovery must remain durable without revealing hidden tiers.
- [td-203 map](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-203.md), [td-204 health](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-204.md), [td-205 gig menu](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-205.md): Muse-owned. This proposal does not rewrite, reassign or close them.
- [PR457 Fuel](https://github.com/doublehidenblade/tokyo-drift-3d/pull/457) and [central PR330 handoff](https://github.com/doublehidenblade/game-dev-central/pull/330): existing dot fuel/cash presentation and recovery lane. Fuel/cash remain run-scoped until the single td-200 migration contract lands.
- [PR446 Wanted/physical systems](https://github.com/doublehidenblade/tokyo-drift-3d/pull/446): existing dot presentation lane; proposed icon changes do not change police authority, escalation, collisions or arrest.
- [Central PR327 garage design](https://github.com/doublehidenblade/game-dev-central/pull/327), [Tokyo PR455 task revision](https://github.com/doublehidenblade/tokyo-drift-3d/pull/455), [garage epic450](https://github.com/doublehidenblade/tokyo-drift-3d/issues/450): existing garage sequence and admissions. Do not duplicate a live garage worker.
- Claude retains physical shop/vehicle/faction assets and story ownership. Japanese-police research is recognition guidance, not permission to replace faction canon or cruiser art.


## Minimal owner-safe sequence

1. **Correct and inspect mocks.** Show a desktop drive with no touch controls and small labels, both phone orientations, actual minimap, supplied police symbol and bold green money. Show on-time, late and untimed reports and one adverse outcome. Inspect the symbol against Craig’s original at final size. Use current game frames; label every generated/overlaid board as a mock. The source-based ¥6,000/85%/45-seconds-late example pays ¥2,420, not an invented easier balance. Mocks are design proof only.
2. **Admit dot’s bounded presentation slice.** Recheck its existing PR/worker and reserve one exact task/runtime before edits. Fuel/Wanted presentation may remove card backgrounds, adjust desktop sizes, render bold green cash, and replace wanted markers. Keep existing balance, payment, recovery, wanted-level and arrest authority. No new wallet or settlement arithmetic. Shared slot integration waits for the assembly owner; do not independently move Muse controls.
3. **Coordinate the existing Muse-owned interfaces through the authorized workflow.** Map owner supplies always-on minimap/cardinals/heading/target-bearing and click-expand. Controls owner supplies desktop keyboard-first and touch-only driving controls with verified mappings. Health owner retains truthful status and critical warnings. Gig/economy owner supplies authoritative grades and integer receipt fields, then GigMenu consumes them. This document neither contacts nor reassigns those owners.
4. **Continue td-200/201 within their existing scope.** Reuse one discovery, inventory, load and persistence contract. Existing client cargo and purchased supplies count once. Keep soft overload, warnings, penalty contract and hidden-tier rules; no full physical cargo simulation. Do not create a new save store as part of HUD delivery.
5. **Independent combined acceptance.** Test exact pinned source, desktop and touch input, responsive composition and report arithmetic together. Retain the separate minimap/GAS and DamageBar defects under their owners until actually corrected. No claim of live delivery follows merely from a reviewed design or a screenshot.

## Coupled GigDispatch change that must stay with its owner

Source inspected at Tokyo main `9d4a88490c41f86e8d34e1c2c6f142838de20c73`:

- Late delivery already succeeds. The timer can be negative; UNLOAD still works. Do not implement a second late-success path or claim to remove a deadline failure that does not exist.
- `_settle` applies timing and cargo-condition multipliers. Timing bottoms at 0.30 after 60 seconds late; damage reduces the resulting amount further. Total rounds to ¥10. Existing report exposes only total visually.
- Add `is_timed` to offers with true as the existing-offer default. Untimed has no countdown penalty/bonus and time grade is not applicable. Preserve/version all `clock` consumers together.
- Record actual delivery elapsed time from loading completion to accepted UNLOAD, rather than using `started_ms`, which begins at acceptance.
- Add grade fields and authoritative signed integer-yen line items inside `_settle`: base fare, time adjustment, cargo adjustment, rounding adjustment, net payout. Preserve the current total calculation while adding reporting. The UI must not recompute money from `timing` and `condition`, which are already rounded in the emitted result.
- Integer rows must equal the credited earnings delta exactly. Grades are explanatory and add no second multiplier. Report replay/animation must not credit money twice. Reuse the existing settled event and td-200’s planned stable-identity/idempotence contract.
- Keep next/all/close, arrest timing and cargo critical-before-failure behavior. A compact automatic summary has an obvious Details action; the full itemization is available without filling the driving screen by default.

These changes touch Muse-owned `gig_dispatch.gd`, `game_config.gd`, `gig_menu.gd` and their consumers. A dot Fuel/Wanted worker must not implement them in parallel. Block only the dependent report integration until the owner contract is available; independent presentation/mock work may continue.

## Required recommended setup

- Capability tier and reason: frontier; cross-owner UI/input composition plus money arithmetic and persistence compatibility
- Provider preference: provider-neutral; retain the existing owner and choose the route with verified game tools
- Requested model and effort: `gpt-6-astra` high for hierarchy/presentation; `gpt-6-astra` max for coupled gig/economy implementation and independent audit, subject to target-executor catalog verification
- Environment and required tools: existing authorized Tokyo environment, Godot 4.7.2, actual Lower City sources, native/browser rendering, keyboard/multi-touch tests and full-resolution image inspection; target runtime not confirmed by this document
- Availability checked: policy catalog observation is 2026-10-07; current worker account/quota/model/effort availability unverified and must be checked at admission
- Fallback: `wait_for_required_tier`; preserve owner; read-only references/preflight may continue
- Attempt budget: no cheap attempts for coupled economy/gig work; one coherent production attempt and at most one evidence-based correction before replan; dispatcher records a concrete verified session/usage ceiling before launch
- Escalation criteria: unavailable required tier/tools, arithmetic mismatch, changed payout semantics, schema/interface expansion, replay risk, cross-owner file collision or failed correction; retain frontier max review rather than downgrade
- Verification budget: reserve the full boundary/arithmetic and interaction matrix below plus a separate frontier max audit; insufficient budget blocks production admission, not lowers the gate
- Requested versus confirmed setup: recommendation above; actual runtime/model/effort unconfirmed until worker evidence identifies them
- Actual outcome: pending implementation and acceptance; no cost or runtime claim

## Acceptance matrix

- Desktop 1280×720 and 1920×1080: no touch steering/pedal UI or empty pedal reservation; first-use WASD/arrows lesson matches real mappings and can be recalled; no repeated tutorial spam
- Touch 844×390 and 390×844 including mobile browser: safe targets, simultaneous steering/pedals, no GAS release becomes map open, no orientation/input-mode switch steals a gesture
- Driving HUD: no card backdrop, readable contrast over bright/dark streets, bold green cash, minimap continuously present, secondary status accessible and critical warnings visible
- Map: correct N/E/S/W and player heading, target changes from pickup to delivery, off-map bearing accurate, click/tap expand and Close restore the same map/data
- Wanted: exact inspected supplied-symbol silhouette at 0–3 levels; no generic stars/lamps substitution or police-logic drift
- Delivery: on-time, just-late, 30/60-second grade boundaries, lateness-floor, damaged and critical cargo, untimed, arrest/failure and repeated report open. DELIVERED never red; time grade/modifier absent for untimed
- Arithmetic: all signed integer rows equal net credited payout; fractional timing/condition and ¥10 boundaries tested; no replay or animation duplicate reward; rounding policy explicit and unchanged final totals for existing timed gigs
- Integration: payment, report, map, pause, arrest and status sheet permutations preserve input and pause ownership. Compare before/after real cameras and inspect every cited image
- Separate native/browser results, known renderer errors and physical-phone acceptance. No software-renderer FPS claim or self-validated visual completion

## Publication and reuse

Update existing central `game-design/hud-discovery-mvp.md` and `project-management/task-team-system/briefs/hud-discovery-mvp.md`. PR344 is already merged (`60a4f56f`); PR345 worker policy is already merged (`4a074eff`). Use fresh main and preserve independent edits, task ownership and established files. No runtime task IDs or board assignments are created by this document. No Actions or deployment is part of this design revision.
