# M302: Put the pane's count badges after their labels in gray

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane's headings are what operators read
- **Branch/PR:** m302-pane-badge-after-label https://github.com/jmgirard/cairn/pull/316

## Goal

The cairn pane's Blocked, Hotfixes, and Candidates headings draw their count badge right after the label, with one space, in one gray for all three headings.

## Scope

**In:** `hooks/status/badge.ts` takes one desktop fill, `rgb(110,110,110)` with a white number, and one terminal key, `inverseText` on `inactive`, for all three headings. The heading layout in `hooks/status/pane.ts` puts the badge in the line's lead after the label and a space. `hooks/status/register.tsx` centers a row whose lead holds a badge. The unreleased CHANGELOG entry for the badges (M289), the README's pane section, the DESIGN.md status mod bullets, the badge Known issue, and the comments in `hooks/status/` describe the new look. A live look checks the desktop pane.

**Out:** the Tasks and Criteria headings keep their counts and meter at the right end (the user's choice at the question set). The summary card's counts do not change. The terminal badge's look in light themes stays unchecked and stays in the badge Known issue, because the live look covers the desktop app only. The desktop look waits until after the merge, when the idle pane in this repo draws the Candidates heading, because no badge heading draws here while M302 is active (the user's choice at the T4 stop). A poor look then becomes a `/hotfix`.

## Acceptance criteria

- [ ] AC1: The Blocked, Hotfixes, and Candidates headings each draw their count badge right after the bold label, with one space between them, and nothing at the row's right end. The pane's line builder (`paneLines` in `pane.ts`, imported as `layout` in `pane.test.tsx`) gives each of these heading lines a `lead` of the label, a one-space span, and the badge span, and no `tail`. A `pane.test.tsx` test asserts this for each of the three headings.
- [ ] AC2: The three badges share one gray. On the desktop each is a rounded pill in the fill `rgb(110,110,110)` with a white number: `badgeSvg` gives that fill and that number color for each of the three headings, and a `pane.test.tsx` test computes the number's contrast on the fill at 4.5:1 or more by the WCAG 2.2 relative-luminance formula (wcag22). In the terminal each is the count with a space on each side, in `inverseText` on the `inactive` theme key, which a `pane.test.tsx` test asserts for each heading.
- [ ] AC3: On the desktop a heading row that holds a badge centers its row, as it did with the badge in the tail. A `pane.test.tsx` mount of the Pane on a surface with `Svg` finds `alignItems: 'center'` on the line Box and on the lead Box of each of the three headings.
- [ ] AC4: The Tasks and Criteria headings keep their counts and meter at the right end. `paneLines` gives the `tasks-head` and `criteria-head` lines the count and the meter in `tail`, and a `pane.test.tsx` test asserts this for both lines.
- [ ] AC5: A browser page draws the shipped `badgeSvg` output, imported from `hooks/status/badge.ts`, for counts 1, 12, and 123, beside a bold label on a dark and a light ground, and the operator accepts the pill's look. The look does not check the pane's placement, centering, or clipping. The badge Known issue names these as unchecked until a desktop look after the merge.
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

- [x] T1: Badge colors. In `hooks/status/badge.ts`, replace the per-heading `BADGE_FILL` and `BADGE_KEY` with one fill and one terminal key. Drop `BadgeName` from `Span.badge` (`band.ts`) and from `countHeading` if nothing else reads it, and update `types/index.d.ts` if it carries the type. Update the M289 tests in `pane.test.tsx` (about lines 282-300 and 3418-3510) to the one fill and key, and add the AC2 tests.
- [x] T2: Badge place. In `pane.ts`, give `countHeading` a lead of the label, a `' '` span, and the badge span, with the empty growing text and no tail. In `register.tsx`, make `centers` also read a badge in the lead. Add the AC1, AC3, and AC4 tests. Update the `pane.ts` and `register.tsx` comments on the heading and the badge.
- [x] T3: Docs. Edit the CHANGELOG Unreleased badge entry, the README pane section (about line 350), the DESIGN.md status mod history bullet (line 82) and cairn pane part (about line 625), and the badge Known issue (about line 1162): drop the amber and orange hue clause, name `inactive` as the terminal ground, and keep the light-theme terminal look and the row height as unchecked. Run the AC6 sweep.
- [x] T4: Browser preview of the shipped `badgeSvg` for counts 1, 12, and 123 beside a bold label, dark and light ground (AC5). Name the unchecked desktop looks in the badge Known issue.

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
- 2026-10-20: implement started on branch m302-pane-badge-after-label. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-20: T1 done. `badge.ts` has one `BADGE_FILL` (`rgb(110,110,110)`, white number) and `BADGE_KEY = 'inactive'`. `BadgeName` is gone, so `badgeSvg`, `badgeSpan`, `countHeading`, and `Span.badge` take the count only, and `types/index.d.ts` never carried the type. The M289 tests now assert the one fill, the white number, the 4.5:1 contrast, and the `inactive` key. Mod tests 2415 pass. Verify green.
- 2026-10-20: T2 done. `countHeading` puts the label, a space, and the badge in the lead, with no tail. `register.tsx` `centers` reads a badge or icon in the lead or tail. New tests: all three headings' leads from one `layout` call with no active milestone (AC1), the mounted lead's Text, Text, Svg and `alignItems` on the line and lead Boxes (AC3), the Criteria tail (AC4). A planted defect (the old lead-icons-only `centers`) failed the AC3 test with `undefined` for `center`. Mod tests 2417 pass. Verify green.
- 2026-10-20: T3 done. The CHANGELOG Unreleased badge entry, the README pane section, the DESIGN.md status mod bullet and cairn pane part, and the badge Known issue (narrowed: the hue clause is gone, `inactive` named) describe the gray badge after the label. The AC6 sweep read each `badge` hit with its block. No block names a per-heading color or a badge at the right end. The CHANGELOG entry dropped a "before" sentence, because M286's right-end gray number never shipped in a release. The simple-english lint hook flags the whole CHANGELOG and README, and nearly all of its hits are in text this milestone did not write. Only the edited sentences were kept within its limits.
- 2026-10-20: T4 stop: no badge heading draws in this repo while M302 is active (no blocked rows, no open hotfix PRs, and Candidates only when idle). The user chose a browser preview now and the desktop look after the merge, over a throwaway hotfix PR or no look.
- 2026-10-20: substantive amendment: AC5 changed from a desktop live look to a browser preview of the pill for counts 1, 12, and 123, with the desktop placement, centering, and clipping named as unchecked in the badge Known issue. Scope Out and T4 follow.
- 2026-10-20: re-audit: AC5 (full) — 4 findings, all taken: vary the count, not the heading, since `badgeSvg` takes no heading; bind the pill's look, not the page's placement; give the deferred desktop look a durable home in the Known issue. Reachability and proportionality had no findings.
- 2026-10-20: T4 done. A scratch page built by `node` from the shipped `badgeSvg` drew the gray pill for counts 1, 12, and 123 after bold labels on a dark (#1f1f1e) and a light (#faf9f5) ground in the browser pane. The operator accepted the look. The badge Known issue names the desktop placement, centering, and clipping as unchecked until a look after the merge.
- 2026-10-20: claim audit: 39 claims read, 0 corrected — CHANGELOG.md, README.md, hooks/status/badge.ts, band.ts, pane.ts, register.tsx, pane.test.tsx. Two unclear wordings were reworded: the badge.ts "not bold" clause and the AC1 test comment on why no milestone is active.
- 2026-10-20: implement done. All four tasks are checked, verify is green (mod tests 2417 pass), and the status is review.

## Decisions

## Review
