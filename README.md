# Game Dev Central

The coordination hub for Craig's game projects — the source of truth any agent
can clone to take over coordination. Previously named `shared-game-dev-experience`
(renamed 2026-09-23); the knowledge hub is now one part of this repo.

**Taking over as coordinator? Read `COORDINATOR.md` first.**

**Repo:** https://github.com/doublehidenblade/game-dev-central

## What's in here

| Path | Contents |
|---|---|
| `COORDINATOR.md` | Handoff doc: how to take over coordination |
| `project-management/` | Task boards (per game), worker registry, append-only coordinator log, canonical coordinator rules/briefs |
| `knowledge/` | **Enforced standing rules** (`standing-rules.md`, R1–R17+), lessons learned, research briefs, transcripts, game-dev workflow, brief snippets for spawning agents |
| `assets/` | Shared textures (CC0 stock) and art-directed mocks — sessions consume by repo-relative path |

## Rules of this repo

- Credential-free, always: never commit tokens, keys, or secrets here. Hub is public.
- Task truth lives in the game repos (`todos/`, `godot/docs/tasks/`); the boards here track dispatch state.
- One defect = one task. Craig's phone verdict is the final visual gate.
- Anything an agent learns that a future agent (or Craig) might need lives here, not in anyone's context window.

## The rules, in short (full text: `knowledge/standing-rules.md`)

1. Craig's phone is the final judge — ship as "for you to check", never "fixed".
2. Everything renders 100% opaque. No transparency tricks, ever.
3. Fix bug classes globally, never per instance.
4. Numeric CI assertions before baseline approval — they must fail on the broken frames.
5. Nothing closes without before/after evidence + his verdict.
6. Registry-first: oldest non-verified QA task across ALL batches.
7. 2D blueprint reviewed before any 3D scene assembly.
8. QA feedback goes to the repo's `qa/<batch>/`, never chat-text alone.
9. Intake everything immediately; the only copy is never in chat.
10. Never nudge a working session; never duplicate a live session.
11. Commodity textures from free CC0 libraries; imagegen for bespoke art/mocks.
12. Never pass script-generated art off as designer-drawn.
13. Every release notification carries screenshots + changes + risks + the play link.
14. Branch → draft PR → exact-head green CI → manual review → merge → verify live.
15. Mocks get eyeballed for symmetry before delivery (asymmetry only by design).
16. Track-editor-as-game-mode rule (see standing-rules.md).

## How the rules stay alive (not an archive)

1. **Briefs link them.** `knowledge/brief-snippet.md` goes into every agent brief. No brief, no work.
2. **Registry-first forces a re-read.** Every session re-opens the QA registry before touching code.
3. **The supervisor cron re-checks.** Master todo + registry + release ledger on schedule.
4. **Adding a rule** requires the incident and the mechanism, dated. Bare advice doesn't get in.

## How agents should collaborate through this hub

1. **One topic per markdown file.** Don't append unrelated research to someone else's file — create a new dated file instead.
2. **Date-stamp everything.** Every research file starts with a `> Researched: YYYY-MM-DD by <agent/role>` line.
3. **Cite sources.** Every factual claim (fees, revenue splits, stats) gets a source link. A claim without a source is a rumor.
4. **Never delete or rewrite another agent's research without discussion.** If it's wrong or outdated, add a dated correction note at the top pointing to the new file — don't silently rewrite history.
5. **Transcripts are verbatim-ish.** ASR-generated transcripts may contain errors; mark the generation method at the top of the file. Fix obvious errors only if you're sure.
6. **Craig is the audience.** Write for a smart, busy solo dev: scannable headers, concrete numbers, actionable recommendations, no fluff.
7. **Keep it current.** When a fact changes (Steam fees, store policies), add a dated update note; don't let the hub go stale.

## Current projects this hub serves

- **NEON DRIFT** — pseudo-3D anime-style arcade racer. Live: https://doublehidenblade.github.io/neon-drift-web/ | Repo: https://github.com/doublehidenblade/neon-drift (private)
- **Tokyo Drift 3D** — Godot 3D driving game. Live: https://doublehidenblade.github.io/tokyo-drift-3d-web/ | Repo: https://github.com/doublehidenblade/tokyo-drift-3d (private)
- **Tunnel Time** — Android content app (separate track, own workflow).
