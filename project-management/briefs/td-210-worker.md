# td-210 same-environment worker brief

FIRST read `/workspace/game-dev-central/project-management/task-team-system/SYSTEM.md`, then the current `project-management/rules/WORKER_SELECTION_POLICY.md`, `knowledge/standing-rules.md`, applicable role brief, checkout AGENTS/README required readings, and `/workspace/tokyo-drift-3d/godot/docs/tasks/td-210.md`. User instructions override older merge, Actions, publication, blueprint-stop and branch-base rules. The canonical task supplies six measurable criteria, exact source pins, requested setup and exclusions.

## Recommended setup

```json
{
  "capability_tier": "frontier: district-scale 3D composition, resource sharing, memory/startup attribution and visual preservation",
  "provider_preference": "OpenAI per Craig’s selected GPT-6 Astra High instruction",
  "requested_model": "gpt-6-astra",
  "requested_effort": "high",
  "environment_and_tools": "Existing Game-development /workspace only; Godot 4.7.2 ed1daf0bf, Blender4.3.2, Node24.19.0, retained native/browser harness and Xorg :99. No new cloud task or environment.",
  "availability_checked": "2026-10-08T01:36:49.095589+00:00; model-selecting catalog supports Astra/high; same-environment `/root/kamome_worker` dispatch accepted gpt-6-astra/high.",
  "fallback": "wait_for_required_tier; stop and report if this existing environment becomes unavailable; no switch, duplicate task or silent downgrade",
  "attempt_budget": "One coherent bounded district implementation plus evidence-based correction where needed; stop after two identical failures until a changed hypothesis is recorded. No invented billing limit.",
  "escalation_criteria": "Existing Kamome ownership, unavailable required environment/tier, necessary road/city-data/protected-owner changes, invalid reference inputs or unexplained coverage/performance regression.",
  "verification_budget": "Reserve before/after all345-lot native pairs, actual native/browser street/HUD views, baseline/prototype/full profiling, coverage/clearance/variation/material/resource checks, regressions, shipping export audit/entry, and a fresh independent Astra/high reviewer plus justified correction.",
  "requested_versus_confirmed": "Requested Astra/high in the existing environment; model-selecting collaboration call accepted exactly gpt-6-astra/high. Runtime internals unexposed.",
  "actual_outcome": "Admission preflight complete; implementation and independent review pending."
}
```

## Ownership and exclusions

- Sole implementation owner reserved: `/root/kamome_worker` in the existing environment. Root owns central coordination, admission, draft metadata and the later independent-review/public-QA handoff. No external cloud task is created.
- Branch `feat/td-210-kamome-live-buildings`, stacked on `feat/td-209-tenjin-live-buildings` at `0b2652bc86b6824444af277fdb34af5bdd981066`. Never push to or rewrite the Tenjin branch/PR489.
- Allowed: new Kamome module(s), minimal `lower_city_world.gd` hook, existing placement/batching interfaces with evidence-backed optional/shared resource improvements, scoped tests/capture/profile tooling, selective export inclusion, task/docs/evidence. Preserve Tenjin’s geometry/appearance and legacy backend behavior unless an equivalence-proven shared optimization is necessary.
- Excluded: authored GLBs/atlases/source asset scripts; other district design; HUD/controller/camera/traffic/pedestrians/taxi/AnimeLook; Fuel/economy; roads/city.json; global fog or visibility settings. Preserve gig destinations, sidewalks and collision access. Report any demonstrated need to cross these boundaries before editing them. No Muse/Claude contact.
- Reuse CityDressing.frontage and CityKitBatch/CityBatch conventions; world coordinate Godot(x,height,-plan_y), seed185. Kamome hall24×16×7.7m; source metre-scale bays, clipping/wing composition, never whole-model footprint stretch. Buildings<15ktris including ink; texture/prop contracts from td-186.
- Prior Tenjin costs:930→3866ms construction,133.0→294.6MB retained static; shippingPCK108704384B. Profile actual present causes and preserve art. Parent owns publishing route.
- Explicit user instruction supersedes older branch-from-main, blueprint-stop, CI, merge and public-main publishing rules: existing authored city layout and approved district integration are authorized; preserve that layout. Private-playtest CI waiver only. No Actions, merge, deployment or environment switch.

## Remaining approved whole-city scope

Issue491 remains open. Completing Kamome does not complete Chidori, Kotobuki, Daikoku, Shinkai, North Rail Depots, bespoke T2/PaperExchange or all asset integration. Phone acceptance and publishing readiness are separate gates.

## Execution and handoff

Use the existing Game-development /workspace only, explicitly requested gpt-6-astra/high. No new external cloud task/environment, no further subagents, no PR489 edits, no main edit/merge, Actions or deployment. A new same-environment implementation worker is the task-team role, not a cloud task launch. Root owns coordination and later reviewer/public-QA handoff.

Read original Kamome meshes and `godot/assets/td-186/{ASSET_INDEX.md,CONVENTIONS.md,source/bld_kamome.py,source/bld_storefronts.py,source/bld_props.py,source/td186lib}` as applicable, plus source-kit triptychs. Open the pinned references under `godot/qa/td-210/references` yourself before production. Record a measured build sheet using original footprints and CityDressing.frontage. The user approved this district integration into the existing authored layout; no extra permission is required for routine composition. Preserve source assets and seed185.

Before scaling, collect an unchanged reviewed-base profile, identify allocation/build stages and repeated geometry/material costs, implement and compare a bounded prototype sharing reusable meshes/materials, and demonstrate equivalent intended geometry/materials with measured duplication reduction. Then expand to345. Record and send root the profile checkpoint before scaling; do not wait for another permission when the evidence supports an in-scope choice. No global fog/range changes or required-art cuts. No citywide uncullable MultiMesh. Preserve Tenjin appearance and source shape; any necessary shared-backend change must prove no other-district regression and stay on the new branch.

Adapt proven td-209 capture/export/reproduction tools into td-210, use seed185, and capture all345 same-camera native lot pairs plus actual main/side-street native/browser views with ordinary HUD and HUD-hidden states separately. Actual shipping menu/input entry is separate from QA entry. Any MultiMesh test must inspect expanded geometry, materials, bounds and clearances, not merely count instances. Meaningful negative controls must fail for missing lots, footprint overflow, invisible opening walls and doubled ink. Inspect every final sheet and appropriate original detail. Preserve raw failures and label superseded runs.

Use official checkout `.tools/Godot_v4.7.2-stable_linux.x86_64`, never system Godot4.6.3. Source `/workspace/.setup/activate.sh`; verify retained Xorg DISPLAY=:99 and browser/Playwright. Root verified Godot4.7.2 ed1daf0bf, Blender4.3.2 and Node24.19.0. Byte-identical importer parity and native mipmap provenance are required; td-209 tools document the prior missing-PNG/mipmap errors. Do not repeat those or broad-clean the shared checkout. Network calls may require exec `sandbox_permissions:with_additional_permissions` plus network enabled; that succeeds for authorized GitHub reads. Never print credentials. If this EXISTING environment becomes unavailable, stop and report; do not switch or start another.

Commit buildable source and evidence/docs checkpoints with [skip ci], pull --rebase before every push to your new branch only, and maintain its draft PR. Stage only owned paths; inherited generated import outputs are untracked and must be preserved. Root maintains central records and reserves a fresh independent Astra/high reviewer. Write a heartbeat about every10 minutes to `/workspace/game-dev-central/project-management/watchdog/state/worker-heartbeats/td-210.json` without committing the heartbeat.

When complete, freeze runtime/evidence, set task in_review with verdict null, and update TODO/DEVLOG/CHECKPOINT/new PR. Do not self-accept or touch Tenjin PR489. Report exact commits, source/mesh provenance, performance/export deltas, all failures, publishing needs and whole-city/phone limits. No Muse/Claude contact.

Draft implementation [PR494](https://github.com/doublehidenblade/tokyo-drift-3d/pull/494); coordination [PR350](https://github.com/doublehidenblade/game-dev-central/pull/350). Initial game intake commit6e510fb1c95dbaeecf7c1f8f675d608f4c977ae3 contains no runtime changes. Same-environment Astra/high worker dispatch accepted 2026-10-08T01:40:58.841822+00:00; no external cloud task API or environment launch was used.
