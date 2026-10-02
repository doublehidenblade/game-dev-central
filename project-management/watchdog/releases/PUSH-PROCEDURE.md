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
is bypassed by force. If the UI/car models (or any reviewed content) are ready,
deploy without waiting for Craig to say the word — publication is Muse's job.

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
