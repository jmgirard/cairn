# M197: A band that fits narrow windows and the desktop font

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m197-band-narrow-fit

## Goal

Keep each band row inside the window from 36 columns up, with a steady label gap, bar, and close control in the desktop app.

## Scope

**In:** If the full right group leaves the text too little room, `hooks/status/band.ts` picks a shorter form. In the same case, a skill row drops its slash command. A fit rule replaces the fixed 60-column bar cutoff. Each label is followed by one space instead of padding. The bar draws ten `█` cells, and the empty ones are dim. `hooks/status/register.tsx` draws the close control in the form the operator picks at a live look. Two fixtures are new: `widest`, with rows at the bounds AC1 names, and `six-active`. `hooks/status/band.test.tsx` follows. The README's "The milestone band" section, the CHANGELOG's Unreleased band entry, and the `hooks/status/` paragraph of `cairn/DESIGN.md` also follow.

**Out:** A skill row that folds onto the milestone row stays in the candidate row "Band one row with a skill". A lost press and the band's return stay in "Band close-state edge cases". Some rows are wider than the `widest` fixture, for example with a 6-character id or 4-digit counts. Some terminals draw `→`, `█`, or `×` two columns wide. Both stay outside AC1, and no row holds them until a real session draws one. The engine scrolls a tree taller than `maxRows`, so the close button stays on the first row. The stored `band`, `step`, and `dismissed` values keep their layouts and shape tags.

## Acceptance criteria

- [ ] AC1: In the terminal, at each band width from 36 to 120 columns, each sampled row fits the width in its parts that never shrink. The sampled rows are three sets. The first set is each row of each fixture under `hooks/status/fixtures/`, with no skill running. These fixtures include `widest`, whose rows reach the id `M1000`, the counts `100/100`, and the label `all 100 criteria checked`. The second set is the rows that carry a skill at a long chapter and show counts, on each fixture with such a row. That is the row that carries `/milestone-implement` at `T10a: Long step`, and the row that carries `/milestone-review` at `AC10a: Long step`. The third set is the skill row of each `SKILL_LABELS` skill on the `no-active` fixture, at the chapter `Question gate`. The parts that never shrink are the Texts in the head Box and the right group. They also include the right group's left margin, and the close gap and label on the first row. A `band.test.tsx` sweep counts one column per code point in those parts, for each sampled row and width.
- [ ] AC2: A row's right group takes the first of its forms that leaves enough room for the row's text, else its last form. Enough room is the text's full width or 10 columns, whichever is less. In its task or criterion loop, a row starts at the bar and counts. It then goes to the counts with their noun (`2/3 criteria`), and then to the bare counts (`2/3`). Its other counts start at the counts with their noun. `all N <noun> checked` goes to `N/N checked`, and `no milestone file` goes to `no file`. This rule replaces the fixed 60-column bar cutoff. If a skill row's head leaves less than enough room for its chapter, the row drops its slash command. For each change of form, `band.test.tsx` asserts the earlier form at the narrowest width that keeps it. It asserts the later form one column below that width.
- [ ] AC3: Every row's head draws its phase or skill label and then exactly one space. Every bar draws its ten cells with the one glyph `█`, and the empty cells are dim. `band.test.tsx` asserts both at 120 columns, on every row of every fixture and on the skill row of each `SKILL_LABELS` skill.
- [ ] AC4: In the desktop app, the band's close control draws no smaller than the close icon on the app's bar above the band. This holds at the default zoom in the light and dark themes. The evidence is an operator live look in a new Code session, with its screenshots.
- [ ] AC5: The mod draws one row per active milestone whatever `maxRows` is. A `band.test.tsx` test uses the `six-active` fixture at a `maxRows` of 3. It asserts six milestone rows in ROADMAP order and the close button on the first row only.
- [ ] AC6: Three docs describe the shorter forms, the one-space label, and the one-glyph bar with its dim empty cells. They are README's "The milestone band" section, CHANGELOG's unreleased entry, and DESIGN.md's `hooks/status/` entry. At review, you compare each line inside a `text` block of that README section by hand with the rows `band.test.tsx` asserts. Each line equals one of those rows.
- [ ] AC7: The verify slot of `cairn/PROFILE.md` is clean. That is both Python suites (`scripts/tests`, `hooks/tests`), `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T2, T3
- AC3 → T2, T3, T5
- AC4 → T4
- AC5 → T1, T2
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Add the `widest` and `six-active` fixtures under `hooks/status/fixtures/`, each with its `expected.json`. `widest` holds one row per right-group form at the AC1 bounds, all with 5-character ids. Its rows are an open `T10a:` task, an open `AC10a:` criterion, all of 100 checked, and a missing file. The open-task row comes first among the `in-progress` rows, and the open-criterion row comes first among the `review` rows. Run `python3 hooks/status/gen_fixtures.py`, then the Python suites, which read every fixture.
- [x] T2: Write the failing tests in `band.test.tsx` first. They are the AC1 width sweep, the AC2 form changes at their switch widths, the AC3 label and glyph tests, and the AC5 six-row test. Rewrite the hand-written `DRAWN` rows with one-space labels. Retire the 59-column and 60-column bar tests and the `░` filters.
- [x] T3: Change `band.ts`. Drop `padEnd(LABEL_WIDTH)`, draw the empty bar cells as dim `█`, and replace `BAR_MIN_COLUMNS` with the AC2 form choice. `bandLines` and `skillLines` need the first row's close width to measure the fit. Change `register.tsx` only for what the measure needs.
- [ ] T4: In a new desktop Code session, look at two close-control forms in the light and dark themes. One is a Button without `plain`, so the app draws its native close control. The other is the label `✕`. Keep the form the operator picks, and log the screenshots. If neither form matches the app's icon, open the amendment gate to move AC4 back to a candidate row.
- [ ] T5: In a new desktop Code session, look at a narrow pane with an active milestone and a skill row. Make sure that the rows stay inside the pane and that the bar keeps one width at two counts. Make sure that the gap after `implement` and after `review` is the same. Log what the look shows.
- [ ] T6: Update README's "The milestone band" section, the CHANGELOG's Unreleased band entry, and DESIGN.md's `hooks/status/` paragraph. Say that README rows show the empty bar cells as `█`, because a text block cannot show dim.
- [ ] T7: Run the verify slot from the repo root and read each exit code. Run `python3 -m unittest` in `scripts/tests` and in `hooks/tests`. Then run `claude plugin validate .claude-plugin/plugin.json` and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`.

## Work log

- 2026-10-01: created by /milestone-plan from the `[high]` candidate row "Band layout edge cases" (M193 review R4, M194 review F1, M196 review F1–F2).
- 2026-10-01: criteria audit (full mode, fresh Opus reader) returned 12 findings, and all were fixed before the gate. AC1 covers the terminal at one column per code point, with a `widest` fixture and carrier rows. AC2's text room is the smaller of the text's width and 10. The 60-column bar cutoff is retired, and each form change is tested at its switch width. AC5 covers the mod's rows only, because the engine scrolls. AC6's README check is a hand comparison at review.
- 2026-10-01: plan gate chose shorter right-group forms over letting the engine cut the right group, because a cut count such as `2/1…` reads wrong. Falsified by a live look where a shorter form reads worse than a cut one.
- 2026-10-01: plan gate chose one space after the label over a 9-column Box. The gap is the same in both fonts, and a Box's desktop width is unknown. Falsified by a live look where unaligned rows of different phases read worse than the padded gap.
- 2026-10-01: plan gate chose one dim `█` glyph for empty cells over `█` and `░`. One glyph keeps the bar one width in any font. Falsified by a terminal theme where dim and filled `█` look the same.
- 2026-10-01: plan gate chose to fix the close control's size here over leaving it as a candidate, because the operator raised it with the layout items. Falsified by T4 finding that no form the mod can draw matches the app's icon.
- 2026-10-01: criteria re-audit (full mode, same Opus reader) after the gate returned 2 findings, and both were fixed. AC1's second set now holds only carrier rows that show counts, because a labeled chapter on a state-label row needs 38 columns. T1 now orders `widest` so its open rows carry the skill. Narrowing the promise won over a fallback that drops the positional label. Falsified by a real session whose all-checked carrier row overruns a narrow window.
- 2026-10-01: T1 done. In `widest`, M1000 is in-progress at an open `T10a:` with 99/100 tasks, and M1001 is in-progress with no file. M1002 is in review at an open `AC10a:` with 99/100 criteria, and M1003 has all 100 criteria checked. `six-active` has six active rows and one planned row between them. The Python helpers match both hand-written `expected.json` files. Verify clean: scripts 394, hooks 174, validate 0, mod tests 196/196.
- 2026-10-01: T2 done. The new tests ran first against the old `band.ts`: 133 of 260 failed, the AC1 sweep among them (the implement skill row needed 38 columns at 36 and 37). The 59 and 60 column tests became 56 and 57, the switch width of mixed's first row.
- 2026-10-01: T3 done. `band.ts` picks each form with `fit`, the skill row drops its command, labels take one space, and the bar draws one glyph. `register.tsx` passes the close gap and label columns. A planted close width of 0 failed 9 tests, the AC2 switch tests among them, and the AC1 sweep stayed green because a 3-column error only shrinks the text. Verify clean: mod tests 260/260.

## Decisions

## Review
