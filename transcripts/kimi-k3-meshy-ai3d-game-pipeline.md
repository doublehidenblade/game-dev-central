# Kimi K3 + Meshy: AI 3D 游戏素材制作并应用到游戏中

- **Source:** RedNote video by 神秘的鱼仔, 2:31 — http://xhslink.com/o/siLEYoEjK8 (note 6ac74caf000000001203b2b0), transcribed 2026-10-08 via `scripts/xhs_transcript.py` (no-login subtitle pull)
- **Title (original):** 都在用GPT6在做3D建模？AI3D项目到底怎么做

## Digest

- **Core thesis: AI 3D project = general large model + specialized AI 3D tool.** The video argues against driving Blender via computer-use (burns through Plus/Pro quota fast) or via Blender MCP (reads the scene but can't faithfully reproduce your own reference images). The better split: the LLM directs and integrates, the specialized tool generates.
- **Demo pipeline (Kimi K3 + Meshy):** prompt → Meshy image generation (with prompt-optimization toggle) → image-to-3D. Two modes: agent form (prompt only, end-to-end) or manual step-by-step. High-detail mode claims up to 4K 3D generation with texture + image enhancement; white-model (untextured) preview, environment-lighting preview, wireframe/normal-map inspection.
- **The poly-count problem, quantified:** a high-detail mech came out at ~1.8M faces — unusable in a game. Two fixes: retopologize the generated model (set polygon count + topology type) or use smart-topology at the image→model step. Result: ~1.8M → ~10k faces, directly game-usable. This is a concrete acceptance reference for mobile/Godot asset budgets.
- **Animation:** Meshy's smart rigging / auto-rigging handled even an odd-shaped mech; the rigged model walks in-engine. Meshy's docs (meshy.ai) confirm auto-rigging + 600+ game-ready animation presets, native Godot/Unity/Unreal/Blender plugins, and a REST API + MCP server.
- **Godot handoff:** DCC bridge / native plugin sends the model straight into Godot. Final integration step is described as "one prompt to the LLM": tell it which models you have, replace the placeholder boxy characters. (Oversimplified — integration, scale, materials, and collision still need real work; matches our reuse-first rule.)
- **Same pipeline claimed reusable** for 3D websites, 3D animation, 3D printing.

## Why it's recorded

- Validates our existing division of labor (Gemini imagegen + Tripo for generation; LLM sessions for direction/integration) against the computer-use-Blender alternative.
- **Meshy is a credible Tripo alternative** for the asset-generation leg: broader pipeline (text-to-3D + image-to-3D + PBR texturing + Smart Remesh + auto-rigging + Godot plugin + API/MCP). Third-party comparison (wavespeed.ai, Oct 2026) positions Meshy as "best for broad text-to-3D workflow" vs Tripo as "best for fast image-to-3D prototyping." Worth evaluating if Tripo's topology/rigging output ever blocks us. Note: Meshy licensing varies by plan; free-tier outputs need a license check before shipping in a commercial game (same caution as Tripo free-plan CC BY 4.0).
- The 1.8M → 10k retopo datapoint is a useful stick for asset acceptance: any AI-generated model arriving at game integration must state its face count and retopo path.

## Caveats

- Creator claims (4K generation quality, "AI recognizes bones", one-prompt integration) are unverified marketing-adjacent statements from a small creator (57 likes). Treat as leads, not facts.
- Auto-rigging per Meshy's own docs focuses on humanoids and quadrupeds, not arbitrary mechanical joints — verify before depending on it for vehicles/mechs.
- Subtitles are machine-generated; names below are normalized (MeShy/Metro/mystery → Meshy, bland → Blender, kimik三 → Kimi K3).

## Full transcript (Chinese, machine subtitles, lightly cleaned)

最近我刷到了很多用 GPT-6 Astra 以及 Opus 5.5 操控 Blender 去做 3D 建模的视频。如果是用 computer use 操控电脑的方法，Plus 和 Pro 五倍的额度会在很短时间内被打满；如果用 Blender 的 MCP 工具，它会直接读取 Blender 里的场景和物体，但这样就无法准确复刻你自己的图片。目前用 AI 做 3D 项目，更合适的方式还是使用通用大模型加专门的 AI 3D 工具。本期视频我们就用 Kimi K3 加 Meshy，来实现一个 AI 3D 游戏的素材制作，并且应用到游戏中。

要做出一个出色的 3D 模型，比较好用的方式是先通过提示词生成图片，再通过图片生成 3D 模型。Meshy 同时提供了图像生成和 3D 建模生成的大模型。有两种方式：一是直接使用 Agent 的形式，只需要写下提示词，Agent 会自己完成从图片到建模的创建全过程；二是通过图像模型按手动一步步执行。本期视频用第二种方式演示。

先在图像这里生成一些图片出来。比如我这次想要生成硬核工业风格的产物，可以用简单的提示词直接描述想要的内容，然后开启提示词优化；如果提示词本身已经很详细了，就不需要再额外开启。在风格上选择写实主义深沉，这样一个机甲就出来了。

有了图片之后就是模型的生成。先生成一个高精度的模型看看效果。在高细节模式下上传刚刚生成的图片，Meshy 现在支持超精细 4K 的 3D 模型生成，在分辨率这里选上超清晰 4K，这里额外选上贴图和图像增强直接生成。先看看白膜的细节效果：3D 模型的整体还原度很高，拉近后的几何细节展示都很合理，单张照片中没有出现过的几个面，模型的生成效果都很不错。接下来看看上了贴图之后的版本，可以调整不同的环境光查看不同光线下的模型效果，也可以开启线框、法线模式。

高细节模式的 3D 模型虽然很精致，但是面数和顶点数都太大了，不太适合直接用于游戏。现在有两种方式：第一种是直接基于生成的模型进行重拓扑，可以设置多边形的数量以及拓扑形式，我们直接来生成这个机甲的重拓扑版本；或者是在图片生成模型的这一步就使用智能拓扑功能，生成的效果是一样的。来看一下智能拓扑之后的模型效果：面数直接从精细版的 180 万降到了一万出头，这样就可以直接用到游戏中了。

可以通过 DCC 桥直接将模型发到对应的软件，比如我用 Godot 做了一个 3D 游戏的基础版本，装好对应的插件，直接把 3D 模型发给 Godot。这种静态的模型是不会走动的，那就可以使用动画中的智能绑骨功能，哪怕是这种比较异形的机甲，也能实现智能绑骨，这样应用到游戏中时 AI 就能识别到骨骼，实现走动的效果。

我同时又生成了其他的几个怪物、NPC 的模型以及主角的模型，接下来把这几个模型都应用到游戏中。3D 模型应用到游戏的过程其实就是一句提示词的事情：告诉大模型你有哪些模型，然后替换游戏中原本的方块人，这样你就能得到一个模型都是自己定义的 3D 游戏了。通过这种方式，不仅能结合通用大语言模型做 3D 游戏、3D 网站项目，还能去做 3D 动画、3D 打印。AI 3D 建模工具已经比以前强太多了。
