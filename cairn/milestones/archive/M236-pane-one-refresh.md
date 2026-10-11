# M236: The pane has one ↻ Button and counts only unresolved threads

**Status:** done (2026-10-10, PR #246 https://github.com/jmgirard/cairn/pull/246)

**Goal:** The cairn pane shows only the unresolved review threads of each PR, and one ↻ Button at the right end of the pane's first line reads everything again and shows ⋯ while a read runs.

**Outcome:** `counts.ts` queries only `reviewThreads(last: 100)`, and
`countPr` gives `{ unresolved }`. The `unanswered` count and its anchor
rule are gone (`CairnPrRead`, tag `prs-3`). The PR #245 reply is a fixture.
`paneLines` gives `refresh` and `grow` to its first line, the first head
line or `no-active`, and the render grows that line's text Box. The heading
Refresh Buttons and the `-hotfixes` key are gone. A `reading` atom
(`reading-1`) makes the label `⋯` until the newest read settles, and each
write rechecks `prReads`. A module-level `pressing` flag ignores a press
during an earlier press's read. Head lines lead with the id in
`PHASE_COLOR`, with no phase word.

**Decisions:** none promoted. The first live look moved ↻ off its own row,
dropped the phase word, and swapped `dimColor`, unseen on the desktop
Button, for `⋯`. The operator accepted the second look.

**Review:** claim audits read 80 claims and corrected 4. Three lenses gave
24 findings: 8 fixed (the reading-flag race, stale comments and rows, tests),
6 to "Pane edges (M236 review)", 10 rejected. Copilot (Lite) found none.
Mod tests went to 1560. Nothing retired.
