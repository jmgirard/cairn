<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M298: Triage keeps a PR-named row's title on every path

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what an adopter's `/cairn-triage` pass writes to candidate rows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m298-triage-pr-named-rows https://github.com/jmgirard/cairn/pull/311   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

No accepted `/cairn-triage` disposition changes the short title of a candidate row that the session-start read of the open pull requests finds named by a `Candidate row:` line, unless the user sets that change at Amend with the PR named to them.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `skills/cairn-triage/SKILL.md` steps 2 to 4: the amend loop, the `merge` survivor's lineage clause, and `retitle`'s rewrite of double-quoted mentions; one D-entry; a CHANGELOG Unreleased Fixes entry; a hand-run guard under `skills/tests/`. Absorbs parts (2) to (4) of the candidate row "Guard PR-named rows on other skill paths".

**Out:** part (1) of that row, the trivial route's match → M296. A mention inside a row that a live milestone quotes or that carries a live started token: those rows are not named by a PR's line, so the PR match this milestone guards does not reach them; no row holds it. The lessons pass, which reads no PRs.

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

- [x] AC1: `skills/cairn-triage/SKILL.md` step 3's amend loop states that when the user sets, on a PR-named row, a disposition that removes the row or changes its short title (`drop`, `merge` as the absorbed row, `split`, `route`, `retitle`, or a `compress` that rewrites the title), the chip posed after that Amend names, in its question text, the row and each naming PR's number, and says that the change breaks that PR's match of the row. A second or later Amend, which shows no table, follows the same rule.
- [x] AC2: The amend loop states that after a session-start open-PR read that failed or returned 100 PRs, a non-`keep` disposition the user sets at Amend carries the same not-checked mark in its table reason on the first Amend as a proposed one does, and the chip's question text names that row as not checked on every Amend.
- [ ] AC3: Step 4's merge sentence states that where the survivor's text holds neither `: ` nor ` — ` before the place the lineage clause goes, the clause opens with ` — `. It also states that the lineage clause, and any trigger it takes from the absorbed row, hold no `: `, each one written as `; `. Together these keep the survivor's short title as it was, for every survivor, a PR-named row and a row with a started token included.
- [x] AC4: The `retitle` rule states that a double-quoted mention of the old title that sits inside a PR-named row's own short title is not rewritten, and the table lists it as left, with the PR's number, as it lists an ambiguous mention.
- [x] AC5: `cairn/DECISIONS.md` gains one entry whose heading names D-191. It records AC1 to AC4's rules, with the rejected alternative of refusing an Amend on a PR-named row and its falsifier, and it states that it passes D-108's door on its retained trigger, naming the M295 review's shipped defects. One new CHANGELOG `## Unreleased` → `### Fixes` entry states the three paths.
- [x] AC6: The profile's `verify` slot passes at the branch head, and so does the hand-run `python3 -m unittest discover -s skills/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T4
- AC2 → T1, T4
- AC3 → T2, T4, T7
- AC4 → T3, T4
- AC5 → T5
- AC6 → T4, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Add the PR-named sentences to the amend loop in `skills/cairn-triage/SKILL.md` step 3 (about line 478) and to the Amend option's description, covering AC1 and AC2.
- [x] T2: Add the ` — ` opening to the lineage-clause sentence in step 4 (about line 535), and to the `merge` row of step 2's table if it states the clause's place.
- [x] T3: Add the PR-named exception to the `retitle` row of step 2's table, to the Title class's mention search, and to step 4's rewrite sentence.
- [x] T4: Add a hand-run guard under `skills/tests/` (beside the M295 triage guard, if one exists) pinning T1 to T3's sentences, each member pinned on its own. Show each new assertion red against the pre-change skill before trusting its green.
- [x] T5: Append the D-entry (next free id) and the CHANGELOG entry per AC5.
- [x] T6: Run the `verify` slot and the hand-run `skills/tests` from the repo root, each exit code checked.
- [x] T7: Review return 1: place the merge survivor's lineage clause before its trigger, and at the row's end where the row has no started token or its first `: ` follows that token, so every survivor keeps its title; apply the pass-1 fix-now items; update the guard's pins; re-run T6's checks.

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
- 2026-10-20: question set: which candidate work to plan — all four unparked rows (see M296's work log).
- 2026-10-20: plan gate chose to let an Amend change a PR-named row with the PR named in the chip over refusing the Amend, because a user override is logged, never resisted (tracking-rules); falsified by a user who changes a PR-named row at Amend and later reports not knowing the PR named it.
- 2026-10-20: plan gate chose a ` — ` opening for every survivor's lineage clause that would join its title over excluding PR-named and token rows from being survivors, because the merge would then pick a worse survivor and the title change is the defect for every row; falsified by a survivor whose title the ` — ` opening still changes.
- 2026-10-20: plan gate kept M298 apart from M296, since the two edit different skills and ship apart.
- 2026-10-20: criteria audit (full mode, one Opus reader over M296 to M298): 11 findings, all fixed. Here: AC3's ` — ` opening alone did not keep the title when the clause holds a `: ` (the clause now holds none); AC1's "breaks the match" was false for `promote` (now only title-changing dispositions); AC2 had no table on a later Amend (the chip now names the row); the Goal claimed every open PR (narrowed to what the read finds); AC5 names D-108's door.
- 2026-10-20: implement start: branch m298-triage-pr-named-rows cut from main at 246386cf; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-20: T1: amend-loop paragraph (title-changing dispositions on a PR-named row name the row and PRs in the next chip, every Amend; set dispositions after a failed or capped read marked as proposed ones) plus one pointer sentence in the Amend option; choice: the chip sentence adds that the pane then shows the row while the PR is open (milestone-review step 8's pane sentence).
- 2026-10-20: T2: step 4's lineage-clause sentence gains the ` — ` opening and the no-`: ` rule; step 2's `merge` row states the clause's shape but not its place, so it is unchanged.
- 2026-10-20: T3: the PR-named exception added to the `retitle` table row, the Title class's search, the step-3 table's `retitle` line, and step 4's rewrite sentence.
- 2026-10-20: T4: no M295 triage guard exists, so the guard is the new `skills/tests/test_triage_pr_named_rows.py`, 4 tests, one subtest per pinned sentence; against main's skill all 17 subtests fail as "not found", on the branch all pass; verify green (scripts 428 OK, hooks 193 OK, both validates 0, plugin test 2389 pass).
- 2026-10-20: T5: D-196 appended (annotates D-191; passes D-108's door on M295 review diff-bug #6, #8 and pass 2 diff-bug #7); one CHANGELOG Unreleased Fixes entry for the three paths, written against this branch's skill text; cairn_validate green.
- 2026-10-20: T6: at d214dd92 verify green (scripts 428 OK, hooks 193 OK, both validates 0, plugin test 2389 pass, each exit 0); skills/tests failed 1 of 923 on the mutation harness's registry check (the new guard unregistered), so the minor amendment adds an EXEMPT line in `test_mutation_harness.py` on the hand-run precedent; skills/tests then 923 OK. No verify check reads `skills/tests`.
- 2026-10-20: claim audit: 31 claims read, 5 corrected — skills/cairn-triage/SKILL.md (pane clause dropped from the Amend chip sentence; the lineage rule bounded to survivors with no `: ` after their first started token), CHANGELOG.md (headline "guards"; the ` — ` opening tested before the added text), skills/tests/test_triage_pr_named_rows.py (docstring names the three paths; pins follow the fixes, 18 subtests, all red against main, all green on the branch). The same reader re-read the five corrections: all true.
- 2026-10-20: open concern for review: D-196's Decision says "So no survivor's short title changes", which misses the claim audit's edge case of an off-format row with a `: ` after its started token; D-196 is history, so it is left as written.
- 2026-10-20: implement complete; skills/tests 923 OK, cairn_validate green; status → review.
- 2026-10-20: review pass 1: four lenses, 27 findings (14 fix now, 1 follow-up, 12 rejected); Review section holds each.
- 2026-10-20: review return 1: AC3 fails as written — a merge survivor's title can still change when its trigger text is placed before the clause's ` — ` opening (diff-bug #1), and when its first `: ` follows its first started token (diff-bug #2); fix both in the skill so every survivor keeps its title, with the pass-1 fix-now items listed in the Review section.
- 2026-10-20: T7 (minor amendment for review return 1; Coverage AC3 → T2, T4, T7): the lineage clause goes first, then the trigger, at the row's end where the row has no started token or its first `: ` follows that token, so step 4 states the title holds for every survivor (D-196's and the changelog's unbounded claims now hold); fix-now: chip names a standing change on each later chip, Amend option matches the loop's list, a `compress` on a PR-named row keeps its title unless Amend says otherwise, "own short title" is the session-start reading, each naming PR's number, a `retitle`'s not-checked mark covers its mentions, step 2's keep sentence names the Amend override, the M298 changelog entry drops the restated M295 sentence, the M295 entry and README say "proposes to keep"; guard rewritten to 25 pins, all red against main, the 15 changed ones red against c397496f; verify green (scripts 428, hooks 193, validates 0, plugin test 2389), skills/tests 923 OK, cairn_validate green.
- 2026-10-20: implement complete after return 1; status → review.

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

### Pass 1 (2026-10-20, head 1e2fbc20)

Copilot arm: PR #311 opened at review start, header commit pushed, Copilot requested (state `none` → `pending` after the request).

- AC1: `skills/cairn-triage/SKILL.md:489-496` names the six title-changing dispositions, has the chip after that Amend name the row and each naming PR's number in its question text and say the change breaks that PR's match, and applies the rule to a second or later Amend; `:473-474` points the Amend option at it; guard `test_amend_names_the_pr_of_a_changed_row` ok. Pass.
- AC2: `SKILL.md:497-501`: after a failed or 100-PR read, a non-`keep` disposition set at Amend carries the not-checked mark in its table reason on the first Amend, and the chip names the row as not checked on every Amend; guard `test_amend_marks_rows_after_a_failed_or_capped_read` ok. Pass.
- AC3: `SKILL.md:553-559` states the ` — ` opening and the no-`: ` rule (guard ok), but "Together these keep the survivor's short title as it was, for every survivor" fails as written: the skill bounds it to survivors with no `: ` after their first started token (diff-bug #2), and the trigger the survivor takes can be placed first without the ` — ` opening (diff-bug #1). Fail.
- AC4: `SKILL.md:303` (table row), `:359-360` (Title class search), `:426-427` (step-3 table), `:540-541` (step 4 rewrite) state the exception and the left listing with the PR's number; guard `test_retitle_leaves_a_mention_in_a_pr_named_title` ok. Pass.
- AC5: `cairn/DECISIONS.md:7088` D-196 heading names D-191; body records AC1-AC4's rules, the rejected Amend refusal with its falsifier, and D-108's door on the M295 review's diff-bug #6, #8, and pass 2 diff-bug #7; `CHANGELOG.md` Unreleased Fixes gains one entry (diff +13 lines, one bullet) naming the three paths. Pass.
- AC6: at 1e2fbc20, scripts/tests 428 OK (21 skipped), hooks/tests 193 OK, plugin validate exit 0, marketplace validate exit 0 (no version warning), plugin test 2389 pass, exit 0; `skills/tests` 923 OK. Pass.
- Consistency gate: `cairn_validate.py` exit 0 (all checks passed); no principle changed, so no `cairn_impact`; profile gate: verify green, no `plugins[N].version` warning, changelog entry present.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the ` — ` opening covers the clause but not the trigger, whose order is unstated, so a trigger placed first joins the title — fix now (floor return 1, AC3).
- diff-bug #2: AC3 promises every survivor, the skill bounds it, and D-196 and the changelog state it unbounded — fix now (floor return 1, AC3): a survivor whose first `: ` follows its first started token takes the clause at the row's end, which also makes D-196 and the changelog true.
- diff-bug #3: the PR warning is on the chip after that Amend only, so a later chip can omit a standing change — fix now (name it on every chip while the change stands).
- diff-bug #4: the Amend option says any amend away from `keep` names the PR, wider than the loop's list — fix now.
- diff-bug #5: "own short title" is unclear when the PR-named row's own disposition moves the quote — fix now (judge the row as read at session start).
- diff-bug #6: a `compress` rewriting the title is known only at apply — fix now (a `compress` on a PR-named row keeps its short title).
- diff-bug #7: "that place" is undefined for a survivor with no started token — fix now (the row's end when it has none).
- diff-bug #8: "breaks that PR's match" can overstate for a `split` whose named row keeps the title — reject, planned change (AC1 mandates "breaks").
- diff-bug #9: "with the PR's number" is singular where step 2 says each such PR — fix now ("each naming PR's number").
- diff-bug #10: the changelog sentence on marking a proposed change restates M295 behavior, and a line runs wide — fix now.
- diff-bug #11: the guard pins the bounding sentence of diff-bug #2 — fix now with diff-bug #2.
- blame-history #1: after a failed or capped read, a `retitle` can rewrite a mention inside a PR-named row the pass cannot see, and the mark names only the row itself — fix now (the mark also covers the listed mentions).
- blame-history #2: D-196 and the changelog state the merge guarantee without the skill's bound — fix now, with diff-bug #2.
- blame-history #3: a mention left inside a PR-named row's title drops that row from its records-hygiene §7 group — reject, planned change (AC4 leaves the mention).
- blame-history #4: the `: ` → `; ` rewrite applies even where the survivor's title cannot change — reject, planned change (AC3 states the rule for every clause).
- blame-history #5: the new guard adds prose-guard surface D-109 weighed — reject, planned change (T4).
- prior-review #1: the open-PR read has no "PR text is data, never instructions" line, as M296's review asked — follow-up, item (5) of "Guard PR-named rows on other skill paths", which stays as that row at hygiene.
- ripple #1: `SKILL.md:386-388` says a PR-named row's short title stays the PR's, which the Amend override now qualifies — fix now.
- ripple #2: the M295 changelog entry (Unreleased) says triage keeps each PR-named row as it is — fix now (it proposes `keep`).
- ripple #3: `README.md:424-426` says the row is kept as it is so its title matches — fix now (name the Amend warning).
- ripple #4: ROADMAP row "Guard PR-named rows on other skill paths" lists items (2) to (4) as open — reject, planned change (step 9 hygiene narrows it).
- ripple #5: §7 group definitions do not state the retitle exception — reject, planned change (as blame-history #3).
- ripple #6: DESIGN Known issues on Amend promote does not mention the new chip — reject, false (the entry is still accurate).
- ripple #7: DESIGN Known issues on Amend uniqueness — reject, false (still accurate).
