<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M289: The cairn pane draws each section count as a colored badge

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane is part of the plugin that users install
- **Branch/PR:** m289-pane-count-badges https://github.com/jmgirard/cairn/pull/301   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The cairn pane's Blocked, Hotfixes, and Candidates headings show their count
as a filled rounded badge in the section's color in place of a bare gray
number.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a badge for the count at the right end of the Blocked, Hotfixes,
and Candidates headings: on the desktop an `Svg` pill with the number, in a
fixed fill per heading (Blocked amber, Hotfixes orange, Candidates plan
blue); in the terminal the number padded with a space on each side on that
heading's theme color. A `badgeSvg` builder, a per-heading color table, the
register.tsx change that draws a badge in a pane line's tail, tests, and
the README, DESIGN, CHANGELOG, and header-comment text.

**Out:** the Tasks and Criteria fraction and meter, and the summary card's
numbers, stay as they are (the user's choice at the question set; no row
filed, since nothing was deferred). A live look in a new Code session is
not part of this milestone (the user's choice); the browser screenshots of
AC5 stand in for it.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: On the desktop surface, the Blocked, Hotfixes, and Candidates
      headings each draw their count as one `Svg` badge in the heading's
      tail, a rounded rectangle holding the number, and draw no count text;
      tests assert, for each of the three headings, the badge element, the
      number it holds, and its fill color as `BADGE_FILL` names it for that
      heading, and that the three fills differ from each other.
- [x] AC2: In the terminal, each of those three headings draws its count as
      one text span, the number with one space on each side, in
      `inverseText` on the theme key that `BADGE_KEY` names for that heading
      as background; each `BADGE_FILL` hex is the fixed value near its
      heading's `BADGE_KEY` color, as `ICON_COLORS` does for the icons; a
      test per heading asserts the span's text, color, and backgroundColor.
- [x] AC3: A badge's width grows with its number's digits: a test asserts
      that `badgeSvg` widths strictly increase for 9, 10, and 100, that each
      SVG's text is the number, and that the text's `textLength` is the
      badge width less its padding, as the band pill's is (track.ts).
- [x] AC4: The existing `pane.test.tsx` cases for the Tasks and Criteria
      heading tails and for the summary card pass with no change to their
      expected values, and the profile's `verify` slot passes.
- [x] AC5: Rendered in the browser pane on a dark and on a light page
      ground, the `badgeSvg` images for 7 and 100 in each of the three
      headings' fills show a rounded pill whose number is legible, in the
      text color `BADGE_FILL` gives that fill; the evidence is the two
      screenshots taken at review.
- [x] AC6: `grep -n "bare count\|count in gray"` over README.md,
      cairn/DESIGN.md, `hooks/status/pane.ts`, and
      `hooks/status/register.tsx` returns nothing; `grep -n badge` returns
      at least one line in each of README.md, cairn/DESIGN.md, the new
      CHANGELOG.md entry, `pane.ts`, and `register.tsx`; any remaining
      "count at the right end" line in README.md or cairn/DESIGN.md names
      the badge or only the Tasks and Criteria headings. Released CHANGELOG
      entries stay unchanged.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T2, T3
- AC2 → T1, T2, T3
- AC3 → T2
- AC4 → T3, T5
- AC5 → T1, T5
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Set the colors. Read the theme keys near amber, orange, and plan
      blue (`warning`, `claude`, `planMode`; `FLOW_COLORS` in band.ts:132,
      `ICON_COLORS` in icons.ts). Pick each fill's hex and its text color
      for legibility on both themes, serving a scratch page from the
      scratchpad with `python3 -m http.server` (LESSONS M201).
- [x] T2: Tests first, then `BADGE_KEY`, `BADGE_FILL`, and `badgeSvg(count,
      heading)` (icons.ts or a new badge module): a rounded rect with
      `rx` half its height and the number as text, with `textLength` set as
      in track.ts:195-198. Give `Span` a badge field, or a separate tail
      field, and have `countHeading` (pane.ts:455) emit it with no gray
      count text.
- [x] T3: register.tsx draws a pane line's tail through the span drawer,
      with a badge span as `<Svg>` on the desktop and as padded
      `inverseText`-on-key text in the terminal (the pane's tail draws as
      plain `<Text>` today). Update the Blocked, Hotfixes, and Candidates
      heading tests (pane.test.tsx:959 and the `headText(…, '15')` cases)
      and add the desktop and terminal draw tests.
- [x] T4: Docs: README.md (near line 330), cairn/DESIGN.md (near line 558),
      a new CHANGELOG.md Unreleased entry, and the `pane.ts` and
      `register.tsx` header comments describe the badge; run AC6's greps.
- [x] T5: Run the profile's `verify` slot from the repo root and check each
      exit code. Render the three badges in the browser pane on a dark and a
      light ground for AC5.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-19: created by /milestone-plan.
- 2026-10-19: tier check: milestone — a change to the pane's drawing, a runtime surface, with a look to choose.
- 2026-10-19: question set: badge look — filled colored pill (Blocked amber, Hotfixes orange, Candidates plan blue).
- 2026-10-19: question set: which counts — the Blocked, Hotfixes, and Candidates heading counts only.
- 2026-10-19: question set: live look before review — declined; AC5's browser screenshots stand in.
- 2026-10-19: plan gate chose an `Svg` pill on the desktop over a text span with a background color because a text background draws square corners and the band's track pill is already an `Svg`; falsified by the desktop drawing a rounded text background or the `Svg` badge failing to align in the heading row.
- 2026-10-19: collision sweep: no ROADMAP row, archive summary, or D-entry covers heading badges; M208 drew a pill for the Next command, which M286 removed for that line only. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-19: criteria audit (full mode, Opus): 6 findings, all taken. AC1 narrowed to the desktop surface and requires the three fills to differ. AC2 names `BADGE_KEY`. AC3 drops "no digit is clipped" for a `textLength` check. AC4 names the Tasks, Criteria, and card cases. AC5 drops its reference to AC1's test clauses. AC6's greps check both that the old wording is gone and that badge wording is present.
- 2026-10-19: AC5 re-audited after the live look was declined: reworded to "the text color `BADGE_FILL` gives that fill" and to name the numbers 7 and 100. The reader measured white on amber #d9a21b at about 2.3:1, below the 3:1 floor, and the `ink` gray (#1f1f1e) at 5.2:1 or more on all three fills, so T1 starts from one dark text color.
- 2026-10-19: T1: kept the white number the user picked and darkened the fills instead: the band pill's plan blue rgb(71,103,158) and implement orange rgb(152,85,57) (track.ts `PHASE_FILLS`), and a dark amber rgb(146,103,22) near `warning`. White on each measured 5.0:1 or more (WCAG ratio, computed in a scratch script). Terminal keys: `warning`, `claude`, `planMode`.
- 2026-10-19: T2, T3: new `hooks/status/badge.ts` (`BADGE_KEY`, `BADGE_FILL`, `badgeWidth`, `badgeSvg`, `badgeSpan`); `Span` gains `badge`; `countHeading` takes the badge name; register.tsx draws a pane tail through `drawSpan` and centers a row with a badge. Six existing heading tests now expect the badge; four new tests. Planted defects (a shared fill, a fixed width, a wrong text key) turned 6 tests red; restored. Mod tests 2281 → 2285, all five verify checks green.
- 2026-10-19: T4: README, DESIGN, a new CHANGELOG Unreleased entry, and the pane.ts comments describe the badge; AC6's greps: no old phrase, `badge` in all five, no "count at the right end" line left. The simple-english hook flagged README (231) and CHANGELOG (381) counts that predate this branch; the README count did not change with the new lines, and they were left.
- 2026-10-19: T5: all five verify checks green (mod tests 2285 pass). A scratch page built by node from the repo's `badge.ts` drew 7 and 100 in all three fills on a dark and a light ground in the browser pane; each number read clearly.
- 2026-10-19: claim audit: 33 claims read, 2 corrected — hooks/status/badge.ts (a one-digit badge is a 19×16 short pill, not a circle, and the dead `Math.max` floor went; the terminal badge shares the band pill's colors but is not bold). Re-read once: both true. Mod tests 2285 pass after the width change.
- 2026-10-19: implement done; status review.
- 2026-10-19: step-7 approval: m289-pane-count-badges approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Pass 1 (2026-10-19), on f608584d, synced with main (0 behind). PR #301 opened at review start (Copilot arm); Copilot requested, state `pending`.

- AC1: `claude plugin test .` 2285 pass, 0 fail; "desktop: each count is one Svg pill holding the number, in its own fill" passes: for each of the three headings, one `Svg` in the tail with the number as alt and `>N</text>` in its source, the plan's fill per heading, no other tail text than the space, and three distinct fills (Blocked 7, Hotfixes 1).
- AC2: "terminal: each count is one span, the padded number in inverseText on the heading key" passes for all three headings (no `Svg` drawn; ` 7 ` and ` 1 ` read back); `BADGE_KEY` is `warning`, `claude`, `planMode`. Read in badge.ts: the Hotfixes and Candidates fills equal track.ts `PHASE_FILLS` implement and plan, the band pill's fills for the `claude` and `planMode` phases, and Blocked's rgb(146,103,22) is a dark amber for `warning`, each a fixed value beside its key as `ICON_COLORS` is.
- AC3: "widths strictly increase for 9, 10, and 100, and each text is its number" and "the text length is the width less the padding, and the Svg width matches" pass (widths 19, 26, 33).
- AC4: `git diff main...HEAD -- hooks/status/pane.test.tsx` removes 10 lines, all on the Blocked, Hotfixes, or Candidates heading counts; none names Tasks, Criteria, or the card, so those cases' expected values are unchanged, and they pass. Verify slot: scripts/tests 428 OK (21 skipped), hooks/tests OK, both `claude plugin validate` exit 0, `claude plugin test .` 2285 pass 0 fail.
- AC5: a scratch page built by node from the branch's `badge.ts` drew `badgeSvg` for 7 and 100 in all three fills on a dark (#262624) and a light (#faf9f5) ground; two browser-pane screenshots (dark half, light half) show rounded pills with each number legible in white, the text color `BADGE_FILL` gives every fill.
- AC6: `grep -n "bare count\|count in gray"` over README.md, cairn/DESIGN.md, pane.ts, register.tsx: no match (exit 1). `grep -c badge`: README 2, DESIGN 2, pane.ts 6, register.tsx 7, and 3 added CHANGELOG lines in the new Unreleased entry. `grep -c "count at the right end"` in README and DESIGN: 0. The CHANGELOG diff removes no line, so released entries are unchanged.
- Gate: `cairn_validate` all checks passed; no principle changed, so `cairn_impact` was skipped; the consistency-gate slot's checks: verify green on the review head (AC4 line), the marketplace validate prints no `version` warning, and CHANGELOG has an Unreleased entry for the badge with no milestone ids. The repo has no CI.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the terminal badge's `inverseText` on `warning` is a pairing the band never draws, unchecked on light themes — follow-up, row "Badge look checks"
- diff-bug #2: `textLength` stretched a one-digit count about 10–15% (7 px for a 6 px digit) — fix now: `BADGE_DIGIT` 7 → 6 (widths 18, 24, 30), fixed 94dabc61
- diff-bug #3: the 16 px badge may make its heading row taller than the 14 px icon rows; unchecked in the pane — follow-up, row "Badge look checks"
- diff-bug #4: tail children have no keys — reject, false as a defect: the old tail map had none either, and a Text drops its key
- diff-bug #5: the terminal tail grows two columns — reject, false as a defect: it fits a 44-column dock
- diff-bug #6: band.ts and badge.ts import types from each other — reject, false as a defect: type-only imports are erased
- diff-bug #7: badge.ts said the terminal badge has "the colors of the band's terminal pill", but `warning` is never a band pill ground — fix now: the comment names the shared text key only, fixed 94dabc61
- blame-history #1: track.ts:44 says its palette holds "the only raw colors the mod draws", stale since icons.ts and now badge.ts — fix now: the comment names both, fixed 94dabc61
- blame-history #2: amber Blocked and orange Hotfixes differ mostly by hue — follow-up, row "Badge look checks"
- blame-history #3: `warning` as the Blocked ground can read as a problem — reject, planned change: the user picked amber for Blocked at the question set
- blame-history #4: pane.ts said the badge is "in the heading's color", but the desktop fill is fixed — fix now: the comments say theme key in the terminal, a fixed fill near it on the desktop, fixed 94dabc61
- blame-history #5: the CHANGELOG entry sits under "Changes that affect existing repos" — reject, false: M286's pane look entry sits there, and the look changes in every adopted repo on update
- prior-review #1: the terminal badge's theme pairings are unchecked, as M204's review left the pill's — follow-up, row "Badge look checks"
- prior-review #2: no test computes the badge fills' contrast, as M217's does for the band pill — fix now: "each badge number reads on its fill at 4.5:1 or more" (a planted pale fill turned it red), fixed 94dabc61
- prior-review #3: font-weight 650 on the desktop number, against M208's pill-bold fix — reject, false: the band's own desktop pill label is `font-weight="650"` (track.ts:199)
- prior-review #4: a desktop surface with no `Svg` falls back to a Text with a background — reject, planned change: the same fallback the icons take (M286)
- prior-review #5: the fixed desktop fills follow M217's image palette — reject, no defect reported
- ripple #1: register.tsx:393 says a line with a lead icon centers its row, not a badge — reject, false: the comment added above `drawSpan` says a heading with a badge centers its row too
- ripple aside: "track.ts `PILL_TEXT` does not exist" — reject, false: `export const PILL_TEXT = 'inverseText'` is track.ts:214
- After the fixes: verify green (mod tests 2286 pass, 0 fail); AC3's tests pass at widths 18, 24, 30; AC5 re-rendered at the new widths on both grounds, every number legible.
- conversation: PR #301 has no unresolved thread, no conversation comment before the summary reply, and one review, Copilot's (COMMENTED on f608584d, "No open issues") — noted.
- copilot: review body — no threads or body items; summary reply posted (issuecomment-6275110645).
- Copilot level: Lite (set by GitHub's settings). The state query printed `unknown` for the level, the format change the "Copilot level line format" row records; the level is read from the body's `<sub>Review effort: Lite</sub>`. The review covered f608584d; 76cd776f and 94dabc61 came after it.
