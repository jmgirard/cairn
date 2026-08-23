# M87 — Density-threshold recalibration — the weight axis is derived from what records actually cost

**Status:** done · approved 2026-07-19 · PR #86

## Goal
Re-derive both `record density` thresholds from the mass the item caps actually permit.

## Outcome
M84-D1 derived both as `item_cap × target_mean` without measuring either mean — LESSONS
`50 × 340` against a real 581, ROADMAP `60 × 150` against a blended 497 — so both bound
BEFORE their line caps (29 lessons against capacity 35; ROADMAP 16 against 40), firing at
ordinary density with no remedy but compressing unrelated lessons, three passes running.
The item axis sat inert meanwhile: lessons are consolidated not appended, and consolidating
raises the mean itself. Now: non-item mass + capacity × measured mean, rounded up to 500,
capacity = `(cap − 1) − non-item lines`. LESSONS < 20,500, ROADMAP < 21,000.

## Decisions
D-049 (supersedes M84-D1): thresholds are the mass each line cap permits at MEASURED item
length; measure, never assume. Rejected a mean-drift test. M87-D1 holds the arithmetic.

## Review
3 lenses + scorer: blame clean, no prior-PR evidence, diff-bug 6. Fixed F1/90 (LESSONS.md's
header — a third encoding — still taught 17,000; now guarded), F5/80 (capacity read the cap
inclusively though it fails at `>=`, moving both values down), F6/75 (AC1 required the
command). F2/60 recorded, F3/45 rejected, F4/40 reworded. Also retired M84's prune anchor.
