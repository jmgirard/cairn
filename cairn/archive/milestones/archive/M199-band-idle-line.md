# M199: A band that names the next milestone

**Status:** done (2026-10-02, PR #206 https://github.com/jmgirard/cairn/pull/206)

**Goal:** Name the next workable milestone in the band between milestones, after the last cairn skill ends.

**Outcome:** With no `in-progress` or `review` row and no cairn skill running, the band draws one gray idle row: `next`, the bold id, the title, and `/milestone-implement <id>` at the right edge. If the title gets less than its room, the command drops out. With nothing workable, the band draws nothing. `reader.ts` computes the workable list from the ROADMAP and a listing of `cairn/milestones/archive/`. It mirrors `workable` in `cairn_next.py`, a new helper that `render()` also calls. Two fixtures, `idle-order` and `idle-deps`, and a `workable` list in every `expected.json` hold the two sides to one order. A main-loop `turn.complete` with reason `answer` now ends a cairn skill's step. The close mark gains the idle id under `dismissed-3`, and the band state moved to `band-3`. Mod tests went from 506 to 603.

**Decisions:** The plan gate chose to end a skill's step at its turn's end. With nothing workable, it chose an empty band. It chose a TypeScript mirror with shared fixtures over running `cairn_next.py`. The live look at T6 showed that a question chip keeps the step.

**Review:** The three-lens fan-out gave 17 findings. The gate fixed six of them. It added reader tests for a done row at another padding and for a non-`.md` archive file, each shown to fail on its plant. It also made `render()` call `workable()`, added the idle row to the width sweep, and fixed the doc wording and wraps. D1 is follow-up: a skill that waits on background work ends its turn and loses its label. That is the plan's own falsifier, met in mechanism. It became the candidate row "Band skill label across background waits", and README and CHANGELOG state the limit. D5 and B7 joined "Band close-state edge cases", which the operator chose to promote to a milestone. Four findings were rejected with reasons. The "Band idle line" candidate graduated.
