# M311: Link the pane card to the repo on GitHub

**Status:** done (2026-10-21, PR #325 https://github.com/jmgirard/cairn/pull/325)

**Goal:** In the desktop app, the name and counts on the cairn pane's summary card open the project's GitHub pages.

**Outcome:** `webOf` in `hooks/status/repo.ts` gives the repo page of a github.com base remote whose owner and repo match `[A-Za-z0-9._-]+`, are not `.` or `..`, and fit GitHub's 39 and 100 characters, else null. `readRepo` stores it as `web` in the `repo` value (`CairnRepoRead`, shape `repo-4`). `Span` gains `href`. `cardLines` links the name to the page and each count and its word to `/pulls` or `/issues`. Off the terminal, `register.tsx` draws the name and each run of spans with one `href` as one `Link` in a `Text` with `wrap: 'truncate-end'`. Inside it each span is a `Text` in its own style, the theme's `text` color where it names none, with `underline: false`. The terminal draws no `Link`, since a terminal without OSC 8 prints the URL and would push ⌂ and ↻ off the row. README, DESIGN.md, and CHANGELOG follow.

**Decisions:** none. Two live looks set the drawing: look 1 found a bare `Link` blue, underlined, and split per span, and look 2 approved the grouped, card-colored form. AC3 and AC4 were amended to match, and the 44-column row-fit clause was dropped as unevidenced.

**Review:** Criteria audit at plan (full, 7 findings fixed). Claim audit 44 claims, 3 corrected. Two re-audits of the amended AC3 and AC4. Four fresh reviewers: 17 findings, 9 fixed (name length cap, wrap on linked Texts, fixture `web`, doc wording, README antecedent), 8 rejected (none as `edge`), 0 to candidate rows. Copilot (Lite): 1 body item fixed. Hygiene: M308 row pruned to the terminal cap; one mod fact added to the existing LESSONS line; no row unparked.
