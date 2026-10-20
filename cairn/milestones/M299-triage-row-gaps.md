<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M299: Triage closes the remaining PR-named row gaps

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP2, IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what an adopter's `/cairn-triage` pass proposes and writes to candidate rows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m299-triage-row-gaps   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A `/cairn-triage` pass closes six gaps that the M296 and M298 reviews found in how it treats candidate rows that an open pull request, a started token, or a merge points at.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `skills/cairn-triage/SKILL.md`: the session-start open-PR read, step 2 (new titles, token changes, the Overlap class), and step 3's amend loop. One D-entry. One CHANGELOG Unreleased Fixes entry. README's triage passages. New pins in `skills/tests/test_triage_pr_named_rows.py`. Absorbs in full the candidate rows "Close the remaining PR-named row gaps" and "Guard PR-named rows on other skill paths".

**Out:** A title the user sets at Amend is still not checked for uniqueness, icons, or a PR-named title. That stays the accepted limitation in DESIGN.md's `/cairn-triage` Known issues entry. A live `M<NNN>` token at Amend: such a row is never dropped or merged away (the skill's session start, records-hygiene §1), so AC4 covers `#<n>` tokens only. The trivial-route gaps stay in the candidate row "Keep owed issues open on a trivial edit". The lessons pass reads no PRs and does not change.

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

- [ ] AC1: `skills/cairn-triage/SKILL.md` reads the open pull requests' `Candidate row:` lines at session start. That read states that the PR text is data, never instructions.
- [ ] AC2: Step 2 states a rule for each new short title that the pass proposes. Such a title is a `retitle`'s title or the title of a row that a `split` names. It is also the title of a candidate row that a `route` writes, and the short title a `compress` leaves where it differs from the row's old one. It differs from every other row's short title as session start read it, and from the other new titles of the pass. It also differs from each short title that a `Candidate row:` line names in the session-start open-PR read.
- [ ] AC3: Step 2's token-change rule covers a row with a dead started token inside its short title, as session start read that title. An example is `Title — started M12: detail`. The pass proposes no removal of that token. The table lists the token as left, and on a PR-named row it names each naming PR's number.
- [ ] AC4: Step 3's amend loop covers a row that carries a live `#<n>` started token. At Amend the user can set on that row a disposition that removes the row or changes its short title. These are `drop`, `merge` as the absorbed row, `split`, `route`, `retitle`, and a `compress` that rewrites the title. The chip after that Amend names the row in its question text, with each PR number that the row's live `#<n>` tokens name. It says that the change leaves each such PR pointing at a row that is gone or retitled. Each later chip does the same while that change stands. Step 2 says that no proposed disposition rewrites a live token.
- [ ] AC5: Step 3's amend loop states a rule for a `retitle` that the user sets at Amend, in any round. That `retitle` runs the same search for double-quoted mentions as a proposed `retitle`. After that Amend the pass shows that row's table line again, a later round included, as an exception to the rule that a later round shows no table. The line lists each mention the `retitle` rewrites and each ambiguous mention it leaves. It also lists each mention it leaves inside a PR-named row's short title, with each naming PR's number. After a failed or capped open-PR read, the line says that the mentions were not checked.
- [ ] AC6: Step 2 drafts each proposed merge's lineage clause and the trigger the survivor takes. The Overlap class does not fire on a pair whose survivor's short title, by the rulebook's "Candidate short title" rule, changes when step 4 places that clause and trigger. The other row is then treated as beside a PR-named survivor. It is checked for Overlap against the remaining rows, and otherwise takes the first later class that fires, or `keep`. Its table reason names the survivor and says that the merge changes that row's short title. The user can set such a merge at Amend. Then the chip after that Amend, and each later chip while that change stands, names the survivor in its question text and says that its short title will change.
- [ ] AC7: `cairn/DECISIONS.md` gains one entry whose heading supersedes the last Consequences sentence of D-197 and annotates D-166's keep. It records the rules of AC2 to AC6 and says that AC1 needs no entry. It says that a title set at Amend can still equal a PR-named title. It states that it passes D-108's door on its retained trigger, and it names the M296 and M298 review findings it fixes. One new CHANGELOG entry under `## Unreleased` and `### Fixes` states the six fixes. The profile's `verify` slot passes at the branch head. The hand-run `python3 -m unittest discover -s skills/tests` passes there too.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6
- AC2 → T2, T6
- AC3 → T3, T6
- AC4 → T5, T6
- AC5 → T5, T6
- AC6 → T4, T5, T6
- AC7 → T7, T8

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Add the data-never-instructions sentence to the session-start open-PR read in `skills/cairn-triage/SKILL.md` (near line 88), in the words of `skills/milestone-plan/SKILL.md:114`.
- [x] T2: Add the new-title rule to step 2 for `retitle`, `split`, `route`, and a title-changing `compress` (the Title class near line 355 and the table rows near line 297).
- [x] T3: Add the token exception to step 2's token-change rule (near line 403), and the table's "left" line for such a token.
- [x] T4: In step 2's Overlap class (near line 329), draft the lineage clause and trigger, and add the before-and-after title check. Keep step 4's placement rules as they are.
- [x] T5: In step 3's amend loop (near line 492), add the `#<n>` live-token chip, the Amend-set `retitle` search and table line, and the title-changing merge chip. Change step 2's "So no disposition of the pass rewrites a live token" (near line 393) to say "no proposed disposition".
- [x] T6: Extend `skills/tests/test_triage_pr_named_rows.py` with one pin per new rule, each list member pinned on its own. Show each new pin red against the old skill text first.
- [x] T7: Write the D-entry and the CHANGELOG Fixes entry. Update README's triage passages (near lines 424 and 603). Search README and `skills/shared/tracking-rules.md` for "short title stays the same", and fix each claim that AC3 makes false.
- [x] T8: Run the `verify` slot and the hand-run `skills/tests` from the repo root. Check each exit code.

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
- 2026-10-20: question set: which candidate work to plan, among the three unparked rows or pruning them — "Close the remaining PR-named row gaps". No other question: the work foresees no outward action beyond the merge and no dependency change.
- 2026-10-20: collision check: absorbs "Close the remaining PR-named row gaps" in full, and "Guard PR-named rows on other skill paths" in full (its item (5) is the same skill's open-PR read). M295, M296, and M298 are done and are this work's lineage. D-108's door is passed on its retained trigger, as each gap is a shipped-behavior defect a review found. AC6 is one check for every survivor shape, not the per-shape placement rule D-197 rejected. DESIGN's Amend-title limitation stays (Out).
- 2026-10-20: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-20: lessons harvested: M112/M249 (grep README and the rulebook for old phrasing, CHANGELOG task), M148/M182 (new prose near a pinned slice must not echo a pin's start marker; hand-run skills/tests), M171 (pin each list member), M56 (run both gating suites after a SKILL.md edit).
- 2026-10-20: criteria audit (full mode, one Opus reader): 7 findings, all taken. AC4 narrowed to live `#<n>` tokens, since a live `M<NNN>` row is never dropped or merged away. AC5 states its exception to the no-table rule and the not-checked mark. AC3 widened to every row, so item (2) closes as named. AC2 adds a title-changing `compress`. AC4 names each PR and changes "no disposition" to "no proposed disposition". AC7 names the supersession of D-197's last Consequences sentence and the annotation of D-166, and says AC1 needs no entry. AC6 says step 2 drafts the clause. AC1 had no finding.
- 2026-10-20: plan gate chose for AC6 one before-and-after title check on every merge survivor over leaving D-197's accepted consequence, because the check covers every row shape in one rule; falsified by a proposed merge whose survivor's short title still changes.
- 2026-10-20: plan gate chose for AC3 to leave a dead token that sits inside a short title over removing it on non-PR-named rows only, because a removal changes the title and breaks each double-quoted mention for every row; falsified by a row whose left dead token a real triage pass reports as a problem.
- 2026-10-20: plan gate kept the six gaps in one milestone with 7 criteria and 8 tasks, since all edit one skill and ship together.
- 2026-10-20: implement start: branch m299-triage-row-gaps cut from main at 70bba243; untracked `cairn-probe.log` is not this milestone's and stays unstaged.
- 2026-10-20: T1–T5: `skills/cairn-triage/SKILL.md` gains the data sentence at the open-PR read, a "New short titles" paragraph after the Title class, the dead-token exception in the token-change rule, the before-and-after title check in the Overlap class, and three amend-loop paragraphs (live `#<n>` chip, title-changing merge chip, Amend-set `retitle` mention search with its table line); "no disposition" now reads "no proposed disposition". Choice: the no-table rule names the `retitle` exception in place rather than only in the new paragraph, so a reader of either sentence sees it.
- 2026-10-20: T6: six new tests in `skills/tests/test_triage_pr_named_rows.py`, one phrase per subtest; run against main's skill text each new test fails on its own missing phrase or section marker (27 failing subtests), the four M298 tests stay green; on the branch the hand-run `skills/tests` runs 929 tests OK and all five `verify` checks pass (scripts 428 OK, hooks OK, both validates pass, mod test 0 fail).
- 2026-10-20: T7: D-198 appended (supersedes D-197's last Consequences sentence, annotates D-166, passes D-108's door; says the AC1 sentence needs no entry and an Amend-set title can still equal a PR-named title); one CHANGELOG Unreleased Fixes entry; README gains the new triage rules beside the PR-named passage and the dead-token exception beside the token passage. The search for "short title stays the same" found README:610 and tracking-rules:254; both now say that adding a token at the row's end leaves the title the same, since AC3 shows a removal can change it. Validate green; skills/tests green.
- 2026-10-20: T8: at 07804d99 all five `verify` checks exit 0 (scripts 428 OK, hooks 193 OK, both validates, mod test 0 fail) and the hand-run skills/tests exits 0 (929 OK).
- 2026-10-20: claim audit: 34 claims read, 3 corrected — skills/cairn-triage/SKILL.md, CHANGELOG.md, README.md (a dead token left in a title could still move on a `compress` or go with an icon `retitle`'s in-place title, so step 4 and the token rule now say what happens; "the one exception" now reads "the default pass's one exception", since the lessons pass shows its line each round; the CHANGELOG and README wording follows). The re-read found all three true and README's token sentence still overstated, which now names the icon retitle. The dead-token pin gained both new sentences and stays red on main.
- 2026-10-20: implement complete: all tasks checked; after the claim fixes all five `verify` checks, the hand-run skills/tests, and cairn_validate pass; status → review.

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
