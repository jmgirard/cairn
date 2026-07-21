# M104: Work-log staleness signal — bookkeeping entries no longer reset the idle clock

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m104-worklog-staleness-signal · https://github.com/jmgirard/cairn/pull/102   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

The `/milestone` audit's `in-progress` staleness signal measures the recency of
genuine work, so a milestone whose only recent work-log lines are bookkeeping
(Depends-on amendments, status/mirror catch-ups, git-reconciliation lines) is
flagged as stale instead of reading as active.

## Scope

**In:** Reword the SKILL §2 Staleness bullet so the 14-day `in-progress` signal
is measured from the last work-log line recording actual work, treating
bookkeeping entries as clock-neutral; add a mutation-registered prose-guard over
the new clause.

**Out:**
- Mechanizing the signal into a script — rejected at this plan gate; staleness
  stays LLM-owned (`cairn_validate.py:6`). Recorded as the gate's rejected
  option, not a candidate row.
- The release / `planned`-milestone idleness case — already owned by the
  `release window` advisory (M88, D-050); unchanged here.
- The RB (7-day) and candidate (~6-month) staleness thresholds — untouched.

## Acceptance criteria

- [x] AC1 — The SKILL §2 Staleness bullet states the `in-progress` 14-day signal
      is measured from the last work-log line recording actual work, and names
      Depends-on amendments, status/mirror catch-ups, and git-reconciliation
      catch-up lines as clock-neutral bookkeeping. (tested: wording present in
      `milestone()`)
- [x] AC2 — A new prose-guard in `TestMilestoneAuditWiring`
      (`skills/tests/test_release_timing.py`) asserts the classification clause's
      load-bearing bytes and is registered in the mutation harness; blanking the
      clause reddens the guard, and the completeness meta-test stays green.
      (tested: mutation harness over the new registration)
- [x] AC3 — The existing `test_advisory_owns_idleness_against_the_staleness_bullet`
      guard stays green: the release advisory still solely owns the release-case
      idleness question, with no double-counting introduced between it and the
      reworded bullet. (tested: that guard)
- [x] AC4 — `skills/tests`, `scripts/tests`, and `hooks/tests` all green
      (profile `verify` slot).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3

## Tasks

- [x] T1 — Reword the Staleness bullet at `skills/milestone/SKILL.md:91`:
      bookkeeping (a Depends-on amendment, a status/mirror catch-up, a
      git-reconciliation line) is clock-neutral; the signal is measured from the
      last entry recording actual work; cite the M88 T3 lineage inline.
- [x] T2 — Add prose-guard `test_staleness_signal_discounts_bookkeeping_entries`
      to `TestMilestoneAuditWiring` asserting the clause's bytes; register the
      anchor in `skills/tests/test_mutation_harness.py`; run the mutation harness
      and confirm it reddens on blanking.
- [x] T3 — Run the three suites; confirm the existing idleness-ownership guard
      and the completeness meta-test stay green.

## Work log

- 2026-07-20: created by /milestone-plan.
- 2026-07-20: start — in-progress; branch m104-worklog-staleness-signal.
- 2026-07-20: T1 — reworded SKILL §2 Staleness bullet; bookkeeping entries clock-neutral, signal from last work entry (M88 T3, generalizes M88-D1).
- 2026-07-20: T2 — added guard test_staleness_signal_discounts_bookkeeping_entries + 2 mutation registrations; both anchors redden on blank.
- 2026-07-20: T3 — suites green (skills 556, scripts 269, hooks 72); idleness-ownership guard and completeness meta-test green; validate green. Status → review.

## Decisions

<!-- owner: implement / review · append-only; milestone-local -->

## Review

**Reviewed 2026-07-20 · PR #102 · branch m104-worklog-staleness-signal.**

Fresh evidence per criterion:

- **AC1 — PASS.** `skills/milestone/SKILL.md` §2 Staleness bullet reworded:
  clock runs from "the last work-log line that records actual progress"; a
  `Depends-on` amendment, a status-transition or mirror catch-up, and a
  git-reconciliation catch-up line are named clock-neutral. Both anchor
  phrases present (grep = 2).
- **AC2 — PASS.** Guard `test_staleness_signal_discounts_bookkeeping_entries`
  added to `TestMilestoneAuditWiring`; two mutation registrations. Manual
  mutation: clean tree passes; blanking either anchor reddens the guard.
  Completeness meta-test green within the skills suite.
- **AC3 — PASS.** `test_advisory_owns_idleness_against_the_staleness_bullet`
  green (test_release_timing 16/16 OK). The reworded general-case bullet and
  the release-advisory ownership clause (SKILL §2 lines 66–69, untouched)
  do not double-count.
- **AC4 — PASS.** Suites all green: skills 556, scripts 269, hooks 72.

Consistency gate: `cairn_validate` exit 0 (only the pre-existing
`references staleness` advisory on rulebook-classification-ledger, unrelated).
Profile `generic` → no toolchain consistency checks. No principle change →
`cairn_impact` skipped.
