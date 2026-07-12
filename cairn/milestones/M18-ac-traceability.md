<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M18: Acceptance-criteria traceability

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M17   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m18-ac-traceability   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] The milestone template (`skills/shared/templates/milestone.md`) has a
      **Coverage** section mapping criterion → satisfying task(s), with an
      owner/write-mode ownership comment (owner: plan).
- [ ] `/milestone-plan` SKILL.md instructs authoring the Coverage map when it
      writes the acceptance criteria and tasks.
- [ ] `/milestone-review` SKILL.md enforces AC fencing: no criterion checkbox
      ticked without recorded evidence, and every criterion maps to ≥1 task via
      Coverage (a criterion with no task is a gate failure).
- [ ] `tracking-rules.md` section-ownership table lists the Coverage section
      (owner: plan) and the review-discipline text states the fencing rule.
- [ ] `skills/tests/test_ac_traceability.py` asserts the template section
      exists and the plan/review skills carry the coverage + fencing text.
      Test passes.

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] Add the Coverage section to `skills/shared/templates/milestone.md`
      (between Acceptance criteria and Tasks) with the ownership comment.
      ([template:25-31](../../skills/shared/templates/milestone.md))
- [ ] Update `/milestone-plan` step 4 to author the criterion→task Coverage
      map. ([SKILL.md](../../skills/milestone-plan/SKILL.md))
- [ ] Update `/milestone-review` steps 3–4 to enforce AC fencing + the
      coverage check. ([SKILL.md:31-42](../../skills/milestone-review/SKILL.md))
- [ ] Update `tracking-rules.md`: add the Coverage row to the section-ownership
      table and state the fencing rule in the review discipline.
      ([tracking-rules.md:47-58](../../skills/shared/tracking-rules.md))
- [ ] Write `skills/tests/test_ac_traceability.py`; run it green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (split from the "Review pipeline
  upgrades" candidate; sibling M17 covers reviewer fan-out).
- 2026-07-11: started implement; branch m18-ac-traceability. Gate chose
  positional-map Coverage format (AC1 → T1) — compact, cap-friendly,
  mechanically lint-able for the deferred cairn_validate.py check.
- 2026-07-11: T1 — added Coverage section to milestone template with
  positional-numbering + AC-fencing ownership comment.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
