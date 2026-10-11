# M241: A ⌂ Button in the cairn pane clears the conversation and brings the pane to the front

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing, because every adopter sees the Button in the cairn pane
- **Branch/PR:** m241-pane-home-button

## Goal

The cairn pane's first line carries a ⌂ Button that clears the conversation and opens the pane, which brings a hidden pane forward.

## Scope

**In:** A `home` Button, labeled ⌂, on the pane's first line before ↻,
shown while no cairn skill's step is set. Its press runs the built-in
`clear`, guarded as the Clear press is but with no `ended` check. At the
session end of that `/clear`, the mod calls `$.ui.open` for the pane. The
pane's Next line loses its Clear Button. The band keeps its own Clear. The
press is the person's consent to drop the conversation, as a press of Clear
is (IP3, DESIGN.md's M221 note). README, DESIGN, and CHANGELOG describe the
change.

**Out:** A close and reopen of the pane, or a pane reset with no clear.
The user chose a clear with the pane brought to the front at the question
set. The two-click press on an unfocused pane stays with the candidate row
"Pane Button takes two clicks (upstream)". The older pane gaps stay with
the "Pane edges (M238 review)" row.

## Acceptance criteria

- [ ] AC1: While no cairn skill's step is set, `paneLines` gives the pane's first line the Buttons `home` then `refresh`. The first line is the first milestone's head line, or the `no active milestone` line. register.tsx draws `home` as a `secondary` Button labeled `⌂` with key `cairn-pane-home`. While a step is set, the first line carries `refresh` alone. Mod tests cover both states on both kinds of first line.
- [ ] AC2: A free press of ⌂ runs the built-in `clear` command once, with empty args. A press is free when no step is set, no Button's run is in flight or held, and no earlier ⌂ press is pending. A drawn ⌂ press runs no command in three guarded cases. They are a run in flight, a held `Plan` or `Implement` command, and a pending ⌂ press. While a step is set, ⌂ is not drawn (AC1). Mod tests assert the `$.command.run` calls in the free case and in each of the three guarded cases.
- [ ] AC3: At the session end of a ⌂ press's `/clear` (reason `clear`), the mod calls `$.ui.open` for the pane exactly once. A session end with any other reason after a ⌂ press calls no open. A ⌂ press whose `/clear` run is refused leaves no pending open, so a later `clear` end from another Button calls no open. A session end with no ⌂ press pending calls no open. Mod tests assert the open calls in each of these four cases.
- [ ] AC4: The pane's Next line carries no Clear Button, with `ended` true or false. It carries Status after the next-step Button as before. The band's Clear Button draws and presses as the existing band tests assert, and those tests pass.
- [ ] AC5: A live look in the desktop app shows ⌂ just before ↻ on the pane's first line. A press of ⌂ there clears the conversation, and the cairn pane stays open. The operator accepts the look.
- [ ] AC6: Three texts describe ⌂ and its press and say that the pane's Next line has no Clear. They are README.md's and DESIGN.md's text on the pane's current behavior, and a new CHANGELOG.md entry. Earlier CHANGELOG entries and the history in DESIGN.md do not change. A reader of the README and DESIGN lines that describe the pane's Next line finds no claim that it carries Clear.
- [ ] AC7: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1, T2
- AC2 → T2
- AC3 → T2
- AC4 → T1
- AC5 → T4
- AC6 → T3
- AC7 → T1, T2, T3

## Tasks

- [x] T1: pane.ts: add `home` to `PaneButton` and `HOME_LABEL = '⌂'`. Give the first line `['home', 'refresh']` while `acts` is true, and `['refresh']` otherwise. Drop `clear` from the Next line and update the `paneLines` comments. Update pane.test.tsx.
- [x] T2: register.tsx: add `PANE_BUTTONS.home` and route `home` in `pressPane` to a new `pressHome`. It returns at once while `busy()`, a step, or its own pending mark is set. Otherwise it sets the mark and runs `clear` through `run`, and a refused run clears the mark. `session.end` reads the mark and clears it at any end. On reason `clear`, it opens the pane unawaited, as the `heldRun` path runs its command. Write the AC2 and AC3 tests.
- [x] T3: README, DESIGN (current-behavior text and the `hooks/status/` entry), and a CHANGELOG entry.
- [ ] T4: Live look in the desktop app (granted at the question set).

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: what one ⌂ press does — clear the conversation, then open the pane so it comes to the front.
- 2026-10-10: question set: the pane's Clear Button — remove it from the pane. The band keeps its Clear.
- 2026-10-10: question set: ⌂ during a cairn skill's run — hidden, as Next and Status are.
- 2026-10-10: question set: a live look in the desktop app at implement — granted.
- 2026-10-10: plan gate chose a `/clear` and an open over closing and reopening the pane, because a Button's `/clear` keeps the pane open (M222). Falsified by a live look where the pane closes or moves after a Button's `/clear`.
- 2026-10-10: plan chose to open at the `clear` session end, not after `run` resolves. A Button's `/clear` run can fail to settle (M216, M221 T1). Falsified by a probe where the run always resolves before the session end.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 10 findings, all fixed in this file. AC2 split held and in-flight runs and added a second ⌂ press. AC3 added a refused run. AC4 named the band tests. AC5 dropped the refill claim, which holds without M241, and the recording clause. AC6 left CHANGELOG history alone and replaced a grep with a reader's check. The open's effect was narrowed to a pane behind another tab.
- 2026-10-10: inbox sweep: no open issues and no open PRs on jmgirard/cairn.
- 2026-10-10: collision check: M219 shipped the pane's Clear, which this milestone removes, as the user chose. M222 shipped the pane kept open across a Button's `/clear`. No candidate row or D-entry overlaps a ⌂ Button.

- 2026-10-10: substantive amendment: AC2 drops the set-step press from its tested guards. ⌂ is not drawn while a step is set (AC1), and `ui.press` presses only a drawn Button. `pressHome` keeps its step check, and no criterion promises it. The deliverable the user sees does not change.
- 2026-10-10: re-audit: AC2 (full) — the "free" definition contradicted the pending-⌂ guard, and the press-time step check had no promise. Fixed the definition, and kept no promise for the step check (narrower).
- 2026-10-10: re-audit: AC2 (full) — "pending" is not defined. The tests covered one in-flight run, one held label, and one kind of first line. Wording kept as audited. The tests now cover Status and Resume runs in flight, both held labels, and both kinds of first line.
- 2026-10-10: implement chose a module mark `homeRun` beside `heldRun` over an atom. A reload must drop a pending press, as it drops `heldRun`. `paneLines` lost its `ended` parameter, which only the pane's Clear read.
- 2026-10-10: T1, T2 done. ⌂ draws before ↻ while no step is set, a press runs `/clear`, and a `clear` end opens the pane. The pane's Clear is gone. 13 old pane tests changed to the new Button lists, and 17 M241 tests added. Mod tests 1625 pass, and all five verify checks pass.
- 2026-10-10: T3 done. README, DESIGN, and a CHANGELOG New entry describe ⌂ and the Next line with no Clear. DESIGN's Known issues line on the pane's Clear is corrected in place. Code comments no longer say the open brings a pane forward, since the API says only that an open id retitles. The live look checks it. The T1/T2 line's "13 old pane tests" was not counted.

## Decisions

## Review
