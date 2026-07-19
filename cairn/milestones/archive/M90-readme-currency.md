# M90: README currency — the front door catches up with what shipped

**Status:** done · 2026-07-19 · PR https://github.com/jmgirard/cairn/pull/89

**Goal:** make the README describe what 1.1.0 shipped, and make the profile
enumeration a guarded surface so it cannot silently go stale again.

**Outcome:** new `## Keeping track of sources` section; the "does NOT do" list
now states cairn never proposes or nominates a release (D-050's user-facing
half); the install section names each advisory nudge by its trigger;
`/cairn-release` row profile-neutral; `LESSONS.md` joins the file map and
boundary rule. The structural piece is `TestShippedProfilesAreAdvertised`,
deriving the list from `skills/shared/profiles/` and requiring every shipped
profile in README ¶1 and both manifests — M54 pinned ¶1's *framing* but never
its *list*, so M70's fourth profile left three surfaces green and wrong.
M90-D1: derived guard over a hand-maintained tuple (the pattern that had just
failed); hook-inventory derivation stays Out.

**Review:** 8/8 fresh, AC4 proven differentially; gate clean. Diff-bug [O] and
blame-history [S] independently reproduced the same two defects; prior-PR [S]
a clean no-op; none sub-threshold. F1/96 — the manifest guard never checked
`plugin.json`: a mis-indented inner loop ran once against the last-bound text,
defeating the milestone's premise inside the guard meant to fix it. F2/82 —
"two advisory nudges" against three shipping and `DESIGN.md:55`; fixed by
dropping the count, not restating it. Both fixed on the branch.
