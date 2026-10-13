<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M248: The plan offers to assign you to an issue it resolves, in place of a comment

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes the GitHub write that the plan question set offers every operator
- **Branch/PR:** m248-issue-assign-offer, PR #258 https://github.com/jmgirard/cairn/pull/258   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When a plan resolves a GitHub issue, the question set offers to assign the operator's own account to it, in both modes, and never offers a comment.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the "Issue acknowledgement (one option)" paragraph of `skills/milestone-plan/SKILL.md` step 3 (lines 176-189 on 2026-10-12), which offers `Queued as M<NNN>: <title>` in owner mode and `Working on this: <issue title>` in guest mode. It becomes an assignment offer, gated on the account's access to the repo. Also the README issue-linkage bullet (lines 745-751), a CHANGELOG entry, the guards in `skills/tests/test_issue_linkage.py` and `skills/tests/test_mutation_harness.py`, and the ROADMAP candidate "Intake and guest edges (M234 review)", whose `--body` edge this change removes.

**Out:** the post-merge `partial` comment and the close comment of `/milestone-review` step 9 stay as they are, since they report what shipped. The `/milestone` §4 reply draft stays, since it is a separate offer. Removing the assignment after a merge is not part of this milestone. It stays a manual act on GitHub.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: Step 3 of `skills/milestone-plan/SKILL.md` offers one option to assign the operator's own GitHub account to every issue in the `Resolves:` slot with `gh issue edit <N> --add-assignee @me`, plus `--repo <base-repo>` in guest mode. The paragraph says that the command runs only on selection, after step 4 writes the milestone file, and that the option posts no comment. `grep -n -e "gh issue comment" -e "Queued as" -e "Working on this" skills/milestone-plan/SKILL.md` prints no line.
- [x] AC2: The paragraph says that the agent reads the account's access at the gate with `gh repo view <base-repo> --json viewerPermission`. If the value is below `TRIAGE`, or the read fails, the set poses no assignment option, and the chat says in one line that the account cannot assign on that repo.
- [x] AC3: The paragraph says that the option description names the current assignees of each slotted issue, read with `gh issue view <N> --json assignees` (plus `--repo <base-repo>` in guest mode). If another account holds the issue, the description says so. If the read fails, the description calls the assignees unknown.
- [x] AC4: The paragraph says that if the assign command fails for an issue, or `gh` cannot run at that point, the agent names the issue and the error in chat and in one work-log line, and writes nothing else to GitHub for that issue.
- [x] AC5: The issue-linkage bullet of `README.md` describes the assignment offer and its access gate in both modes, and `grep -n -e "Queued as" -e "Working on this" README.md` prints no line. The Unreleased section of `CHANGELOG.md` has one entry that states the change.
- [x] AC6: The `verify` slot of `cairn/PROFILE.md` is clean on the branch head, and the hand-run `python3 -m unittest discover skills/tests` exits 0.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Rewrite the step-3 paragraph of `skills/milestone-plan/SKILL.md` for AC1-AC4. The assignment covers `closes` and `partial` entries alike.
- [x] T2: Rewrite `TestPlanGateAcknowledgement` and the module docstring in `skills/tests/test_issue_linkage.py`, and the matching entries in `skills/tests/test_mutation_harness.py` (near lines 3161-3177), to pin each AC1-AC4 sentence. Plant the removal of each pinned sentence and see its guard fail.
- [x] T3: Rewrite the README bullet and its guard `test_plan_time_acknowledgement_offer` (with its harness entries near lines 3321-3330), and add the CHANGELOG entry (AC5). Remove the `--body` edge from the ROADMAP candidate "Intake and guest edges (M234 review)".
- [x] T4: Run the `verify` slot and `skills/tests` (AC6).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-12: created by /milestone-plan, from the user's request to replace the "Working on this" comment offer with a self-assignment offer.
- 2026-10-12: collision check: no D-entry or ROADMAP row covers the offer. M166 added it as milestone-local conduct, M234 added the guest body, and the "Intake and guest edges (M234 review)" row's `--body` edge becomes moot (T3). The inbox sweep found 0 open issues and 0 open PRs in jmgirard/cairn.
- 2026-10-12: criteria audit (full mode, fresh Opus reader) returned 7 findings, all fixed: the guest access gap (now AC2), assignee-read fallback and other-assignee cases (AC3), write timing after step 4 and `gh` missing (AC1, AC4), "never otherwise" restated as a property of the paragraph (AC1), `partial` entries (decided in T1), stale guard and ROADMAP sites (T2, T3), and the full `verify` set (AC6).
- 2026-10-12: question set: when the account cannot assign on the repo, what does the plan offer — nothing, with one line saying the account cannot assign.
- 2026-10-12: question set: should owner mode's `Queued as M<NNN>` comment also become an assignment offer — yes, both modes.
- 2026-10-12: plan gate chose to offer no option below `TRIAGE` access over falling back to the "Working on this" comment, because the user wants no post; falsified by a guest operator who loses track of an upstream issue nobody acknowledged.
- 2026-10-12: plan gate chose to assign on `partial` entries as on `closes` entries over skipping them, because the operator works on the issue in both cases and the post-merge `partial` comment still names the remainder; falsified by an operator left assigned to a `partial` issue's remainder they do not mean to take.
- 2026-10-12: implement started on branch m248-issue-assign-offer. The untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-12: T1 done: the step-3 paragraph is now "Issue assignment (one option)". The access read uses `gh repo view <base-repo>` in both modes, since the slug recipe defines `<base-repo>` in both; the guest arm adds `--repo` to the issue view and edit commands only.
- 2026-10-12: T2 done: `TestPlanGateAcknowledgement` became `TestPlanGateAssignment` (7 tests, one a negative check on the retired comment terms) with 12 registry entries, one per pinned line. The registry test passes with each line blanked in turn; `verify` is clean (5 of 5 exit 0).
- 2026-10-12: T3 done: README bullet and its guard (now `test_plan_time_assignment_offer`, 3 registry entries) rewritten, CHANGELOG entry added, and the `--body` edge removed from the "Intake and guest edges (M234 review)" row. The README text uses two sentences where the old one used an em dash.
- 2026-10-12: T4 done: `verify` 5 of 5 exit 0, `skills/tests` 736 tests OK, `cairn_validate` exit 0.
- 2026-10-12: claim audit: 30 claims read, 2 corrected — skills/milestone-plan/SKILL.md (`NONE` is not a `viewerPermission` value, now "`READ` or empty"), CHANGELOG.md and README.md (now say a failed access read also offers nothing). The same reader re-read both and found them accurate; guards and one new README registry entry follow the new text, and `verify` plus `skills/tests` exit 0.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

- 2026-10-12 (review): M248 replaces the plan-time acknowledgement comment, a milestone-local choice of M166 with M234's guest body, by an offer to assign the operator, in both modes, at the user's request at the M248 question set. Below triage access the plan offers nothing. The cost is that an operator with read access only, the usual guest case, leaves no mark on the upstream issue at plan time, which M166's comment did. The falsifier is the plan-gate work-log line on the guest case.

## Review
<!-- owner: review · exclusive. -->

Review pass 1, 2026-10-12, on branch head 1e7fa897 plus the PR record commit. PR #258 opened at review start (Copilot round on); Copilot requested on state `none`.

- AC1 evidence: `skills/milestone-plan/SKILL.md:177-196` read: one option assigns the operator's own account to every slotted issue (177-178), "The option posts no comment." (180), the command runs only on selection after step 4 writes the file with `gh issue edit <N> --add-assignee @me` (189-190), and the guest arm adds `--repo <base-repo>` to the edit (195-196). `grep -n -e "gh issue comment" -e "Queued as" -e "Working on this" skills/milestone-plan/SKILL.md` printed no line (exit 1).
- AC2 evidence: lines 181-185 read: `gh repo view <base-repo> --json viewerPermission`, and below `TRIAGE` (`READ` or empty) or a failed read poses no option and says in one line that the account cannot assign on that repo.
- AC3 evidence: lines 185-189 read: assignees read with `gh issue view <N> --json assignees` (guest `--repo` at 195-196), the description names them, says so when another account holds an issue, and calls them unknown on a failed read.
- AC4 evidence: lines 191-194 read: a failed assign command or `gh` unable to run names the issue and the error in chat and in one work-log line, and writes nothing else to GitHub for that issue.
- AC5 evidence: `README.md:745-754` describes the assignment offer and the access read "in owner and guest mode alike"; `grep -n -e "Queued as" -e "Working on this" README.md` printed no line (exit 1). The Unreleased section of `CHANGELOG.md` opens with the one entry "The plan offers to assign you to an issue it resolves, in place of a comment."
- AC6 evidence: `verify` all exit 0 (scripts/tests 407 tests, hooks/tests 175 tests, plugin validate, marketplace validate, plugin test); hand-run `skills/tests` 736 tests OK, exit 0.
- Consistency gate: `cairn_validate` all checks passed (exit 0); no principle changed, so `cairn_impact` skipped; marketplace validate shows no `version` warning; the changelog entry names no milestone number (its `M<NNN>` is the retired comment's placeholder).
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the "cannot assign" line is pre-tool-call chat and can go unseen, with no work-log line — fix now: the line rides in a question's text or the turn's final text, and step 4 logs it, fixed f85b04dd
- diff-bug #2: a failed access read is reported as a permission fact — fix now: the line names the read's failure where the read failed, fixed f85b04dd
- diff-bug #3: the assign command's timing relative to step 6's commit is open — fix now: it runs before step 6's commit, so its work-log line rides in that commit, fixed f85b04dd
- diff-bug #4: "can pose" is weaker than AC1's "offers" — fix now: "poses ... unless the access read below withholds it", fixed f85b04dd
- diff-bug #5: GitHub can drop an ineligible assignee with exit 0 — fix now: the agent re-reads the assignees after the command, and a missing account counts as a failed command, fixed f85b04dd
- diff-bug #6: README "in owner and guest mode alike" unguarded — fix now: pinned in `test_plan_time_assignment_offer` with a registry entry, fixed f85b04dd
- diff-bug #7: "`closes` and `partial` entries alike" unguarded — fix now: pinned with a registry entry, fixed f85b04dd
- diff-bug #8: the CHANGELOG entry has no guard and an odd wrap — reject (style): changelog entries are not prose-guarded in this repo, the behavior they state is pinned in the skill guards, and the wrap is cosmetic
- diff-bug #9: the retired-terms check covers only the plan skill — fix now: it also checks README for the two retired bodies (README keeps `gh issue comment` for the `/milestone` reply draft), fixed f85b04dd
- diff-bug #10: with the fork at `origin` and no `upstream`, the access read reads the fork — follow-up: added to the existing fork edge in "Intake and guest edges (M234 review)"
- diff-bug #11: a `partial` issue keeps the operator assigned after merge — reject (planned change): Scope Out and the plan-gate line record it
- blame-history #1: guest acknowledgement mostly disappears for read-only contributors — reject (planned change): the user chose "offer nothing" at the question set; the cost is now a milestone-local Decisions entry
- blame-history #2: owner mode loses the `Queued as` comment, partly rebuilding M166's falsifier as a hard rule — reject (planned change): the user chose both modes at the question set
- blame-history #3: no Decisions entry records the reversal — fix now: milestone-local Decisions entry added, fixed f85b04dd
- blame-history #4: `partial` issues stay assigned after merge — reject (planned change): Scope Out
- blame-history #5: `@me` may need a newer `gh` — reject (false): `gh issue edit --help` documents `@me`, and a failure takes the failed-command path
- blame-history #6: the ROADMAP `--body` edge removal leaves review step 9's `--body` comment — reject (false): no defect, that row never named step 9's comment
- blame-history #7: test pins match the new text — noted, no finding
- prior-review #1: run-time reads and the edit use only `<N>` and `<base-repo>`, no issue text — reject (false): the lens itself found no regression
- prior-review #2-#6: retired text gone, harness entries complete, guest `--repo` kept, no baseline to re-seed, README and SKILL agree — noted, no finding
- Re-verify after fix-now commit f85b04dd: `verify` 5 of 5 exit 0, `skills/tests` 738 tests OK, `cairn_validate` exit 0; AC1-AC4 text re-read at `skills/milestone-plan/SKILL.md:176-201`, unchanged in substance and extended by the fixes; the AC1 and AC5 greps still print no line.
- copilot: skills/milestone-plan/SKILL.md:184 — `viewerPermission` can be `NONE`, outside the "`READ` or empty" list — fix now: the gate names the allowed values (`ADMIN`, `MAINTAIN`, `WRITE`, `TRIAGE`), fixed dc0eb45f
- copilot: cairn/milestones/M248-issue-assign-offer.md:14 (outdated) — the header carried only the branch name — fix now, fixed 504faadb (the header names PR #258 since the start of review)
- copilot: cairn/milestones/M248-issue-assign-offer.md:53 — checked-off tasks name the retired test class and old line range — reject (false): the tasks name what they rewrote as it stood at plan time, and the work log records the new names
- copilot: review body — the index of the three threads above, and a review effort line — noted
- Copilot level: Lite (set by GitHub's settings); the review covered head 1e7fa897, before the fix-now commits.
- conversation: PR #258 — no conversation comments; the one review is Copilot's (above).
- Re-verify after dc0eb45f: `verify` 5 of 5 exit 0, `skills/tests` 738 tests OK.
