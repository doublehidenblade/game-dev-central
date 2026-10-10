# Watchdog runbook — scoped coordinator decisions

Run from the repo root (`game-dev-central`). All paths below are repo-relative
unless stated otherwise. The supported coordinator route below is read-only;
legacy automatic admission and queue delivery are retired.

## Current authorization boundary (2026-10-08 19:56 UTC)

Before any push or merge, read the [canonical deployment authorization and budget policy](releases/PUSH-PROCEDURE.md#deployment-authorization-and-actions-budget-craig-2026-10-08-1956-utc). Deploy only on Craig's explicit request, including site/deployment-branch pushes that trigger Pages. The GitHub Actions budget is **$50/month**: a ceiling, not standing permission or verified current spend. Ordinary source pushes and independently accepted merges need no fresh go-ahead; inspect current push/PR/merge and publication triggers first and hold operations that would deploy or run unauthorized Actions. Do not assume all pushes are free.

This boundary applies to any externally performed merge, conflict-resolution push or state push. Required acceptance checks and independent verification remain mandatory for merges; no incomplete or failing work is accepted by this policy. Do not manually dispatch/rerun Actions or change billing/security. Keep merged-but-unpublished changes in pending.json. Shuto stays frozen; NEON stays paused/read-only. No scripted verdict or old instruction creates permission to deploy.

[JUDGMENT-ONLY: authenticated request scope and current external trigger configuration require inspection; this documentation does not implement a new automatic watchdog gate.]

## Implementation-first Lower City priorities (Craig, 2026-10-09)

Craig asked for High / Medium / Low ranking, with implementation ahead of
browser, phone and visual-evidence follow-up. Apply this dated ordering when
selecting among otherwise authorized, owner-safe next actions; it supersedes
oldest-unverified-first **selection** for these records, not acceptance rules.
Do not manufacture a new feature, dispatch, owner transfer or acceptance from a
priority label. Existing stops, frozen authors and source-merge gates remain.

- **Implement useful gameplay first.** Distinguish absent behavior from code
  already on a branch or merged. Preserve existing work; investigate a concrete
  remaining defect instead of recreating a feature because evidence is missing.
- **Browser / phone / visual-evidence follow-up is LOW.** A High feature row
  does not elevate its evidence-only follow-up. Renderer unavailability does not
  block separately authorized implementation. Missing evidence remains missing;
  required acceptance checks and independent verification still gate source
  merges, and visual closure still requires the applicable Craig verdict.
- **Personal playtests are separate.** On Craig's explicit deployment request,
  CI/gameplay/browser/visual/phone checks need not delay that requested playtest;
  disclose failed and unrun checks and known defects. This ranking is not a
  deployment request, merge acceptance or permission to run Actions. Follow the
  [existing deployment procedure](releases/PUSH-PROCEDURE.md), existing sites,
  $50/month Actions ceiling and all publication/ownership stops.
- **Unblock or surface the exact dependency.** Pursue safe, already-authorized
  source recovery, contract discovery and isolated work proactively. If a
  decision, owner handoff, denied publication or real packaging limit remains,
  tell Craig the affected task, missing input, attempted safe next step and the
  specific decision needed. Do not hide these as generic external waits or
  substitute low-value parser/evidence work. Respect the existing coordination
  cadence and external-contact limits; this creates no permission to contact an
  outside agent. Continue another authorized implementation lane when possible.
- **Keep explicit stops.** td-233's aborted admission stays stopped until Craig
  explicitly resumes it, despite its High gameplay value. td-238 debug terminal
  and parser work stay **LOW / PARKED**. Shuto stays frozen and NEON paused.

### Ranked snapshot: 19 High, 13 Medium, 10 Low

These 42 retained records comprise 40 unresolved/open rows plus td-245 and td-248
whose merged-code acceptance is disputed. They are not 42 unimplemented features
or a dispatch batch. Rank expresses gameplay value; prerequisites and current
owners still determine which action can actually proceed. The existing
[canonical board](../boards/tokyo-drift-3d.md) and linked source tasks remain the
ownership/status truth. No board or task status is changed here.

Source snapshot checked 2026-10-09: central main
`4bb11ee327d2a2a766e48145e101b7b42c2354dc`, board blob
`368e4c47574faf9b55a6b1ed31b9a275f5f9cab9`; Tokyo source main
`50616cb024f64af4b20be8e0e0ef7738b5c918e3`. All 42 source-task blobs were checked
against that source tree. This is a dated planning snapshot, not a live claim of
worker availability or implementation acceptance. Re-read affected sources before
acting; do not use stale prose to override a newer hold or an existing owner.

| Rank | Priority | Task | Remaining work / existing code | Next action and dependency |
|---:|---|---|---|---|
| 1 | High | [td-217](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-217.md) | Implementation needed | Reproduce repeated/over-severe contact damage, then repair scaling/deduplication with the existing vehicle/damage owner; preserve cargo/body semantics. |
| 2 | High | [td-218](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-218.md) | Implementation needed | Define real repair-service and persistent-condition providers with the existing damage owner, then implement discoverable, quoted, exactly-once paid recovery. Preserve current task criteria pending reconciliation: its zero-cash wording conflicts with Craig’s explicit broke/no-gas or unsalvageable game-over direction; no free/debt recovery is authorized. Existing runtime lacks those providers; do not invent them. |
| 3 | High | [td-231](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-231.md) | Implementation needed | Repair abrupt coasting stop and add tunable progressive throttle/brake response; coordinate impact semantics with td-217. |
| 4 | High | [td-195](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-195.md) | Further repair needed | Retain merged collision body; fix remaining cop height/surface alignment defect through the existing Muse lane. |
| 5 | High | [td-220](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-220.md) | Implementation needed | Trace isolated pedestrian hit to crime/cops; prevent repeated crime escalation from a single contact. |
| 6 | High | [td-200](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-200.md) | Foundation exists; production missing | Recover the exact previously tested corrected snapshot and reconcile publication first; then implement production inventory/supplier/save adapters after garage contracts. |
| 7 | High | [td-197](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-197.md) | Prerequisite design work | Complete measured, real-geometry garage layout and usable first-slice mock decision; unblock geometry rather than polishing presentation indefinitely. |
| 8 | High | [td-198](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-198.md) | Implementation needed | Build real Lower City drivable garage with loaded-car clearances, safe entry/exit and fixed workshop camera after layout acceptance. |
| 9 | High | [td-199](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-199.md) | Implementation needed | Implement entry/shutter/obstruction and legitimate police-shelter contract without heat reset or timer exploits. |
| 10 | High | [td-201](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-201.md) | Implementation needed | Implement usable first-upgrade workshop flow and prerequisite-aware discovery against real inventory. |
| 11 | High | [td-213](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-213.md) | Code exists; integration/test later | Preserve shared map/gig-access candidate; make available in a requested playtest composition without rewriting already-fixed logic. |
| 12 | High | [td-214](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-214.md) | Code exists; child acceptance | Use PR545 cancel/abandon implementation; retain lifecycle and no-double-payout checks; no new worker. |
| 13 | High | [td-219](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-219.md) | Code exists; child acceptance | Use PR545 real fuel waypoint/navigation; retain inconclusive arrival/Fuel evidence as disclosed limit. |
| 14 | High | [td-223](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-223.md) | Code exists; known verification failure | Preserve deadlock repair; determine whether nine shutdown errors are existing teardown noise or repair regression; only implement a demonstrated defect. |
| 15 | High | [td-224](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-224.md) | Code exists; test later | Preserve camera-wall repair and include in requested candidate as appropriate; browser/phone proof stays later. |
| 16 | High | [td-212](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-212.md) | Partial code; optimization still needed | Keep resolution controls; use Craig-provided slow-route evidence to scope actual bottleneck optimization, not another generic UI pass. |
| 17 | High | [td-233](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-233.md) | Implementation needed | STOPPED: prior admission explicitly aborted. Resume only on Craig’s explicit direction; shared loader/td-226 handoff remains required. |
| 18 | High | [td-234](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-234.md) | Packaging code exists; release capacity blocker | Recompute complete candidate size and use bounded runtime-reuse packaging for one preview if feasible; no deployment authorized now. |
| 19 | High | [td-185](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-185.md) | Core code already merged; umbrella stale | Retain existing world/gig assembly and Craig ownership; reconcile any actual remaining scoped gaps, do not recreate PR407. |
| 20 | Medium | [td-215](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-215.md) | Implementation needed | Expose one-action authoritative cargo/vehicle details without inventing persistent condition/capacity. |
| 21 | Medium | [td-216](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-216.md) | Code frozen; publication incomplete | Preserve cash/fuel readability work; resolve existing publication blocker, then include exact candidate when permitted; do not recode. |
| 22 | Medium | [td-222](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-222.md) | Implementation needed | Display existing lost-sight countdown truthfully; do not create another heat timer. |
| 23 | Medium | [td-221](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-221.md) | Implementation needed | Render real police pose/FOV on both maps through read-only interface; distinguish geometry from actual occlusion. |
| 24 | Medium | [td-228](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-228.md) | Code exists; child acceptance | Use shared PR545 recenter/bounds; no new worker or separate implementation. |
| 25 | Medium | [td-226](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-226.md) | Implementation needed | Provide immediate Lower City Restart cover/progress and single restart lifecycle; reuse shared owner work without assuming Tokyo Bay fix closes it. |
| 26 | Medium | [td-235](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-235.md) | Implementation needed | Implement contrasting target symbol only, then hand shared MapSheet region to itinerary work. |
| 27 | Medium | [td-237](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-237.md) | Implementation needed | Build single synchronized editable itinerary and truthful destination/service cues from real owner APIs. |
| 28 | Medium | [td-236](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-236.md) | Implementation needed | Build map-led briefing and central navigation shell as client of shared itinerary/status/inventory contracts. |
| 29 | Medium | [td-229](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-229.md) | Implementation needed after reproduction | Identify why highway lacks civilians on reported route; fix shared spawn/lane eligibility with existing traffic owner. |
| 30 | Medium | [td-230](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-230.md) | Feature integration/tuning needed | Establish useful street/highway speed-density-delivery contrast; consume existing signals rather than rebuild td-248. |
| 31 | Medium | [td-248](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-248.md) | Implementation repair needed | Repair continuous pedestrian crossings and missing road-paint ARRAY_INDEX wiring through the existing Muse owner; PR620 code is merged. Evidence retakes follow functional repair. |
| 32 | Medium | [td-186](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-186.md) | Assets already merged; integration gaps | Reuse Forge outputs; no new wholesale asset job. Track real third-party rig/access limits separately with Claude owner. |
| 33 | Low | [td-245](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-245.md) | Code merged; acceptance disputed | Retain Lower City WantedHUD mount and evidence; do not recode notices/stars; resolve production-scene arc/log readiness dispute later. |
| 34 | Low | [td-192](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-192.md) | Code merged; acceptance later | Keep separation source fix; later verify real-player three-cop pursuit without invented four-cop requirement. |
| 35 | Low | [td-232](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-232.md) | Code frozen; UI refinement | Park payout animation/color refinement; preserve frozen source and known acceptance gaps; no new correction budget. |
| 36 | Low | [td-243](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-243.md) | Code exists; Tokyo Bay check later | Let existing Muse owner finish restart criterion when capacity permits; does not outrank Lower City work. |
| 37 | Low | [td-225](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-225.md) | Implementation needed; visual placement | Fix shared sign placement/clearance later unless a specific instance obstructs driving or essential navigation. |
| 38 | Low | [td-227](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-227.md) | Implementation needed; cosmetic | Repair police floating black geometry in asset binding after core collision/playability work. |
| 39 | Low | [td-187](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-187.md) | Future art assembly | Keep art-book district scene work parked until gameplay foundations; consume existing Forge assets. |
| 40 | Low | [td-238](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-238.md) | No implementation; LOW / PARKED | Leave terminal and parser work parked. Documentation registration does not create gameplay implementation or admit an author. |
| 41 | Low | [td-249](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-249.md) | Implementation needed; explicitly low | Later replace pedestrian pop-in/out with door entry/exit using actual door data and documented fallback. |
| 42 | Low | [td-202](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-202.md) | Validation only; later | Run independent full garage first-slice integration after usable implementation exists; do not make this a new feature job. |

### Serialize overlapping file areas (Craig 2026-10-10)

The td-204 → td-205 → td-207 revert/redo (three PRs, net zero) happened because
parallel workers rewrote the same UI files without coordination. Prevention:

- **One worker per file area at a time.** Before dispatching, check live workers'
  registered file areas (worker heartbeats + task files). If a candidate task
  touches files another live worker is actively modifying, hold the dispatch
  until that worker merges or goes idle. File areas: HUD/UI scripts, scene
  files (.tscn), autoloads, vehicle physics, pedestrian systems.
- **Worker-side check-main-first is mandatory** (WORKER_BRIEF.md rule 13):
  every worker reads the current main state of shared files before writing.
  Silently reverting merged work is banned.
- **Briefs name the conflict explicitly.** When dispatching onto files another
  worker recently touched, the brief's "already on main" section must describe
  what is there and how to build on it, not overwrite it.


### What should move next, and what is genuinely blocked

- First implementation candidates are damage scaling/contact deduplication
  (td-217), repair/tow recovery (td-218), coasting/throttle/braking (td-231),
  remaining police road-height/collision repair (td-195), and the garage
  progression chain (td-197 → td-198 → td-199 → td-200 → td-201). These are
  candidates, not new admissions. Existing Muse/Claude owners retain their lanes;
  the damage/vehicle handshake follows the existing scheduled coordination route.
- td-200 has reviewed foundation work, but its corrected source packet must be
  recovered before publication is proposed; its author remains frozen, production
  adapters are absent, and the rejected obsolete payload must never be retried.
  The garage chain also needs measured layout, real geometry and entry/shutter/
  police contracts. td-216 likewise has frozen local code with incomplete
  publication; preserve it instead of recoding it.
- td-218 and td-237 require authoritative repair-service / persistent-condition
  contracts. Missing providers are implementation dependencies, not browser
  failures. td-217 has real contact inputs to investigate within its existing
  damage/vehicle ownership boundary.
- td-234 packaging capacity needs fresh accounting for the exact requested
  candidate. The prior approximately 5.2 MB proxy headroom estimate is not current
  verified capacity. Deferring browser checks cannot create packaging capacity.
- Existing code should be retained: PR545 covers td-213/214/219/228; PR531 td-223;
  PR544 td-224; PR532 td-212; PR550 td-232; PR556 td-234. Their presence is not
  acceptance. td-223's strict verifier failure remains disclosed; td-212 still
  lacks measured performance gain. td-185/186 have merged PR407/416 despite
  stale open umbrella rows; reconcile actual remaining gaps, not duplicate code.
- td-245's merged HUD mount is retained; its full production-scene acceptance
  dispute is later evidence work. td-248's merged code has concrete crossing and
  mesh-index defects, so those repairs remain Medium implementation work.
  td-192 keeps its canonical three-cop criterion, not an invented four-cop gate.

This section is documentation only. It installs no collector, dispatcher,
ranking engine, queue reader or framework, and does not run a coordinator cycle.

## Coordinator engineering registration — 2026-10-09 12:44 UTC

| Task | Work | Status | Owner | Review | Updated (UTC) |
|---|---|---|---|---|---|
| ops-coordinator-enforcement-20261009 | Script scoped blockers, task rotation, executor capacity and truthful idle decisions | accepted and merged — PR396 review5471277399; merge39aa747c7f1f35393a316faebd942386579ff913 | dot — coordinator enforcement; one native implementation author, separate independent reviewer | Registration PR393; final PR396 independently accepted and merged at2026-10-09T14:17:33Z; runtime attestation remains unconfirmed; no live collector installed | 2026-10-09 14:17 |

Craig requested scripted enforcement and repository-owned reusable coordinator logic on 2026-10-09. This row registers that bounded central-repository work; it does not register a live implementation worker, accept code or change any existing game task's owner/status.

- **Implementation scope:** one pure decision layer and side-effect-free command entrypoint under `project-management/watchdog/`; fail-closed integration of existing dispatch/eligibility/idle entrypoints in `watch.py`; regression tests in `test_rules.py` with public-safe fixtures; concise usage in this runbook and, only as needed, `COORDINATOR.md`. No new workflow framework. PR143's separate visual-evidence onboarding edits must be preserved if `COORDINATOR.md` changes.
- **Acceptance:** blockers identify their task, operation and executor scope; upload or deployment holds do not silently block authorized implementation, admission or independent verification. Rotation considers those distinct next actions, while preserving explicit stops, denials, ownership and required capability. Native dot capacity is separate from Codex/Claude capacity. Implementation, upload, merge and deployment gates remain separate.
- **Evidence and idle checks:** a complete, fresh source manifest and current exact-head evidence reconcile stale main/PR-body descriptions without overriding explicit holds. Missing, stale or contradictory required inputs fail closed. A shared decision result must reject idle when an authorized, ownership-safe next action and qualified available executor exist; missing inputs cannot return OK. Compatibility entrypoints must not bypass this result.
- **Verification:** replay the overnight failure classes, including scoped publication holds, unavailable Codex with available native capacity, review/admission work, stale-head claims, stopped/owned lanes and malformed/incomplete snapshots. Prove the new entrypoint and integrated aliases do not write state, queues or ledgers, call external dispatch, or contact providers. Exercise old aliases without a verified snapshot and require an input error rather than stale-state approval. Independent exact-head review must cite these checks; documentation alone is not enforcement of any live coordinator.
- **Recommended setup:** frontier native dot author, requested `gpt-6-astra/xhigh`, with Python and isolated fixtures; one initial attempt plus at most one evidence-based correction within two hours, with a separate frontier/xhigh review budget. Native catalog and repository tools are available; the registration originally preceded author startup and did not attest a runtime. Verify the selected author and Python test setup before implementation. Wait for the required tier if unavailable; report scope/ownership conflicts, unsafe entrypoint effects or failed tests without weakening gates. Outcome pending.
- **Attempt amendment — 2026-10-09 13:28 UTC:** the initial candidate `b765a587cd78554d047e06b6bafee9de91c1be7e` and first correction `82a6df52855a3b3a07b9bdc177684214e2946ff0` are retained. [The coordinator's bounded amendment](https://github.com/doublehidenblade/game-dev-central/pull/396#issuecomment-6081855820) authorizes one additional correction for two reproduced read-only routing defects: unrelated unmapped branches blocking exact-head verification, and explicit post-merge verification losing its source. The outer deadline stays 2026-10-09 14:46:40 UTC. No broader retry, weaker acceptance, live operation or merge is authorized by this amendment; independent repaired-head review remains required.
- **Bounded v4 correction — 2026-10-09 14:00 UTC:** v3 `b0b3c8a465c0cfd6b1b03fc87092094dbf29a457` is retained with its changes-required review. [The recorded amendment](https://github.com/doublehidenblade/game-dev-central/pull/396#issuecomment-6082442592) allows only the independently reproduced acceptance-isolation repair: conflicting same-head PASS/FAIL acceptance must retain a separately authorized, explicitly needed independent read-only verification path, while conflict warnings, acceptance/mutation blocks and all source/ownership/capability/stops remain. Both open and merged regression probes are retained. The original 14:46:40 UTC outer deadline and separate exact-head review remain; evidence-feedback framework work is outside this task.
- **Bounded v5 correction — 2026-10-09 14:11 UTC:** v4 `bf4251a0c63464bf91457352e2bd3e504b5904c4` is retained. Independent review reproduced a remaining same-family defect: removing verification from a merged task's needs hid its known same-head conflicting acceptance and could recommend upload or false idle. The coordinator authorized a bounded correction to resolve known immutable source/acceptance independently of the requested operation list, within the original 14:46:40 UTC deadline. The unchanged independent 128-case needs matrix and two-case hold-invariance probe are retained; unrelated operation-specific source requirements are not broadened. Independent exact-head acceptance remains pending.
- **Preflight:** central main `0b4f00e6c5fa810ad2e8e2a94758c9ba60e8a354`; canonical rules, board, registry, log and current state read; all 100 open PR changed-file lists and 322 branch names checked. No open PR changes `RUNBOOK.md`, `watch.py` or `test_rules.py`; PR143 touches `COORDINATOR.md`. The complete tree has no GitHub Actions workflow files. The legacy registry and empty worker ledger are not proof that outside sessions are idle; this reservation grants no game-task takeover.
- **Boundaries:** the original registration changed only this runbook; this candidate implements its bounded read-only enforcement scope. No legacy watcher execution, live queue/state/ledger writes, automatic dispatch, external-agent contact, Actions, deployment, provider/security workaround or stopped-operation retry. Existing td-200/216 upload denials and central PR374/376/368 plus Tokyo PR553 holds stay unchanged. Shuto stays frozen; NEON stays paused. Registration was independently reviewed and merged as PR #393. One scoped native author started 12:46:40 UTC with Python 3.12.14, reverified for the v5 correction; requested model/effort remains distinct from runtime attestation. PR396 received independent exact-head acceptance in review5471277399 and merged as39aa747c7f1f35393a316faebd942386579ff913 at2026-10-09T14:17:33Z. Requested/native selection remains distinct from runtime attestation; no live collector or dispatcher is installed. Later evidence-policy changes require their own independent acceptance; no additional user-approval gate is introduced.

## Supported coordinator route (2026-10-09)

[SCRIPTED: watch.py coordinator-plan] The supported route is a read-only decision
cycle over an explicit snapshot. It does **not** run the old watcher, write live
state, claim ownership, create sessions, deliver queues, contact providers, merge,
upload, trigger Actions, or deploy. A permitted action is a scoped recommendation
for the authorized coordinator, not proof an action happened or new permission.

1. Read the current task sources, board, ownership registry, live worker/session
   observations, pending queue, requests, holds, branches, PRs and review/check
   evidence. Exhaust pagination. Include all known task/PR IDs, not a shortlist.
   Reconcile identities and preserve unknowns rather than converting them to idle.
2. Normalize those observations using the version-1 contract below. Keep live
   snapshots private if their source data is private. Do not commit private
   prompts, session URLs, tokens, or internal notes. Reusable code and synthetic
   fixtures belong in this repository.
3. Run `python3 project-management/watchdog/watch.py coordinator-plan --snapshot <snapshot.json>`.
   `ACTION_REQUIRED` means at least one scoped next action exists; report/use an
   authorized alternative instead of claiming global idle. `INPUT_REQUIRED`
   means required observations are missing, contradictory or stale. `IDLE` means
   no permitted action was found **within the declared, fully accounted scope**;
   inspect `blocked` to see why, rather than assuming tasks are complete.
4. The `actions` list contains alternatives, **not a concurrent dispatch batch**.
   Select one, retain its complete JSON object, and refresh observations before
   the action. Revalidate with:

   `python3 project-management/watchdog/watch.py dispatch-guard --snapshot <fresh.json> --decision <selected-action.json> --task <id> --operation <operation> --executor <id> --owner <identity> --head <full-sha>`

   Any input, owner, source, permission, hold, target or freshness change invalidates
   the receipt. Re-plan after a changed observation or completed action. Revalidation
   does not execute the action, reserve a worker, authorize an upload target, or
   replace the existing confirmation, workflow-trigger and release checks.
5. Report useful results and scoped blockers. Do not wait on one blocked task
   while another authorized action exists. Admission of an unfiled ask and an
   independent review are work too. Retain acceptance and publication holds.

### Entry points and exit codes

[SCRIPTED: watch.py idle-defect-check] These names all use the same evaluator and
JSON contract: `coordinator-plan`, `dispatch-candidates`, `dispatch-eligible`,
`dispatch-guard`, `idle-defect-check`, `all-blocked`, `review-sweep`, `heartbeat`.
They require `--snapshot`; there is no fallback to legacy state. The idle check
returns **3** when an action exists, never an `OK`/idle verdict. Missing input
returns **2**, guard mismatch returns **3**, a valid plan/guard returns **0**.
`ACTION_REQUIRED` may coexist with warnings about unrelated scope or missing
acceptance-only evidence. Warnings always prevent a global `IDLE` conclusion.

The new route bypasses `_capture_verdicts`, which historically wrote live state
in a `finally` block even for an idle check. Both CLI routing and imported
`cmd_*` aliases use the safe adapter; regression tests exercise both.

### Snapshot contract

`coordinator.py:validate` is the strict executable schema. Unknown fields,
malformed types, duplicate IDs/JSON keys, ambiguous repositories and abbreviated
SHAs are rejected. [The synthetic fixture](fixtures/coordinator-snapshot.json)
is a shape example, deliberately dated and **not authority or a live inventory**.
Never refresh its timestamps to masquerade as a new observation. The fixture
builders in `test_rules.py` are test-only, not a collector.

Top-level fields:

- `version`: integer `1`; `observed_at`: explicit UTC timestamp
- `repositories`: map of each subject/source `owner/repo` to its observed full
  lowercase 40-character head SHA
- `sources`: one source receipt for each repository × table below
- Twelve normalized record arrays: `policies`, `board`, `tasks`, `prs`,
  `branches`, `reviews`, `checks`, `requests`, `owners`, `queue`, `blockers`,
  `executors`. Every record has a unique table-local `id` and `repository`

Each source receipt contains `id`, `kind` (table name), `repository` (subject
scope), `source_repository` (origin), `ref_sha` (origin repository pin),
`observed_at`, `read_status` (`ok`, `partial`, `unreadable`), `pagination`
(`pages_read`, `items_seen`, `exhausted`), and explicitly enumerated `ids`.
Repository-level pins describe the observation context; task/branch/PR/review
records additionally pin the actual candidate/evidence head. A source receipt
aggregates **all** necessary reads for that kind: for example, ownership includes
registry, sessions, reservations and known outside workers, not just one empty
legacy ledger. `requests` includes current asks and authorized routine-work scope;
`blockers` includes current stops, denials, release/packet holds and cancellations.
If any constituent read fails or pagination is unfinished, mark the aggregate
partial/unreadable. Do not assert an empty successful source when it was unread.

IDs and item counts must match normalized records exactly. Board and task-file
inventories must reconcile; every PR lists its exact `review_ids` and `check_ids`,
which must match the review/check arrays. All related records must refer to the
same task, repository and PR. Unknown/unmapped branches require reconciliation.
The observation age limit is 15 minutes, exclusive, including each review/check
record's `observed_at`; a fresh aggregate receipt cannot refresh an old individual
read. Future or timezone-naive observations are invalid. No `complete=true`, caller-supplied candidate array,
or empty queue can override these checks.

Record-specific fields (see fixture/schema for complete types):

- `policies`: exactly one per repository; `triggers_checked`, `push_runs_actions`,
  `push_deploys`, `merge_runs_actions`, `merge_deploys`. Record actual observations,
  not permission inferred from budget. Unknown triggers hold source upload/merge
- `board`: task `id`, full `head_sha`, `status`, `owner_id` (null means positively
  observed unassigned). Stale ordinary status descriptions can be reconciled to
  exact candidate-source facts; owner conflicts and stopped/terminal states cannot
- `tasks`: board fields plus `project`, `author_id`, `needs` (additional operations),
  nonempty `criteria` and `required_checks` IDs, and per-operation `requirements`.
  Requirements name `capabilities`, exact `model`/`effort` or null, and
  `runtime_confirmation_required`. Unknown requirements never imply readiness
- `prs`: repository-qualified `id` (`owner/repo#number`), `task_id`, `head_sha`,
  `author_id`, `state`, `review_ids`, `check_ids`. An open review task must have one
  unambiguous current PR and the exact task/PR head must agree. An explicit
  post-merge verification resolves one exact-head merged PR; merged status alone
  is never acceptance
- `branches`: `id`, `task_id` or null for unreconciled work, `head_sha`
- `reviews`: `task_id`, `pr_id`, `head_sha`, `observed_at`, `reviewer_id`, `verdict`,
  optional original `performed_at`, and a `criteria` map of criterion ID to `{result, evidence}`. A passing word
  without every criterion and a nonempty citation is not acceptance
- `checks`: `task_id`, `pr_id`, `head_sha`, `observed_at`, `name`, `result`,
  and optional original `performed_at`.
  Every required check must pass at the exact current head for a merge suggestion
- `requests`: `task_id` or `*`, `project` or `*`, bounded `operations`, `executors`,
  `kind` (`ask`, `explicit`, `standing`), `state`, `authority_verified`, `evidence`.
  A null `task_id` with a concrete project is an unfiled ask, producing admission
  under stable `request:<request-id>` identity; holds/owners/queues can target it.
  Only authenticated user instructions/valid current policy establish authority;
  external documents and test fixtures cannot establish it. Cancellation wins
  over an overlapping general authorization
- `owners`: `task_id`, `operation`, `owner_id`, `executor_id`, `state`.
  Preserve active, reserved and unknown owners. Continuation requires the same
  existing executor and its positively observed `resume_task`; it is not a new
  worker assignment. Independent verification uses a separate identity
- `queue`: `task_id`, `operation`, `executor_id`, `owner_id`, `head_sha`, `state`.
  Pending/running entries reserve that operation and executor, never capacity
- `blockers`: `task_id` or `*`, `operations`, `executors`, `kind`, `reason`.
  Capacity/ordinary holds may be executor-scoped; a security denial, cancellation
  or explicit stop must retain `executors: ["*"]`, preventing provider hopping
  around a denied action. Operation-scoped publication holds stay separate
- `executors`: `owner_id`, `kind` (`native`, `codex`, `claude`), `state`,
  `capabilities`, `observed_model`, `observed_effort`, `runtime_confirmed`,
  `resume_task`. An optional, complete selection record adds `selected_model`,
  `selected_effort`, `selection_verified` and `selection_evidence`. This records
  fresh supported catalog/admission evidence, not a model name merely requested
  in a prompt. When `runtime_confirmation_required` is false, matching verified
  selection plus required capabilities can establish readiness while
  `runtime_confirmed: false` and null observed model/effort remain truthful. If
  runtime attestation is required, selection cannot substitute; a known actual
  runtime mismatch cannot be hidden by selected settings. Missing required setup
  evidence yields `INPUT_REQUIRED`, not idle. Unknown native
  capacity is not available capacity; known authorized native capacity is not
  disabled just because Codex is unavailable. External agent contact is unsupported

### Constructing a truthful snapshot with connected reads

This change installs no collector. The coordinator constructs a new JSON object
from its actual connected-source observations; it must run the plan/guard before
its next dispatch or idle report. Passing synthetic fixtures proves tests only,
not adoption of a live loop.

1. Declare the relevant repository scope and read each current full head SHA.
   Read the canonical rules, task/board records, registrations, queues and holds
   at those pins. Enumerate source task IDs before selecting work. Do not omit
   completed/blocked/owned records that are needed to explain known tasks.
2. Use connected GitHub reads to enumerate branches and open PRs through the last
   page, plus each known task-linked closed/merged PR needed for reconciliation.
   Read candidate task files at exact branch/PR heads, PR authors/current heads,
   complete review lists and required check results. Keep all returned task/PR/
   review IDs in the receipt before normalizing candidates. Copy immutable full
   SHAs rather than a title, short SHA or PR-body description.
3. Read the ownership registry and currently available worker/session observations,
   including native work, reserved owners and pending operations. An old empty
   watchdog ledger is not evidence that outside workers are absent. Record
   actual observed native capacity and tools. For a supported native selection,
   copy its verified catalog/admission model and effort into the selection fields,
   cite that observation, and leave runtime identity unconfirmed when unexposed.
   Carry current authenticated asks/authorizations and all stops/denials into
   their separate tables without broadening the authorized action or audience.
4. Record the UTC read time and returned IDs/counts for each constituent source.
   Build each repository/table receipt from those reads: `ok` and `exhausted`
   only when every required constituent succeeded and pagination ended. If any
   required part is unavailable, retain observed IDs and use `partial` or
   `unreadable`; do not fill an empty successful receipt. Never use the test-only
   `coordinator_seal` helper as proof of external completeness.
5. For review/check evidence, preserve the source's original execution/submission
   time in `performed_at` when known. Refresh `observed_at` only after freshly
   retrieving the immutable result and checking its current PR/head applicability.
   Old evidence does not require a rerun just because it is old; old observations
   cannot authorize a merge. Do not rewrite an original performance time.
6. Save this newly constructed object to an ordinary private input file, run the
   supported command above, and resolve the reported missing inputs without
   changing true facts to make it pass. Select one action, refresh observations,
   then run the guard with the selected receipt and exact target. A receipt from
   a different input, owner, head or expired read cannot be reused. Leave live
   state/queues unchanged; any actual authorized assignment is a separate action.

A scope-bounded `IDLE` result must be reported with its repository coverage and
blockers. It is never a claim that all the user's projects, unknown external
sessions or undeclared sources have no work.

### Gates, guarantees and limits

[SCRIPTED: watch.py coordinator-plan] Operations are distinct: `admission`,
`implementation`, `verification`, `upload`, `merge`, `deploy`. Open engineering
work, unfiled asks and review work are derived from accounted records, not a
caller-supplied shortlist. A task's upload/deployment hold cannot silently become
an implementation hold. Required acceptance evidence governs merge separately;
unknown acceptance-only reads do not stop separately authorized coding/admission.
Unrelated unmapped/unknown branches remain a coverage warning, but do not suppress
independently verified read-only verification at an exact open/merged PR head.
All mutation operations still require complete branch and ownership observations.
Explicit `needs: ["verification"]` on a merged task can request post-merge review;
it never restarts implementation, repeats the merge, or treats the merge as
independent acceptance. Missing exact source/readiness facts return
`INPUT_REQUIRED`, including when the rest of the inventory is complete.

Exact full-SHA task/PR/review/check facts reconcile stale ordinary board summaries.
Same-head closed/merged board or terminal PR facts require reconciliation
before an open task can restart implementation; stale source text cannot reopen
completed work. A reviewer must be independent of the task author, PR author and implementation
owner. Failed/incomplete criteria, failed checks, self-review, old-head evidence,
conflicting verdicts and missing inventory cannot produce merge acceptance.
Conflicting same-head PASS/FAIL verdicts remain an acceptance/mutation hold, but
explicit `needs: ["verification"]` can preserve an independently authorized
read-only review to resolve the dispute. That action must still pass every
source, ownership, capability and stop gate; the conflict warning stays visible.
Known exact-head merged source and its acceptance conflicts are reconciled even
when no verification operation is requested. Removing a need cannot clear a hold
or turn conflicting evidence into idle. Missing optional PR linkage does not
create a blanket upload hold; each operation retains its own source requirements.
No reconciliation clears an explicit hold. Shuto stays frozen, NEON paused,
`td-054` no-redispatch and preservation PR `#253` never-merge remain enforced.
Deployment is always directed to the separate explicitly requested release flow;
this adapter cannot authorize or execute it. Actual uploads still require the
approved payload/destination and existing transmission checks.

Each action binds task, operation, executor, owner, repository, full candidate
SHA, authorizing record IDs, canonical input digest and expiry. A changed input
invalidates a prior receipt, even if a human thinks the change is harmless.
The guard is a recheck, not an atomic lock: external changes after checking still
require normal ownership/target verification immediately before action.

The collector is a trust boundary. Schema/accounting validation cannot prove a
caller disclosed every external conversation, supplied authentic evidence, or
inspected a citation's contents. A review record is admitted only after its
independent reviewer actually checks the evidence; this code checks the record's
coverage and binding, not the screenshots themselves. The guarantee covers the
supplied validated facts and declared source scope, not every external scheduler
or browser agent. No live collector/dispatcher is installed by this change.

### Retired routes

[SCRIPTED: watch.py dispatch-guard] Historical admission producers and consumers
now return `INPUT_REQUIRED / RETIRED_UNGUARDED_ROUTE` before any I/O, through both
CLI and imported command functions: `gate`, `check-done`, `classify`, `decide`,
`nudge`, `resume`, `rebrief`, `failover`, `failover-undo`, `register-worker`,
`assign`, `liveness`, `queue-action`, `adopt-orphans`, `classify-report`,
`sibling-check`, `entry-start`, `pending-validate`, `validator-dispatched`,
`ship-verify`, `publish-verify`, `audit-task`, `validate-task`, `transitions`.

Do not deliver entries from the old queue or run the historical scheduler,
`push_code.py`, or browser dispatch instructions. They are not converted into a
new automatic dispatcher. Existing state/ledgers remain untouched. Other old
read/ledger helpers and pure state-machine functions remain for historical
compatibility, not as supported admission or acceptance APIs. This runbook's
supported route supersedes the old merge-on-build, blanket all-blocked failover
and unconditional browser-handoff procedure, preserved in
[the prior runbook](https://github.com/doublehidenblade/game-dev-central/blob/3c1481b699098103ccc073c0c358a6d1beab3dbd/project-management/watchdog/RUNBOOK.md).

### Offline verification

Run from the repository root:

- `python3 project-management/watchdog/test_rules.py` — legacy pure regression
  cases plus the coordinator suite (Pillow needed by legacy image tests)
- `python3 -m unittest discover -s project-management/watchdog -p test_rules.py -v`
  — coordinator suite only, standard library
- `python3 project-management/watchdog/test_coordinator_review.py` — unchanged
  32-assertion independent correction/adoption probes, including the two new
  failure classes. Kept separately from the author's regression methods
- `python3 project-management/watchdog/test_coordinator_acceptance_isolation.py`
  — independent 14-case acceptance-versus-review matrix for open and merged PRs
- `python3 project-management/watchdog/test_coordinator_final_guards.py`
  — independent 15-case source, stop, ownership and operation-isolation probes
- `python3 project-management/watchdog/test_coordinator_operation_needs.py`
  — independent 128-case open/merged × all needs subsets × clean/conflicting
  acceptance matrix
- `python3 project-management/watchdog/test_coordinator_hold_invariance.py`
  — independent two-case proof that removing verification cannot erase a hold

The acceptance-isolation and final-guard probe sources were restored from their retained exact review text
after the review workspace was replaced. Rerunning them against the retained v3
head reproduced the original 2/14 and 1/15 failures before this correction; their
restored source bytes are committed unchanged here. They are synthetic regression
evidence, not a live coordinator inventory or independent acceptance of v5.

The new suite denies filesystem access except supplied in-memory CLI reads,
network, subprocesses, state/queue/ledger helpers and legacy verdict capture.
It asserts no input mutation, tests actual CLI/imported aliases, and replays
scoped holds, task rotation, ownership, admission/review, incomplete manifests,
exact-head acceptance, denied routes, requested-versus-observed setup and replay
invalidation. Test-only clocks/fixtures are never live dispatch evidence.

## Evidence-feedback policy integration (2026-10-09)

Read [EVIDENCE_POLICY.md](EVIDENCE_POLICY.md) before constructing an admission or
completion packet. The coordinator independently supplies current authority,
complete canonical rule inventory, task/source scope, ownership/stops and
actor-observation receipts. Worker submissions do not establish authority.
Raw Git commit/tree/blob objects prove immutable artifact membership.

Use `watch.py brief-check --authority <file> --submission <file> --objects <file>`
for admission and `watch.py acceptance-check` with the same arguments for
completion. `evidence-check`, `evidence-checks` and `validator-check` use the
same completion result; exit 2 is missing input, exit 3 is a denied/stopped gate.
No positional/header-only or filename-only route grants acceptance.

Include each task's `{authority, submission, objects}` packet in
`snapshot.evidence_policy[task_id]` before coordinator implementation/upload or
merge decisions. All PR396 source/permission/owner/stop/operation guards remain.
Missing/conflicting completion evidence must not suppress independently
permitted read-only verification; it still blocks acceptance/merge. An unfiled
ask's admission action is registration only, not production implementation.
No workflow dispatch, deployment, external contact or queue/ledger write follows
from a policy result. Explicit human visual/device judgments stay separate.

## Timeout discipline (2026-10-09)

A timeout of the coordinator's own run never waives independent acceptance.

Incident: 2026-10-09, the 11:42 UTC watchdog run timed out and merged PR #610
(td-247 harness + trace evidence) with no validator pass. The post-merge
retro-validator verdict (#613) could not retroactively satisfy the pre-merge
gate, and its all-PASS verdict was overbroad — the per-tick trace lacked the
required source-SHA/Godot/build provenance header — so td-247 had to move back
to in_review for the provenance gap (dot timeout-gate reconciliation,
game-dev-central#358 comment 6085103271).

Rules going forward:

- On a timeout, keep the pending operation BLOCKED and proceed to another
  independently ready task. Never merge first and reconcile later.
- Evidence-only merges are not exempt from independent acceptance.
- Retro-validation is a repair/reconciliation route, never a substitute for
  the pre-merge gate; record that honestly in the task's evidence list.
- Per EVIDENCE_POLICY.md, a gate receipt (authority/submission/objects refs)
  is recorded before every merge decision; the absence of a receipt is itself
  a stop condition.

## Duplicate dispatch after timeout (2026-10-09)

Incident: the 11:42 UTC watchdog run timed out before recording its td-246
worker dispatch. The supervisor, seeing no branch and no record, dispatched a
second td-246 worker. Both workers completed independently: PR #618
(fix/td-246-bust-speed-production) and PR #619 (td-246-bust-evidence, merged
17:15:03Z). The td-246 validator merged #618, which overwrote #619's
`td246_bust_run.log` and task file; it repaired by restoring #619's log as
`godot/qa/td-246/td246_bust_run_619.log`, independently verified both evidence
sets (all criteria PASS under both), and cited both in the verdict
(docs PR #621, 08b03939). No game code was ever at risk (both evidence-only);
nothing was lost.

Rules going forward:

Rules going forward (reconciled 2026-10-09, dot game-dev-central#358):

- A dispatch is not real until it is recorded as a *receipted* admission: the
  authorized route is `watch.py coordinator-plan --snapshot <fresh.json>`
  (see "Supported coordinator route" above), one selected action re-validated
  with `watch.py dispatch-guard --snapshot <fresh.json> --decision <action>`,
  and the decision + dispatch-guard receipt (task, operation, executor, owner,
  full head SHA, UTC timestamps) appended to the coordinator log. The legacy
  `register-worker` and `state-push` admission routes are RETIRED (see
  "Retired routes" above) — do not require them, do not execute them, and do
  not write RUNBOOK instructions that presume them. A dispatch recorded only
  in a scheduler's local memory (or lost to a timeout) has no standing.
- If a run times out before its dispatch receipt exists, the next run assumes
  *unknown* dispatch state and checks actual live state BEFORE any
  re-dispatch: live branches (exhaustive pagination, filtered by task prefix),
  `pulls?head=<branch>`, recent task-file commits, and open PRs. Never
  dispatch a replacement on "no branch seen" or "no record" alone when the
  previous run may have dispatched silently. A dispatch receipt with a live
  branch or open PR is proof of life; its absence is unknown, not idle.
- Heartbeats are a second positive signal, never a death sentence: Craig's
  liveness rule — absence of heartbeat is insufficient to duplicate; a worker
  that IS heartbeating must never be duplicated. Only actual
  session/branch/receipt checks decide lost vs. unknown; never duplicate on
  heartbeat absence alone. (The 2026-10-09 wording "presumed lost after 30
  minutes without heartbeat" is struck.)
- When a duplicate mergeoverwrites a sibling's evidence, restore (never
  delete): keep both evidence sets, verify both, cite both.


## Task-scoped source coverage (isolated repair, 2026-10-09)

The existing `coordinator-plan` / `dispatch-guard` route accepts an optional
`scoped_source` object in the same snapshot. This repairs a source-accounting
circularity: an independently safe filed-task operation need not normalize every
historical task or infer current liveness for every old branch. It does **not**
waive acceptance, current rule acknowledgment, real required checks, ownership,
user stops, denied routes or publication policy. No collector or dispatcher is
installed. Craig's exception admitted only the isolated repair itself.

### Supported scope and honest limits

- Version 1 supports one exact filed-task `implementation`, `verification`,
  `upload` or `merge` operation with one current open/draft PR and candidate
  branch. Unfiled-ask registration, post-merge review and deployment retain the
  existing routes; they cannot be smuggled through this scoped schema.
- A successful scoped action leaves `source_scope.global_coverage: unknown` and
  a visible coverage warning. No scoped-only snapshot can yield global `IDLE`.
  Incomplete global source receipts remain incomplete; do not reseal them as
  complete just to obtain an action.
- Raw branch and open-PR inventories must still be exhaustively enumerated for
  every declared repository. Their full SHA inventory is retained even when
  historical tasks are not normalized. This is bounded *normalization and
  liveness*, not permission to search only a task-name prefix or hide a sibling.
- Normalize only the target in `task_ids`. Multi-task prerequisite graphs fail
  closed in this first version: complete canonical/transitive source proof is
  not implemented, so an owner-free status word cannot imply readiness. Other
  related identities, including a canonical `parent_task` and selected board-row keys,
  must appear in `related_task_ids` for ownership/stop queries. A parent relation
  alone does not assert a completed prerequisite. Canonical `depends_on` and
  `dependencies`, when present, must be empty string-ID lists; a nonempty graph
  or unsupported shape requires canonical/transitive reconciliation outside this
  scoped-v1 route. Source-file dependency/owner regions remain protected.
- Source/dependency/owner-region closure is an authenticated collector and
  independent-review responsibility. The code proves candidate diff coverage,
  named canonical source paths, current rule pins and Git exclusions, and rejects declared
  prerequisite graphs it cannot prove;
  it cannot discover an undisclosed semantic dependency or external session.
  Unknown relevant scope, inability to perform the exact queries, or an
  unresolved owner/queue reservation is a blocker, not an empty successful read.
- Existing source/owner/state guards are retained. Relevant prerequisite
  task/board ownership, unfinished/unknown states, conflicting rows, owner
  records, queued work and holds cannot disappear behind a branch exclusion.
  Branch ancestry is evidence about source bytes, never proof of worker death.
- Table-row scoping is conservative. It supports unique simple first-cell IDs
  in header-led pipe-row blocks, including this board's historical blank-
  separated row blocks. Candidate row keys must exactly equal its real row
  delta. All non-row bytes, each row's context anchor/order and regular-file
  mode are retained. Duplicate IDs, header/context edits, row moves/reordering,
  table creation/deletion or unsupported formats fail closed. There is no
  blanket documentation exemption. Use whole-file scope when appropriate.

### Scoped object contract

Keep the normal version-1 snapshot, its relevant normalized tables and its
truthful global `sources`. Add one `scoped_source` with exactly:

- `version: 1`
- `binding`: exact `task_id`, `repository`, `operation`, `executor_id`,
  `owner_id`, `head_sha` (all SHA values are full lowercase 40-character IDs)
- `base_heads`: exactly the snapshot repository map and current evidence-policy
  `rule_heads`, including cross-repository rule authorities
- `task_ids` (exactly the target), `related_task_ids`: identities described above
- `regions`: `{repository, path, row_keys}` objects. An empty `row_keys` means
  the entire exact file; a trailing slash means an entire directory. Nonempty
  row keys require an exact file. Include every candidate changed path, the
  canonical task, every canonical evidence source path and all additional
  relevant dependency/owner regions. Canonical rules are independently verified
  current-base authority pins, not automatic write/dependency/owner regions.
  Include a rule path here if the candidate writes it or actually depends on
  its file contents as source; every explicitly listed region stays protected.
  Rules/tasks cannot use row exclusion
- `candidate`: `pr_id`, `branch_id`, `fork_sha`, `base_chain`, `head_chain`.
  The chains go from current base and candidate head to the same proved
  ancestor. Every listed parent edge is verified from hash-checked raw commits
- `inventory`: `branches` and `prs` arrays. Each item has `id`, `repository`,
  `head_sha`, `proof`; PRs also have `branch_id`, `author_id`. Use repository-
  qualified branch IDs. PR IDs retain `owner/repo#number`. Every PR head branch
  must be observed at the identical head; every current base must be represented
- `receipts`: scoped collection receipts below
- `objects`: the existing raw Git object representation used by evidence policy
  (`repository -> SHA -> {type, base64}`). Missing objects never mean absent
  files. All inspected objects are content-hash verified

Inventory proof variants are deliberately not `unrelated: true`:

1. `{"kind":"candidate"}` only for the exact selected branch and current PR
2. `{"kind":"base_ancestor","chain":[...]}` proves the source head is already
   contained by the current base, including the base itself
3. `{"kind":"candidate_ancestor","chain":[...]}` can account for an older
   branch contained by this candidate; never an overlapping open sibling PR
4. `{"kind":"disjoint","fork_sha":"...","base_chain":[...],"head_chain":[...]}`
   proves the fork and computes a complete Git tree diff. Every relevant region
   must be unchanged by that delta, or its entire relevant result must already
   equal the current base (accounting for an already-contained squash result).
   Unknown/overlapping source stays blocked; labels and task-name prefixes do
   not establish disjointness

The candidate's protected source dependencies must also be unchanged between its
fork and current base, or exactly equal its reviewed candidate. Canonical rule
pins outside those regions are checked at their actual current base membership;
the unchanged evidence-policy gate requires current acknowledgment and applicable
independent evidence. A merely proposed rule change on a different branch does
not change the current authority. For example, PR143's four rule-document edits
need not block a docs-only task that does not write or depend on those files as
source. A candidate rule edit must be included as a protected region, and any
explicit rule dependency receives the same overlap/divergence checks as other
source. This does not exclude owners, queue reservations, wildcards or holds:
the complete relevant region/identity queries and all receipts remain mandatory.
Full-file equivalence includes Git file mode, not just blob bytes.

### Opt-in v2 runtime composition and foreign historical context

Version 1 and snapshots without `scoped_source` keep their existing behavior.
Version 2 keeps the same operation limits, complete raw inventory, protected
regions, strict candidate diff and evidence/ownership/publication gates. It adds
exactly `composition` and `context_assessments` to the scoped object, and `target`
to `candidate` and the selected raw PR. It does not install a collector or grant
permission to act from a fixture or a successful unit test.

- `base_heads`, snapshot repositories, rule membership and the genuine ACK
  remain pinned to current canonical rule heads. They never become the runtime
  target. `composition` contains `repository`, `target_ref` (full `refs/heads/...`),
  `head_sha`, `request_id`, `designation_ref`. The canonical task and its candidate
  artifact must both contain an identical `runtime_composition` object with the
  first four fields. This is an explicit per-task opt-in, not an inferred base.
- The actual selected PR `target` is `{repository, ref, head_sha}`. Collect its
  real current base ref and branch head, including an exact raw branch entry
  identified as `repository:refs/heads/...`. A same-SHA different ref, retarget,
  moved/deleted target or candidate-as-target is rejected. The candidate fork
  must equal the composition head and its verified parent chain must include
  the implementation head. For this repository only, all source comparison and
  containment proofs use the designated composition; current main is still
  included in the complete inventory and genuine protected conflicts block.
- The named request must independently authorize this exact task, operation
  and executor. A wildcard executor alone is insufficient. `designation_ref`
  cites a raw Git JSON decision with exactly `kind: runtime-composition`,
  `task_id`, `actor_id`, `performed_at`, `binding` (the exact scoped action),
  `composition` (the task's four-field descriptor), `candidate` (PR ID, branch
  ID and target), `request_digest`, `decision: DESIGNATED`, and `rationale`.
  Exactly one matching designation is accepted.

Foreign **row-region** source only may additionally use a context assessment
when the strict row parser cannot prove disjointness. Candidate/dependency row
parsing, whole-file conflicts, modes, absent objects and unsupported prerequisite
graphs receive no relaxation. Both foreign fork/head leaves must be regular,
same-mode, hash-proved UTF-8 files with no protected row identity anywhere in
either blob, including recognized encoded/ambiguous forms. Literal ID absence
alone never proves that a paragraph is unrelated: a global stop or shared-owner
change can apply without naming the task.

`context_assessments` is a unique list of exact Git citations. Each assessment
has exactly `kind: foreign-row-context`, `task_id`, `actor_id`, `performed_at`,
`binding`, `spans`, `identity`, `decision: OUTSIDE_SCOPE`, and `rationale`:

- `binding` is the complete `context_binding(...)` value: action, current rule
  heads, composition, protected/related identities and regions, plus exact raw
  source kind/ID/repository/branch/head/fork/comparison-base/before-commit/path
  and both file modes/blobs. Branch and PR entries need their own assessments.
  Its `owner_closure` also binds current normalized task author/owner, authenticated
  authority owner/principals, relevant normalized tasks/board, every relevant
  owner reservation, queue and blocker row, selected executor and raw PR authors.
  A same-head owner transfer or changed reservation invalidates the judgment;
  resealing collection receipts or rerunning review cannot refresh its meaning.
- `spans` must cover every changed line span returned by `context_spans(...)`,
  with exact zero-based half-open line bounds and digests of both line lists.
  Each span adds a nonempty `rationale` and `effects` containing exactly `task`,
  `dependency`, `owner`, `global_stop`, all explicitly `outside_scope`.
- `identity` contains `classification: unambiguous_foreign` and a nonempty
  rationale. An independent person/agent must actually inspect all changed
  context and its applicability/closure. The code validates the authenticated
  judgment's source, coverage and schema; it does not infer semantics with NLP.
  Unknown or ambiguous context must be reported as such and remains blocked.

Both decision kinds use the existing authenticated `authority.attestations`
channel: `kind: decision`, exact `ref`, `actor_id`, `observed_at`, nonempty
`provenance`, and `binding: {kind: <decision kind>, digest: <ep.digest(record)>}`.
The actor must be the authenticated coordinator or independent reviewer, never
the author. A worker-supplied artifact or provenance string cannot authenticate
itself. The collector must inspect all matching assessments, not select a
convenient PASS: duplicates/conflicts, unselected current assessments, applicable
or unknown effects fail closed. Every selected assessment must actually be used.
Structural source identity is matched before outer kind/task labels; a conflicting
or unknown envelope cannot hide a matching blocking assessment.
Judgments cannot postdate their observations; observations expire after fifteen
minutes. All new inputs and decision contents are bound by the ordinary input
digest, scope digest and dispatch guard. The earliest observation limits expiry.
Independent review artifacts may live on a separate proof commit; do not put an
artifact-tip-bound designation inside that same tip and invent a circular hash.

The scoped query includes composition, actual PR target, assessment citations and
`include_complete_foreign_context_and_applicability: true`. Current complete
owner/queue/global-wildcard-stop queries remain required even for contained or
context-excluded source. See the inline `RuntimeCompositionTests` fixtures and
`fixtures/scoped-runtime-base/README.md` for offline reproduction and limits.

### Actual scoped collection receipts (both versions)

For each required table in every declared repository, provide one receipt with:
`id`, `kind`, `repository`, `source_repository`, `ref_sha`, `observed_at`,
`read_status`, `pagination`, `ids`, `query_digest`, `inventory_digest`,
`records_digest`, `provenance`.

- Perform the exact query represented by `scoped_admission.query(scope)` against
  every relevant constituent. It includes all related task identities,
  prerequisite identities, protected regions, global/wildcard holds and all
  target-owner/target-executor reservations anywhere. The binding retains the
  operation. Do not omit an unknown branch/session/owner or scope a provider
  denial down to one provider. Read-only verification retains its original
  independent-identity requirements
- In `provenance`, identify the actual authenticated sources, their coverage,
  how relevant identities/regions were resolved, and what was inspected. A
  receipt's existence or a fabricated provenance string is not authentication.
  Incomplete/unreadable queries must remain blocked. Source collection and
  identity attestation are the same explicit trust boundary as evidence policy
- `ids` equals the complete raw inventory for branches/PRs, or the complete
  relevant normalized inventory for other tables. Record actual pagination:
  positive `pages_read`, exact `items_seen`, `exhausted: true`, `read_status: ok`
  only after all constituents succeeded. Every relevant record must be retained
- `query_digest` is the canonical digest of that exact query. `records_digest`
  binds the table's normalized records for the receipt repository.
  `scoped_admission.inventory_digest(snapshot, coordinator.TABLES)` binds the
  complete raw inventories, normalized record IDs and collector/source
  identities. The scope and input digests also bind all timestamps and results.
  These helpers calculate hashes; they **do not** collect observations or prove
  coverage. Never use the test-only `seal` helper for a real decision
- Receipts and individual review/check observations must be genuinely retrieved
  within 15 minutes; original performance times remain unchanged. Exactly one
  current trigger policy per repository is required. A second contradictory
  policy cannot be ignored in favor of a safe-looking first row

Malformed scoped input fails the whole scoped request closed; it never falls
back to legacy mutation admission. Existing snapshots without `scoped_source`
retain their prior behavior. All supported aliases and initialized imported
`watch.cmd_*` callables use the same evaluator. Decisions additionally bind
`source_scope_digest` and `source_inventory_digest`. Revalidate using the usual
exact-target `dispatch-guard`; any changed input/receipt/base/head invalidates
an old decision. This remains a recheck, not an atomic distributed lock.

### Module bundle, private inputs and reproduction

Use the repository's complete matching module bundle: `watch.py`,
`coordinator_cli.py`, `coordinator.py`, `scoped_admission.py`, `evidence_policy.py`.
A copied historical standalone `watch.py` does not gain these commands through
a documentation update. At module initialization, canonical `watch.py` wraps
supported/retired `cmd_*` names, and its CLI dispatch selects the same adapters.
Reading an old function body alone misses those wrappers. `review-sweep` remains
a supported read-only alias; retired liveness/transitions/admission routes stay
quarantined. This repair does not modify anyone's private copy or install sync.

Keep actual session, queue, ownership and authority observations in private local
inputs. Do not commit them or an actionable decision receipt. Published fixtures
must be synthetic or bounded already-public source evidence with explicit limits.
The fixtures here include a real immutable PR430 documentation packet replay
inside synthetic surrounding collection; that proves interoperability only.
Its current-rule stale-acknowledgment control still fails. It does not authorize
a current docs merge or claim any game/runtime/visual check.

Additional local commands (no GitHub Actions):

- `python3 -m unittest discover -s project-management/watchdog -p test_scoped_admission.py -v`
- Existing 37 coordinator methods, 53 evidence-policy methods, full legacy
  `test_rules.py`, and all five standalone independent probe scripts above
- See `fixtures/scoped-admission/README.md` for immutable real-source provenance,
  local-input replay and the recorded failing-original/positive controls

## Additive td-236 and td-237 components (2026-10-10)

Craig prioritizes bounded gameplay workers before new retry/resource enforcement.
This is a source-only **conditional admission proposal**, not runtime activation
or full-task acceptance. One central author owns these board/runbook amendments;
the two source-document authors do not write shared central files.

| Task | Sole component author | Distinct reviewer | Exact Tokyo source-admission PR/head |
|---|---|---|---|
| td-237 | dot-td237-itinerary-author | dot-td237-itinerary-reviewer | Pending coordinator relay; no acceptance inferred |
| td-236 | dot-td236-briefing-author | dot-td236-briefing-reviewer | Pending coordinator relay; no acceptance inferred |

**Allowlist, new files only.** td-237:
`godot/scripts/lower_city/navigation_itinerary.gd`,
`godot/scripts/lower_city/navigation_route_adapter.gd`,
`godot/scripts/lower_city/mission_navigation_adapter.gd`, matching `.gd.uid`
files only if generated, and `godot/qa/td-237/itinerary/**`.
td-236: `godot/scripts/lower_city/gig_briefing_view.gd`, its generated
`.gd.uid`, and `godot/qa/td-236/briefing/**`.

**Activation and precedence.** Each component activates separately only after
the coordinator records its exact source amendment PR/head, independent exact-head
acceptance and required merges of that canonical Tokyo amendment and this central
admission, and fresh owner/source/tier/tool preflight. Missing/changed pins,
denials or unresolved overlap hold that component. Once those gates pass, this
grant supersedes inherited no-author/documentation-only clauses for that additive
allowlist only; unchanged scope needs no repeat registration. Source-document
authors already working are not evidence of runtime activation. Full-task status
stays blocked; td-236 criteria 1–8 and td-237 criteria 1–10 remain unchanged.

**Runtime pin.** Use Tokyo PR545 `e8bdfc0ff742d7b3cd4a86a213c3369d555e7027`
for read-only contract fixtures (verified head of an open PR, not a merged/live
build). Re-hash CityData `55dcf8012fdbd317b74bd27a0d3c84d80296b61d`,
CityRouter `815b6c88d71dc26afdd1b76db1258c4eab983ff2` and
GigDispatch `e66b4656d38814b6bcc4fba971ac3cc034538ae6` before tests.
Source publication adds only allowed files to the admitted source-doc base;
do not replace main or merge historical runtime ancestry into main.

**Boundaries.** No existing runtime file edits, production mount, autoload,
scene or project-setting changes. MapSheet/minimap/PaperMap/gig_menu, td-235's
target region, td-232/PR550 payout, PR549 fit, td-215 status, td-200/201 inventory,
mission/fuel/damage providers and Craig's td-185 assembly authority stay with
their owners. Production wiring requires exact owner handoff and separate
integration admission. Preserve all old mission-cue files/evidence and its
publication hold; no retry of denied cue/td-231 publication or alternative route
to change the denied automation. Shuto frozen; NEON paused.

**Component acceptance, independent exact head.** td-237 proves one revisioned
itinerary, real directed route/layer geometry, immutable mission-stop order,
stale-revision Apply/Cancel, once-only custom arrival, duplicate/stale mission
events and zero mission/economy writes. td-236 proves authoritative offer/value
fidelity, explicit accept intent, stale/expired selection rejection, truthful
unavailable data and single-itinerary revision consumption; selection/preview
never accepts a gig. Its fixture may use a documented snapshot while the accepted
td-237 interface is pending; that is not production interoperation. No invented
history, inventory, condition, repair destinations or route segments.
For each: diff/UID checks restrict changes to the allowlist, raw failures and
broken-case controls are retained, and a separate reviewer verifies source and
claimed evidence. Native rendered briefing pixels require actual inspection;
full-scene/browser/CSS-DPR/phone gates stay open. Author stops at source/evidence
PR and never self-accepts or merges.

**Setup.** Preserve requested frontier `gpt-6-astra/xhigh` author/reviewer settings;
requested is not runtime attestation. Coordinator verifies exact-source fixtures,
Godot 4.7.2 and required renderer/pixel tools before implementation; readiness is
not established by this document. Wait for required tier/tools; no downgrade.
Each activated component retains one initial attempt plus at most one
evidence-based correction within two hours, reserving independent review time.
Stop on permission/auth denial, overlap, excluded-file need or exhausted bound.

**Documentation preflight.** Central `daf20aa79ce7ceb61440b96870752f60b79108f5` has no
`.github` workflow files. Both PR545 and Tokyo main
`f671c0745bae514d5003d090b1f536f2515854a2` lack the proposed new paths.
Current board/task/old worker registry and all open-PR metadata pages were read
(central 102, Tokyo 219); targeted searches found no competing named component
registration. This is not complete branch-region or live-session clearance;
stale registry/quiet GitHub cannot establish idle ownership. The coordinator
retains fresh scoped owner/guard checks before dispatch, and rechecks actual
workflow/publication triggers before writes. No executable changes, Actions,
merge, deployment, external-agent contact, credential/security change or
retry/resource-enforcement work is authorized by this documentation.
