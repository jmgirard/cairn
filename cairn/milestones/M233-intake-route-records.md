# M233: Issue intake routes keep their records and read the right repo

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — it edits shipped skill prose and the rulebook that adopting repos run
- **Branch/PR:** m233-intake-route-records, PR #242 https://github.com/jmgirard/cairn/pull/242

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

- [x] AC1: `skills/milestone/SKILL.md` §4 gives the `reply` verdict to a request the project declines only when a record of the reason to decline exists. The verdict's reason sentence names that record. In owner mode the record is a D-entry, a `cairn/DESIGN.md` line, or a dropped milestone's archive summary. In guest mode it is the upstream repo's own docs or a maintainer's statement on GitHub. §4 states that a decline with no such record takes the `milestone` verdict at the `decide` level, and that the chip's candidate-row option then holds the decline's record.
- [x] AC2: The Intake paragraph of `skills/shared/tracking-rules.md` names a reply (`/milestone` §4) and `/milestone-plan` as issue routes beside `candidate` rows and the hotfix path. It limits the reply route to an issue whose answer leaves nothing new for cairn to record. Its `leave` sentence keeps its current wording: "`leave` is legal only for noise, duplicates, or items already cross-referenced in cairn — never anything genuinely new".
- [x] AC3: Each `gh issue list` and `gh pr list` command in `skills/milestone-plan/SKILL.md`, as `git grep -n -e 'gh issue list' -e 'gh pr list' -- skills/milestone-plan/SKILL.md` lists them, carries `--repo <base-repo>` on the same line. Step 2 states that in guest mode these reads go to the base repo's inboxes, unlike `/milestone` §2's inbox bullet, which skips guest mode. Step 2 gives the reason: the plan's sweep looks for overlap with the planned work, such as an upstream issue that the work resolves.
- [x] AC4: The profile's `verify` slot passes: both `python3 -m unittest discover` suites (`scripts/tests`, `hooks/tests`), both `claude plugin validate` runs, and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T1, T2, T3, T4

## Tasks

- [x] T1: Rewrite the `reply` verdict's decline case in `skills/milestone/SKILL.md` §4 (~lines 380-383) as a rule with its owner and guest records and the `milestone`/`decide` fallback (AC1). Add asserts to `skills/tests/test_issue_look_in.py` for the owner record list, the guest record, and the fallback.
- [x] T2: Edit the Intake paragraph of `skills/shared/tracking-rules.md` (~lines 191-192) to name the reply and `/milestone-plan` routes, with the `leave` sentence untouched (AC2). Append D-154 to `cairn/DECISIONS.md`, annotating D-044: a reply carries leave's narrowing, and an unrecorded decline routes to `milestone`/`decide`. Add a guard to `TestIntakeRouting` in `skills/tests/test_external_pr_intake.py`. Re-seed the rulebook-mass baseline "629 lines / 59,832 chars" with `wc -l -m` at its three sites: the `skills/milestone/SKILL.md` audit line, `skills/tests/test_cost_audit_line.py`, and `skills/tests/test_mutation_harness.py`.
- [x] T3: Add `--repo <base-repo>` to both inbox reads in `skills/milestone-plan/SKILL.md` step 2 (~lines 99-103). State the guest-mode difference from `/milestone` §2 with its reason (AC3). Add a guard to `skills/tests/test_issue_triage.py`.
- [x] T4: Add a CHANGELOG.md Unreleased entry and one README sentence in the look-in paragraph (README.md ~lines 72-81) on the decline rule. Register or exempt the new guards per the rule in `skills/tests/test_mutation_harness.py`. Run the `verify` slot (AC4). Run `python3 -m unittest discover -s skills/tests` by hand.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: what to work on: "Issue look-in edges", the three items the chip named (decline record, Intake routes, plan-sweep `--repo`). Go on through review after the plan: yes.
- 2026-10-10: collision check: absorbs the candidate row "Issue look-in edges (M232 review)". Its other four items stay there, and the row graduates at hygiene (records-hygiene §1). D-044 and D-042 read whole and applied, not superseded. Inbox sweep found 0 open issues and 0 outside PRs. No checker-regress shape (skill prose, no checker).
- 2026-10-10: lessons harvested: M112 (sweep the old phrasing across README, so T4 adds the README sentence), M149 (rulebook mass is pinned at three sites, so T2 re-seeds all three), M185 (sweep per `gh` command, which found the §2 reads now on the row), M154 (the row is not pruned at plan).
- 2026-10-10: plan gate chose routing an unrecorded decline to `milestone`/`decide` over adding a candidate-row write to the reply path, because the chip already offers the row and the reply path stays write-free. Falsified by a real look-in where declining a request forces the user to file a row and then drop it.
- 2026-10-10: plan gate chose `--repo` at each of the two plan-sweep reads over a blanket session-start clause, because the plan skill holds only these two inbox reads. Falsified by a later `gh issue` or `gh pr` read added to the plan skill without `--repo`.
- 2026-10-10: criteria audit (full mode, fresh Opus reader): 4 findings, all fixed. AC1 changed from an example condition to a rule, gained a guest-mode record arm, and now says where an unrecorded decline's record lands. AC3 now requires step 2 to state its guest-mode difference from `/milestone` §2 and the reason. AC2 and AC4 had no finding.
- 2026-10-10: no split: 4 criteria, 4 tasks, one PR.
- 2026-10-10: implement start: branch m233-intake-route-records cut from main at db92fd5. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-10: T1 done: §4 `reply` decline rule with owner and guest records and the `milestone`/`decide` fallback. 3 new tests in `test_issue_look_in.py` pass, and the same 3 fail against the old prose. Verify slot 5/5 green.
- 2026-10-10: T2 done: Intake paragraph names the reply and `/milestone-plan` routes, `leave` sentence unchanged and still on one line. D-154 appended, annotating D-044. Rulebook mass re-seeded to 630 lines / 59,932 chars (`wc -l -m`) at its three sites. New intake guard registered in the mutation harness, and it fails against the old rulebook. Verify slot 5/5 green, `cairn_validate` green.
- 2026-10-10: T3 done: both plan-sweep reads carry `--repo <base-repo>`, and step 2 states the guest-mode difference from `/milestone` §2 with its reason. Implement choice: an overlapping PR names the maintainers in guest mode, not `/hotfix`, and §3 triage is marked owner-mode, since the new guest reads would otherwise route to a door guest mode lacks. `TestPlanSweepRepo` (3 tests) passes, 2 fail against the old prose, and one mutation entry is registered. Verify slot 5/5 green.
- 2026-10-10: T4 done: two CHANGELOG entries under "Changes that affect existing repos" and one README sentence in the look-in paragraph. Verify slot 5/5 green, and the hand-run `skills/tests` run passed 698 tests.
- 2026-10-10: claim audit: 31 claims read, 3 corrected — skills/milestone/SKILL.md, skills/milestone-plan/SKILL.md, CHANGELOG.md
- 2026-10-10: claim audit re-read: 4 of the 5 corrected sentences hold. §4's "the chip's candidate-row option then holds the decline's record" is kept as AC1 words it. The reader noted that an owner-mode row is not written off the default branch or with a dirty ROADMAP. The candidate-row option's own description in §4 already states those cases.
- 2026-10-10: implement complete: T1–T4 checked. Verify slot 5/5 green and hand-run `skills/tests` green after the claim fixes. Status set to review.
- 2026-10-10: review start: branch up to date with origin/main (db92fd5). Copilot round on: branch pushed, PR #242 opened, state query `none`, Copilot requested.

## Review

- AC1 evidence (head f88dc6c): `skills/milestone/SKILL.md` §4 lines read by `sed` over the section: "A request the project declines takes `reply` only when a record of the reason to decline exists, and the verdict's reason names that record." The owner record list (D-entry, `cairn/DESIGN.md` line, dropped milestone's archive summary) and the guest record (upstream docs or a maintainer's statement on GitHub) follow. The fallback reads "A decline with no such record takes the `milestone` verdict at the `decide` level, and the chip's candidate-row option then holds the decline's record."
- AC2 evidence (head f88dc6c): `skills/shared/tracking-rules.md:191-193` reads "Issues → `candidate` rows, the hotfix path, `/milestone-plan`, or a reply (`/milestone` §4) whose answer leaves nothing new for cairn to record;" and the `leave` sentence follows with its words unchanged from main ("`leave` is legal only for noise, duplicates, or items already cross-referenced in cairn — never anything genuinely new"), now on one line.
- AC3 evidence (head f88dc6c): `git grep -n -e 'gh issue list' -e 'gh pr list' -- skills/milestone-plan/SKILL.md` lists 2 lines, 101 and 102, and each carries `--repo <base-repo>` on that line. Lines 120-124 state that in guest mode the reads go to "the base repo's inboxes, unlike `/milestone` §2's inbox bullet, which skips guest mode", with the reason that the plan's sweep looks for overlap with the planned work, such as an upstream issue that the work resolves.
- AC4 evidence (head f88dc6c): `scripts/tests` exit 0, `hooks/tests` exit 0 (174 tests), `claude plugin validate` plugin.json exit 0, marketplace.json exit 0, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0, each exit code read on its own.
- Consistency gate (head f88dc6c): `cairn_validate` exit 0, all checks passed. No principle changed, so `cairn_impact` was skipped. Profile gate: the verify checks are green on this head (AC4), the marketplace validate output has no `version` line, and CHANGELOG.md has two Unreleased entries with no milestone number.
- Process note: the AC4 box was ticked in the same edit batch as a failed evidence write. The evidence line above was written before any commit, and no commit carries the tick without it.
