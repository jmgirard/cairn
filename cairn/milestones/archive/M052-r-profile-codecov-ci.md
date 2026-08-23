# M52: r-package profile — GitHub Actions CI (R-CMD-check + Codecov)

**Status:** done · PR https://github.com/jmgirard/cairn/pull/50 · merged 2026-07-12 (local-green, no CI on this repo).

**Goal:** Document the standard R GitHub Actions CI pair in the r-package
profile's `test-doctrine` slot, framed diagnostic-only, without a schema or
doctrine change.

**Outcome:** The r-package profile ([test-doctrine slot]) now names the
standard `usethis` pair — `use_github_action("check-standard")` (R CMD check,
a normal red-CI gate) and `use_github_action("test-coverage")` (covr →
Codecov, `covr::codecov()`) — with coverage reporting **diagnostic-only**
(annotates the PR, never gates the merge), plus the `.github/` `.Rbuildignore`
`^\.github$` note. Folded into the existing slot: `_REQUIRED_SLOTS` stays six,
the "covr is a diagnostic, never a gate" line and tracking-rules' "no
coverage-percentage target" both retained. Guard: `TestRPackageCodecovCI`
in `test_toolchain_profiles.py` (anchored on uniquely-new tokens; red→green
deletion sanity-check). Symmetric python-profile parallel banked as a candidate.

**Decisions (plan gate):** scope = Codecov + R-CMD-check pair; placement =
fold into test-doctrine (no new slot); gate = diagnostic-only (no D-entry
superseding "never a gate"). No new DECISIONS.md entry (all within doctrine).

**Review:** 3 fresh-context lenses (diff-bug/blame/prior-PR) — zero findings.
All 5 criteria verified; cairn_validate clean; suites green (134/65/32).
