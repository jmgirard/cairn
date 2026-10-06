# M220: An Implement button in place of the idle row's command

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the status band and pane ship to every plugin user
- **Branch/PR:** m220-band-implement-button

## Goal

The band's idle row starts its milestone from a button labeled `Implement`, and no longer draws the command `/milestone-implement <id>` as text.

## Scope

**In:** `idleLines` in `band.ts` drops the gray command span, so the idle
row's right side is the track alone, and a narrow row drops the track. The
next-step Button label for the `implement` action in `NEXT_LABELS`
(`pane.ts`) changes from `Start` to `Implement`. The band and the pane's
Next Button read that one map (M218), so both read `Implement`. The
Buttons keep their M212 rules. They show while no cairn skill's step is
set and no turn is working, if `actionsFit` passes. When they do not show, the idle
row draws no command in their place. README, DESIGN, CHANGELOG, and the
header comments of `band.ts` and `register.tsx` describe it.

**Out:** The pane's Next pill, which keeps its command text. Milestone rows,
the empty row, and their Buttons. A Button that shows during a turn or a cairn
skill's step. M212 hides it there, and the press items of "Band button
follow-ons (M212, M213 review)" cover it.

## Acceptance criteria

- [ ] AC1: For each fixture that the idle-domain check at
      `band.test.tsx:1688-1690` lists, on the terminal and desktop surfaces,
      at a band width of 120 columns with no cairn skill's step set and no
      turn working, the row draws a Button with key `cairn-next` and label
      `Implement`, then a Button with key `cairn-status`, and no text that
      reads `/milestone-implement`. Mod tests assert the Button keys, the
      label, and the absent text.
- [ ] AC2: While the pane's Next Button shows, it reads `Implement` on every
      `WITH_ROADMAP` fixture whose next action is `implement`. The M218 pane
      test's `ACTION_LABELS` map, and the band test's `LABELS` map, map
      `implement` to `Implement`.
- [ ] AC3: For the `no-active` fixture, on the terminal and desktop
      surfaces, in three cases the idle row draws no `cairn-next` Button and
      no text that reads `/milestone-implement`: while a cairn skill's step is
      set, while a turn is working (`isWorking: true`), and at a band width of
      50 columns. Mod tests assert the three cases.
- [ ] AC4: At a live look in the desktop app, in a fresh Code session in a
      cairn repo other than this one, with a workable planned milestone and
      no active one, the operator sees the idle row's `Implement` Button with
      no command text beside it. The operator presses it and sees
      `/cairn:milestone-implement <id>` start for that milestone. The operator can
      then stop the run, and accepts the look.
- [ ] AC5: README.md and `cairn/DESIGN.md` describe the idle row's
      `Implement` Button, and neither file says that the idle row draws the
      command. CHANGELOG.md's unreleased section has an entry for it.
- [ ] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1
- AC3 → T1, T2
- AC4 → T4
- AC5 → T3
- AC6 → T5

## Tasks

- [x] T1: Write the AC1 to AC3 tests first. Change the tests that expect the
      command text or `Start`: `IDLE_DRAWN` (`band.test.tsx:435-441`), the
      200-column idle test (`band.test.tsx:2019-2047`), the line at
      `band.test.tsx:2585`, `expectedFlow`'s `right`
      (`band.test.tsx:2692`), the `idleLines` width tests
      (`band.test.tsx:1731-1738`), `LABELS` (`band.test.tsx:2916`), and
      `ACTION_LABELS` (`pane.test.tsx:702`).
- [x] T2: In `band.ts`, make `idleLines` return the track alone where it has
      room and an empty tail otherwise (`band.ts:245-256`). In `pane.ts`,
      set `NEXT_LABELS.implement` to `Implement`. Check that `actionsFit` and
      the row loop in `register.tsx:366-392` still read the idle line
      correctly.
- [x] T3: Update README.md (`README.md:170-183`, `README.md:257`),
      `cairn/DESIGN.md` (`DESIGN.md:83`, `DESIGN.md:156-159`), CHANGELOG.md,
      and the header comments of `band.ts` and `register.tsx`.
- [x] T4: Live look (AC4): the operator opens a fresh Code session in
      another cairn repo whose state shows an idle row, such as the
      HiTOP-DAT repo, and presses `Implement` (LESSONS M195, M213).
- [x] T5: Run every `verify` command from the repo root and check each exit
      code.

## Work log

- 2026-10-06: created by /milestone-plan.
- 2026-10-06: collision check: M212 (done) already draws a `Start` Button on the idle row beside the command text, while no step is set, no turn works, and the row fits. No D-entry, no open issue, and no open PR overlaps. Not a checker scope.
- 2026-10-06: criteria audit (full mode, fresh Opus reader) returned findings on AC2 to AC5. AC1 now names the idle-domain check as its domain. AC2 covers every fixture through the existing label maps rather than one exemplar. AC3 names the `no-active` fixture and 50 columns, because "a width with no room" had no fixed value. AC4 moved to another repo, because during review this repo shows the M220 row and a step is set. AC5 now also bars stale text. The instrument note on "Mod tests assert" clauses was answered: the tests carry their expected strings.
- 2026-10-06: question set: label — both the band and the pane read `Implement` (one map).
- 2026-10-06: question set: fallback when the Buttons hide — the idle row shows nothing in their place (the agent recommended keeping the command text).
- 2026-10-06: question set: live look — the operator will look in a fresh session in another cairn repo before review. The operator can stop the run it starts.
- 2026-10-06: plan gate chose one shared label map over a band-only label because the band and pane share it since M218; falsified by a pane reader who needs `Start` there.
- 2026-10-06: plan gate chose no fallback text over keeping the command when the Buttons hide, at the operator's choice; falsified by a session where the next step is hard to find mid-turn.
- 2026-10-06: implement started on m220-band-implement-button. Untracked `cairn-probe.log` and `tsconfig.json` stay unstaged, as they are not milestone work.
- 2026-10-06: T1, T2: the tests changed first (57 red), then `idleLines` dropped the command and `NEXT_LABELS.implement` became `Implement`. With the command's 26 columns free, the track now stays at 40 columns, so the M199 40-column test now asserts the track and no action Buttons. The `idleLines` width test covers where the track goes. Mod tests 1246 pass.
- 2026-10-06: T3: README (the idle row's text block and the pane's label list), DESIGN (the right group and the idle row), CHANGELOG (a New entry), and the `register.tsx` press comment now name `Implement` and no idle command. The `band.ts` header and `idleLines` comments changed in T2.
- 2026-10-06: claim audit: 28 claims read, 3 corrected — CHANGELOG.md (the button now has room 22 columns narrower than before, not "where it showed before"; the row keeps its open and close buttons), README.md (the same, and the `Clear` button after a skill ends)
- 2026-10-06: T4 live look (openac, M21): the operator reports that the idle row shows the Implement and Status Buttons. The press and the look's acceptance are still to come.
- 2026-10-06: T4 live look (openac, M21): the operator pressed Implement, `/cairn:milestone-implement M21` ran, and the row showed no command text. The agent reads this report as the operator's acceptance of the look.
- 2026-10-06: T5: all five verify commands exit 0 (scripts and hooks suites OK, both validates pass, mod tests 1246 pass).
