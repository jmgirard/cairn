# M42: Oracle-doctrine validation against intraclass — done 2026-07-12

**Goal:** validate cairn's D-024 oracle-type doctrine against `jmgirard/intraclass`'s
real oracle system (the practice cairn descends from); record fit findings and fix
any exposed defect.

**Outcome:** classified all 34 `data-raw/oracle-*.R` scripts
(`references/oracle-doctrine-intraclass-notes.md`). Headline: **31/34 use
simulation-coverage** (recover a known population parameter / nominal interval
coverage) — an oracle mapping to none of cairn's four types, the missing analog of
intraclass's inviolable `PRINCIPLES.md #1(c)` and the primary oracle for every CI
method. `PRINCIPLES.md #1` vs cairn's ≥2-types bar: **AGREE on the bar, DIVERGE on
the taxonomy**. Corroborated D-024's freeze-only-when-expensive nuance. Both deferred
oracle candidates (ORACLES.md registry, R-provenance guard) → **REVISE/keep-deferred**
(registry distributed in intraclass + downstream of the taxonomy fix; provenance
mechanism varies across the two exemplars → mandate content, not shape).

**Key decision:** **D-025** — added `simulation-coverage` as the fifth first-class
oracle type in the Validation doctrine, counting toward the ≥2-types bar; annotates
(not supersedes) D-024. Guard-tested (`test_oracle_doctrine.py`, failed pre-fix).

**Review:** all 5 ACs verified fresh; 3-lens review — diff-bug caught a count-summary
inconsistency (fixed, verified by recount), blame-history + prior-PR clean.

**PR:** https://github.com/jmgirard/cairn/pull/40
