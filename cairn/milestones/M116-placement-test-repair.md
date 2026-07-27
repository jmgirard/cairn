# M116: Repair the three-step placement test — retention takes the deletion arm, inversion moves to guard verification, and a step-0 single-home check (RR04 rec 9)

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** `m116-placement-test-repair` / https://github.com/jmgirard/cairn/pull/116

## Goal

Repair the placement test the rulebook states at `tracking-rules.md:820`, superseding D-056 narrowly and replacing its false yield clause with the ledger's measurements.

## Scope

**In:** RR04 §6's three prescribed edits — a step-0 single-home check, splitting the deletion probe (retention) from the inversion probe (guard verification), and replacing D-056's yield clause with measured figures — landed as one appended D-entry plus the repaired rule in `tracking-rules.md`, with every guard, registry block and docstring the rewrite invalidates re-anchored. Folds in D-069's scope clause for `guard-doctrine.md` §8, whose ROADMAP row asks for exactly this timing: before the next guard-authoring milestone's first certification round.

**Out:** Any stock-side weight pass — cutting rulebook lines for size → stays closed under D-057; the ledger remains a record of what *could* be cut, not a work order. Editing D-056's own bytes → forbidden by IP4; supersession is the remedy. A compliance sweep applying step 0 retroactively to existing near-restatements (`:115`/`:186`, `:144-145`) → out; step 0 governs text authored or edited from here on, and a retroactive sweep would be a fresh milestone. The partial-pin assert row and the one-surface pin row → stay `candidate`; neither promotion condition is met.

## Acceptance criteria

- [x] AC1: `cairn/DECISIONS.md` gains one appended entry whose heading names D-056 as **narrowly** superseded. Its body states that D-056's parts 1 and 3 stand; states two of RR04 §6's three prescribed edits — the step-0 single-home check, and the assignment of the deletion probe to retention with the inversion probe to guard verification — and, as the third, replaces D-056's yield clause with the measured figures from `cairn/references/rulebook-classification-ledger.md`. `git diff` shows zero changed bytes inside D-056's own entry.
- [x] AC2: In `skills/shared/tracking-rules.md`, the retention test for rulebook text is stated as deletion changing a compliant agent's behavior, and the string `deleted or inverted` does not occur in that file.
- [x] AC3: `skills/shared/tracking-rules.md` states a single-home check running before the retention test, scoped intra-file and governing text authored or edited from that point on: text already stated elsewhere in `tracking-rules.md` keeps one home, every other site carrying at most a cross-reference.
- [x] AC4: `skills/shared/tracking-rules.md` states that the inversion procedure (relabel, negate, transpose, require red) is the guard-verification protocol and not the placement test.
- [x] AC5: Exactly two sites in `skills/shared/tracking-rules.md` refer to the placement steps — the test paragraph under "What gets a test" and the always-read governance table's inflow cell — and they share no registered literal, the inflow cell carrying a pointer rather than a restatement. Verified by `grep -n 'D-056\|D-071\|three-step\|placement step' skills/shared/tracking-rules.md` returning exactly those two lines, and by `test_only_two_sites_name_the_placement_steps` pinning the count.
- [x] AC6: `skills/shared/guard-doctrine.md` §8 states that a certification's own report lies outside the scope that certification covers (D-069).
- [x] AC7: `skills/tests/test_rule_placement.py` carries a positive assert for each of AC2–AC5 and `skills/tests/test_fresh_context_readers.py` one for AC6; every assert, `REGISTRY` block and module-docstring claim the rewrite invalidates is re-anchored or corrected — at minimum `test_rule_placement.py:44-47`, its `test_module_does_not_become_the_sole_home` absence-assert, its module docstring, `test_always_read_frame.py:76-80`, and `test_mutation_harness.py:2075` and `:2342`; every newly pinned block has its own `REGISTRY` entry; and `python3 -m unittest discover` over `skills/tests`, `scripts/tests` and `hooks/tests` each exits 0 with `TestRegisteredGuardsFailWhenBlanked` reporting no non-reddening or erroring entry.

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
- [x] T3: Rewrite the placement-test paragraph at `skills/shared/tracking-rules.md:820-826` — deletion arm for retention, step 0 above it, inversion reassigned to guard verification.
- [x] T4: Re-anchor every guard the rewrite invalidates, working from the shipped bytes and never from the draft (M95); the paragraph is hard-wrapped, so use `\s+` matchers across wrap points (M105).
- [x] T5: Repoint the always-read table's inflow cell at `:175` as a pointer whose literal is lexically distinct from the test paragraph's — `blank_block` errors on a locator occurring twice as loudly as on zero (`mutation_engine.py:41-49`).
- [x] T6: Add §8's scope clause and its assert in `test_fresh_context_readers.py`.
- [x] T7: Run all three suites plus the harness sweep; run `guard-doctrine.md` §8 certification before `status -> review`, with the new scope clause in place first.

## Work log

- 2026-07-27: created by /milestone-plan. Criteria audited twice by a fresh-context [O] reader (D-067); round 1 found {AC2, AC5, AC6} jointly unsatisfiable, round 2 found four drafting defects and the exactly-once locator constraint now carried by AC5 and T5. Stopped at two rounds: re-certifying the auditor's own report is the regress D-069 names, which AC6 fixes.

- 2026-07-27: absorbs two candidate rows — RR04 rec 9 (the D-056 supersession, parked by D-057) and D-069's §8 scope clause; both removed from ROADMAP Candidates in the same commit.

- 2026-07-27: T1 D-071 verified unclaimed across all 82 branches; T2 D-071 appended, D-056 bytes unchanged (pure append verified by git diff), skills suite 654 green.

- 2026-07-27: T3-T5 placement test repaired at `tracking-rules.md:820-837` (step 0, deletion-only retention, inversion reassigned); inflow cell at `:175` repointed as a pointer naming D-071; six guards re-anchored across `test_rule_placement.py`, `test_always_read_frame.py` and the registry, +6 REGISTRY entries. Two anchor bugs caught by the suite and fixed against shipped bytes: a lowercase `relabel` where the file ships `Relabel` (M95), and a registry entry naming the wrong class. All three suites green (659/280/hooks).

- 2026-07-27: T6 guard-doctrine §8 gains D-069's scope clause plus its convergence rationale; two asserts in `test_fresh_context_readers.py`, two REGISTRY entries. Registry 412 -> 419; all three suites green and the harness sweep clean.

- 2026-07-27: §8 certification round 1 returned 9 discrepancies, all fixed. #1 shipped D-069's premise that D-070 had already superseded (rounds 3-4 -> round 4 alone); #2 D-071 overclaims the guard's coverage of D-056 -> D-072 appended (IP4 attaches at append time, D-070's route); #3/#4 AC3's intra-file scoping and its before-the-retention-test ordering were unpinned; #5 a registry comment miscounted its own block; #7 two anchors had no REGISTRY entry; #8 the module docstring claimed all asserts are positive with three assertNotIn present; #9a AC5's site count was unpinned.
- 2026-07-27: correcting the T3-T5 entry above (certification #6): the net REGISTRY delta there was +5, not +6 — of seven entries in the M116 block two were repointed pre-existing entries and five were new. Registry now 421 (main 412).
- 2026-07-27: AC5 amended at the mini gate (certification #9b) — the repair removed the literal `placement test` from the file, so the criterion's own grep recipe returned one line instead of the two it describes; recipe and count assert corrected, requirement unchanged.

- 2026-07-27: §8 certification round 2 verified all nine round-1 fixes real in the shipped bytes, re-probing #3 and #4 by mutation (both were green before the fix, red after) and re-checking all 421 REGISTRY blocks. Two new discrepancies were introduced by the fixes; #1 (a registry comment made stale by its own fix) is fixed.
- 2026-07-27: certification round 2 #2 DECLINED on scope, not softened: D-072's Consequences calls what D-070 caught an "overclaimed guard-coverage sentence" where D-070 caught a false premise sentence plus an unengaged heading cite. The clause is wrong. It is declined because its subject is a certification round, which §8's new bound puts outside the certified scope, and because D-072 is append-only under IP4 — so correcting it means D-073 correcting D-072 correcting D-071, the regress that bound exists to stop. Carried to the review gate as an open item for the maintainer, never closed by me.

## Decisions

## Review

**PR:** https://github.com/jmgirard/cairn/pull/116 · reviewed 2026-07-27 · first review pass, 0 prior returns.

**Acceptance-criteria evidence** (fresh, by command):

- AC1 — `grep -c "^### D-071"` = 1; heading carries "**narrowly** superseded". `git diff main...HEAD -- cairn/DECISIONS.md` shows 0 deletion lines, so the file is a pure append and D-056's bytes are unchanged. D-071's body carries parts-1-and-3-stand, both probe edits, and the ledger figures.
- AC2 — the repaired sentence occurs once; `grep -c "deleted or inverted"` = 0 in `tracking-rules.md`.
- AC3 — "Step 0 — one home", the intra-file clause "ask whether the rulebook already says it", and the forward-binding clause each occur once.
- AC4 — "guard-verification protocol" occurs once, carrying the relabel/negate/transpose procedure.
- AC5 — the amended recipe `grep -n 'D-056\|D-071\|three-step\|placement step'` returns exactly 2 lines (`:175`, `:829`); `test_only_two_sites_name_the_placement_steps` pins the count.
- AC6 — `guard-doctrine.md` §8 carries the scope bound and its convergence rationale.
- AC7 — suites `skills` 663 / `scripts` 280 / `hooks` 91, all OK; `TestRegisteredGuardsFailWhenBlanked` passes over 421 REGISTRY entries with no non-reddening or erroring entry.

**Consistency gate:** `cairn_validate` exit 0, 16 checks PASS and 7 advisories OK. `generic` profile's `consistency-gate` slot names no toolchain checks. No `DESIGN.md` principle changed, so `cairn_impact` is not run — IP4 is worked under, not modified.

**§8 description-layer certification** (D-067; the milestone authored/edited prose-guards): round 1 returned 9 discrepancies, all fixed; round 2 verified all nine in the shipped bytes and re-probed two by mutation, and found 2 new discrepancies introduced by the fixes — 1 fixed, 1 declined on scope (recorded in the work log, carried to this gate).

**Fresh-context review fan-out** (three distinct evidence bases, then an independent scorer):

- **[O] diff-bug** — 7 findings.
- **[S] blame-history** — 0 findings. Verified D-056 parts 1/3 survive in prose and mechanically; the always-read cell change is what D-071 prescribes; §8's addition transcribes D-069's own Decision; M98 F4/82's docstring rationale preserved.
- **[S] prior-review** — 0 findings. Walked 13 archived `## Review` sections; cleared all seven recurring finding classes. GitHub comment probe returned empty, so the thread walk was correctly skipped.

**Scored and triaged** (scorer did not generate the findings):

- **F4 (87) — actioned.** D-072's heading/Context name five pinned spans; its Decision enumerated four, dropping the heading regex, while claiming the guard reds "not on an edit elsewhere in the entry" — false, `test_entry_exists_and_annotates_d045` pins the heading. Fixed by appended **D-073**.
- **F5 (85) — actioned.** `test_rule_placement.py:99-100` claimed "the assertIn anchors below sit on one physical line each"; every new assertIn spans two. Comment rewritten to the true reason (regex tolerates reflow because AC3 pins by meaning; assertIns carry their wrap so a reflow *should* red).
- **F1 (68) — logged, then fixed at the maintainer's direction.** D-071's "parts 1 and 3 stand unchanged" is false of part 3's framing sentence, which D-071(2) reverses. Fixed by **D-073**.
- **F3 (78) — logged, then fixed at the maintainer's direction.** The "where no guard exists" tail was stranded by the reassignment and its guard comment argued from the retired rationale. The paragraph now cross-references the guard-must-fail rule; `test_rulebook_covers_the_unguarded_case` repointed onto `still needs its own entry or the by-hand check` with its REGISTRY block updated.
- **F2 (58) — logged, then fixed at the maintainer's direction.** The new paragraph restated the guard-verification proposition already owned two paragraphs below, violating the step 0 this milestone introduces. Now a pointer. (Scorer partially refuted the finding: the two by-hand fallbacks are different checks, so only the proposition was a true duplicate.)
- **F6 (60) — logged, not actioned.** Two order/count asserts carry no REGISTRY entry. The repo's existing convention leaves pure order/count assertions unregistered (`test_both_statements_precede_the_guard_obligation`), and registering the order assert would be a false green: blanking makes `str.index` raise, which `guard_fails_when_blanked` scores as reddening for the wrong reason.
- **F7 (30) — logged, declination upheld.** D-072's "second consecutive milestone … overclaimed guard-coverage sentence" is inaccurate about what D-070 caught. Declined on scope — its subject is a certification round, which §8's new bound excludes; the scorer independently judged the scope reading better supported than the finding's rebuttal.

**Re-verification after all fixes:** suites 663 / 280 / 91 OK; `cairn_validate` exit 0; AC2 forbidden-string count 0; AC4 and AC5 recipes unchanged; registry 421.
