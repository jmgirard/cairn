# M123: Rebuild guard-doctrine §8 so its certification loop converges

**Status:** done (2026-07-30, PR #123 https://github.com/jmgirard/cairn/pull/123)

**Goal:** Rebuild `guard-doctrine.md` §8 so its certification loop terminates on
its own stated rules rather than by maintainer override.

**Outcome:** §8 draws two lines on different axes — subject matter decides what is
checked and fixed (D-069/D-070), provenance decides what reopens. A finding reopens iff
it falls within §8's three named checks AND its only subject is not a **fix-authored
record** (a docstring, comment, work-log line or record claim a previous round's fix
wrote); three classes, one confirmation obligation each, none on the author. The
round-count falsifier — which fired precisely when the instrument had yield — becomes a
three-clause yield-based one, clause (iii) retiring the step whole on round-1 yield
decay. §8 went 46 → 149 lines, derivations relocated to D-085. Guard: 89 tests, 84
registry blocks in §8, sweep 84/84, anchors scoped to the section.

**Decisions:** D-083 (the rebuild; supersedes D-082 part 2, narrows D-067 twice),
D-084/D-086 (measurement corrections), D-085 (relocated derivations, RR10's independent
ground, clause (iii)), D-087 (D-083 part 4 narrowed). None milestone-local.

**Review:** Seven certification rounds, reopening counts 16, 13, 7, 5, 3, 1, 0 — the
gate opened on the rule, no override. One return (AC8/AC11/AC13). Fan-out: 16 findings,
1 ≥80 (A5, a guard false-redding on innocuous edits) fixed. Banked and disclosed: a
rename reusing no word of the term, and a contradicting sentence added elsewhere.
