# Lesson: Procedural scenery variety is the differentiator

Date: 2026-09-23. Incident: Slipstream teardown showed their roadside
buildings visibly repeat per section — procedural *placement* with no
procedural *variety*. Craig's correction: our edge is not "a better-looking
billboard" (knock-off framing) — it is **procedurally generated scenery
variety with more carefully designed aesthetics**.

## The bar

- **No identical building twice in view.** Placement patterns (offset,
  spacing, wander, scale, mirror) must draw from a *varied set* per prop
  type, seeded per track so layouts are stable and reproducible.
- **Per-district aesthetic sets.** A downtown section, a coastal section,
  and a mountain section should not share a building pool. Track identity =
  palette + texture + background + its own scenery set.
- **Variety is data, not hand placement.** Same mechanism as density: the
  track format carries which sets a section draws from and with what
  weights. Hand-placing hundreds of sprites does not scale; weighted sets
  do.
- **Careful design beats more sprites.** A small set of well-designed,
  district-coherent sprites with real variety reads richer than a large
  atlas stamped on repeat. Art direction is the multiplier on the
  procedural system.

## Mechanism

- CI assertion on generated layouts: sample the placed roadside sprites
  per track and fail if any identical sprite appears twice within the
  visible window, or if a section's set diversity falls below its quota.
- The track editor (see `track-editor.md`) previews variety live — the
  designer sees repetition while editing, not after shipping.

## Applies to

- NEON DRIFT: roadside sprite sets per track/district, seeded variety in
  the placement patterns.
- Tokyo Drift 3D: district composition — same discipline for building
  variety in stitched scenes.
