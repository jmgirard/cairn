# M113: Bounded session-start injection — cap-exempt sections read-bounded newest-first, and the active milestone file joins the always-read frame

**Status:** done (2026-07-25, PR #113 https://github.com/jmgirard/cairn/pull/113)

**Goal:** Make the SessionStart injection tell a resuming session the truth
about current state, and give that surface the three frame elements.

**Outcome:** `session_context` gains `heading_name`/`split_sections`/`_blocks`/
`bounded_tail` and a reallocated `build_context`. Cap-exempt sections inject
their newest entries within `SECTION_MAX_CHARS = 6000` (the measured p90 of
both types over 111 files), each elision marked with counts and path; capped
sections inject whole, and headings normalize as `_plan_owned_scan` does
(lowercased, fence-aware). Actives inject `in-progress`→`review`→`blocked`,
keeping header and path when the budget binds; an oversized ROADMAP truncates
with its own marker. On M95's 65-entry log the newest entry goes absent→present.

**Decisions:** the 6,000-char budget and its measured basis; degradation order
by status. Cross-cutting: D-063 (the frame's fifth row).

**Review:** three lenses + scorer; blame-history and prior-PR clean. Round 1:
F2 (92) headers lost to an oversized ROADMAP, F1 (85) prose above a section's
first entry neither bounded nor marked, F3 (80) heading match diverged from the
cap's — fixed, F4 (75) logged; AC1/AC4 failed as written, milestone returned.
Round 2 on the fixes: R2-F1 (a regression — the second pass undid the entry
floor), R2-F2, R2-F3 fixed; R2-F4 rejected.
