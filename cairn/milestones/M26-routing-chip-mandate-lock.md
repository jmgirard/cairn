<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M26: Lock the routing-chip mandate; exempt review as the chip-less phase

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m26-routing-chip-mandate-lock

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

- [ ] `tracking-rules.md` states, on single lines, (a) a prose list of
      options is not a routing chip, and (b) `/milestone-review`'s end is the
      sole exception to the routing-chip mandate (a `/clear` nudge, no chip).
- [ ] Every non-review phase skill that ends with a routing chip names
      `AskUserQuestion` at that step (`milestone-plan`, `milestone-implement`,
      `milestone`, `cairn-init`, `cairn-release`, `design-interview`).
- [ ] `/milestone-review`'s end-of-phase step is a plain-prose `/clear` nudge
      with no routing chip, while its merge-approval gate remains an
      `AskUserQuestion` chip.
- [ ] `test_gate_wording.py` asserts the two criteria above — loops the
      non-review skills for `AskUserQuestion`, asserts review's ending is
      chip-less yet retains its merge chip, and asserts the rulebook
      clarifier — and the full `skills/tests` suite passes.
- [ ] A `DECISIONS.md` D-entry records the refinement (review exempt from the
      routing-chip mandate), referencing D-003.

## Coverage

- AC1 → T1
- AC2 → T3
- AC3 → T2
- AC4 → T4
- AC5 → T5

## Tasks

- [ ] T1 — In `skills/shared/tracking-rules.md` "Question gates and routing
      chips", add a single-line clarifier that a prose list of options is not
      a chip, and state review's end is the sole exception (chip-less `/clear`
      nudge). Keep asserted phrases on single lines (M23 lesson: prose guards
      `assertIn` fail across newlines).
- [ ] T2 — Rewrite `skills/milestone-review/SKILL.md` step 10: replace the
      routing chip with a plain-prose `/clear` encouragement. Leave the
      step-6 merge-approval `AskUserQuestion` chip untouched.
- [ ] T3 — In `milestone-plan` (step 7), `milestone-implement` (step 8),
      `cairn-init` (step 8), `cairn-release` (step 9), `design-interview`
      (Routing), name `AskUserQuestion` explicitly at the routing-chip step.
- [ ] T4 — Extend `skills/tests/test_gate_wording.py`: loop the six
      non-review skills asserting `AskUserQuestion` at their routing-chip
      step; assert review's ending is a `/clear` nudge with no end chip while
      the merge gate keeps `AskUserQuestion` (key on the ending, not the mere
      presence of the word); assert the rulebook clarifier. Run
      `python3 -m unittest discover -s skills/tests`.
- [ ] T5 — Append a `cairn/DECISIONS.md` entry refining D-003 (every phase
      ends with a chip → review exempted, chip-less `/clear` nudge).

## Work log

- 2026-07-12: created by /milestone-plan (absorbs candidates "End-of-review
  routing chip → /clear nudge" and "Lock the routing-chip mandate with a
  guard test", both 2026-07-12 Jeff feedback).

## Decisions

## Review
