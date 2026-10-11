# Frozen td201 registration replay

Run from the central repository with its normal environment activation:

```sh
set -euo pipefail
source /workspace/.setup/activate.sh
python3 -B project-management/watchdog/fixtures/registration-admission/replay_td201.py \
  /workspace/td201-frozen-input/td201-admission-frozen-20261011.zip \
  --central-git /workspace/game-dev-central
```

The unchanged archive is Library `libfile_d6ea4167f8148191bd43222ea2e426e7`,
version 1, SHA256 `35b6a2bde4d1506c0b4de7779d34bb7932959f858a21f326610e9d2f943dff87`.
The replay verifies this hash before reading the supplied objects. It does not
publish the archive or its private parent notes. The central checkout must retain
historical commit `7aba8fceb697085fe179ca34795d5bfe40a99133` so the existing board
and attempt journal can be read with `git cat-file`. No fetch, write or new sweep
occurs during replay.

The real unpublished candidate is `4c5381ab698a15ebbd947906843ffd311055d87f`.
Its ten actual document edits are measured from its reviewed source parent;
canonical main's unrelated `td-229.md` addition is not a candidate deletion.
The original td201 document is intact with an appended reconciliation section.
The blocked parent, td200 dependency and transitive td197–td200 chain survive.
The archive's 659 historical branches remain historical, not admission work.

`td201-pr455-coexistence.json` contains only exact public PR455 Git objects,
the public issue450 owner source, and the coordinator's explicitly approved
same-owner serialized disposition. It proves the six-file PR delta and disjoint
parent appendix regions without combining source hunks. It preserves the old
td198 assigned-session identity found in the public source: the live guard needs
a current, exact ended-session receipt before using this disposition. The
disposition is evaluated at its recorded observation for reproducibility; it
does not stay fresh indefinitely or authenticate an inclusive live collection.

The [saved result](../../../dispatch/registration-admission/TD201_REPLAY.json)
reports source-scope PASS and live INPUT_REQUIRED. The original authority's
21:34 observation remains stale. No current owner/session/stop/queue/trigger or
finite-allocation receipt is fabricated. The replay exercises the same source
inspection and compatibility functions called by the guard and then supplies
the disposition to the full guard, which remains held on missing current inputs.
