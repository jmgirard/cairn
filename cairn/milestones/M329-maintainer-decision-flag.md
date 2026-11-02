# M329: Flag maintainer decisions at the plan

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — `/milestone-plan` and `/milestone-review` text that every guest repo runs
- **Branch/PR:** —

## Goal

In guest mode, a plan poses a needed maintainer decision before it goes on, and review shows a reported planned removal and a render.

## Scope

**In:** three changes from easystats/see PR 487, guest mode only. The case record is `/Users/jmgirard/github/easystats/see/cairn/milestones/M015-outliers-panel-y-axis.md`.

(1) `/milestone-plan` step 2 flags work that needs a maintainer's decision, and step 3 poses the question before any file is written for that work. The options are to draft a question for the maintainers, to name an agreement the read missed, and not to build. A draft goes to the system temp directory and the close block, and the user posts it, as in `/milestone` §4. A logged user override remains possible. Step 4 writes a `maintainer decision:` line. Guest rule (4)'s last sentence in `skills/shared/tracking-rules.md` and the README's text on that rule change to match. `/milestone-review` step 8's guest body says when a design has no agreement.

(2) `/milestone-review` step 5 gains a reject ground, `planned removal`, for a reported finding that a removal the plan called for takes output from users. Its reason says what users no longer see and how often. Step 7 shows it verbatim, and the chip's question text names it.

(3) `/milestone-review` step 7 gains a paragraph on rendered output whose snapshots cannot be compared on this machine. Step 8 limits what a guest PR can claim about a snapshot.

Also README, CHANGELOG, one D-entry, and the rulebook-mass seed.

**Out:** owner mode, because no owner-mode defect triggers these rules and the user did not choose it. `/hotfix` and a surface with no snapshot tests are also out. All three go to the candidate row "Widen the render rule past its trigger". A reviewer lens question that looks for removals is not built, because the case's reviewer did report the removal. A PR body line for an approved removal is not built, because the plan flags that work first. A removal first found at review still reaches the operator only.

## Acceptance criteria

Reader runs. A reader run is one fresh-context subagent that has not seen this plan. It gets the named skill file and `skills/shared/tracking-rules.md` at the branch head, and the case text. It says what the skill text requires for that case. Each criterion below states what the skill text requires.

- [ ] AC1: Reader run of `/milestone-plan` on M015's Goal and Scope and its two `question set:` lines, in guest mode, with no issue and no maintainer comment. The skill text requires a question at step 3 before any file is written for that work. The question names the maintainers' decision, and its options are to draft a question, to name an agreement, and not to build.
- [ ] AC2: Reader run of `/milestone-plan` on these guest cases, one reader per case. No question is required for a documented-behavior fix with no design choice, or for an issue whose member comment agrees with the design. The second requires a `maintainer decision:` line. A question is required for a member's comment that leaves a user-visible design choice open, for an agreeing comment by the operator's own login, for a fix that `/hotfix` sent over because of a design decision, and for a request that names no work.
- [ ] AC3: Reader run of `/milestone-plan` on the three option outcomes and on a rerun. Drafting writes the temp file, shows the draft and the command in the close block, posts nothing, and writes no milestone file for that work. An existing row stays as it is, and a parked row is written when no row holds the work. Not building writes no file. A rerun with no maintainer answer poses the question again, and a maintainer's no goes to the idea vet's flaw question.
- [ ] AC4: Reader run of `/milestone-review` in guest mode on M015 pass 1's `blame-history #1`, up to its ` — `, with M015's Scope and AC4. The skill text forbids the plain planned-change ground. It requires a reason that says what users no longer see and a count over a named set, and chip question text that names both. A planned change that hides a panel behind a new default-off option requires the same. A case with no set to run requires the reason to say that no count was run.
- [ ] AC5: Reader run of `/milestone-review` on these findings, each up to its ` — `. `diff-bug #2` of M015 pass 1 and a planned reword of an axis label take the plain planned-change ground. `diff-bug #4` of that pass takes no `planned removal` ground. Neither does PR 487's review text, "Contour lines should not be removed from plots". `blame-history #1` in owner mode takes the plain planned-change ground.
- [ ] AC6: Reader run of `/milestone-review` in guest mode, with `Surface tier:` user-facing and M015's work-log line beginning "T3: full `devtools::test()`". The skill text requires a before and after render of the default case for each entry point the diff changes, a `render:` Review line, and chip question text that says what the reader sees. The same is required when the snapshot tests skip at both, fail at the head and skip at the base, or fail in part at both, and for a web page's `__snapshots__` tests. When no render can be made or looked at, the line and the chip say so and the run does not stop.
- [ ] AC7: Reader run of `/milestone-review` on three cases that require no render: guest mode with the snapshot tests passing at the base on this machine, guest mode with an in-repo dev plot at tier internal, and M015's facts in owner mode.
- [ ] AC8: Reader run of `/milestone-review` step 8 on PR 487's body line "check-model-outliers, check-model-panel, check-outliers-default, check-outliers-modern, outliers-plot-low-n, and the default plot.see_check_outliers snapshot: shorter y axis, cut contour lines." with no render made. The skill text bars it unless each named snapshot's case has a render, and requires the line to say the render was local. The body's sentence that the snapshots "need a re-record in CI" is allowed. A work log with `maintainer decision: none` requires the body to say that no maintainer agreed with the design.
- [ ] AC9: `cairn/DECISIONS.md` holds an entry that supersedes D-214's rejection of a plan-step check and its "runs no check of its own" clause at the user's decision. The entry states D-108's door for each rule and the `maintainer decision:` line. It annotates D-144's reject-ground and question lists, D-206, D-207, D-208, and D-155, and it names a falsifier for each rule.
- [ ] AC10: `git grep -n -F` over tracked files at the head, without `cairn/DECISIONS.md`, `cairn/milestones/`, and the changelog's released sections, finds no remaining "runs no check of its own". README and CHANGELOG's Unreleased section state the three changes.
- [ ] AC11: The `verify` slot's five commands exit 0 at the head, and `python3 scripts/cairn_validate.py` passes.

## Coverage

- AC1 → T1, T4
- AC2 → T1, T4
- AC3 → T1, T4
- AC4 → T2, T4
- AC5 → T2, T4
- AC6 → T3, T4
- AC7 → T3, T4
- AC8 → T1, T3, T4
- AC9 → T5
- AC10 → T5
- AC11 → T6

## Tasks

- [ ] T1: Edit `/milestone-plan` steps 2, 3, and 4, the rule (4) sentence in tracking-rules, and the `maintainer decision: none` sentence in `/milestone-review` step 8. Re-seed the rulebook mass in the `/milestone` skill line and the two hand-run pins.
- [ ] T2: Edit `/milestone-review` steps 5 and 7 for `planned removal`.
- [ ] T3: Add step 7's render paragraph and edit step 8's snapshot sentences. Resume route (b) skips the paragraph, since its PR has merged. The session removes the scratch worktree right after each render.
- [ ] T4: Run the reader runs at the head. If a reader disagrees with a criterion, read the sentence it quotes, then change the text or record why not before a new reader runs. Run the AC1, AC4, and AC6 cases once at the plan commit as a baseline. Replay the render rule on PR 487's branch and base from `git archive` copies in a temporary directory, and record what each render shows.
- [ ] T5: Write the D-entry, README, CHANGELOG, and the candidate row. Run the AC10 search.
- [ ] T6: Run `verify`, `cairn_validate`, and the hand-run `skills/tests`.

## Work log

- 2026-11-02: created by /milestone-plan.
- 2026-11-02: tier check: milestone — the request is a design decision in three skill rules, sent by another session from the see PR 487 case.
- 2026-11-02: idea vet: flaw — the request's premise for a plan check is that the M015 plan broke guest rule (4), but it was planned on 2026-10-17 and handed off on 2026-10-17 and 2026-10-20, before the rule's 2026-10-22 date; the user answered with a new shape, a flag at planning that poses the question. gap — "snapshots cannot be compared" read as tests that fail or skip at both the head and the base, not as a surface with no snapshot tests. gap — "removes or hides" read as a removal the plan called for, so an unplanned one stays a defect.
- 2026-11-02: lessons used: 2026-07-24 (M112), 2026-08-17 (M149), 2026-10-29 (M325), 2026-10-30 (M327), 2026-10-30 (M326).
- 2026-11-02: collision check: D-214 rejected "a plan-step check for the issue-first rule (the user chose an instruction)". The user's answer at the question set supersedes that clause, so the D-entry does. D-108's door applies to the review rules and the new work-log line. D-057 closes size work only and raises no bar: the rulebook grows by one sentence's change. D-155 set the user-posted draft shape that this plan reuses. D-205 rejected a new disposition beside reject, so `planned removal` is a reject ground.
- 2026-11-02: inbox sweep: no open issues and no open PRs in jmgirard/cairn.
- 2026-11-02: rule (4) evidence: since 2026-10-22, the easystats repos hold six non-hotfix PRs by the operator. Five remove tests, and insight#1301 opens "As discussed in #1295". None breaks the rule, and the only plan file on disk from that time, datawizard M013, resolves issue #48. PR 487's review of 2026-11-02 reads "In summary: Contour lines should not be removed from plots".
- 2026-11-02: question set: which repos the review rules cover, whether a guest PR names an approved removal, and whether the plan checks rule (4) — the user sent "a better approach is to flag during PLANNING when a maintainer decision is needed and then pose the question before continuing" and picked no option. That message settles the third. The first two took the narrower reading: guest only, because D-108's owner half needs the user's decision, and no PR body line.
- 2026-11-02: plan gate chose a draft that the user posts over a post the plan makes, because the rulebook says nothing cairn writes reaches the maintainers and `/milestone` §4 already works this way, and the second audit found rerun, quoting, and started-row faults in a posting flow; falsified by users who ask the plan to post.
- 2026-11-02: plan gate chose no plan-anyway option over offering one, because rule (4) and the easystats instructions say to wait, and a typed override still works and is logged; falsified by users who keep typing that override.
- 2026-11-02: plan gate kept the review chip beside the plan flag because a plan can miss a removal and only the branch can count it; falsified by a run of guest reviews in which the plan had flagged every planned removal.
- 2026-11-02: criteria audit (full mode, two fresh Opus readers): 26 and 27 findings, all taken or answered. Second-round fixes: the operator's login is left out of agreement, the agreement read covers issue bodies and all of the operator's PRs for the work, a fix that `/hotfix` sent over is not exempt, design choices are limited to user-visible ones with more than one fitting reading, a maintainer's no goes to the flaw question, the draft is composed after the set's answers, criteria name what the skill text requires, cases are cut before their dispositions, the reader retry moved to T4, and route (b) skips the render. Answered with no change: the audit's cost on a stopped plan is accepted, and the PR 487 replay stays a task because a render in another repo is not a property of this deliverable. Its limit stands: the default case can show less loss than other inputs, and the count in `planned removal` covers those.

## Decisions

## Review
