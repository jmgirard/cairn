# M193: A styled milestone band that follows the phase

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m193-styled-band

## Goal

Redraw the milestone band so that each active milestone shows a styled header row and the next open item of its phase. That item is a task during implement and an acceptance criterion during review.

## Scope

**In:**
- Two rows per active milestone in `hooks/status/`: a header row (phase label, id, title, progress bar, counts) and an item row (the next unchecked task or criterion). Colors are theme keys, so they follow the person's light or dark theme.
- The reader's new fields (criterion counts, the first unchecked line of each section), the `cairn.band` state contract in `types/index.d.ts`, and their fixtures.
- Cairn's rows drawn above what the hooks beneath return from `next(e)`. This absorbs one item of the "Status mod follow-ons" candidate row. The row stays until post-merge hygiene narrows it.
- README "The milestone band" section, the DESIGN.md `hooks/status/` line, and a CHANGELOG entry.

**Out:**
- A dim idle line naming the next planned milestone → new candidate row "Band idle line".
- A full checklist of the phase's items, or a button that expands one → not planned. The gate chose the two-row layout.
- A roadmap pane, clickable next-command actions, `vscode` and `mobile` tests, and the Windows UNC walk → the "Status mod follow-ons" candidate row.

## Acceptance criteria

- [x] AC1: Take each `in-progress` or `review` row whose milestone path is a readable regular file and whose phase section holds an unchecked checkbox. For each such row, the band draws two rows, in ROADMAP order. The phase section is what `_section_body` returns for `Tasks` on an `in-progress` row and for `Acceptance criteria` on a `review` row. The header row names the id, the title, the phase (`implement` or `review`), a progress bar (at `bodyColumns` 60 or more, AC3), and `<checked>/<total> tasks` or `<checked>/<total> criteria`. The counts are over the phase section's lines that `_AC_ITEM` matches. The item row shows the first such line whose box is `[ ]`, less the prefix that `^\s*-\s*\[ \]\s*` matches. Shown by `claude plugin test` cases on the terminal and desktop surfaces over three fixtures: `single-in-progress`, `mixed`, and a fixture whose first unchecked task is nested. The `review` row M010 in `mixed` has 3/5 tasks and 2/3 criteria.
- [x] AC2: Three states draw the header row alone, with no bar and no item row. The first is a row whose milestone path is not a readable regular file (`no milestone file`). The second is a phase section with no checkboxes, or no such section (`no tasks` or `no criteria`). The third is a phase section whose checkboxes are all checked (`all <N> tasks checked` or `all <N> criteria checked`). Shown by `claude plugin test` cases over fixtures that hold four cases in each phase. The cases are a path that is not a readable regular file, no phase section, a phase section with no checkboxes, and an all-checked phase section.
- [x] AC3: The Text elements inside the `cairn-band` Box carry style props. The phase label's color differs between `implement` and `review`. The id is bold. The bar's filled cells carry a color. `no milestone file` carries a color. The item row is dim. In the drawings of the AC1 and AC2 cases, every Text inside the `cairn-band` Box carries `wrap="truncate-end"`. When `bodyColumns` is below 60, the header row omits the bar and keeps the counts. At 60 or more, it shows the bar. Shown by `claude plugin test` cases that read the drawn elements' props from `findAll`. The cases mount `mixed`, which holds both phases and a missing file, at `bodyColumns` 59, 60, and 120.
- [x] AC4: The band follows edits at the next turn end. M191's five edit cases stay, with their expected rows restated in the new layout. In addition, a check on the item row's task grows the bar's filled cells and shows the next unchecked task. A row that moves from `in-progress` to `review` switches both rows from tasks to criteria, over a fixture whose row holds an unchecked criterion. Shown by the edit cases in `hooks/status/band.test.tsx` on both surfaces.
- [x] AC5: The reader and the Python helpers agree on every fixture. For each active row, the reader's task and criterion counts, and the first unchecked line of each section, equal the values that `scripts/tests/test_status_fixtures.py` computes. A first unchecked line is null where the path is not a readable regular file or the section has no unchecked box. The Python side computes counts with `_section_body` and `_AC_ITEM`, and the first unchecked line by AC1's rule over the same `_section_body`. Shown by `hooks/status/reader.test.ts` and `test_status_fixtures.py` over each fixture's `expected.json`, both of which fail on any difference.
- [x] AC6: When the band has rows to draw, it draws them above the tree that the hooks beneath it return from `next(e)`, so another plugin's band beneath cairn's still shows. Shown by a `claude plugin test` case on both surfaces with a second plugin beneath cairn (tier `append`) that draws its own band row.
- [x] AC7: The verify slot in `cairn/PROFILE.md` runs clean: both Python suites, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T2, T3, T4
- AC2 → T1, T3, T4
- AC3 → T3, T4
- AC4 → T1, T5
- AC5 → T1, T2
- AC6 → T4
- AC7 → T2, T4, T5, T6

## Tasks

- [x] T1: Fixtures. Add `## Acceptance criteria` sections to the existing fixture files (one unchecked criterion in `single-in-progress` M002, task counts unchanged). Add fixtures for a nested first unchecked task and for each AC2 state in each phase. Extend each `expected.json` with criterion counts and the first unchecked line of each section, then regenerate `fixtures.gen.ts`.
- [x] T2: Reader. Add criterion counts and the first unchecked line per section to `reader.ts` and `BandRow`, and the same shape to `CairnBandRow` in `types/index.d.ts`. Hold `reader.test.ts` and `scripts/tests/test_status_fixtures.py` to the new `expected.json` fields, red first.
- [x] T3: Layout in `band.ts`. Build the header and item rows as element descriptions: phase label, bold id, a bar of filled and empty cells, counts, and the AC2 labels. Pick theme keys for the colors and drop the bar below 60 `bodyColumns`.
- [x] T4: Render in `register.tsx`. Draw the rows from T3, stacked above the tree from `next(e)`, and still yield to a survey. Rewrite the `band.test.tsx` cases for AC1–AC3 and AC6 on both surfaces, including a beneath-cairn plugin that draws its own row. That test plugin's `register` closes over nothing in the test file, so its row text is written inside it.
- [x] T5: Edit cases. Restate M191's five cases in the new layout, and add the check-a-task and the in-progress-to-review cases on both surfaces.
- [x] T6: Docs. Rewrite README "The milestone band" (its example rows taken from a test case's drawing), update the DESIGN.md `hooks/status/` line, and add a CHANGELOG `Unreleased` entry.
- [x] T7: Look at the band live in the desktop app at a normal and a narrow width, in implement and in review, and record what it showed in the work log.

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request to make the band less plain and to show criteria during review.
- 2026-10-01: criteria audit, full mode, one fresh Opus reader read twice. The draft drew 15 findings and the revised text drew 4. Seventeen had one clear fix and were fixed at the gate. Stacking above `next(e)` was posed as a gate question. The reader left AC2's fixture breadth open, and the plan took the wider form (four cases per phase).
- 2026-10-01: plan gate chose a header row plus the next open item over a full checklist and over a checklist behind an expand button, because two rows keep the band short and need no focus or hotkey handling. Falsified by sessions where the operator opens the milestone file to see the rest of the list.
- 2026-10-01: plan gate chose to stack cairn's rows above `next(e)` in this milestone over leaving it in the follow-ons row, because the render is rewritten here anyway. Falsified by an engine version that refuses a band tree holding another plugin's drawing.
- 2026-10-01: plan gate chose to keep the band empty between milestones over a dim next-milestone line, because that line needs a second reader of `cairn_next.py`'s logic. Falsified by a session between milestones that misses the next step because the band was empty.
- 2026-10-01: implement started on `m193-styled-band`. Question gate: the phase label is the theme's `claude` color for implement and `success` for review, the bar's filled cells take the phase color, and `no milestone file` takes `warning`. The bar is a fixed 10 cells. The item row opens with two spaces and an arrow.
- 2026-10-01: T1, T2: three new fixtures (`nested-first`, `states-implement`, `states-review`) and an open criterion in `single-in-progress`. Each `expected.json` row now carries task and criterion counts and `nextTask` and `nextCriterion`, written by hand. The reader and `CairnBandRow` carry the same fields. The old Python test failed on 7 fixtures before the change, and a planted wrong value failed it after. `band.ts` reads the renamed task fields until T3 rewrites it. Verify clean: scripts 394, hooks OK, validate passed with 1 warning, mod tests 37/37.
- 2026-10-01: T3, T4, T5: `band.ts` builds each row as styled spans, and `register.tsx` draws them in the `cairn-band` Box above the tree from `next(e)`. A narrow band cuts the title so the counts stay. The engine drops `key` from a Text, so each row's key sits on a Box. M191's in-progress-to-review edit case now asserts both rows switch to criteria, since `single-in-progress` holds an open criterion. Three planted defects turned tests red: no stacking, no `wrap` on spans, and the bar threshold at 59. Verify clean: scripts and hooks OK, validate passed with 1 warning, mod tests 47/47.
- 2026-10-01: T6: README "The milestone band" rewritten, its example rows copied from the `mixed` drawing in `band.test.tsx`. The DESIGN.md `hooks/status/` line names the two rows and the stacking. The band is still unreleased, so its CHANGELOG `Unreleased` entry was rewritten in place, not joined by a second entry. Verify clean, `cairn_validate` all checks passed.
- 2026-10-01: T7 checkpoint, half done: the operator saw implement at a normal width. Status is set to `review` for one turn only, so the band draws the review rows for the remaining screenshots. It goes back to `in-progress` after them.
- 2026-10-01: T7: the operator sent three desktop screenshots, and the status is back to `in-progress`. Implement, normal width: orange `implement`, bold id, 8 of 10 cells filled for 6/7 tasks, a dim item row with the arrow, cut with `…`. Review, normal width: green `review` padded to the width of `implement`, 10 empty cells, `0/7 criteria`, AC1 on the item row. Review, narrow: no bar, the title cut with `…`, the counts kept. Two observations, no defect: the desktop font draws `░` narrower than `█`, so the bar width changes with the count. The item row shows raw markdown, so backticks appear, as AC1 specifies.
- 2026-10-01: claim audit: 69 claims read, 8 corrected — hooks/status/band.ts, hooks/status/register.tsx, hooks/status/band.test.tsx, README.md, CHANGELOG.md. The corrections say the item row and the bar appear only when the section has an open box, and `lineText` serves the tests alone. The DESIGN.md line sits under `cairn/`, outside the audited diff. Verify clean: scripts 394, hooks 174, plugin validate with its known warning, mod tests 47/47.
- 2026-10-01: implement done. All tasks checked, verify clean, status set to `review`.
- 2026-10-01: step-7 approval: m193-styled-band approved for merge (fix R2 and R3 first, R4 to a candidate row).

## Decisions

## Review

- AC1: `claude plugin test` on terminal and desktop (`mountEach`), 2026-10-01: the three AC1 cases pass over `single-in-progress`, `mixed`, and `nested-first`. Each drawing equals the hand-written rows in ROADMAP order. `mixed` `expected.json` gives M010 3/5 tasks and 2/3 criteria, and its review header reads `2/3 criteria` with `AC3: Third criterion.` on the item row. PASS.
- AC2: `claude plugin test` on both surfaces: `states-implement` (M040–M043) and `states-review` (M050–M053) each hold the four cases (missing file, no section, section with no boxes, all checked). Each draws only `<id>-header` keys, no `█`/`░` text, and the labels `no milestone file`, `no tasks`/`no criteria`, `all 3 tasks checked`, and `all 2 criteria checked`. `missing-file` and `subdirectory` pass too. PASS.
- AC3: `claude plugin test`, `mixed` at 59, 60, and 120 columns on both surfaces: `implement` takes `claude` and `review` takes `success`, M010 is bold, the filled cells take `success`, `no milestone file` takes `warning`, and the item row Texts are `dimColor`. At 59 there is no bar and the header ends `2/3 criteria`. At 60 and 120 the bar is drawn. Review added the `wrap` assertion to the AC1 and AC2 cases (finding R1). A planted defect that dropped `wrap` from the span Text failed all 10 AC1–AC3 cases. With the assertion in place, all pass. PASS.
- AC4: `claude plugin test`: M191's five edit cases (a task gets checked, planned to in-progress, in-progress to review with both rows switching to criteria, leaving from review, leaving from in-progress) and the nested check case pass on terminal and desktop, 12 tests. The nested case goes from 3 to 6 filled cells and names T2 next. PASS.
- AC5: `reader.test.ts`: 11 per-fixture agreement tests plus 3 named ones pass. `python3 -m unittest scripts.tests.test_status_fixtures`: 3 tests OK, including `test_python_helpers_match_expected` and `test_generated_module_is_current`. Both sides read each fixture's `expected.json`. PASS.
- AC6: `claude plugin test`, "single-in-progress over a plugin beneath" on both surfaces: cairn's two rows draw first, then the BENEATH plugin's row, which is outside the `cairn-band` Box. With nothing active, the row beneath shows alone. PASS.
- AC7: verify slot, 2026-10-01, after the R1 test change: scripts 394 OK (21 skipped), hooks 174 OK, `claude plugin validate` passed with 1 warning (the existing `state reads: cairn.band` notice), `claude plugin test` 47 pass and 0 fail. `cairn_validate` all checks passed. PASS.

Findings:

- R1 (review, step 3): AC3 promises `wrap="truncate-end"` on every Text in the AC1 and AC2 drawings, but only the `mixed` AC3 case asserted it. Fix now: the assertion was added to the AC1 and AC2 cases in `hooks/status/band.test.tsx`. No status change, because the property held.
- R2 (diff-bug 1, blame-history 1): `cairn.band` changed shape with no `shape` tag, so a plugin reload mid-session reads M191-shaped rows and draws `undefined/undefined tasks` until the next turn end. Proposed: fix now, `atom(..., { shape: 'band-2' })` and `Shaped<CairnBandRow[]>` in `types/index.d.ts`.
- R3 (diff-bug 11, blame-history 6, prior-review 2): ragged wraps in CHANGELOG.md, README.md, DESIGN.md and the `reader.ts` header, and "their place" with an unclear antecedent. Proposed: fix now.
- R4 (diff-bug 2, 3, blame-history 3, 4, 5): layout edge cases. The title is cut by UTF-16 length, not cell width, and can split a surrogate pair. Below about 30 columns the counts are cut. The desktop font draws `░` narrower than `█`. More than five active milestones are untested against `maxRows`. Proposed: follow-up, one new candidate row "Band layout edge cases".
- R5 (prior-review 1, diff-bug 11): the "Status mod follow-ons" row still lists the hidden-band defect that M193 fixes. Proposed: noted, the plan narrows the row at post-merge hygiene.
- R6 (diff-bug 4, 5, blame-history 2): a blank open box draws `  → ` alone, and an empty title leaves three spaces. Proposed: reject, because cairn task and criterion lines carry a `Tn:`/`ACn:` label and ROADMAP rows carry a title.
- R7 (diff-bug 6, 7): TS and Python `\s` disagree on `\x1f` and U+FEFF, and the Python helper raises on an unreadable file where the reader returns nulls. Proposed: reject, because neither character occurs in a milestone file and the helper reads committed fixtures only.
- R8 (diff-bug 8, 9, 10, blame-history 7): `phaseOf` has no fallback, a rejecting `next(e)` would lose cairn's rows, and span Texts carry no keys. Proposed: reject, because the reader filters to the two phases (and R2 closes the stale path), the engine skips a throwing hook and runs the hooks beneath, and the engine drops a Text's `key`.
- Gate dispositions (operator, 2026-10-01): R2 fixed. The `band` atom takes `{ shape: 'band-2' }`, and `types/index.d.ts` declares `band: Shaped<CairnBandRow[]>`. `claude plugin validate` does not type-check that file, because a misspelled `Shapedx` passed it, so the type line has no tool check. R3 fixed, and the DESIGN.md line now also says that the item row appears only with an open box. R4 follow-up: a candidate row "Band layout edge cases", filed at hygiene. R5 noted. R6, R7, and R8 rejected for the reasons above. Verify after the fixes: scripts 394 OK, hooks 174 OK, plugin validate passed with its CLAUDE.md warning, mod tests 47/47, `cairn_validate` all checks passed.
