# Game-dev workflow (centralized source of truth)

> Created: 2026-09-22 by coordinator agent
> Extracted from `doublehidenblade/neon-drift` and `doublehidenblade/tokyo-drift-3d`
> (read-only API extraction 2026-09-22). Game-specific details stay in the game
> repos; this file holds the GENERIC workflow every agent session must follow.
> If a game repo's local workflow notes conflict with this file, this file wins
> and the repo's copy should be marked stale.

## 1. Pre-work checklist (before any implementation)

1. Read this file, the game repo's README, its AGENTS.md/CLAUDE.md if present, the
   dev log (newest first), current checkpoint, lessons file, and the task file.
   Never depend on chat history or a previous machine for context.
2. Bootstrap and verify the runtime environment first (install documented
   dev/verification tools, run pinned bootstrap scripts, record tool versions
   and failures in the dev log).
3. **Intake first:** the moment a prompt raises an ask, bug, feature, or
   reference image — save it in the repo's task/todo structure with acceptance
   criteria and status, and commit/push that record on its own if the fix will
   take a while. Never leave the only copy of a request in a disposable
   container or chat.
4. Work on a branch from updated `main`, never directly on `main`. Reuse the
   existing branch when resuming its unfinished work.
5. Log before long steps: before downloads, exports, CI waits, or big asset
   generation, append a dated dev-log entry saying what you are about to do and
   why, and push it — so a session that dies mid-execution leaves a trail.
6. Asset-license check: never introduce assets with unclear commercial rights;
   reference images are mood/composition reference only, never shipped in builds.
7. Layout work starts with a design artifact (e.g. a 2D top-down blueprint with
   labeled footprints at real scale), self-checked before any 3D build.

## 2. Post-work checklist (after every task and CI run)

1. Commit small, coherent, buildable changes frequently; commit and push after
   every completed task and every CI run (pass or fail) before moving on.
2. Update the TODO, dev log, and PR body/checklist at each meaningful
   checkpoint — record unfinished work and evidence before stopping.
3. At each checkpoint update devlog + task file + TODO + lessons; add a lesson
   entry whenever a mistake teaches something durable.
4. Record evidence links, exact commit SHAs, and CI run IDs in the task file
   and dev log; never claim an image or run was reviewed unless it was.
5. Never delete or rewrite another agent's research/notes without discussion —
   add a dated correction note pointing to the new file instead.

## 3. QA expectations

1. **Deterministic harness:** tests run against a seeded, reproducible harness
   (fixed seeds, frozen state, query-param controlled), with test hooks
   unavailable in normal play.
2. **Real-input gameplay checks:** drive the game with actual input events
   (steer/drift/nitro/restart, pause/resume), not scripted fakes.
3. **Golden screenshots** at representative checkpoints with pixel-diff
   thresholds; missing or changed baselines fail.
4. **Non-blank frame checks** (numeric "lit pixel" ratio), finite/valid draw
   coordinates, render-queue/workload caps.
5. **Class-level continuity assertions:** sweep authored transition boundaries
   in fine increments and assert no abrupt discontinuity beyond a threshold.
6. **Performance budgets:** frame/render p95 and long-frame fractions recorded
   per zone; exact run-by-run numbers in the dev log.
7. **Negative tests:** prove gates can fail (a positive control passes, a
   negative control fails an unchanged numeric threshold).
8. **Never bypass failed gates, loosen thresholds, or regenerate baselines to
   get green.** New baselines require visual review first.
9. Engine/log errors fail the job even if the exit code is zero.

## 4. Screenshot / visual verification practices

1. **Before/after screenshots for every visual bug/feature**, same framing,
   stored in the task's `before/` and `after/` folders (or CI artifact) and
   linked from the task file.
2. **Personally open every image used as acceptance evidence** — full
   resolution for anomalies and milestones; reject black, empty, uniform,
   occluded, or obviously broken frames. Generate contact sheets for routine
   review, but open the full image when something looks wrong.
3. **Automated pixel checks cannot decide whether a scene looks artistically
   correct.** A green build or non-blank screenshot is NOT visual approval;
   the recorded manual review is the visual approval.
4. Never present an image you have not personally opened; never claim an image
   was shown when it was not.
5. Keep a table of user feedback → correction + evidence → still-open; do not
   claim an image was inspected anew unless personally opened in the current
   session.
6. Reference images are guidance only (composition/material) — never copy them
   as assets, never ship them.

## 5. Visual standards for new agent sessions (Craig's hard rules)

These are non-negotiable. They outrank any workflow convenience:

1. **Craig's phone is the final judge.** No visual fix is claimed done on test
   evidence, green CI, or generic screenshots alone — verify against his exact
   frames (frame-by-frame review of his recordings) and ship as "for him to
   check", never "fixed".
2. **Everything 100% opaque.** No fading or transparency tricks anywhere;
   geometry must be correct in perspective first, sprites are surface detail
   only, never a way to game around a bug.
3. **Fix bug classes globally, never per instance.** Classify each visual bug
   (projection, scale, anchoring, transition, occlusion, lifecycle, …), repair
   the shared invariant, and add deterministic CI exercising the class across
   representative assets/scenes and continuous boundary sweeps.
4. **Numeric CI assertions before baseline approval.** Every bug class ships
   with a numeric assertion that fails on the broken phone frames; an
   assertion that cannot fail on the evidence is not a guard.
5. **Honest limitations recorded:** what wasn't verified (physical device,
   other browsers) and what wasn't implemented (rather than faked) go into the
   task file/dev log. Experiments that fail visual review are removed, not
   retained as dishonest evidence.
6. **When green CI misses a shipped bug:** write a post-mortem first — quote
   what the assertion actually measured, explain why it passed while the bug
   was visible, and replace it with one that fails on the evidence frames
   (see neon-drift `todos/todo121/README.md`).

## 6. Branch / task / release conventions

1. Task intake: one task file per task, one evidence folder per feedback item
   with `before/` + `after/` (+ `reference/` for user-supplied images).
2. Todo checkboxes: `- [x] ~~completed item~~ — evidence/link` for done;
   `- [ ] planned item — exact next action` for unfinished.
3. Each session: intake → branch → draft PR (body/checklist maintained) →
   implementation → exact-head green CI → manual image review → merge → verify
   the live deployment (open the live URL, exercise the affected area, report
   the play link + PR + remaining limitations).
4. Merge only when the exact PR head is satisfactory and CI is green.
5. Release/publish: pin the reviewed candidate explicitly (run ID, full SHA);
   the publisher promotes the pinned artifact, never an arbitrary newer run.
   Store releases need separate explicit authorization.

## 7. Performance discipline

1. Measure frame rate before and after every lighting/shadow change; record
   exact before/after numbers (a single shadow setting once cost ~110 → 42
   fps in a reference project — see `research/ai-assisted-forest-pipeline-skills.md`
   skill 8).
2. Never describe software-renderer or host-throttled FPS as real-device
   performance; keep host-throttled failures out of budget decisions (do not
   loosen budgets because a shared runner was slow).
3. Optimize representation before adding geometry: e.g. baked textures on
   crossed planes over mass-instanced 3D detail (see the skills file).

---
*Local copies of this workflow in individual game repos may be stale — this
file is the source of truth.*
