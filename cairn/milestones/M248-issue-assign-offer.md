<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M248: The plan offers to assign you to an issue it resolves, in place of a comment

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes the GitHub write that the plan question set offers every operator
- **Branch/PR:** m248-issue-assign-offer   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When a plan resolves a GitHub issue, the question set offers to assign the operator's own account to it, in both modes, and never offers a comment.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the "Issue acknowledgement (one option)" paragraph of `skills/milestone-plan/SKILL.md` step 3 (lines 176-189 on 2026-10-12), which offers `Queued as M<NNN>: <title>` in owner mode and `Working on this: <issue title>` in guest mode. It becomes an assignment offer, gated on the account's access to the repo. Also the README issue-linkage bullet (lines 745-751), a CHANGELOG entry, the guards in `skills/tests/test_issue_linkage.py` and `skills/tests/test_mutation_harness.py`, and the ROADMAP candidate "Intake and guest edges (M234 review)", whose `--body` edge this change removes.

**Out:** the post-merge `partial` comment and the close comment of `/milestone-review` step 9 stay as they are, since they report what shipped. The `/milestone` §4 reply draft stays, since it is a separate offer. Removing the assignment after a merge is not part of this milestone. It stays a manual act on GitHub.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: Step 3 of `skills/milestone-plan/SKILL.md` offers one option to assign the operator's own GitHub account to every issue in the `Resolves:` slot with `gh issue edit <N> --add-assignee @me`, plus `--repo <base-repo>` in guest mode. The paragraph says that the command runs only on selection, after step 4 writes the milestone file, and that the option posts no comment. `grep -n -e "gh issue comment" -e "Queued as" -e "Working on this" skills/milestone-plan/SKILL.md` prints no line.
- [ ] AC2: The paragraph says that the agent reads the account's access at the gate with `gh repo view <base-repo> --json viewerPermission`. If the value is below `TRIAGE`, or the read fails, the set poses no assignment option, and the chat says in one line that the account cannot assign on that repo.
- [ ] AC3: The paragraph says that the option description names the current assignees of each slotted issue, read with `gh issue view <N> --json assignees` (plus `--repo <base-repo>` in guest mode). If another account holds the issue, the description says so. If the read fails, the description calls the assignees unknown.
- [ ] AC4: The paragraph says that if the assign command fails for an issue, or `gh` cannot run at that point, the agent names the issue and the error in chat and in one work-log line, and writes nothing else to GitHub for that issue.
- [ ] AC5: The issue-linkage bullet of `README.md` describes the assignment offer and its access gate in both modes, and `grep -n -e "Queued as" -e "Working on this" README.md` prints no line. The Unreleased section of `CHANGELOG.md` has one entry that states the change.
- [ ] AC6: The `verify` slot of `cairn/PROFILE.md` is clean on the branch head, and the hand-run `python3 -m unittest discover skills/tests` exits 0.

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

## Review
<!-- owner: review · exclusive. -->
