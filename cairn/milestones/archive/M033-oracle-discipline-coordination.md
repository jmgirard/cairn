# M33: Assess ackwards' oracle discipline and fold its generalizable core into cairn — done 2026-07-12

**Goal.** Assess the oracle discipline ackwards built in its M57 ("Ossify oracles") and fold the
generalizable core into cairn's validation doctrine.

**Outcome.** Strengthened the shared `tracking-rules.md` "Validation doctrine": added the
frozen/live/invariant/closed-form oracle-type vocabulary + "live independent-impl is the stronger
form" nuance, the **≥2 independent oracle *types* per numeric result** bar, and a reproducibility
hard-stop ("no unsourced *or unreproducible* reference value ships") — the priority list preserved,
additions self-contained (no cross-repo citation in the shared rulebook). Captured the assessment in
`references/oracle-discipline-notes.md` (intraclass→ackwards lineage — intraclass originated the
`data-raw/` provenance-script practice, ackwards formalized the registry/taxonomy/guard; E1–E8 gap
ledger). New guard `skills/tests/test_oracle_doctrine.py` locks the anchors.

**Key decisions.** D-024 records the maturation and defers the two **structural** pieces as ROADMAP
candidates, not rejections: adopting `ORACLES.md` as a cairn tracking file (tied to toolchain-profiles;
the D-015/M16 four-wiring-points path) and generalizing the R-specific `provenance`-attr/guard (an R
toolchain-profile slot). Full type-vocabulary folded per the plan gate; registry file held back.

**Review.** All 6 ACs verified fresh; `cairn_validate` 10/10; suites green (4 new + 78 skills + 45
scripts). Two-lens fan-out: F2 (97) — the Review section blew the 150-line cap + left a stale
"validate passes" claim; fixed via the M19/M22 remedy. F1 (68) — ledger E7 used a `split` tag outside
AC1's three-value vocabulary; retagged E7 → `fix-here` at user request.

PR: https://github.com/jmgirard/cairn/pull/31 · merged on local-green (no CI in this repo).
