# Task-Team System (supervisor / worker / validator)

Read this file FIRST. It is the canonical description of how task teams work.
It lives on disk because no agent's context can be trusted to remember it:
the main agent's context accumulates many unrelated tasks (meals, travel,
calendars, other projects) and has forgotten bug reports from hours ago and
accepted worker claims without checking. Task truth lives in files, not in
anyone's memory. If this file contradicts something in your inherited
transcript, this file wins.

## Roles

- **Supervisor** — the main agent, acting on a schedule (cron) or an event
  (hook). Owns liveness (dead workers), leftover-work pickup, dispatching
  workers and validators, and reporting meaningful transitions to Craig.
  The supervisor does NOT validate work quality itself.
- **Worker** — a subagent that executes ONE task. Reads this file, reads its
  task file, does the work, gathers evidence, writes a work log, and sets
  the task status to `in_review`. A worker NEVER declares its own work
  accepted.
- **Validator** — a subagent that judges ONE completed task against its
  written completion criteria. Scoped brief: the task file plus the listed
  evidence are its only sources of truth; the inherited transcript is
  background noise. Returns per-criterion PASS/FAIL verdicts, each with an
  evidence citation. A validator NEVER fixes the work — it judges it.

## The loop

1. Supervisor dispatches a worker (brief template: `WORKER_BRIEF.md`).
2. Worker does the work, collects evidence for every completion criterion,
   updates the task file (work log + evidence links), sets
   `status: in_review`.
3. Board watcher (hook) sees `in_review` → wakes the supervisor →
   supervisor dispatches a validator (brief template: `VALIDATOR_BRIEF.md`).
4. Validator checks each criterion, writes the verdict into the task file
   (per-criterion PASS/FAIL + evidence citation), and sets
   `status: validated` or `status: rejected` (with rejection notes).
5. Board watcher sees `validated` / `rejected` / `blocked` → wakes the
   supervisor → supervisor decides what Craig needs to hear (see below).
6. `rejected` → back to `in_progress` with the validator's notes appended;
   a worker iterates. Second rejection, or a validator question for Craig,
   escalates to Craig.

## Task file contract

Every task file MUST contain these fields (JSON):

- `id`, `title`
- `status` — one of: `open`, `in_progress`, `in_review`, `validated`,
  `rejected`, `blocked`, `abandoned`
- `ask` — whose ask it was and what was requested, with date
- `bug_shape` — the observable shape of the bug: what it looks like, where
  it appears, reference images of the wrong state
- `reference_images` — what the correct state looks like
- `completion_criteria` — concrete, checkable criteria. Each one must say
  HOW it is verified (which screenshot angle, which numeric diff, which
  test). A criterion you cannot verify is not a criterion — rewrite it.
- `evidence` — paths to captures/logs/diffs produced by the worker
- `work_log` — dated entries of what was done
- `verdict` — written ONLY by the validator: per-criterion PASS/FAIL with
  evidence citations, plus overall status change

## Status transitions the board watcher cares about

- → `in_review`: dispatch a validator.
- → `validated`: work accepted. Tell Craig (with the relevant link).
- → `rejected`: send back for iteration. Tell Craig only on the 2nd+
  rejection, or if the validator flagged a question only Craig can answer.
- → `blocked`: tell Craig — it needs a decision only he can make.

Everything else (routine `open` → `in_progress`, work-log edits) is silent.

## Hard rules

1. Worker-reported validation is NEVER acceptance. Only a validator verdict
   of `validated` counts — and Craig's own eye is the final gate.
2. A validator verdict without an evidence citation per criterion is itself
   rejected; the validator re-does it.
3. Validators never edit the work under review. Workers never set
   `validated`.
4. No role invents, prioritizes, or adds new tasks. New tasks come from
   Craig's explicit asks, bug reports, or ideas.
5. Every subagent brief MUST link this file (`~/workspace/supervisor-system/SYSTEM.md`)
   and instruct the subagent to read it before anything else. Then the brief
   scopes the ONE task. This is how future subagents learn the system —
   never via the spawner's context memory.
6. Evidence must be openable: on-disk paths for agents, public HTTPS links
   for anything Craig needs to see.
7. Never send Craig an image the validator hasn't opened. (Standing rule
   from 2026-09-19.)

## Where boards live

- Tokyo Drift: `~/workspace/tokyo-drift-godot/docs/tasks/td-*.md`
  (mirrored in the `tokyo-drift-3d` repo under `godot/docs/tasks/`)
- New projects: add their board path here when created.
