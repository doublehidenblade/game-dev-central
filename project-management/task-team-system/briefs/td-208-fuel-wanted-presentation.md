# td-208 worker brief: Fuel/Wanted presentation

> Prepared 2026-10-07 by dot coordination. Read SYSTEM first. Planning-ready, runtime not admitted.

## Task and authority

Implement only [td-208](https://github.com/doublehidenblade/tokyo-drift-3d/blob/212e28b096d2b7d024cc47c4b3bcaddd543c74e1/godot/docs/tasks/td-208.md), filed in [Tokyo draft PR479](https://github.com/doublehidenblade/tokyo-drift-3d/pull/479). The canonical JSON contains all six required criteria and source pins. Re-read its latest revision before launch. This is one bounded slice of [the existing merged HUD design](../../../game-design/hud-discovery-mvp.md) and [existing execution plan](hud-discovery-mvp.md), not a parallel feature queue.

Read [SYSTEM](../../rules/SYSTEM.md), [WORKER_BRIEF](../../rules/WORKER_BRIEF.md), [worker-selection policy](../../rules/WORKER_SELECTION_POLICY.md), [standing rules](../../../knowledge/standing-rules.md), [brief snippet](../../../knowledge/brief-snippet.md), the game AGENTS/README/CHECKPOINT and QA index. Check checkout .agents/skills for relevant skills. Craig's latest background-free driving-HUD instruction is the explicit exception to the older opaque HUD rule; it does not change world materials.

## Exclusive implementation boundary

- Owner: GPT Dots. No confirmed assigned runtime/session. Keep task open until admission.
- Allowed: FuelHud and WantedHud presentation, exclusively owned UI resources, their focused tests and td-208 QA/docs.
- Preserve FuelService balance/range/payment/recovery and wanted/police/arrest signal authority. No wallet, payout formula, extra debit or settlement writer.
- Preserve Muse map/minimap/gig/health/controls, shared input and global scene assembly. Do not edit GigDispatch, GameConfig, GigMenu, GigHud, DamageBar, lower_city.tscn or Claude assets.
- Remove only Fuel/Wanted normal-driving backgrounds, adopt compact desktop type and bold green authoritative cash, and replace stars with a faithful original rendering of the supplied police symbol. Paid service sheets remain functional; this is not a blanket deletion of modal surfaces.
- Reuse existing reserved rectangles/yield behavior. Global placement and controls/input-mode changes require their existing owner contract. No duplicate HUD manager or heuristic relocation of other owners.
- Existing minimap/GAS release and DamageBar renderer defects remain separately reported. Natural chassis-wreck production and physical-phone acceptance are also outside this slice. Never call the combined build green while those gates remain.

## References and transfer gate

The four corrected version-2 boards were delivered to Craig at approximately 16:24 UTC. For this slice use 01-quiet-drive.png and 04-pressure-states.png plus the actual supplied user-police-symbol.png. Exact board hashes are recorded in the canonical task. The coordinator supplies confirmed Library identities at launch through the supported consumer-local materialization route; public PNG publication is not claimed by this text brief.

The consuming executor must materialize each reference locally, verify the readable bytes and board hashes, and open actual full-resolution pixels before image-dependent work. A parent-local path is not a transfer guarantee. If transfer fails, report the exact blocker and continue only read-only source preflight. Never reconstruct the police symbol from prose or generated rays.

Mock limitations matter: reconstructed scenery and Japanese lettering are not game assets; minimap topology is illustrative. Generated hero-size emblem rays differ from the original. Collage viewport proportions and targets are not measured proof; actual 1280x720, 1920x1080, 844x390 and 390x844 frames are required. Quiet/warning boards control small desktop type, not the larger discovery/receipt board lettering.

## Required recommended setup

```json
{
  "capability_tier": "frontier: responsive multi-owner presentation with existing input and money invariants",
  "provider_preference": "OpenAI route for existing dot-owned sources; preserve Muse/Claude ownership",
  "requested_model": "gpt-6-astra",
  "requested_effort": "high",
  "independent_reviewer": "Separate gpt-6-astra max acceptance audit; never the implementation author",
  "environment": "Existing authorized Tokyo Game saved environment; exact current catalog/runtime not verified",
  "required_tools": [
    "Godot 4.7.2",
    "Actual Lower City with pinned sources",
    "Native and browser renders",
    "Keyboard and multi-touch test harness",
    "Full-resolution reference/pixel inspection"
  ],
  "availability_checked": "2026-10-07 16:30 UTC: coordinator reports environment-list service failure. No task runtime admitted; model, effort, tools and quota unconfirmed.",
  "fallback": "wait_for_required_tier",
  "attempt_budget": "One coherent production attempt plus at most one correction justified by new evidence. Before launch, dispatcher must record a verified session/time/usage ceiling and reserve the separate review budget; missing ceiling blocks production.",
  "escalation_criteria": [
    "Required model, tools or references unavailable",
    "Cross-owner source or global placement change needed",
    "Money/police/input semantics change",
    "Failed correction or repeated unchanged failure"
  ],
  "verification_budget": "Reserve all six criterion matrices, before/after capture inspection and a separate frontier-max audit before admission. No downgraded rubber-stamp review.",
  "requested_vs_confirmed": "Astra high requested for future implementation and Astra max for future reviewer; no runtime identity attested.",
  "actual_outcome": "Planning only; implementation and acceptance pending; cost unknown."
}
```

## Admission and next action

Recheck current main and PR446/457 heads, existing worker state, open task/branch equivalents and the central reservation. Do not duplicate a live task or infer liveness from the historical registry. Confirm required tier/effort, Godot 4.7.2, real native/browser capture and input tools, reference pixels and concrete usage/session ceiling before production. Reserve independent Astra-max review budget. If any required capability is unavailable, use wait_for_required_tier rather than downgrade.

Current observed pins: main 9d4a88490c41f86e8d34e1c2c6f142838de20c73; PR446 64ccf666847499c076edaffcebf2ca303f462a8f; PR457 827e058c6e11e8bb923b9fefa7471227bae59a40. Their runtime/evidence is not this task's acceptance. A new implementation branch must be coordinator-recorded and safe against current owner edits; do not push onto a live existing worker branch or merge dependencies to main merely for convenience.

Environment catalog access is currently failing for the coordinator. No runtime launch was attempted in this pass and no user decision is needed merely to restate the approved design. The dispatcher owns service recovery and worker admission. No Actions dispatch/rerun/workflow edits, merge, auto-merge, deployment or other-agent contact is authorized for this worker.

## Evidence and handoff

Use the canonical six-criterion matrix. Every visual criterion needs same-defect/same-camera before/after files under godot/qa/td-208, with viewport/state suffixes where needed, plus inspected full-resolution pixels. Test bright/dark scenes, 0–3 wanted levels, paid recovery invariants, modal/arrest permutations, interrupted/repeated flows and multi-touch. Preserve all raw errors and failed attempts. Record exact head and each check as passed, failed or not run. Required aggregate checks cannot be replaced by a focused pass.

Worker sets in_review only after completing its scope and writing evidence/work log; verdict stays null. Separate reviewer uses per-criterion evidence citations. Phone/device and deployment gates remain distinct. Return branch/PR/full SHA, source pins, exact test results, inspected images, remaining blockers and next action; do not self-validate or describe the feature as live.
