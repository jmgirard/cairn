# M215: Move this repo to the claude-plugin profile

**Status:** done (2026-10-04, PR #222 https://github.com/jmgirard/cairn/pull/222)

**Goal:** This repo declares the `claude-plugin` toolchain profile in place of `generic`, with its own Python suites kept as gating checks.

**Outcome:** `cairn/PROFILE.md` was rebuilt from
`skills/shared/profiles/claude-plugin.md`. verify gates on five checks: the
`scripts/tests` and `hooks/tests` suites, `claude plugin validate` on
`plugin.json` and on `marketplace.json` (new), and `claude plugin test .`.
consistency-gate adds the marketplace version-warning check and a changelog
entry for user-visible changes, and keeps the no-CI note. release-walk bumps
`version` in both manifests. test-doctrine keeps the no-`pytest` rule and
says `skills/tests` gates nothing. `CLAUDE.md` and `cairn/DESIGN.md` name the
new profile. Promotes the candidate row "cairn's own profile" (M192 Out).

**Decisions:** none. D-143's checks are kept, and the marketplace validate
is credited to M215.

**Review:** one return (AC4: test-doctrine did not say `skills/tests` gates
nothing), fixed in T5. Second pass: one Opus diff reviewer, 7 findings: 3
fixed (the D-143 credit, the other-runner test warning, the prose-guard
wording), 1 to the candidate row "claude-plugin profile edge cases" (no
stated lowest Claude Code version), 3 rejected (1 false, 2 planned changes).
Nothing retired.
