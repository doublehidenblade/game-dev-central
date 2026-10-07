# HUD and discovery MVP: bounded implementation plan

> 2026-10-07. Documentation-only proposal for Craig's requested Japanese-world/localized-HUD direction. No runtime worker is assigned by this document. No canonical task IDs or board statuses are created or changed here.

## Read first

Read [SYSTEM](../../rules/SYSTEM.md), [worker brief](../../rules/WORKER_BRIEF.md), [standing rules](../../../knowledge/standing-rules.md), and the [design brief](../../../game-design/hud-discovery-mvp.md). This bounded publication leaves a draft PR open: no main merge, auto-merge, Actions dispatch/rerun/workflow edit, deployment, external-agent contact, or runtime edit. Generic merge instructions do not authorize a merge for this task.

Craig authorized GitHub design/task publication and mock-first work on 2026-10-07, without a mandatory pause for his design review. The latest requested scope is contextual translation of Japanese-world signage, recognizable HUD icons and pedals, a Japanese-police-inspired wanted indicator, hover/focus help and mobile teaching, rewarding delivery settlement, readable cash/status/fuel/speed, and simple load penalties. Independent mock inspection still precedes implementation; his final phone verdict remains distinct from engineering or screenshot evidence.

## Current ownership and reuse

The [central board](../../boards/tokyo-drift-3d.md) and the following existing task files were read at publication. Recheck them and live workers immediately before runtime admission.

- [td-200](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-200.md): dot-owned atomic inventory, persistent wallet/ownership, carried packs, discovered suppliers and aggregate client/supply load. Extend this contract; never create another discovery database, wallet, save service or inventory implementation.
- [td-201](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-201.md): dot-owned workshop and prerequisite-aware reveal UI. Early discovery must remain durable without revealing hidden tiers.
- [td-203 map](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-203.md), [td-204 health](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-204.md), [td-205 gig menu](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-205.md): Muse-owned. This proposal does not rewrite, reassign or close them.
- [PR457 Fuel](https://github.com/doublehidenblade/tokyo-drift-3d/pull/457) and [central PR330 handoff](https://github.com/doublehidenblade/game-dev-central/pull/330): existing dot fuel/cash presentation and recovery lane. Fuel/cash remain run-scoped until the single td-200 migration contract lands.
- [PR446 Wanted/physical systems](https://github.com/doublehidenblade/tokyo-drift-3d/pull/446): existing dot presentation lane; proposed icon changes do not change police authority, escalation, collisions or arrest.
- [Central PR327 garage design](https://github.com/doublehidenblade/game-dev-central/pull/327), [Tokyo PR455 task revision](https://github.com/doublehidenblade/tokyo-drift-3d/pull/455), [garage epic450](https://github.com/doublehidenblade/tokyo-drift-3d/issues/450): existing garage sequence and admissions. Do not duplicate a live garage worker.
- Claude retains physical shop/vehicle/faction assets and story ownership. Japanese-police research is recognition guidance, not permission to replace faction canon or cruiser art.

## Proposed sequence and handoff boundaries

### 1. Mock and composition package — dot design preparation

Status: planned; execution assignment is not recorded by this publication.

Create the six state boards listed in the design brief at 844×390 and 390×844, plus one desktop composition. Use real current Lower City frames; label overlays/generated imagery as design mocks. Define actual screen-space hit rectangles, clear driving corridor, localized icon labels, focus order, sheet priority, and reduced-motion delivery behavior. Compare sunburst-medallion/three-lamp wanted treatment with simpler beacon/roundel option.

Acceptance: independent reviewer opens full-resolution mocks, checks opacity, deliberate symmetry, Japanese glyphs and physical control recognition; every interactive target is at least 44 screen pixels at smallest layout. Mock review is design evidence only.

### 2. Fuel and Wanted presentation — proposed dot implementation slice

Status: blocked on inspected mocks, exclusive runtime admission, and agreed shared slots.

Adapt existing FuelHud and WantedHud only, with source authority and existing payment/arrest behavior preserved. Cash and fuel remain continuously readable during driving; icons have hover/focus labels. No new balance, payout or police logic. Do not independently move Muse controls or edit the shared scene assembly.

Acceptance: exact-head same-camera before/after evidence in both phone orientations; opaque rendering; balance/range match authoritative values; payment and arrest visibility/pause regressions remain intact. Local Godot 4.7.2/native and browser results are separate. Draft PR only.

### 3. Discovery and load contract refinement — reuse td-200/td-201

Status: planned additions to existing dot work, not a new save/inventory task.

Agree stable POI/item IDs, category, localized display-name key, physical entrance/service zone and single discovery event. Looking reveals a contextual name; service-area entry discovers the supplier. Persist through reload using td-200; expose one read-only marker set to the existing map. Keep prerequisites/source/price knowledge separate in td-201.

Reconcile the older mass-limit wording with the latest overload direction before implementing: weight alone is a soft capacity with explicit warning and bounded monotonic acceleration/speed/handling penalties. Any separate volume/physical-fit limit remains explicit. No slot/center-of-gravity/falling-cargo simulation. Client cargo and owned supplies count once each. HUD consumes values; vehicle/controller owner supplies behavior.

Acceptance: one discovery event per POI, no through-wall discovery, reload/failure/arrest/revisit durability, disclosed storage failures, exact aggregate mass, no duplicate item or wallet state, overload penalty monotonicity under equal road/input conditions, unload restores intended performance. Existing td-200 atomicity and td-201 hidden-tier tests remain required.

### 4. Cross-owner presentation interfaces — pending coordination

These are proposals, not assignments or authorization to edit another owner's code:

- Muse map: folded-map icon, reserved dock/expanded bounds, discovery-marker consumer of the single td-200 record; preserve shared MapSheet renderer
- Muse health: discuss quiet healthy status versus its existing always-visible acceptance; preserve critical-before-failure and truthful BODY semantics. Do not silently rewrite td-204 criteria
- Muse gig/settlement: concise objective plus rewarding receipt/stamp/chime/count-up driven only by its authoritative result; retain next/all/close, failure reasons and arrest timing
- Controls owner: accelerator/brake silhouettes, readable teaching/focus labels and gesture ownership; no layout release can become a map/menu action
- Claude assets: readable service silhouettes, Japanese physical signs and entrance identifiers; reconcile amber-canon/red-image discrepancy without altering assets here
- Shared assembly owner: one set of reserved zones and sheet priority, serialized scene/GigDispatch schema integration

These interfaces stay pending until coordinated through the authorized owner workflow. No external owner or agent was contacted by this publication.

### 5. Independent composition review

Status: blocked on implementations and exact pinned combination.

Require before/after captures for every claimed visual defect, actual browser touch and desktop focus input, sheet permutations, arrest/settlement ordering, orientation changes during held gestures, and full-resolution inspection. Test broken-baseline GAS overlap at the observed coordinate before claiming the regression guarded. Preserve/report the separate DamageBar triangulation failure; 772 passing fixture assertions are not a clean renderer verdict. No fabricated phone performance or final acceptance.

## Scope and task filing boundary

This is the requested task/implementation plan in game-dev-central, not a duplicate canonical td task queue. No numeric ID is reserved. Runtime admission must first reconcile board/PR/live-worker state and add only genuinely new dot-owned presentation work via the canonical game-repository task process. td-200/201 are reused rather than cloned. Cross-owner work remains unassigned. Existing task files, board rows and runtime files are untouched.

The new design is not a release. Publication verification consists of remote readback of these two documents, draft/open PR state, exact head SHA, and changed-file list. No build, new runtime validation or deployment is claimed.
