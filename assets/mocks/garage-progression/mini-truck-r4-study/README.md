# Garage MVP: corrected R4 isolated-study reference proposal

**Status: LOCAL PROPOSAL ONLY, awaiting parent and independent review.** Six original editable SVG diagrams, six inspected PNG renders, one explicit numeric design option, and the exact staged amendment in `R4_TASK_BRIEF_AMENDMENT.md`. No GitHub write, reference upload retry, 3D modeling, paused-worker resumption, runtime/world edit, Actions run, merge or deployment occurred.

## Useful result

The ready next portion of td-197 is to make the **shared bed-floor interface and first rack/padded/garage reservations reviewable**. The old r3 pixels remain unavailable. The two newer work-truck concepts were opened and inspected, but their cold-box/finish focus does not supply the rack, padded carrier, bench, shelf or threshold contract. A second speculative cold-box image would not close that gap.

This pack proposes one coherent, modest option so future modeling has something specific to evaluate. It deliberately does **not** represent recovered r3 art, trace dimensions from generated pixels, or claim the existing eleven-sheet gate has passed. The six sheets are engineering/design schematics rather than replacement beauty images or final game art.

## Open these files

1. `sheets/01-shared-bed-sockets.svg` / `.png`: original metric plan, compact truck/bed targets, A/B/C/D floor mounts, tailgate reservation and unresolved interfaces
2. `sheets/02-utility-rack.svg` / `.png`: separate open-rack elevation and plan using the same four floor mounts
3. `sheets/03-padded-carrier.svg` / `.png`: low padded cassette plan/elevation and deliberately distinct silhouette
4. `sheets/04-workshop-reservations.svg` / `.png`: same provisional room/facility reservations as the measured foundation, with proposed bench/shelf asset dimensions
5. `sheets/05-shutter-threshold-states.svg` / `.png`: open, interrupted-closing and fully-closed intended states; no runtime implementation implied
6. `sheets/06-roll-up-retraction-section.svg` / `.png`: metric side section of the fixed casing, stylized retracted roll and free-curtain collision extent
7. `interfaces.json`: machine-readable numeric option, source pins, category labels and null unresolved fields
8. `reference-gap-and-revision.md`: exactly what is still missing and the proposed task-document amendment route
9. `validation.json`: author's arithmetic/file checks and failing-before controls, including the previously undetected drawn padded-base width; **not independent acceptance**

R4 correction note: the full padded base is now drawn from interfaces.json at 1.20 m width, not the erroneous prior 1.28 m. The shutter is a roll-up curtain, not a rigid 3.20 m leaf lifted above its opening. The roll fits a 4.40 W × 0.50 D × 0.45 H m casing at h = 3.20…3.65 m; its 0.40 m diameter is a stylized game-art target.

SVGs are editable. PNGs are 1600 × 1100, rendered with Inkscape. Rebuild with `python build_reference_pack.py`. No copied reference image or supplied user photo is embedded in this deliverable.

## M / D / U: dimensions are not interchangeable

- **M: measured current game**: externally supplied measurement evidence, independently checked by the measurement reviewer. The current playable **coupe**, not the future mini-truck, has a conservative 2.00 × 4.50 m plan union. Its measured-body-heading low-speed sweep is 10.147658468 m diameter. The current Repair Row parcel is 16.00 m deep × 13.65 m frontage, with a 5.00 m road and only 1.00 m existing frontage strip. Its decorative garage mouth is backed by a solid collision wall. The nominal deck soffit is 4.30 m above ground. Those measurements have bounded scope; there is no accepted future truck, entry path or garage.
- **D: deliberately chosen, unaccepted design target**: compact body 3.40 L × 1.50 W × 1.85 H m, mirrors within 1.72 m; bed 1.30 W × 1.70 L m at floor height 0.72 m. Four bed-floor sockets at x = ±0.500 m, z = ±0.675 m. Rack 1.20 W × 1.60 L × 1.20 H m above the floor; padded carrier same footprint × 0.45 H m. Bench 3.00 × 0.80 m at height 0.90 m; shelf asset 1.60 W × 0.60 D × 1.90 H m inside the inherited 2 × 2 m reservation. These are original proposals, not historical vehicle claims or measured/source assets.
- **U: unknown**: actual source mesh, collider/root/wheel transforms, real sockets and brackets, wheel/light/window/tailgate envelopes, loaded handling, pack sizes/masses, capability modifiers, camera and moving-door validation against the chosen margin. JSON nulls are unknown, never zero.

The 12 × 10 m room, 6.5 × 3.2 m park/unload rectangle and 4.2 × 3.2 m opening remain the **existing provisional targets**, not new measured facts. The full 2.00 W × 4.50 L × 2.20 H m truck/fitting/cargo budget is an **additional design allowance**; its width/length were chosen to stay within the current coupe's measured plan baseline, but its height is entirely a new design target. It is not the selected truck's collider and does not prove future truck fit.

## Why this option is worth reviewing

- The compact cab-over body preserves the visible working bed and small-truck identity. Its body and mirror targets sit within the measured current-car plan envelope. This is a static sizing rationale, **not** a handling or legal kei-class claim.
- A shared floor grid is testable and independent of drop-side rails. The bed-local frame is +X left, +Y up, +Z forward. Its origin is the usable bed-floor center. A is front-left, B front-right, C rear-left, D rear-right. The proposed design-root transform is explicitly separate from the unknown runtime root.
- Both 1.20 × 1.60 m module boxes leave just **0.05 m gross clearance at each bed edge**. The 0.10 × 0.10 m mount plates stay inside the modules and bed. For the game asset, choose a **0.02 m minimum visible/collision gap** to adjacent bed geometry, with brackets remaining inside the declared module box. At most 0.03 m of each nominal gap may be used by bed trim. Check overlap in the actual source; this is not manufacturing certification. Do not quietly grow the modules after approval.
- A rack top at 1.92 m and padded top at 1.17 m give visibly different silhouettes and lie below the proposed 2.20 m all-up height budget. The 3.20 m doorway leaves 1.00 m gross height to that budget, with a proposed 0.20 m full-inside closure margin and 0.45 m mechanism headroom reservation. The resulting 3.65 m opening-plus-mechanism target leaves 0.65 m to the nominal 4.30 m soffit before actual roof/lights. Moving/pose validation remains open. Static height arithmetic does not establish load clearance.
- The 2 × 2 m stored-module reservation can contain a centered 1.20 × 1.60 m box with 0.40 m and 0.20 m gross floor margins. Only one unequipped fitting is contemplated. Choose a fixed-slot swap with a simple presentation cut while parked; no hoist simulation, free assembly or physical removal animation is required for this proposal. Actual stored/mounted geometry and readable service views still need to agree with ownership.
- The rack and padded carrier use the same four mounts and are alternatives. No cold box, second installed layer, paint economy, new cargo capability or refrigeration mechanic enters this proposal.
- The room plan intentionally retains the measurement worker's unbuilt reservations. It does not duplicate that worker's site/turning investigation. The measured 10.1477 m current-car sweep warns against assuming an indoor U-turn in a 10 m-deep room. No reduced sweep is inferred merely because the proposed truck is shorter.

## Actual visual references inspected

### Current work-truck concept pixels

- `worktruck-concept-01-reference.png`, SHA-256 `e169a1e879561ac2132d27fc6632d68264a263744bebcc0d21355d682b6b03b0`: corrected concept-v2 bytes under the delivery filename. Cream compact cab-over, open flatbed, front/side/rear views and cold-box concept. Original shape direction only; no reliable dimensions, rack or padded mounting geometry.
- `worktruck-concept-02-garage.png`, SHA-256 `c15585b6ec9f3bec9ba17ab21effc52da4343b1022c73aec79a3d1372efca67a`: warm workshop/finish-viewer mock, cream/teal vehicle with cold box. Neither a measured room nor implemented UI. Its cold-box label is not used as a first-slice feature requirement.

### Game art book

Read [Fleet & Gear](https://github.com/doublehidenblade/game-dev-central/blob/c15641a595d4b23d3e73acb1dc239d22fd1ed263/game-design/art-book/fleet-gear/chapter.md) and [Lower City / Kotobuki](https://github.com/doublehidenblade/game-dev-central/blob/2f138f5c2cfd703733b002008f1007fba0012694/game-design/art-book/lower-city/chapter.md). Opened the real [Kotobuki garage art](https://github.com/doublehidenblade/game-dev-central/blob/2f138f5c2cfd703733b002008f1007fba0012694/game-design/art-book/lower-city/mock-kotobuki.png) pixels and verified the local file's Git blob `2b14cd88c997e11e7aa982a20307358896230cea` against the pinned GitHub directory. Also opened the locally available KMTED artwork for the broader analog/cel language; it is not a truck interface authority.

Carried forward: broad paint fields, ink-like outlines, modest chunky hardware, muted cream/ochre/steel/olive, analog workshop identity and uncluttered readable silhouettes. The illustrated old sedan/starter progression is superseded by the corrected mini-truck direction. Painterly art-book grain/detail is not an instruction to add dense PBR texture. No new branding or Japanese lettering is fabricated. All diagram annotations are English; environmental signs remain blank pending the existing checked Japanese sign assets.

## Exact authority and measurement provenance

- [Corrected td-197](https://github.com/doublehidenblade/tokyo-drift-3d/blob/b570ac3e590739782c463a3a620670122a8d5b95/godot/docs/tasks/td-197.md) and [td-198](https://github.com/doublehidenblade/tokyo-drift-3d/blob/b570ac3e590739782c463a3a620670122a8d5b95/godot/docs/tasks/td-198.md), Tokyo PR #455
- [Central garage execution brief](https://github.com/doublehidenblade/game-dev-central/blob/2f138f5c2cfd703733b002008f1007fba0012694/project-management/task-team-system/briefs/garage-progression-first-slice.md)
- [Current r3 README](https://github.com/doublehidenblade/game-dev-central/blob/2f138f5c2cfd703733b002008f1007fba0012694/assets/mocks/garage-progression/mini-truck-r3/README.md)
- [Customization sequence](https://github.com/doublehidenblade/game-dev-central/blob/f49d39dbbf5bd080dc6e445fe3a2940c58b68dd7/game-design/research/truck-customization-20261008/sequence.md), central PR #351
- Measurement source candidate `9e5b23663642762d993ce9c7f3a49755d65394b6`; frozen-v2 artifact manifest SHA-256 `7bd29394844dc5cc6a9a87aadc4ee3b4fed22975962f07cc9fa3d12bd1cceb28`; independently reviewed bounded measurement preparation, not full td-197 acceptance

## Staged authority and next action

The exact coordinated R4 replacement-reference/task/brief proposal is in **R4_TASK_BRIEF_AMENDMENT.md**. It is not enacted by these files. Independent correction recheck and verified GitHub publication must occur before a new exclusive isolated common-blockout study is assigned. The old paused td-198 worker stays paused.

After that explicit amendment, the selected corrected concept and R4 numeric targets can guide a scratch-only primitive study. Measured common geometry, matched rear-left views, orthographic sockets, wheel/window/lamp/tailgate reservations, simple rear access, separate fixtures and counted shelf packing become required study outputs. Final paint, detailed hardware engineering and physical-phone evidence do not block this primitive investigation.

The current r3 rule is not silently claimed passed. The amendment explicitly replaces/defer its listed reference prerequisites **for the study only**, using a new R4 name. Full td-197 layout/UX/mock completion, actual-world garage integration, gameplay and phone gates remain open. No actual-world scene, shipping asset, old thread, repository or runtime was changed.

## Independent-review lineage

The prior 16-file candidate manifest was `070b2c0fa0c0717308395ea4b694d26d2e46efd61ff12d3db4969c9967e20346`. Independent review judged it an acceptable bounded design option with two required corrections. This new candidate corrects both and adds stage-specific prerequisites. Its revised hashes are in artifact-manifest.json. Do not apply the previous review as acceptance of these new bytes; request a bounded recheck.
