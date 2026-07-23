# M110: Records-hygiene doctrine module

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP4
- **Branch/PR:** m110-records-hygiene-module

## Goal

Graduate the gate-time records-hygiene lesson family from `LESSONS.md` into a
second conditionally-read doctrine module — the second application of
maturation (D-055).

## Scope

**In:** Author `skills/shared/records-hygiene.md`, distilling the eight-item
family that fires at a hygiene or plan gate — M35 (candidate rows graduate at
completion), M51 + M87 (compression craft: only a whole wrapped line lowers a
count; compress what your phase owns), M69 (amend the AC when you improve a
delivered output), M73 (a sub-threshold score gates the actioned list, not
judgment), M77 (the collision sweep greps the archive for decisions), and
M78 ×2 (run a new rule over your own artifacts; a rule's home is decided by
"would a repo with no numeric work need this?"). The module declares its
read-trigger and that it is a module of `tracking-rules.md` (D-031 shape).
Graduate the family from `LESSONS.md` — delete whole where covered, trim to the
uncovered remainder where `guard-doctrine.md` already partly covers, no line or
breadcrumb left. Add a rulebook pointer beside the retirement rule. Ship a
mutation-registered guard and D-061 (annotating D-055).

**Out:** Ownership-retiring M69/M77 into `/milestone-implement` step 6 and
`/milestone-plan`'s collision sweep — rejected at the plan gate; they graduate
instead, so no skill-prose edits here. Changing the maturation *mechanism* →
D-055 owns it. Re-sweeping `LESSONS.md` for further families → out; scoped to
these eight (the guard-doctrine family and unrelated lessons stay).

## Acceptance criteria

- [ ] `skills/shared/records-hygiene.md` exists, declares its read-trigger (a
      milestone hygiene or plan gate) and "a module of `tracking-rules.md`"
      (D-031), and covers the graduated family in anchored sections.
- [ ] `tracking-rules.md` points at the module on one pinnable physical line
      beside the LESSONS retirement rule, stating when to read it and that it
      is read conditionally (a session not at such a gate never pays for it).
- [ ] Every graduated lesson is absent from `LESSONS.md` — no line, no
      breadcrumb (`records-hygiene.md` unmentioned there); each partial is
      trimmed to its uncovered remainder and marked trimmed (D-051).
- [ ] `LESSONS.md` is back under the `<50` item cap with headroom, the count
      stated; a kept lesson remains (positive control).
- [ ] D-061 exists, annotates D-055, and records the module identity plus the
      M69/M77 graduate-not-ownership disposition.
- [ ] A mutation-registered guard (`test_records_hygiene_graduation.py`) locks
      the AC1–AC5 surfaces; every asserted block is in the harness registry,
      the completeness meta-test passes, and `verify` (all three suites) is
      clean.

## Coverage

- AC1 → T2
- AC2 → T4
- AC3 → T1, T3
- AC4 → T3
- AC5 → T6
- AC6 → T5

## Tasks

- [ ] T1 Map each of the eight family lines to a disposition — graduate whole,
      or trim to the remainder `guard-doctrine.md` already covers (M78's
      own-artifacts overlaps its §7; M87 cites M51's wrapped-line rule) —
      against the D-055 bar; confirm M69/M77 graduate.
- [ ] T2 Author `skills/shared/records-hygiene.md`: header stating the
      read-trigger + "a module of `tracking-rules.md`", then thematic sections
      per T1's map (mirror `guard-doctrine.md`). Draft against `cairn_budget`.
- [ ] T3 Graduate the family from `LESSONS.md` per T1: delete whole / trim
      partials, leave no breadcrumb; `wc -l` confirms back under `<50` with
      headroom.
- [ ] T4 Add the rulebook pointer beside the retirement rule — one pinnable
      physical line mapping the module to its coverage, plus when-to-read and
      the conditional-read note; grep every adjacent guard's anchor is still
      contiguous on one line (M104).
- [ ] T5 Write `test_records_hygiene_graduation.py` from the module's actual
      bytes (M95): assert AC1–AC5 surfaces (module + read-trigger + section
      anchors, pinnable pointer, family-left with positive control + trimmed
      remainders, D-061 annotates-D-055); register each block in
      `test_mutation_harness.py`; run the harness + completeness meta-test;
      all three suites green.
- [ ] T6 Author D-061 (annotate D-055): second maturation, module identity,
      M69/M77 graduate-not-ownership.

## Work log

- 2026-07-23: created by /milestone-plan.

## Decisions

## Review
