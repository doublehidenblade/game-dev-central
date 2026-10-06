# SHOWA GROUNDING — art book reference-mock audit
### 2026-10-05 · Showa-grounding worker

**Craig (verbatim):** "some of the art references are not Japanese/showa enough. Seemed generic mad max. Again, do actual references like: what would this look like in showa era, then what would a retro-futuristic dust future look like for this."

**Method.** Every [REFERENCE] mock opened and judged by the chain:
**SHOWA REALITY** (the specific real thing it extrapolates from, with source) → **40 YEARS OF DUST** (what changed) → **THIS IMAGE**.
Period references I couldn't name myself were verified via the gemini-consult skill (gemini-3.8-flash, 2026-10-05; full notes in §6).

**Verdict key:** GROUNDED (chain holds) · REWORK (has a Showa root but the image drifted — regenerated) · CUT (no Showa root, generic Mad Max — removed).

## Summary

| Set | Images | GROUNDED | REWORK | CUT |
|---|---|---|---|---|
| art-book/lower-city | 5 | 4 | 1 (regenerated) | 0 |
| art-book/factions | 5 | 5 | 0 | 0 |
| art-book/fleet-gear | 5 | 5 | 0 | 0 |
| art-book/outskirts | 4 | 4 | 0 | 0 |
| art-book/upper-city | 5 | 5 | 0 | 0 |
| art-book/world-lore | 4 | 4 | 0 | 0 |
| mocks/ (qa/kurogane-bay: gig-city + gig-city-v2) | 12 | 12 | 0 | 0 |
| **Total** | **40** | **39** | **1** | **0** |

The book's Showa grounding is strong: 39 of 40 images hold their chains. The single failure was `mock-kotobuki.png` (an American muscle car in the chop shop) — regenerated 2026-10-05, now grounded. No CUTs: nothing in the book is rootless Mad Max; Craig's complaint traced to the one American car plus a few images whose roots were real but unnamed until this audit.

---

## 1. LOWER CITY (`art-book/lower-city/`)

### mock-kamome.png — GROUNDED
- **Showa reality:** Tsukiji outer-market alleys (築地場外市場), 1960s–80s — wooden shopfronts, vertical kanji 看板, kei vans (Suzuki Carry, in production since 1961), rope-lashed fish crates, hanging menu strips. Source: period photos of Tsukiji jōgai; extrapolation doc Photo 1 (shotengai storefront) signage-sediment law.
- **40 years of dust:** Enamel plates survive and thrive (sand-blasting keeps them legible); noren become weighted canvas dust flaps; the wet tarmac survives under the ochre murk (Kamome's signature read); kei van dust-caked but working.
- **Notes:** Flag for the character-law worker — several market workers read as unmasked faces (Showa grounding is fine; the mask law is a separate lane).

### mock-chidori.png — GROUNDED
- **Showa reality:** Showa 歓楽街 — 1960s–70s Kabukicho/Shinjuku pleasure quarters: vertical blade signs (袖看板), paper-lantern (提灯) rows, izakaya storefronts, a black Cedric/Crown-class taxi with fender mirror queued at the curb. Source: 1970s Kabukicho night photography.
- **40 years of dust:** Chidori is canon's neon exception — warm red/amber gas-discharge blades cut the amber murk; lantern wires carry the cable-canopy read; the taxi queue is fleet-cab canon.
- **Notes:** Some blade-sign lettering is gibberish — text-audit worker's lane. Two left-side figures read as unmasked — character-law flag.

### mock-kotobuki.png — REWORK (regenerated 2026-10-05, now GROUNDED)
- **Defect:** the car on stands was an American muscle car (Dodge Challenger-class long hood, quad lamps) — the only non-Japanese subject in the entire book, and the one image that justified Craig's "generic mad max" read.
- **Showa reality (restored):** 1970s Shuto-undercroft chop shops — Nissan Skyline C10 "Hakosuka" / C110 "Kenmeri", Fairlady Z S30, Toyota Celica Liftback TA27 on low-profile steel ramps and work pits; corrugated namiban (波板) lean-tos framed against raw concrete piers; oxy-acetylene torch rigs, oil drums, bias-ply tire racks; bare 40W fluorescent battens. Source: Gemini consult 2026-10-05.
- **40 years of dust:** the expressway deck soffit becomes the district's signature ceiling read; arc light retuned warm amber (resolves the §11 palette breach — the cobalt arc is gone); swept-dust piles, canvas dust flaps, cyclone intake on the Hakosuka's hood, caged headlights.
- **Rework notes:** regenerated via gemini-imagegen with the prompt leading on the Showa reference ("1970s Tokyo chop shop under the Shuto expressway, Nissan Skyline C10 'Hakosuka'… then 40 years of industrial dust"). Original preserved as `mock-kotobuki-v1-superseded.png`. The [IMPLEMENTATION] twin (`impl-kotobuki.png`) was translated from the muscle-car reference — it needs a follow-up pass to match the Hakosuka (owner: the production-translation worker, not this lane). Chapter §11 updated.

### mock-shinkai.png — GROUNDED
- **Showa reality:** Keihin industrial zone refineries (Kawasaki/Mizue-chō/Ukishima), 1960s–80s — flare stacks, spherical gas holders, distillation towers wrapped in pipe runs, pipeline gantries; Japanese cab-over tanker trucks. Source: Showa-era Keihin coastal industrial photography; extrapolation doc §5 (the earnestness of industry).
- **40 years of dust:** sulfur-yellow haze replaces the night sky; the hauler gets cyclone-filter roof canisters, caged headlights, enamel SOL-88 plates; flare stacks become the district's shift-clock.

### mock-tenjin.png — GROUNDED
- **Showa reality:** 1970s–80s Tokyo business districts (Marunouchi/Otemachi) + Shuto toll plazas — sheer board-formed concrete slabs, Solari split-flap departure boards (real: Japanese stations/airports used them), kōban police boxes, red nobori banners, boxy Mark II/Cedric-class sedans queuing at toll booths. Source: 1970s Marunouchi streetscapes; Shuto toll-gate photography.
- **40 years of dust:** the kōban becomes the dust-lock booth with the bribe-chute slot at bumper height (extrapolation doc §5.6); amber hazard beacons + painted iron intersection mirrors replace traffic lights; the Solari gantry clacks toll brackets.

---

## 2. FACTIONS (`art-book/factions/`)

### mock-kaiun-checkpoint.png — GROUNDED
- **Showa reality:** 1960s–70s Yokohama/Kobe dockworkers — tobi trousers (鳶ズボン), sandblasting hoods, cargo hooks as daily tools; the checkpoint banner on lashed poles is a festival-banner (幟) form. Source: Showa-era port-labor photography; Yamaguchi-gumi's 1915 dock-labor origins (energy, per chapter).
- **40 years of dust:** respirators replace tenugui; cargo hooks become bandolier armor (tools as uniform); sodium-orange canvas hi-vis.
- **Notes:** the "DOCKERS' SYNDICATE" English banner is text-audit's lane (banner form is Japanese; lettering is not).

### mock-kanzaki-mask.png — GROUNDED
- **Showa reality:** Showa-era Ginza cabaret culture + noh-mask aesthetics — lacquered urushi-black full-face mask with painted red smile, kimono robe with gold trim, velvet lounge; the club "mama-san" of 1960s–70s hostess clubs. Source: Ginza club photography; noh-mask (能面) craft tradition.
- **40 years of dust:** the mask becomes dust-protection rank insignia (plain black = footman, red smile = inner circle); the velvet lounge survives as Chidori's sealed interior.

### mock-ironwheel-garage.png — GROUNDED
- **Showa reality:** Showa-era kei-van repair shops — Subaru Sambar/Daihatsu Hijet-class vans on lifts, engine exposed, tire walls, oxy-acetylene welding, masked mechanics. (The van is the correct Japanese vehicle for this shop — compare mock-kotobuki's defect.)
- **40 years of dust:** expressway undercroft, welder's masks over respirators, checkered union banner as faction ID, filter-canister pyramids.

### mock-kmted-cruiser.png — GROUNDED
- **Showa reality:** Showa-era Japanese police — white/black Crown/Cedric patrol cars (パトカー) with mechanical roof beacons and push-bars; police scooters (Honda Super Cub-class) with white helmets; industrial-zone smokestacks. Source: 1970s Japanese police-vehicle photography.
- **40 years of dust:** officers in respirators + amber goggles; enforcement becomes bureaucratic (push-bars and paperwork, not guns); the cruiser is dust-beige, not panda-black.
- **Notes:** door lettering ("KMTED - TRAFFIC ENFORCEMENT") is text-audit's lane.

### mock-american-depot.png — GROUNDED
- **Showa reality:** US military presence in Showa Japan (Yokota/Yokosuka/Camp Zama) + Mitsubishi's licensed Willys Jeeps (built from 1953 into the 1990s, used by the JSDF) + post-war black markets (闇市 — Ameya-Yokocho in Ueno began as one). Quonset huts, chain-link, olive-drab trucks with US star roundels, canvas-awning stalls with salvaged cans.
- **40 years of dust:** the surplus depot becomes the gray-market parts economy; the yami-ichi stall sells filter cartridges and canned fuel.
- **Notes:** canon art rules allow English ONLY in American-army-camp contexts — this is one. Text on the trucks is text-audit's lane regardless.

---

## 3. FLEET & GEAR (`art-book/fleet-gear/`)

### mock-hinode-carrier.png — GROUNDED
- **Showa reality:** 1970s Japanese taxi — Nissan Cedric 330 / Toyota Crown class: fender mirrors (legally required in Japan until March 1983; taxi companies kept them after — Gemini consult 2026-10-05), illuminated rooftop andon fleet sign, two-tone fleet livery (Nihon Kotsu canary-yellow/red), lace seat covers over vinyl, mechanical 空車 flip-flag. Source: Gemini consult 2026-10-05.
- **40 years of dust:** conical cyclone intake on the hood (the bonnet-bus lineage, extrapolation doc §5.2, shrunk to cab scale), roof rack of spare filter canisters like ammunition, wire-caged headlights, dust caked on every horizontal surface.

### mock-ohtori-sovereign.png — GROUNDED
- **Showa reality:** Toyota Century (1967–, the imperial/state limousine) / Nissan President — fender mirrors, formal vertical-bar chrome grille, lace curtains (the Century's signature), deep imperial purple over cream reserved by taste for the top. Source: Century press photography, 1967–.
- **40 years of dust:** gasketed dust-proof body panels (rubber bead on every shut line), caged headlights, full-width vacuum-tube taillight bar recessed behind a washable lens; imperial purple is Upper-City-only by canon.

### mock-goliath-800.png — GROUNDED
- **Showa reality:** 1970s–80s Japanese truck-mounted cranes — Tadano TS-series / Kato NK-series with safety-orange booms on Nissan Diesel/Isuzu carriers; hazard striping on boom tips, hook blocks, and outriggers. Source: Gemini consult 2026-10-05 (confirms the orange-boom Showa construction look).
- **40 years of dust:** winch, push-bar grille, caged headlights, chained cargo on the flatbed, hazard chevrons.
- **Notes:** callout labels on the image are gibberish — text-audit's lane.

### mock-driver-gear.png — GROUNDED
- **Showa reality:** Showa taxi-driver kit — peaked 制帽 with winged-wheel company badge, hanko-stamped paper waybills, mechanical split-drum taximeter flipping brass plates, red-felt coin tray, clamp-on oscillating metal fan. Source: Showa taxi-interior photography.
- **40 years of dust:** industrial respirator + amber goggles join the kit; brass-zipper coverall; ROUTE-88 punch cards replace the radio log.

### mock-cargo-lashing.png — GROUNDED
- **Showa reality:** the handcart economy — 柳行李 (yanagi-gōri) wicker hampers, wooden export crates, hand-lashed hemp rope (extrapolation doc §5.8: the daihachiguruma handcart's DNA survives as the *manner* of loading).
- **40 years of dust:** brass pneumatic courier cylinders, red fuel can, canvas tarp, roof-rack rig; unsecured-cargo physics is the comedy engine.

---

## 4. OUTSKIRTS (`art-book/outskirts/`)

### mock-viaduct-sea.png — GROUNDED
- **Showa reality:** Showa coastal expressways — 1960s Tomei/Meishin viaducts, coastal national roads (Izu-class coastline); Japanese cab-over tanker rig. Source: 1960s expressway construction photography.
- **40 years of dust:** the teal "wrong-colored sea" is canon lore, not Showa — the infrastructure is era-correct; the rig carries roof filter canisters.

### mock-fishing-harbor.png — GROUNDED
- **Showa reality:** 1960s–70s Japanese fishing ports — wooden fishing boats, yellow fish tubs (魚箱), winches, coiled rope, concrete quay buildings with brick patches. Source: Showa fishing-port photography (Chiba/Shizuoka-class ports).
- **40 years of dust:** masked fishermen, teal-stained hulls, crusted mooring lines, IBC water tanks on the quay.

### mock-waystation-dusk.png — GROUNDED
- **Showa reality:** 1960s–70s roadside 給油所 on national highways — concrete-block station, mechanical pumps, handwritten chalkboard road-condition board (道路情報板), Japanese cab-over trucks (Hino/Mitsubishi Fuso-class), oil-drum stove with kettle, canvas awning. Source: Showa highway rest-stop photography.
- **40 years of dust:** masked mechanics, Iron Wheel union flags, lashed antenna farm, radio-frequency board (pirate dispatch replaces the station jingle).
- **Notes:** pump label typo ("DISEL") is text-audit's lane.

### mock-switchback.png — GROUNDED
- **Showa reality:** Showa mountain national highways — Hakone Turnpike-era passes (峠), curve mirrors (カーブミラー) on poles, concrete retaining walls with form-tie holes, hazard-orange guardrails, dark cedar/pine slopes. Source: 1970s mountain-pass road photography.
- **40 years of dust:** the long-haul rig with roof filter canisters; the road is the only way out to the teal sea.

---

## 5. UPPER CITY (`art-book/upper-city/`)

### mock-1-skyway-ribbon.png — GROUNDED
- **Showa reality:** Shuto Expressway interchanges (the Hakozaki Junction spiral, 1960s–70s) + Nakagin Capsule Tower (Kurokawa, 1972) — capsule pods with round porthole windows, green Japanese highway direction signs, concrete piers. Source: Shuto construction photography; Nakagin archival photos.
- **40 years of dust:** the capsule towers weather in ochre above the cloud layer; the interchange becomes the Upper City's skyway ribbon.

### mock-2-haibara-estate.png — GROUNDED
- **Showa reality:** Showa-era Japanese estate architecture — kawara tile roof, white plaster walls, ishigaki castle-style stone retaining wall, pruned pine (matsu), stone lantern. Source: Showa villa/shoin-style residence photography.
- **40 years of dust:** the estate sits above the dust-sea — the Lower City's inversion layer becomes its borrowed scenery (shakkei, re-aimed at ochre).

### mock-3-terminal-1.png — GROUNDED
- **Showa reality:** Showa mechanical parking towers (立体駐車場 erebētā-shiki, late 1960s–70s — IHI/Shin Meiwa; open-lattice steel cages, hoist cables, traction sheaves/cable drums, ground-level turntables) + toll plazas. Source: Gemini consult 2026-10-05.
- **40 years of dust:** the parking tower scales up into the sky-elevator; the taxi queue at the toll booths is part of the architecture.

### mock-4-corporate-plaza.png — GROUNDED (Craig's example of a grounded image)
- **Showa reality:** 1970s Japanese corporate plazas — black 社用車 exec sedans (Crown Royal Saloon / Cedric Brougham), white concrete HQ tower with corporate 社旗 flags and red mon, green highway signs, Solari flip boards. Source: 1970s Otemachi/Marunouchi corporate photography.
- **40 years of dust:** toll gantries, imperial-purple accents (Upper-City-only), halogen white; the plaza reads as Minami's toll empire made stone.

### mock-5-cloudbreak-vista.png — GROUNDED
- **Showa reality:** Kenzo Tange's Tokyo Bay Plan (1960) — the 18 km linear megastructure across the bay, three levels of looping highways, designed around the automobile. Source: extrapolation doc §4; Tange's 1960 plan drawings.
- **40 years of dust:** the Bay Plan's ghost built cheaper and dustier — the ring road on piers above the dust sea; megastructures rise from ochre, not water.

---

## 6. WORLD LORE (`art-book/world-lore/`)

### mock-worldmap.png — GROUNDED
- **Showa reality:** an assembly of grounded elements — Keihin industrial belt + Tokyo Bay geography, red-white power-plant smokestacks, container port with gantry cranes, mountain switchbacks, coastal highway. Source: the same roots as §§1–5.
- **40 years of dust:** the vertical cross-section makes the dust layer geography — Upper City on its deck, sky-elevators as the only roads between.

### mock-sea-night.png — GROUNDED (weakest chain in the book — named, not cut)
- **Showa reality:** 工場夜景 (kōjō yakei) — the night views of Kawasaki/Ukishima refineries with burning flare stacks, the iconic Showa industrial night image; plus Japan's real offshore platforms — the Agaoki (阿賀沖) oil/gas platform off Niigata, installed 1974, with a flare boom; plus Showa wooden fishing boats. Source: Gemini consult 2026-10-05.
- **40 years of dust:** extraction moved offshore; the flares burn at sea; the sea changed color; the fishermen are masked and watching.
- **Notes:** the chain holds because the roots are named — but this is the image to re-audit first if Craig flags it again. A rework would push it toward the Ukishima night-refinery look with the wooden boat, away from generic oil-rig-at-night.

### mock-elevator-build.png — GROUNDED
- **Showa reality:** the Showa construction boom — Tokyo Tower (1958) and Shuto expressway construction, the 1964 Olympics build-up: lattice boom cranes, scaffolded workers in coveralls and hard hats, cars hoisted by slings, cobblestone streets with kawara roofs below. Source: 1958–64 Tokyo construction photography.
- **40 years of dust:** the Lift Era — the same hands, the same cranes, building the sky-elevators instead of the expressway.

### mock-dust-tithe.png — GROUNDED
- **Showa reality:** Showa car-wash / 手洗い洗車 culture + expressway undercrofts + ticket-booth stalls; the car is a 1970s Japanese sedan (Corolla E70-class) with fender mirror. Source: Showa streetscape photography.
- **40 years of dust:** filter-rinse booths become a municipal ritual (the Dust Tithe); swept-dust piles, canvas dust flaps, corrugated shanties, gooseneck lamps.
- **Notes:** booth sign lettering is gibberish — text-audit's lane.

---

## 7. QA MOCKS (`mocks/` — the 12 qa/kurogane-bay sources)

All 12 hold their chains. The gig-city set is the pre-art-book QA round; the gig-city-v2 set is Craig's refinement round (already documented as opened/verified in the identity plan — re-audited here against the Showa-grounding bar and confirmed).

| Image | Verdict | Showa root → dust |
|---|---|---|
| gc1-cab-expressway.png | GROUNDED | Shuto Expressway + Tokyo Tower (1958, the Showa icon) + Showa taxi, green expressway sign → dust-era expressway run |
| gc2-harbor-delivery.png | GROUNDED | 1970s Japanese container ports (Kobe/Yokohama containerization era) + kei van with roof-rack cargo → Daikoku piers. Weakest of the 12 (generic box van) but the port root holds |
| gc3-neon-strip.png | GROUNDED | 1970s Shinjuku/Kabukicho blade signs + Tokyo Tower + black Cedric/Crown taxi with fender mirror → Chidori night |
| gc4-refinery-run.png | GROUNDED | Keihin refinery belt; Japanese cab-over tanker with hazard chevrons → Shinkai haul road |
| gc5-dash-computer.png | GROUNDED | 1980s Japanese dashboards (analog dials, chunky buttons); early nav prototypes (Honda Electro Gyrocator, 1981) → ROUTE-88 punch-card CRT |
| gc6-market-morning.png | GROUNDED | Tsukiji outer-market morning — tuna on a Suzuki Carry kei truck, striped awnings, hanging tuna/ice, rubber-booted workers → Kamome |
| v2a-lower-dust-street.png | GROUNDED | Nakagin Capsule Tower + Showa ramen yatai (屋台) with noren → drive-up ramen window, masked figures |
| v2b-upper-city-cloudbreak.png | GROUNDED | Mechanical parking tower + Tange's Bay Plan → car elevator ascending through the dust layer |
| v2c-sky-elevator-terminal.png | GROUNDED | erebētā-shiki parking towers (IHI/Shin Meiwa) + Shuto toll plaza → Terminal 2 |
| v2d-outskirts-wacky-sea.png | GROUNDED | Showa coastal highways (Izu-class coastline); yellow Showa taxi → the one highway to the teal sea |
| v2e-bay-floating-panels.png | GROUNDED | Japanese container ports + Tange Bay Plan's bay structures → the panel fields to the horizon |
| v2f-masked-driver.png | GROUNDED | Showa taxi-driver uniform (制服/制帽) + Expo '70 pavilion architecture in the background → the character law in one image |

## 8. Actions taken

1. **REWORK — `art-book/lower-city/mock-kotobuki.png`:** regenerated 2026-10-05 via the gemini-imagegen skill with a prompt leading on the Showa reference (1970s Tokyo chop shop under the Shuto expressway, Nissan Skyline C10 "Hakosuka") then the 40-year dust extrapolation; warm-amber arc light (palette-safe), masked mechanics, no unmasked faces. Verified by opening. Original preserved as `mock-kotobuki-v1-superseded.png`. Chapter filename unchanged — no chapter.md link edits needed.
2. **CUT:** none — no image was rootless.
3. **Chapter edits:** `art-book/lower-city/chapter.md` §10/§11 updated to record the kotobuki rework and its palette-breach resolution.
4. **Flags for other workers (not my lane):** unmasked faces in mock-kamome, mock-chidori, mock-sea-night (character-law worker); gibberish/English lettering on signs in mock-chidori, mock-kaiun-checkpoint, mock-kmted-cruiser, mock-dust-tithe, mock-goliath-800, mock-waystation-dusk (text-audit worker); `impl-kotobuki.png` needs a follow-up pass to match the reworked Hakosuka reference (production-translation worker).
