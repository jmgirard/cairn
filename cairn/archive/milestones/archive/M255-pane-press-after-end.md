# M255: Pane Buttons recover after a session end

**Status:** done (2026-10-15, PR #266 https://github.com/jmgirard/cairn/pull/266)

**Goal:** A pane Button press whose check was cut off by a session end neither freezes later presses nor runs late, and a ⌂ press still opens the pane when the session-end chain rejects.

**Outcome:** `register.tsx` counts session ends in `ends`. `pressChecked` records the count with its mark, and checks that settle after an end began run and hold nothing. The `session.end` handler counts itself before `next(e)` and clears `pressCheck` beside `running`, after its own updates, so no press reads the ending session's state and a cut-off press leaves the Buttons free. A rejecting `next(e)` at a `clear` end still opens the pane for a pending ⌂ press, then rethrows. pane.test.tsx gains `holdStep` (a one-shot `step` read hold) and `Copy.endThrows`/`endHold`, with cases for a Status press after the end, a cut-off next-step press, a press during a held end, and the ⌂ open with and without a press. DESIGN and CHANGELOG describe it.

**Decisions:** none promoted. The plan kept "open the ⌂ pane only if still listed" out, as unlooked live. Implement opened the pane in a catch and rethrew, keeping the later updates' behavior on a rejection.

**Review:** Three-lens fan-out, 27 findings: 12 fixed (the first fix freed the mark before `next(e)`, letting a new press read pre-end state; an end counter replaced it), 9 to the new row "Press end edges (M255 review)", 2 rejected, 4 noted. "Home Button edges (M241 review)" and "Shared press mark edges (M243 review)" were narrowed. Copilot (Lite) raised 2 threads, both fixed and resolved. The claim audit corrected 3 of 23 claims. No lesson captured: LESSONS.md is at its byte budget.
