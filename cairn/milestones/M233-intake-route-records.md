# M233: Issue intake routes keep their records and read the right repo

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — it edits shipped skill prose and the rulebook that adopting repos run
- **Branch/PR:** —

## Goal

Close three issue-intake gaps from the M232 review, so that no issue route leaves a new idea recorded only on GitHub or reads the wrong repo.

## Scope

**In:** the `/milestone` §4 `reply` verdict's rule for a declined request, in owner and guest mode. The rulebook's Intake paragraph names the reply and `/milestone-plan` routes. `/milestone-plan` step 2's inbox reads name `<base-repo>`. Also a D-entry annotating D-044, prose guards, the rulebook-mass re-seed, a CHANGELOG entry, and one README sentence.

**Out:** these stay on the candidate row "Issue look-in edges (M232 review)":

- the look-in reply hand-off's `'\''` quoting in PowerShell,
- `/hotfix` naming no `issue <URL>` argument form,
- closing an orphaned issue from the look-in,
- the `<fork-owner>` recipe reading `origin`,
- `/milestone` §2's orphan and outside-merges reads carrying no `--repo` (added to that row at this plan).

## Acceptance criteria

- [ ] AC1: `skills/milestone/SKILL.md` §4 gives the `reply` verdict to a request the project declines only when a record of the reason to decline exists. The verdict's reason sentence names that record. In owner mode the record is a D-entry, a `cairn/DESIGN.md` line, or a dropped milestone's archive summary. In guest mode it is the upstream repo's own docs or a maintainer's statement on GitHub. §4 states that a decline with no such record takes the `milestone` verdict at the `decide` level, and that the chip's candidate-row option then holds the decline's record.
- [ ] AC2: The Intake paragraph of `skills/shared/tracking-rules.md` names a reply (`/milestone` §4) and `/milestone-plan` as issue routes beside `candidate` rows and the hotfix path. It limits the reply route to an issue whose answer leaves nothing new for cairn to record. Its `leave` sentence keeps its current wording: "`leave` is legal only for noise, duplicates, or items already cross-referenced in cairn — never anything genuinely new".
- [ ] AC3: Each `gh issue list` and `gh pr list` command in `skills/milestone-plan/SKILL.md`, as `git grep -n -e 'gh issue list' -e 'gh pr list' -- skills/milestone-plan/SKILL.md` lists them, carries `--repo <base-repo>` on the same line. Step 2 states that in guest mode these reads go to the base repo's inboxes, unlike `/milestone` §2's inbox bullet, which skips guest mode. Step 2 gives the reason: the plan's sweep looks for overlap with the planned work, such as an upstream issue that the work resolves.
- [ ] AC4: The profile's `verify` slot passes: both `python3 -m unittest discover` suites (`scripts/tests`, `hooks/tests`), both `claude plugin validate` runs, and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T1, T2, T3, T4

## Tasks

- [ ] T1: Rewrite the `reply` verdict's decline case in `skills/milestone/SKILL.md` §4 (~lines 380-383) as a rule with its owner and guest records and the `milestone`/`decide` fallback (AC1). Add asserts to `skills/tests/test_issue_look_in.py` for the owner record list, the guest record, and the fallback.
- [ ] T2: Edit the Intake paragraph of `skills/shared/tracking-rules.md` (~lines 191-192) to name the reply and `/milestone-plan` routes, with the `leave` sentence untouched (AC2). Append D-154 to `cairn/DECISIONS.md`, annotating D-044: a reply carries leave's narrowing, and an unrecorded decline routes to `milestone`/`decide`. Add a guard to `TestIntakeRouting` in `skills/tests/test_external_pr_intake.py`. Re-seed the rulebook-mass baseline "629 lines / 59,832 chars" with `wc -l -m` at its three sites: the `skills/milestone/SKILL.md` audit line, `skills/tests/test_cost_audit_line.py`, and `skills/tests/test_mutation_harness.py`.
- [ ] T3: Add `--repo <base-repo>` to both inbox reads in `skills/milestone-plan/SKILL.md` step 2 (~lines 99-103). State the guest-mode difference from `/milestone` §2 with its reason (AC3). Add a guard to `skills/tests/test_issue_triage.py`.
- [ ] T4: Add a CHANGELOG.md Unreleased entry and one README sentence in the look-in paragraph (README.md ~lines 72-81) on the decline rule. Register or exempt the new guards per the rule in `skills/tests/test_mutation_harness.py`. Run the `verify` slot (AC4). Run `python3 -m unittest discover -s skills/tests` by hand.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: what to work on: "Issue look-in edges", the three items the chip named (decline record, Intake routes, plan-sweep `--repo`). Go on through review after the plan: yes.
- 2026-10-10: collision check: absorbs the candidate row "Issue look-in edges (M232 review)". Its other four items stay there, and the row graduates at hygiene (records-hygiene §1). D-044 and D-042 read whole and applied, not superseded. Inbox sweep found 0 open issues and 0 outside PRs. No checker-regress shape (skill prose, no checker).
- 2026-10-10: lessons harvested: M112 (sweep the old phrasing across README, so T4 adds the README sentence), M149 (rulebook mass is pinned at three sites, so T2 re-seeds all three), M185 (sweep per `gh` command, which found the §2 reads now on the row), M154 (the row is not pruned at plan).
- 2026-10-10: plan gate chose routing an unrecorded decline to `milestone`/`decide` over adding a candidate-row write to the reply path, because the chip already offers the row and the reply path stays write-free. Falsified by a real look-in where declining a request forces the user to file a row and then drop it.
- 2026-10-10: plan gate chose `--repo` at each of the two plan-sweep reads over a blanket session-start clause, because the plan skill holds only these two inbox reads. Falsified by a later `gh issue` or `gh pr` read added to the plan skill without `--repo`.
- 2026-10-10: criteria audit (full mode, fresh Opus reader): 4 findings, all fixed. AC1 changed from an example condition to a rule, gained a guest-mode record arm, and now says where an unrecorded decline's record lands. AC3 now requires step 2 to state its guest-mode difference from `/milestone` §2 and the reason. AC2 and AC4 had no finding.
- 2026-10-10: no split: 4 criteria, 4 tasks, one PR.
