# M206: A simpler band: id, title, and the track

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the band draws in every adopter's session
- **Branch/PR:** m206-simpler-band

## Goal

Make the band's row the milestone id and title on the left and the flow track on the right, on every surface and at every width.

## Scope

**In:** A milestone row's left group becomes the bold id and the title. The phase or skill label, the `→`, the chapter, and the next open item go. The flow track is the only progress form. On the desktop, a row too narrow for the 360-pixel track draws a shorter image track. When the pill is tight, it shows only its count. The terminal draws a track of `█` cells in three segments with the count after it. This takes in the "Terminal flow track" candidate row. The ten-cell bar and the counts-only forms are deleted. The skill row goes, so a running cairn skill with no active milestone changes nothing the band draws. The idle row drops its `next` label. The chapter-tool hook and the step's chapter go. A row with no milestone file keeps its warning label. README, DESIGN, CHANGELOG, and the mod's header comments follow.

**Out:** A pressable button that runs the next command stays in "Status mod follow-ons". The pane is unchanged, so its items stay in "Pane follow-ons (M205 review)". The track's colors in light, colorblind, and ANSI themes stay in "Desktop track follow-ons (M204 review)" and "Band label colors in other themes". The track's column-to-pixel estimate also stays in "Desktop track follow-ons".

## Acceptance criteria

- [ ] AC1: On the terminal and desktop surfaces, a milestone row's left group is the bold id, one space, and the milestone's title. It has no phase or skill label, no `→`, and no chapter or open-item text. A row whose counts cannot be read keeps its `no milestone file` or `no file` warning label on the right. `band.test.tsx` cases assert this on both surfaces for an `in-progress` row and a `review` row, each with an unchecked next item. The cases run with no cairn skill, with `/milestone-review`, and with `/milestone-implement` running, and assert the warning label at widths 40 and 200.
- [ ] AC2: On the desktop surface, a milestone row whose counts can be read draws the flow track as an `Svg` at every `bodyColumns` width from 40 to 200. At each of those widths the title keeps min(title width, 10) columns. The track is 360 pixels wide where that room allows, and narrower where it does not. A `band.test.tsx` sweep over every width from 40 to 200 asserts the `Svg` element, its width, and the title's room. The sweep covers titles shorter and longer than 10 columns, and partial, all-checked, and zero-item counts, on an `in-progress` and a `review` row.
- [ ] AC3: On the terminal surface, a milestone row whose counts can be read draws the flow track at every `bodyColumns` width from 40 to 200. The track is a run of braille cells whose `backgroundColor` is the theme key `userMessageBackground`, with dots in the active phase's `FLOW_COLORS` color before the fill edge. A pill in that color shows the active phase's `checked/total` count, or `no tasks`, `no criteria`, or `none` for a section with no items, and the percent follows the track. The title keeps min(title width, 10) columns. A `band.test.tsx` sweep over every width from 40 to 200, with and without the open button, asserts each of these over AC2's titles and its partial, all-checked, and zero-item counts, on an `in-progress` and a `review` row.
- [ ] AC4: The band draws no skill row. With no active milestone, it draws the idle row whether or not a cairn skill runs, or nothing when no planned milestone is workable. The idle row's left group is the bold id and the title, with no `next` label, and at 200 columns it shows `/milestone-implement <id>` and the track. A press that hides the idle row keeps it hidden through a cairn skill's start and its end. `register.tsx` has no `tool.call` hook for the chapter tool. `band.test.tsx` cases assert each of these on both surfaces, the skill cases once for each directory under `skills/` that holds a `SKILL.md`, and assert that a chapter call leaves a milestone row and the idle row unchanged.
- [ ] AC5: README's "The milestone band" section, the `hooks/status/` bullet of `cairn/DESIGN.md`, and the header comments of `band.ts`, `track.ts`, and `register.tsx` describe the new row. They contain no claim that the band draws a phase or skill label, a chapter, a skill row, or the ten-cell bar. CHANGELOG's Unreleased section has an entry for the change.
- [ ] AC6: At a live look the operator accepts the desktop row at full width, the narrow desktop track at the docked-pane width of 44 columns, and the terminal row.

## Coverage

- AC1 → T2, T6
- AC2 → T1, T4
- AC3 → T1, T5
- AC4 → T2, T3, T6, T7
- AC5 → T7
- AC6 → T8

## Tasks

- [x] T1: Build browser-pane prototypes of 2 or 3 narrow desktop tracks and 2 terminal tracks, each in a dark and a light block (LESSONS M201, M204). The operator picks one of each, and a work-log line records the picks.
- [x] T2: In `band.ts`, make the left group the bold id and the title on every milestone row and on the idle row. Drop the head label, the arrow, the step body, and the `next` label. Keep the warning label for a row with no readable counts. Remove the skill row from `stepLines`, and draw the idle row while a skill runs.
- [x] T3: Remove the chapter. `CairnStep` in `types/index.d.ts` loses `chapter`, and the `step` atom takes a new shape tag. The chapter-tool `tool.call` hook in `register.tsx` goes. `SKILL_LABELS` shrinks to the cairn skill names that `cairnSkill` and the fixture test need. `mark` sets the idle id whether or not a skill runs.
- [x] T4: Build the desktop narrow track. `track.ts` takes a width, and below a width set from the T1 pick the pill shows only its count. `band.ts` picks the track width from the room the row leaves. Add the AC2 sweep.
- [x] T5: Build the terminal braille-speck track from the same `Flow` model as spans, its cell count set from the room. Delete `BAR_CELLS`, `bar`, and the counts forms. Add the AC3 sweep.
- [x] T6: Rewrite or delete the `band.test.tsx` cases for the removed forms: the phase and skill labels, chapters, the skill row, `next`, and the ten-cell bar. Add the AC1 and AC4 cases.
- [x] T7: Update README (its close-button paragraph too), the DESIGN bullet, the CHANGELOG, and the header comments of `band.ts`, `track.ts`, and `register.tsx`.
- [x] T8: Do the live look in the app at desktop full width, at the docked pane's 44 columns, and in the terminal. A mod edit needs a new Code session (LESSONS M193).

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: collision sweep: the "Terminal flow track" candidate row is absorbed (pruned at post-merge hygiene). "Status mod follow-ons" and "Band label colors in other themes" hold items about chapters, skill rows, labels, and the ten-cell bar that this milestone makes moot, so hygiene trims them. No D-entry conflicts (D-143 read). Inbox: 0 open issues, 0 open PRs.
- 2026-10-04: criteria audit (full mode, user-facing tier, fresh Opus reader) returned 9 findings, all taken toward the narrower wording. The tests use rows with an open item under three skill states. A title-room floor holds at 40 columns. The sweeps vary title length and counts. The terminal colors name `FLOW_COLORS`. The warning label is kept. The docs criterion binds the docs, not the review's audit. The pick is recorded in the work log. AC4's track and command are stated per row.
- 2026-10-04: AC4 changed after the question set and went back through the full audit. It returned 4 findings, all taken: the close state records the idle id under a running skill, the idle track holds only where it fits, every skill in `SKILL_LABELS` is probed, and AC5 names the skill row.
- 2026-10-04: question set: terminal form — a three-segment cell track (recommended) over count text only and over keeping the old bar there. Falsified if the cell track reads worse than the count text at the terminal live look.
- 2026-10-04: question set: narrow desktop — a shorter image track (recommended) over the terminal's cell track on the desktop. Falsified if no prototype reads at 44 columns.
- 2026-10-04: question set: skill row — the operator said the row adds little without a button to run the skill, so the plan removes skill rows. A pressable next-command button stays in "Status mod follow-ons".
- 2026-10-04: plan chose to remove the chapter hook and state over keeping them unused, because nothing draws a chapter after this milestone. Falsified if another surface needs the chapter.
- 2026-10-04: the T1 and T8 live looks are stops for the operator's eyes on the closed list. No outward action or dependency change is foreseen.
- 2026-10-04: T1 picks: the narrow desktop track is variant A (the image track drawn shorter, the pill cut to its count when tight, the percent kept). The operator rejected two terminal looks (block segments, line segments) and picked T3, braille specks on a gray ground with the pill at the fill edge, from a second round (shade ramp and line slider lost).
- 2026-10-04: implement chose the theme key `userMessageBackground` for the terminal ground. Every built-in theme in 2.1.286 defines it (read from the binary's strings). Falsified if a terminal theme draws the ground darker than the specks.
- 2026-10-04: re-audit: AC3 (full) — 6 findings on the braille wording: the zero-item short pill, sparse blank cells, the pill's place at the edge, a theme lacking the key, unprobed clauses, and T1/T5 still naming block cells.
- 2026-10-04: re-audit: AC3 (full) — re-entry reader found 4 more: the pill and the blank-cell clauses can contradict near the track's start, the cell count and narrow rule have no stated rule, the open button's width is not varied, and an all-blank track passes. Second line on AC3, so its wording goes to the operator.
- 2026-10-04: re-audit: AC4 (full) — 4 findings: the command cannot fit at 40 columns, the close-state clause bound the stored value, the idle cases named no width, and the terminal track was implied. All taken, and the re-entry reader runs.
- 2026-10-04: re-audit: AC4 (full) — re-entry reader found 2 more: the idle track had no least width, and the cases did not vary width or title or check a skill's start and end. Second line on AC4, so its wording went to the operator.
- 2026-10-04: substantive amendment: AC3 and AC4 narrowed at the operator's selection. AC3 tests the braille track, ground, dot color, pill count, percent, and title room, and the dot pattern is judged at the live look. AC4 tests the idle row's command and track at 200 columns and a hidden idle row through a skill's start and end.
- 2026-10-04: checkpoint, half done: T2 to T5 code and T7 docs written, Python suites green. `band.test.tsx` still tests the old forms and is red until the T6 rewrite lands (delegated to an Opus agent). The idle row also draws its track in the terminal. A running skill with nothing active or workable now yields the band slot.
- 2026-10-04: T6 delegated to an Opus agent: `band.test.tsx` rewritten (79 test blocks, 847 mod tests pass across 3 files). Seven planted defects each went red in the expected suite and were restored. I removed the pane test's skill-row case and its chapter event, which tested removed behavior. All four verify gates are green. T2 to T7 checked.
- 2026-10-04: T8 live look: the operator accepted the desktop row at full width, the narrow track beside a docked pane, and the terminal braille row in a new session.
- 2026-10-04: claim audit: 140 claims read, 5 corrected — README.md, hooks/status/band.ts, hooks/status/track.ts, hooks/status/band.test.tsx (plus one stale register.tsx comment it noted); the same reader re-read all six as correct.
- 2026-10-04: implement done, status review. All four verify gates green (847 mod tests).

## Decisions

## Review
