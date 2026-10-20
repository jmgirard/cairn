<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M294: A candidate row's ⓘ card opens where the cairn pane has room for it

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the cairn pane is the mod that adopters see   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m294-pane-card-placement   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

On the desktop, a candidate row's ⓘ card opens above its row when it fits there, else below it, and is cut to the larger side only when it fits on neither.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** In `hooks/status/pane.ts`, a pure `cardRows` (an estimate of the rows a card's text takes at the pane's width) and a pure `cardPlace` (the side and any row cap). Each candidate line carries `rowsAbove`. The render in `register.tsx` places each candidate card from the Pane props `bodyColumns`, `scroll.offset`, `scroll.bodyRows`, and `placement`. A card that opens below is drawn as an overlay at the end of the pane, revealed by the line's ⓘ scope. README, DESIGN, CHANGELOG, and the code comments follow.

**Out:** Items (1) and (2) of "Fix cut and odd names on the pane card" (a cut project name with no card, and repo names as parsed) stay in that row. The cards of other pane lines (head, task, criterion, queue, blocked, hotfix) keep opening upward. A card that closes when the pointer moves onto it stays item (5) of "Gaps only the app or mod API can close". The terminal draws no card.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `cardPlace(need, above, below)` returns `up` when `need <= above`, else `down` when `need <= below`, else the side with more rows (`up` on a tie) with a row cap equal to that side's rows, and no card when that side has fewer than 3 rows. A `pane.test.tsx` table asserts each branch, the tie, the boundaries `need = above` and `need = below`, and the under-3 case, against values written out by hand.
- [ ] AC2: `cardRows(text, columns)` estimates a card's rows: a greedy wrap of `text` at spaces at `columns - 4` columns counted by `width` in `band.ts` (code points), a word longer than a row split across rows, plus 2 border rows. The desktop's own wrap can differ from it. A `pane.test.tsx` table asserts it for an empty text, one short word, a text that fills a row exactly, a row plus one word, a word longer than a row, repeated spaces, and a word that exactly fills the last row, against values written out by hand.
- [ ] AC3: Each candidate line carries `rowsAbove`: the count of lines `paneLines` returns before it, plus the summary card's 2 border rows, each line taken as one row. A `pane.test.tsx` table over idle states asserts it against values written out by hand, varying the release line (present or absent), a blocked row with and without its counts line, a hotfix line, waiting rows, and the Next line (present or absent).
- [ ] AC4: The render places each candidate card with `cardPlace(cardRows(full, bodyColumns), rowsAbove - offset, room - (rowsAbove - offset) - 1)`, where `bodyColumns`, `offset` (`scroll.offset`), and `bodyRows` (`scroll.bodyRows`) are the Pane render's props. `room` is `bodyRows` when `placement` is `dock`, and the smaller of `bodyRows` and the pane's line count plus 2 when it is `inline`. A `pane.test.tsx` test redraws with varied `scroll.offset`, `scroll.bodyRows`, `bodyColumns`, and `placement`, and asserts the up, down, capped, and no-card results against values written out by hand.
- [ ] AC5: On the desktop, an `up` card is drawn as before (an absolute Box at `bottom: 1` in its line). A `down` card is an unkeyed `position: 'absolute'` Box drawn after every line in the pane's root Box, at `top` equal to its line's `rowsAbove` plus 1, hidden until the line's ⓘ scope lights. A cut card (AC1's result with a row cap) sets no `height` and holds `cardCut(full, cap, bodyColumns)`, with `cap` the cap from `cardPlace` and `bodyColumns` the Pane prop. For `rows >= CARD_MIN_ROWS`, the pure `cardCut(full, rows, columns)` in `pane.ts` returns `full` unchanged when `cardRows` fits it in `rows`, else its longest run of words from the start (the non-empty pieces between runs of spaces, joined by one space) that `cardRows` fits in `rows` with ` …` after it, then ` …`, or `…` alone when no word fits. The desktop's own wrap can differ from `cardRows`, so a cut card can take fewer or more rows than its cap. The terminal draws no card. A `pane.test.tsx` table asserts `cardCut`, against values written out by hand, for a cut mid-text, a run whose ` …` would wrap past `rows`, a first word that does not fit alone, a text that fits whole, repeated and leading spaces, and a word longer than a row that fits in `rows` once split; render tests assert the props above on both surfaces and a cut card's text on the desktop.
- [ ] AC6: README.md's pane paragraph, the `cairn/DESIGN.md` hover-card entry, the CHANGELOG's Unreleased ⓘ-card entry, and the comments at the card's render in `register.tsx` say that a candidate card opens above its row when it fits, else below, else cut to the larger side. None of them says that a candidate card always opens above.
- [ ] AC7: The profile's five `verify` checks pass on the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T3, T5
- AC6 → T4, T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: `pane.ts`: write the AC1 and AC2 tables first in `pane.test.tsx`, then `cardPlace` and `cardRows` (the latter on `width` from `band.ts`).
- [x] T2: `pane.ts`: add `rowsAbove` to `PaneLine` for candidate lines in `paneLines` (~line 800), as each line's index in the returned list plus 2. Write the AC3 table first.
- [x] T3: `register.tsx` (~527-545): read `bodyColumns`, `scroll`, and `placement` from `e.props`; for a candidate line, keep the `up` card in its line, or draw the `down` card as an absolute Box last in the `cairn-pane` Box, with the cap's `height` and `overflow`. Write the AC4 and AC5 tests first (redraw with new props; `flat(root)` will list the overlay, so line-counting tests allow for it).
- [x] T4: README, DESIGN, the CHANGELOG ⓘ-card entry (unreleased, so edit it), and the render comments.
- [x] T5: `pane.ts`: `cardCut`, its AC5 table first; register.tsx's `cardBox` draws a cut card with `cardCut`'s text and no `height`; update the cut-card render test, the DESIGN placement paragraph, and the `cardBox` comment (amendment after the live look).
- [ ] T6: run the five `verify` checks. Ask the operator for the live look in circumplex's docked pane: ⓘ on the first, a middle, and the last candidate row. Check that a down card draws over the rows under it, opens only from ⓘ (the keyed `cairn-pane` Box does not light it), and that its size estimate is about right. Record a miss in the parked rows that Out names.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — where a card opens is a design choice with no documented behavior to restore.
- 2026-10-20: collision check: absorbs item (3) of the candidate row "Fix cut and odd names on the pane card" (added by M293's live look); items (1) and (2) stay in that row, a split that keeps the remainder there. M286 (cards open upward) and M293 (whole-row candidate card) shipped what this extends. No D-entry covers card placement. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-20: lessons surfaced: M286 (an absolute Box paints over the rows before it, so a card opens upward), M290 (a Box in a hover group does not light it; hover needs a live look), M201/M213 (look in a real cairn repo), M193 (a state layout change needs a new shape tag; none here, since placement is computed at render).
- 2026-10-20: criteria audit (full mode, fresh Opus reader): findings on all of AC1-AC6, all taken toward the narrower promise. The Pane render's props carry `bodyColumns` and `scroll` (`offset`, `bodyRows`), and a scroll asks for a new render, so AC4 reads them and the planned `ui.scroll` state was dropped. AC2 is an estimate in code points (`width` counts no wide characters), with repeated-space and full-last-row cases. AC3 counts each line as one row and varies the lines before the candidates. AC1 gives no card under 3 rows. AC4 covers `inline` placement. AC6 names the three-way rule. T5's live look checks that the root's keyed scope does not light a down card.
- 2026-10-20: question set: a card too tall for either side — cut to the larger side (over always opening below and running off the end).
- 2026-10-20: question set: live look at implement — granted, in circumplex's docked pane, ⓘ on the first, a middle, and the last candidate row.
- 2026-10-20: plan chose an overlay at the pane's end for a card that opens below, over an in-line card at `top: 1`, because an absolute Box paints only over the rows before it, so later rows would cover an in-line card; falsified by a live look where the overlay is covered or lights from anywhere in the pane.
- 2026-10-20: plan chose render props (`scroll`, `bodyColumns`) over tracking `ui.scroll` events, because the props are given on every render and a scroll asks for a new one; falsified by a live look where a scrolled pane places cards from a stale offset.
- 2026-10-20: changelog: edit the unreleased ⓘ-card entry, since no release shipped the card.
- 2026-10-20: implement started on branch m294-pane-card-placement; untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-20: T1 done: `cardPlace` and `cardRows` in pane.ts with `CardPlace`, `CARD_MIN_ROWS` (3), and `CARD_FRAME_COLUMNS` (4); the AC1 (9 cases) and AC2 (7 cases) tables pass. The tables were appended with a shell heredoc, not Edit (a departure from the rulebook's Write/Edit rule).
- 2026-10-20: T2 done: `PaneLine.rowsAbove` is set on each candidate line as `out.length + 2` at its push; the AC3 table (8 cases) passes. The M261 tests that compare lines with and without hidden rows now leave `rowsAbove` out, since a hidden row moves the rows after it.
- 2026-10-20: T3 done: `cardPlaces(lines, view)` in pane.ts, which the render calls with `e.props.bodyColumns`, `scroll.offset`, `scroll.bodyRows`, and `placement`. register.tsx's `cardBox` draws an up card in its line at `bottom: 1` and a down card last in the `cairn-pane` Box at `top: rowsAbove + 1`, with `height` and `overflow: 'hidden'` when cut. The AC4 table (8 cases) and the AC5 render tests (3 per surface, each mount unmounted after its read) pass. A planted defect (placement ignoring the scroll offset) failed 7 of them, 5 AC4 and 2 AC5, then was restored.
- 2026-10-20: T4 done: README, DESIGN (the placement paragraph and two rewrapped lines), the CHANGELOG ⓘ-card entry, and the register.tsx comments state the three-way rule. A `git grep` for upward-only phrasing finds only the other lines' cards, which still open upward.
- 2026-10-20: verify green: scripts 428 OK, hooks 193 OK, both validates exit 0, mod tests 2374 pass 0 fail.
- 2026-10-20: live look (operator, circumplex docked pane): cards open on a side with room, draw over the rows, and open only from ⓘ; the second row's card (795 characters, the one cut card) showed empty rows above and below its text, read as its fixed `height` exceeding the rows the desktop's wider wrap takes.
- 2026-10-20: re-audit: AC5 (full) — 9 items: the cut needs a pure `cardCut` with its own table; the terminal clause; leading spaces; dropping `height` lets a card overrun, so say so (no `maxHeight` prop); DESIGN and the `cardBox` comment go stale; "longest run" well defined; no IP or D-entry conflict.
- 2026-10-20: re-audit: AC5 (full) — 5 findings on the fixed wording: "last" with several down cards, the render's `cardCut` arguments, a ` …` that wraps past `rows`, `rows >= CARD_MIN_ROWS` for `…` alone, and the cut/capped terms. Applied; a second re-audit line on AC5 is the stop, so the wording goes to the operator.
- 2026-10-20: substantive amendment: AC5's cut-card clause now cuts the text by whole words with `cardCut` and sets no `height`, at the operator's approval of the wording shown; T5 added for it, the old T5 renumbered T6, Coverage renumbered. The live look's verify-and-look step stays in the new T6 as a short recheck of the second row.
- 2026-10-20: T5 done: `cardCut` in pane.ts; `cardBox` draws a cut card with `cardCut(full, cap, bodyColumns)` and no `height` or `overflow`; the cardCut table (6 cases) passes, and the cut-card render test asserts no height and the text `Long row: aaaa bbbb cccc …`. DESIGN's placement paragraph and the `cardBox` comment follow. Verify green: scripts 428 OK, hooks 193 OK, both validates exit 0, mod tests 2380 pass 0 fail.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
