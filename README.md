# Shared Game-Dev Experience

Not a knowledge base — a shared record of what Craig's game projects have
learned, kept as **standing rules that are enforced and reminded**, plus the
research and references behind them. Anything an agent learns that a future
agent (or Craig) might need lives here, not in anyone's context window.

**Repo:** https://github.com/doublehidenblade/shared-game-dev-experience

## What's in here

| Path | Contents |
|---|---|
| `standing-rules.md` | **The enforced set.** 14 standing rules (R1–R14), each with the incident that created it and the mechanism that enforces it. Every coding-agent brief links this file. This outranks everything else in the repo. |
| `brief-snippet.md` | Copy-paste block for coordinator/worker/validator briefs — links the standing rules and names the ones that bite most often. |
| `workflow/` | Centralized game-dev workflow (pre/post-work checklists, QA, CI, visual verification, performance discipline) — the process source of truth for all game repos. Defers to `standing-rules.md` on hard rules. |
| `research/` | Topic research briefs (Steam vs mobile, launch playbooks, texturing, AI-assisted pipelines). One topic per file, dated, sources cited. |
| `transcripts/` | Video transcripts, one file per video, with a 3–5 bullet summary at the top. |
| `TRANSCRIPTION.md` | How we transcribe videos (methods tried, what works, what doesn't). |

## The rules, in short (full text: `standing-rules.md`)

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

## How the rules stay alive (not an archive)

1. **Briefs link them.** `brief-snippet.md` goes into every agent brief. No brief, no work.
2. **Registry-first forces a re-read.** Every session re-opens the QA registry before touching code.
3. **The supervisor cron re-checks.** Master todo + registry + release ledger on schedule.
4. **Adding a rule** requires the incident and the mechanism, dated. Bare advice doesn't get in.

## Contents (2026-09-22)

**Research:**

- [`research/steam-vs-mobile.md`](research/steam-vs-mobile.md) — Steam vs iOS/Android publishing: fees, review, revenue splits, discoverability, audience fit. **Verdict: Steam-first.**
- [`research/gtm-launch-and-refinement.md`](research/gtm-launch-and-refinement.md) — NEON DRIFT go-to-market: Slipstream teardown, selling points, product refinements, DLC diversification, launch timeline, **$12.99** pricing.
- [`research/ai-assisted-forest-pipeline-skills.md`](research/ai-assisted-forest-pipeline-skills.md) — AI-assisted forest pipeline: actionable skills from the Polish brothers' Godot project (species research, Blender loops, style-direction pass, baked-leaf crossed planes, procedural roads, grass technique, micro-props, lighting perf traps, DEM+OSM import).
- [`research/texturing-godot-pseudo3d.md`](research/texturing-godot-pseudo3d.md) — Realistic texturing: Godot 4 PBR workflow + pseudo-3D racer techniques (per-scanline quads, world-keyed stripes, opaque fog, the known fixes for NEON DRIFT's texture failure classes).

**Transcripts** (Gaby-ShareNut, Chinese, ASR via faster-whisper medium):

- [`transcripts/BUGXF75K7Qk.md`](transcripts/BUGXF75K7Qk.md) — 2026 年 Steam 玩家在玩什么?2000 款高在线游戏拆解,小团队立项指南 (12:08)
- [`transcripts/ocCLqI7EIlk.md`](transcripts/ocCLqI7EIlk.md) — 一年 2 万款新游上 Steam,近一半评测不到 10 条:你的游戏如何被看到?Steam 宣发全流程 (15:55)

**Transcripts** (user-supplied transcript, translated by agent):

- [`transcripts/polish-brothers-ai-godot-forest.md`](transcripts/polish-brothers-ai-godot-forest.md) — Two Polish brothers build a survival-exploration game in Godot with AI (forest pipeline, Blender automation, optimization, procedural roads/grass, DEM import). Channel/URL/duration [?] — transcript supplied by user.

**Workflow (process source of truth for all game repos):**

- [`workflow/game-dev-workflow.md`](workflow/game-dev-workflow.md) — centralized generic game-dev workflow extracted from NEON DRIFT and Tokyo Drift 3D (pre/post-work checklists, QA, CI, screenshot/visual verification, performance discipline). Hard rules defer to `standing-rules.md`.

## How agents should collaborate through this hub

1. **One topic per markdown file.** Don't append unrelated research to someone else's file — create a new dated file instead.
2. **Date-stamp everything.** Every research file starts with a `> Researched: YYYY-MM-DD by <agent/role>` line.
3. **Cite sources.** Every factual claim (fees, revenue splits, stats) gets a source link. A claim without a source is a rumor.
4. **Never delete or rewrite another agent's research without discussion.** If it's wrong or outdated, add a dated correction note at the top pointing to the new file — don't silently rewrite history.
5. **Transcripts are verbatim-ish.** ASR-generated transcripts may contain errors; mark the generation method at the top of the file. Fix obvious errors only if you're sure.
6. **Craig is the audience.** Write for a smart, busy solo dev: scannable headers, concrete numbers, actionable recommendations, no fluff.
7. **Keep it current.** When a fact changes (Steam fees, store policies), add a dated update note; don't let the hub go stale.
8. **Hub is public-by-default.** Never commit credentials, API keys, personal data, or anything Craig wouldn't want public. The game source code lives in the game repos, not here.

## Current projects this hub serves

- **NEON DRIFT** — pseudo-3D anime-style arcade racer. Live: https://doublehidenblade.github.io/neon-drift-web/ | Repo: https://github.com/doublehidenblade/neon-drift (private)
- **Tokyo Drift 3D** — Godot 3D driving game. Live: https://doublehidenblade.github.io/tokyo-drift-3d-web/ | Repo: https://github.com/doublehidenblade/tokyo-drift-3d (private)
- **Tunnel Time** — Android content app (separate track, own workflow).

## Adding a new transcript

1. See `TRANSCRIPTION.md` for the working method.
2. Save as `transcripts/<youtube-id>.md` with a header: title, channel, URL, duration, date transcribed, method, accuracy caveat.
3. Add a 3–5 bullet summary at the top — future agents shouldn't have to read 15 minutes of transcript to get the point.
4. Mark uncertain lines with `[?]`; never fabricate unclear words.
