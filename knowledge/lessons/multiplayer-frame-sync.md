# Frame Sync (帧同步) — deterministic multiplayer via input broadcast

Source: 浙大猫学长 video series "howto vibe一款网络游戏" (VibeMotion tutorial album), frames captured by Craig 2026-10-07.
Status: **reference knowledge** — not a standing rule. Our shipped multiplayer (Tokyo Drift 3D, td-054/td-087/td-126) is host-authoritative state sync; frame sync is the alternative architecture for future deterministic games.

Note: the full video was not retrieved (search did not surface it); this doc is built from Craig's captured frames plus standard netcode practice. Video-specific claims are marked.

## The two architectures (the video's framing)

- **传结果 — send results (state sync).** The server simulates the world authoritatively and broadcasts *results*; clients render what they are told. The video's examples: 英雄联盟 (LoL), 守望先锋 (Overwatch), CS, 和平精英 — "走的都是这条路" (they all take this path).
- **传操作 — send operations (frame sync, aka lockstep).** Every client runs the *full simulation* locally; only player *inputs* are broadcast. All clients advance the same fixed timestep with the same inputs, so identical worlds emerge on every machine.

## When to use which

- **State sync:** FPS, MOBA, battle royale, open worlds, anything with heavy continuous physics. Tolerates latency (client prediction + server reconciliation), and the server is the cheat-resistant authority. Costs: bandwidth (whole state, many Hz), server CPU, rubber-banding under packet loss.
- **Frame sync:** small deterministic games — RTS, fighting games, turn-based, party mini-games. Tiny bandwidth (inputs only), perfect rule-fairness, free replays (record inputs, not states), and result-tampering cheats are structurally impossible. Costs: latency-sensitive (every client waits for the slowest input each tick — one laggy player stalls the room), and it *demands* determinism.

## The three principles (the video's vibe-coding prompt)

The video's prompt for AI-coding a frame-sync mini-game — "帮我 coding 一个帧同步小游戏" — starts with three principles to memorize first:

1. **逻辑和画面分开** — simulation logic decoupled from rendering. The sim must run identically with the renderer unplugged.
2. **计算只用整数** — integer-only math inside the sim. Floats diverge across ARM/x86, devices, and compilers; integers don't.
3. **随机数共用一个种子** — one shared RNG seed across all clients, so "random" events unfold identically everywhere.

## Engineering notes (standard practice, beyond the video)

- **Fixed timestep + input delay.** Collect inputs for tick N, execute them at tick N+D, so a late packet delays one client instead of stalling the room. Fighting games go further with rollback netcode (GGPO-style: predict, then re-simulate on correction).
- **Desync detection.** Broadcast a periodic state hash (checksum of sim state). On mismatch, resync from authority — never let clients silently diverge for minutes.
- **Determinism hygiene.** No wall-clock in the sim, no frame-rate-dependent updates, no platform RNG (use a seeded PRNG such as xorshift), no hash-map iteration order leaking into logic, integer or fixed-point positions.
- **Godot 4 caveat.** The engine's physics is *not* deterministic across platforms. A frame-sync sim in Godot must be custom integer/fixed-point logic stepped manually — never drive the authoritative sim from `_physics_process`, never read physics state as sim input. Treat engine physics as presentation-side only.

## Relevance to our stack

- Our current MP is host-authoritative star topology over a Node.js signaling server (`server/signaling-fly/`, room codes, the td-087 spawn + countdown barrier) — i.e. **state sync**. That is the correct choice for a driving game: continuous physics, latency tolerance, 2–4 friends.
- **Do not retrofit frame sync onto the driving sim.** Reach for frame sync when we build a deterministic mini-game or party mode — that is the game shape this architecture wins at.
