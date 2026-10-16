# M261: The cairn pane hides started candidate rows

**Status:** done (2026-10-16, PR #272 https://github.com/jmgirard/cairn/pull/272)

**Goal:** The cairn pane's Candidates list leaves out each candidate row that work has started, in place of drawing it with the started mark `◐`.

**Outcome:** `paneLines` in `pane.ts` filters out each candidate row that `startedRefs` marks (an open PR body's `Candidate row:` line, a listed `#<n>` token, a counted `M<NNN>` token) before the heading. The heading counts the drawn rows and is not drawn when none is left. A drawn line keeps `candidate-<i>` and ✎ target `i`, its index in `state.candidates`, so `pressCandidate`'s lookup is unchanged. `STARTED_MARK` is removed. The readers, tokens, and body lines are unchanged. README, DESIGN, tracking-rules "Candidate started token", hotfix and milestone-review SKILL.md, and the unreleased CHANGELOG entries (rewritten in place) describe the hiding. Mod tests 1777.

**Decisions:** D-167 (annotates D-165 and D-166). The question set chose hiding with no trace over a gray count line and over moving the rows last, a count of the rows shown, and no live look.

**Review:** No returns. Criteria audit (full): 4 findings fixed (DESIGN.md provenance line spared, D-entry task, keys pinned, neighbour case). Claim audit 52 claims, 1 corrected. Three lenses, 20 findings: 13 fixed (a kit test's positive control, D-167's milestone-PR sentence, hotfix SKILL.md condition, test names and controls, README wording, the "Started mark edges (M252 review)" row reworded), 5 rejected, 2 logged as follow-up to "Plan Button edges (M242 review)", which M260's hygiene had already pruned at the user's choice, so not refiled. Copilot (Lite) 1 thread fixed and resolved. No lesson captured; nothing retired.
