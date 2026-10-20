<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M298: Triage keeps a PR-named row's title on every path

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what an adopter's `/cairn-triage` pass writes to candidate rows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m298-triage-pr-named-rows   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: `skills/cairn-triage/SKILL.md` step 3's amend loop states that when the user sets, on a PR-named row, a disposition that removes the row or changes its short title (`drop`, `merge` as the absorbed row, `split`, `route`, `retitle`, or a `compress` that rewrites the title), the chip posed after that Amend names, in its question text, the row and each naming PR's number, and says that the change breaks that PR's match of the row. A second or later Amend, which shows no table, follows the same rule.
- [ ] AC2: The amend loop states that after a session-start open-PR read that failed or returned 100 PRs, a non-`keep` disposition the user sets at Amend carries the same not-checked mark in its table reason on the first Amend as a proposed one does, and the chip's question text names that row as not checked on every Amend.
- [ ] AC3: Step 4's merge sentence states that where the survivor's text holds neither `: ` nor ` — ` before the place the lineage clause goes, the clause opens with ` — `. It also states that the lineage clause, and any trigger it takes from the absorbed row, hold no `: `, each one written as `; `. Together these keep the survivor's short title as it was, for every survivor, a PR-named row and a row with a started token included.
- [ ] AC4: The `retitle` rule states that a double-quoted mention of the old title that sits inside a PR-named row's own short title is not rewritten, and the table lists it as left, with the PR's number, as it lists an ambiguous mention.
- [ ] AC5: `cairn/DECISIONS.md` gains one entry whose heading names D-191. It records AC1 to AC4's rules, with the rejected alternative of refusing an Amend on a PR-named row and its falsifier, and it states that it passes D-108's door on its retained trigger, naming the M295 review's shipped defects. One new CHANGELOG `## Unreleased` → `### Fixes` entry states the three paths.
- [ ] AC6: The profile's `verify` slot passes at the branch head, and so does the hand-run `python3 -m unittest discover -s skills/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T4
- AC2 → T1, T4
- AC3 → T2, T4
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
- [ ] T5: Append the D-entry (next free id) and the CHANGELOG entry per AC5.
- [ ] T6: Run the `verify` slot and the hand-run `skills/tests` from the repo root, each exit code checked.

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
