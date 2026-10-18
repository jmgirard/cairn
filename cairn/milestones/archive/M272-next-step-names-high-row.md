# M272: The next-step recommendation names the first unstarted high-priority candidate

**Status:** done (2026-10-17, PR #284 https://github.com/jmgirard/cairn/pull/284)

**Goal:** When nothing is in review, in progress, or workable, `cairn_next.py` and the cairn pane recommend planning the first unstarted `[high]` candidate row by its short title, and the Plan press plans that row.

**Outcome:** `scripts/cairn_next.py` gains `candidate_texts`, `short_title`, and `high_title` (rows under any `## candidates…` heading, per-section comment strip, JS-trim `JS_TRIM` built from code points, a `STARTED` token with any digits ending at a non-ASCII-alphanumeric); `recommend` returns `title` (None outside planning) and the `Recommended:` line ends `→ /milestone-plan <title>`. `hooks/status/reader.ts` mirrors it (`highTitle`, `NextStep.title`, `recommend(rows, workable, roadmap)`); `pane.ts` `nextTitle` drops the title when the pane's last PR read finds a `Candidate row:` body naming it, and the Next pill and the shared `pressNext` (pane and band `Plan`) use it. Pane state tag `pane-7`; `types/index.d.ts` `next.title`. Fixture `high-candidate`; every fixture's expected `next` gains `title`. README, CHANGELOG, DESIGN.md.

**Decisions:** none promoted. The plan gate chose the first unstarted `[high]` row in ROADMAP order over the row the pane draws, since Python cannot read PR bodies and the parity test needs one rule; falsified by a session where the Next line names a row the Candidates list hides. Token end ASCII-only, as the pane's M258 `STARTED_TOKEN`.

**Review:** user-facing tier, two passes, defect-return count 0, amendment-return count 1 (AC1: token end "ASCII letter or digit", candidate-row rule stated; two re-audits). Claim audit: 41 claims read, 1 corrected. Pass 1: 22 findings, 5 fixed, 6 rejected, 10 to the candidate row "Plan target edges (M272 review)", 1 amendment. Pass 2: 16 fixed (literal invisible characters in `JS_TRIM`, README/CHANGELOG wording, ASCII wording in DESIGN, the type declaration), 13 rejected. Copilot: 1 thread rejected, replied, resolved. Lesson captured on the Edit tool decoding `\u` escapes.
