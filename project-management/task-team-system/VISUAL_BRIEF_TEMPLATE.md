# Visual-task worker brief — MANDATORY template (Craig 2026-10-01)

Use this template for EVERY visual/art dispatch (3D models, renders, UI, art).
Fill every section. A brief that skips a section does not get dispatched.
This exists because the td-138 round-2 brief had no skill workflow, no quality
bar, and no excluded shortcuts — the worker shipped a 14-minute box-model and
self-certified it. (See AGENTS.md "Visual-task dispatch rule".)

## 0. Cost rules (always)
NEVER touch GitHub Actions: no `gh workflow run`, no re-runs, no clicks.
Local checks only. (Craig 2026-09-27)

## 1. Skill workflow injection (MANDATORY — name the skill and its process)
The worker MUST follow this process, not just deliver the outcome:
- Skill: 3dviz-pro-max — Visual-iteration workflow
- Process: real reference photo → 2D mock → 3D render at matching angles →
  side-by-side triptych → iterate until the 3D reads as real against the photo.
- (For UI/art tasks: name the equivalent skill workflow here instead.)

## 2. Quality bar (MANDATORY — what "good" looks like, concretely)
Describe the bar in terms a renderer can check against the reference:
- Proportions/surfacing/detail expectations, named per part.
- What the current/rejected version got wrong, specifically.
- The reference files (paths) the work will be judged against.

## 3. Excluded degenerate shortcuts (MANDATORY — name them)
Explicitly unacceptable, e.g.:
- A script-generated placeholder/low-poly stand-in is NOT a submission.
- A video-game screenshot is NEVER a "real photo" reference; every triptych
  panel must be honestly labeled (real photo vs 2D mock vs 3D render).
- Checkbox completion (files committed, tri counts) without visual quality
  does not count as done.

## 4. Effort calibration (MANDATORY)
State the expected order of effort (e.g. "serious multi-hour Blender modeling,
not a quick script"). If a genuine build takes a day, say so.

This is production/workflow effort, separate from model reasoning effort.
For reference-critical 3D work use frontier high/max with
`wait_for_required_tier`; locked-mock implementation may use the bounded
fallback in the policy. Fill the setup record below before dispatch.

## Recommended setup (MANDATORY per task and brief)

Read [WORKER_SELECTION_POLICY.md](https://github.com/doublehidenblade/game-dev-central/blob/main/project-management/rules/WORKER_SELECTION_POLICY.md).
Copy this completed block into the task record as `recommended_setup` (or the
equivalent Markdown section). It is a recommendation and preflight check, not
permission to replace an active owner or change dispatch automatically.

- Capability tier and reason: [frontier / balanced / efficient; coupling, risk, ambiguity]
- Provider preference: [provider-neutral, or provider + concrete task/tool reason]
- Requested model and effort: [exact available model ID; supported effort/thinking setting]
- Environment and required tools: [verified executor, repo, Blender/Godot/browser/pixel inspection as needed]
- Availability checked: [UTC time + account/catalog source; available / unverified / quota-blocked]
- Fallback: [wait_for_required_tier OR bounded_attempt_then_escalate; allowed alternative]
- Attempt budget: [one initial attempt + at most one evidence-based correction; time/usage ceiling]
- Escalation criteria: [failed checks, structural mismatch, missing tools, quota ceiling; named stronger setup]
- Verification budget: [named local checks, evidence coverage, independent reviewer setup, reserved time/usage]
- Requested versus confirmed setup: [request; observed model/effort + evidence, or unconfirmed]
- Actual outcome: [accepted/rejected/pending; total usage/cost when known; review/rework time]

Do not silently downgrade, infer runtime identity from the requested setting,
or treat extra reasoning as a replacement for tools and verification.

## 5. Evidence (MANDATORY)
- Triptychs/wireframes/statistics paths under the task's QA folder.
- Every path recorded in the task file's evidence list.

## 6. Merge and status (MANDATORY — no exceptions)
- When done: push to the branch and LEAVE THE PR OPEN. DO NOT MERGE.
- DO NOT set done-pending-verdict — that follows independent inspection only.
- A supervisor inspects the renders against the references before anything merges.
- Merging unverified work gets reverted.

## 7. Standing constraints
- Token discipline: same approach failing twice identically → stop, log it.
- Status table is source of truth; board updates via PR only, own row only.
- Environment: Blender is REQUIRED for 3D modeling work. Check for it first
  (`blender --version`); if missing, install it yourself before starting —
  portable tarball from https://download.blender.org/release/ (no root
  needed; on this project's worker VM: ~/workspace/tools/blender-5.2.0-linux-x64/blender).
  Headless: `blender --background --python script.py`. Never start modeling
  without a working Blender and never claim "Blender unavailable" without
  trying the install.
- Royalty-free assets only, licenses verified (CC0/CC-BY); no purchased packs
  without Craig's approval; no commercial-game assets ever.
- Materials/textures — realistic PBR, never flat single-color surfaces.
  Approved texture sources, NO keys or accounts needed (direct download):
  Poly Haven (https://polyhaven.org, CC0) and ambientCG
  (https://ambientcg.com, CC0). Sketchfab is whole PARTS ONLY, never
  textures (UVs won't transfer, per-model licensing murky, rip risk), with
  per-model CC0/CC-BY verified — and downloads need Craig's logged-in
  account. Never reuse baked AI-generated textures; strip all real-world
  branding; 100% opaque.
