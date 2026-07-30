# M122: A differential guard holding the hook and the cap counters to one heading contract

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** `m122-heading-normalization-differential-guard`

## Goal

Pin the session-context hook and the cap counters to one heading-classification
contract with a table-driven differential guard, so a normalization step dropped
on either side reds instead of silently unbounding a milestone's history sections.

## Scope

**In:** a differential test in `hooks/tests/test_hooks.py` driving both
classifiers over one shared table — the counters through a real file
(`cairn_scripts.milestone_body_line_count`), the hook through its real injection
path (`session_context.milestone_part`) — with an expected-verdict column, a
both-directions non-vacuity assert, and mutation evidence scoped to the new
class. Graduating the falsified candidate row out of `cairn/ROADMAP.md` with the
true measurement recorded here.

**Out:** changing either layer's behaviour — both classify correctly today
(measured 2026-07-30), so this milestone adds a guard and no code change;
a shared constant or module across the two packages — a hook may import only
`cairn_common` (D-063), which is why a guard is the instrument and M119's
`TestExemptSetMirror` the precedent; deriving the renderings from a producer
instead of listing them (`guard-doctrine.md` §3) — milestone headings are
hand-authored and have no producer to sweep, the negative M117 already recorded;
trimming `cairn/LESSONS.md:42` to its uncovered remainder → this milestone's
post-merge hygiene pass, decided at the plan gate 2026-07-30.

## Acceptance criteria

- [ ] AC1: A guard in `hooks/tests/test_hooks.py` asserts, for every row of one
      shared table, that three verdicts agree: the counters' (from writing a real
      milestone file and calling `cairn_scripts.milestone_body_line_count`), the
      hook's (from `session_context.milestone_part`, reading whether an elision
      marker was emitted), and the row's own expected verdict, which pins ground
      truth so a drift hitting both layers identically still reds. Neither
      measured verdict restates the other's expression, and every fixture section
      carries more than `MIN_TAIL_BLOCKS` entries (`session_context.py:59`, = 3),
      below which no budget elides and the guard would red on correct code.
- [ ] AC2: The table covers both axes. Format: `## Work log`, `## Work Log`,
      `## WORK LOG`, `##  Work log` (two spaces), `## Work log ` (trailing space).
      Site: at least one `## Review` and one `## Decisions` rendering, because the
      counters normalize at two sites — `cairn_scripts.py:376` (boundary) and
      `:412` (subtraction) — and a work-log-only table never reaches the first.
      Controls: `## Reviewers`, `## Decisions notes`, `## Scope`.
- [ ] AC3: Each control pairs its no-marker assert with a positive signal that the
      section was injected whole (its own content present in the returned text),
      so a `milestone_part` returning nothing cannot satisfy it.
- [ ] AC4: A non-vacuity assert over the OBSERVED verdicts fails when the table
      stops exercising both outcomes, proven both ways: reduced to exempt-only
      rows the hooks suite reds, reduced to controls-only it reds.
- [ ] AC5: Guard-must-fail evidence in the Review section, scoped to the new test
      class — 7 of 98 hooks tests already red on the `.lower()` mutation
      pre-milestone (baseline measured 2026-07-30), so a whole-suite verdict
      proves nothing about this guard: `.strip()` removed from
      `session_context.heading_name` reds the new class; `.lower()` removed reds
      it; both restored, it passes.
- [ ] AC6: The candidate row "The hook's heading normalization is unguarded
      against case drift" is gone from `cairn/ROADMAP.md`, and this file records
      what it got wrong: `.lower()` removal reds 7 of 98 hooks tests (the row
      claimed all 98 green), `hooks/` byte-identical to `016a210` so the tree had
      not moved, and `.strip()` the one axis actually uncovered.
- [ ] AC7: The `verify` slot is clean — `skills/tests`, `scripts/tests` (OK with
      1 skip) and `hooks/tests` all green, run from the repo root.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T1, T2
- AC5 → T2
- AC6 → T4
- AC7 → T2

## Tasks

- [x] T1: Write the guard beside `TestExemptSetMirror`
      (`hooks/tests/test_hooks.py:466-540`, which already puts `scripts/` on
      `sys.path` and imports both modules): the shared table with its expected
      column, the counters driver over a temp file, the hook driver through
      `milestone_part`, controls carrying positive signals, and the
      observed-verdict non-vacuity assert.
- [x] T2: Run the guard-must-fail protocol — `.strip()` dropped, `.lower()`
      dropped, the table reduced each way — requiring red from the new class each
      time; restore, confirm the three suites green, record each result in the
      Review section.
- [x] T3: Confirm the file needs no mutation-harness registration (a behavioural
      guard over code, not a prose-guard asserting doc substrings) against
      `skills/tests/test_mutation_harness.py`'s completeness meta-test; register
      it if it does.
- [x] T4: Remove the candidate row from `cairn/ROADMAP.md` and record the
      correction here.

## Work log

- 2026-07-30: created by /milestone-plan.
- 2026-07-30: investigation falsified the candidate row's premise — `.lower()` removed from `heading_name` reds 7 of 98 hooks tests, not zero, and `hooks/` is byte-identical to `016a210`, so the tree had not moved since the row was written 2026-07-27. A five-mutation sweep found `.strip()` on the hook side the only uncovered axis (hook `.strip()` green; hook `.lower()`, hook `~~~` fence, counters subtraction `.lower()`, counters boundary `.lower()` all red).
- 2026-07-30: criteria audit ([O] fresh-context reader) returned 14 findings, reproduced every measurement above, and built AC1's mechanism to confirm it is achievable. Twelve had one clear right answer and are fixed in the criteria above — `MIN_TAIL_BLOCKS` reachability, the non-discriminating `.lower()` arm, the missing site axis, the missing expected-verdict column, vacuous absence controls, and seven wording or duplication repairs. Two went to the gate: row disposal and the LESSONS trim.
- 2026-07-30: plan gate chose a shared-table differential guard over pinning only the two uncovered spellings in the existing hook tests, because a spelling list re-opens the gap the moment either side gains a normalization step; falsified by a measured divergence the table's renderings cannot distinguish.
- 2026-07-30: plan gate chose removing the candidate row over keeping a narrowed third-caller row, because this milestone closes its only live residue; falsified by a third caller appearing that needs the same normalization.
- 2026-07-30: plan gate decided `cairn/LESSONS.md:42` is trimmed to its uncovered remainder — that matching two layers' rules by hand stays a review item — at this milestone's post-merge hygiene, the covered instance dropped.
- 2026-07-30: implement started on `m122-heading-normalization-differential-guard`; no implementation choice was left open by the plan, so no question gate.
- 2026-07-30: T1 — `TestHeadingNormalizationContract` added to `hooks/tests/test_hooks.py` beside `TestExemptSetMirror`: a 12-row table (5 work-log renderings, 4 review/decisions renderings for the site axis, 3 controls), each row measured three ways — counters via `milestone_body_line_count` over a real file, hook via `milestone_part` at budget 0, and the row's expected verdict — with positive signals on both arms and an observed-verdict non-vacuity assert. Hooks suite 98 -> 101 tests.
- 2026-07-30: T2 — guard-must-fail protocol run scoped to the new class, all four required reds: `.strip()` dropped from `heading_name` RED (3 failures, the axis that was green pre-milestone), `.lower()` dropped RED (3), table reduced to exempt-only rows RED (1), table reduced to controls-only RED (2). Restored and re-run: the class is green and all three suites pass (skills 700, scripts 332, hooks 101).
- 2026-07-30: AC7's parenthetical did not reproduce — `scripts/tests` reported plain `OK` today, not `OK (skipped=1)`; the skip is machine-conditional (M109). The criterion's substance, all three suites green, holds and the AC text is left as written.
- 2026-07-30: T3 — no mutation-harness registration owed: `prose_guard_modules` (`skills/tests/test_mutation_harness.py:3227-3230`) globs `skills/tests/test_*.py` only, so a guard in `hooks/tests/` is outside the completeness meta-test's scope, and this is a behavioural guard over code rather than a prose-guard asserting doc substrings.
- 2026-07-30: T4 — the candidate row was already removed in the plan commit `1966e1f`, earlier than the task placed it; the correction it owed is recorded in AC6 and in this log rather than re-done here.

## Decisions

## Review
