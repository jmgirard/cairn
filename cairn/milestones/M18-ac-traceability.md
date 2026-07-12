<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M18: Acceptance-criteria traceability

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M17   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m18-ac-traceability · [PR #16](https://github.com/jmgirard/cairn/pull/16)   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make acceptance-criteria verification traceable end-to-end: a criterion→task
coverage map authored at plan, and evidence-before-checkbox fencing enforced at
review.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- Add a **Coverage** section (each acceptance criterion → the task(s) that
  satisfy it) to the milestone template, authored by `/milestone-plan`.
- `/milestone-plan` populates the map when it writes criteria and tasks.
- `/milestone-review` enforces **AC fencing**: a criterion checkbox is never
  ticked without recorded evidence in the Review section, and every criterion
  maps to ≥1 task via the Coverage section.
- `tracking-rules.md` updated: section-ownership table gains the Coverage row;
  the review-discipline text states the fencing rule.
- Guard test locking the template section and the plan/review skill text.

**Out:**
- Reviewer fan-out / confidence scorer → M17.
- Mechanical coverage lint in `cairn_validate.py` (structural "every criterion
  referenced in Coverage" check) → candidate row; M18 starts with skill-text
  enforcement, a script can follow once the shape is proven.

**Depends on M17:** both milestones edit `milestone-review/SKILL.md` and
`tracking-rules.md`; M18 builds on M17's versions to avoid a merge conflict
(the user chose M17 first).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] The milestone template (`skills/shared/templates/milestone.md`) has a
      **Coverage** section mapping criterion → satisfying task(s), with an
      owner/write-mode ownership comment (owner: plan).
- [x] `/milestone-plan` SKILL.md instructs authoring the Coverage map when it
      writes the acceptance criteria and tasks.
- [x] `/milestone-review` SKILL.md enforces AC fencing: no criterion checkbox
      ticked without recorded evidence, and every criterion maps to ≥1 task via
      Coverage (a criterion with no task is a gate failure).
- [x] `tracking-rules.md` section-ownership table lists the Coverage section
      (owner: plan) and the review-discipline text states the fencing rule.
- [x] `skills/tests/test_ac_traceability.py` asserts the template section
      exists and the plan/review skills carry the coverage + fencing text.
      Test passes.

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] Add the Coverage section to `skills/shared/templates/milestone.md`
      (between Acceptance criteria and Tasks) with the ownership comment.
      ([template:25-31](../../skills/shared/templates/milestone.md))
- [x] Update `/milestone-plan` step 4 to author the criterion→task Coverage
      map. ([SKILL.md](../../skills/milestone-plan/SKILL.md))
- [x] Update `/milestone-review` steps 3–4 to enforce AC fencing + the
      coverage check. ([SKILL.md:31-42](../../skills/milestone-review/SKILL.md))
- [x] Update `tracking-rules.md`: add the Coverage row to the section-ownership
      table and state the fencing rule in the review discipline.
      ([tracking-rules.md:47-58](../../skills/shared/tracking-rules.md))
- [x] Write `skills/tests/test_ac_traceability.py`; run it green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (split from the "Review pipeline
  upgrades" candidate; sibling M17 covers reviewer fan-out).
- 2026-07-11: started implement; branch m18-ac-traceability. Gate chose
  positional-map Coverage format (AC1 → T1) — compact, cap-friendly,
  mechanically lint-able for the deferred cairn_validate.py check.
- 2026-07-11: T1 — added Coverage section to milestone template with
  positional-numbering + AC-fencing ownership comment.
- 2026-07-11: T2 — /milestone-plan step 4 now authors the positional
  Coverage map; unmapped criterion is a planning gap.
- 2026-07-11: T3 — /milestone-review step 3 fences evidence-before-checkbox;
  step 4 gate adds a Coverage-completeness check (unmapped criterion = gate
  failure, back to implement).
- 2026-07-11: T4 — tracking-rules gains the Coverage ownership row and an
  "AC fencing (review discipline)" paragraph.
- 2026-07-11: T5 — added test_ac_traceability.py (11 assertions). Full skills
  suite 46/46 green; cairn_validate.py exit 0. Status → review.
- 2026-07-11: review — merged main (M19 plan + candidates; ROADMAP conflict
  resolved to M18=review), PR #16, 5/5 criteria evidenced, consistency gate
  clean. Fan-out: 1 finding (scored 90) — AC-fencing told review to tick a
  plan-owned criterion box with no authorizing write-mode. Fixed on branch:
  authorized review's tick as a verification mark (SKILL step 3 + tracking-
  rules AC row + fencing paragraph); M14 allow-list guard caught a dropped
  phrase mid-fix, restored. 46/46 green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

**Reviewed 2026-07-11 · branch m18-ac-traceability · [PR #16](https://github.com/jmgirard/cairn/pull/16)**

### Acceptance-criteria evidence (fresh, by command)

- **AC1** ✓ — `skills/shared/templates/milestone.md` has `## Coverage`
  between Acceptance criteria and Tasks; ownership comment `owner: plan ·
  create/amend-via-gate`, positional convention stated, sample `AC1 → T1`.
- **AC2** ✓ — `milestone-plan/SKILL.md:77–82` instructs authoring the
  positional Coverage map after criteria/tasks; unmapped criterion = planning
  gap.
- **AC3** ✓ — `milestone-review/SKILL.md`: AC fencing (step 3, "evidence
  before the checkbox") and Coverage-completeness gate (step 4, unmapped
  criterion = gate failure back to implement).
- **AC4** ✓ — `tracking-rules.md:55` Coverage ownership row (owner: plan);
  `:61–63` "AC fencing (review discipline)" paragraph ("no evidence line, no
  tick").
- **AC5** ✓ — `test_ac_traceability.py` 11/11 pass; full `skills/tests` suite
  46/46 green post-merge.

### Consistency gate

- `cairn_validate.py` exit 0 (all 9 checks pass), incl. post-merge (M19 row +
  candidates merged from main, ROADMAP conflict resolved to M18=review).
- **Coverage completeness:** N/A for M18 — M18 predates the Coverage section
  it introduces (planned under the old template). The gate is live for
  milestones planned under the updated template (M19 has a Coverage section).
  Review does not retro-add one: Coverage is plan-owned (amend-via-gate).
- Principle change: none (no IP/GP edited) → `cairn_impact` skipped.
- R-package gates (`devtools::*`, README.Rmd, pkgdown, NEWS, `.Rbuildignore`):
  waived — plugin repo, per CLAUDE.md / ROADMAP note.

### Independent review (two lenses + scorer)

- **[O] diff-bug (Opus):** 1 finding. **[S] blame-history (Sonnet):** no
  findings (M14 allow-lists, M17 fan-out, D-016 all intact).
- **Finding (scored 90 → actioned):** the new AC-fencing rule told review to
  tick the acceptance-criterion checkbox, but the section-ownership table +
  review step 3 said review never writes the plan-owned Acceptance criteria
  section, and no write-mode authorized the tick — an internal contradiction
  in M18's own deliverable (and this very review was enacting it).
  **Triage: fixed now on the branch** — authorized review's tick as a
  *verification mark* distinct from editing the criterion text:
  `milestone-review/SKILL.md` step 3, the `tracking-rules.md` Acceptance-
  criteria ownership row, and the AC-fencing paragraph all updated. The fix
  briefly dropped the "section-ownership table" reference and the M14
  allow-list guard caught it; restored. Full suite 46/46 green after the fix.
- Sub-threshold (<80): none.
