# M147: The records shrink to their jobs

- **Status:** planned
- **Priority:** normal
- **Depends on:** M146
- **Driving RR:** —
- **Principles touched:** GP1, IP4
- **Branch/PR:** —

## Goal

cairn's own always-read records shrink to their jobs — one lesson (or one
named family) per LESSONS line, idea/parking/promotion per candidate row —
against a committed per-entry disposition ledger (RR13 rec 8). Internal
tier: no external consumer of the repo relies on cairn's own LESSONS and
ROADMAP rows.

## Scope

**In:**
- A per-entry disposition ledger in this file over every LESSONS entry and
  every ROADMAP candidate row at the pre-milestone default-branch commit;
  the rewrite ships against it.
- The five machinery rows whose drop the 2026-08-16 plan gate approved —
  write-time stamp check, budget redistribution, re-pin Substantive bullet,
  partial-pin asserts, one-surface pin — dropped via the ledger with a
  one-line reason each; the archive summary points at the ledger.
- The retired-artifact name cleanup M146 deferred (guard-doctrine,
  DENSITY_FILES, cairn_budget mentions inside rows).

**Out:** no new caps, formats, or checking machinery of any kind — the
reduction just removed that class (D-108); ROADMAP milestone rows and
statuses untouched beyond normal hygiene; RR13 rec 9's post-reduction
re-measurement stays with the existing re-measurement candidate row.

## Acceptance criteria

- [ ] AC1: Every lesson entry of `cairn/LESSONS.md` at the pre-milestone
      default-branch commit is dispositioned in the ledger — kept, trimmed
      to its uncovered remainder, or retired under a named D-051/D-055
      ground or the RR13-reduction ground — and the shipped file contains
      exactly the kept and trimmed entries, each a single
      `- YYYY-MM-DD (M<NN>):` line stating one lesson or one consolidated
      family with its members named.
- [ ] AC2: Every candidate row of `cairn/ROADMAP.md` at the pre-milestone
      default-branch commit is dispositioned in the same ledger — rewritten,
      merged, or dropped — and each surviving row states the idea, why it is
      parked, its promotion condition, and its added-date/source, plus any
      search-first cross-reference, and nothing else; no surviving row names
      a retired artifact, verified by re-running M146's AC2/AC4 greps
      without their ROADMAP/LESSONS exclusions.
- [ ] AC3: `cairn_validate` exits 0 (item caps hold after the rewrite).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks

- [ ] T1: Ledger and rewrite `cairn/LESSONS.md` (32 lesson entries at
      today's tree; grounds named per entry).
- [ ] T2: Ledger and rewrite the ROADMAP candidate rows; execute the five
      gate-approved drops; re-run M146's greps over ROADMAP/LESSONS.
- [ ] T3: Run `cairn_validate`; confirm exit 0; commit ledger + rewrites
      together.

## Work log

- 2026-08-16: created by /milestone-plan (RR13 step 2, gate round 1).
- 2026-08-16: criteria audit ran ([O] fresh reader): AC1 gained the consolidated-family form and the RR13-reduction retirement ground (a strict one-lesson-per-line split would breach the 50-line cap); AC2 gained the search-first cross-reference allowance; the completeness-claiming drop criterion was demoted to ledger dispositions with the reasons in this file, not the capped archive summary; AC3 tightened to exit 0.
- 2026-08-16: plan gate approved the five machinery-row drops via the ledger rather than a completeness-claiming criterion; falsified by a dropped row's subject resurfacing as needed work.
- 2026-08-16: M146 review note — the In-scope row-drop list intersects D-115's Consequences: the write-time-stamp-check row is D-115's named remedy path, so dropping it requires a superseding clause in the same milestone or sparing (and correcting) the row; that row's premise and blocker analysis also name machinery M146 retired, and LESSONS.md line 18 cites the deleted test_cairn_budget — both are this milestone's cleanup ground (M146 review findings O2/O5/O8).

## Decisions

## Review
