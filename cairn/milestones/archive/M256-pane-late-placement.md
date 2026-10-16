# M256: Pane reads after late placement

**Status:** done (2026-10-15, PR #267 https://github.com/jmgirard/cairn/pull/267)

**Goal:** A pane placed while a clear start is still listing panes gets its pull-request read at once, and the placed-and-shown test lives in one place.

**Outcome:** The classic `SessionStart` hook in `register.tsx`, after it sets `owed` for a listed but unplaced pane, lists the panes a second time and reads when the pane is now placed and `owed` still holds, so a pane placed and drawn during the first list reads with no further draw. `placedAndShown(mine)` holds the placed-and-shown test for the command's close branch, `isShown`, and `markReopen`. pane.test.tsx gains `Copy.panesHold` (a one-shot `ui.panes` hold that computes its answer first) and `panesHeld` (the held answer), with cases for the late placement over two fixtures, a draw while the second list waits, and the `owed` reset at `session.end`. DESIGN, README, and CHANGELOG describe it, for `/clear` only, since no test drives `/resume`.

**Decisions:** none promoted. Implement named the predicate `placedAndShown` and re-checks `owed` alone after the second listing, since every `startRead = true` write clears `owed`.

**Review:** Three-lens fan-out, 23 findings: 6 fixed (a case for the second listing's `owed` check, the held answer asserted not placed, DESIGN/README/an older CHANGELOG bullet naming the second listing), 5 to the new row "Late placement edges (M256 review)", 12 rejected. "Pane edges (M238 review)" was narrowed. Copilot (Lite) raised 1 thread, already fixed, replied and resolved. The claim audit corrected 4 of 21 claims. No lesson captured: LESSONS.md is at its byte budget.
