# M116: Repair the three-step placement test — retention takes the deletion arm, inversion moves to guard verification, and a step-0 single-home check (RR04 rec 9)

**Status:** done (2026-07-27, PR #116 https://github.com/jmgirard/cairn/pull/116)

**Goal:** Repair the placement test the rulebook states under "What gets a test",
superseding D-056 narrowly and replacing its false yield clause with the ledger's measurements.

**Outcome:** Retention now requires **deletion** alone — RR04 §6 found the old
"deleted **or** inverted" disjunction routed every duplicate to "keep", since
inverting a copy contradicts the original. The relabel/negate/transpose
procedure is reassigned to guard verification and cross-references the
guard-must-fail rule owning it; a **step 0 — one home** check runs ahead of
both, binding intra-file on text authored or edited onward. `guard-doctrine.md`
§8 gained D-069's certified-scope bound. Registry 412 → 421.

**Decisions:** D-071 (the three edits; D-056's parts 1 and 3 stand), D-072
(narrows D-071's "reds on any edit" overclaim), D-073 (narrows D-071's "parts 1
and 3 unchanged" to part 3's asymmetry; restates D-072's five spans).

**Review:** §8 certification 2 rounds, 9 + 2 discrepancies, all resolved or
declined on scope. Fan-out: diff-bug 7, blame-history 0, prior-review 0.
Actioned F4 (87), F5 (85); F1 (68), F2 (58), F3 (78) fixed at maintainer's
direction; F6 (60), F7 (30) logged. Pruned M60/M85's template-registration
lesson (D-015); trimmed M110's to its uncovered remainder.
