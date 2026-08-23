# M26: Lock the routing-chip mandate; exempt review as the chip-less phase

**Status:** done · **PR:** #24 (merged 2026-07-12) · **Priority:** normal

## Goal
Make the end-of-phase routing-chip mandate drift-proof: every phase skill
names `AskUserQuestion` at its routing-chip step, `/milestone-review` the sole
chip-less exception (a `/clear` nudge), locked by a guard test.

## Outcome
- `tracking-rules.md`: mandate tightened (a prose list is not a chip); review
  stated as the sole chip-less exception.
- 6 non-review skills carry the token `routing chip (AskUserQuestion)` at
  their routing-chip step (cairn-init in both endings); `milestone-review`
  step 10 → `/clear` nudge, no end chip, step-7 merge chip untouched.
- `test_gate_wording.py` gains `TestRoutingChipMandate` (5 tests); suite 68/68.
- **D-019** refines D-003: review exempt from the routing-chip mandate.

## Review
All 5 ACs verified by command. Two-lens fan-out + scorer: F1 (92) fixed —
review mislabeled the merge gate step-6 → step-7; F2 (65, below threshold) —
`milestone-brief`'s ingest phase ends on an unmarked routing chip → banked as
a candidate. `TestMergeGateIsAChip` byte-unchanged; no decision contradicted.
