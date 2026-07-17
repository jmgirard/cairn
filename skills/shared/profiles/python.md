# Toolchain profile: python

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in skills/shared/validation-doctrine.md
     (referenced from tracking-rules). All seven `## <slot>` sections
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
- The declared changelog (`## changelog` slot) has an entry for this
  milestone's user-visible changes (no milestone numbers in user-facing text).

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
- GitHub Actions CI uses the standard pair (the r-package profile's
  covr→Codecov analog — M52): a test workflow runs `pytest` on push/PR (a
  normal CI check — cairn's git model never merges red or pending CI), and a
  coverage workflow runs `pytest --cov` (pytest-cov) and uploads to Codecov.
  Coverage reporting is diagnostic-only: Codecov annotates the PR, but it
  never gates the merge — the `coverage.py` line above and tracking-rules'
  "no coverage-percentage target" both hold.
- Change governance renders here as: the dependency surface is `pyproject.toml`
  dependencies/optional-dependencies; a breaking-change deprecation cycle emits
  `DeprecationWarning` before removal. The gates themselves — question-gate +
  D-entry for dependencies, pre-1.0 waiver rule — are universal
  (tracking-rules "Universal tracking rules").

## release-walk
Followed by `/cairn-release` — a PyPI release walk (never self-submits):
- Version decision (patch/minor/major) from the declared changelog; pre-1.0
  conventions per DESIGN.md.
- Changelog consolidation (the declared file): retitle the dev heading to the
  version; group entries; prune noise.
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
Language-specific openers `cairn-init` asks in a new/empty Python package. The
universal openers — distribution ambition (rendered here as **PyPI intent**) and
numeric-work-needs-oracle-verification — come from cairn-init's universal layer,
so they are not repeated here.

- **Typing strictness?** Run `mypy --strict` from the start?
  - Options: **non-strict** (reversible default) · strict.
  - Consequence: strict ⇒ every module must be fully typed from day one.
    Tightening a non-strict package to `--strict` later is a bounded opt-in
    cleanup, so the reversible default is non-strict.
  - Lands in: the `verify` slot's `mypy` invocation (`mypy` vs `mypy --strict`)
    and `test-doctrine`.
- **Layout?** `src/` layout or flat layout?
  - Options: **`src/`** (reversible default) · flat.
  - Consequence: `src/` prevents importing the un-built package by accident and
    is the modern default; flat is simpler for a tiny single-module repo, but
    converting flat → `src/` later is a structural move.
  - Lands in: DESIGN Conventions (the package layout convention).

## changelog
The repo's changelog file, read by `/hotfix`, the release-walk, and the
consistency-gate: **`CHANGELOG.md`**.
