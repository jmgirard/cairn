# M98: Lesson graduation to doctrine — a matured lesson family leaves LESSONS.md whole

**Status:** done · 2026-07-20 · PR #95

**Goal.** Give `LESSONS.md` a third outflow — graduation to doctrine — by
distilling its matured guard-craft family into a conditionally-read module.

**Outcome.** `skills/shared/guard-doctrine.md` (7 sections) holds the
guard/fixture/matcher authoring craft, wired from the rulebook's "What gets a
test" and read only at guard-authoring time. LESSONS.md 49 → 35 lines,
21,085 → 8,605 chars, 32 → 17 items; `record density` WARN → OK.

**Graduated:** 15 deleted whole; 3 trimmed to uncovered remainders (M72
rebase sync, M81/M91 synthesis aging, M60/M85 template registrability).

**Decisions.** D-055 — maturation is a third retirement criterion, distinct
from D-051's rejected "separate graduated-lessons file" because the source
line dies in the same pass. M98-D1 — boundary re-derived independently,
differing from RR03 on 6 of 18; the records-hygiene family (8 items) is real
but fires at a different gate, deferred to a candidate.

**Review.** 3 lenses + scorer; 7 findings, all fixed, none deferred: stale
figures in an append-only record (F1/92, two lenses, re-derived twice), RR03
rec-1 doctrine from the wrong home (F4/82), DESIGN inventory (F3/80), and
four sub-80 actioned on substance. 809 tests green.
