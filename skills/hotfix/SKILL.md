---
name: hotfix
description: Fix a user-visible bug in a cairn repo, or adopt an incoming external PR that fixes one, without milestone ceremony - regression test first, gate-lite checks, PR, merge on user approval. Use whenever a bug is reported or described ("users report an error in X", "this crashes when...", "fix this bug"), or an incoming pull request needs taking in ("adopt PR #12", "review this external PR", "a contributor opened a PR"), and no milestone already covers it.
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

1. **Tier check first.** Reproduce or at least localize the bug. When the
   input is a PR reference instead of a bug report (`#N`, a PR URL, "adopt
   PR 12"), read the contributor's work first — `gh pr view <N>`,
   `gh pr diff <N>` — and tier-check *that* diff. Either way this stays
   a hotfix only if it restores documented behavior and fits one sitting.
   If it needs a design decision, changes exported behavior beyond
   restoring what was documented, or won't fit one sitting — stop: add a
   `candidate` row (or offer a routing chip to `/milestone-plan` if it's
   urgent) and say why. An incoming PR over the hotfix bar takes that same
   route and becomes (or joins) a milestone — the disposition is unchanged,
   only the entry point is new. If an active milestone covers this code,
   flag the overlap instead of racing it.

2. **Branch — cut one, or adopt the PR's.** Check `git status` (dirty tree
   with unrelated changes → ask).
   *Authoring a fix:* branch `hotfix-<slug>` from the up-to-date default
   branch (detect it per the tracking-rules git model; fetch, pull ff-only,
   push any unpushed local commits).
   *Adopting a PR:* run `gh pr checkout <N>` — never cut a fresh branch,
   which would orphan work that already exists. The contributor's branch
   name is **exempt** from the `hotfix-<slug>` contract (tracking-rules, git
   model): the branch is theirs, renaming it breaks the PR, and the PR
   number is the identifier that matters.

3. **Regression test first.** The bug gets a test either way; only the
   sequence differs.
   *Authoring a fix:* write the test that fails because of the bug; confirm
   it fails; then fix; confirm it passes.
   *Adopting a PR:* the fix already exists, so the author-side
   "fails before the fix" sequence is unreachable — the test is **added**,
   and it earns its keep by **failing against the default branch and passing
   on the PR head**. Prove both directions: run it on the PR head, then in a
   throwaway worktree of the default branch created **outside the repo**
   (`git worktree add /tmp/<repo>-verify <default-branch>`) with only the
   test file copied in — then `git worktree remove` it. Clean up even when
   the check fails: a leftover worktree inside the repo becomes an untracked
   directory that trips step 2's own dirty-tree check on the next run.
   A test that passes on both proves nothing about the
   bug. A test the contributor already wrote goes through that same two-way
   check — adopting a PR means verifying its evidence, not inheriting it.

4. **Gate-lite:** run the active profile's `verify` slot (`cairn/PROFILE.md`;
   absent → infer per tracking-rules "Toolchain profiles") — its gate-lite
   checks must be clean before the fix is proposed for merge.

5. Add a changelog entry to the file the active profile's `changelog` slot
   declares (`cairn/PROFILE.md`; a slot value of "none" → skip the entry;
   PROFILE.md absent → infer per tracking-rules "Toolchain profiles":
   `NEWS.md` for r-package, else the repo's `CHANGELOG.md` / convention)
   under the current development version (no milestone/issue jargon in the
   user-facing text).
   *Authoring a fix:* push; open the PR — `Fixes #N` in the description if a
   GitHub issue exists.
   *Adopting a PR:* the PR already exists — never open a second one, except
   through the user-gated fallback below. If the
   contributor added an entry, check it against the declared file and the
   user-facing-text rule and edit it in place rather than appending a
   duplicate; if none is present, add one. Push the test and the entry to the
   PR's head branch — this works on a fork when the contributor left
   "allow edits by maintainers" on (GitHub's default).
   **When the head branch cannot be pushed to:** ask the contributor on the
   PR to add the missing pieces — it is their work and their credit.
   If they go quiet, re-landing the work locally is the fallback, but it
   closes another person's PR under the user's GitHub identity — outward-facing
   and irreversible from the contributor's side, so it is **never** done
   unilaterally. Put it to the user as an `AskUserQuestion` chip (recommended
   = re-land, with a decline option), showing the closing comment's text in
   chat first. Only on approval: recreate their commits on a
   `hotfix-<slug>` branch (`git cherry-pick`), add the test and changelog
   there, open a PR crediting them (`Co-authored-by:`), and close theirs with
   that comment. Declined → leave their PR open and stop.
   Never merge a fix whose regression test
   is still missing — that is the one gate this path exists to enforce.

6. **Approval gate:** present the diff, the regression-test evidence, and
   the changelog line (when the `changelog` slot declares a file); put the
   merge authorization to the user as an
   `AskUserQuestion` chip (recommended = merge, e.g. `Merge PR #N to
   <default-branch>`, with a decline option) — never a prose yes/no, the same gate discipline
   as `/milestone-review`. Merge (`gh pr merge <N> --squash --delete-branch`
   — name the PR number explicitly; a bare `gh pr merge` is denied because the
   approval cannot be checked against it; **drop `--delete-branch` on a
   fork PR** — that branch lives in the contributor's repo and is not ours
   to delete)
   only on explicit approval at that chip, with green CI (one blocking
   `gh pr checks --watch` wait). On approval, write the merge-guard
   marker first: `cairn/.merge-approved` (gitignored; one line:
   `hotfix <slug> approved YYYY-MM-DD for PR #<N>` — the marker names the PR
   it approves, and the guard refuses a merge that names a different PR or
   none) — the plugin's hook denies
   merges to the default branch without it and consumes it per attempt. Write the marker
   in a **separate** step before the `gh pr merge` command — the hook checks
   it before the command runs, so writing it in the same shell line is
   denied.

7. If the fix revealed deeper work, add a `candidate` row before closing
   out — sweep first per the search-first candidate-creation rule
   (`tracking-rules.md`, Intake). If a milestone branch is currently active, remind the user that its
   next implement/review session will merge the default branch into it (the
   branch-sync rule) — nothing to do now.
