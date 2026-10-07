# Worker model and effort selection

> Researched: 2026-10-07 by game-dev coordination research
> Scope: recommendations for new tasks and briefs. No automatic worker changes.

## Verdict

For tightly coupled 3D game work, buy the strongest coherent first attempt you
can afford, then verify it. Craig's experience is a useful project-specific
signal: repeated cheap attempts can cost more once geometry, architecture and
assumptions need rebuilding. It is not evidence that every task benefits from
maximum effort or that any provider wins universally.

**Model capacity is more than general knowledge:** it includes reasoning,
coding, visual understanding, instruction-following and keeping constraints
consistent. **Effort is inference-time reasoning expenditure within that
model**, not an upgrade to a different capability tier. More effort can help a
capable model use its capacity; it does not supply missing tools, references,
context or competence. OpenAI documents separate model and effort choices;
Anthropic describes effort as a behavioral signal, not a strict token budget.
Supported settings and defaults differ by model and product. [1][2][3][4]

A strong first pass should preserve coherent decisions across the task.
“One shot” never waives running the game, inspecting pixels, regression tests,
reference comparison, independent review, or Craig's existing acceptance gates.

## Task matrix

These are project recommendations, not measured cross-provider benchmarks.
“Frontier” means the strongest suitable model actually available with the
required tools. Select an exact effort supported by that model at dispatch.

| Task type | Recommended setup | If quota/capacity is unavailable | Verification that must be budgeted |
| --- | --- | --- | --- |
| Hero vehicle/character assets, complex 3D proportions, topology, rigging, scene composition | Frontier + high/max; prefer max for expensive-to-rebuild, reference-critical assets | Wait for the required tier. Read-only reference/tool preparation is fine; no weaker production substitute | Working Blender; real reference/2D mock/matching render; actual pixel and topology inspection; independent strong reviewer |
| Driving physics, collision/projection invariants, economy balance, persistence/migrations, architecture | Frontier + high; max for deeply coupled or stubborn failures | Wait for the required tier; retain current owner | Reproduction, invariant/edge-case tests, regression coverage; balance simulations or save round-trips as applicable; independent frontier audit |
| Ambiguous debugging, repeated rejected fixes, cross-system refactors | Frontier + high/max, with fresh evidence and a changed hypothesis | Wait; do not buy a chain of weaker retries | Failure reproduction, class-level fix, tests that fail on the broken version, adjacent-system checks |
| Art direction, new UI language, visual hierarchy | Frontier + high for direction/reference selection | Wait if direction is not locked | Inspect rendered mock, exact viewport and visual comparisons; required design approval |
| UI implementation from a locked mock and established component system | Balanced + medium/high | One bounded lower-cost attempt only if layout and behavior checks are explicit; escalate on drift | Screenshot comparison, interactions, accessibility, responsive states; strong visual review |
| Bounded routine feature in stable architecture | Balanced + medium/high | Bounded efficient attempt if interfaces, scope and tests are fixed | Local focused + regression tests; escalate on interface or architectural changes |
| Mechanical edits, file moves, formatting, documentation against known facts, test boilerplate with an existing oracle | Efficient + low/medium | Cheap-first is appropriate; stop when the bound is reached | Diff/link/schema checks and relevant local tests; domain judgment or new test-oracle design moves to a stronger tier |
| Independent acceptance audit of high-risk work | Frontier + high/max, separate reviewer from author | Wait; no weak rubber stamp | Inspect original evidence and affected behavior; per-criterion citations, not the worker's summary |
| Low-risk deterministic validation/status extraction | Efficient + low/medium | Bounded attempt | Exact SHA/source and reproducible checks; ambiguous findings escalate |

## Provider and environment routing

- **Muse** is a coordinator/product or execution route, not a specific model.
  A Muse task still needs the underlying model, effort and tool environment
  identified. An unconfirmed model is recorded as unconfirmed.
- **GPT/Codex:** OpenAI's current guidance distinguishes Astra for demanding
  ambiguous work, Sol for balanced complex work, and Luna for scoped efficient
  work. [1] The task-launch catalog observed on 2026-10-07 offers
  `gpt-6-astra` with high/max, `gpt-6.1-sol`, and `gpt-6-luna`.
  This is a dated availability observation, not proof of any worker's actual
  runtime. Recheck the target executor's catalog before requesting a model.
- **Claude:** verify the exact model and effort offered by the actual account,
  client and executor. An available Opus-class model may fill the frontier role
  and Sonnet-class model the balanced role when task evidence supports that
  choice; neither name is a permanent rank or availability guarantee. Current
  model catalogs and per-model effort guidance are the authority. [3][4]
- Prefer the route with the needed **Blender/Godot versions, reference files,
  render/pixel inspection and test access**. A model badge cannot compensate
  for absent tools. Check tool readiness before spending the main work budget.
- Keep routing provider-neutral unless measured task results, tool access or
  an explicit user instruction justify a preference. Honor existing ownership;
  this policy does not contact agents, start workers or reassign live tasks.

## Fallback and escalation contract

Choose exactly one mode in each brief:

1. **`wait_for_required_tier`:** quota exhaustion means park the dependent
   implementation and report the required setup and blocker. Record a known
   reset time only when verified. Do not silently reduce the model or effort.
   Independent reference collection or tool preflight may continue.
2. **`bounded_attempt_then_escalate`:** one lower-cost initial attempt and at
   most one correction justified by new evidence, within a stated time/usage
   ceiling. Accept only if all specified checks pass. Escalate immediately for
   structural mismatch, missing tools, scope expansion, untestable claims,
   safety/data-loss risk or exhausted budget. Repeated identical failure twice
   is a hard stop under existing token discipline; never loop on paraphrases.

An escalation is a recommendation to the coordinator, not a second worker.
Confirm the existing worker's state and ownership before any authorized
handoff. Pass the current branch/SHA, evidence, failure and attempted approach;
do not pay the stronger worker to reconstruct missing context.
A stronger cleanup pass may replace the cheap patch completely if its
foundation is wrong. Do not make salvage mandatory.

## Required setup record

Every newly created task, worker brief and validator brief records the same
`recommended_setup`. Existing active tasks receive it at their next ordinary
planning/review update without interrupting the owner. No mass redispatch or
runtime enforcement is introduced by this document.

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


For a high-risk task, missing required-tier/tool verification blocks production
work; record the uncertainty instead of asserting readiness. For a low-risk
bounded task, an unconfirmed runtime may be tried only when explicitly recorded
and the brief's fallback permits it. The dispatcher checks this record before
starting; the reviewer checks it before accepting the deliverable. These are
human/agent review checks, not a claim that an automated validator exists.

## Cost and learning

Optimize **cost per accepted deliverable**, not raw tokens or the price of the
first attempt. Record total billed cost where available across attempts,
reasoning/output, review, tests/tool charges and cleanup, plus elapsed time and
Craig's review time. Token counts across providers, model rates, cached inputs
and subscription quotas are not equivalent dollars. If billing is unavailable,
report usage and time separately; do not invent a dollar conversion. OpenAI
notes that reasoning tokens are billed even when not visible. [2]

Reserve verification time/usage before implementation; do not consume the
whole quota on generation. For low-risk work, start with enough room for the
named tests and one correction. For critical 3D/system work, reserve a full
independent review and any required corrective pass. If the budget cannot
cover the gates, reduce scope or wait rather than reduce the acceptance bar.

Compare matched tasks with the same inputs and acceptance rubric; keep first-pass
acceptance, total cost, rework and escaped defects. Downgrade future tasks only
when evidence shows the quality bar holds. Maximum effort is justified by
measured improvement or expensive failure consequences, not habit.

## Sources and limits

Primary documentation retrieved 2026-10-07:
1. [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection)
2. [OpenAI reasoning effort and token accounting](https://developers.openai.com/api/docs/guides/reasoning)
3. [Anthropic effort: supported levels and per-model guidance](https://platform.claude.com/docs/en/build-with-claude/effort)
4. [Anthropic model catalog and capability discovery](https://platform.claude.com/docs/en/models/overview)

No Claude account/model-picker access or cross-provider game-development
benchmark was verified for this research. No pricing claim, universal winner,
or runtime attestation is implied. The matrix is a risk-based recommendation
to test on this project's work. Existing standing rules, task acceptance,
ownership, Actions restrictions and merge/publish permissions remain in force.
