### 1. Hybrid Spine: The Verdict

**Verdict: Build B+E. Execute C strictly as seasoning, never the spine.**

* **Pure B** is clean, but leaves the solo dev sweating over producing endless bespoke story content.
* **B+E is the sweet spot.** E (deliveries) is your systemic infinite gameplay loop: high-density traffic, procedural delivery contracts, earning cash to buy junkyard parts. B (the Rival Ladder) is your structural gating: reach a rep milestone, a psycho rival blocks your turf, beat them to unlock the next district. *Persona* loop meets *Tokyo Xtreme Racer*. Day job funds the night war.
* **Failure Mode of B+E+C:** **Tonal suicide.** If the player is driving a literal toilet on wheels or the story is pure ironic shitposting, the driving mechanics immediately feel weightless. Players don’t optimize gear ratios or master apex braking for a joke. The comedy must be the *garnish* on a fundamentally high-stakes world, not the foundation.

---

### 2. Concrete F2P Economy (Mobile/Web, Godot)

#### (a) Session Model: Unlimited Runs with Diminishing Returns
**Defend it:** Energy timers scream "predatory 2014 mobile trash" and kill web engagement immediately. Arcade players want flow state. Let them drive forever. 
* *Mechanism:* First 5 delivery runs of the day pay 100% Yen. Runs 6–10 pay 50%. Runs 11+ pay 10% Yen and pure Leaderboard/XP. Grinders can grind; exploiters get choked out.

#### (b) Two Currencies
1. **Yen (Soft):** Earned via clean drifts, deliveries, and rival defeats. Buys consumable tires, engine tune-ups, and repairs.
2. **Tapes / Cassettes (Hard, Purchasable):** Earned rarely via boss wins or bought with real cash. Buys garage bays, licensed-adjacent retro aero kits, paint finishes, and instant rerolls on delivery contracts.

#### (c) The 30-Day Battle Pass: "The Midnight Pass" ($4.99)
* **Free Track:** Flat Yen payouts, basic tire sets, standard color swatches, consumable fuel boosters.
* **Paid Track:** Exclusive 1986-spec aero body kit at Tier 30, 3 vintage lo-fi synth tracks for the in-game radio, a neon interior dashboard accessory, and up to 50% of the Pass’s Cassette cost refunded through progression.

#### (d) The Never-Sell Item
**Tire Grip and Weight Distribution.** Never sell pure physics advantages for hard cash. Tuning must only be bought with in-game earned Yen and garage time. If a credit card makes a car corner sharper, your arcade game is dead.

---

### 3. Three Retention Hooks

1. **The 3:00 AM Ghost (Daily Time-Gate):** A phantom black FC RX-7 haunts the downhill route only between 02:00 and 04:00 local player time. Beating its ghost time yields an exclusive cursed cosmetic exhaust that spits purple backfire flames.
2. **Rush Hour Surge (Daily Window):** Between 8:00–9:00 AM and 6:00–7:00 PM local time, delivery contracts pay 3x Yen, but ambient traffic density increases by 300%. High-risk lane-splitting for fast progression.
3. **The Sunday Junkyard Scramble (Weekly Gauntlet):** Every Sunday, the local mechanic lends you a broken, asymmetrical death-trap with severe handling defects (e.g., pulling hard left, no handbrake). Clear three specific mountain sectors with it to scavenge a random top-tier performance part.

---

### 4. Scope Reality Check (Solo Dev + AI, 3 Months)

**Winner:** **B+E Hybrid.** Retro-futurism (D) requires too much bespoke world-building asset overhead; pure B requires writing 40 anime scripts.

**The Brutal Cuts to Ship v1:**
* **Cut Open-World Roaming:** The map is a slick, stylized 2D neon highway map vector. Click a node, jump straight onto the asphalt.
* **Cut Multi-Vehicle Physics:** Program **one** damn good arcade drift-handling model with three sliders: Weight, Grip, Acceleration. Every car in v1 uses this same base script with altered float variables.
* **Cut 3D Story Cutscenes:** Rivals are 2D visual-novel portraits with three AI-generated expressions: Smug, Sweating, Defeated. Text crawls over an engine-revving background.
* **Cut Synchronous Multiplayer:** Leaderboards and asynchronous ghost runs only. Real-time netcode will murder your 3-month timeline.

---

### 5. Weaponizing "搞抽象" (Absurdity) in Direction B

Absurdist humor works if the *characters inside the world take it dead seriously* (the *Yakuza* rule).

1. **The Volatile Cargo:** A high-paying delivery mission where you aren’t delivering illegal car parts; you’re transporting a hyper-fragile wedding cake, or an unrestrained, furious stray cat on the passenger seat. G-force meters dictate your cash bonus: drift too violently and the cat attacks the steering wheel (inverting controls for 1.5 seconds).
2. **The Corporate Salaryman Rival:** A rival who drives a totally stock, dented kei commercial van with hazards flashing, racing with unhinged, blood-vessel-bursting intensity because his delivery of fax paper is 3 minutes late and his boss will execute him. His dialogue reads like unhinged LinkedIn corporate buzzwords mixed with battle anime threats.
3. **The Decadent Unlockable:** The top-tier secret car isn’t a supercar—it’s a ridiculously over-the-top *Dekotora* (Japanese decorated chrome dump truck) completely covered in flashing 100,000-lumen stage lights that blind the rival ahead of you, with an air horn that plays an 8-bit enka song.

---

### 6. Anime Look Fit & The Art-Direction Rule

**Direction that makes it sing:** **B+E Hybrid.** Gritty, late-80s straight-to-video OVA aesthetic (think *Megazone 23*, *Riding Bean*, and early *Initial D*). The clash between gritty asphalt reality and neon-lit anime arrogance is peak arcade iconography.

**The One Rule for the AI Pipeline:**
> *"Render all assets with hard-edged, 3-tone flat cel-shading, heavy variable-width black ink outlines, hand-painted gouache skies, and zero airbrushed gradients or modern digital soft-lighting."*