# M55 — Milestone-file cap exempts the Review section

**Status:** done · approved 2026-07-13 · PR #53

## Goal
Cap a live milestone file on its plan-owned body only (lines before `## Review`),
exempting the review-exclusive `## Review` section.

## Outcome
`check_caps` measures the plan-owned body against `MILESTONE_CAP` (unchanged at
150) via a new fence-aware `milestone_body_line_count` (tracks ```/~~~, matches an
exact `## Review`; no-Review files count whole — back-compat). Ends the recurring
evidence-vs-cap scramble (M19/M22/M33/M50) without loosening plan discipline.
Rulebook + template state the exemption; `test_milestone_cap_exemption.py` locks
the wording + stated↔enforced 150, both blocks mutation-registered.

## Decisions
- D-030: cap the plan-owned body only, `## Review` exempt (parallels D-018);
  rejected split-budget 120/40, a Review sub-cap, exempting `## Decisions`.

## Review
All 5 ACs verified fresh; `cairn_validate .` exit 0 (generic → no toolchain check;
no principle touched). 3-lens review: blame + prior-PR clean; diff-bug found a
prefix-match boundary bug (`## Reviewers` could truncate the scan) — scored 82,
fixed in-review (exact match + regression test). scripts 73 + skills 153 green.
