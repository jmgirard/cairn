# M196: A one-line milestone band

- **Status:** review
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

- [x] AC1: Each `in-progress` or `review` ROADMAP row draws one band row. A running cairn skill with no milestone row of its phase draws one skill row above them. The first row ends in the close button. A test runs over every fixture in `FIXTURES` (`hooks/status/fixtures.gen.ts`) three times: with no skill, with `milestone-implement` and a chapter, and with `milestone-review` and a chapter. It asserts that the drawn row count equals the fixture's count of active rows, plus one when the skill has no row of its status. Tests of each case whose drawing starts with a skill row, with and without a chapter, also verify it.
- [x] AC2: A milestone row's left group is the phase label, the bold id, and one text. If the running skill sits on the row and a chapter is set, that text is the chapter. If not, it is the phase's next open task or criterion. If there is none, it is the title. A chapter or item follows a `→`. Its positional label (`T<n>`, `T<n><letter>`, or `AC<n>`, with its colon) draws bold. A skill row is its label and its slash command, then `→` and the chapter when a chapter is set. Tests cover each text source in both phases, and a skill row with and without a chapter.
- [x] AC3: If a milestone row with counts shows no chapter, or a chapter that opens with a positional label, its right group shows the bar and the counts. If it shows a chapter without one, its right group shows the counts alone. A row with a state label (`no milestone file`, `no tasks|criteria`, `all N … checked`) keeps that label whatever text its left group shows. Below 60 columns the bar is still left out. Tests cover a labeled chapter, an unlabeled chapter, no chapter, and a chapter on a state-label row.
- [x] AC4: README's "The milestone band" section, the CHANGELOG's Unreleased band entry, and the `hooks/status/` paragraph of `cairn/DESIGN.md` describe one row per active milestone and a one-row skill row. The README's example rows are rows that `band.ts` builds from a test fixture. Where a row shows a chapter, a test marks that chapter. None of those files, nor `band.ts` or `register.tsx`, uses the phrase "item row" or "header row". The check is `grep -n -i -E 'item row|header row' README.md CHANGELOG.md cairn/DESIGN.md hooks/status/band.ts hooks/status/register.tsx`.
- [x] AC5: In the desktop app at its default window width, the band draws three rows each on one line. They are a milestone row at a labeled chapter, a milestone row at an unlabeled chapter, and a skill row with a chapter. A chapter longer than the room left of the right group is cut at its end by `…`. The right group and the close button stay whole.

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
- [x] T5: Do a live look in a new desktop Code session from the branch, because a session keeps the mod it loaded at start (M195 lesson). Mark a long `T<n>:` chapter during implement, a long unlabeled chapter, and a chapter on a skill row. Take a screenshot of each at the default window width.

## Work log

- 2026-10-01: created by /milestone-plan. The criteria audit (full mode, fresh Opus reader) returned eight findings, all fixed before the gate. The AC1 count test also runs with a skill and a chapter, and it names its skill-row cases. AC1 and AC4 now promise the deliverable, not the check. AC2 counts nested `T<n><letter>` labels and both phases. AC3 keeps a state label under a chapter. AC4 lets a README example carry a test's chapter. AC5 is limited to the default window width, with a defined long chapter.
- 2026-10-01: plan gate chose the bar only during the task or criterion loop over pre and post cells on every bar. The cells must guess from chapter titles which side of the loop a step is on, and a mid-loop "Plan amendment" chapter reads as after. They also need a new stored value and add two cells to a bar whose glyph widths drift in the desktop font. Falsified by a live session where the missing bar at gate and check steps hides where the milestone stands.
- 2026-10-01: plan gate chose the current step on the left, with the title as fallback, over the title with no step. The id names the milestone, and the step is the part that changes. Falsified by sessions where two active milestones cannot be told apart by id alone.
- 2026-10-01: started on branch m196-one-line-band. No question gate: the plan left no implementation choice open.
- 2026-10-01: T1–T3 done. The rewritten `band.test.tsx` ran 146 red of 188 on the two-row code, each sampled red showing two rows or the old `-header`/`-item` keys, then 188 green on the one-line code. A step's arrow is dim, its label bold, and its rest at full strength, since the step is now the row's main text. Scripts and hooks suites, plugin validate, and plugin test are green.
- 2026-10-01: T4 done. README, CHANGELOG, and DESIGN.md describe one row per milestone. The README examples are the mixed fixture's rows, the M010 post-merge chapter row, and the plan skill row, each asserted in `band.test.tsx`. The AC4 grep prints nothing (exit 1). The M062 fixture's criterion text still reads "The item row stays dim." It is fixture data the band never draws, outside the AC4 files. All four verify checks are green.
- 2026-10-01: claim audit: 70 claims read, 5 corrected — README.md, CHANGELOG.md, hooks/status/band.test.tsx. The same reader re-read the five corrected claims once and found all accurate. Mod tests 188 green, AC4 grep empty.
- 2026-10-01: T5 needs a new desktop Code session that loads the mod from this branch, because a session keeps the mod it loaded at start (M195 lesson). The plugin path `~/.claude/skills/cairn` links to this checkout, so a new session on the branch loads the M196 mod.
- 2026-10-01: T5 done in a new desktop Code session on the branch, at the default window width, from operator screenshots. A long `T5:` chapter drew on one line with the bar, `4/5 tasks`, and `×` whole and the chapter cut by `…`. A long unlabeled chapter drew the counts alone, no bar, cut by `…`. With `/milestone` loaded and a long chapter, a `status /milestone →` skill row drew above the M196 row, cut by `…` before `×`. The operator asked why that case draws two rows, and chose to keep the separate skill row and file the candidate row "Band one row with a skill".

## Decisions

## Review

Fresh evidence 2026-10-01 on `m196-one-line-band`. The branch holds `origin/main`, so no merge was needed. Verify: scripts 394 OK (21 skipped), hooks 174 OK, plugin validate exit 0 with warnings. `claude plugin test .` gave 188 pass and 0 fail (binary 2.1.286, function hooks on).

- AC1: the "one row per active milestone" block passes. It runs all 13 `FIXTURES` keys three ways: no skill, implement with a chapter, review with a chapter. Each case compares the drawn rows with the active rows, plus one skill row for a skill that no row carries. Each case asserts that the first row ends in `cairn-close`. The M195 skill-row tests and close-button tests also pass, with and without a chapter.
- AC2: the "a row's one text" block passes 8 tests. They cover chapter, next open item, and title in both implement and review, and a skill row with and without a chapter on both surfaces. The "step's label draws bold" block passes 4 tests: `AC3:`, `T2:`, and `T1a:` draw bold after a dim arrow, and an unlabeled item draws no bold text after the id.
- AC3: the "right group shows the bar only in the task or criterion loop" block passes 6 tests. A labeled chapter and a nested labeled chapter keep the bar and counts. An unlabeled chapter shows the counts alone, and no chapter keeps the bar. Below 60 columns a labeled chapter shows the counts alone. A chapter on a state-label row keeps the label.
- AC4: the AC4 grep printed nothing (exit 1). README, CHANGELOG, and DESIGN.md read as one row per active milestone and a one-row skill row. The four README fixture rows are the `mixed` entry of `DRAWN`, which "the hand-written rows match what band.ts builds" checks. The `Post-merge hygiene` row is asserted at `band.test.tsx:1058` and the `Question gate` skill row at `band.test.tsx:369`.
- AC5: the T5 live look (work log, 2026-10-01) is the evidence, and it holds for the review head. `git diff --stat 268923a..HEAD` shows that `band.ts` and `register.tsx` did not change after T4, so T5 looked at the code under review. At the default window width it drew three one-line rows. A long `T5:` chapter kept the bar, `4/5 tasks`, and `×` whole, with the chapter cut by `…`. A long unlabeled chapter showed the counts alone, cut by `…`. A `status /milestone →` skill row with a long chapter was cut by `…` before `×`. The screenshots were the operator's, so this review did not repeat the look.

Consistency gate: `cairn_validate.py` passed all checks (exit 0), coverage complete included. No principle changed, so `cairn_impact` was skipped. The `generic` profile names no toolchain checks.

Independent review: three fresh reviewers (Opus diff-bug, Sonnet blame-history, Sonnet prior-review). The prior-review probe found no GitHub review comments, so that lens read the M191, M193, M194, and M195 archive reviews. No finding shows a criterion failing. Proposed dispositions, for the gate:

- F1 (diff-bug 1, blame 2): a skill row's slash command moved into the head Box, which never shrinks. At 36 columns `implement /milestone-implement → ` plus `  ×` overruns. Narrow-width overrun is Out of scope. Proposed: follow-up, extend the candidate row "Band layout edge cases".
- F2 (diff-bug 5, blame 5): that candidate row still says "a header row can overrun" and "the engine cuts the title". Proposed: follow-up, corrected in the same row edit.
- F3 (prior-review 1, blame 6): ragged wraps in CHANGELOG.md lines 17, 28, 33, and 36, and long lines in README.md 139 and 145. Three past reviews fixed the same thing. Proposed: fix now.
- F4 (diff-bug 6): two test names at `band.test.tsx:1050` and `:1064` say "put the title on". The tests put the chapter on the row. Proposed: fix now.
- F5 (diff-bug 7): the test "a labeled chapter keeps the bar" uses `T2: Write the command.`, which equals M002's next open task. If `bandLines` ignores the chapter, the test still passes. Proposed: fix now with a different labeled chapter.
- F6 (diff-bug 8): DESIGN.md line 75 reads as if only the open box follows a `→`. Proposed: fix now.
- F7 (diff-bug 2, blame 3): the bar test accepts any positional label in either phase, so an `AC2:` chapter during implement keeps the tasks bar. Proposed: reject. AC3 states this rule, and the skills mark `Tn:` chapters in implement and `ACn:` in review.
- F8 (diff-bug 3): a range label such as `T1-T3:` reads as unlabeled and hides the bar. Proposed: reject. The skills mark one task or criterion per chapter.
- F9 (diff-bug 4): the README example `review M010 → Post-merge hygiene 2/3 criteria` is a state the review flow never reaches. Proposed: reject. The README says it shows a test fixture's row.
- F10 (diff-bug 9, blame 5): the M062 fixture still says "The item row stays dim." Proposed: reject. It is fixture data, and the work log records it.
- F11 (blame 1, prior-review 2): a row with an open item no longer shows the title, which reverses the M195 layout. Proposed: reject. The plan gate chose this, and the work log records the choice and the evidence that falsifies it.
- F12 (blame 4): older guards were rewritten, not carried over. The 40-column title test now runs through a chapter. Proposed: reject. Rows with no open item and state-label rows still draw the title at narrow width.
- F13 (prior-review 3): no stale test counts found. Noted.
