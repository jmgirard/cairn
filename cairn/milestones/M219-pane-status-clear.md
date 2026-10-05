# M219: Status and Clear buttons in the cairn pane

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m219-pane-status-clear

## Goal

The cairn pane carries the band's Status and Clear buttons on a row of their own under the Next line.

## Scope

**In:** A new pane line with key `actions` comes right after the Next
line, indented under the pill. It holds the Clear Button, key
`cairn-pane-clear`, after a cairn skill ends (the `ended` atom, M216),
then the Status Button, key `cairn-pane-status`. Both are `secondary` and
use the band's labels, `Clear` and `Status`. The line shows while no cairn
skill's step is set, as the Next Button does (M218). A press runs the band's
press (`pressClear` or `pressStatus` in `register.tsx`), so it runs the same
command and does nothing in the same cases. README, DESIGN, CHANGELOG, and
the header comments of `pane.ts` and `register.tsx` describe it.

The milestone promotes the item "The pane has no Status or Clear Button
(M218 plan)" of "Pane button follow-ons (M218 review)".

**Out:** Changes to the band's Buttons. A pane line that hides while a turn
runs outside a cairn skill. A pane gets no `isWorking` prop, and
`$.command.run` queues a press until the session is idle. That item stays in
"Pane button follow-ons (M218 review)". A test that the pane redraws on a
change to `ended` alone, after a dropped typed prompt. The band's M216 tests
cover that path, and review files the gap in the same row.

## Acceptance criteria

- [ ] AC1: The fixtures with a ROADMAP are `WITH_ROADMAP` in
      `pane.test.tsx`. For each one, on the terminal and desktop surfaces,
      with no cairn skill's step set and no cairn skill ended, the pane draws
      a line with key `actions` directly after the Next line. The line holds
      one Button, with key `cairn-pane-status`, `variant` `secondary`, and
      label `Status`, and no element with key `cairn-pane-clear`. Mod tests
      assert the line's place, that its Button keys are exactly
      [`cairn-pane-status`], and the variant and label.
- [ ] AC2: For one fixture with a next step, on the terminal and desktop
      surfaces, after a cairn skill's prompt starts its step, the pane draws
      no element with key `cairn-pane-status` or `cairn-pane-clear`. After a
      Stop with nothing in flight ends the step, the `actions` line draws a
      Button with key `cairn-pane-clear`, `variant` `secondary`, and label
      `Clear`, then `cairn-pane-status`. After an idle typed prompt that
      follows, the line draws `cairn-pane-status` and no `cairn-pane-clear`.
      A mod test asserts the three states in order.
- [ ] AC3: On the terminal and desktop surfaces, a press of
      `cairn-pane-status` runs `$.command.run` with the command
      `cairn:milestone` and the args `''`. A press of `cairn-pane-clear`,
      drawn after a Stop ends a step, runs the command `clear` with the args
      `''`. Mod tests press each Button and read the command and args that
      reached beneath. A press of `cairn-pane-status` while a run started by
      `cairn-pane-next` is held runs no command, and a mod test asserts this.
- [ ] AC4: At a live look in the desktop app, in a real cairn repo, the
      operator presses the pane's Status Button and sees the status skill
      start. After that skill ends, the operator sees the pane's Clear
      Button, presses it, and sees the conversation clear. The operator
      accepts the look of the Next and actions lines.
- [ ] AC5: README.md and `cairn/DESIGN.md` describe the pane's Status and
      Clear Buttons. CHANGELOG.md's unreleased section has an entry for them.
- [ ] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T4
- AC5 → T3
- AC6 → T5

## Tasks

- [x] T1: Write the AC1 and AC2 tests first in `pane.test.tsx`. Change the
      M218 AC1 test, which asserts that the pane's only Button is
      `cairn-pane-next` (`pane.test.tsx:746`), to read the Next line's
      Buttons alone. In `pane.ts`, give `paneLines` a flag for `ended`.
      While `acts` is true, add the `actions` line after `next`. It carries
      the Buttons to draw, in order. Move `STATUS_LABEL` and `CLEAR_LABEL`
      beside `NEXT_LABELS`, so the band and pane read one place.
- [x] T2: Write the AC3 tests first, with the press pattern of the M218 AC3
      tests (`copy.runHold`, `copy.commands`). In the pane's `ui.render` hook
      (`register.tsx:155-213`), read `ended`. Draw each Button of the
      `actions` line in a Box with `flexShrink` 0. Its `onPress` is
      `pressClear($)` or `pressStatus($)`.
- [ ] T3: Update README.md, `cairn/DESIGN.md`, CHANGELOG.md, and the header
      comments of `pane.ts` and `register.tsx`.
- [ ] T4: Live look (AC4): the operator opens a new Code session in a real
      cairn repo whose state shows a Next line (LESSONS M195, M213). The
      operator opens the pane and presses Status. After the status skill
      ends, the operator presses Clear.
- [ ] T5: Run every `verify` command from the repo root and check each exit
      code.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to build — the pane's Status and Clear Buttons (promotes that item of "Pane button follow-ons (M218 review)").
- 2026-10-04: question set: where the Buttons go — a row of their own under the Next line, lined up under the pill.
- 2026-10-04: question set: a live look in the desktop app before the merge question — yes, one live look.
- 2026-10-04: plan gate chose a row of its own under the Next line over the Next line itself. At the 44-column dock, the pill, Next, Clear, and Status do not fit on one line, and the pill gets cut. An operator rejection of the row at the AC4 look falsifies it.
- 2026-10-04: plan gate chose to show Status whenever no cairn skill's step is set. The band also needs a next-step label, but the pane's Next line exists for every found ROADMAP, because reader.ts `recommend` never returns null. Falsified by a pane state with no Next line in a real session.
- 2026-10-04: criteria audit (full mode, fresh Opus reader) returned 2 minor findings and a wording note. Each went toward the narrower promise. AC1 names the exact-keys assertion for its one-Button and no-Clear claims. T1 changes the M218 test that reds once Status draws. AC2 stays as written. Its three states each rewrite the pane, so the band's M216 tests keep the dropped-prompt path, and Out names it. AC4 says "the status skill" and not `/milestone`. AC3, AC5, and AC6 had no finding. No IP or D-entry blocks a criterion.
- 2026-10-04: collision check: the plan absorbs the Status-or-Clear item of candidate "Pane button follow-ons (M218 review)", and post-merge hygiene trims it. The GitHub inbox has no open issues or PRs. D-143 (the mod ships in the plugin) has no conflict. No D-entry rejects the change.
- 2026-10-04: the new row put ROADMAP.md at 24,117 bytes, over its 24,000 budget. The plan cut two `[low]` rows' asides, to 23,998 bytes.
- 2026-10-04: the plain-English lint hook keeps 12 hits on this file. They are cairn's required `—` slot markers and question-set separators, and three long sentences in the audited criteria, which stay as the audit read them.
- 2026-10-04: implement started on branch m219-pane-status-clear. The untracked `cairn-probe.log` and `tsconfig.json` predate the milestone and stay unstaged.
- 2026-10-04: minor amendment: T1 also draws the `actions` line's Buttons in `register.tsx`, because the AC1 and AC2 tests mount the pane. T2 keeps the presses and their tests.
- 2026-10-04: T1 done. `paneLines` takes `ended` and adds `actions` (indent 6, the Next lead's width) with `['clear', 'status']` or `['status']`. `STATUS_LABEL` and `CLEAR_LABEL` moved to `pane.ts`. The M218 AC1 test reads the Next line's Buttons alone. The press goes through an inline `onPress` to the top-level `pressClear` or `pressStatus` (LESSONS M191). A planted swap of the Clear and Status order turned both AC2 cases red, and it was restored. Verify: all five exit 0, mod tests 1237.
- 2026-10-04: T2 done. Six AC3 tests press Status, Clear after a Stop, and Status during a held Next run, on both surfaces. Planted swapped presses turned the 4 press cases red. A `pressStatus` with no `running` check turned the 2 held-run cases red. Both were restored. Verify: all five exit 0, mod tests 1243.

## Decisions

## Review
