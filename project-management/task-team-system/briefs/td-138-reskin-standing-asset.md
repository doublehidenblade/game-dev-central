# td-138 hero car — reskin from standing asset (Craig 2026-10-01)

Pivot ordered by Craig after two failed script-driven Blender iterations
(PR #253 rejected, PR #260 rejected — faceted panels, black-void grilles,
bulbous cabin, crude hood vents, slab headlights). New approach: start from a
verified royalty-free base mesh, verify against real dimensions/photos, reskin.

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks.
Local checks only. (Craig 2026-09-27)

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow
- Process: real reference photo → 3D render at matching angles →
  side-by-side triptych (reference + render) → iterate until the render reads
  as the real car against the photo. No 2D mock needed (base mesh exists);
  the triptych comparison against real photos is still mandatory.

## 2. Quality bar (MANDATORY)
- **Base mesh:** "Nissan GT-R LM Nismo" by vecarz, CC-BY 4.0, 62.8k tris /
  39.7k verts —
  https://sketchfab.com/3d-models/nissan-gt-r-lm-nismo-wwwvecarzcom-e2b7988d402a4af6af9cf51144daa798
  The model file will be provided in the repo (see branch). If it is missing,
  STOP and report — do not substitute another model.
- **Real car:** 2015 Nissan GT-R LM Nismo, LMP1 Le Mans prototype (Japanese
  race car). Real dimensions per Nissan/Wikipedia: **4.645 m long × 1.900 m
  wide × 1.030 m high**. Scale the import so the model is exactly 4.645 m
  long; verify width/height against the real numbers after scaling.
- **Must read as the photographed car:** long front deck, enclosed cockpit
  canopy, full-width rear wing, LMP1 proportions (very low, very wide).
  Judge against REAL photos of the GT-R LM Nismo (2015 Le Mans), not renders.
- **Smooth shading everywhere.** The faceted "folded paper" look of the
  rejected iteration is the primary defect to avoid — check every body panel
  in the render.
- **Livery:** white-front / black-rear split, FLAT UV-painted. Raised-geometry
  livery was the round-3 rejection — never again.
- **Detail:** headlights with internal detail (not featureless slabs); grilles
  with mesh/slat detail (not black voids); panel gaps tight and even;
  mirrors, wing mounts and aero parts fully connected — no floating pieces.
- **Provenance check:** the source page carries a "gta" tag. Visually confirm
  the mesh matches real GT-R LM Nismo photos. If it looks like a ripped
  video-game asset rather than the real car, STOP and report — do not ship it.

## 3. Excluded degenerate shortcuts (MANDATORY)
- The base mesh is provided; generating a new script-built car is NOT the task.
- A video-game screenshot is NEVER a "real photo" reference; every triptych
  panel must be honestly labeled (real photo vs 3D render).
- Checkbox completion (files committed, tri counts) without visual quality
  does not count as done.
- Do not "fix" proportions by stretching the mesh non-uniformly — if the base
  mesh doesn't match real dimensions after uniform scaling, report it.

## 4. Effort calibration (MANDATORY)
Serious multi-hour Blender work, not a quick script: import, uniform
scale-to-real-dimensions, smooth-shading pass, UV livery paint, material
pass (paint / carbon / glass / tire), connected-parts check, triptych
renders at matching angles, iterate until it reads as the real car.

## 5. Evidence (MANDATORY)
- `godot/qa/td-138/reskin-triptych-front.png` (real photo + render, front 3/4)
- `godot/qa/td-138/reskin-triptych-side.png` (real photo + render, side)
- `godot/qa/td-138/reskin-triptych-rear.png` (real photo + render, rear 3/4)
- `godot/qa/td-138/reskin-detail.png` (headlight/grille close-up vs real photo)
- Real reference photo sources credited in `godot/docs/tasks/td-138.md`.
- Every path recorded in the task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- New branch `td-138-reskin-lm-nismo`. Push to the branch and LEAVE THE PR
  OPEN. DO NOT MERGE. DO NOT set done-pending-verdict — that follows
  independent supervisor inspection only.
- A supervisor inspects the triptychs against the real photos before anything
  merges. Merging unverified work gets reverted.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Status table is source of truth; board updates via PR only, own row only.
- **CC-BY attribution (legally required):** credit in
  `godot/docs/tasks/td-138.md` AND wherever the game credits third-party
  assets: "Nissan GT-R LM Nismo 3D model by vecarz
  (https://sketchfab.com/3d-models/nissan-gt-r-lm-nismo-wwwvecarzcom-e2b7988d402a4af6af9cf51144daa798),
  licensed CC Attribution 4.0 International."
- No purchased packs; no commercial-game assets ever.
- Any code follows SCS architecture (scene split + config + signals).
