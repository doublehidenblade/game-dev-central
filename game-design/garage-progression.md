# Tokyo Drift: A Garage Worth Coming Home To

## Approved direction and first-slice plan · 7 October 2026

> Craig approved publishing this design, creating tasks and proceeding mock-first on 7 October 2026. The first slice below is the execution scope; next/later catalogue sections remain roadmap direction. Runtime implementation is not claimed. Canonical task specs: td-197–td-202 in Tokyo Drift 3D; see the [execution brief](../project-management/task-team-system/briefs/garage-progression-first-slice.md).

**Recommendation:** make the garage the physical record of the player becoming a better-equipped independent driver. Earn money on the road, buy a few recognizable supplies from the city, carry them home, and turn them into a visible improvement that changes the next driving decision.

Build the first loop around **one real drive-in home garage, one starter car, three material families, and a choice between two cargo fittings**. The player drives inside, parks, and sees the shutter close behind the fully cleared car. The workshop is a safe haven when the player has actually broken police sight, not an instant heat-reset button. Expand into refrigeration and a second vehicle only after that loop is enjoyable. Trucks, animals, hazardous loads, and concealed cargo belong to later, distinct specializations.

This is the approved design direction; implementation is bounded by the first-slice task specs. All prices, capacities, percentages, and timings below are **provisional playtest starting points**. The proposals deliberately replace parts of the older progression bible; they do not silently add another upgrade system on top of it.

## 1. What the player should feel

“That workshop is mine. I remember driving those steel bundles through the market. The carrier on my car lets me take jobs I used to turn down. Now I know why I want a van, and I know which streets it will struggle with.”

The garage provides three satisfactions:

- **A reason to earn:** each purchase opens a useful choice, a new kind of work, or a personally desirable vehicle
- **A reason to learn the city:** suppliers live in recognizable neighborhoods, so material trips reinforce route knowledge
- **A reason to return:** the car and workshop visibly change, and the next outing begins with a deliberate loadout

The driving remains the game. No resource mining, free-placement construction, recipe chains, crafting timers, hired drivers, or passive income.

### The loop

Discover a place or earn a story blueprint → reveal the next achievable project → work gigs → buy its supplies at discovered city shops → carry supplies home → install the improvement in its fixed position → choose a newly practical gig or loadout → earn toward the next discovery. The starter begins with a basic plan so discovery never blocks the first earning loop.

Allow a player to mix an affordable supply pickup into an ordinary working circuit when capacity permits. Do not require every profitable gig to end at the garage. Coming home should feel purposeful rather than compulsory.

## 2. Current foundation and what changes

The inspected game source at main commit **58516c0** already has a useful foundation: nineteen Lower City gig bays; six cargo descriptions with different fragility; pickup and delivery phases; a delivery timer; collision/scrape cargo damage; distance, timing, and condition-based payouts; and session earnings. It does **not** yet establish this proposal’s persistent wallet, owned supplies, spending, owned vehicles, or capability-gated cargo equipment. The existing vehicle specification describes geometry, wheels, and collision dimensions; it is not a progression inventory.

Keep the current Lower City’s street-name briefings, signs, landmarks, and paper map. Suppliers need addresses and readable loading bays, not a new GPS interface. The source’s implemented routes take precedence over older bible route-computer concepts.

Keep the central art book’s strongest ingredients: original analog vehicles, chunky visible modifications, masked workshop workers, industrial putty and ochre, warm work lamps, stamped steel, bakelite, enamel labels, and physical dispatch paperwork. The supplied visual descriptions inform this proposal; this pass is not a new image-quality review.

**Explicit changes proposed to the older bible:**

- Replace five tiers across four stats per chassis with a small set of capabilities and reversible choices
- Replace the early 30–40-gig vehicle ladder with a more attainable first second-vehicle goal
- Start with one home garage rather than a property network
- Do not introduce fuel, filter, rent, repairs, and fines simultaneously as recurring money drains
- Do not import old no-pedestrian, police, navigation, or automatic-heat-reset rules into this feature; those systems have separate current decisions and owners
- Keep extra districts, leases, faction gates, and advanced logistics outside the first garage slice

Draft police/traffic work is not assumed merged. Craig’s 7 October refinement makes sight-gated garage hiding an explicit integration requirement: a small police-state and shelter-transition interface must be agreed before that behavior can be accepted. The physical garage can be built and tested independently, but cop hiding cannot be called complete without the police owner’s live sight/pursuit signals.

## 3. Three different things the player improves

### Garage facilities: what home can do

Facilities are permanent, visible fixtures in predetermined locations. Bay and storage expansions replace authored wall/room sections with larger real spaces; floors, walls, door clearance, lighting, collision, parking positions, and storage capacity all change together. They unlock services or ownership capacity, not universal driving buffs. Place the first home provisionally on Kotobuki Repair Row near a signed street, with an approach that can eventually accommodate the heavy pad; validate the actual entrance and turn space before choosing its final frontage.

1. **Starter workbench and unloading shelf:** available immediately; supports the first fittings and stores owned supplies
2. **Powered service station:** appears with the first refrigerated installation; supports powered modules. Bundle its first installation into that project’s displayed price
3. **Service lift:** later enables advanced suspension, reinforcement, and cheaper full repairs
4. **Second parking bay:** opens a predetermined adjoining bay, enlarging the actual drivable interior and enabling a second owned vehicle. Present it alongside the vehicle it makes possible; it is not just another inventory slot
5. **Storage alcove:** opens a predetermined additional room or side recess with visibly more shelving and usable cargo-storage space. It raises the stored-material limit only when that real space is added
6. **Heavy pad:** later accommodates the first genuine truck. It is a larger fixed exterior position, not an invisible ordinary parking slot

No facility should be a cash toll followed immediately by an equally expensive purchase before anything useful happens. A new service fixture should arrive with its first usable product, or visibly explain the complete combined cost before spending.

### Vehicle equipment: what this car can do

Equipment belongs to an individual vehicle. A rack, padded carrier, refrigerator, animal cage, tank, or concealed compartment creates a capability with a cost in space, weight, maneuverability, passenger compatibility, or operating risk.

Start with **one active cargo fitting per vehicle**, including the standard empty configuration. Owned fittings can be swapped freely at home while the vehicle is empty. The player buys an option once, not a recurring reconfiguration fee. Modules remain owned when unequipped.

One fitting is a first-slice scope limit, not a permanent ban on sensible layering. Later, allow one small utility slot alongside the primary cargo module where weight, volume, power, and compatibility permit: for example, a compact refrigerator plus a small concealed compartment. Utility equipment must not grant another full-size cargo specialization for free. A refrigerator, livestock cage, aquatic tank, and hazmat enclosure remain mutually exclusive primary arrangements.

### Appearance, condition, and player skill

- **Appearance/appeal:** paint, upholstery, trim, lights, and general presentation support identity and later passenger income. A cheap cared-for car should qualify for ordinary passengers
- **Mechanical condition:** separate from client cargo condition. Do not interpret cargo HP as chassis health or add purchasable hearts to the racing mode
- **Player skill:** braking, wide-turn judgment, shortcut knowledge, gentle delivery, and route planning. Do not sell an upgrade that removes the need to learn these

Avoid a separate driver XP tree in the first two hours. The meaningful progression already lives in knowledge, ownership, and available work.

## 4. Physical supplies: three now, a fourth later

Materials are purchasable **finished workshop supplies**, not raw ore. Each has a distinct package silhouette and a fixed, authored supplier that the player discovers in the world. No intermediate components, random material placement, random drops, or random quality rolls. The document lists the full design catalogue for planning; the player never sees this entire table at the start.

| Family | Proposed first source | Package / provisional load | Price | Progression purpose |
|---|---|---|---:|---|
| Structural supplies: steel bundles (F in recipes below) | Daikoku tally-office supplier, using an existing accessible frontage | Steel sections and brackets; 40 kg, 1 cargo unit | ¥600 | Racks, bench fixtures, parking-bay fittings, reinforcement |
| Mechanical packs (M) | Kotobuki Repair Row | Crated springs, bearings, linkages; 30 kg, 1 unit | ¥900 | Carriage fittings, suspension options, service lift |
| Sealing and lining packs (S) | Kamome cold-store supplier | Wrapped liners, cushioning, gaskets; 20 kg, 1 unit | ¥700 | Padded cargo, insulation, seats, sealed containers |
| Electrical kits (E), next phase | Tenjin instrument counter | Analog controls, wiring, pumps; 20 kg, 1 unit | ¥1,200 | Refrigeration, aerated tanks, powered service equipment |

**Later structural discovery: timber.** A fixed North Rail Depots timber yard supplies visibly different plank bundles, provisionally 25 kg, 1 cargo unit, ¥400 each. Timber is a distinct variant within structural supplies, not a fifth broad material family and not a substitute for steel in every recipe. Show its actual name and plank icon; do not merge it into a generic structural-points counter. A wooden storage-alcove project can require timber while a steel roof rack still requires steel. Until the player physically discovers the timber supplier, timber-specific projects remain hidden. The later catalogue therefore has four broad families and five named stock items, including distinct steel and timber; do not add further variants without a demonstrated driving purpose. This adds a meaningful place and material without starting a timber→plank→board crafting chain.

These are proposed shop assignments, not claims that shops already exist. Reuse the established districts and bay interaction language; avoid expanding the map just to sell materials. The fourth family enters only when an earned powered-project blueprint provides a clear purpose and a lead to its supplier. Shinkai can supply later certified specialist equipment without adding a fifth generic currency.

Every first-tier pack, including a later timber bundle, must fit the unmodified starter car. Shops sell individual packs, so no project requires the upgrade being built merely to bring its ingredients home. A supplier’s discovery never requires the module, vehicle, or facility sold through that supplier. A larger car can collect several projects’ supplies in fewer trips, which makes capacity valuable without trapping the starter.

**Purchase flow:** stop at supplier → see project requirements, total purchase cost, and remaining load capacity → choose quantities → pay and load visible packs → drive home → clear the garage doorway and park on the interior unloading mark → transfer to the shelf. No on-foot carrying mode is required. Physical means “exists in the vehicle and must travel,” not “add walking and hand manipulation.”

For the first slice, paid supplies are durable. Ordinary collisions affect the journey and other cargo but do not permanently destroy purchased upgrade packs. Recovery returns them with the car. Client cargo is a separate category and still follows its gig’s damage rules.

## 5. Discoveries and story blueprints, one layer at a time

Craig’s latest requirement is deliberate progressive disclosure. The city should reveal what the garage can become. A full branching tree of greyed-out future upgrades would spoil discovery and overwhelm the first visit.

### Five different conditions, clearly separated

Do not compress every reason into a generic padlock:

1. **Known:** has the player encountered the place, plan, or contextual clue that makes this project intelligible?
2. **Prerequisite applied:** has the necessary earlier upgrade actually been installed at least once, rather than merely bought or pinned? Permanent facility prerequisites must still exist; active equipment compatibility is checked separately
3. **Blueprint earned:** if this is a key upgrade, has its short story mission awarded the plan?
4. **Supplier discovered:** has the player physically pulled into the relevant source and learned it sells the required material?
5. **Affordable and ready:** are the required supplies at home and the remaining cash available?

Installation checks the exact required conditions, but the UI reveals only what the player currently needs to know. Discovery is durable knowledge; it does not vanish if the player changes loadout. Completed story gates do not have to be replayed when an owned fitting is re-equipped. Record first-installation milestones permanently: swapping a reversible module must not hide an already discovered branch or make an earned blueprint disappear.

### Reveal rules

- **Far-future or skipped tier:** absent from the workshop catalogue. A fixed garage doorway may be dark or boarded up, but no named future item, full recipe, price, or giant locked branch is displayed
- **Immediate next physical space:** at most one anonymous silhouette or boarded opening with a short contextual label, such as “Adjoining unit.” It previews possibility without exposing the whole ladder
- **Prerequisite not installed:** do not reveal a later-tier project even if its eventual shop was visited early. Save that discovery quietly and use it when the project becomes relevant
- **Discoverable-material project:** once its earlier prerequisite is installed, reveal it when the player pulls into the authored supplier. Timber storage projects use this rule; merely driving past the timber yard does not count
- **Key story project:** reveal the project when its mission awards the blueprint and its earlier prerequisite is installed. The blueprint lists the required materials, what the improvement does, and where to find the missing supplies. Quote an all-in budget only when its prices are known; otherwise clearly label the unknown supplier-price portion rather than inventing an exact total. It may name an unvisited supplier and provide a street/landmark lead without pretending the supplier has already been discovered
- **Known but missing blueprint:** show only an immediately relevant contextual lead, such as “Help the cold-store dispatcher,” rather than its undiscovered upgrade name/recipe or a long list of locked descendants
- **Known but missing source:** show the blueprint’s specific shopping directions and an unvisited-source icon. A named lead is not the same as a discovered shop with full stock/prices
- **Known but missing resources/cash:** show exact remaining quantities, total remaining cost, and what the player already owns
- **Ready:** one clear install action and the physical before/after preview

Discovery-only and story-blueprint projects are different reveal paths, not contradictory requirements applied indiscriminately to everything. For a key timber project, author the sequence so the depot is discovered before the mission awards its blueprint; there is no visible timber-upgrade spoiler ahead of the depot visit.

### The world does the introducing

Suppliers occupy fixed addresses. Their materials tell the story before a UI label does: stacked planks and a timber gantry at the rail depot; steel sections beside dock tally windows; springs and wheel racks on Repair Row; insulated doors, liners, and ice crates at Kamome. Mounted signage, a clear pull-in lane, recognizable frontage, and a working attendant establish that the place is usable.

A discovery event occurs when the player enters the actual service/pull-in area and slows or stops, using the familiar bay interaction. A brief sign/shop card says, for example, “North Depot · timber sold here.” The material icon and supplier entry then become available in the paper shopping list. Buying immediately is optional.

Do not scatter collectible blueprints or random question marks around the map. Discovery comes from a deliberately routed job, a remembered landmark, a visible side entrance, or a specific character’s practical lead. The player may also find the fixed supplier independently. No random spawn, real-time stock lottery, or missable discovery window.

The map initially shows the city’s established navigation information and known places, not every future shop. A blueprint can add its one specific destination or search area to the paper map as a labeled lead. Pulling in turns that lead into a discovered supplier. Keep street-name directions and physical signage; no floating breadcrumb route or all-shops reveal is required.

### Three proposed mission/discovery beats

These are small beats using the existing delivery structure, not a request for a large scripted campaign or new dialogue system. Names and details are proposals, not implemented content. One brief radio line or paper chit establishes the practical situation; completion is communicated by the place, object, and blueprint reward.

**1. “Keep the Ice House Running” → powered station and refrigerator blueprint**

After the first cargo fitting is installed, a Kamome dispatcher needs ordinary spare parts carried to the cold store so its service counter can keep operating. The starter can do the job; the player does not need refrigeration to earn refrigeration. Successful delivery awards a refrigerator plan showing steel, mechanical parts, lining, and an electrical kit, with a named Tenjin instrument-counter address. The player follows that concrete lead and discovers the electrical supplier by pulling in. This replaces an unexplained refrigeration unlock with a small story about the city’s cold chain.

**2. “The Rail Yard’s New Order” → timber discovery and storage-alcove blueprint**

After the first fitting, an ordinary document delivery is deliberately routed to the North Rail Depots timber yard. Stacked planks, a timber loading gantry, and a signed drive-up office make its business legible. Pulling into the yard discovers timber for sale. Completing the job awards a plan for a timber-lined storage alcove, with its exact plank/steel requirements and the already-discovered supplier. The workshop reveals this project only now. A player who independently discovered the yard earlier keeps that knowledge; the story blueprint still gates this key expansion.

**3. “Open the Adjoining Bay” → second-bay blueprint and van purchase lead**

Once the first fitting is installed, a neighboring Repair Row mechanic needs a normal-sized parts load brought back so the disused unit next door can be cleared and made serviceable. Delivering it unlocks the second-bay plan and a lead on the used van. The shutter or boarded opening beside the player’s original bay becomes a relevant project preview. Completing the paid expansion opens real floor space and side shelving; the key has been earned through useful work, not purchased from an unexplained global menu.

Only two beats need to be authored first for the next phase: refrigeration and the adjoining bay. Add the timber/storage beat when its new supplier frontage and physical storage variant are ready. Do not expose its locked card in advance merely to advertise future content.

### Starter path and anti-deadlock rules

The starter receives a basic workbench plan with the rack/padded-carrier choice and plain directions to the first required suppliers. Initial ordinary paid gigs intentionally pass or terminate near those locations, giving a reason to notice and pull in. Existing basic work remains available before any discovery.

A key blueprint mission uses ordinary cargo and a vehicle the player already owns, or explicitly supplies a suitable vehicle without a purchase requirement. Its payout counts as an ordinary completed gig in the pacing budget; it is not an unpaid extra grind gate. Retry is available, with no permanent fail state or faction relationship required to recover the main progression route.

Never require timber storage to carry timber, refrigeration to earn its plan, a van to reach the van-plan mission, or an expanded shelf to unload the ingredients that build that shelf. If a player spends money elsewhere, the story lead and discovered supplier remain available. If a mission chain is not built, hide that future branch rather than leaving the player stuck behind a fake placeholder lock.

## 6. A small dependency graph

Start: home bay + workbench + basic rack/padded-carrier plans + starter vehicle + ordinary small deliveries. Later key branches require their short story blueprint; this is the designer’s graph, not a full tree displayed to the player.

- **Workbench → rack OR padded carrier → bulk OR delicate-certified offers → increased earning choices**
- **First fitting installed → cold-store story delivery → refrigerator blueprint → discover electrical supplier → powered station with compact refrigerator → cold-chain offers**
- **First fitting installed → adjoining-bay story delivery → second-bay blueprint → second-bay/van project → second owned vehicle + larger loads → fund another specialization**
- **First fitting installed → timber-yard delivery/pull-in discovery → storage blueprint → real storage alcove expansion**
- **Service lift → one chosen chassis tune and reinforcement options → a more suitable version of a vehicle**
- **Van + appropriate specialist fitting → livestock OR aquatic work**
- **Heavy pad + truck purchase + clearance-ready routes → oversized freight**
- **Later enforcement contract + concealed fitting → discreet small-load work**
- **Later specialist service + certified hazmat module → hazardous transport**

The rack branch is not a prerequisite for the refrigerator branch. The van is an alternative early savings goal, not a mandatory link after buying every car fitting. Money and materials govern purchase readiness, while a few key story blueprints govern important capability or space unlocks. Ordinary minor fittings do not each require a mission. A short free vehicle familiarization run belongs only where it teaches a genuinely different driving skill.

### Provisional project prices

Prices below are **all-in**, including the listed supplies and installation. The UI should always display this total as well as supplies already owned.

| Project | Supplies | Installation / purchase balance | All-in price | Result |
|---|---|---:|---:|---|
| Rack package | 2F + 1M = ¥2,100 | ¥3,900 | **¥6,000** | Bench visibly organized; rack equipped; more volume |
| Padded-carrier package | 1F + 1M + 1S = ¥2,200 | ¥3,800 | **¥6,000** | Bench visibly organized; carrier equipped; delicate certification |
| Powered refrigeration package | 1F + 1M + 2S + 1E = ¥4,100 | ¥7,900 | **¥12,000** | Powered station and first compact refrigerator together |
| Second bay and used van | Bay: 2F + 1M = ¥2,100 | ¥3,900 bay + ¥30,000 van | **¥36,000** | An actual adjoining bay, expanded side shelving, and a useful second vehicle; standard cargo configuration included |
| Chassis tune, next phase | 1M + 1S = ¥1,600 | ¥6,400 | **¥8,000** | One tune purchased; free later re-selection among owned tunes |

Do not consume materials until installation is confirmed. Pinning a project is free and reversible. Bought packs can serve any project needing that family.

## 7. Equipment should change decisions

### First two cargo choices

**Utility rack:** increases usable cargo volume from 4 to 6 units, adds 25 kg of module mass, leaves the starter’s payload rating unchanged. Bulky light work becomes attractive; dense steel can still reach the weight limit first. A modest loaded speed/handling penalty and lower passenger presentation make it a working-car identity.

**Padded carrier:** 35 kg and 1 unit of occupied space, leaving 3 usable cargo units. Start with 25% less impact damage to compatible client cargo. It grants delicate-certified capacity, but never makes rough driving harmless. It is not a blanket reduction to vehicle damage or all failure conditions.

Existing cargo families remain available as small ordinary jobs. New certified variants or quantities provide the upgrade’s opportunity; buying a carrier should not be required to regain jobs the player could already accept.

### Next and later specialist fittings

- **Compact refrigerator:** 60 kg, occupies 1 of the starter’s 4 units; gives cold-storage capability and a provisional 50% increase in the cargo’s freshness budget. It does not extend the client’s appointment deadline. No fridge in the garage can protect fish while the car is across town
- **Animal cage:** van-scale fitting; consumes a substantial part of the cargo area, excludes passengers and incompatible food loads. It unlocks livestock jobs. Start with a simple stress meter and animated cargo response, not individual escaping-animal AI
- **Aerated water tank:** van/truck fitting with water included in its payload mass. It unlocks live aquatic cargo. Liquid weight and gentle-turn requirements distinguish it from a cage; full simulated fluid physics is unnecessary
- **Certified hazmat module:** a heavy specialist enclosure with approved fictional shielding/containment, safety interlocks, and a stated permit class. It supports a narrow hazardous-cargo family and excludes passengers. Ordinary thermal insulation is not radiation protection; do not describe “insulation” as sufficient. The real-world distinction is appropriate shielding and containment, abstracted here into fictional certified equipment ([NRC shielding guidance](https://www.nrc.gov/facilities-safety/radiation-protection/how-the-nrc-protects-you/minimize-your-exposure))
- **Concealed compartment:** a small-volume fitting with reduced payload room and an inspection-risk modifier. It does not make the car universally invisible to police or automatically clear heat on entering the garage. Keep it fictional and abstract; no real-world concealment procedure is needed

The last two require the relevant gig/enforcement rules to exist. They should not be sold as nonfunctional promises.

### Chassis choices, not additive ladders

Use one tune slot. Purchased tunes are reversible at home; the first implementation need only offer two once cargo choices work.

- **Agility tune:** approximately 10% better low-speed steering response; 15% lower certified payload. High-speed yaw safety limits remain
- **Load tune:** payload rises from 240 to 300 kg; steering response about 8% slower. Suspension support does not make the car larger
- **Express tune:** about 10% stronger acceleration and 8% higher speed ceiling; about 8% longer braking distance. It does not improve fragile-cargo protection

These are desired design outcomes, not values to paste blindly into the controller. Test loaded and empty behavior using the existing per-vehicle handling profile. Gains should be legible but modest; no upgrade should erase a truck’s wheelbase or turn every chassis into the same best car.

**Durability and repair cost:** later reinforcement reduces chassis impact damage by a provisional 20% but adds mass and worsens agility. A service lift reduces paid full-repair bills by about 25%. Keep these distinct: protection reduces damage; the facility reduces the bill. Neither protects client cargo automatically.

**Appearance and tips:** later, professional presentation can raise the available passenger-tip ceiling by up to roughly 10% of the base fare, realized only with a sufficiently comfortable, clean journey. A loud rack or industrial tank can conflict with passenger presentation. Paint color itself remains self-expression, not a mandatory optimum. Prestige jobs should specify comfort/presentation/seating requirements; do not force one exact luxury chassis when another legitimately meets them.

## 8. Weight, volume, and compatibility

Use two easily understood capacity bars: **kilograms** and **cargo units**. Units are an abstract volume measure, not a spatial packing puzzle.

Provisional vehicle targets:

| Vehicle | Payload rating, including fitted equipment and loads | Standard cargo volume | Purpose |
|---|---:|---:|---|
| Starter car | 240 kg | 4 units | Small jobs, narrow routes, low commitment |
| Cargo van | 600 kg | 8 units | Larger batches and specialist equipment |
| Later rigid truck | 1,800 kg | 16 units | Oversized loads and genuine wide-turn routing |

Each revealed offer and discovered supply pack declares mass and volume. Each fitting declares its mass, occupied volume or explicit added-volume allowance, compatible vehicle classes, and conflicting uses. “Space available” never means “weight allowed.” Count supply packs alongside client cargo. Passenger capacity and occupied seats are an additional compatibility rule, not free cargo space.

Block purchases and job acceptance that cannot fit; explain the exact reason before payment. Do not allow overloading in the first version. Reserve capacity when a gig is accepted so the player cannot unknowingly fill its promised space with steel on the way to pickup.

Within legal capacity, progressively reduce acceleration and lengthen braking with load. As a first test ceiling at full rated load, use around 15% less acceleration and 15% longer stopping distance, plus a small steering-response change. Show “light / working / heavy” alongside the exact totals. Preserve usable low-speed control.

For a tank, count water and the container once, then add the carried animals. Do not double-count a turnkey tank-and-water package. Large or hazardous cargo can require an exclusive load even when the numeric bars still have room.

## 9. First twenty minutes

The goal is proof of desire, not a perfectly optimized tutorial route. Measure real door-to-door time, including reading and getting lost.

**0–3 minutes:** start in the short approach outside home with ¥1,500 working cash, the starter car, and a serviceable workbench. A lit door frame and one-line cue invite the player to drive in. Teach full-car clearance, the shutter closing, and parking on the marked bay before showing the workshop. Then reveal just the two basic plans, rack and padded carrier. The player pins one and sees its specific supplier directions and quoted starter-kit all-in price, with unvisited shops clearly marked as leads; exit returns smoothly to driving.

**3–13 minutes:** complete two or three short existing-style deliveries. Favor clear signed routes and ordinary cargo, deliberately introducing the basic suppliers through those routes. The player learns that gentler driving protects payout. Do not require perfect results or a multi-gig streak.

**13–18 minutes:** buy the pinned project’s supplies on a short supplier circuit and carry them home. The rack uses two suppliers; the padded carrier uses three, so its introductory route must be validated against the same time budget. Keep the first supplier circuit away from unintroduced hazards. Do not stage a mandatory police chase during the shopping lesson; teach the sight gate contextually when a pursuit first brings the player home. A loaded crate is visible and the capacity display changes immediately.

**18–20 minutes:** drive back inside, park and unload, install the chosen fitting, see the bench and car change, and receive one immediately usable offer showing “newly available because of your rack” or “requires padded carrier.” The first next-step benefit must be concrete, not a generic “+5 cargo” toast.

Success means the player can explain what they built, why they chose it, and what it now lets them do. The other branch stays affordable later; the first decision is not a permanent trap. Target the first upgrade by minute 20, then completion of its first newly eligible gig around minutes 25–30. The benefit is not considered proven until that run is actually played.

## 10. First two hours

These are pacing targets for a successful player, not promises that everyone will reach them on schedule.

- **20–45 minutes:** several upgraded jobs, one voluntary return home, and a short relevant story lead that reveals the choice between a refrigeration blueprint and the adjoining-bay/van blueprint
- **45–75 minutes:** a specialist-focused player earns the cold-store blueprint, discovers its electrical supplier, gets refrigeration and tries its first contract. A vehicle-focused player earns the adjoining-bay blueprint and saves toward the complete bay-and-van project. Neither must buy the other route first
- **75–105 minutes:** repeat enough familiar streets to notice faster routes and the loadout’s disadvantages. A van buyer collects the remaining bay supplies, previews its footprint, and takes a short familiarization drive
- **105–120 minutes:** aim for either a second owned vehicle with an immediately useful loadout, or a well-developed starter with multiple owned fittings and meaningful savings. The garage visibly tells those two different stories: the specialist has more workshop equipment; the van owner has a physically larger interior with another marked parking bay and shelving

With a provisional median retained payout of ¥2,400, eighteen successful gigs plus ¥1,500 starting cash produce ¥44,700. The first ¥6,000 fitting and ¥36,000 van package leave ¥2,700. Adding the ¥12,000 refrigerator first instead moves that combined goal to roughly twenty-three successful gigs. Do not advertise all three purchases inside an eighteen-gig budget.

Target 18–24 completed jobs in two hours only if actual job-plus-pickup travel, supply runs, and garage time support it. If newcomers take longer, lower early prices or shorten the introductory circuit before cutting the driving challenge out of later work.

## 11. Economy without a punishment spiral

The current fare formula starts at ¥900 plus ¥1,400 per route kilometer, adjusted for cargo fragility and then timing and condition. A 1.6 km job is ¥3,140 before those modifiers. **That is gross, not money reliably retained.** Use an observed median net payout to tune prices; ¥2,400 is a provisional target, not measured telemetry.

The first meaningful improvement should take about 2–3 successful early jobs. A specialist purchase should take another 4–6. The first second-vehicle package should be a clear savings goal of around 15 median payouts, pursued instead of buying everything else.

Specialization should improve earning opportunities, not grant a universal payout multiplier. Target a modest 15–30% improvement in expected net earnings per minute for well-chosen specialist jobs after pickup travel, difficult handling, and downtime. Large vehicles may earn much more per job while still being worse at short alley work. Track net earnings per minute, not the biggest number on the job board.

**Recovery rules:**

- Always retain the starter car and an accessible ordinary job offer; never require selling it to progress
- Free basic recovery brings the starter and paid supplies home in a drivable state. It does not complete or pay a failed gig
- In the first slice, no persistent mechanical wear, fuel purchases, filter costs, rent, interest, or garage upkeep. Introduce one recurring expense at a time only after observed income can support it
- Later, free basic repair remains available; paid full restoration improves condition/presentation. No debt is required to resume earning
- Discovered shops have deterministic stock for relevant projects, no random rare drops and no real-time restock waits; important story gates are retryable and cannot consume the means to unlock themselves
- An abandoned installation does not consume supplies; an uninstalled purchase can be resold at a clearly stated reasonable rate. First-purchase mistakes should not require starting over
- Supplier crates never become sellable copies of client cargo. No buying and reselling the same pack for profit
- Parked vehicles earn nothing, consume nothing, and deteriorate no further while not in use
- Garage hiding requires lost police sight, a fully entered vehicle, and a safely closed shutter. It breaks observation physically and uses the police system’s ordinary search/decay rules; it never instantly wipes heat, illegal cargo, fines, or an active gig. No portable garage teleport used as a profitable shortcut

Reserve a small guaranteed ordinary delivery when random offers would otherwise all need unavailable equipment. Advanced offers may be visible as aspirations, but label the missing capability and keep at least one actionable choice.

## 12. Vehicle ownership and the truck payoff

Own a few vehicles because they produce different driving experiences. One is active; the others occupy their real marked parking bays at home. A bay cannot be sold as usable if the parked vehicle blocks the active car’s exit, the unloading zone, or the shutter. Switching requires returning home and completing or cancelling incompatible active work. No dispatching other drivers and no automatic fleet earnings.

Start with one occupied slot. Second-bay construction and the first van can be bought as one transparent ¥36,000 project, avoiding a stranded empty bay. Completion opens an authored adjoining room, adds another vehicle-sized floor area and parking mark, and extends the supply shelving. It increases physical space, not only the vehicle counter. A player may choose to prepare the bay separately, but show the remaining vehicle price before they spend. Do not charge a second slot fee when they later buy the promised van.

Retain vehicle-specific fittings, paint, tune, and later condition. Show module compatibility before buying. Compatible modules can be transferred between parked vehicles freely; incompatible sizes remain owned rather than silently disappearing. No early forced vehicle sale.

**The truck should be a new verb.** Begin with a rigid truck before committing to an articulated tractor and trailer: longer wheelbase, larger turning envelope, slower response, visibly heavy cargo, deliberate braking, and loading docks that require planning. Upgrade from a van because the job needs its rating or dimensions, not merely because its income multiplier is larger.

The existing traffic truck dimensions, 6.4 m long and 2.2 m wide, are a useful reference contract, not proof of a finished player truck. Verify the player controller, swept corner clearance, cab visibility, loading area, and recovery before selling it. Every truck offer must have at least one proven-clear route and sufficient legal unloading space. A suggested safe route can use streets and signs; no GPS line is necessary.

Keep the starter’s narrow-route advantages. Do not widen all of Kamome to accommodate a truck. Ineligible alley jobs should say why; larger outer loading bays can serve those businesses later if deliberately authored.

The useful Euro Truck Simulator reference is vehicle identity, equipment ownership, and the satisfaction of handling a substantial load. Its wider company-management layer is explicitly outside this proposal ([official ETS2 overview](https://eurotrucksimulator2.com/about.php)).

## 13. A real garage, with fixed workshop views after parking

### Drive in, close the shutter, then work

The garage is a real, drivable interior connected to the street by an entry apron. The car travels through the doorway under ordinary driving control, clears it with its entire collision footprint, and parks on a visibly marked interior bay. There is no fade-to-garage teleport at the curb and no on-foot avatar requirement.

Give the frontage an enamel garage sign, a recognizable door frame, a clear approach, and a lit parking/unloading mark inside. Show entry availability from the street before the player commits to the apron, and preserve a drive-past or turnaround path when entry is denied. Keep the starter approach forgiving enough to learn at low speed. Provisional sizing can begin with a clear parking rectangle around 3.2 × 6.5 m, but the actual hero-car collider, fitted protrusions, approach angle, door sweep, and camera must determine final dimensions. The later van and truck need their own swept-clearance validation.

Driving control remains active until the player is fully inside and stopped on the parking mark. Once the shutter is safely closed, a single “Open workshop” action changes to an authored camera, subject to active-cargo restrictions. The shutter can close once the complete vehicle and attached load are beyond the threshold and its sweep is clear; it must never push, crush, clip, or cut through the car. A parked car outside or partly in the opening never counts as safely garaged.

### The shutter as a way to lose the cops

Craig’s rule: **entry is unavailable while police can see the player**. The entrance should not become a shortcut that lets a visibly pursued car disappear into a menu.

- **Unobserved approach:** the door offers entry. Test a provisional two-second continuously unseen confirmation to prevent one-frame sight flicker; if used, show a short countdown rather than a hidden delay. If a pursuit is still active, the ready cue reads “Out of sight · get inside”
- **Observed approach:** keep the shutter closed and show a lock/sight icon plus “Break police sight before entering.” A lamp reinforces this, but color is never the only signal
- **Entering:** recheck actual police visibility until the whole car clears the threshold. If a cop regains sight during the approach or doorway crossing, cancel the safe-entry attempt. Do not slam a shutter onto the car or teleport it outside; keep the opening safe while the player clears it, retain driving control and pursuit, and withhold workshop/shelter status until the entry conditions are valid again
- **Securing:** after full clearance and a valid visibility check, close the shutter physically. Until it is fully shut, the car has not gained sealed shelter. If visibility returns before closure completes, pause/reopen the shutter safely and cancel securing rather than finishing the closure to force concealment. Retry only after the sight gate is valid again; the pursuit owner retains its search state
- **Sheltered:** the closed shutter and building provide real line-of-sight occlusion. Notify the police system that the vehicle is inside an occluding shelter. Heat/search can decay according to that system’s rules; it is not instantly set to zero. Nearby police may still be searching outside
- **Leaving:** the player explicitly chooses “Open shutter” from the in-car view; open it fully before releasing the parking hold. Closing a workshop panel or pressing Back returns to the car with the shutter still closed, not automatically to the street. A non-obstructive “Police still searching outside” cue can warn when the police system knows this; it does not guarantee a clear street. Leaving may expose the car and resume pursuit normally

A nearby cop without a sight line should not block entry merely because of distance. Conversely, a cop with an actual view through an open doorway must still count. Use the police owner’s visibility verdict and real door occlusion; do not invent a second garage-only wanted system or an unexplained radius check. The provisional short visibility debounce is a tuning detail with a visible countdown, not an additional hidden permit requirement. Represent the gate as observed/locked, recently unseen/counting, and available/open using distinct labeled icons and patterns as well as lamps.

A cancelled entry remains a live driving situation. The player can back out, move clear, or hide behind real geometry and retry. No immunity begins just because the nose crossed an invisible trigger. Garage walls and shutter must participate consistently in collision and police visibility.

### Safe entry, exit, and recovery

- Keep the door sweep and apron free of parked owned cars and stored packs
- Validate every sold vehicle and fitting against entry width, height, and full swept footprint. A paid roof rack or load must not strand an otherwise eligible owned car outside its home
- Check the full vehicle and fitted cargo, not just its center point, before closing
- Do not make a shutter animation an unavoidable collision or trap. Pause/reverse closure when obstructed; re-evaluate entry/shelter state safely
- Do not spawn moving traffic, police, or owned cars inside the player’s garage footprint or door sweep. A legitimately approaching external vehicle can still keep an exit unsafe
- If the exit is obstructed, keep the car controllable or safely parked and offer retry; never release it into a closing shutter or force it into traffic
- A stuck-car recovery must preserve paid supplies and ownership. During a pursuit it must not convert an invalid entry into successful shelter or erase enforcement consequences; use the agreed recovery outcome
- On reload, restore a consistent inside/parked/door state rather than a car intersecting a shutter. Preserve active pursuit/search state and outstanding cargo obligations

### Physical expansion, visibly earned

The starting room contains one parking bay, a workbench, and a compact supply shelf. The next garage variant opens a prebuilt adjoining bay and side-storage area. Later variants open another predetermined storage alcove or the heavy pad. No free placement is needed, but the new floor area must be genuinely usable.

The player should be able to drive into the new bay and see its old wall line disappear. The increased material capacity must have matching racks, floor markings, and staged supply packs in the new alcove. Stored packs can be grouped into clear stacks instead of one mesh for every item, but the visual fullness and available capacity must agree.

Car changes must match their benefit: a rack adds a visible basket and anchor points; padding shows a lined carrier; the refrigerator adds a distinct insulated chest and analog indicator; reinforcement adds visible protection; a larger bay really holds another car. Avoid an upgrade that exists only as a number.

### Workshop cameras and accessible controls

Use a small set of authored cameras within the actual room:

1. **Home overview:** parked car, shelf, workbench, future opening, pinned project
2. **Car view:** fitting preview, before/after capacity and handling, compatible owned loadouts
3. **Workshop view:** supplies on the shelf, project recipe, facility preview, missing-item shopping list
4. **Parking view:** owned vehicles in real bays and only the immediately relevant expansion opening; show the active vehicle clearly. A heavy pad is named and previewed only after its reveal conditions are met

Tap/click large hotspots or use equivalent controller focus. Tabs duplicate every world hotspot so a tiny prop is never the only way to act. Include a clear “Back to car” action that leaves the shutter closed; opening it to depart is a separate explicit action. The fixed cameras support workshop decisions after parking; they do not replace physical arrival or departure.

Every revealed project previews its predetermined installation position. Far-future projects and skip-level upgrades stay hidden; only an immediately relevant opening may have an anonymous blocked silhouette. Completing it replaces that object or room section with the finished version and a short skippable work transition while the car is safely parked. This is an authored reward, not a real-time crafting queue. Check parked vehicles and stored materials before any geometry change.

### Tutorial and cues: one action at a time

Teach the current next action, not the entire economy. Each cue is one short line paired with a physical affordance:

- At the first door: “Drive inside” beside the lit opening
- At the parking rectangle: “Stop in the marked bay”
- After parking: “Open workshop” with the current device’s button/touch icon
- At the initial project choice: two basic-plan previews, one benefit and one tradeoff each; later branches appear only through their prerequisites, discoveries, and blueprints
- After pinning: “Buy these supplies” on a compact paper shopping list with district, street, and landmark; show only its relevant known suppliers or blueprint leads, with unvisited/discovered states clearly different
- At the supplier: “3 packs · 110 kg · fits your car,” adjusted to the actual purchase
- On the return: “Park to unload”; then the shelf fills visibly
- At installation: the changed car part, changed room fixture, and a concise before/after capacity display
- At the next offer: “New: bulk load · your rack fits it” or the equivalent padded-cargo cue
- At the first relevant pursuit: explain the sight gate when the player approaches home, not in an unrelated tutorial popup

Reveal refrigeration, power, vehicle slots, repairs, and specialist risk only when the specific prerequisite and discovery/blueprint conditions are met. Do not replace progressive disclosure with a wall of blacked-out named upgrades. Show at most one primary tutorial cue; dismiss it when the player succeeds, allow it to be recalled, and avoid repeated blocking prompts. A concise optional help panel can hold deeper rules.

Icons always have labels. Door states combine shape/icon, text, lamp state, and optional sound rather than red/green alone. Touch targets and text must remain readable in portrait phone framing; focus order, button hints, and back/confirm behavior must work on controller and keyboard. Do not steal steering input or open a modal while the car is moving through the threshold. Caption important audio cues and reduce camera motion where needed.

The project decision screen answers five questions: what changes, what work becomes possible, what becomes worse, what supplies are already home, and the complete remaining cost. Previewing a revealed project is free; hidden descendants have no browsable recipe or spoiler name. Avoid a page of tutorial prose before the first drive.

Garage menus are a respite once safely parked and free of active obligations. Do not let a loaded live gig enter upgrade or vehicle-switch mode: finish or cancel it first. Physical shelter can still be used while carrying cargo, but the delivery clock and normal police search rules continue in live driving/shelter state. A parked in-car waiting view lets the player remain behind the closed shutter while the live world’s search rules run. Explicit pause follows the game’s ordinary pause rules; merely entering home does not pause the world. Workshop menus must not accelerate police decay, and offline time must not clear a pursuit. No freshness decay while the game is closed or during a mandatory transition that removes driving control.

## 14. Inventory and persistence requirements

Persistent ownership is part of the first slice, not polish to add after spending exists.

Keep distinct records for wallet balance; lifetime earnings; session summary; owned vehicles; active vehicle; parking capacities and actual garage layout tier; stored-material capacity; parked vehicle positions; shutter/entry/shelter state; installed facilities; owned and equipped modules/tunes; appearance; supplies at each physical location; pinned project; discovered suppliers and materials; earned blueprint IDs; completed story gates; completed installation milestones; reveal state derived from those facts and permanent facility prerequisites; and active-gig state. Future chassis condition must remain separate from gig cargo HP.

Supplies occupy exactly one location: supplier purchase transaction, active vehicle, or home shelf. Paying, loading, unloading, and consuming materials are atomic transitions with stable item/transaction identities. Reloading during one cannot duplicate a crate or charge twice. Installed modules are not simultaneously loose inventory.

Save after settlement, supplier discovery, blueprint/story rewards, purchases, unloading, installation, and vehicle switches. Mission rewards and discoveries must be idempotent and never duplicated or lost on reload. Keep a previous valid save and a versioned migration path. A persistent gig settlement must be credited only once even if its completion signal repeats or the scene reloads.

A normal quit/resume restores the current job, remaining timer, cargo state, vehicle, carried supplies, garage layout, door state, and relevant pursuit/search state where technically reliable. If safe position restoration is impossible, recover explicitly using a valid home or exterior recovery anchor, preserve owned items, and fail/refund only the appropriate unresolved job state. An active pursuit must use the enforcement owner’s recovery outcome; do not grant safe shelter simply because the save needed recovery. Do not silently erase paid ownership. No offline timer decay.

Start with 12 supply units of real shelf capacity, enough for the early recipes, with a warning before purchase if the planned unload would exceed it. The second-bay project physically opens an adjoining bay and side shelving and raises storage to 24 units. A later standalone storage-alcove project can provide an alternative expansion path at a price tuned after the first slice; it must add real usable room and visible shelving. Do not require a storage expansion merely to make the first recipe fit. Test purchases exceeding a single trip, partial unloading, a full shelf, and returning with both supplies and client cargo.

Existing session-only earnings need an explicit migration decision. Start a new progression save with a disclosed grant; do not invent historical income or repeatedly convert a session counter into spendable cash.

## 15. Interface to gigs and ownership boundaries

The garage should publish a **read-only vehicle capability snapshot**. It should not redesign dispatch, write new mission stories, or directly manipulate the gig generator’s internal state.

The snapshot describes vehicle identity and class; payload and usable volume; occupied/reserved load; seating; installed module capabilities; presentation/comfort band; and supported handling/condition modifiers. Example capabilities are delicate carrier, cold storage, livestock carrier, aquatic tank, concealed storage, and certified hazmat class. Names are illustrative contracts, not implementation demands.

Each gig definition provides required capabilities, mass, volume, seating/exclusivity, and allowed vehicle envelope or route class. Eligibility returns either “ready” or a specific missing requirement. Recheck on acceptance and loading; lock the relevant capability snapshot for a live run. Ordinary existing offers default to no special capability requirement.

Preserve the current settlement result as the authority for gross payout, timing, condition, success, and failure reason. A new wallet consumes an idempotent settlement event. Garage bonuses must not multiply the final payment a second time. Cargo durability, freshness, comfort, and inspection risk are separate modifiers consumed by the system that owns each mechanic.

The garage/police boundary should expose a small explicit state contract: whether pursuit/search is active, whether any relevant police observer currently sees the player, whether a sheltered car may be reported as hidden, and the recovery outcome. The garage reports fully-inside and parked state, shutter-open/closed state, shelter entered/left, and interrupted entry. The police system owns heat, search progression, visibility checks, and reacquisition. Recheck eligibility before opening and before granting closed-door shelter; coordinate real shutter collision/occlusion rather than relying only on UI state. These names describe responsibilities, not a demand for a particular API implementation.

Keep delivery deadlines and freshness distinct. Refrigeration alters freshness, not the dispatcher’s deadline. Start freshness once loading is complete and driving control returns; suspend it during mandatory transitions. Fit-specific content only appears when its actual mechanic is ready.

**Suggested work boundary, after design approval:**

- Garage/progression work: physical interior/apron/shutter and safe vehicle transitions, authored room expansions, persistent ownership, suppliers and owned-material lifecycle, fixed workshop views, facilities, contextual tutorial cues, recipes, loadout choice, capability snapshot, economic telemetry
- Claude’s gig work: offers, cargo behavior, job requirements, eligibility presentation, timers, settlement, specialist contract content, and the few short blueprint-awarding story deliveries. Agree their prerequisites/reward IDs; garage reads rewards rather than recreating mission logic
- Claude’s vehicle/assets work: final models, sockets, silhouette changes, cargo props, and geometry contract
- Traffic/police/arrest work: authoritative police visibility, pursuit/search state, nearby-search warning, and enforcement/recovery outcomes; garage consumes these and reports entry cancellation, shutter-closed shelter, and exit exposure. It does not invent confiscation, fines, or instant heat clearing
- Shared agreement required: cargo units, mass accounting, modifier composition, no-eligible-offer fallback, settlement identity, route-clearance validation, police line-of-sight authority, door-occlusion timing, shelter transition, live timers, recovery/save behavior, supplier-discovery triggers, blueprint reward identity, and reveal prerequisites

Do not change the existing geometry/wheel/collider contract to smuggle in economy fields. Add a separate progression/capability definition that references the model identity. Preserve the distinction between a traffic vehicle model and an owned playable vehicle.

## 16. Build order and scope ceiling

### First slice: prove “earn → fetch → improve → earn differently”

- One real Lower City garage interior, entry apron, functioning shutter, safe drive-in/park/drive-out, and fixed workshop views after parking
- Contextual one-line onboarding, physical cues, accessible touch/controller controls, and progressive reveal
- Sight-gated garage hiding integrated through the police owner’s visibility/pursuit contract; no instant heat wipe
- Persistent wallet and save recovery
- Three initial supply families at readable authored frontages, discovered by physically pulling in; a solvable basic-plan path and relevant paper-map leads
- Prerequisite-aware reveal states; hidden skip-level upgrades and no full exposed technology tree
- Visible bought supplies, shared load accounting, and home unloading
- Rack versus padded carrier; one equipped fitting; free swaps among owned items
- Two meaningful capability-consuming offer variants in coordination with the gig owner
- Small, bounded loaded-handling difference
- At most one anonymous next-space silhouette; reveal refrigeration/van goals only when their relevant short story lead and prerequisites are ready. Hide unbuilt future branches rather than advertising unusable locked content

No fuel economy, mechanical wear, passengers, new fines/confiscation economy, crafting queues, new city layer, or truck physics required for this proof. Police sight-gated hiding is now requested first-slice behavior; if its dependency is unavailable, ship neither a claim of completed hiding nor a fabricated substitute. If capability-consuming gigs are not ready, the slice is not complete merely because an upgrade menu works.

### Next: prove a sustained first two hours

- Short cold-store story delivery, refrigerator blueprint, fourth supply-family discovery, and refrigeration/freshness
- Short adjoining-bay story delivery and blueprint, real bay/side-storage expansion, plus van ownership and switching
- Optional timber-yard discovery and storage-blueprint beat when that supplier and physical alcove are ready; timber-specific upgrades remain hidden beforehand
- A small choice of chassis tunes
- Passenger presentation/tips only when passenger comfort exists
- Service lift and repair savings only when there is a tested chassis-condition economy
- Price rebalance using observed net income and real return-trip time

### Later: earn the broader fantasy

- Rigid truck, physical heavy pad, oversized route contracts
- Further predetermined storage-room/bay expansion, each with matching geometry and capacity
- Livestock cage and aquatic tank, each with one distinctive readable behavior
- Bounded primary-plus-utility module combinations once single-module tradeoffs are proven
- Concealed compartment after the inspection/enforcement contract is stable
- Certified hazmat module after hazardous-cargo rules are scoped
- Luxury/tuner/exotic vehicles as meaningful alternatives or aspirational looks
- Articulated trucks, more garage sites, and cross-stratum hauling only after the smaller systems hold up

The brainstorm is preserved, but its ideas are not equally ready. **Highest-value now:** real drive-in shelter, sight-gated shutter hiding, contextual onboarding, authored supplier discovery, hidden skip-level upgrades, physical supply trips, fixed workshop changes, cargo specialization, and visible car improvement. **Strong next:** refrigeration, second slots/van, modest handling choices, appeal tied to comfort. **Reshape:** radiation “insulation” into certified containment; all-stat upgrades into tradeoffs; materials into three or four finished packs. **Defer:** animal escape simulations, liquid simulation, articulated rigs, deep contraband enforcement, twenty upgrades per chassis, and property empires. **Exclude:** free building and automated fleet management.

## 17. Playtest acceptance and risks

Validate the first-slice behaviors before the catalogue grows; the explicitly marked later checks apply only when their underlying systems enter scope:

1. Most new testers complete a supply haul and meaningful upgrade within twenty minutes, then finish a newly eligible gig by roughly minutes 25–30; record the slowest quartile and why they missed either target
2. After installation, players can correctly explain the benefit, disadvantage, next available job, and remaining goal without a tutorial recap
3. Both rack and padded carrier are chosen voluntarily across a varied test set; either can support profitable next jobs. If one dominates every route, fix the offers or tradeoff
4. The player can see purchased supplies before returning home, see them on the shelf, and see them disappear exactly once when installed. Car and garage changes visibly match their actual benefits
5. Every valid offer fits both mass and volume, has compatible equipment, and has a physically usable route and destination
6. A player at zero cash with a failed gig, damaged starter, and carried supplies can recover and earn again without deleting the save
7. Reload at every transaction edge: no duplicated payout, lost vehicle, double charge, duplicated pack, or installed module that also remains in loose storage
8. Fitting swaps and workshop entry cannot stop a loaded timer, duplicate an item, grant incompatible capabilities, or cleanse enforcement/cargo obligations. Police shelter uses ordinary search/decay rather than a heat reset
9. Empty versus loaded driving is perceptibly different but controllable on phone. When performance tunes arrive, verify that none invalidates the shared steering-safety envelope
10. In the next-phase two-hour test, the retained-earnings ledger supports the advertised branch. Compare time spent driving gigs, fetching supplies, returning home, and reading menus

11. Test a denied high-speed approach with a readable gate and safe drive-past path. Drive the actual car fully in and out in both directions, with empty and maximum allowed cargo and every first-slice fitting. No trigger teleport, clipping, trapped shutter, unsafe camera switch, or doorway load collision
12. Test police sight continuously: seen approach, unseen approach, nearby cop without sight, sight regained with the car partly inside, sight regained during closure, closed-door hiding, police searching outside, and exit reacquisition. No immunity before valid full closure and no instant heat wipe
13. Test a stopped car in the door sweep, an obstructed exit, recovery during entry, save/reload during door transitions, reload while hidden, and parked-vehicle interference. Closing a menu must never open the shutter or return the player to waiting police automatically. Preserve supplies and enforcement state without embedding the vehicle in geometry
14. In the next-phase expansion, drive into the newly opened second bay, park both vehicles, access enlarged storage, and leave without moving through the other car. Capacity must increase only with the correct physical room/shelving variant
15. First-time phone and controller testers can enter, park, pin a project, shop, unload, install, and leave using contextual cues without a compulsory text wall. Verify icons plus labels, readable text, focus order, and no prompts stealing live steering

16. An undiscovered timber yard exposes no timber-upgrade catalogue; pulling in records it once. A premature shop discovery does not reveal skipped tiers, while installing the correct prerequisite reveals the appropriate next step
17. A key mission awards its blueprint once, clearly names materials and source leads, and remains solvable with already available equipment. Test mission failure, early independent supplier discovery, spending savings elsewhere, and reload before/after rewards
18. New players can identify why their next known project is unavailable without seeing the whole tree: prerequisite, story blueprint, undiscovered supplier, materials, and cash have distinct concise states

**Principal risks and responses:**

- **Shopping becomes errands:** keep only a few regional suppliers, predictable stock, compact recipes, and opportunities to combine trips
- **Upgrade purchases feel abstract:** every milestone changes a visible fixture or car part and produces a specific usable offer
- **The best build does everything:** start with one fitting, then permit only bounded primary-plus-utility layering with capacity costs and route-specific value
- **Money disappears into upkeep:** no stacked recurring expenses; budget against net income, protect recovery
- **Large vehicles feel unfair:** validate swept turns, clearances, unloading space, and attainable deadlines before offering the work
- **Simulation scope grows invisibly:** animated cargo response first; fluid, animal, and trailer simulation require separate proof
- **Garage conflicts with parallel work:** freeze the capability/settlement and police-sight/shelter contracts before either owner extends them
- **Shutter becomes an exploit or trap:** real full-car clearance, interrupted-entry tests, physical occlusion, no automatic heat wipe, and pursuit-aware recovery
- **Expansion is only cosmetic:** add actual drivable floor and usable storage space together with capacity
- **Complexity overwhelms the player:** one contextual cue at a time, prerequisite-aware reveal, authored discovery, spatial previews, and short optional help
- **Hidden progression becomes aimless:** fixed environmental clues and one practical story/source lead; never a random discovery requirement or circular hidden lock
- **Story scope explodes:** two initial blueprint deliveries built on existing gig verbs; timber/storage beat later, not a campaign per upgrade

## 18. Approved first-slice direction

Approval scope is the first slice, with the next/later sections serving as direction rather than a commitment to build them all.

1. **Physical home and supplies:** drive into a real garage, park behind a functioning shutter, and carry three initial supply families home without on-foot crafting
2. **Upgrade structure:** visible car/facility changes and real predetermined bay/storage expansion, plus one initial swappable cargo fitting with meaningful disadvantages
3. **First choice:** rack or padded carrier; refrigeration next
4. **Ownership pace:** retain starter, bundle second bay with a used van, keep the truck for a later handling milestone
5. **Clarity and recovery:** contextual low-text tutorial and spatial affordances, persistent save from day one, protected paid supplies, and a recoverable ordinary-income path
6. **Police hiding:** entry only after breaking sight, no shelter before full-car clearance and safe shutter closure, and normal pursuit/search rules afterward
7. **Discovery and story gates:** hide skip-level upgrades, discover fixed suppliers by pulling in, and earn key blueprints through a few short contextual missions that explain materials and source leads

The implementation sequence starts with measured reference mocks, then graybox and explicit integration contracts; dependencies on gig/asset owners remain separately owned. The full catalogue should wait for the first material haul and upgrade choice to prove fun.

## Source notes

Craig’s 7 October refinement explicitly requires a real drive-in interior and closing shutter, entry gated on being out of police sight, visible garage/car upgrades, actual larger vehicle/storage space, and UI/tutorial cues without overwhelming text. These requirements are incorporated above and supersede the earlier purely menu-oriented framing. His subsequent refinement requires hidden/blacked-out skip-level upgrades, authored material/supplier discovery (including a timber-depot example), and key upgrades gated by story-awarded blueprints explaining requirements and locations. Section 5 defines those rules without a full exposed tree or random discovery.


- [Central world bible, especially economy and vehicles](https://github.com/doublehidenblade/game-dev-central/blob/c15641a595d4b23d3e73acb1dc239d22fd1ed263/game-design/gig-city-world-bible.md): lore, six-vehicle ambitions, older upgrade/economy plan
- [Fleet & Gear art-book chapter](https://github.com/doublehidenblade/game-dev-central/blob/c15641a595d4b23d3e73acb1dc239d22fd1ed263/game-design/art-book/fleet-gear/chapter.md): vehicle identities, visible equipment, cargo telegraphs, unresolved class-gating questions
- [Lower City plan](https://github.com/doublehidenblade/tokyo-drift-3d/blob/58516c0dcdbadbbc360b051015ba215057995911/godot/docs/city-design/lower-city/CITY_PLAN.md): implemented neighborhood structure, nineteen bays, roads, no-GPS navigation, clearance context
- [Current gig dispatch](https://github.com/doublehidenblade/tokyo-drift-3d/blob/58516c0dcdbadbbc360b051015ba215057995911/godot/scripts/lower_city/gig_dispatch.gd) and [configuration](https://github.com/doublehidenblade/tokyo-drift-3d/blob/58516c0dcdbadbbc360b051015ba215057995911/godot/scripts/game_config.gd): inspected cargo, phases, timing, fragility, payout, and session counters
- [Vehicle model geometry contract](https://github.com/doublehidenblade/tokyo-drift-3d/blob/58516c0dcdbadbbc360b051015ba215057995911/godot/data/vehicles/vehicle_spec.json) and [handling profile](https://github.com/doublehidenblade/tokyo-drift-3d/blob/58516c0dcdbadbbc360b051015ba215057995911/godot/scripts/vehicle-config.gd): existing geometry and tuning interfaces, not proof of owned playable truck support

Publication update, 7 October 2026: this design and dependency-ordered task specifications are now proposed through documentation-only GitHub draft PRs. No game state, implementation, external-agent instructions, merge, deployment or Actions dispatch is part of this publication.
