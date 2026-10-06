# td-138 stage 4 — rough Blender blockout of the BMW M4 GT3

Repo: doublehidenblade/tokyo-drift-3d (environment: tokyo-drift-3d)
Task file: godot/docs/tasks/td-138.md
Authoritative inputs (all on main, supervisor-inspected PASS — reuse, do not redo):
- godot/qa/td-138/mock-side.png, mock-front.png, mock-rear.png, mock-three-quarter.png
  (2400x1400 measured boards; side: 5.020 m = 1,200 px = 4.183 mm/px; front/rear: 470 px/m)
- godot/qa/td-138/mock-dimension-spec.md — numeric source of truth (datums, 25 parts, bounds)
- godot/qa/td-138/modeling-spec.md — THE build contract: 25-part build order (§2),
  triangle budget 60k floor / 84k target (§3), topology standards (§4),
  25-item connection-verification checklist (§5), Blender setup + acceptance triptychs (§6)
- godot/docs/research/td-138-round2-research.md — stage-1 research

## Context: why stages now
Round 3 was the last single-worker attempt at the hero car. Craig's fallback:
decompose into dependent staged sessions, each gated on supervisor inspection.
Stages 2 (mocks) and 3 (modeling spec) PASSED inspection and are merged to main.
This is STAGE 4: the first 3D work. Build the rough blockout — every major mass
at real dimensions, every part joined, proportions verified against the photos
before any detail work begins.

## Your deliverable (this stage ONLY — blockout, no detail pass, no textures)
1. A Blender blockout (.blend committed under godot/qa/td-138/) with ALL 25
   parts from modeling-spec §2 built as joined masses at the spec's real
   dimensions — body shell, greenhouse, bumpers, flares, hood, vents, splitter,
   skirts, diffuser, wing + swan-neck mounts, kidneys, intakes, canards,
   lamps, mirrors, wheels/brakes, exhausts. Every part CONNECTED per spec §5
   (no floating pieces — the standing rule that killed round 1).
2. Correct proportions: long hood, rearward cabin, boxed GT3 arches, 5.020 m
   envelope, axles at X=1.020/3.937. Quad-dominant topology, subdivision-ready;
   blockout does not need the full 60k triangles yet, but the topology must be
   able to reach it (no n-gons on visible surfaces, edge loops on panel lines).
3. The three acceptance triptychs from modeling-spec §6 (reference photo + 2D
   mock + blockout screenshot at matched angles: front three-quarter, side,
   rear) PLUS the 25 connection-verification screenshots from spec §5.

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks. Local
checks only.

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow.
- Process: real reference photo → 2D mock → 3D screenshot, as side-by-side
  triptychs. Iterate the blockout until its silhouette, stance, and part
  placement match the photo at all three angles.
- Build order: follow modeling-spec §2 exactly (01–25). Do not reorder.
- Reference setup: modeling-spec §6 (units in meters, calibrated background
  images per view).

## 2. Quality bar (MANDATORY)
- Every one of the 25 parts present, at the dimension sheet's bounds, visibly
  connected (spec §5 checklist — every box ticked with a named screenshot).
- The blockout reads as the photographed M4 GT3: sharp GT3 aero, tall paired
  kidneys, blade lamps, vented hood, boxed arches, deep splitter/diffuser,
  swan-neck wing — not a generic wedge. Round 3 failed exactly here.
- All dimensions trace to the dimension sheet; the gaps in modeling-spec §7
  are respected (no invented numbers — provisional shapes only, clearly labeled).

## 3. Excluded degenerate shortcuts (MANDATORY)
- A single merged blob with no separate parts is NOT a blockout — 25 named
  parts, each identifiable.
- Screenshots without the triptych structure (reference + mock + render) are
  NOT acceptance evidence.
- Skipping the connection screenshots is NOT acceptable — spec §5 is binding.
- Do not redo stages 1–3. Build on them.

## 4. Effort calibration (MANDATORY)
Real Blender modeling work — this is the foundation the detail pass builds on.
A blockout that gets the proportions wrong poisons every later stage. Take the
time to match the photos.

## 5. Evidence (MANDATORY)
Commit under godot/qa/td-138/:
- blockout.blend (the model)
- triptych-front.png, triptych-side.png, triptych-rear.png (reference + mock + render)
- connection-*.png (the 25 spec-§5 proof screenshots)
- Record EVERY path in the td-138.md task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- Branch from main as td-138-stage4-blockout. Open the PR and LEAVE IT OPEN. DO NOT MERGE.
- DO NOT MERGE PR #253 (td-138-round3, rejected negative evidence, do-not-ship).
- DO NOT set done-pending-verdict — that follows independent supervisor inspection only.
- A supervisor inspects the triptychs and connection screenshots before STAGE 5
  (detail pass) is dispatched. Nothing proceeds on self-certification.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Board status table is source of truth; update ONLY your own row, via PR.
- Reference photos are CC BY-SA 4.0: evidence only, never in runtime exports.
- No purchased packs without Craig's approval; no commercial-game assets ever.
- Standing vehicle rules: (1) no disconnected pieces, (2) real-world dimensions,
  (3) royalty-free stores researched, CC0/CC-BY verified before adopting.
- Craig 2026-10-01: completed models are placed without waiting for go-ahead
  ("we have 0 players") — but THIS stage is blockout only; placement comes later.
