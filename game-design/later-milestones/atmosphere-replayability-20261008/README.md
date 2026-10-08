# Bring back changing skies and a readable city

> Recorded: 2026-10-08 by dot, from Craig's direction of the same date
> **Later milestone; documentation only. No execution authorized now.**

[Canonical parked planning record](task.json)

## Decision and release boundary

Craig rejects heavy permanent dust and the orange veil as the long-term visual direction: it weakens the driving fantasy and hides the city's aesthetics. A small open-world city should earn repeat drives through changing atmosphere on the same recognizable routes.

Approved direction is to bring back a day/night cycle and dynamic weather in a later milestone, with clearer air as the intended default. This records direction, not proof of implementation feasibility or permission to start work. The current gigs, usable UI, lively city and traffic release comes first. This milestone is **not a release blocker** and does not claim, interrupt or reassign any active owner.

Do not implement, dispatch implementation workers, generate mocks, edit runtime code/configuration/assets/fog, trigger or rerun Actions, merge, or deploy under this filing. Resume only after the current priority release and Craig's explicit go-ahead. Upper-city alternatives below remain undecided; seasons are stretch scope.

## What this changes in the design history

The [world bible](https://github.com/doublehidenblade/game-dev-central/blob/168965ceeade680f6c8729b19a9d52059984b8d4/game-design/gig-city-world-bible.md) specifies permanent dust, fixed lighting and fog-as-culling; the [identity plan](https://github.com/doublehidenblade/game-dev-central/blob/168965ceeade680f6c8729b19a9d52059984b8d4/game-design/gig-city-retrofutur-identity.md) cuts day/night and dynamic weather; the [upper-city chapter](https://github.com/doublehidenblade/game-dev-central/blob/168965ceeade680f6c8729b19a9d52059984b8d4/game-design/art-book/upper-city/chapter.md) imposes noon-lock. Those are historical constraints that this dated, approved **future direction supersedes where they conflict**. They are not instructions to restore dust or refuse changing light when this milestone is later authorized.

This isolated addendum does not rewrite those documents or their active production tasks now. During later planning, reconcile the relevant bible sections explicitly and preserve unrelated Showa/cel, masked-character, mechanical technology, vehicle and gameplay decisions.

Draw-distance performance has **not been established as the reason this project needs permanent dust**. Older games' close draw distances are a design precedent for tolerating visible distance limits, not measured proof of this game's performance. No current frame time, FPS, safe draw distance, light count or memory budget is established by this filing.

## Intended first slice

- Reuse the same authored city routes at **dawn, noon, dusk and night**
- Support **clear, overcast and rain** initially, with controllable, reproducible transitions
- Let assets respond coherently to illumination, light color, exposure and wetness rather than applying only a full-screen tint
- Preserve the 80s-anime cel/Showa identity: readable silhouettes, deliberate cel bands, restrained local emissives, industrial materials and signage
- Keep player-facing UI in English and Japanese environmental identity/signage intact
- Seasons are an optional later exploration, not an MVP promise; do not add snow, seasonal asset sets, flood simulation, handling changes or narrative systems by implication

The user's supplied sunset image was inspected directly. It shows an expansive pink/orange sky, a legible mountain horizon, cooler foreground and vehicle surfaces, and warm local service-station lighting. Use the relationship between broad sky light, surface values, distance and local lights as inspiration. It is not a performance benchmark, a literal American-desert location brief, a requirement for neon lighting, or evidence of a production renderer. The private image is not copied into this public repository.

## Restore and adapt before inventing

Limited read-only audit, pinned to Tokyo source `9d4a88490c41f86e8d34e1c2c6f142838de20c73`:

- [CityAtmosphere](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/scripts/lower_city/city_atmosphere.gd) currently samples per-district fog, density, ambient, sun and sky values and blends them spatially. Its comment explicitly describes authored fixed light; this is a reuse/integration seam, not an existing verified day/night controller
- [Lower-city anime adapter](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/scripts/anime/anime_adapter_lower_city.gd) writes palette warmth, shadow and emission values, builds local flares/pools and sets sky-fog influence. Coordinate ownership here so a clock/weather controller and district overrides do not fight every frame
- [NightLightingRig](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/scripts/night_lighting_rig.gd) contains player-following streetlight pools and tunnel-light behavior, coupled to WorldTrack. Evaluate reuse and adaptation; its presence does not prove Lower City wiring, night acceptance or current-device performance
- The [anime road entry shader](https://github.com/doublehidenblade/tokyo-drift-3d/blob/9d4a88490c41f86e8d34e1c2c6f142838de20c73/godot/shaders/anime/anime_road.gdshader) delegates to a shared include. Review road and city material families before assuming a screen-space rain sheen is sufficient

No full history audit or runtime test was performed. At activation, inspect current source, relevant historical branches/commits and scene wiring for earlier clock/weather systems. Restore/reuse suitable existing code before proposing replacements; record why any old system is unsuitable. Do not infer from a filename search that no prior implementation exists.

## Material and lighting work to investigate later

1. **Neutral foundations:** audit baked orange albedo/vertex colors, fixed warmth multipliers, unlit surfaces, baked shadows and unconditional emission. Preserve material identity while permitting time/weather lighting; do not remove every warm material simply because the old atmosphere was warm
2. **Lighting response:** test directional sunlight/moonlight or an art-directed equivalent, sky/ambient balance, shadow/cel-band transitions and exposure. Changing a light must change the corresponding surfaces and shadow relationships. A full-screen filter alone fails
3. **Local light:** headlights, tail/brake lights, streetlights, signs and tunnel/garage lighting must remain readable across day/night; avoid day-bright emission, night-black road users, light leakage and glare that obscures hazards
4. **Rain/wetness:** road, paint, metal, concrete, foliage and cloth must respond appropriately. Test roughness/specular/reflection compatibility and drying transitions while keeping opaque stylized surfaces and bounded reflection costs; not every surface becomes a mirror
5. **Outlines and imported assets:** verify ink width/contrast, dark-surface detail, imported material variants and palette adapters under every state. Avoid popping cel thresholds and disappearing outlines
6. **Bounded rendering:** use physically sensible, art-directed responses without committing to real-time GI, volumetrics, heavy transparency or unrestricted shadowed lights. Choose light/shadow/reflection budgets only after measurements. Keep current opaque-rendering constraints; any incompatible technique requires a separate decision
7. **Accessibility and play:** preserve road edges, traffic/pedestrians, wanted/gig cues and UI legibility at night, in rain and facing low sun. Plan reduced glare/bloom and stable exposure options; never make a pretty sunset hide a collision

## Performance question, answered with evidence later

Benchmark the actual target devices and renderer, including Craig's phone where available. Disclose unavailable devices and distinguish desktop simulation from a physical-phone result.

Compare the same route, source commit, camera, viewport/resolution, traffic seed/load, weather/time and quality settings with:
- Clear air without global dust
- Clear air with measured distance, LOD and culling options
- Appropriate atmospheric haze in the weather conditions that actually call for it

Include the old dust baseline when reproducible, without making it the required final look. Separate visibility distance from geometry submission/culling cost; do not assume visual fog alone removes rendering work. Log frame-time median/tail behavior, hitches, CPU/GPU observations where available, draw calls, visible geometry and memory with method and tool limits. Set numerical acceptance budgets from the agreed target-device baseline **before** implementation, not after seeing convenient results.

Show visible distance compromises honestly in matched stills and driving clips. Do not add global dust to disguise incomplete building coverage, missing scenery or unproven optimization assumptions.

## Lore survives clearer air

Gas masks, filters and masked silhouettes can remain grounded in poor air quality or industrial hazards. Dangerous air does not require a permanently opaque visible dust wall. Keep the mystery and recognizable character design without assuming all existing dust-related economy or dialogue must be rebuilt in this lighting milestone.

Upper-city geography is a **separate future design decision and construction scope**, not a prerequisite for the clock/weather slice:

| Undecided option | Value | Cost and questions to test later |
| --- | --- | --- |
| A long mountain ascent to a wealthy enclave | Earns altitude through driving; switchbacks, approach views and route variety; keeps the rich physically separated | Longer travel and streamed/world-scale coverage, road grades, barriers, truck/headroom clearance, traffic/save transitions and gig travel time; adapt elevator-only access and toll/decon lore |
| A megastructure car-elevator cutscene to an expanded inhabited rooftop mini-city/road system | Keeps the mechanical elevator fantasy; bounded transition can hide loading; strong lower/upper social contrast | Rooftop road length and loop quality, believable support/scale, clearance for trucks and buildings, barriers, cutscene/skip/loading/save behavior; avoid a small prop roof pretending to be a city |

Both can preserve Showa infrastructure, wealth/access contrast and a road system worth driving. Neither needs an endless opaque dust sea. After the priority release and explicit authorization, compare a visual mock and route blockout before choosing. Do not build either now, and do not silently bundle a full upper-city rebuild into atmosphere work.

## Future acceptance and evidence contract

These are future gates, not claims of present completion:

1. **Reuse and scope:** a source-pinned audit lists retained/adapted/replaced systems, current owners and the one authority for clock/weather vs district lighting. Confirm no upper-city rebuild is required
2. **Capture matrix:** lock one chase-camera pose at each of three existing route anchors: an open street/intersection, an enclosed/underpass transition, and a landmark/material-rich frontage. Capture all **4 times × 3 weather states** at each pose (36 states). Record source SHA, actual scene/route location, camera transform/FOV, seed, clock, weather transition phase, wetness, quality, device/browser/renderer, resolution and capture time. All states within a comparison set use the same source and camera; label before/after source differences explicitly
3. **Material proof:** include matched neutral/directional/local-light and dry/wet comparisons for every changed material family and imported asset class claimed as supported. Actual in-engine captures must demonstrate surface response; clearly label generated reference art separately. Retain same-instance, same-angle before/after pairs per visual criterion as required by SYSTEM
4. **Driveability:** driving clips and checks cover dawn/dusk sun glare, clear night, rainy night, district boundaries and tunnel/garage entry/exit, with hazards, route cues, lights and English UI readable. Preserve Japanese environmental signage. Cover every affected instance claimed fixed; three anchors do not excuse incomplete defect coverage
5. **Performance:** provide matched-route target-device measurements with agreed numerical budgets, methods and transparent unsupported-device limits. Report actual before/after frame-time/hitch and memory behavior. A lower fog density or a good screenshot is not a benchmark
6. **State correctness:** deterministic clock/weather transition tests; pause/resume, scene reload and save/load round trips preserve time, weather, transition progress and relevant wetness state. Repeated identical inputs produce the agreed identical state; handle invalid/older saves safely. Define authority/synchronization only if the activated mode requires it. Optional photo-mode time/weather controls are not an MVP dependency
7. **Independent acceptance:** a separate strong reviewer inspects source, actual pixels and test results per criterion at the exact final head. Craig's phone visual verdict remains the final visual gate. Never mark the implementation accepted from the author's claim alone

## Recommended future setup

Use the [worker-selection policy](https://github.com/doublehidenblade/game-dev-central/blob/168965ceeade680f6c8729b19a9d52059984b8d4/project-management/rules/WORKER_SELECTION_POLICY.md) and [task-team SYSTEM](https://github.com/doublehidenblade/game-dev-central/blob/168965ceeade680f6c8729b19a9d52059984b8d4/project-management/rules/SYSTEM.md); the full setup contract is in [task.json](task.json).

Request a frontier worker, preferably `gpt-6-astra` at high effort for the initial audit and max for tightly coupled lighting/shader/persistence changes, subject to the actual dispatch catalog. Reserve a separate frontier high/max reviewer. Required Godot renderer, asset/material inspection, reproducible captures, target-device profiling and test access must be verified before production. Availability and runtime identity are **unconfirmed**; this is a recommendation, not an attestation or dispatch.

## Filing verification boundary

Only this brief and its planned task record are created. Existing design history, boards, worker registry, runtime repositories and the separate truck-customization work are unchanged. Implementation evidence is empty by design. The documentation can be reviewed and retained without granting execution.
