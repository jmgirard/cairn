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
Phase header: `# Hotfix: <slug>` → `## <step>`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

## Workflow

1. **Tier check first.** Reproduce or at least localize the bug. This stays
   a hotfix only if it restores documented behavior and fits one sitting.
   If it needs a design decision, changes exported behavior beyond
   restoring what was documented, or won't fit one sitting — stop: add a
   `candidate` row (or offer a routing chip to `/milestone-plan` if it's
   urgent) and say why. If an active milestone covers this code, flag the
   overlap instead of racing it.

2. **Branch.** Check `git status` (dirty tree with unrelated changes → ask).
   Branch `hotfix-<slug>` from the up-to-date default branch (detect it per
   the tracking-rules git model; fetch, pull ff-only, push any unpushed local
   commits).

3. **Regression test first.** Write the test that fails because of the bug;
   confirm it fails; then fix; confirm it passes.

4. **Gate-lite:** `devtools::test()` clean; `devtools::document()` if
   roxygen changed; `devtools::check()` if anything structural was touched.

5. NEWS.md entry under the development version (no milestone/issue jargon in
   the user-facing text). Push; open the PR — `Fixes #N` in the description
   if a GitHub issue exists.

6. **Approval gate:** present the diff, the regression-test evidence, and
   the NEWS line; put the merge authorization to the user as an
   `AskUserQuestion` chip (recommended = merge, e.g. `Merge PR #N to
   <default-branch>`, with a decline option) — never a prose yes/no, the same gate discipline
   as `/milestone-review`. Merge (`gh pr merge --squash --delete-branch`)
   only on explicit approval at that chip, with green CI (one blocking
   `gh pr checks --watch` wait). On approval, write the merge-guard
   marker first: `cairn/.merge-approved` (gitignored; one line:
   `hotfix <slug> approved YYYY-MM-DD`) — the plugin's hook denies
   merges to the default branch without it and consumes it per attempt. Write the marker
   in a **separate** step before the `gh pr merge` command — the hook checks
   it before the command runs, so writing it in the same shell line is
   denied.

7. If the fix revealed deeper work, add a `candidate` row before closing
   out. If a milestone branch is currently active, remind the user that its
   next implement/review session will merge the default branch into it (the
   branch-sync rule) — nothing to do now.
