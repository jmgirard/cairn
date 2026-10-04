# M207: Candidate rows in the idle cairn pane

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane draws in every adopter's session
- **Branch/PR:** m207-pane-candidates

## Goal

When no milestone is active, show the ROADMAP's candidate rows in the cairn pane.

## Scope

**In:** `reader.ts` reads the top-level `- ` bullets under `## Candidates` that sit outside HTML comments. Each row has a priority and a short title. The `pane` state gains the rows and a new shape tag. With no `in-progress` or `review` row, `pane.ts` draws a `Candidates` heading with the row count below the queue, then one line per row. A Python implementation in `scripts/tests/test_status_fixtures.py` holds the reader to each fixture's `expected.json`, as M205 did for the queue. README, DESIGN, CHANGELOG, and the header comments of `reader.ts` and `pane.ts` follow. This takes in the candidate-row part of the "Pane content follow-ons" row.

**Out:** Decisions and lessons in the pane stay in "Pane content follow-ons". The candidate rows while a milestone is active are not asked for. The new look of the section goes to M208. A press that opens a candidate stays with the clickable actions in "Status mod follow-ons".

## Acceptance criteria

- [ ] AC1: With no `in-progress` or `review` row, the pane draws, below the queue, a `Candidates` heading with the number of candidate rows, then one line per row in ROADMAP order. A line is a mark for the row's priority and the row's short title. A row whose text starts with exactly `[high] ` or `[low] ` has that priority, and any other row is `normal`. The short title is the text after that token up to the first `: `. For a row with no `: `, it is the whole text after the token. `pane.test.tsx` cases assert the heading, the count, the marks, and the titles for a high, a normal, and a low row, and for a row with no `: `. They also assert `normal` and the full text for rows that open with `[HIGH]`, with `[high]` and no space, and with `[low]` in mid-row. A case with a long title asserts that its line ends in an ellipsis.
- [ ] AC2: With an active row, or with no candidate rows, the pane draws no `Candidates` heading and no candidate line. `pane.test.tsx` cases assert both.
- [ ] AC3: For every fixture under `hooks/status/fixtures/`, the candidate rows that `loadCairn` reads equal the `candidates` list in the fixture's `expected.json`. For each fixture with no HTML comment in its Candidates section, the number of rows equals `candidate_count` of that fixture's ROADMAP. One fixture holds a high, a normal, and a low row. One holds no Candidates section. One holds the `/cairn-init` skeleton's comment with its two placeholder rows, and its `candidates` list is empty.
- [ ] AC4: README's "The cairn pane" section and the pane paragraph of `cairn/DESIGN.md` describe the Candidates section. CHANGELOG's Unreleased section has an entry for it.
- [ ] AC5: The four commands of the verify slot in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T1, T2, T3

## Tasks

- [x] T1: In `reader.ts`, read the candidate rows into the `pane` state, skipping HTML comments as the M205 pane does for boxes, and bump the shape tag in `register.tsx`. Add the three AC3 fixtures and the `candidates` key to every `expected.json`. Add the Python implementation to `test_status_fixtures.py`, compare its row count to `candidate_count`, and regenerate `fixtures.gen.ts`.
- [ ] T2: In `pane.ts`, with no active row, draw the heading and the lines. Add the AC1 and AC2 cases.
- [ ] T3: Update README, the DESIGN pane paragraph, the CHANGELOG, and the header comments of `reader.ts` and `pane.ts`.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: collision sweep: the candidate-row part of "Pane content follow-ons" is absorbed. Its decisions and lessons part stays, and hygiene trims the row. M205 shipped the pane (done). D-134 sets the priority token and was read whole. No D-entry conflicts. Inbox: 0 open issues, 0 open PRs.
- 2026-10-04: plan split the request into M207 (candidates), M208 (look, depends on M207), and M209 (placement). The goal tripwire fired, and the three parts ship apart. Placement goes last, because its probe can end the run at the goal-wrong stop.
- 2026-10-04: criteria audit (full mode, user-facing tier, fresh Opus reader) returned 12 findings over the three files, all taken toward the narrower wording. Here: rows inside HTML comments are skipped, because `candidate_count` counts the skeleton's two placeholders. AC3 binds the reader and `candidate_count`, and the Python mirror moved to T1. The token match is exact, with cases for case, spacing, and position, and a long-title case asserts the ellipsis.
- 2026-10-04: question set: candidate line. The plan shows a priority mark and the short title (recommended), over adding the date and over counts with high rows only. Falsified if the operator misses the age or the full rows in use.
- 2026-10-04: implement started on branch `m207-pane-candidates`. The untracked `tsconfig.json` in the tree is not this milestone's and stays unstaged.
- 2026-10-04: T1 done. `candidateRows` in `reader.ts` and `python_candidates` in `test_status_fixtures.py` read the rows, and the pane state's tag is `pane-2`. New fixtures are `candidates` (three levels, no `: `, `[HIGH]`, `[high]` with no space, mid-row `[low]`, a long title, a colon in backticks) and `candidates-skeleton` (the `/cairn-init` skeleton verbatim, plus a flush-left row in a comment). Every `expected.json` gained `candidates`. With the comment removal turned off, the Python reader returned the commented row on the skeleton fixture. `band.test.tsx` gained the new fixture's idle row. Verify: 397, 174, and 904 tests pass, and validate exits 0.
- 2026-10-04: implement chose a top-level `- ` match, as Scope says, over `candidate_count`'s indented match, because ROADMAP rows are one top-level line each. Falsified if a real ROADMAP indents its candidate rows.
- 2026-10-04: T2 code in place: `pane.ts` draws a `Candidates` heading with the count and one line per row while no row is active, with marks `↑` (orange, bold), `·`, and `↓` (gray, with a gray title). `pane.test.tsx` gained the AC1 and AC2 cases. Mod tests: 953 pass. AC1's ellipsis clause cannot be asserted as written, because the test API shows props and not drawn text.
- 2026-10-04: re-audit: AC1 (full) — of the amended ending "its line's text holds the whole short title and carries the `truncate-end` wrap, which draws the ellipsis": name the `-text` element, require both surfaces, and drop the claim about the renderer.
- 2026-10-04: re-audit: AC1 (full) — of the fixed ending "on both surfaces, the `-text` element holds the whole short title and carries `wrap: 'truncate-end'`; the renderer draws the ellipsis from that prop": "a long title" has no length bar, and the renderer sentence is an unchecked claim. This is the second re-audit line on AC1, so the wording goes to the operator.

## Decisions

## Review
