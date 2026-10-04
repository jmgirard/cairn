# M207: Candidate rows in the idle cairn pane

- **Status:** review
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

- [x] AC1: With no `in-progress` or `review` row, the pane draws, below the queue, a `Candidates` heading with the number of candidate rows, then one line per row in ROADMAP order. A line is a mark for the row's priority and the row's short title. A row whose text starts with exactly `[high] ` or `[low] ` has that priority, and any other row is `normal`. The short title is the text after that token up to the first `: `. For a row with no `: `, it is the whole text after the token. `pane.test.tsx` cases assert the heading, the count, the marks, and the titles for a high, a normal, and a low row, and for a row with no `: `. They also assert `normal` and the full text for rows that open with `[HIGH]`, with `[high]` and no space, and with `[low]` in mid-row. A case on each of the terminal and desktop surfaces, with a short title longer than the pane's body width, asserts that the `-text` element of its line holds the whole short title and carries `wrap: 'truncate-end'`. The test API cannot see drawn text, so the case checks the prop and not the ellipsis.
- [x] AC2: With an active row, or with no candidate rows, the pane draws no `Candidates` heading and no candidate line. `pane.test.tsx` cases assert both.
- [x] AC3: For every fixture under `hooks/status/fixtures/`, the candidate rows that `loadCairn` reads equal the `candidates` list in the fixture's `expected.json`. For each fixture with no HTML comment in its Candidates section, the number of rows equals `candidate_count` of that fixture's ROADMAP. One fixture holds a high, a normal, and a low row. One holds no Candidates section. One holds the `/cairn-init` skeleton's comment with its two placeholder rows, and its `candidates` list is empty.
- [x] AC4: README's "The cairn pane" section and the pane paragraph of `cairn/DESIGN.md` describe the Candidates section. CHANGELOG's Unreleased section has an entry for it.
- [x] AC5: The four commands of the verify slot in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T1, T2, T3

## Tasks

- [x] T1: In `reader.ts`, read the candidate rows into the `pane` state, skipping HTML comments as the M205 pane does for boxes, and bump the shape tag in `register.tsx`. Add the three AC3 fixtures and the `candidates` key to every `expected.json`. Add the Python implementation to `test_status_fixtures.py`, compare its row count to `candidate_count`, and regenerate `fixtures.gen.ts`.
- [x] T2: In `pane.ts`, with no active row, draw the heading and the lines. Add the AC1 and AC2 cases.
- [x] T3: Update README, the DESIGN pane paragraph, the CHANGELOG, and the header comments of `reader.ts` and `pane.ts`.

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
- 2026-10-04: substantive amendment: AC1's last sentence now reads "A case on each of the terminal and desktop surfaces, with a short title longer than the pane's body width, asserts that the `-text` element of its line holds the whole short title and carries `wrap: 'truncate-end'`. The test API cannot see drawn text, so the case checks the prop and not the ellipsis." The operator chose this, the second reader's wording, at the stop. The deliverable is unchanged.
- 2026-10-04: T3 done: README's pane section, the DESIGN pane paragraph, a CHANGELOG entry, and the `reader.ts` and `pane.ts` header comments describe the Candidates section. A `git grep` for `pane-1` outside the archive finds nothing. Verify: 397, 174, and 953 tests pass, and validate exits 0.
- 2026-10-04: claim audit: 41 claims read, 2 corrected — scripts/tests/test_status_fixtures.py
- 2026-10-04: implement done, status `review`. The two corrections were docstrings: the count agreement holds only where no HTML comment sits in the section, and the Python reader takes flush-left rows only. The scripts suite passes after them (397 tests).
- 2026-10-04: step-7 approval: m207-pane-candidates approved for merge

## Decisions

## Review

Review pass 1, 2026-10-04, on `968818e`. Main had not moved since the branch was cut, and no PR existed.

- AC1 evidence: `claude plugin test .` passes 956 of 956. The cases "the candidates fixture's heading, count, marks, and titles", "each priority's mark", and "a long title is kept whole and cut by the truncate-end wrap" pass on terminal and desktop. They assert `Candidates 9` after the queue, the hand-written lines for the high, normal, and low rows and the row with no `: `, and the full text with `normal` for the `[HIGH]`, `[high]` with no space, and mid-row `[low]` rows. The long title is 113 characters against a body width of 60, and its `-text` element carries `truncate-end`.
- AC2 evidence: the per-fixture cases "candidates only while idle" pass on both surfaces for every fixture with a ROADMAP. They assert no candidate keys for the active fixtures with candidate rows (`mixed`, `single-in-progress`) and for the idle fixtures with none. The domain case confirms both kinds exist.
- AC3 evidence: `reader.test.ts` "the pane's milestones and next step match expected.json" passes for every fixture, and it compares `pane.candidates` to `candidates`. `test_python_helpers_match_expected`, `test_candidate_rows_match_candidate_count`, and `test_candidate_fixtures_hold_the_shapes_ac3_names` pass. Fixture `candidates` holds all three levels, `no-active` has no Candidates section, and `candidates-skeleton` holds the skeleton's comment with an empty list.
- AC4 evidence: README.md:216-221 describes the Candidates section in "The cairn pane", `cairn/DESIGN.md`:190-199 does in the pane paragraph, and CHANGELOG.md:7-12 is the Unreleased entry.
- AC5 evidence: on `968818e` the scripts suite ran 397 tests OK (21 skipped), the hooks suite 174 OK, `claude plugin validate` exited 0 with the CLAUDE.md warning that main also has, and `claude plugin test .` exited 0 with 956 passing.
- Consistency gate: `cairn_validate.py` passes all checks. No principle changed, so no impact report runs. The `generic` profile names no toolchain checks.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: HTML comments were removed from the whole ROADMAP, so a `<!--` in another section could hide candidate rows — fix now, fixed 968818e (removal per Candidates section, a fixture row and a `reader.test.ts` case that the old removal fails).
- diff-bug #2: after a mid-session reload the `pane-2` tag reads the old value as absent, so an open pane says `no cairn ROADMAP found` until the next refresh — follow-up, row "Candidate pane follow-ons (M207 review)".
- diff-bug #3: AC1 names the full text for the three token rows, but each held a `: `, so the tests asserted a short title — fix now, fixed 968818e (those rows hold no `: `, and the tests assert the full text).
- diff-bug #4: `cairn_status` counts the skeleton's commented placeholders and indented lines, and the pane does not — follow-up, row "Candidate pane follow-ons (M207 review)".
- diff-bug #5: DESIGN and the `reader.ts` header said the reader is held to `candidate_count` without the comment and indent limits — fix now, fixed 968818e.
- diff-bug #6: the mark test did not assert the bold high mark, the uncolored normal mark, or the gray low title — fix now, fixed 968818e.
- diff-bug #7: the section match is a prefix match, so `## Candidates (dropped)` is read too — follow-up, row "Candidate pane follow-ons (M207 review)".
- diff-bug #8: a row with an empty title draws a bare mark — follow-up, row "Candidate pane follow-ons (M207 review)".
- diff-bug #9: no CRLF case covered the candidate reader — fix now, fixed 968818e (`reader.test.ts` "CRLF line breaks read as LF ones").
- diff-bug #10: JS `trim()` and Python `strip()` differ on U+FEFF and `\x1f` — follow-up, row "Candidate pane follow-ons (M207 review)", beside the same item in "Pane follow-ons (M205 review)".
- diff-bug #11: `↑`, `·`, and `↓` are ambiguous width in CJK terminals — follow-up, row "Candidate pane follow-ons (M207 review)".
- diff-bug #12: some comment and doc lines run past the wrap width — reject, style.
- diff-bug #13: the "Pane content follow-ons" row still names the candidate rows — follow-up, trimmed at this milestone's post-merge hygiene (LESSONS M154).
- blame-history #1: `CairnPaneState` in `types/index.d.ts` lacked `candidates` — fix now, fixed 5b2e010.
- blame-history #2: the "Pane content follow-ons" row is stale — follow-up, the same hygiene trim as diff-bug #13.
- blame-history #3: the reader takes flush-left rows and `candidate_count` takes indented ones — reject, planned change (Scope says top-level), with the wording fixed under diff-bug #5.
- blame-history #4: a row in the skeleton's `idea — added …` shape has no `: `, so its date and links show — follow-up, row "Candidate pane follow-ons (M207 review)".
- blame-history #5: `[HIGH]` and `[high]` with no space read as normal — reject, planned change (AC1).
- blame-history #6: the trim difference — follow-up, as diff-bug #10.
- blame-history #7: `no active milestone` and the Candidates section show together — reject, planned change (the section sits below the queue).
- blame-history #8: uneven reflow, and a DESIGN sentence that named `pane.ts` twice — reject, style, though the sentence was fixed in 5b2e010.
- prior-review #1: `CairnPaneState` not updated — fix now, as blame-history #1, fixed 5b2e010.
- prior-review #2: the trim difference — follow-up, as diff-bug #10.
- prior-review #3: the band's count and the pane differ on commented rows — follow-up, as diff-bug #4.
