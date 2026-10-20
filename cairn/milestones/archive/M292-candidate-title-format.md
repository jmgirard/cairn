# M292: Candidate row titles are one short sentence that fits the cairn pane

**Status:** done (2026-10-19, PR #304 https://github.com/jmgirard/cairn/pull/304)

**Goal:** A candidate row's short title says what the work would do in one sentence of at least 5 words that fits the desktop cairn pane's line, ending with its GitHub issue number when it has one.

**Outcome:** tracking-rules "Candidate short title" tells a writer to open a row with one sentence, no ending period, at least 5 words (runs between spaces, less a trailing issue reference; no floor for a script written without spaces) and at most 40 characters (a wide character counts 2), sized to the room the desktop's docked pane leaves for a candidate line at rest. An issue row ends its title with `(#N)`, or `(#N, #M)` where it fits; an issue absorbed later goes in the detail. New example titles replace `ordinal REML` and `Home Button edges`. `/cairn-triage`'s Title class flags fewer than 5 words or more than 40 characters in place of over 60 code points, and new titles take the bounds and the issue reference (forms: `/issues/N`, `<base-repo>#N`, `(#N)` ending the old title, `#N` the row calls an issue). README, the `/cairn-init` skeleton comment, and the CHANGELOG's Unreleased entry state it. Rulebook baseline re-seeded to 761 lines / 73,442 bytes.

**Decisions:** D-189 (annotates D-108, D-163, D-164; D-108's door excepted by name at the user's decision). Question set: go ahead past the door; a cap that fits the pane over the user's first 5-15 words; existing rows left for the next `/cairn-triage`. Plan gate: 40 characters at rest over 34 under the pointer.

**Review:** Criteria audits at plan, 10 then 6 findings, all taken. Claim audit: 44 claims, 3 corrected. Four lenses and Copilot (Lite, one thread; summary reply posted), 24 items: 7 fixed (title's own `(#N)` kept on retitle, no word floor without spaces, guest-mode issue forms, D-189 heading, a doubled colon, line wraps), 3 to the new rows "Keep tier check for issue-titled rows" and "Keep rows named by open PRs at triage", 14 rejected. No lessons added or retired, nothing unparked.
