# Multiplayer Lag Lessons — what actually fixed guest lag in Tokyo Drift 3D

Source: our own PRs and task files — td-093, td-095, td-102, td-104, td-120, td-121, td-129, td-131 — plus Craig's phone QA verdicts v23–v31 (2026-09-27..30).
Status: **distilled 2026-10-07** — Craig's v31 phone verdict was "improved a lot" on guest lag. td-054 acceptance still open (rail magnet td-130 unresolved; desync fixes awaiting his re-verdict).

## 0. The arc in one paragraph

Craig reported "very laggy for guest" (v22). We built a TURN relay (td-095) — still laggy. Diagnosis (td-102) showed the lag wasn't the transport at all: the owning guest waited a full round trip for its own inputs, both transports applied poses at once, and reconciliation compared against stale snapshots. Fixes landed in layers: owning-client prediction + host reconciliation (td-102), measured-not-guessed send rates (td-104), smooth convergers instead of teleports (td-121), snapshot interpolation for remote cars (td-129), and ack-aligned reconciliation + traffic dead reckoning (td-131).

## 1. Measure before adding infrastructure

Craig said "try turn server" — we built coturn beside the signaling server with time-limited credentials (td-095, PR #143). Guest still laggy. The actual causes (below) had nothing to do with NAT traversal.

Separately, Craig asked "send more frequently?" — td-104 measured the real host at **9.99/s over 74.9s** (PR #199, no code change) and closed the question with data: the send rate was never the problem.

**Lesson:** instrument first, build second. The `?mptrace=1` opt-in phone-trace pipeline (10s uploads, server-side ring buffer) is what made the v28/v29 diagnoses possible. Never add another relay layer on a hunch.

## 2. The owning client must predict; the host reconciles

td-102's core finding: the owning guest applied its own inputs only after they round-tripped through the host — every steering input felt delayed by a full RTT. **Fix:** owning-client prediction (apply your own inputs instantly, locally) with host-authoritative reconciliation (the host corrects you when you diverge). This is the single biggest feel win in the whole arc, and it is industry-standard for a reason.

## 3. Transports must be mutually exclusive

td-102 found WebRTC *and* the WebSocket fallback applying poses simultaneously — duplicate pose application from two transports. **Fix:** one active transport at a time, direct-first ICE with TURN strictly as NAT fallback, plus honest transport/candidate telemetry so you always know which path is actually negotiated. If you can't name the active path from a log line, you don't have one path.

## 4. Reconcile against the right point in history (ack-aligned)

td-131's root cause: the reconciler compared the *current* predicted pose against an *RTT-old* snapshot, mistaking systematic v·RTT staleness (~5m at driving speed) for real divergence — then "corrected" a car that was never wrong. The guest lived ~5m from authority continuously and drove into traffic it couldn't see ("air walls").

**Fix:** look up the prediction history at the *acked input's send time* and compare like with like. Banded response: <0.35m ignore, ≤1.5m snap, >1.5m converge, with history-shift on correction. Simulated 3s RTT: p95 error 2.90m → **0.15m**; air walls 47/47 → **0/47**.

**Lesson:** a reconciler that doesn't account for the age of what it compares against manufactures the very desync it claims to fix.

## 5. Never teleport the player — converge; never hard-set remotes — interpolate

- td-121: a >8m error used to teleport the guest car in one frame. Replaced with a per-frame exponential converger (6.0/s): 8.5m settled in 0.48s, max 0.81m per frame. Dead zones for small errors (<3m untouched).
- td-129: remote cars were hard-set on every snapshot arrival — with 16 snapshot outages >0.5s (max 15.4s) in one traced race, every resumed snapshot teleported the host car on the guest's screen (freeze, then leap). **Fix:** interpolation buffer — hold 2–3 snapshots (~200–300ms), render remotes at `now − INTERP_DELAY` with lerp/slerp between bracketing snapshots. Constant, documented render delay; never variable, never growing.

**Lesson:** the human eye forgives a constant 250ms delay; it never forgives a teleport.

## 6. Keep collisions host-authoritative, but mirror the response locally

td-121: civilian traffic is host-simulated (lockstep rejected as out of scope — right call for a driving game). But when the guest's predicted car hit a civilian, only the host applied the bump response, so predicted and authoritative trajectories diverged and the reconciler snapped.

**Fix:** the owning guest applies the *same* `apply_bump()` locally with the *same* 1.5s cooldown, ticked on the guest — predicted and authoritative post-collision trajectories agree. Hearts/scoring stay host-authoritative; remote cars untouched. Share the response function, not the authority.

## 7. Dead-reckon remote traffic

td-131's second root cause: guest-side traffic was hard-set on snapshot receipt, rendering ~RTT/2 behind, while the host collided against true positions — the guest hit cars that weren't there on its screen. **Fix:** extrapolate traffic by transit time + snapshot age. Stale data plus a velocity is more truthful than stale data alone.

## 8. Design for the worst link, not the best

td-131's trace: guest RTT p50 2866ms vs host 84ms on the *same* server — the guest's link, not the server. td-093 had already built the floor: guest keeps racing over the signaling WebSocket (10Hz poses) when WebRTC is unavailable. Prediction, interpolation buffers, and convergers degrade gracefully under a 3s-RTT link; hard-sets and round-trip-owned inputs do not.

## 9. The phone is the only profiler that counts

Every fix in this arc gated on Craig's real-phone QA — harness numbers (including the simulated-3s-RTT criteria above) supported but never closed a task. Build the telemetry pipeline *before* you need it; diagnose from real-device traces, not from reasoning about the code.

## Still open (do not present as solved)

- td-130 "rail magnet" — unresolved.
- td-054 acceptance — the desync fixes (td-129/td-131) have strong harness evidence but no phone re-verdict yet.
