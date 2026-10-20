<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M294: A candidate row's ⓘ card opens where the cairn pane has room for it

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the cairn pane is the mod that adopters see   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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
- [ ] AC5: On the desktop, an `up` card is drawn as before (an absolute Box at `bottom: 1` in its line). A `down` card is an unkeyed `position: 'absolute'` Box drawn last in the pane's root Box, at `top` equal to its line's `rowsAbove` plus 1, hidden until the line's ⓘ scope lights. A capped card has `height` equal to its cap and `overflow: 'hidden'`. The terminal draws no card. `pane.test.tsx` tests assert these props on both surfaces.
- [ ] AC6: README.md's pane paragraph, the `cairn/DESIGN.md` hover-card entry, the CHANGELOG's Unreleased ⓘ-card entry, and the comments at the card's render in `register.tsx` say that a candidate card opens above its row when it fits, else below, else cut to the larger side. None of them says that a candidate card always opens above.
- [ ] AC7: The profile's five `verify` checks pass on the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T3
- AC6 → T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [ ] T1: `pane.ts`: write the AC1 and AC2 tables first in `pane.test.tsx`, then `cardPlace` and `cardRows` (the latter on `width` from `band.ts`).
- [ ] T2: `pane.ts`: add `rowsAbove` to `PaneLine` for candidate lines in `paneLines` (~line 800), as each line's index in the returned list plus 2. Write the AC3 table first.
- [ ] T3: `register.tsx` (~527-545): read `bodyColumns`, `scroll`, and `placement` from `e.props`; for a candidate line, keep the `up` card in its line, or draw the `down` card as an absolute Box last in the `cairn-pane` Box, with the cap's `height` and `overflow`. Write the AC4 and AC5 tests first (redraw with new props; `flat(root)` will list the overlay, so line-counting tests allow for it).
- [ ] T4: README, DESIGN, the CHANGELOG ⓘ-card entry (unreleased, so edit it), and the render comments.
- [ ] T5: run the five `verify` checks. Ask the operator for the live look in circumplex's docked pane: ⓘ on the first, a middle, and the last candidate row. Check that a down card draws over the rows under it, opens only from ⓘ (the keyed `cairn-pane` Box does not light it), and that its size estimate is about right. Record a miss in the parked rows that Out names.

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

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
