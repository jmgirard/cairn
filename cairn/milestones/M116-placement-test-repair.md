# M116: Repair the three-step placement test — retention takes the deletion arm, inversion moves to guard verification, and a step-0 single-home check (RR04 rec 9)

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** `m116-placement-test-repair`

## Goal

Repair the placement test the rulebook states at `tracking-rules.md:820`, superseding D-056 narrowly and replacing its false yield clause with the ledger's measurements.

## Scope

**In:** RR04 §6's three prescribed edits — a step-0 single-home check, splitting the deletion probe (retention) from the inversion probe (guard verification), and replacing D-056's yield clause with measured figures — landed as one appended D-entry plus the repaired rule in `tracking-rules.md`, with every guard, registry block and docstring the rewrite invalidates re-anchored. Folds in D-069's scope clause for `guard-doctrine.md` §8, whose ROADMAP row asks for exactly this timing: before the next guard-authoring milestone's first certification round.

**Out:** Any stock-side weight pass — cutting rulebook lines for size → stays closed under D-057; the ledger remains a record of what *could* be cut, not a work order. Editing D-056's own bytes → forbidden by IP4; supersession is the remedy. A compliance sweep applying step 0 retroactively to existing near-restatements (`:115`/`:186`, `:144-145`) → out; step 0 governs text authored or edited from here on, and a retroactive sweep would be a fresh milestone. The partial-pin assert row and the one-surface pin row → stay `candidate`; neither promotion condition is met.

## Acceptance criteria

- [ ] AC1: `cairn/DECISIONS.md` gains one appended entry whose heading names D-056 as **narrowly** superseded. Its body states that D-056's parts 1 and 3 stand; states two of RR04 §6's three prescribed edits — the step-0 single-home check, and the assignment of the deletion probe to retention with the inversion probe to guard verification — and, as the third, replaces D-056's yield clause with the measured figures from `cairn/references/rulebook-classification-ledger.md`. `git diff` shows zero changed bytes inside D-056's own entry.
- [ ] AC2: In `skills/shared/tracking-rules.md`, the retention test for rulebook text is stated as deletion changing a compliant agent's behavior, and the string `deleted or inverted` does not occur in that file.
- [ ] AC3: `skills/shared/tracking-rules.md` states a single-home check running before the retention test, scoped intra-file and governing text authored or edited from that point on: text already stated elsewhere in `tracking-rules.md` keeps one home, every other site carrying at most a cross-reference.
- [ ] AC4: `skills/shared/tracking-rules.md` states that the inversion procedure (relabel, negate, transpose, require red) is the guard-verification protocol and not the placement test.
- [ ] AC5: The only sites in `skills/shared/tracking-rules.md` naming the placement test are the test paragraph and the always-read governance table's inflow cell; both name the repaired test and the new D-id, and they share no registered literal — the inflow cell carries a pointer, not a restatement. Verified by `grep -n 'D-056\|three-step\|placement test' skills/shared/tracking-rules.md` returning only those sites.
- [ ] AC6: `skills/shared/guard-doctrine.md` §8 states that a certification's own report lies outside the scope that certification covers (D-069).
- [ ] AC7: `skills/tests/test_rule_placement.py` carries a positive assert for each of AC2–AC5 and `skills/tests/test_fresh_context_readers.py` one for AC6; every assert, `REGISTRY` block and module-docstring claim the rewrite invalidates is re-anchored or corrected — at minimum `test_rule_placement.py:44-47`, its `test_module_does_not_become_the_sole_home` absence-assert, its module docstring, `test_always_read_frame.py:76-80`, and `test_mutation_harness.py:2075` and `:2342`; every newly pinned block has its own `REGISTRY` entry; and `python3 -m unittest discover` over `skills/tests`, `scripts/tests` and `hooks/tests` each exits 0 with `TestRegisteredGuardsFailWhenBlanked` reporting no non-reddening or erroring entry.

## Coverage

- AC1 → T2
- AC2 → T3, T4
- AC3 → T3, T4
- AC4 → T3, T4
- AC5 → T4, T5
- AC6 → T6
- AC7 → T4, T5, T6, T7

## Tasks

- [x] T1: Confirm `D-071` is unclaimed across all branches before authoring (verified free at plan time 2026-07-27; nothing checks D-id uniqueness, and re-checking costs one command).
- [x] T2: Author the superseding D-entry, quoting the ledger's figures (`cairn/references/rulebook-classification-ledger.md:36-42`) rather than restating them from memory.
- [ ] T3: Rewrite the placement-test paragraph at `skills/shared/tracking-rules.md:820-826` — deletion arm for retention, step 0 above it, inversion reassigned to guard verification.
- [ ] T4: Re-anchor every guard the rewrite invalidates, working from the shipped bytes and never from the draft (M95); the paragraph is hard-wrapped, so use `\s+` matchers across wrap points (M105).
- [ ] T5: Repoint the always-read table's inflow cell at `:175` as a pointer whose literal is lexically distinct from the test paragraph's — `blank_block` errors on a locator occurring twice as loudly as on zero (`mutation_engine.py:41-49`).
- [ ] T6: Add §8's scope clause and its assert in `test_fresh_context_readers.py`.
- [ ] T7: Run all three suites plus the harness sweep; run `guard-doctrine.md` §8 certification before `status -> review`, with the new scope clause in place first.

## Work log

- 2026-07-27: created by /milestone-plan. Criteria audited twice by a fresh-context [O] reader (D-067); round 1 found {AC2, AC5, AC6} jointly unsatisfiable, round 2 found four drafting defects and the exactly-once locator constraint now carried by AC5 and T5. Stopped at two rounds: re-certifying the auditor's own report is the regress D-069 names, which AC6 fixes.

- 2026-07-27: absorbs two candidate rows — RR04 rec 9 (the D-056 supersession, parked by D-057) and D-069's §8 scope clause; both removed from ROADMAP Candidates in the same commit.

- 2026-07-27: T1 D-071 verified unclaimed across all 82 branches; T2 D-071 appended, D-056 bytes unchanged (pure append verified by git diff), skills suite 654 green.

## Decisions

## Review
