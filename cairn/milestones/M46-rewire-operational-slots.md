# M46: Rewire operational slots — implement/review/hotfix/doctrine read the profile; dogfood generic

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M45
- **Principles touched:** GP3
- **Branch/PR:** m46-rewire-operational-slots

## Goal

Rewire the operational skills and the rulebook's language-mechanical doctrine
to read the active profile's slots instead of hardcoded R commands, and
dogfood the `generic` profile in this repo.

## Scope

**In:**
- `milestone-implement` verify steps and `hotfix` gate-lite → read the profile
  `verify` slot.
- `milestone-review` consistency gate → the R-mechanical checks become the
  profile `consistency-gate` slot; the universal cairn-file checks
  (`cairn_validate`, coverage completeness, `cairn_impact`) stay unconditional.
- `tracking-rules` "R package guardrails" and the R-mechanical half of "What
  gets a test" (exported-fn edge cases, `cli_abort`, deprecation cycle) →
  relocated into the `r-package` profile's `test-doctrine`/`consistency-gate`
  slots; the universal test rules stay in `tracking-rules`.
- `milestone.md` template acceptance guidance → profile-aware (drop the
  hardcoded `devtools::check()` line; reference the active profile's verify).
- Dogfood: this repo gains `cairn/PROFILE.md` = `generic`; the CLAUDE.md
  hand-waiver note ("R-specific gates … are waived here") is replaced by the
  declared generic profile. `DESIGN.md` Purpose & Scope updated to name the
  language-agnostic core + profile mechanism (architecture-as-it-is).

**Out:**
- Release-walk / `cairn-release` generalization → M47.
- Greenfield opener content → greenfield-init candidate.
- Oracle / Validation doctrine untouched (universal, orthogonal — D-024/D-025).

## Acceptance criteria

- [ ] `milestone-implement` and `hotfix` name the profile `verify` slot, not
      `devtools::test()` literally. Evidence: skill prose + guard test.
- [ ] `milestone-review`'s consistency gate reads the profile `consistency-gate`
      slot for language checks while keeping the universal cairn-file checks
      (validate, coverage, impact) unconditional. Evidence: skill prose + a
      guard test asserting the split.
- [ ] `tracking-rules` "R package guardrails" + the R-mechanical half of "What
      gets a test" are relocated into the `r-package` profile; the universal
      test rules remain in `tracking-rules`. Evidence: a guard test asserting
      the R tokens (`devtools`/`roxygen`/`NAMESPACE`) no longer appear in the
      universal sections and do appear in the `r-package` profile.
- [ ] The `milestone.md` template no longer hardcodes `devtools::check()`; it
      references the active profile's verify/check. Evidence: template diff +
      guard test.
- [ ] This repo declares `cairn/PROFILE.md` = `generic`, the CLAUDE.md "R gates
      waived here" note is gone, `DESIGN.md` names the profile mechanism, a full
      `cairn_validate` run passes (exit 0), and the script + skill suites are
      green under the generic profile. Evidence: `PROFILE.md` exists, CLAUDE.md
      + DESIGN.md diffs, validate exit 0, `python3 -m unittest` green.
- [ ] The `r-package` profile still reproduces the pre-M46 R behavior after the
      relocation (no R adopter regresses). Evidence: the text-equivalence guard
      test, updated to the relocated slot content, passes.

## Coverage

- AC1 → T2, T3, T8
- AC2 → T4, T8
- AC3 → T1, T7, T8
- AC4 → T5, T8
- AC5 → T6
- AC6 → T7, T8

## Tasks

- [x] T1 — `tracking-rules`: relocate "R package guardrails" + the R-mechanical
      test rules into the `r-package` profile; keep the universal rules; add the
      framing "profiles supply language mechanics; oracle doctrine stays
      universal".
- [x] T2 — `milestone-implement`: verify steps read the profile `verify` slot.
- [x] T3 — `hotfix`: gate-lite reads the profile `verify` slot.
- [ ] T4 — `milestone-review`: split the consistency gate into universal
      (cairn-file) checks and the profile `consistency-gate` slot.
- [ ] T5 — `milestone.md` template: profile-aware acceptance guidance.
- [ ] T6 — Dogfood: add `cairn/PROFILE.md` (`generic`) to this repo; remove the
      CLAUDE.md waiver note; update `DESIGN.md` Purpose & Scope; run full
      `cairn_validate` + the unittest suites.
- [ ] T7 — Update the `r-package` profile with the relocated doctrine; update
      the text-equivalence guard to the new slot content.
- [ ] T8 — Guard tests for the T1–T5 splits (verify-slot read, gate split,
      doctrine relocation, template de-R).

## Work log

- 2026-07-12: created by /milestone-plan (toolchain-profiles arc, milestone 2 of 3).
- 2026-07-12: T1 — relocated "R package guardrails" + R-mechanical "What gets a test" out of tracking-rules into the r-package profile (added the generated-file `NAMESPACE`/`man`/`data` guardrail there); universal floor genericized + framing added. Flipped `test_toolchain_profiles` source-of-truth to the profile; added `TestRulebookRelocation` (AC3). Guard-test updates fold into each task commit to keep the suite green per checkpoint (minor amendment to plan's separate-T8).
- 2026-07-12: T2 — `milestone-implement` now runs the active profile's `verify` slot (per-task, resume, completion) and its `test-doctrine` slot for idioms; no `devtools::` left. Replaced M45 AC6 guard with growing `TestOperationalSkillsReadProfile` + `TestReleaseSkillUntouched` (M47 boundary).
- 2026-07-12: T3 — `hotfix` gate-lite now runs the profile's `verify` slot; no `devtools::` left. Added `hotfix` to the rewired-skills guard. (NEWS.md changelog requirement left as-is — changelog-mechanism generalization is out of M46 scope.)

## Decisions

## Review
