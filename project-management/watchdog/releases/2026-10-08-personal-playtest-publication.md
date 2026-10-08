# Tokyo Drift personal playtest publication — 2026-10-08

## Scope and status

`playtest-20261008-1a5d967` is published to the existing personal playtest sites, for Craig to check. This record documents publication and its bounded readback evidence. It does not establish a source-main merge, full gameplay or visual QA, independent source acceptance, or Craig's phone verdict. Existing task status, worker ownership, historical accepted baselines, and pending release entries are unchanged.

## Pinned release

- Runtime source: [`1a5d967ca81d285aecf07be830811aff4fbef48f`](https://github.com/doublehidenblade/tokyo-drift-3d/commit/1a5d967ca81d285aecf07be830811aff4fbef48f)
- Base web commit: [`271ede178f1aa4d072cf988c1d2ba43d18911efd`](https://github.com/doublehidenblade/tokyo-drift-3d-web/commit/271ede178f1aa4d072cf988c1d2ba43d18911efd)
- Shuto web commit: [`991decf0f94c7bc4e5619d637f4ffba157da2641`](https://github.com/doublehidenblade/tokyo-drift-3d-shuto-web/commit/991decf0f94c7bc4e5619d637f4ffba157da2641)
- [Base playtest](https://doublehidenblade.github.io/tokyo-drift-3d-web/releases/playtest-20261008-1a5d967/index.html)
- [Shuto playtest](https://doublehidenblade.github.io/tokyo-drift-3d-shuto-web/releases/playtest-20261008-1a5d967/index.html)

## Publication evidence and limits

- Base first served at 2026-10-08 13:35:03 UTC. Complete readback at 13:36:14 UTC returned HTTP 200 with exact expected bytes for all 30 checked files, including the selectors, release metadata, loader, engine, and pack chunks. Reassembled base pack SHA-256: `eac2b4bf93a1826bdd878187adfb803a0df27af865cb8950c066b83018c73e4f`.
- Shuto selector, release HTML, and manifest returned HTTP 200 with exact expected bytes at 2026-10-08 13:38:31 UTC. Full Shuto binary readback was not completed; do not interpret this as complete binary parity or gameplay verification.
- [Pinned base deployment manifest](https://github.com/doublehidenblade/tokyo-drift-3d-web/blob/271ede178f1aa4d072cf988c1d2ba43d18911efd/releases/playtest-20261008-1a5d967/deployment.json) and [pinned Shuto release selector](https://github.com/doublehidenblade/tokyo-drift-3d-shuto-web/blob/991decf0f94c7bc4e5619d637f4ffba157da2641/release.json) identify the release and runtime source.
- No GitHub Actions workflow was manually dispatched for publication. GitHub's built-in Pages publication job ran automatically on the web-repository pushes. This documentation change does not dispatch Actions or deploy a game.
- The prior `releases/live-v46-4ecd2089` rollback directory and unrelated web-tree entries were preserved and verified during publication.

## Known limitations

Phone device-pixel-ratio sizing, incomplete legal-gig and station-fuel behavior, collision-blame behavior, and state resetting on reload remain disclosed limitations of the personal preview. Publication is not a claim that these are fixed. Full gameplay, visual acceptance, and Craig's phone confirmation remain outstanding.

## Ledger treatment

The `tokyo.personal_playtest` entry in [baselines.json](baselines.json) points to this publication separately from the historical normal-release fields. No entries are removed from [pending.json](pending.json), because personal-preview publication alone does not reconcile normal-release or source acceptance.
