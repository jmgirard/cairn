# M18: Acceptance-criteria traceability — done 2026-07-12

**Goal:** make AC verification traceable end-to-end — a criterion→task
Coverage map at plan, evidence-before-checkbox fencing at review.

**Outcome:**
- Milestone template gains a **Coverage** section: positional criterion→task
  map (`AC1 → T1`), owner: plan.
- `/milestone-plan` authors the map; unmapped criterion = planning gap.
- `/milestone-review` fences: no criterion tick without recorded evidence
  (step 3); Coverage-completeness gate (step 4) fails a criterion mapped to
  no task, back to implement.
- `tracking-rules.md`: Coverage ownership row + "AC fencing (review
  discipline)" paragraph.
- `skills/tests/test_ac_traceability.py` (11 assertions) locks it.

**Key decisions:** positional-map Coverage format (compact, cap-friendly,
future-lintable). Review's own AC checkbox tick is a *verification mark*
(distinct from editing criterion text) — authorized in the ownership row
after the fan-out caught the omission.

**Review:** 5/5 criteria evidenced; 46/46 guard tests green. Fan-out found 1
issue (scored 90): AC fencing told review to tick a plan-owned box with no
authorizing write-mode; fixed on-branch. PR #16.
