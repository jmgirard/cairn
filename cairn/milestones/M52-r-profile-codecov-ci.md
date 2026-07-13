<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M52: r-package profile — GitHub Actions CI (R-CMD-check + Codecov)

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** m52-r-profile-codecov-ci · https://github.com/jmgirard/cairn/pull/50

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

- [x] The r-package `test-doctrine` slot documents both standard workflows —
      R-CMD-check (`use_github_action("check-standard")`) and covr→Codecov
      test-coverage (`use_github_action("test-coverage")`).
- [x] The coverage-reporting guidance is explicitly diagnostic-only / never a
      merge gate, and the existing "covr is a diagnostic, never a gate" line is
      retained (no doctrine edit elsewhere in the profile or tracking-rules).
- [x] The six-slot schema is unchanged: `test_shipped_reference_profiles_are_valid`
      passes, `_REQUIRED_SLOTS` is untouched, and no slot is added or renamed.
- [x] A guard test in `test_toolchain_profiles.py` locks the guidance on
      uniquely-new tokens and fails if the CI-pair guidance is deleted
      (deletion sanity-check per the M47/M39/M40 false-coverage lessons).
- [x] The active profile's `verify` slot clean: all three unittest suites green
      (`skills/tests`, `scripts/tests`, `hooks/tests`).

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T3
- AC4 → T1
- AC5 → T3

## Tasks

- [x] T1 — Write the guard test in `skills/tests/test_toolchain_profiles.py`:
      assert the r-package `test-doctrine` names `check-standard`,
      `test-coverage`, and `codecov`, plus the diagnostic-only framing; anchor
      on the uniquely-new tokens and include a mental/actual deletion check so
      the test fails if the CI-pair block is removed. (Red first.)
- [x] T2 — Edit the `test-doctrine` slot of `skills/shared/profiles/r-package.md`
      to add the CI-pair + Codecov guidance (diagnostic-only) and the
      `^\.github$` `.Rbuildignore` note; retain the existing covr line. Make T1
      green.
- [x] T3 — Run all three unittest suites + `test_shipped_reference_profiles_are_valid`;
      confirm the six-slot schema still validates and nothing regressed.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: status → in-progress; branch m52-r-profile-codecov-ci cut from main.
- 2026-07-12: T1 — guard test TestRPackageCodecovCI added (red: the CI-pair tokens check-standard/test-coverage/codecov/"never gates the merge" are absent pre-M52); the covr-line retention check is green.
- 2026-07-12: T2 — r-package test-doctrine gains the usethis CI-pair (check-standard + test-coverage→Codecov) after the covr line, diagnostic-only framing, `^\.github$` .Rbuildignore note; T1 now green (red→green = the deletion sanity-check).
- 2026-07-12: T3 — all three suites green (skills 134 / scripts 65 / hooks 32); test_shipped_reference_profiles_are_valid passes (six-slot schema intact); cairn_validate all checks pass. Status → review.

## Decisions

## Review

PR: https://github.com/jmgirard/cairn/pull/50 · main in sync (0 behind, 2 ahead at review).

**Acceptance-criteria evidence** (fresh, by command):
- AC1 ✓ — r-package `test-doctrine` names both workflows: `use_github_action("check-standard")` and `use_github_action("test-coverage")`→Codecov ([r-package.md](skills/shared/profiles/r-package.md) test-doctrine slot).
- AC2 ✓ — coverage framed diagnostic-only ("coverage never gates the merge"); the `covr` is a diagnostic, never a gate line retained; no edit to tracking-rules or other profiles (diff scope confined to the r-package slot).
- AC3 ✓ — `test_shipped_reference_profiles_are_valid` passes; `_REQUIRED_SLOTS` untouched; no `## ` heading added/renamed (edit is body-only).
- AC4 ✓ — `TestRPackageCodecovCI` (3 tests) green; the CI-pair tokens were red pre-edit (2 failures) and green post-edit — the red→green transition is the deletion sanity-check.
- AC5 ✓ — all three suites green: skills 134 / scripts 65 / hooks 32.

**Consistency gate:**
- Universal: `cairn_validate` → all checks passed (exit 0). Coverage completeness: AC1→T2, AC2→T2, AC3→T3, AC4→T1, AC5→T3 — every criterion maps to an existing task.
- Toolchain: this repo's active profile is `generic`; its consistency-gate slot names no toolchain checks → clean no-op.
- No DESIGN principle changed (none exist) → `cairn_impact` skipped.

**Independent review (3 lenses + scorer):** all three fresh-context lenses returned **zero findings** → nothing to score, no triage.
- [O] diff-bug (Opus): clean on all four axes — gate distinction (check-standard is a normal red-CI gate; only coverage is diagnostic-only), usethis-name accuracy, deletion sanity-check (every anchor exists only in the new block), cross-doctrine consistency. Dropped one taxonomy item (a red test-coverage *job* would still gate under "never merge red CI" — the plan-mandated diagnostic-only framing is about the coverage %, correct as written).
- [S] blame-history (Sonnet): clean — insertion sits between the covr line and the dependency line, leaving M49/D-028 provenance content and M46 slot structure intact; no D-entry contradicted; new test asserts disjoint tokens from TestRPackageFixtureProvenance.
- [S] prior-PR-comments (Sonnet): no prior-PR evidence (PRs #43–#48 touching these files carry zero inline review comments) — expected no-op on this repo.
