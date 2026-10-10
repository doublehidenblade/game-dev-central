# Deployment runbook: Tokyo personal playtests and legacy releases

> Updated 2026-10-09. This is the existing deployment runbook, shared by every coordinator, including Muse. The current Tokyo procedure below supersedes the historical Tokyo dispatch instructions retained at the end. It does not change NEON policy, task ownership, source merge acceptance, or grant new access.

## Deployment authorization and Actions budget (Craig, 2026-10-08 19:56 UTC)

**Deploy only when Craig explicitly requests that deployment.** This supersedes earlier standing auto-deploy permission and any historical instruction to publish merely because a build, model or fix is ready. A request to implement, merge, or push ordinary source changes is not a deployment request.

- Treat a deployment-branch or site-repository push/ref update as a deployment whenever it publishes or triggers GitHub Pages, including prebuilt Git-data publication without manual workflow dispatch. Updating live selectors, markers or rollback selection is also publication.
- The GitHub Actions budget is **$50/month**, a spending ceiling, not standing authorization to deploy, run Actions, or incur charges. This is Craig's stated budget, not verified current spend or proof of the configured billing limit. Do not change billing, account access, credentials or security settings.
- Ordinary source pushes and completed merges may continue without a fresh go-ahead, subject to existing ownership, required acceptance checks and independent verification. Inspect the target repository/ref's current push, pull-request and merge-triggered workflows and publication hooks first; do not assume all pushes are inherently free. If the operation would trigger deployment or unauthorized Actions, hold that operation and report the exact trigger instead of bypassing it.
- Keep accepted-but-unpublished work in the existing pending-release ledger. Readiness, a successful merge, restored Actions capacity or unused budget never creates deployment authorization.
- Record Craig's request and its target/scope before publication. Preserve the no-manual-Actions-dispatch/rerun restriction; an explicit deployment request does not itself authorize those actions. Once requested, a personal playtest may ship without waiting for CI/gameplay/visual acceptance, with known failures and unverified behavior disclosed; source-merge acceptance remains separate.
- Shuto remains frozen with no new builds, fixes or deployments. NEON remains paused/read-only. A general Lower City deployment request does not lift either stop.

[JUDGMENT-ONLY: this documentation records owner authorization, scope and budget; the current watchdog does not deterministically verify an authenticated deployment request or live repository trigger configuration. Do not treat this prose update as an implemented automatic authorization gate.]

## Current Lower City focus: existing destinations, prebuilt publication

- Base: https://doublehidenblade.github.io/tokyo-drift-3d-web/ — public repository `doublehidenblade/tokyo-drift-3d-web`, branch `main`
- Shuto: https://doublehidenblade.github.io/tokyo-drift-3d-shuto-web/ — public repository `doublehidenblade/tokyo-drift-3d-shuto-web`, branch `main`
- These remain the existing repository/site names; no repository rename or new hosting target is approved. “Lower City” is a working title, not the final game name. These are the same destinations named by Muse's existing publish workflows. This does not establish which procedure another coordinator is currently executing; coordinate a single publisher before writing.
- Export a pinned source locally with official Godot `4.7.2.stable.official.ed1daf0bf` and matching export templates. Package prebuilt static files into immutable `releases/<release-id>/` directories; the stable root selector chooses the active directory.
- Only after Craig's explicit deployment request, publish Git blobs/tree/commit directly to the authorized active web repository. Do not commit exports to game-source main or rewrite its history. Do not manually dispatch/rerun Actions. GitHub's existing automatic Pages publication follows the web-branch update; this is not a claim of “no Actions at all.” [GitHub documents this distinction](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- Authorized personal playtests need not wait for CI, gameplay, visual or phone acceptance. Disclose known failures and unverified behavior. Publication does not accept implementation or waive the independent source-merge gates. No paid service, credential or access change is included.

### Scope update: Shuto frozen; Lower City separation requested

Craig's 2026-10-08 15:59:48 UTC direction stops all Shuto tasks and focuses development on Lower City. **No new Shuto builds, fixes or deployments.** Preserve its existing playable site at source `841ec6b8dd7ac6150d81d21a0df95f7ea68602f3`, publication `ca485191a6c2f8dd95c385c4ad75c5a85362d5bc`; this is a deliberate frozen baseline, not a stale variant to catch up. Do not delete its site, release folders or rollback.

The requested future experience is a separate direct-launch Lower City build at the existing main/base site, an explicit entry to the preserved old combined game, and one continuous startup-loading experience instead of the current menu loading followed by a second Lower City loading screen. **This separation/loading change is requested, not implemented or deployed.** Keep the old combined game's immutable archives and playable links. Do not remove old game content or rename repositories/hosting under this documentation task.

Going forward, select and verify the active Lower City source independently. Track Shuto's frozen source/publication separately: do not require source/version parity across both sites and do not treat their intentional future divergence as a deployment failure. The paired export/publication instructions below describe the already-shipped October 8 previews; Shuto-specific steps are frozen reference only and are not to be executed while this stop remains in effect.

### Compatibility stop: do not run the legacy Tokyo mirror cleanup

Rechecked on 2026-10-08 after [PR #543](https://github.com/doublehidenblade/tokyo-drift-3d/pull/543) merged as `69a1fc2ede3c260d64628c6df604f33f99a79ecb`: source-main [publish-web.yml](https://github.com/doublehidenblade/tokyo-drift-3d/blob/69a1fc2ede3c260d64628c6df604f33f99a79ecb/.github/workflows/publish-web.yml) now excludes `releases/` from `rsync -ac --delete`, alongside the existing gallery exclusions. That preserves release directories in the base mirror, but **does not clear this compatibility stop**: legacy staging still copies root `index.*` and legacy markers, overwriting the release selector, and does not stage or exclude root `release.json`, leaving it subject to deletion. [publish-web-shuto.yml](https://github.com/doublehidenblade/tokyo-drift-3d/blob/69a1fc2ede3c260d64628c6df604f33f99a79ecb/.github/workflows/publish-web-shuto.yml) still excludes only `.git`, so it can delete release folders and overwrite its selector; Shuto publication remains frozen. `publish-game.yml` chains these legacy workflows and remains unsafe for this layout.

[PR496](https://github.com/doublehidenblade/tokyo-drift-3d/pull/496) proposes preservation/installation logic, but an open PR is not proof that source main has it. **Do not use the historical Tokyo dispatch route or any equivalent `--delete` cleanup until the exact publishing revision is independently verified to preserve all immutable releases, rollback bytes, selectors and unrelated content.** Workflow/code repair is separate work, not part of this documentation update. No Actions permission is inferred from deployment permission. A denied Pages-administration request is not a reason to retry or alter hosting settings.

### 1. Freeze source, release identity and export provenance

Record full source commit, branch, included changes, intended variants and exclusions. Export in a disposable checkout; verify its game-content tree against the selected source, including any omitted development-only files. The source commit is not the web publication commit and need not be game-source main.

Use the `Web` debug preset for the active main/base publication. The direct-launch Lower City preset/scene change is not implemented by this runbook. **Frozen reference only:** for the prior Shuto publication, use a separate disposable copy, set only the established export-time `application/run/main_scene` override to `res://scenes/shuto_c1/shuto_c1.tscn`, then export `Web Shuto`. Record the override and restore/discard the copy; do not silently change source. Typical local commands, with absolute paths supplied by the publisher (the current cloud-environment caveats below must be checked before reusing the headless examples):

```sh
"$GODOT" --version
"$GODOT" --headless --path "$SOURCE/godot" --editor --import
"$GODOT" --headless --path "$SOURCE/godot" --export-debug Web "$EXPORT_BASE/index.html"
# FROZEN REFERENCE ONLY: do not run new Shuto exports while the stop is active.
# Historical separate Shuto copy, after the documented main-scene override/import:
"$GODOT" --headless --path "$SHUTO_SOURCE/godot" --export-debug 'Web Shuto' "$EXPORT_SHUTO/index.html"
```

Keep exit codes/logs and hash inventory. Require complete `index.html`, `index.js`, `index.wasm`, `index.pck` and matching `build-sha.txt`; audit resource inclusion. Re-exported packs may differ in generated bytes, so source equivalence alone is not a binary-integrity claim.

### Local Godot and cloud-browser readiness findings (2026-10-09)

[JUDGMENT-ONLY: these are bounded observations from the coordinator's cloud environment, not a deterministic watchdog gate, a standing test authorization, or a root-cause diagnosis. Existing ownership, independent acceptance, explicit deployment authorization and frozen-work boundaries above are unchanged.]

#### Pin the toolchain and separate the execution paths

Use an explicitly resolved executable, not an unverified `godot` from PATH. The inspected PATH installation was 4.6.3; these observations used official `Godot_v4.7.2-stable_linux.x86_64`, reporting `4.7.2.stable.official.ed1daf0bf`.

- Engine SHA256: `8d106cbe6144c2dc7e881d61d2429c1a8a76e6b22ef48bd5e48dcf934953f71e`
- Matching `4.7.2.stable/web_nothreads_debug.zip` SHA256: `08962aefef811b603541d7951ac67ef00413aad2d978855183c28adee98f626a`
- Template `godot.wasm` SHA256: `11ea19645368f8e73cf337b59cfd7ceeb4ebb51f7a3bbf77d1a5c3ddfedbc522` (37,902,138 bytes)

Set HOME and XDG_DATA_HOME/XDG_CONFIG_HOME/XDG_CACHE_HOME explicitly to writable, task-isolated directories. Changing HOME alone does not override inherited XDG paths. For export, use the matching template directory or an explicit verified template path; a successful native runtime does not test exporter/template availability.

1. **Native direct runtime works for the observed renderer.** At 05:38 UTC, the pinned executable ran the unchanged v49 MapSheet renderer, city data and retained imported font through the supported cloud desktop Terminal, with inherited DISPLAY=:0 and `--rendering-method gl_compatibility`. It rendered real pixels and exited 0 after the fixture's five-second observation interval. The log identifies X11, Mesa llvmpipe and OpenGL 4.5. The source is [the composed v49 commit](https://github.com/doublehidenblade/tokyo-drift-3d/commit/fa081b42197d50e6adaf202f899146fbffeab725), MapSheet blob `dfbbdda84a74de77122368a3cf52d236837879f3`. This path used retained imports and did not initialize the editor; it proves neither browser CSS/DPR behavior nor full-scene acceptance.
2. **The tiny headless-import stall is observed, not explained.** Initial attempts reported unwritable default data/config paths. Writable HOME/XDG retries still timed out; the latest verbose log ended after `EditorTheme: Generating new styles`, with exit 124 and no completed filesystem scan. The earlier attempt launched through the desktop Terminal also passed `--headless`; calling it a graphical-editor failure would be inaccurate. The last log line is not proof of a font/theme defect. Earlier retained imports and Web exports with the same pinned engine had succeeded, so do not generalize this to a universally broken executable/exporter.
3. **One graphical tiny export completed, with qualifications.** At 06:54:12–06:54:19 UTC, a fresh isolated copy of the four-file diagnostic fixture ran one direct `--export-debug Web` through the supported Terminal, with `--rendering-method gl_compatibility`, the explicit no-threads template, inherited DISPLAY and no `--headless` or separate `--import`. It passed the earlier last-seen theme phase, completed packing and exited 0 in 7.714 seconds. Nonempty HTML/JS/WASM/PCK were produced; WASM exactly matched the template hash above. This establishes this tiny graphical export path, not the cause of the headless stall.
   - The strict unchanged-source gate **failed**: Godot automatically rewrote only isolated `project.godot`, adding `config/features=PackedStringArray("4.7")` and normalizing formatting. The other three inputs and all original fixture files remained byte-identical. Preserve and report such diffs; do not restore them before capturing evidence or call the run byte-identical.
   - The intended 1 GiB RSS guard was **not verified**: the monitor saw only the timeout wrapper, not the engine process. Its 897,024-byte sample is invalid engine-memory evidence. The 45-second TERM/2-second kill-after timeout was configured, but natural completion did not exercise it. Observed isolated-file output stayed below 64 MiB. This was not a fully validated bounded-probe pass.
   - Retain the nonfatal audio fallback, VSync/cursor, desktop-portal, Vulkan-probe, missing minimal-preset filter-key and shutdown StringName messages. Exit 0 is not an error-free log.
4. **The actual tiny browser load stopped before engine startup.** At 06:58 UTC, one supported cloud Chromium load of that existing export showed the exact Godot feature-check error: `WebGL2 - Check web browser configuration and hardware support`. DOM, console and inspected screenshot pixels agreed: Godot splash/error overlay, not the fixture label/rectangle/button. HTTP logs showed HTML/JS/splash requests and no WASM or PCK request. The canvas remained 300×150 backing/CSS pixels at DPR 1. The test tab and its own localhost-only server were closed after 35.009 seconds, within the 60-second observation bound. No reload, engine launch or build occurred. This identifies the current browser feature-check blocker; it does not explain the earlier full-artifact browser Error 9, establish an OOM cause, or support game/input/full-scene/phone acceptance.

Public-safe evidence identities: native rendered capture SHA256 `28fd1d0f0e960560ec20869fcd5c1fc4b02467b06e25590890dfa1a00745bd58`; tiny PCK SHA256 `d027ed960dfe617122f2b80f80f834dd5e5045182182f953ed2d8e0215486da5` (3,016 bytes); browser failure JPEG SHA256 `a2195839d8a300eb0ff461ddab5d355768a73755983c0b451034a3ccb1e79de4` (1180×757). Full diagnostic logs, source manifests/diff and original captures are retained with the coordinator; they are not published evidence links or independent acceptance. Do not publish private session URLs, account data or unredacted desktop captures.

#### Before any future scoped local test

- Check the current task owner and concurrent engine/browser workers first. Serialize expensive probes against active tests/benchmarks where they would contend, keep isolated paths, and stop only processes/servers/tabs created by that test. Do not disturb another worker's files or reservations.
- Confirm the actual engine child/process tree is visible to the monitor before treating an RSS limit as enforced; a wrapper PID or isolated shell process listing is insufficient. If monitoring is unavailable, stop before the memory-bounded test and report the missing capability. Record exact commands, toolchain/input/output hashes, source changes, error logs, timing, limits and cleanup.
- Use the supported cloud Terminal/native-app route and documented CUA browser APIs. The observed local HTTP route served only the fixture directory, bound to 127.0.0.1, with COOP same-origin, COEP require-corp and no-store headers. Ordinary HTML serving success is not proof of WebGL2 support.
- The graphical-export and tiny-browser one-shot attempts are consumed. Never remove, reset, reuse or invoke their attempt markers/runners to obtain another launch. Do not blindly repeat the same headless import or heavy full-game browser load; any separately scoped test needs a current evidence-based purpose, applicable authorization and explicit success/failure stop conditions.
- Respect the earlier denied PTRACE tracing and shell Chromium/socket/sandbox routes. Do not retry them, swap tools/routes to evade a denial, alter browser security flags, or change authentication, certificates, provider restrictions or security settings as a workaround. If the supported route is blocked, preserve the exact blocker and stop the dependent test.
- A local renderer/export recovery does not authorize publication, Actions, worker contact, source merging or expansion into frozen Shuto/paused NEON work. Keep native render, editor/import, export integrity, browser startup, full-scene behavior and physical-phone acceptance as separate reported stages.

### 2. Reproduce the actual 8 MiB transport

The deployed transport is **not the unmodified PR496 packager**. At pinned source revision [`c3f521af86938ca30444ae746a5bd684279e61e4`](https://github.com/doublehidenblade/tokyo-drift-3d/tree/c3f521af86938ca30444ae746a5bd684279e61e4/deploy/chunked), `deploy/chunked/package.mjs` and `loader.js` use 32 MiB. The published preview used precisely these two local packaging changes:

```diff
- export const CHUNK_BYTES=32*1024*1024;
+ export const CHUNK_BYTES=8*1024*1024;
-   const CHUNK = 32 * 1024 * 1024;
+   const CHUNK = 8 * 1024 * 1024;
```

Portable reproduction: obtain those two files from the pinned revision into a separate `tools/` directory, apply only the matching constant changes, then verify SHA256:

- `package.mjs`: `c6535d3c6cd00c73a822ed3edc59d4697912c8328a330a7e4816925097f9f96c`
- `loader.js`: `a5bcd74193188f34ee975d60b4159ee4de22e2774fbc20823232d2d7839add7e`

This exact transformation was checked against the tools used for both October 8 previews. The 8,388,608-byte chunks fit the working upload route; this is an operational chunk size, not a stated GitHub API limit. Keep a separate packaging-provenance record containing these hashes, chunk bytes, original tool revision, source SHA, engine/template version, export settings and artifact hashes. Do not label the runtime source hash as full packaging provenance.

In a local staging site, preserve the existing release tree and rollback release. For a first migration only, `archive-legacy --input LEGACY_EXPORT --site SITE --version v46` preserves the actual old client bytes and records historical manifest discrepancies; do not synthesize or overwrite an archive. Then use the reproduced tools:

```sh
node tools/package.mjs pack --input "$EXPORT" --site "$SITE" --version "$RELEASE_ID" --source "$SOURCE_SHA"
node tools/package.mjs activate --site "$SITE" --version "$RELEASE_ID"
node tools/package.mjs verify --site "$SITE"
```

The packager rejects an existing release directory, verifies every listed size/hash and reassembled PCK, pins the manifest and loader, and creates the canonical root selector. Run applicable packaging checks against the actual 8 MiB tools; old 32 MiB test results do not automatically cover the adaptation. Local packaging verification is not browser/gameplay acceptance.

### 3. Publish without losing other releases or another writer's work

1. Verify the recorded explicit Craig deployment request covers this target and release; inspect the current publication triggers. Then read the exact current active main/base web `main` commit and complete tree. Shuto publication is stopped; do not write its branch. For any separately authorized future variant publication, read its own tree independently. Save the expected old head. Coordinate a single publisher; base and Shuto updates are not one atomic transaction.
2. Build the new tree from that existing tree. Add the new immutable release and replace only the selected root files (`index.html`, `release.json`, `deployment.json`, `build-sha.txt`, `version.txt`, `.nojekyll`) plus explicitly scoped release notes. Preserve every other existing entry, including all previous releases, rollback, `art-book/`, `qa/`, `research/`, README and unrelated galleries.
3. Hash local bytes. Reuse same-repository Git blob IDs for byte-identical files, including unchanged engine `index.js`/`index.wasm`; upload only missing blobs using the supported base64 blob route, with PCK files at most 8 MiB. Never assume an engine blob matches merely because the engine version string matches.
4. Create the tree using the old tree as the base, verify all preserved/new paths and blob IDs, and total the complete proposed site's file bytes. Create a commit whose parent is the expected old head. Re-read the ref and update it with an **expected-old-head lease**, normally `force: false`; stop/rebase the proposed publication on a changed head. A read followed by an unconditional forced update is not a lease. A tool without an atomic expectation must use an equivalent compare-and-swap/explicit git force-with-lease or fail safely; never discard concurrent work. Force is permitted for an authorized deployment when necessary, not required for an ordinary fast-forward. It never authorizes source-history rewriting.
5. Read back web `main` and confirm the exact publication commit. Existing Pages publication may start automatically; observe it read-only, never manually dispatch/rerun. Do not change Pages settings or retry a denied metadata route.

### 4. Verify serving, report accurately, retain rollback

Check HTTP status and exact bytes for root selector/markers, selected shell and manifests, and verify the selector's executable target (a comment containing the expected URL is insufficient). Check selected source/version agreement and retained rollback. Full chunk/engine HTTP readback and real browser loading are additional distinct checks: record which were actually completed, cancelled, blocked or not run. A green Pages run or a new version badge alone proves neither correct payload nor gameplay.

Report the human version first, stable play links, source/build provenance, included changes, known failures and exact verification scope. Do not describe unshipped camera/map or other changes as included. Update the existing release ledger only after the corresponding live scope is established; preserve pending entries and historical normal-release fields. Reconcile with the existing [first-preview release-record PR356](https://github.com/doublehidenblade/game-dev-central/pull/356), rather than duplicating/overwriting its work.

Rollback selects a previously verified immutable directory by regenerating only the root selector/markers and publishing another leased web commit. Verify the result; do not overwrite release bytes, delete newer releases or reset unrelated gallery history.

### Verified publication snapshot (2026-10-08, not a gameplay verdict)

- Runtime source: `841ec6b8dd7ac6150d81d21a0df95f7ea68602f3`, branch `preview/quality-traffic-20261008`; includes graphics PR532 at `a7c9c216aab3b929800911de6e1e721f798021a1` and traffic PR531 at `a1e12db80f9a68724a0f310da50ae5c3b24a9fb1`. Camera/map updates are not included.
- Base publication: [`bac35b433dfbdb4433e374ac1f5d1583ae7b6d5b`](https://github.com/doublehidenblade/tokyo-drift-3d-web/commit/bac35b433dfbdb4433e374ac1f5d1583ae7b6d5b), `Web` debug export. [Immutable base link](https://doublehidenblade.github.io/tokyo-drift-3d-web/releases/playtest-20261008-841ec6b/index.html).
- Shuto publication: [`ca485191a6c2f8dd95c385c4ad75c5a85362d5bc`](https://github.com/doublehidenblade/tokyo-drift-3d-shuto-web/commit/ca485191a6c2f8dd95c385c4ad75c5a85362d5bc), `Web Shuto` debug export with the main-scene override above. [Immutable Shuto link](https://doublehidenblade.github.io/tokyo-drift-3d-shuto-web/releases/playtest-20261008-841ec6b/index.html).
- Both serve the selected source with exact selector/shell/metadata checks. Complete HTTP pack readback remains unverified; cancelled verification was not retried. No gameplay, rendered visual, FPS or physical-phone acceptance is implied. The stable roots above select the latest publication; these immutable URLs continue selecting this specific preview.
- Previous preview source `1a5d967ca81d285aecf07be830811aff4fbef48f` remains under `releases/playtest-20261008-1a5d967/`; its first-publication commits were base `271ede178f1aa4d072cf988c1d2ba43d18911efd` and Shuto `991decf0f94c7bc4e5619d637f4ffba157da2641`. Retain the actual v46 rollback too.

### Human version numbers, storage and pipeline compatibility

Use `v<N>` as the user-facing version; retain full source SHA and immutable directory ID as secondary provenance. Before assigning a number, inspect source `build-number.txt`, both live root `version.txt` files, existing release directories, release ledger and any in-flight publisher reservations. Reserve a mapping for the active Lower City release with the publisher; never infer a number from source main alone. Historical paired releases may share a mapping, but frozen Shuto must not be rebuilt or relabeled to match subsequent Lower City versions.

As of the 2026-10-08 inspection, source main still has counter `46` and `v46 4ecd2089c1b292c11c70b7e9701f77df39cca044`; both current web markers instead name `playtest-20261008-841ec6b`. A proposed retrospective mapping is `v47` for `playtest-20261008-1a5d967` and `v48` for `playtest-20261008-841ec6b`. **This runbook does not reserve those numbers or claim they are live.** Confirm no reservations before applying it.

For future active Lower City releases, allocate `v<N>` before packaging so directory, manifests, badge and root markers agree. For already-published releases, keep their immutable bytes/URLs; record a human label mapping without cloning the binary payload merely to rename it. The current schema ties release IDs across manifests, selector, badge and verifier: changing just `version.txt` creates inconsistency. Any alias/display-label implementation requires explicit compatibility verification. Before any later legacy workflow is allowed again, reconcile its source counter and teach its staging/preservation logic about the new layout; otherwise it could allocate a duplicate `v47` and erase releases.

Chunking changes delivery and per-file size, not asset size: the browser still reconstructs the full PCK. Git blob reuse avoids uploading identical objects again but does not prove a smaller client download or smaller published tree when identical bytes exist at multiple paths. No total cost saving, free-account guarantee, faster startup or lower memory use is established by this route.

[Current GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) specify a 1 GB published-site maximum and a soft 100 GB/month bandwidth limit (checked 2026-10-08). The packager conservatively caps total site bytes at 1,000,000,000; include galleries and every retained release. The two current publication trees measured 731,027,978 bytes (base) and 551,813,973 bytes (Shuto), before any new aliases/releases. Recompute on every proposed tree. Base is already large enough that duplicate full releases consume meaningful headroom. Retention/deletion is a separate explicit decision: no cleanup or old-version deletion is authorized by this runbook. If capacity is insufficient, stop the dependent publication and seek an approved retention/hosting plan.

---

## Historical procedure (reference only; Tokyo dispatch unsafe, Shuto work frozen above)

# Push-on-request procedure (Craig 2026-09-27; force rule 2026-10-02)

**Rule: nothing goes live until Craig explicitly asks to push.** Merges to main
keep flowing (workers + watchdog SHIP), but the publish workflows
(publish-web, publish-game, publish-web-shuto, deploy-signaling in
tokyo-drift-3d; publish-web in neon-drift) are `workflow_dispatch`-only and
are NEVER dispatched except on Craig's explicit push request.

**Rule (Craig 2026-10-02): every authorized deploy uses `force: true`.**
Smoke/test results NEVER gate publication — smoke runs after the fact, and
failures become post-publication follow-up work, not publish blockers. The
reviewed-candidate pointer, source-SHA check, same-repository check, artifact
provenance, and rollback guards remain mandatory; only the smoke-success gate
is bypassed by force. **Superseded 2026-10-08 19:56 UTC:** readiness never authorizes deployment; wait for Craig's explicit deployment request under the current policy above.

Ledger files (this dir):
- `baselines.json` — last live web SHAs per game (updated ONLY after a push
  is verified live).
- `pending.json` — merged-but-not-live entries the watchdog SHIP step appends
  (schema: {pending: [{game, task, pr, merged_sha, merged_at, summary}]}).

## When Craig asks for a TOKYO push

1. Export/publish ALL pending Tokyo client changes: dispatch `publish-game.yml`
   (workflow_dispatch on main) via the github skill with force ALWAYS on:
   `bin/gh api POST /repos/doublehidenblade/tokyo-drift-3d/actions/workflows/publish-game.yml/dispatches '{"ref":"main","inputs":{"run_id":"<smoke-run-id>","force":true}}'`
   (needs `actions: write`). It exports the reviewed candidate build, commits it
   to the source repo root, and auto-dispatches `publish-web.yml`, which mirrors
   it to the public `-web` repo (GitHub Pages). Do NOT dispatch `publish-web.yml`
   alone: it only mirrors the repo root's already-committed export and no-ops
   when nothing was rebuilt (observed 2026-09-27).
   The `force: true` input is MANDATORY on every dispatch (Craig 2026-10-02) —
   never dispatch with force false or omitted. The guard then skips ONLY the
   smoke-success requirement (publish-then-fix); the reviewed-candidate pointer,
   same-repo check, and rollback guard stay on, and any smoke failure becomes a
   follow-up task.
2. Signaling: if any pending change touched the multiplayer protocol/server
   (td-079 did — server blocks START until all ready), dispatch
   `deploy-signaling.yml` in the same release, BEFORE client verification.
3. Verify parity: source main SHA → exported build → `-web` repo main SHA →
   live site build marker. All four must agree the publish went through.
4. Run a REAL two-client test: create room → join → both ready → host starts.
   Confirm the guest enters the race with the host (this is td-079's defect).
5. Tell Craig exactly what changed since the recorded baseline
   (`baselines.json` → tokyo.web_sha), LEADING WITH THE VERSION
   (publish-game.yml stamps an incrementing v<N> into every export; the
   game UI shows it in a corner badge, and the badge self-reports staleness
   by polling the live version.txt). Report format: "v23 live: ..." then
   the terse change list, with the game link
   https://doublehidenblade.github.io/tokyo-drift-3d-web/ and inspected
   screenshots where applicable.
6. Update `baselines.json` tokyo to the new live SHAs and remove the
   published entries from `pending.json`.

## When Craig asks for a NEON push

1. Build and publish ALL pending NEON changes: dispatch `publish-web.yml`
   on neon-drift main.
2. Verify source/build/public-web/live parity (same four-way check as Tokyo).
3. Android-verify relevant phone-visible fixes — p3d-084 (gantry signs) gets
   an independent phone-visible check; Craig's phone verdict is final.
4. Tell Craig exactly what changed since `baselines.json` → neon.web_sha,
   with https://doublehidenblade.github.io/neon-drift-web/ and inspected
   screenshots where applicable.
5. Update `baselines.json` neon and clear the published entries from
   `pending.json`.

## Never

- Dispatch a publish workflow because "Actions capacity is back" or because a
  merge just landed — only on Craig's explicit push request.
- Dispatch publish-game.yml with `force: false` or without the force input —
  every authorized deploy uses `force: true` (Craig 2026-10-02).
- Tell Craig to retest a fix until the updated client is confirmed live.
- Describe a merged-but-unpublished fix as live on his phone.

## Lesson: 100MB push limit (2026-10-02)

GitHub rejects pushes containing any file over 100MB. The web export's
`index.pck` counts: on 2026-10-02 the traffic-fleet's 2048x2048 car textures
bloated the .pck to ~168MB, and publish-game.yml failed at the `git push`
step (exit 1, "exceeds GitHub's file size limit"). Fix was to optimize the
source assets (resized embedded textures to 512x512, 70MB → 15MB), not to
work around the limit. Keep the export .pck comfortably under 100MB; if a
new asset pushes it over, optimize the asset before publishing.
