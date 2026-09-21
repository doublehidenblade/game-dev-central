# Game Dev Knowledge Hub

A shared knowledge base for Craig's game projects, maintained collaboratively by
Craig and his agents. Anything an agent learns that a future agent (or Craig)
might need — Steam publishing research, marketing playbooks, video transcripts,
post-mortems — lives here, not in anyone's context window.

**Repo:** https://github.com/doublehidenblade/game-dev-knowledge

## What's in here

| Path | Contents |
|---|---|
| `transcripts/` | Video transcripts, one file per video. Filenames: `<youtube-id>.md`. |
| `research/` | Topic research briefs (Steam vs mobile, launch playbooks, pricing, marketing). One topic per file. |
| `TRANSCRIPTION.md` | How we transcribe videos (methods tried, what works, what doesn't). |

## Contents (2026-09-21)

**Transcripts** (Gaby-ShareNut, Chinese, ASR via faster-whisper medium):

- [`transcripts/BUGXF75K7Qk.md`](transcripts/BUGXF75K7Qk.md) — 2026 年 Steam 玩家在玩什么?2000 款高在线游戏拆解,小团队立项指南 (12:08)
- [`transcripts/ocCLqI7EIlk.md`](transcripts/ocCLqI7EIlk.md) — 一年 2 万款新游上 Steam,近一半评测不到 10 条:你的游戏如何被看到?Steam 宣发全流程 (15:55)

**Research:**

- [`research/steam-vs-mobile.md`](research/steam-vs-mobile.md) — Steam vs iOS/Android publishing: fees, review, revenue splits, discoverability, audience fit. **Verdict: Steam-first.**
- [`research/gtm-launch-and-refinement.md`](research/gtm-launch-and-refinement.md) — NEON DRIFT go-to-market: Slipstream teardown, selling points, product refinements, DLC diversification, launch timeline, **$12.99** pricing.

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

- **NEON DRIFT** — pseudo-3D anime-style arcade racer (web). Live: https://doublehidenblade.github.io/neon-drift/ | Repo: https://github.com/doublehidenblade/neon-drift
- **Tunnel Time** — Android content app (separate track).

## Adding a new transcript

1. See `TRANSCRIPTION.md` for the working method.
2. Save as `transcripts/<youtube-id>.md` with a header: title, channel, URL, duration, date transcribed, method, accuracy caveat.
3. Add a 3–5 bullet summary at the top — future agents shouldn't have to read 15 minutes of transcript to get the point.
4. Mark uncertain lines with `[?]`; never fabricate unclear words.
