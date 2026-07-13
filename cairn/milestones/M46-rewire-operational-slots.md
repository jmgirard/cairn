# M46: Rewire operational slots — implement/review/hotfix/doctrine read the profile; dogfood generic

- **Status:** review
- **Priority:** normal
- **Depends on:** M45
- **Principles touched:** GP3
- **Branch/PR:** m46-rewire-operational-slots · PR #44

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

- [x] `milestone-implement` and `hotfix` name the profile `verify` slot, not
      `devtools::test()` literally. Evidence: skill prose + guard test.
- [x] `milestone-review`'s consistency gate reads the profile `consistency-gate`
      slot for language checks while keeping the universal cairn-file checks
      (validate, coverage, impact) unconditional. Evidence: skill prose + a
      guard test asserting the split.
- [x] `tracking-rules` "R package guardrails" + the R-mechanical half of "What
      gets a test" are relocated into the `r-package` profile; the universal
      test rules remain in `tracking-rules`. Evidence: a guard test asserting
      the R tokens (`devtools`/`roxygen`/`NAMESPACE`) no longer appear in the
      universal sections and do appear in the `r-package` profile.
- [x] The `milestone.md` template no longer hardcodes `devtools::check()`; it
      references the active profile's verify/check. Evidence: template diff +
      guard test.
- [x] This repo declares `cairn/PROFILE.md` = `generic`, the CLAUDE.md "R gates
      waived here" note is gone, `DESIGN.md` names the profile mechanism, a full
      `cairn_validate` run passes (exit 0), and the script + skill suites are
      green under the generic profile. Evidence: `PROFILE.md` exists, CLAUDE.md
      + DESIGN.md diffs, validate exit 0, `python3 -m unittest` green.
- [x] The `r-package` profile still reproduces the pre-M46 R behavior after the
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
- [x] T4 — `milestone-review`: split the consistency gate into universal
      (cairn-file) checks and the profile `consistency-gate` slot.
- [x] T5 — `milestone.md` template: profile-aware acceptance guidance.
- [x] T6 — Dogfood: add `cairn/PROFILE.md` (`generic`) to this repo; remove the
      CLAUDE.md waiver note; update `DESIGN.md` Purpose & Scope; run full
      `cairn_validate` + the unittest suites.
- [x] T7 — Update the `r-package` profile with the relocated doctrine; update
      the text-equivalence guard to the new slot content.
- [x] T8 — Guard tests for the T1–T5 splits (verify-slot read, gate split,
      doctrine relocation, template de-R). Folded into each task's commit (T1–T7)
      to keep the suite green per checkpoint; this task is the whole-suite pass.

## Work log

- 2026-07-12: created by /milestone-plan (toolchain-profiles arc, milestone 2 of 3).
- 2026-07-12: T1 — relocated "R package guardrails" + R-mechanical "What gets a test" out of tracking-rules into the r-package profile (added the generated-file `NAMESPACE`/`man`/`data` guardrail there); universal floor genericized + framing added. Flipped `test_toolchain_profiles` source-of-truth to the profile; added `TestRulebookRelocation` (AC3). Guard-test updates fold into each task commit to keep the suite green per checkpoint (minor amendment to plan's separate-T8).
- 2026-07-12: T2 — `milestone-implement` now runs the active profile's `verify` slot (per-task, resume, completion) and its `test-doctrine` slot for idioms; no `devtools::` left. Replaced M45 AC6 guard with growing `TestOperationalSkillsReadProfile` + `TestReleaseSkillUntouched` (M47 boundary).
- 2026-07-12: T3 — `hotfix` gate-lite now runs the profile's `verify` slot; no `devtools::` left. Added `hotfix` to the rewired-skills guard. (NEWS.md changelog requirement left as-is — changelog-mechanism generalization is out of M46 scope.)
- 2026-07-12: T4 — `milestone-review` consistency gate split into "Universal cairn-file checks" (validate/coverage/impact, unconditional) + the profile `consistency-gate` slot (toolchain checks; read-the-slot, no hardcoded R list); AC-evidence step de-hardcoded. Added `TestReviewGateSplit` (AC2); review joins rewired-skills guard. No R tokens left in the skill.
- 2026-07-12: T5 — `milestone.md` template AC guidance de-R'd (no `devtools::check()`); references the active profile's `verify`/check. Added `TestTemplateProfileAware` (AC4).
- 2026-07-12: T6 — dogfood: added `cairn/PROFILE.md` = `generic` (verify slot = this repo's three `python3 -m unittest` suites); replaced the CLAUDE.md R-waiver note with the declared generic profile; DESIGN.md Purpose & Scope + Architecture now name the language-agnostic core + profile mechanism. `cairn_validate` exit 0 (profile valid); suites 112/65/32 green.
- 2026-07-12: T7 — confirmed the r-package profile reproduces every relocated guardrail (generated-file `NAMESPACE`/`man`/`data`, README.Rmd, dependency/deprecation, `.Rbuildignore`, `_pkgdown`, `cli_abort`); text-equivalence guard flipped to profile-as-source (T1) + `test_relocated_guardrail_specifics_survive` added (AC6).
- 2026-07-12: T8 — guard tests for all splits folded into their task commits (`TestRulebookRelocation`, `TestOperationalSkillsReadProfile`, `TestReviewGateSplit`, `TestTemplateProfileAware`, `TestReleaseSkillUntouched`); whole-suite pass at completion.

## Decisions

## Review

_Reviewed 2026-07-12 · PR #44 · branch `m46-rewire-operational-slots` (8 commits)._

### Acceptance-criteria evidence (fresh)

- **AC1** — `milestone-implement` names the profile `verify` slot in 3 places
  (per-task, resume, completion) and `test-doctrine` for idioms; `hotfix`
  gate-lite names it once. Zero `devtools` tokens remain in either skill.
  Guard: `TestOperationalSkillsReadProfile.test_rewired_skills_read_a_profile_slot`.
- **AC2** — `milestone-review` gate labels "Universal cairn-file checks"
  (validate/coverage/impact, unconditional) and reads the profile
  `consistency-gate` slot for toolchain checks. Guards:
  `TestReviewGateSplit.{test_universal_checks_stay_unconditional,test_review_reads_the_profile_consistency_gate_slot}`.
- **AC3** — `## R package guardrails` section removed from `tracking-rules`;
  the R gate tokens are absent from the universal "What gets a test" floor and
  present in the `r-package` profile. Guards: `TestRulebookRelocation` (3).
- **AC4** — `milestone.md` template AC guidance carries zero `devtools` tokens
  and references `PROFILE.md`/`verify`. Guards: `TestTemplateProfileAware` (2).
- **AC5** — `cairn/PROFILE.md` present (generic); CLAUDE.md waiver replaced;
  DESIGN.md Purpose & Scope + Architecture name the profile mechanism.
  `cairn_validate` exit 0 (profile valid, scaffold present, coverage complete);
  suites **skills 113 / scripts 65 / hooks 32** green.
- **AC6** — `r-package` profile reproduces every relocated command + guardrail
  specific (`data-raw`, deprecation, Imports/Suggests, assertthat). Guards:
  `test_r_package_profile_holds_relocated_commands`,
  `test_relocated_guardrail_specifics_survive`.

### Consistency gate

- `cairn_validate` — exit 0, all 14 checks + sizing pass.
- Coverage completeness — every AC maps to ≥1 existing task (AC1→T2,T3,T8;
  AC2→T4,T8; AC3→T1,T7,T8; AC4→T5,T8; AC5→T6; AC6→T7,T8). Validated.
- `cairn_impact` — GP3 is *touched* (the milestone instantiates portability)
  but its DESIGN.md wording is unchanged (diff confirms), so no Sync Impact
  Report is due. Skipped per the no-principle-change rule.
- Toolchain checks — active profile is `generic`; its `consistency-gate` slot
  names no checks → clean no-op.

### Independent review
