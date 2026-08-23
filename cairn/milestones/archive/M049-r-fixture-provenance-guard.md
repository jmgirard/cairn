# M49: R fixture-provenance guard fold-in (done 2026-07-13)

**Goal:** Fold a reproducible-fixture-provenance requirement into the
`r-package` profile's `test-doctrine`, mandating the provenance *content*
while leaving its *shape* to the repo.

**Outcome:** The r-package profile `test-doctrine` slot now mandates that every
committed test fixture carry reproducible provenance — its source + a committed
generator (a `data-raw/` script that regenerates it) + any seed — the
R-mechanical concretization of the universal "Reproducibility (hard stop)". The
required *content* is fixed; the *shape* (a `provenance` attribute, embedded
`.rds`/`.rda` fields, or a header comment) is the adopting repo's choice. Locked
by `TestRPackageFixtureProvenance` in `test_toolchain_profiles.py` (content
tokens + shape-freedom). Profile 76 lines (< 90 cap); all verify suites green.

**Key decision:** D-028 — mandate provenance *content*, leave the *shape* free;
rationale = the two-exemplar variance (ackwards' `provenance`-attr + guard test
vs. intraclass's embedded `.rds` fields); no guard *test* mandated on the
adopting repo; supersede path stated. Executes the D-024/D-025-deferred
"R-profile provenance guard" candidate (graduated at this completion).

**Review:** three fresh-context lenses, zero findings; consistency gate green
(`cairn_validate` all-pass, coverage complete).

**PR:** https://github.com/jmgirard/cairn/pull/47 (squash `6890b7e`).
