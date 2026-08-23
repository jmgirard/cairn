# M92 — Lesson retirement — a lesson leaves LESSONS.md when a guard enforces it

**Status:** done · approved 2026-07-19 · PR #91

## Goal
Give `cairn/LESSONS.md` an outflow, not only a ceiling.

## Outcome
The file hit both caps at once — 49 lines against a capacity of 49 — so the next
hygiene pass could not capture a lesson, and D-015's prune-by-age was the only
exit. Two criteria now retire one: **enforcement** (a test *fails* on the mistake
it warns about, not merely that a guard exists) and **ownership** (another file's
slot owns it; the milestone may *move* it there); partial coverage trims to the
remainder. Applied: 2 retired into `PROFILE.md`, 2 trimmed, 3 consolidated → 47.

## Decisions
D-051 (annotates D-015, distinguishes D-045): both criteria, trim-to-remainder,
archive-summary tombstone. Rejected in-file breadcrumbs (D-049), a separate
graduated file (M56), age-pruning, full-sweep re-evaluation. Graduated the
M87-Out candidate; formalizes what M53 improvised by hand.

## Review
3 lenses + scorer: blame 0, prior-PR 0 (measured no-op, 29 PRs `comments=0`),
diff-bug 3. F1/92 — the ownership "may move" clause, added by a gate amendment,
was pinned by nothing. F3/78, F2/68 sub-threshold, fixed anyway under M73.
