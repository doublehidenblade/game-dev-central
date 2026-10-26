# Sequence, owners and release boundary

Snapshot checked: 2026-10-08 02:00 UTC. Read-only evidence can age; check current heads and active ownership before dispatch.

## What happens first

1. **Finish the current playtest:** ongoing gigs, UI, whole-city architecture/props, traffic/pedestrians and existing system repairs stay ahead of customization.
2. **Parallel preparation only when collision-free:** reference inspection and original 2D concepts, then an isolated original truck asset kit after reuse/ownership preflight. No release-critical shared-file changes.
3. **Later playable minimum:** wire the garage viewer and base plus two finishes into existing vehicle, upgrade and persistence contracts after the release and required garage gates.
4. **Independent acceptance:** exact-head code/visual review and actual-world drive-in → inspect → apply/cancel → drive-out → reload checks. Report physical-phone appearance/performance separately.

This is a sequencing change, not permission to lower existing acceptance gates or publish a failing release. This task does not trigger Actions, merge or deploy.

## Existing work to preserve

| Existing scope | Checked source | Boundary |
| --- | --- | --- |
| Garage design and mini-truck direction | [central #327](https://github.com/doublehidenblade/game-dev-central/pull/327), head `2f138f5c2cfd703733b002008f1007fba0012694` | Do not rewrite its design, manifest, board/log changes or uncertain prior image upload |
| Garage tasks td-197–202 | [Tokyo #455](https://github.com/doublehidenblade/tokyo-drift-3d/pull/455), head `b570ac3e590739782c463a3a620670122a8d5b95`; [epic #450](https://github.com/doublehidenblade/tokyo-drift-3d/issues/450) | Reuse their reference, blockout, entry, inventory, UI and validation contracts; do not start another garage architecture owner |
| td-197 reference gate / td-198 common blockout | Same corrected task revision; central board marks td-198 in progress while its task reports missing image inputs | Assignment/status needs coordinator reconciliation. Last published record is image-input-blocked; it is not proof of a currently live worker. Do not duplicate or restart on this document alone |
| Current private-playtest assembly | [Tokyo #488](https://github.com/doublehidenblade/tokyo-drift-3d/pull/488) | City-completion and owner-patch hold remains; customization is excluded |
| Tenjin td-209 / Kamome td-210 | [Tokyo #489](https://github.com/doublehidenblade/tokyo-drift-3d/pull/489), [#494](https://github.com/doublehidenblade/tokyo-drift-3d/pull/494); [whole-city #491](https://github.com/doublehidenblade/tokyo-drift-3d/issues/491) | Preserve world placement, CityDressing, city data, shared architecture modules and district assets |
| Fuel/Wanted, gigs and owner controls | [Tokyo #483](https://github.com/doublehidenblade/tokyo-drift-3d/pull/483), td-203–208 and existing owner patches | No HUD, wallet, input, police, fuel, settlement or gig refactor for a viewer |
| Pedestrians and taxi / Forge assets | [Tokyo #486](https://github.com/doublehidenblade/tokyo-drift-3d/pull/486), td-186 | Reuse approved assets if suitable; existing adapter, traffic and animation remain owner-controlled |
| Large-build delivery | [Tokyo #496](https://github.com/doublehidenblade/tokyo-drift-3d/pull/496) | No export/deploy/workflow changes to carry optional truck art into the current release |

The published garage design branch contains a final-only image manifest and README, but the checked tree contains no PNGs under `assets/mocks/garage-progression/mini-truck-r3/`. That does not rule out files elsewhere or a pending upload. Verify actual readable bytes before reference-dependent 3D; do not retry an uncertain upload blindly.

## Collision-safe plan records

The `tc-mvp-01` through `tc-mvp-04` identifiers are local planning IDs within this addendum, not new global td reservations or authoritative board transitions. Each is a JSON task record following the established ownership, dependencies, criteria, evidence, work-log and independent-verdict structure. Their `blocked` status prevents the filing itself from implying dispatch or completion.

- [tc-mvp-01](tasks/tc-mvp-01.json): inspect source pixels and deliver an original, labeled reference/mock contact sheet
- [tc-mvp-02](tasks/tc-mvp-02.json): reuse or produce the smallest original mini-truck source/export kit, with one visible module demonstration
- [tc-mvp-03](tasks/tc-mvp-03.json): integrate the later rotatable actual-garage viewer and minimal appearance flow
- [tc-mvp-04](tasks/tc-mvp-04.json): independently validate the exact integrated slice

**Proposed next task:** tc-mvp-01, mapped into td-197's existing reference lane. Preserve current owner work and use a new isolated output folder. Its first gate is actual accessible source pixels plus rights/provenance labels, not another runtime garage task.

The coordinator should bind each plan record to the existing task owner or reserve a new canonical td task only after verifying no overlap. Fill the actual executor, supported model/effort, capacity, exclusive paths, source SHA and worker assignment before claiming `in_progress`. Do not interpret these recommendations as confirmed runtime capability.

## Allowed paths and later handoff

This documentation filing owns only `game-design/research/truck-customization-20261008/`. Existing central boards, coordinator log, old garage assets and all game runtime files are read-only here.

A later reference/mock producer may add original output beneath this folder's `mocks/` after file and provenance review. Asset authoring must first agree a fresh source/export/QA subfolder with the td-198/Forge owner. Read the actual vehicle, common sockets and approved source asset before creating a second chassis. No main-scene hookup belongs in the asset task.

A later runtime handoff needs a written exact-file allowlist approved by the owner of the shared garage/vehicle/UI interfaces. If those files are actively owned, park the dependent integration instead of broadening this task. Paid paint, gig rewards or new module capability are separate owner integrations; the viewer cannot mint money, equipment or unlocks.

## Stop and escalation gates

- Required reference bytes missing, mismatched or denied: stop image-dependent work and report the exact input gap
- Active equivalent owner or uncertain stopped-worker state: reconcile before another worker begins
- Required frontier tier, Blender/Godot, or pixel inspection missing: wait; no weaker production substitute
- Same approach fails twice identically, or ownership/schema/economy scope expands: stop with evidence and a changed hypothesis
- Mock/asset is ready: independent reviewer opens it before it is used as an accepted gate
- Runtime or current release dependency is not ready: keep tc-mvp-03/04 blocked and keep customization out of the release
