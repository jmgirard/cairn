# M305: Trim the idle pane and separate the candidate levels

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane is what operators see in the desktop app and the terminal
- **Branch/PR:** m305-idle-pane-trim

## Goal

With no active milestone, the cairn pane shows only lines that add something, and it shows where each candidate priority level starts.

## Scope

**In:**
- Remove the `no active milestone` line.
- Hide the Next line, and the blank row before it, when its command is `/milestone-plan` and the Candidates list draws at least one row, whether or not the line names a `[high]` row (the user's choice at the question set).
- Draw a rule line between adjacent drawn priority levels of the Candidates list: an `Svg` on the desktop, a gray `─` run in the terminal.
- If the user's live look rejects the rule, draw `[parked]` rows in a color that differs from the `[low]` rows' color instead (the user's fallback, 2026-10-20).
- Update README, DESIGN, and CHANGELOG.

**Out:**
- The band (status line) stays as it is, with its idle row and its Status button.
- The pane loses its Plan and Status buttons while it is idle with candidates, because the Next line that carries them is hidden. Each candidate line keeps its ✎, and the band keeps its Status button.
- The summary card's layout stays, except for the parked color if the fallback ships.

## Acceptance criteria

- [ ] AC1: The pane no longer builds the `no active milestone` line. `grep -n "'no-active'\|NO_ACTIVE" hooks/status/pane.ts hooks/status/register.tsx` prints nothing. A mod test over a pane state with no active milestone finds no line whose text is `no active milestone`.
- [ ] AC2: `paneLines` returns no line keyed `next` or `next-gap` when no milestone is active, the next step's command is `/milestone-plan`, and at least one candidate line draws. Mod tests cover the bare command and the command that names a `[high]` row, each with `acts` true and false, and a list where only `[parked]` rows draw.
- [ ] AC3: In two other cases the Next line draws as it did before this milestone. The first is a `/milestone-plan` next step with no drawn candidate line: with no candidate rows, with every row hidden by a started token, and with every row hidden because an open hotfix PR names it. There the line keeps its Plan action and Status button while `acts` is true. The second is a `/milestone-implement` next step for a workable milestone while at least one candidate line draws. Mod tests cover each case.
- [ ] AC4: Exactly one of (a) or (b) holds in the shipped code, the one the user's live look kept.
  (a) The rule: one rule line between each two adjacent drawn levels, and none before the first drawn level, after the last, or between two rows of one level. A rule line's key does not start with `candidate-`, it carries no `rowsAbove`, and each candidate line's `rowsAbove` counts every line drawn before it, rules included. Mod tests cover rows in all four levels with at least two rows in one level (3 rules, each at its boundary), rows in one level (0 rules), rows in high and parked only (1 rule), and a level whose rows are all hidden as started (no rule for it).
  (b) The color: a `[parked]` row's mark span and title draw in a color key that differs from a `[low]` row's, in the Candidates list and in the card's level counts, and the `parked` icon's stroke color differs from the `low` icon's. Mod tests assert each.
- [ ] AC5: If the rule ships, it draws on one row. On the desktop surface it draws as an `Svg`, and in the terminal as `Text` of `─` with `wrap="truncate-end"`; mod tests assert the element for each surface. The user's live look in the docked desktop pane, in the dark and the light theme, finds that the rule draws on one row.
- [ ] AC6: README's pane section, DESIGN's pane paragraphs, and CHANGELOG's Unreleased section describe the shipped behavior of AC1 to AC5. Each claim is read against the code in the same session.
- [ ] AC7: The `verify` slot in `cairn/PROFILE.md` is green: both `unittest` suites, the two `claude plugin validate` runs, and `claude plugin test`.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T2
- AC4 → T3, T4
- AC5 → T3, T4
- AC6 → T5
- AC7 → T6

## Tasks

- [x] T1: Remove the `no-active` line (`pane.ts:839`) and `NO_ACTIVE` (`pane.ts:466`). Update the mod tests that expect the line (`pane.test.tsx` near 6002 and 6359; the assertion near 1695 passes either way, so rewrite it to assert the line is absent) and each `rowsAbove` figure it shifts. The `no-active` fixture name stays.
- [x] T2: In `paneLines` (`pane.ts:844-861`), skip the Next line and its `next-gap` when the command is `/milestone-plan` and the drawn candidate list is not empty. Add the AC2 and AC3 tests.
- [x] T3: Add a rule line between adjacent drawn levels in the Candidates loop (`pane.ts:931`), keyed outside `candidate-*`, with a `PaneLine` flag that `register.tsx` draws as a thin `Svg` line on the desktop (a text rule drew as two lines there, LESSONS M286) and as a gray truncated `─` run in the terminal. Check the tests near `pane.test.tsx:6684` and 6739, which treat `candidate-` keys and `rowsAbove` lines as rows. Add the AC4 (a) and AC5 tests.
- [ ] T4: Preview the rule `Svg` in the browser pane in dark and light (LESSONS M204). Then open a new desktop session in `~/github/modelbased`, which has no active milestone and rows in all four levels. `~/.claude/skills/cairn` links to this checkout, so that session loads the branch's mod; check that its pane shows no `no active milestone` line before judging. The user looks in dark and light. If the user rejects the rule, remove it, give `[parked]` its own color key (`PRIORITY_MARK.parked` at `pane.ts:487`, the title color at `pane.ts:936`, the icon stroke at `icons.ts:64`) with the AC4 (b) tests, and append a D-entry superseding D-184's gray-mark clause. Log the look's result and which means shipped.
- [ ] T5: Update README (the pane section near line 345), DESIGN's pane paragraphs, the comments at the top of `pane.ts`, and CHANGELOG Unreleased.
- [ ] T6: Run the `verify` slot.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — changes the lines the cairn pane draws, a runtime surface.
- 2026-10-20: question set: hide the planning Next line also when it names a `[high]` row — yes, hide it whenever a candidate line draws.
- 2026-10-20: question set: live look — in a new desktop session in modelbased before the merge question, granted.
- 2026-10-20: the user named the fallback in chat: if the rule does not work or look good, give parked rows a color that differs from low rows'.
- 2026-10-20: collision check: no candidate row, planned milestone, or D-entry overlaps. M286 dropped a text rule after headings because the desktop drew it as two lines, so the rule draws as an `Svg` there. D-184's pane clause (gray parked mark) and D-182's level order bear on it: the rule draws D-182's order and adds no grouping, so it needs no D-entry; the color fallback would change D-184's clause, so T4 writes that D-entry only if the fallback ships.
- 2026-10-20: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-20: criteria audit (full mode, fresh Opus reader) returned 9 findings, all fixed: AC2 also hides `next-gap` and tests a parked-only list; AC3's implement case now has candidates drawing and its review case was cut (no candidates draw with an active milestone); AC3 adds a row hidden by an open hotfix PR; AC4 says exactly one means ships and drops the work-log promise; AC4 (a) adds a two-row level, an all-hidden level, and the key and `rowsAbove` rules; AC4 (b) adds the icon stroke; T4 names how the branch's mod loads in modelbased; T1's 1695 assertion passes either way; the Next block is `pane.ts:844-861`.
- 2026-10-20: plan gate chose an `Svg` rule on the desktop over a text rule of `─` because M286 saw a one-row text rule draw as two lines there; falsified by a desktop text rule that draws on one row at the 44-column dock.
- 2026-10-20: plan gate chose to try the rule first and the parked color second, in the user's order; falsified by the live look.
- 2026-10-20: implement started on m305-idle-pane-trim; untracked cairn-probe.log and tsconfig.json predate the branch and stay unstaged.
- 2026-10-20: T1+T2 in one checkpoint, since both shift the same row figures in the M294 tests. The card's blank row now draws only before the first milestone, because every later section opens with its own and removing `no active milestone` left two blank rows in a row. The pane's Next line no longer calls `nextTitle`: a drawn `[high]` row hides the line, so a shown planning line names nothing; the band's Plan press still does. Tests that read the planning line in fixtures with drawn rows now loop over `WITH_NEXT`, and the M272/M273 press tests press the band. A drawn row whose short title is empty has no ✎ and still hides the line, as AC2 is written; the band's Plan remains. verify green (mod 2410 pass).
- 2026-10-20: T3: a `rule-<level>` line with `rule: true` before the first drawn row of each level after the first. `register.tsx` draws it as `ruleSvg()` (icons.ts: a 4000-wide markup, `preserveAspectRatio="none"`, the icons' gray at half opacity, one non-scaling pixel, `height` 14 and no `width`) on the desktop, and as `─` repeated to `bodyColumns` less the indent in `subtle`, `wrap="truncate-end"`, in the terminal. Chose a fixed gray at half opacity because an image has no theme signal; the live look judges it in both themes. verify green (mod 2417 pass).

## Decisions

## Review
