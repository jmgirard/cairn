# M204: A flow track band: plan, implement, review

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the band every adopter sees above the prompt
- **Branch/PR:** —

## Goal

On the desktop surface, draw the band's progress as one rounded track whose three equal segments run plan, implement, and review, with a pixel-texture fill, a pill label at the fill's edge, tick marks, and a percent.

## Scope

**In:** A pure flow model in `hooks/status/band.ts`. A milestone row's three segments fill as follows. Plan is full. Implement fills by checked tasks over all tasks for an `in-progress` row and is full for a `review` row. Review fills by checked criteria over all criteria for a `review` row and is empty for an `in-progress` row. A section of zero items is empty, and its pill reads `no tasks` or `no criteria`. The percent is `floor(100 × (sum of the three fills) / 3)`, computed in integer arithmetic. The pill reads `Implement <checked>/<total>` or `Review <checked>/<total>`. A milestone row keeps the track under any skill label and any chapter, so M196's bar-only-in-the-loop rule ends on the desktop. Two other rows join the flow. The idle row (M199) has plan full, the rest empty, pill `Planned`, and its `/milestone-implement <id>` command on the right. A `/milestone-plan` skill row with no active milestone has plan drawn running with no fill fraction, pill `Plan`, and no percent. A builder turns the model into an SVG document with a rounded track and the pill. Each filled part draws in a fixed dither (pixel-texture) pattern of its phase's color. Item ticks are n−1 marks inside a segment of n items. Phase-edge marks are two stronger marks between the segments. The SVG holds a light and a dark palette for the track ground and the ticks, chosen by `prefers-color-scheme`. Implement keeps `rgb(194,122,92)` and review keeps `rgb(106,165,122)`. Plan gets a new muted blue, and the `/milestone-plan` skill label takes it too. `register.tsx` draws the track as the desktop's `Svg` element, its `width` a fixed `TRACK_PX`, in a group that does not shrink. The group sits between the left text and a right group. The right group holds the percent, or the idle command, and the close button. The fit (M197) gains the track as the longest form, counted as a fixed `TRACK_COLUMNS`. Below that room the row falls back to today's text forms. README, DESIGN.md, and CHANGELOG describe the track.

**Out:** A cell-grid track in the terminal, which keeps today's text row and ten-cell bar (new candidate row "Terminal flow track"). The `vscode` and `mobile` surfaces, where the engine raises no `AbovePrompt` and no band draws. Animation of the fill. A row whose milestone file cannot be read keeps its text row and `warning` label, with no track. The skill row of any other cairn skill (`/hotfix`, `/cairn-triage`, and the rest) with no active milestone keeps its text row, as it is not part of the flow. The stored `band`, `step`, and `dismissed` values do not change.

## Acceptance criteria

- [ ] AC1: A `band.test.tsx` test covers every fixture in `hooks/status/fixtures.gen.ts` whose row drawn with no skill is a milestone row with readable counts. For each, it asserts the flow model's three fills, pill text, and percent against values written by hand. Further cases assert a section of zero items and an all-checked `review` row. Two more assert the idle row and the `/milestone-plan` skill row with no active milestone.
- [ ] AC2: A `band.test.tsx` walk draws every fixture on the `desktop` surface at 200 columns. It runs under no skill, `/milestone-plan`, `/milestone-implement`, `/milestone-review`, and `/hotfix`, each with no chapter and with an unlabeled chapter. A row in the flow draws exactly one `Svg`, with `width` equal to `TRACK_PX`. A row in the flow is a milestone row with readable counts, the idle row, or the `/milestone-plan` skill row with no active milestone. Its source holds a fill in a phase's color for each segment whose fill is above 0, and none for an empty one. It holds the pill text, with the pill inside the track's bounds, and a `prefers-color-scheme: dark` rule. In a milestone row's implement and review segments of n ≥ 1 items, it holds n−1 item ticks. It also holds two phase-edge marks. Its `alt` names the phase and, where the row has them, the counts and the percent. Any other row draws no `Svg`.
- [ ] AC3: A `band.test.tsx` walk draws every fixture on the `terminal` surface under the step states of AC2 and asserts that the band draws no `Svg`. The band tests from M193 to M201 pass on the terminal surface. Their desktop cases move to AC2 and AC4. The `/milestone-plan` label color is the only other edit to their inputs, surfaces, or expected values.
- [ ] AC4: A `band.test.tsx` sweep draws every fixture with no skill on the `desktop` surface at each width from 36 to 200 columns. For each fixture whose row is in the flow, a width W is written by hand. The row draws the `Svg` at widths of W and above, and draws no `Svg` below W. Below W it draws the text form that M197's room rule picks.
- [ ] AC5: The operator looks at the band in the desktop app, in its light and dark themes, and accepts the track's look. Each change they ask for at the look that lies within Scope is made before review. Any other change they ask for becomes a candidate row.
- [ ] AC6: README's band section and the `hooks/status/` entry of `cairn/DESIGN.md` describe the desktop track. They name the segments, fill, pill, ticks, percent, and narrow fallback, and say that the terminal keeps the text row. CHANGELOG's Unreleased section has an entry for the track.
- [ ] AC7: The four commands of the verify slot in `cairn/PROFILE.md` exit 0.

## Coverage

- AC1 → T1
- AC2 → T2, T4
- AC3 → T4
- AC4 → T3
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks

- [ ] T1: Add the flow model to `band.ts` (fills, pill, percent for milestone, idle, and plan-skill rows) and the plan hue, with its tests.
- [ ] T2: Add the SVG builder: rounded track, dither pattern per phase color, item ticks, phase-edge marks, pill clamped inside the track, light and dark palettes, and `alt`, with tests over its source.
- [ ] T3: Add the track as the fit's longest form on the desktop, counted as `TRACK_COLUMNS` and drawn at `TRACK_PX`, and the width sweep with its hand-written thresholds.
- [ ] T4: Draw the `Svg` in `register.tsx` on the desktop only, with the percent or idle command and the close button on the right. Give the `/milestone-plan` label the plan hue, and add the surface walks.
- [ ] T5: Stop for the operator's live look in the desktop app, light and dark, and make the changes asked for.
- [ ] T6: Update README's band section, DESIGN.md's `hooks/status/` entry, and CHANGELOG.
- [ ] T7: Run the four verify commands and fix any failure.

## Work log

- 2026-10-03: created by /milestone-plan, from the operator's screenshot of a mod in a Claude mods video (a dithered track with a pill label, ticks, and a percent).
- 2026-10-03: question set: segments — equal thirds (over weighting by items).
- 2026-10-03: question set: terminal — keep today's text row; a cell-grid track became the candidate row "Terminal flow track".
- 2026-10-03: question set: colors — keep implement orange and review green, plan gets a muted blue.
- 2026-10-03: question set: live look — the operator agreed to one live look in the desktop app, light and dark, near the end of implement (T5).
- 2026-10-03: plan gate chose the desktop `Svg` element over a `Box`/`Text` track with background colors because only an image draws the dither, rounded ends, and floating pill; falsified by the desktop drawing the `Svg` blurred, mis-sized, or out of line with the row at the live look.
- 2026-10-03: plan gate chose `prefers-color-scheme` inside the SVG over one fixed palette because an image cannot read theme keys; falsified by the SVG following the OS theme instead of the app's at the live look.
- 2026-10-03: collision check: band milestones M191-M201 are done and archived, none used `Svg`; candidate rows "Band label colors in other themes" and "Status mod follow-ons" are adjacent and stay; no D-entry blocks the change. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-03: criteria audit (full mode, fresh Opus reader) returned 13 findings, all fixed by narrowing: AC1 domain to drawn rows with readable counts; zero-item fill defined as empty and "only 100% case" dropped; AC2 fills, ticks, and alt limited to what each row has, run at 200 columns, more step states, `TRACK_PX` pinned, pill bounds and dark rule asserted; AC3 drops `vscode` and `mobile`, which raise no `AbovePrompt`; AC3 desktop cases move to AC2/AC4; AC4 thresholds written by hand; AC5 bounded to in-Scope asks; integer percent.

## Decisions

## Review
