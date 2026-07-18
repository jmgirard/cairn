# Oracle doctrine validated against intraclass (M42)

**Provenance.** Citekey `oracle-doctrine-intraclass-notes` · ingested 2026-07-12 by M42 from synthesis note — read-only fit assessment of cairn's D-024 doctrine against `jmgirard/intraclass`'s 34-script oracle system.
Pagination: —.
Extraction: read against the intraclass suite at assessment time; that repo has moved on independently since, so the 31/34 classification is a 2026-07-12 snapshot.

_Scope: a read-only fit assessment of cairn's D-024 oracle-type doctrine (the
`tracking-rules.md` "Validation doctrine" section; since M58, 2026-07-16,
extracted to `skills/shared/validation-doctrine.md` — D-031) against `jmgirard/intraclass`'s
real oracle system — the practice cairn's doctrine descends from (D-024). Records
findings that sharpen the doctrine and the two deferred oracle candidates; builds
nothing. Not a cairn tracking authority — status lives in ROADMAP, decisions in
DECISIONS. Evidence snapshot: intraclass @ `/Users/jmgirard/GitHub/intraclass`,
read 2026-07-12._

## What intraclass's oracle system is (T1)

34 `data-raw/oracle-*.R` scripts, each a **seeded, standalone, reproducible
generator** (`Rscript data-raw/oracle-<name>.R`) with a structured provenance
header naming: the oracle ID(s) (O5, O-Bayes, O-cluster-fit, …), the source
(cited DOI or "own seeded output"), the asserting test file, and the reproduction
recipe. Two consumption paths:

- **Expensive oracles → committed frozen fixture.** 24 `tests/testthat/fixtures/
  *-oracle.rds` files, each written by its generator with provenance embedded as
  named fields inside the saved object — `source`, `generated` (date), `dgp`,
  `base_seed`, `n_rep`, `stats` (e.g. `oracle-bayesian.R:252`). Frozen because the
  oracle is a live Stan refit or a 240-rep coverage sim, too slow for CI
  (`test-icc-brms.R:8` — "a single LIVE brms fit, skip_on_cran").
- **Cheap oracles → live recompute in the test suite.** The other ~10 scripts
  are engine-level derivations whose checks (`lme4` cross-engine, published-value
  reduction) run live in `tests/testthat/` (e.g. `test-icc-incomplete.R:72` asserts
  the published Shrout & Fleiss `0.290/0.620`; `:109` refits under `lme4`). No
  fixture — the recompute is cheap, so it stays live.

This split **directly corroborates cairn's D-024 nuance**: "prefer live; freeze it
only when it becomes expensive or network-bound." intraclass froze exactly the
expensive oracles (Stan, 240-rep coverage) and kept the cheap ones live.

## Classification against cairn's four types + per-type counts (T2 / AC1)

Mechanism codes — **CF** closed-form (published/definitional formula recomputed
with dumb code), **LV** live (independent implementation: `lme4`/`psych`/`gtheory`
cross-engine, or cross-engine credible-interval containment), **IN** invariant (two
internal routes agree: reduction pins, `fixed==random` on balanced data,
single-level ties), **FZ** frozen (committed `.rds` w/ generator), **SC**
simulation-coverage — recovery of a **known population parameter** and/or nominal
Monte-Carlo interval **coverage**. Every script carries ≥2 independent mechanisms
(the ≥2-types bar in practice); the **bold** code is the script's *lead* oracle
per its provenance header (for a multi-oracle frequentist script, the header's
first-listed / dominant oracle — a judgment call among co-equal oracles, not a
countable per-type tally).

| # | script (`oracle-…R`) | role | mechanisms |
|---|---|---|---|
| 1 | bayesian | O-Bayes two-way coverage | **SC**, FZ |
| 2 | oneway | O-Bayes-OW coverage | **SC**, FZ, CF |
| 3 | fixed | O-Bayes-Fixed coverage | **SC**, FZ, CF |
| 4 | multilevel | O-Bayes-ML coverage | **SC**, FZ |
| 5 | multilevel-fixed | O-Bayes-FML coverage | **SC**, FZ, CF |
| 6 | nested | O-Bayes-NML coverage | **SC**, FZ |
| 7 | nested-fixed | O-Bayes-FNML (2b) coverage | **SC**, FZ, IN |
| 8 | replicates | O-Bayes-Rep coverage | **SC**, FZ, LV |
| 9 | fixed-replicates | O-Bayes-FRep coverage | **SC**, FZ, CF |
| 10 | multilevel-replicates | O-Bayes-MLRep coverage | **SC**, FZ |
| 11 | conflated | O-Bayes-Conflated coverage | **SC**, FZ, LV |
| 12 | incomplete | O-Bayes-Incomplete coverage | **SC**, FZ, IN |
| 13 | incomplete-oneway | O-Bayes-IOneway coverage | **SC**, FZ, IN |
| 14 | incomplete-fixed | O-Bayes-IFixed coverage | **SC**, FZ, IN |
| 15 | incomplete-multilevel | O-Bayes-IML coverage | **SC**, FZ, LV |
| 16 | incomplete-fixed-multilevel | O-Bayes-IFML coverage | **SC**, FZ, LV |
| 17 | incomplete-nested | O-Bayes-INML-clusters coverage | **SC**, FZ, LV |
| 18 | incomplete-nested-subjects | O-Bayes-INML-subjects coverage | **SC**, FZ, LV |
| 19 | incomplete-fixed-nested | O-Bayes-IFNML coverage | **SC**, FZ, IN |
| 20 | cluster-ck | O-Bayes-cluster-ck coverage | **SC**, FZ, LV |
| 21 | cluster-ck-coverage | frequentist ICC(c,k) coverage | **SC**, FZ |
| 22 | cluster-ck-incomplete | ICC(c,k) point, ≥2 named oracles | **LV**, IN |
| 23 | d-study | D-study projection | CF, LV, **SC** |
| 24 | fixed-cluster-level | fixed cluster-level recovery | **IN**, SC, FZ |
| 25 | fixed-incomplete | O6 fixed incomplete | IN, LV, **SC** |
| 26 | fixed-multilevel | fixed multilevel subject | **IN**, LV, SC |
| 27 | fixed-vs-random | ADR-006 equivalence | **IN** |
| 28 | incomplete-fixed-nested | O-IFNML recovery + coverage | **SC**, IN, FZ |
| 29 | incomplete-multilevel | M9 subject-level ragged | LV, **SC**, IN |
| 30 | incomplete | O5 two-way ragged | LV, **SC** |
| 31 | multilevel | O-ML Design 1 | LV, **SC**, IN |
| 32 | nested-fixed-interval | O-NFI 2b coverage | **SC**, FZ, IN |
| 33 | nested-multilevel | O-NML Design 2/3 | LV, **SC**, IN |
| 34 | sem | O-SEM lavaan engine | CF, LV, **IN** |

**Per-mechanism count (scripts using it — any-use, of 34):** SC **31**, FZ 24,
LV 16, IN 16, CF 6. (Scripts are multi-oracle, so these sum past 34 — the
≥2-types bar in practice.) A precise per-type *defining*-oracle tally is not
reported: for the multi-oracle frequentist scripts the lead oracle among 2–3
co-equal ones is a judgment call. What is unambiguous: SC leads all **20**
Bayesian CI oracles plus every dedicated frequentist coverage oracle
(`cluster-ck-coverage`, `nested-fixed-interval`, …) — each header states "a CI
method's oracle is COVERAGE".

**Doctrine-gap flag.** Only **3** scripts (22 `cluster-ck-incomplete` LV,
27 `fixed-vs-random` IN, 34 `sem` CF/IN) use no SC at all — they rest entirely on
cairn's four types. **The other 31 use SC — simulation-coverage — which maps to
NONE of cairn's four types**, and it is the *lead* oracle for every one of the 20
Bayesian CI oracles and the frequentist coverage oracles. SC is neither frozen
(nothing expensive is committed — the population
value is analytic), nor live (no independent implementation of the estimator), nor
invariant (it checks against an **injected external truth**, not two agreeing
internal routes), nor closed-form (the mechanism is a **probabilistic**
sampling-distribution check — bias/coverage — not deterministic pointwise
agreement). cairn's four types are all deterministic numeric-agreement oracles; SC
is the one probabilistic oracle, and it is essential for interval methods ("A CI
method's oracle is COVERAGE" recurs verbatim across the Bayesian headers). **This
is the concrete Validation-doctrine defect** (see T4).

## PRINCIPLES.md #1 vs cairn's ≥2-types bar (T2 / AC2)

intraclass `cairn/PRINCIPLES.md` #1 ("Oracle-first verification") — an **inviolable**
principle — requires correctness be *established* by numerical agreement with
independent oracles across three categories: **(a)** closed-form / textbook values
(Brennan 2001, Shrout & Fleiss 1979); **(b)** ≥1 established package on the balanced
case (`psych::ICC`, `gtheory`); **(c)** simulation with known population variance
components — and closes: "Every exported estimator must pass **≥2 independent
oracle types**." (#4 adds the reproducibility hard-stop: "No fabricated reference
values … a cited source or a reproducible script committed to the repo (with
seed).")

**Verdict: AGREE on the bar, DIVERGE on the taxonomy.**

- **Agree (the bar itself).** Both demand **≥2 *independent* oracle types** per
  estimator/result. cairn's D-024 bar ("never two instances of one type") is a
  faithful generalization of PRINCIPLES.md #1's "≥2 independent oracle types" —
  unsurprising, since D-024 records cairn's doctrine as *descending from* this
  practice. The reproducibility hard-stop matches too (cairn "unsourced *or
  unreproducible*" ≙ #4 "cited source or reproducible script with seed").
- **Diverge (the type list).** intraclass's (a)/(b)/(c) do not line up 1:1 with
  cairn's frozen/live/invariant/closed-form: (a) ≈ CF (+ FZ when committed);
  (b) ≈ LV; **(c) simulation-with-known-truth has no cairn type at all.**
  Conversely cairn's frozen and invariant are not named in #1 (though intraclass
  *uses* both heavily). So the two taxonomies **agree on the discipline and miss
  each other on membership** — and intraclass's category (c), the one cairn lacks,
  is used by 31/34 of its scripts and leads all 20 Bayesian CI oracles.

## Deferred-candidate fit assessments (T3 / AC3)

**Candidate — `ORACLES.md` registry (ID, type, asserting test:line, source,
provenance): REVISE, keep deferred.** intraclass has **no** `ORACLES.md` file;
its registry is **distributed** — the structured provenance header of each
`oracle-*.R` script plus the embedded `.rds` fields, referenced conceptually
("the O5 registry row", `oracle-incomplete.R:20`). Findings: (1) the registry's
*column shape* (ID, type, asserting test, source, provenance) **matches** what
intraclass records per oracle — the content is real and it scales (34 scripts,
dozens of named oracles, an at-a-glance ≥2-types audit is genuinely hard across
distributed headers, which argues *for* a central index at this scale); but
(2) intraclass proves a **distributed** registry is a viable shape, so cairn must
not assume the central-file form is the only one; and (3) the registry's `type`
column **cannot describe intraclass's oracles until the taxonomy gains the
simulation-coverage type** (T4) — so the registry is *downstream* of the doctrine
fix. Still entangled with toolchain-profiles (domain-specific). → keep deferred,
row sharpened.

**Candidate — R-provenance guard (`provenance`-attr fixture convention +
`test-oracle-provenance.R` guard): REVISE, keep deferred.** intraclass records
provenance as **named fields inside the saved object** (`source`, `generated`,
`base_seed`, `dgp` — `oracle-bayesian.R:252`), **richer** than ackwards'
`provenance`-attr, but with **no blocking guard test** (no
`test-oracle-provenance.R`; discipline is carried by the seeded standalone
generator + the ≥2-types tests, not a fixture gate). Findings: the provenance
*content* principle (source + generator + seed per fixture) is **independently
corroborated** across both exemplars, but the *mechanism* varies — attr+guard
(ackwards) vs. embedded-fields-no-guard (intraclass). Generalizing ackwards'
exact attr+guard into an R profile slot would **over-fit one exemplar**; a profile
slot should mandate the required provenance *content* and leave the *shape* (attr
vs. embedded fields vs. header) to the repo. The two-exemplar shape variance is an
argument **against** premature promotion to a single fixed form. → keep deferred,
row sharpened.

## Doctrine defect and fix (T4 / AC4)

**Defect (confirmed, not null):** cairn's Validation doctrine presents its priority
list and its four-type taxonomy as covering "every numeric result," but omits the
**simulation-coverage** oracle — recovery of a known population parameter and/or
nominal Monte-Carlo interval coverage. This is the defining oracle for interval
estimation and for any estimator lacking a closed form or reference implementation
(31/34 of intraclass's scripts; the practice cairn descends from). A statistical
repo following cairn's doctrine literally would have **no named home for its most
important oracle**, and could not count coverage toward the ≥2-*types* bar.

**Fix (D-025):** **simulation-coverage** added as the fifth first-class oracle
type in the Validation doctrine — priority-list item (5) + the type paragraph —
counting toward the ≥2-types bar like any other type, with the
freeze-only-when-expensive nuance. Locked by `skills/tests/test_oracle_doctrine.py`
(`test_names_the_five_oracle_types` + the coverage-oracle anchor), updated to
assert the fifth type and confirmed failing against the pre-fix doctrine before
the text was added. Not a null result.
