# Kurogane Bay design sources — reconciliation draft

Status: **in review, 2026-10-06**. This is the source companion to [web artbook draft PR #2](https://github.com/doublehidenblade/tokyo-drift-3d-web/pull/2), whose original reviewed head was `2761d844d7e630d0a6492db9590bb0df8af1e719`. Canonical branch: `docs/lower-city-systemic-source-reconciliation`; web branch: `docs/lower-city-systemic-economy`. No design recommendation here authorizes game implementation, worker reassignment, merge, deployment or Actions. No supervisor rules, schedules or operational files are changed.

## Source map and authority

| Source | Role in this revision |
|---|---|
| [World bible](gig-city-world-bible.md) | Preserved world canon plus revised §§2/4/7/8/9/10/11/14/15/17: bounded production and jobs, analog navigation, garage progression, reduced mandatory story, staged roadmap and current-worker boundary. |
| [Identity plan](gig-city-retrofutur-identity.md) | Preserved Showa visual vocabulary; replaces unsupported competitor-absence claims, route tracing and blanket cancellation language with sourced positioning and scope limits. |
| [Dust extrapolation](showa-dust-extrapolation.md) | Available visual research, targeted delivery/garage implications, explicit incomplete-import notice. Missing tail is not reconstructed. |
| [Lower City](art-book/lower-city/chapter.md), [World Lore](art-book/world-lore/chapter.md), [Fleet & Gear](art-book/fleet-gear/chapter.md), [Factions](art-book/factions/chapter.md) | Existing canonical chapter sections reconciled with the web draft; newer suited-worker law preserved. |
| [Research/review](art-book/design-review.md) | Shared comparison, primary-source links, recommendations, phase gates, open decisions and source pins; byte-identical to the web draft copy. |
| `art-book/upper-city/`, `art-book/outskirts/`, images, `consult/`, `showa-direction-options.md` | Unchanged source/history. Historical consultation or option text is not a current implementation brief and does not override the revised bible. |

Craig requested the systems-first direction. Counts, prices, tick timing, recipes, risk ordering, recovery policy and staged feature sequencing are **recommendations for review**. Existing Showa canon, Upper City above clouds, masked cast, suited outdoor workers at posts and no-GPS map/sign navigation remain. Current Lower City/Forge/traffic/police workers retain their scope; the older bible's no-pedestrian/no-steering claims are not grounds to delete that work.

## Publication audit — observed, not assumed

Audited central main `3bdf1181b003e38ec9602f0d2ae03e8fb9ea6f01`, against web baseline `2e8c63e3030247fc90e0eea273867181bd5d1098` and initial web draft `2761d844d7e630d0a6492db9590bb0df8af1e719`.

- **112** tracked files under `game-design/`; **11** under `project-management/task-team-system/`. Their combined total is **123**. The GitHub recursive tree was not truncated. This does not establish 123 files under game-design alone.
- All three named upstream documents and all six chapter Markdown files are present. No central artbook `index.html` or renderer was published. The existing `mocks/gig-city/img2img.py` is image-generation history, not an artbook renderer; it was not run or modified.
- Five chapter files were byte-identical to web main before the design draft. Central Lower City had newer Kuro-Kiri law/caption corrections missing from web Markdown, although the served HTML already carried the corrected law. This revision merges those corrections with the new systems sections instead of overwriting them.
- All **47** same-path artbook PNGs have different Git blob hashes between the new central source and web baseline. They are preserved in place. Hash difference alone does not establish which pixels are newer/better or prove corruption. Image acceptance is outside this text reconciliation.
- `showa-dust-extrapolation.md` ends mid-sentence in §5.9 followed by the literal text `...[truncated 12607 chars]`. Original blob: `6ad994c348da6ef2401787bc30471f112cb52f8e`, introduced at `1541bd9ebb07c92b5bc2159f299712b55421ff11`; available history contains no complete alternative. The readable text is revised, but the damaged tail is retained visibly. **A complete original is still needed; no invented restoration is claimed.**
- No AGENTS.md or `.agents/skills` files were present in the published tree. COORDINATOR, current boards/workers/log, standing rules and the newly published task-team-system SYSTEM/WORKER_BRIEF were read. Current user instructions restrict this job to draft design PRs; older merge/QA-publication directions do not expand that scope.
- Game PR #407 (`ccr-7a504622-gmq51e`, `ea3b07575c3244359c6673c817c0c8a0e9bcd9c6`) and Forge PR #416 (`ccr-4570dae0-xgbjgu`, `9fd40751a54d27e5d2efd12939bfba3d98e8e00a`) remained open at this audit. Central PR #299 is the existing Lower City board update, not this task. No branch was taken over and no board row was added/reassigned.

The claimed 1:1 equivalence to Muse's VM-local originals cannot be independently verified from this cloud environment. The counts, file hashes and truncated source above are the observable evidence. Internal memory, credentials and inspector/watch state are not imported into these documents.

## Regeneration / mirror contract

1. Review this canonical draft **together with web PR #2**; neither main branch includes these new design changes yet. Use a recorded central commit/branch, not an unversioned VM cache or the earlier v2 mechanics.
2. Mirror only the four revised `art-book/<chapter>/chapter.md` files and `art-book/design-review.md` as text. They must compare byte-for-byte between this checkout and the paired web draft. Keep source links/version notes; never copy whole directories over divergent images.
3. Refresh the corresponding sections in web `art-book/index.html`, including its research spread, while preserving the existing galleries and the two unchanged chapters. Until an actual renderer is published, this is an explicit document synchronization step, not an assumed automatic pipeline.
4. Check no-GPS navigation, no automatic 3×/5× local arbitrage, scoped story/convoy/combat commitments and suited-worker law in source **and** served HTML. Historical rejected ideas may remain labeled as history in consults; they must not be promoted back into current design.
5. Run the web draft's `art-book/review-evidence/verify.cjs` locally and inspect desktop/phone captures after HTML edits. Review the pinned [initial evidence](https://github.com/doublehidenblade/tokyo-drift-3d-web/blob/2761d844d7e630d0a6492db9590bb0df8af1e719/art-book/review-evidence/README.md) and updated evidence in PR #2. No Actions or live publication is required.
6. Restore the extrapolation's missing tail only from an actual complete original, with provenance and a reviewed diff. Its absence does not justify fabricating source material or dropping preserved lore.

## Validation and handoff

`source-audit.json` records original source hashes, candidate document hashes and preserved shared-asset divergence. Worker checks: `git diff --check`, five mirrored text files byte-identical, all original image/consult/history files unchanged, and no edits outside `game-design/`. These are document integrity checks, not independent design acceptance or gameplay tests. Browser layout evidence lives in the paired web PR rather than duplicating images here.

Next action: review the linked draft pair and decide the open design questions in the research review; obtain the complete extrapolation original before claiming source completeness. Leave existing worker tasks and supervisor configuration untouched. The remaining source-completeness gap is explicitly bounded; the design-document reconciliation itself is reviewable now.
