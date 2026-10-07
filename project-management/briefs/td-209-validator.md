# td-209 independent validator brief — reserved, not yet dispatched

FIRST read [task-team SYSTEM](../task-team-system/SYSTEM.md) and [worker selection policy](../rules/WORKER_SELECTION_POLICY.md). Judge the canonical [td-209 contract](https://github.com/doublehidenblade/tokyo-drift-3d/blob/feat/td-209-tenjin-live-buildings/godot/docs/tasks/td-209.md) and its listed evidence at the final source/evidence pins supplied on dispatch. Draft [implementation PR489](https://github.com/doublehidenblade/tokyo-drift-3d/pull/489) targets integration PR488. Do not review a moving working tree.

Implementation source is frozen at `847270a40257c83cdcab364c52631e386218c3a2`; final evidence pin is still pending. Base runtime is `2227f71e784f581d11ace8f90e7201fbb59b1f63` / `8e7caeb1209c0d47dfea3ac57308e693a00b3983`; baseline QA tooling checkpoint is `ad4f24229a7ba80e25e3d4ddc1e83a33f3db0c47`. Initial before captures predate complete td-119 importer recovery and are being relabeled/replaced from the restored isolated baseline. Review the final restored pairs and their resource hashes, not the retained preliminary attempts. Current matching local ordinary exports are 92196912→98201888 bytes; do not equate that base with the supplied 102777824-byte playtest artifact without an artifact comparison.

Final importer correction (23:31 UTC): the earlier 92/98 MB pair lacked original 3D mipmap settings and is **superseded**. `native-import-provenance.json` verifies all 666 generated outputs from 29 unchanged GLBs match between base and implementation after editor scans. Correct ordinary exports are `build/td209-base-native-import/index.pck` (102777856 bytes) and `build/td209-final-native-import/index.pck` (108704304 bytes), +5926448 bytes; the final pack exceeds 100 MiB by 3846704 bytes. Base is only 32 bytes above the supplied playtest artifact. Final native/browser evidence is now being captured with this corrected import state. Verify that the final report uses these artifacts and keeps earlier attempts clearly labeled.

## Recommended setup

- Capability tier/reason: frontier; independent audit of coupled 3D geometry, visual coverage, collision and export behavior.
- Provider preference: OpenAI per Craig's explicit request and this environment's Godot/Blender/browser tools.
- Requested model/effort: `gpt-6-astra` / `max`.
- Environment/tools: selected Game-development `/workspace`; official Godot4.7.2 ed1daf0bf, Blender4.3.2, Chromium151.0.7922.173, Playwright1.62.1, actual Node24.19.0. Native Xorg dummy `DISPLAY=:99` and Mesa llvmpipe; browser SwiftShader. Source `/workspace/.setup/activate.sh`; use checkout Godot, never system4.6.3.
- Availability: model-selecting collaboration catalog exposes Astra/max; reviewer not yet dispatched. At dispatch record accepted selection and any unexposed runtime identity honestly.
- Fallback: `wait_for_required_tier`; no weak replacement or silent downgrade.
- Attempt budget: full independent inspection of every criterion plus one correction review tied to new evidence; second rejection or repeated unchanged failure is an escalation. No invented usage/cost ceiling or billing estimate.
- Escalation: missing images, unverifiable pins, uncovered near-road lots, geometry/collision/packing regressions, author ownership overlap, missing required tier/tool.
- Verification budget: reserve original images/contact sheets, source diff, local focused checks and matched base/final regressions, actual export/browser inspection and a corrective pass before closing the task.
- Requested versus confirmed: requested above; pending dispatch, runtime internals not attested.
- Outcome: pending. No current review/acceptance claim.

## Review contract

Review only; do not fix the implementation. Open the source/evidence yourself. For each of the five task criteria return PASS/FAIL with exact citations. Distinguish final acceptance evidence from explicitly retained failed smoke/capture attempts; a failed attempt is not a final frame, nor may it be hidden. Author-reported counts alone are not evidence.

1. Check the manifest against all 77 source lot indices. Every claimed completed frontage needs a matched pair covering that instance; inspect the full coverage sheets and original detail wherever needed. Ensure the street-facing and exposed side walls are architecture rather than blank shells behind isolated props. Judge declared simple/distant exceptions against the actual road relationship.
2. Compare actual native/browser streets and the pinned warm Showa artbook. Assess believable floor/bay scale, variation, roofs/corners, physically mounted Japanese signs, open warm retail, district skyline and 30m detail/100m silhouette. Ordinary HUD and matched HUD-hidden views are separate records. Diagnostic lot surveys must not masquerade as driving views; a QA capture entry must not replace proof that the actual game export opens.
3. Check protected-source hashes, lot/road data, drive geometry, Fuel's two stations/44 instances and gig/sidewalk/road clearances. New recessed lobby entries need visible-matching simple proxies: no old invisible footprint wall across the arcade. Inspect meaningful negative controls and the unchanged route/ramp/sign/drive checks.
4. Inspect batching bounds/material sharing/culling ranges, triangle/texture budgets, baked ink and no added per-window lights. Audit the actual PCK and Fuel JSON/Shuto exclusions. Report increased bytes or inherited runtime errors accurately; do not demand unrelated owner fixes or remove required art to meet the temporary 100MiB hosting route.
5. Verify reproducibility, exact source/evidence pins, raw logs and failures, draft target, preserved scope and still-open district/asset backlog. No whole-city completion claim.

Craig's explicit limits override older generic merge/mirror rules: **no main edit, merge, Actions or deployment**, no contact with Muse/Claude, no repair of their owned files. Record the independent verdict for the parent; it is not Craig's final phone verdict and does not authorize publication. Root owns coordination and any QA-only public evidence branch.
