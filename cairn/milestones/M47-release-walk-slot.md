# M47: Release-walk slot — generalize cairn-release to read the profile

- **Status:** review
- **Priority:** normal
- **Depends on:** M45
- **Principles touched:** GP3
- **Branch/PR:** m47-release-walk-slot · https://github.com/jmgirard/cairn/pull/45

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

- [x] `cairn-release`'s CRAN walk is expressed as the `r-package` profile's
      `release-walk` slot, and the skill reads the active profile's slot rather
      than hardcoding CRAN. Evidence: skill prose + `r-package` profile content +
      guard test.
- [x] The `generic` profile defines a `release-walk` (version bump + NEWS + tag,
      no CRAN), and `cairn-release` run against a generic profile follows it
      without invoking devtools/CRAN. Evidence: `generic` profile content +
      skill prose + guard test.
- [x] `cairn-release` preconditions no longer assume DESCRIPTION/devtools
      unconditionally — they gate on the active profile. Evidence: skill diff +
      guard test.
- [x] Existing R release behavior is preserved for an `r-package` repo (the CRAN
      steps are the same content, now sourced from the slot). Evidence: a
      text-equivalence guard test.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T2, T3
- AC4 → T1, T3

## Tasks

- [x] T1 — Move the CRAN walk into the `r-package` profile `release-walk` slot;
      author the `generic` `release-walk` (version bump + NEWS + tag path).
- [x] T2 — `cairn-release`: read the active profile's `release-walk` slot; gate
      the preconditions (DESCRIPTION/devtools/clean-tree) on the profile.
- [x] T3 — Guard tests: CRAN content lives in the `r-package` slot, the generic
      tag path exists, precondition gating, and r-package text-equivalence.

## Work log

- 2026-07-12: created by /milestone-plan (toolchain-profiles arc, milestone 3 of 3).
- 2026-07-13: started /milestone-implement on m47-release-walk-slot; status → in-progress.
- 2026-07-13: T1 — r-package release-walk slot already held the full CRAN walk (M45); enriched the generic release-walk from a one-line summary into a followable bump→NEWS→commit→tag walk (shipped generic.md + this repo's PROFILE.md); dropped the obsolete "lands in M47" note.
- 2026-07-13: T2 — rewrote cairn-release/SKILL.md as a universal spine that reads the active profile's release-walk slot (r-package = CRAN walk, generic = tag walk) and gates toolchain preconditions on the profile; removed the hardcoded CRAN/devtools walk. Minor plan amendment (M46 lesson): folded the boundary-guard flip into this commit — added cairn-release to REWIRED_SKILLS and removed TestReleaseSkillUntouched, since removing devtools:: from the skill would otherwise leave that guard red mid-milestone.
- 2026-07-13: T3 — added TestReleaseSkillReadsProfile (skill reads the release-walk slot, gates preconditions on the profile, generic slot defines a tag path with no CRAN); AC4 text-equivalence already locked by test_r_package_profile_holds_relocated_commands. All three verify suites green (115 + 65 + 32). Status → review.

## Decisions

## Review

**2026-07-13 — evidence (PR #45).** Verify slot green: skills 115 · scripts 65 · hooks 32.
`cairn_validate` 14/14 PASS + sizing OK. Consistency gate: generic profile names
no toolchain `consistency-gate` checks → that half is a clean no-op; universal
checks (validate, coverage complete, cairn_impact) done. No DESIGN.md principle
text changed (diff touches 0 DESIGN files) → `cairn_impact` skipped; M47 works
under GP3, doesn't alter it.

- **AC1** (skill reads the `release-walk` slot, not hardcoded CRAN) — PASS.
  Skill: 6 `release-walk` refs, 1 `PROFILE.md` ref, **0** `devtools::`.
  `test_skill_reads_the_release_walk_slot` + `TestOperationalSkillsReadProfile`
  (now includes cairn-release: PROFILE.md present, no `devtools::`) +
  `test_r_package_profile_holds_relocated_commands` (CRAN content in the slot).
- **AC2** (generic profile defines a release-walk, tag path, no CRAN) — PASS.
  Generic slot is a 4-step bump→NEWS→commit→tag walk; 0 CRAN/devtools tokens.
  `test_generic_release_walk_defines_a_tag_path` (slot-isolated).
- **AC3** (preconditions gate on the active profile) — PASS. Skill line 28
  "Toolchain preconditions gate on the profile"; `DESCRIPTION`/registry required
  only when the slot names them. `test_skill_gates_preconditions_on_the_profile`.
- **AC4** (r-package behavior preserved, text-equivalence) — PASS. r-package slot
  holds `submit_cran()`, `devtools::check()` (×3), `cran-comments`, `NEWS.md`.
  `test_r_package_profile_holds_relocated_commands`.

**Independent review — three lenses + scorer.** [O] diff-bug, [S] blame-history,
[S] prior-PR-comments: **zero actionable findings** (no scorer run — nothing to
score). blame-history confirmed the `TestReleaseSkillUntouched` removal is the
pre-declared M47 boundary flip with no behavior dropped; prior-PR lens no-op'd
cleanly (repo carries zero inline PR review comments). One sub-threshold,
non-blocking observation (surfaced per IP3): `test_generic_release_walk_defines_a_tag_path`
locked AC2 but not T1's slot enrichment (the old one-liner already had tag/version).
Fix-now: added an `assertIn("commit", …)` assertion anchoring on the enriched
walk's unique step. Full skills suite green (115) after the hardening.
