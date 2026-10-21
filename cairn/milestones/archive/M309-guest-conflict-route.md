# M309: Route a handed-off PR with merge conflicts to a sync

**Status:** done (2026-10-21, PR #323 https://github.com/jmgirard/cairn/pull/323)

**Goal:** `/milestone` finds a handed-off PR that no longer merges cleanly and routes it to a sync.

**Outcome:** `/milestone` §2's guest `blocked` read adds `mergeable`. After the existing arms, an `OPEN` PR reading `CONFLICTING` routes to `/milestone-implement` and one reading `UNKNOWN` is reported with no route. Both arms also quote unanswered maintainer comments. The "Open hotfix PRs" read adds `mergeable` and reports a conflicted PR. `/milestone-implement` step 1 resumes a `blocked` guest milestone for the guest sync (the stacked sync for a stacked one) on a fresh `mergeable` read of `CONFLICTING`. Step 2's guest sync handles a rebase that stops on conflicts. The session resolves the files, stages them, and runs `git rebase --continue`, then runs `verify` green before any push, the stacked lease push included. If it cannot resolve them, it lists the files with `git diff --name-only --diff-filter=U`, runs `git rebase --abort`, pushes nothing, and stops naming them. The rulebook's guest route list, `/milestone-review`'s guest close label, the pane's `PR_BUTTON` comment, DESIGN.md, and CHANGELOG follow. Trigger: modelbased #696 and #697.

**Decisions:** none.

**Review:** Criteria audit at plan (full). Claim audit 15 claims, 4 corrected. Four fresh reviewers plus Copilot (Lite, one body item): 12 fixed, 8 rejected (none as `edge`), 5 to the parked candidate row "Close the guest conflict sync edges". Hygiene: M306 row pruned to the terminal cap; no lesson added (LESSONS at its cap); no row unparked.
