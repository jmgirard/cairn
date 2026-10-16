# M260: Press and placement races end cleanly

**Status:** done (2026-10-15, PR #271 https://github.com/jmgirard/cairn/pull/271)

**Goal:** A rejected session end, an end during a ⌂ press's state read, and an end during a start's second pane listing each leave the pane's Buttons and PR read in the state a person expects.

**Outcome:** `register.tsx`'s `session.end` handler takes the run number and press mark current at its start and, on the resolved and the rejected path alike, frees only those, so a press made while `next(e)` is pending keeps its run. On a rejected end it now frees them before it rethrows and hands a held command to `fallBack` with `the session end failed`, for either reason. `pressHome` returns when `ends` moved during its step read, so its `/clear` does not run; a `clear` end still opens the pane. The classic SessionStart hook snapshots `ends` at entry and, after a session end, reads and owes nothing at either listing. Test kit: a `prompt.fill` record (`copy.fills`). 11 new tests in `pane.test.tsx`. CHANGELOG Fixes entry, README failed-end sentence, DESIGN.md press and start-hook lines.

**Decisions:** none promoted. The plan chose a new `the session end failed` reason over reusing `the session ended before /clear`, and `ends` snapshots over per-press tokens. Planned from the `/milestone` audit's disposition of the six-row pane and press group; the user chose three fixes and pruning the other 15 items.

**Review:** No returns. Criteria audit (full): AC2–AC4 narrowed or made observable. Claim audit 21 claims, 4 corrected. Three lenses, 26 findings: 8 fixed (first-listing end guard, an end freeing a newer press, `pressCheck` and rejecting-`other` tests, fill polling, stale DESIGN/README), 5 to "Rejected end edges (M260 review)", 12 rejected, 1 noted. Copilot (Lite) 2 threads fixed and resolved. Graduated rows: "Pane edges (M238 review)", "Home Button edges (M241 review)", "Plan Button edges (M242 review)", "Shared press mark edges (M243 review)", "Press end edges (M255 review)", "Late placement edges (M256 review)". No lesson captured.
