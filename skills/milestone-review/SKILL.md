---
name: milestone-review
description: Verify and ship a finished milestone in a cairn repo - fresh evidence for every acceptance criterion, consistency gate, independent code review, and merge on user approval. Use when the user wants to review, verify, finish, ship, or merge a milestone.
argument-hint: "<id>"
---

# /milestone-review <id> — review → done

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: approval model, CI waiting rules, archive protocol).
Phase header: `## Milestone <NN>: <title>` → `### Review`.

## Session start

Read, in order: `cairn/ROADMAP.md`, the target milestone file,
`cairn/DECISIONS.md`. Status must be `review` (or the user explicitly
overrides — log the override).

## Workflow

1. **Sync with main first** — main means origin/main: `git fetch` before
   comparing, and push main if it has unpushed local commits. If main has
   moved since the branch was cut, merge main into the branch and re-run
   tests before gathering any evidence — evidence from a stale branch is
   worthless and the squash-merge would conflict anyway.

2. Push the branch; open a **draft PR** (`gh pr create --draft`) so CI runs
   in the background while the review proceeds. Record the PR URL in the
   milestone header.

3. **Execute every acceptance criterion with fresh evidence** — actually run
   the tests, actually run `devtools::check()`; record results per criterion
   in the milestone's Review section (summaries, never pasted output).

   **Criteria are never reinterpreted at review.** If the work seems right
   but a criterion as written fails, the criterion is wrong — send the
   milestone back for a gated amendment (`/milestone-implement` step 6),
   then re-review. A charitable reading silently destroys what criteria are
   for.

4. **Consistency gate** — mechanical checks, by command, never recall:
   - `devtools::document()` produces no diff.
   - README.Rmd present and out of sync with README.md →
     `devtools::build_readme()`, commit.
   - pkgdown site present → `pkgdown::check_pkgdown()` passes (catches
     exports missing from `_pkgdown.yml`).
   - NEWS.md has an entry for this milestone's user-visible changes (no
     milestone numbers in user-facing text).
   - New top-level files have `.Rbuildignore` entries (check `check()`
     NOTEs).

   Any criterion or gate failure → status back to `in-progress`, work-log
   line naming exactly what failed, stop. **Thrash rule:** if this is the
   milestone's third trip back from review (count the work-log), do not
   queue another retry — that's a mis-planned milestone; recommend re-plan
   or split via `/milestone-plan`.

5. **Independent fresh-context review.** Spawn an **Opus subagent**
   ([O]-tagged description) that has not seen the implementation to
   review the full diff
   (`git diff main..HEAD`) against the acceptance criteria, DESIGN.md
   conventions, and DECISIONS.md. Triage its findings: fix now / spawn a
   follow-up (candidate row or milestone) / reject with reason — all logged
   in the Review section.

6. Final checkpoint commit on the branch.

7. **Final approval gate.** Present, outcome-first (per tracking-rules):
   what the user is approving in plain words — what the milestone does or
   changes — then acceptance-criteria evidence, problems
   found and how each was handled, diffstat, anything the user should eyeball
   directly. Ask any remaining clarifying questions first (batched, with
   recommendations). Then put the merge authorization **itself** to the user
   as an `AskUserQuestion` chip — this is the third gate (per tracking-rules),
   never a prose yes/no: the recommended option merges (e.g. `Merge PR #N to
   main`) and a decline option is present. Approval withheld (or declined at
   the chip) → log the requested changes as tasks, status back to
   `in-progress`, stop.

8. **On approval — and only then:** record the approval for the merge
   guard — write `cairn/.merge-approved` (gitignored; one line:
   `M<NN> approved YYYY-MM-DD`). The plugin's PreToolUse hook denies
   merges to main without this marker and consumes it per merge attempt;
   if a merge fails and is retried under the same approval, rewrite the
   marker. Then mark the PR ready; require green CI
   (`gh pr checks <pr> --watch` with a timeout — one blocking wait; on
   timeout report fresh state and stop). Red CI → fix on the branch,
   re-verify, re-request approval if the fix was nontrivial. When green:
   `gh pr merge --squash --delete-branch` with a clean summary message.

9. **Post-merge hygiene pass on main:** check out main and pull first —
   after a squash-merge, local main is behind origin and any leftover local
   commits mean divergence to resolve before committing. Then compress the
   milestone file to a
   ≤25-line summary (goal, outcome, key decisions, PR link) and move it to
   `cairn/milestones/archive/`; ROADMAP row → `done` + archive path;
   archive any resolved RB/RR pairs; update "Last hygiene check"; verify
   weight caps. Docs-only commit: `review M<NN>: done`; push. The done
   recap leads with what shipped, in plain words; hygiene mechanics
   compress to one line.

10. **Routing chip**, composed from the post-merge state (chip rules per
    tracking-rules). Precede it with one line: M<NN>
    is archived and all state is on disk, so this is a natural `/clear`
    point — selecting a chip continues this session; a fresh session
    starts the next milestone with clean context (recommended when this
    session already ran implement or is otherwise long). E.g.:
    - **Plan the next milestone** → `/milestone-plan` (recommended when
      planned/candidate work exists)
    - Run a health audit → `/milestone`
    - Stop here
