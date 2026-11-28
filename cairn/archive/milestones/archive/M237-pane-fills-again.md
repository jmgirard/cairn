# M237: The pane fills again after a resume or a hidden-tab clear, and reads each PR with one call

**Status:** done (2026-10-10, PR #247 https://github.com/jmgirard/cairn/pull/247)

**Goal:** The cairn pane fills its lines at each session start that empties the host's state. It shows ⋯ only during a read of its own, and it reads each github.com pull request with one `gh` call.

**Outcome:** `classic.SessionStart` with source `resume` reads the files
again, as `clear` does. Both start `readPrs` for a placed pane through the
new `isPlaced`, shown or behind another tab. A module-level `inFlight`
count gates ⋯ beside the stored `reading`, and a failed write of false asks
for a redraw. `prRead` in `counts.ts` reads the word and the thread count
from one `gh api graphql --hostname github.com` reply. `wordOf` in
`pane.ts` maps the state for `prRead` and `prWord`, and `prCounts` is gone.
A URL on another host keeps one `gh pr view` call and no count. The test
fake merges its two answers into one reply and records `reads`. Captured
PR #246 and PR #247 replies are fixtures. Mod tests went to 1592.

**Decisions:** none promoted. At the question set the user picked the
visible fixes only, merged the three "Pane edges" rows, and dropped their
test-gap items. No live look.

**Review:** claim audit, 56 claims, 3 corrected. Three lenses, 27 findings:
8 fixed, 9 to candidate rows ("Pane edges (M237 review)" and the older
row), 10 rejected. Copilot (Lite) had one thread, fixed. No test covers the
redraw after a failed write. Nothing retired. The M191 lesson was extended.
