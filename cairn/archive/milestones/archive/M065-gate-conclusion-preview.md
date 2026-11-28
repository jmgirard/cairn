# M65: Gate-time conclusion preview — acceptance chips show what's accepted

- **Status:** done (2026-07-16) · PR: https://github.com/jmgirard/cairn/pull/63
- **Priority:** high · **Principles touched:** GP4

**Goal:** a chip that asks acceptance of a produced conclusion (review
findings, subagent verdict, audit result, amended text) always has that
conclusion's substance verbatim in chat above it.

**Outcome:** "Acceptance chips show what's accepted" rule (D-037 verbatim
bar) + cross-reference from "Chips carry choices, not evidence" ("Two
exceptions" now named in Deltas-not-dumps); directives at the five
conclusion-feeding chip steps (plan gate, implement gate + mini gate,
review approval gate, brief RB gate + RR routing, milestone Route); guard
file (8 tests) + 12 mutation entries incl. first registration of the
chips-carry-choices block. Gate-time sibling of M64; origin: live hit in
circumplex (a plan session asked acceptance of an unseen review conclusion).

**Review:** all 5 ACs on fresh command evidence; fan-out F1 (65, "One
exception" under-inclusive) fixed at user direction — the fix itself first
broke M64's registered block via an exit-blind piped chain (M56 recurrence,
self-caught), refixed with the suite's exit code verified.
