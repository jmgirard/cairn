<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M294: A candidate row's ⓘ card opens where the cairn pane has room for it

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the cairn pane is the mod that adopters see   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m294-pane-card-placement, https://github.com/jmgirard/cairn/pull/307   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

On the desktop, a candidate row's ⓘ card opens above its row when it fits there, else below it, and is cut to the larger side only when it fits on neither.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** In `hooks/status/pane.ts`, a pure `cardRows` (an estimate of the rows a card's text takes at the pane's width) and a pure `cardPlace` (the side and any row cap). Each candidate line carries `rowsAbove`. The render in `register.tsx` places each candidate card from the Pane props `bodyColumns`, `scroll.offset`, `scroll.bodyRows`, and `placement`. A card that opens below is drawn as an overlay at the end of the pane, revealed by the line's ⓘ scope. README, DESIGN, CHANGELOG, and the code comments follow.

**Out:** Items (1) and (2) of "Fix cut and odd names on the pane card" (a cut project name with no card, and repo names as parsed) stay in that row. The cards of other pane lines (head, task, criterion, queue, blocked, hotfix) keep opening upward. A card that closes when the pointer moves onto it stays item (5) of "Gaps only the app or mod API can close". The terminal draws no card.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: `cardPlace(need, above, below)` returns `up` when `need <= above`, else `down` when `need <= below`, else the side with more rows (`up` on a tie) with a row cap equal to that side's rows, and no card when that side has fewer than 3 rows. A `pane.test.tsx` table asserts each branch, the tie, the boundaries `need = above` and `need = below`, and the under-3 case, against values written out by hand.
- [x] AC2: `cardRows(text, columns)` estimates a card's rows: a greedy wrap of `text` at spaces at `columns - 4` columns counted by `width` in `band.ts` (code points), a word longer than a row split across rows, plus 2 border rows. The desktop's own wrap can differ from it. A `pane.test.tsx` table asserts it for an empty text, one short word, a text that fills a row exactly, a row plus one word, a word longer than a row, repeated spaces, and a word that exactly fills the last row, against values written out by hand.
- [x] AC3: Each candidate line carries `rowsAbove`: the count of lines `paneLines` returns before it, plus the summary card's 2 border rows, each line taken as one row. A `pane.test.tsx` table over idle states asserts it against values written out by hand, varying the release line (present or absent), a blocked row with and without its counts line, a hotfix line, waiting rows, and the Next line (present or absent).
- [x] AC4: The render places each candidate card with `cardPlace(cardRows(full, bodyColumns), rowsAbove - offset, room - (rowsAbove - offset) - 1)`, where `bodyColumns`, `offset` (`scroll.offset`), and `bodyRows` (`scroll.bodyRows`) are the Pane render's props. `room` is `bodyRows` when `placement` is `dock`, and the smaller of `bodyRows` and the pane's line count plus 2 when it is `inline`. A `pane.test.tsx` test redraws with varied `scroll.offset`, `scroll.bodyRows`, `bodyColumns`, and `placement`, and asserts the up, down, capped, and no-card results against values written out by hand.
- [x] AC5: On the desktop, an `up` card is drawn as before (an absolute Box at `bottom: 1` in its line). A `down` card is an unkeyed `position: 'absolute'` Box drawn after every line in the pane's root Box, at `top` equal to its line's `rowsAbove` plus 1, hidden until the line's ⓘ scope lights. A cut card (AC1's result with a row cap) sets no `height` and holds `cardCut(full, cap, bodyColumns)`, with `cap` the cap from `cardPlace` and `bodyColumns` the Pane prop. For `rows >= CARD_MIN_ROWS`, the pure `cardCut(full, rows, columns)` in `pane.ts` returns `full` unchanged when `cardRows` fits it in `rows`, else its longest run of words from the start (the non-empty pieces between runs of spaces, joined by one space) that `cardRows` fits in `rows` with ` …` after it, then ` …`, or `…` alone when no word fits. The desktop's own wrap can differ from `cardRows`, so a cut card can take fewer or more rows than its cap. The terminal draws no card. A `pane.test.tsx` table asserts `cardCut`, against values written out by hand, for a cut mid-text, a run whose ` …` would wrap past `rows`, a first word that does not fit alone, a text that fits whole, repeated and leading spaces, and a word longer than a row that fits in `rows` once split; render tests assert the props above on both surfaces and a cut card's text on the desktop.
- [x] AC6: README.md's pane paragraph, the `cairn/DESIGN.md` hover-card entry, the CHANGELOG's Unreleased ⓘ-card entry, and the comments at the card's render in `register.tsx` say that a candidate card opens above its row when it fits, else below, else cut to the larger side. None of them says that a candidate card always opens above.
- [x] AC7: The profile's five `verify` checks pass on the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2, T8
- AC4 → T3, T7, T9
- AC5 → T3, T5
- AC6 → T4, T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: `pane.ts`: write the AC1 and AC2 tables first in `pane.test.tsx`, then `cardPlace` and `cardRows` (the latter on `width` from `band.ts`).
- [x] T2: `pane.ts`: add `rowsAbove` to `PaneLine` for candidate lines in `paneLines` (~line 800), as each line's index in the returned list plus 2. Write the AC3 table first.
- [x] T3: `register.tsx` (~527-545): read `bodyColumns`, `scroll`, and `placement` from `e.props`; for a candidate line, keep the `up` card in its line, or draw the `down` card as an absolute Box after every line in the `cairn-pane` Box (a cut card's `height` and `overflow`, first planned here, were replaced by T5's cut text and no height). Write the AC4 and AC5 tests first (redraw with new props; `flat(root)` will list the overlay, so line-counting tests allow for it).
- [x] T4: README, DESIGN, the CHANGELOG ⓘ-card entry (unreleased, so edit it), and the render comments.
- [x] T5: `pane.ts`: `cardCut`, its AC5 table first; register.tsx's `cardBox` draws a cut card with `cardCut`'s text and no `height`; update the cut-card render test, the DESIGN placement paragraph, and the `cardBox` comment (amendment after the live look).
- [x] T6: run the five `verify` checks. Ask the operator for the live look in circumplex's docked pane: ⓘ on the first, a middle, and the last candidate row. Check that a down card draws over the rows under it, opens only from ⓘ (the keyed `cairn-pane` Box does not light it), and that its size estimate is about right. Record a miss in the parked rows that Out names.
- [x] T7: review return 1: render tests that redraw at a second `bodyColumns` and with `placement: 'inline'`, asserting the side and cut against values written out by hand (AC4).
- [x] T8: review pass 1's fix-now batch: the stale "above the row" comments and DESIGN lines, the two comment grammar fixes, the `isCard` and `flat` comments, the `unplaced` rename, the down list taking only lines with the ⓘ scope, and a `rowsAbove` case after a hidden started row.
- [x] T9: review return 2: a redraw too short on both sides that asserts no card (AC4), and pass 2's fix-now wording.

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
- 2026-10-20: T6 done: verify green (above); the operator's recheck in circumplex found the second row's card ending in "…" with no empty rows.
- 2026-10-20: claim audit: 75 claims read, 5 corrected — pane.test.tsx (the AC5 comment still said a cut card takes a height), pane.ts (`CardPlace.rows` is the rows the text is fitted to), register.tsx ("only over the rows before it" restated as the type doc's siblings, with the live look as the source), README.md and CHANGELOG.md (the no-card case, "when it fits only below", and the estimate's limit replace "no longer runs past the pane's top").
- 2026-10-20: implement done; status review.
- 2026-10-20: review return 1: AC4 fails as written: its test clause names a redraw varying `bodyColumns` and `placement`, and the render tests vary only `scroll.offset` and `scroll.bodyRows` (diff-bug #3). The pass's fix-now findings ride with the return (Review section).
- 2026-10-20: tasks T7 (the return's AC4 redraw tests) and T8 (the pass's fix-now batch) added after T6, Coverage updated (AC3 → T2, T8; AC4 → T3, T7); a minor amendment.
- 2026-10-20: T7 done: three render tests per surface redraw the hand-built pane: the line on row 11 (counted by hand), a 60-column pane opening the card above where a 14-column one opens it below (`top` 12), and `inline` cutting the card to `Long row: aaaa bbbb cccc dddd eeee …` where a dock opens it whole. The `mountAt` and `drawn` helpers take `bodyColumns` and `placement`.
- 2026-10-20: T8 done: register.tsx's card comment and the `cardPlaces` comment reworded; the down list takes only lines with the ⓘ glyph (`infos`); DESIGN's two candidate-card sentences fixed; the `isCard` and `flat` comments name the root's down card; the M261 helper renamed `withoutRow`; an AC3 case shows the row after a hidden started row moving up. Verify green: scripts 428 OK, hooks 193 OK, both validates exit 0, mod tests 2387 pass 0 fail.
- 2026-10-20: claim audit: 27 claims read, 2 corrected — register.tsx (the card comment now names the tie, the no-card case, and a cut card drawn at the root) and pane.test.tsx (two test names say no card draws in the terminal); scoped to the return's added lines, `git diff f5df4519..HEAD`.
- 2026-10-20: implement done after review return 1; status review.
- 2026-10-20: review return 2: AC4 fails as written: its test clause names a no-card result, and no redraw asserts one (pass 2 diff-bug #1). Pass 2's fix-now wording items ride with it.
- 2026-10-20: task T9 added for return 2 (a minor amendment), Coverage AC4 → T3, T7, T9.
- 2026-10-20: T9 done: a redraw at `scroll.offset` 10 and `bodyRows` 3 draws no card on either surface, with a control at 200 rows that draws one on the desktop; the inline test's terminal branch checks both draws' lines and roots; DESIGN's card paragraph names where each card sits and that `cardPlaces` reads `bodyColumns`; the `cardPlaces` comment gains its comma. Verify green: scripts 428 OK, hooks 193 OK, both validates exit 0, mod tests 2389 pass 0 fail.
- 2026-10-20: implement done after review return 2; status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->

Pass 1, 2026-10-20, head bb6d0181 (the PR-URL commit); main is an ancestor, so no sync was needed. The run: `claude plugin test .` exit 0, 2380 pass, 0 fail.

- AC1: the "cardPlace picks the side a candidate card opens on (M294 AC1)" table passes 9 of 9: fits above, exactly fits above, fits only below, exactly fits below, neither with more above, neither with more below, a tie (up), the larger side under 3 rows (null), and a larger side of exactly 3 (down, cap 3).
- AC2: the "cardRows estimates the rows a candidate card takes (M294 AC2)" table passes 7 of 7 at 14 columns: an empty text (2), one short word (3), a text that fills a row (3), a row plus a word (4), a word longer than a row (4), repeated spaces (3), and a word that exactly fills the last row (5).
- AC3: the "each candidate line carries the rows drawn before it (M294 AC3)" table passes 8 of 8: the bare idle state (first candidate on row 9), the Next line (11), the release line (10), a blocked row with its counts line (13) and without (12), a hotfix line (12), a workable row and two waiting rows (16), and no line but a candidate carries a row.
- AC4: the "each candidate card is placed from the Pane props (M294 AC4)" table passes 8 of 8, varying `bodyColumns` (14, 60), `scroll.offset` (0, 5, 7, 8), `scroll.bodyRows` (3 to 200), and `placement` (`dock`, `inline`), with up, down, cut (above on a tie, below), and no-card results, plus only candidate lines placed. The register.tsx render calls `cardPlaces` with `e.props.bodyColumns`, `e.props.scroll.offset`, `e.props.scroll.bodyRows`, and `e.props.placement`, and the AC5 render tests below vary `scroll` through the mount props.
- AC5: the "a candidate card is drawn on the side it opens on (M294 AC5)" render tests pass 6 of 6 (3 per surface). On the desktop: an up card in its line at `bottom: 1` with the ⓘ scope and no height; a down card as the last child of `cairn-pane`, unkeyed, `position: 'absolute'`, `top` = its row plus 1, `display: 'none'`, hover `{ display: 'flex', scope: 'cairn-info-candidate-0' }`; a cut card with no `height` or `overflow` and the text `Long row: aaaa bbbb cccc …`. In the terminal, no card. The "cardCut cuts the text of a card by whole words (M294 AC5)" table passes 6 of 6: a cut mid-text, a run whose ` …` would wrap past the rows, a first word that does not fit (`…`), a text that fits whole, repeated and leading spaces, and a word longer than a row that fits once split. Live looks (operator, circumplex): cards open on a side with room, draw over the rows, and open only from ⓘ; the recheck found the cut card with no empty rows.
- AC6: read at the head: README.md:340-345, CHANGELOG.md:124-129 (the Unreleased ⓘ-card entry), cairn/DESIGN.md:520-537, and register.tsx:438-444 and 411-415 each state the three-way rule: above when it fits, else below, else cut to the larger side. `git grep -n -i -e "always open" -e "always upward"` over those files exits 1, with no match.
- AC7: from the repo root, each exit checked: `scripts/tests` 428 OK (21 skipped), `hooks/tests` 193 OK, both `claude plugin validate` runs exit 0, `claude plugin test .` exit 0 with 2380 pass and 0 fail.

Consistency gate: `cairn_validate.py` exit 0, all checks passed; no principle changed, so `cairn_impact` is skipped. Profile slot: the verify checks pass on the review head (AC7); the marketplace validate output holds no `version` warning (0 matches); the unreleased ⓘ-card CHANGELOG entry was edited to state the rule, with no milestone id added.

AC4 unticked: diff-bug #3 shows its evidence line overstated. The render tests vary only `scroll.offset` and `scroll.bodyRows`; no redraw varies `bodyColumns` or `placement`, which AC4's test clause names.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: rows holding Buttons or a 16 px badge may draw taller than one cell, which would shift `rowsAbove` and a down card's `top` — follow-up, into "Check the pane badges in a real session" item (3), which already asks whether a badge makes its row taller.
- diff-bug #2: a desktop wheel scroll might not ask for a new render, leaving a stale offset — reject, false by the live look: the operator hovered rows after scrolling down and the cards opened on a side with room.
- diff-bug #3: AC4's redraw test clause names `bodyColumns` and `placement`, and no redraw varies them — fix now through review return 1 (render tests at a second width and `inline`).
- diff-bug #4: DESIGN's "opens above its row only when it fits there" contradicts the cut-above case — fix now.
- diff-bug #5: `cardBox`'s unscoped hover fallback would light a down card from anywhere in the pane, if one ever drew without `info` — fix now (the down list takes only lines with the ⓘ scope).
- diff-bug #6: a cut card can exceed its cap where the desktop wraps narrower — reject, planned change (amended AC5 states it).
- diff-bug #7: `cardCut` gives `…` alone for a no-space text that does not fit — reject, planned change (AC5's spec).
- diff-bug #8: a line outside the window gets a negative `above` — reject, false: its ⓘ cannot be hovered, so nothing draws wrong.
- diff-bug #9: `cardRows` with under 5 columns or a wide character — reject, planned change (AC2's estimate).
- diff-bug #10: the AC4 inline case uses offset 5, which an inline frame would not show — reject, style (the expected values are right for the input).
- diff-bug #11: awaits — reject, false: `e` belongs to one render and `lines` and `places` come from one `paneLines` call.
- diff-bug #12: the M261 tests strip `rowsAbove` — reject, planned change (blame-history #4 covers the lost check).
- blame-history #1: the down cards in `below.map` carry no keys — reject, false risk: a key would scope hover (M290), and the parked ✎ Box map is the same precedent.
- blame-history #2: the window-relative row picks the side while `top` is in tree rows — reject, false by the live look after scrolling, and `top` is in the tree's coordinates on purpose.
- blame-history #3: register.tsx's comment still says a card is "placed above the row" — fix now.
- blame-history #4: no test checks `rowsAbove` after a hidden started row — fix now (an AC3-style case).
- blame-history #5: hover scope kept — reject, no finding.
- blame-history #6: the M294 block splits the label constants — reject, style.
- prior-review #1: the `cardPlaces` comment's inline clause lacks a verb (PR #264's grammar point) — fix now.
- prior-review #2: register.tsx's "from the end of the pane" clause does not parse — fix now.
- prior-review #3: DESIGN.md:516 "reveals it above the row" — fix now (as ripple #1).
- ripple #1: DESIGN.md:515-516 says a candidate card reveals above the row — fix now.
- ripple #2: register.tsx:407-409 "placed above the row out of the flow" — fix now (as blame-history #3).
- ripple #3: the `isCard` comment says a card is a line's child — fix now.
- ripple #4: the `flat` comment says the root holds only lines — fix now.
- ripple #5: the helper name `unplaced` collides with the pane's "unplaced" term — fix now (renamed).
- ripple #6: DESIGN.md:512-513 "inside such a line's keyed Box" is false for a down card — fix now.

Pass 2, 2026-10-20, head acaaac1c after review return 1; main is an ancestor. `claude plugin test .` exit 0, 2387 pass, 0 fail; the M294 blocks: AC1 9, AC2 7, AC3 9 (the hidden-row case added), AC4 8, AC5 18 (6 cardCut, 6 placement renders, 6 return-1 redraws), all passing. `scripts/tests` 428 OK (21 skipped), `hooks/tests` 193 OK, both `claude plugin validate` runs exit 0 with no `version` warning, `cairn_validate.py` all checks passed. AC1-AC3 and AC5-AC7 hold at this head with those counts.

- AC4: the `cardPlaces` table passes 8 of 8 as in pass 1, and the review-return-1 render tests redraw the pane with varied props on both surfaces, passing 6 of 6: the line on row 11 (counted by hand); at `scroll.offset` 7, `bodyColumns` 60 draws the card in its line at `bottom: 1` and `bodyColumns` 14 draws it at the root at `top: 12`; at offset 6, `placement: 'inline'` cuts the card to `Long row: aaaa bbbb cccc dddd eeee …` where `dock` opens it whole, both at `top: 12`; the terminal draws no card. With the pass 1 render tests varying `scroll.offset` and `scroll.bodyRows`, the redraws vary all four props.

AC4 unticked again: pass 2 diff-bug #1 shows that no redraw asserts the no-card result that AC4's test clause names.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: no redraw asserts a no-card result, which AC4's test clause names — fix now through review return 2 (a redraw too short for any card).
- diff-bug #2: the inline test's terminal branch checks only the root — fix now (it checks both draws' lines and roots).
- diff-bug #3: DESIGN.md:515-516 still says the pointer reveals a card above the row — fix now (the paragraph is rewritten; pass 1's fix added a sentence and left the phrase).
- diff-bug #4: DESIGN's "the one card drawn outside its line" suggests one such card — fix now.
- diff-bug #5: DESIGN's `cardPlaces` sentence leaves out `bodyColumns` — fix now.
- diff-bug #6: the row-11 test checks tree order, not drawn height — reject, already a follow-up (pass 1 diff-bug #1).
- ripple #1: the "Fix cut and odd names on the pane card" row's item (3) describes a cut this merge removes — reject, planned change: post-merge hygiene narrows the row (records-hygiene §1), since the row's started token names M294.
- blame-history #1: `flat` lists a root down card as an entry, so line-wise card checks skip it — reject, false: no fixture there draws a down card, and the AC5 tests read the root's children directly.
- blame-history #2: M286's and M290's facts still stated — reject, no finding.
- blame-history #3: DESIGN.md:515-516's "(below)" reads as the card's side — fix now (as diff-bug #3).
- blame-history #4: DESIGN.md:512-513 gives `bottom: 1` as the only placement — fix now (as diff-bug #3).
- blame-history #5: DESIGN's "opens where it fits" is loose for a cut card — fix now.
- blame-history #6: the `below` filter's reason rests on M290's keyed-scope claim — reject, no finding (M290's probe and DESIGN record it).
- blame-history #7: `withoutRow` rename complete — reject, no finding.
- blame-history #8: the hidden-row test agrees with D-167 — reject, no finding.
- prior-review #1: the `cardPlaces` comment's "Inline the frame fits the tree" still reads as a fragment (PR #264's point) — fix now.
- prior-review #2: as diff-bug #3 — fix now.
- prior-review #3: DESIGN.md:512-513's rule before its exception (pass 1 ripple #6) — fix now (as diff-bug #3).

Pass 3, 2026-10-20, head f153a27b after review return 2; main is an ancestor. Verify as recorded in the T9 line at this head: mod tests 2389 pass, 0 fail.

- AC4: the `cardPlaces` table passes 8 of 8, and the render redraws on both surfaces pass 8 of 8: the line on row 11; at offset 7, 60 columns opens the card above (`bottom: 1`) and 14 columns below (`top: 12`); at offset 6, `inline` cuts it to `Long row: aaaa bbbb cccc dddd eeee …` where `dock` opens it whole; at offset 10 with `bodyRows` 3, no card on either surface, with a 200-row control drawing one on the desktop. The redraws vary `bodyColumns`, `scroll.offset`, `scroll.bodyRows`, and `placement`, and assert up, down, cut, and no-card results.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: DESIGN names `placement` but not what it changes — fix now.
- diff-bug #2: the pass 3 AC7 record cites T9's run — fix now (a fresh run is recorded below).
- diff-bug #3: the no-card redraw covers only the tie — reject, planned change: AC4 names a no-card result, and AC1's table covers the unequal case.
- diff-bug #4: two reflow leftovers in DESIGN's card paragraph — fix now.
- blame-history #1: DESIGN states the placement rule twice, the first time without the no-card case — fix now (one statement).
- blame-history #2: the no-card redraw runs only in a dock — reject, planned change: AC4 names results, not a result per placement.
- prior-review #1: "The cards of other lines still open upward" implies one down card — reject, false: it names the non-candidate lines' cards.
- prior-review #2: "(below)" after the ⓘ group can read as the card's side — fix now.
- ripple: no ripple evidence.

After pass 3's fixes (DESIGN wording only): from the repo root, `scripts/tests` 428 OK (21 skipped), `hooks/tests` 193 OK, both `claude plugin validate` runs exit 0, `claude plugin test .` exit 0 with 2389 pass and 0 fail, `cairn_validate.py` all checks passed. This is AC7's fresh evidence at the pre-merge head.

PR-conversation read (PR #307): one Copilot review (COMMENTED, on bb6d0181), two threads, no other review or comment.
- copilot: cairn/DESIGN.md (the "(below)" after the ⓘ group) — fix now, fixed 0145393f (as pass 2 diff-bug #3 and pass 3 prior-review #2)
- copilot: cairn/milestones/M294-pane-card-placement.md:55 (T3 still names a cut card's `height` and `overflow`) — fix now, fixed in the next commit (a minor task edit naming T5's replacement)
- Copilot level: Lite (set by GitHub's settings). Summary reply posted.
- 2026-10-20 minor task edit: T3's text names that T5 replaced the cut card's `height` and `overflow` (Copilot thread on PR #307).
