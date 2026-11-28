# M291: The cairn pane's summary card names the project at its top left

**Status:** done (2026-10-19, PR #303 https://github.com/jmgirard/cairn/pull/303)

**Goal:** The cairn pane's summary card shows the project's name in bold at the left of its first line, before the open pull request and issue counts.

**Outcome:** `card-repo` holds the name bold in its `text` (cut first, `truncate-end`) and the counts in its `tail`. A new `tailGrows` flag gives the tail Box `flexGrow: 1`, so ⌂ and ↻ sit at the right end, and the first line no longer sets `grow`. `projectName` in `repo.ts` picks the repo part of a github.com base remote URL, else the folder holding a common git dir named `.git` (`COMMON_DIR_ARGS`, `git rev-parse --path-format=absolute --git-common-dir`, run only without a github.com URL, last output line only for git before 2.31), else the root's `lastSegment`. `readRepo` writes `name` even when the `gh` call fails. `CairnRepoRead` gains `name`, and the `repo` atom moves to shape `repo-3`. `paneLines` takes the root and names its last segment while no read for that root is stored, so a worktree shows its own name until the read. README, DESIGN, the CHANGELOG's Unreleased card entry, and code comments describe it. Mod tests went from 2304 to 2332.

**Decisions:** none promoted. Question set: the name on the counts line (over a new title line), bold (the user's mid-plan ask), no live look (a hand-built browser preview stood in). Plan gate: GitHub name with main-tree fallback over the root folder alone, folder name before the read over a blank.

**Review:** Criteria audits at plan, 5 then 3 findings, all taken. Claim audit: 48 claims, 3 corrected. Four lenses and Copilot (Lite, no threads; summary reply posted), 24 items: 12 fixed (old-git output, stale comments and DESIGN text, a test literal), 3 to the new parked row "Card name edges" (no hover card for a cut name, odd repo segments, no live look), 9 rejected. No lessons added or retired, nothing unparked.
