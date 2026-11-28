# M186: The PR opens after approval, so CI first runs on the head that merges

**Status:** done (2026-09-10, PR #193 https://github.com/jmgirard/cairn/pull/193)

**Goal:** Review and hotfix push the branch and open the pull request only after the user approves at the merge gate, so a `pull_request`-triggered suite first runs on the head that merges instead of on every pre-approval push.

**Outcome:** `/milestone-review` step 2 pushes nothing; step 8 pushes, runs `gh pr create --title --body` (ready, never draft, `Closes`/`Refs` body), records the PR URL in the header as an unpushed commit, then marker, CI wait (a fresh PR re-read before the no-checks case), merge. The step-7 chip is `Merge <branch> into <default-branch>` and the approval line `step-7 approval: <branch> approved for merge`, read by prefix; resume routes, `/milestone` §2, and the archive summary fall back to `gh pr list --head <branch>` once `--delete-branch` has removed the local branch. The M177 PR-conversation read runs only where a PR pre-exists, once per pass through the gate. `/hotfix` step 5 pushes nothing; step 6 opens the PR after approval, skipping the create on a PR-reference re-entry. Guest handoff = push to fork + create against the base repo, no ready-marking. Rulebook "A branch push starts CI" bullet, Collaboration-mode bullets, implement step 9's CI line, README, CHANGELOG follow; eleven `skills/tests` pins re-seeded.

**Decisions:** D-138 (post-approval open; serial CI wait as the cost; the unpushed record with the by-branch fallback; the pre-gate open, the post-CI read, and the ready-for-review workflow config rejected with reopeners).

**Review:** Implement-time claim audit read 47 claims, corrected 3 (the unpushed record, a hotfix "first", a CHANGELOG overstatement). Three-lens fan-out: blame-history and prior-PR-comments clean; diff-bug 8 findings, all fixed at the gate — the by-branch resume fallback (F1/F3), the fresh-PR no-checks re-read (F2), the hotfix skip-create guard (F4), D-138 naming the unpushed record (F5), implement wording (F6), explicit `--title`/`--body` (F7), once-per-pass wording (F8). No returns. Nothing graduated or retired at hygiene.
