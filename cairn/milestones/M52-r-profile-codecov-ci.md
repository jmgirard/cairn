<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M52: r-package profile — GitHub Actions CI (R-CMD-check + Codecov)

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** —

## Goal

Document the standard R GitHub Actions CI pair — R-CMD-check and covr→Codecov
coverage reporting — in the r-package profile's `test-doctrine` slot, framed
diagnostic-only, without changing the six-slot schema or the "coverage is
never a gate" doctrine.

## Scope

**In:**
- Extend the `test-doctrine` slot of `skills/shared/profiles/r-package.md`
  (currently the lone `covr` line, [r-package.md:42](skills/shared/profiles/r-package.md)):
  name the standard usethis GitHub Actions pair — `use_github_action("check-standard")`
  (R CMD check) and `use_github_action("test-coverage")` (covr → Codecov upload) —
  and state that Codecov/coverage reporting is **diagnostic-only, never a merge
  gate**, coherent with the retained "covr is a diagnostic, never a gate" line
  and tracking-rules' "no coverage-percentage target".
- Note the R-mechanical `.Rbuildignore` `^\.github$` entry (usethis adds it) so
  the workflow dir stays out of the built package — parallel to the existing
  `^cairn$` note in `init-detection`.
- Guard test in `skills/tests/test_toolchain_profiles.py` locking the new
  guidance, anchored on tokens the new work uniquely introduces (`codecov`,
  `test-coverage`, `check-standard`) with a deletion sanity-check.

**Out:**
- A new `ci` profile slot / schema change → refused: the user chose fold-into-
  `test-doctrine`; `_REQUIRED_SLOTS` stays six ([cairn_validate.py:336](scripts/cairn_validate.py)).
- Coverage as a merge gate → refused: the user chose diagnostic-only; no D-entry
  superseding the "never a gate" doctrine.
- Parallel Codecov mention in the `python` profile (symmetric `coverage.py`
  line) → candidate row (symmetry, not requested here).
- Scaffolding actual workflow YAML into adopting repos or this repo, and a
  pkgdown-deploy workflow → not this milestone (the profile documents the
  practice; it does not generate CI files).

## Acceptance criteria

- [ ] The r-package `test-doctrine` slot documents both standard workflows —
      R-CMD-check (`use_github_action("check-standard")`) and covr→Codecov
      test-coverage (`use_github_action("test-coverage")`).
- [ ] The coverage-reporting guidance is explicitly diagnostic-only / never a
      merge gate, and the existing "covr is a diagnostic, never a gate" line is
      retained (no doctrine edit elsewhere in the profile or tracking-rules).
- [ ] The six-slot schema is unchanged: `test_shipped_reference_profiles_are_valid`
      passes, `_REQUIRED_SLOTS` is untouched, and no slot is added or renamed.
- [ ] A guard test in `test_toolchain_profiles.py` locks the guidance on
      uniquely-new tokens and fails if the CI-pair guidance is deleted
      (deletion sanity-check per the M47/M39/M40 false-coverage lessons).
- [ ] The active profile's `verify` slot clean: all three unittest suites green
      (`skills/tests`, `scripts/tests`, `hooks/tests`).

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T3
- AC4 → T1
- AC5 → T3

## Tasks

- [ ] T1 — Write the guard test in `skills/tests/test_toolchain_profiles.py`:
      assert the r-package `test-doctrine` names `check-standard`,
      `test-coverage`, and `codecov`, plus the diagnostic-only framing; anchor
      on the uniquely-new tokens and include a mental/actual deletion check so
      the test fails if the CI-pair block is removed. (Red first.)
- [ ] T2 — Edit the `test-doctrine` slot of `skills/shared/profiles/r-package.md`
      to add the CI-pair + Codecov guidance (diagnostic-only) and the
      `^\.github$` `.Rbuildignore` note; retain the existing covr line. Make T1
      green.
- [ ] T3 — Run all three unittest suites + `test_shipped_reference_profiles_are_valid`;
      confirm the six-slot schema still validates and nothing regressed.

## Work log

- 2026-07-12: created by /milestone-plan.

## Decisions

## Review
