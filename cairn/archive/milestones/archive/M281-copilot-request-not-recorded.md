# M281: A Copilot request that GitHub does not record is reported

**Status:** done (2026-10-18, PR #293 https://github.com/jmgirard/cairn/pull/293)

**Goal:** When the Copilot request command exits 0 but GitHub records no request, the round says so in one line instead of reporting nothing.

**Outcome:** `skills/shared/copilot-review.md` §2 runs the §3 state query once more after a zero-exit `gh pr edit <N> --add-reviewer @copilot`; on `none` it reports `Copilot request on PR #<N> may not be recorded by GitHub (used-up Copilot credits are one cause)`, makes no second request at that step, and adds no wait. §6 names that line among the reasons no review exists. Other module text was compressed to hold the 140-line / 8,000-byte budget (139 lines, 7,993 bytes). README Copilot paragraph and a CHANGELOG Unreleased Fixes entry state the same. Triggered by PR #291 and #292, whose requests GitHub dropped while the user's Copilot credits were used up; the line ran live on PR #293 in both review passes.

**Decisions:** none promoted. Question set: plan the report even though used-up credits explained the drops; report and go on, no retry through a second command. Plan gate: an immediate re-query over a delayed one. Criteria audit (full): 6 findings fixed. AC3 amended once ("goes on without Copilot" was false under §4's read-time wait), re-audited.

**Review:** user-facing, three-lens fan-out, two passes, defect-return count 1 (AC1: the line stated "not recorded" as fact where AC1 requires "may not"), amendment-return count 0. Claim audits: 17 claims, 3 corrected; 13 claims, 1 corrected. 33 findings: 1 return, 7 fixed (wording and wraps), 6 to the new row "Copilot not-recorded edges (M281 review)" (a late-recorded request gets a false line; a later pass that reads `none` requests again, which pass 2 did on PR #293 and which D-153 names as its falsifier, though GitHub recorded neither request; step 7's presentation omits §6's reason line), 19 rejected. Graduated the candidate row "Copilot request not registered". No lesson captured or retired.
