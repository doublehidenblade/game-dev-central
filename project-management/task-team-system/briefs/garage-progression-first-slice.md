# Garage progression: first-slice execution brief

> Planned 2026-10-07 by dot. Documentation and task filing only; all execution stages remain blocked until their gates and runtime admission are evidenced.

## Authority and ownership

Craig: “Make sure its on the GitHub, instead of just local, with the task (you can create tasks). Then assign to workers. But you prob need mocks before going straight into 3D? No need to get me to review. Full steam ahead.”

This opens the new garage work under dot. It does not take over the wider coordinator role or any Muse/Claude task. The latest request removes a mandatory pause for Craig's design review: use an independent mock/layout review before 3D. Do not confuse that with proof of actual-world or physical-phone acceptance.

- Design authority: [garage-progression.md](../../../game-design/garage-progression.md)
- Canonical task truth: game-repo `godot/docs/tasks/td-197.md` through `td-202.md`, proposed on `tasks/td-197-202-garage-progression`
- Status authority: [Tokyo board](../../boards/tokyo-drift-3d.md); new rows only, via PR
- Read [SYSTEM](../../rules/SYSTEM.md), [worker brief](../../rules/WORKER_BRIEF.md), [visual brief](../../rules/VISUAL_BRIEF_TEMPLATE.md) and [standing rules](../../../knowledge/standing-rules.md)
- Current inspected game main: `58516c0dcdbadbbc360b051015ba215057995911`; central base: `943b2d518bd601bb45dea7621f5128a0546bedf3`. Recheck before any implementation
- Muse police/traffic/pedestrian/arrest tasks td-188–196 and Claude/Opus gigs/Lower City/Asset Forge td-185/186 retain their owners. An open PR, stale registry or board row is not proof of merged interface or a live session
- No external-agent contact, takeover, merge, deployment, auto-merge or GitHub Actions dispatch/rerun. No worker is marked active merely because its task exists

## Dependency-ordered tasks

- [td-197: Garage reference mocks and measured layout gate](https://github.com/doublehidenblade/tokyo-drift-3d/blob/tasks/td-197-202-garage-progression/godot/docs/tasks/td-197.md). Depends on: confirmed runtime plus reference/site access. Owner: dot; execution worker unassigned.
- [td-198: Driveable garage graybox in the actual Lower City](https://github.com/doublehidenblade/tokyo-drift-3d/blob/tasks/td-197-202-garage-progression/godot/docs/tasks/td-198.md). Depends on: td-197. Owner: dot; execution worker unassigned.
- [td-199: Garage entry, shutter and police shelter contract](https://github.com/doublehidenblade/tokyo-drift-3d/blob/tasks/td-197-202-garage-progression/godot/docs/tasks/td-199.md). Depends on: td-198. Owner: dot; execution worker unassigned.
- [td-200: Atomic garage inventory and fixed supplier first loop](https://github.com/doublehidenblade/tokyo-drift-3d/blob/tasks/td-197-202-garage-progression/godot/docs/tasks/td-200.md). Depends on: td-199. Owner: dot; execution worker unassigned.
- [td-201: Phone workshop UI and prerequisite-aware discovery](https://github.com/doublehidenblade/tokyo-drift-3d/blob/tasks/td-197-202-garage-progression/godot/docs/tasks/td-201.md). Depends on: td-200. Owner: dot; execution worker unassigned.
- [td-202: Independent garage first-slice integration validation](https://github.com/doublehidenblade/tokyo-drift-3d/blob/tasks/td-197-202-garage-progression/godot/docs/tasks/td-202.md). Depends on: td-197, td-198, td-199, td-200, td-201. Owner: dot; execution worker unassigned.

The initial planning rows use the valid status `blocked` with exact reasons, not an invented active/planned status. Runtime admission means a confirmed worker in a suitable environment for its required tools, one task per worker, no duplicate live owner. On admission, record real identity/time in its own board row and registry; do not invent those here. Standalone art-direction preparation does not satisfy measured-layout, 3D, implementation or runtime admission.

td-197 → td-198 → td-199 → td-200 → td-201 → td-202 is the acceptance order. Contract reading and fixtures may be prepared earlier, but dependent implementation cannot bypass a gate. td-199 also waits for authoritative police signals; td-200 for settlement/load contracts; td-202 for two actual capability-consuming gig variants from their current owner. Do not quietly expand garage scope to fill an unavailable owner dependency.

## Scope ceiling

First slice: one actual drivable home and working shutter; safe drive-in/park/drive-out; police sight-gated shelter without heat wipe; contextual phone/controller UI; persistent wallet and atomic owned-material lifecycle; three fixed physically discovered suppliers; rack versus padded carrier; one active fitting with reversible owned swaps; visible car/shelf changes; bounded loaded handling; two real capability-consuming gig variants through the existing gig owner.

Next: refrigerator/powered station, electrical supplier and one short cold-store blueprint delivery; real second bay/side shelves plus van and one short adjoining-unit blueprint delivery. Optional timber-depot/storage-alcove beat later. These are small existing-delivery-verb beats, not new campaigns, and garage consumes rewards rather than owning story content.

Later: truck/heavy pad, further actual room expansions, animals/tanks, bounded utility layering, concealment/hazmat and broader fleet fantasy. No all-catalogue implementation, passive fleet income, free building, fuel/wear/fines stack or extra districts now.

## Contract boundaries that must stay intact

1. Vehicle progression references existing model identity separately from geometry/wheel/collider schema. Read-only capabilities include payload, usable volume, occupied/reserved load, fitting capabilities and compatible modifiers. Gig owner validates eligibility at acceptance/loading and locks live-run requirements
2. Existing settlement remains authority for gross payout, timing, condition, success and failure. Wallet credits a stable settlement ID once; bonuses never multiply twice. Chassis condition is separate from gig cargo HP
3. Police owns sight, pursuit/search, heat decay/reacquisition and recovery. Garage reports full-inside/parked, shutter state, shelter entered/left and interrupted entry. Recheck sight before opening and shelter; real door occlusion/collision must match state
4. Every pack occupies one location. Purchase/payment/load, partial unload and install consumption are atomic with idempotent IDs. Retain a previous valid versioned save. Reload during an operation never duplicates or erases paid ownership
5. Persist current job/timer/cargo, vehicle/supplies, layout/door and relevant enforcement reliably; otherwise explicit recovery uses the owning system's outcome. No offline timer decay or save-recovery heat exemption
6. Known project, prerequisite installed-ever, story blueprint, supplier physically discovered and affordable resources are separate durable states. Early discovery cannot reveal skipped tiers; swapping owned fittings cannot erase milestones
7. Three first suppliers at fixed readable authored frontages. Individual packs fit starter; client cargo and packs share mass/volume limits. Initial shelf 12 units; 24 only with actual later bay/shelving geometry. Timber is a distinct named stock variant, never hidden generic points

## Visual brief: all mandatory sections

### 0. Cost rules
No Actions runs/reruns or workflow edits. Local tests only after runtime admission. This publication runs no build.

### 1. Skill workflow injection
For production 3D modeling, follow the available `3dviz-pro-max` visual-iteration workflow (real licensed reference → labeled 2D mock → matching-angle 3D → triptych → inspect/iterate). If that skill is unavailable in the assigned checkout, report the precise missing step; do not claim compliance. Read relevant checkout `.agents/skills` and current visual research instructions.
For UI, use a state-board workflow: actual phone/game constraints → task/state map → labeled mock → real-runtime matching state captures → touch/controller walkthrough → independent review.
The measured top-down layout extracts actual road geometry and playable-car dimensions. Generated illustrations are art direction only.

### 2. Quality bar
Readable 1980s anime-Japan garage aligned to the existing art book: industrial putty/ochre, stamped steel, enamel labels, analog paperwork, warm work lights and original chunky equipment. Driveable apron/doorway and visible packs matter before decorative density. Fixed floor/door/camera relationships must agree across boards. Later expansion adds genuine floor, walls, clearance, lights, parking and visible shelves together. One short contextual cue at a time; icons plus labels, readable phone text and predictable controller focus.

### 3. Excluded shortcuts
No image mock presented as game evidence or real reference photo; no isolated beauty scene as world proof; no teleport-to-menu garage; no lock-tree spoiler catalogue; no invisible storage/vehicle slot sold as expansion; no full catalogue build. A deliberately labeled graybox is acceptable only for td-198's geometry gate, never as final art. No replacement of Forge vehicles or changed shared geometry schema to hide economy fields.

### 4. Effort calibration
This is a measured layout and iterative interaction pass followed by substantial actual-world integration, not a quick box-building script. Mocks can guide immediate work; final 3D/material quality requires reference matching and repeated in-engine inspection. Give task-specific estimates only after inspecting the runtime and exact integration interfaces.

### 5. Evidence
Central art-direction boards live under `assets/mocks/garage-progression/`; source/label limitations in its README. Task truth and engine evidence live under `godot/docs/tasks/td-NNN.md` and `godot/qa/td-NNN/` in Tokyo. Every visual criterion has same-instance/same-camera before/after captures; feature absence is labeled honestly. Commit logs, fixtures, negative controls and actual-world videos, citing full SHA. Independent reviewer opens each image. Phone-sized captures do not establish physical-phone performance or Craig's verdict.

### 6. Merge and status
Push feature branches and leave draft PRs open. No merge/deploy/Actions. Worker reports `in_review`, never `validated`. Independent reviewer supplies per-criterion evidence; a mock pass does not clear the actual-world gate. No done-pending-verdict until implementation is truly independently verified and the phone verdict is the sole remaining gate.

### 7. Standing constraints
One exclusive task per confirmed worker; no nudging/duplicating live sessions. Preserve all existing owner scopes. Same identical failure twice: stop and report evidence. Board edits via PR and own row only. Use verified free asset licenses; no purchased or ripped assets. Production modeling uses the required working toolchain; verify it instead of assuming absence. Keep credentials and secrets out of repositories.

## Actual-world acceptance checklist

- [ ] Real car fully enters/parks/leaves in both directions, empty and max legal cargo/fittings, with safe fast drive-past and no trigger teleport
- [ ] Door sweep obstruction, exterior obstruction, partial entry, cancellation, reload transition and parked interference cannot trap or clip the car
- [ ] Seen/unseen approach, nearby cop without sight, sight regained during entry/closure, closed shelter, outside search and exit reacquisition use actual police authority; no instant heat wipe
- [ ] UI close/cancel never opens shutter or auto-exposes player; workshop/refit cannot pause loaded job obligations
- [ ] Visible purchase→vehicle→shelf→once-only install; full shelf, partial unload, multiple trips and mixed client/owned cargo covered
- [ ] Reload/failure/double-click at every transaction edge proves no double payout/charge/pack and no lost ownership; zero-cash recovery stays earnable
- [ ] Hidden skipped tiers, physical fixed-supplier discovery and idempotent story rewards behave correctly after early discovery, equip swaps, failure/reload and spent savings
- [ ] First-time touch/controller loop readable; record first upgrade near 20 minutes and eligible-gig completion near 25–30, with slowest-quartile analysis
- [ ] Two real capability-consuming gig variants make both fitting choices useful; otherwise slice remains blocked
- [ ] Later expansion criterion reserved: drive into genuinely opened bay, park both vehicles, access larger real shelves and leave without crossing another car; no current claim this exists

## Publication verification

Task files and design are publication deliverables only. Empty evidence arrays and null verdicts are intentional. No tests, images, worker admission, implementation or validation are claimed by filing these specs.
