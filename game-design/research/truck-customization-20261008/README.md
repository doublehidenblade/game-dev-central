# The working truck as the player's avatar

Research/design addendum • 8 October 2026 • **Stashed for the next garage slice**

## Priority and delivery boundary

Finish the already ongoing playable release first: gigs, usable UI, a lively functional Lower City and traffic. This customization plan is **not a new release blocker**. Reference gathering, original concept mocks and isolated source assets may progress in parallel only when they do not consume the critical release owner's capacity or modify owned runtime files. The rotatable garage showcase is a later, dependency-gated integration.

The requested outcome is a humble utility mini-truck that becomes visibly personal as it becomes useful. It should feel like the driver's working-life avatar. It is not the red racing coupe and does not require a giant decorated heavy truck as the endgame.

This is a bounded addendum to [the existing garage design/brief, central PR #327](https://github.com/doublehidenblade/game-dev-central/pull/327), [garage epic #450](https://github.com/doublehidenblade/tokyo-drift-3d/issues/450) and [corrected mini-truck task revision, Tokyo PR #455](https://github.com/doublehidenblade/tokyo-drift-3d/pull/455). It does not replace td-197–202 or their owners. [Sequencing and collision notes](sequence.md) and [four bounded task records](tasks/) turn the direction into reviewable work without reserving another global td number.

## What is historical, and what is our invention?

### Supported historical anchors

- Suzuki dates the first Carry to 1961. Its 1976 Carry Wide entry describes separate cab and bed construction that made changing the bed easier. The 660 cc new-standard Carry is dated 1990; do not label that standard as Showa-era. [Suzuki vehicle history](https://www.suzuki.co.jp/suzuki_digital_library/1_auto/carry.html)
- Suzuki lists a 1962 panel van, 1975 insulated and refrigerated food bodies, and a 1978 mobile refrigerated vending body. Specialized working bodies have a real period foundation. This does not establish that quick-swap game modules operated as proposed here. [Suzuki food-body history](https://www.suzuki.co.jp/suzuki_digital_library/6_special/food.html)
- Toei dates the first *Truck Yaro* film to August 1975 and describes friendship, rivalry, truck decoration and solidarity in the series. Use the social pride of working drivers as inspiration, without copying characters, liveries or film art. [Toei series introduction](https://www.toei-video.co.jp/catalog/bstd03710/)
- Aoshima's company timeline places its 1/32 dekotora series in 1976. [Aoshima history](https://special.aoshima-bk.co.jp/100th/history.php)
- Camion's publisher dates the magazine's launch to May 1984 and describes readers including professional drivers, truck enthusiasts and model enthusiasts. This supports a cultural/audience overlap worth exploring, not a measured market-size claim. [Camion publisher profile](https://geibunsha.co.jp/brand/camion/)

### Creative extrapolation

A small, original kei-scale work truck with restrained dekotora-inspired personal details is our art direction. These sources do **not** establish that every pictured truck is period-correct, kei-class, or an authentic Showa customization. Our fictional district commissions, earned liveries, garage module sockets and rotating viewer are game design.

The supplied seven-image reference set mixes ornate full-size mural trucks, a modern pink Liberty Walk hauler, black/red convoy styling, a B120 pickup and commercial diecast/catalogue imagery. These categories were reported from the preceding image inspection; this documentation pass did not independently inspect those image pixels. They are useful for motif, stance and presentation discussion, not a single historical specification. The next visual worker must inspect actual pixels and label each reference's type and limits.

### Audience hypotheses to test

Practical-vehicle affection, model-kit collection, maker pride and expressive customization may overlap. Test whether players enjoy a cared-for everyday truck as much as a loud showpiece. No claim is made about audience size, willingness to pay or guaranteed retention.

## Equal style families

1. **Neighborhood workhorse:** cared-for cream/ochre or faded utility paint, simple steel wheels, restrained shop identity, small signs of working life
2. **Street courier:** crisp two-tone or a directional stripe, purposeful trim and a readable personal signature
3. **Local showpiece:** one original mural or tailgate motif, restrained andon/light-box detail and selected polished accents

These are equally valid identities. “Most decorated” is never a mandatory progression tier. A plain, well-kept vehicle remains desirable and effective.

Use three independent layers:
- Paint, trim and wheels: fixed paint zones and a small authored selection
- Functional bed module: an existing approved upgrade whose silhouette communicates its actual capability
- Personal signature: tailgate art, small andon, mudflaps or a district-commission motif

The chase camera makes the rear especially important: tailgate, bed, cab-back window and cargo should remain readable. Preserve lamps, wheel travel, cargo visibility and clearance. Use authentic, separately checked Japanese environmental lettering with English player-facing UI. Generated lettering is not final signage. Use original brands and artwork; do not reproduce Liberty Walk logos or existing murals.

## Strict playable MVP

**One coherent mini-truck chassis; base finish plus two authored finishes; one visible upgrade demonstration; one simple garage viewer.**

Reuse the corrected approved mini-truck/common bed geometry and existing garage work before creating anything equivalent. Keep a few material zones and small trim changes. Six curated looks are a useful future direction, not a six-skin implementation requirement.

The new concept pack may illustrate a base flatbed and a single cold-box module alongside two or three finishes. The cold box is a design/fit demonstration until its capability is genuinely implemented. For playable integration, choose one already supported cargo upgrade from the garage owner's plan, such as the rack or padded carrier. Do not add refrigeration mechanics just to match a mock, or present a purely cosmetic box as an earned functional upgrade.

The original garage's cold box, animal cage, tank, later van and heavy-truck ideas remain later options. Do not implement the catalogue, new vehicle classes, giant decorations, free building or a new economy in this slice. Heavy decorated trucks can later be special NPCs or distinct fleet goals.

### Rotatable garage showcase

- Activate while safely parked in the **actual garage**, using the player's actual equipped vehicle, skin and visible upgrade
- Mouse/touch drag rotates the view; provide reset view and bounded zoom. Use a predictable camera pivot and keep the truck framed
- Preview, Apply and Cancel are separate. Cancel or close returns to the equipped appearance; Apply changes it once
- The camera or presentation copy reads the same authoritative vehicle/loadout data as gameplay. No alternate showroom inventory or fabricated “equipped” state
- Block driving input leakage while inspecting; restore driving/control focus cleanly on exit. Respect the garage owner's door/shelter and job-timer contracts
- Show the same vehicle when leaving the garage and after reloading. Do not pause obligations, open shutters or reset wanted state through viewer actions
- One phone-readable compact control set. This is vehicle inspection, not a garage-building editor

If the actual garage, vehicle identity or persistence contracts are unavailable, park integration. A separate beauty render can support art review but cannot satisfy playable acceptance.

## Earned expression without grind

Longer-term appearance can come from district delivery commissions, discovered paint-shop services, a few materials and short blueprint beats. Reuse existing discovery and reward contracts. No random duplicate grind, hidden performance stats attached to paint or compulsory decoration ladder.

A small transparent passenger tip for a cared-for look is compatible with earlier direction only after passenger eligibility and its economy are real; it is outside this MVP. Do not award passenger benefits to an unsafe open bed. All mechanical effects belong to actual equipment. Previewing cosmetics is free; any eventual paid Apply must show its cost and use the existing once-only transaction authority.

## Art workflow and acceptance

Actual reference pixels → labeled 2D mock/contact sheet → original editable 3D source and game export at matching angles → independent visual review → later minimal garage integration → separate actual-world acceptance.

Follow [the visual brief template](../../../project-management/rules/VISUAL_BRIEF_TEMPLATE.md), [the task contract](../../../project-management/rules/SYSTEM.md), [worker-selection policy](../../../project-management/rules/WORKER_SELECTION_POLICY.md), [standing rules](../../../knowledge/standing-rules.md) and [anime NPR workflow](../../../knowledge/lessons/anime-npr-scene-workflow.md). Use the task-specific current cel-anime direction: broad paint zones, restrained surface detail and readable forms under the real Godot look. Do not let older generic PBR wording pull this slice back to the rejected realistic sedan treatment.

References, generated concepts and engine evidence must be honestly distinct. Never infer dimensions from generated perspective. Use verified geometry for scale, wheel centers, collider and bed-floor sockets. Record no-build envelopes for cab, lamps, wheels, tailgate and cargo. Original modeling uses working Blender plus Godot import and pixel inspection; no placeholder box model can pass as finished art.

Every visual acceptance criterion needs its matching before/after camera pair and exact source SHA. The reviewer must open the pixels and judge each criterion independently; renders, triangle counts and a successful import alone do not prove quality. Craig's physical-phone verdict remains separate from agent inspection.

## Publication and reference handling

This repository is public. This filing includes text, primary-source links and task records only. Do not upload the user's supplied photographs, private attachment identifiers, sign-in links or private session URLs. Public availability of a source does not grant image-reuse rights.

Original generated concepts may later be added under `mocks/` on this same branch, after actual file availability, pixel inspection and provenance checks. Record filename, bytes/hash, generation date, honest “concept mock” label, input category and limitations. Never overwrite the earlier pending garage image upload or pretend its manifest proves the image files exist.

No source code, models, screenshots, completed visual gate or playable result is delivered by this document.
