# M105: Incremental AC check-off — review ticks each criterion box as its evidence lands, not in a batch at phase end

**Status:** done (2026-07-20, PR #103 https://github.com/jmgirard/cairn/pull/103)

**Goal:** `/milestone-review` ticks each acceptance-criterion checkbox at the moment that criterion's fresh evidence line is recorded, never in one batch pass at phase end.

**Outcome:** The review skill's step 3 + AC-fencing sub-block and `tracking-rules.md`'s AC-fencing block now mandate incremental per-criterion check-off — tick each box as its evidence line lands, mirroring `/milestone-implement`'s tick-at-checkpoint — never one batch pass at phase end. The evidence-before-tick invariant ("no evidence line, no tick") is unchanged; this closes the optimistic-batch gap structurally rather than by discipline. Pinned by two guard asserts in `test_ac_traceability.py` (TestReviewFences + TestRulesDiscipline), each mutation-registered; wrap-safe `\s+` matchers span the skill's line-wrap. No script change (generic profile). Promoted from the review-AC-checkoff-timing candidate (M104-observed).

**Decisions:** none — batch-vs-incremental was an unspecified gap in M18's AC fencing, now filled, not a reversal; no D-entry.

**Review:** 4/4 ACs fresh, all PASS; `cairn_validate` exit 0 (one pre-existing references-staleness WARN, untouched by the diff). 3-lens fan-out (diff-bug [O], blame [S], prior-review [S]) + scorer — no findings on any lens, actioned list empty. First review to follow the incremental rule it ships.
