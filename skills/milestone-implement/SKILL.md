---
name: milestone-implement
description: Implement a planned milestone in a cairn repo on its own branch with tests-first tasks and checkpoint commits. Use when the user wants to start, resume, work on, or continue a milestone (e.g. "work on M07", "resume the milestone", "start implementing").
argument-hint: "<id>"
---

# /milestone-implement <id> — planned → review

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: git model, tracking-travels-with-code, delegation policy,
CI waiting rules).

## Session start

Read, in order: `project/ROADMAP.md`, the target milestone file,
`project/DECISIONS.md`. If an un-ingested RR exists for this milestone,
run ingestion first (see `/milestone-brief`).

## Workflow

1. Verify status is `planned` (fresh start) or `in-progress` / `blocked`
   with a resolved blocker (resume). Verify all `Depends on:` milestones are
   `done`. Set `in-progress` in ROADMAP + header mirror.

2. **Branch.** Check `git status` first — a dirty tree with unrelated
   changes means ask the user; never sweep strangers into a checkpoint
   commit. First session: sync main with origin first — `git fetch`, pull
   (ff-only), and **push any unpushed local commits** — so the branch is cut
   from pushed main and the PR diff will contain only milestone work; then
   `git checkout -b m<nn>-<slug>`; record the branch in the milestone
   header. Resume sessions: check out the
   existing branch; if main has moved since the branch was cut (e.g., a
   hotfix merged), merge main into the branch and re-run `devtools::test()`
   before continuing.

3. **Question gate:** surface the implementation choices the plan left open
   (API shape, naming, dependency picks — dependency changes always need a
   gate + D-entry) with recommendations. Skip only if nothing is genuinely
   open.

4. **Work tasks in order, autonomously.** For each task:
   - Tests first where feasible (testthat 3e); numeric results per the
     oracle doctrine; new user-facing conditions via `cli::cli_abort()`.
   - After roxygen changes: `devtools::document()`. Gate:
     `devtools::test()` clean before checking the task off.
   - Checkpoint-commit per task on the branch, **including** the milestone
     file update (checkbox + one work-log line) in the same commit.

5. **Delegate** per tracking-rules (Sonnet for well-specified mechanical
   work; Opus for design-sensitive work; never Haiku; Fable only via
   `/milestone-brief`). Verify subagent diffs yourself; one work-log line
   per delegation.

6. **Plan amendments** (implementation always learns things planning
   didn't know):
   - *Minor* (reorder tasks, refine wording, add a discovered sub-task):
     edit the milestone file; one work-log line.
   - *Substantive* (a criterion or scope must change): mini question gate
     with a recommendation; record the amendment as a dated work-log line
     (+ D-entry if cross-cutting).
   - *The goal itself is wrong*: stop; status back to `planned`; routing
     chip to `/milestone-plan` for a proper re-cut.
   Never silently deliver something other than what the plan promised —
   review checks criteria as written.

7. **Blocked?** External blocker → status `blocked` + work-log line naming
   it, stop. Needs Fable-level judgment → routing chip to
   `/milestone-brief`, stop.

8. **Completion.** When all tasks are checked and `devtools::check()` is
   clean: set status `review`, checkpoint-commit, then stop with a recap —
   file-level summary of the branch diff, test/check results, deviations
   from plan, open concerns — and a **routing chip** (AskUserQuestion, one
   question, options in this order):
   - **Proceed to review** → `/milestone-review <id>` (recommended)
   - **Adjust first** — changes on the branch before review
   - **Pause here** — stop; milestone stays at `review`
   Honor "Other" free-text as adjustment instructions. The chip is a stop,
   never an auto-proceed. Note in the recap that the checkpoint makes this
   a safe `/clear` point — review resumes statelessly in a fresh session
   (same-session review via the chip is also fine; see tracking-rules
   context hygiene).
