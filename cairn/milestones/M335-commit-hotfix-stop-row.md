# M335: Commit the row a hotfix stop writes

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, GP2
- **Resolves:** —
- **Surface tier:** user-facing — changes what `/hotfix` does in every adopting repo
- **Branch/PR:** m335-commit-hotfix-stop-row, https://github.com/jmgirard/cairn/pull/350

## Goal

In owner mode, a candidate row that a `/hotfix` step 1 stop writes reaches the default branch in a docs-only commit before the close block, or the close block carries the row and says why it could not.

## Scope

**In:** Absorbs the candidate row "Commit the hotfix over-the-bar row". A stated commit sequence in `skills/hotfix/SKILL.md` step 1 for the row that each stop writes: the over-the-bar route (the owner arm's withdrawn approval included), the open-PR cap stop, and the merged-PR re-entry's decline. What the stop does when the commit cannot be made, and what it does with no remote. The merged-PR re-entry's over-the-bar row lands in step 7's one commit. The open-PR cap stop says it pushes no work branch, in step 1 and in the rulebook, since its row now takes a docs-only push. A changelog entry and a D-entry.

**Out:**
- Guest mode: its row stays on disk with no commit, as now.
- A stop on another branch switching to the default branch to commit: it ends with the close block (work-log line).
- A no-remote rule at step 7: no run reaches step 7 with no remote (ledger in the work log).
- What step 7 does when its own fetch, pull, or commit fails: candidate row "Say what a failed step 7 commit does".
- Any change to `hooks/stop_guard.py`.

## Acceptance criteria

- [x] AC1: `skills/hotfix/SKILL.md` step 1 states that in owner mode a row that a stop adds or absorbs into lands in one docs-only commit on the default branch before the close block, and that the close block names the commit. It gives these commands in this order, with the row edit between the pull and the add: `git fetch <base>`, `git pull --ff-only <base> <default-branch>`, `git add -- cairn/ROADMAP.md`, `git commit -m "<one-line summary>" -- cairn/ROADMAP.md`, `git push <base> HEAD:<default-branch>`. It names the stops this covers: the over-the-bar route, the owner arm's withdrawn approval included, the open-PR cap stop, and the merged-PR re-entry's decline. It says that in guest mode the row stays on disk with no commit.
- [x] AC2: Step 1 states the checks that run before the row edit: the checkout is on the default branch, `cairn/ROADMAP.md` has no uncommitted change, and after the fetch and pull the checkout is level with `<base>/<default-branch>`. When a check, the fetch, the pull, the add, or the commit fails, `cairn/ROADMAP.md` ends with no uncommitted change from the stop, by making no edit or, after a failed add or commit, by `git restore --staged --worktree -- cairn/ROADMAP.md`. The close block then shows the row verbatim, names what failed, and fences `/hotfix` with the same argument. When the stop guard blocks on a change the stop did not make, the run leaves that change uncommitted and ends with the same close block. When the push fails or is rejected, the run never forces, and the close block shows the row verbatim and names the local commit and the undo command `git reset --keep HEAD~1`.
- [x] AC3: Step 1 states that with no remote the run skips the fetch, the pull, the level check, and the push, and that the close block says the commit is local and nothing was pushed.
- [x] AC4: The merged-PR re-entry's over-the-bar bullet and step 7 each state that step 7 writes that row in its one docs-only commit (guest mode: on disk). That bullet no longer says the row rides in the close block. Step 1's commit sequence states that it does not cover that row.
- [x] AC5: The AC1 commands, with AC2's restore and undo, run as written in throwaway git repos, give these results. (a) With a bare remote and an uncommitted change in another tracked file, the remote's default branch gains one commit whose only changed path is `cairn/ROADMAP.md`, and the other file stays modified. (b) With the remote one commit ahead, the remote ends with both commits. (c) With no remote, and the fetch, pull, and push skipped, the local default branch gains that same one-path commit. (d) With a staged change in another file, the commit carries only `cairn/ROADMAP.md`, and the other file stays staged. (e) With a local default branch that diverged from the remote, the pull exits nonzero. (f) With a failing pre-commit hook, the commit exits nonzero, and the restore leaves `cairn/ROADMAP.md` with no uncommitted change. (g) With the push rejected because the remote moved, the undo leaves `cairn/ROADMAP.md` with no uncommitted change and another modified file still modified.
- [x] AC6: For each case below, `skills/hotfix/SKILL.md` and the rulebook it requires decide what the run does. Owner mode unless named: (a) a new bug over the hotfix bar, on the default branch, clean tree, remote present; (b) the same on a milestone branch; (c) the same on the default branch with `cairn/ROADMAP.md` already modified; (d) the same with no remote; (e) a merged PR whose diff is over the bar; (f) a merged PR with nothing owed whose acceptance chip the user declines; (g) a new bug at the open-PR cap, no matched row; (h) that cap stop on a non-default branch; (i) a push rejected after the commit; (j) a failed fetch at the stop; (k) a new bug over the hotfix bar in guest mode.
- [x] AC7: `CHANGELOG.md`'s Unreleased section has an entry under "Changes that affect existing repos" that says, in owner mode, a row that a `/hotfix` stop writes is now committed and pushed to the default branch, that the close block carries the row when that cannot happen, and that with no remote the commit stays local. Guest mode is named as unchanged.
- [x] AC8: All five commands of the `verify` slot in `cairn/PROFILE.md` exit 0.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2
- AC5 → T3
- AC6 → T1, T2, T5, T7
- AC7 → T4
- AC8 → T6

## Tasks

- [x] T1: In `skills/hotfix/SKILL.md` step 1, write the commit sequence, its checks, its failure arms, and its no-remote arm (AC1, AC2, AC3), and point the three stops at it: the stop at lines 45-47, the re-entry's decline at lines 182-183, and the cap stop at line 301. End each `old_string` at a line end when rewrapping.
- [x] T2: Reword the merged-PR re-entry's over-the-bar bullet (lines 124-130) and step 7's docs-only commit sentence (lines 648-650) for AC4.
- [x] T3: Run AC5's seven cases in throwaway repos with the commands as the skill now states them, and record the results in one work-log line.
- [x] T4: Add the CHANGELOG entry. Grep `README.md` and `skills/` for text about a hotfix stop's row and fix what the change makes stale. Append a D-entry that annotates D-042 and D-225 (the close block can be a stop's only record of a row) and records that the work passes D-108's door on its retained trigger.
- [x] T5: Give a fresh Opus reader `skills/hotfix/SKILL.md`, the rulebook, and AC6's cases, each with its facts in neutral words, and have each answer quote its deciding sentence. Fix any case the text leaves open. After any later edit to a quoted sentence, rerun that case.
- [x] T6: Run the five `verify` commands, each with its own exit code. Hand-run the `skills/tests` guards that pin this text (`test_hotfix_candidate_graduation`, `test_resume_routing`, `test_external_pr_intake`, `test_idea_vet`), and re-pin what T1 and T2 moved.
- [x] T7: Review return 1: name the close block's next command once step 7 writes the row (AC6), and make the fix-now items that the return's work-log line lists.

## Work log

- 2026-11-05: created by /milestone-plan.
- 2026-11-05: tier check: not run — work named at the question set
- 2026-11-05: idea vet: no flaw. gap: the row names one stop, but the cap stop and the re-entry's decline write a row with no commit too; reading taken: cover all three. gap: what happens when the commit cannot be made; reading taken: no edit and the close block carries the row, since an uncommitted row is what the row complains of. gap: no remote; reading taken: commit locally and say nothing was pushed. gap: the row asks for a no-remote rule at step 7, but a merge needs a PR and an authored fix with no remote stops at the cap's failed read, so no run reaches step 7 with no remote; reading taken: the rule sits at step 1, the one place such a run reaches, with no user-visible difference.
- 2026-11-05: lessons used: 2026-10-29 (M324), 2026-10-29 (M325), 2026-10-31 (M328), 2026-11-02 (M329), 2026-11-02 (M330), 2026-11-02 (M331), 2026-07-24 (M112), 2026-08-17 (M148), 2026-07-16 (M56+M65)
- 2026-11-05: collision: candidate row "Commit the hotfix over-the-bar row" absorbed. D-108 passes on its retained trigger, a defect in shipped behavior: the owner-mode stop ends with an uncommitted row, `hooks/stop_guard.py` blocks that turn end, and the skill names no commit. D-225's close-block record of a flaw stands, and the fallback here is a further residual of D-042's rule (T4's D-entry). IP1 is not in conflict: the git model accepts docs-only commits on the default branch.
- 2026-11-05: inbox sweep: 0 open issues, 0 open PRs, nothing to dispose.
- 2026-11-05: plan gate chose committing only when the checkout is on the default branch over switching to it and back, because `/milestone-plan`'s trivial route does the same, switching adds a stop point, and a worktree session could not switch anyway; falsified by a real stop on another branch whose close-block row was lost.
- 2026-11-05: plan gate chose no edit plus the close block over leaving the row uncommitted on disk, because the stop guard blocks an uncommitted row and tells the session to commit it; falsified by a user who lost a row that a file on disk would have kept.
- 2026-11-05: plan gate chose `git reset --keep HEAD~1` as the undo over the trivial route's `--soft`, because `--soft` leaves the row staged, which the stop guard blocks and a rerun's ROADMAP check fails; falsified by AC5's case (g) failing.
- 2026-11-05: criteria audit (full, fresh Opus reader): 11 findings, all taken: undo leaves the row staged; guard block on an earlier change; Goal wider than AC4's route; AC6 bound an evidence quotation; AC6 cases lacked deciding facts; AC5's merge probe never reached the commit; probes did not vary the remote state or the stops; AC5 bound a location; `git add` missing from the failures; AC3's step 7 half unreachable (see the idea vet); "one paragraph" bound layout.
- 2026-11-05: remainder: step 7's own fetch, pull, or commit failure has no stated arm, found by the audit, and goes to the parked candidate row "Say what a failed step 7 commit does".
- 2026-11-05: changelog: one entry under Unreleased (AC7); test scope: no new prose guard, per the profile's test-doctrine; AC5 and AC6 are the evidence.
- 2026-11-05: T1, T2 done: step 1 gains the **Row at a stop** paragraph, and the over-the-bar stop's two other row writers point at it; the re-entry bullet and step 7 say step 7 writes that row. Suites green; the mod test runs at T6, since this checkpoint changes no `hooks/` code.
- 2026-11-05: the simple-english lint hook reports 203 hits on `skills/hotfix/SKILL.md`, the same count as main; the text is unchanged outside this milestone's lines, so those hits stay.
- 2026-11-05: T3 done: AC5's seven cases ran in throwaway repos with the skill's commands, 14 of 14 checks passed (script in the session scratchpad, not committed).
- 2026-11-05: T4 done: CHANGELOG entry; D-240; the sweep of `README.md` and `skills/` found nothing stale, since README's `/hotfix` row names the candidate row and no commit.
- 2026-11-05: substantive amendment: Scope In gains "The open-PR cap stop says it pushes no branch, in step 1 and in the rulebook, since its row now takes a docs-only push." The T5 reader found that the cap stop's "push nothing" conflicts with the row's push; no criterion changes; the rulebook baseline is re-seeded in its three places.
- 2026-11-05: T5 first reader pass: all cases decided in the row's handling. Fixed: the cap stop's push conflict; a fence for each stop (`/milestone-plan` with the row's short title unless the stop names its own, `/hotfix` after a rejected push and undo); other uncommitted paths on the success route; a row that needs no edit. Left as they were, since they predate this work and the row does not touch them: the re-entry's gate-lite and changelog wording, its "no regression test demanded" against a vet flaw, and a sweep rerun after the pull. Left because the rulebook settles them: docs-only commits need no approval chip, and a preview adds no stop.
- 2026-11-05: T5 second reader pass (cases a, d, f, g, i, k, plus an unrelated dirty file and a row that needs no edit): no case open. The rulebook's "dirty tree means ask" against step 1's "with no question" stays, since `/milestone-plan`'s trivial route commits past other paths the same way and step 1's sentence is explicit.
- 2026-11-05: claim audit: 29 claims read, 4 corrected — CHANGELOG.md, skills/hotfix/SKILL.md (the cap's failed read, a push-only failure, the guest fence, a failed restore); the loose "pushes no branch" also became "pushes no work branch" (Scope In follows; rulebook baseline re-seeded to 894 lines / 88,669 bytes); the one re-read found all corrected claims true, and case (g) has no conflict.
- 2026-11-05: T6 done: `skills/tests` hand-run green after two re-pins and the baseline re-seed; verify run on the final text.
- 2026-11-05: review return 1: AC6 case (e) is open, since no sentence names the close block's next command once step 7 writes the row. Also owed from pass 1's fix-now list in the Review section: README's cap sentence; a recipe that names no branch; the row read moved after the level check; the fence made owner mode only (CHANGELOG too); "the same close block" reworded; the rulebook's exception for other uncommitted paths with its baseline re-seed; the parked row "Keep staged files on a row push undo".
- 2026-11-05: T7 done: step 7 names the close block's next command; step 1's row read follows the level check, a recipe with no branch counts as a failed check, and the fence is owner mode only; README, CHANGELOG, and the rulebook follow; baseline re-seeded to 894 lines / 88,741 bytes.
- 2026-11-05: claim audit: 16 claims read, 2 corrected — CHANGELOG.md, README.md (the guest sentence; the cap's row names its matched-row and failed-read cases); the step 7 fence became owner mode only, so guest mode stays as it was. Scope: the lines added since the first audit.

## Decisions

## Review

**Pass 1 (2026-11-05, head b2ad9109).**

- AC1: a script checked each named property and site against `skills/hotfix/SKILL.md` step 1, 10 of 10 present, command order included.
- AC2: same script, 10 of 10.
- AC3: same script, 2 of 2.
- AC4: same script, 4 of 4.
- AC5: the seven cases ran in throwaway repos with the skill's commands, 14 of 14 checks passed.
- AC6: a fresh Opus reader decided ten of eleven cases from the text. Case (e) is open: no sentence names the close block's next command once step 7 writes the row. AC6 not met, so its box stays unticked.
- AC7: same script, 6 of 6.
- AC8: all five `verify` commands exit 0; the mod test ran 2466 tests with 0 fails.
- Consistency gate: `cairn_validate` passes with the one sizing advisory; the marketplace output has no `plugins[N].version` warning; the changelog has its entry.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: README's "At the cap they push nothing" is false for `/hotfix` — fix now
- diff-bug #2: the recipe has no arm when it yields no default branch — fix now
- diff-bug #3: the "row already holds" read comes before the pull, so a row that landed upstream can be duplicated — fix now
- diff-bug #4: the both-modes fence and two other additions are outside the plan and conflict with "Guest mode… as now" — fix now: the fence becomes owner mode only; the other two are details of AC1 and AC2's commit
- diff-bug #5: `git reset --keep HEAD~1` unstages another file's staged change — follow-up: new parked row "Keep staged files on a row push undo", promote when a user reports it, since only a rejected push with an unrelated staged file reaches it and nothing is lost
- diff-bug #6: a rerun without the undo finds the row and makes no edit, so the unpushed commit goes unreported — fix now: moving the row read after the level check sends that rerun to the failure arm
- diff-bug #7: "the same close block" reads as the push-failure block — fix now
- diff-bug #8: "with no question" conflicts with the rulebook's dirty-tree rule — fix now: the rulebook names the exception
- diff-bug #9: `hooks/commit_guard.py` can nudge falsely when another file is staged — reject, edge: only an unrelated staged file at a stop reaches it, outside common use, and the effect is a warning that does not block
- diff-bug #10: the `/hotfix` fence after a failure repeats the tier check and can re-pose a chip — reject, edge: only a failed commit at a stop reaches it, outside common use, and the effect is repeated work
- diff-bug #11: on a protected default branch every row push is rejected — follow-up: absorbed by the existing parked row "Support a protected default branch", which holds that case already
- diff-bug #12: the "if it's urgent" arm overlaps the new fence — reject, style: both name `/milestone-plan`, and the arm predates this work
- diff-bug #13: the over-the-bar row sits under the matched-rows heading — reject, style: the sentence and its parenthetical state the rule
- diff-bug #14: AC5's script and AC6's answers are not in the repo — reject, false: the Review section records results, and the rulebook bars pasted output
- diff-bug #15: D-240's falsifiers are folded into Rejected — reject, style
- diff-bug #16: the "(owner mode)" label heads a paragraph with a guest sentence — reject, style
- blame-history #1: the default-branch push has no approval step — reject, false: the git model accepts docs-only commits there and says to push them immediately
- blame-history #2: D-240 says guest mode is unchanged but the skill changes it — fix now: same fix as diff-bug #4
- blame-history #3: the re-entry bars default-branch commits for owed items — reject, false: that rule covers the test and the changelog entry, not a candidate row
- blame-history #4: "pushes no work branch" narrows M315's rule — reject, planned change: Scope In names it after the amendment
- blame-history #5: the stop can ask a question with no remote — reject, false: the recipe's question names the branch, and the skip covers only the four named steps
- prior-review #1: the cap stop's push loosens M262's guard with no pin — reject, planned change: the profile owes no new prose guard
- prior-review #2: other uncommitted paths at a stop can leak — reject, false: the pathspec commit carries only `cairn/ROADMAP.md`
- prior-review #3: the stop does not state what happens off the default branch — reject, false: the first check fails and the failure arm states the rest
- ripple #1: README's cap sentence — fix now: same fix as diff-bug #1
- ripple #2: `/milestone-review` still says "push nothing" at the cap — reject, false: it writes no row, so that holds for it
- ripple #3: `skills/hotfix/SKILL.md`'s "and nothing is pushed" on the change route — reject, false: that route is guest mode, where the row stays on disk
- ripple #4: the ROADMAP still lists the absorbed row — reject, false: hygiene removes it at merge
- copilot: skills/hotfix/SKILL.md:74 — fix now: same fix as diff-bug #8; comment and resolve wait for the next pass
- Return floor: AC6 fails inside its domain, so the milestone returns (`review return 1`).
- Pass 1's fix-now items: all fixed 9f967cb8 and 707c7ffa, return 1's T7.

**Pass 2 (2026-11-05, head 60f21049 and its record commit).**

- AC1: the text script ran again, 10 of 10.
- AC2: 10 of 10; the stop-guard sentence now ends "the close block that this paragraph gives for the stop's outcome".
- AC3: 2 of 2; the close block now says "any commit is local".
- AC4: 4 of 4.
- AC5: the seven cases ran again, 14 of 14 checks passed.
- AC6: a fresh Opus reader decided all eleven cases with none open, and step 7's fence now decides case (e). A second fresh reader reran cases (b), (c), (d), and (j) after pass 2's edit to their sentences, with none open.
- AC7: 6 of 6, and the entry names no milestone number.
- AC8: all five `verify` commands exit 0 at 60f21049; the mod test ran 2466 tests with 0 fails; `skills/tests` hand-run green.
- Consistency gate: `cairn_validate` passes with the one sizing advisory; no `plugins[N].version` warning; the changelog has its entry; no changed snapshot files; no check runs on the PR, and the profile says this repo has no CI.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the failure arm's `/hotfix` fence reruns from the same checkout with no word on switching branches — fix now, fixed 60f21049
- diff-bug #2: a resume on the PR's head branch takes the failure arm, so the withdrawn approval's row rarely commits — reject, planned change: AC1 and AC2 state both
- diff-bug #3: a rejected step 7 push has no arm and no row names it — follow-up: extends the parked row "Say what a failed step 7 commit does", fixed 60f21049
- diff-bug #4: the re-entry bullet's "or" sits beside step 7's fence — reject, style: the urgent arm writes no row, and a row takes the fence
- diff-bug #5: step 7's over-the-bar row sentence has no search-first clause — reject, false: step 7 opens with that sweep
- diff-bug #6: with no remote and the row already present, the close block claims a local commit — fix now, fixed 60f21049
- diff-bug #7: a rerun without the undo names a level-check failure, not the stranded commit — reject, edge: only ignoring the fence's "after the undo" reaches it, outside common use, and the effect is a stop with an error
- diff-bug #8: after a failed restore the guard blocks on the stop's own edit — reject, edge: only a held index lock reaches it, outside common use, and the effect is a warning
- diff-bug #9: the CHANGELOG's "the stop writes nothing" is loose after a failed add or commit — fix now, fixed 60f21049
- diff-bug #10: README's cap sentence states no failure case — reject, style: the CHANGELOG entry has the detail
- blame-history #1: the row commit reaches the default branch with no approval at a gate, reopening pass 1's disposition — reject, false: the git model's first bullet accepts docs-only commits and says to push them immediately, and the plan and hygiene commits do so; shown at the merge question for the user's call
- blame-history #2: the dirty-tree exception — reject, false: settled at pass 1, fixed by T7
- blame-history #3: "pushes no work branch" — reject, planned change: settled at pass 1
- prior-review #1: `/milestone-review`'s cap sites still say "push nothing" — reject, false: a review writes no row at the cap, so that holds for it
- prior-review #2: Copilot's thread is answered by the diff — noted
- ripple #1: rulebook line 343 and IP1 against the row commit — reject, false: same as blame-history #1
- ripple #2: `skills/hotfix/SKILL.md`'s "and nothing is pushed" — reject, false: the change route is guest mode, settled at pass 1
- ripple #3: step 2's "ask" against step 1's "with no question" — reject, false: step 2 cuts a branch, and the rulebook names the stop's exception alone
- ripple #4: the rulebook's guest "no docs-only commit" — reject, false: that bullet is guest mode, where the row stays on disk
- ripple #5: leaving a change uncommitted at a turn end against "stop points are commit points" — reject, planned change: AC2 states it for a change the stop did not make
- ripple #6: `/milestone-review`'s "push nothing" — reject, false: same as prior-review #1
- ripple #7: the ROADMAP still lists the absorbed row — reject, false: hygiene removes it at merge
- ripple #8: "88,669" gone, 88,741 matches — noted
- conversation: PR #350 has no human review, comment, or thread; Copilot's review is the only item.
- copilot: skills/hotfix/SKILL.md:74 — fixed 9f967cb8
- copilot: https://github.com/jmgirard/cairn/pull/350#pullrequestreview-5780908497 — no comment
- Copilot level: Lite (set by GitHub's settings)
