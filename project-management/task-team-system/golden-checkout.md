# Golden checkout — worker staging trees without the clone tax

**Skill / playbook for coordinators and workers on Tokyo Drift 3D.**
Tool: `~/workspace/agent-watch/worker_tree.py` (VM-local; this doc is the portable copy —
any coordinator taking over from GitHub alone should rebuild the tool's behavior from here).

## The problem this solves

Every worker used to clone the full Godot project and run a full import before writing a
line: ~6 min tarball download + ~13 min Godot import, per worker, per death. Staging trees
were also never cleaned up, repeatedly driving the VM disk to 100% (2026-10-13: a failed
write truncated watchdog state; 2026-10-14 morning: 96–100% full again).

## The system (three parts, all scripted — no prose-only rules)

1. **GOLDEN TREE** — one pristine, pre-imported checkout of `tokyo-drift-3d` main at
   `~/workspace/.golden/tokyo-drift-3d` (1.6 GB; the Godot import cache lives inside at
   `godot/.godot`, ~409 MB / ~3,100 files). Its `.golden-meta.json` records the main SHA
   it was built from. `create` copies the golden (plain copy — this VM's storage rejects
   every copy-on-write trick: FICLONE reflink EPERM, no btrfs ioctls, overlay mounts
   refused), so a new worker tree costs ~25 s and inherits the import cache. Disk cost is
   the same as any tree; the reaper is the disk backstop.
2. **REGISTRY** — every tree `create` makes is registered in
   `~/workspace/agent-watch/state/worker-trees.json` and carries a `.worker-tree.json`
   marker. `close <slug>` deletes the tree when its task merges/closes.
3. **REAPER** — `worker_tree.py reap --apply` runs as watchdog STEP 0a2 every ~30 min. It
   deletes only trees with no live process referencing them AND no file modified for 48 h
   (emergency tiers: git-clean trees at 12 h when free <8 GB; any quiet tree at 24 h when
   free <5 GB). Every deletion is logged (path, bytes, git HEAD, dirty count) to
   `~/workspace/agent-watch/state/reaped.jsonl`. The denylist always wins
   (`state/tree-denylist.txt` + built-ins: `user`, `td138*`, `td245*`, `game-dev-central`,
   `ts-spaces`, `tools`, canonical sources). If free space is still <8 GB after reaping,
   the reaper prints **DISPATCH-HOLD** — no new worker dispatches until it clears.

## Commands

```
python3 ~/workspace/agent-watch/worker_tree.py create <slug>     # ~25 s; refreshes golden first if main moved
python3 ~/workspace/agent-watch/worker_tree.py close <slug>      # on task merge/close, same close-out
python3 ~/workspace/agent-watch/worker_tree.py list              # free space + golden status + trees
python3 ~/workspace/agent-watch/worker_tree.py reap --apply      # backstop sweep (watchdog runs this)
python3 ~/workspace/agent-watch/worker_tree.py golden-refresh    # rebuild golden if main's SHA moved (no-op if current)
python3 ~/workspace/agent-watch/worker_tree.py golden-refresh --force
```

Rules:
- **Never hand-clone or tarball-extract a worker tree again.** `create` is the only way in.
- `create` refreshes the golden lazily when main's SHA has moved; if the GitHub API is
  down it degrades to the existing golden, and refuses (loudly) only when no golden
  exists yet. There is no hand-clone workaround — fix the API path instead.
- Hand copies out of the golden need `cp --no-preserve=ownership` (plain `cp -a` fails at
  the last step with an ownership EPERM on this storage). `create` already handles this.
- Staging trees are disposable clones. GitHub is the source of truth; a reaped tree is
  re-creatable via `create`. Protect a tree from the reaper by adding its name to the
  denylist BEFORE it goes quiet.

## Worker prompt snippet (paste into every worker brief)

> STAGING TREE: create your working tree ONLY with
> `python3 ~/workspace/agent-watch/worker_tree.py create <slug>` — a ~25-second copy of
> the pre-imported golden checkout (import cache inherited). Never clone the repo or
> download a tarball. When your task merges or closes, delete the tree in the same
> close-out: `python3 ~/workspace/agent-watch/worker_tree.py close <slug>`.

## First-time setup (new coordinator / fresh VM)

1. Clone `game-dev-central` and read `project-management/task-team-system/SYSTEM.md`,
   then this file.
2. Make sure `~/workspace/agent-watch/worker_tree.py` exists (it syncs with the watchdog
   state in game-dev-central `project-management/watchdog/`; if the VM is rebuilt from
   GitHub alone, restore `agent-watch/` from that mirror first).
3. Build the golden once: `python3 ~/workspace/agent-watch/worker_tree.py golden-refresh --force`
   — expect ~20 min total (~6 min tarball download, ~13 min one Godot import). Do this
   when the VM is quiet (load < ~8, MemAvailable > ~2.5 GB); under load the download and
   import stall and retry.
4. Verify end to end (do not skip — an untested golden is a rumor):
   - `worker_tree.py list` prints `golden=True`.
   - `.golden-meta.json` in the golden root names the current main SHA.
   - `create td-golden-test` finishes in well under a minute and the new tree contains
     `godot/.godot/imported/` with thousands of files.
   - `close td-golden-test` removes it and the deletion appears in
     `state/reaped.jsonl` with `reason: close`.
5. Confirm the watchdog cron (`agent-session-watch`) STEP 0a2 is present in its saved
   body — that's what runs the reaper and enforces DISPATCH-HOLD.

## Refresh policy

- **Lazy (primary):** every `create` checks main's SHA against `.golden-meta.json` and
  refreshes first when it moved. Workers always start from current main.
- **Periodic (backstop):** the `golden-checkout-refresh` cron runs every ~6 h, guarded:
  it refreshes only when the golden is stale AND the VM is quiet (load and MemAvailable
  checks in its body); it stays silent unless it refreshed or failed. This keeps the
  first `create` after a merge from paying the ~20 min rebuild inside a worker's run.
- **On demand:** any coordinator can run `golden-refresh` (or `--force`) directly —
  e.g., right after a big merge lands, during a quiet window.

## Measured (2026-10-15, first build + lifecycle test)

- Golden built at main `61517f85`: 1.6 GB total, import cache ~409 MB.
- Build: ~20 min (download ~6 min at ~1 GB in RAM, import ~13 min).
- `create td-golden-test`: 24 s. `close`: freed 1.56 GB, audit-logged.
- The day before the golden existed, worker setup was ~19 min of download + import per
  worker — and per worker *death*, which during restart storms was the dominant cost.

## Failure modes seen (so the next coordinator doesn't rediscover them)

- `cp -a` out of the golden fails at the last step ("failed to preserve ownership",
  EPERM) — use `--no-preserve=ownership`; `create` already does.
- Copy-on-write is unavailable on this storage (reflink EPERM even as root). Don't
  re-attempt btrfs/overlay approaches without new evidence.
- Golden build under heavy load: GitHub API disconnects + VM restarts killed the first
  attempts (2026-10-14). Build in a quiet window.
- The GitHub credential helper path moved once (`dynamic_credentials`): if `create`
  dies with ModuleNotFoundError, set
  `PYTHONPATH=/opt/hatch/workflow-skills/custom-connector-setup/bin`.
