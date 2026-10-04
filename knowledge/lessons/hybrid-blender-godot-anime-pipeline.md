# Lesson: Hybrid Blender-to-Godot retro anime pipeline (Craig's directive, 2026-10-04)

Date: 2026-10-04. Source: Gemini's "Hybrid Blender-to-Godot Retro Anime
Pipeline" skill, commissioned by Craig after he confirmed the key
architectural question: **Option 2 — Runtime in Godot** — is correct.
Frozen/baked lighting would break the illusion of speed at night in a
racing game; dynamic lights must react to moving vehicles in real time.

## The decision this resolves

Blender = asset authoring. Godot = runtime. The export boundary (.glb)
dictates every technique's home:
- SURVIVES export: geometry, UVs, baked flat albedo textures, Material
  ID slots, Solidify outlines applied as real geometry.
- DIES at export: Eevee shader nodes (Shader to RGB), compositor
  (glare/grain/chromatic aberration), world lighting.

## Part 1 — Blender phase (per the skill)

- Tripo cleanup: Decimate 0.3–0.5 (jagged tris flutter in real-time
  cel-shaders), Weighted Normals on mechanical models, separate moving
  components with programmatic names (Chassis_Mesh, Wheel_FrontL…).
- No PBR nodes. Bake flat hand-painted albedo only. Assign Material ID
  slots (Mat_Neon_Pink, Mat_Car_Body, Mat_Windows) — Godot consumes
  these, never Blender materials.
- Optional: Solidify outline (Thickness −0.02 m, Flip Normals, High
  Quality) applied at GLTF export so outlines are real geometry.

## Part 2 — Godot phase (per the skill)

- Import hook (`_post_process_import`): walk MeshInstance3D nodes,
  assign `retro_toon_shader` by material-slot/name match.
- Cel shader (GLSL): `render_mode diffuse_toon, specular_toon`; flat
  albedo from baked texture; shadow tinted late-80s indigo
  (vec3(0.05, 0.05, 0.15)); hard step band at 0.5.
- Lighting: DirectionalLight3D moon + Omni/Spot street lamps; shadow
  blur 0.0 everywhere for razor-sharp toon lines.
- Screen filter: ColorRect over the viewport — chromatic aberration
  (0.002 at edges) + floating film grain.
- Full VHS/film GLSL stack and a streetlight fade/move GDScript were
  offered as follow-ups — claimed by td-162 and td-158 respectively.

## Digest — conflicts resolved

- Palette: the skill's cyberpunk-OVA framing (pastel pinks, dense neon
  billboard "Glimmer Grid") CONFLICTS with the standing Showa art
  direction (deep-blue night, amber sodium glow, restrained signage —
  Craig 2026-09-29: "Not this neon color sht"). Resolution: adopt the
  PIPELINE, keep the SHOWA PALETTE. The skill's indigo shadow tint is
  already Showa-compatible; neon density stays restrained.
- Framerate: the skill suggests 960x720 and optional 24 FPS. Our ship
  target is the web build on phones — perf is measured, never assumed;
  no frame-rate cap without Craig's call.
- Task split: td-160 (Blender prep pipeline) → td-161 (Godot import
  hook, needs td-160's slot convention + td-156's shader) → td-162
  (screen filter, needs td-159's grade). td-158 absorbs the
  streetlight-fade script.
