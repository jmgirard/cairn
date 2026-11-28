# M47: Release-walk slot — generalize cairn-release to read the profile

**Status:** done · PR #45 · merged 2026-07-13 · milestone 3 of 3, closes the toolchain-profiles arc (M45 spine, M46 rewire).

## Goal
Generalize `/cairn-release` to read the active profile's `release-walk` slot instead of hardcoding the CRAN/devtools walk; give the `generic` profile a language-appropriate (bump + NEWS + tag, no CRAN) release path.

## Outcome
- `cairn-release/SKILL.md` rewritten as a universal spine (version decision, changelog consolidation, handoff, routing chip) that reads the active profile's `release-walk` slot for toolchain-specific steps; no literal `devtools::` left.
- Preconditions gate on the profile — `DESCRIPTION`/registry install required only when the slot names them (r-package does, generic doesn't).
- `generic` `release-walk` enriched from a one-line summary into a followable 4-step walk (decide bump → consolidate NEWS → commit → tag), shipped `generic.md` + this repo's `cairn/PROFILE.md` (byte-identical, GP3).
- r-package `release-walk` slot already held the full CRAN walk (relocated at M45) — behavior preserved, now the single source.
- Guards: `cairn-release` joined `REWIRED_SKILLS`, `TestReleaseSkillUntouched` removed (the pre-declared M47 boundary flip); new `TestReleaseSkillReadsProfile`.

## Key decisions
- No new D-entry — mechanism settled in M45; GP3-instantiating, wording unchanged.
- Boundary-guard flip folded into the T2 skill-rewrite commit (M46 lesson) — a separate guard task would leave the suite red mid-milestone. Minor amendment.

## Review
- ACs 1–4 fresh-verified; suites 115/65/32 green; `cairn_validate` 14/14 + sizing OK.
- Three-lens independent review: **zero findings**; prior-PR lens no-op (repo has no inline PR comments). One sub-threshold test-strength note → hardened `test_generic_release_walk_defines_a_tag_path` with a `commit`-step assertion locking T1's enrichment.
