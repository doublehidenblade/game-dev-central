### (a) Arcology Facade Strategy

* **P-con Holes & Slip-Form Banding:** **100% texture.** Use a single 512×512 tiling trim-sheet with baked albedo dot-grids and horizontal seams. Geometry here is an anti-pattern: at driving distance, dense vertices cause sub-pixel shimmer and triangle-setup bottlenecks.
* **Pod-Cleavage (Capsules):** **Real geometry, heavily simplified.** The characteristic silhouette read relies on casts shadows and outline stepping. Model pods as single 12-triangle boxes instanced via MultiMeshInstance3D, penetrating the core wall by 0.2m. Never model air gaps behind them.
* **Window Insets & Gaskets:** **Pure texture.** Paint the rounded gasket and glass directly onto the pod's front quad. Avoid modeled reveals or bevels; the quantized cel shader handles the lighting step across the flat face.
* **MEP Ducts/Pipes:** **Hybrid.** Do not wrap towers in 3D pipe networks. Place 4-to-6-sided polygonal extrusions *only* along external structural corners where they break the building's outer silhouette against the sky. Paint wall-climbing pipe runs directly into the core trim-sheet.

---

### (b) High-Cost Elements, Inverted-Hull Pitfalls, & Fixes

**Inverted-Hull Rule:** Any geometry thinner than $2 \times \text{grow\_amount}$ turns into solid black ink. Never apply an inverted-hull `next_pass` to alpha-tested cards, lattice trusses, or thin cables. Disable the outline pass on these meshes entirely and let high-contrast albedo create the visual edge.

* **Skyway Ribbon:**
  * *Expensive:* Modeled lattice toll gantries and crash barriers. 
  * *Substitute:* Box-girder gantries (solid rectangular extrusions) and solid concrete Jersey barriers instead of metal rails.
  * *Hull Fix:* If cables/lattice must exist, use flat 2D planes with an unlit cel-cutout shader and zero outline pass.
* **Terminal 1:**
  * *Expensive:* Exposed multi-strand elevator cables and functional Solari flap drums.
  * *Substitute:* Merge cable bundles into single thick hexagonal steel rods. Replace the Solari board with a flat, emissive quad running a stepped UV-scroll shader.
  * *Hull Fix:* Apply the outline material exclusively to the main tower volume and counterweights, never to the suspension rods.
* **Haibara Estate:**
  * *Expensive:* Modeled Japanese *kawara* barrel caps and individual cyclopean retaining wall stones.
  * *Substitute:* Roof is a simple flat wedge plane using a stepped normal map or high-contrast 512px directional striping texture; retaining wall is a single beveled cliff hull using a non-repeating world-projected UV texture.
  * *Hull Fix:* Pine tree foliage cards will render as a jumbled black mess if given hull passes. Hull-outline only the main trunk/branches; render foliage "clouds" as solid low-poly convex hulls (blobs) with inverted-hull active, rather than alpha-cutout leaf cards.

---

### (c) Dust-Cloud Sea

**The Solution:** A single flat horizontal quad mesh positioned at sea level, running a custom unlit shader:
1. Sample two scrolling low-frequency Voronoi/Simplex textures moving at differing speeds/angles.
2. Quantize the result into 2 sharp bands using `floor(val * 2.0) / 2.0` (ochre base and sunlit amber).
3. Fade edges near the cliff using depth-buffer intersection (`PROJECTION_MATRIX` linear depth comparison).

*Do not use volumetric fog, CPU particle fields, or stacked translucent planes.* Translucency forces expensive sort passes and breaks clean inverted-hull passes rendering behind it.

---

### (d) Masked Humans

**Recommendation: 2D Unlit Impostor Cards (Billboard Quads).**
* For driving cameras moving at speed, low-poly 3D characters waste skinning and draw calls.
* Use a single quad oriented Y-billboard (`StandardMaterial3D.billboard_mode = BILLBOARD_FIXED_Y`).
* Paint 4-frame run/idle loops on an 80s anime-style atlas, masks included. Ink lines are drawn directly into the sprite frames; do not use hull passes on them.
* Hard despawn/cull all figures beyond 35 meters using an aggressive visibility range (`visibility_range_end = 35.0m`).

---

### (e) Low-Poly Vehicle Budgets

* **Budget:** **300–450 triangles** for spline traffic; **800–1,000 triangles** for player/hero car.
* **What Survives:**
  * Clean silhouette-defining wedge profile (A/C-pillars, hood-to-trunk rake).
  * Solid-color opaque glass surfaces (pure 100% black/dark blue quads, zero transparency).
  * 8-sided polygonal prism wheels (flat cylinder caps, no modeled treads).
* **What Dies:**
  * Modeled wheel wells and undercarriages (seal flush with bottom hull plane).
  * Side mirrors and wipers (delete entirely or paint onto texture).
  * Headlight/taillight geometry (flat quads mapped to emissive palette indexes).
  * Separate interior or suspension meshes.

---

### Cut-First Summary Table

| Scene | Element | Cut This First | Replace With This (Cheap Read) |
|---|---|---|---|
| **Skyway Ribbon** | Road Signs / Gantries | 3D open-web steel lattice | Solid rectangular box-beam portals, no hull pass |
| **Skyway Ribbon** | MEP Facade Detailing | 3D wall-climbing pipe networks | Facade trim-sheet texture; 4-sided pipes on silhouette edges only |
| **Terminal 1** | Sky-Elevator Rigging | Individual braided steel cables | 1 solid hexagonal tension rod with flat black albedo |
| **Terminal 1** | Parking Decks | Open safety wire/mesh fences | Solid 1m concrete crash lips |
| **Haibara Estate** | Villa Roofing | Individual 3D *kawara* tiles | Flat angled plane + directional banded cel texture |
| **Haibara Estate** | Pine Foliage | Alpha-tested needle cards | Clustered low-poly convex hulls with hull outlines |
| **Global / Tech** | All Humans / Crowds | Skinned low-poly 3D meshes | 2D Y-axis billboard quads; bake ink into sprite |