# Push-on-request procedure (Craig 2026-09-27)

**Rule: nothing goes live until Craig explicitly asks to push.** Merges to main
keep flowing (workers + watchdog SHIP), but the publish workflows
(publish-web, publish-game, publish-web-shuto, deploy-signaling in
tokyo-drift-3d; publish-web in neon-drift) are `workflow_dispatch`-only and
are NEVER dispatched except on Craig's explicit push request. CI/smoke must
not gate his requested push — publish then fix.

Ledger files (this dir):
- `baselines.json` — last live web SHAs per game (updated ONLY after a push
  is verified live).
- `pending.json` — merged-but-not-live entries the watchdog SHIP step appends
  (schema: {pending: [{game, task, pr, merged_sha, merged_at, summary}]}).

## When Craig asks for a TOKYO push

1. Export/publish ALL pending Tokyo client changes: dispatch `publish-game.yml`
   (workflow_dispatch on main) via the github skill:
   `bin/gh api POST /repos/doublehidenblade/tokyo-drift-3d/actions/workflows/publish-game.yml/dispatches '{"ref":"main"}'`
   (needs `actions: write`). It exports the reviewed candidate build, commits it
   to the source repo root, and auto-dispatches `publish-web.yml`, which mirrors
   it to the public `-web` repo (GitHub Pages). Do NOT dispatch `publish-web.yml`
   alone: it only mirrors the repo root's already-committed export and no-ops
   when nothing was rebuilt (observed 2026-09-27).
   Force button: if the candidate smoke run is red and Craig wants the build live
   for playtest anyway, dispatch with inputs `'{"ref":"main","inputs":{"force":true}}'`.
   The guard then skips ONLY the smoke-success requirement (publish-then-fix);
   the reviewed-candidate pointer, same-repo check, and rollback guard stay on,
   and the smoke failure becomes a follow-up task. Only Craig authorizes force.
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
- Tell Craig to retest a fix until the updated client is confirmed live.
- Describe a merged-but-unpublished fix as live on his phone.
