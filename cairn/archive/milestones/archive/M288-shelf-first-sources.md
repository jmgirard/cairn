# M288: Sessions read the repo's source shelf before they search the web for a paper

**Status:** done (2026-10-19, PR #300 https://github.com/jmgirard/cairn/pull/300)

**Goal:** A session in a cairn repo looks for a cited paper in `cairn/references/` before it searches the web, both inside the cairn skills and in plain conversation.

**Outcome:** `hooks/session_context.py` gains `shelf_section`: when `cairn/references/INDEX.md` has a column-0 `- ` line or `references/sources/` has a top-level entry not starting with `.`, a `## Source shelf` part goes ahead of the ROADMAP part (outside every shedding step). It gives the INDEX entry and shelf entry counts and lists up to 30 names (`SHELF_MAX_NAMES`) in sorted order, with an "and N more" line past 30. Each name has control characters replaced by `?` and is cut to 60 characters (`SHELF_MAX_NAME_CHARS`). INDEX.md is read with `errors="replace"`. The part says to read `INDEX.md`, the note, and the file before searching the web, and that a worktree or fresh clone can have an empty shelf while the main checkout's is full. The preamble names the part. The primary-sources rule in `validation-doctrine.md` now reads the shelf first and says a note without the file does not count as found. A "Shelf first." paragraph in tracking-rules "References pages" covers any source. `/milestone`'s rulebook mass baseline was re-seeded to 753 lines / 72,590 bytes. README and CHANGELOG describe the notice and the rule. Hook tests: 14 shelf cases.

**Decisions:** none promoted. Out of scope: the legacy `references/pdf/` shelf, and deleting the datawizard memory note `check-cairn-shelf-first.md` (the user's to remove).

**Review:** Four lenses and Copilot (Lite). 14 lens findings fixed (newline injection through shelf names, also Copilot's thread; a bad byte zeroing the count; the "source pages" label; no name length cap; the worktree shelf; a note counted as the source; the stale mass baseline) and 9 rejected (planned scope, style, or the hook's existing no-op contract). Copilot: 2 fixed, thread resolved, summary answered once. Claim audit: 30 claims, 4 corrected. No candidate rows filed.
