# M258: Started token on candidate rows

**Status:** done (2026-10-15, PR #269 https://github.com/jmgirard/cairn/pull/269)

**Goal:** A candidate row that a planned or handed-off milestone absorbs, or that an open guest hotfix PR fixes, draws the started mark `◐` in the cairn pane through a ` — started <ref>` token on the row itself.

**Outcome:** `/milestone-plan` step 6 ends each candidate row a plan absorbs with ` — started M<NNN>`, both modes; `/hotfix`'s guest arm ends each matched row with ` — started #<n>` on disk after its create. `startedTokens` and `takenRows` in `reader.ts` read the tokens into `PaneState.taken` (tag `pane-6`): a token ends at any non-letter-or-digit, an M id counts while its row is `planned` or `blocked` and not archived as done, given padded. `startedRefs` in `pane.ts` marks a row by body lines, listed #n tokens, and M tokens; the tail shows the lowest PR number, else the lowest id; no ✎, and `pressCandidate` refuses a stale press. tracking-rules "Candidate started token", records-hygiene §1 and hotfix step 7 drop a narrowing work's token. README, DESIGN, CHANGELOG, D-165. Mod tests 1759.

**Decisions:** D-165. The plan chose the row token over a milestone-file line and over a hotfix or tracker file.

**Review:** One defect return (AC1's done, dropped, and absent cases were only in reader.test.ts) and one amendment return (AC6's "only through the tokens" was false, since hand-written lines count). Claim audit: 48 claims, 4 corrected (a false no-`upstream` claim). Pass 2 three lenses, 31 findings: 11 fixed (token end rule, padded ids, archived blocked rows, `pane-6` in DESIGN, hotfix narrowing text, D-165 and README clauses), 9 to "Started mark edges (M252 review)" and "Plan Button edges (M242 review)", 11 rejected. Copilot (Lite) 2 threads fixed and resolved. No lesson captured.
