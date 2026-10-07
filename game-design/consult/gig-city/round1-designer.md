Here is your operational blueprint. No fluff.

---

### (a) Gig Taxonomy: 10 Core Templates

Procedural replayability relies on stacking three axes: **Payload Rules** (how it behaves in the car), **Route Pressures** (what the world throws at you), and **Payout Conditions** (how you get paid).

```
[Template] -> [Randomized Parameters] -> [Stat / Skill Tested]
```

1. **Point-to-Point Express (Standard Dash)**
   * **Varies:** Time buffer (generous to razor-thin), traffic density, weather (rain/slick roads), police radar zones along the path.
   * **Tests:** Speed stat; map knowledge, clean apex cornering, shortcut identification.
2. **Fragile Egg-Run (Stemware, Nitro, Wedding Cakes)**
   * **Varies:** Fragility threshold, G-force tolerance meter, road bump sensitivity, payload weight.
   * **Tests:** Suspension/Health stat; throttle/braking modulation, curb avoidance, avoiding jumps.
3. **The Multi-Drop Milk Run**
   * **Varies:** 3 to 6 drop locations, drop order lock (strict sequence vs. player choice), dynamic drop timers (dropping at Stop A adds 45s to Stop B).
   * **Tests:** Cargo Size stat; spatial micro-routing, handbrake parking precision, rapid stop-and-go acceleration.
4. **V.I.P. Chauffeur (The Diva Run)**
   * **Varies:** Passenger neuroticism (e.g., "Hates red cars," "Wants high speed," "Gets nauseous over 40 mph"), paparazzi tailing.
   * **Tests:** Appeal stat; maintaining high "Comfort Meter" while evading tailing vehicles; lane discipline under time pressure.
5. **Hot Contraband (Heat Wave)**
   * **Varies:** Initial Heat Level (1–4 stars), contraband decay/smell meter, active police patrol density, roadblock frequency.
   * **Tests:** Speed + Health stats; line-of-sight breaking, alleyway navigation, baiting police into environmental hazards.
6. **Volatile Mass (Sloshing Tanker / Live Animal)**
   * **Varies:** Center-of-mass shift frequency (liquid sloshing throws weight left/right on sharp turns), detonation/escape timer.
   * **Tests:** Handling/Weight stats; counter-steering, weight transfer management, low-speed preservation of momentum.
7. **Undercover Shadow (Tailing)**
   * **Varies:** Target speed, paranoia meter (spotted if too close for 3s), drop-back limit (lost if >100m away for 5s), randomized target turns.
   * **Tests:** Throttle control, blending into ambient traffic, predicting intersection lane choices without rubber-banding.
8. **Heavy Haul / Flatbed Repo**
   * **Varies:** Towed chassis weight, towed object swing physics, low bridge clearances, pursuers trying to ram the tow-hitch.
   * **Tests:** Torque/Engine Power (Speed sub-stat), wide-turn trajectory planning, defensive ramming.
9. **Organ / Coolant Rush (Cryo-Timer)**
   * **Varies:** Payload ambient temperature, cooling station locations across the map, melting rate tied to engine RPM/exhaust heat.
   * **Tests:** Route flexibility; intentional path detours to hit cooling checkpoints (drive-through car washes, industrial ice bays) while maintaining a macro countdown.
10. **The Road Rage Escort**
    * **Varies:** VIP car health bar, number of aggressive pursuers, weaponized traffic (hostile ramming vans).
    * **Tests:** Vehicle Health + Mass; defensive blocking, pit-maneuvers, peeling aggro off the VIP vehicle.

---

### (b) Pre-Gig GPS Planning System

Pre-gig planning fails when it feels like filling out an Excel sheet. It succeeds when it feels like **gambling with time.**

```
[Contract Board] 
       │
       ▼
[Route Canvas (3D Vector Map)] ─── Add Gas Stop? (+Cash saved, -15s)
       │                        ─── Add Chop-Shop Drop? (Bank loot, off-route)
       ▼                        ─── Add Side-Fare? (Ride-along, tighter clock)
[Lock & Launch] (Bonus if locked < 15s)
```

#### What the Player Sees
* A top-down, cel-shaded vector map showing:
  * Origin (Player current spot) and Destination pin.
  * Baseline Route (calculated for safety, not speed; pays 1.0x).
  * 3–5 glowing **Opportunity Nodes** slightly off-route: Cheap Gas Station, Garage/Stash, Black Market Drop, Secondary Hitchhiker.
  * Hazards: Speed traps, construction blockades, street riots, traffic jams.

#### Decisions & Trade-Offs (Time vs. Money vs. Risk)
* **Gas Stop:** Current fuel level dictates engine output. Running on fumes caps max speed at 60%. Stopping adds 12 seconds to the route but guarantees 100% boost performance.
* **Garage Drop:** Stashing contraband drops player Heat to zero, but requires an off-route detour. Keeping it risks confiscation if rammed by police before the finish line.
* **Hitchhiker Stacking:** Pick up an extra passenger *during* a cargo run. Payout doubles, but their destination adds an intermediate stop, and their comfort constraints apply instantly to your fragile cargo.

#### Keeping Planning Under 60 Seconds
* **Snap-to-Grid Waypoint Drawing:** The player does not place coordinates; they drag the path line, and it snaps magnetically to intersections and Opportunity Nodes. Maximum 3 custom waypoints allowed.
* **The "Fast-Commit" Cash Bonus:** A visible countdown ticker (15 seconds). Locking in the plan before the timer hits zero awards a **"Quick Dispatch" +15% tip bonus**. After 45 seconds, the client begins texting annoyance, and the base payout decays by 1% per second.
* **One-Button Default:** Pressing `Spacebar` / `X` instantly accepts the baseline automated route and launches the car out of the stall.

---

### (c) Progression Economy

```
Tier 1: Beater Hatchback ──► Tier 2: Cargo Van / Hot Hatch ──► Tier 3: Executive / Muscle ──► Tier 4: Heavy Rig / Exotic
(Low Gig Classes)           (Unlocks Freight & Smuggling)      (Unlocks VIP / Outrun)         (Unlocks High-End Syndicates)
```

#### Pacing Numbers
* **Average Gig Duration:** 2 to 3.5 minutes.
* **Average Gig Payout (Early Game):** $200 – $400.
* **Minor Upgrade Cost (Speed +5%, Cargo +1 Slot, etc.):** $1,000 – $1,500 (~3–4 gigs per upgrade).
* **Major Vehicle Class Tier:** $12,000 – $20,000 (~30–40 gigs + milestone gate).
* **Upgrade Sinks Per Car:** 5 tiers per stat (Speed, Cargo, Health, Appeal) across 4 stats = 20 upgrades per chassis.

#### Vehicle Class Gating (Without Frustration)
Vehicle classes must not feel like arbitrary locked doors. They are operational permits:
* **The Cargo Van:** Unlocks *Multi-Drop* and *Heavy Haul* gigs (Hatchback simply lacks physical bounding boxes for 6 pallets).
* **The Luxury Sedan:** Unlocks *VIP Chauffeur* and *Corporate Escort* gigs (Corporate clients refuse to step inside a rusted hatchback; Appeal rating must be $\ge 70$).
* **The Tuner/Muscle:** Unlocks *High-Heat Contraband* and *Underground Outrun* (requires top speed > 130 mph to outrun interceptors).
* **No Hard Walls:** If a gig requires a class the player doesn't own, offer a **"Subcontract / Lease" option**: The client provides the vehicle, but takes a 50% cut of the profits. The player tastes the content immediately without the grind, turning it into a showroom test-drive.

#### Anti-Grind Levers
* **District Surge Multipliers:** Every 3 in-game days, one of the 6 city districts rolls an economic event (e.g., "Tech Expo in Neon Heights = VIP payouts +80%," "Docks Strike = Cargo payouts 2.5x").
* **Flawless Tip Chains:** Consecutive gigs without collision damage stack a persistent tip multiplier up to 2.5x. One crash resets the streak to 1.0x. Highly skilled drivers scale the economy 250% faster.

---

### (d) Emergent Comedy via Mechanics (No Scripted Jokes)

Comedy must come from the physics engine, conflicting AI goals, and absurd cascading failures.

```
[Systemic Chain Reaction Example]
Loose Sheep in Cargo ─(Brake Hard)─► Sheep hits Windshield ─► Vision Blocked ─► 
Crash into Donut Cart ─► Cop eats Donut, drops gun ─► Pedestrian panics and steals Cop Car
```

1. **Unsecured Cargo Ragdolls & Windshield Penetration**
   * *Inspiration:* *FlatOut* / *Wobbly Life*.
   * *Mechanism:* Cargo inside vehicles has real Godot rigid-body mass. If you stop abruptly without securing cargo, the item launches forward. A heavy safe busts the front windshield and crushes a parking meter. A crate of live chickens breaks open, turning the interior cockpit view into a whirlwind of feathers that physically obstructs the camera until the player rolls down the windows.
2. **Aggro-Redirect Cascades**
   * *Inspiration:* *Far Cry* animal-vs-guard systems / *GTA* road-rage loops.
   * *Mechanism:* NPCs have an "Aggro State Machine." If a hostile cop or rival delivery driver tries to ram you, but you dodge and they ram a civilian muscle-car NPC instead, the civilian NPC drops their routine, exits the car, and physically drags the cop out of the cruiser to brawl. The player drives away cleanly while the simulation devours itself in the rearview mirror.
3. **The Absurd Passenger State-Machine**
   * *Inspiration:* *RollerCoaster Tycoon* nausea/intensity systems + *Crazy Taxi*.
   * *Mechanism:* VIPs have low tolerance thresholds. High G-forces build their "Ejection Meter." When it caps, they don’t just deduct your tip: they bail out of the moving car at 40 mph, roll into an open dumpster, or trigger a self-preservation panic AI that forces them to yank your handbrake randomly while you are at top speed.
4. **Volumetric Hazardous Spills**
   * *Inspiration:* *Goat Simulator* / *Streets of Rogue*.
   * *Mechanism:* Puncturing certain cargo drops physical decals on the road with dynamic friction/physics values:
     * *Cooking Oil:* Friction = 0.05. Any AI car hitting it spins out uncontrollably like bowling pins.
     * *Glue / Wet Cement:* Friction = 3.0. AI and player cars stop dead, causing instant 10-car chain pileups behind you.
     * *Propane Tanks:* Detonate only when hit by high-velocity impacts or backfires from an upgraded exhaust system.

---

### (e) Scripted-vs-Generic Narrative Layer

* **The Ratio:** **90% Procedural Gigs / 10% Hand-Crafted Story Missions.**
* Total Story Gigs: **25 missions total.** That’s it. They function strictly as **Tier Advancement Exams** between car classes and district licenses.
* **Pacing Architecture:** You never get a story mission through a quest log. They arrive via an emergency pager beep *only* after hitting economic and reputation milestones (e.g., Earn $25k total, hit 5-star rating in the Industrial District).

```
[10-15 Procedural Gigs] ──► [Milestone Hit] ──► [Urgent Scripted Anchor Mission] ──► [New Vehicle/District Unlocked]
```

#### 4 Scripted Mission Premises
1. **The Mistress Round-Trip (Businessman Panic)**
   * *Premise:* Pick up a sweaty corporate exec from a cheap love motel, race across town to pick up his dry-cleaned suit, then deliver him to his wedding anniversary dinner at a 5-star restaurant before his wife arrives.
   * *Twist:* If the car sustains more than 10% cosmetic damage, the wife notices the broken glass and cancels his credit card, failing the mission payout.
2. **The Yakuza Helicopter Tail**
   * *Premise:* A mob boss sits in the back of your cab, tailing his teenage daughter's first date through the city. 
   * *Twist:* You must maintain a strict distance (30m–50m). If the date tries to hold her hand at an intersection, the boss forces you to hit the horn or bump their bumper slightly without alerting them to who is inside the car.
3. **The Defective Smart-Car Escort**
   * *Premise:* A tech startup's autonomous cab has suffered a software loop and refuses to drop below 60 mph (Speed-style), zooming through the city screaming corporate platitudes via loudspeaker.
   * *Twist:* You must drive alongside it, use your own vehicle's physical body to gently steer it away from crowded intersections, and guide it onto an unfinished highway ramp into the bay.
4. **The Live Mascot Kidnapping**
   * *Premise:* Rival sports franchise hires you to transport their team mascot to the stadium—except the mascot is an enraged, tranquilized 800-pound cyber-alligator in a jersey.
   * *Twist:* The tranquilizer wears off every 45 seconds. You must intentionally hit drift apexes or slide the vehicle into lamp-posts to rattle the reptile back to sleep without destroying your chassis.

---

### (f) Retention Mechanics on ONE Static Map

To keep a single Godot-built map fresh for months, the city must never be in the same state twice.

```
Map Longevity = Dynamic Geometry + Economic Fluctuations + Asynchronous Competition
```

#### 1. Weekly City Infrastructure Shifts (Dynamic Geometry)
Never change the landmass; change the **flow network**:
* **Monday Maintenance:** The main cross-city expressway is closed for repaving. All fast routes are forced into narrow, claustrophobic alleyways.
* **Flood / Typhoon Weekend:** Low-lying canal districts are submerged; water physics apply to roads, turning muscle cars into hydroplaning death traps and making lifted utility vehicles king.
* Godot implementation: Simple collision toggle layers on pre-built detour barricades and water plane triggers. Zero new geometry assets required.

#### 2. The Daily "Hot Route" Shift (Asymmetric Seeded Run)
* Every 24 hours, the server generates a seeded **"Mega-Shift"**: A set sequence of 5 fixed drop points across the city.
* Every player runs the exact same weather, traffic seed, and cargo constraints.
* Ranked purely on: **Net Profit = Gross Bounty - Fuel Costs - Vehicle Damage - Violations**.
* Rewards: Unique anime cosmetic liveries, custom exhaust sound-fonts, interior dashboard bobbleheads (prestige, zero power-creep).

#### 3. Territory Investment / Asynchronous Money Sinks
* Once the player buys all cars, money becomes useless unless it buys the world:
  * **Buying Garages:** Buy real-estate properties scattered across the map to act as forward operating bases (instant repair, gas-free refueling, new jump-off points for pre-gig planning).
  * **Buying City Infrastructure:** The player can sink end-game cash into bribing city council members to permanently change the map:
    * Pay $150,000 to *remove the speed camera* on the main bridge.
    * Pay $300,000 to *install a high-speed ramp* over the central canal.
    * The single map becomes a customized, player-carved playground.