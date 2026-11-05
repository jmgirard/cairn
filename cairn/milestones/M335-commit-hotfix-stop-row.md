# M335: Commit the row a hotfix stop writes

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, GP2
- **Resolves:** —
- **Surface tier:** user-facing — changes what `/hotfix` does in every adopting repo
- **Branch/PR:** —

## Goal

In owner mode, a candidate row that a `/hotfix` step 1 stop writes reaches the default branch in a docs-only commit before the close block, or the close block carries the row and says why it could not.

## Scope

**In:** Absorbs the candidate row "Commit the hotfix over-the-bar row". A stated commit sequence in `skills/hotfix/SKILL.md` step 1 for the row that each stop writes: the over-the-bar route (the owner arm's withdrawn approval included), the open-PR cap stop, and the merged-PR re-entry's decline. What the stop does when the commit cannot be made, and what it does with no remote. The merged-PR re-entry's over-the-bar row lands in step 7's one commit. A changelog entry and a D-entry.

**Out:**
- Guest mode: its row stays on disk with no commit, as now.
- A stop on another branch switching to the default branch to commit: it ends with the close block (work-log line).
- A no-remote rule at step 7: no run reaches step 7 with no remote (ledger in the work log).
- What step 7 does when its own fetch, pull, or commit fails: candidate row "Say what a failed step 7 commit does".
- Any change to `hooks/stop_guard.py`.

## Acceptance criteria

- [ ] AC1: `skills/hotfix/SKILL.md` step 1 states that in owner mode a row that a stop adds or absorbs into lands in one docs-only commit on the default branch before the close block, and that the close block names the commit. It gives these commands in this order, with the row edit between the pull and the add: `git fetch <base>`, `git pull --ff-only <base> <default-branch>`, `git add -- cairn/ROADMAP.md`, `git commit -m "<one-line summary>" -- cairn/ROADMAP.md`, `git push <base> HEAD:<default-branch>`. It names the stops this covers: the over-the-bar route, the owner arm's withdrawn approval included, the open-PR cap stop, and the merged-PR re-entry's decline. It says that in guest mode the row stays on disk with no commit.
- [ ] AC2: Step 1 states the checks that run before the row edit: the checkout is on the default branch, `cairn/ROADMAP.md` has no uncommitted change, and after the fetch and pull the checkout is level with `<base>/<default-branch>`. When a check, the fetch, the pull, the add, or the commit fails, `cairn/ROADMAP.md` ends with no uncommitted change from the stop, by making no edit or, after a failed add or commit, by `git restore --staged --worktree -- cairn/ROADMAP.md`. The close block then shows the row verbatim, names what failed, and fences `/hotfix` with the same argument. When the stop guard blocks on a change the stop did not make, the run leaves that change uncommitted and ends with the same close block. When the push fails or is rejected, the run never forces, and the close block shows the row verbatim and names the local commit and the undo command `git reset --keep HEAD~1`.
- [ ] AC3: Step 1 states that with no remote the run skips the fetch, the pull, the level check, and the push, and that the close block says the commit is local and nothing was pushed.
- [ ] AC4: The merged-PR re-entry's over-the-bar bullet and step 7 each state that step 7 writes that row in its one docs-only commit (guest mode: on disk). That bullet no longer says the row rides in the close block. Step 1's commit sequence states that it does not cover that row.
- [ ] AC5: The AC1 commands, with AC2's restore and undo, run as written in throwaway git repos, give these results. (a) With a bare remote and an uncommitted change in another tracked file, the remote's default branch gains one commit whose only changed path is `cairn/ROADMAP.md`, and the other file stays modified. (b) With the remote one commit ahead, the remote ends with both commits. (c) With no remote, and the fetch, pull, and push skipped, the local default branch gains that same one-path commit. (d) With a staged change in another file, the commit carries only `cairn/ROADMAP.md`, and the other file stays staged. (e) With a local default branch that diverged from the remote, the pull exits nonzero. (f) With a failing pre-commit hook, the commit exits nonzero, and the restore leaves `cairn/ROADMAP.md` with no uncommitted change. (g) With the push rejected because the remote moved, the undo leaves `cairn/ROADMAP.md` with no uncommitted change and another modified file still modified.
- [ ] AC6: For each case below, `skills/hotfix/SKILL.md` and the rulebook it requires decide what the run does. Owner mode unless named: (a) a new bug over the hotfix bar, on the default branch, clean tree, remote present; (b) the same on a milestone branch; (c) the same on the default branch with `cairn/ROADMAP.md` already modified; (d) the same with no remote; (e) a merged PR whose diff is over the bar; (f) a merged PR with nothing owed whose acceptance chip the user declines; (g) a new bug at the open-PR cap, no matched row; (h) that cap stop on a non-default branch; (i) a push rejected after the commit; (j) a failed fetch at the stop; (k) a new bug over the hotfix bar in guest mode.
- [ ] AC7: `CHANGELOG.md`'s Unreleased section has an entry under "Changes that affect existing repos" that says, in owner mode, a row that a `/hotfix` stop writes is now committed and pushed to the default branch, that the close block carries the row when that cannot happen, and that with no remote the commit stays local. Guest mode is named as unchanged.
- [ ] AC8: All five commands of the `verify` slot in `cairn/PROFILE.md` exit 0.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2
- AC5 → T3
- AC6 → T1, T2, T5
- AC7 → T4
- AC8 → T6

## Tasks

- [ ] T1: In `skills/hotfix/SKILL.md` step 1, write the commit sequence, its checks, its failure arms, and its no-remote arm (AC1, AC2, AC3), and point the three stops at it: the stop at lines 45-47, the re-entry's decline at lines 182-183, and the cap stop at line 301. End each `old_string` at a line end when rewrapping.
- [ ] T2: Reword the merged-PR re-entry's over-the-bar bullet (lines 124-130) and step 7's docs-only commit sentence (lines 648-650) for AC4.
- [ ] T3: Run AC5's seven cases in throwaway repos with the commands as the skill now states them, and record the results in one work-log line.
- [ ] T4: Add the CHANGELOG entry. Grep `README.md` and `skills/` for text about a hotfix stop's row and fix what the change makes stale. Append a D-entry that annotates D-042 and D-225 (the close block can be a stop's only record of a row) and records that the work passes D-108's door on its retained trigger.
- [ ] T5: Give a fresh Opus reader `skills/hotfix/SKILL.md`, the rulebook, and AC6's cases, each with its facts in neutral words, and have each answer quote its deciding sentence. Fix any case the text leaves open. After any later edit to a quoted sentence, rerun that case.
- [ ] T6: Run the five `verify` commands, each with its own exit code. Hand-run the `skills/tests` guards that pin this text (`test_hotfix_candidate_graduation`, `test_resume_routing`, `test_external_pr_intake`, `test_idea_vet`), and re-pin what T1 and T2 moved.

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

## Decisions

## Review
