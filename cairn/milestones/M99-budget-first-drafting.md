<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M99: Budget-first drafting — a capped artifact's size is visible while it is written

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make a capped artifact's size visible at drafting time — a path-scoped counter
plus measured per-artifact budgets in the templates — so first drafts land
under cap by construction instead of being compressed afterward.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A new `scripts/cairn_budget.py` reporter taking a path and reporting
that file against whichever cap applies, milestone files additionally getting
the plan-owned section breakdown; per-section drafting budgets in
`skills/shared/templates/milestone.md`, derived by measurement; a new
archive-summary template, which does not exist today (the ≤25-line artifact
with the worst measured thrash is drafted freehand from
`skills/milestone-review/SKILL.md:183`); wiring at the two drafting steps that
produced that thrash — `/milestone-plan` step 4 and `/milestone-review` step 9.

**Out:**
- **Changing any cap number, threshold, or comparison operator.** M69 spun this
  candidate off with "what's counted untouched (D-030)"; D-049's measured
  thresholds and M96's fence over `LINE_CAPS`/`CHAR_CAPS` both stand.
- **New enforcement.** Budgets are drafting guidance; the only gate-failing
  size check stays `cairn_validate`'s existing `weight caps`. A second,
  per-section cap is the split-budget shape D-030 already declined → not here,
  and not deferred elsewhere.
- Rulebook prose. `tracking-rules.md` is M95's editorial surface; this
  milestone adds no line to it. The budgets live where drafting happens.
- A growth ratchet over the uncapped always-read files → M96.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: `cairn_budget.py` reports a given path against its cap for every
      capped artifact class — live milestone plan-owned body, archive summary,
      `ROADMAP.md`, `LESSONS.md`, `PROFILE.md`, and a CLAUDE.md cairn section —
      with a test per class firing in both directions (under and over), and
      exits 2 outside a cairn repo like the other reporters.
- [ ] AC2: Every cap it reports is read from `cairn_scripts`, never restated:
      a guard reddens if a cap literal appears in `cairn_budget.py`, and the
      body count it prints for a milestone equals `milestone_body_line_count`
      for that same file, so the drafting counter and the gate counter can
      never disagree.
- [ ] AC3: The per-section budgets in `templates/milestone.md` are **derived by
      measuring** this repo's live and archived milestone files — never assumed
      (D-049, M87) — the measurement recorded in the work log, and their sum
      leaves stated headroom under the 150-line cap.
- [ ] AC4: An archive-summary template exists carrying the ≤25-line budget and
      a per-section allocation derived the same measured way, and
      `/milestone-review` step 9 authors the summary from it.
- [ ] AC5: Both drafting steps hand the operator a runnable counter command in
      its own fenced block (D-048), and that wiring is guard-pinned with the
      guards registered in the mutation harness — per file, since an added
      assertion in an already-registered file is not covered (M60/M85).
- [ ] AC6: This milestone runs its own rule over its own artifacts (M78): its
      milestone file and its archive summary each land under budget on first
      draft, with the counter output recorded rather than asserted.
- [ ] AC7: `verify` clean — `python3 -m unittest` over all three suites, each
      run from the repo root with its exit code checked separately (M56/M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T1, T4
- AC4 → T1, T5
- AC5 → T6, T7
- AC6 → T2, T7
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Measure, and record the distributions in the work log: plan-owned
      section sizes across `cairn/milestones/*.md` + `archive/*.md`, and
      section sizes across the archive summaries. Derive both budget sets from
      what is measured; state the headroom each set leaves.
- [ ] T2: `scripts/cairn_budget.py` — resolve a path to its artifact class,
      report count vs. cap vs. headroom, reusing `cairn_scripts` constants and
      helpers (`milestone_body_line_count`, `milestone_section_line_counts`,
      `char_count`, `non_item_lines`, `claude_section_line_count`); milestone
      paths also get the heaviest-first section breakdown M69 established.
- [ ] T3: `scripts/tests/test_cairn_budget.py` — a fixture per artifact class,
      both directions; the no-cap-literal guard; the body-count agreement test
      against `milestone_body_line_count`.
- [ ] T4: `skills/shared/templates/milestone.md` — add T1's per-section budgets
      to the existing ownership comments, as drafting guidance.
- [ ] T5: `skills/shared/templates/archive-summary.md` — new, from T1's
      allocation, in the idiom of the shipped templates.
- [ ] T6: Wire `/milestone-plan` step 4 and `/milestone-review` step 9 — the
      fenced counter command, and for review a pointer to author from T5.
- [ ] T7: Guards in `skills/tests/` for T4–T6 wording, registered in
      `test_mutation_harness.py`; update `cairn/DESIGN.md:58`'s `scripts/`
      inventory to name `cairn_budget` — and `cairn_cost`, absent from that
      bullet since M94; run the counter over this milestone's own file and
      record; run all three suites.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-20: created by /milestone-plan. Graduates the budget-first-drafting candidate (lineage: M69 Out, "prevention (budget-first drafting) → candidate"); gate took all four recommendations — cover every capped artifact, templates-only budget home plus a new archive template, advisory per-section budgets, no M95 dependency.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
