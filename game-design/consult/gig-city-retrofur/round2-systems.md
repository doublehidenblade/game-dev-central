### 1. The Scope Trick: Killing Pedestrians with Lore

To ship an open-world driving game in Godot without burning your budget on pedestrian navigation, collision ragdolls, crowd shaders, and moral-choice edge cases, **you do not build walking NPCs.** You build an excuse for their absence that reinforces the oppressive Showa-industrial atmosphere.

```
+-----------------------------------------------------------------------------------+
| CANDIDATE 1: The "Kuro-Kiri" (Black Mist) Industrial Smog Ordinance [RECOMMENDED] |
+-----------------------------------------------------------------------------------+
- Lore: Kurogane Bay sits under an inversion layer of sulfurous, petroleum-laced smog 
  discharged by the Zaibatsu iron foundries. Ground-level foot travel without an industrial 
  filter suit is an immediate municipal felony and a fast track to chemical bronchitis. 
  The civilian populace moves exclusively through pressurized upper-level skybridges 
  and subterranean shopping arcades.
- What You DON'T Build: Walking pedestrian AI, navmeshes on sidewalks, collision logic 
  for running people over, screaming audio barks, crowd LODs, pedestrian hitboxes.
- What You Build INSTEAD: 
  * Backlit silhouettes visible through yellow-tinted second-story skybridge windows.
  * Static NPC interactions at drive-up infrastructure: pneumatic capsule pods, curbside 
    ticket booths, drive-up ramen windows, and cargo bays with masked workers who lean 
    into your window.
  * Heavy ambient steam, visible exhaust stacks, and dripping pipes across the lower streets.
- Why It Works: It justifies the vehicle cabin as your life-support capsule. The street 
  is a machine trench; humans stay above or inside.
```

```
+-----------------------------------------------------------------------------------+
| CANDIDATE 2: The Two-Tier Infrastructure (Catwalk City)                           |
+-----------------------------------------------------------------------------------+
- Lore: Built along a tidal estuary, Kurogane Bay's street level is permanently slicked 
  with harbor slop, grease, and high-tide drainage. 30 years ago, the city converted all 
  sidewalks into drainage channels and moved foot traffic to suspended steel catwalks 
  suspended 15 feet in the air.
- What You DON'T Build: Ground-level pathfinding or collision.
- What You Build INSTEAD: Overhead catwalks with low-poly static characters looking down. 
  Deliveries are made via baskets lowered on pulleys or drop chutes straight to your roof 
  rack or trunk.
- Why It's Secondary: Requires building heavy overhead geometry everywhere, complicating 
  camera angles and lighting passes.
```

```
+-----------------------------------------------------------------------------------+
| CANDIDATE 3: The Totalitarian 24-Hour Logistics Shift Mandate                      |
+-----------------------------------------------------------------------------------+
- Lore: Under martial recovery laws, streets are strictly zoned for commercial production 
  vehicles during active operational hours. Unsanctioned foot traffic on public roadways 
  is treated as economic sabotage and penalized with hard labor.
- What You DON'T Build: Any foot traffic systems whatsoever.
- What You Build INSTEAD: Stationary checkpoint guards, automated loudspeaker towers 
  broadcasting shift whistles and propaganda, and empty sidewalks lined with barricades.
- Why It's Secondary: A bit too sterile. Candidly feels like an asset-flip ghost town 
  unless heavily stylized.
```

**Verdict:** **Go with Candidate 1 (The Kuro-Kiri).** It explains why people interact exclusively through your rolled-down window or trunk, justifies thick volumetric fog (which doubles as an aggressive draw-distance optimization in Godot), and gives the city a grim, coal-and-oil Showa identity.

---

### 2. Traffic Lights and Traffic AI: The Minimal Viable City

#### Do you need traffic lights?
**No. Cut them entirely.** 
Traditional traffic signals destroy driving flow, force players to stare at static red textures, and demand complex intersection-clearance AI states. 

**The Replacement:** **The "Tonnage Priority" Rule (Gross Weight Right-of-Way).**
In Kurogane Bay, traffic law is codified by kinetic mass:
1. **Harbor Trams & Heavy Rail** yield to nothing.
2. **Zaibatsu Haulers & Cement Mixers** yield only to rail.
3. **Sedans, Couriers, and Taxis (The Player)** yield to heavy trucks.
4. **Kei-Trucks & Three-Wheelers** yield to everyone.

Intersections feature **blinking amber hazard beacons** and **painted iron mirrors on telephone poles**. The player navigates intersections through momentum, horn blasts, and aggressive posture, not by waiting for a timer.

```
       [ Harbor Tram / Rail ] (Fixed spline, infinite mass, kills everything)
                 |
       [ Heavy Haulers ] (Fixed spline, yields only to rail, pushes cars)
                 |
  ===> [ PLAYER / Taxis / Couriers ] <=== (Dynamic physics, dodges or dies)
                 |
       [ Midget Three-Wheelers / Kei ] (Spline + brake trigger on horn)
```

#### The Minimal Traffic Fleet (3 Archetypes Only)
1. **The Harbor Tram (The Anchor):** Runs on fixed rail splines down center boulevards. Kinematic, completely unstoppable, dinging a brass bell. It acts as a moving piece of dynamic cover or a lethal wall.
2. **The Zaibatsu Heavy Hauler (The Bully):** Massive 6-wheeled cab-over trucks moving along primary arteries. They don't brake for player misbehavior; they tap their air horns and plow forward.
3. **The Midget / Kei Van (The Mobile Obstacle):** Brittle, slow-moving three-wheelers (like the Daihatsu Midget) carrying crates. Easy to bully, easy to dodge, but panic-brake if you lay on your horn.

#### The Cheap Implementation Pipeline
* **No Dynamic Steering AI:** Traffic vehicles follow raw 3D paths (Godot `Path3D` / `PathFollow3D`) baked into road lanes. They do not calculate lane changes.
* **Two Raycasts per Car:** 
  * `RayCast_Near`: Distance 4m. If colliding with a vehicle, hard-brake.
  * `RayCast_Far`: Distance 15m. If colliding with a vehicle, cut throttle by 50%.
* **The Horn Override:** When the player honks within a 12m sphere, small vehicles (`Kei` class) fire a `yield()` trigger: they swerve 1.5m to the gutter spline and freeze for 4 seconds.
* **The Despawn Bubble:** Maintain a hard cap of **12–16 active traffic vehicles** in a 150m donut around the player. If a car leaves the donut, despawn it and recycle it ahead along the player’s velocity vector.

---

### 3. Cops / Heat: Showa Bureaucratic Enforcement

Forget *GTA* 5-star airborne swarms. Kurogane Bay has no GPS, no helicopters, and no centralized compute. Law enforcement is run by the **Kurogane Municipal Traffic Enforcement Division (KMTED)**: bored, underpaid officers driving heavy, understeered pursuit sedans with mechanical roof sirens and dashboard dispatch radios.

```
                        [ INFRACTION OCCURS ]
                                  |
                +-----------------+-----------------+
                |                                   |
         Stationary Cop                     Signal Box Tripped
       (Sees you directly)                 (Excessive speed trap)
                |                                   |
                +-----------------+-----------------+
                                  |
                        [ HEAT LEVEL RISES ]
                                  |
         +------------------------+------------------------+
         |                                                 |
   HEAT 1: THE TICKET                                HEAT 2: THE RAM
   - Solo cruiser tailgating.                         - 2 cruisers attempt to
   - Loudspeaker barking.                               box & pin against walls.
   - Demands you pull over.                           - Roadblocks at toll bridges.
         |                                                 |
         +------------------------+------------------------+
                                  |
                             HEAT 3: SEIZURE
                             - Heavy paddy wagons ram head-on.
                             - Iron spike barricades at district borders.
```

#### Mechanics of Heat
* **Heat Accrual:** You do not get heat for driving fast in back alleys. Heat builds through **visible friction**:
  * Tearing down state telephone/pneumatic poles.
  * Blowing through toll plazas without paying the coin-hopper.
  * Speeding past stationary patrol boxes (*Kōban*) situated at major intersections.
* **The Pursuit Dynamic:** KMTED cruisers do not shoot guns; they use **mechanical leverage**. They pull alongside, scrape your paint, and use their heavy push-bars to force you into street furniture, seawalls, or tram corridors to immobilize your chassis.
* **Shedding Heat:**
  * **The Alley Break:** Break line-of-sight for 8 seconds, turn off your headlamps via a dash toggle, and idle your engine in a dead-end or beneath an elevated rail bridge.
  * **Toll Gate Escape:** Blow through a toll gate into another Zaibatsu district. KMTED jurisdiction breaks down at corporate borders unless your Heat is maxed.
  * **The Bribe Chute:** Drive past a Kōban or drop-box and launch a fat envelope of scrip into their pneumatic receiver using your bumper interaction.

#### The Demoted Traffic Detective Fare: "Inspector Makino"
Makino is your cheat code and your systemic chaos agent.
* **The Passive Perk:** While Makino is riding in your passenger seat, your Heat is locked to **ZERO**. Patrol cruisers tap their sirens in salute as you pass; toll gates open automatically.
* **The Complication:** Makino is a chain-smoking degenerate demoted to processing municipal impounds. He routinely orders you to commit blatant moving violations to settle his personal beefs ("Clip that courier's fender," "Blow this toll plaza, I don't pay corporate taxes"). 
* **The Gig Tension:** If you carry contraband for the harbor syndicates *while* Makino is in your cab, your payout doubles (the ultimate irony), but if your vehicle takes heavy chassis damage, his glovebox contraband check triggers, flipping him instantly into a deadly close-quarters cabin threat.

---

### 4. Build / Cut / Fake Master Scope Sheet

| System | Verdict | One-Line Technical Justification | Canonical Lore Reason for Cut |
| :--- | :--- | :--- | :--- |
| **Pedestrians** | **FAKE** | Static 2D card silhouettes in windows + 3D curb-side pickup models with zero locomotion AI. | **The Kuro-Kiri Smog Ordinance:** Ground-level foot travel without breathing apparatus is a municipal felony. |
| **Traffic Lights** | **CUT** | Eliminates idle player downtime and intersection state-machine bugs. | **Gross Tonnage Rule:** Showa industrial deregulation grants right-of-way strictly to larger industrial vehicles. |
| **Traffic AI** | **FAKE** | 12-car donut pool running strictly on baked lane splines with raycast braking; no pathfinding. | *N/A (System is faked, not cut).* |
| **Cops / Heat** | **BUILD** | Lightweight 2-car physics chase state targeting vehicle pinning, shedding via line-of-sight & bribes. | *N/A (Built to drive gig stakes).* |
| **Day / Night Cycle**| **CUT** | Dynamic shadows and global illumination passes in open-world Godot destroy frame budgets. | **Perpetual Smog Twilight:** The sky is permanently choked in charcoal industry haze; time is measured by factory shift horns, not the sun. |
| **Weather** | **BUILD** | Screen-space rain/oil-slick shaders and altered tire friction curves provide massive atmospheric ROI for cheap. | *N/A (Rain/wet asphalt is foundational to Showa neo-noir).* |