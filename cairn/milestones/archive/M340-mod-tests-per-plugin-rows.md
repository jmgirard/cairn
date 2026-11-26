# M340: Fix mod tests that fail on main

**Status:** done (2026-11-25, PR #355 https://github.com/jmgirard/cairn/pull/355)

**Goal:** The status mod's test suite passes on the installed `claude` binaries again, with its band tests written for the engine's per-plugin `AbovePrompt` rows.

**Outcome:** Claude Code (2.1.323, 2.1.331) asks each plugin for its own `AbovePrompt` row and draws the engine's slot after them. 19 tests in `hooks/status/band.test.tsx` failed on main: the PROBE plugin's `next.trace` no longer listed cairn's link, and a plugin that never calls `next` no longer hid the engine's slot. PROBE is removed. The two no-roadmap cases assert only `[ENGINE]` and are renamed "draws nothing and the engine's slot shows". The M213 empty-row cases rely on `isEmptyRow`. The five other-plugin cases expect the engine's slot after that plugin's row, and the "shows alone" case is renamed. A vacuous `not.toContain(BENEATH_ROW)` and two unproven `keepsBeneath()` checks are gone, and the BENEATH and `lines()` comments describe the new order. `claude plugin test .` passes 2466 of 2466 under both binaries. The mod's code is unchanged.

**Decisions:** none cross-cutting. AC2 (a planted-throw discrimination) was removed at implement, because a planted first-statement throw stops the test file from loading and the kit gives a test no skipped-hook signal; a state-read check was weighed and not taken.

**Review:** Reduced criteria audit at plan (findings taken). Four lenses plus Copilot: 9 fixed, 8 to the parked row "Recheck band tests for per-plugin rows" (thrown hook in the no-roadmap cases; other-plugin cases test engine stacking), 5 rejected. Copilot at Low: one thread (T1 claimed the signal search delivered) fixed and resolved, no comment. Hygiene: graduated "Fix mod tests that fail on main"; M337 row pruned; `used M340` on the M56, M286, and M321 lessons; no lesson captured.
