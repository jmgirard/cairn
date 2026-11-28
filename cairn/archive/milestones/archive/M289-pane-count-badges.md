# M289: The cairn pane draws each section count as a colored badge

**Status:** done (2026-10-19, PR #301 https://github.com/jmgirard/cairn/pull/301)

**Goal:** The cairn pane's Blocked, Hotfixes, and Candidates headings show their count as a filled rounded badge in the section's color in place of a bare gray number.

**Outcome:** New `hooks/status/badge.ts`: `BADGE_KEY` (terminal grounds `warning`, `claude`, `planMode`), `BADGE_FILL` (fixed desktop fills rgb(146,103,22) amber, rgb(152,85,57) orange and rgb(71,103,158) blue, the last two track.ts `PHASE_FILLS`, each with a white number at 5.0:1 or more), `badgeWidth` (6 px a digit plus 12, height 16), `badgeSvg` (a rounded rect and the number with `textLength`), and `badgeSpan`. `Span` gains `badge`. `countHeading` takes the badge name. register.tsx draws a pane line's tail through `drawSpan`, so a badge span draws as an `Svg` on the desktop and as ` N ` in `inverseText` on its key in the terminal, and a row with a badge centers. Tasks and Criteria counts and the card are unchanged (the user's choice at the question set). The user declined a live look, so AC5 was browser screenshots on dark and light grounds. README, DESIGN, CHANGELOG, and the pane.ts and track.ts comments describe it. Mod tests went from 2281 to 2286.

**Decisions:** none promoted. Question set: filled colored pill, section counts only, no live look. T1 kept the white number and darkened the fills, since white on the theme-like amber measured about 2.3:1.

**Review:** Four lenses and Copilot (Lite, no open issues; summary answered). 19 findings: 5 fixed (a one-digit count stretched by `textLength`, a badge contrast test, three stale comments), 4 to the new parked row "Badge look checks" (terminal theme pairings, amber against orange for colorblind eyes, row height), 10 rejected as false or planned. Claim audit: 33 claims, 2 corrected. Criteria audit: 6 findings at plan, all taken; AC5 re-audited after the live look was declined. No lessons added.
