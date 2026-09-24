# Lesson: Slipstream teardown — what a honed pseudo-3D system looks like

Date: 2026-09-23. Source: local study of the commercial game Slipstream
(© ansdor) installed via Steam — asset formats and observable structure only,
no source (compiled FNA/.NET binary). **Technique notes only: no Slipstream
assets, art, or verbatim data files are reproduced here or anywhere in this
repo. Never ship their assets; derive techniques and create originals.**

## Why this lesson exists

Slipstream is the reference implementation of the pseudo-3D arcade racer we
are building. Studying it tells us what "honed" looks like — and where the
honed system still leaves room to beat it.

## What their system is

- **Cars are pre-rendered yaw strips, never 2D-rotated sprites.** Player cars
  ship as 16-frame strips covering the rear hemisphere (the chase-camera view
  range); the engine cross-selects a frame by relative yaw vs. camera. A
  separate 16-frame full-360° strip plays on spin-out, a 12-frame strip plays
  a barrel-roll on crash, and a small taillight-glow strip is composited
  additively when braking. Traffic cars get 4 rear-biased frames — enough,
  because you only ever see traffic from behind at small yaw offsets.
  Shadows are baked into every frame; there is no runtime shadow math.
- **Everything roadside is a billboard sprite.** Buildings, tunnel walls and
  entrances, cliffs, trees, lamps — one large atlas, all sprites, no
  projected quads or canvas geometry for "sides." When the road curves, the
  billboard keeps facing the camera and depth-scales. Collision boxes are
  *narrower than the sprite* (a column for a signpost) so poles collide but
  overhangs don't.
- **Roadside density is procedural data, not hand placement.** Each track is
  a list of sections (curve, slope, length); each section carries placement
  patterns per prop type: lateral offset, repeat spacing, sine-wave lateral
  wander (amplitude), scale variance, and a mirror-to-other-side flag.
  One-off landmarks use the same mechanism with a single occurrence.
- **Road is a vertical cross-section tile.** One small texture holds
  edge-band columns (rumble strips) plus the lane-surface column; the
  renderer stretches it per scanline. Per-track palettes re-tint the same
  tile — track identity comes from palette + texture + background, not new
  geometry.
- **Backgrounds are a parallax ladder.** Full-width strips per depth layer
  with simple integer scroll factors increasing by layer, plus a drift speed
  for clouds. Nothing fancier.
- **The track editor is a game mode, not a tool.** Their `track_editor.sh`
  is a 7-line launcher for `./slipstream --editor` — the editor runs *inside
  the game binary* and edits the same track format the game loads. That is
  what a honed system compounds into: the format stabilizes, then the editor
  ships, then track variety follows. See `track-editor.md`.

## Where they are weak (verified from the data, not taste)

- Roadside buildings **visibly repeat per section** — the same sprites
  stamped along the road. Procedural placement without procedural variety.
- Billboards read **paper-thin on tight curves** — no perspective treatment
  on sides at all.
- No crossroads, no trains, no lane-count changes — one road, fixed width.

## Our differentiation (Craig's direction, 2026-09-23)

Parity first on the technique list above. Then differentiate on:

1. **Procedural scenery variety + careful art direction** — seeded variety
   so no identical building appears twice in view, per-district aesthetic
   sets. See `procedural-scenery-variety.md`. Never "a better-looking
   billboard" — that framing is a knock-off.
2. **Track/map variety** — catch up to their breadth, then lead, using the
   track editor as the compounding mechanism.
3. **Stretching pseudo-3D past their limits** — crossroads, trains,
   bridges, tunnels, 2-lane ↔ 4-lane transitions.
4. **Vehicle variety — later.** Scenery, tracks, and tech first.

## Applies to

- NEON DRIFT (pseudo-3D racer): directly — every bullet.
- Tokyo Drift 3D (Godot): the editor-as-game-mode pattern and the
  procedural-variety discipline transfer; the sprite specifics don't.
