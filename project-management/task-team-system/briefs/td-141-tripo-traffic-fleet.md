# td-141 — Tripo traffic fleet: 12 base car models → Blender rebuild → in the game scene

Craig's directive (2026-10-01, upgraded same day): dispatch workers on the 12
Tripo base models — REBUILD them as clean low-poly in Blender (the raw
image-to-3D outputs are reference only: rough unclean edges, fused single
meshes, baked branding) — and don't stop until they are in the game scene.

Source assets (already staged, verified valid single-mesh GLBs):
`~/workspace/tripo-batch/<name>/<name>.glb` + `ref.*` (the real-photo reference)
+ `manifest.json`, for: sedan, suv, van, bus, pickup, hatchback, coupe,
keicar, wagon, minivan, luxury, boxtruck. Each generated 2026-10-01 via the
Tripo API with face_limit=15000 (already game-range poly counts, ~2.5–3.9 MB
each). Generation cost 360 credits (~$3.60).

Blender (installed 2026-10-01 on the worker VM): `~/workspace/tools/blender-5.2.0-linux-x64/blender`
(5.2.0 LTS, verified). Use this binary directly — no system blender exists.
Headless: `blender --background --python script.py`.

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks.
Local checks only. (Craig 2026-09-27)

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow.
- Process: real reference photo → matching-angle 3D render → side-by-side
  triptych → iterate until the 3D reads as real against the photo.
- The staged `ref.*` images ARE the real-photo references each model was
  generated from. Cleanup iterates the Blender result against them.

## 2. Quality bar (MANDATORY)
- REBUILD, don't clean up. The raw Tripo GLBs are proportion/visual reference
  ONLY — never used directly in-game. Per model in Blender: retopo/model a
  clean low-poly body (clean quad topology, no AI-mesh garbage edges; target
  ~3–8k tris per traffic car — they are background vehicles seen at distance),
  using the Tripo GLB + ref photo for proportions.
- Wheels are SEPARATE meshes/nodes from the body so they can spin (raw GLBs
  are one fused mesh — wheels cannot turn). Simple low-poly wheel: dark tire
  + plain hub. A tiny spin script driven by vehicle speed wires up in Godot.
- Smooth shading everywhere. Faceted/flat-shaded body panels read as folded
  paper — this exact failure killed td-138 stage 6 (PR #260, rejected by
  Craig). Auto-smooth or proper smooth shading on all body panels.
- No disconnected/floating parts — every part joined to the body (Craig's
  standing modeling rule #1, from the td-138 round-1 rejection). Exception:
  the 4 wheels, deliberately separate for rotation.
- Generic liveries, varied paint colors across the 12. NO real-world
  branding: strip every badge, logo, and CALSONIC/Nissan-style text the
  Tripo textures baked in. No baked Tripo textures reused.
- Materials: realistic PBR, NOT flat single-color surfaces. Car paint =
  metallic, low roughness — it must read as glossy paint under the scene's
  sky/environment (verify in-game that reflections actually read; paint
  looking flat means the env contribution is missing). Glass = dark tinted,
  slight metallic. Tires = near-black, high roughness. Where a tileable map
  helps (tire rubber grain, subtle paint roughness variation), pull CC0
  sets from Poly Haven / ambientCG — never lift textures off Sketchfab car
  models (per-model licenses are murky, UVs won't match, provenance risk;
  Sketchfab's licensed use is whole parts like wheels, verified CC0/CC-BY
  per Craig's standing asset rule).
- Proportions must read as the real car in the reference photo at matching
  angles. 4 wheels on the ground plane, left-right symmetric, glass where
  the windows are.
- Materials 100% opaque — no transparency anywhere.

## 3. Excluded degenerate shortcuts (MANDATORY)
- No script-generated primitive stand-ins, and NO raw Tripo GLBs used
  directly in-game. The Tripo outputs are reference for the Blender rebuild,
  not the deliverable.
- Triptych panels honestly labeled: reference photo vs Blender render vs
  in-game capture. A game screenshot is never a "render".
- Checkbox completion (12 files committed, tri counts) without visual
  quality does not count as done.
- No merging without independent supervisor inspection.

## 4. Effort calibration (MANDATORY)
Serious multi-day-capable effort: 12 models × a real Blender cleanup pass,
then Godot import + vehicle wiring + TrafficManager variety + in-game
verification. Parallelize cleanup across subagents (3–4 models each), then
one integration pass. A rushed single-session pass will be rejected.

## 5. Evidence (MANDATORY)
- Per model: triptych `godot/qa/td-141/<model>-triptych.png` (ref photo →
  cleaned Blender render, matching angles).
- In-game: `godot/qa/td-141/traffic-*.png` — traffic with the new models
  visible on the road, chase-cam and roadside angles.
- Every path recorded in the `godot/docs/tasks/td-141.md` evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- Branch: `td-141-tripo-traffic-fleet`. Task file: `godot/docs/tasks/td-141.md`.
- When done: push, open the PR, LEAVE IT OPEN. DO NOT MERGE.
- DO NOT set done-pending-verdict — that follows independent inspection only.
- Board: add the td-141 row via PR to
  `doublehidenblade/game-dev-central` (`project-management/boards/tokyo-drift-3d.md`),
  own row only, status-cell prefix matching.
- Merging unverified work gets reverted.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Royalty-free only; no purchased packs without Craig's approval; no
  commercial-game assets ever.
- Tripo provenance: generated 2026-10-01 via Tripo API on Craig's paid API
  credits. Record in `godot/assets/ATTRIBUTION.md` and
  `THIRD_PARTY_LICENSES.md`. Liveries genericized, zero trademarks.

## Pipeline (coordinator runs this end to end)
1. RECON — read `godot/scripts/traffic.gd`, `traffic_ai.gd`,
   `vehicle-model.gd`, `godot/scenes/tokyo_vehicle.tscn`,
   `tokyo_sedan.tscn`, and `godot/models/cars/` (existing fleet: sedan,
   suv, van, taxi, race). Learn exactly how a .glb becomes a traffic car
   today. TrafficManager spawns `count` cars from a `vehicle_scene`
   PackedScene — figure out the cleanest way to give it 12-model variety.
2. REBUILD (Blender, fan out) — per model: import the Tripo GLB as a
   proportion/visual reference; retopo/model a clean low-poly body (~3–8k
   tris, clean quads, smooth-shaded); model wheels as SEPARATE meshes (dark
   tire + plain hub) so they can spin; generic opaque materials, all baked
   branding stripped, varied plain colors; sanity-check proportions vs the
   ref photo at matching angles; export the game-ready GLB. Triptych per
   model: ref photo → Blender render → (later) in-game capture.
3. IMPORT — rebuilt GLBs → `godot/models/cars/tripo/` (new dir), following
   the repo's .glb conventions. Raw Tripo GLBs NEVER enter the repo.
4. WIRE — vehicle scenes for the new models; extend TrafficManager/config
   so spawned traffic draws from the 12-model variety. SCS architecture:
   scene = one scene one script; config numbers separated (autoload or
   @export); modules communicate via signals. Do NOT refactor working
   traffic code for compliance — add variety cleanly.
5. VERIFY IN-GAME — headless-harness run, capture traffic screenshots with
   the new models visible; confirm variety (not 8 copies of one model),
   no z-fighting, wheels on road, no console errors from the new assets.
6. TASK FILE + BOARD ROW + PR (open, unmerged). Done = "in the game scene"
   with evidence, PR open for inspection.

Craig's close-out bar: the 12 models drive as traffic in the game scene,
visibly varied, clean-shaded Blender rebuilds (not raw Tripo outputs),
generic liveries, no branding, wheels separate and spinning — PR open with
triptychs + in-game captures. Do not stop until that is true.
