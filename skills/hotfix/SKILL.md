---
name: hotfix
description: Fix a user-visible bug in a cairn repo without milestone ceremony - regression test first, gate-lite checks, PR, merge on user approval. Use whenever a bug is reported or described ("users report an error in X", "this crashes when...", "fix this bug") and no milestone already covers it.
argument-hint: "[description]"
---

# /hotfix — the fast lane for real bugs

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: work tiers, git model). Read `cairn/ROADMAP.md` to check
whether an existing milestone already covers this, and `cairn/DECISIONS.md`
for standing constraints. If an un-ingested RR sits in `cairn/reviews/`,
handle ingestion first (see `/milestone-brief`).
Stage banner: `[cairn · hotfix · <slug> · <step>]`.

## Workflow

1. **Tier check first.** Reproduce or at least localize the bug. This stays
   a hotfix only if it restores documented behavior and fits one sitting.
   If it needs a design decision, changes exported behavior beyond
   restoring what was documented, or won't fit one sitting — stop: add a
   `candidate` row (or offer a routing chip to `/milestone-plan` if it's
   urgent) and say why. If an active milestone covers this code, flag the
   overlap instead of racing it.

2. **Branch.** Check `git status` (dirty tree with unrelated changes → ask).
   Branch `hotfix-<slug>` from up-to-date main (fetch, pull ff-only, push
   any unpushed local commits — see tracking-rules git model).

3. **Regression test first.** Write the test that fails because of the bug;
   confirm it fails; then fix; confirm it passes.

4. **Gate-lite:** `devtools::test()` clean; `devtools::document()` if
   roxygen changed; `devtools::check()` if anything structural was touched.

5. NEWS.md entry under the development version (no milestone/issue jargon in
   the user-facing text). Push; open the PR — `Fixes #N` in the description
   if a GitHub issue exists.

6. **Approval gate:** present the diff, the regression-test evidence, and
   the NEWS line; merge (`gh pr merge --squash --delete-branch`) only on
   explicit user approval, with green CI (one blocking
   `gh pr checks --watch` wait). On approval, write the merge-guard
   marker first: `cairn/.merge-approved` (gitignored; one line:
   `hotfix <slug> approved YYYY-MM-DD`) — the plugin's hook denies
   merges to main without it and consumes it per attempt.

7. If the fix revealed deeper work, add a `candidate` row before closing
   out. If a milestone branch is currently active, remind the user that its
   next implement/review session will merge main into it (the branch-sync
   rule) — nothing to do now.
