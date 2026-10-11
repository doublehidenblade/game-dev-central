# td-238 terminal component — independent review

**CHANGES REQUIRED. T1, T2, T4 and T5 pass the component review; T3 fails two focus-restoration cases.** The existing 147 assertions all pass, but do not cover these failures. Formal evidence-policy acceptance is also unavailable: the five planned execution records do not have the canonical schema, and genuine current acceptance/admission inputs were not supplied. This report does not grant acceptance, a new correction, publication, or full td-238 completion.

Reviewer role: `dot-td238-terminal-component-reviewer`. Requested Astra/max is selection metadata; serving-model identity and billing are unconfirmed. Review performed 2026-10-11 in the selected `/workspace` environment, on isolated checkouts. No product source or policy was edited. No Actions, merge, deployment, export, paid service, security/credential change, external-agent contact or owner prompt-queue read occurred. Shuto and NEON were untouched.

## Exact sources and rules

- Source repository: `doublehidenblade/tokyo-drift-3d`, draft PR684.
- Artifact head: `709ea8711799cd44a87db643eef7409ac16f8e44`.
- Tested implementation: `fd8776c02aefab4f4de6cc0d2208838be93990d4`.
- Original source base: `f81232f777ea4151af6e096121087ef9890fa4e9`.
- Current source main observed: `f80754ea8c5cea99138f9c3623e155925f9b016e`.
- Current central rules main observed: `12dfb166d99f18d092c2b3066fc04481f6f5ef4a`.
- Source checkout: `/workspace/td238-review`; central: `/workspace/td238-review-central`.
- Evidence directory: `/workspace/td238-review-evidence`.

Read the source AGENTS/README, parent `godot/docs/tasks/td-238.md`, component companion, complete author handoff, relevant current canonical rules and policy/guard contracts, current td-238 board row, worker-registry references, and QA index. The source/central checkouts contain no `.agents/skills`; workspace `.agents` is empty. The 14 applicable rule paths were inspected in scope; their blobs match the prior document-review rule heads. The explicit delegated component review takes precedence over unrelated historical registry pickup and old merge/deploy/heartbeat instructions.

`source-equivalence.json` proves Git ancestry and **blob plus mode equality** for all nine code/UID paths and the entire parent task between implementation and artifact heads. Every existing Godot runtime blob/mode is unchanged from the source base. All nine code paths are new. Original parent text is an identical prefix; original fenced JSON, six criteria and four dependencies are unchanged. The artifact-only delta is evidence and one companion work-log entry. No production component mount/import or project/input/owner-file change exists.

## Findings

### IR1 — P2: immediate close/reopen forgets valid previous focus (T3 FAIL)

`godot/scripts/lower_city/debug_terminal_panel.gd:60-61` replaces `_previous_focus` on every open. `close_terminal()` hides the panel and schedules deferred restoration at lines 70-78. If the panel reopens before that callback runs, viewport focus is already null, so the original live sentinel reference is overwritten with null. The later final close cannot restore it.

Reproduction on unchanged source: sentinel focus → `open_terminal(1)` → frames → `close_terminal(); open_terminal(1)` in the same tick → frames → `close_terminal()` → frames. Expected: original `fixture.sentinel`; actual: null. Both headless and native X11 fail `rapid_reopen_preserves_original_focus`.

The author test at `test_terminal_component.gd:153-160` checks focus while the rapid toggles are open, then explicitly grabs the sentinel after closing. It never checks the final restoration and therefore misses this defect.

Evidence: `focus-probe.txt`, `focus-probe/execution.json`, `focus-probe/T2-raw.log`, `focus-probe-native/execution.json`, `focus-probe-native/T3-raw.log`.

### IR2 — P2: an allowed focusable parent cannot regain focus (T3 FAIL)

`debug_terminal_panel.gd:181-184` explicitly allows the fixture boundary itself to be focused when opening. The restore predicate at lines 202-204 requires `boundary.is_ancestor_of(target)`, which excludes `target == boundary`. A live, visible, focusable parent is consequently accepted at open and rejected at close.

Reproduction: set `fixture.focus_mode = Control.FOCUS_ALL`; `fixture.grab_focus()`; open; frames; close; frames. Open succeeds, but final focus is null instead of the same fixture parent. `parent_focus_restored_on_close` fails in headless and native X11. This remains inside the component's existing local boundary; it does not require gameplay integration.

Evidence: same six-check focus probe and native confirmation as IR1. No correction was attempted.

### IR3 — acceptance-record gap: all five execution artifacts fail canonical schema

The companion plans `T1-execution.json` through `T5-execution.json` as required assertion records. Their actual top-level shape is the runner receipt built at `run_checks.py:255-274`: nested `baseline`, `invocation`, hashes and controls. The canonical reader at central `project-management/watchdog/evidence_policy.py:566-578` strictly requires exactly `check_id command exit_code output source_head build performed_at actor_id`.

Directly applying the unchanged canonical `fields()` validator to each committed JSON returns **MALFORMED**, retained in `execution-schema-check.json`. This is a direct schema check, not a full acceptance-check run. The detailed receipts and raw outputs remain legitimate observations, and their hashes verify. However they are not currently consumable as the planned canonical execution records. A parent-authorized evidence step must preserve originals and supply genuine conforming records, the resulting exact evidence manifest and authenticated execution/capture observations. It must not fabricate actor receipts, command invocations, timestamps or digests.

## Criterion judgments

| Criterion | Decision | Independently verified evidence and limits |
|---|---|---|
| T1 | PASS | `debug_terminal_commands.gd:5-16,19-32,35-72`; 57 author assertions reproduced. Stable names/digits, both traffic presets, 256/257 boundary, rejection matrix and returned-container isolation work. Extra numeric formats, all ASCII controls, Unicode separator and aliases reject/accept correctly. Registry array and entry dictionaries are actually read-only. Wrong-number and numeric-coercion controls fail unchanged assertions. |
| T2 | PASS | `debug_terminal_panel.gd:105-158,161-178,210-240,322-330`; 19 author assertions reproduced. Tickets/revisions/generations reject stale or duplicate work; 100 repeated ticket/signal combinations produce exactly 100 accepted commands. Output stays 128 lines × 512 characters, recall 32; 512/513 boundaries and returned-history mutation isolation verified. BBCode, URL and image markup remain literal. All unavailable commands have no adapter path. Duplicate-submit and unbounded-history controls fail. |
| T3 | **FAIL** | 48 author assertions reproduce, including actual native XTest key/wheel flow, but IR1 and IR2 violate valid previous-focus restoration. Four matched original visual pairs pass direct pixel inspection; additional captures prove bottom content accessible at both sizes. Stale-focus negative control fails as intended. Human visual verdict remains pending. |
| T4 | PASS | `debug_terminal_panel.gd:41-52,177-184,210-248`; 16 author assertions reproduce. Disabled/mobile/unknown/empty platform, stale and nonpositive generations fail closed. Disable invalidates queued focus/submission; removal rejects submission; ordinary fixture input/button work. No real browser, mobile OS or network context is exercised. |
| T5 | PASS | `run_checks.py:202-233` and independent `source-equivalence.json`; seven author checks reproduce. Stronger Git blob/mode comparison, source hashes and production import/API inspection establish the admitted new-file-only source boundary. The inert owner-state dictionary is supplementary, not proof of production save/economy safety. No parent C1–C6 acceptance. |

All committed `Tn-raw.log` hashes match the respective execution records; all recorded implementation source hashes match the exact artifact bytes. Each negative control runs only in an isolated copy, leaves the original assertion source intact and retains unchanged committed source hashes. Negative failures: wrong-number 4, numeric-coercion 4, duplicate-submit 2, unbounded-history 1, stale-focus 1; these are expected control failures, separate from the two real-source focus defects.

Counts: **147/147 original assertions pass; 5/5 controls detected.** Broader independent probes: **105/105 pass**. Focus probe: **4/6 pass, 2/6 fail**, independently confirmed under native X11 with the same 4/6 result. Thus there are 111 distinct extra assertions, 109 passing and two failing; the native confirmation is a repeat in another rendering context, not six new distinct checks.

## Pixel inspection and comparability

Opened all eight original PNGs at original resolution, not just hashes or thumbnails. Each before image is explicitly labeled COMPONENT ABSENT with ordinary fixture controls; each after adds a real opaque terminal. This is a fixed 2D Control fixture, so comparability means identical viewport, screen-space framing, header position and panel margins, not a 3D camera claim. Same-size before images are intentionally identical across the two after states. Every image is nonempty and meaningful; there are no black/uniform/occluded substitute frames. All eight independent native rerenders are **byte-identical** to their original counterparts (`image-comparison.json`).

| Original pair (prefix under `godot/qa/td-238/terminal_component/`) | Direct observation |
|---|---|
| `T3-long-help-1280x720-{before,after}.png` | Matching fixture header/framing. Full title, Close, focused editor and hints visible. Help top shows options 1–3; lower options intentionally continue in the viewport. Actual wheel reaches bottom 394, revealing options 4–6, bounds and final hint. |
| `T3-long-help-960x540-{before,after}.png` | Same 960×540 framing, 28px side margins, readable title/Close/editor. The top frame clips at option 2; scrolling reaches 574 and reveals option 6, limits and all bottom hint text. |
| `T3-unavailable-1280x720-{before,after}.png` | All four owner-contract refusal messages fit, with explicit Nothing was applied. No scrollbar is needed; viewport remains 1280×720. |
| `T3-unavailable-960x540-{before,after}.png` | Exit refusal is clipped by the initial output viewport. Actual wheel moves 0→22 and reveals the full final refusal while editor/Close stay visible. Scrollbar visibility is false for this small overflow; wheel access is independently proven, but the original still alone does not show the hidden text. |

Also opened all four independent `adversarial-rerun/review-*-bottom.png` captures. The top/bottom help images together and scroll observations establish access to all entries. The unavailable bottom probes deliberately use numeric aliases `1`, `2 busy`, `4`, `6`, confirming identical truthful refusal output. Keyboard Escape/F10/3/Return was exercised in all four size/state cases. These supplementary bottom captures are scope-labeled probes, not replacement before/after evidence.

Actual native path: existing Xorg dummy configuration on isolated display `:98`, Godot 4.7.2 OpenGL compatibility, Mesa llvmpipe, X11/Xtst. The original 15 driver event records include eight OS wheel events moving help 394→10. These are actual injected OS events, not a physical keyboard/device claim. No browser/phone rendering, CSS/DPR behavior, production Lower City interaction or performance acceptance is established.

## Admission and preserved attempt history

Fresh connected PR reads verify source681 merged as `f80754ea8c5cea99138f9c3623e155925f9b016e` at 07:17:34Z, and central469 merged as `da1c3c0097a0c4cf887ef0b130b0851ba4ba6f27` at 07:18:12Z. Their committed independent A1–A4 document verdicts exist. These are document admission, not runtime acceptance.

Inspected `admission-guard.json`: recorded actual result is GO, with one ACTION_REQUIRED implementation action, author/owner/executor `dot-td238-terminal-component-author`, exact admitted head `d1c892184a6dc00c661f8cc807d1324ffdb1b4f3`, decision ID `18fad328263aadb0b10c41516fca159d3dc1cdd50a74552987e7cbb5c2177645`, performance time 07:51:57.912258Z and expiry 08:00:32Z. `implementation-start.json` binds the same head/decision and T0 07:52:27.394435Z, before expiry; deadline is 09:52:27.394435Z. The receipt explicitly leaves global coverage unknown. Actual Git ancestry reaches the artifact.

The original admission authority/snapshot/raw-object inputs are not in this checkout; the retained result cannot independently prove source/owner/queue completeness. Requested those retained inputs and a current exact-head reviewer verification guard from the parent. None has been supplied. This review proceeds under the explicit reserved read-only delegation; it does **not** claim a newly established supported GO or global inventory/liveness. Owner prompt queues were not read. A parent-supplied fresh verification snapshot is the concrete missing prerequisite to replay that guard.

Preserved initial implementation `a37416f0a4294a7396844d1e2babbd920fc52f34` failed at test line 143 before any behavioral assertion: inferred Variant from `weakref` was treated as an error. Initial raw logs and records remain under `initial-attempt/`. The sole correction at `fd8776c...` changes only `var previous := ...` to `var previous: WeakRef = ...` plus retained failure evidence. Parser and panel bytes were unchanged. `correction-record.json` records one correction used, zero remaining. **The two new failures must be parked for a parent decision; this reviewer neither fixes them nor resets the budget.**

One reviewer probe initially failed at result parsing because a literal U+2028 in a test label was split by Python `splitlines()`. Its text and diagnostic are retained in `independent-probe-initial.txt` and `adversarial/initial-probe-failure.txt`. The corrected reviewer-only label uses UTF-8 hex; no product or committed assertion changed. No pass/count is claimed for the failed probe invocation.

## Reproduction and handoff

From `/workspace/td238-review`, run the existing runner with a fresh evidence output directory for each criterion:

```sh
python3 godot/qa/td-238/terminal_component/run_checks.py --godot /workspace/tokyo-drift-3d/.tools/Godot_v4.7.2-stable_linux.x86_64 --criterion T1 --output /tmp/td238-review-fresh-T1
```

Use T2/T4/T5 likewise; T5 base is `f81232f777ea4151af6e096121087ef9890fa4e9`. T3 requires `DISPLAY=:98`, `--criterion T3 --render` and a working isolated X11 display. Engine hash is `8d106cbe6144c2dc7e881d61d2429c1a8a76e6b22ef48bd5e48dcf934953f71e`; the runner verifies it and exact version before running. The runner copies only the component/fixtures into a fresh minimal temporary project, uses Dummy audio, isolates XDG paths and cleans up its child processes. It never launches the production Godot project.

The one-off probe texts and `probe-reproduction.txt` document how the existing runner was reused with temporary fixture scripts. Every product source hash is retained before/after. They are review evidence, not new committed tooling or a policy change. Native focus confirmation uses the same probe with rendering enabled, while the lifecycle operations remain programmatic; real OS input is covered by the original T3 and broader probe.

`independent-review.json` contains structured criterion findings with actual immutable Git blob citations and local evidence. It is deliberately **not** labeled a canonical acceptance verdict: genuine parent authority, full final submission evidence manifest, conforming execution/capture records and collection receipts are missing, so no authority/evidence digest or attestation is invented. The canonical verdict schema is at `evidence_policy.py:645-698`; it cannot accept this source while T3 fails. Craig's visual judgment remains pending separately.

Inspected screenshot saved successfully to Library: `td238-terminal-inspected.png`, file ID `file_00000000a9d881f7815c2ab79cbddb0d`, Library ID `libfile_e83fbb0e43a881919f77d1d3da18976a`; exact original bytes and returned identity/xattrs were retained. It is the 1280×720 unavailable-command frame.

All review outputs remain local. No source publication was performed. Seven exact source workflows were inspected as dispatch-only, and central has no workflow files; current target triggers must be checked again before any later source publication. Parent may request an exact evidence-only destination/publication step after judging this report. Both review checkouts finish with no tracked or untracked changes. Original author evidence and all failures are preserved.
