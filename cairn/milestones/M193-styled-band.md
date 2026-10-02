# M193: A styled milestone band that follows the phase

- **Status:** in-progress
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

- [ ] AC1: Take each `in-progress` or `review` row whose milestone path is a readable regular file and whose phase section holds an unchecked checkbox. For each such row, the band draws two rows, in ROADMAP order. The phase section is what `_section_body` returns for `Tasks` on an `in-progress` row and for `Acceptance criteria` on a `review` row. The header row names the id, the title, the phase (`implement` or `review`), a progress bar (at `bodyColumns` 60 or more, AC3), and `<checked>/<total> tasks` or `<checked>/<total> criteria`. The counts are over the phase section's lines that `_AC_ITEM` matches. The item row shows the first such line whose box is `[ ]`, less the prefix that `^\s*-\s*\[ \]\s*` matches. Shown by `claude plugin test` cases on the terminal and desktop surfaces over three fixtures: `single-in-progress`, `mixed`, and a fixture whose first unchecked task is nested. The `review` row M010 in `mixed` has 3/5 tasks and 2/3 criteria.
- [ ] AC2: Three states draw the header row alone, with no bar and no item row. The first is a row whose milestone path is not a readable regular file (`no milestone file`). The second is a phase section with no checkboxes, or no such section (`no tasks` or `no criteria`). The third is a phase section whose checkboxes are all checked (`all <N> tasks checked` or `all <N> criteria checked`). Shown by `claude plugin test` cases over fixtures that hold four cases in each phase. The cases are a path that is not a readable regular file, no phase section, a phase section with no checkboxes, and an all-checked phase section.
- [ ] AC3: The Text elements inside the `cairn-band` Box carry style props. The phase label's color differs between `implement` and `review`. The id is bold. The bar's filled cells carry a color. `no milestone file` carries a color. The item row is dim. In the drawings of the AC1 and AC2 cases, every Text inside the `cairn-band` Box carries `wrap="truncate-end"`. When `bodyColumns` is below 60, the header row omits the bar and keeps the counts. At 60 or more, it shows the bar. Shown by `claude plugin test` cases that read the drawn elements' props from `findAll`. The cases mount `mixed`, which holds both phases and a missing file, at `bodyColumns` 59, 60, and 120.
- [ ] AC4: The band follows edits at the next turn end. M191's five edit cases stay, with their expected rows restated in the new layout. In addition, a check on the item row's task grows the bar's filled cells and shows the next unchecked task. A row that moves from `in-progress` to `review` switches both rows from tasks to criteria, over a fixture whose row holds an unchecked criterion. Shown by the edit cases in `hooks/status/band.test.tsx` on both surfaces.
- [ ] AC5: The reader and the Python helpers agree on every fixture. For each active row, the reader's task and criterion counts, and the first unchecked line of each section, equal the values that `scripts/tests/test_status_fixtures.py` computes. A first unchecked line is null where the path is not a readable regular file or the section has no unchecked box. The Python side computes counts with `_section_body` and `_AC_ITEM`, and the first unchecked line by AC1's rule over the same `_section_body`. Shown by `hooks/status/reader.test.ts` and `test_status_fixtures.py` over each fixture's `expected.json`, both of which fail on any difference.
- [ ] AC6: When the band has rows to draw, it draws them above the tree that the hooks beneath it return from `next(e)`, so another plugin's band beneath cairn's still shows. Shown by a `claude plugin test` case on both surfaces with a second plugin beneath cairn (tier `append`) that draws its own band row.
- [ ] AC7: The verify slot in `cairn/PROFILE.md` runs clean: both Python suites, `claude plugin validate`, and `claude plugin test`.

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
- [ ] T7: Look at the band live in the desktop app at a normal and a narrow width, in implement and in review, and record what it showed in the work log.

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

## Decisions
