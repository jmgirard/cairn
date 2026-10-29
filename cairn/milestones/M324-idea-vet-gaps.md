<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M324: Settle vague ideas and ask about flawed ones

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes what `/milestone-plan` and `/hotfix` ask adopters
- **Branch/PR:** m324-idea-vet-gaps, https://github.com/jmgirard/cairn/pull/337

## Goal

The idea vet settles a concern that one fitting reading of the request avoids, and asks the user about a concern that no fitting reading avoids.

## Scope

**In:** `/milestone-plan` step 2's idea vet sorts each concern as a gap or a flaw. Step 3 asks about flaws, and about a gap only when fitting readings give the user different behavior. Step 4's `idea vet:` line tags each concern. `/hotfix` step 1's vet sorts concerns the same way. A flaw in a name, argument, or behavior that the fix's diff leaves as it was no longer stops a hotfix and becomes a candidate row. This absorbs the parked candidate row "Do not stop fixes on old naming flaws". The hand-run guard `skills/tests/test_idea_vet.py`, the README, the CHANGELOG Unreleased vet entry, and a D-entry that narrows D-204 follow.

**Out:** A fresh reader for the vet stays rejected (D-204), with no row. `/milestone` §4 gets no vet of its own (D-204's Consequences). A count of past misroutes is not possible, because archives keep no `idea vet:` line, so there is no row for it.

## Acceptance criteria

- [x] AC1: `skills/milestone-plan/SKILL.md` step 2's **Idea vet.** paragraph sorts each concern it finds. If one reading of the request avoids a set of concerns, each of them is a gap. That reading fits the request's words and the records it cites. Its user-visible behavior is behavior that the request's words name or leave open. Nothing the request asks for is left out. A reading whose user-visible behavior differs from behavior the words name is not such a reading. A concern that this one reading cannot also avoid is a flaw.
- [x] AC2: The same paragraph says that the plan drafts the criteria to that reading. The plan asks nothing about a gap, with one exception. That exception is a gap where another reading also fits the request and gives different user-visible behavior. Such a gap goes to step 3's set. Before the vet sorts a concern on a candidate row's request, it reads each record the row cites.
- [x] AC3: Step 3's idea-vet bullet poses only flaws, each with an option not to build. It says that the agent never decides a flaw. Step 3's "choices that the request leaves open" bullet poses each gap that AC2 sends to the set. That question recommends the reading taken and has no option not to build. Step 3's "Work chosen at the set" arm ends with its goal-wrong close on a flaw. It ends the same way on a gap of AC2's exception. The agent decides any other gap there.
- [x] AC4: Step 2 states the form of the `idea vet:` work-log line. Each concern is a clause tagged `gap` or `flaw`. A gap carries the reading taken, and a flaw carries the set's answer. With no concern, the line says that the vet found none.
- [ ] AC5: `skills/hotfix/SKILL.md` step 1's **Idea vet (M306).** paragraph sorts concerns by AC1's test. For a gap that is not one of AC2's exception, the fix takes the reading, and the chat result names it. A gap of AC2's exception takes the over-the-bar route, because a choice between its readings is a design decision, and the route's candidate row or close block names the readings. A flaw in a name, argument, or behavior that the fix's diff changes takes the over-the-bar route, as now. A flaw only in a name, argument, or behavior that the fix's diff leaves as it was does not stop the fix, and the hotfix goes on. If the run reaches step 7, step 7 adds a candidate row that names the flaw (search-first applies). A close block that ends the run before step 7 names the flaw. On the merged-PR re-entry the vet runs after the merge. When step 7 runs, a flaw goes in its close block, and a flaw the merged diff leaves as it was gets the candidate row there. The guest change route's vet sentence gives a concern on the changed diff the same dispositions.
- [x] AC6: On the branch head, the `verify` slot passes. That slot is both gating `python3 -m unittest` suites, `claude plugin validate` on both manifests, and `claude plugin test`.
- [x] AC7: Four doc sites say that the agent settles a gap without a question unless its reading changes what you get. They also say that the agent asks you about a flaw. The sites are README.md's `/milestone-plan` row, its `/hotfix` row, and its "Answer two questions in a run" bullet. The fourth site is the CHANGELOG Unreleased entry "The plan and the hotfix question the request before they build it." The `/hotfix` row and that entry also say that a flaw in behavior the fix leaves as it was does not stop a hotfix.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T1
- AC5 → T3, T7, T8
- AC6 → T4, T6
- AC7 → T5, T8

## Tasks

- [x] T1: Edit `/milestone-plan` step 2's Idea vet paragraph (`skills/milestone-plan/SKILL.md:257`) and step 4's Idea-vet line bullet (`:627`) (AC1, AC2, AC4). Add a gap example beside the winsorize flaw example.
- [x] T2: Edit step 3's choices-left-open bullet, its idea-vet bullet (`:389`), and the "Work chosen at the set" arm (`:401`) (AC3).
- [x] T3: Edit `/hotfix` step 1's Idea vet paragraph (`skills/hotfix/SKILL.md:52`), the guest change route's vet sentence (`:224`), and step 6's approval chip text (AC5).
- [x] T4: Update `skills/tests/test_idea_vet.py`. Re-pin each changed phrase, and add one assertion per new clause. Show each new pin red by deleting its clause, and log the hand-run `skills/tests` result. The mutation-harness EXEMPT entry stays.
- [x] T5: Edit the three README vet sites and the CHANGELOG Unreleased vet entry (AC7). Append D-224, which narrows D-204 and names its D-108 door.
- [x] T6: Run the `verify` slot on the branch head (AC6).
- [x] T7: Review return 1: have step 7 write the hotfix's left-as-it-was flaw row in its docs-only commit, so it is never left uncommitted in owner mode (AC5).
- [x] T8: Carry out the AC5 amendment: an exception gap takes the hotfix's over-the-bar route, the chip naming and its stand-in list go, and README, CHANGELOG, and D-224's chip sentence follow (AC5, AC7).

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: milestone — changes skill behavior and needs a design decision.
- 2026-10-29: idea vet: gap — "a reasonable reading" was undefined, resolved as one reading that fits the words and cited records, names or leaves open the user-visible behavior, and drops nothing asked; no flaw.
- 2026-10-29: lessons used: 2026-07-24 (M112, extended M249, used M323); 2026-08-17 (M148, extended M182, used M323); 2026-08-22 (M152, extended M287, used M323); 2026-07-16 (M56+M65, consolidated M78/M83/M124, extended M121/M138, corrected M144, trimmed M147, used M323).
- 2026-10-29: collision: narrows D-204 (decided at plan, D-224 at T5); extends M306 (archived); absorbs the parked row "Do not stop fixes on old naming flaws", whose promotion condition has not held, at the user's choice in the question set.
- 2026-10-29: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-29: door: D-108 passes. Narrowing what the vet asks is its carve-out. The tag and the hotfix row rest on the retained trigger: the shipped vet asked the user about vague cairn-written rows that the agent could settle (user report, 2026-10-29).
- 2026-10-29: criteria audit (full, fresh Opus reader): 10 findings, all taken. Gap test bound to user-visible behavior (1). One reading covers all gaps (2). Exception baseline is another fitting reading (3). "Unclear" replaced by a provenance read before sorting (4). Step 3 names which bullet poses a gap (5). D-108 door named (6). Hotfix gap exception at the approval chip (7). Old flaw bound to the fix's diff, and the merged-PR re-entry writes the row (8). Hand-run `skills/tests` dropped from AC6 per D-109 (9). AC7 names its four sites, not a grep (10).
- 2026-10-29: question set: a gap whose fitting readings give different behavior is asked, not decided — ask (recommended).
- 2026-10-29: question set: a hotfix flaw in what the fix's diff leaves as it was lets the fix go on with a candidate row — fix goes on (recommended).
- 2026-10-29: plan gate chose the one-reading test over a rule that only cairn-written candidate rows skip the vet question, because a user's own vague request has the same gaps and a cairn row can hold a real flaw; falsified by a gap the agent settled that the user would have read differently.
- 2026-10-29: M324 in-progress on m324-idea-vet-gaps; untracked `cairn-probe.log` and `tsconfig.json` left unstaged.
- 2026-10-29: T1 done: step 2's Idea vet sorts gap and flaw, reads a candidate row's cited records first, sends an exception gap as an open choice, and tags the `idea vet:` line; step 4's bullet already points at step 2's form, unchanged. Gap example added beside the winsorize flaw. Both suites green.
- 2026-10-29: T2 done: step 3's open-choices bullet takes an exception gap (reading recommended, no option not to build); the idea-vet bullet now poses only flaws; "Work chosen at the set" closes on a flaw or an exception gap, and the agent decides other gaps.
- 2026-10-29: T3 done: `/hotfix` step 1's vet reads a named row's cited records, sorts by the plan's test, names gap readings in chat and an exception gap at step 6's chip (guest handoff chip too); a flaw the fix's diff changes goes over the bar, one it leaves as it was gets a row written as the over-the-bar row is (step 7's docs-only commit) and the fix goes on, merged-PR re-entry included; change route takes the vet's dispositions. Both suites green.
- 2026-10-29: T4 done: `test_idea_vet.py` re-pinned (12 broken pins) and extended to 34 tests; a scratch script deleted each of its 54 pinned phrases from the flattened skill text in turn, and each deletion turned a test red. Hand-run `skills/tests`: 987 tests OK. Mutation-harness EXEMPT entry unchanged.
- 2026-10-29: T5 done: README `/milestone-plan` row, `/hotfix` row, and "Answer two questions in a run" bullet, and the CHANGELOG Unreleased vet entry (edited in place, still unreleased) describe the gap and flaw sort and the hotfix old-flaw row; D-224 appended. Validate and both suites green.
- 2026-10-29: T6 done: `verify` slot green on f7237258 (both suites exit 0, plugin and marketplace validate exit 0, `claude plugin test` 2466 pass 0 fail in 140 s).
- 2026-10-29: claim audit: 38 claims read, 3 corrected — README.md, CHANGELOG.md, skills/hotfix/SKILL.md. Docs' flaw definition now matches step 2's "the reading taken cannot avoid". `/hotfix` names an exception gap in the stand-in chip on paths with no step 6 chip (merged-PR nothing-owed acceptance chip, change route's push chip), pinned in the guard. CHANGELOG states that work chosen at the set stops and the rerun asks. Guard 35 tests, 55 pins red on deletion; `skills/tests` 987 OK; both suites green after the fix.
- 2026-10-29: M324 to review.
- 2026-10-29: review pass 1: four lenses, 28 findings; 16 fix now on the branch, 8 rejected, 2 noted, 4 to the AC5 amendment. Hand-run `skills/tests` 977 OK after the trim.
- 2026-10-29: review return 1: diff-bug #1, the hotfix's left-as-it-was flaw row was never committed in owner mode; fixed on the branch in review pass 1 (step 7 writes it).
- 2026-10-29: amendment routed: AC5 — an exception gap named at the hotfix approval chip conflicts with the hotfix bar and cannot act on the other reading (blame-history #2, diff-bug #3, #4, #10); AC5 also says step 1 adds the left-flaw row, which step 7 now writes (diff-bug #1).
- 2026-10-29: minor amendment: T7 (review return 1, done in review pass 1) and T8 (the AC5 amendment, pending its re-audit) added; Coverage AC5 → T3, T7, T8 and AC7 → T5, T8.
- 2026-10-29: re-audit: AC5 (full) — 6 findings: gap sentences contradicted (taken), event order wrong (taken), merged-PR row unconditional (taken), D-224's chip clause needs a superseding entry (taken, T8), README/CHANGELOG chip claims go stale (taken as doc edits, AC7 not widened per D-118), resumed owner-arm merge skips the vet (not taken: widening after a defect return; to a candidate row).
- 2026-10-29: re-audit: AC5 (full) — 3 findings: the merged-PR clause reads as if step 7 always runs (reworded), the draft widens past the original (chat clause dropped; the close-block clause kept and logged as a widening), a run that ends before step 7 leaves the close block as the flaw's only record, a D-042 residual (named in the new D-entry). Second re-audit on AC5: further wording goes to the user.
- 2026-10-29: amendment return: AC5 — "For a gap that is not one of AC2's exception, the fix takes the reading, and the chat result names it. A gap of AC2's exception takes the over-the-bar route, because a choice between its readings is a design decision, and the route's candidate row or close block names the readings. A flaw in a name, argument, or behavior that the fix's diff changes takes the over-the-bar route, as now. A flaw only in a name, argument, or behavior that the fix's diff leaves as it was does not stop the fix, and the hotfix goes on. If the run reaches step 7, step 7 adds a candidate row that names the flaw (search-first applies). A close block that ends the run before step 7 names the flaw. On the merged-PR re-entry the vet runs after the merge. When step 7 runs, a flaw goes in its close block, and a flaw the merged diff leaves as it was gets the candidate row there."
- 2026-10-29: question set (amendment stop): should a hotfix stop and send a two-reading gap to a plan instead of naming it at the approval chip — stop and plan (recommended). Widening adopted at the user's selection: AC5 gains "A close block that ends the run before step 7 names the flaw".
- 2026-10-29: T8 done: hotfix step 1 sends an exception gap over the bar with its readings named, step 7 writes the left-flaw row if reached, the merged-PR clause is conditional on step 7; step 6's gap chip sentence and the stand-in chip list removed; README `/hotfix` row and CHANGELOG entry say the hotfix stops so a plan can ask; D-225 supersedes D-224's chip clause and names the D-042 residual; candidate row "Vet a hotfix on a resumed merge" added (search-first: no overlap).
- 2026-10-29: claim audit: 17 claims read, 2 corrected — README.md, CHANGELOG.md (the gap trigger is a fitting reading with different behavior, and the merged-PR exception); scoped to the amendment's diff since 485024bd.
- 2026-10-29: M324 to review.

## Decisions

## Review

Evidence gathered 2026-10-29 on ecc512ab (branch level with origin/main).

- AC1: `skills/milestone-plan/SKILL.md:275-280` holds the sort: one reading avoiding a set of concerns makes each a gap, the reading fits words and cited records, its behavior is what the words name or leave open with nothing asked left out, a reading differing from named behavior is not such a reading, and a concern that reading cannot also avoid is a flaw. Pinned by `test_gap_is_what_one_reading_avoids` (guard OK).
- AC2: `skills/milestone-plan/SKILL.md:280-284`: the plan drafts to that reading and asks nothing about a gap with one exception, another fitting reading with different user-visible behavior, which goes to step 3's set; `:272` reads each record a candidate row cites before sorting. Pinned by `test_gap_asks_nothing_but_the_exception`, `test_reads_a_rows_cited_records_first`.
- AC3: `skills/milestone-plan/SKILL.md:408-417`: the idea-vet bullet poses only flaws with the do-not-build option and says the agent never decides a flaw; `:400-403`: the open-choices bullet takes each gap step 2 sends, its question recommending the reading taken with no do-not-build option; `:419-426`: "Work chosen at the set" closes on a flaw or a sent gap, and the agent decides any other gap. Pinned by `test_step3_gap_is_an_open_choice`, `test_step3_cap_rule`, `test_step3_no_milestone_left_and_never_agent_decided`, `test_work_chosen_at_the_set`.
- AC4: `skills/milestone-plan/SKILL.md:290-293` states the `idea vet:` line form: each concern a clause tagged `gap` or `flaw`, or none found; a gap carries the reading taken, a flaw the set's answer. Pinned by `test_work_log_line_form`, `test_line_carries_reading_or_answer`.
- AC5: `skills/hotfix/SKILL.md:62-64` reads a named row's cited records and sorts by the plan's test, the fix taking the gap's reading; `:65-69` names an exception gap in step 6's chip (or the stand-in chip on paths with none) and states the result in chat with each gap's reading; `:70-75` sends a flaw the diff changes over the bar; `:76-79` lets the fix go on with a candidate row for a flaw the diff leaves as it was; `:80-84` puts a flaw in step 7's close block on the merged-PR re-entry, the left flaw also getting its row; `:241` gives the change route the vet's dispositions; `:437-439` step 6's chip text. Pinned by the `TestHotfixIdeaVet` tests (guard OK, 35 tests).
- AC6: `verify` on ecc512ab: `scripts/tests` exit 0, `hooks/tests` exit 0, `claude plugin validate` plugin.json exit 0 and marketplace.json exit 0, `claude plugin test .` exit 0 (2466 pass, 0 fail, 139 s).
- AC7: README.md:772 (`/milestone-plan` row: flaw posed with do-not-build, gap settled without a question unless another fitting reading changes what you get), README.md:776 (`/hotfix` row: gap settled unless it changes what you get, then named at the approval gate; a flaw in what the fix changes stops it; a flaw in what the fix leaves does not and becomes a candidate row), README.md:872-877 ("Answer two questions in a run": asked about each flaw; a gap settled unless another fitting reading gives different behavior), CHANGELOG.md:345-372 (Unreleased entry: gap settled unless readings differ, flaw asked, and a flaw the fix leaves as it was does not stop the hotfix). Read 2026-10-29.
- Consistency gate: `cairn_validate` all checks passed; coverage complete; no principle changed, so `cairn_impact` skipped; verify green on the review head (AC6); marketplace validate prints no `version` warning; CHANGELOG Unreleased vet entry carries this change, no milestone ids in added lines.
- Copilot: request made on PR #337 (exit 0); state still `none` after it, so Copilot request on PR #337 may not be recorded by GitHub (used-up Copilot credits are one cause). No second request.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the left-as-it-was flaw row is never committed in owner mode and can leak into the hotfix branch or stay dirty on a decline — fix now (step 7 writes it in its one docs-only commit after its matched-row edits, guest on disk; a close before step 7 names the flaw); floor return (load-bearing), fixed 3600a485
- diff-bug #2: the new row can be taken by the candidate-row match and deleted at step 7 — fix now (same change: written at step 7, after the match), fixed 3600a485
- diff-bug #3: a gap named as a choice at the chip has no way to pick the other reading — amendment routed AC5
- diff-bug #4: an exception gap at the chip contradicts the hotfix bar's design-decision stop — amendment routed AC5
- diff-bug #5: "the fix takes that step's reading" is undefined for an adopted PR or merged diff — fix now (a PR diff that takes another reading has a flaw in what it changes); its guest change-route part rejected, false: a maintainer's requested item is part of the request that route vets, fixed 3600a485
- diff-bug #6: an exception gap's question can fall to the question cap — fix now (it counts among the questions that matter most), fixed 3600a485
- diff-bug #7: a gap close is labelled the goal-wrong stop — fix now (the goal is not settled until the user picks a reading), fixed 3600a485
- diff-bug #8: guest scope still says the vet "poses that as a concern" — fix now ("as a flaw"), fixed 3600a485
- diff-bug #9: the hotfix citation read covers only argument-named rows — fix now (rows that describe the bug too), fixed 3600a485
- diff-bug #10: the stand-in chip list misses the merged-PR over-the-bar path — amendment routed AC5 (the chip naming goes)
- diff-bug #11: a cited record that no longer exists has no rule — fix now (reads each cited record "that still exists"), fixed 3600a485
- diff-bug #12: guard growth when new skill rules owe no prose guard, and a docstring milestone cite — fix now (same as prior-review #1, #2), fixed 3600a485
- diff-bug #13: path check — noted; dirty tree and moved remote failed only through #1
- diff-bug #14: D-204 carries no forward pointer to D-224 — reject, false: the bounded read back-references D-204's id, which finds D-224's heading
- blame-history #1: the plan never says which reading it takes, so a concern only another reading avoids sorts both ways — fix now (the plan takes the fitting reading that avoids the most concerns), fixed 3600a485
- blame-history #2: the hotfix asks about an exception gap only after the code exists, against the hotfix bar — amendment routed AC5
- blame-history #3: an exception-gap question can fall to the cap — fix now (same as diff-bug #6), fixed 3600a485
- blame-history #4: a gap reading may contradict an uncited D-entry — reject, false: the collision check reads DECISIONS.md and surfaces a settled record as a question, and the vet names a settled concern with its record
- blame-history #5: the gap example is unclear — fix now (reworded), fixed 3600a485
- blame-history #6: the parked row is absorbed before its condition held — reject, planned change (user's choice at the question set)
- blame-history #7: the tag rests on D-108's trigger — reject, planned change (D-224 names the trigger)
- blame-history #8: D-109, D-162, M306 loop protection checked — noted
- prior-review #1: new pins for new skill rules, which the profile says owe no prose guard and M323 removed — fix now (pins for new clauses dropped; re-pins of existing members kept; 24 tests, 34 pins red on deletion), fixed 3600a485
- prior-review #2: bare milestone cite in the test docstring — fix now (cite removed), fixed 3600a485
- ripple #1: the hotfix row "names it as a design decision" while the hotfix goes on, against the tier rule — fix now (the fix itself needs no design decision; the row names one for later work), fixed 3600a485
- ripple #2: the parked row's text is stale — reject, planned change: step 9 hygiene graduates it (`started M324`)
- ripple #3: guest scope "poses that as a concern" — fix now (same as diff-bug #8), fixed 3600a485
- ripple #4: the settled-concern sentence names no tag — reject, false: it names the record whatever tag the concern takes
