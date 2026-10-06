# M220: An Implement button in place of the idle row's command

- **Status:** review
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

- [x] AC1: For each fixture that the idle-domain check at
      `band.test.tsx:1688-1690` lists, on the terminal and desktop surfaces,
      at a band width of 120 columns with no cairn skill's step set and no
      turn working, the row draws a Button with key `cairn-next` and label
      `Implement`, then a Button with key `cairn-status`, and no text that
      reads `/milestone-implement`. Mod tests assert the Button keys, the
      label, and the absent text.
- [x] AC2: While the pane's Next Button shows, it reads `Implement` on every
      `WITH_ROADMAP` fixture whose next action is `implement`. The M218 pane
      test's `ACTION_LABELS` map, and the band test's `LABELS` map, map
      `implement` to `Implement`.
- [x] AC3: For the `no-active` fixture, on the terminal and desktop
      surfaces, in three cases the idle row draws no `cairn-next` Button and
      no text that reads `/milestone-implement`: while a cairn skill's step is
      set, while a turn is working (`isWorking: true`), and at a band width of
      50 columns. Mod tests assert the three cases.
- [x] AC4: At a live look in the desktop app, in a fresh Code session in a
      cairn repo other than this one, with a workable planned milestone and
      no active one, the operator sees the idle row's `Implement` Button with
      no command text beside it. The operator presses it and sees
      `/cairn:milestone-implement <id>` start for that milestone. The operator can
      then stop the run, and accepts the look.
- [x] AC5: README.md and `cairn/DESIGN.md` describe the idle row's
      `Implement` Button, and neither file says that the idle row draws the
      command. CHANGELOG.md's unreleased section has an entry for it.
- [x] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

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
- 2026-10-06: the operator approved deleting the M217 done row (its file is archived), which brings the ROADMAP under its line cap. Status set to review.
- 2026-10-06: review started on route (d): no PR yet, main unmoved since the branch was cut.

## Review

Evidence (2026-10-06, review head before fix-now commits; mod tests 1246 pass, 0 fail):

- AC1: the five `the idle row with its track and the Implement Button at 120 columns (M220 AC1)` tests pass, one per fixture in `IDLE_DRAWN`. The idle-domain check (`the hand-written idle rows cover every fixture that draws one`) passes. Each test mounts terminal and desktop, asserts action keys `cairn-next`, `cairn-status`, label `Implement`, and no `/milestone-implement` text.
- AC2: the M218 AC1 tests (42 pass) read `ACTION_LABELS`, which maps `implement` to `Implement` (`pane.test.tsx:702`). `the fixtures reach every action` checks `nextLabel` against the map, and the per-fixture tests check the drawn label. The band's `LABELS` map reads `Implement`, and its 8 `each press runs its command` tests pass.
- AC3: both `no-active: a cairn skill's step, a working turn, and 50 columns each leave no Implement Button and no command (M220 AC3, terminal|desktop)` tests pass.
- AC4: the work log records the operator's openac look: the Buttons showed, the press ran `/cairn:milestone-implement M21`, and the row had no command text.
- AC5: README.md:182 and DESIGN.md:158-159 describe the `Implement` Button. A grep for the idle command block, `track and command`, and `` `Start` `` in README.md and DESIGN.md finds nothing. CHANGELOG.md's Unreleased New section opens with the entry.
- AC6: scripts suite OK (397, 21 skipped), hooks suite OK, both `claude plugin validate` exit 0, mod tests exit 0.

Gate: `cairn_validate` exit 0. Marketplace validate prints no `plugins[N].version` warning. The CHANGELOG entry carries no milestone number.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: CHANGELOG's M218 and M212 entries in Unreleased still say `Start` — rejected (false): the Unreleased section records each change in order, as the M206 entry says the M199 `next` label is gone, and the M220 entry states the rename.
- diff-bug #2: the new CHANGELOG entry compares against unreleased state, and "22 columns" holds only for 4-character ids — fix now: the number is gone; "which read `Start`" stays under the same ordering convention.
- diff-bug #3: at a 44-column dock the pane's Next line leaves its pill about 3 columns — follow-up: "Implement button follow-ons (M220 review)".
- diff-bug #4: no test sums the pane's Next-line Buttons against 44 columns — follow-up: the same row.
- diff-bug #5: DESIGN.md:73's `hooks/status/` list does not name M220 — fix now.
- diff-bug #6: the `register.tsx` header comment does not describe the Implement Button — fix now.
- diff-bug #7: DESIGN.md:158-159 runs past the wrap width — fix now.
- diff-bug #8: the AC3 test's working and 50-column mounts have no positive control of their own — rejected (false): the same test's third mount, on the same fixture and state, shows `ACTION_KEYS` first, and the reviewer confirmed the old code fails the 50-column case.
- diff-bug #9: the 40-column test keeps its track only for the fixtures' id lengths — noted: correct for every fixture the domain check lists.
- blame-history #1: the idle row shows no command while the Buttons hide, which undoes M199's always-shown command — rejected (planned change): the plan gate chose it.
- blame-history #2: the track now stays down to 24 columns, which changes M206's narrow-window rule — rejected (planned change): it follows from dropping the command, and the work log records it.
- blame-history #3: the wider label moves `actionsFit` on milestone rows — rejected (false): `cairn_next.py` names `implement` only when no milestone is active, so only the idle row draws it.
- blame-history #4: the `register.tsx:366-367` comment says the row draws as before M212 — fix now.
- blame-history #5: the rename reverses M212's `Start` — noted: the plan gate chose it.
- blame-history #6: the branch drops the M217 done row — noted: the operator approved it.
- blame-history #7: hand-written expectations changed with the code — noted: the new assertions are independent.
- prior-review #1: the pane pill at 44 columns — follow-up: "Implement button follow-ons (M220 review)" (same as diff-bug #3).
- prior-review #2: "Band button follow-ons (M212, M213 review)" still says the idle command repeats `Start` — fix now.
- prior-review #3: Button fit between 40 and 120 columns is untested with the longer label — follow-up: "Implement button follow-ons (M220 review)".
- prior-review #4: "22 columns narrower" may be 26 — rejected (false): 26 is the track's threshold, and the Buttons' moved 22 for a 4-character id; the number is gone (diff-bug #2).
- prior-review #5: the 24-39 column range is covered only by the `idleLines` unit test — noted.

Fix-now verify (after the fixes): all five verify commands exit 0, mod tests 1246 pass; `cairn_validate` exit 0.

