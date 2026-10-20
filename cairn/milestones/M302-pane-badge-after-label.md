# M302: Put the pane's count badges after their labels in gray

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane's headings are what operators read
- **Branch/PR:** —

## Goal

The cairn pane's Blocked, Hotfixes, and Candidates headings draw their count badge right after the label, with one space, in one gray for all three headings.

## Scope

**In:** `hooks/status/badge.ts` takes one desktop fill, `rgb(110,110,110)` with a white number, and one terminal key, `inverseText` on `inactive`, for all three headings. The heading layout in `hooks/status/pane.ts` puts the badge in the line's lead after the label and a space. `hooks/status/register.tsx` centers a row whose lead holds a badge. The unreleased CHANGELOG entry for the badges (M289), the README's pane section, the DESIGN.md status mod bullets, the badge Known issue, and the comments in `hooks/status/` describe the new look. A live look checks the desktop pane.

**Out:** the Tasks and Criteria headings keep their counts and meter at the right end (the user's choice at the question set). The summary card's counts do not change. The terminal badge's look in light themes stays unchecked and stays in the badge Known issue, because the live look covers the desktop app only.

## Acceptance criteria

- [ ] AC1: The Blocked, Hotfixes, and Candidates headings each draw their count badge right after the bold label, with one space between them, and nothing at the row's right end. The pane's line builder (`paneLines` in `pane.ts`, imported as `layout` in `pane.test.tsx`) gives each of these heading lines a `lead` of the label, a one-space span, and the badge span, and no `tail`. A `pane.test.tsx` test asserts this for each of the three headings.
- [ ] AC2: The three badges share one gray. On the desktop each is a rounded pill in the fill `rgb(110,110,110)` with a white number: `badgeSvg` gives that fill and that number color for each of the three headings, and a `pane.test.tsx` test computes the number's contrast on the fill at 4.5:1 or more by the WCAG 2.2 relative-luminance formula (wcag22). In the terminal each is the count with a space on each side, in `inverseText` on the `inactive` theme key, which a `pane.test.tsx` test asserts for each heading.
- [ ] AC3: On the desktop a heading row that holds a badge centers its row, as it did with the badge in the tail. A `pane.test.tsx` mount of the Pane on a surface with `Svg` finds `alignItems: 'center'` on the line Box and on the lead Box of each of the three headings.
- [ ] AC4: The Tasks and Criteria headings keep their counts and meter at the right end. `paneLines` gives the `tasks-head` and `criteria-head` lines the count and the meter in `tail`, and a `pane.test.tsx` test asserts this for both lines.
- [ ] AC5: A live look runs in a new desktop Code session on this repo, in a dark and a light theme. Each of the three headings that the repo's state draws shows its badge right after its label in the gray pill, and the operator accepts the look. The work log names each heading that the look did not see.
- [ ] AC6: The docs describe the badge after the label in one gray. The procedure is `git grep -n -i badge -- README.md CHANGELOG.md cairn/DESIGN.md hooks/status`, and each hit is read with its whole comment block or paragraph. No such block outside the CHANGELOG's released sections names a per-heading badge color or puts a badge at the right end. Text that puts only the Tasks and Criteria counts at the right end passes.
- [ ] AC7: The five `verify` commands in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T2
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T4
- AC6 → T3
- AC7 → T1, T2, T3

## Tasks

- [ ] T1: Badge colors. In `hooks/status/badge.ts`, replace the per-heading `BADGE_FILL` and `BADGE_KEY` with one fill and one terminal key. Drop `BadgeName` from `Span.badge` (`band.ts`) and from `countHeading` if nothing else reads it, and update `types/index.d.ts` if it carries the type. Update the M289 tests in `pane.test.tsx` (about lines 282-300 and 3418-3510) to the one fill and key, and add the AC2 tests.
- [ ] T2: Badge place. In `pane.ts`, give `countHeading` a lead of the label, a `' '` span, and the badge span, with the empty growing text and no tail. In `register.tsx`, make `centers` also read a badge in the lead. Add the AC1, AC3, and AC4 tests. Update the `pane.ts` and `register.tsx` comments on the heading and the badge.
- [ ] T3: Docs. Edit the CHANGELOG Unreleased badge entry, the README pane section (about line 350), the DESIGN.md status mod history bullet (line 82) and cairn pane part (about line 625), and the badge Known issue (about line 1162): drop the amber and orange hue clause, name `inactive` as the terminal ground, and keep the light-theme terminal look and the row height as unchecked. Run the AC6 sweep.
- [ ] T4: Live look in a new desktop Code session on this repo, dark and light theme (AC5). Record what the look saw.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — a small change to running code (the pane's heading layout and colors), not a bug.
- 2026-10-20: collision check: extends M289 (done, archived), which added the badges. No D-entry covers badges. The DESIGN.md badge Known issue (M289, M294) is narrowed by T3. No candidate row overlaps.
- 2026-10-20: inbox sweep: no open issues and no open PRs.
- 2026-10-20: lessons harvested: drawing needs a live look in a new Code session (M193 line), and Node imports `badge.ts` directly for a browser preview (M289 line).
- 2026-10-20: criteria audit (full mode, Opus reader): 6 findings, all taken toward the narrower promise. AC1 names `layout` and no `tail`. The Tasks and Criteria criterion asserts the two lines' tails, not test history. The live look checks only the headings the repo draws. The docs sweep reads whole blocks and allows Tasks and Criteria text at the right end. The terminal light-theme look stays in the Known issue. The color, terminal, and centering criteria and proportionality had no findings.
- 2026-10-20: plan merged the desktop and terminal color criteria into AC2 to clear the more-than-7-criteria split warning; the promises are unchanged.
- 2026-10-20: question set: where the Tasks and Criteria counts go — keep at the right end.
- 2026-10-20: question set: the gray look — a mid gray pill, `rgb(110,110,110)`, with a white number.
- 2026-10-20: question set: a live look at implement time — granted, in a new Code session on this repo.
- 2026-10-20: plan gate chose a mid gray pill over a plain gray number with no pill because the user picked it; falsified by a live look where the pill reads poorly on one theme.
- 2026-10-20: plan chose to put the badge in the line's lead over keeping it in the tail with a non-growing text, because the lead already draws spans through `drawSpan` and keeps its width; falsified by the lead Box clipping or misaligning the badge at the live look.
- 2026-10-20: changelog: T3 edits the unreleased M289 badge entry and adds no new entry, since the badges have not shipped in a release.

## Decisions

## Review
