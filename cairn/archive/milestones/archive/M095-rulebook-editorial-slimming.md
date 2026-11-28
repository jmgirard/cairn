# M95: Rulebook editorial slimming — the rulebook states rules, not their legislative history

**Status:** done (2026-07-20, PR #97 https://github.com/jmgirard/cairn/pull/97)

**Goal:** Run the editorial pass on `tracking-rules.md` under the corrected
premise that the rulebook is current knowledge, and leave M96 its first stamp.

**Outcome:** D-056 classifies `skills/shared/tracking-rules.md` as current
knowledge under D-045 — the class both its lists omitted — so justification
recording no decision is deletable against git with no backfill, on D-052(2)'s
reasoning. The rulebook gains the behavioral inversion test and the reddening
asymmetry in "What gets a test" (M98 F4's owed item), guarded by
`test_rule_placement.py` with 5 mutation registrations. Twelve blocks removed,
RR01 rec 7's prune completed: 788 → 779 lines, 54,584 → 53,751 chars.

**Decisions:** D-056 (the license, the three-step placement test, the
guard-pinning asymmetry). Milestone-local: B21 kept on the behavioral test
rather than on its guard; B3 compressed rather than deleted.

**Review:** Three lenses — [O] 1, [S] blame 0, [S] prior-PR 0 (no-op). F1 (78,
sub-threshold, actioned per M73): D-056 asserted a yield floor the pass missed;
fixed pre-merge. Inversion sweep 13 guarded / 0 unpinned. Graduated the
"Rulebook read-cost reduction" row.
