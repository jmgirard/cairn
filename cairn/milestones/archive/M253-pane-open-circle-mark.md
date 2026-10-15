# M253: A normal candidate row's mark is an open circle

**Status:** done (2026-10-15, PR #264 https://github.com/jmgirard/cairn/pull/264)

**Goal:** In the cairn pane, a normal-priority candidate row that no open pull request names leads with `○` in place of `·`, so the candidate marks read ↑ high, ↓ low, ○ normal, and ◐ started at any priority.

**Outcome:** `PRIORITY_MARK.normal` in `pane.ts` is `{ text: '○' }`, the
glyph `OPEN_MARK` uses, in the default text color. The pane tests state
each mark as a literal through a hand-written `MARKS` map, assert
`PRIORITY_MARK` and `STARTED_MARK` whole, and expect `○` in the M207
fixture lines, the M242 ✎ rows, and M252's unmarked line. README's mark
list, DESIGN.md's ambiguous-width list (`↑ ○ ↓`, and `◐`, an M252 gap),
and CHANGELOG name the change.

**Decisions:** none promoted. The question set chose the default text
color and a look at the merge question; that look could not run, since
an active milestone hides candidate rows, so it follows the merge.

**Review:** claim audit, 12 claims, 2 corrected. Three lenses and Copilot
(Lite), 19 items: 6 fixed (AC2's DESIGN span twice reported, the
CHANGELOG ◐ clause, the test's single literal map and bold check, a code
comment), 12 rejected, 1 noted. Nothing retired.
