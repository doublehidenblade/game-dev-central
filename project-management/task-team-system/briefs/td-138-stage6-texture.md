# td-138 stage 6 — polish + texture (materials, paint, livery) for the BMW M4 GT3

Repo: doublehidenblade/tokyo-drift-3d (environment: tokyo-drift-3d)
Task file: godot/docs/tasks/td-138.md
Authoritative inputs (all on main, supervisor-inspected PASS — reuse, do not redo):
- godot/qa/td-138/detail.blend — the stage-5 detail geometry (79,696 evaluated
  tris, 25 named parts, all connected, geometry-only, supervisor PASS 2026-10-01).
  Branch FROM THIS detail model — do not rebuild geometry from scratch.
- godot/qa/td-138/modeling-spec.md — THE build contract: 25-part build order (§2),
  triangle budget 60k floor / 84k target (§3), topology standards (§4),
  25-item connection-verification checklist (§5), Blender setup + acceptance triptychs (§6)
- godot/qa/td-138/mock-dimension-spec.md — numeric source of truth (datums, 25 parts, bounds)
- godot/qa/td-138/triptych-detail-front.png, triptych-detail-side.png,
  triptych-detail-rear.png — the stage-5 acceptance triptychs
- godot/docs/research/td-138-round2-research.md — stage-1 research

## Context: why stages now
Round 3 was the last single-worker attempt at the hero car. Craig's fallback:
decompose into dependent staged sessions, each gated on supervisor inspection.
Stages 2 (mocks), 3 (modeling spec), 4 (rough blockout), and 5 (detail geometry)
PASSED inspection and are merged to main. This is STAGE 6: polish + texture —
turn the detailed clay geometry into a finished hero car. Stage 7 (turntable
animation) comes after; this stage is the final static model.

## Your deliverable (this stage ONLY — materials and finish, no geometry rebuild)
Start from detail.blend on main. Keep the 25-part structure, datums, envelope
(5.020 x 2.040 x 1.310 m), and axle positions. Geometry changes are limited to
fixing defects the texturing exposes (seams, normal flips, UV stretch) — no
new modeling unless a part is broken.
1. Materials: automotive clearcoat-style paint (dark + white split per the
   reference livery), carbon-fiber for splitter/diffuser/wing elements, brushed
   metal for exhaust outlets, rubber for tires, dark glass for the greenhouse,
   emissive lamp materials for headlights/taillights (off-state look, not lit).
2. Livery: BMW Motorsport-style racing livery — M-color stripes (light blue /
   dark blue / red) on the hood and flanks, BMW roundel on hood and grille,
   "M4 GT3" script on the kidney surround, door number roundels, windshield
   banner. DECALS must sit on the surface (no floating planes — the standing
   no-disconnected-pieces rule applies to decals too). Keep it restrained and
   close to the reference photos — this is a race car, not a billboard.
3. Glass: transparent greenhouse with the stage-5 seat/roll-cage mass visible
   through it. No transparency anywhere else — every other surface 100% opaque
   (Craig 2026-09-16/21: no transparency in game art).
4. Tires/wheels: dark tire rubber with tread hint, wheel spokes in a dark
   metallic finish, visible brake discs + calipers behind them.
5. Lighting/render: studio-style three-point lighting renders, not flat clay.
   The final triptychs must read as a real GT3 race car against the reference
   photos.

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks. Local
checks only.

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow.
- Process: real reference photo → 2D mock → 3D render at matched angles →
  side-by-side triptychs. Iterate the materials/livery until the 3D reads as
  the photographed M4 GT3 at all three angles.
- Honest evidence: the triptychs are composed from the SAME .blend in ONE
  deterministic Blender render session. Every panel is honestly labeled (real
  photo vs 2D mock vs 3D render).

## 2. Quality bar (MANDATORY)
- The finished render reads as the photographed M4 GT3 in BMW Motorsport
  livery — sharp GT3 aero, M-stripe livery, tall paired kidneys, blade lamps,
  vented hood, boxed arches, swan-neck wing. Round 3 failed exactly here.
- Livery is restrained and matches the reference — stripes, roundels, number
  roundels, windshield banner. No invented sponsors, no clutter.
- Decals sit ON the surface — zero floating planes, zero z-fighting.
- Glass is the ONLY transparent material; everything else 100% opaque.
- Reference photos are CC BY-SA 4.0: evidence only, never in runtime exports.

## 3. Excluded degenerate shortcuts (MANDATORY)
- A flat color fill passed off as "paint" is NOT acceptable — clearcoat-style
  materials with proper specular response.
- Livery as floating decal planes hovering off the surface is NOT acceptable —
  shrink-wrapped or surface-conforming decals only.
- Transparency anywhere except the greenhouse glass is NOT acceptable.
- Invented sponsor logos or cluttered fantasy liveries are NOT acceptable —
  restrained, reference-matched.
- Screenshots without the triptych structure (reference + mock + render) are
  NOT acceptance evidence. Video-game screenshots are never "real photos".
- Checkbox completion (files committed) without visual quality does not count
  as done.

## 4. Effort calibration (MANDATORY)
Serious multi-hour Blender materials/lighting work — this is the finish Craig's
QA verdict lands on. The geometry is done; this stage is what makes it read as
real. Take the time to match the photos.

## 5. Evidence (MANDATORY)
Commit under godot/qa/td-138/:
- hero-m4gt3.blend (the finished model — keep detail.blend intact, do not overwrite)
- triptych-final-front.png, triptych-final-side.png, triptych-final-rear.png
  (reference + mock + finished render, matched angles, studio lighting)
- material-proof.png (close-up boards: paint, carbon, glass, tire, lamp materials)
- livery-proof.png (close-up boards: hood stripes, door roundels, windshield
  banner, kidney script — proving decals sit on the surface)
- Record EVERY path in the td-138.md task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- Branch from main as td-138-stage6-texture. Open the PR and LEAVE IT OPEN. DO NOT MERGE.
- DO NOT MERGE PR #253 (td-138-round3, rejected negative evidence, do-not-ship).
- DO NOT set done-pending-verdict — that follows independent supervisor inspection only.
- A supervisor inspects the final triptychs and material/livery boards before
  STAGE 7 (turntable animation) is dispatched. Nothing proceeds on self-certification.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Board status table is source of truth; update ONLY your own row, via PR.
- No purchased packs without Craig's approval; no commercial-game assets ever.
- Standing vehicle rules: (1) no disconnected pieces, (2) real-world dimensions,
  (3) royalty-free stores researched, CC0/CC-BY verified before adopting.
- Craig 2026-10-01: completed models are placed without waiting for go-ahead
  ("we have 0 players") — placement happens after stage 7, not in this stage.
