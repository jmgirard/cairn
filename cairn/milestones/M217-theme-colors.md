# M217: Band and pane colors that follow the theme

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the status band and the cairn pane ship to every plugin user
- **Branch/PR:** m217-theme-colors

## Goal

The status band and the cairn pane take their colors from the Claude Code theme wherever the surface can read it.

## Scope

**In:** The terminal band's track and pill change their phase colors from
fixed `rgb()` values to Claude Code theme keys, one key per phase. So do the
pane's section marks, meters, and Next pill, and the candidate `↑` mark. The
light, colorblind, and ANSI themes then recolor them. The desktop track is
an image and cannot read theme keys. Its colors move into one palette block
in `track.ts`. Its phase fills are dark enough that the pill's white label
and count meet the WCAG text contrast on the fill, whatever the app's
ground. A source note records WCAG 2.2's contrast ratio. README, DESIGN, and
CHANGELOG describe the result.

The milestone promotes the color parts of four candidate rows. These are
"Band label colors in other themes", "Desktop track follow-ons (M204
review)" (pill contrast, unchecked themes), "Pane look follow-ons (M208
review)" (fixed phase colors, pill contrast, orange and green, the `↑`), and
"Band follow-ons (M206 review)" (track colors in other themes).

**Out:** A desktop track that changes its palette with the app's light,
dark, or colorblind theme. The image gets no theme signal, because the mod
API has none. M204 found that a `prefers-color-scheme` rule in such an
image follows the browser, not the page. This stays in "Band label colors
in other themes". Text contrast inside the terminal pill and the pane's Next
pill stays in "Pane look follow-ons (M208 review)". Those pills take the
theme's own colors, so their contrast is the theme's. The gray `secondary`
Buttons are the app's own look and stay in "Band button follow-ons". The
column estimates, the `clipPath` scrub, and the CJK widths stay in their
rows.

## Acceptance criteria

- [x] AC1: The terminal band's track and pill draw each phase color as a
      Claude Code theme key. So do the pane's section marks, meters, and Next
      pill. There is one key per phase, named once in `band.ts`. The text of
      the terminal pill and of the pane's Next pill is a theme key. Mod tests
      over the existing fixtures assert that each such span's `color` or
      `backgroundColor` equals the key named for its phase, and that the
      candidate `↑` mark's `color` equals the implement key.
- [x] AC2: `grep -nE 'rgba?\(|#[0-9a-fA-F]{3,8}\b' hooks/status/band.ts
      hooks/status/pane.ts hooks/status/track.ts hooks/status/register.tsx`
      prints only lines between the `// palette` start and end comments in
      `track.ts`.
- [x] AC3: For each of the three phases, the desktop track's pill fill is
      opaque. The pill label, and the pill count where the built SVG draws
      one, each have a contrast ratio of at least 4.5:1 against that fill. The ratio is the WCAG 2.2 contrast ratio `wcag22 (SC 1.4.3)`. A
      mod test reads the fill and text colors from the SVG that the track
      builds for that phase, composites any text opacity over the fill, and
      computes the ratios.
- [x] AC4: At a live look in a real cairn repo, the operator sees the band
      and the pane in the desktop app's light and dark appearance, and the
      terminal band in one light theme and one colorblind theme. The
      operator accepts the colors at that look.
- [x] AC5: README.md and `cairn/DESIGN.md` describe the theme keys and the
      desktop palette. `grep -nE 'rgb\((194,122,92|106,165,122|110,140,190)\)' README.md cairn/DESIGN.md`
      prints nothing. CHANGELOG.md's unreleased section has an entry for
      the change.
- [x] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1
- AC2 → T2, T4
- AC3 → T2, T3, T5
- AC4 → T7
- AC5 → T6
- AC6 → T8

## Tasks

- [x] T1: In `band.ts`, `FLOW_COLORS` (band.ts:127) takes theme keys:
      `planMode` for plan, `claude` for implement, `success` for review.
      Remove `ORANGE`, `GREEN`, and `BLUE` (band.ts:23-26). The terminal
      pill's text (`PILL_TEXT`, track.ts:195, :227) takes `inverseText`. The
      pane's `↑` (pane.ts:37) takes the implement key, and its Next pill
      (pane.ts:180-182) follows `FLOW_COLORS`, its stale contrast comment
      (pane.ts:182) rewritten. Band and pane tests assert that each phase's
      spans carry its key over the existing fixtures. The SVG draws its fills
      from `FLOW_COLORS` today (track.ts:153, :179), so T1 and T2 land in one
      commit.
- [x] T2: In `track.ts`, gather every raw color the SVG draws into one
      palette block, marked by `// palette` start and end comments, that only
      the SVG reads. These are `GROUND`, `GRAY`, `MARK` (track.ts:39-41), the
      phase fills of the specks and the pill (track.ts:153, :179), and the
      pill text and count (`#fff`, track.ts:182).
      Choose phase fills near the old hues and dark enough that the white
      label and count reach 4.5:1 on them.
- [x] T3: Add the contrast test to the mod tests. Write a WCAG
      relative-luminance and contrast-ratio helper, and check it first
      against the definition's endpoints: 21:1 for black on white, 1:1 for a
      color on itself. Then, for each phase, parse the pill's fill and its
      label and count fills from the built SVG, composite any opacity over
      the fill, and assert that each ratio is at least 4.5.
- [x] T4: Run AC2's grep. Move or replace any raw color it still prints
      outside the palette block in `register.tsx`, `band.ts`, or `pane.ts`.
- [x] T5: Write `cairn/references/wcag22.md` from the source-note template.
      Record the relative-luminance and contrast-ratio definitions and SC
      1.4.3's 4.5:1 minimum, with section anchors. Add its `INDEX.md` line.
- [x] T6: Update README.md (the band paragraphs near README.md:94-112 and
      the pane paragraph near :251-253) and `cairn/DESIGN.md` (near :197-210
      and :257-259). Add a CHANGELOG.md unreleased entry. Write each one
      against the shipped code.
- [x] T7: Draw the desktop track for each phase in a dark and a light block
      in the browser pane, served from the scratchpad, and check it. Then do
      the live look in this repo: the desktop app in light and dark
      appearance, and a terminal session in a light theme and a colorblind
      theme.
- [x] T8: Run every `verify` command from the repo root, check each exit
      code, and fix any red.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to work on (no work named). Answer: theme-aware band and pane colors.
- 2026-10-04: question set: a live look in the desktop app during review. Answer: granted.
- 2026-10-04: collision sweep: no open issues or PRs. M198 (done) rejected dim theme keys because the dim `claude` orange drew brown in the desktop dark theme, and it kept full-strength keys for the bar, so this plan uses full-strength keys. M204 (done) chose the fixed colors and the plan blue, which T1 replaces. Post-merge hygiene prunes the four promoted candidate rows.
- 2026-10-04: plan gate chose `planMode` for plan over the `suggestion` or `permission` blue (M204's hue), because the colorblind themes draw `success` in a near blue. Falsified by the operator rejecting the teal at the live look.
- 2026-10-04: plan gate chose one desktop palette whose white pill text reaches 4.5:1 on the fill over a palette per app theme, because the image gets no theme signal and text on the fill does not depend on the ground. Falsified by the mod API gaining a light or dark signal.
- 2026-10-04: criteria audit (full mode, fresh Opus reader): 11 findings, all taken toward the narrower promise. The Goal narrowed to "wherever the surface can read it". AC1 names both pills and pins `↑` to the implement key. AC2 takes 3 to 8 digit hex and is bounded by `// palette` comments. AC3 requires an opaque fill and checks the count only where drawn, since the plan pill has none. AC5 dropped `do not follow your theme`. T1 and T2 land together, T1 rewrites the pane.ts:182 comment, and T2 names the specks and `#fff`.
- 2026-10-04: implement started on branch m217-theme-colors. The untracked `cairn-probe.log` and `tsconfig.json` from earlier sessions stay unstaged.
- 2026-10-04: T1-T3: `FLOW_COLORS` is `planMode`/`claude`/`success`, the terminal pill text `inverseText`, the pane `↑` the implement key. `track.ts` holds the desktop palette between `// palette` comments: fills rgb(71,103,158), rgb(152,85,57), rgb(68,113,81), white label, count opacity raised from 0.72 to 0.85 so the count also reaches 4.5:1 (label about 5.6:1, count about 4.6:1, from the scratchpad computation). The band and pane tests carry the keys and fills by hand; the new AC3 test computes the WCAG ratio from the built SVG per phase. Mod tests 1133 to 1137, all five verify commands exit 0.
- 2026-10-04: AC3 test plant: count opacity back to 0.72 and the plan fill back to rgb(110,140,190) turned all three AC3 tests red on their contrast assertions (plan label, implement and review counts), 24 fails in all; `track.ts` restored from daf86e7.
- 2026-10-04: T4: AC2's grep prints only track.ts:47-55, inside the `// palette` comments at :40 and :56; nothing to move.
- 2026-10-04: T5: `cairn/references/wcag22.md` written from the W3C Recommendation of 2024-12-12, read by curl at `#contrast-minimum`, `#dfn-contrast-ratio`, `#dfn-relative-luminance`; INDEX line added; cairn_validate green.
- 2026-10-04: T6: README (band and pane color paragraphs), DESIGN (terminal track, desktop palette, pane colors), and a CHANGELOG Unreleased New entry, written against track.ts, band.ts, pane.ts and the theme tables read from Claude Code 2.1.287 this session. AC5's grep prints nothing.
- 2026-10-04: the T6 commit (1a5e707) went in with the scripts suite red: `TestShippedPageStateLedger` pins every references page and lacked `wcag22.md` since T5. Fixed by pinning it as `ok` (dated direct-read claim) with its justification comment; scripts suite exit 0.
- 2026-10-04: T7 preview: the desktop track for plan, implement, and review, before (M204 colors, count 0.72) and after (M217 palette), drawn by `trackSvg` on the app's light grounds rgb(250,249,245) and white and dark grounds rgb(38,38,36) and rgb(48,48,46), in the browser pane from the scratchpad. The after pills keep their hues, draw darker, and their label and count read on every ground; the dark-ground pills stand out less than before. Live look next.
- 2026-10-04: T7 live look (the granted stop): the operator looked at the band and pane in a new Code session with the app in light and dark appearance and in a terminal in a light and a colorblind theme, and chose "Accept the colors" at the chip.
- 2026-10-04: T8: all five verify commands exit 0 from the repo root: scripts 397 tests OK (21 skipped), hooks 174 OK, both validates pass, mod tests 1137 pass.
- 2026-10-04: claim audit: 40 claims read, 2 corrected — hooks/status/track.ts, hooks/status/band.ts, CHANGELOG.md (the terminal-track constants comment called braille characters theme keys; "the light theme recolors them" was false for `claude`, which light keeps at rgb(215,119,87); DESIGN.md got the same fix). The re-read cleared band.ts and CHANGELOG and refined the track comment's speck wording, applied as given. Mod tests 1137 pass after the comment edits.

## Decisions

## Review

Pass 1, 2026-10-04, on branch head 05fa1d0 (main dc3cc7c, not moved since the branch was cut).

- AC1 evidence: `claude plugin test .` exit 0, 1137 pass. The key assertions pass in: pane.test "each priority's mark" (`↑` color is `'claude'`, written by hand), "partly checked and all checked" (meters `claude`/`success`), "section headings and Next in the set-off form (M208 AC3)" (accent marks per phase, queue `planMode`), "the Next command sits in a pill of its phase's color" (fill per phase over pane-full, single-in-progress, all-waiting; text `inverseText`); band.test `trackProblems` (terminal pill on `claude`/`success`, text `inverseText`), "the idle row at 200 columns" (plan pill on `planMode`, text `inverseText`), and the per-fixture desktop/terminal track test (pill on `PHASE_KEYS[index]`, text `inverseText`). A grep of the four source files finds the keys only at band.ts:128 (`FLOW_COLORS`, one key per phase) and track.ts:213 (`PILL_TEXT`).
- AC2 evidence: the grep prints track.ts:47, 48, 49, 51, 52, 53, 55, all between `// palette` (:40) and `// palette end` (:56).
- AC3 evidence: band.test "the desktop pill text reads on its fill (M217 AC3)" passes its four tests: the helper's 21:1 and 1:1 endpoints, and the plan (label only), implement, and review pills (label and count at its fill-opacity, each at least 4.5, pill rect without opacity). The T3 plant (count 0.72, old plan fill) turned all three pill tests red (work log).
- AC4 evidence: the T7 live look; the operator chose "Accept the colors" at the chip after viewing desktop light and dark and a light and a colorblind terminal theme (work log 2026-10-04).
- AC5 evidence: the rgb grep over README.md and cairn/DESIGN.md exits 1 with no output. README.md:94-117 and :255-259 and DESIGN.md:199-205 and :216-221 name the theme keys and the desktop palette. CHANGELOG.md:7 holds the entry under `## Unreleased` (:3).
- AC6 evidence: from the repo root, scripts 397 tests OK (21 skipped), hooks 174 OK, plugin validate exit 0 (one warning, the root CLAUDE.md), marketplace validate exit 0, mod tests 1137 pass, exit 0.
- Consistency gate: `cairn_validate` exit 0, all checks passed (coverage complete included). No principle changed, so `cairn_impact` skipped. Profile gate: verify green on the review head (AC6); the marketplace validate prints no `plugins[N].version` warning; CHANGELOG.md:7 covers the change with no milestone number in it.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: in light-daltonized the terminal and pane implement pill is white `inverseText` on `claude` rgb(255,153,51), 2.13:1, below the old 2.9-3.4:1 (light theme 3.15:1) — follow-up, new row "Theme color follow-ons (M217 review)" (Scope Out left pill contrast to the theme).
- diff-bug #2: the AC3 test ignores opacity on `<text>`, an `opacity` or `fill` on a tspan, so a later edit could dim the count with the test green — fix now, fixed 3a2afb8 (a planted `opacity="0.7"` on the count tspan turned the implement and review pill tests red, then restored).
- diff-bug #3: no test shows the desktop resolves `planMode`/`inverseText`/`success` — reject (false): the operator saw the pane and band on the desktop in light and dark at the live look.
- diff-bug #4: `PHASE_FILLS` is exported and nothing imports it — fix now, fixed 3a2afb8.
- diff-bug #5: README.md:94 says "green for review" while the colorblind themes draw it blue — fix now, fixed 3a2afb8.
- diff-bug #6: edited lines run past the wrap width (track.ts:206, CHANGELOG, README) — fix now, with prior-review #1, fixed 3a2afb8.
- blame-history #1: the terminal pill text changed from M206's white to `inverseText` (black in dark themes) and no dark terminal theme was looked at — reject (planned change): T1 named `inverseText`, and the operator saw it in the desktop dark appearance.
- blame-history #2: the desktop track's plan fill is blue and implement a darker orange, while the pane on the same desktop draws teal `planMode` and `claude` orange, undoing M204's one hue per phase — follow-up, "Theme color follow-ons (M217 review)".
- blame-history #3: the darker desktop track stands out less on dark grounds — reject (planned change): accepted at the live look.
- blame-history #4: the count opacity rose from 0.72 to 0.85, shrinking M204's label and count hierarchy — reject (planned change): T2 and AC3 call for it.
- blame-history #5: M198's dim-key rejection is respected — reject (false): reports no defect.
- blame-history #6: ROADMAP candidate rows still describe fixed colors — reject (planned change): post-merge hygiene trims the promoted rows.
- blame-history #7: DESIGN does not say light keeps `claude` unchanged — reject (false): "the light theme changes plan and review" says it.
- blame-history #8: the test changes strengthen the pins — reject (false): reports no defect.
- prior-review #1: ragged wraps in README.md:96, track.ts:206, CHANGELOG.md:12, DESIGN.md:205 reintroduce M198 R5 and M204 #6 — fix now, fixed 3a2afb8.
- After the fixes: all five verify commands exit 0 (mod tests 1137 pass), the AC2 grep still prints only track.ts:47-55, `cairn_validate` passes. The two follow-ups are filed at post-merge hygiene as "Theme color follow-ons (M217 review)", because a new row now would put ROADMAP.md at the 60-line cap; the hygiene pass frees a line by dropping the M214 terminal row.
- prior-review #2: plan teal and review blue may be close in the colorblind themes — reject (planned change): the plan gate weighed this (work log), and in the tables light-daltonized is rgb(51,102,102) against rgb(0,102,153), dark-daltonized rgb(102,153,153) against rgb(51,153,255); the operator accepted a colorblind theme at the live look.
- prior-review #3: the `↑` takes the implement key under the plan-colored heading — reject (planned change): AC1 calls for it.
