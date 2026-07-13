<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M48: Python toolchain profile

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** m48-python-toolchain-profile · https://github.com/jmgirard/cairn/pull/46

## Goal

Ship a `python` toolchain profile at R-parity opinionation and wire it into
cairn-init selection and the absent-PROFILE inference fallback.

## Scope

**In:** A new `skills/shared/profiles/python.md` reference profile filling all
six slots with one blessed toolchain (no menus) — PEP 621 `pyproject.toml`
metadata, `pytest` tests, `ruff` (lint+format) and `mypy` as consistency-gate
checks, `python -m build` + `twine check` with a user-run `twine upload`
handoff (trusted-publishing noted as the CI alternative), `coverage.py` as a
diagnostic never a gate. Wiring: cairn-init detects python on a
`pyproject.toml` (or legacy `setup.py`/`setup.cfg`) marker and backfills it in
repair mode; the tracking-rules "Toolchain profiles" inference lists
`pyproject.toml → python`; guard tests lock all of it.

**Out:** The R fixture-provenance guard fold-in → M49 (independent, no
dependency). Filling the python `greenfield-openers` flow → the "Greenfield
init flow" candidate (the slot ships as a declared placeholder, parallel to R).
Any package skeleton / scaffolding of a real python project → out (cairn-init
stays tracking-only).

## Acceptance criteria

- [x] `skills/shared/profiles/python.md` exists and defines exactly the six
      known slots (`verify`, `consistency-gate`, `test-doctrine`,
      `release-walk`, `init-detection`, `greenfield-openers`), each non-empty —
      i.e. it satisfies the same `cairn_validate` slot schema the shipped
      profiles do.
- [x] The profile encodes the blessed python toolchain at R-parity
      opinionation: `pyproject.toml`/PEP 621, `pytest`, `ruff`, `mypy`,
      `python -m build`, `twine` — one pick per category, verifiable by
      guard-test tokens; the release-walk hands off `twine upload` to the user
      and self-submits nothing (parallel to the CRAN handoff).
- [x] cairn-init selects `python` on a `pyproject.toml` (or `setup.py`/
      `setup.cfg`) marker with `DESCRIPTION` retaining precedence for hybrid
      repos, and repair-mode inference backfills it — locked by a guard test.
- [x] tracking-rules "Toolchain profiles" states three profiles ship and its
      absent-PROFILE inference lists `pyproject.toml → python` (order:
      `DESCRIPTION → r-package`, `pyproject.toml → python`, else `generic`) —
      locked by a guard test.
- [x] Guard tests added to `skills/tests/test_toolchain_profiles.py` lock the
      four criteria above; the active profile's `verify` slot is clean (all
      three `unittest` suites green).

## Coverage

- AC1 → T1, T4
- AC2 → T1, T4
- AC3 → T2, T4
- AC4 → T3, T4
- AC5 → T4

## Tasks

- [x] T1 — Author `skills/shared/profiles/python.md`: six slots, opinionated
      modern toolchain (pyproject/PEP 621, pytest, ruff, mypy, build+twine,
      coverage-as-diagnostic); release-walk = local build + `twine check` +
      user-run `twine upload` (note trusted-publishing OIDC as the CI
      alternative), no self-submit; note `cairn/` is not a python package so no
      build-exclude entry is needed (the python analog of R's `.Rbuildignore
      ^cairn$`); `greenfield-openers` a declared placeholder parallel to R.
      Stay under the 90-line PROFILE cap.
- [x] T2 — Wire `cairn-init` SKILL.md: detection recognizes `pyproject.toml`
      (primary) / `setup.py` / `setup.cfg` → python, `DESCRIPTION` still wins a
      hybrid; confirm the recommended profile with the user before writing;
      repair-mode backfill inference gains the python branch; update the
      scaffold comment lines that enumerate profile names
      (`r-package | generic` → add `python`).
- [x] T3 — Update tracking-rules "Toolchain profiles": "Two profiles ship" →
      three; the "Absent `PROFILE.md` → infer" line gains `pyproject.toml →
      python` in the stated order; sweep for any other "two profiles" mention.
- [x] T4 — Add guard tests to `test_toolchain_profiles.py`: python profile
      defines the six slots non-empty; holds its toolchain tokens; generic
      carries no python toolchain tokens; cairn-init selects/​backfills python;
      the rulebook inference names `pyproject.toml`. Run all three suites green.

## Work log

- 2026-07-13: created by /milestone-plan (paired with M49; independent, no dependency).
- 2026-07-13: T1 — authored skills/shared/profiles/python.md (82 lines, six non-empty slots; pyproject/PEP621, pytest, ruff, mypy, build+twine, coverage-as-diagnostic; release-walk hands off twine upload + notes OIDC trusted-publishing, no self-submit).
- 2026-07-13: T2 — wired cairn-init: selection order DESCRIPTION→r-package, pyproject/setup.py/setup.cfg→python (DESCRIPTION wins hybrids), else generic; repair-mode backfill gains the python branch; scaffold comment + instantiate step enumerate python; non-R-package bullet routes pyproject repos to python.
- 2026-07-13: T3 — tracking-rules "Toolchain profiles": "Two profiles ship" → three (added python); absent-PROFILE inference lists DESCRIPTION→r-package, pyproject→python, else generic. Swept: only the one mention.
- 2026-07-13: T4 — added python guards to test_toolchain_profiles.py (exact-six-slots, toolchain tokens, release-walk handoff+no-self-submit, generic-negative, init select/backfill, rulebook three-profiles+inference-order). All three unittest suites green (121/65/32); cairn_validate all-pass.

## Decisions

## Review

**Reviewed 2026-07-13 · PR #46 · branch m48-python-toolchain-profile.**

Acceptance-criterion evidence (fresh):
- AC1 — `skills/shared/profiles/python.md` present, 82 lines (< 90 cap), exactly
  six `## ` headings matching the required slots; run through `cairn_validate._profile_slots`
  + `check_profile` logic: all six present & non-empty, zero unrecognized slots.
- AC2 — toolchain tokens all present by grep: `pyproject.toml`, `PEP 621`,
  `pytest`, `ruff`, `mypy`, `python -m build`, `twine check`, `twine upload`,
  `coverage.py`; release-walk slot carries `twine upload` handoff + "self-submits
  nothing" + "trusted-publishing" OIDC note.
- AC3 — cairn-init SKILL.md selection order (DESCRIPTION → r-package; else
  pyproject/setup.py/setup.cfg → python; else generic), "DESCRIPTION outranks a
  pyproject.toml in a hybrid", and repair-mode backfill inference all present.
- AC4 — tracking-rules "Toolchain profiles": "Three profiles ship", inference
  order DESCRIPTION → r-package, pyproject → python, else generic.
- AC5 — all three unittest suites green (skills 121, scripts 65, hooks 32); 7
  python guards confirmed running (not skipped).

Consistency gate: `cairn_validate` all-pass (14 checks + sizing); coverage
completeness — every AC maps to ≥1 existing task (AC1→T1,T4 · AC2→T1,T4 ·
AC3→T2,T4 · AC4→T3,T4 · AC5→T4); profile `consistency-gate` slot is `generic`
(no-op); no DESIGN principle changed (cairn_impact skipped).
