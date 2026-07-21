# M105: Incremental AC check-off — review ticks each criterion box as its evidence lands, not in a batch at phase end

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m105-incremental-ac-checkoff

## Goal

`/milestone-review` ticks each acceptance-criterion checkbox at the moment that
criterion's fresh evidence line is recorded, never in one batch pass at phase end.

## Scope

**In:** Make review check-off incremental and mandatory. Amend
`milestone-review/SKILL.md` step 3 and the AC-fencing sub-block to require that
each AC box is ticked as its own evidence line is written (per-criterion),
mirroring how `/milestone-implement` ticks each task box at its checkpoint
commit; amend the `tracking-rules.md` AC-fencing block to state the same
discipline; add a prose-guard assertion (registered in the mutation harness)
that reddens if the incremental wording is removed.

**Out:** The evidence-before-tick invariant itself ("no evidence line, no tick";
an already-ticked box with no evidence is a gate failure) — unchanged; this
milestone changes only *timing*, not what fencing requires. `/milestone-implement`
task check-off — already per-task-at-checkpoint, needs no change. Any change to
the Coverage-completeness gate — untouched.

## Acceptance criteria

- [ ] `milestone-review/SKILL.md` step 3 (and its AC-fencing sub-block) states
      that each AC checkbox is ticked at the moment its evidence line is
      recorded — per-criterion, never batched at phase end — while preserving
      the evidence-before-tick invariant.
- [ ] The `tracking-rules.md` AC-fencing block states the incremental check-off
      discipline and ties it to `/milestone-implement`'s per-task tick.
- [ ] A guard in `test_ac_traceability.py` asserts the incremental wording on
      both surfaces and reddens when that wording is removed; the new
      anchor(s) are registered in `test_mutation_harness.py`.
- [ ] `verify` clean: `python3 -m unittest discover -s skills/tests` and the
      scripts suite green.

## Coverage

<!-- owner: plan · create/amend-via-gate -->

- AC1 → T2
- AC2 → T3
- AC3 → T1
- AC4 → T1, T2, T3

## Tasks

- [x] T1 (test-first): Add to `TestReviewFences` in
      `skills/tests/test_ac_traceability.py` an assertion pinning the
      incremental-check-off requirement in `review()`, and to
      `TestRulesDiscipline` one pinning it in `rules()`; register the new
      anchor(s) in `skills/tests/test_mutation_harness.py` (per-file, one
      exemplar block each — M60/M85). Both assertions fail against the current
      batch wording.
- [x] T2: Amend `milestone-review/SKILL.md` step 3 and its AC-fencing sub-block
      (lines ~40-55) to mandate ticking each AC box as its evidence line is
      recorded; keep "no evidence line, no tick" intact. Re-anchor any adjacent
      guard whose asserted phrase reflows (M104 lesson).
- [x] T3: Amend the `tracking-rules.md` AC-fencing block (lines ~62-71) to state
      the incremental discipline, cross-referencing implement's tick-at-checkpoint.
      Run the full skills + scripts suites from repo root, check each exit code
      (M56 lesson), confirm green.

## Work log

- 2026-07-20: created by /milestone-plan (promoted from the review-AC-checkoff-timing candidate; disposition "mandate incremental, hard rule" chosen at the plan gate).
- 2026-07-20: T1 — added incremental-check-off guards (TestReviewFences + TestRulesDiscipline in test_ac_traceability.py) + two mutation-harness registrations; both red against current batch wording (tests-first), box unticked until T2/T3 land the prose.
- 2026-07-20: T2 — amended `milestone-review/SKILL.md` step 3 + AC-fencing sub-block to mandate incremental per-criterion check-off (tick as each evidence line lands), preserving "no evidence line, no tick"; T1's review anchor caught a line-wrap on the "phase end" regex (M95/M104 class) — fixed with a `\s+` matcher rather than reworking wrap-fragile prose.
- 2026-07-20: T3 — amended the `tracking-rules.md` AC-fencing block to state the incremental discipline (mirrors implement's tick-at-checkpoint). Full skills + scripts suites green (exit 0 each); mutation harness confirms both new anchors redden when blanked. All three task boxes ticked.

## Decisions

## Review
