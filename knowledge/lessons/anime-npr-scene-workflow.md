# Lesson: Anime NPR scene workflow (Craig's directive, 2026-10-04)

Date: 2026-10-04. Source: Craig's own research brief on building anime
scenes in Blender. Saved verbatim first, then digested for our Godot game.

## The source workflow (Blender NPR)

Making a scene read as anime requires combining non-photorealistic
rendering (NPR) shaders, painterly textures, and stylized lighting to mimic
hand-drawn 2D backgrounds.

1. **Reference images first.** Import background art or concept sketches
   into the viewport to guide 3D modeling proportions. Never model the
   anime look from memory.
2. **Block out the environment.** Basic meshes (cubes, planes) for
   structural elements — rooms, hallways, street corners — with Array and
   Bevel modifiers for clean geometry.
3. **Toon shaders.** Diffuse BSDF → Shader to RGB → Color Ramp: break
   smooth gradients into sharp, cartoonish color bands.
4. **Stylized lighting.** Dramatic world lighting (deep blues for night,
   warm oranges for sunset) paired with directional sunlight for a
   cinematic anime mood.
5. **Compositing finish.** Glare, Color Balance, Kuwahara (or Grease
   Pencil line art) for painterly blooms and hand-drawn outlines.

References Craig attached: a full anime-background blockout tutorial, a
Coloso 3D-to-2D asset-coordination course, and a CGDASH stylized line-art
/ hand-shadow tutorial.

## Digest: what this means for Tokyo Drift 3D (Godot, not Blender renders)

The game renders in Godot — Blender is asset-authoring only. Each
Blender-side technique needs a Godot-side equivalent:

- **Toon shading** does not survive GLB export as Blender shader nodes.
  The anime banding must be re-implemented as Godot spatial shaders
  (quantized NdotL into 2–3 bands, banded specular) applied to the
  imported models — or baked into the textures.
- **Painterly textures** DO survive: author them (hand-painted or
  imagegen-guided) and bake to image textures on the GLB.
- **Stylized lighting** happens in the Godot scene: WorldEnvironment sky,
  ambient, and placed lights — deep-blue night ambient with warm amber
  sodium key lights is already the Showa art direction; this makes it
  systematic instead of per-asset.
- **Compositing** maps to Godot's WorldEnvironment: glow (bloom),
  adjustments (color grade), vignette. Kuwahara-style painterly
  post-processing is expensive — evaluate, but never at the cost of
  web/mobile frame rate.
- **Line art** maps to inverted-hull outlines or screen-space line
  detection in Godot — evaluate on hero props only; ship only if it reads
  anime without artifacts.

## Standing rule derived from this

Anime look = reference bible → toon-shader kit → painterly textures →
stylized lighting rig → post-process grade → (optional) line art, in that
dependency order. No asset gets "anime-ified" ad hoc; every step has
in-engine before/after evidence at the same camera.
