# M208: A fuller look for the cairn pane

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M207
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane draws in every adopter's session
- **Branch/PR:** m208-pane-look

## Goal

Give the cairn pane a fuller look, picked by the operator from browser prototypes, on the desktop and in the terminal.

## Scope

**In:** Three additions to the pane's look. Each active milestone's head line gains the band's flow track and its percent: an `Svg` on the desktop and braille cells in the terminal, from `track.ts`. The `Tasks` and `Criteria` headings gain a short meter beside their counts. Section headings are set off from their items by a rule or a mark, and the `Next` line is set off from the queue. The operator picks the form of each from 2 or 3 browser prototypes in a dark and a light block. The pane keeps one line per item, with the goal wrapping (M205). The line Box gains `minWidth: 0`, from "Pane follow-ons (M205 review)". README, DESIGN, CHANGELOG, and the header comments of `pane.ts` and `register.tsx` follow.

**Out:** The fixed phase colors in light, colorblind, and ANSI themes stay in "Band label colors in other themes". The other "Pane follow-ons (M205 review)" items stay there. Clickable actions stay in "Status mod follow-ons". Pane widths under 44 columns are not swept.

## Acceptance criteria

- [ ] AC1: The head line of each active milestone draws the flow track and percent that the band draws for the same row: an `Svg` on the desktop surface and braille cells on the terminal surface. A head line of a milestone with no readable file draws no track and keeps `no milestone file`. `pane.test.tsx` cases assert this on both surfaces for an `in-progress` row, a `review` row whose criteria hold a box inside an HTML comment, and a row with no file.
- [ ] AC2: The `Tasks` and `Criteria` headings each draw a meter beside their `checked/total` count, in the form the operator picked at T1. `pane.test.tsx` cases assert the meter for a partly checked, an all-checked, and an all-open section on both surfaces. If the operator picks no meter at T1, the headings draw none, and a case asserts that.
- [ ] AC3: Each section heading (`Goal`, `Tasks`, `Criteria`, `Work log`, `Workable`, `Waiting`, `Candidates`) and the `Next` line draw in the set-off form the operator picked at T1. `pane.test.tsx` cases assert the form for each of these headings and the `Next` line on both surfaces. If the operator picks no set-off form at T1, they draw as before, and a case asserts that.
- [ ] AC4: Over the `pane-full` fixture and an idle fixture with candidate rows, at each `bodyColumns` width from 44 to 120, each line's indent plus lead width is at most `bodyColumns`. Each line Box carries `minWidth: 0`. A `pane.test.tsx` sweep asserts both on both surfaces.
- [ ] AC5: README's "The cairn pane" section, the pane paragraph of `cairn/DESIGN.md`, and the header comments of `pane.ts` and `register.tsx` describe the new look. CHANGELOG's Unreleased section has an entry for it.
- [ ] AC6: The four commands of the verify slot in `cairn/PROFILE.md` each exit 0.
- [ ] AC7: At a live look the operator accepts the desktop pane docked at 44 columns and at a wider dock, and the terminal pane.

## Coverage

- AC1 → T2
- AC2 → T1, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T5
- AC6 → T2, T3, T4, T5
- AC7 → T1, T6

## Tasks

- [ ] T1: Build 2 or 3 browser-pane prototypes of the pane with all three additions, each in a dark and a light block, served with `python3 -m http.server` from the scratchpad (LESSONS M201, M204). The operator picks the meter and the set-off form. A work-log line records the picks.
- [ ] T2: Draw the flow track and percent on each head line, reusing `flowOf`, `trackSvg`, and `brailleSpans`. The track width follows the pane's `bodyColumns`. Add the AC1 cases.
- [ ] T3: Draw the meters and the set-off headings and `Next` line in the picked forms. Add the AC2 and AC3 cases.
- [ ] T4: Give the line Box `minWidth: 0`. Add the AC4 sweep.
- [ ] T5: Update README, the DESIGN pane paragraph, the CHANGELOG, and the header comments of `pane.ts` and `register.tsx`.
- [ ] T6: Do the live look in a new Code session (LESSONS M195), docked at 44 columns, at a wider dock, and in the terminal.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: collision sweep: the `minWidth: 0` item of "Pane follow-ons (M205 review)" is absorbed, and hygiene trims it from the row. Its other items stay. No D-entry conflicts (D-143 read). Inbox: 0 open issues, 0 open PRs.
- 2026-10-04: criteria audit (full mode, user-facing tier, fresh Opus reader) returned 12 findings over M207 to M209, all taken. Here: AC1 draws the band's own track and percent, with a review-row case whose comment box makes the two counts differ. AC4's sweep starts at the 44-column dock, since a head line with a track needs about 32 columns before its title. AC4 binds lead widths and `minWidth: 0` and leaves the drawing to AC7. AC2 and AC3 cover a pick of none.
- 2026-10-04: question set: additions. The operator chose all three: the flow track on each milestone, meters by the counts, and set-off headings with the `Next` line. Falsified if the live look shows the pane too busy to read.
- 2026-10-04: question set: look pick. The run stops once at T1 for the operator to pick from browser prototypes (recommended), over the agent picking and showing the look only at the merge. The T1 pick and the T6 live look are stops for the operator's eyes on the closed list.
- 2026-10-04: implement started on branch `m208-pane-look`. The untracked `tsconfig.json` stays unstaged.
- 2026-10-04: T1 prototypes served from the scratchpad on port 8765: three variants (square meters with solid rules; thin bars with accent marks; braille meters with dotted leaders), each in desktop dark and light at 44 columns, terminal dark, and an idle pane with candidates. The real `trackSvg` and `brailleSpans` output is drawn there. At 44 columns the track on the head line left the title no room, so the page also compares the track on its own line under the head line. Stopping for the operator's pick.
- 2026-10-04: T1 pick: the percent alone at the end of the head line, with no track bar (the operator's own answer, over the track on its own line and over the planned track on the head line). Meter: variant 1's eight squares. Headings: variant 2's blank row, orange `▎` accent, and gray uppercase label, with the Next command in an orange pill.
- 2026-10-04: re-audit: AC1 (full) — of the percent-only wording: no fixture row makes the band's percent differ from the pane's in the phase that sets it, and a long title at 44 columns could cut the percent; Scope, T2, and the AC4 work-log reason still name the track.
- 2026-10-04: re-audit: AC1 (full) — of the fixed wording: the review-row probe passes vacuously with no checked box outside the comment, the "outside the truncate-end element" case names no single element, the "left whole" claim is the live look's to show, and AC4 measures the lead and not the tail. This is the second re-audit line on AC1, so the wording goes to the operator.

## Decisions

## Review
