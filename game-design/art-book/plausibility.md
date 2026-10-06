# Kurogane Bay Art Book — Plausibility + Explanation Pass
Date: 2026-10-05 | Worker: plausibility + explanation (depth 2/2)

## Craig's law (verbatim, obeyed throughout)

1. "The first image is a bit eerie (not in a intended way) cuz the women are standing on the streets unnaturally, and shops are closed. Is it supposed to be red light district? Then it's not appealing enough. Not saying I dont want eerie, some parts of the lower city can feel dystopian, oppressed, cuz of dust and reclusion. But needs to be a plausible way. This image instance here isn't expainable."
2. "Every artwork needs a text explanation on what's in it, how it reflects the setting, why things are the way it is in there. Needs to be intentional design, not stereotypical racist impression."

Rules derived: dystopia/oppression ALLOWED; unexplained eeriness is a DEFECT; stereotype is NEVER allowed. When in doubt, cut the figure or explain them — never leave an unexplained body on the street.

## Canon bible (re-read 2026-10-05, v2 — the rules every image is judged against)

- **Character law:** every face masked — respirators, goggles, hoods; no faces modeled.
- **Kuro-Kiri ordinance:** foot travel without a filter suit is a felony → drive-up economy; static masked figures only in unreachable perches; zero locomotion.
- **Dust:** visibility wall (100 m cap) + economic burden (Dust Tithe — recurring filter/rinse costs).
- **Fake-life rules:** window silhouettes, static masked pickup figures, drive-through counters.
- **Cab is sovereign ground; the wheelman never leaves the vehicle.**
- Chidori Neon Strip: multi-tiered red-light alleyways, Gokuraku-kai, dust thins enough for blade signs to cut through, authored night, warm red/amber only.

## Scope notes

- 47 art-book images reviewed in full (28 `mock-*.png` REFERENCE + 19 `impl-*.png` IMPLEMENTATION), each opened and judged myself. Every verdict below is grounded in the pixels, not in worker captions.
- **The 12 `qa/kurogane-bay` mocks do not exist on disk** — no such directory or files were found anywhere in the workspace (searched 2026-10-05). They are not covered here; if a sibling worker produces them later, they will need their own pass.
- The taxi-street PROBLEM image Craig attached is byte-identical in composition to `lower-city/impl-chidori.png` — it was already in the book, not a separate file. It is the one REWORKED image in this pass.
- Gemini (gemini-3.8-flash) was used to pressure-test the impl-chidori rework decision. Its attack confirmed the defect and picked option (a).

---
---

# CHAPTER 1 — LOWER CITY

## `mock-chidori.png` — PASS

**WHAT'S DEPICTED:** Street-level view down the Chidori red-light alley at night: an era-correct boxy taxi in the foreground with headlights on and a lit lantern lashed to its roof rack, a masked driver at the wheel, one passenger figure beside it. Both sides are OPEN doorways — glowing interiors, lit paper lanterns strung overhead, blank red/amber blade signs. Warm light spills from interiors; the dust thins enough for the signs to read.

**HOW IT REFLECTS THE SETTING:** This is the Chidori Neon Strip per the bible — multi-tiered, Gokuraku-kai-run, authored night, warm red/amber only, dust thinned enough for blade signs to cut through. The drive-up economy is honored: the taxi is the sovereign ground, the driver and passenger are inside it or at its doors, nobody is loitering in the open street. Character law is honored — every visible figure is masked.

**WHY THINGS ARE THE WAY THEY ARE:** The shops are OPEN because Chidori is an authored nightlife zone — the syndicate pays for the thinning and the lighting. The lantern on the taxi's roof rack is the cabbie's advertisement for hire in a district where foot-hailing is impossible. The two figures by the taxi are a fare exchange in progress: client boards, driver stays in the vehicle. Nothing stands unexplained; every body has a job.

**VERDICT: PASS**

## `impl-chidori.png` — REWORKED (2026-10-05)

**WHAT WAS WRONG (Craig's finding):** The original impl-chidori was the taxi-street image he flagged: shuttered, closed storefronts, but three masked women standing unexplained on the sidewalks in dark dresses, lanterns lit over a dead street. Under the bible this is world-building malpractice — the Kuro-Kiri ordinance makes unsuited foot-loitering a felony, dust ruins exposed clothing, and shuttered shops contradict Chidori's authored night. It read neither as a red-light district (no appeal, no economy) nor as a coherent lockdown (lanterns lit over nothing). Unexplained eeriness — a defect.

**WHAT'S DEPICTED (new image, verified by opening it):** The Chidori alley reworked as a legible, drive-up red-light district. A taxi waits head-on at center, queued at a sealed drive-through exchange booth where a masked attendant leans from the window to serve it — the cab never opens its doors to the street. Lit paper lanterns string overhead; red/amber blade signs glow through the dust. On both sides, OPEN doorways spill warm light: floor-to-ceiling sealed display windows behind which masked hostesses in ornamental respirators stand — visible THROUGH glass, never on the sidewalk. The street itself is empty of pedestrians.

**HOW IT REFLECTS THE SETTING:** Chidori's authored night (Gokuraku-kai, warm red/amber only, blade signs cutting through thinned dust) is intact. The drive-up economy is now the point of the image: vice happens through sealed glass and service booths because the air is hostile to lungs. The hostesses' ornamental respirators fold the character law into the district's own aesthetic — the mask IS the costume. This turns the Kuro-Kiri restriction into an alluring, claustrophobic design language rather than an error.

**WHY THINGS ARE THE WAY THEY ARE:** Nobody stands on the street because the street is the vehicular channel — standing there would be a felony under Kuro-Kiri. The attendant exists to transact with the queued taxi (drive-through counters per the fake-life rules). The hostesses are behind display glass because a red-light district that can't use the street uses the window instead — they are the visible goods, safely sealed. Every figure is explained; nothing is decorative atmosphere at the cost of canon.

**VERDICT: REWORKED** — Gemini pressure-test (attack on the original) confirmed the defect and picked the red-light-district rework over the lockdown option; new image generated via gemini-imagegen and verified by the worker's own eyes.

## `mock-kamome.png` — PASS

**WHAT'S DEPICTED:** A dust-hauler rig — a dust-armored freight truck with orange chevron markings — drives toward the viewer through a sealed refinery gate arch into the Shinkai basin, flare stacks and industrial towers rising behind it in the orange haze.

**HOW IT REFLECTS THE SETTING:** Shinkai is the basin refinery zone; the dust as visibility wall is literal here (the rig emerges from haze). The industrial economy of the Lower Trench — bulk goods in and out by road — is the whole reason the game needs trucks. No people at all: a machine image, which sidesteps every figure rule by construction.

**WHY THINGS ARE THE WAY THEY ARE:** The rig is approaching the gate because refineries take bulk deliveries by road convoy — that is the economy. The gate arch exists because refinery perimeters are sealed and guarded. There is no driver visible because the cab is sovereign ground and the wheelman never leaves the vehicle; in a gate approach the correct thing for the driver to be is invisible inside the cab.

**VERDICT: PASS**

## `mock-kotobuki.png` — PASS

**WHAT'S DEPICTED:** Under the expressway deck, a chop-shop bay: a muscle car on jack stands, surrounded by three masked mechanics — one crouched washing parts in a basin, one standing over the engine bay, one seated working on the side. Tool tables, parts bins, a work lamp. The deck piers frame the space.

**HOW IT REFLECTS THE SETTING:** Kotobuki is the workshop district — the Dust Tithe economy made visible: keeping a car breathing in the dust is a recurring cost, so the mechanics' trade is the Lower Trench's bread. All figures masked (respirators under hoods). The bay is enclosed under the deck — sheltered work, not open-street loitering.

**WHY THINGS ARE THE WAY THEY ARE:** Every figure has a job: parts-washing, engine work, chassis work — three stations of one repair. They are indoors-in-effect (the deck is their roof), which is why they can be on foot without violating the spirit of Kuro-Kiri: they are at work in a workplace, not wandering the street. The car is on stands because the bay does heavy service, not just wash-and-go.

**VERDICT: PASS**

## `mock-shinkai.png` — PASS

**WHAT'S DEPICTED:** Refinery haul road: a dust-armored hauler approaches through the refinery gate, flare stacks burning off in the background, industrial towers in orange haze. A sealed checkpoint booth at the gate.

**HOW IT REFLECTS THE SETTING:** Same Shinkai logic as mock-kamome — bulk industrial economy, dust as visibility wall, sealed perimeter. No figures on foot; the booth is the fake-life fixture (manned post, static).

**WHY THINGS ARE THE WAY THEY ARE:** The hauler is mid-approach to the gate because that's the refinery's intake rhythm. The gate and booth exist to control and meter industrial traffic. No pedestrians because there is nothing in a refinery approach a pedestrian would survive — the scene is vehicles and infrastructure only, which is exactly correct.

**VERDICT: PASS**

## `mock-tenjin.png` — PASS

**WHAT'S DEPICTED:** The Tenjin transit canyon: a wide avenue between brutalist towers, a Solari-style departure gantry spanning the road with split-flap boards and arrow signals, era-correct sedans queued in lanes, kōban (police-box) booths on both sidewalks with seated keepers visible inside, red banners on the facades.

**HOW IT REFLECTS THE SETTING:** Tenjin is the ordered civic canyon — transit authority, signage, enforcement. The kōban booths are the fake-life fixture done right: static masked figures in sealed posts. The Solari gantry is transit information made monumental. Dust thins enough for the canyon to read; the palette stays Lower Trench orange.

**WHY THINGS ARE THE WAY THEY ARE:** The keepers are seated INSIDE their booths — that is their post, the only legal way to be a person on this street. The sedans queue because Tenjin meters traffic through the gantry. The banners mark civic authority, not commerce. Nobody walks the avenue because the avenue is for cars.

**VERDICT: PASS**

## `impl-kamome.png` — PASS

**WHAT'S DEPICTED:** A market alley: a yellow kei van parked center, market stalls with awnings on both sides, crates of goods, three masked stall-hands in work clothes and caps — one at a stall on the left, two on the right, one mid-arranging produce.

**HOW IT REFLECTS THE SETTING:** Kamome is the market district — the drive-up economy's retail face: stalls serve vehicles and the van is the delivery unit. Character law honored (all masked). The van is era-correct and dust-worn.

**WHY THINGS ARE THE WAY THEY ARE:** The stall-hands are at their stalls — that is their workplace; they are staff, not pedestrians. The van is parked at the alley's center because market alleys load and unload by vehicle. The crates are the goods in motion. Every figure is explained by employment; the alley is a workplace, not a promenade.

**VERDICT: PASS**

## `impl-kotobuki.png` — PASS

**WHAT'S DEPICTED:** Under the expressway deck, a chop-shop bay: a car on jack stands, four masked mechanics around it, a welding spark burst from the left bay, tire stacks, oil drums, corrugated work shacks.

**HOW IT REFLECTS THE SETTING:** The Kotobuki workshop economy in implementation style — the Dust Tithe made visible (vehicles need constant service to survive the dust). Figures masked, sheltered under the deck.

**WHY THINGS ARE THE WAY THEY ARE:** The four mechanics are the shop crew mid-repair on a lifted car — one welding (the spark), the others spotting and prepping. They are on foot because the bay is their enclosed workplace. The tire stacks and drums are the consumables of the trade. Nothing is atmospheric filler; it is a working bay, fully staffed.

**VERDICT: PASS**

## `impl-tenjin.png` — PASS

**WHAT'S DEPICTED:** The Tenjin canyon in implementation style: sedans queued through the avenue, kōban booths on both sidewalks, a large gantry sign overhead, towers closing in, dust haze softening the distance.

**HOW IT REFLECTS THE SETTING:** Tenjin's civic order — metered traffic, signage, enforcement posts — translated to the achievable in-engine look. No figures on the street; the booths carry the human presence as sealed fixtures.

**WHY THINGS ARE THE WAY THEY ARE:** The cars queue because the gantry meters them. The booths are manned because Tenjin is a policed corridor. The absence of pedestrians is the point: this is a transit artery, and the Kuro-Kiri ordinance keeps it one. The haze at the vanishing point is the dust visibility wall doing its compositional job.

**VERDICT: PASS**

---
---

# CHAPTER 2 — FACTIONS

## `mock-kaiun-checkpoint.png` — PASS

**WHAT'S DEPICTED:** Two Kaiun dock enforcers in heavy work gear and respirators stand flanking a checkpoint under a canvas banner reading "DOCKERS' SYNDICATE — CHECKPOINT —", container stacks towering on both sides, orange dust light.

**HOW IT REFLECTS THE SETTING:** The Kaiun-gumi are the dockworkers' syndicate — civilian origins, muscle-first, controlling what moves through the Daikoku piers. The checkpoint is how a syndicate taxes trade: a banner, two enforcers, a chokepoint. Character law honored.

**WHY THINGS ARE THE WAY THEY ARE:** The two enforcers are the checkpoint's staff — they stand there because the checkpoint is their post; the banner announces whose toll this is. They are on foot because a checkpoint is a fixed installation they man, the classic permitted exception to the no-loitering rule. (English banner text is the text-audit worker's lane — not judged here.)

**VERDICT: PASS**

## `impl-kaiun-checkpoint.png` — PASS

**WHAT'S DEPICTED:** Two Kaiun enforcers in orange coveralls and boxy respirator hoods stand at a steel checkpoint gantry between container walls, a hanging banner with the syndicate hook-mark, work lamps lit.

**HOW IT REFLECTS THE SETTING:** The same syndicate checkpoint in implementation style — the faction's visual identity (hook-mark, orange coveralls) carried into the achievable look. The container canyon is the Daikoku piers' architecture.

**WHY THINGS ARE THE WAY THEY ARE:** The enforcers man the gantry — fixed post, permitted on-foot presence. The lamps are lit because checkpoints run around the clock. The banner marks territory. Nothing unexplained; the whole image is one checkpoint doing its job.

**VERDICT: PASS**

## `mock-kanzaki-mask.png` — PASS

**WHAT'S DEPICTED:** Portrait of Madame Kanzaki in her velvet office above the Starlight Lounge: a lacquered black mask with a painted red smile and glowing amber eyes, ornate dark gown, cigarette held in a long holder with smoke curling, red velvet booth seating, warm lamps, a blurred couple in the background lounge.

**HOW IT REFLECTS THE SETTING:** Kanzaki runs the Gokuraku-kai's Chidori operation — the authored night has an author, and she is it. The mask is character law elevated to status symbol: the painted smile is branding, not a face. The office-above-the-club geography matches the bible's multi-tiered Chidori.

**WHY THINGS ARE THE WAY THEY ARE:** She is in her office because it overlooks her floor — the blurred couple in the background is the club operating below her. The cigarette holder exists so she can smoke through the mask's filter slot — the detail that proves the mask is a respirator first, ornament second. She is seated and still because power in this city does not walk the street.

**VERDICT: PASS**

## `mock-kmted-cruiser.png` — PASS

**WHAT'S DEPICTED:** A KMTED patrol cruiser (white sedan, light bar, door markings) on a factory-district road, two masked officers visible through the windshield, and the Meter Maid on her yellow scooter alongside writing a ticket. Smokestacks and factory blocks in the haze.

**HOW IT REFLECTS THE SETTING:** The KMTED are the traffic authority — the faction that meters and fines the drive-up economy. The cruiser is their instrument; the Meter Maid is their street-level arm. Officers stay in the vehicle (cab is sovereign ground, even for police).

**WHY THINGS ARE THE WAY THEY ARE:** The officers are in the cruiser because patrol is vehicular. The Meter Maid is on her scooter because ticketing is done vehicle-to-vehicle — she rides alongside, writes the ticket, never dismounts into traffic. The factory backdrop places the patrol in the industrial belt where heavy vehicles need metering. Every figure is on duty, in or on a vehicle.

**VERDICT: PASS**

## `impl-kmted-cruiser.png` — PASS

**WHAT'S DEPICTED:** A KMTED cruiser at a kōban booth at night, one officer standing at the booth, the Meter Maid on her scooter with arm raised holding a ticket book, the cruiser's light bar casting red glow.

**HOW IT REFLECTS THE SETTING:** Traffic enforcement in implementation style — the booth is the fixed post, the scooter is the mobile arm, the cruiser is the authority's body. Dust haze, night lighting, all masked.

**WHY THINGS ARE THE WAY THEY ARE:** The officer is at the booth because it is his post. The Meter Maid's raised arm is the ticketing gesture — the whole reason she exists in the fiction. The light bar is on because a stop is in progress. Nobody is on foot in the roadway; the one standing figure is at the booth, the permitted fixed post.

**VERDICT: PASS**

## `mock-ironwheel-garage.png` — PASS

**WHAT'S DEPICTED:** The Iron Wheel Union garage under the expressway: five masked mechanics around a kei van with its engine bay open — one welding (spark burst), one holding work, one observing, tire walls stacked high on both sides, a checkered banner strung overhead.

**HOW IT REFLECTS THE SETTING:** The Iron Wheel Union are the mechanics' syndicate — civilian origins, the people who keep the Dust Tithe economy running. The garage under the deck is their hall: sheltered, collective, union-marked.

**WHY THINGS ARE THE WAY THEY ARE:** All five are the shop crew mid-job — welding, holding, fitting, supervising. They are on foot because the garage is their enclosed workplace. The tire walls are the union's stockpile (tires are consumables in the dust). The banner marks union territory. A full crew, fully employed, no spectators.

**VERDICT: PASS**

## `impl-ironwheel-garage.png` — PASS

**WHAT'S DEPICTED:** Three union mechanics in coveralls and respirators around a red-and-yellow panel van raised on a scissor lift under the expressway, an "IRON WHEEL UNION" banner overhead, tire stacks, steam venting.

**HOW IT REFLECTS THE SETTING:** The union garage in implementation style — the achievable in-engine version of the workshop. (The chapter already flags one mis-sided sleeve chevron — the grounding/text lane's note, not a plausibility defect.)

**WHY THINGS ARE THE WAY THEY ARE:** The van is on the lift because it is mid-service; the three mechanics are the crew on that job. The banner marks the union hall. Steam and tire stacks are the working environment. All figures are staff at work in an enclosed bay.

**VERDICT: PASS**

## `mock-american-depot.png` — PASS

**WHAT'S DEPICTED:** A surplus depot: three soldiers in olive fatigues and respirators among olive-drab jeeps and trucks with white star markings, Quonset huts behind a chain-link fence, a PX-style stall with stacked goods to the right.

**HOW IT REFLECTS THE SETTING:** PROPOSED (not yet canon) — the American army camp presence in the outskirts, the bible's one sanctioned context for English markings. The depot is where surplus military hardware leaks into the civilian economy — the plausible source of the game's tougher vehicles.

**WHY THINGS ARE THE WAY THEY ARE:** The soldiers are depot staff — one leaning on a jeep (motor-pool duty), two walking the yard (perimeter/stock duty). They are on foot because a fenced depot yard is a controlled military installation, not a public street. The PX stall is the depot's retail leak — surplus goods sold to drivers without leaving the fence. (Flagged PROPOSED in the chapter; plausibility holds if the faction is canonized.)

**VERDICT: PASS** (as a proposed faction piece; canon status is the chapter's open question, not a figure-plausibility issue)

---
---

# CHAPTER 3 — FLEET & GEAR

All eight images are vehicle/gear studies with no human figures. Plausibility for this chapter is about the machines and kit belonging to the economy — which they do, uniformly.

## `mock-hinode-carrier.png` — PASS

**WHAT'S DEPICTED:** The Hinode Carrier starter cab — a two-tone orange/cream sedan with a roof rack loaded with luggage and a "VACANT" taxi sign, a hood-mounted spotlight, era-correct boxy proportions, photographed against a neutral backdrop with faint industrial silhouettes.

**HOW IT REFLECTS THE SETTING:** This is the player's first sovereign ground — the cab as home, office, and armor. The roof rack and luggage mark it as a working hire car; the VACANT sign is the drive-up economy's handshake; the spotlight is the dust-visibility answer. Era-correct sedan per the style bar.

**WHY THINGS ARE THE WAY THEY ARE:** No driver is shown because the wheelman is the player — the cab is presented empty the way a character-creation screen presents a class. The luggage is on the rack because the cab carries its life with it. The spotlight is hood-mounted because the dust swallows stock headlights.

**VERDICT: PASS**

## `impl-hinode-carrier.png` — PASS

**WHAT'S DEPICTED:** The Hinode Carrier in implementation style — low-poly showroom turntable view, two-tone paint, TAXI sign, roof-rack cargo, plain studio backdrop.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine version of the starter cab — proof the reference mock survives translation to Godot/low-poly constraints. Same kit, same read.

**WHY THINGS ARE THE WAY THEY ARE:** Showroom presentation because this is the implementation reference — clean geometry, readable silhouette, the exact prop load the game will spawn. No driver, same reason as the mock: the cab awaits its player.

**VERDICT: PASS**

## `mock-ohtori-sovereign.png` — PASS

**WHAT'S DEPICTED:** The Ohtori Sovereign — a long executive limousine in two-tone cream/purple, armored, V12 turbo-diesel per the spec block, presented as a studio side-profile with dimensions.

**HOW IT REFLECTS THE SETTING:** The Upper Aerium's answer to the cab: executive transport for the stratum that lives above the dust. Armored chassis because even the rich travel through the Trench to reach their elevators. (Spec text is the text-audit lane's business.)

**WHY THINGS ARE THE WAY THEY ARE:** Studio profile because this is a design spec sheet — the image's job is to fix proportions, not to stage a scene. No figures because it is a machine document.

**VERDICT: PASS**

## `mock-goliath-800.png` — PASS

**WHAT'S DEPICTED:** The Goliath 800 — a heavy orange crane-truck with boom, winch, and cargo bed, presented as an annotated concept sheet with part callouts, harbor cranes in the background haze.

**HOW IT REFLECTS THE SETTING:** The heavy-industry end of the fleet — the machine that loads what the haulers carry, the reason the Daikoku piers function. Annotated because it is a working design document.

**WHY THINGS ARE THE WAY THEY ARE:** Callouts exist because the art team needs to know what each assembly is. The harbor backdrop places its workplace. No figures — machine document.

**VERDICT: PASS**

## `impl-goliath-800.png` — PASS

**WHAT'S DEPICTED:** The Goliath 800 in implementation style — the crane-truck in flat dusty light, containers behind, simplified geometry for the engine.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine heavy rig — the implementation layer doing its stated job.

**WHY THINGS ARE THE WAY THEY ARE:** Simplified forms and flat lighting because this is the polygon budget made visible. No figures — machine document.

**VERDICT: PASS**

## `mock-cargo-lashing.png` — PASS

**WHAT'S DEPICTED:** A roof-rack cargo still life: wicker baskets, stenciled crates (FRAGILE, EXPORT), brass canisters, a red jerry can, rope lashing with proper knots, a canvas tarp — the whole vocabulary of carried goods.

**HOW IT REFLECTS THE SETTING:** Cargo is the game's verb — deliveries are the gig economy. This image is the prop bible for what "loaded" looks like: lashed, mixed, improvised, heavy. The rope work matters because unsecured cargo in the dust is lost cargo.

**WHY THINGS ARE THE WAY THEY ARE:** Every item is lashed because the city's roads shake loads apart — the knots are the honest detail. Mixed cargo types (baskets, crates, canisters) because a gig driver takes whatever pays. No figures — prop document.

**VERDICT: PASS**

## `impl-cargo-lashing.png` — PASS

**WHAT'S DEPICTED:** Implementation-style cargo props: a braced crate frame, a lidded canister, a glowing orb device in a case, a red jerry-can set — simplified geometry prop sheet.

**HOW IT REFLECTS THE SETTING:** The in-engine prop set for cargo — the same vocabulary at the achievable fidelity.

**WHY THINGS ARE THE WAY THEY ARE:** Prop sheet because the engine needs discrete spawnable items. Simplified because these are background/foreground dressing, not hero assets. No figures — prop document.

**VERDICT: PASS**

## `mock-driver-gear.png` — PASS

**WHAT'S DEPICTED:** A flat-lay of the wheelman's kit on wood: respirator mask, goggles, leather gloves, peaked cap with wheel-and-wings badge, fare meter, route punch-cards, coin dish of fare tokens, a small fan, a tire iron.

**HOW IT REFLECTS THE SETTING:** This is the character law made personal — the mask and goggles are not costume, they are the uniform of survival. The fare meter and punch-cards are the cash/Sol-88 gig economy in objects. The fan and gloves are the Dust Tithe in miniature — the cab's climate is the driver's whole world.

**WHY THINGS ARE THE WAY THEY ARE:** Flat-lay because this is the player's loadout screen made physical — every item is something the driver touches every shift. The respirator is centered because it is the single most important object in the city. No figure because the kit IS the portrait — the driver is whoever wears it.

**VERDICT: PASS**

---
---

# CHAPTER 4 — OUTSKIRTS

## `mock-viaduct-sea.png` — PASS

**WHAT'S DEPICTED:** The coastal viaduct: a long concrete ribbon on piers curving along a cliffed coast, a tanker rig crossing it, the city skyline faint across the water, pine forest and mountains behind.

**HOW IT REFLECTS THE SETTING:** The Nagisa Outskirts are the city's lungs — outside the dust wall, the palette breaks to blue-green and the air clears. The viaduct is the umbilical: the only road in and out, carrying fuel and goods between the city and the coast.

**WHY THINGS ARE THE WAY THEY ARE:** The rig is on the viaduct because that is the freight artery — everything the city burns or eats crosses this ribbon. No figures because there is nowhere for a person to be on a viaduct except inside a vehicle. The clear air is the geographic fact the whole setting is built around.

**VERDICT: PASS**

## `impl-viaduct-sea.png` — PASS

**WHAT'S DEPICTED:** The viaduct in implementation style: a red tanker rig on the curving deck, low-poly pines, faceted cliffs, the skyline across the water.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine version of the outskirts artery — the same clear-air palette break, the same freight logic.

**WHY THINGS ARE THE WAY THEY ARE:** The rig is the scale reference and the economic reason for the road. Simplified pines and cliffs because the outskirts are vista geometry. No figures — a road with no sidewalks needs none.

**VERDICT: PASS**

## `mock-waystation-dusk.png` — PASS

**WHAT'S DEPICTED:** The Iron Wheel waystation at dusk: a concrete fuel block with a chalkboard (viaduct wind/axle-limit/radio-frequency notes), two masked mechanics in coveralls by the diesel pump, rigs parked under the canopy, a brazier burning, union flags.

**HOW IT REFLECTS THE SETTING:** The waystation is the outskirts' service node — fuel, information, and shelter at the halfway point, run by the Iron Wheel Union. The chalkboard is the driver's internet: conditions, limits, frequencies. (Board text is the text-audit lane's business.)

**WHY THINGS ARE THE WAY THEY ARE:** The two mechanics are the station crew — one at the pump (fueling), one beside (assisting) — staff at their post, the permitted on-foot presence. The brazier burns because dusk at altitude is cold and the station is a rest stop. The rigs are parked because drivers stop here the way sailors stop at a lighthouse.

**VERDICT: PASS**

## `impl-waystation-dusk.png` — PASS

**WHAT'S DEPICTED:** The waystation in implementation style: a small fuel block, one masked attendant at the pump with a box truck, brazier, flagpole, simplified geometry.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine service node — same function, lower fidelity.

**WHY THINGS ARE THE WAY THEY ARE:** The single attendant is the duty crew — one person runs the pump at this hour. The truck is being fueled because that is the station's entire purpose. The brazier and flags carry the identity at low cost.

**VERDICT: PASS**

## `mock-fishing-harbor.png` — PASS

**WHAT'S DEPICTED:** The fishing harbor: moored boats, stacked crates and winches on the quay, warehouses, and two masked fishermen in oilskins and caps hauling a line on a boat's stern.

**HOW IT REFLECTS THE SETTING:** The Nagisa coast's working edge — the food economy that doesn't depend on the city's dust-choked logistics. The quay is cluttered with the tools of the trade because this is a workplace, not a vista.

**WHY THINGS ARE THE WAY THEY ARE:** The two fishermen are hauling a line because that is the job — they are crew on a working boat, the classic permitted on-foot presence (on a vessel, at work). The crates and winches are the catch-handling chain. The warehouses store what the boats land.

**VERDICT: PASS**

## `impl-fishing-harbor.png` — PASS

**WHAT'S DEPICTED:** The harbor in implementation style: quay, sheds, water tanks, moored boats, two small figures by a skiff.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine harbor — the working coast at game fidelity.

**WHY THINGS ARE THE WAY THEY ARE:** The two figures are boat crew at the skiff — crew at work on a vessel. The tanks and sheds are the harbor's infrastructure. Same logic as the mock, simplified.

**VERDICT: PASS**

## `mock-switchback.png` — PASS

**WHAT'S DEPICTED:** Mountain switchbacks above the sea: a tanker rig descending the hairpins, pine forest, rock faces, guardrails, the sea and horizon beyond.

**HOW IT REFLECTS THE SETTING:** The outskirts' driving fantasy — the road as the destination. This is the route the GPS plans around: fuel, gradient, and the long way home. Clear air, blue palette, the city's opposite.

**WHY THINGS ARE THE WAY THEY ARE:** The rig is on the switchbacks because the coast road is the freight route around the mountain — no alternative exists. No figures because a mountain road has no sidewalks and the driver belongs in the cab. The guardrails and mirrors are the road furniture that makes the descent survivable.

**VERDICT: PASS**

---
---

# CHAPTER 5 — UPPER CITY

## `mock-1-skyway-ribbon.png` — PASS

**WHAT'S DEPICTED:** The skyway ribbon: an elevated expressway curving between two concrete residential towers, green directional signs on gantries, empty lanes, facade details (vents, pipes, bolt patterns), pale blue sky.

**HOW IT REFLECTS THE SETTING:** The Upper Aerium is the city above the dust — clean air, pale light, infrastructure as architecture. The skyway is how the upper stratum moves without touching the Trench. The empty lanes are honest: this is a road portrait, not a traffic scene.

**WHY THINGS ARE THE WAY THEY ARE:** No vehicles and no figures because the image's job is the road's geometry — the ribbon itself is the subject. The signs and gantry furniture prove it is a working road, not a sculpture. (Sign text is the text-audit lane's business.)

**VERDICT: PASS**

## `impl-1-skyway-ribbon.png` — PASS

**WHAT'S DEPICTED:** The skyway in implementation style: two towers, the curving deck, a few black sedans in the lanes, green gantry signs, low-poly facades.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine skyway — the upper-city driving surface the player will actually use.

**WHY THINGS ARE THE WAY THEY ARE:** The sedans are there to prove the lanes work at game scale — traffic, not portraiture. No figures because the Aerium's people are inside buildings and vehicles; the street level of the upper city is not a pedestrian realm in this fiction.

**VERDICT: PASS**

## `mock-2-haibara-estate.png` — PASS

**WHAT'S DEPICTED:** The Haibara estate: a walled villa with tiled roofs and a pruned pine, perched on a stone bastion above a sea of dust-clouds, pale sky.

**HOW IT REFLECTS THE SETTING:** The Aerium's thesis in one image — wealth as altitude. The estate sits above the dust the way the whole upper city does; the cloud-sea is the Trench's atmosphere seen from the winning side. The walled garden is seclusion made architecture.

**WHY THINGS ARE THE WAY THEY ARE:** No figures because the estate's power is in its emptiness — it is a fortress of privacy, and staff would be inside. The pine and tiles are the Showa-rooted domestic architecture the grounding worker traces; the altitude is the class statement.

**VERDICT: PASS**

## `impl-2-haibara-estate.png` — PASS

**WHAT'S DEPICTED:** The estate bastion in implementation style: stone wall, villa roofline, pine, the dust-sea rendered as flat bands.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine version of altitude-as-wealth — the same class statement at game fidelity.

**WHY THINGS ARE THE WAY THEY ARE:** No figures, same reason as the mock: the estate is a sealed property. The flattened dust bands are the honest low-poly translation of the cloud-sea.

**VERDICT: PASS**

## `mock-3-terminal-1.png` — PASS

**WHAT'S DEPICTED:** Terminal 1: a vehicle elevator tower — a tall concrete shaft with open parking decks full of cars, a cage lift hoisting a taxi up the side on cables, toll booths and a Solari board at the base, tiny figures on the observation balcony and bridge.

**HOW IT REFLECTS THE SETTING:** The sky elevators are the city's vertical transit — cars go up, people stay in them. The terminal is the airport of this fiction: queuing, signage, the machinery of ascent. The tiny balcony figures are observers, not pedestrians.

**WHY THINGS ARE THE WAY THEY ARE:** The figures are on the balcony and bridge — elevated, railed, unreachable perches, the bible's permitted placement for static people. They are observers because a terminal is a place people watch machines work. The cage lift carries a taxi because vehicles ascend; drivers ride inside. The Solari board is the departure logic made visible.

**VERDICT: PASS**

## `impl-3-terminal-1.png` — PASS

**WHAT'S DEPICTED:** Terminal 1 in implementation style: the elevator shaft with stacked parking decks, cars on every level, a Solari board at the base, small masked figures queuing at the entrance.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine terminal — the vertical transit hub at game fidelity.

**WHY THINGS ARE THE WAY THEY ARE:** The small figures are queuing at the entrance — a managed line at a staffed gate, the permitted form of pedestrian presence (directed, purposeful, at a threshold). The stacked cars are the terminal's inventory. The Solari board is the information fixture.

**VERDICT: PASS**

## `mock-4-corporate-plaza.png` — PASS

**WHAT'S DEPICTED:** The corporate toll plaza: a row of era-correct executive sedans queued at toll booths, Solari gantries with fare boards, a flag-bedecked headquarters tower behind, a few attendants at the booths, hedges and paving in pale light.

**HOW IT REFLECTS THE SETTING:** This is the style/plausibility bar for the whole book — Craig's reference image. The Aerium's order made ceremonial: metered access, uniformed attendants, the corporation's flag over the gate. Every element has a job.

**WHY THINGS ARE THE WAY THEY ARE:** The sedans queue because the plaza meters entry to the corporate zone. The attendants are at their booths — fixed posts. The flags mark whose gate this is. The hedges are the Aerium's luxury: greenery is the one thing the Trench can't afford. Nothing is unexplained because the composition was built around the transaction.

**VERDICT: PASS** — the bar the rest of the book is held to.

## `mock-5-cloudbreak-vista.png` — PASS

**WHAT'S DEPICTED:** The cloudbreak vista: the Aerium's tower cluster ringed by an orbital roadway, rising from the dust-cloud sea, a gantry crane-tower at the center, pale sun.

**HOW IT REFLECTS THE SETTING:** The upper city's master shot — the ring road, the towers, the dust below. The city as a machine for living above the problem.

**WHY THINGS ARE THE WAY THEY ARE:** No figures because this is a planning-model view — the city as diagram. The ring road is the Aerium's circulatory system; the central tower is the elevator hub. The dust-sea below is the reason everything is up here.

**VERDICT: PASS**

---
---

# CHAPTER 6 — WORLD LORE

## `mock-dust-tithe.png` — PASS

**WHAT'S DEPICTED:** A rinse station under the expressway: a masked attendant in coveralls scrubbing a red sedan's windshield with a brush and hose, water sheeting off, a second masked figure at the booth window handling payment, barrels and corrugated shacks around.

**HOW IT REFLECTS THE SETTING:** The Dust Tithe made literal — the recurring rinse cost every vehicle pays to keep moving. The booth is the transaction point; the attendant is the tithe's collector in work clothes. This is the economy's most honest image.

**WHY THINGS ARE THE WAY THEY ARE:** The attendant scrubs because dust blinds windshields — the service is survival, not luxury. The second figure is at the booth because the rinse is a paid transaction (cash/Sol-88). The barrels are the water stock — water is the tithe's currency. Both figures are staff at their workplace.

**VERDICT: PASS**

## `impl-dust-tithe.png` — PASS

**WHAT'S DEPICTED:** A "WASH & GO!" rinse bay in implementation style: a masked attendant pressure-washing a red taxi under a corrugated canopy, barrels alongside, the expressway deck above.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine Dust Tithe — the same transaction at game fidelity. (The English sign is the text-audit lane's business.)

**WHY THINGS ARE THE WAY THEY ARE:** The attendant washes because the taxi must stay in service — a working cab pays the tithe daily. The canopy is the bay's shelter. The barrels are the water stock. One attendant, one job, no bystanders.

**VERDICT: PASS**

## `mock-elevator-build.png` — PASS

**WHAT'S DEPICTED:** A sky-elevator tower under construction: a concrete core wrapped in red steel bracing, tower cranes on both sides hoisting loads, small worker figures on the ground, at the scaffold levels, and on balconies.

**HOW IT REFLECTS THE SETTING:** The city's vertical ambition under construction — the elevators are how the Aerium was built and how it grows. The red bracing is the construction-phase identity; the cranes are the scale reference.

**WHY THINGS ARE THE WAY THEY ARE:** The workers are construction crew — on the ground (material handling), on the scaffolds (assembly), on the balconies (supervision). A building site is the definitive permitted on-foot workplace: everyone is staff, everyone has a station, the site is enclosed. The cranes hoist because the tower is assembled from lifted modules.

**VERDICT: PASS**

## `impl-elevator-build.png` — PASS

**WHAT'S DEPICTED:** The elevator tower in implementation style: simplified concrete shaft, red bracing, two cranes, a few ground-crew figures at the base.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine construction site — same vertical ambition, lower fidelity.

**WHY THINGS ARE THE WAY THEY ARE:** The ground crew are the site staff at the material-handling level. The cranes are the assembly method. Simplified because the tower is background architecture at game distance.

**VERDICT: PASS**

## `mock-sea-night.png` — PASS

**WHAT'S DEPICTED:** Night at sea: two figures in a small boat — one standing in a coat and cap, one seated in a hooded oilskin with a respirator — looking out at offshore refinery platforms with flare stacks burning on the horizon, teal water, stars.

**HOW IT REFLECTS THE SETTING:** The Shinkai basin's offshore face — the refineries that feed the city's industry, seen from the water at night. The flares are the industry's signature: burning off gas around the clock. The respirator on the seated figure is the character law reaching even the sea.

**WHY THINGS ARE THE WAY THEY ARE:** The two are a night boat crew — the bible's fishers run night shifts when the sea air clears; they are on a vessel, at work, the permitted presence. They face the platforms because the flares are the landmark and the workplace. The boat is small because the near-shore fleet is small craft.

**VERDICT: PASS**

## `impl-sea-night.png` — PASS

**WHAT'S DEPICTED:** The night sea in implementation style: two figures in a boat (one standing, one seated in a respirator and hood), four flare platforms on the horizon, stylized wave bands.

**HOW IT REFLECTS THE SETTING:** The achievable in-engine night sea — same offshore industry, same crew logic.

**WHY THINGS ARE THE WAY THEY ARE:** The crew are on the boat because it is their workplace; the seated figure's respirator is the character law. The platforms are the destination/market they work around. Stylized waves because the sea is a shader surface at game fidelity.

**VERDICT: PASS**

## `mock-worldmap.png` — PASS

**WHAT'S DEPICTED:** The world map illustration: the Upper City on its elevator platform above the dust, the Sky Elevators' shafts descending through the cloud layer, Daikoku Piers with container cranes, the Kamome market blocks, Tenjin's towers, the Shinkai Basin's refinery stacks, the Panel Fields' solar rafts, Mt. Kurogane and the Nagisa Coast with the switchback road — every district labeled.

**HOW IT REFLECTS THE SETTING:** The whole bible in one image — three strata, the districts, the elevator system, the dust layer as the literal divider between worlds. This is the map the GPS plans on.

**WHY THINGS ARE THE WAY THEY ARE:** Every district is shown because the map's job is orientation — the player needs to see where the gigs are. The dust band sits between the platform and the ground because that is the city's founding geography. No figures because it is a cartographic document. (Labels are the text-audit lane's business.)

**VERDICT: PASS**

---
---

# SUMMARY

| Chapter | Images | PASS | REWORKED |
|---|---|---|---|
| Lower City | 9 | 8 | 1 (`impl-chidori.png`) |
| Factions | 8 | 8 | 0 |
| Fleet & Gear | 8 | 8 | 0 |
| Outskirts | 7 | 7 | 0 |
| Upper City | 8 | 8 | 0 |
| World Lore | 7 | 7 | 0 |
| **Total** | **47** | **46** | **1** |

**The 12 `qa/kurogane-bay` mocks:** do not exist on disk (no such directory found anywhere in the workspace as of 2026-10-05). Not covered by this pass — they need their own plausibility review when produced.

**Method:** every image opened and judged by the worker's own eyes; Gemini (gemini-3.8-flash) used only to pressure-test the impl-chidori rework decision. Japanese/English text strings left untouched (text-audit lane); Showa roots left untouched (grounding lane).

**Standing rule applied throughout:** when in doubt, cut the figure or explain them — no unexplained bodies on the street. The one image that failed this rule (`impl-chidori.png`) was reworked, not patched with prose.
