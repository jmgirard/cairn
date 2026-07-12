<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M26: Lock the routing-chip mandate; exempt review as the chip-less phase

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m26-routing-chip-mandate-lock · https://github.com/jmgirard/cairn/pull/24

## Goal

Make the end-of-phase routing-chip mandate drift-proof — every phase skill
names `AskUserQuestion` at its routing-chip step, `/milestone-review` is the
sole deliberate exception (a plain-prose `/clear` nudge), all locked by a
guard test.

## Scope

**In:**
- Rulebook clarifier that a prose list of options is **not** a routing chip,
  and that `/milestone-review`'s end is the one exception to the mandate.
- Tighten the routing-chip step in the phase skills that currently say
  "routing chip" without naming the tool — `milestone-plan`,
  `milestone-implement`, `cairn-init`, `cairn-release`, `design-interview`
  (`milestone` already names `AskUserQuestion`).
- Replace `/milestone-review`'s end-of-phase routing chip (step 10) with a
  plain-prose `/clear` nudge; its merge-approval gate (step 6) stays an
  `AskUserQuestion` chip.
- Extend `skills/tests/test_gate_wording.py` to lock both directions.
- A `DECISIONS.md` entry refining D-003.

**Out:**
- Any change to the phase-header/TOC convention → M27.
- `hotfix` / `milestone-brief` routing-chip wording — neither ends on a
  standalone routing-chip step (they end on merge / RR-ingest), so they are
  outside the guarded set; revisit only if that changes.

## Acceptance criteria

- [x] `tracking-rules.md` states, on single lines, (a) a prose list of
      options is not a routing chip, and (b) `/milestone-review`'s end is the
      sole exception to the routing-chip mandate (a `/clear` nudge, no chip).
- [x] Every non-review phase skill that ends with a routing chip names
      `AskUserQuestion` at that step (`milestone-plan`, `milestone-implement`,
      `milestone`, `cairn-init`, `cairn-release`, `design-interview`).
- [x] `/milestone-review`'s end-of-phase step is a plain-prose `/clear` nudge
      with no routing chip, while its merge-approval gate remains an
      `AskUserQuestion` chip.
- [x] `test_gate_wording.py` asserts the two criteria above — loops the
      non-review skills for `AskUserQuestion`, asserts review's ending is
      chip-less yet retains its merge chip, and asserts the rulebook
      clarifier — and the full `skills/tests` suite passes.
- [x] A `DECISIONS.md` D-entry records the refinement (review exempt from the
      routing-chip mandate), referencing D-003.

## Coverage

- AC1 → T1
- AC2 → T3
- AC3 → T2
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1 — In `skills/shared/tracking-rules.md` "Question gates and routing
      chips", add a single-line clarifier that a prose list of options is not
      a chip, and state review's end is the sole exception (chip-less `/clear`
      nudge). Keep asserted phrases on single lines (M23 lesson: prose guards
      `assertIn` fail across newlines).
- [x] T2 — Rewrite `skills/milestone-review/SKILL.md` step 10: replace the
      routing chip with a plain-prose `/clear` encouragement. Leave the
      step-7 merge-approval `AskUserQuestion` chip untouched.
- [x] T3 — In `milestone-plan` (step 7), `milestone-implement` (step 8),
      `cairn-init` (steps for scaffold + migration), `cairn-release` (step 9),
      `design-interview` (Routing), name `AskUserQuestion` explicitly at the
      routing-chip step via the contiguous token `routing chip
      (AskUserQuestion)`. (`milestone` already carried it.)
- [x] T4 — Extend `skills/tests/test_gate_wording.py`: loop the six
      non-review skills asserting `AskUserQuestion` at their routing-chip
      step; assert review's ending is a `/clear` nudge with no end chip while
      the merge gate keeps `AskUserQuestion` (key on the ending, not the mere
      presence of the word); assert the rulebook clarifier. Run
      `python3 -m unittest discover -s skills/tests`.
- [x] T5 — Append a `cairn/DECISIONS.md` entry refining D-003 (every phase
      ends with a chip → review exempted, chip-less `/clear` nudge).

## Work log

- 2026-07-12: created by /milestone-plan (absorbs candidates "End-of-review
  routing chip → /clear nudge" and "Lock the routing-chip mandate with a
  guard test", both 2026-07-12 Jeff feedback).
- 2026-07-12: T1 — rulebook clarifier (prose list ≠ chip) + review-end
  exception added to tracking-rules "Question gates and routing chips".
- 2026-07-12: T2 — review SKILL step 10 now a plain-prose `/clear` nudge,
  no end chip; step-7 merge gate untouched.
- 2026-07-12: T3 — 6 non-review skills carry the contiguous token `routing
  chip (AskUserQuestion)` at their routing-chip step (cairn-init in both
  scaffold + migration endings).
- 2026-07-12: T4 — `TestRoutingChipMandate` (5 tests) added to
  test_gate_wording.py; full skills/tests suite green (68 tests).
- 2026-07-12: T5 — D-019 appended, refining D-003 (review exempt). All tasks
  done; status → review.

## Decisions

## Review

_Reviewed 2026-07-12 · PR #24 · diff `main..HEAD` (11 files)._

**Acceptance-criteria evidence** (fresh, by command):
- AC1 — `tracking-rules.md` contains "a prose list of options is not a
  routing chip" (1) and "the sole phase whose end is deliberately chip-less"
  (1), each on one line.
- AC2 — token `routing chip (askuserquestion)` (case-insensitive) present in
  all six non-review skills: plan/implement/milestone/cairn-release/
  design-interview ×1, cairn-init ×2 (scaffold + migration endings).
- AC3 — `milestone-review` step 10: "no routing chip" (1), merge-gate "this
  is the third gate" (1) intact; routing-chip token absent (0).
- AC4 — `test_gate_wording.py` 8/8 (3 merge-gate + 5 `TestRoutingChipMandate`);
  full `skills/tests` 68/68.
- AC5 — `cairn/DECISIONS.md` D-019 present, refining D-003 in two parts.

**Consistency gate:** `cairn_validate` exit 0 (10/10). Coverage complete —
AC1→T1, AC2→T3, AC3→T2, AC4→T4, AC5→T5, all tasks present. `scripts/tests`
43/43. No DESIGN IP/GP changed → `cairn_impact` skipped. R gates (devtools,
README.Rmd, pkgdown, NEWS, .Rbuildignore) waived — plugin repo, per CLAUDE.md.

**Independent review** (two-lens fan-out + Sonnet scorer):
- **F1 (score 92, fixed):** `milestone-review` step 10 said "the step-6
  merge-approval gate" but the approval gate is step 7 (step 6 is the
  checkpoint commit) — a misdirecting cross-reference I introduced in T2.
  Both lenses caught it independently. Fixed on the branch (also corrected
  the same typo in this file's T2 task + work-log lines). No guard covers
  step numbers, so it wouldn't regress-fail — corrected by hand.
- **F2 (score 65, below threshold → logged + candidate):** `milestone-brief`
  step 5 ends its RR-ingest phase with a "Routing chip" that doesn't name
  `AskUserQuestion`, so the mandate lock isn't fully complete. AC2 as written
  enumerates only the six covered skills and still passes; extending the
  guard to `milestone-brief` is genuine new scope, banked as a candidate row
  rather than expanded review-side (AC fencing). The Scope-Out rationale that
  excluded it rested on a wrong premise (its ingest phase *does* end on a
  routing chip).
- Both reviewers confirmed clean: the guard token is non-vacuous and present
  in all six skills; `TestMergeGateIsAChip` is byte-unchanged (prior hotfix
  lock intact); D-019 properly refines (not contradicts) D-003; no D-010/
  D-012/D-009 or LESSONS entry contradicted.
