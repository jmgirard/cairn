<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M296: The trivial route matches a pressed title, not PR rows

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes which candidate rows an adopter's trivial-tier commit deletes or narrows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m296-trivial-route-row-match   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The trivial route's candidate-row match takes the row whose short title a ✎ press sends as the whole request, and it takes no row that its read of the open pull requests finds named by a `Candidate row:` line.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-plan` step 1's "Candidate-row match (trivial route)" paragraph and the trivial option's description; one D-entry; README's trivial-edit row, a CHANGELOG Unreleased Fixes entry, and the hand-run guard in `skills/tests/test_plan_tier_check.py`. Absorbs the candidate row "Match bare titles on the trivial route" in full and part (1) of the candidate row "Guard PR-named rows on other skill paths".

**Out:** closing the GitHub issue that a deleted row names → M297 (candidate row "Close the issue a trivial edit fixes"). Parts (2) to (4) of "Guard PR-named rows on other skill paths", the `/cairn-triage` paths → M298. A title that appears unquoted inside a longer request stays unmatched, at the user's choice in the question set; no row holds it. The rulebook's "Candidate short title" section keeps its wording: the match rule lives in the skill, as D-191's rejection of a rulebook sentence decided.

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

- [ ] AC1: `skills/milestone-plan/SKILL.md` step 1's candidate-row match states that a row matches when the request quotes its short title, and also when the request text with outer spaces removed equals the short title, which is what a ✎ press sends. The paragraph states that a short title that appears unquoted inside a longer request does not match. The live-milestone exclusion and the started-token exclusion keep their current wording.
- [ ] AC2: The same paragraph states that, before the chip, the plan reads the open pull requests' `Candidate row:` lines with the call and the parse that `/cairn-triage` session start names, citing that section rather than restating the parse. It states that a row such a line names is not matched, and that the trivial option's description names each row the request would otherwise match that such a line names, with each naming PR's number. It states that when the read fails, or returns 100 PRs, the match goes on, and when at least one row matched, the description says the matched rows were not checked against every open pull request.
- [ ] AC3: `cairn/DECISIONS.md` gains one entry whose heading names D-170 and D-191. It supersedes the reason in D-170's Rejected section, "because a pane press sends the quoted title", and keeps that rejection of matching by the "describes the bug" judgment. It annotates D-191's Consequences sentence that the match still asks for a quoted title. It records AC1's and AC2's rules with a rejected alternative and its falsifier, and it states that it passes D-108's door on its retained trigger, naming the shipped defect.
- [ ] AC4: README's trivial-edit row and one new CHANGELOG `## Unreleased` → `### Fixes` entry state the match of a pressed title and the skip of a row that an open PR names. `git grep -n -e "request quotes" -e "your request quotes" -- . ':!cairn/milestones' ':!cairn/ROADMAP.md' ':!cairn/DECISIONS.md' ':!cairn/legacy' ':!cairn/reviews'`, run at the branch head, lists no line outside a released CHANGELOG section that states the quoted title as the only way a row matches.
- [ ] AC5: The profile's `verify` slot passes at the branch head, and so does the hand-run `python3 -m unittest discover -s skills/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5
- AC5 → T3, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Widen the match sentence in `skills/milestone-plan/SKILL.md` step 1 (the "Candidate-row match (trivial route)" paragraph, about line 99) to the whole-request case, and add the unquoted-mention sentence.
- [x] T2: Add the open-PR read to the same paragraph, citing `skills/cairn-triage/SKILL.md` session start (about line 88), with the PR-named exclusion, the description's naming, and the failed or 100-PR case. Add the PR-named rows to the trivial option's description sentence.
- [x] T3: Update `skills/tests/test_plan_tier_check.py`'s `test_trivial_route_graduates_matched_rows` to pin T1's and T2's sentences, each member of a list pinned on its own (LESSONS M171). Show each new assertion red against the pre-change step 1 before trusting its green.
- [x] T4: Append the D-entry (next free id) per AC3.
- [x] T5: Edit README's trivial-edit row (about line 734) and add the CHANGELOG Fixes entry; run AC4's grep and fix any line it lists.
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
- 2026-10-20: question set: which candidate work to plan — all four unparked rows; a ripple-lens follow-up chosen "leave it as it is" (D-192).
- 2026-10-20: question set: when an unquoted title matches — only when the whole request, trimmed, is the title.
- 2026-10-20: plan gate split the three trivial-route rows into M296 (which rows match) and M297 (closing the issue), since both edit one paragraph and M297's goal is its own; M297 depends on M296.
- 2026-10-20: plan gate chose to keep matching on a failed or capped open-PR read, with the description saying so, over matching no row, because a failed `gh` read would then stop every trivial edit from graduating its row (the same choice D-191 made for triage); falsified by a trivial edit that deletes a row an open PR names after a failed read.
- 2026-10-20: plan gate chose to cite triage's read and parse over restating them, because one parse in two places drifts; falsified by a skill reading that needs a parse the triage section does not give.
- 2026-10-20: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-20: criteria audit (full mode, one Opus reader over M296 to M298): 11 findings, all fixed. Here: AC4's grep left the absorbed ROADMAP row in its domain (pathspec now excludes `cairn/ROADMAP.md`); the Goal claimed every open PR, past a read capped at 100 (narrowed to what the read finds); AC2's "each such row" and the not-checked note made definite; AC3 now supersedes only D-170's reason, annotates D-191's Consequences, and names D-108's door.
- 2026-10-20: status in-progress; branch m296-trivial-route-row-match cut from origin/main at dd99e0ba; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-20: T1, T2: step 1's match takes a trimmed whole-request title and skips a PR-named row, citing triage's read and parse; the option description names skipped rows and the not-checked case. The simple-english lint hook counts the whole file (196 hits before the edit); the new sentences were rewritten until the file count fell to 195, and the file's older hits are left alone, outside this scope.
- 2026-10-20: T3: `test_trivial_route_matches_pressed_title_not_pr_rows` pins 12 new phrases and their place in the match paragraph; red against main's step 1 on the first phrase, and a scratch check found none of the 12 in main's text; green after.
- 2026-10-20: verify after T1-T3: scripts/tests, hooks/tests (193), both plugin validates, plugin test (2389 pass), and hand-run skills/tests (918) all exit 0.
- 2026-10-20: T4: D-193 appended (supersedes D-170's Rejected reason, keeps its rejection; annotates D-191's Consequences; D-108's door passed on the two shipped defects).
- 2026-10-20: T5: README trivial-edit row and a CHANGELOG Unreleased Fixes entry; lint counts on both files equal main's after two sentences were split. AC4's grep lists CHANGELOG.md:169 (the new entry, stating the old behavior in the past), :402 and :746 (released sections), the widened SKILL.md:102 sentence, and test_plan_tier_check.py:159 (the kept pin of the quote sentence); none states the quote as the only match.

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
