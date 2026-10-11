# M244: Turn on the Copilot round in the easystats checkouts, and name the line when Copilot reviews a PR with the round off

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing, because adopters read the `/hotfix` and `/milestone-review` close blocks and the README
- **Branch/PR:** m244-copilot-round-off-note

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

- [ ] AC1: Each of the six checkouts `correlation`, `insight`, `modelbased`, `parameters`, `performance`, and `see` under `/Users/jmgirard/github/` has `# Copilot review: on` as a header line of `cairn/PROFILE.md`. In each, `git status --short` lists no `cairn/` path, and `cairn_validate` passes.
- [ ] AC2: `skills/shared/copilot-review.md` §1 states the off-but-present rule for `/hotfix` and `/milestone-review` at the closes AC3 names. With the round off, on a PR the round covers (an authored hotfix PR, or a milestone PR with no companions, not already merged at review start), the skill runs one §3 state query with §3's owner and name (guest mode: the base repo's). On `pending` or `reviewed`, the close block gets one line that names the PR and the line `# Copilot review: on`. On `none` or a failed query, it gets nothing. The rule makes no request, reply, or resolve. §1 no longer says that a skill with the round off keeps its usual flow with no exception.
- [ ] AC3: `/hotfix` step 7, `/hotfix` step 6's guest handoff close, `/milestone-review` step 10, and `/milestone-review` step 8's guest handoff close each point to §1's off-but-present rule.
- [ ] AC4: README.md's Copilot paragraph and a new CHANGELOG.md `## Unreleased` entry say that with the line absent, a Copilot review on the PR gets a close-block note naming the line, and that cairn does not handle its threads.
- [ ] AC5: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T2, T3, T4

## Tasks

- [x] T1: In each of the six checkouts, add `# Copilot review: on` under the `# Collaboration mode: guest` line of `cairn/PROFILE.md`. Run `git status --short` and `cairn_validate` there.
- [ ] T2: Write the rule in `skills/shared/copilot-review.md` §1, reword the "usual flow" sentence, and update the module's opening, which says only opted-in repos read it. Keep `wc -l -c` under the module's 140 lines and 8,000 bytes. Run the §3 query once, read-only, with owner `easystats`, name `performance`, PR 964, and record that it prints `reviewed`. Hand-run `skills/tests` (`test_copilot_review_round.py` pins this module).
- [ ] T3: Add the pointer at the four close sites in `skills/hotfix/SKILL.md` and `skills/milestone-review/SKILL.md`. Hand-run `skills/tests`.
- [ ] T4: README Copilot paragraph and CHANGELOG entry. Run the five `verify` checks.

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
