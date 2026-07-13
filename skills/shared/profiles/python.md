# Toolchain profile: python

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in tracking-rules. All six `## <slot>` sections
     are defined; cairn_validate FAILs on a missing or empty slot. -->

The Python-package toolchain: PEP 621 `pyproject.toml`, pytest, ruff, mypy,
`python -m build` + twine (PyPI). One blessed pick per category — no menus.
Selected by `cairn-init` when a `pyproject.toml` (or legacy `setup.py`/
`setup.cfg`) is present and no `DESCRIPTION` outranks it.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite):
- After code changes, before a task is checked off: `pytest` clean.
- `ruff format` (formatter) then `ruff check --fix` (lint) leave no diff.
- After touching typed code: `mypy` clean on the package.
- `/hotfix` gate-lite: `pytest` clean; `ruff check` + `mypy` if code changed;
  `python -m build` if packaging metadata was touched.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- `ruff check` reports no violations and `ruff format --check` no diff.
- `mypy` clean on the package's own typed code (justify or fix any remaining
  note, the analog of an R CMD check NOTE).
- `python -m build` succeeds and `twine check dist/*` passes (metadata/README
  render valid for PyPI).
- Generated/vendored files are never hand-edited; lockfiles regenerate from
  their tool (`uv lock`, `pip-compile`) — a stray diff is drift.
- CHANGELOG has an entry for this milestone's user-visible changes (no
  milestone numbers in user-facing text).

## test-doctrine
Python-mechanical test expectations layered on the universal "What gets a test"
rules in tracking-rules:
- Tests are written for `pytest` (fixtures, parametrize), discovered under `tests/`.
- Every public function: happy path, every raised-exception branch fired via
  `pytest.raises(...)`, Python edge cases — empty inputs, `None`, single element,
  wrong type / `TypeError`, zero-length and unicode strings.
- New user-facing errors raise a specific built-in or a package exception with a
  clear message, never a bare `assert` or generic `Exception`.
- Indirect by default: private helpers (direct tests only for independent logic).
- Never test string-formatting cosmetics beyond meaningful snapshots, trivial
  pass-throughs, or dependency behavior.
- `coverage.py` is a diagnostic, never a gate.
- Dependency changes (`pyproject.toml` dependencies/optional-dependencies) are
  never unilateral — question-gate + D-entry.
- Breaking changes to public API follow a deprecation cycle (`DeprecationWarning`)
  unless pre-1.0 and explicitly waived.

## release-walk
Followed by `/cairn-release` — a PyPI release walk (never self-submits):
- Version decision (patch/minor/major) from the CHANGELOG; pre-1.0 conventions
  per DESIGN.md.
- CHANGELOG consolidation: retitle the dev heading to the version; group
  entries; prune noise.
- Full local verification: `pytest`, `ruff check`, `ruff format --check`, and
  `mypy` clean; `python -m build`; `twine check dist/*` passes.
- Bump the version (`project.version` in `pyproject.toml`, or the `__version__`
  the build reads).
- Handoff checklist (user runs): `twine upload dist/*` (or an equivalent
  trusted-publishing / OIDC CI job — the recommended alternative that keeps no
  long-lived token), confirm the release on PyPI, then tag `v<version>` and cut
  the GitHub release. cairn self-submits nothing.

## init-detection
Recognized by `cairn-init` when a **`pyproject.toml`** (primary) or a legacy
**`setup.py`** / **`setup.cfg`** is present at the repo root and no
`DESCRIPTION` outranks it (a hybrid repo stays `r-package`). `cairn/` is not a
Python package directory, so no build-exclude entry is needed (the Python
analog of R's `.Rbuildignore` `^cairn$` is unnecessary — `cairn/` is neither a
package nor under a `src/` root).

## greenfield-openers
Opener questions `cairn-init` asks in a new/empty Python package: PyPI intent,
typing strictness (`mypy --strict` from the start?), and `src/` vs. flat layout.
Currently a declared placeholder — the greenfield opener flow is a downstream
candidate; this slot names the intended Python questions but the flow that asks
them ships later.
