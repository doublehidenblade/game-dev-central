# Taking over coordination? Read this first.

This repo is the source of truth for Craig's game-dev agent team. If you are picking up the coordinator role (Muse, GPT, Claude — any agent), everything you need is here. Do not rely on any single agent's memory; this repo is the handoff plane.

## Where things live

- `project-management/boards/neon-drift.md` — NEON DRIFT task board (task truth: `todos/todoNNN/README.md` in the neon-drift repo)
- `project-management/boards/tokyo-drift-3d.md` — Tokyo Drift 3D task board (task truth: `godot/docs/tasks/td-*.md` in the tokyo-drift-3d repo)
- `project-management/workers.md` — who is on what, last-seen state
- `project-management/coordinator-log.md` — append-only dispatch history (read the tail first)
- `project-management/rules/` — canonical `SYSTEM.md`, `WORKER_BRIEF.md`, `VALIDATOR_BRIEF.md` (read SYSTEM.md before spawning any worker)
- `knowledge/` — enforced standing rules (R1–R17+), lessons, research, workflow
- `assets/` — shared textures and art-directed mocks (sessions consume by repo-relative path; never paste images into session chat)

## How to coordinate

1. **Read the tail of the coordinator log**, then the boards and worker registry. Board rows marked `unverified` need re-verification before you act on them.
2. **Claim a task** by writing your worker id + UTC timestamp into the board row. One task per worker. **Never two workers on one task.**
3. **Update the board** on every transition: claimed → in_progress → PR opened → merged → validated. Mark blocked with the exact reason; surface a block to Craig once, then stop nudging it.
4. **Append to the coordinator log** whenever dispatch state changes (spawned, steered, shipped, parked).
5. **Pull --rebase before every push.** If a push fails twice, stop and report (stop-after-2) — do not force-push over another coordinator's writes.

## Hard rules (from Craig)

- **One defect = one task.** A batch is a filing label only. A bundled parent becomes SUPERSEDED and never closes; each child closes only when its exact defect is fixed and verified.
- **Craig's phone verdict is the final visual gate.** Never close a visual QA item on a worker's claim or on test evidence alone — closure needs before/after screenshots from the fixed build and his verdict.
- **Never nudge a working session. Never duplicate a live session.** Fresh session per task.
- **Never commit credentials, tokens, or secrets** to this repo or any game repo. This repo stays credential-free, always.
- QA feedback to sessions goes as committed files under the game repo's `qa/<topic>/` with the exact repo-relative path — never as chat text alone.
- Every release/PR report: inspected screenshots, what changed, who shipped it, remaining work, live link.
