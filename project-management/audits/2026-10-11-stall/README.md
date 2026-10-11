# Stall audit evidence — 2026-10-11

Pulled from Craig's Mac (`~/Desktop/AI/gpt-stall-evidence`) on 2026-10-11 and
committed here so dot can pull the canonical copy. Byte counts verified against
the Mac's reported sizes; SHA-256 recorded in `manifest.json`.

## Contents

- `Game-coordination-stall-audit.md` — dot's own audit: 12 incident groups
  (Oct 9–11), 45 idle/no-implementation reports across 8 runs, repository
  evidence index, and the garage/PR374 selection failure.
- `Second-opinion-prompt.txt` — dot's generated prompt for an independent
  second opinion.
- `td197-stall-audit-evidence-20261011/` — garage task admission result and
  PR374 stop provenance (the missed R4 stop).
- `td238-terminal-independent-review-audit/` — terminal independent-review
  evidence (T1–T5 probes, adversarial reruns, screenshots).
- `worker-status-registration-cbf9393-private-audit/` — worker-status
  registration, admission-blocker history, runbook excerpts, board snapshot.

## Gaps (recorded, not reconstructed)

- `Second-opinion-prompt (1).txt` on the Mac is a byte-identical download
  duplicate of `Second-opinion-prompt.txt`; not committed.
- The audit's "Read in this order" lists companion files that were NOT in the
  Mac folder and are therefore missing from this package: `chronology.md`,
  `repository-index.md`, `workers/worker-index.md`, `local-inventory.md`,
  `watchdog-saved-config.json`, `inspector-saved-config.json`,
  `USER-PROJECT-PERMISSIONS.md`, and the project-only transcript
  (`history-project.md`) behind the `[^E1]`–`[^E130]` message references.
  A second-opinion review cannot verify claims that cite those files.

## Status

Evidence only. No policy change, dispatch, merge, or deployment is authorized
by this commit.
