# M257: Started mark skips fenced lines

**Status:** done (2026-10-15, PR #268 https://github.com/jmgirard/cairn/pull/268)

**Goal:** A `Candidate row:` line quoted inside a fenced code block of a pull-request body no longer marks a candidate row, and README says where the mark comes from and when it goes.

**Outcome:** `startedRows` in `pane.ts` keeps a per-body `fenced` flag that a module-private `FENCE_LINE` (`/^ *(```|~~~)/`) toggles: any fence line closes an open fence, and each body starts closed. pane.test.tsx gains cases for backtick, tilde, and spaced fences, mixed-character closes, and an unclosed fence followed by a next body. README says only owner-mode `/hotfix` and `/milestone-review` write the line, which line format and title count (hand-written lines too), that fenced lines do not count, and that `◐` goes at the first successful PR read after the merge, after which the row shows its priority mark until hygiene removes it. DESIGN and the unreleased CHANGELOG entry state the fence rule.

**Decisions:** none promoted. Implement read AC1's "optional spaces" as any number of spaces and folded the CHANGELOG sentences into the unreleased started-mark entry.

**Review:** Two passes of the three-lens fan-out. Pass 1 found AC2's "shows no mark" false of the code (the priority mark returns), so it took an amendment return; two Opus re-audits narrowed AC2, and the user adopted the final wording at the second-re-audit stop. 13 findings fixed (antecedents, a mixed-fence test, README conditions on hand-written and guest lines and on clearing, DESIGN), 13 rejected. "Started mark edges (M252 review)" lost its fence and merge-to-hygiene edges and took the 6 follow-ups (fence forms CommonMark reads differently, mark clears without a successful read), in place of the separate row the merge question named, to keep ROADMAP under its line cap and byte budget. ROADMAP's two widest rows were compressed for the same reason. Copilot (Lite) raised 2 threads, both already fixed, replied and resolved. The claim audit corrected 3 of 16 claims. No lesson captured.
