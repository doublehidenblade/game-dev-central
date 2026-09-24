# Standing rules — shared game-dev experience

> These rules are **enforced**, not advisory. They outrank workflow convenience,
> CI greenness, and any agent's judgment call. Every coding-agent brief links
> this file; the supervisor cron re-checks it; violations get called out in
> review and roll back the "done" claim.
>
> Per-rule format: the rule, the incident that created it (dated), and the
> mechanism that enforces it. **A rule without a mechanism is a wish** — if you
> can't point at the enforcement, add it before adding the rule.
>
> Authority order: this file > `workflow/game-dev-workflow.md` > repo-local
> notes. If they conflict, this file wins.

## R1 — Craig's phone is the final judge

No visual fix is claimed done on test evidence, green CI, or generic
screenshots alone. Verify against his exact frames (frame-by-frame review of
his recordings) and ship as "for you to check", never "fixed".

- **Why:** p3d-030 was validated and went live, but his phone showed otherwise —
  he only learned by asking "Status?". v112's 7 phone-reported bugs the same way.
- **Enforced by:** `verified` status requires his phone confirmation (R6);
  release messages say "for you to check", never "fixed".

## R2 — Everything renders 100% opaque

No fading or transparency tricks anywhere. Geometry must be correct in
perspective first; sprites are surface detail only, never a way to game around
a bug. Prefer real sprites/textures over procedural canvas.

- **Why:** his call in the v112 bug report, 2026-09-21. Re-affirmed on NEON
  DRIFT canvas elements, 2026-09-22.
- **Enforced by:** visual-review checklist; numeric opacity assertions wherever
  the harness supports them.

## R3 — Fix bug classes globally, never per instance

Classify each visual bug (projection, scale, anchoring, transition, occlusion,
lifecycle, …), repair the shared invariant, and add deterministic CI exercising
the class across representative assets/scenes and continuous boundary sweeps.

- **Why:** one-off fixes kept coming back on his phone. 2026-09-22: "solve and
  CI them systematically."
- **Enforced by:** R4 — no baseline approval without the class-level assertion.

## R4 — Numeric CI assertions before baseline approval

Every bug class ships with a numeric assertion that **fails on the broken
frames**. An assertion that cannot fail on the evidence is not a guard. When
green CI misses a shipped bug: post-mortem first — quote what the assertion
actually measured, explain why it passed while the bug was visible, replace it
with one that fails on the evidence frames.

- **Why:** green CI shipped visible bugs (TODO 120 tunnel, among others).
- **Enforced by:** baseline approval checklist; the post-mortem is filed in the
  task's dev log before any replacement assertion lands.

## R5 — Nothing closes without evidence + his verdict

A QA item is never closed on an agent's claim alone. Closure needs before/after
screenshot evidence from the fixed build, and his verdict is final. When he
rejects a "fixed" task, it reopens with the rejection reason + date + evidence
link appended (prior evidence is never deleted); the worker must read the
rejection reason first and must never silently re-check a reopened item.

- **Why:** 2026-09-22 — "I constantly have to repeat myself and feel ignored."
- **Enforced by:** the registry status vocabulary (R6); `reopened` jumps the
  queue; only a validator verdict (system tasks) or his phone confirmation
  (visual tasks) moves an item to `verified`.

## R6 — Registry-first: oldest non-verified task across ALL batches

Before any QA work, read the repo's `todos/QA_INDEX.md` (human table) and take
the oldest non-`verified` task across all batches — never just the latest
folder. `reopened` tasks jump the queue. Any task in `open` / `in_progress` /
`reopened` with no update in 7+ days is flagged for supervisor review. Silence
is not progress. Never invent statuses — prefer `unknown` over guessing.

- **Why:** agents assumed only the latest batch mattered and missed pending
  older work and tasks he had rejected after they were marked fixed (2026-09-21).
- **Enforced by:** `todos/QA_INDEX.md` + `todos/qa-registry.jsonl` in each game
  repo (both exist: neon-drift, tokyo-drift-3d); the supervisor cron runs the
  stale scan. Full status vocabulary: `workflow/game-dev-workflow.md` §8.

## R7 — 2D blueprint reviewed before any 3D scene assembly

Scene stitching/composition always starts with a Craig-reviewed 2D blueprint:
extract actual road geometry (never invented), top-down SVG+PNG with labeled
footprints at real-world scale, the continuous route, explicit transition
zones, key landmarks; self-sanity-check (roads connect, curves drivable, route
continuous); then STOP and hand the PNG + layout summary + open questions over.
No 3D assembly until a proceed decision.

- **Why:** his standing spec-and-review loop; unreviewed 3D gets rebuilt.
- **Enforced by:** the brief template — the blueprint deliverable is a gate,
  not a suggestion.

## R8 — QA feedback goes to the repo, never chat-text alone

His screenshots and feedback files go to the repo's `qa/<batch>/` folder
(screenshot + `notes.md` with numbered items); the agent is told the exact
repo-relative path. The agent needs the file on disk in its workspace — chat
carries only the path.

- **Why:** QA feedback delivery rule, 2026-09-22. Chat-only feedback got lost.
- **Enforced by:** the filing checklist; the brief carries the path, not the prose.

## R9 — Intake everything immediately; the only copy is never in chat

The moment a prompt raises an ask, bug, feature, or reference: save it in the
repo's task/todo structure with acceptance criteria and status, and commit/push
that record on its own if the fix will take a while. Re-check the master todo
before claiming anything finished.

- **Why:** his standing working discipline; disposable containers and chat
  history eat requests.
- **Enforced by:** the pre-work checklist; the periodic cron re-check.

## R10 — Never nudge a working session; never duplicate a live session

STALLED: at most one `continue` every 45 minutes, after re-verification.
DEAD: resume only after confirming no live equivalent exists. Never
merge, publish, or implement game code through the watchdog.

- **Why:** watchdog hard rules, 2026-09-22. Duplicate sessions waste paid
  compute and corrupt task state.
- **Enforced by:** the watchdog decision code, not prose.

## R11 — Commodity textures from free CC0 libraries; imagegen for bespoke work

Commodity game textures come from free texture libraries (document sources +
licenses, e.g. `qa/td016-texture-requests/sources.md`). Image generation is
reserved for bespoke art-directed pieces and mocks. Never claim stock textures
were image-generated.

- **Why:** his decision, 2026-09-22. Paid-tier imagegen is for what stock
  can't do.
- **Enforced by:** the texture-sourcing checklist in task briefs; sources.md
  required per texture batch.

## R12 — Never pass script-generated art off as designer-drawn

Mocks are labeled as mocks. AI direction references are direction-only; the
real references are the authority.

- **Why:** NIGHTRUN mock rejection, 2026-09-14.
- **Enforced by:** review; mislabeled art is called out and removed.

## R13 — Every release notification carries proof + the play link

Inspected screenshots of what changed, what the latest PR changed, what's
still planned / remaining work and risks, and the game link — every time. No
screenshot-less or context-less "merged" pings.

- **Why:** his coding-agent rules, 2026-09-22.
- **Enforced by:** the release ledger — marked only after the message is
  actually sent; the watchdog re-flags anything finished-but-not-announced.

## R14 — Branch → draft PR → exact-head green CI → manual review → merge → verify live

Work on a branch from updated `main`, never on `main`. Merge only when the
exact PR head is satisfactory and CI is green. After merge, verify the live
deployment: open the live URL, exercise the affected area, report the play
link + PR + remaining limitations.

- **Why:** workflow extraction, 2026-09-22. Stale-head merges shipped
  unverified code.
- **Enforced by:** the per-session checklist; the publisher pins the reviewed
  candidate (run ID, full SHA), never an arbitrary newer run.

## R15 — Symmetry check on mocks and renders; asymmetry must be by design

Lane markings, paired props, road furniture, and mirrored set pieces render
symmetric unless the design says otherwise. Mocks get eyeballed for symmetry
before delivery; game CI asserts it numerically where the harness supports it
(e.g. mirrored-region pixel diff on straight-road frames). An agent bypassing
the check must state the design reason in the task notes.

- **Why:** 2026-09-23 — the tunnel treatment mock shipped with blue dashes on
  one side and purple on the other (a generation artifact, not design).
  Craig: "if agent wanna bypass that CI it better have a good reason, like
  it's by design."
- **Enforced by:** the mock review checklist; CI symmetry assertions; a bypass
  without a stated design reason fails review.

## R16 — Ship the track editor as a game mode once the track format is stable

Once the track data format is honed, the editor ships *inside the game* as a
mode (not a separate tool), editing the same format the game loads. Expose it
early so maps get hand-tuned by playing them; saves go to local storage
first; "bake into a named track" exports the repo's track format. A track
that can't be opened in the editor is not shippable.

- **Why:** 2026-09-23 — Slipstream's `track_editor.sh` is a 7-line launcher
  for `./slipstream --editor`: the editor is a game mode, and that is how a
  honed system compounds into track variety. Craig: expose it early "so I can
  edit the map by hand and tell you 'hey this configuration plays well, bake
  it into a named track'."
- **Enforced by:** CI round-trip check — every named track in the repo loads
  in the editor and re-saves byte-clean.

---

## How rules get reminded (the loop that makes this more than an archive)

1. **Briefs link this file.** Every worker/validator/coordinator brief includes
   the copy-paste block from `brief-snippet.md`. No brief, no work.
2. **Registry-first forces a re-read.** R6 makes every session re-open the QA
   registry before touching code — open items resurface on their own.
3. **The supervisor cron re-checks.** Master todo + registry + release ledger,
   on schedule; finished-but-not-announced keeps flagging until the message
   goes out.
4. **Adding a rule** requires the incident and the mechanism, dated. Rules are
   never added as bare advice. If a rule's mechanism stops working, the rule is
   flagged, not quietly ignored.
