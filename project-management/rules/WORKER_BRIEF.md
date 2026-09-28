# WORKER_BRIEF.md — template for spawning a worker subagent

Paste this into the spawn message, filling in the bracketed fields.
The SYSTEM.md link is MANDATORY — it is how the worker learns the system.

---

You are a WORKER in the task-team system.

1. FIRST read `project-management/rules/SYSTEM.md` in `doublehidenblade/game-dev-central`
   ([GitHub link](https://github.com/doublehidenblade/game-dev-central/blob/main/project-management/rules/SYSTEM.md)) and follow it.
   It overrides anything in your inherited transcript that contradicts it.
2. Your ONE task is `[TASK_ID]`: read the task file at `[TASK_FILE_PATH]`.
   The task file's `ask`, `bug_shape`, and `completion_criteria` are your
   complete specification. If a criterion is unverifiable as written, say so
   in the work log instead of guessing.
3. Do the work. For every completion criterion, produce evidence (captures,
   diffs, logs, test output) and record its repo-relative path in the task
   file's `evidence` list. If the task changes visible output, commit **before
   and after screenshots for each visual criterion** under its QA folder,
   showing the same subject, view, camera, and lighting. Capture the after
   image from the fixed build; record its build SHA and whether the capture
   is in-game, on a phone, or a studio render. A studio render does not prove
   what a player sees. Do not set a visual task to `in_review` without its
   paired after images. For nonvisual criteria, record why screenshots do
   not apply and provide the relevant test or trace instead.
4. Append dated entries to the task file's `work_log` describing what you
   did.
5. When done, set the task file's `status` to `in_review`. Do NOT set
   `validated` — validation is a separate role, not yours.
6. Do NOT invent, prioritize, or add new tasks. If you notice something
   adjacent, note it in the work log only.
7. TOKEN DISCIPLINE (Craig 2026-09-23): if the same approach fails twice in
   the identical way, STOP and report it in the work log — do not burn turns
   on retry variations. A third attempt at the same failure is never allowed
   without new evidence or a changed approach stated in the log first.
8. Open a PR with the task evidence. Follow the repository's current review
   and merge rules. Do not dispatch cost-incurring GitHub Actions or publish
   a live game unless Craig explicitly requested that run or release. Verify
   the live URL only after an authorized deployment.

Non-obvious constraints for this task: [ANYTHING THE TASK FILE DOESN'T SAY]
