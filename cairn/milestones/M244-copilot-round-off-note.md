# M244: Turn on the Copilot round in the easystats checkouts, and name the line when Copilot reviews a PR with the round off

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing, because adopters read the `/hotfix` and `/milestone-review` close blocks and the README
- **Branch/PR:** m244-copilot-round-off-note, https://github.com/jmgirard/cairn/pull/254

## Goal

The six easystats guest checkouts run the Copilot round, and four named `/hotfix` and `/milestone-review` closes name the opt-in line when Copilot is on a PR that the round covers but the round is off.

## Scope

**In:** The Copilot round runs only in a repo whose `cairn/PROFILE.md`
carries `# Copilot review: on` (D-152). Of the local cairn checkouts, only
this repo has the line. No `/hotfix` session in `performance` ran a Copilot
command, and the Copilot reviews on some easystats PRs were requested under
the operator's account about two minutes after each PR opened. Nobody
handled those reviews' threads. This milestone adds the line to the six
easystats guest checkouts (`correlation`, `insight`, `modelbased`,
`parameters`, `performance`, `see`). The files are local and never
committed. It also adds an "off but present" rule to
`skills/shared/copilot-review.md` §1, rewords §1's "keeps its usual flow"
sentence, and updates the module's opening. At four close sites, with the
round off and on a PR the round covers, the skill runs the §3 state
query once. On `pending` or `reviewed`, the close block carries one line
naming the PR and the opt-in line. The sites are `/hotfix` step 7 and its
step 6 guest handoff close, and `/milestone-review` step 10 and its step 8
guest handoff close. README and CHANGELOG describe it.

**Out:** Handling Copilot threads with the round off, a change to D-152's
opt-in. The line in `brms` and `glmmTMB`. Notes at other closes: the CI
timeout stops, the companion timeout close, `/hotfix`'s merged-PR re-entry,
`/milestone-review` resume route (a), and the later guest hygiene run
reached through `/milestone`. Adopted PRs, an already-merged review, and
milestones with companions, which the round never covers. In `parameters`
and `see` a guest push stops for want of a fork remote, so a round's fix
push there stops too. That gap stays with "Intake and guest edges (M234
review)". Bot threads after a round stay with "`/milestone` reads each bot
thread on the operator's open PRs".

## Acceptance criteria

- [x] AC1: Each of the six checkouts `correlation`, `insight`, `modelbased`, `parameters`, `performance`, and `see` under `/Users/jmgirard/github/` has `# Copilot review: on` as a header line of `cairn/PROFILE.md`. In each, `git status --short` lists no `cairn/` path, and `cairn_validate` passes.
- [x] AC2: `skills/shared/copilot-review.md` §1 states the off-but-present rule for `/hotfix` and `/milestone-review` at the closes AC3 names. With the round off, on a PR the round covers (an authored hotfix PR, or a milestone PR with no companions, not already merged at review start), the skill runs one §3 state query with §3's owner and name (guest mode: the base repo's). On `pending` or `reviewed`, the close block gets one line that names the PR and the line `# Copilot review: on`. On `none` or a failed query, it gets nothing. The rule makes no request, reply, or resolve. §1 no longer says that a skill with the round off keeps its usual flow with no exception.
- [x] AC3: `/hotfix` step 7, `/hotfix` step 6's guest handoff close, `/milestone-review` step 10, and `/milestone-review` step 8's guest handoff close each point to §1's off-but-present rule.
- [x] AC4: README.md's Copilot paragraph and a new CHANGELOG.md `## Unreleased` entry say that with the line absent, a Copilot review on the PR gets a close-block note naming the line, and that cairn does not handle its threads.
- [x] AC5: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T2, T3, T4

## Tasks

- [x] T1: In each of the six checkouts, add `# Copilot review: on` under the `# Collaboration mode: guest` line of `cairn/PROFILE.md`. Run `git status --short` and `cairn_validate` there.
- [x] T2: Write the rule in `skills/shared/copilot-review.md` §1, reword the "usual flow" sentence, and update the module's opening, which says only opted-in repos read it. Keep `wc -l -c` under the module's 140 lines and 8,000 bytes. Run the §3 query once, read-only, with owner `easystats`, name `performance`, PR 964, and record that it prints `reviewed`. Hand-run `skills/tests` (`test_copilot_review_round.py` pins this module).
- [x] T3: Add the pointer at the four close sites in `skills/hotfix/SKILL.md` and `skills/milestone-review/SKILL.md`. Hand-run `skills/tests`.
- [x] T4: README Copilot paragraph and CHANGELOG entry. Run the five `verify` checks.

## Work log

- 2026-10-11: created by /milestone-plan.
- 2026-10-11: investigation: this repo's hotfix PR #245 (after M231) requested Copilot and read its review (0 findings), so the owner arm runs here. `grep '# Copilot review'` over the 24 local `cairn/PROFILE.md` files finds the line only in this repo. No `add-reviewer @copilot` call appears in the 12 newest `performance` session transcripts. On easystats PRs, `performance#964`, `correlation#393`, `see#465`, and `performance#965` carry Copilot requests by `jmgirard` about 2 minutes after the open, and `performance#962` and `parameters#1272` carry none.
- 2026-10-11: inbox sweep: no open issues and no open PRs on jmgirard/cairn.
- 2026-10-11: collision check: M231 shipped the round, and D-152 and D-153 make it opt-in, which this plan keeps. "`/milestone` reads each bot thread on the operator's open PRs" covers bot threads that arrive after a round, a different case, and stays a row. "Intake and guest edges (M234 review)" holds the fork-recipe stop.
- 2026-10-11: question set: what to change — turn the round on in the easystats checkouts, and add a close note when Copilot is on a PR with the round off.
- 2026-10-11: question set: which checkouts get the opt-in line — the six easystats checkouts, local files never committed. Granted for T1's writes there.
- 2026-10-11: criteria audit (full mode, fresh Opus reader) returned 13 findings, 9 fixed in this file. AC1 now checks `git status --short` for `cairn/` paths. AC2 names its skills and closes, covers only PRs the round covers, names the guest owner and name, and rewords §1's "usual flow" sentence. The Goal narrows to the four closes, and Out lists the other closes and the fork-remote gap. T2 rewrites the module opening, keeps the budget, and runs a read-only query probe on `easystats/performance#964`. Answered: a read-only query is no outward write and keeps no record, so D-152 and D-153 stand with no new entry. The budget and the probe stay in T2, not in a criterion, since both are instrument properties. AC4, AC5, and the instrument check were clean.
- 2026-10-11: plan chose a note that names the line over handling Copilot threads with the round off. Handling them reverses D-152's opt-in and writes on upstream PRs unasked. Falsified by an opted-out repo whose operator acts on the note's Copilot threads by hand each time.
- 2026-10-11: plan chose the rule in the module's §1 with four pointers over a copy of the rule at each site. Four copies drift apart. The cost is a read of the module at a round-off close. Falsified by a measured `cairn_cost` reading that attributes a material share of a round-off hotfix's tokens to that read.
- 2026-10-11: implement started on m244-copilot-round-off-note. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-11: T1 done. `# Copilot review: on` sits on line 3 of `cairn/PROFILE.md`, under the collaboration-mode line, in correlation, insight, modelbased, parameters, performance, and see. In each, `git status --short` lists no `cairn/` path and `cairn_validate` exits 0.
- 2026-10-11: T2 done. The read-only §3 query on `easystats/performance#964` printed `reviewed earlier-head Lite` (exit 0). §1 now says off means no request, reply, or resolve, but for the note, and gains the "Off but present" paragraph with the note's fixed text. The opening says round-off skills read §1 and §3 at the named closes. The module is 138 lines and 7,937 bytes. `skills/tests` ran 726 OK, and the five verify checks pass (1660 mod tests, 0 red).
- 2026-10-11: T3 done. `/hotfix` step 6's guest handoff close and step 7, and `/milestone-review` step 8's guest handoff close and step 10, each point to §1's rule. Step 7 excludes an adopted PR and the merged-PR re-entry, and step 10 excludes resume route (a) and the later guest hygiene run, as Out states. `skills/tests` ran 726 OK, both Python suites and both validates pass.
- 2026-10-11: T4 done. README's Copilot paragraph and a CHANGELOG `### New` entry describe the note. The five verify checks pass (1660 mod tests, 0 red), and `skills/tests` ran 726 OK.
- 2026-10-11: claim audit: 18 claims read, 5 corrected — skills/shared/copilot-review.md, skills/hotfix/SKILL.md, README.md, CHANGELOG.md
- 2026-10-11: the 5 corrections: the module's covered hotfix PR is one this run merged or handed off, and a failed query skips §3's error line. Hotfix step 7 counts a re-entry's follow-up PR and excludes the re-entry's merged PR. README and CHANGELOG say "a merge made in that run" and limit the note to PRs the round itself would review. The same reader's re-read found all 5 hold. The module is 139 lines and 7,995 bytes. Verify passes after the edits (1660 mod tests, 0 red), and `skills/tests` ran 726 OK.
- 2026-10-11: implement done, status review. No deviation from the plan.
- 2026-10-11: step-7 approval: m244-copilot-round-off-note approved for merge

## Decisions

## Review

- Copilot arm: branch pushed, PR #254 opened, state query `none`, Copilot requested (exit 0).
- AC1: on 8779eee, in each of correlation, insight, modelbased, parameters, performance, and see, the header block of `cairn/PROFILE.md` (lines above the first `## `) holds `# Copilot review: on` once, `git status --short` lists no `cairn/` path, and `cairn_validate` exits 0.
- AC2: on 8779eee, `skills/shared/copilot-review.md` §1 holds the "Off but present" paragraph at line 25. It names `/hotfix` and `/milestone-review` at the four closes, limits the query to an authored hotfix PR this run merged or handed off or a milestone PR with no companions not merged before review, names the base repo's owner and name in guest mode, gives the one-line note naming the PR and `# Copilot review: on` on `pending` or `reviewed`, gives nothing on `none` or a failed query, and makes no request, reply, or resolve. Line 17's "off" sentence replaced "keeps its usual flow".
- AC3: on 8779eee, `grep -n off-but-present` finds the pointer at skills/hotfix/SKILL.md:294 (step 6 guest handoff close) and :311 (step 7), and at skills/milestone-review/SKILL.md:636 (step 8 guest handoff close) and :774 (step 10), each citing `skills/shared/copilot-review.md` §1.
- AC4: on 8779eee, README.md:718-723 and the first `### New` entry under CHANGELOG.md `## Unreleased` (line 52) say that without the line cairn does not handle Copilot's threads, and that a close names the line when Copilot is on the PR.
- AC5: on 8779eee, `scripts/tests` ran 406 OK (21 skipped), `hooks/tests` 174 OK, both validates exit 0, and the mod test ran 1660 with 0 red. `skills/tests` (hand-run) ran 726 OK.
- gate: `cairn_validate` all checks passed. The marketplace validate prints no `plugins[N].version` warning. CHANGELOG has the entry with no milestone number. No principle changed, so `cairn_impact` was skipped.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: one query at the close misses Copilot requests that land minutes after the PR opens, so the note often stays silent — fix now: the module, README, and CHANGELOG say a request made after the query goes unreported, fixed de81e76.
- diff-bug #2: the new module line ran past 80 columns, and the module had no headroom — fix now: reflowed, the module is 139 lines and 7,983 bytes, fixed de81e76.
- diff-bug #3: the note said "Add", which misleads when a misspelled value is present — fix now: it says "Set", fixed de81e76.
- diff-bug #4: "did not handle its threads" does not fit `pending` — fix now: "does not handle Copilot's threads", fixed de81e76.
- diff-bug #5: the note was one code span wrapped across three lines — fix now: a plain line, fixed de81e76.
- diff-bug #6: the module did not say where the note goes in the close block — fix now: the recap ends with it, fixed de81e76.
- diff-bug #7: nothing names how owner mode gets the owner and name — reject, false: §3 names the base repo, and the rulebook's slug recipe gives it.
- diff-bug #8: step 10's exclusion names route (a) but not route (b) — reject, false: "a merge this run made" already excludes route (b).
- diff-bug #9: no prose guard covers the rule or its pointers — reject, planned change: the plan scoped no guard, and `skills/tests` is hand-run and gates nothing (D-109).
- diff-bug #10: a CHANGELOG sentence started on a fresh line mid-paragraph — fix now, fixed de81e76.
- diff-bug #11: the opening dropped "costs nothing" and the read cost is real — reject, planned change: the work log records the choice and its falsifier.
- blame-history #1: the note will rarely fire at the guest closes it targets, since the query runs seconds after the open — follow-up: new row "Late Copilot requests with the round off (M244 review)" at hygiene; the caveat is diff-bug #1's fix.
- blame-history #2: "does not handle" overstates, since the PR-conversation read gives bot threads dispositions — reject, false: with the round off, an authored hotfix PR and a fresh milestone PR open after the chip and merge with no conversation read.
- blame-history #3: every round-off close now reads the module and runs one query — reject, planned change, as diff-bug #11.
- blame-history #4: the module used all its headroom — fix now, as diff-bug #2, fixed de81e76.
- blame-history #5: DESIGN.md's module line and tracking-rules:255 describe only the opted-in reading — fix now for DESIGN.md, fixed de81e76; reject, false, for tracking-rules:255, which states when the PR opens, unchanged.
- blame-history #6: a note after the merge comes too late for a pending review — reject, planned change: with the round off nothing waits on Copilot (D-152), and the opt-in is the remedy the note names.
- blame-history #7: the step 7 and step 10 exclusions are hard to follow — reject, style.
- blame-history #8: the note was not checked against guest mode's no-vocabulary rule — reject, false: the note goes in the chat close block, never to the repo.
- blame-history #9: no D-entry records the narrowed "usual flow" wording — reject, false: D-152 decides when the PR opens and what the line permits, and neither changed.
- blame-history #10: README says a GitHub setting requests Copilot, which is unconfirmed — fix now: README and CHANGELOG say "someone or something else", fixed de81e76.
- prior-review #1: the README and CHANGELOG lacked M231's "present when the read runs" qualifier — fix now, as diff-bug #1, fixed de81e76.
- prior-review #2: §3's error rule does not mention the carve-out — reject, false: the closes reach §3 through §1, which states the carve-out first.
- prior-review #3: the budget header still cites 126 lines and 7,142 bytes — reject, false: it states where the budget figure came from.
- prior-review #4: the "costs nothing" promise is gone — reject, planned change, as diff-bug #11.
- prior-review #5: the hotfix re-entry enumeration may drift — reject, false: the claim audit read it against step 1's routes and it holds.
- copilot: review body — noted: "Copilot was unable to review this pull request because the user who requested the review has reached their quota limit."
- Copilot level: none, the review did not run (quota limit).
- conversation: no human reviews or comments on PR #254.
