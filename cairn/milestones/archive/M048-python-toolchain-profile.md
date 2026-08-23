# M48: Python toolchain profile — done 2026-07-13

**PR:** https://github.com/jmgirard/cairn/pull/46 · **Depends on:** —

**Goal.** Ship a `python` toolchain profile at R-parity opinionation and wire it
into cairn-init selection + the absent-PROFILE inference fallback.

**Outcome.** cairn ships a third profile. `skills/shared/profiles/python.md`
(82 lines) fills all six slots with one blessed toolchain: PEP 621
`pyproject.toml`, `pytest`, `ruff` (format+lint), `mypy`, `python -m build` +
`twine` (release-walk hands `twine upload` to the user, OIDC noted as the CI
alternative, self-submits nothing), `coverage.py` as diagnostic. cairn-init
selection + repair backfill: `DESCRIPTION → r-package`, else
`pyproject.toml`/`setup.py`/`setup.cfg → python`, else `generic` (DESCRIPTION
wins a hybrid). Rulebook "Toolchain profiles": three ship, inference order
stated. Seven guard tests in `test_toolchain_profiles.py` lock it.

**Review.** 3-lens fresh-context review + scorer; prior-PR lens no-op'd. Three
findings (all ≥80), all fixed: T3's "two profiles" sweep missed `DESIGN.md:12`
and `:35` (F1/93, F2/82); the guard running the *real* validator on shipped
profiles looped only (r-package, generic), leaving `python.md` unexercised by
the schema AC1 cites (F3/80 — added `python`).

**Key facts.** No new D-entry (parallel third profile within the M45 spine).
`greenfield-openers` ships as a declared placeholder. No principle touched.
