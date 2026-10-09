# Evidence feedback and acceptance policy

This policy implements task `ops-evidence-feedback-enforcement-20261009`.
It is a **read-only decision layer**, not a scheduler, identity service, GitHub
collector, repair bot or authorization grant. Inspector findings never dispatch
workers, create game tasks, change ownership, modify rules or close tasks.

## Trust boundary

`evidence_policy.py` takes three separate data inputs and an explicit UTC clock:

- **authority**: independently collected by the coordinator from current
  authenticated sources, including the complete canonical rule inventory,
  task/source refs, ownership/stops, and authenticated actors' observations
- **submission**: the worker's acknowledgment, criterion plans and evidence refs
- **objects**: raw Git commit/tree/blob payloads needed to prove those refs

Only the first input establishes authority. Never copy worker-provided claims
into it, accept a worker's partial rule inventory, or turn a filename/Boolean
into an authentication receipt. The module cannot prove that its caller really
contacted GitHub, that an undeclared outside source does not exist, or that a
person inspected pixels. The authenticated collector and independent reviewer
are explicit boundaries, not hidden Boolean assumptions inside a PASS packet.

The committed canonical task's `evidence_rule_inventory` fixes the complete
applicable inventory (ID, repository, path). The authority must account for
exactly that inventory at the freshly observed authoritative branch heads.
Each rule's actual commit/tree/path/blob is checked and the worker must
acknowledge all current exact refs. This prevents submission-side narrowing.
Changing the applicability inventory itself requires canonical task review.

No I/O, subprocess, network access, clock read, mutable global cache or mutation
of input dictionaries occurs in the policy module. The CLI only reads explicitly
named JSON files and writes stdout. No live queue, ledger or state fallback.

## Supported commands and exit codes

From the repository root:

    python3 project-management/watchdog/watch.py brief-check \
      --authority current-authority.json --submission worker-submission.json \
      --objects verified-git-objects.json

`admission-check` is the same admission route. `evidence-check`,
`evidence-checks`, `validator-check` and `acceptance-check` all use the shared
completion route. `finding-check` uses reconciliation, needing authority and
objects but no submission. Imported `cmd_*` functions use those same routes.
Legacy positional/header-only/image-only inputs fail closed, with no remote
reads or downloads. Pixel-difference helpers remain diagnostics, never verdicts.

Exit 0 means ADMISSIBLE, ACCEPTABLE or RECORDED for the named operation;
exit 2 means INPUT_REQUIRED (including missing, unreadable or malformed inputs);
exit 3 means NO_GO or STOPPED. A nonzero evidence verdict is a real process
failure. RECORDED means a reconciliation decision exists, never that the defect
is fixed. ACCEPTABLE means the supplied, independently authenticated proof set
satisfies this policy; it does not itself merge, publish or change task status.

The existing `coordinator-plan` and all its aliases, including
`dispatch-guard`, also consume packets at `snapshot.evidence_policy[task_id]`:

    {"authority": {...}, "submission": {...}, "objects": {...}}

A valid admission packet is required before implementation/upload actions;
full completion proof is additionally required before merge. Exact task/PR
artifact tip, task identity, criterion inventory, author, status and owner must
match the coordinator snapshot. Existing source/permission/owner/stop/capacity/
publication guards continue to apply. A policy pass cannot override any guard.
Missing or disputed acceptance still permits separately authorized independent
read-only verification. Filing an unfiled ask remains a registration/reconciliation
operation, **not** admission to production implementation. No blanket stall from
an unrelated publication hold. Dispatch-guard re-evaluates the full current
snapshot; altered proof inputs invalidate its input-bound decision receipt.

## Schema and proof representation

`fixtures/evidence-policy/positive.json` is a reproducible complete example.
The fixture identities and Git repository are synthetic and public-safe;
they do not attest real users or live work. Field names are strict in the
policy contracts: missing, unknown and malformed fields fail closed.

Authority version 1 contains:

- `observed_at`: fresh UTC collection time (maximum 15 minutes)
- `rule_heads`: repository → full current authoritative commit
- `rules`: nonempty `{id, ref}` list, equal to the canonical task inventory
- `task_ref`: immutable citation of the canonical JSON task
- `candidate`: `{repository, implementation_head, artifact_head}`
- `principals`: `{author, coordinator, reviewer, human}`; reviewer distinct
  from author, human null only when no visual human gate is applicable
- `owner_id`, `status`, `stopped`: current ownership and explicit stop facts
- `exclusions`: bounded coordinator-authorized criterion exclusions
- `attestations`: authenticated observations of review, human, execution or
  coordinator-decision artifacts, with exact ref, actor, observation time and
  collection provenance. Executions cannot postdate their collection receipts
- `findings`, `decisions`: all relevant structured findings and committed
  coordinator reconciliation-decision citations, including unresolved ones

Every citation is `{repository, commit, path, blob}`. Commits/blobs are full
lowercase 40-hex IDs; paths are regular repository-relative files, without
traversal, symlinks or submodules. `objects[repository][sha]` is
`{type: "commit"|"tree"|"blob", base64: "raw payload bytes"}`. Each object is
rehashed with Git's `type size\0` prefix. Commits identify trees; raw binary tree
entries prove path membership recursively; the cited blob must match and its
actual bytes must be accessible and nonempty. A collector's claimed `committed`
flag, mutable ref, file existence, fabricated 40-hex ID or metadata-only content
cannot pass. Export raw objects using a read-only authenticated Git reader;
never commit credentials. Missing objects produce a scoped INPUT_REQUIRED.

The task's existing nonempty `completion_criteria` list defines all criterion
IDs/descriptions/verification requirements. A matching `evidence_policy` map
adds for each criterion: explicit applicability, rationale, authoritative rule
ID, all claimed instance IDs, relevant source paths, build binding (or null),
visual Boolean and concrete required checks (`id` plus command argument list).
A not-applicable exclusion additionally needs an authenticated coordinator
criterion-exclusion artifact matching task, criterion, rationale and rule;
a worker cannot exclude its own criterion. Zero parsed or zero applicable
criteria never automatically pass.

Submission fields:

- `acknowledgment`: task ID, author ID and the exact complete current rule refs
- `plans`: every applicable criterion, with nonempty method, concrete artifact
  paths/types, full source scope, build/variant/environment, all instances and
  designated independent reviewer. A heading alone is not a plan
- `evidence`: per-artifact ID, criterion/instances/type/ref/source head/build/
  performance time and required check ID (null for documents/images/diffs)
- `verdict`: independent review citation; `human_verdict` additionally for
  visual tasks. Absence of either required verdict is a pending gate

A log/assertion is a structured actual execution record with exact required
command/check ID, exit code, observed output, source head, build/variant/
environment, time and actor. It requires an authenticated execution observation.
A nonzero, missing, unrelated or unbound command cannot become green from a
reviewer's text. Nonvisual documents/diffs can be appropriate when the task
requires them; screenshots are not universally compulsory.

## Reconciliation, not automatic rule creation

A finding records stable ID and deterministic failure fingerprint, source repo/
full observed head/time, task/criterion, machine failure code, actual citations,
coverage and source-read limitations. Same ID with a changed payload conflicts.
Exact replay is idempotent; every distinct finding must receive an explicit
coordinator decision. Contradictory dispositions fail, including equivalent
fingerprints under different finding IDs. The inspector is never the decider.

Allowed decisions:

1. `existing_rule`: cite the exact current rule ID/revision
2. `task_limitation`: bounded task/criterion/instance scope, required action and
   evidence, and explicit admission/completion gates that remain blocked
3. `reusable_guideline`: recorded incident, invariant and genuinely distinct
   contexts, actual changed authoritative rule bytes and bound delta artifact,
   plus authenticated regression execution that fails on that incident's
   committed broken fixture and binds the executable assertion and rule delta

The module cannot judge the intellectual quality of a generalization rationale.
That remains independent review. Repetition counts alone never create a rule.
Regression booleans, invented paths, unrelated failures and unchanged rule bytes
are rejected. The tests actually execute the synthetic broken-fixture assertion
and inspect the resulting failure; the evaluator itself never executes code.

## Source, evidence and verdict commits are separate

The reviewed `implementation_head` can precede `artifact_head`, including the
commit that contains the verdict itself. Raw parent traversal must prove the
artifact tip descends from the implementation. Every authoritative relevant
source path must have identical actual blob IDs across those commits. The
current canonical task's criteria, applicability and rule inventory must also
remain unchanged; work-log/evidence/verdict-only task edits do not create a
circular self-hash requirement.

Evidence must be reachable from the artifact tip and retain its cited bytes at
that tip. Historical evidence additionally requires actual ancestor/source-scope
equivalence and matching applicable build/variant/environment provenance.
Old dates alone do not force a rerun; old filenames/metadata alone never suffice.
Fresh authenticated applicability reads remain mandatory.

Independent verdicts bind the exact implementation head, semantic task/rule
scope, full evidence-manifest digest, distinct authenticated reviewer identity,
and a nonempty inspected decision/citation set for **every** criterion and every
artifact/instance. Rule content (blob) changes invalidate the review; mere
movement of an authoritative branch with proven identical rule bytes does not.
The acknowledgment still refreshes to the current full rule commit refs.
Active conflicting FAIL/PENDING judgments cannot be hidden by selecting a PASS.

Machine source/evidence binding, independent review, and human visual judgment
are distinct output gates. A matched before/after pair is required for each
visual instance, with same camera and distinct bytes. Those checks do not judge
pixels: direct inspected meaningful/nonempty/matched/improved judgments must
come from the independent reviewer, then Craig's explicit device verdict.
Numeric differences, filenames, scripts or green CI cannot manufacture either
judgment. Identical or rejected wrong-state images fail. Pending human judgment
remains pending, and explicit stops/terminal ownership are preserved.

## Verification and integration history

PR396's accepted source merge `39aa747c7f1f35393a316faebd942386579ff913`
provided the serialized integration base, after independent review5471277399.
Only evidence-related routes/calls and minimal usage documentation were handed
off. PR143 canonical visual-onboarding hunks are unedited. The current accepted
rule bytes are pinned by the real-input manifest; this work does not claim
acceptance of unmerged PR143 content.

Run locally, without Actions:

    cd project-management/watchdog
    python3 -m unittest -v test_evidence_policy
    python3 test_rules.py
    python3 test_coordinator_review.py
    python3 test_coordinator_acceptance_isolation.py
    python3 test_coordinator_final_guards.py
    python3 test_coordinator_hold_invariance.py
    python3 test_coordinator_operation_needs.py

PR396's fake-SHA fixtures remain **operation-layer unit tests**, with only the
new policy boundary explicitly mocked in their test-only `coordinator_forbid_io`
helper. Their source/owner/stop/capability/hold assertions remain unchanged.
The new tests exercise actual production aliases, coordinator decisions and
revalidation with raw-object proof packets and without that mock. There is no
production skip flag, test identity exception or missing-packet success path.

The real-input capture is a truthful current task/rule/source check, with raw
immutable Git objects and explicit denials where evidence/independent review
are not yet present. A synthetic PASS is not live adoption. No collector or
external scheduler is installed or claimed to be enforcing this policy.
