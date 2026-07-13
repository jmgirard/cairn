# M47: Release-walk slot — generalize cairn-release to read the profile

- **Status:** planned
- **Priority:** normal
- **Depends on:** M45
- **Principles touched:** GP3
- **Branch/PR:** —

## Goal

Generalize the release path so `cairn-release` reads the active profile's
`release-walk` slot — the CRAN walk becomes the `r-package` profile's
release-walk, and the `generic` profile gets a language-appropriate (version
bump + NEWS + tag, no CRAN) release path.

## Scope

**In:**
- `cairn-release` reads the profile `release-walk` slot instead of hardcoding
  the CRAN/devtools walk; its preconditions gate on the profile rather than
  assuming DESCRIPTION/devtools unconditionally.
- The CRAN/devtools steps become the `r-package` profile's `release-walk`
  content (verbatim).
- The `generic` profile's `release-walk` defines a minimal path (version bump +
  NEWS + tag, no CRAN); `cairn-release` in a generic repo follows it without
  invoking devtools.

**Out:**
- Any non-R release automation beyond a simple tag — a real language profile
  can extend its own slot later (YAGNI here).
- Greenfield openers, oracle doctrine (untouched).

## Acceptance criteria

- [ ] `cairn-release`'s CRAN walk is expressed as the `r-package` profile's
      `release-walk` slot, and the skill reads the active profile's slot rather
      than hardcoding CRAN. Evidence: skill prose + `r-package` profile content +
      guard test.
- [ ] The `generic` profile defines a `release-walk` (version bump + NEWS + tag,
      no CRAN), and `cairn-release` run against a generic profile follows it
      without invoking devtools/CRAN. Evidence: `generic` profile content +
      skill prose + guard test.
- [ ] `cairn-release` preconditions no longer assume DESCRIPTION/devtools
      unconditionally — they gate on the active profile. Evidence: skill diff +
      guard test.
- [ ] Existing R release behavior is preserved for an `r-package` repo (the CRAN
      steps are the same content, now sourced from the slot). Evidence: a
      text-equivalence guard test.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T2, T3
- AC4 → T1, T3

## Tasks

- [ ] T1 — Move the CRAN walk into the `r-package` profile `release-walk` slot;
      author the `generic` `release-walk` (version bump + NEWS + tag path).
- [ ] T2 — `cairn-release`: read the active profile's `release-walk` slot; gate
      the preconditions (DESCRIPTION/devtools/clean-tree) on the profile.
- [ ] T3 — Guard tests: CRAN content lives in the `r-package` slot, the generic
      tag path exists, precondition gating, and r-package text-equivalence.

## Work log

- 2026-07-12: created by /milestone-plan (toolchain-profiles arc, milestone 3 of 3).

## Decisions

## Review
