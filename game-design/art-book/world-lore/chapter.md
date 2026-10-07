# KUROGANE BAY — Art Book Chapter: WORLD MAP + LORE + TIMELINE
### The city as the gigs reveal it

*Canon: `~/workspace/game-design/gig-city-world-bible.md` (v2). This chapter is the story the player learns from behind the wheel — never a codex, never a lecture. History law applies: nothing here is historically accurate; it is post-war in energy and retro-futurist in fact. Nobody may correct it against real history.*

*Two mock layers per scene: **[REFERENCE]** is the aspirational painterly art direction; **[IMPLEMENTATION]** is what the final 3D actually renders under our real technology — Godot low-poly geometry, the AnimeLook shader module (flat color fields, ink outlines, cel-shading bands, washed-out texture noise), dust-culling fog, masked characters, no faces ever. Where a scene can't be built in-engine at all (the world map is a diagram, not a place), it stays reference-only — said explicitly, never silently.*

![[REFERENCE] Kurogane Bay — vertical cross-section world map](mock-worldmap.png)
*The three strata: the Aerium above the cloud deck, the Trench below, the Outskirts road west. The elevator pylons are the city's spine.*

**Production translation — REFERENCE ONLY, no implementation layer.** This image is a diagram, not a place. In-game the driver never sees an abstract cross-section camera — the strata exist only through the windshield, so a 3D implementation mock would burn budget on a viewpoint the shipped game never renders. The reference layer stands as the art-book diagram, unchanged. The closest it ever gets to the engine is a flat, unlit 2D graphic on the dash monitor (a folded tourist-pamphlet texture at 512×512), which is a UI prop, not a scene.

---

## A. WORLD MAP — Layout Spec for the Map Artist

### The governing rule: one bay, three strata, three gates between worlds

Kurogane Bay is a port city built around a single deep-water bay. The bay opens to the **south**; the city wraps its western and northern shores. To the **west** rise the pine mountains of Mt. Kurogane and the Nagisa Coast beyond them. The entire city is stratified vertically: the Lower City drowns in dust at ground level, the Upper City floats above the inversion layer, and the two are joined by exactly three car-elevator shafts. Draw the map as a cross-section first, a plan view second — the vertical dimension is the city's identity.

### LOWER CITY ("The Trench") — plan view, west to east

The Lower City is a crescent pressed between the mountains (west), the bay (south/east), and the North Canal (north, defining Chidori's edge). Reading west → east along the waterfront:

1. **The West Gate** — where the Nagisa highway enters the city. A single toll gantry under Minami's concession, flanked by Iron Wheel scouts. This is the only road out; it is also the city's softest ambush point. The gate faces the mountain switchbacks.

2. **Kotobuki Slums & Repair Row** — west-central, *sunken*. The district sits in a basin beneath the elevated tollway ring's support piers; the expressway passes overhead on concrete stilts and the shantytown grows in their shadow. Dust is thickest here. Adjacent east: the Shinkai haul roads; adjacent north: the canal shallows (South Canal, where Iron Wheel boats work). Key locations: the **train-shed garages** (Mariko's shed among them, an abandoned locomotive depot), the **filter-rinse bays** (the dust tithe's churches — rows of pressure-washer stalls under corrugated awnings), surplus markets, pirate-radio masts on the stilts.

3. **Daikoku Piers** — the southern waterfront, running the full length of the bay's western shore: miles of gantry cranes, container stacks, open-flame shipbreaking yards. The quay is divided into **Freight Gates 1–9**, numbered west to east. Gates 1–3 (west) are Kaiun-gumi stevedore turf; Gates 4–6 are the contested customs gates where Kaiun and Tsuru-kai fight over the cold-chain; Gates 7–9 (east) are the panel-field service docks. Offshore, the bay is carpeted with **floating panel arrays** in geometric grids to the horizon, with service catwalks and maintenance boats — contested between Kaiun-gumi (maintenance fees) and KPC (power revenue). North of the piers: Kamome; inland (north-east): Shinkai.

4. **Kamome Wholesale Ward** — north of the Daikoku quay, a wet-pavement labyrinth of seafood halls, cold storage, and auction stalls. This is the food throat of the city: everything edible passes through here before sunrise. Adjacent east: Tenjin (the paper-money district its cash flows into); adjacent north-east: the North Rail Depots (Tsuru-kai turf, dead freight yards); adjacent south: the contested customs gates at Daikoku 4–6. **Kamome auction halls** are the district's anchor — the dawn tuna auction is the city's loudest room.

5. **Shinkai Basin** — south-east inland, the refinery zone. Sol-88 cracking plants, chemical canals lit by flare stacks, bulk-plastics works. The dust *source*: visibility at its worst, the murk here has a sulfur tint. Bordered west by Kotobuki (the gray-fuel pipeline runs Shinkai → Kotobuki chop shops; this is the shortest smuggling corridor in the city), north by Tenjin's southern edge, south-east by the **Shinkai cracking plants** proper and KPC's security perimeter. **KPC security** holds the plant compounds; Kaiun-gumi leans on the fence lines.

6. **Tenjin Mid-Corridor** — dead center, the city's brutalist spine: a north–south canyon of trading houses, banks, and dispatch offices. This is the only district every other district must pass through — which is why the wars are fought at its edges. Its north end is anchored by **sky-elevator Terminal 2** (the corporate gate; Highline Adaeze's domain). Key locations: the **Tenjin dispatch offices** (Asahi Radio Cab's headquarters among them), the shell banks that receive Chidori's cab-laundered cash, the customs clearing houses. Contested by municipal patrols paid off by corporate security — the only district where the fighting is done with injunctions instead of pipes.

7. **Chidori Neon Strip** — east of Tenjin, across the **North Canal**: multi-tiered red-light alleyways, cabarets, capsule motels, pachinko palaces. The canal is crossed by three bridges — the district's chokepoints, each watched by Gokuraku-kai spotters. The dust thins here enough for blade signs to cut through; this is the one Lower district with authored night lighting. Key locations: the **Chidori Starlight Lounge** (Madame Kanzaki's velvet office above it), the North Canal motel row. Adjacent north: the North Rail Depots (supply lines into Chidori, the Gokuraku/Iron Wheel proxy-war corridor).

### UPPER CITY ("The Aerium") — above the cloud deck

The Upper City is a plateau of megastructures floating in clean pale sunlight above the ochre cloud sea. The three elevator shafts rise from the Lower City and pierce the cloud deck; their upper terminals open onto the **skyway ribbon** — curvilinear viaducts and banked ring roads linking the arcologies.

- **Minami Aerium** — central, the corporate megastructure plateau: white concrete towers, skybridges, 360° plazas. Houses **sky-elevator Terminals 1 & 3** (the upper ends of the two commercial shafts) and **Minami's toll HQ** — the Metropolitan Transport Board's headquarters, the building that taxes every wheel in the city, vertically. The Aerium ring road connects all three shaft-tops.
- **Haibara Heights** — the eastern cliffside: terracotta-roofed estates and executive villas above the cloud layer, private gardens, the dust a distant amber sea below. Reached from the Aerium by the eastern skyway ribbon — no elevator lands here directly, which is the point: the tycoons' demilitarized zone is one removable bridge away from everything. Private security; no faction holds it.

**Terminal numbering, settled for the artist:** each of the three shafts is a paired installation — a Lower terminal and an Upper terminal on the same cable line.
- **Shaft 1:** Lower base in Daikoku's east end (panel-field service side) ↔ **Terminal 1, Minami Aerium** (commercial freight).
- **Shaft 2:** **Terminal 2, Tenjin north end** (corporate gate) ↔ upper customs esplanade on the Aerium's south face.
- **Shaft 3:** Lower base in Kotobuki's under-expressway basin (the working shaft — broken lifts, union traffic) ↔ **Terminal 3, Minami Aerium** (west freight deck).

Canon names Terminals 1 & 3 by their Aerium ends and Terminal 2 by its Tenjin end; the pairing above is the art-book's recommended resolution (see Open Questions).

### OUTSKIRTS ("Nagisa") — the single road west

One highway leaves the West Gate, climbs the **Mt. Kurogane switchbacks** (mountain logging crews, the road's only company), crosses the **coastal viaduct** over the teal sea, and ends at the **Nagisa waystation** — an Iron Wheel fuel-and-filter stop with a beach beyond it. Nagisa Coast: pine mountains, a vivid teal-green sea (§B), fishing boats, the city's skyscrapers a hazy silhouette across the water (skybox — never geometry). Unaligned territory: hermit fishermen, mountain crews, the Union waystation. The waystation is the long-haul driver's church, garage, and rumor exchange.

### Chokepoints (the war is fought at these points, never on abstract turf)

| Chokepoint | Who bleeds for it | Why it matters |
|---|---|---|
| Elevator Terminals 1/2/3 | Everyone, endgame | The only way up; whoever holds a terminal taxes the vertical economy |
| Daikoku Freight Gates 1–9 | Kaiun-gumi vs. port inspectors | Everything imported enters through nine numbered gates |
| Kamome cold-storage customs gates (Daikoku 4–6) | Kaiun-gumi vs. Tsuru-kai (blood feud) | The food throat: who taxes the cold-chain taxes breakfast |
| North Canal bridges (3) into Chidori | Gokuraku-kai vs. Iron Wheel (proxy war) | The vice supply lines |
| Shinkai→Kotobuki gray-fuel corridor | KPC security vs. Iron Wheel siphoners | The underground's fuel artery |
| West Gate toll gantry | Minami's board vs. everyone | The only road out; the only road in |
| Aerium ring-road junctions | Minami's corporate security vs. corporate rivals | Upper City movement is tolled per junction |

### Faction control, at a glance (present day)

- **Daikoku Piers:** Kaiun-gumi (Gates 1–6); panel fields contested Kaiun vs. KPC
- **Kamome:** Tsuru-kai (auction halls, cold storage, North Rail Depots)
- **Chidori:** Gokuraku-kai (strip + motel row)
- **Tenjin:** contested — municipal patrols on corporate retainer
- **Kotobuki:** Iron Wheel Union (train sheds, rinse bays, under-expressway ring)
- **Shinkai:** KPC security (plants), Kaiun-gumi leaning on the fences
- **Haibara:** tycoon DMZ, private security
- **Minami Aerium:** Councilman Minami's transport board + corporate security
- **Nagisa:** unaligned — Iron Wheel waystation, fishermen, mountain crews

### The endgame war map

Faction war phases move blockades and change **elevator terminal control** — the terminals are the city's tollbooths, and holding one means taxing every crate, fare, and filter that crosses the dust layer. The war map is legible from the driver's seat: a terminal under new control changes its banners, its queue bribes, its inspection strictness, and the ROUTE-88's toll brackets before any dispatcher tells you why. The endgame is not a boss fight; it is the week all three terminals change hands at once.
---

## B. LORE — The City as the Gigs Reveal It

*Nothing in this section is told to the player. Everything is learned from the passenger seat, the payout chit, and the road. The world takes itself seriously; the absurdity arrives when high stakes collide with a Tuesday shift.*

### How the player learns the economy: the settlement chit

Every gig ends the same way: the ROUTE-88's brass slot spits a printed settlement chit, and the deductions are itemized before the net. The player does not read the economy in a codex — the economy *taxes* them, line by line:

- **Gross fare** — what the client paid.
- **Sol-88 excise** — KPC's per-liter cut, printed as a government stamp. When faction wars spike the fuel price, this line grows and the player feels the war in their pocket before any dispatcher mentions it.
- **Dust Tithe** — the filter-rinse levy, the radiator-scrub fee, the sealed-bearing surcharge. Every Lower City mile accrues it; Kotobuki's rinse bays are where you pay it in cash instead of performance.
- **Roadbed access tariff** — Minami's tolls, per district crossed, per stratum changed. The elevator toll is its own line, and it is always the largest.

A driver who never reads a word of lore still learns the city's power structure from these four lines: KPC owns the fuel, the dust owns the car, Minami owns the road. The settlement chit is the city's autobiography, printed after every job.

### The seven money flows, as jobs

**1. The Harbor Siphon.** *Who hires you:* a burner terminal at Daikoku Gate 5 texts a one-line offer that only appears when your tank drops below a quarter — the dispatch algorithm can smell desperation. *What you move:* unregistered cargo from a midnight van to a Kotobuki chop shop, gravity-fed Sol-88 straight into a hidden auxiliary tank. *What you learn:* the car goes tail-heavy and the exhaust smokes black; KPC's official ledgers write off the missing fuel as "seabed leakage," and the siphon crews are the leak. The harbor doesn't get robbed. It gets *reconciled*.

**2. The Synthetic Bloodline.** *Who hires you:* Mariko "Zero-Gauge" Katsu, who needs gray-market distillate for a speed trial and doesn't ask where you got it. *What you move:* siphoned Sol-88 in jerrycans — volatile, sloshing, and chemically wrong. *What you learn:* the engine knocks, the throttle lags, backfires draw KMTED patrols, and the fouling clogs your filter twice as fast (the Dust Tithe again). The monopoly isn't just enforced by KPC security. It's enforced by chemistry — the city's engines were built around Sol-88's burn rate, and everything else is a confession.

**3. The Morning Wholesale Squeeze.** *Who hires you:* Kenji the Fish-King, 4:40 AM, a 220-kilo bluefin that must reach the Grand Bay Hotel before the press breakfast — or a Tsuru-kai dispatcher with six crates of company-store produce and a route through a picket line. *What you move:* perishables on a melting clock; the ice kills your rear traction as it thaws. *What you learn:* Tsuru-kai doesn't sell food, it sells *permission to eat* — the auction, the synthetic-ice monopoly, the merchant loans are one machine, and the blockade at the cold-storage customs gate is the Kaiun-gumi trying to starve it. Cross the picket line and the payout clears; dump the cargo to the strikers and the payout dies — but a new dispatcher, one who never uses a name, starts offering you untracked work.

**4. The Neon Wash.** *Who hires you:* Taro "Clean Towel" Inaba, or a Gokuraku bagman who never introduces himself. *What you move:* nothing, at first — you drive loops through Chidori with a silent passenger while a mechanical cash-counter clicks in the back seat, and at every third loop the passenger feeds a brick of harbor cash into your meter as an "overpaid fare." *What you learn:* there is no wire transfer in Kurogane Bay, so dirty money gets laundered one cab ride at a time, and your car is the washing machine. Madame Kanzaki's intelligence network runs on the same principle: cab drivers hear everything, because passengers confess to the rear-view mirror.

**5. The Paper Chase.** *Who hires you:* Shinji "Slippery" Uno, three gold watches, sweating through a paper mask. *What you move:* bearer bond certificates and blackmail photographs in a briefcase that may not pass through corporate scanner grids — Tenjin's arteries are laced with them. *What you learn:* paper is the only true wealth left, because the paper can't be scanned, seized, or traced — only *driven*. You learn the drainage canals and service alleys the way other drivers learn shortcuts, because the main roads belong to the scanners. When the corporate recovery trucks come, they don't shoot. They pit-maneuver you into a contract default. Bureaucracy, with push-bars.

**6. The Vertical Arbitrage.** *Who hires you:* "Highline" Adaeze Okafor — or rather, the queue outside Terminal 2, which is its own employer. *What you move:* Lower City goods sealed for the Upper market (3× after decontamination), Upper City tech bound for Kotobuki (filters, compensators, sealed trunks — 5× below). *What you learn:* the elevator toll is priced with surgical precision — always *just* cheaper than the cost of the alternative. The alternative is the broken industrial lift in Kotobuki (30% mechanical failure, or a syndicate ambush) or the lead-lined smuggler trunk (decon-proof, but the mass changes your drift physics for the worse). Every driver does this math at the terminal gate, every day. The arbitrage isn't a secret. It's the tollbooth.

**7. The Dust Tithe.** *Who hires you:* your own engine. *What you move:* yourself, to a rinse bay, before the filter chokes. *What you learn:* the filter gauge is the city's slowest countdown — boost dies as it saturates, and the rinse costs money or minutes, always both. Kotobuki's rinse bays are the most recession-proof business in Kurogane Bay because the dust is the one tax nobody can dodge, bribe, or outrun. The bay attendants stamp your union card like priests stamping a pilgrim's passport.

### The three tycoons, as the work introduces them

The player never meets the tycoons. The player meets their *paperwork* — and their fares.

**Baroness Chiyo Moriyama** (land, tariffs) arrives as a fare: a tariff assessor in a sealed car who rides with you from Daikoku to Tenjin auditing your cargo against her schedule, stamping each crate's worth with a brass seal. The Kaiun-gumi think they run the harbor; the chit they pay her every month says otherwise. You learn she owns the ground the docks sit on the day a syndicate blockade evaporates — not because anyone fought, but because her office re-zoned the street it stood on.

**Director Hidetaka Vance** (KPC, the Sol-88 monopoly) arrives as an escort contract: ride shotgun — figuratively — for a KPC engineer convoy through Shinkai, while whistleblower extraction gigs offer you life-changing money to drive the *other* way. The choice between the convoy and the engineer is the city's thesis in one gig: the fuel is the blood, and everyone is deciding whose heart it pumps for.

**Councilman Goro Minami** (tolls, the suppressed rail, the Minotaur) arrives as infrastructure. You meet him every time you pay a toll, every time the ROUTE-88 shows a dead rail line as a dotted scar on the map, every time a shell-company shuttle gig asks you to ferry stranded factory workers from a welded-shut rail gate to the docks because his private bus fleet "broke down" again. The workers talk in the back seat. They always talk. Minami is never fought. He is driven *around* — which is slower, costs more, and is the entire game.

### The sea, as the gigs keep not explaining

The teal sea is never a mission objective. It is the thing at the end of the long-haul: the Nagisa run pays less per mile than city work, and drivers take it anyway, because the dust ends at the coast and the water is the wrong color and nobody can stop looking at it. The Iron Wheel waystation keeps a logbook of the nights the water glows — a driver can read it while the tank fills, and the entries disagree with each other and with KPC's bulletins, and that is the whole of it. Old fishermen at the beach terminus will tell you, unasked, that something woke up down there. KPC's public line is copper runoff. The logbook's last page is always blank, waiting for tonight. **The mystery is never resolved.** It is the city's exhale, and exhaling doesn't require an explanation.

### The laws, as friction

**The Kuro-Kiri dust ordinance** is why every NPC interaction happens through your window: foot travel without a filter suit is a felony, so the docker waves you in from the curb, the hostess ducks into the back seat, the mechanic leans into your window. The street is a machine trench; your cab is your life-support capsule. You learn this the first time a fare refuses to walk ten meters to your bumper.

**Tonnage Priority** is why intersections have no lights: right-of-way goes by gross vehicle weight, announced by blinking amber beacons and iron mirrors on poles. You learn it the first time a zaibatsu hauler doesn't brake for you — it never brakes for you — and the horn becomes a verb: kei vans scatter when you honk inside twelve meters, and scattering them is sometimes the job.

**The cab is sovereign ground** is why syndicate blockades wave you through — the food, the fuel, and the vice move through neutral drivers, and everyone knows it. You learn the exact shape of this sovereignty the first time you carry contraband through a blockade that *would* have waved you through: the wave becomes a search, the search becomes a chase, and the rule reveals its boundary. Neutral is a license. It can be revoked.

![[REFERENCE] The night the sea changed color](mock-sea-night.png)
*Deep-sea rigs on the horizon; the water lit from within. KPC called it copper runoff. The fishermen never did.*

![[IMPLEMENTATION] The night the sea changed color — as the shipped 3D renders it](impl-sea-night.png)
*The same scene through the AnimeLook module: unlit flat teal fields slammed against ink-black silhouettes. The glow survives as value contrast, not as light.*

**Production translation.** Survived: the whole idea — teal water against night-black — carried entirely by material-ID flat fills; silhouette oil rigs and boat with inverted-hull ink outlines; flare stacks as billboarded unshaded orange diamond quads; both masked figures (full respirator per the mask law, hood and cap, no faces ever). Cut: bloom, glow gradients, screen-space water reflections, Fresnel, atmospheric distance haze — the reference's "lit from within" luminescence cannot exist under flat-shaded low-poly; the glow is faked by setting the teal material *unshaded* so it reads as brighter than everything around it. Honest flag: the sea is a stepped-poly grid of hard teal bands, not water — the illusion thins up close, so this scene is staged at distance (the Nagisa waystation overlook, the coast run), never as a swim-up-to-it moment. The mystery is never resolved either way.
---

## C. TIMELINE — A Civic Artifact, Not a Wiki

*How to read this: the city dates itself by winters since the Surrender and by municipal cycles — never by calendar years, which belong to a history that never happened here. Entries are drawn from union minutes, KPC bulletins, ordinance ledgers, and garage relic walls (§5.9: the city curates its own past — every chop shop keeps an enamel plate from a dead business and argues about what the sea used to look like). What the clerks didn't write down is gone. That is the point.*

### ERA ONE — THE SCRAPE (the Surrender → ~the 12th winter)

*Mud, bilge water, and salvage. The city is horizontal: everything that matters floats or sinks.*

**Winter 0 — the Surrender.** The harbor is a wreck-yard: sunken destroyers, snapped cranes, a carrier's stern across the main channel. Nobody writes this down at the time. What survives is a photograph on a Kotobuki relic wall — a destroyer's bow being dragged ashore by ox teams, a naval ensign folded on a crate in the foreground — captioned in grease pencil: *"Day one. We started with the small ones."*

**Winters 1–4 — the Clearance.** Demobilized naval logistics crews and dockers clear the wreckage by hand, cutting hulls into breakwaters and crane parts. The work gangs formalize into the **Kaiun-gumi**: not a crime family — a labor monopoly with pipes. Their first ledger, still quoted at Gate 3, lists tonnage cleared per crew and the price of a snapped cable in fingers.

> [EXCERPT — Harbor Clearance crew tally, winter 2]: *"The Hōshō's hoisting tackle is ours. The municipal surveyors can have the rust. — R.M."*

**Winters 3–6 — the dance halls.** In the bombed-out blocks north of the canal, black-market dance halls open in half-collapsed theaters — kerosene lamps, demob uniforms tailored into band jackets, a generator and a horn speaker. The hall owners' mutual-protection pact becomes the **Gokuraku-kai**. Their founding document is a dance license paid for in kerosene chits, with a municipal stamp and a handwritten condition: *"the house band ceases percussion during air-raid drills."* The drills never come again. The condition stays on every license they ever hold.

**Winters 7–9 — the Great Fuel Famine.** The refineries are rubble and the winter is the coldest anyone remembers. Fishmongers and grain peddlers arm their supply wagons and run them in convoy through the dark — mutual aid with shotguns. The **Tsuru-kai** is born here, and its founder's abacus — brass, war-surplus — is still carried by "Abacus" Sato, who uses it the way other bosses use guns. The famine ends; the convoy discipline never does. Every Kamome auction still opens with the roll-call of the nine wagons that didn't come back.

**Winter 10 — the first municipal ledger.** The city government, such as it is, issues Ration Cycle tallies and a harbor tariff schedule. A young widow named **Chiyo Moriyama** buys the bombed-out freehold under three city blocks of the western quay at auction — cash, no financing, while everyone else is still counting ration chits. The clerks note the sale in one line. Nobody notes that she has just bought the ground the Kaiun-gumi's entire economy stands on. She will spend the next forty winters never having to mention it.

### ERA TWO — THE BLOOM (the 12th winter → ~the 25th)

*The sea changes color, and the city learns what it will sell its soul for — wholesale, in bulk, on contract.*

**Winter 12 — the deep boring begins.** Kurogane Petro-Chemical's survey rigs find coal seams under the bay floor — deep, dense, and wrong in a way the geologists' reports describe as "promising." The rigs go up: steel islands on the horizon, flare stacks lit like votive candles.

**Winter 13 — the night the sea changed color.** The cracking starts. One night the bay water turns a vivid, unnatural teal-green — lit from within, the fishermen say, like the sea is thinking. By morning every boat in the harbor is stained at the waterline.

Three accounts survive, and they have never agreed:

> [KPC Public Safety Bulletin #12]: *"Coastal luminescence attributed to benign copper leaching from deep-boring operations. Claims of brass corrosion are dockside hysteria. Swimming is discouraged pending further study."*
>
> [Fishmonger Brotherhood rite, instituted the same month]: *"No mackerel hauled past the breakwater may be sold until its eye-fluid is checked against the green glass marble. The marble belonged to old Jiro, who stopped going out past the rigs."*
>
> [A dockworker's boot, on a Kotobuki relic wall]: the leather is eaten through at the ankle. The tag reads: *"Coat them in mutton fat. Every tide. — advice of the 13th winter, still good."*

Nobody swims. Nobody has to explain it further.

**Winters 14–18 — Sol-88.** KPC cracks the refining process: a high-density synthetic kerosene from the deep-sea coal, and the city's engines — rebuilt around its burn rate — will never run on anything else again. The **Sol-88 monopoly charter** is granted by a government that needs the export revenue more than it needs competition. Director Hidetaka Vance signs it with a brass-nibbed pen; the pen is in a museum now. The charter's fine print contains the **Standard Valve No. 8** — threaded counter-clockwise, so no legacy engine can accept unauthorized distillate without violent manifold failure. Seven machine shops burn that winter. The arson is never solved. The valve becomes standard.

**Winters 16–22 — the tariff wall.** Moriyama Heavy Logistics consolidates the quay freeholds, the warehouse blocks, and the approach roads. She does not raise the tariffs — she *schedules* them, publishing a brass-bound tariff book with seasonal rates, and the syndicates discover that a predictable tax is harder to fight than a greedy one. The Kaiun-gumi's oyabun learns he is a tenant the way a man learns he is standing in someone else's shadow: gradually, then all at once.

**Winters 18–24 — the rail dies by inches.** Councilman Goro Minami's family holds the bus concessions and the tollway rights, and the municipal rail — cheap, public, and in the way — begins to fail in small, deniable ways. A timetable is "revised." A maintenance budget is "deferred." A commuter line is paved over for a bus lane, one segment at a time, each with its own ordinance number. The drivers who will one day be gig workers watch the last ground-level pedestrian crossing on the harbor boulevard get welded shut, and the foreman's work order — framed in a Tenjin dispatch office — reads in full: *"Obstruction to traffic flow. Remove."*

> [FIELD NOTE — Iron Wheel waystation logbook, winter 23]: *"The water glowed again Tuesday. Third time this month. Old Jiro's marble is still greener. — K."*

### ERA THREE — THE LIFT (the 25th winter → the present)

*The dust comes down like a lid, and the city goes vertical. Everything after this is the game.*

**Winters 25–30 — the dust age begins.** Forty years of foundries, strip-mined bay fill, and unregulated exhaust cross a threshold nobody measured: the inversion layer locks the particulate over the Lower City permanently. Visibility drops to a hundred meters and stays there. The municipal government, with the poetry of bureaucrats, names it the **Kuro-Kiri** — the black mist — and issues the dust ordinances: ground-level foot travel without a filter suit is a felony; every vehicle pays the filter levy; the rinse bays are licensed, taxed, and then taxed again. Drivers call it what it is: *the dust*.

The ordinances' small print contains the city's strangest decade-long argument: whether a fishmonger's delivery tricycle counts as a "locomotive engine" under the toll regime. The legal debate runs eleven years, generates four hundred pages of filings, and is settled when the last tricycle rusts through its frame. The monumental things get one line each. The tricycle gets a chapter. That is how civic memory works.

**Winter 31 — the last rail gate is welded.** Minami's suppression is complete: no public rail runs anywhere in the metropolitan boundary. His family's bus networks, tollway concessions, and taxi medallions now toll every wheel in the city — and the gig driver, the independent wheelman, becomes the only transit the poor can afford and the only courier the rich can trust. The Minotaur of Kurogane Bay is not a monster. He is a transport chairman, which is worse: you cannot stab a fare schedule.

**Winters 32–38 — the elevator construction.** Three brutalist shafts rise through the dust layer — open freight decks on cables, counterweight drums, Solari split-flap boards. They are built with the scuttled carrier's hoisting tackle and the wreck-clearance crews' grandchildren, and they leak oil on the tenement roofs below (carriages with weeping oil pans are charged double fare, per the posted notice, to discourage it). Terminal 2 opens at Tenjin's north end with a brass band; Terminals 1 and 3 open in the Aerium with a tariff schedule. The 8-second ascent becomes the city's signature vista: the fog dropping away beneath you, the Lower City shrinking into an amber sea, the punch through into blinding sunlight. The first driver to ride it up with a fare in the back seat doubles his price on the spot, and the price holds.

![[REFERENCE] Sky-elevator construction, the Lift Era](mock-elevator-build.png)
*Built with a scuttled carrier's hoisting tackle. The oil leaks were priced into the fare schedule.*

![[IMPLEMENTATION] Sky-elevator construction — as the shipped 3D renders it](impl-elevator-build.png)
*Brutalist massing survives; the crowd becomes low-poly silhouettes. The shaft is still the biggest thing in the Lower City.*

**Production translation.** Survived: the shaft's brutalist massing (flat-shaded concrete pillar + red steel framework, 2-step cel bands, inverted-hull outlines), twin cranes hoisting low-poly loads on cables, worker crews reduced to boxy hardhat-and-mask primitives, the brick warehouses and flat ochre dust fog at the base. Cut: the reference's dozens of individually-posed workers and hand-drawn texture detail — in-engine the crews are ~8 blocky figures with backs turned, the lattice cranes are angular low-poly geometry, and the "city skyline" is a handful of fog-swallowed boxes. Honest flag: this is history, not a playable space — in the present-day game the shafts stand complete, so this mock only justifies itself for timeline vignettes or loading-screen stills; don't budget a construction *scene* as in-game geometry.

**Winter 36 — the wildcat founding.** Rogue courier drivers, midnight drag-racers, and chop-shop mechanics who refuse the harbor syndicates' terms walk out of a Kaiun-controlled garage *en masse*, tools in hand, and set up under the expressway in Kotobuki. The **Iron Wheel Union** is founded without a charter, a headquarters, or permission — its founding document is a union card stamped in grease, and its first act is to run the broken industrial lift that the elevator authority condemned. Boss Tetsu's rule, still quoted: *"The roads are a commons. Drive well."*

**Winters 38–40 — the panel fields.** KPC carpets the bay's southern reach with floating photovoltaic arrays — the Bay Plan's ghost, built cheaper and stranger than the megastructure the old planners dreamed of. Kaiun-gumi claims the maintenance fees; KPC claims the power revenue; the Iron Wheel tappers claim the dark corners between the pontoons, siphoning current for elevator bribes. Three claims, one grid, no resolution. The city stops asking who owns things and starts asking who collects.

**The present — the gig-driver economy.** The map is fixed. The dust is permanent. The settlement chit prints after every job: Sol-88 excise, dust tithe, roadbed tariff, elevator toll. Auntie Shizue barks orders over the radio; the Meter Maid writes tickets in silence; Mrs. Yamashita calls her cab every Tuesday at 11:15 sharp. The faction wars tick through their phases — blockades move, terminals change hands, surge multipliers follow the fighting. And on certain nights, out past the rigs, the water glows teal-green, and the Iron Wheel logbook gets a new entry, and nobody — not KPC, not the fishermen, not the drivers — explains it. The page stays blank after the entry. It is always waiting for tonight.

> [IRON WHEEL WAYSTATION LOGBOOK — last entry, undated]: *"Glowed again. Brighter past the third rig. Jiro's marble, the sea, the marble. The sea wins. — K."*

![[REFERENCE] The Dust Tithe, paid weekly at Kotobuki](mock-dust-tithe.png)
*The most recession-proof business in Kurogane Bay: the rinse bay. The dust is the one tax nobody dodges.*

![[IMPLEMENTATION] The Dust Tithe — as the shipped 3D renders it](impl-dust-tithe.png)
*Behind-car chase camera, the taxi's rear bumper anchoring the frame. The water jet is an opaque white anime splash — zero fluid simulation, zero cost.*

**Production translation.** Survived: the whole staging — low chase-cam behind the taxi, red taxi body at ~1,500 tris with 2-step cel bands and ink outlines, stepped-geometry corrugated awning, the attendant as a boxy masked primitive with blocky backpack (back turned, face fully covered), the wooden booth and barrels, flat ochre dust fog. Cut: alpha-blended mist, fluid dynamics, wet-surface shaders, specular highlights on paint — the reference's wet sheen and drifting dust can't survive the AnimeLook module and are replaced by flat fog and the sprite jet. The water jet itself is the cheapest win in this chapter: a 2D sprite-flipbook splash, opaque and sharp-edged, with no lighting calculation at all. Honest flag: the reference's hand-drawn respirator detail is gone — attendants read as silhouettes, which is also why the mask law is free to enforce.

---

## OPEN QUESTIONS — pending BIBLE DELTA

*These are decisions the bible has not yet taken. Nothing here is canon until Craig rules.*

1. **Terminal pairing (map canon):** the bible names Terminals 1 & 3 by their Aerium ends and Terminal 2 by its Tenjin end. This chapter pairs each shaft with a Lower and Upper terminal (Shaft 1: Daikoku-east ↔ Aerium T1; Shaft 2: Tenjin-north T2 ↔ Aerium customs esplanade; Shaft 3: Kotobuki basin ↔ Aerium T3). Confirm or redraw.
2. **The Harbor Tram's fixed route:** the tram is a kinematic spline — which boulevards does it run? Proposed: the Daikoku quay boulevard → Tenjin's central canyon → the West Gate road. Needs a bible line.
3. **The panel fields' disputed history:** who built the first arrays, and when did KPC's claim begin? Kaiun, KPC, and the Union each tell it differently — the bible should pick the *official* lie and note the other two.
4. **Dating convention:** this chapter uses winters-since-the-Surrender plus era names (Scrape / Bloom / Lift). Ratify, or replace with municipal ordinance-cycle dating.
5. **The distant skyscrapers:** the Nagisa skybox shows a city across the water. Is it the mainland capital, a rival port, or uninhabited? Canon currently says "skybox, not geometry" — the art book should name what the silhouette *is*, even if drivers never go there.
6. **Moriyama's acquisition winters:** her land consolidation is dated by implication only. Does the bible want her origin story told (the auction, the tariff book), or should she remain an off-page force?
7. **Sea-mystery guardrails for future writers:** folklore entries and conflicting institutional voices are allowed; scientific resolution is banned. Should the bible also ban *new* physical evidence (e.g., a recovered artifact), or only explanations?
8. **Minami's first name and face:** "Goro" is bible canon; the mask law means no face is ever shown — but the art book should fix his *mask* (transport-board chairman's regalia) so every depiction agrees.
9. **The Meter Maid's jurisdiction:** she tickets wherever you idle illegally — does she operate in the Upper City too, or is she a Lower City fixture? (Affects the comedy engine's range.)
10. **Nagisa's teal catch:** the fishing economy runs on seafood from the changed sea. Is the catch safe to eat, and does anyone in-universe ask? (The Fishmonger Brotherhood's green-marble rite implies they ask every morning — the bible should say whether the question is ever answered. It shouldn't be.)

## Plausibility — what's depicted, why it's that way (2026-10-05)

Per Craig's law: dystopia allowed, unexplained eeriness is a defect, stereotype never. Every figure below was judged in the pixels against the bible (all faces masked; Dust Tithe — recurring filter/rinse costs; the sea mystery is never resolved). Full text in `~/workspace/game-design/art-book/plausibility.md`.

- **`mock-dust-tithe.png` — PASS.** Rinse station under the expressway: masked attendant scrubbing a sedan's windshield, second masked figure at the booth window, barrels, shacks. *Reflects:* the Dust Tithe made literal — the recurring rinse cost every vehicle pays to keep moving; the booth is the transaction point. *Why:* the attendant scrubs because dust blinds windshields (survival, not luxury); the second figure takes payment (cash/Sol-88); the barrels are the water stock — water is the tithe's currency. Both are staff at their workplace.
- **`impl-dust-tithe.png` — PASS.** "WASH & GO!" rinse bay in-engine: masked attendant pressure-washing a taxi under a canopy. *Why:* a working cab pays the tithe daily; one attendant, one job, no bystanders.
- **`mock-elevator-build.png` — PASS.** Sky-elevator tower under construction: concrete core, red bracing, cranes hoisting, worker figures on the ground, scaffolds, and balconies. *Reflects:* the city's vertical ambition being built — the elevators are how the Aerium grows. *Why:* construction crew at their stations — ground (materials), scaffolds (assembly), balconies (supervision). A building site is the definitive permitted on-foot workplace: enclosed, everyone staffed.
- **`impl-elevator-build.png` — PASS.** Tower in-engine: simplified shaft, red bracing, two cranes, ground-crew figures. *Why:* site staff at the material-handling level; the cranes are the assembly method.
- **`mock-sea-night.png` — PASS.** Night at sea: two figures in a small boat (one standing in coat and cap, one seated in hooded oilskin with respirator) facing offshore refinery platforms with burning flares. *Reflects:* the Shinkai basin's offshore face — industry's signature burning around the clock; the character law reaching even the sea. *Why:* a night boat crew — fishers run night shifts when the sea air clears; on a vessel, at work, the permitted presence; the flares are the landmark they work around.
- **`impl-sea-night.png` — PASS.** Night sea in-engine: two figures in a boat, four flare platforms, stylized wave bands. *Why:* same crew logic; the seated figure's respirator is the character law; stylized waves because the sea is a shader surface at game fidelity.
- **`mock-worldmap.png` — PASS.** The world map: Upper City on its elevator platform above the dust, Sky Elevator shafts, Daikoku Piers, Kamome, Tenjin, Shinkai Basin refineries, Panel Fields, Mt. Kurogane, Nagisa Coast. *Reflects:* the whole bible in one image — three strata, the districts, the dust layer as the literal divider between worlds; the map the GPS plans on. *Why:* every district shown because the map's job is orientation; the dust band sits between platform and ground because that is the city's founding geography; no figures because it is a cartographic document.

*End of chapter. BIBLE DELTA pending — no implementation tasks until Craig approves the bible.*
