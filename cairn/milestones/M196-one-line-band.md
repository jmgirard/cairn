# M196: A one-line milestone band

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m196-one-line-band

## Goal

Draw each active milestone and each skill row on one line that shows the current step, with the bar shown only during the task or criterion loop.

## Scope

**In:** `hooks/status/band.ts` builds one line per milestone and one per skill row. These lines replace the header row and the item row. The left group is the phase label, the bold id, and one text. That text is the chapter when the running skill sits on the row, else the phase's next open task or criterion, else the title. The right group shows the bar and the counts when the row shows no chapter or a chapter with a positional label. At any other chapter it shows the counts alone. `hooks/status/register.tsx` draws the one line. The tests in `hooks/status/band.test.tsx` follow. The README's "The milestone band" section, the CHANGELOG's Unreleased band entry, and the `hooks/status/` paragraph of `cairn/DESIGN.md` also follow.

**Out:** Pre and post cells on the bar were rejected at the plan gate (see the work log). The phase-label padding and the overrun at narrow widths stay in the candidate row "Band layout edge cases". An idle line between milestones stays in the candidate row "Band idle line". The stored `band`, `step`, and `dismissed` values keep their layouts and shape tags.

## Acceptance criteria

- [ ] AC1: Each `in-progress` or `review` ROADMAP row draws one band row. A running cairn skill with no milestone row of its phase draws one skill row above them. The first row ends in the close button. A test runs over every fixture in `FIXTURES` (`hooks/status/fixtures.gen.ts`) three times: with no skill, with `milestone-implement` and a chapter, and with `milestone-review` and a chapter. It asserts that the drawn row count equals the fixture's count of active rows, plus one when the skill has no row of its status. Tests of each case whose drawing starts with a skill row, with and without a chapter, also verify it.
- [ ] AC2: A milestone row's left group is the phase label, the bold id, and one text. If the running skill sits on the row and a chapter is set, that text is the chapter. If not, it is the phase's next open task or criterion. If there is none, it is the title. A chapter or item follows a `→`. Its positional label (`T<n>`, `T<n><letter>`, or `AC<n>`, with its colon) draws bold. A skill row is its label and its slash command, then `→` and the chapter when a chapter is set. Tests cover each text source in both phases, and a skill row with and without a chapter.
- [ ] AC3: If a milestone row with counts shows no chapter, or a chapter that opens with a positional label, its right group shows the bar and the counts. If it shows a chapter without one, its right group shows the counts alone. A row with a state label (`no milestone file`, `no tasks|criteria`, `all N … checked`) keeps that label whatever text its left group shows. Below 60 columns the bar is still left out. Tests cover a labeled chapter, an unlabeled chapter, no chapter, and a chapter on a state-label row.
- [ ] AC4: README's "The milestone band" section, the CHANGELOG's Unreleased band entry, and the `hooks/status/` paragraph of `cairn/DESIGN.md` describe one row per active milestone and a one-row skill row. The README's example rows are rows that `band.ts` builds from a test fixture. Where a row shows a chapter, a test marks that chapter. None of those files, nor `band.ts` or `register.tsx`, uses the phrase "item row" or "header row". The check is `grep -n -i -E 'item row|header row' README.md CHANGELOG.md cairn/DESIGN.md hooks/status/band.ts hooks/status/register.tsx`.
- [ ] AC5: In the desktop app at its default window width, the band draws three rows each on one line. They are a milestone row at a labeled chapter, a milestone row at an unlabeled chapter, and a skill row with a chapter. A chapter longer than the room left of the right group is cut at its end by `…`. The right group and the close button stay whole.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: Write the tests first in `hooks/status/band.test.tsx`. Rewrite the `DRAWN` map and the M193, M194, and M195 drawing tests for one line per row. Add the every-fixture row-count test (AC1) and the text-source tests in both phases (AC2). Add the right-group tests for a labeled chapter, an unlabeled chapter, no chapter, and a chapter on a state-label row (AC3). Confirm that the new tests fail on the two-row code for the reason they name.
- [x] T2: In `hooks/status/band.ts`, replace `HeaderLine` and `ItemLine` with one line type. Its left group is the head and one text: an arrow, a bold positional label, and the rest, or the title alone. `bandLines` picks the text (chapter, next item, title) and the right group (bar and counts, counts alone, or the state label). `skillLines` builds one line, and `lineText` follows.
- [x] T3: In `hooks/status/register.tsx`, draw the one line with the close button on the first row. Keep the M194 flex rules: `minWidth: 0` on each shrinking Box, and `flexShrink: 0` on the head, the arrow and label, and the right group. Run the four verify checks of `cairn/PROFILE.md`.
- [x] T4: Rewrite the band text in README.md, CHANGELOG.md, and `cairn/DESIGN.md`, and the comments in `band.ts` and `register.tsx`, for one row. Take the README examples from `lineText` output over a fixture and a test's chapter. Run the AC4 grep.
- [ ] T5: Do a live look in a new desktop Code session from the branch, because a session keeps the mod it loaded at start (M195 lesson). Mark a long `T<n>:` chapter during implement, a long unlabeled chapter, and a chapter on a skill row. Take a screenshot of each at the default window width.

## Work log

- 2026-10-01: created by /milestone-plan. The criteria audit (full mode, fresh Opus reader) returned eight findings, all fixed before the gate. The AC1 count test also runs with a skill and a chapter, and it names its skill-row cases. AC1 and AC4 now promise the deliverable, not the check. AC2 counts nested `T<n><letter>` labels and both phases. AC3 keeps a state label under a chapter. AC4 lets a README example carry a test's chapter. AC5 is limited to the default window width, with a defined long chapter.
- 2026-10-01: plan gate chose the bar only during the task or criterion loop over pre and post cells on every bar. The cells must guess from chapter titles which side of the loop a step is on, and a mid-loop "Plan amendment" chapter reads as after. They also need a new stored value and add two cells to a bar whose glyph widths drift in the desktop font. Falsified by a live session where the missing bar at gate and check steps hides where the milestone stands.
- 2026-10-01: plan gate chose the current step on the left, with the title as fallback, over the title with no step. The id names the milestone, and the step is the part that changes. Falsified by sessions where two active milestones cannot be told apart by id alone.
- 2026-10-01: started on branch m196-one-line-band. No question gate: the plan left no implementation choice open.
- 2026-10-01: T1–T3 done. The rewritten `band.test.tsx` ran 146 red of 188 on the two-row code, each sampled red showing two rows or the old `-header`/`-item` keys, then 188 green on the one-line code. A step's arrow is dim, its label bold, and its rest at full strength, since the step is now the row's main text. Scripts and hooks suites, plugin validate, and plugin test are green.
- 2026-10-01: T4 done. README, CHANGELOG, and DESIGN.md describe one row per milestone. The README examples are the mixed fixture's rows, the M010 post-merge chapter row, and the plan skill row, each asserted in `band.test.tsx`. The AC4 grep prints nothing (exit 1). The M062 fixture's criterion text still reads "The item row stays dim." It is fixture data the band never draws, outside the AC4 files. All four verify checks are green.

## Decisions

## Review
