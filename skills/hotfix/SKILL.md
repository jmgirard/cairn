---
name: hotfix
description: Fix a user-visible bug in a cairn repo, or adopt an incoming external PR that fixes one, without milestone ceremony - regression test first, gate-lite checks, PR, merge on user approval. Use whenever a bug is reported or described ("users report an error in X", "this crashes when...", "fix this bug"), or an incoming pull request needs taking in ("adopt PR #12", "review this external PR", "a contributor opened a PR"), and no milestone already covers it.
argument-hint: "[description]"
---

# /hotfix — the fast lane for real bugs

Plugin root: every `${CLAUDE_PLUGIN_ROOT}` path below is under the plugin
install directory. When the shell has that variable unset or empty — the
symlink install in `~/.claude/skills` leaves it so — substitute the
grandparent of this skill's directory (the `Base directory for this skill:`
line the harness prints above) in every read and command below; never run a
command with the variable empty.

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: work tiers, git model). Read `cairn/ROADMAP.md` to check
whether an existing milestone already covers this, `cairn/DECISIONS.md`
for standing constraints, and `cairn/DESIGN.md`'s Conventions section
for the repo's per-change rules, which step 5 applies.
If an un-ingested RR sits in `cairn/reviews/`,
handle ingestion first (see `/milestone-brief`).
Phase header: `# Hotfix: <slug>` → `## <step>`.
Chapter markers: mark a chapter at each phase transition and at each numbered step
(session start implicit).
Guest arm (tracking-rules "Collaboration mode"): every `gh pr` read in this
skill — step 1's tier-check and re-entry reads included — carries
`--repo <base-repo>` (the rulebook's slug recipe), since a bare PR number
can resolve against the fork instead of the base repo.

## Workflow

1. **Tier check first.** Reproduce or at least localize the bug. When the
   input is a PR reference instead of a bug report (`#N`, a PR URL, "adopt
   PR 12"), read the contributor's work first — `gh pr view <N>`,
   `gh pr diff <N>` — and tier-check *that* diff. Either way this stays
   a hotfix only if it restores documented behavior and fits one sitting.
   If it needs a design decision, changes exported behavior beyond
   restoring what was documented, or won't fit one sitting — stop: add a
   `candidate` row (or point the close block's next command at
   `/milestone-plan` if it's urgent) and say why.
   An incoming PR over the hotfix bar takes that same
   route and becomes (or joins) a milestone — the disposition is unchanged,
   only the entry point is new. If an active milestone covers this code,
   flag the overlap instead of racing it.
   **Candidate-row match (M249).** Step 1 also finds the candidate rows
   this hotfix fixes. It runs on every entry to step 1, PR-reference
   re-entries included, before any stop this step takes, and never from
   memory. A matched row is a row of `cairn/ROADMAP.md`'s Candidates
   section whose title the argument quotes, or a row that describes the bug
   being fixed. A row's title is its short title (tracking-rules
   "Candidate short title"). For a PR-reference argument, read the PR's
   title, body and `Fixes #N` line against the rows. Name each matched row's title in
   chat, or say that no row matched. A row whose title a live milestone
   file quotes is not matched: that milestone's post-merge hygiene
   graduates it (records-hygiene §1). Within a hotfix, only step 7, after
   a merge, removes or narrows a matched row. A search-first absorb on
   another path can add to the row, but it never removes or narrows it.
   **Closed-PR stop (M266).** A PR-reference argument whose
   `gh pr view <N> --json state,headRefName` reports `CLOSED`, with a head
   branch not matching `m<nnn>-*`, stops here in owner and guest mode. The
   PR closed without a merge, so no walk can merge it. Make the
   candidate-row match above, then skip the tier check and steps 2 to 7.
   In owner mode, remove step 6's merge-guard marker when its line starts
   with `hotfix ` and names that PR (`for PR #<N>`), and leave any other
   marker as it is. The stop edits no candidate row. End with a close block that
   says the PR closed without a merge and that reopening it on GitHub is
   the operator's choice. The close block names each matched row that ends
   with ` — started #<N>`, a dead token that `/cairn-triage` proposes to
   remove. Its fenced next command is `/hotfix` with a description of the
   bug, which starts over on a new branch.
   **Merged-PR re-entry (M172, M174).** A PR-reference argument whose
   `gh pr view <N> --json state,headRefName` reports `MERGED` and a head
   branch not matching `m<nnn>-*` (a hotfix branch or an adopted PR, merged
   outside the session or after a stopped CI wait) states in chat that the
   hotfix bar never ran before this merge, then runs a post-hoc
   verification of the merged diff before step 7 — the hotfix bar holds on
   every path to the default branch, not only the one the session drove:
   - *Tier check* the merged diff (`gh pr diff <N>`) as above. A diff over
     the hotfix bar takes the over-the-bar disposition above with no
     regression test demanded, and step 7's close-out still runs — the
     candidate row or the `/milestone-plan` next command rides in that
     close block; when the PR body carries a `Fixes #N` line, the issue
     close is put to the user as a chip before step 7 runs, never written
     unasked.
   - *Baseline.* The pre-fix baseline is the oid `gh pr view <N> --json
     baseRefOid` reports, cross-checked against the merge commit's first
     parent (`gh pr view <N> --json mergeCommit --jq .mergeCommit.oid`,
     then `git rev-parse <oid>^`); a disagreement is stated in chat,
     `baseRefOid` governing. The current default branch is never the
     baseline: it already carries the fix, so a test passes on both and
     proves nothing.
   - *Regression test*, per step 3's adopting sequence: a test the merged
     diff carries is run on the default branch, checked out and brought up
     to date (fetch, pull ff-only; guest arm: `git fetch <base>` then
     `git merge --ff-only <base>/<default-branch>` — the merged fix is on
     the base repo, not the fork), and in a throwaway worktree of the
     baseline created outside the repo (`git worktree add --detach /tmp/<repo>-verify <baseRefOid>`)
     with only the test file copied in; it must pass on the default branch
     and fail on the baseline. When the merged diff carries no test, or its
     test passes on both, author one on a `hotfix-<slug>` branch cut from
     the up-to-date default branch and prove it the same two ways.
     `git worktree remove` the worktree either way, a failed check included
     (step 3's leftover-worktree hazard).
   - *Gate-lite:* the active profile's `verify` slot on the default branch
     (step 4). A red run the merged diff introduced is a third owed item,
     fixed on the follow-up branch below; one it did not introduce is
     stated in chat and is not this route's to fix.
   - *Changelog:* when the profile's `changelog` slot declares a file and
     the merged diff did not update it, an entry is owed (step 5's
     user-facing-text rule).
   - *Owed items land through the PR path only.* The regression test and
     the changelog entry land on the `hotfix-<slug>` branch (cut here when
     the regression-test move did not) and reach the default branch only
     through step 6's authoring variant — the approval chip, then the push
     and a new PR opened after that approval, or before it where step 6's
     Copilot round arm runs (the merged PR's head branch
     is gone after `--delete-branch`, and step 5's never-a-second-PR clause
     is about that merged PR, not this follow-up) — never by a commit to
     the default branch.
     Step 6's chip for the follow-up PR also carries the merged PR's
     `Fixes #N` close, so the re-entry poses no separate issue-close chip;
     step 7 then runs for the merged PR.
   - *Nothing owed* — test present and two-way proven, `verify` green on the
     default branch, changelog entry present or the slot `none` — pose one
     `AskUserQuestion` chip whose question text names acceptance of the
     post-hoc verification and, when the PR body carries a `Fixes #N` line,
     the issue close it authorizes (a hotfix keeps no work log to show
     whether step 6's chip authorized it, so it is asked once here, and the
     issue-close chip is not posed separately), the recommended option
     accepting and a decline option present. Step 7 runs only on acceptance
     — the candidate-row check, the issue close, then the close block with
     one recap line naming the merged PR and its verification. A decline
     stops with a close block naming the decline and the reason where the
     user gave one, plus a `candidate` row (search-first). In both modes
     the acceptance chip's question text also names each matched row's
     title and says whether step 7 removes the row or narrows it.
   **Open-PR re-entry (M262).** A PR-reference argument whose
   `gh pr view <N> --json state,headRefName,headRefOid,latestReviews,author`
   reports `OPEN` takes one of the two arms below when its conditions
   hold. Any other open PR takes the tier-check walk that opens this step.
   - *Owner arm.* This arm runs in owner mode. Its head branch does not
     match `m<nnn>-*`. Step 6's merge-guard marker starts with `hotfix `
     and names that PR (`for PR #<N>`). Such a marker means that an earlier
     run approved this merge at step 6 and stopped before the merge, most
     often at the CI wait. Quote the marker's line in chat. Make the
     candidate-row match above.
     The run resumes the approved merge only when three conditions hold.
     First, the marker's ` at <oid>` equals the PR's `headRefOid`. Second,
     no entry of `latestReviews` has the state `CHANGES_REQUESTED`, even
     one the user overrode at the earlier chip. Third, the match names
     exactly the rows that the PR body's `Candidate row:` lines name.
     When all three hold, say that the run resumes the approved merge. Skip
     the tier check, steps 2 to 5, and step 6's Copilot round arm,
     PR-conversation read, approval chip, and marker write. Go on at step
     6's CI wait, then the merge with `--match-head-commit <oid>`, then step
     7 as it runs after an approval at step 6's chip. Before the merge,
     read `gh pr view <N> --json isCrossRepository`, and drop
     `--delete-branch` when it is `true` (a fork PR). Step 7's
     off-but-present Copilot rule applies to a resumed authored fix as it
     does to one this run merged.
     If GitHub refuses the merge because the head moved during the wait,
     stop with a close block that names the refusal and the PR's current
     `headRefOid`. Its fenced next command is `/hotfix` with the PR
     reference.
     When a condition fails, or the marker names no head oid, say in chat
     which one. Then take the tier-check walk that opens this step, which ends at step 6's chip. A
     decline at that chip removes the marker (step 6). If the walk stops
     before that chip, remove the marker too.
   - *Guest arm.* This arm runs in guest mode, for an `OPEN` PR whose head
     branch starts with `hotfix-`. Such a PR is the operator's handoff,
     still with the maintainers. Read `gh pr view <N> --repo <base-repo>
     --json state,headRefName,reviewDecision`, and make the candidate-row
     match above. Skip the tier check and steps 2 to 7. Report the PR's
     number, state, and review decision (an empty decision shown as
     `none`). Then stop with a close block. Its CI line says that the
     maintainers' CI on the PR is the check that counts. It also says that
     nothing waits on that CI here. Its fenced next command is `/hotfix`
     with the PR reference, to run after they merge.
   **Own open PR (M266).** This paragraph covers an `OPEN` PR in owner
   mode whose `headRefName` starts with `hotfix-` and whose `author.login`
   equals `gh api user --jq .login`. Such a PR is the operator's own
   authored fix. When the owner arm above does not resume it, the run
   takes the tier-check walk with it as an authored fix whose PR exists,
   not as an adopted PR. Steps 2, 3, and 5 take their adopting variants.
   Step 2 runs `gh pr checkout <N>`, step 3 runs the two-way check of the
   regression test, and step 5 runs the changelog check. Pushes go to the
   PR's head branch, and step 5's contributor fallback does not apply.
   Step 6's Copilot round arm runs for it, with a push to the PR's
   head branch and no `gh pr create`. Step 7's off-but-present rule
   applies to it as to an authored fix this run merged.

2. **Branch — cut one, or adopt the PR's.** Check `git status` (dirty tree
   with unrelated changes → ask).
   *Authoring a fix:* branch `hotfix-<slug>` from the up-to-date default
   branch (detect it per the tracking-rules git model; fetch from `<base>`,
   pull ff-only, push any unpushed local commits — in guest mode the fetch
   is the whole sync, the default branch is never pushed, and the branch is
   cut from `<base>/<default-branch>`, as `/milestone-implement` step 2
   states).
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
   Then apply each per-change rule DESIGN.md's Conventions section states,
   for example a development-version bump on every PR or a NEWS heading
   format. Where
   the Conventions section states none, no version is bumped: cairn never
   bumps one on its own cadence (D-041).
   *Authoring a fix:* nothing is pushed and no PR is opened here — step 6
   pushes and opens the PR after the approval chip, so a
   `pull_request`-triggered suite first runs on the head that merges
   (D-138). Where `cairn/PROFILE.md` opts in to the Copilot review round
   (`skills/shared/copilot-review.md` §1), owner mode opens it before the
   chip instead, at step 6's round arm (D-152).
   *Adopting a PR:* the PR already exists — never open a second one, except
   through the user-gated fallback below. If the
   contributor added an entry, check it against the declared file and the
   user-facing-text rule and edit it in place rather than appending a
   duplicate; if none is present, add one. Hold the PR to the same
   Conventions rules, adding a missing version bump. Push the test, the
   entry, and any convention edits to the PR's head branch — this works on a fork when the contributor left
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
   there, open a PR crediting them (`Co-authored-by:`), its body carrying
   in owner mode the `Candidate row:` lines that step 6 names, and close theirs with
   that comment. Declined → leave their PR open and stop.
   Never merge a fix whose regression test
   is still missing — that is the one gate this path exists to enforce.

6. **Approval gate:** in owner mode, the Copilot round arm runs first.

   **Copilot round arm** (owner mode, an authored fix, the round on per
   `skills/shared/copilot-review.md` §1; D-152). Before the approval
   gate below, push and open the PR the way this step states for an
   approved fix — `git push -u origin hotfix-<slug>`, then `gh pr create
   --title <title> --body <body>` ready, `Fixes #N` in the body when an
   issue exists, and the `Candidate row:` lines the approval paragraph
   below names. Then run the
   round in that module, asking for Lite: the state query (§3), the
   request on `none` (§2), and the bounded wait while the request is
   pending (§4). The PR-conversation read below then runs on this PR,
   which now pre-exists. Each Copilot thread takes the agent's disposition
   under the opt-in line, then the module's reply and resolve (§5), and
   its `copilot:` line and the level line are stated in chat at the chip
   (§6); every other item keeps the four options. A decline at the chip
   closes this PR with `gh pr close <N>` and keeps the branch, and the
   close block names both; a later `/hotfix` for the same bug cuts a new
   branch under a new slug. An adopted PR skips the round: the
   contributor's PR is theirs to put to a reviewer. Step 1's own open PR
   is outside that exemption: the round runs for it, with a push to the
   PR's head branch and no `gh pr create`. With the round off,
   nothing in this arm runs.

   **The gate:** present the diff, the regression-test evidence, and
   the changelog line (when the `changelog` slot declares a file), and
   the version bump when a Conventions rule required one; then,
   only when a PR already exists — an adopted PR, or the PR-reference
   re-entry of an authored fix — run the PR-conversation read
   `/milestone-review` step 7 states — the
   same three paginated reads, the any-author presentation, and the
   changes-requested blocking rule with its override option, except that
   a hotfix keeps its own questions: each item is offered to the user with
   four triage options (fix now / follow-up / reject with reason / noted,
   requests nothing) where review's agent settles them — an adopted
   PR's contributor comments in scope; the hotfix difference is that a
   hotfix keeps no milestone file, so each disposition, and a selected
   override, is stated in the chat presentation beside the item it
   answers, never logged to a Review section or a work log — a hotfix
   keeps neither. An authored fix's PR is opened below, after the chip,
   and is merged with no read — the read runs at most once per hotfix,
   here. With the Copilot round arm above, the PR already exists, so the
   read runs on it, as the module's §5 states. Then put the
   merge authorization to the user as an
   `AskUserQuestion` chip (recommended = merge, e.g. `Merge PR #N to
   <default-branch>` for an existing PR, `Merge hotfix-<slug> into
   <default-branch>` for an authored fix not yet opened — address-first
   instead, when the blocking rule
   above fires — with a decline option) — never a prose yes/no, the same gate discipline
   as `/milestone-review`. A `Fixes #N` line, in the PR body or owed to the
   one about to be opened, adds to the
   chip's question text the post-merge close-if-open of that issue it
   authorizes (hotfix step 7). When step 1 matched a candidate row, the
   question text also names each matched row's title and says whether the
   merge removes the row or narrows it to the part the fix leaves (step 7).
   The guest handoff chip below carries no row text.
   When the gate presents the diff, note the head it shows: local `HEAD`
   for an authored fix not yet pushed, or the PR's `headRefOid` where a PR
   already exists. A decline at the chip removes any merge-guard marker
   that names this PR.
   On approval of an authored fix, push and
   open the PR before the marker write below — `git push -u origin
   hotfix-<slug>`, then `gh pr create --title <title> --body <body>`
   opening it ready for review, never as a draft, `Fixes #N` in the body
   when a GitHub issue exists (the create is skipped when the fix already
   has an open PR — the PR-reference re-entry, or the Copilot round arm —
   where the branch is pushed and the existing PR stands). In owner mode
   the body also carries one `Candidate row: <short title>` line for each
   candidate row that step 1 matched, each line unwrapped and the title
   bare, with no quotes or backticks. The title is cut from the row in
   `cairn/ROADMAP.md` as tracking-rules "Candidate short title" states. While
   the PR is open, the cairn pane in a checkout with no active milestone
   leaves that row out of its Candidates list (M252, M261). The guest arm
   below writes no such line. Merge (`gh pr merge <N> --squash --delete-branch
   --match-head-commit <oid>`, `<oid>` the marker's head oid, so GitHub
   refuses the merge if the head moved after the approval
   — name the PR number explicitly; a bare `gh pr merge` is denied because the
   approval cannot be checked against it; **drop `--delete-branch` on a
   fork PR** — that branch lives in the contributor's repo and is not ours
   to delete)
   only on explicit approval at that chip, with green CI (one foreground
   `gh pr checks <pr> --watch --fail-fast` wait with a timeout below the
   harness ceiling — the tracking-rules wait rule; a call moved to the
   background at the ceiling is reported from fresh `gh pr checks` state,
   stopped with `TaskStop`, and the session stops there with a close block
   whose fenced next command is `/hotfix` with the PR reference — step 1
   re-derives the PR's state: while the PR is still open and the marker
   names it, step 1's open-PR re-entry resumes at this wait (or takes the
   walk again when one of its conditions fails), and for a PR
   merged since, step 1's merged-PR re-entry verifies the merged diff
   post-hoc — and whose CI line (tracking-rules close-block
   shape) states the current check state as read from fresh `gh pr checks`,
   then that rerunning `/hotfix` with the PR reference re-derives that state
   and, when step 1 resumes, waits again, so waiting for green first is optional and never
   required; never left armed,
   never merged past; a PR created moments ago can report no checks before
   GitHub registers them, so where the profile does not declare the repo
   CI-less, re-read `gh pr checks` after a short wait, up to about a
   minute, before taking the no-checks case). In owner mode, on approval, the order is
   fixed: the push and any `gh pr create` above, then the merge-guard
   marker, then the CI wait, then the merge. Write the marker before the
   wait, so a run that stops at the wait leaves it on disk for step 1's
   open-PR re-entry. Just before the marker write, read the head with
   `gh pr view <N> --json headRefOid`. If it differs from the head the gate
   showed, write no marker and stop with a close block that names the new
   head. Its fenced next command is `/hotfix` with the PR reference, which
   takes the new commits through the tier-check walk. The
   marker is `cairn/.merge-approved` (gitignored; one line:
   `hotfix <slug> approved YYYY-MM-DD for PR #<N> at <headRefOid>`, the
   head oid that read returned —
   the marker names the PR it approves, and the guard refuses a merge that
   names a different PR or none) — the plugin's hook denies
   merges to the default branch without it and consumes it per attempt. Write the marker
   in a **separate** step before the `gh pr merge` command — the hook checks
   it before the command runs, so writing it in the same shell line is
   denied. If GitHub refuses the merge because the head no longer matches
   `--match-head-commit`, do not retry it and do not drop the flag,
   whatever the guard's restore note says. Stop
   with a close block that names the refusal and the PR's current
   `headRefOid`. Its fenced next command is `/hotfix` with the PR
   reference. The guard restores the marker, and the rerun finds a moved
   head and takes the walk.
   **Guest arm — the handoff** (tracking-rules "Collaboration mode"): cairn
   never merges in guest mode, so the chip is the same gate with the merge
   taken out — recommended `Hand hotfix-<slug> to the maintainers of
   <base-repo>`, a decline option, no merge option — and on selection the
   sequence is the push to the fork (`git push -u <fork> hotfix-<slug>`,
   `<fork>` being the rulebook's fork remote)
   and the PR opened against the base repo — `gh pr create --repo
   <base-repo> --head <fork-owner>:hotfix-<slug>`, opened ready for their
   review (never a draft, so no later ready-marking step), no cairn
   vocabulary in its title or body, so no `Candidate row:` line (the changelog entry is the branch's
   only prose) — then no marker, no CI wait, no merge. After the create,
   append ` — started #<n>` on disk, `<n>` the new PR's number, to the end
   of each candidate row step 1 matched (tracking-rules "Candidate started
   token"), so the cairn pane in a checkout with no active milestone hides the row while the PR is open. With the Copilot
   review round on (`skills/shared/copilot-review.md` §1), run it next,
   asking for Lite: the state query, the request on `none`, the bounded
   wait while pending, then the Copilot threads by the module's §5. Use
   the module's guest forms: `--repo <base-repo>`, the base repo's owner
   and name in each `gh api` call that addresses a repository (the resolve
   takes only a thread id), and fix pushes to `<fork>`. Its `copilot:`
   lines ride in the close block, which also says that a Copilot review
   arriving after the wait is the operator's to handle by hand. Then
   stop with the close block: the recap says the fix is in the maintainers'
   hands; the CI line says their CI on the PR is the check that counts and
   nothing waits on it here; the fenced next command is `/hotfix` with the
   PR reference, whose step 1 re-derives the PR's state (a hotfix has no
   milestone row to set `blocked`, so the PR itself is the record;
   `/milestone` §2 reports the open PR in its "Open hotfix PRs" bullet).
   With the Copilot round off, this close also follows the off-but-present
   rule (`skills/shared/copilot-review.md` §1).
   Step 7's issue
   close is theirs — the `Fixes` keyword closes it at their merge. The
   handoff changes a matched candidate row only by its started token. Step
   7's guest arm edits it on a later `/hotfix` run with the PR reference,
   after the maintainers merge.

7. If the fix revealed deeper work, add a `candidate` row before closing
   out — sweep first per the search-first candidate-creation rule
   (`tracking-rules.md`, Intake). When the PR body carries a `Fixes #N`
   line, read that issue's state after the merge with
   `gh issue view <N> --json state`; one still open is closed with
   `gh issue close <N> --comment` carrying a one-line comment naming the
   merged PR; a PR with no such line is a no-op here. When `gh` is missing,
   unauthenticated, or the repo has no remote, name which of the three it
   was in the recap — never a failure.
   **Matched candidate rows (M249).** In owner mode, after a merge whose
   diff passed the hotfix bar, edit each row step 1 matched. This covers an
   authored fix, an adopted PR, a re-landed PR, and the merged-PR re-entry
   once its post-hoc verification is accepted, or, where items were owed,
   once the follow-up PR merges. Delete each row that the fix covers in
   full. Narrow each row that the fix covers in part to the part left,
   keeping its title, with a `narrowed YYYY-MM-DD by the PR #N hotfix`
   note, where `#N` is the merged PR that carried the fix. The part left is
   that narrowing, never a second new row. On step 1's over-the-bar
   disposition, step 7 neither removes nor narrows a matched row.
   In owner mode, every ROADMAP edit step 7 makes on any path, the
   candidate row added above included, lands in one docs-only commit on the
   default branch. Run step 2's `git status` check first, then check out
   the default branch, bring it up to date (fetch, pull ff-only), commit,
   and push at once. When step 7 makes no ROADMAP edit, nothing is checked
   out or committed. Show each deleted, narrowed, and new row verbatim in
   chat (the durable-record preview).
   *Guest arm:* the handoff only appends its started token to each matched
   row. When the
   merged-PR re-entry finds that the maintainers merged the PR, and its
   post-hoc verification is accepted, remove or narrow each matched row on
   disk with no commit, judged against the merged diff, and show each
   deleted, narrowed, and new row verbatim in chat. A narrowed row loses
   this hotfix's ` — started #<n>` token and keeps any other token
   (records-hygiene §1). A PR closed without a merge leaves the row.
   If a milestone branch is currently active, remind the user that its
   next implement/review session will merge the default branch into it (the
   branch-sync rule) — nothing to do now. With the Copilot round off, the
   close after an authored fix this run merged also follows the
   off-but-present rule (`skills/shared/copilot-review.md` §1); an adopted
   PR, or the re-entry's already-merged PR, does not, and a follow-up PR
   the re-entry opens and merges does. Step 1's own open PR is outside
   that adopted-PR exemption, so the rule applies to it. End with the close block
   (tracking-rules "Question gates and phase closes"), composed from the
   hotfix's end state — recap of what was fixed and merged, status line,
   fenced next command(s) where any follow-up exists, and the safety line;
   no chip.
