<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M306: Vet an idea before planning its build

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP3, GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/milestone-plan` and `/hotfix` ask before they build work in an adopter's repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m306-idea-vet https://github.com/jmgirard/cairn/pull/320   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Before it plans a milestone or makes a hotfix, cairn asks if the requested behavior is correct, wanted, and framed right, and puts each concern to the user.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-plan` step 2 (the vet), step 3 (concerns as questions), step 4 (the work-log line), and the arm for work chosen at the question set. `/hotfix` step 1 (the vet of the behavior that the fix or PR diff produces). A hotfix concern goes over the hotfix bar. One D-entry. README's `/milestone-plan` and `/hotfix` rows. A CHANGELOG `## Unreleased` entry. A hand-run guard in `skills/tests`. The milestone absorbs the candidate row "Vet an idea before planning its build" in full.

**Out:** `/milestone` §4's issue look-in gets no vet of its own. Its `milestone` and `hotfix` verdicts hand the issue to `/milestone-plan` and `/hotfix`, which vet it. No row holds this. The working session answers the three questions itself, and no fresh reader is spawned for the vet, by the user's choice at the question set. No row holds this.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [x] AC1: `skills/milestone-plan/SKILL.md` step 2 holds a vet of the request as framed. The vet asks three questions. (1) Is the requested behavior correct by its field's standards (for example statistical or technical), and does it do what its name says for every input type it touches? (2) Do the project's users want it, beyond what the request literally asks? (3) Is it framed right, in its name, its function, and its arguments? Step 2 states that an issue's wording or a maintainer's agreement answers none of the three. It states that the vet runs at step 2 on every request that names work, a request that names an issue and a request that a router sent included.
- [x] AC2: In the same skill, step 3's set poses the vet's concerns within its cap, as one question per concern or as one combined question when the cap would be passed. Each such question has a recommendation, and its options include not building the work. Where another framing fits, they also include building it under another name or shape. Choosing not to build writes no milestone file and leaves any source candidate row in place. Step 4 writes one work-log line `idea vet: <result>` in the first milestone file it writes. The line names each concern in a clause, or says that the vet found none.
- [x] AC3: In the same skill, for a request that names no work, the vet runs on the work chosen at the question set before step 4 writes a file. If it finds a concern, the plan writes nothing and ends with a close block. The close block names the concern, and its fenced command is `/milestone-plan` with the chosen work named.
- [x] AC4: `skills/hotfix/SKILL.md` step 1, on every entry that runs the tier check, asks the same three questions of the behavior that the fix or PR diff produces, documented behavior included. It states the result in chat. A concern counts as a design decision and takes step 1's over-the-bar route, and the candidate row or close block that the route writes names the concern. On the merged-PR re-entry the vet runs after the merge, and the concern goes in step 7's close block.
- [x] AC5: `cairn/DECISIONS.md` gains entry D-204. It records the vet and the alternatives that the plan rejected, with their falsifiers. It records whether D-108's door applies and why, naming the shipped-behavior defect if the door is passed on its trigger: in datawizard M012, `/milestone-plan` planned issue #48 as written, and the built option does not winsorize.
- [x] AC6: README's `/milestone-plan` and `/hotfix` rows and a CHANGELOG `## Unreleased` entry under `### New` state the three questions. They state that the plan's question set poses each concern with a do-not-build option. They state that a hotfix concern leaves a candidate row or a `/milestone-plan` next command that names the concern, and stops the hotfix unless its PR is already merged.
- [x] AC7: The profile's `verify` slot passes at the branch head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3
- AC2 → T1, T3
- AC3 → T1, T3
- AC4 → T2, T3
- AC5 → T4
- AC6 → T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: In `skills/milestone-plan/SKILL.md`, add the vet paragraph to step 2 after the collision check and the inbox sweep. Add vet concerns to step 3's list of questions, with the cap rule. Add the `idea vet:` line to step 4's work-log lines beside the tier-check line. Add the arm for work chosen at the question set. Trace the no-work arm's close to its rerun (LESSONS M172).
- [x] T2: In `skills/hotfix/SKILL.md` step 1, add the vet beside the tier check, for every entry that tier-checks a fix or a PR diff, the merged-PR re-entry included. Send a concern through the existing over-the-bar route.
- [x] T3: Add `skills/tests/test_idea_vet.py`. Pin each of the three questions, the not-proof sentence, the cap rule, the do-not-build option and its no-write result, the work-log line, the no-work arm, and the hotfix route, with one assertion per member (LESSONS M171). Delete each pinned sentence and see its assertion fail before you trust the pass.
- [x] T4: Append D-204 per AC5.
- [x] T5: Edit README's two rows and add the CHANGELOG entry. Grep both for wording that the change makes stale (LESSONS M112).
- [x] T6: Run the `verify` slot from the repo root, and also hand-run `python3 -m unittest discover -s skills/tests`, which gates nothing. Examine each exit code.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a new step in the conduct of two skills, which needs design decisions.
- 2026-10-21: question set: what /hotfix checks — every hotfix, documented behavior included (over plan only).
- 2026-10-21: question set: who answers the three questions — the working session (over a fresh reader per plan and hotfix).
- 2026-10-21: collision check: candidate row "Vet an idea before planning its build" absorbed in full. D-108's door applies at least to the `idea vet:` record line; the plan reads it as passed on its retained trigger, a shipped-behavior defect (in datawizard M012 `/milestone-plan` planned issue #48 as written and shipped an option that does not winsorize). D-201 differs: its row named no shipped defect. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-21: lessons harvested: M171 (pin each list member), M172 (trace each new route to where it lands), M112 (grep README and CHANGELOG for stale wording), M148 (reword new prose near pinned markers), M56 (skill edits run both gating suites).
- 2026-10-21: plan gate chose the working session's own answers over a fresh reader per plan and hotfix because the three questions are written into the skill at no added cost; falsified by a request built after this merge whose concern the session's vet missed and a fresh reader on the same request finds.
- 2026-10-21: plan gate chose to vet work chosen at the question set and end with a rerun on a concern over logging the vet as not run because the candidate row asks for the check on each plan; falsified by reruns that surface no concern a later review would have caught.
- 2026-10-21: plan gate chose to vet every hotfix over vetting only behavior a report, issue, or PR asks for because the hotfix bar already sends that behavior to a plan, so the narrow check changed no outcome; falsified by a hotfix vet concern that the plan's vet would have raised anyway.
- 2026-10-21: criteria audit (full mode, one fresh Opus reader): 8 findings, then 2 on a re-audit of the criteria the answers changed, all fixed. The Goal no longer says the request is never built as written. AC1 asks about correctness by the field's standards and covers requests that name work. AC2 keeps concerns within the cap, says a do-not-build choice writes nothing and keeps the row, and names the file for the line. AC4 covers every tier-check entry and the merged-PR re-entry. AC5 asks whether the door applies. AC7 drops the hand-run suite, which gates nothing; T6 runs it. AC3 and AC6 passed.
- 2026-10-21: T1 done: `/milestone-plan` step 2 gains the idea vet after the checker-regress paragraph, step 3 gains the concerns bullet and the "Work chosen at the set" arm, step 4 the idea-vet line; the no-work arm's close reruns `/milestone-plan` with the work named, whose step-2 vet and step-3 set pose the concern. Untracked `cairn-probe.log` and `tsconfig.json` left unstaged. verify green.
- 2026-10-21: T2 done: `/hotfix` step 1 gains the idea vet after the over-the-bar paragraph; it runs on every entry that runs the tier check, and the merged-PR re-entry's "Tier check the merged diff as above" reaches it, its concern riding in step 7's close block. verify green.
- 2026-10-21: T3 done: `skills/tests/test_idea_vet.py`, 17 tests; a scratchpad probe planted 24 removals (16 in the plan skill, 8 in the hotfix skill), each one a failure and none an error, with the unmutated control green and the skill files restored.
- 2026-10-21: T4 done: D-204 appended; it reads D-108's door as applying to the `idea vet:` records line and passed on its retained trigger, and records the three rejected alternatives with their falsifiers.
- 2026-10-21: T5 done: README's `/milestone-plan` and "Fix a reported bug quickly" rows and a CHANGELOG Unreleased `### New` entry; the adopt-a-PR row says "holds it to the same bar", which now includes the vet, so it stays. A grep of README for the plan's step list found no other stale description.
- 2026-10-21: T6 done: the hand-run `skills/tests` first failed twice. The idea-vet paragraph sat inside the slice that `test_stakes_tier`'s checker-regress fixture pins, so it moved before the collision check (LESSONS M148, the new text moves, the pinned text stays), and `test_idea_vet` gained its EXEMPT line in `test_mutation_harness.py`. Then 947 tests OK, the 24-plant probe all red again, verify green (all five exit 0), and `cairn_validate` green.
- 2026-10-21: claim audit: 16 claims read, 2 corrected — README.md, CHANGELOG.md (a hotfix concern leaves a candidate row or a `/milestone-plan` command rather than "sends the work to a milestone plan"; the question set "poses each concern", since the cap rule can combine them). The agent also dropped "first" from the README hotfix row, since the merged-PR re-entry vets after the merge.
- 2026-10-21: substantive amendment: AC6's last two sentences now match the corrected docs, wording only, the deliverable unchanged: "They state that the plan's question set poses each concern with a do-not-build option. They state that a hotfix concern leaves a candidate row or a `/milestone-plan` next command that names the concern, and stops the hotfix unless its PR is already merged."
- 2026-10-21: re-audit: AC6 (full) — one finding: "stops the hotfix" is false on the merged-PR re-entry; fixed with "unless its PR is already merged" in AC6, README, and CHANGELOG. Checkpoint: the fixed wording's own fresh reader is still running.
- 2026-10-21: re-audit: AC6 (full) — met as written; two wording points: the hotfix row names the questions by reference to the plan row, and "the `/hotfix` rows" could be read to include "Take in an outside pull request". AC6 is left unchanged (a further change is the stop); that README row now says the bar includes the three questions, so either reading holds.
- 2026-10-21: all tasks done; verify green; status set to review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->

Pass 1 (2026-10-21), on head a42f1746, branch synced with origin/main (0 commits behind). PR #320 opened at review start (Copilot arm); Copilot requested, state `pending`.

- AC1: `skills/milestone-plan/SKILL.md:257-273`, the **Idea vet.** paragraph inside step 2 (step 2 at :225, step 3 at :348): the three questions at :259-263 as worded in AC1, "An issue's wording or a maintainer's agreement answers none of the three" at :263-264, "The vet runs at step 2 on every request that names work, a request that names an issue and a request that a router sent included" at :265-267. `test_idea_vet` pins each (17 tests OK).
- AC2: step 3's bullet at `skills/milestone-plan/SKILL.md:360-366`: concerns posed within the cap, one per concern or one combined question where separate questions pass the cap; each with a recommendation; options include not building the work and, where another framing fits, another name or shape; not building writes no milestone file for that work and leaves any source candidate row in place. The `idea vet: <result>` line goes in the first milestone file step 4 writes, naming each concern or saying none was found (:270-273), and step 4's **Idea-vet line.** bullet at :591.
- AC3: **Work chosen at the set.** at `skills/milestone-plan/SKILL.md:368-373`: for a request naming no work the vet runs on the chosen work before step 4 writes a file; a concern means the plan writes nothing and ends with a close block naming the concern, fenced `/milestone-plan` with the chosen work named.
- AC4: `skills/hotfix/SKILL.md:52-64`, **Idea vet (M306).** inside step 1 right after the over-the-bar paragraph: "Every entry that runs this tier check also vets the behavior that the fix or the PR diff produces, documented behavior included", the same three questions, "State the result in chat", a concern takes the over-the-bar route and the row or close block names it, and on the merged-PR re-entry the concern goes in step 7's close block. The re-entry bullet's "*Tier check* the merged diff ... as above" reaches it.
- AC5: `cairn/DECISIONS.md:7413`, D-204: Decision records the vet; **Rejected:** names three alternatives, each with a "Falsified by" clause; **Door:** says D-108's door applies (the `idea vet:` records line) and is passed on its retained trigger, naming datawizard M012, where `/milestone-plan` planned issue #48 as written and the option "is not winsorizing".
- AC6: `README.md:750` (`/milestone-plan` row: the three questions, "an issue's wording is not proof", the question set "poses each concern with an option not to build the work"); `README.md:754` (hotfix row: same three questions, "A concern leaves a candidate row or a `/milestone-plan` next command that names it, and stops the hotfix unless its PR is already merged"); `README.md:755` (adopted PR: the bar includes the three questions); `CHANGELOG.md:162` under `## Unreleased` → `### New` states all three.
- AC7: verify slot at the review head, from the repo root, each exit code read: `scripts/tests` 0, `hooks/tests` 0, plugin validate 0, marketplace validate 0, `claude plugin test .` 0.
- Gate: `cairn_validate` exit 0 (all checks passed); no principle text changed, so `cairn_impact` skipped; marketplace validate has no `plugins[N].version` warning (0 lines); CHANGELOG Unreleased `### New` entry present with no milestone number; hand-run `skills/tests` 947 OK (gates nothing, D-109). Diffstat: 9 files, +284 −14.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: on the merged-PR re-entry a vet concern took the over-the-bar route, which waives the re-entry's regression test, baseline, verify, and changelog checks — fix now: the concern now waives none of them and its candidate row still names it, fixed b8c194d1
- diff-bug #2: a row a hotfix concern writes could be tiered `hotfix` by a later plan and sent back, a loop — fix now: the row or close names the concern as a design decision, which the tier check reads as a milestone, fixed b8c194d1
- diff-bug #3: "not building" named no ending when the plan is left with no milestone — fix now: the plan writes nothing and ends with the close block naming each concern, fixed b8c194d1
- diff-bug #4: a typed request not built leaves the concern unrecorded — reject (planned change): not building is the user's explicit choice at a chip, IP3 bars silent drops only, and the close block now names the concern
- diff-bug #5: the rulebook's "ask the 3 that matter most" could leave a concern to the agent — fix now: an idea-vet question always counts among them, fixed b8c194d1
- diff-bug #6: one combined question cannot carry a separate answer per concern — reject (planned change): AC2 specifies the combined form for past-cap concerns
- diff-bug #7: "build anyway" left no record of the answer — fix now: each concern in the `idea vet:` line carries the set's answer, fixed b8c194d1
- diff-bug #8: the no-work close is not on the closed stop list, re-asks the set, and can hit an existing planned milestone — fix now in part: the close is named as the goal-wrong stop, fixed b8c194d1; the rest reject (planned change, AC3; a no-work set chooses unplanned work)
- diff-bug #9: a framing concern about a name the fix leaves as it is stops a valid fix — follow-up: candidate row "Do not stop fixes on old naming flaws"
- diff-bug #10: the hotfix restated question (2) without "beyond what the request literally asks" — fix now, fixed b8c194d1
- diff-bug #11: the vet runs before the collision check and can re-raise a concern a D-entry settled — fix now: such a concern is named with its record, fixed b8c194d1
- diff-bug #12: `/milestone` §4 can give a hotfix verdict that the hotfix vet then stops — reject (planned change): Scope Out
- diff-bug #13: D-204 annotates neither D-162 nor the gate entry — reject (false): a concern was already a design decision under the hotfix bar, so D-162's tiers are unchanged
- diff-bug #14: one long line at :362 — reject (style)
- diff-bug #15: "vetted at step 3" was unpinned — fix now, fixed b8c194d1
- blame-history #1: the hotfix vet contradicts the rulebook's hotfix bar — reject (false): the bar excludes work that "requires a design decision", and a concern counts as one
- blame-history #2: same as diff-bug #5 — fix now, fixed b8c194d1
- blame-history #3: same as diff-bug #2 — fix now, fixed b8c194d1
- blame-history #4: the no-work arm needs a second set against D-144's one set, and vet questions may be agent-settleable — reject (planned change): the rerun is a new run, and not building asked-for work is the user's call
- blame-history #5: the hotfix vet is wider than the candidate row's wording — reject (planned change): the user chose "check every hotfix" at the question set
- blame-history #6: a concern after a merge leaves no durable record — fix now: the over-the-bar route's candidate row still names it, fixed b8c194d1
- blame-history #7: D-204's door reasoning confines D-108 to the record line — reject (false): the door is read as applying and passed on its trigger either way, and D-204 is not edited in place (IP4)
- blame-history #8: the winsorize example is specific to one repo — reject (planned change): it states the triggering case, and GP3 is met by the field-neutral questions
- prior-review #1: concerns as questions conflict with "asks only what the user alone can settle" — reject (planned change): not building or reframing asked-for work is the user's call
- prior-review #2: the vet has no stakes gate — reject (planned change): the user chose the working session's own answers at no added cost
- prior-review #3: the vet does not say to read the issue's text — fix now, fixed b8c194d1
- prior-review #4: the no-work rerun has no loop bound — reject (false): the rerun names the work, so its step-3 set poses the concern and the user answers it
- ripple #1: tracking-rules' "ask the 3 that matter most" — fix now in the plan skill (diff-bug #5), fixed b8c194d1; the rulebook line stays, since step 3 names its questions
- ripple #2: README's run section omitted the vet's questions — fix now, fixed b8c194d1
- ripple #3: the no-work close is not on the stop list — fix now (diff-bug #8), fixed b8c194d1
- ripple #4: the candidate row's wording differs from the shipped scope — reject (false): step 9 graduates the row
- ripple #5: same as diff-bug #10 — fix now, fixed b8c194d1
- copilot: skills/hotfix/SKILL.md:64 — the guest change route's post-edit tier check did not run the vet — fix now: that tier check now runs the idea vet on the changed diff, fixed b8c194d1
- Copilot level: Lite (set by GitHub's settings)
- Return floor: none of these demonstrates a criterion failing; diff-bug #1 is a defect on a rare path (a merged-PR re-entry with a concern) fixed in one sentence, judged not load-bearing. Probe: 34 plants red, control green; verify green at b8c194d1.
