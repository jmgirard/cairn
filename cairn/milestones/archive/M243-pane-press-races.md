# M243: A second press during a press's checks runs no second command

**Status:** done (2026-10-11, PR #253 https://github.com/jmgirard/cairn/pull/253)

**Goal:** Each band and pane press that runs a command marks itself busy before its first await, so a second such press runs no second command.

**Outcome:** register.tsx gains `pressChecked`, which returns while
`busy()`, sets the shared mark `pressCheck` before its first await, runs
the press's checks, sets `heldRun` for a `clears` command, and releases the
mark right before `run`. `pressNext`, `pressStatus`, `pressClear`,
`pressBlocked`, and `pressCandidate` pass their checks to it, and M242's
`candidateCheck` is gone. `pressHome` keeps `homeRun`. Tests cover double
presses (band Next, Status, Clear, an Implement hold, pane Finish, Status
with ⌂), a later-tick press, and two checks-fail cases. Mod tests 1660.

**Decisions:** none promoted. The question set picked this candidate. The
plan chose one shared mark over a mark per press, and a mark at entry over
setting `running` at entry. Implement added `pressClear` to the row's three
presses and moved ✎ onto the helper.

**Review:** claim audit, 24 claims, 5 corrected. Three lenses and Copilot
(Lite), 25 items: 12 fixed (4 tests, 4 test asserts, 3 DESIGN fixes, the
PR URL), 6 rejected, 6 to "Shared press mark edges (M243 review)" or the
older edge rows, 1 noted. Nothing retired.
