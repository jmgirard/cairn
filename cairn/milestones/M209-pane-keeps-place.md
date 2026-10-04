# M209: The cairn pane stays where it is put

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane draws in every adopter's desktop session
- **Branch/PR:** —

## Goal

Make a cairn pane that the operator moved to another column or resized in the desktop app keep that column and width when the operator switches to another session and back.

## Scope

**In:** The operator reports that the pane goes back to the rightmost column at its first width after a switch to another session in the desktop app and back. A probe finds which mod calls, if any, run at that switch and at a turn end, with the operator moving the pane between them. Change the mod so that none of its calls at those two events puts the pane back. One possible fix is a refresh that writes nothing when the pane state did not change. The `columns` open option is not a fix here, because a width the person dragged wins over it and it sets no column. The CHANGELOG and the README pane section follow.

**Out:** If the probe shows any put-back with no mod call involved, alone or beside a mod cause, the run stops at the goal-wrong stop. Then an upstream report to the desktop app (an outward action, asked at that stop) and a candidate row hold the fix. The pane's candidate rows are M207 and its look is M208. The other "Pane follow-ons (M205 review)" items stay in that row.

## Acceptance criteria

- [ ] AC1: In the desktop app, the operator drags the open cairn pane to another column and resizes it. The pane then keeps that column and that width through three switches to another session and back, and through three turn ends. At least one of those turn ends follows a box checked in the active milestone file. The operator accepts this at a live look.
- [ ] AC2: The T1 probe names each `$.ui.open` call, `$.ui.close` call, or `pane` state write that it skipped in the hot-reload copy and whose skip stopped the put-back. The mod no longer makes that call, or a `pane` write whose value equals the stored one, at that event while the pane is open and shown. The event is the one the T1 work-log line records for the switch or the turn end. A `claude plugin test` case raises that event and asserts this through what the test's mocks record: the opens and closes lists for a call, and the `ui.render` raises for a write. With the call or write restored, the case fails.
- [ ] AC3: `/cairn-pane` still opens a closed pane and closes a shown one, and the band's `≡` button still opens a closed pane. The M205 AC1 and AC4 cases in `pane.test.tsx` stay green, unedited in what they assert.
- [ ] AC4: The four commands of the verify slot in `cairn/PROFILE.md` each exit 0.
- [ ] AC5: CHANGELOG's Unreleased section has an entry for the fix. README's "The cairn pane" section has no sentence that the changed behavior makes false.

## Coverage

- AC1 → T1, T2, T4
- AC2 → T2
- AC3 → T2
- AC4 → T2, T3
- AC5 → T3

## Tasks

- [ ] T1: Probe the cause in a desktop Code session. A copy of the mod in the session's hot-reload folder (LESSONS M205) logs each `$.ui.open`, `$.ui.close`, `pane` write, and `ui.render` to a file kept out of git (LESSONS M201). The operator moves and resizes the pane, then switches sessions and back, and then ends turns. For each call that ran before the pane went back, the copy skips that call alone and the operator repeats the move. A work-log line names the event that reached the mod at the switch and each call whose skip stopped the put-back, or says that no skip did. If no skip did, or the pane also goes back with no call, the run stops at the goal-wrong stop.
- [ ] T2: Change the mod at each event T1 names, in `register.tsx`. Add the AC2 cases, and restore each call once to see its case red.
- [ ] T3: Update the CHANGELOG, the header comment of `register.tsx`, and any README pane sentence that the change makes false.
- [ ] T4: Do the live look in a new Code session (LESSONS M195).

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: collision sweep: no row or archive entry covers the pane's placement. M205 shipped the pane (done), and its `ui.open` call passes no `columns`. No D-entry conflicts (D-143 read). Inbox: 0 open issues, 0 open PRs.
- 2026-10-04: plan routed the placement bug through a milestone and not `/hotfix`, because its cause is unknown and a regression test needs the probe first.
- 2026-10-04: question set: snap-back. The operator sees the pane go back after switching to another session in the desktop app and back. The probe tests that switch first, and the turn end as the mod's own refresh.
- 2026-10-04: criteria audit (full mode, user-facing tier, fresh Opus reader) returned 12 findings over M207 to M209, all taken. Here: AC2 holds only while the pane is open and shown, so AC3's opens of a closed pane stand. AC2 names the calls the mod makes and what the test's mocks record for each. A turn end follows a checked box. Any put-back with no mod call stops the run. AC3 names the M205 cases in `pane.test.tsx`. The goal names the two events as the whole domain.
- 2026-10-04: operator note after the plan commit: only the cairn pane goes back after a session switch. The app's own panes keep their column and width. T1 therefore also logs each event that reaches the mod at the session's return (a `session.start`, a new `ui.render`, a re-seat of the pane), and compares a pane opened with `columns` against one opened without.
- 2026-10-04: the T1 probe and the T4 live look are stops for the operator's eyes on the closed list. An upstream report is an outward action, asked only at the goal-wrong stop.
- 2026-10-04: criteria re-audit (full mode, same fresh Opus reader) of AC1 to AC5 after the snap-back answer returned 5 findings, all taken. AC2 and T1 name a call only when skipping it stops the put-back, so order alone is not a cause. AC2 removes only a `pane` write of an unchanged value, so AC1's checked-box turn end still updates the pane. The event is the one T1 records for the switch. The `columns` lever left Scope, because a width the person dragged wins over it. AC1, AC3, AC4, and AC5 were clean.
- 2026-10-04: plan chose a skip-and-repeat probe over reading the call order alone, because a refresh can run before an app-side re-seat without causing it. Falsified if a skip stops the put-back yet the shipped change does not.

## Decisions

## Review
