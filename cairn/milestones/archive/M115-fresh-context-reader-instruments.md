# M115: Fresh-context reader instruments — plan-gate criteria audit and independent description-layer certification (RR06 recs 4–5)

**Status:** done (2026-07-26, PR #115 https://github.com/jmgirard/cairn/pull/115)

**Goal:** Adopt RR06's two fresh-context reader instruments — a criteria audit at the
plan and RR-ingest gates, description-layer certification before review — retiring
author self-certification of guard coverage as a D-059-shaped move.

**Outcome:** Two `[O]` readers, neither mechanized. The **criteria audit**
(`/milestone-plan` step 3, `/milestone-brief` RR ingestion) asks of each criterion, and
of a binding-criteria set as a whole, what state of the world satisfies it as written
and whether any IP or D-entry makes that state unreachable; criteria authoring moved
step 4 → step 2 so the reader sees shipped bytes. **Certification** is
`guard-doctrine.md` §8 — clause-to-assert coverage, claim-vs-file accuracy,
anchor-vs-bytes fidelity, at zero unresolved — fired by `/milestone-implement` step 8
on any guard-touching milestone; operation stays with the author. 27 asserts / 27
entries; `tracking-rules.md` and `scripts/` untouched. Unblocks M114.

**Decisions:** D-067 (both adoptions, the retirement, and why D-064–D-066 are reserved
for M114's unmerged branch). Gated amendments: AC2/AC6 after a plan-time criteria
re-read; AC5's ambiguous `verbatim` settled at the gate.

**Review:** Blame-history and prior-review zero findings; diff-bug seven, two actioned.
F1 (92) an advisory count stated inside the file the advisory scans. F7 (80) the
certifier's tier unnamed where §8 fires. Logged: F2 65, F6 58, F4 55, F3 42, F5 25.
