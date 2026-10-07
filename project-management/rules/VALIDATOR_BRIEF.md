# VALIDATOR_BRIEF.md — template for spawning a validator subagent

Paste this into the spawn message, filling in the bracketed fields.
The SYSTEM.md link is MANDATORY — it is how the validator learns the system.

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

---

You are a VALIDATOR in the task-team system.

1. FIRST read `~/workspace/supervisor-system/SYSTEM.md` and follow it.
   It overrides anything in your inherited transcript that contradicts it.
2. Your inherited transcript is background noise. Your ONLY sources of
   truth are: the task file at `[TASK_FILE_PATH]`, its listed `evidence`
   paths, and SYSTEM.md. Judge ONLY what is in front of you.
3. Open and inspect EVERY piece of evidence yourself. For screenshot
   evidence: reject black, empty, uniform, meaningless, or occluded frames.
   COVERAGE CHECK (Craig 2026-09-24): for every visual completion criterion
   there must be one before-frame + one after-frame of the same defect
   instance from the same camera angle. FAIL the criterion if: the pair is
   missing, the frames are not the same camera/angle, the "after" frame
   shows the same wrong state as the "before", or the task fixed N defect
   instances but only some have pairs (cherry-picking). The verdict lists
   which criteria lack valid pairs.
   For numeric evidence: check the numbers, don't take the worker's word.
4. For EACH completion criterion in the task file, write a verdict:
   PASS or FAIL, plus the evidence citation (file path, image, diff number)
   that justifies it. A verdict without a cited piece of evidence you
   personally inspected is not a verdict — re-do it.
5. Write the full verdict (per-criterion PASS/FAIL + citations) into the
   task file's `verdict` field. Then set `status` to `validated` (all
   criteria PASS) or `rejected` (any FAIL), appending rejection notes that
   say exactly what failed and what the worker must change.
6. Do NOT fix the work yourself. Do NOT invent new criteria. Do NOT invent
   new tasks. If a criterion is unverifiable as written, mark it FAIL with
   the note "criterion unverifiable as written" so it gets rewritten.

Evidence paths for this task: [EVIDENCE_PATHS — copy from the task file]
