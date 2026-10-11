# M238: The pane reads its pull requests once per start, at its first draw when placed later

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane is part of the shipped status mod
- **Branch/PR:** m238-pane-one-read-per-start

## Goal

Each `/clear` or `/resume` that finds the cairn pane open leads to one read of its pull requests. The read runs at the start for a placed pane, and at the first draw for a pane placed later.

## Scope

**In:** In `register.tsx`, a `classic.SessionStart` with source `clear` or `resume` that finds the pane listed but not placed owes a read. The Pane's first draw starts it. An open before that draw takes its place. A start that already read owes nothing, and its other start hook starts no second read. One function holds the `$.ui.panes()` call. Update the code comments, README, DESIGN, and CHANGELOG.

**Out:** These items stay in the two "Pane edges" rows: the hotfix filter's exact-string URL compare, the reopen-mark edges, source `fork`, the reload edges, and the code copies. The phase word stays out, because the operator dropped it at the M236 live look. A timer or turn-end read stays out (M224, M230).

## Acceptance criteria

- [ ] AC1: Take a `classic.SessionStart` with source `clear` or `resume` that finds the pane listed but not placed. It starts no pull request read, and the pane's next draw starts one. `claude plugin test .` passes two tests, one per source, one over the `blocked-active` fixture and one over `blocked-prs`. Each asserts that the `gh` fake's `reads` is empty after the start. Each asserts that `reads` holds each blocked row's URL once after the first `ui.render` of the Pane. Each asserts that `reads` does not change after a second draw. Two more tests open the pane between such a start and the first draw, one by `/cairn-pane` and one by the band's open button. Each asserts that the first draw then starts no read. Three more tests assert that the first draw starts no read. In the first, no such start came before the draw. In the second, the start found no pane listed. In the third, the start's `$.ui.panes()` threw.
- [ ] AC2: One process start can raise both `session.start` with a reopen and `classic.SessionStart` with source `resume`. Source `clear` is tested too, as a guard, because no record shows that pairing. In either order, the start reads each blocked row's URL once, before and after the pane's first draw. `claude plugin test .` passes four tests, for two sources and two orders, in a folder marked for reopen. Each asserts that every URL appears once in `reads`. A fifth test makes the reopen's open unplaced, raises `classic.SessionStart`, then draws the pane, and asserts each URL once. A sixth test holds an open's read unsettled. It then raises `session.end` and a `classic.SessionStart` with source `clear` for a placed pane. It asserts that the start reads each URL again.
- [ ] AC3: register.tsx calls `$.ui.panes()` in one function, and every other place that needs the pane's listing uses that function. `git grep -n '\$\.ui\.panes(' -- hooks/status/register.tsx` returns one line that is not a `//` comment.
- [ ] AC4: Four texts state the owed read at the first draw and the one read per start. They are the register.tsx comments, README's pane section, DESIGN.md's `hooks/status/` section (lines near 286-440), and CHANGELOG.md's `## Unreleased` section. The sweep is this command: `git grep -n -e '/resume' -e 'resume`' -e 'first draw' -e 'reads the files twice' -e 'undrawn' -e 'placed pane' -e 'not placed' -- README.md cairn/DESIGN.md hooks/status/register.tsx`. No line it returns states a read trigger or read count that the new code contradicts. DESIGN.md's milestone history list near line 77 is exempt.
- [ ] AC5: The five `verify` commands in `cairn/PROFILE.md` exit 0 on the branch head.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T4
- AC4 → T5
- AC5 → T6

## Tasks

- [x] T1: Write the AC1 and AC2 tests in `hooks/status/pane.test.tsx`, with the `gh` fake's `reads`, `copy.notPlaced`, and the reopen setup near `pane.test.tsx:1375`. Run them and record which fail on the current code. The reopen-first AC2 tests and the AC1 draw tests are expected to fail. The classic-first AC2 tests pass today.
- [x] T2: Owed read (AC1). A `classic.SessionStart` (`register.tsx:241`) that finds a listed, unplaced pane sets a module flag, unless this start already read. The Pane `ui.render` hook (`register.tsx:280`) clears the flag before its first await and then starts `readPrs`. A `/cairn-pane` open, a band open, a reopen, and a `session.end` clear the flag.
- [x] T3: One read per start (AC2). A start hook's read sets a module mark that holds until the next `session.end`, settled or not. While the mark is set, `reopen` (`register.tsx:1066`) and `classic.SessionStart` start no read and set no owed flag.
- [x] T4: One listing function (AC3). Fold the `$.ui.panes()` calls in `command.run`, `isShown`, `isPlaced`, and `markReopen` (`register.tsx:264`, `679`, `690`, `1047`) into one function.
- [x] T5: Docs (AC4). Update the comments at `register.tsx:69-82` and `234-240`, README near lines 339-343, DESIGN.md near lines 318-320 and 425-440, and CHANGELOG `## Unreleased`. Run the AC4 grep.
- [x] T6: Run the five `verify` commands (AC5).

## Work log

- 2026-10-10: created by /milestone-plan with no work named. The question set offered four candidate rows.
- 2026-10-10: question set: which work. Answer: pane edges, with no edges named, so the plan picked them.
- 2026-10-10: question set: live look if the work changes what the pane draws. Answer: yes, one live look. This milestone changes when the pane reads, not what it draws. Also, no blocked or hotfix PR is open to show. So the plan owes no live look.
- 2026-10-10: plan picked three read-timing edges from "Pane edges (M237 review)": placed later, four `$.ui.panes()` sites, and a resumed reopen that reads twice. It also picked the older row's two-start-hooks item. They are behavior fixes in one hook path. The hotfix URL compare stays in the row, because it needs a second goal clause. The phase-color item stays out, because the operator dropped the phase word at the M236 live look.
- 2026-10-10: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-10: collision: the two "Pane edges" candidate rows hold the absorbed items. Their prune waits for post-merge hygiene. M230, M236, and M237 (done) shipped the reads this milestone changes. No D-entry collides. D-143 covers the mod and stands.
- 2026-10-10: plan chose a read at the Pane's first draw over a turn-end check of `$.ui.panes()`. The operator wants no repeating reads, and a turn end can come long after the placement. Falsified by a host where a Pane placed after a start does not raise `ui.render`.
- 2026-10-10: plan chose a per-start mark held until `session.end` over a skip while a read is in flight. A fast read settles before the second hook, and the skip then depends on timing. Falsified by a start that raises a hook after a read without a `session.end` between, where a second read is wanted.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 11 items, 9 with findings, and the plan took all 9. AC1 drops the ↻ case, which cannot happen before a draw, adds `blocked-prs` for more than one URL, and adds the not-listed and throw cases. AC2 names `clear` as a guard, adds the unplaced-reopen case, and T3 takes the per-start mark. AC3's grep catches a call without `await` and skips comments. AC4's grep adds the stale README and DESIGN lines and bounds "agrees". T2 clears the flag before its first await, for two draws at once.
- 2026-10-10: implement started on branch m238-pane-one-read-per-start. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-10: T1 done. 12 tests in `pane.test.tsx` ("M238 AC1" and "M238 AC2" groups). On the current code, 4 fail: both AC1 first-draw tests read nothing at the draw, and both reopen-first AC2 tests read the URL twice. The other 8 pass, as the plan expected. Suite: 1601 pass, 4 fail.
- 2026-10-10: T2, T3, and T4 done in one commit, because the classic start hook used the removed `isPlaced`. `paneOf` holds the one `$.ui.panes()` call, and `listedPane` answers null when it throws. Module flags `owed` and `startRead` do the rest. The engine refused a helper named `listing`, since `readPrs` already declares a const of that name, so it is `listedPane`. The 4 T1 reds pass now. All five verify commands exit 0 (mod tests 1605 pass).
- 2026-10-10: T5 done. The `register.tsx` comments, README near line 343, DESIGN.md near lines 318-325 and 430-434 and its history line 77, and two CHANGELOG Fixes entries describe the first-draw read and one read per start. Each line the AC4 sweep returns was read and agrees.
- 2026-10-10: claim audit: 28 claims read, 4 corrected — CHANGELOG.md, README.md, hooks/status/register.tsx, hooks/status/pane.test.tsx. The double-read entry named the wrong order, the first-draw claim left out the reopen's read and a failed pane list, and a test comment named the wrong cause. The same reader re-read the fixes once and found the failed-list case still missing, which the next commit adds. A new test covers the session-end reset of `startRead`. Removing that reset failed only that test (1605 pass, 1 fail), and the file was restored.
- 2026-10-10: T6 done. All five verify commands exit 0 (mod tests 1605 pass), and `cairn_validate` passes.

## Decisions

## Review
