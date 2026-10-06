# td-138 stage 3 — Blender modeling specification for the BMW M4 GT3

Repo: doublehidenblade/tokyo-drift-3d (environment: tokyo-drift-3d)
Task file: godot/docs/tasks/td-138.md
Stage 1 research (DONE, reuse, do not redo): godot/docs/research/td-138-round2-research.md
Stage 2 deliverables (DONE, supervisor-inspected PASS 2026-10-01, do not redo):
  branch td-138-stage2-mocks, PR #254 (open, do not merge):
  - godot/qa/td-138/mock-side.png, mock-front.png, mock-rear.png, mock-three-quarter.png
    (2400x1400 measured boards; side board: 5.020 m = 1,200 px, i.e. 1 px = 4.183 mm;
    front/rear boards: width at 470 px/m)
  - godot/qa/td-138/mock-dimension-spec.md — THE source of truth: coordinate datums,
    26 parts with target bounds, surfacing notes, and physical connection points.
    If any raster line disagrees with a number, the number wins.

## Context: why stages now
Round 3 was the last single-worker attempt at the hero car. Craig's fallback:
decompose into dependent staged sessions, each gated on supervisor inspection.
Stage 2 (2D measured mocks + dimension sheet) PASSED inspection. This is STAGE 3.
Nothing here is 3D modeling yet — this stage produces the document the Blender
stages (4–6) build from, so a modeler never has to guess a dimension, a build
order, or a topology decision.

## Your deliverable (this stage ONLY — no Blender, no mesh)
`godot/qa/td-138/modeling-spec.md`: a Blender modeler's build plan that turns the
stage-2 dimension sheet into an unambiguous construction order. It must contain:
1. **Part-by-part build order** — the exact sequence a modeler follows
   (e.g. main body shell → greenhouse/glass → fender flares → splitter/diffuser →
   wing + mounts → hood/vents → lamps/kidneys/intakes → mirrors → wheels/brakes →
   panel gaps/bevels). Every part in the stage-2 spec appears exactly once, in order.
2. **Per-part construction method** — for EACH part: how to build it in Blender
   (starting primitive or profile, key modifiers, topology approach), which
   orthographic mock(s) to use as background reference images (with the exact
   px-to-meter mapping from stage 2), and the target bounds copied from the
   dimension sheet (do not invent new numbers — cite the sheet).
3. **Triangle budget table** — allocate the hero-car bar (floor 60,000, target 80,000+)
   across parts (body shell, glass, wheels ×4, brakes, aero, lamps, details…).
   The allocations must sum to ≥60k with a stated path to 80k+. The stage-4/5
   workers will be held to this table.
4. **Topology standards** — quad-dominant, edge loops follow panel lines, support
   loops at hard edges, no n-gons on visible surfaces, 5–7 mm modeled panel gaps
   with sealed dark backing, bevel targets (3–6 mm body creases, 1–2 mm carbon
   blades, 0.5–1 mm lens edges), 10–15 mm glass inset. Copy the numbers from the
   stage-2 spec §4; do not restate them loosely.
5. **Connection verification checklist** — for every aerodynamic add-on and every
   part, the physical root/bolt-pad/fillet/bonded-seam that proves it is CONNECTED
   (standing rule 1: no disconnected pieces, no floating mounts, no raw junctions).
   The stage-4 worker must tick every box with a screenshot.
6. **Stage-4 readiness** — what the blockout worker needs on day one: background
   image setup (which PNG on which Blender view, scale calibration), unit setup
   (meters), and the three acceptance renders it must produce (triptych:
   reference photo + 2D mock + blockout screenshot at matching angles).

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks. Local
checks only.

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow (specification stage).
- Process: every number in your spec traces to the stage-2 dimension sheet or the
  stage-1 research doc. Quote the source (sheet §N / research doc section) for
  every dimension you copy. If the sheet is missing a number you need, say so
  explicitly in a "gaps" section — never invent it silently.

## 2. Quality bar (MANDATORY)
- Zero invented dimensions. Every bound cites mock-dimension-spec.md §2/§3.
- The build order is physically sensible (shell before aero bolted to it; glass
  before the trim that frames it).
- The triangle budget is realistic per part (a GT3 wheel with tire + rim + brake
  is thousands of tris, not hundreds) and sums to ≥60k.
- The connection checklist covers every part that round 1 left floating
  (rear-deck wing mounts especially).
- A competent Blender modeler with no other context could build the car from
  this document + the stage-2 boards alone.

## 3. Excluded degenerate shortcuts (MANDATORY)
- A parts list with no build order, no construction method, and no triangle
  budget is NOT a specification — it is a table of contents. Not acceptable.
- Copying the stage-2 spec verbatim with "model this in Blender" appended is
  NOT stage 3 — the value you add is build order, construction method, topology
  decisions, and the budget table.
- Do not redo stage 1 research or stage 2 mocks. Reference them; build on them.

## 4. Effort calibration (MANDATORY)
Careful technical writing — this document is the contract every Blender stage
works to. If it takes a full session, that is expected. Precision over speed.

## 5. Evidence (MANDATORY)
Commit under godot/qa/td-138/:
- modeling-spec.md (the build plan)
- Record the path in the td-138.md task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- Branch from main as td-138-stage3-spec; push and LEAVE THE PR OPEN. DO NOT MERGE.
- DO NOT MERGE PR #253 (td-138-round3, rejected negative evidence, do-not-ship)
  or PR #254 (stage 2, stays open until the pipeline completes).
- DO NOT set done-pending-verdict — that follows independent supervisor
  inspection only.
- A supervisor inspects the spec before STAGE 4 (rough Blender blockout) is
  dispatched. Nothing proceeds on self-certification.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Board status table is source of truth; update ONLY your own row, via PR.
- Reference photos are CC BY-SA 4.0: evidence only, never in runtime exports.
- No purchased packs without Craig's approval; no commercial-game assets ever.
- Standing vehicle rules: (1) no disconnected pieces, (2) real-world dimensions,
  (3) royalty-free stores researched, CC0/CC-BY verified before adopting.
