# NAGISA — The Outskirts
### KUROGANE BAY art book, chapter: Outskirts

*The game's exhale. The one place the dust can't reach — and the water is the wrong color.*

**TWO MOCK LAYERS (Craig 2026-10-05):** every scene below ships both layers. **[REFERENCE]** = the aspirational art-directed target. **[IMPLEMENTATION]** = what the shipped game actually looks like under our real tech — Godot low-poly geometry, the AnimeLook module (flat color fields, inverted-hull ink outlines, 2-band cel shading, washed-out texture noise), masked characters (no faces ever), teal sea hue-locked 168–174°. Nagisa has long sightlines and no dust wall — the cost centers are water-shader simplicity and mountain geometry.

![Coastal viaduct over the teal sea [REFERENCE]](mock-viaduct-sea.png)

![Coastal viaduct over the teal sea [IMPLEMENTATION]](impl-viaduct-sea.png)

**Production translation — viaduct / sea.** SURVIVED: curved viaduct on bored piers, rust-red filter-canister rig, faceted cone-pine cliffs, flat skyline-card horizon, the wrong viridian sea, the hard ink waterline at piers and shore. CUT: smooth water gradients, foam, painted brushwork on water — impl keeps only hard two-tone cel banding on the sea plane; reference's painted cloud masses become flat cloud cards. HONEST FLAGS: (1) the reference's painterly shoreline detail (stained rocks, tide texture) cannot survive — impl shore is faceted rock plus a flat teal-stain decal ring with hard ink edges, and that is the closest achievable version; (2) the knife-edge waterline depends on the depth-sampled shader band — an unlit fallback would lose it, so the water shader is one of the few non-negotiable custom shaders in the district; (3) camera must never skim parallel to the water surface (minimum −3° pitch) or the flat plane loses all sense of distance — viaduct railings are authored to block grazing views.

---

## The landscape: one road in, one sea that refuses the sky

Nagisa is the entire outside world compressed into a single corridor. **One long highway** runs from the Lower City to the coast — the only road in and out. Off it, a coastal viaduct sweeps across the water on concrete piers, and mountain switchbacks claw down the slopes of Mt. Kurogane through dark pine forest. There are no shortcuts, no side routes, no grid: this stratum is a line, not a network. Driving it is endurance — fuel and filter math, axle-weight limits on the viaduct, fog and crosswind warnings from the waystation chalkboard.

The mountains are pine-black, cut with board-formed concrete retaining walls, hazard-orange guardrails, and painted iron mirrors on concrete pylons at the blind hairpins. The beach is not a destination — it is a narrow strip of teal-stained rock and gravel between the road and the water. Nobody goes there.

Across the water, on the far horizon: **skyscraper silhouettes, painted flat into the skybox**. Not geometry. A backdrop card of towers, hazy and pale — the city is always *over there*, and you cannot drive to it. (Canon performance trick: zero draw calls beyond the fog wall.)

**The light:** Nagisa gets the authored fixed lighting of a teal afternoon — pale chalk-bone sky, hand-painted clouds, warm umber shadows. It is the visual antithesis of the Lower City's amber murk and the Upper City's clean white sun. **The color shift is the UI.** The moment the cutscene plays and the teal hits the screen, the player has left the city. No map label, no text — just the wrong water.

### Arriving: the cutscene (canon, 4–6 seconds, three Showa-anime shots)

1. **Wheel close-up** — a tire at full speed, pine forest strobing past.
2. **Wide coastal viaduct over the teal sea** — the money shot, mock #1.
3. **Dashboard radio scrub** — the in-cab ROUTE-88 as a vacuum-tube radio scrubs through pirate stations, 89.4 MHz settling with a *CHUNK*.

The player enters the district **at full cruising speed**. A catapult, not a parking brake.

---

## The sea: how to paint wrong water

The sea at Nagisa is a vivid, unnatural **teal-green**. Not tropical, not algae — the wrong color, like a misprinted postcard. It stains the shoreline, the fishing boats, the sky at sunset. Art-direction rules for the sea (digested from a Gemini consult with an anime art director — principles, not quotes):

- **Hue lock: 168°–174° — a cold, synthetic viridian/phthalocyanine green.** Never drift toward 185°+ (sky cyan = Caribbean resort) or 145°–155° (olive = pond algae). Think poster color Viridian cut with Cerulean and a trace of black.
- **The water refuses the sky's light.** The sky is high-value, low-saturation (chalk-bone, ash-peach). The water is *darker and more saturated* than the atmosphere above it — low-value, hyper-saturated midtones. In nature, dark water mirrors a bright sky. Here, the water declines the reflection. That refusal is the misprint effect.
- **Flat and viscous, never wet.** No smooth horizon-to-shore gradients, no translucent refraction, no sand visible beneath. A flat gouache base with a rigid **2-step cel treatment** (base wash + shadow tone cut hard, zero feathering). Swells rendered as calligraphic cut-creases. It must read as cold machine oil or liquid enamel, not water.
- **The knife-edge boundary.** Where water meets shore: a hard ink line, no white foam, no surf break. Water laps against rip-rap and stained concrete without transition — the *Ponyo*-storm device. Teal tide-line rings stain pilings, hulls, and rocks. No barnacles, no mussels, no sea lettuce — this water does not seed life; it deposits **crystalline yellow-green mineral crust** on mooring lines and cables, stiffening ropes into calcified rods.
- **Foam, when it exists, is never white.** On the glow-nights (see § The mystery), the surface films teal-pale, like a lamp lit from below.

**The skyline trick:** keep the teal water flat and the skyscraper silhouettes flatter — both painted, both wrong. The whole horizon is a postcard that misprinted.

### Production consult — what survives the engine (Gemini, Godot technical-art; digested, not quoted)

Nagisa has no dust wall, so the two real costs are water and mountains. The verdict:

- **The sea ships as a flat plane, not a water shader.** Single camera-parented `PlaneMesh`, 4×4 subdivisions, fragment shader ~18 ALU: two scrolled noise lookups → hard `step()` → 2-tone cel mix (base `#00A896` hue 173°, trough `#025E5A`), noise faded 800–1500m into pure base teal at the horizon to kill shimmer. No normals, no SSR, no fresnel, no refraction, no mesh displacement, <0.04 ms at 1440p. The hard ink waterline is a depth-buffer diff band (dark line where sea meets piers/shore) — the non-negotiable signifier that keeps geometry from reading unclipped.
- **Mountains are three distance bands.** 0–400m: instanced low-poly terrain + pine cutouts + real road mesh. 400–1200m: faceted peaks (600–1200 tris each), zero individual trees (the mesh vertices *are* the pines), switchbacks as floating ribbon geometry — 2 tris/segment, 14m wide (cartoonishly wide on purpose, so it reads at distance), white vertex-color guardrail edge. 1200m+: flat silhouette cards with switchbacks baked as ≥2px vector lines. Because fog is banned, depth comes from value-stepping (near `#153028` → mid `#21443B` → far `#3A6359`) — far mountains read as paper cutouts, which the anime look absorbs.
- **Cut list:** dynamic foam/wake at viaduct footings (static ink ring instead), realistic road width at distance, individual trees beyond 300m, atmospheric perspective, decals for switchbacks (depth precision fails at 1km — ribbons, not decals).
- **Collapse risks:** grazing camera angles parallel to the water kill the sense of distance — enforce a minimum −3° camera pitch or block grazing views with railings; sub-pixel noise shimmer beyond 1.5km — the 800–1500m noise fade handles it.

---

## Locations

### The Iron Wheel waystation (District 9, mile 88 on the highway)

![The waystation at dusk [REFERENCE]](mock-waystation-dusk.png)

![The waystation at dusk [IMPLEMENTATION]](impl-waystation-dusk.png)

**Production translation — Iron Wheel waystation.** SURVIVED: chalkboard, union pennants, tire windsocks, rooftop Yagi antenna, drum stove + kettle, iron-wheel signage, box trucks, rock cliff and amber dusk cel bands, the masked mechanic (full respirator + dust hood — faces are never modeled here, no lip/face animation budget ever spent on this district). CUT: legible chalk text — impl uses abstract chalk scribbles, which is also the production truth: in-engine world-space text at playable distance would be an unreadable smudge anyway, so route advisories reach the player through the UI overlay, not world text. Reference's painterly grime becomes AnimeLook's washed-out noise at low intensity. HONEST FLAG: the two-mechanic scene thins to one — humans in Nagisa are set dressing with zero animation cost; the vacuum-tube radio gear is prop geometry only, the pirate station lives in audio.

The Union's sovereign outpost: refueling, repairs, pirate radio, and the last place that will save you before the viaduct. Design language: a mechanics' republic, deadpan-serious — mutual survival carved out of state infrastructure.

- **The cold chalkboard.** A massive slate-and-angle-iron board beside the fuel island, hand-lettered in industrial wax chalk with military timestamps: *VIADUCT: HIGH WIND, AXLE LIMIT 20T · RADIO FREQ 89.4 FM LIVE.* Route conditions are public infrastructure here — reading them is survival, not flavor.
- **Stenciled logistics markings only.** No municipal signs: *DIESEL A-HEAVY ONLY · NOT FOR DOMESTIC BURNERS* spray-stenciled on fuel tanks; weight-tiered parking bays sprayed directly on tarmac (light utility up top, triple-axle low).
- **Flags and territory.** Union pennants on grime-stained sailcloth — a fuel-injector cross-section over an anchor, branch number *DISTRICT 4 HARBOR HAUL*, safety-wired against the gale. Tire-casing windsocks on salvaged tubular-steel masts read viaduct wind-shear for incoming drivers.
- **The scrap stove.** A 55-gallon drum with a home-welded flue, glowing red in the repair bay; workers burn logging offcuts in it. A cast-iron kettle sits on top, baling-wired down so it can't vibrate off. Perpetually boiling.
- **The tally-peg board.** Drivers inbound from the switchbacks drop heavy brass numbered tags on a nail board at the dispatch desk. The tag stays until the driver clears the viaduct outbound. **An unclaimed tag means a breakdown or spill on the only road.** The board is the district's heartbeat and its missing-persons system.
- **The logbook of the glowing nights.** Kept at the dispatch desk in a brass-capped ledger. The waystation keeper records, in the same hand, dates and brief factual notes: *water glow observed 23:40, tide ebb, no wind.* No theories. No underlining. Just the record.
- **The pirate radio.** A rooftop vacuum-tube transmitter on a salvaged antenna mast (mock #2 shows the Yagi array). The Union's mouthpiece: shift-horn schedules, axle-limit warnings, driver call-ins. Frequency 89.4 FM — the third shot of the arrival cutscene.

### The fishing village

![The fishing harbor [REFERENCE]](mock-fishing-harbor.png)

![The fishing harbor [IMPLEMENTATION]](impl-fishing-harbor.png)

**Production translation — fishing harbor.** SURVIVED: trawlers with teal tide-ring stains, mineral-crust ropes, yellow HDPE tub stacks, winches, IBC tanks on stilts, blank windowless sea-facing walls, masked fishermen (hats + cloth masks, no faces), faceted pine hills, the flat wrong sea. CUT: rust/corrosion micro-detail, petroleum-scum waterline — no water micro-variation at dock scale; hull stains become a flat decal band with hard ink edges. Rigging wires become 1-pixel lines or nothing. HONEST FLAGS: (1) the reference's dense labor clutter (crates, coils, tools) is the district's main perf risk — it survives only as instanced low-poly prop clusters, never unique meshes; (2) the water at dock scale gets NO extra shader treatment — it is the same flat plane, and the knife-edge ink boundary against the breakwater carries the entire "wrong sea" effect.

A working harbor, never a postcard. Hermit fishermen, teal-stained boats, and a village that has physically turned its back on the sea.

- **Structural avoidance — architectural denial.** Sea-facing walls are blank masonry, bitumen-coated bricked-up voids, solid sheet-metal cladding: *zero windows face the water*. Houses and warehouses orient toward the mountain cuts; steps down to the water do not exist — only sheer concrete breakwaters with ladder rungs removed at the bottom two meters. The slipways are sealed with railway iron welded between H-beams, anchored into bedrock; boats go out on davits and hoists, never launched.
- **Decontamination as routine, not medicine.** Wheel-wash trenches of lime-clouded water at the dock apron — trucks scrub teal sediment off their tires before touching the waystation or the mountain road. IBC tanks of clear mountain water, trucked down from the logging camps, stand on stilts at the pier head: fishermen wash decks, tools, and boots with mountain water, never seawater.
- **The wear patterns.** Creosote-blackened docks; high-tide lines of iridescent petroleum scum, not algae; fractured concrete piers with rusty rebar spalling out; dissimilar-metal corrosion blooming powdery white and pale-green where brass meets steel.
- **The props of labor.** Yellow HDPE fish tubs warped by UV, stacked five high with frayed ratchet bands; hydraulic winches on raw I-beams wound with grease-soaked wire rope; corrugated sorting tables sluiced by battery pumps — bare of fish, bearing only scraping paddles and disinfectant buckets.
- **Giyōfū remnants** stand in the village's upper row: sand-blasted hybrids where European brick facades meet Japanese tile roofs — plaster stripped in patches by the wind into a map of the wall's own construction, arched windows bricked halfway up into squinting half-arches, verandas enclosed into **amber dust-lock porches** glazed with smoked acrylic. Two architectures weathering differently: the blend is legible as struggle.

### The logging camps (Mt. Kurogane slopes)

Upper-mountain clearings above the switchbacks: canvas-and-timber barracks, spar-pole yarders with wire rope, slash piles burned in ringed pits. The camps are the district's water supply (mountain-water tankers run downhill to the fishing village — the only clean water the village trusts) and its firewood source for the waystation stove. Mountain service vehicles — not trucks — own these roads: short-wheelbase winch rigs with cyclone intakes and chain racks, built for switchbacks a long-haul rig would die on.

### The coastal viaduct

The single engineering boast of the district: a concrete viaduct on bored piers, sweeping across a headland bay to shorten the highway. Wind warnings are real — the waystation posts axle limits, and heavy trailers cross at reduced speed or wait. The viaduct is the arrival cutscene's wide shot and the district's most dramatic driving: open air, the teal sea below, nothing between the player and the horizon but guardrail.

---

## Vehicles

| Vehicle | Role | Signature |
|---|---|---|
| **Long-haul rig (Goliath 800-class)** | The highway's sovereign. Outskirts runs are its gig type. | Cyclone filter intake cone on the hood, spare filter canisters strapped on the cab roof like ammunition, hazard-orange stripes, dust-ochre over rust-red primer, wired headlight guards |
| **Fishing truck** | Short-haul from docks to the waystation and city | Cab-over flat-nose, insulated fish box with teal-stained scuppers, rubber-booted drivers, wheel-wash lime residue on the tires |
| **Mountain service vehicle** | Logging-camp winch rig | Short wheelbase, spar-pole A-frame, cyclone intake, chain racks, high-clearance leaf springs — built for switchbacks, not speed |
| **Harbor workboat (small craft, static)** | Background only — the wheelman never leaves the wheel | Flat-bottom skiffs and steel trawlers: red-lead primer peeling over oxidized steel, vertical soot streaks from dry-exhaust stacks, teal tide-rings at the waterline |

---

## Characters (all masked — character law holds: no faces, ever)

- **The waystation keeper** — Iron Wheel Union, mid-50s. Grease-blackened coverall, canvas dust hood under a welder's mask pushed up over a full respirator, brass tally-tags on a lanyard. Speaks in single-sentence route advisories. Maintains the glow-night logbook without comment. *The district's dispatcher and its archivist.*
- **The hermit fishermen** — no names given, none offered. Sou'westers, rubber boots, simple cloth masks under rubberized aprons. They haul with body weight against the cleats and wash their boots in mountain water. When asked about the sea, they change the subject to the weather — a refusal so consistent it is a district law.
- **The mountain crew** — logging fallers and the tanker drivers who run mountain water downhill. Ear-protection muffs worn over dust hoods, canvas chaps, long-handled brass testing hammers for the winch rigs. Their labor ritual is the shift-change inspection: circling a vehicle, tapping axle boxes and rims in rhythm, listening for fractures — automatic, wordless, earned.
- **The radio voice (89.4 FM)** — never seen. The pirate station's night announcer: static-laced, unhurried, reading viaduct wind reports and the waystation's tally board like a shipping forecast.

---

## Items

- **The teal catch** — the village's product: fish pulled from the wrong water, crusted with mineral scale at the gills. Packed in yellow HDPE tubs on ice, wrapped in sealed lead-lined containers for the city run — raw contraband through the elevator scrubbers unless sealed (canon: the Decon Dodge). Fragile high-speed cargo: Kenji the Fish-King's gigs originate here.
- **Logging gear** — chain, wire rope, felling wedges, brass testing hammers; the consumables of mountain work.
- **The waystation logbook** — brass-capped ledger at the dispatch desk. Dates, times, observed glow. No theories. The only written record of the mystery, and it refuses to become evidence.
- **Refueling equipment** — stencil-marked diesel bowsers (*DIESEL A-HEAVY ONLY*), hand-cranked transfer pumps, brass fuel cans with lead-seal tags. Sol-88 arrives by tanker; gray fuel changes hands off the books.

---

## The sea-mystery treatment (canon — sketchy Evangelion-like, NEVER resolved)

The year the deep-sea coal seams were cracked for Sol-88, the water changed color overnight. Three accounts exist, and all three stay in the chapter, forever unresolved:

1. **KPC's official line:** copper runoff from the drilling rigs. Printed on a faded enamel sign at the waystation fuel island, sand-blasted to near-illegibility.
2. **The old fishermen:** something woke up down there, and the sea is *looking back*. Offered only when the player isn't asking — a line dropped over the radio or at the tally board, never explained.
3. **The waystation logbook:** the nights the water glows. Dates and times. No theories.

**Design function:** the sea is the game's exhale — the one place the dust can't reach — and the mystery is the content. The rules:

- **Nobody swims.** No swimming animation, no beach activity, no pier-jumping. The avoidance is total and unexplained.
- **Never resolve it.** No quest, no lab report, no NPC confession, no document that says what happened. If a future task proposes explaining the sea, it fails review.
- **Keep it behavioral, not expository.** The mystery lives in what people *do*: windows bricked against the water, masks hung outside quarters, mountain water trucked downhill to wash boots, the sealed slipways, the logbook's flat factual tone. Partial information is the whole aesthetic.
- **Comedy never touches it.** Craig's law holds hardest here: the sea is the one thing in Kurogane Bay that is never funny.

---

## Mocks (this chapter)

**[REFERENCE] layer** — aspirational, painterly, art-directed:

- `mock-viaduct-sea.png` — coastal viaduct over the teal sea, skyscraper silhouettes on the horizon, filter-canister rig crossing. The arrival establishing shot.
- `mock-waystation-dusk.png` — Iron Wheel waystation at amber dusk: chalkboard, pennants, windsocks, pirate antenna, scrap stove, masked mechanics.
- `mock-fishing-harbor.png` — working harbor: teal-stained hulls, crusted mooring lines, yellow fish tubs, IBC water tanks, blank sea-facing walls, masked fishermen hauling lines.
- `mock-switchback.png` — mountain switchbacks through dark pines, hazard-orange guardrails, iron mirrors, the long-haul rig, the wrong-colored sea at the horizon.

**[IMPLEMENTATION] layer** — what the shipped 3D actually looks like (Godot low-poly, AnimeLook ink/cel, masked figures only, teal sea hue-locked 168–174°):

- `impl-viaduct-sea.png` — the viaduct shot as an in-engine render: faceted cliffs, cone pines, flat viridian sea with hard ink waterline at the piers.
- `impl-waystation-dusk.png` — the waystation as an in-engine render: flat concrete, abstract chalk scribbles, full-face-respirator mechanic, drum stove.
- `impl-fishing-harbor.png` — the harbor as an in-engine render: faceted trawlers, flat stain bands on hulls, mineral-crust ropes, flat wrong sea with knife-edge boundary.

`mock-switchback.png` has no impl twin yet — the mountain bands (instanced cutouts / faceted peaks / silhouette cards) are specified in "Production consult" above but not yet rendered; that render is a follow-up, not a blocker.

### Plausibility — what's depicted, why it's that way (2026-10-05)

Per Craig's law: dystopia allowed, unexplained eeriness is a defect, stereotype never. Every figure below was judged in the pixels against the bible (all faces masked; Kuro-Kiri ordinance — unsuited foot travel is a felony; the outskirts are the city's clear-air lungs). Full text in `~/workspace/game-design/art-book/plausibility.md`.

- **`mock-viaduct-sea.png` / `impl-viaduct-sea.png` — PASS.** Coastal viaduct on piers, a tanker rig crossing, skyline across the water. *Reflects:* the Nagisa Outskirts as the city's lungs — the palette breaks to blue-green outside the dust wall; the viaduct is the umbilical carrying fuel and goods. *Why:* the rig is the freight artery's whole reason; no figures because there is nowhere for a person to be on a viaduct except inside a vehicle.
- **`mock-waystation-dusk.png` — PASS.** Iron Wheel waystation at dusk: chalkboard (wind/axle-limit/radio notes), two masked mechanics by the diesel pump, rigs under the canopy, brazier, union flags. *Reflects:* the outskirts' service node — fuel, information, shelter at the halfway point; the chalkboard is the driver's internet. *Why:* the two mechanics are the station crew (fueling + assisting) — staff at their post; the brazier burns because dusk at altitude is cold and drivers rest here.
- **`impl-waystation-dusk.png` — PASS.** Waystation in-engine: one masked attendant at the pump with a box truck, brazier, flags. *Why:* one duty crew runs the pump at this hour; the truck is being fueled — the station's entire purpose.
- **`mock-fishing-harbor.png` — PASS.** Working harbor: moored boats, crates, winches, warehouses, two masked fishermen hauling a line on a boat's stern. *Reflects:* the coast's food economy, independent of the city's dust-choked logistics. *Why:* the two are crew on a working boat — on a vessel, at work, the permitted presence; the quay clutter is the catch-handling chain.
- **`impl-fishing-harbor.png` — PASS.** Harbor in-engine: quay, sheds, tanks, two small figures by a skiff. *Why:* boat crew at the skiff — same vessel-at-work logic, simplified.
- **`mock-switchback.png` — PASS.** Mountain switchbacks above the sea: tanker rig descending the hairpins, pines, guardrails. *Reflects:* the outskirts' driving fantasy — the road as the destination; the route the GPS plans around. *Why:* the rig is on the coast freight route (no alternative exists); no figures because a mountain road has no sidewalks and the driver belongs in the cab.

---

## OPEN QUESTIONS (pending BIBLE DELTA items)

1. **Who owns the road?** The single highway connects the Lower City to Nagisa through open country — no faction claims it in the current bible. Is it municipal, unaligned, or quietly tolled by someone? The KPC angle (the road exists to serve the deep-sea drilling logistics) is unresolved.
2. **The viaduct's builder.** Brutalist concrete on bored piers is expensive civil engineering for a fishing coast. Who built it, when, and why — pre-dust public works, or a KPC drilling-access project? Answer changes the set-dressing (plaques, enamel plates).
3. **The drilling rigs.** The deep-sea coal seams were cracked offshore for Sol-88 — but Nagisa shows no rigs, no platform silhouettes. Are they beyond the horizon, mothballed, or deliberately kept off the skybox? The horizon composition depends on this.
4. **The teal catch's market.** Kamome Wholesale sells seafood; Kenji the Fish-King auctions dawn tuna. Does the city eat the teal catch, or is it exported/industrial? The answer sets the economics of the village and the Decon Dodge stakes.
5. **Glow-night frequency.** The logbook records glow nights — how often? A seasonal rhythm would let gig generation reference them (e.g., certain gigs only on glow nights) without explaining anything. Needs a design decision: rare enough to stay strange.
6. **Giyōfū remnants vs. Nagisa foreign-settlement history.** The bible names the sand-blasted hybrid facades for Nagisa/Daikoku, but the district's settlement history (who built European facades on this coast — a treaty-port town? a company town?) is unwritten. The extrapolation doc covers the weathering; the *origin* is still open.
7. **Pirate radio's reach and risk.** 89.4 FM broadcasts from the waystation roof — does KPC or the municipality try to shut it down? The answer sets whether the antenna is a defended asset (raid gigs) or tolerated background.
8. **Nobody swims — but what about wreck-diving gigs?** A future gig designer will want to put a payload under the water. The rule says the mystery never resolves; does it also forbid any sub-surface content? Needs an explicit ruling before a worker invents one.

---

*Chapter written 2026-10-05 by the Outskirts artist/writer. Gemini consults (sea-color art direction, coastal design devices) digested above — raw consult output not pasted per chapter convention. Awaiting bible approval; nothing dispatches until Craig approves.*
