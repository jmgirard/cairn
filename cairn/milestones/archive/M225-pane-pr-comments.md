# M225: The pane counts each handed-off PR's unanswered comments

**Status:** done (2026-10-09, PR #233 https://github.com/jmgirard/cairn/pull/233)

**Goal:** On request, each open handed-off PR in the cairn pane also shows its unresolved review threads and the reviews and comments from others that are newer than its author's last comment, review, or commit.

**Outcome:** After a `gh pr view` whose word is in `OPEN_WORDS`, `readPrs`
runs one `gh api graphql` query (`counts.ts`, `countsArgv`), 15 s timeout.
`prNodes` checks the reply's shape. `countPr` counts threads with
`isResolved` false, and others' COMMENTED or CHANGES_REQUESTED reviews and
conversation comments after the anchor. The anchor is the author's newest
review or comment, or the PR's newest commit time from anyone, in UTC. The
`prs` atom holds `{ word, counts }` (`CairnPrRead`, tag `prs-2`), written
once every call settles. `paneLines` draws `blocked-<id>-counts` at indent 4.

**Decisions:** none promoted. The anchor rule stands in for reply tracking,
since GitHub links no reply to a review or a conversation comment. The look
used insight PR 880 through a temporary M007 header, since PR 1250 counted
zero. The operator accepted it at the merge question.

**Review:** claim audit, 66 claims, 5 corrected. Three lenses, 22 findings:
4 fixed (UTC commit time, timeout comment, DESIGN wording, one counts type),
13 to "Pane count edges (M225 review)" or the M224 row, and 5 rejected. Mod
tests went to 1739. Nothing retired.
