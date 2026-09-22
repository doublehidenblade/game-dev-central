# Research: AI-assisted forest pipeline — skills from the Polish brothers' Godot project

> Researched: 2026-09-22 by coordinator agent
> Source: [`transcripts/polish-brothers-ai-godot-forest.md`](../transcripts/polish-brothers-ai-godot-forest.md) — translated transcript of the Polish brothers' AI-built Godot survival game video. All numbers below are from the video (unverified against the original Polish/English audio — treat as reported).

## Skill 1 — Research the real reference before generating anything

- **What:** Have the AI research what actually grows in the target region first, then a human picks the final species list (spruce, beech, birch, hazel).
- **Why:** AI-generated vegetation defaults to generic; the reference list anchors it.
- **Apply to Craig's projects:** for NEON DRIFT roadside greenery and any Tokyo Drift 3D district, start vegetation work with a species list for the biome, not with prompts.

## Skill 2 — Blender model → check → improve loop

- **What:** AI runs an automated cycle in Blender: generate the model, inspect it, improve it, repeat — a full tree/bush set in a few hours.
- **Why:** Replaces days of manual iteration; the check step is the loop's quality gate.
- **Apply:** any repeated prop or vegetation family where volume matters more than a single hero asset.

## Skill 3 — Style-direction pass on a small set before scaling

- **What:** The first generation was "too realistic, too generic" — no mysterious stillness. They re-ran reference images toward a stylized direction, tested on 3 trees, confirmed the style held, then expanded to 5 species.
- **Why:** Scaling up before the style is locked multiplies rework.
- **Apply (Tokyo Drift 3D):** directly relevant to the pseudo-3D districts — lock the stylized visual direction on 3 assets, confirm with screenshots, then scale. Never mass-produce before the style test passes.

## Skill 4 — Trunk skeleton + baked leaf textures on crossed planes

- **What:** Keep trunks and main branches as real 3D geometry; bake dense foliage into textured maps with bump lighting and put them on simple crossed planes. Birch: 34,528 → 2,812 triangles (~12× reduction).
- **Why:** Foliage is the polygon hog; crossed planes read as full canopies at game distances.
- **Apply (Tokyo Drift 3D):** the hedge/tree clusters in td012-06 are the obvious first candidates for a baked-leaf crossed-plane pass if poly counts balloon.

## Skill 5 — Procedural roads: layers, not scans

- **What:** Dirt road fully code-generated (no photogrammetry): base path → wheel ruts → dirt-surface material detail → scattered gravel.
- **Why:** Layering cheap procedural detail beats expensive scanned assets at speed.
- **Apply (NEON DRIFT):** the terrain-texture work in todo120/121 — procedural layering (ruts, edge wear, gravel) over flat scans.

## Skill 6 — Grass as textured crossed planes, not instanced 3D blades

- **What:** Mass-instanced 3D grass blades looked like "a layer of plastic brushes floating above the surface" — they never merged with the ground. Hand-drawn blade textures on a few crossed planes (12 triangles per tuft, layering from texture) finally read as weeds growing from soil.
- **Why:** Silhouette and lighting consistency with the ground matter more than blade count.
- **Apply:** the standard technique for any ground cover in both games. Instancing more geometry is not the fix when it looks wrong — change the representation.

## Skill 7 — AI-batched micro-props for ground richness

- **What:** Mushrooms, dead stumps, fallen logs, rocks generated in batches by the AI; dressing the ground with them immediately enriched the wilderness feel.
- **Why:** Cheap detail density; the small stuff sells the biome.
- **Apply (Tokyo Drift 3D):** district ground dressing; (NEON DRIFT): roadside clutter where gaps in vegetation show empty ground.

## Skill 8 — Lighting perf trap: measure every slider

- **What:** A shadow-softness slider took the game from ~110 fps to 42 fps — over half the performance gone from one setting; restored to 105 fps when pulled back.
- **Why:** Lighting settings are the classic silent perf killer; frame rate must be measured before and after every lighting change.
- **Apply:** both games — every lighting/shadow change ships with an fps before/after number. This belongs in the workflow CI section (see `workflow/game-dev-workflow.md`).

## Skill 9 — Real DEM + OSM vectors, layers separated

- **What:** 801×801 elevation points (2.6 MB) from Poland's national geo-portal + road/stream vectors from OpenStreetMap; roads, margin layer and original survey base stored separately so roads can be built without destroying real terrain. Imported area: 8×8 km.
- **Why:** Real elevation beats hand-sculpted for exploration; separation keeps the source data intact.
- **Apply (Tokyo Drift 3D):** relevant to any future district built on real terrain (e.g. mountain stretches) — source DEM, vectors, and built layers stay separate.

## Skill 10 — The meta-skill: AI in the pipeline, judgment on top

- **What:** "AI can't replace humans, but it gave two people the ability to build a mountain forest. What decides demo→Steam is every trade-off between performance, style and reality."
- **Why:** AI multiplies output; the developer's eye is the scarce resource — consistent with Craig's rule that his phone is the final judge.
- **Apply:** embed AI in the loop (generate → check → improve), keep human verification (screenshot review, phone check) as the gate.
