# M301: Show each open PR's merge state in the pane

**Status:** done (2026-10-20, PR #315 https://github.com/jmgirard/cairn/pull/315)

**Goal:** Each open pull request line in the cairn pane shows an icon that tells whether the PR can merge or has conflicts.

**Outcome:** The pane's PR read asks GitHub for `mergeable`: `COUNTS_QUERY` in `counts.ts` gains the field, and the `gh pr view` call for a URL on another host uses `PR_VIEW_FIELDS` (`state,reviewDecision,mergeable`) through `prViewRead`, which replaced `prWord`. `mergeOf` in `pane.ts` maps MERGEABLE to `mergeable` and CONFLICTING to `conflicts` for a word in `OPEN_WORDS`; UNKNOWN, any other value, an absent field, and a word that is not open give null. `CairnPrRead` gains `mergeable`, and the `prs` shape tag moved to `prs-4`. `prLine` ends an open line's tail with `MERGE_MARK` after the word: the `mergeable` icon (a green merge symbol, `✓` in the terminal) or the `conflicts` icon (a red disc with an ink cross, `✗`), with `red` added to `ICON_COLORS`. `centers` also centers a row with a tail icon. README, CHANGELOG, and DESIGN describe the mark.

**Decisions:** none promoted. Question set: an icon for both states; a throwaway draft hotfix PR for the live look. Plan gate: the mark last in the tail over beside the number; `mergeable` over `mergeStateStatus`. Implement: a disc-and-cross for conflicts over a red merge symbol, so the two differ by shape.

**Review:** Criteria audit at plan (full, 6 findings, all fixed). Claim audit 36 claims, 1 corrected. Live look on draft PR #314 (closed unmerged): red mark, then green after ↻, both themes. One pass of four lenses: 17 findings, 4 fixed (open-only check in `prLine`, README wording, `prWord` removed, 13 stale doc and comment lines), 12 rejected, 1 noted. Copilot (Lite, no threads, 1 body item rejected; summary reply posted). No returns, no amendments. Hygiene: M298 row pruned to the 3-row terminal cap. No lessons added or retired, nothing unparked, no candidate row graduated.
