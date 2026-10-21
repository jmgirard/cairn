<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M306: Vet an idea before planning its build

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP3, GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/milestone-plan` and `/hotfix` ask before they build work in an adopter's repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m306-idea-vet   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: `skills/milestone-plan/SKILL.md` step 2 holds a vet of the request as framed. The vet asks three questions. (1) Is the requested behavior correct by its field's standards (for example statistical or technical), and does it do what its name says for every input type it touches? (2) Do the project's users want it, beyond what the request literally asks? (3) Is it framed right, in its name, its function, and its arguments? Step 2 states that an issue's wording or a maintainer's agreement answers none of the three. It states that the vet runs at step 2 on every request that names work, a request that names an issue and a request that a router sent included.
- [ ] AC2: In the same skill, step 3's set poses the vet's concerns within its cap, as one question per concern or as one combined question when the cap would be passed. Each such question has a recommendation, and its options include not building the work. Where another framing fits, they also include building it under another name or shape. Choosing not to build writes no milestone file and leaves any source candidate row in place. Step 4 writes one work-log line `idea vet: <result>` in the first milestone file it writes. The line names each concern in a clause, or says that the vet found none.
- [ ] AC3: In the same skill, for a request that names no work, the vet runs on the work chosen at the question set before step 4 writes a file. If it finds a concern, the plan writes nothing and ends with a close block. The close block names the concern, and its fenced command is `/milestone-plan` with the chosen work named.
- [ ] AC4: `skills/hotfix/SKILL.md` step 1, on every entry that runs the tier check, asks the same three questions of the behavior that the fix or PR diff produces, documented behavior included. It states the result in chat. A concern counts as a design decision and takes step 1's over-the-bar route, and the candidate row or close block that the route writes names the concern. On the merged-PR re-entry the vet runs after the merge, and the concern goes in step 7's close block.
- [ ] AC5: `cairn/DECISIONS.md` gains entry D-204. It records the vet and the alternatives that the plan rejected, with their falsifiers. It records whether D-108's door applies and why, naming the shipped-behavior defect if the door is passed on its trigger: in datawizard M012, `/milestone-plan` planned issue #48 as written, and the built option does not winsorize.
- [ ] AC6: README's `/milestone-plan` and `/hotfix` rows and a CHANGELOG `## Unreleased` entry under `### New` state the three questions. They state that a plan concern becomes a question with a do-not-build option. They state that a hotfix concern sends the work to a milestone plan.
- [ ] AC7: The profile's `verify` slot passes at the branch head.

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
