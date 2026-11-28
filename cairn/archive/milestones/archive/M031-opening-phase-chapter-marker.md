# M31: Mark the opening phase — drop the "session start implicit" carve-out

- **Status:** dropped (2026-07-12)
- **Branch/PR:** m31-opening-phase-chapter-marker · PR #29 (closed unmerged)

## Goal (as planned)

Drop the "session start implicit" carve-out so a session's opening phase marks
a chapter and becomes navigable in the Claude Code TOC.

## Why dropped

Premise false. Review (blame-history lens), confirmed against the primary
in-repo source, found the opening phase is **already** navigable:
`references/desktop-toc-mechanism.md:29-30` (M27's live probe) records one
`mark_chapter` call yielding a two-entry outline — `"Session Start" (implicit)`
+ the marker — and the `mark_chapter` docstring says "do not mark the very first
message." So `main`'s carve-out and D-021 were correct; M31's D-024 + rulebook
reword asserted a false "no auto session-start node" claim, mis-citing M27/D-020.
Built branch abandoned unmerged. Residual (empty TOC in single-phase sessions;
generic "Session Start" label) needs marking the first message + live Desktop
probing (D-020) → parked as a ROADMAP candidate. Detail: PR #29 commits.
