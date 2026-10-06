# td-138 stage 5 — detail pass on the BMW M4 GT3

Repo: doublehidenblade/tokyo-drift-3d (environment: tokyo-drift-3d)
Task file: godot/docs/tasks/td-138.md
Authoritative inputs (all on main, supervisor-inspected PASS — reuse, do not redo):
- godot/qa/td-138/blockout.blend — the stage-4 rough blockout (48,568 evaluated
  tris, 25 named parts, all connected, supervisor PASS 2026-10-01). Branch FROM
  THIS blockout — do not rebuild the masses from scratch.
- godot/qa/td-138/modeling-spec.md — THE build contract: 25-part build order (§2),
  triangle budget 60k floor / 84k target (§3), topology standards (§4),
  25-item connection-verification checklist (§5), Blender setup + acceptance triptychs (§6)
- godot/qa/td-138/mock-dimension-spec.md — numeric source of truth (datums, 25 parts, bounds)
- godot/qa/td-138/triptych-front.png, triptych-side.png, triptych-rear.png — the
  stage-4 acceptance triptychs (reference photo + 2D mock + blockout render)
- godot/docs/research/td-138-round2-research.md — stage-1 research

## Context: why stages now
Round 3 was the last single-worker attempt at the hero car. Craig's fallback:
decompose into dependent staged sessions, each gated on supervisor inspection.
Stages 2 (mocks), 3 (modeling spec), and 4 (rough blockout) PASSED inspection
and are merged to main. This is STAGE 5: the detail pass — turn the blockout's
correct masses into real GT3 surface detail. Stage 6 (materials/livery/textures)
comes after; this stage is GEOMETRY only.

## Your deliverable (this stage ONLY — detail geometry, no materials/livery)
Start from blockout.blend on main. Keep the 25-part structure, datums, envelope
(5.020 x 2.040 x 1.310 m), and axle positions. Add real GT3 detail to every part:
1. Aero detail: front splitter with fences and full-span root, canards (stacked
   blades on both corners), vented hood with louvered outlets, boxed fender
   flares front/rear, side skirts with vertical fences, rear diffuser with
   vertical strakes, rear wing plane with endplates + the connected swan-neck
   mounts (already connected in stage 4 — keep them connected).
2. Face detail: tall paired kidney grilles with slat structure, corner intakes
   with depth, blade headlights and taillight blades (lamp housings, not decals),
   side mirrors with stalks.
3. Wheels/brakes/exhausts: multi-spoke wheel geometry, visible brake discs +
   calipers behind them, dual exhaust outlets with depth.
4. Interior hint: dark glasshouse with a visible seat/roll-cage mass behind the
   glass — enough to read as a race car through the windshield, not an empty shell.
5. ALL 25 parts remain CONNECTED per modeling-spec §5 (no floating pieces — the
   standing rule that killed round 1). Topology: quad-dominant, subdivision-ready,
   no n-gons on visible surfaces, edge loops on panel lines. Triangle count:
   60,000 floor / 84,000 target per modeling-spec §3 (stage-4 blockout was
   48,568 — grow it honestly, not by subdivision alone).

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks. Local
checks only.

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow.
- Process: real reference photo → 2D mock → 3D render at matched angles →
  side-by-side triptychs. Iterate the detail pass until the 3D reads as the
  photographed M4 GT3 at all three angles.
- Detail order: follow modeling-spec §2 exactly (01–25). Do not reorder.
- Honest evidence: the triptychs and connection boards are composed from the
  SAME .blend in ONE deterministic Blender render session. Every panel is
  honestly labeled (real photo vs 2D mock vs 3D render).

## 2. Quality bar (MANDATORY)
- The render reads as the photographed M4 GT3: sharp GT3 aero, tall paired
  kidneys, blade lamps, vented hood, boxed arches, deep splitter/diffuser,
  swan-neck wing — not a generic wedge. Round 3 failed exactly here.
- Every one of the 25 parts present, at the dimension sheet's bounds, visibly
  connected (spec §5 checklist — every box ticked with a named screenshot).
- Panel gaps, bevels, glass insets, and wheel clearances per modeling-spec §4.
- 60k tri floor / 84k target per modeling-spec §3, earned with real detail.
- Reference photos are CC BY-SA 4.0: evidence only, never in runtime exports.

## 3. Excluded degenerate shortcuts (MANDATORY)
- Subdivision-surface inflation to hit the tri floor without real detail is NOT
  acceptable — the budget must be earned with modeled features.
- Texture/paint/livery tricks are NOT a substitute for geometry — stage 6 is
  the materials stage; this stage is geometry only. Clay/matcap renders are fine.
- A single merged blob with no separate parts is NOT a model — 25 named parts,
  each identifiable.
- Screenshots without the triptych structure (reference + mock + render) are
  NOT acceptance evidence. Video-game screenshots are never "real photos".
- Checkbox completion (files committed, tri counts) without visual quality
  does not count as done.

## 4. Effort calibration (MANDATORY)
Serious multi-hour Blender modeling — this is the geometry Craig's QA verdict
lands on. Round 2 shipped a 14-minute script box-model and was reverted; that
is the failure mode this brief exists to prevent. Take the time to match the
photos. A script may BUILD the deterministic scene, but the detail must be
modeled, not inflated.

## 5. Evidence (MANDATORY)
Commit under godot/qa/td-138/:
- detail.blend (the detailed model — keep blockout.blend intact, do not overwrite)
- triptych-detail-front.png, triptych-detail-side.png, triptych-detail-rear.png
  (reference + mock + detail render, matched angles)
- connection-detail-*.png (the 25 spec-§5 proof screenshots, re-shot on the
  detailed model — connections must survive the detail pass)
- wireframe-detail.png (subdivision cage / wireframe proof of quad topology)
- tri-count.txt (evaluated triangle count + per-part breakdown vs the §3 budget)
- Record EVERY path in the td-138.md task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- Branch from main as td-138-stage5-detail. Open the PR and LEAVE IT OPEN. DO NOT MERGE.
- DO NOT MERGE PR #253 (td-138-round3, rejected negative evidence, do-not-ship).
- DO NOT set done-pending-verdict — that follows independent supervisor inspection only.
- A supervisor inspects the triptychs, connection boards, and wireframe before
  STAGE 6 (polish + texture) is dispatched. Nothing proceeds on self-certification.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Board status table is source of truth; update ONLY your own row, via PR.
- No purchased packs without Craig's approval; no commercial-game assets ever.
- Standing vehicle rules: (1) no disconnected pieces, (2) real-world dimensions,
  (3) royalty-free stores researched, CC0/CC-BY verified before adopting.
- Craig 2026-10-01: completed models are placed without waiting for go-ahead
  ("we have 0 players") — placement happens after stage 7, not in this stage.
