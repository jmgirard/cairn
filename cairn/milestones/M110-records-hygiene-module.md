# M110: Records-hygiene doctrine module

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP4
- **Branch/PR:** m110-records-hygiene-module · https://github.com/jmgirard/cairn/pull/108

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

- [x] `skills/shared/records-hygiene.md` exists, declares its read-trigger (a
      milestone hygiene or plan gate) and "a module of `tracking-rules.md`"
      (D-031), and covers the graduated family in anchored sections.
- [x] `tracking-rules.md` points at the module on one pinnable physical line
      beside the LESSONS retirement rule, stating when to read it and that it
      is read conditionally (a session not at such a gate never pays for it).
- [x] Every graduated lesson is absent from `LESSONS.md` — no line, no
      breadcrumb (`records-hygiene.md` unmentioned there); each partial is
      trimmed to its uncovered remainder and marked trimmed (D-051).
- [x] `LESSONS.md` is back under the `<50` item cap with headroom, the count
      stated; a kept lesson remains (positive control).
- [x] D-061 exists, annotates D-055, and records the module identity plus the
      M69/M77 graduate-not-ownership disposition.
- [x] A mutation-registered guard (`test_records_hygiene_graduation.py`) locks
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

- [x] T1 Map each of the eight family lines to a disposition — graduate whole,
      or trim to the remainder `guard-doctrine.md` already covers (M78's
      own-artifacts overlaps its §7; M87 cites M51's wrapped-line rule) —
      against the D-055 bar; confirm M69/M77 graduate.
- [x] T2 Author `skills/shared/records-hygiene.md`: header stating the
      read-trigger + "a module of `tracking-rules.md`", then thematic sections
      per T1's map (mirror `guard-doctrine.md`). Draft against `cairn_budget`.
- [x] T3 Graduate the family from `LESSONS.md` per T1: delete whole / trim
      partials, leave no breadcrumb; `wc -l` confirms back under `<50` with
      headroom.
- [x] T4 Add the rulebook pointer beside the retirement rule — one pinnable
      physical line mapping the module to its coverage, plus when-to-read and
      the conditional-read note; grep every adjacent guard's anchor is still
      contiguous on one line (M104).
- [x] T5 Write `test_records_hygiene_graduation.py` from the module's actual
      bytes (M95): assert AC1–AC5 surfaces (module + read-trigger + section
      anchors, pinnable pointer, family-left with positive control + trimmed
      remainders, D-061 annotates-D-055); register each block in
      `test_mutation_harness.py`; run the harness + completeness meta-test;
      all three suites green.
- [x] T6 Author D-061 (annotate D-055): second maturation, module identity,
      M69/M77 graduate-not-ownership.

## Work log

- 2026-07-23: created by /milestone-plan.
- 2026-07-23: T1 disposition map — all 8 family lines graduate whole, 0 trims (each single-subject; M78-own-artifacts is the general rule, guard-doctrine §7 the grep instance, no LESSONS dup); M69/M77 graduate confirmed.
- 2026-07-23: T2 authored skills/shared/records-hygiene.md (97 lines, 6 sections); prose-guard order — module before its byte-anchored guard (M95), as M98 did.
- 2026-07-23: T3 graduated 8 lessons whole from LESSONS.md via targeted Edits (M61); 49→41 lines, headroom 9; no breadcrumb, all distinctive phrases absent.
- 2026-07-23: T4 added rulebook pointer beside the retirement rule (tracking-rules.md); coverage mapping on one pinnable line; adjacent guard anchor still contiguous (M104 check clean).
- 2026-07-23: T6 before T5 (minor reorder — the guard asserts D-061, so D-061 authored first); D-061 appended, shown verbatim before commit.
- 2026-07-23: T5 wrote test_records_hygiene_graduation.py (byte-anchored, M95; \s+ for wrapped anchors, M105); 17 blocks registered in the mutation harness. All three suites green (skills 598, scripts, hooks 72); cairn_validate exit 0.

## Decisions

## Review

**Evidence (fresh, by command; 2026-07-23):**
- AC1 — `records-hygiene.md` present (97 lines); read-trigger line and "a
  module of `tracking-rules.md`" each grep=1; six anchored sections asserted
  green by `test_records_hygiene_graduation.TestModuleExists` (22 tests OK).
- AC2 — pointer + when-to-read each grep=1 in `tracking-rules.md`;
  coverage mapping pinned to one physical line by `TestRulebookPointer`.
- AC3 — no breadcrumb (`records-hygiene` grep=0 in LESSONS.md); all six
  distinctive graduated phrases grep=0; positive control present.
  Note: T1 found all 8 graduate **whole** — 0 partials — so the "each partial
  trimmed" clause is vacuously satisfied (no partial existed to trim).
- AC4 — `LESSONS.md` 41 lines (<50, headroom 9); `weight caps` PASS.
- AC5 — D-061 heading grep=1; annotates-D-055 and graduate-not-ownership
  asserted green by `TestDecisionEntry`.
- AC6 — guard 22 tests OK; mutation harness 9 tests OK (canonical `discover`);
  `verify` all three suites green (skills 598 / scripts exit 0 / hooks 72);
  17 blocks registered, `TestRegistryCompleteness` passes. (A direct
  `-m unittest skills.tests.test_mutation_harness` errors on
  `import mutation_engine` — an invocation-path artifact, green under
  `discover`, the canonical runner.)

**Consistency gate:** `cairn_validate` exit 0 — 16 checks PASS, 1 pre-existing
advisory (`references staleness` on the rulebook-classification ledger,
untouched here). `coverage complete` PASS. Generic profile `consistency-gate`
names no toolchain checks (no-op). No principle changed (GP1/GP4 worked under,
not modified) → `cairn_impact` skipped.
