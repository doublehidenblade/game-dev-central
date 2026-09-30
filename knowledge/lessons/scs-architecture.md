# SCS Architecture — the three-rule framework for small Godot projects

Source: 野路子游戏车间 (video essay, "AI开发游戏时使用的游戏架构"), captured by Craig 2026-09-30.
Status: **adopted standing rule** — Craig 2026-09-30: all current and future game projects comply.

## Why this exists

AI agents building games reliably produce three defects:
1. One giant script file (`game.gd`, 1800 lines) — every change risks the whole game.
2. Magic numbers hardcoded in logic — tuning requires code changes and restarts.
3. Cross-scene `get_node()` references — renaming a node breaks scripts elsewhere.

SCS exists to stop those three defects. Three letters, three rules, one debugging order.

## Rule 1 — S: Scene（场景）: one scene, one script

- One scene = one `.tscn` = one script that only manages its own scene.
- `main.tscn` is assembly only — it instances `player.tscn`, `enemy.tscn`, `hud.tscn`, wires nothing beyond that.
- Payoff: a change touches one scene, not the whole file. AI debugging context stays small (one script instead of 1800 lines).

## Rule 2 — C: Config（配置）: separate numbers from logic

- All tuning values live in one autoload, e.g. `game_config.gd`: `hp = 100`, `player_speed = 300`, `jump_force = 500`.
- Scene-local tuning uses `@export` (Inspector sliders), no restarts needed between runs.
- Rule: a number change must never require a code change or a restart.

## Rule 3 — S: Signal（信号）: signals only, never direct references

- Modules communicate by **broadcast only** — the emitter never names the listener.
- `player.gd` emits `signal player_died`; HUD shows the death screen, main scene schedules restart — each on its own subscription.
- Forbidden: `get_node()` up or sideways (child scripts referencing parents/siblings). The emitter "only notifies, doesn't know who's listening."
- Node-rename test: renaming a node must not break unrelated scripts.

## The three rules composed (worked example)

Player hits spikes and dies:
1. **Assemble** (Scene): `main.tscn` = `player.tscn` + `spike.tscn` + `hud.tscn`.
2. **Values** (Config): `game_config.gd`: `hp = 100`, `damage = 100`, `respawn_wait = 2.0`.
3. **Logic** (inside player only): detect collision → `hp <= 0` → emit `player_died`.
4. **Response** (each on its own): HUD shows death screen, main scene restarts after delay.
When it breaks, exactly one of two faults: signal wasn't emitted, or it wasn't connected.

## Debugging order (fixed — always in this sequence)

1. **Config first**: are the numbers right? Push one to an extreme — if the symptom changes, it's the config.
2. **Logic second**: is the script right? Paste only that one scene's script to the AI.
3. **Signals last**: check both ends — was it emitted? was it connected?

## Working with AI under SCS

- Before work: make the AI state the structure (scene split list ≤6 items, config list, signal contract — what each signal emits and who subscribes) and confirm it before any code.
- During work: one module per feature, one at a time. After each, answer: which values changed, how verified in 30 seconds.
- Architecture decisions stay with the human; the AI executes.

## Compliance (project-level)

- New game projects: briefed with SCS on day one; task briefs must state the scene split, config file, and signal contract.
- Current projects: adopt opportunistically — never refactor working code for compliance, but every new feature/fix follows the three rules. Flag violations (giant shared script, hardcoded tuning, cross-scene get_node) as new tasks, one defect per task.
