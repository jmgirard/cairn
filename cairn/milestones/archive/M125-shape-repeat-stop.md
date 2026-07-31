# M125: Certification loops stop on a repeated defect shape

**Status:** done (2026-07-30, PR #125 https://github.com/jmgirard/cairn/pull/125)

**Goal:** End a certification loop by rule when consecutive rounds return the
same defect shape, converting the obligation to a class-closing structural
remedy — termination never again by maintainer override.

**Outcome:** `guard-doctrine.md` §8 gains the shape-repeat stop rule: a finding
clearing both reopening lines, repeating the previous round's reopening
finding's shape, convenes no further round — it obliges a structural remedy
closing the shape's class, confirmed by operation; stopped runs count toward
the falsifier window as run; own falsifier, tolerance one occurrence. §6:
recorded counts carry their producing procedure at verbatim-reproducible
grade. D-091–D-093 appended; rules pinned, harness-registered; §8 ledger
regenerated; M125's certification ended by the rule's first firing, 2 rounds.

**Decisions:** cross-cutting all promoted — D-091 (stop rule, gloss
supersession, count rule, deviation), D-092/D-093 (IP4 corrections); local none.

**Review:** all six ACs on fresh evidence; fan-out 14 findings, 4 actioned —
O4 (92), O5 (90), O6 (82) record corrections appended (two were live
violations of the milestone's own §6 rule); O1 (80) mixed-round precedence
gap parked as a candidate row promoting on the first live mixed round; 10
sub-threshold logged. Nothing graduated or retired.
