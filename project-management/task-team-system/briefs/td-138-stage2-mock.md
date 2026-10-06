# td-138 stage 2 — 2D orthographic mocks of the BMW M4 GT3 (line + color, 4 views)

Repo: doublehidenblade/tokyo-drift-3d (environment: tokyo-drift-3d)
Task file: godot/docs/tasks/td-138.md
Research (STAGE 1 — DONE, reuse it, do not redo): godot/docs/research/td-138-round2-research.md
Reference photos (CC BY-SA 4.0, evidence only, excluded from runtime exports): see godot/qa/td-138/reference_sources.txt for the two redistributable multi-angle photographs and their license URLs. Attribute per that file.

## Context: why stages now
Round 3 was the last single-worker attempt at the hero car. The worker honestly
self-rejected its iteration 01 (it did not read as the photographed M4 GT3) and
then finished without producing iteration 02 — one session cannot carry this
build. Craig's fallback: decompose into dependent staged sessions, each gated on
supervisor inspection before the next dispatches. This is STAGE 2. Stage 1
(research) is complete and committed — reuse it.

## Your deliverable (this stage ONLY — no Blender, no 3D)
1. Four 2D mocks, line AND color: SIDE, FRONT, REAR, THREE-QUARTER views of the
   BMW M4 GT3, drawn from the real reference photos at real proportions.
2. A per-part dimension spec sheet (markdown): every major part with its
   dimensions, surfacing notes, and connection points — the document the Blender
   stages will build from.

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks. Local
checks only.

## 1. Skill workflow injection (MANDATORY)
- Skill: 3dviz-pro-max — Visual-iteration workflow (2D stage adaptation).
- Process: real reference photo → 2D mock drawn AT the photo's measured
  proportions → side-by-side photo-vs-mock comparison pairs → iterate until the
  mock's silhouette, stance, and part placement match the photo.
- The dimension sheet is the source of truth both stages use: if the mock and
  the sheet disagree, fix one of them and say which.

## 2. Quality bar (MANDATORY)
- Envelope (from the research doc — BMW M Motorsport published data): 5.020 m
  long (splitter/wing), 2.040 m wide, 1.310 m high, 2.917 m wheelbase, 1.700 m
  track. Every mock view is drawn to these numbers — measure, don't eyeball.
- Every major part placed at its real position and size: front splitter,
  canards, vented hood, fender flares, swan-neck wing mounts + rear wing,
  rear diffuser, headlights, taillights, kidney grilles + intakes, mirrors,
  wheels/brakes (12.5/13x18-inch GT3 package).
- The mocks must read as the PHOTOGRAPHED M4 GT3 — sharp GT3 aero, not a
  generic race car. Round-3 iteration 01 failed exactly here: proportions soft,
  didn't read as the sharp GT3 reference. Name what you changed vs that
  failure in your summary.
- Judged against: the CC BY-SA reference photos in reference_sources.txt.

## 3. Excluded degenerate shortcuts (MANDATORY)
- A traced outline with no proportional verification is NOT a submission — every
  view must be dimension-checked against the 5.020/2.040/1.310/2.917/1.700 sheet.
- AI-image-generator output passed off as drafted mock is NOT acceptable (Craig's
  standing rule: never pass generated art off as designer-drawn). Construct the
  mocks from the dimension sheet; label every comparison pair honestly
  (real photo vs 2D mock).
- One, two, or three views is not four views. All four + the spec sheet, or the
  stage is not done.

## 4. Effort calibration (MANDATORY)
Careful measured 2D drafting — hours of proportion work, not a quick sketch.
This is the foundation every Blender stage builds on; sloppy mocks here mean a
sloppy car later. If it takes a full session, that is expected.

## 5. Evidence (MANDATORY)
Commit under godot/qa/td-138/:
- mock-side.png, mock-front.png, mock-rear.png, mock-three-quarter.png
  (each paired against its reference photo in the same comparison)
- mock-dimension-spec.md (per-part dimensions, surfacing notes, connection points)
- Record EVERY path in the td-138.md task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- Push to branch td-138-stage2-mocks and LEAVE THE PR OPEN. DO NOT MERGE.
- DO NOT MERGE the old PR #253 (td-138-round3) — it holds only rejected
  negative evidence and is flagged do-not-ship.
- DO NOT set done-pending-verdict — that follows independent supervisor
  inspection only.
- A supervisor inspects the mocks against the reference photos before STAGE 3
  (modeling spec) is dispatched. Nothing proceeds on self-certification.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Board status table is source of truth; update ONLY your own row, via PR.
- Reference photos are CC BY-SA 4.0: attribute per reference_sources.txt,
  evidence only, never in runtime exports. No purchased packs without Craig's
  approval; no commercial-game assets ever.
