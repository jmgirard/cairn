# M46: Rewire operational slots — implement/review/hotfix/doctrine read the profile; dogfood generic

**Status:** done · PR #44 · merged 2026-07-13 · milestone 2 of the toolchain-profiles arc (M45 spine, M47 release).

## Goal
Rewire the operational skills + the rulebook's language-mechanical doctrine to read the active profile's slots instead of hardcoded R commands, and dogfood the `generic` profile in this repo.

## Outcome
- `milestone-implement` (per-task/resume/completion) + `hotfix` gate-lite now run the active profile's `verify` slot; no literal `devtools::` left.
- `milestone-review` consistency gate split: **universal cairn-file checks** (validate/coverage/impact) stay unconditional; toolchain checks come from the profile `consistency-gate` slot (generic → clean no-op).
- `tracking-rules` "R package guardrails" + the R half of "What gets a test" relocated into the `r-package` profile (added the generated-file `NAMESPACE`/`man`/`data` guardrail there); universal floor kept + framing "profiles supply language mechanics; oracle doctrine stays universal".
- `milestone.md` template AC guidance de-R'd → references the profile.
- Dogfood: this repo declares `cairn/PROFILE.md` = `generic` (verify = its `python3 -m unittest` suites); CLAUDE.md waiver replaced; DESIGN.md Purpose & Scope + Architecture name the language-agnostic core + profile mechanism.
- Guards flipped source-of-truth to the profile; `test_toolchain_profiles` grew 3→15 assertions incl. the M47 `cairn-release` boundary.

## Key decisions
- No new D-entry (mechanism settled in M45; this is the rewire). GP3-instantiating; GP3 wording unchanged.
- Guard tests folded into each task commit (not a separate T8) to keep the suite green per checkpoint — minor amendment.

## Review
- ACs 1-6 fresh-verified; suites 113/65/32 green; `cairn_validate` exit 0.
- Independent review: 1 diff-bug finding (scored 82) — `testthat` edition-3 convention dropped in the relocation; fixed by relocating it into the r-package `test-doctrine` slot + a guard. Blame-history & prior-PR lenses clean.
