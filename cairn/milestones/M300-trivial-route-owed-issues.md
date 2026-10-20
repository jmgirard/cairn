<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M300: A trivial edit keeps owed issues open

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes which GitHub issues an adopter's trivial-tier route closes   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m300-trivial-route-owed-issues   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In owner mode, the trivial route closes no issue whose number a kept candidate row holds as `#N` or an open milestone's `Resolves:` slot holds, and none after an open-PR read it could not finish or a failed check.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-plan` step 1's issue read (trivial route, owner mode) and the trivial option's description; one D-entry; README's trivial-edit row, M297's CHANGELOG `## Unreleased` entry, and the hand-run guard in `skills/tests/test_plan_tier_check.py`. Absorbs the candidate row "Keep owed issues open on a trivial edit" in full.

**Out:** a number named only in a deleted row's own detail stays unread and open, as D-195's Consequences state for that row; no row holds a change to it. An issue that an open milestone names only outside its `Resolves:` slot, or that a row names as a URL or as "issue 12", is not protected; no row holds this. Guest mode still reads and closes no issue. Telling an issue number from a review-finding number (`diff-bug #4`) in a kept row is not attempted: such a row leaves the issue open, and the option names it; no row holds this.

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

- [ ] AC1: `skills/milestone-plan/SKILL.md` step 1's issue read states that the route leaves alone a number that a kept row's text holds as `#N` with no digit right after it, in the row's title or its detail. It also states that the route leaves alone a number that the `Resolves:` header slot of a `planned`, `in-progress`, `blocked`, or `review` milestone file holds in that form. The trivial option's description names each number of a deleted row that such a reference holds as left alone, with its reason.
- [ ] AC2: In owner mode, step 1 states that when the open-PR read fails, `gh` cannot run for it, or it returns 100 PRs, the route closes no issue, and the trivial option's description names each number of a deleted row as left alone for that reason.
- [ ] AC3: Step 1 states that the issue read runs only after all five trivial-route checks pass, and that when a check fails the plan reads no issue and names no number for closing.
- [ ] AC4: `cairn/DECISIONS.md` gains an entry (next free id) whose heading states that it narrows D-195's kept-row clause and its Consequence that an issue named only in a row's detail stays open. It records the cases of AC1 to AC3, the rejected alternative of protecting only issue-shaped references in a kept row's detail with its falsifier, and whether D-108's door applies and why.
- [ ] AC5: README's trivial-edit row and the CHANGELOG `## Unreleased` entry "A direct edit closes the issue of the row it removes" state that the route also leaves alone an issue that a kept row names anywhere in its text and one that an open milestone's `Resolves:` slot names, and closes no issue when its check of the open pull requests fails or is cut short.
- [ ] AC6: The profile's `verify` slot passes at the branch head, and so does the hand-run `python3 -m unittest discover -s skills/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T4
- AC6 → T2, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: In `skills/milestone-plan/SKILL.md` step 1's issue read, widen the kept-row clause from the title reference to the whole row, add the open milestone's `Resolves:` slot, the failed or capped open-PR read, and the order after the five checks. With a failed check the option names no issue number at all. Check that the trivial option's description names each new reason, and trace each new path to the close it reaches (LESSONS M172).
- [x] T2: In `skills/tests/test_plan_tier_check.py`, replace the pinned kept-row phrases and pin each new sentence on its own (LESSONS M171). Show each new assertion red against the pre-change step 1 before trusting its green.
- [ ] T3: Append the D-entry (next free id) per AC4.
- [ ] T4: Edit README's trivial-edit row and M297's CHANGELOG Unreleased entry; grep both for the old wording first (LESSONS M112).
- [ ] T5: Run the `verify` slot and the hand-run `skills/tests` from the repo root, each exit code checked.

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

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: not run — work named at the question set.
- 2026-10-20: question set: which work to plan, with only one candidate row not parked and this the sixth milestone in a row on trivial-route and triage edges — plan a small fix (over parking the row or stopping).
- 2026-10-20: collision check: candidate row "Keep owed issues open on a trivial edit" absorbed in full; D-195 (the close rule) is narrowed by this milestone's D-entry; D-108's door does not apply, since the work fixes a shipped route's outward write and adds no conduct rule about verification or records. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-20: lessons harvested: M172 (trace each new path to its outward write), M171 (pin each list member), M112 (grep README and CHANGELOG for old wording), M148 (reword new prose near pinned markers).
- 2026-10-20: plan gate chose to protect any `#N` in a kept row's text over protecting only issue-shaped references, because review-finding numbers (`diff-bug #4`) share the spelling and a wrong protect only leaves an issue open, which the option names; falsified by a user who wants an issue closed that a kept row names only as a finding number.
- 2026-10-20: plan gate chose to edit M297's Unreleased CHANGELOG entry over adding a new one, because that behavior has not shipped in a release; falsified by a release cut before this merges.
- 2026-10-20: criteria audit (full mode, one fresh Opus reader): 5 findings, all fixed. The Goal narrowed to `#N` in a kept row and the `Resolves:` slot (Out names the rest); AC1's naming clause limited to deleted rows' numbers; AC2 scoped to owner mode, so guest mode keeps its own reason; AC4 states what the entry does to D-195 and no longer says "one"; AC5 also names a kept row's detail. AC3 and AC6 passed; T1 settles that a failed check names no number.
- 2026-10-20: implement started on branch m300-trivial-route-owed-issues; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-20: T1 done: step 1's issue read now runs after the five checks pass, protects a number a kept row holds anywhere as `#N` or an open milestone's `Resolves:` slot holds, and closes nothing after a failed or capped open-PR read; paths traced: each new case ends at "left alone", and the post-push close still runs only on numbers the option named. The simple-english lint hook flags 200 pre-existing style hits in the file; only the new sentences were kept short, the rest left alone as out of scope.
- 2026-10-20: T2 done: `test_trivial_route_closes_deleted_rows_issues` drops the two title-reference phrases and pins 10 phrases, each its own member; against main's step 1 all 10 are absent and the test fails on its own assertion (`AssertionError` in that test, not a crash), against the branch all 10 are present; full `skills/tests` green.
