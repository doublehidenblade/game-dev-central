# Coordinator durability — nothing lives only on a local VM

**Standing rule (Craig, 2026-09-28).** Any agent that picks up the coordinator
role by reading this repo must know: this repo is the durable home for
everything the coordinator depends on. A VM is ephemeral; an agent is
replaceable. The repo is neither.

## The rule

Everything coordinator-critical lives in this repo (`game-dev-central`),
never only on an agent's local VM:

- Scripts the coordinator runs (release-report generator, budget checker,
  watchdog helpers) → `tools/`
- Ledgers and state (pending releases, baselines, coordinator log) →
  `project-management/`
- Standing rules, briefs, workflow docs → `project-management/rules/`
- Harnesses and verification tooling → `tools/` or the relevant workspace
  folder, mirrored here when the coordinator depends on it

A local working copy is scratch. The repo is the source of truth. Before a
coordinator reports work done, the durable artifact is committed and pushed.
If it only exists on the VM, it does not exist.

## Why

2026-09-28: the VM was unavailable for ~half a day during migration. The
release-report script existed only on the VM, so the incoming coordinator
had to reconstruct it from scratch — wasted work and risk of drift. The
pre-existing local `~/workspace/game-dev-central/standing-rules.md`
(R1–R17) has the same exposure: it is not this repo.

One agent can crash, run out of tokens, or lose its VM mid-shift. The next
coordinator takes over by reading this repo — never by asking the previous
agent for its local files.

## Enforcement

- The coordinator handoff checklist: every durable artifact is committed to
  this repo before the shift's report goes out.
- An incoming coordinator's first step is reading this repo, not inheriting
  local files.
- Reviews call out any "it's on my VM" as a defect, not a status.
