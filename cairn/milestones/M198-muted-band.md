<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M198: A muted band that matches the app's own bar

- **Status:** in-progress
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

- [ ] AC1: The phase label and a cairn skill's label draw in a fixed muted color with no `dimColor`: `rgb(194,122,92)` for the implement hue and `rgb(106,165,122)` for the review hue. A skill's label takes the review hue for `/milestone-review` and the implement hue for every other skill. The phase label takes its phase's hue. The bar's filled cells take the phase's theme key with no `dimColor`: `claude` for `implement` and `success` for `review`. The empty cells take the theme key `subtle` with no `dimColor`. The AC2 walk checks this on every row it draws. The label-color table in `band.test.tsx` also checks two rows that draw a bar. They are `single-in-progress` with no skill, and M010 in `mixed` under `/milestone-review`.
- [ ] AC2: Every other Text leaf inside the `cairn-band` Box takes the theme key `inactive` with no `dimColor`. There are two exceptions. A leaf that holds only spaces is exempt. `no milestone file` and `no file` keep `warning`. A test in `band.test.tsx` draws every fixture under `hooks/status/fixtures/` on both surfaces, at the default width and at 36 columns. It draws each fixture with no skill, with `/milestone-review` running, and with `/milestone-plan` running. It walks every Text leaf inside `cairn-band` and asserts the color rule above for each leaf. A drawing that shows a row must hold at least one leaf. `no-active`, `no-roadmap`, and `repo-at-cut` draw no row with no skill. The walk must see at least one skill row for each of the two skills. The id and a step's positional label stay bold. The close Button keeps its M197 props.
- [ ] AC3: The docs describe the new colors. The sweep is `git grep -n -iE 'orange|green|gray|grey|colou?r|dim|muted|subtle|inactive|tint|hue' -- README.md CHANGELOG.md cairn/DESIGN.md`. Each hit about the band states the colors this milestone draws, or stays true under them. README.md's paragraph that begins "The phase label is drawn" says four things. The label draws in a muted orange or green. The filled cells draw in the theme's full Claude orange or success green. The empty cells draw in the theme's subtle gray, near the background. The rest of the row draws in the theme's gray.
- [ ] AC4: A live look at a new desktop Code session, on a row that draws a bar, shows the band's text in gray and its label in a muted orange or green. The filled cells stand apart from the empty cells, and the empty cells stay visible. The operator confirms this at the review chip.
- [ ] AC5: The verify slot of `cairn/PROFILE.md` runs clean: `python3 -m unittest` over `scripts/tests` and `hooks/tests`, `claude plugin validate`, and `claude plugin test`.

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
- [ ] T6: Rerun the AC3 sweep against the look D colors and fix each hit, the labels' fixed colors included.
- [ ] T7: Run the verify slot.

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

## Decisions

## Review
