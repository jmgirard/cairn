<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M198: A muted band that matches the app's own bar

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m198-muted-band

## Goal

Draw the band's text in the theme's gray, with only the phase label and the bar's filled cells in a dim orange or green.

## Scope

**In:** The colors of the Text leaves that `hooks/status/band.ts` and `hooks/status/register.tsx` draw in the band.
The phase label and a skill's label draw in a fixed muted orange or green with no dim. The filled bar cells keep the phase's theme key (`claude` or `success`) at full strength, and the empty cells take the theme key `subtle`.
The other leaves take the theme key `inactive`, except the `warning` labels and the space leaves.
The tests in `hooks/status/band.test.tsx` change to match.
README.md, cairn/DESIGN.md, and the CHANGELOG band entry describe the new colors.

**Out:** The font. The mod API's `Text` has no font prop, and the `Code` element draws in the engine's own colors.
That work goes to a new candidate row, "Band in the app's code font".
The close Button keeps its M197 props.
The row layout, the forms, and the fit stay as M197 left them.

## Acceptance criteria

- [x] AC1: The phase label and a cairn skill's label draw in a fixed muted color with no `dimColor`: `rgb(194,122,92)` for the implement hue and `rgb(106,165,122)` for the review hue. A skill's label takes the review hue for `/milestone-review` and the implement hue for every other skill. The phase label takes its phase's hue. The bar's filled cells take the phase's theme key with no `dimColor`: `claude` for `implement` and `success` for `review`. The empty cells take the theme key `subtle` with no `dimColor`. The AC2 walk checks this on every row it draws. The label-color table in `band.test.tsx` also checks two rows that draw a bar. They are `single-in-progress` with no skill, and M010 in `mixed` under `/milestone-review`.
- [x] AC2: Every other Text leaf inside the `cairn-band` Box takes the theme key `inactive` with no `dimColor`. There are two exceptions. A leaf that holds only spaces is exempt. `no milestone file` and `no file` keep `warning`. A test in `band.test.tsx` draws every fixture under `hooks/status/fixtures/` on both surfaces, at the default width and at 36 columns. It draws each fixture with no skill, with `/milestone-review` running, and with `/milestone-plan` running. It walks every Text leaf inside `cairn-band` and asserts the color rule above for each leaf. A drawing that shows a row must hold at least one leaf. `no-active`, `no-roadmap`, and `repo-at-cut` draw no row with no skill. The walk must see at least one skill row for each of the two skills. The id and a step's positional label stay bold. The close Button keeps its M197 props.
- [x] AC3: The docs describe the new colors. The sweep is `git grep -n -iE 'orange|green|gray|grey|colou?r|dim|muted|subtle|inactive|tint|hue' -- README.md CHANGELOG.md cairn/DESIGN.md`. Each hit about the band states the colors this milestone draws, or stays true under them. README.md's paragraph that begins "The phase label is drawn" says four things. The label draws in a muted orange or green. The filled cells draw in the theme's full Claude orange or success green. The empty cells draw in the theme's subtle gray. The rest of the row draws in the theme's gray.
- [ ] AC4: A live look at a new desktop Code session, on a row that draws a bar, shows the band's text in gray and its label in a muted orange or green. The filled cells stand apart from the empty cells, and the empty cells stay visible. The operator confirms this at the review chip.
- [x] AC5: The verify slot of `cairn/PROFILE.md` runs clean: `python3 -m unittest` over `scripts/tests` and `hooks/tests`, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2, T3
- AC3 → T4, T6
- AC4 → T5
- AC5 → T7

## Tasks

- [x] T1: Write the tests first in `band.test.tsx`. Change the label-color table (about line 354) and the bar asserts (about lines 543-557 and 1665-1668) to the dim hues. Add the two bar rows that AC1 names. Add the AC2 leaf walk over every fixture, both surfaces, both widths, and the three skill states. Change the arrow assert (about line 761) to `inactive` with no dim. See the new tests fail.
- [x] T2: In `band.ts`, give the phase and skill label spans and the filled bar cells `dimColor`. Give the id, the counts, the state labels, and the slash command the color `inactive`. Drop `dimColor` from the state labels.
- [x] T3: In `register.tsx`, draw the arrow, the positional label, and the row's text in `inactive`, with no `dimColor` on the arrow. Leave the close Button as it is. Run `claude plugin test` until it is green.
- [x] T4: Run the AC3 sweep. Update each hit about the band that the new colors make false, then run the sweep again and read each hit.
- [x] T5: Do a live look in a new desktop Code session, because a running session keeps the mod it loaded at its start. If the dim hues do not read as muted, amend through the gate to two fixed mid-tone colors.
- [x] T6: Rerun the AC3 sweep against the look D colors and fix each hit, the labels' fixed colors included.
- [x] T7: Run the verify slot.
- [x] T8: Review return (R1, R2). Make the band color claims in README.md and CHANGELOG.md true in every theme. Drop "near the background" for the empty cells. The ANSI themes give `subtle` the value of `inactive`. The desktop dark theme drew the empty cells mid gray at the review look. Say that the colorblind themes draw `success` in blue. Then rerun the AC3 sweep and read each hit.
- [x] T9: Review return (R5, R6). Reflow the edited CHANGELOG and DESIGN band paragraphs to even wraps. Name `no file` beside `no milestone file` as a warning text in README and CHANGELOG.
- [x] T10: Review return (R7). Remove the unused `dimColor` field from `Span` in `band.ts` and its branch in `style()` in `register.tsx`. Run the verify slot.

## Work log

- 2026-10-02: created by /milestone-plan.
- 2026-10-02: criteria audit (full mode, fresh Opus reader) returned 12 findings on the first draft. The plan fixed all 12 and asked the operator none of them. Among the fixes: the leaf walk is scoped to `cairn-band` and runs on both surfaces, space-only leaves are exempt, the empty cells keep their props, the close Button is named unchanged, and the accent check uses rows that draw a bar.
- 2026-10-02: the criteria re-audit after the gate (full mode, same reader) returned 5 findings. The plan fixed all 5: the filled cells keep the phase's hue, the walk asserts a skill row per skill, the AC3 sweep covers every color word, T1 names the arrow test, and AC4 stays at one theme.
- 2026-10-02: plan gate chose each phase's own hue drawn dim over one orange for both, at the operator's request for two distinct muted colors. Falsified by a live look where a dim hue reads as bright as today.
- 2026-10-02: plan chose dim theme keys over fixed mid-tone colors, because theme keys follow the light, dark, and colorblind themes. Falsified by a desktop live look where `dimColor` on a colored leaf draws at full strength.
- 2026-10-02: plan gate chose to leave the font over trying the `Code` element, because `Code` draws in the engine's colors, not the plugin's. Falsified by a mod API release that gives `Text` a font prop.
- 2026-10-02: implement started on m198-muted-band. No question gate: `inactive` is a theme key in the 2.1.286 binary, and the plan left nothing else open.
- 2026-10-02: T1–T3 done. Tests first: 76 red on the color asserts alone. `band.ts` exports `GRAY = 'inactive'`, and the labels and filled cells carry `dimColor`. `register.tsx` draws the arrow, positional label, and text in gray. The M197 AC3 skill-row bar assert (about line 1720) also changed to dim filled cells, a sub-task the plan did not name. Two planted defects turned the AC2 walk red: the slash command with no color failed only the 6 skill-row drawings, and dim counts failed 22. Verify clean: scripts 394, hooks 174, validate passed with warnings, mod tests 506/506.
- 2026-10-02: T4 done. The sweep found 16 hits before the edit. README, CHANGELOG, and DESIGN now state the dim label and filled cells and the gray rest of the row. The second sweep's hits each state the new colors, or name the close button's dim `✕`, which the Scope leaves as it is.
- 2026-10-02: T5 first live look (desktop, dark theme): the gray text read closer to the app's bar, but the dim `claude` orange drew brown. This fires the plan's falsifier for dim theme keys. The operator chose fixed mid-tone colors at a chip.
- 2026-10-02: T5 look build B. The label and filled cells take `rgb(194,122,92)` for implement and `rgb(106,165,122)` for review, with no `dimColor`. The tests follow. AC1 is not yet amended, and the amendment waits for the look. Mod tests 506/506.
- 2026-10-02: T5 look B: the operator found the implement label right, but the filled orange cells too close to the gray empty cells. Look build C gives the empty cells the theme key `subtle` (`rgb(80,80,80)` in the CLI dark theme) with no `dimColor`. Mod tests 506/506.
- 2026-10-02: T5 look C: closer, but the operator still found too little contrast in the bar. Look build D keeps the muted label and gives the filled cells the theme keys `claude` and `success` at full strength. Mod tests 506/506.
- 2026-10-02: T5 look D: the operator confirmed the bar now reads right. T5 done.
- re-audit: AC1 (full) — nothing
- re-audit: AC2 (full) — nothing
- re-audit: AC3 (full) — the docs still describe build A, so a new T6 reruns the sweep. The `-w` sweep missed `dimColor`. "Darker gray" is false in the light theme. All three fixed before the gate.
- re-audit: AC4 (full) — a live look needs a row that draws a bar. Fixed before the gate.
- 2026-10-02: substantive amendment at the mini gate, operator's choice. Scope In, AC1, AC2, AC3, and AC4 now name the look D design: labels in fixed `rgb(194,122,92)` or `rgb(106,165,122)`, filled cells in `claude` or `success` at full strength, empty cells in `subtle`, no `dimColor`. A new T6 reruns the AC3 sweep, and the verify task is now T7. The Goal still says "dim". The operator chose to log this departure over a re-plan: the label is a fixed muted color, and the filled cells draw at full strength.
- re-audit: AC3 (full) — "three things" named four, and the sweep's words can miss T6's new wording. Fixed by the reader's own replacement text. This is AC3's second line, so no further reader runs for it.
- re-audit: AC4 (full) — nothing
- 2026-10-02: T6 done. README, CHANGELOG, and DESIGN now name the fixed label colors, the full-strength filled cells, and the `subtle` empty cells. README's "The phase label is drawn" paragraph says the four things AC3 names. The other sweep hits are the close button's dim `✕` and two "greenfield" lines.
- 2026-10-02: T7 done. Verify clean: scripts 394, hooks 174, plugin validate exit 0, mod tests 506/506.
- claim audit: 51 claims read, 5 corrected — hooks/status/band.ts, hooks/status/band.test.tsx, README.md
- 2026-10-02: the same reader re-read the 5 corrections, and one DESIGN.md line fixed in the same spirit. All hold. Mod tests 506/506. Status set to review.
- 2026-10-02: review return 1 (defect track): AC3 failed. Two band claims in README and CHANGELOG are false in the ANSI and colorblind themes (R1, R2). Operator chose send-back at the gate, with R5, R6, and R7 fixed in the same return as T8-T10. R3 and R4 went to a candidate row. Status set to in-progress.
- 2026-10-02: AC4 not yet confirmed. The operator's desktop screenshot of look D showed the label muted orange and the green filled cells apart from visible empty cells. The empty cells drew mid gray, not near the background, and the row text read lighter than the app's own bar text. AC4 is put to the operator again at the re-review.
- 2026-10-02: implement resumed on the return. No question gate: T8-T10 leave nothing open.
- 2026-10-02: substantive amendment at the mini gate, operator's choice: AC3 no longer requires README to say the empty cells are "near the background". R1 showed that required text false in the ANSI themes and in the review screenshot. AC3 already had two re-audit lines, so the change went to the operator with no reader. The criterion narrows, and nothing widens.
- 2026-10-02: T8 done. The 2.1.286 binary sets `success` blue in both colorblind themes, `claude` to `ansi:redBright` in both ANSI themes, and `subtle` equal to `inactive` there. README and CHANGELOG now say so and drop "near the background". The AC3 sweep's band hits each read true. The `band.ts:25` comment still says "near the background" and goes with T10. Verify clean: scripts 394, hooks 174, plugin validate exit 0, mod tests 506/506.
- 2026-10-02: T9 done. The band paragraphs M198 edited are reflowed: CHANGELOG lines 38-56, README 102-122, and DESIGN 77-115, with no inline code span split across lines. A word diff shows only the new `no file` words in README and CHANGELOG. Verify clean: scripts 394, hooks 174, plugin validate exit 0, mod tests 506/506.
- 2026-10-02: T10 done. `Span` has no `dimColor` field, and `style()` has no `dimColor` branch. The only `dimColor` left in the band is the close Button's, which Scope keeps. The `EMPTY` comment now says the light and dark themes set `subtle` fainter than `inactive` and the ANSI themes set it equal. Verify clean: scripts 394, hooks 174, plugin validate exit 0, mod tests 506/506.
- claim audit: 17 claims read, 0 corrected — README.md, CHANGELOG.md, hooks/status/band.ts, hooks/status/register.tsx (the return's added lines, 950ad5e..HEAD)
- 2026-10-02: the claim reader noted the colorblind themes also draw Claude orange brighter, `rgb(255,153,51)`. The docs list only the changes that alter a hue, so they stay as written. Status set to review.

## Decisions

## Review

Evidence from 2026-10-02, on the branch after merging main at 6b23b01 (a ROADMAP stamp change only).

- AC5: `scripts/tests` 394 tests OK (21 skipped), exit 0. `hooks/tests` 174 tests OK, exit 0. `claude plugin validate` (2.1.286 binary) passed with warnings, exit 0. `claude plugin test .` 506 pass, 0 fail, exit 0.
- AC1: The 506 green mod tests include the AC2 walk. On every row it draws, the walk asserts the label hue and the cell keys, with no `dimColor`. The hues are `rgb(194,122,92)` and `rgb(106,165,122)`. The cell keys are `claude`, `success`, and `subtle`. The label-color table holds two bar rows. They are `single-in-progress` with no skill, and M010 in `mixed` under `/milestone-review`. In `band.ts`, the label takes `ORANGE` or `GREEN`. The filled cells take `phase.fill`, and the empty cells take `subtle`.
- AC2: The walk is the `describe` at `band.test.tsx` line 1799, green in the 506. It runs every fixture under `hooks/status/fixtures/` with no skill, `/milestone-review`, and `/milestone-plan`. It draws each on the `terminal` and `desktop` surfaces at 120 and 36 columns. Each leaf in `cairn-band` must be `inactive` with no `dimColor`, or `warning` for the two warning texts. The label, the cells, and space-only leaves are exempt. A drawn row must hold at least one leaf. A first test pins the three no-row fixtures. Under each skill those three draw a `skill-row`, so the walk sees a skill row per skill. The id and a positional label are asserted bold, and the close Button keeps its M197 props.
- AC3: The AC3 `git grep` sweep returns 28 hits. Each band hit states the new colors or stays true: CHANGELOG lines 41-44, README lines 91-93, 102-109, and 125-126, and DESIGN lines 81-86 and 105-106. The close button's dim `✕` (CHANGELOG 21, README 169, DESIGN 93) is unchanged by Scope. CHANGELOG 853 and DESIGN 9 are "greenfield". README's "The phase label is drawn" paragraph names the muted orange or green label and the full Claude orange or success green filled cells. It also names the subtle gray empty cells near the background and the theme's gray for the rest of the row.
- Consistency gate: `cairn_validate.py` exit 0, all checks passed. No principle changed, so `cairn_impact` is skipped. The `generic` profile names no toolchain checks.
- AC3 unticked after the review: findings R1 and R2 show two band hits false in some themes. The 2.1.286 binary was read to confirm both. The AC3 line above stands as written and is wrong for those hits.

Findings, from three fresh reviewers (Opus diff, Sonnet history, Sonnet prior review), most severe first. The prior-review PR-comment probe found no threads. Each line gives the proposed disposition, and the gate records the final one.

- R1 (Opus, history): "the empty cells draw in the theme's subtle gray, near the background" (README 91-92 and 106-107, CHANGELOG 42) is false in the ANSI themes. There `subtle` equals `inactive` (`ansi:blackBright` light, `ansi:white` dark). AC3 fails. Proposed: fix now.
- R2 (Opus): "your theme's full Claude orange or success green" (README 104-105, CHANGELOG 41-42) is false in the colorblind themes, where `success` is blue. AC3 fails. Proposed: fix now.
- R3 (Opus, history): the fixed label colors no longer follow the light, colorblind, or ANSI themes. The orange and green have near-equal lightness, so a red-green colorblind reader can confuse them. The label text still differs. Proposed: follow-up candidate row.
- R4 (Opus, history): the labels' contrast on a white background is unchecked, about 2.9:1 for the green and 3.4:1 for the orange. AC4 looked at the dark theme only. Proposed: follow-up, with R3.
- R5 (prior review, history): ragged wraps in the edited CHANGELOG band paragraph ("cells with `█`. In a narrow window the right part") and DESIGN ("labels. `band.ts` measures the parts"). Earlier reviews (M193, M195, M196) fixed this at their gates. Proposed: fix now.
- R6 (history): CHANGELOG 43 and README 109 name `no milestone file` as the warning text but not its short form `no file`. Proposed: fix now.
- R7 (Opus, history): `dimColor` on `Span` (`band.ts:20`) and in `style()` (`register.tsx:210-213`) is now dead code. Proposed: fix now.
- R8 (Opus): the AC2 walk never draws a bar with no filled cells. The empty `''` filled leaf is exempt as space-only, and no fixture draws a bar at 36 columns. The leaf draws nothing, and AC1 holds wherever cells exist. Proposed: reject.
- R9 (Opus): the walk matches the bold and warning rules by leaf text, and its Button lookup is not scoped to `cairn-band`. No fixture collides. Proposed: reject.
- R10 (Opus): the M197 skill-row bar test checks only the empty run's color. The AC2 walk covers the rest. Proposed: reject.
- R11 (all three): the Goal still says "dim", and the title says the band matches the app's bar. The work log records the operator's choice to keep the Goal. Proposed: reject, already logged.
- R12 (history): the M196 and M197 archive summaries still say "dim". Archives are history and are not edited. Proposed: reject.

Gate dispositions, 2026-10-02: R1 and R2 fix now, as a return to in-progress (T8). R5 and R6 fix now (T9). R7 fix now (T10). R3 and R4 follow-up, as the candidate row "Band label colors in other themes". R8-R12 rejected for the reasons given above. AC4 is open, and the operator was not sure of the look.

Re-review evidence from 2026-10-02, on the branch at 382d85c. The branch already holds `origin/main` (merge base 95680db), so no merge was needed.

- AC5 (re-review): `scripts/tests` 394 tests OK (21 skipped), exit 0. `hooks/tests` 174 tests OK, exit 0. `claude plugin validate .claude-plugin/plugin.json` (2.1.286) passed with warnings, exit 0. `claude plugin test .` 506 pass, 0 fail, exit 0.
- AC1 (re-review): in the same 506, the label-color table at `band.test.tsx` line 361 holds the two bar rows AC1 names. It asserts the label hue, the filled key (`claude` or `success`), and `subtle` on the empty run, each with no `dimColor`. The walk asserts the same on every row it draws. In `band.ts`, `PHASES` gives `ORANGE` and `claude` to implement and `GREEN` and `success` to review, and `skillColor` gives `GREEN` only to `milestone-review`. `Span` has no `dimColor` field.
- AC2 (re-review): the walk at `band.test.tsx` line 1799 ran 45 tests, one per fixture and skill state: the 15 fixtures in `fixtures.gen.ts`, the same 15 names as `hooks/status/fixtures/`, by no skill, `/milestone-review`, and `/milestone-plan`. Each test draws on `terminal` and `desktop` at 120 columns (the `BAND` default) and 36. All 45 pass.
- AC3 (re-review): the sweep returns 25 hits. The band hits each state the colors drawn or stay true: CHANGELOG 41-46, README 91-93, 102-112, and 128-129, and DESIGN 81-86 and 104-105. They name the colorblind blue, the ANSI bright red, and the ANSI `subtle` equal to the row's gray. None says "near the background". The close button's dim `✕` (CHANGELOG 21, README 172, DESIGN 92) is kept by Scope. CHANGELOG 855 and DESIGN 9 are "greenfield". README's "The phase label is drawn" paragraph names the four things AC3 lists. They are the muted orange or green label, the full Claude orange or success green filled cells, the subtle gray empty cells, and the theme's gray for the rest of the row.
- Consistency gate (re-review): `cairn_validate.py` exit 0, all checks passed. No principle changed, so `cairn_impact` is skipped. The `generic` profile names no toolchain checks.
