# M204: A flow track band: plan, implement, review

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the band every adopter sees above the prompt
- **Branch/PR:** m204-flow-track-band

## Goal

On the desktop surface, draw the band's progress as one rounded track whose three equal segments run plan, implement, and review, with a pixel-texture fill, a pill label at the fill's edge, tick marks, and a percent.

## Scope

**In:** A pure flow model in `hooks/status/band.ts`. A milestone row's three segments fill as follows. Plan is full. Implement fills by checked tasks over all tasks for an `in-progress` row and is full for a `review` row. Review fills by checked criteria over all criteria for a `review` row and is empty for an `in-progress` row. A section of zero items is empty, and its pill reads `no tasks` or `no criteria`. The percent is `floor(100 × (sum of the three fills) / 3)`, computed in integer arithmetic. The pill reads `Implement <checked>/<total>` or `Review <checked>/<total>`. A milestone row keeps the track under any skill label and any chapter, so M196's bar-only-in-the-loop rule ends on the desktop. Two other rows join the flow. The idle row (M199) has plan full, the rest empty, pill `Planned`, and its `/milestone-implement <id>` command on the right. A `/milestone-plan` skill row with no active milestone has no fill, pill `Plan`, and no percent. A builder in `hooks/status/track.ts` turns the model into an SVG document in the look the operator chose at the live look (design A). The track is a rounded, quiet gray ground. Two-pixel specks run from the left edge to the active phase's fill edge, sparse at the left and dense near the edge, gray at first and more often the active phase's color near the edge. The pill sits at the fill edge in the active phase's color, its label bold and its count dimmer. Two edge marks sit between the segments. Item ticks fall only in the active segment, past the fill edge, when the items are 6 pixels apart or more. One set of translucent grays serves light and dark, because the image follows the system's setting, not the app's theme. Implement keeps `rgb(194,122,92)` and review keeps `rgb(106,165,122)`. Plan gets a new muted blue, and the `/milestone-plan` skill label takes it too. `register.tsx` draws the track as the desktop's `Svg` element, its `width` a fixed `TRACK_PX`, in a group that does not shrink. The group sits between the left text and a right group. The right group holds the percent, or the idle command, and the close button. The fit (M197) gains the track as the longest form, counted as a fixed `TRACK_COLUMNS`. Below that room the row falls back to today's text forms. README, DESIGN.md, and CHANGELOG describe the track.

**Out:** A cell-grid track in the terminal, which keeps today's text row and ten-cell bar (new candidate row "Terminal flow track"). The `vscode` and `mobile` surfaces, where the engine raises no `AbovePrompt` and no band draws. Animation of the fill. A row whose milestone file cannot be read keeps its text row and `warning` label, with no track. The skill row of any other cairn skill (`/hotfix`, `/cairn-triage`, and the rest) with no active milestone keeps its text row, as it is not part of the flow. The stored `band`, `step`, and `dismissed` values do not change.

## Acceptance criteria

- [x] AC1: A `band.test.tsx` test covers every fixture in `hooks/status/fixtures.gen.ts` whose row drawn with no skill is a milestone row with readable counts. For each, it asserts the flow model's three fills, pill text, and percent against values written by hand. Further cases assert a section of zero items and an all-checked `review` row. Two more assert the idle row and the `/milestone-plan` skill row with no active milestone.
- [x] AC2: A `band.test.tsx` walk draws every fixture on the `desktop` surface at 200 columns, with no skill and no chapter, and under `/milestone-plan`, `/milestone-implement`, `/milestone-review`, and `/hotfix`, each with no chapter and with an unlabeled chapter. In the walk, a row in the flow draws exactly one `Svg`, with `width` equal to `TRACK_PX`. A row in the flow is a milestone row with readable counts, the idle row, or the `/milestone-plan` skill row with no active milestone. The active phase is implement on an `in-progress` row, review on a `review` row, and plan on the idle and `/milestone-plan` rows. The fill edge is the active phase's fill edge, in SVG user units. Each speck cell lies between the left edge and the fill edge, in gray or the active phase's color. When the fill edge is above 0, at least one speck is in the active phase's color, and when it is 0, no speck is drawn. The source holds two edge marks at a third and two thirds of the track, and the pill text. The pill is in the active phase's color, with its right edge at the fill edge plus 6, clamped to 1 unit inside the track. Let n count the tasks (implement) or criteria (review), c the checked ones, and s the segment's left edge. Where (TRACK_PX / 3) / n ≥ 6, the source holds one tick at x = s + k × (TRACK_PX / 3) / n for each k with c < k < n. No other tick is drawn in any walked row. Its `alt` begins with the phase name and, where the row has them, names the counts and the percent. Any other row in the walk draws no `Svg`.
- [x] AC3: A `band.test.tsx` walk draws every fixture on the `terminal` surface under the step states of AC2 and asserts that the band draws no `Svg`. The band tests from M193 to M201 pass on the terminal surface. Their desktop cases move to AC2 and AC4. The `/milestone-plan` label color is the only other edit to their inputs, surfaces, or expected values.
- [x] AC4: A `band.test.tsx` sweep draws every fixture with no skill on the `desktop` surface at each width from 36 to 200 columns. For each fixture whose row is in the flow, a width W is written by hand. The row draws the `Svg` at widths of W and above, and draws no `Svg` below W. Below W it draws the text form that M197's room rule picks.
- [x] AC5: The operator looks at the band in the desktop app, in its light and dark themes, and accepts the track's look. Each change they ask for at the look that lies within Scope is made before review. Any other change they ask for becomes a candidate row.
- [x] AC6: README's band section and the `hooks/status/` entry of `cairn/DESIGN.md` describe the desktop track. They name the segments, fill, pill, ticks, percent, and narrow fallback, and say that the terminal keeps the text row. CHANGELOG's Unreleased section has an entry for the track.
- [x] AC7: The four commands of the verify slot in `cairn/PROFILE.md` exit 0.

## Coverage

- AC1 → T1
- AC2 → T2, T4
- AC3 → T4
- AC4 → T3
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Add the flow model to `band.ts` (fills, pill, percent for milestone, idle, and plan-skill rows) and the plan hue, with its tests.
- [x] T2: Add the SVG builder: rounded track, speck field to the fill edge, item ticks in the active segment, phase-edge marks, pill at the fill edge clamped inside the track, and `alt`, with tests over its source. Built rows probe the tick spacing at 20 and 21 tasks and heads near an item edge (7/9 tasks, 11/18 criteria).
- [x] T3: Add the track as the fit's longest form on the desktop, counted as `TRACK_COLUMNS` and drawn at `TRACK_PX`, and the width sweep with its hand-written thresholds.
- [x] T4: Draw the `Svg` in `register.tsx` on the desktop only, with the percent or idle command and the close button on the right. Give the `/milestone-plan` label the plan hue, and add the surface walks.
- [x] T5: Stop for the operator's live look in the desktop app, light and dark, and make the changes asked for.
- [x] T6: Update README's band section, DESIGN.md's `hooks/status/` entry, and CHANGELOG.
- [x] T7: Run the four verify commands and fix any failure.

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
- 2026-10-03: implement: branch cut from origin/main at 396eb97; the untracked `tsconfig.json` in the tree is not this milestone's and stays unstaged.
- 2026-10-03: T1-T4: `flowOf`, `idleFlow`, `planFlow`, and `percentOf` in band.ts; the SVG builder in a new `hooks/status/track.ts` (`TRACK_PX` 224, `TRACK_H` 18, `TRACK_COLUMNS` 32 in band.ts); `register.tsx` draws `Svg` on the desktop only; `/milestone-plan` label in `rgb(110,140,190)`. Chose a separate track.ts over growing band.ts because the SVG markup is its own concern. Old suites' `SURFACES` is now terminal alone and three desktop mounts became terminal, per AC3. Mod tests 600 → 940, all pass.
- 2026-10-03: T1-T4 plants: `TRACK_COLUMNS` 31 failed AC4, a review dither in orange failed AC2, a rounded-up percent failed AC1/AC2, n ticks instead of n−1 failed AC2; each restored.
- 2026-10-03: pre-look in the browser pane: a 2-pixel checkerboard read as a grid, not noise, so the dither became a 24×18 tile of seeded noise blocks; the SVG as an `<img>` followed the browser's dark preference, not the page's `color-scheme`, so the app-versus-OS question goes to the live look.
- 2026-10-03: T5 live look: the operator found the first look ugly, "a lazy adaptation" of the screenshot. Three redesigns were prototyped in the browser pane in dark and light; at the chip the operator chose A: a quiet gray ground, 2-pixel specks from the left edge to the active phase's fill edge, sparse to dense and gray into the phase color, a pill with a bold label and dimmer count at the edge, ticks only in the active segment. Rejected: B, finer 1.5-pixel specks (less visible at a glance), and C, color in the pill only.
- 2026-10-03: T5 rebuild: track.ts redrawn as design A, `TRACK_PX` 360, `TRACK_COLUMNS` 52, one translucent palette with no `prefers-color-scheme` rule (the image follows the system setting, not the app's), `Flow.running` and the dashed plan outline removed. AC4 thresholds redone by hand for 52 columns. Tick test now compares whole numbers (k × den > num × n); the old pixel compare failed the built 7/9 and 18-criteria cases when planted. Mod tests 944, all pass.
- 2026-10-03: re-audit: AC2 (full) — 8 findings on the first amended wording: tick edge ambiguous at the head (a rounding bug, fixed in code), item edges and spacing unit undefined, "no other tick" unbounded, an empty fill could pass, cells could run past the head (fixed: last column cut), pill position unasserted (now asserted), Scope stale.
- 2026-10-03: re-audit: AC2 (full) — 7 findings on the repaired wording: alt phase check vacuous (test now uses startsWith), active phase undefined for idle and plan rows, tick x unstated, "no other tick" and "any other row" unbounded, no-skill chapter case misread, edge marks unpositioned (now asserted), the built-cases clause binds an instrument. Second re-audit on AC2, so the wording goes to the operator.
- 2026-10-03: substantive amendment: Scope's look rewritten to design A (specks to the fill edge, pill at the edge, ticks in the active segment, one palette, no plan outline) and AC2 replaced by the wording the operator accepted at the chip ("Accept wording"); the built-row probes moved from the criterion to T2 as an instrument clause.
- 2026-10-03: T5 done: the operator chose design A from the browser-pane prototype, not from the band in the desktop app; the in-app look in light and dark (AC5) is asked at the merge question.
- 2026-10-03: T6: README gains two desktop-track paragraphs and the `/milestone-plan` blue; DESIGN.md's `hooks/status/` entry gains the track; CHANGELOG Unreleased gains "A flow track in the desktop band"; band.ts and register.tsx header comments name the track.
- 2026-10-03: T7: `scripts/tests` exit 0, `hooks/tests` exit 0, `claude plugin validate` exit 0, `claude plugin test` exit 0 (944 pass, 0 fail); `cairn_validate` all checks passed.
- 2026-10-03: claim audit: 68 claims read, 4 corrected — README.md, CHANGELOG.md (the 100% case and a review row with no criteria, the percent on milestone rows only, ticks between the items left, the `no tasks` pill); the same reader re-read the four as true; a 0.005-pixel rounding note in track.ts was left as is.
- 2026-10-03: implement done: all tasks checked, mod tests 944 pass after the doc fixes; status set to review.
- 2026-10-03: step-7 approval: m204-flow-track-band approved for merge

## Decisions

## Review

- 2026-10-03 round 1, on branch head b836241, origin/main 396eb97 an ancestor (no sync merge needed).
- AC1: `claude plugin test .` (2.1.286) — the "(M204 AC1)" describe ran 15 tests, 15 pass: the domain test equals the 9-fixture FLOWS table, 9 per-fixture hand values, zero-item sections (M042 33%, M052 66%), all-checked review M053 100% and implement M043 66%, unreadable M004 null, idle and plan flows.
- AC2: same run — the "(M204 AC2)" describe ran 158 tests, 158 pass: 17 fixtures × 9 step states (no skill; four skills × no chapter and unlabeled chapter) at 200 columns on `desktop`, each asserting one `Svg` of width 360 or none, speck cells within [0, fill edge] in gray or the active hue with at least one in the hue, edge marks at 120 and 240, the pill's hue, text, and right edge at fill edge + 6 clamped, ticks at the computed x for c < k < n, and the alt's leading phase; plus 4 built rows (20 and 21 tasks, 7/9, 11/18) and the plan-pill test. Plant at implement: the old pixel compare failed the 7/9 and 11/18 rows.
- AC3: same run — the "(M204 AC3)" describe ran 153 tests (17 fixtures × 9 step states), 153 pass, each finding no `Svg` on `terminal` at 200, 120, and 36 columns; the pre-M204 suites ran 600 tests, 600 pass, on the terminal. `git diff origin/main...HEAD -- hooks/status/band.test.tsx` shows the only edits above the M204 block: `SURFACES` to terminal alone, three `surface: 'desktop'` mounts to `terminal` (the desktop cases moved), and `skillHue` plus `BLUE` for the `/milestone-plan` label.
- AC4: same run — the "(M204 AC4)" describe ran 18 tests, 18 pass: the domain test equals the 13-fixture TRACK_FROM table (hand-written W, 87 to 104 columns), and each of 17 fixtures swept 36 to 200 columns on `desktop`, asserting the `Svg` from W up and none below, with the desktop rows below W equal to the terminal's rows at the same width. Plant at implement: `TRACK_COLUMNS` 31 failed the sweep.
- AC5: open — the operator chose design A from a browser-pane prototype (work log); the look in the desktop app, light and dark, is asked at the merge question.
- AC5: 2026-10-03 merge question — the chip asked the operator to look at the band in a new session in the app's light and dark themes, and stated that merging records the track looks right in the app; the operator chose "Merge". No change was asked at the look.
- AC6: the branch's added README lines name the three equal parts, specks, pill, ticks, percent, the narrower-window fallback, and that the terminal keeps the text row; DESIGN.md's `hooks/status/` entry names the three segments, specks, pill, ticks, percent, the fallback below the track's room, and that the terminal never draws the track; CHANGELOG Unreleased opens with "A flow track in the desktop band" (`git diff origin/main...HEAD` greps, each term ≥ 1 hit). The claim audit's 4 corrections are in.
- AC7: from the repo root, each exit checked: `python3 -m unittest discover -s scripts/tests` exit 0 (395 tests, OK, 21 skipped), `python3 -m unittest discover -s hooks/tests` exit 0 (OK), `claude plugin validate .claude-plugin/plugin.json` exit 0 (one root CLAUDE.md warning, as on main), `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0 (944 pass, 0 fail).
- Consistency gate: `cairn_validate` exit 0; no principle changed, so no `cairn_impact`; the generic profile's consistency-gate slot names no toolchain checks.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: an 18px track makes the row taller, so left text sits high while the right group is centered — fix now, fixed 49ca73c (row and right group centered on the desktop only)
- diff-bug #2: the pill text uses per-character estimates and can spill past the pill in a wider font — fix now, fixed 49ca73c (`textLength` with `spacingAndGlyphs`)
- diff-bug #3: `elements.Svg` read from an un-narrowed resolve would fail a strict type check — fix now, fixed 49ca73c
- diff-bug #4: desktop rows outside the flow are checked only for no `Svg` — fix now, fixed 49ca73c (the walk compares them to the terminal's rows and checks the `✕`)
- diff-bug #5: README and CHANGELOG say the track replaces only the bar and counts, but it also replaces `no tasks` and `all … checked` — fix now, fixed 49ca73c
- diff-bug #6: DESIGN says every alt names counts and percent and omits the pill clamp — fix now, fixed 49ca73c
- diff-bug #7: the system-versus-app theme claim was stated as fact from a browser preview — fix now, fixed 49ca73c (hedged in track.ts and DESIGN)
- diff-bug #8: checked above total overflows a segment — reject, false: the reader counts checked boxes among the section's boxes, so checked never exceeds total
- diff-bug #9: `TRACK_COLUMNS` 52 assumes about 7 pixels a column, unchecked — follow-up, row "Desktop track follow-ons"
- diff-bug #10: edge marks faint on light, and a scrub could drop `clipPath` — follow-up, row "Desktop track follow-ons"
- diff-bug #11: the speck loop copies its array per cell — fix now, fixed 49ca73c
- diff-bug #12: a header comment line too long — fix now, fixed 49ca73c
- diff-bug #13: AC5 is open at review — reject, planned change: the plan's work log puts the in-app look at the merge question
- blame-history #1: desktop leaf colors and `dimColor` (M198) no longer checked — fix now, fixed 49ca73c (`desktopProps` checks every leaf)
- blame-history #2: M194's `minWidth: 0` and `flexShrink` no longer checked on the desktop — fix now, fixed 49ca73c (plant: an uncentered row failed 152 tests)
- blame-history #3: the desktop `✕`, `dimColor`, and `plain` checked only on track rows — fix now, fixed 49ca73c
- blame-history #4: press, refresh, and session-end flows no longer run with a desktop render — follow-up, row "Desktop track follow-ons"
- blame-history #5: README's "Three labels replace the bar" conflicts with the desktop — fix now, fixed 49ca73c ("In the text row")
- blame-history #6: `/milestone-plan` blue changes M198's "every other skill" rule — reject, planned change (question set: colors)
- blame-history #7: `alignItems` added on every surface — fix now, fixed 49ca73c (desktop only)
- blame-history #8: the 7-pixel column estimate and the 18px height are unchecked against the app — follow-up, row "Desktop track follow-ons"
- blame-history #9: the `✕` docs and the desktop-only track agree — reject, false: the reviewer found no conflict
- prior-review #1: "grays that read on light or dark" is unverified in the app — fix now, fixed 49ca73c ("meant for")
- prior-review #2: white pill text on the phase colors, about 3:1 — follow-up, row "Desktop track follow-ons"
- prior-review #3: fixed grays unchecked in other themes — follow-up, row "Desktop track follow-ons"
- prior-review #4: column and pill-width estimates — follow-up, row "Desktop track follow-ons" (pill spill fixed by diff-bug #2)
- prior-review #5: a 360px `Svg` could overrun a narrow window — follow-up, row "Desktop track follow-ons" (the fit guards it in columns)
- prior-review #6: ragged wraps in README and register.tsx — fix now, fixed 49ca73c
- prior-review #7: README's `Review 2/3` example matches no tested case — fix now, fixed 49ca73c (`Review 1/2`, the wide-title pill AC1 asserts)
- prior-review #8: DESIGN's system-versus-app claim — fix now, fixed 49ca73c (hedged)
- prior-review #9: DESIGN's history line is long — reject, style
- prior-review #10: CHANGELOG's tick wording drifts from README — reject, false: the claim reader read it as true against track.ts
- Totals: 32 findings — 18 fixed now, 8 to the new candidate row "Desktop track follow-ons", 6 rejected. No finding shows a criterion failing, so no return.
