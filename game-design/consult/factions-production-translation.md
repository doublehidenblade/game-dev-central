Here is the technical production breakdown for translating your faction art book into Godot 4 under mobile-class rendering constraints (TBDR architectures, low vertex budgets, fill-rate sensitivity, custom inverted-hull outline shaders, and dense distance fog).

---

### a) Gokuraku-kai Mask System: Geometry vs. Texture Swap

**Verdict: Texture/Atlas Swap on ONE Mesh (Do NOT model geometry).**

*   **The Technical Reality:** At distance, geometry modeled for the "smile" or the "acoustic grille" will completely collapse. Under Godot 4’s inverted-hull outline pass (which extrudes vertices along averaged normals), micro-geometry on facial features causes inverted-hull self-intersection, producing black, clotted artifacts ("ink cancer") around the mouth.
*   **Implementation:** 
    *   Maintain **one single base mask mesh** for all ranks.
    *   Pack the Footman (plain black lacquer) and Inner Circle (black lacquer + red smile + brass grille) into the same texture atlas. 
    *   To prevent draw-call fragmentation (material swapping breaks Godot’s batching/multimeshing), pass an integer flag via vertex colors or `INSTANCE_CUSTOM.x` to offset the UV coordinates in your custom spatial shader.
*   **Where Geometry IS Allowed:** **Kanzaki’s amber goggles.** Goggles break the external silhouette profile of the cranium. Give Kanzaki a dedicated head mesh variant where the goggles are low-poly, chunky blockouts (8–12 triangles) that physically interrupt the inverted-hull silhouette pass.

---

### b) Distance Readability Ranking in Heavy Ochre Dust Fog (at 100m)

In Godot 4, fog attenuates color toward the environment clear color via Beer-Lambert extinction: 
$$\text{FinalColor} = \text{SurfaceColor} \cdot e^{-kd} + \text{FogColor} \cdot (1 - e^{-kd})$$

At 100m, high-frequency data and subtle value shifts are obliterated. Here is the strict hierarchy of what survives:

```
[BEST]  1. Reflective-Tape / Emissive Strips
        2. Big Livery / Banner Poster-Color Fields
[WORST] 3. Stenciled Insignia Decals
```

#### 1. Reflective-Tape Strips (Emissive/Unshaded Material) — *Most Reliable*
*   **Why:** Normal diffuse cel-shading gets washed out by the ambient ochre fog. Reflective tape must be authored as an **emissive shader component** that writes directly to the color buffer with an unshaded ceiling or self-illumination scalar. It pierces the fog volume where passive albedo dies.

#### 2. Big Banner / Livery Color Fields — *Highly Reliable*
*   **Why:** Large geometric blocks of un-textured poster color (e.g., solid sodium-orange coveralls, bruised-plum trench coats) survive down to the lowest mipmap levels without flickering. They occupy contiguous pixel blocks on low-res mobile screens (e.g., a 20-pixel-high coat reads instantly as an A-line plum silhouette against an ochre background).

#### 3. Stenciled Insignia Decals — *Completely Dead at 100m*
*   **Why:** A crane-hook kamon or police badge scaled to a chest or door occupies roughly $2 \times 2$ to $4 \times 4$ pixels at 100m. Bilinear/trilinear filtering turns it into a dirty gray smudge. Furthermore, decals require extra depth-texture samples or alpha blending—pure fill-rate poison on mobile GPUs. **Never rely on stencils for distance faction ID.**

---

### c) Per-Faction: Non-Negotiables vs. Cheapest Cuts

| Faction | The ONE Non-Negotiable Read (Must NOT Cut) | The Cheapest-to-Cut Detail (Dies Instantly) |
| :--- | :--- | :--- |
| **1. Kaiun-Gumi** *(Dockers)* | **Sodium-Orange Block + Emissive T-Bar Chest Band.** Hard, square sandblaster box-hood silhouette. The T-bar gives instant chest/back orientation in dense fog. | **Crane-hook insignia & canvas folds.** Model the coveralls as straight, rigid, low-poly cylinders. Do not attempt modeled wrinkles. |
| **2. Gokuraku-Kai** *(Cabaret)* | **Vertical A-Line Column Silhouette + Bruised-Plum Value Drop.** Trench coat must extend to the floor to create an unmistakable narrow, vertical block that reads entirely black/dark against bright ochre dust. | **Gold-leaf filigree trim.** Micro-trim turns to shimmering subpixel noise at 30m+ and inflates inverted-hull vertex counts. Cut it to flat texture or eliminate entirely. |
| **3. Tsuru-Kai** *(Fishmongers)* | **Stark White Lower-Leg Blocks (Rubber Boots).** Ground-level value contrast against mud/fog + the tall, rigid verticality of truck-mounted Nobori banners. | **Crane kamon on apron belly & copper scrubber canisters.** At 100m, the apron is just an indigo-dyed quad. The scrubbers read as noise. |
| **4. Iron Wheel** *(Mechanics)* | **Asymmetric High-Vis Right Arm/Leg Only.** When an Iron Wheel NPC/vehicle is driving or running, you must instantly read their vector/heading based entirely on whether the orange hazard bar is camera-facing. | **Patched/welded livery seams & checkerboard banners.** Sub-pixel dither nightmare. Welded panel seams do not survive 2-band cel shading anyway. |
| **5. KMTED** *(Traffic Cops)* | **Flashing Mechanical Push-Bar / Roof Siren Light.** On characters: Stark white bucket helmet + high-riding square respirator (breaks the chin-neck transition). | **Badge numbers, fine belt stripes, and mechanical pursuit sedan greebles.** All fine municipal texturing gets culled. |

---

### d) Micro-Props, Geometry, and LOD Breakpoints

*Micro-props: Brass acoustic grilles, copper scrubber tanks, twin filter cones, gold-leaf trim.*

#### Do they need 3D geometry at 100m?
**No. Zero triangles.** At 100m, every character must be an **LOD2 impostor or unified single-mesh hull** under 400 triangles with zero detached prop geometry. If you run an inverted-hull pass on a detached 12-polygon cylinder at 100m, the hull thickness will completely engulf the prop, rendering it a floating black dot.

#### LOD Breakpoints and Budget Earners

| Prop | 0–15m (LOD0) | 15–40m (LOD1) | 40m–100m (LOD2) | Poly Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Twin Filter Cones** *(Iron Wheel)* | **3D Geometry** (Hexagonal prisms, 12 tris each) | **3D Geometry** (Merged to helmet silhouette) | **Flat Texture** | **EARNS POLYGONS.** Cones extend outside the head perimeter and break the human circle into an aggressive insectoid wedge. |
| **Copper Scrubbers** *(Tsuru-Kai)* | **3D Geometry** (Boxy bevels, 8 tris) | **Flat Texture** (Bake into collar mass) | **Culled** | **MEDIUM.** Cheeks are round; canisters add a blocky silhouette only within close interaction/ramming range. |
| **Acoustic Grille** *(Gokuraku)* | **Flat Texture** (Roughness/Normal step) | **Flat Texture** | **Flat Texture** | **ZERO POLY BUDGET.** It sits entirely within the interior plane of the mask. Geometry here is production malpractice. |
| **Gold-Leaf Trim** *(Gokuraku)* | **Flat Texture** (Cel-specular ramp mask) | **Flat Texture** | **Culled** | **ZERO POLY BUDGET.** Modeled trim geometry creates coplanar Z-fighting on mobile depth buffers. |

---

### e) Asset-Budget Traps: Concept Art vs. Mobile 3D

#### 1. The Nobori Banner Trap (Cloth Physics / Alpha Cutouts)
*   **The Trap:** Reference art shows flowing, dynamic samurai banners flapping off the back of Tsuru-Kai fishmonger trucks.
*   **The Mobile Reality:** Dynamic bones/cloth compute on mobile CPUs will destroy your frame budget during multi-vehicle chases. Using dynamic `AlphaScissor` or alpha blending for shredded banner edges kills TBDR tile performance through non-opaque depth writes.
*   **The Godot 4 Solution:** Model the nobori banners as **rigid, solid low-poly cards** with baked vertex-shader wind sway (using simple `sin(TIME * freq + VERTEX.y)` math in the vertex stage). The banner geometry must be opaque, hard-edged, and completely un-skinned, attached directly to the vehicle chassis node.

#### 2. Inverted-Hull Outlines on Floating Props (The "Black Clot" Trap)
*   **The Trap:** Concept art shows straps, dangling filter tubes, push-bars, and radio antennas outlined in crisp, stylish ink lines.
*   **The Mobile Reality:** Godot's inverted hull (`Cull Mode = Front`, vertex displacement along normal) duplicates draw calls and inflates vertex processing. If applied to thin, detached sub-objects (like antennae or straps), the inflated back-faces will be wider than the object itself. The screen fills with disjointed floating black splotches.
*   **The Godot 4 Solution:** Set a hard visual rule: **The ink outline shader is ONLY applied to base body masses (chassis, torso, cranium).** All sub-props, filters, push-bars, and accessories share an interior un-outlined pass or are integrated into the main manifold mesh.

#### 3. Stylized "Gold-Leaf" Specular Shaders in Dense Fog
*   **The Trap:** Gokuraku-Kai's art book calls for shimmering, metallic gold leaf accents reflecting light through the haze.
*   **The Mobile Reality:** PBR metallic reflections rely on Environment map probes or Screen Space Reflections (SSR). In Godot Forward Mobile or Compatibility, high-roughness metallic reflections blend poorly with distance fog formulas, often glowing unnaturally inside fog volumes or popping between light regions.
*   **The Godot 4 Solution:** Implement gold-leaf as an **unshaded MatCap texture** masked by an ORM channel. Fake the stylized glint with a sharp `step(threshold, dot(NORMAL, LIGHT_DIR))` in your custom cel-shader. Never introduce a standard metallic reflection probe workflow on mobile for a faction trim detail.