<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M39: Search-first candidate creation

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m39-search-first-candidate-creation

## Goal

Before any candidate row is added — by any skill or conversationally — sweep
existing candidates, the archive, and DECISIONS for overlap and absorb or
cross-reference a hit instead of adding a duplicate.

## Scope

**In:** a "search-first candidate creation" rule in `tracking-rules.md`
(sweep targets + on-hit action), generalizing the plan-time collision check
to every candidate-creation point; brief pointers at the ad-hoc creation
steps that run outside that check (`/hotfix`, `/milestone-review`); a
prose-guard test.

**Out:** a mechanical duplicate-detector (fuzzy row-overlap script/validate
check → candidate; noisy, over-scope — the rule is judgment-based like the
plan collision check); restating the rule in each skill (the rulebook states
it once; skills bind through it per the "nothing is said twice" convention).

## Acceptance criteria

- [ ] `tracking-rules.md` states a search-first candidate-creation rule: before
      adding a candidate row, sweep existing candidates + `milestones/archive/`
      + `DECISIONS.md` for overlap; on a hit, absorb into or cross-reference the
      existing row rather than duplicate, and a standing rejection follows the
      existing supersede discipline. Binds any skill and conversational adds.
- [ ] The ad-hoc candidate-creation steps in `/hotfix` and `/milestone-review`
      carry a one-line pointer to the rule (a pointer, not a restatement).
- [ ] A guard test locks the rule's presence in `tracking-rules.md` (single-line
      anchor per the M23/M26 lessons).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks

- [x] T1 — Add the search-first candidate-creation rule to `tracking-rules.md`,
      at/near the Intake "Candidates may be added ... at any time" line.
- [x] T2 — Add a brief pointer at `/hotfix` step 7 and the `/milestone-review`
      follow-up-candidate step referencing the rule.
- [x] T3 — Add a prose-guard test in `skills/tests/` asserting the rule text on
      a single line; run the skills guard suite green.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: T1 — added the "Search-first candidate creation" rule to `tracking-rules.md` after the Intake paragraph; branch cut, status → in-progress.
- 2026-07-12: T2 — one-line pointers at `/hotfix` step 7 and the `/milestone-review` follow-up-candidate triage step (pointers, not restatements).
- 2026-07-12: T3 — added `test_search_first_candidates.py` (rule + both pointers); skills guard suite green (89 tests).

## Decisions

## Review
