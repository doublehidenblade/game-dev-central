# td-200 foundation proposal: durable ownership before playable upgrades

> Proposed 2026-10-09 by dot. Documentation only. This is a bounded admission proposal within dot-owned td-200, not a new task number, implementation admission, runtime hook, or completion of td-200.

## Decision

Build a small, isolated, locally tested persistence/transaction core first. It can proceed independently of garage geometry because it has no scene, vehicle, supplier, UI or police hooks. It must remain unreachable from normal gameplay until the existing owners accept exact production adapter contracts. This advances the requested upgrade progression without restarting stopped replacement-truck/R4 artwork or disguising an unbuilt upgrade menu as gameplay.

Keep the existing first meaningful choice: rack versus padded carrier, one equipped fitting, durable purchased packs, free empty-vehicle swaps. Do not introduce a competing wallet, XP tree, generic speed upgrade, grant-money shortcut, new service, or second gig authority. Lower City only; Shuto remains frozen and NEON paused.

## Ownership and current state

- Parent task: [td-200](https://github.com/doublehidenblade/tokyo-drift-3d/blob/main/godot/docs/tasks/td-200.md). Existing board owner remains dot. Foundation author: unassigned; runtime admission: not granted.
- This document and only the td-200 row annotation register the *proposed* foundation scope. Neither an open draft nor this text proves owner-guard registration or another owner's handoff.
- Preserve td-197/198 geometry/mock stops, td-199 shutter/police contract, td-201 workshop UI and td-202 integration acceptance. Their dependencies and blocked status do not change.
- Existing Muse/Claude gig, damage, vehicle, police and assembly authority stays intact. dot fuel/recovery and presentation lanes stay intact. No edits or contact with those owners are authorized here.
- td-238 terminal intake is separate; no terminal file or feature belongs to this scope.

Required process: [SYSTEM](../../rules/SYSTEM.md), [WORKER_BRIEF](../../rules/WORKER_BRIEF.md), [standing rules](../../../knowledge/standing-rules.md), [selection policy](../../rules/WORKER_SELECTION_POLICY.md). Current task constraints and latest parent/user directions override historical merge/deploy language in older files.

## Exact source audit

The coordinator confirms v49 `fa081b42197d50e6adaf202f899146fbffeab725` remains the approved Lower City composition. Source main inspected at `b871e7879ce44ff16433456df72b673ae116df2c` contains newer documents but older runtime. Do not replace v49 with main or merge unrelated candidate code.

1. [FuelService at v49](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/fuel_service.gd): balance is `profile.starting_cash_yen + _gigs.earnings - spent_yen`. It explicitly describes itself as run-scoped, with no persistent save. `request_service` increments an in-memory integer `_serial`; `confirm(id)` rejects repeated IDs through in-memory `_settlements`, rechecks balance/range/arrest/location and validates a recovery destination before charging. This is a useful validation pattern, not a durable wallet.
2. [GigDispatch at v49](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/gig_dispatch.gd): `settled(gig, result)` exposes the owner's final total after timing and cargo condition; successful settlement increments `earnings`. There is no persisted run/attempt/settlement identity. `started_ms` is a process clock, not a durable ID. Retry starts a fresh run of the offer. Cargo `weight_kg` and human-readable `size` do not implement a capacity reservation API.
3. [FuelProfile](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/fuel_profile.gd): current profile identifies `starter_coupe`, starting cash ¥5,000, range 7.5 km, fill ¥1,200, tow ¥1,800, salvage ¥2,000. These are current run settings, not permission to grant ¥5,000 on every reload.
4. [LowerCity assembly](https://github.com/doublehidenblade/tokyo-drift-3d/blob/fa081b42197d50e6adaf202f899146fbffeab725/godot/scripts/lower_city/lower_city.gd): directly spawns the current coupe and FuelService. Recovery routes through existing service/mission/enforcement seams. It does not establish garage entry or a player-owned mini-truck.
5. [VehicleConfig on main](https://github.com/doublehidenblade/tokyo-drift-3d/blob/b871e7879ce44ff16433456df72b673ae116df2c/godot/scripts/vehicle-config.gd) is a handling resource, not ownership/capacity state. Never mutate its geometry/config to smuggle in a second economy.
6. [Existing design at exact PR327 head](https://github.com/doublehidenblade/game-dev-central/blob/2f138f5c2cfd703733b002008f1007fba0012694/game-design/garage-progression.md) supplies provisional rack/padded recipes and the physical lifecycle. [R4 PR355](https://github.com/doublehidenblade/game-dev-central/pull/355) is bounded reference publication, not accepted geometry. [Customization PR351](https://github.com/doublehidenblade/game-dev-central/pull/351) does not remove the runtime gates.

Conclusion: no production persistent wallet, durable settlement journal, owner-accepted shared load contract or workshop eligibility contract was established. The safe deliverable now is the isolated core below; production integration remains gated.

## Proposed implementation allowlist, after independent admission

Only new files:
- `godot/scripts/lower_city/progression/progression_state.gd`
- `godot/scripts/lower_city/progression/progression_store.gd`
- `godot/scripts/lower_city/progression/progression_rules.gd`
- `godot/tools/test_td200_progression_foundation.gd`
- `godot/qa/td-200/foundation/` documentation, fixtures and raw test evidence

Godot-generated UID sidecars for these new scripts are allowed if required. No existing runtime file, scene, autoload, project.godot, export preset, workflow, wallet/service/gig/damage/UI/vehicle file, packaging file, artwork, terminal, shared log, or another task may be modified. A scoped td-200 task amendment and its own board row may record the proposal/results through documentation PRs; they must preserve original criteria and history.

This is a *proposal*, not an expansion of any currently admitted worker's allowlist. Before author admission: independently accept this document; coordinator verifies all relevant source and central branch/PR reservations and owner state; confirm the exact v49-derived development base and compatible Godot 4.7.2 tools; approve this new-file scope; inspect that base's workflow triggers so source push/PR creation cannot run Actions. Missing preflight blocks author start. No builds, Actions, merge, deploy or external-agent contact is part of this task.

## Minimum core contract

### One authoritative state, deterministic commands

Use one integer-yen balance and one state revision, never separate spendable mirrors. The core is a pure reducer plus storage; consumers get deep-copy snapshots. It cannot read scene singletons, emit currency grants from UI, or call FuelService/GigDispatch. A future adapter passes owner-approved facts.

Version 1 state contains:
- schema version; random profile ID created once; strictly increasing generation/revision; persistent run/attempt/transaction counters
- balance_yen; migration receipt or null; applied immutable transaction receipts
- owned vehicle IDs referencing existing model identity; owned fitting IDs and one equipped fitting per vehicle
- item IDs with exactly one location: carried on a vehicle or stored on shelf; a consumed item is recorded only in the transaction receipt
- discovered supplier IDs, earned blueprint reward IDs and permanent first-install milestones
- reserved client load records supplied by the future gig adapter

Inputs are validated for type, bounded integer arithmetic, nonnegative costs/quantities, known IDs, inventory location and expected state revision. Reject malformed/unknown values, negative price, overflow, stale quote and mismatched replay without mutating state. No arbitrary set_balance, credit_any_amount or raw-state mutation API is exposed to a runtime UI.

Core operations: import_legacy_snapshot_once, apply_gig_settlement_once, purchase_packs, unload_packs, install_fitting, refit_owned_fitting, record_discovery_once, record_blueprint_once. Requests carry explicit request ID and expected revision. Each request is reduced, validated and durably committed as one snapshot before a success receipt is returned; callers cannot directly write individual fields.

### IDs and exactly-once boundaries

Proposed future IDs use persistent profile identity plus monotonically allocated counters, not timestamps, offer endpoints or payout amounts:
- run_id: profile/run sequence
- attempt_id: run_id plus attempt sequence; retries get a new attempt
- settlement_id: attempt_id plus one terminal-settlement marker, for success and failure alike
- transaction_id/request_id: profile plus transaction sequence; caller retains the same request token until outcome is known
- purchased item IDs: transaction_id plus line and unit ordinal; fitted ownership IDs are separate from loose pack IDs

Allocation itself is persisted before an owner exposes a new run/attempt to play. The existing gig owner must later adopt the IDs and own the terminal outcome. The foundation only proves this protocol with injected fixtures. There is no claim these IDs exist today.

Replay of the same ID plus identical canonical payload returns the stored receipt with zero second charge/reward/consumption. Same ID with different payload fails closed. Two attempts of the same route each legitimately pay once; duplicate delivery of one attempt does not. A failed settlement records its terminal ID but pays zero. Do not derive the payment again or apply timing/condition twice.

The future settlement adapter must use a durable outbox or include the owner's terminal outcome and wallet receipt in a jointly committed snapshot: save an immutable owner outcome, apply its stable ID, acknowledge only after commit. If that joint durability is unavailable, production credit remains disabled; a signal listener alone is insufficient.

### Save, reload, corruption and rollback

Use a two-slot versioned snapshot store inside an isolated test save directory. Each slot contains generation, schema and a hash of deterministic canonical serialized payload; the hash detects accidental corruption, not cheating/security. Write the older/inactive slot, close it, reopen and verify the whole payload before reporting success. Preserve the previous valid slot. Serialize writers; no threaded or multi-tab simultaneous writer support in v1.

On load select the highest valid generation. If only one slot validates, recover it and return an explicit recovered_previous state. If neither validates or schema is newer, fail closed with no overwrite, zeroing, default grant or deletion. Equal-generation differing payloads are corruption, not a coin toss. Bounded integers and canonical field ordering are tested, not assumed.

Crash after a complete new slot but before the success response may load the new state; replay of the same request returns its receipt. A torn slot yields the previous complete state. In-memory state must be reloaded after an uncertain disk failure before any next command. Keep a failed commit from appearing as a successful purchase in UI.

Important limit: fallback to an older save cannot independently prove that a newer acknowledged purchase or settlement never happened. Return recovery-required and freeze production economic mutation until the future owner adapter reconciles its durable outbox/receipt high-water mark. Never silently replay historical earnings or claim no-loss recovery from checksums alone. Foundation tests must expose this case explicitly.

Storage success on native disk does not establish browser durable storage. Web filesystem/IndexedDB flush acknowledgement, quota denial, tab close, reload and concurrent-tab exclusion require a separately tested web adapter before production hookup. No native-only result earns web acceptance.

### Migration boundary

No automatic migration runs in this foundation. Fixtures demonstrate a one-time explicit legacy snapshot import for a known profile/run and exact source pin. The future adapter may import the *current authoritative available balance* once, net of existing spent_yen, with a receipt and boundary cutoff. Do not add starting_cash or GigDispatch.earnings a second time. Never reconstruct past lifetime earnings from a fresh session.

Migration must occur at a quiescent owner-agreed boundary: no active gig, service quote, arrest, recovery or pending settlement; existing service economy is frozen/switched atomically with the imported snapshot. Subsequent service debits and gig credits must use the same authority, rather than continuing FuelService's arithmetic alongside a new wallet. Until the owner supplies this transition and save ownership, production migration is blocked.

New profile and developer fixtures are separate: the core defaults to zero money, no grant. If product later retains the existing starting allowance, it requires one explicit once-only new-profile migration receipt, not a reload path. A fresh ordinary earning/recovery path is a production acceptance requirement; the foundation does not claim to solve current game-over economics.

## Bounded first-upgrade model

Use the existing design's values as *fixture-only proposed rules*, not tuned production facts:
- Rack: two steel packs and one mechanical pack; ¥3,900 install balance after the ¥2,100 materials; total ¥6,000. Proposed volume 4→6 units, module mass 25 kg, same payload rating
- Padded carrier: one steel, one mechanical, one lining; ¥3,800 installation after ¥2,200 materials; total ¥6,000. Proposed usable volume 4→3 units, module mass 35 kg, delicate capability and 0.75 compatible-cargo impact factor
- Pack fixtures: steel 40 kg/1 unit/¥600, mechanical 30 kg/1 unit/¥900, lining 20 kg/1 unit/¥700. Shelf starts at 12 units; no expansion mutation
- Proposed 240 kg starter payload is not accepted against the stopped mini-truck geometry. Production must supply validated vehicle/cargo capacities and dimensions; no conversion from human-readable “20 crates” to invented units
- One equipped fitting. Buying and installing consumes only the exact shelf pack IDs plus install money once; unequipping retains fitting ownership. Refit is free but only with no carried supplies, no loaded or reserved client cargo, and no active job
- Capability snapshot is a proposal consumed by a future owner, not a mutation of physics. Padded protection applies only to compatible client cargo, not chassis, police, timers or payout. Rack adds volume, not payload. No speed/handling application in this slice

When an active fitting changes, derive effective values from immutable base plus the single fitting; never multiply already-modified values again. Count fitting mass + carried paid packs + reserved/loaded client cargo exactly once. Reject overload/overvolume before payment. Tests use explicit cargo unit fixtures because current source lacks an accepted shared unit contract.

Discovery/blueprint/first-install state is idempotent and persists independently of equipment selection. No future refrigerator, paint, van, second bay or tree is revealed by this core.

## UI and physical entry prerequisites

There is no menu, buy button, supplier spawn, new garage entry, or loaded handling hook in the foundation. Future UI must consume command results and owner facts, not manufacture “parked” or “safe” flags.

Production installation/refit requires real garage site/clearance and td-199 entry eligibility, fully inside/parked, valid shutter state where required, no forbidden enforcement/transition, current save readiness, and exact no-cargo/no-reservation conditions. Purchase requires authoritative supplier discovery/stop/location and current price/capacity; unload requires actual interior mark and shelf capacity. Revalidate immediately before commit, with owner epoch/revision to invalidate stale quotes.

Opening/closing/cancelling UI must never pause a live job timer, teleport the car, open a shutter, clear heat, lose input ownership, or apply an upgrade. Without accepted td-199/200 adapters these actions stay absent, not clickable placeholders. This is why the isolated core can be implemented before geometry, while the playable loop cannot.

## Future terminal boundary

td-238 must not gain a production money grant through this work. Fixture seeding exists only in the test harness; no production command accepts arbitrary credit, arbitrary item creation or bypassed eligibility. No terminal hook, cheat URL, environment toggle, hidden key binding or exported fixture profile is added. A future explicitly authorized debug build must use a separate save namespace/profile and visibly mark itself; its saves/receipts must be rejected by the production schema/import path. Being a debug export alone is insufficient authority to alter player saves.

## Acceptance matrix for the isolated core

All checks are local; no Actions/build/export is requested. Independent reviewer must reproduce against the exact PR head and cite raw logs per criterion.

1. C1 Scope and dependency: only admitted new files; no autoload/preload/runtime references or source authority edits; stopped assets and v49 composition untouched. Static reachability/import inspection. No claim of playable upgrade
2. C2 Money and identity: duplicate settlement/reward, retry same request, same ID/different payload, identical route/new attempt, failure/arrest result, stale revision, negative/overflow input, double-click and insufficient funds. Assert exact integer balance and exactly one receipt
3. C3 Inventory: purchase then partial unload, full-shelf failure, install then refit, reservation conflict, mixed cargo/pack load, invalid vehicle/fitting, first-install/reveal persistence. Assert every item has one location and every consumed ID is absent from loose stock
4. C4 Durability: deterministic fault injection before/after allocation, reduction, each slot-write segment, close, verification and success response; repeat request after restart. Test one/both corrupt slots, unknown schema, generation collision, read-only storage and quota-style failure. Distinguish rollback from acknowledged-loss recovery-required; no automatic regrant
5. C5 Migration and service boundary: import once, duplicate/mismatched migration, non-quiescent rejection, net-balance equality and cutoff; zero default grant. A contract fixture proves one source of balance; no live FuelService integration is claimed
6. C6 Effects and performance: derive rack/padded capacities and protection exactly once from fixture base, prove no payload increase/chassis protection/payout multiplier. Event-driven commands only, zero idle processing/scene nodes, bounded fixtures (maximum 1,000 transactions). Record command/save timings and serialized size; these are local evidence, not phone FPS
7. C7 Production lock: test-only seeds cannot be imported as production profile; no terminal/UI grant hook; all missing owner, garage and web-persistence capabilities fail closed. Enumerate unresolved runtime/web/phone tests

Negative controls must deliberately remove deduplication, atomic item movement, and stale-state rejection and cause the relevant tests to fail. No self-acceptance or green claim from parser checks alone.

## Recommended setup and stopping rule

- Capability: frontier for persistence, data-loss and cross-owner boundaries
- Provider preference: native dot route with Godot 4.7.2 and isolated filesystem tests; preserve existing owner
- Requested author: gpt-6-astra / xhigh; independent reviewer same frontier tier, separate author/reviewer
- Runtime identity and executor readiness: unconfirmed; no worker started
- Availability: catalog recommendation only; verify at actual admission
- Fallback: wait_for_required_tier; no weaker production fallback
- Budget: one initial implementation and at most one evidence-based correction, two-hour author ceiling; reserve a separate full independent review before author starts
- Escalate/stop: missing required runtime, write-safety failure, need to edit existing owner files, unknown storage semantics, source pin collision, or exhausted budget
- Outcome now: proposal only, acceptance pending, cost/usage unknown

The completion target is an accepted, tested isolated transaction foundation. Stop there. A later production adapter admission must independently establish durable gig settlement IDs/outbox, unified fuel/service balance, real vehicle/load units, save/recovery/police ownership and browser durability; physical upgrade gameplay additionally retains td-197–202 gates. This proposal does not silently approve that second task.
