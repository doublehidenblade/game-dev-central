# Research: Realistic texturing — Godot 4 PBR workflow + pseudo-3D racer techniques

> Researched: 2026-09-22 by deep-research agent (web sources, isolated browser) + coordinator synthesis.
> Caveat: numbers/prices/ToS are web-derived as of 2026-09-22 — re-verify before spending or shipping. Items marked `[?]` were flagged unverifiable by the researcher.

## TL;DR

- **Godot 4 realism = complete PBR map sets + correct import settings + lighting (SDFGI/lightmaps, SSAO) + AgX tonemap.** The $0 pipeline (ambientCG/Poly Haven CC0 maps + Material Maker + Blender for UV/bake only) reaches the bar. Blender is unavoidable *only* for UV unwrapping and normal/AO baking.
- **Hyper3D (Rodin) is made by Deemos — not "formerly Luma AI."** Text/image→3D with native PBR textures, but treat AI output as raw material needing cleanup, not final assets. Free tier = evaluation; commercial rights come with paid plans ($30/mo Creator). Cheapest game-asset AI route: Tripo3D (~$0.15–0.40/model).
- **Honest bar-setting:** the *shipped* photorealistic Godot 4 game list is thin — most shipped Godot 3D games are stylized. The visual bar is best shown by engine demos + Road to Vostok (mixed reception — bar *and* cautionary tale).
- **Pseudo-3D texturing that holds up:** roads as per-scanline horizontal quads (each slice = uniform depth, so the affine-warping problem never occurs), rumble/lane/ground stripes keyed to *world* z / segment index (never screen space), billboard sprites projected from true-3D positions (OutRun's Super Scaler principle), color-lerp opaque fog — no alpha fades. The current NEON DRIFT failure classes (flat/repeating textures, stripes not moving in perspective, static water) each have a known fix in this list.
- **State-of-the-art gallery** (the "look at this — this is the best it can look" bar) is in section B4 below.

---

# TRACK A — Realistic textures in Godot 4

## A1. The standard PBR workflow (StandardMaterial3D)

Godot 4 uses the metallic/roughness workflow:

```gdscript
mat.albedo_texture      = load("wood_albedo.png")   # sRGB
mat.normal_enabled      = true                      # must enable first
mat.normal_texture      = load("wood_normal.png")
mat.orm_texture         = load("wood_orm.png")      # R=AO, G=Roughness, B=Metallic
```

- **Map roles:** albedo = base color with *no lighting baked in*; normal = per-pixel surface perturbation; roughness 0 (mirror)→1 (diffuse); metallic 0 = dielectric, 1 = metal; AO = cavity darkening; optional height for parallax mapping. Packing AO/Rough/Metal into one ORM texture halves samples/memory.
- **Color space (this visibly breaks lighting when wrong):** albedo = **sRGB**; normal/roughness/metallic/AO/ORM = **linear**. Set per-texture in the Import dock.
- **Filtering:** `TEXTURE_FILTER_LINEAR_WITH_MIPMAPS`, mipmaps generated on import. NEAREST aliases HD detail; no-mipmaps shimmers at grazing angles.
- **Normal handedness:** DirectX-style maps (green channel down) light inverted in Godot — fix with "Normal Map: Flip Y" on advanced import.

**What separates flat from realistic — four layers, roughly in order of impact:**

1. **Map completeness.** Flat = albedo-only (or flat colors). Realistic = normal + roughness variation + AO + metallic masks per surface. Micro-surface breakup is what kills the CG-flat look.
2. **Correct import settings** (sRGB vs linear, mipmaps).
3. **Lighting.** SDFGI (real-time open-world GI), VoxelGI, or GPU-baked lightmaps; SSAO/SSIL for contact detail; SSR or reflection probes.
4. **Atmosphere + color.** Volumetric fog, decals (cracks/stains/projected detail), **AgX tonemapping** (best hue preservation — then raise contrast/saturation in the Adjustments tab for punch); optional physical light units.

Sources: Godot 4.0 launch article (godotengine.org/article/godot-4-0-sets-sail) · hexaquo.at photorealistic-setup guide (https://hexaquo.at/pages/environment-and-light-in-godot-setting-up-for-photorealistic-3d-graphics/)

## A2. Is Blender needed? (Required vs optional)

| Step | Needed? | Why / substitute |
|---|---|---|
| UV unwrapping | **Yes, for any baked texturing** | Baking needs a UV map (3D polygons → 2D pixels); Godot cannot unwrap |
| Baking normal/AO from high-poly | **Yes (Blender/Substance)** | Standard high→low bake ("Selected to Active", cage, ray distance) |
| Retopology | **Yes for sculpted/AI meshes** | AI meshes come high-poly/messy; retopo/decimate to game budgets |
| Modeling generic props | Optional | glTF kits (Kenney/KayKit/Quaternius, CC0) cover a lot; Godot CSG for prototyping |
| Procedural materials | **No — Godot alone** | **Material Maker** (materialmaker.org, MIT, Godot-community) — node-based, exports PBR map sets *and* Godot shaders directly; the free Substance Designer substitute |
| Missing-map generation | **No** | **Materialize** (boundingboxsoftware.com, free): synthesize normal/height/AO from a single albedo |
| Texture painting | **No** | **ArmorLab** (armorpaint.org, free/open-source 3D painting); Krita/GIMP for painting + channel packing |
| Lightmaps | **No (in-engine)** | Godot 4 bakes lightmaps on GPU in-editor |

Rule of thumb: Blender is the unavoidable step only where **UVs + bakes** are concerned. Everything else has a free Godot-side substitute.

## A3. Hyper3D (Rodin) — facts, with a premise correction

**Correction:** Hyper3D is made by **Deemos** (Wilmington, DE) — it is *not* "formerly Luma AI." Luma AI is a separate company; its Genie text-to-3D was **sunset 2026-01-01**.

- **What it produces:** text- or image-to-3D (single/multi-view refs), Gen-2.5. Textured mesh with **native PBR textures**, clean quad topology options (4k–50k faces), T/A-pose characters for rigging, up to **10M+ polygon** geometry, optional **HighPack 4K texture** fidelity pack; exports GLB/FBX/OBJ/USDZ; API + web editor. Generation: geometry ~4s, textured model ~5–20s.
- **Texture quality:** strongest high-fidelity output among the AI tools per community reviews — but still needs artist cleanup (decimate, recolor, re-export). Treat output as **raw material, not final**.
- **Pricing (checked 2026-08-28):** Creator **$30/mo** ($24 annual), Business **$120/mo** ($96 annual), Education $12/mo, Enterprise custom; free tier = starter credits, evaluation. **Treat free-tier output as non-commercial by default** — commercial rights come with paid plans + private generation. **Re-verify live ToS before shipping** — tier terms changed between 2025 and Aug 2026.
- **Practical limits:** high-poly output needs retopo/decimation for games; style control = prompt + reference images (no deterministic art-direction lock); seed-based variation only. Exact per-tier texture resolutions/poly budgets not confirmed from Deemos directly — treat as approximate.

**Alternatives, one line each:**

- **Tripo3D** (tripo3d.ai) — current consensus best for *game* assets: fastest, cleanest quad topology, one-click auto-rigging, Blender plugin + MCP; ~$0.15–0.40/model, $10–50/mo.
- **Meshy** (meshy.ai) — most polished mainstream alternative, good API + AI texturing; 200 free credits/mo, $20–60/mo.
- **Sloyd** (sloyd.ai) — parametric + AI hybrid: slider templates for game-ready low-poly props/weapons/buildings (clean topology, auto UVs, LODs, AI texturing to 2K); unlimited generation on paid plans.
- **TRELLIS.2** (Microsoft, MIT) — open-source SOTA image→3D with PBR; needs CUDA GPU (impractical on Apple Silicon — use cloud GPU/hosted endpoint).
- **Hunyuan3D 2.1** — open weights with PBR pipeline; 2.5/3.0 are hosted-API only.

## A4. Non-AI routes + the state-of-the-art bar

- **ambientCG** (https://ambientcg.com/) — ~2,000 **CC0** PBR materials, every map (albedo/normal/rough/metal/AO/height), multi-res to 16K; bundling in a shipped game explicitly allowed. **Start here.**
- **Poly Haven** (https://polyhaven.com/textures) — CC0, fewer but top-tier photoscanned materials (8K+, displacement maps), plus HDRIs and models.
- **Texture discipline:** ship **2K** (1K for background); pack channels; always verify tiling. Photo-scanned look without shooting your own = Poly Haven photoscans.

**Best-in-class Godot 4 visual references** (honest assessment: the *shipped* photoreal bar in Godot 4 is thin — most shipped Godot 3D games are stylized; the engine can do it, the ecosystem proof is mostly demos + one showcase):

1. **Godot 4.0 official demos/media** — SDFGI interiors, volumetric fog, decals, SSAO: the engine-capability bar. https://godotengine.org/article/godot-4-0-sets-sail/
2. **Road to Vostok** (Steam demo, app 1963610) — the community's de-facto realistic 3D Godot showcase (Unity port); Steam discussion notes dated visuals/glitches despite heavy custom work — useful as both bar *and* cautionary tale. https://steamcommunity.com/app/1963610/discussions/0/4629233756626052446
3. **Photorealistic setup guide** (hexaquo.at) — what a correct lighting/tonemap stack looks like, with comparison images. https://hexaquo.at/pages/environment-and-light-in-godot-setting-up-for-photorealistic-3d-graphics/

## A5. Cheapest realistic pipeline for a solo dev, 2026 — total $0

1. **Base surfaces (no art skill):** download CC0 PBR sets from ambientCG (breadth) / Poly Haven (hero photoscans); wire albedo+normal+ORM into StandardMaterial3D; correct import settings. Skill: file management.
2. **Custom materials (node logic):** Material Maker — author procedural PBR sets, export directly to Godot shaders. Skill: node-graph thinking, learnable in days.
3. **Unique models (moderate Blender):** Blender for UV unwrap + high→low bakes + retopo of sculpts/AI outputs. The steepest step — ~2–4 weeks to competence for baking/UV specifically.
4. **Missing maps:** Materialize (albedo→normal/AO/height); ArmorLab for painted detail/decals in-engine.
5. **Lighting (in-engine):** SDFGI or GPU lightmaps, SSAO/SSIL, AgX tonemap + adjustments.
6. **Optional AI boost ($0.10–0.50/model or $10–30/mo):** Tripo3D credits for hard-surface props; Hyper3D Creator ($30/mo) for hero assets. Budget 1–2 hours cleanup per model.
7. **Models you don't author ($0):** Kenney/KayKit/Quaternius CC0 kits for everything generic.

Skip: Substance Painter/Designer subscriptions, paid texture libraries, paid AI tiers — none are required to reach the bar.

---

# TRACK B — Texturing in pseudo-3D racers

## B1. How the good ones actually render textures

**Canonical DIY reference** — Jake Gordon's JS racer (verified live): https://codeincomplete.com/articles/javascript-racer — divide the track into **segments**, **project** each (world→camera→screen with perspective scale), **render back-to-front** (painter's algorithm, no z-buffer); curves = X offsets, hills = Y offsets, clip line hides segments behind crests.

- **Road surface:** each horizontal scanline is a **depth slice** — scale = 1/(y_screen − horizon), road width = base × scale. The road is filled as flat horizontal quads per slice — **no UV mapping on the road**, so the classic affine-warping problem never occurs. Detail = world-locked per-segment color alternation, lane-marking strips drawn as narrower scaled quads within the segment.
- **Rumble strips / lane markings:** drawn in *world* space — pattern offset derives from the segment index / world distance, never screen position, so markings stay glued to the road and compress correctly toward the horizon.
- **Shoulder/ground stripes:** alternating ground colors per segment group (e.g. 3-segment bands) give the checkerboard/striped ground of OutRun-era games; stripes "move" because the *segment pattern* scrolls with playerZ.
- **Sprites (trees, buildings, billboards):** projected billboards — screenX = center + scale·cameraX·w/2, scale ∝ 1/z — drawn far-to-near with clipping. OutRun's actual method: positions/movement computed in **true 3D**, then the appropriate pre-drawn sprite variant displayed and hardware-scaled (Super Scaler).
- **Affine vs perspective-correct:** linearly interpolating UVs in screen space causes swimming/warping; the correct fix interpolates u/z and 1/z per pixel. Pseudo-3D engines **sidestep the whole problem**: scanline quads have uniform depth per slice, and billboards are flat — no UV interpolation across depth ever happens. This is *why* the technique looks stable. **Warping only appears if you try to texture-map a trapezoid spanning multiple depths.**
- **Pre-scaled sprite strips:** pre-render sprites at a set of discrete scales (or drawImage with smoothing off at low res) and snap to nearest — avoids per-frame resampling shimmer. OutRun did this in ROM/hardware; JS engines can do it with offscreen canvases.
- **Parallax backgrounds:** 2–3 layers offset by accumulated curve value (sky, far hills, near hills).

Sources: codeincomplete.com/articles/javascript-racer (verified live) · moegamer.net/2019/07/18/sega-ages-outrun/ · en.wikipedia.org/wiki/Out_Run

## B2. Common failure modes → how the best solve each

| Failure mode | Fix (as the best do it) |
|---|---|
| Road looks flat/repetitive | World-locked rumble alternation + noise-dithered asphalt (bake grain into a small strip texture, drawn per segment), lane dashes, oil/skid marks as segment-locked decals, fog to horizon |
| Roadside props obviously repeat | Multiple sprite variants per biome, randomized lateral offset/scale, clustered compositions (tree+rock+bush as one "set"), distance fog hiding pop-in; change prop *sets* per track section (OutRun's 15 varied stages) |
| Textures don't move in perspective | All offsets keyed to world z / segment index — never screen space; background layers parallaxed by curve accumulation |
| Water looks static [?] | Screen-space water bands beside the road with **world-locked horizontal offset** (scroll = f(playerZ) + sin(time) wave term), plus a second offset "sparkle" strip. Standard practice; no named-game source found documenting it |
| Sprite pop-in at draw distance | Color-lerp fog per segment (opaque — no alpha), so distant sprites fade *in color* not transparency; dense haze at horizon |
| Shimmer on scaled sprites | Pre-scaled sprite buckets / nearest-scale snapping; avoid resampling every frame at fractional scales |

## B3. State-of-the-art gallery — "this is the best it can look"

Each entry below has a **verified direct image** (HTTP 200, content-type image/*, checked 2026-09-22) plus a label of exactly what it demonstrates. These are the visual bars to hold NEON DRIFT's sprite work against.

**Pseudo-3D racers:**

1. **Slipstream** (ansdor, 2018) — the authenticity bar.
   ![Slipstream screenshot](https://media.rawg.io/media/resize/1280/-/screenshots/41e/41e72fd7afde605b4f0d91bd7fd5889e.jpg)
   *What it demonstrates:* hand-made 2D sprite consistency across biomes (desert/city/beach), trackside variety without visible repetition, authentic engine feel with CRT+NTSC filters. 20 tracks, Very Positive (88%, 1,728 Steam reviews). Custom pseudo-3D engine built with Krita/Blender/GIMP on Linux. Source: https://RAWG.io/games/slipstream/screenshots

2. **Horizon Chase Turbo** (Aquiris, 2018) — the color/weather bar.
   ![Horizon Chase Turbo screenshot](https://cdn.mobygames.com/d3ef7bd2-ac07-11ed-b85a-02420a000135.webp)
   *What it demonstrates:* color scripting per location, weather systems (rain/snow/fog/day/night), cel-shaded pop, sense of place. 109 tracks, 4K. Source: https://www.mobygames.com/game/108783/horizon-chase-turbo/screenshots/

3. **Final Freeway 2R** (Oyatsukai, iOS 2012) — the pixel-detail bar.
   ![Final Freeway 2R screenshot](https://media.pocketgamer.com/artwork/na-bxin/final-freeway-2r-ios-5_jpg_640.webp)
   *What it demonstrates:* how much texture detail survives at speed, cohesive pixel art direction, "more detailed sprite work and a greater draw distance," "ridiculous" sense of speed. 13–14 environments, branching paths. Source: https://www.pocketgamer.com/final-freeway-2r/review/

4. **80's OVERDRIVE** (Insane Code; 3DS 2017 / Switch 2020) — the pixel-art + scaling bar.
   ![80's OVERDRIVE screenshot](https://xboxwire.thesourcemediaassets.com/sites/2/2022/07/80s_overdrive-2bf64dfb57ef23a2398f.jpg)
   *What it demonstrates:* handcrafted pixel art that holds up under continuous sprite scaling ("pixel-rich visuals… sprite scaling is smooth and convincing" — Nintendo Life), neon 80s look across 8 visual themes. Source: https://news.xbox.com/en-us/2022/07/08/next-week-on-xbox-new-games-for-july-11-to-15/

5. **Formula Retro Racing: World Tour** (Repixel8/CGA Studio, 2023) — the 3D proof.
   ![Formula Retro Racing: World Tour screenshot](https://worthplaying.com/wpimages/f/o/formularetroracingworldtour/572338.jpg)
   *What it demonstrates:* NOT sprite pseudo-3D — real low-poly 3D (Unity) with the 90s arcade feel at 4K/60fps. Included deliberately: proof that the *aesthetic* target is reachable with true 3D — directly relevant to the Godot side. Trackside density in real 3D. Source: https://worthplaying.com/article/2022/9/15/news/133761-formula-retro-racing-world-tour-is-a-retro-racing-game-coming-to-consoles-in-december-pc-in-2023-playable-demo-now-screens-trailer/images/572338/

**Godot 4 visual bar:**

6. **Road to Vostok** (Steam demo, app 1963610) — the de-facto realistic 3D Godot showcase (Unity port); bar *and* cautionary tale (dated visuals/glitches despite heavy custom work per Steam discussion).
   ![Road to Vostok screenshot](https://clan.fastly.steamstatic.com/images/42476930/6902de48b3d00f8b1ee8aff3ec12157ca6549792.png)
   *What it demonstrates:* the realistic-texture ceiling in Godot 4 — PBR materials, lighting, atmosphere pushed hard, and where it still falls short. Source: https://steamcommunity.com/app/1963610 (see also discussion: https://steamcommunity.com/app/1963610/discussions/0/4629233756626052446)

7. **Godot 4.0 official engine capability** (SDFGI, volumetric fog, decals, SSAO, AgX) — the engine-can-do-it proof.
   ![Godot 4.0 Vulkan rendering](https://itsfoss.com/content/images/size/w600/2023/03/Godot_4.0_vulkan_opengl_rendering.jpg)
   *What it demonstrates:* what the correct lighting/tonemap stack (SDFGI interiors, volumetric fog, decals, SSAO, AgX) looks like when fully wired — the engine-side bar, independent of any shipped game's art. Source: https://itsfoss.com/news/godot-4-0-release/ · setup guide: https://hexaquo.at/pages/environment-and-light-in-godot-setting-up-for-photorealistic-3d-graphics/

## B4. Practical techniques for a JS/canvas pseudo-3D engine

- **Road:** draw each segment as a 1–3px horizontal trapezoid, far→near; colors chosen by segment index (asphalt/rumble/lane/ground bands) — world-locked, so all striping moves in correct perspective automatically. Quantize per-segment scale steps to reduce shimmer.
- **Detailed road surface:** pre-render a small strip texture (asphalt noise + edge wear) on an offscreen canvas; `drawImage` it per segment scaled to segment width with offset = playerZ mod stripLength. **Never stretch one texture across the whole road** (that's where warping/swimming comes from).
- **Sprite strips for tunnels:** tunnel = segments flagged "tunnel"; for those, draw wide billboards (left wall / right wall / ceiling) spanning beyond road width, projected like sprites with baked lighting gradients; approaching darkness handled by per-segment color lerp. All opaque.
- **Animated water:** for segments adjacent to water, draw screen-space horizontal water bands with `offsetX = (playerZ * k + sin(time * w)) mod bandWidth`, plus a second thinner "sparkle" strip at a different scroll rate. World-locked base + time-locked shimmer = reads as moving water.
- **100% opaque seams:** painter's algorithm + clip line; hide pop-in with **color-lerp fog** (blend segment colors toward sky color by depth — no alpha needed); dither segment transitions. No alpha fades anywhere.
- **Perf (from the codeincomplete community):** `clearRect` only dirty areas; cache background layers on separate canvases and redraw only on change; project once per segment.

---

## Apply to Craig's projects

- **Tokyo Drift 3D (Godot):** the current build is real texturing but stylized/materially shallow — not broadly "untextured/flat" (see td-014 PBR audit): AmbientCG color/normal/roughness maps are wired for road/terrain, facade texture families exist, foliage has per-instance tint — but windows are flat, neon strips/barriers/torii lack normal/AO, road markings are emissive geometry rather than integrated paint, car paint has no real metallic/clearcoat/roughness, and no UV/bake pipeline exists. The next pass should be: full PBR coverage by material family (windows with depth/normal/AO, car paint metallic/clearcoat/roughness), road detail that survives at driving distance, signage/rooftop dressing, and output-level CI measuring rendered material contribution. Track in td-014/td-015 or a follow-up task.
- **NEON DRIFT (pseudo-3D):** the two open texture-class items are already in TODO 122 — 122-2 (ground stripes must be world-projection-driven, matching B1/B2 above) and 122-3 (Slipstream learn list: sprite-art consistency with little canvas use, water via offset strips). The B4 strip-texture and water techniques above are directly implementable suggestions for Codex (Muse's opinion only).

## Open questions (researcher-flagged, not resolved)

- No shipped photorealistic Godot 4 title found with strong community consensus as the visual bar.
- Hyper3D exact per-tier texture resolutions/poly budgets and live ToS need re-verification at purchase time.
- Animated-water specifics in named games: technique guidance is standard practice, not a sourced fact.
