# Toolchain profile: r-package

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in tracking-rules. All six `## <slot>` sections
     are defined; cairn_validate FAILs on a missing or empty slot. -->

The R-package toolchain: devtools/roxygen/testthat/pkgdown, CRAN release.
Selected by `cairn-init` when a `DESCRIPTION` file is present.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite):
- After roxygen changes: `Rscript -e 'devtools::document()'`.
- After code changes, before a task is checked off: `Rscript -e 'devtools::test()'` clean.
- `/hotfix` gate-lite: `devtools::test()` clean; `devtools::document()` if
  roxygen changed; `devtools::check()` if anything structural was touched.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- `devtools::document()` produces no diff.
- Generated files are never hand-edited: `NAMESPACE`, `man/`, and `data/*.rda`
  regenerate from roxygen and `data-raw/` scripts (the no-diff `document()`
  check catches drift).
- README.md is knitted from README.Rmd; present and out of sync with README.md → `devtools::build_readme()`, commit.
- pkgdown site present → `pkgdown::check_pkgdown()` passes (catches exports missing from `_pkgdown.yml`).
- NEWS.md has an entry for this milestone's user-visible changes (no milestone numbers in user-facing text).
- New top-level files have `.Rbuildignore` entries (check `check()` NOTEs).
- Full check at review: `Rscript -e 'devtools::check()'` clean (0 errors, 0 warnings; justify NOTEs).

## test-doctrine
R-mechanical test expectations layered on the universal "What gets a test"
rules in tracking-rules:
- Every exported function: happy path, every `cli_abort()` branch fired, R
  edge cases — zero rows, `NA`, length-one, factor vs. character, empty strings.
- New user-facing conditions use `cli::cli_abort()` / rlang, not assertthat.
- Indirect by default: internal helpers (direct tests only for independent logic).
- Never test print cosmetics beyond meaningful snapshots, trivial pass-throughs,
  dependency behavior, or plots except `vdiffr` when the plot is the product.
- `covr` is a diagnostic, never a gate.
- Dependency changes (Imports/Suggests) are never unilateral — question-gate + D-entry.
- Breaking changes to exported behavior follow a deprecation cycle unless pre-1.0 and explicitly waived.
- Every newly exported object gets a `_pkgdown.yml` reference-index row in the same commit.

## release-walk
Followed by `/cairn-release` — a CRAN release walk (never self-submits):
- Version decision (patch/minor/major) from NEWS.md; pre-1.0 conventions per DESIGN.md.
- NEWS consolidation: retitle the dev heading to the version; group entries; prune noise.
- Full local verification: `devtools::document()` (no diff), `devtools::test()`
  and `devtools::check()` clean, `devtools::build_readme()`, `pkgdown::check_pkgdown()`,
  `urlchecker::url_check()`.
- Wide checks as applicable: `devtools::check_win_devel()` and/or R-hub; `revdepcheck` if dependents exist.
- Update `cran-comments.md` (test environments, check results, NOTE justifications, revdep summary).
- Bump `Version:` in DESCRIPTION.
- Handoff checklist (user runs): `devtools::submit_cran()`, confirm the CRAN
  email, then `usethis::use_github_release()` + `usethis::use_dev_version()`.

## init-detection
Recognized by `cairn-init` when a **`DESCRIPTION` file is present** at the repo
root. Carries the `.Rbuildignore` `^cairn$` entry (keeps the tracking dir out
of the built package).

## greenfield-openers
Opener questions `cairn-init` asks in a new/empty R package: CRAN intent,
compiled code (Rcpp/RcppArmadillo), and statistical calculations needing oracle
verification. Currently a declared placeholder — the greenfield opener flow is
a downstream candidate; this slot names the intended R questions but the flow
that asks them ships later.
