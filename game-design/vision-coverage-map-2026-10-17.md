# Vision coverage map — 2026-10-17

*Produced by the vision-breakdown pass under Craig's 2026-10-17 instruction: "If queue empty, it should look at the vision bible doc, break down new tasks and keep executing." Sources: the Kurogane Bay world bible (this repo, `game-design/gig-city-world-bible.md`), the game repo's `VISION.md` and `godot/GAME_DESIGN.md`, the task files on `tokyo-drift-3d` main @ `3a64246bae`, and this board. Statuses cite the task that carries each feature; "filed" means a task file exists as of this map.*

## The bible — status finding

- **The gig-city bible and the Kurogane Bay bible are the same document.** `game-design/gig-city-world-bible.md` is titled "KUROGANE BAY — World Bible (v2)". There is no second bible.
- **No formal approval is on record.** The tracked goal ("Kurogane Bay world bible approval", goal_3e3b09beb04e) still reads: Craig "must approve the bible before any implementation tasks are filed" — and its workspace holds no approval record. The bible itself says "No implementation tasks until Craig approves this bible", and its §17 makes Phase 0 an approval gate. The 2026-10-05 record shows Craig liking the direction, ordering the v2 dust-city revision, and explicitly not approving implementation at that time; no approval appears after that.
- **Operative authority for the first tranche:** Craig's 2026-10-17 queue-refill instruction (quoted above), cited as the `ask` in every task filed from it. In practice, much of the bible's world was already built 2026-10-06 → 10-17 under Craig's direct orders (Lower City, garage loop, gig system, living sky phase 1) — building from the bible is already the de facto state; the goal simply never received its approval tick. The coordinator may want to close or refresh that goal so the paper state matches reality.

## Coverage by bible phase (§17) — 33 feature rows: 6 implemented, 4 partial, 23 not started

| Bible feature | Status | Carried by / note |
|---|---|---|
| 1a Lower City road network (6 districts, expressway ring) | implemented | td-185 + district builds (td-270 Chidori, Tenjin/Kamome passes) |
| 1b Upper City skyway network | not started | likely Craig's Opus lane (sibling of td-185/187) — coordinator's call |
| 1c Sky-elevator terminals (3) | not started | gates every stratum gig; likely Opus lane |
| 1d Outskirts highway + Nagisa Coast | not started | Tokyo Bay is a separate legacy race circuit, not this stratum |
| 1e District visual identity | partial | Tenjin/Kamome/Chidori crafted; capsule towers, Daikoku panel fields, megastructures absent |
| 1f Dust system / living sky | partial | day/night + weather + trees done (td-267 phase 1); **seasons filed as td-276** |
| 2 Vehicle roster — 6 archetypes | not started | one drivable car today; **first slice (cargo van) filed as td-277** |
| 2b Dust-era modules (filter, altitude compensator, smuggler trunk) | not started | |
| 3a Timed-delivery core + gig board | implemented | gig system + td-205/214/260/268 |
| 3b Generic gig templates (10) | partial | point-to-point full; fragile as cargo stat; capability-gated variants (td-260); **chauffeur filed as td-278**; multi-drop, contraband template, shadow, cryo, escort, volatile not started |
| 3c Stratum gig templates (5) | not started | needs 1b/1c/1d |
| 3d Dispatcher (Auntie) + cast-driven gig sources | not started | no character exists in code |
| 4 ROUTE-88 GPS pre-gig planning | partial | td-236 exists but is blocked as a Dot-era documentation-only intake; nothing implemented |
| 5a Garage upgrades (4 stats) + fittings | implemented | td-197–202 first slice, td-260 capability consumption |
| 5b Vehicle purchases | not started | **filed inside td-277** |
| 5c Permits, lease fallback, surge multipliers, tip chains | not started | |
| 6a Heat / wanted / arrest | implemented | td-190/192/196/239 (td-195 collision completion in flight) |
| 6b Factions + standing | not started | zero faction names in code at filing; **foundation filed as td-279** |
| 6c War phases, terminal control, dispatcher loyalty | not started | needs td-279 |
| 7 Scripted missions (25) | not started | 8 premises written in the bible, 17 unwritten; needs 3+5+6 |
| 8a Unsecured-cargo rigid-body physics | not started | |
| 8b Aggro-redirect cascades | not started | see "too vague" — brawl behaviour unbounded |
| 8c Passenger state machines / Ejection Meter | not started | needs td-278 |
| 8d Spill decals / grease-fall drift zones | not started | |
| 8e The Meter Maid | not started | |
| 9a Daily Hot Route | not started | |
| 9b Weekly infrastructure shifts | not started | |
| 9c Dust-storm events | not started | |
| 9d Garage property purchases / infrastructure bribes | not started | bribe prices unscaled — see "too vague" |
| 10 Audio & identity (radio, engine voices, ambience) | not started | |

Surviving items from `VISION.md` / `GAME_DESIGN.md` (the 2026-09-18 racer design, superseded in framing by Craig's 2026-10-05 gig direction):

| Feature | Status | Note |
|---|---|---|
| Online multiplayer, 2–4 players | implemented (race mode) | td-050–053; the td-054 integration test is parked by Craig's explicit no-redispatch — excluded from the queue |
| Tokyo Bay circuit + bridge centerpiece | implemented | legacy race mode; td-243 restart fix in flight |
| World Inspector + asset registry (GAME_DESIGN §6) | not started | no task file exists |

## Full not-started list, in dependency order

Bible §17 dependencies: 1 → 2,3 · 3 → 4,5 · 6 needs 3 · 7 needs 3+5+6 · 8 needs 2+3 · 9 needs 1+3 · 10 anytime after 1.

1. **td-277 — cargo van** (Phase 2/5b) — FILED 2026-10-17
2. **td-278 — personal delivery gigs** (Phase 3b) — FILED 2026-10-17
3. **td-279 — faction standing foundation** (Phase 6b) — FILED 2026-10-17
4. Multi-drop milk run (Phase 3b) — wants td-277's capacity and td-278's gig-kind pattern
5. Vehicle roster remainder — luxury sedan, tuner fastback, flatbed rig, exotic (Phase 2), one per task
6. Dust-era modules: particulate filter tiers, altitude compensator, smuggler trunk (Phase 2b)
7. Progression breadth: gig-class permits, subcontract/lease fallback, surge multipliers, tip chains (Phase 5c)
8. Dispatcher Auntie + cast-driven gig sources (Phase 3d)
9. War phases incl. elevator-terminal control + dispatcher loyalty (Phase 6c) — needs td-279
10. Hot Contraband gig template (Phase 3b) — heat exists (6a); gains meaning with td-279
11. Upper City skyway network (Phase 1b) — likely Opus lane
12. Sky-elevator terminals (Phase 1c) — likely Opus lane; gates 13/14
13. Outskirts highway + Nagisa Coast (Phase 1d)
14. Stratum gig templates (Phase 3c) — needs 11–13
15. Scripted missions (Phase 7) — needs 3+5+6 and premises 9–25 written
16. Emergent comedy (Phase 8): cargo physics, passenger state machines (needs td-278), spills/grease-fall, Meter Maid
17. Retention (Phase 9): Daily Hot Route, weekly shifts, dust-storm events, property purchases
18. Audio & identity (Phase 10)
19. World Inspector + asset registry (GAME_DESIGN §6)
20. District identity completion (Phase 1e remainder)

Already filed and waiting outside this map's tranche: **td-236 (ROUTE-88 planning)** — blocked since the Dot era as documentation-only with an empty runtime allowlist. GPS pre-gig planning is one of Craig's named pillars; under his 2026-10-12 takeover the block reason (Dot-lane admission) no longer exists. Flagged for the coordinator to re-scope and dispatch.

## First tranche filed 2026-10-17 (td-276 – td-279)

| Task | Scope in one line | File area | Model / effort |
|---|---|---|---|
| td-276 Living sky phase 2: seasons | season choice retints foliage, shifts day/night keyframes, reweights weather incl. winter snow — on td-267's seeded hooks | sky director + sky config + tree foliage tint | standard / M |
| td-277 Cargo van (Tatsumi Hauler) | existing van asset becomes purchasable/ownable/drivable; its capacity unlocks td-260's gated heavy variants | vehicle defs + garage purchase/selection + van wiring | standard / L |
| td-278 Personal delivery gigs | passengers wait, board, ride; comfort sets the tip; Appeal ≥ 70 → ~+20% personal offers | gig_dispatch.gd + new passenger standee + gig_hud.gd | standard / M |
| td-279 Faction standing foundation | four syndicates as data; standing accrues from gigs by district; board labels + standing readout; no effects yet | NEW faction module + gig_menu.gd display + one config value | standard / M |

File areas are mutually disjoint and disjoint from the in-flight td-195 (cops), td-235 (map_sheet), td-243 (restart flow), td-245 (WantedHUD), td-274 (cop spawn).

## Too vague to taskify (named, not forced)

- **§7 template 6 Volatile Mass and template 9 Cryo-Timer** — parameter sketches (slosh, melt-vs-RPM) with no acceptance shape until a physics/temperature model is chosen; taskify as gig-variant slices after td-278 establishes the second gig kind.
- **§9 infrastructure-bribe prices** — quoted in dollars ($150k–$500k) while the shipped economy runs in yen at garage scale; no payout criteria can be written until the economy scale is settled.
- **§10 aggro-redirect brawls** — NPCs dragging cops from cruisers to brawl needs agent behaviour far beyond the current pedestrian system; no bounded slice is evident yet.
- **Phase 7 premises 9–25** — the bible itself says "16 more to be written"; unwritten stories cannot be tasked.
- **Phase 10 radio content** — stations are named, no track/content spec exists.
- **§13 the wacky sea's backstory** — deliberately unexplained by design ("the mystery is the content"); the buildable part is Nagisa itself (1d).
- **§16 Tekkonkinkreet steals** — thematic direction for all work, not features.

## Known canon-vs-shipped divergences (Craig's direct orders win)

- Bible §14 canon says "No pedestrians (Kuro-Kiri ordinance)" — the shipped game has pedestrians by Craig's 2026-10-14 playtest order (td-263).
- Bible §14 canon says fixed lighting per stratum, no day/night cycle — Craig's 2026-10-14 order replaced it with the living sky (td-267, and now td-276).
- `VISION.md` / `GAME_DESIGN.md` describe the retired 3-lap racer framing; Craig's 2026-10-05 gig direction and this bible supersede them.
