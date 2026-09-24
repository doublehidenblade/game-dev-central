# Brief snippet — paste into every coding-agent brief

> **Standing rules (enforced, not advisory):** read
> https://github.com/doublehidenblade/game-dev-central/blob/main/knowledge/standing-rules.md
> before starting, and follow every rule. They outrank workflow convenience, CI
> greenness, and your own judgment calls. The ones that bite most often:
>
> - **R1** — Craig's phone is the final judge. Ship as "for you to check",
>   never "fixed".
> - **R2** — Everything 100% opaque. No transparency tricks, ever.
> - **R3/R4** — Fix bug classes globally with numeric CI assertions that fail
>   on the broken frames. No per-instance patches.
> - **R5/R6** — Nothing closes without before/after evidence + his verdict.
>   Read `todos/QA_INDEX.md` first; take the oldest non-`verified` task.
> - **R8** — QA feedback lives in the repo's `qa/<batch>/` folder. The path in
>   this brief is the source of truth, not chat.
> - **R13** — When you finish: inspected screenshots of what changed, what the
>   PR changed, remaining work/risks, and the play link.
>
> The task transcript is background noise. The standing rules + the task file +
> the evidence are the only sources of truth.
>
> **Shared lessons** (technique teardowns both games build on):
> https://github.com/doublehidenblade/game-dev-central/tree/main/knowledge/lessons
> — read the lesson file named in this brief before designing.
