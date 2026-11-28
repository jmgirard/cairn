# M39 — Search-first candidate creation

**Status:** done · approved 2026-07-12 · PR #37

## Goal
Before any candidate row is added — by any skill or conversationally — sweep
existing candidates, the archive, and DECISIONS for overlap and absorb or
cross-reference a hit instead of adding a duplicate.

## Outcome
- `tracking-rules.md` gained a "Search-first candidate creation" rule after the
  Intake paragraph: sweep existing candidates + `milestones/archive/` +
  `DECISIONS.md`; on a hit absorb/cross-reference, don't duplicate; a standing
  rejection is recorded once, following the supersede discipline. Generalizes
  the plan-time collision check to every candidate-creation point.
- One-line pointers (not restatements) at `/hotfix` step 7 and
  `/milestone-review` finding-triage; `test_search_first_candidates.py` (4)
  locks the rule + both pointers. Skills 89 + scripts 53 green; validate 12/12.

## Key notes
- Independent review: 1 finding (scored 88) — the guard's archive/DECISIONS
  assertions matched pre-existing text elsewhere in the file, not the rule;
  fixed by anchoring on the rule's own contiguous phrasing.
- Rejected: a mechanical fuzzy duplicate-detector (noisy, over-scope).
- Graduates the "search-first candidate creation" M06-steal candidate.
