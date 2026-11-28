# M223: The pane lists blocked milestones and their PRs

**Status:** done (2026-10-08, PR #230 https://github.com/jmgirard/cairn/pull/230)

**Goal:** The cairn pane lists each `blocked` milestone and the pull request its header names, so the operator sees waiting PRs without running `/milestone`.

**Outcome:** `scripts/cairn_next.py` gained `blocked`, `pr_number`, and
`read_file`. `pr_number` reads the first `Branch/PR` line above the first
`## ` heading. It takes the first GitHub pull URL before any `companion:`
entry, at most 15 digits, with spaces and tabs spelled out. The
"Externally blocked" lines end with ` (PR #<n>)`. `reader.ts` mirrors it
as `prNumber` and a `blocked` list, and `pane.ts` draws a `BLOCKED`
section after the queue in every state, the number in the line's tail.
The pane shape tag is `pane-3`. Fixtures `blocked-prs` and
`blocked-active` hold both sides to the same values. Docs describe it.

**Decisions:** none promoted. T5 became the look's preparation, and the
look ran at the merge question. There the operator asked for unresolved
threads and unanswered comments, Copilot's included, and chose to add them
to M224.

**Review:** claim audit, 44 claims, 2 corrected. Three lenses, 34
findings: 17 fixed (regex parity, header-only read, digit cap, 4 tests,
docs), 4 to "Blocked-row PR number edges (M223 review)", 7 rejected, the
rest duplicates. Mod tests went to 1442. Nothing retired.
