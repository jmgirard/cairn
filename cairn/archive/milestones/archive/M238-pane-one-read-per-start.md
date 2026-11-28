# M238: The pane reads its pull requests once per start, at its first draw when placed later

**Status:** done (2026-10-10, PR #248 https://github.com/jmgirard/cairn/pull/248)

**Goal:** Each `/clear` or `/resume` that finds the cairn pane open leads to one read of its pull requests. The read runs at the start for a placed pane, and at the first draw for a pane placed later.

**Outcome:** In `register.tsx`, a `classic.SessionStart` with source
`clear` or `resume` that lists the pane but not placed sets `owed`, and the
Pane `ui.render` hook clears it before any await and starts `readPrs`. An
open before that draw or a `session.end` clears `owed`. `startRead` marks
the start's one read, set by the reopen, the classic hook, or the owed
draw, and cleared at `session.end`. The classic hook checks it again after
it awaits the pane list. `paneOf` holds the one `$.ui.panes()` call, and
`listedPane` answers null when it throws. 17 M238 tests, mod tests 1609.

**Decisions:** none promoted. Question set: pane edges with none named, so
the plan picked the read-timing edges. A live look was granted for a
drawing change, and none was owed.

**Review:** 1 defect return (AC2: a resume hook that owed, a draw, then the
reopen read twice; Copilot found it too). Claim audits: 28 claims (4
corrected), then 36 (3). Two three-lens passes, 44 findings: 24 fixed, 10
to "Pane edges (M238 review)", 5 rejected, 5 noted. Copilot (Lite): 1
fixed. Not looked at live: the read started from a render hook, since the
API refuses state writes during a draw. No lesson retired or added.
