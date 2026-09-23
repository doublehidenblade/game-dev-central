# Lesson: Ship the track editor as a game mode

Date: 2026-09-23. Incident: studying Slipstream's `track_editor.sh` showed it
is a 7-line launcher for `./slipstream --editor` — the editor is **a mode of
the game itself**, editing the same track data format the game loads. That is
what you get after the system is honed down: the format stabilizes, the
editor ships inside the game, and track/map variety compounds from there.

## The pattern

1. **Hone the format first.** Track = data (sections with curve/slope/
   length, per-section placement patterns, palette, background). The game
   loads it; nothing about a track is hard-coded.
2. **Build the editor as a game mode, not a separate tool.** Same renderer,
   same data format, round-trip clean: load → edit → save → the game loads
   it back unchanged. A separate tool drifts from the format; a mode can't.
3. **Expose it early.** Don't wait for "done" — expose the editor while the
   game is still being tuned, so maps get hand-tuned by playing them.
   Craig's workflow: hand-edit the map, play it, and when a configuration
   plays well, say "bake it into a named track."
4. **Save locally first.** Browser localStorage (or equivalent local slot)
   is enough to start — the point is round-tripping edits inside the game
   session, not accounts or servers.
5. **"Bake into a named track" = export the format.** The editor exports the
   same track JSON the repo stores; a good configuration becomes a named,
   committed track file. Keep player-facing sharing as a later step, but
   design the save format as if players will exchange it one day.

## Why it matters

Map variety is the most expensive content to produce by hand and the
cheapest to produce once the loop exists: format → editor → playtest →
named track. Every track built without the editor is a track that can't be
iterated.

## Mechanism (a rule without a mechanism is a wish)

- The editor must round-trip the repo's track format: a CI check loads
  every named track in the repo *in the editor* and re-saves it byte-clean.
- A track that can't be opened in the editor is not a shippable track.

## Applies to

- NEON DRIFT: build the in-game editor once the section/pattern format is
  stable; expose early; localStorage saves; bake-to-named-track export.
- Tokyo Drift 3D: the same pattern applies to scene/district composition
  tooling — composition tools edit the same data the game loads.
