<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M99: Budget-first drafting — a capped artifact's size is visible while it is written

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m99-budget-first-drafting` · https://github.com/jmgirard/cairn/pull/96   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: `cairn_budget.py` reports a given path against its cap for every
      capped artifact class — live milestone plan-owned body, archive summary,
      `ROADMAP.md`, `LESSONS.md`, `PROFILE.md`, and a CLAUDE.md cairn section —
      with a test per class firing in both directions (under and over), and
      exits 2 outside a cairn repo like the other reporters.
- [x] AC2: Every cap it reports is read from `cairn_scripts`, never restated:
      a guard reddens if a cap literal appears in `cairn_budget.py`, and the
      body count it prints for a milestone equals `milestone_body_line_count`
      for that same file, so the drafting counter and the gate counter can
      never disagree.
- [x] AC3: The per-section budgets in `templates/milestone.md` are **derived by
      measuring** this repo's live and archived milestone files — never assumed
      (D-049, M87) — the measurement recorded in the work log, and their sum
      leaves stated headroom under the 150-line cap.
- [x] AC4: An archive-summary template exists carrying the ≤25-line budget and
      a per-section allocation derived the same measured way, and
      `/milestone-review` step 9 authors the summary from it.
- [x] AC5: Both drafting steps hand the operator a runnable counter command in
      its own fenced block (D-048), and that wiring is guard-pinned with the
      guards registered in the mutation harness — per file, since an added
      assertion in an already-registered file is not covered (M60/M85).
- [ ] AC6: This milestone runs its own rule over its own artifacts (M78): its
      milestone file and its archive summary each land under budget on first
      draft, with the counter output recorded rather than asserted.
- [x] AC7: `verify` clean — `python3 -m unittest` over all three suites, each
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

- [x] T1: Measure, and record the distributions in the work log: plan-owned
      section sizes across `cairn/milestones/*.md` + `archive/*.md`, and
      section sizes across the archive summaries. Derive both budget sets from
      what is measured; state the headroom each set leaves.
- [x] T2: `scripts/cairn_budget.py` — resolve a path to its artifact class,
      report count vs. cap vs. headroom, reusing `cairn_scripts` constants and
      helpers (`milestone_body_line_count`, `milestone_section_line_counts`,
      `char_count`, `non_item_lines`, `claude_section_line_count`); milestone
      paths also get the heaviest-first section breakdown M69 established.
- [x] T3: `scripts/tests/test_cairn_budget.py` — a fixture per artifact class,
      both directions; the no-cap-literal guard; the body-count agreement test
      against `milestone_body_line_count`.
- [x] T4: `skills/shared/templates/milestone.md` — add T1's per-section budgets
      to the existing ownership comments, as drafting guidance.
- [x] T5: `skills/shared/templates/archive-summary.md` — new, from T1's
      allocation, in the idiom of the shipped templates.
- [x] T6: Wire `/milestone-plan` step 4 and `/milestone-review` step 9 — the
      fenced counter command, and for review a pointer to author from T5.
- [x] T7: Guards in `skills/tests/` for T4–T6 wording, registered in
      `test_mutation_harness.py`; update `cairn/DESIGN.md:58`'s `scripts/`
      inventory to name `cairn_budget` — and `cairn_cost`, absent from that
      bullet since M94; run the counter over this milestone's own file and
      record; run all three suites.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-20: CORRECTION to the T1 archive-summary entry below (IP4: superseded, not edited). That entry recorded the allocation as "title+status+blanks 5, Goal 3, Outcome 8, Decisions 3, Review 3". The allocation that SHIPPED, and that is correct, is `Goal 2 · Outcome 7 · Decisions 3 · Review 3` over 7 fixed lines — counting the skeleton gives title 1 + status 1 + five blank separators 5 = 7, not 5. Both sum to 22; no component agreed. Caught by two independent review lenses (F3); `test_the_archive_allocation_matches_the_templates_actual_fixed_lines` now derives the fixed-line count from the template on disk so the two records cannot re-diverge.
- 2026-07-20: review fan-out — 3 lenses + scorer. Actioned F1 (92), F2 (88), F4 (85); F3 (72) and F5 (35) scored sub-80 and were logged, then fixed anyway on operator judgment per M73. F1: the per-line axis printed OVER but was excluded from the exit verdict, so a wrapper checking `$?` read green on an over file — it is now a real `Axis`. F2: a readable `CLAUDE.md` with no cairn section exited 2 (this repo's not-a-cairn-repo signal) — `check_caps` passes that silently and now so does this. F4: the step-9 rewrite dropped the live milestone file's disposition, so following it literally orphaned the file until `roadmap<->disk orphans` caught it. Suites green after fixes: skills 509, scripts 269, hooks 72.
- 2026-07-20: review opened — draft PR #96. Gate evidence gathered: suites green at three separate exit codes (skills 507, scripts 266, hooks 72), `cairn_validate` exit 0 with 15 PASS and no FAIL/WARN. AC1-AC5 and AC7 verified; AC6 is verified only on its milestone-file half (117/149) — its archive-summary half is not verifiable until the step-9 hygiene pass authors that artifact, so the tick waits rather than resting on a charitable reading. Three review lenses spawned.
- 2026-07-20: T7 landed 16 guards (`skills/tests/test_budget_first_drafting.py`), 4 mutation-registry entries across 3 targets, and the `DESIGN.md` scripts inventory now naming `cairn_budget` — and `cairn_cost`, absent from that bullet since M94. The template-arithmetic guards RE-DERIVE every figure from the template on disk rather than pinning digits, so the self-referential block cannot drift green. Verified by inversion as well as blanking: rewording the budgets as "an enforced per-section cap" reddens, restoring greens.
- 2026-07-20: AC6 self-check — M99's own body is 117/149 (headroom 32) on first draft, so the milestone clears the rule it ships. It does exceed three SECTION budgets (AC 30 vs 28, Coverage 13 vs 11, Tasks 28 vs 25) while far under the cap: the budgets are p75 guidance, a quarter of drafts legitimately exceed a given section, and whole-file headroom absorbs it. That is the intended behaviour, not a miss — a section budget that could fail would be the second cap D-030 declined.
- 2026-07-20: T4–T6 wired the budgets. Milestone template carries one budget block (Goal 7 · Scope 26 · AC 28 · Coverage 11 · Tasks 25 over a 21-line preamble, ≥21 reserved for `## Decisions`, 139 of 149 permitted); the block is SELF-REFERENTIAL — stating the preamble size changes it — so it was measured, corrected, and re-measured to a fixed point rather than stated once. New comment-free `archive-summary.md` (15-line skeleton, 22-line budget). Also fixes label drift the T1 survey exposed: across the 96 summaries `Goal` ran 37 vs `Goal.` 16, and decisions split four ways (`Key decisions` 14, `Decisions` 7, `Decisions.` 7, `Key decisions.` 4).
- 2026-07-20: T2+T3 landed `scripts/cairn_budget.py` (six artifact classes, caps read from `cairn_scripts`, exit 0/1/2) and 20 guards: both directions per class, the `>=` vs `>` operator split (`<150` permits 149, `≤25` permits 25), body-count agreement with `milestone_body_line_count`, and a no-cap-literal assertion over the source. Suites green — skills 491, scripts 229, hooks 72, each exit code checked separately.
- 2026-07-20: T1 archive summaries measured, n=96: mean 23.3, median 25, p90 25, max 25 — 55 of 96 sit at EXACTLY 25, so the distribution is CENSORED at the cap and its percentiles measure the ceiling rather than demand. Unlike the body figures it is not a budget basis; the allocation is set deliberately below the median, targeting 22 (title+status+blanks 5, Goal 3, Outcome 8, Decisions 3, Review 3), leaving 3 lines headroom.
- 2026-07-20: T1 measured, n=99 full milestone files recovered from git history at their pre-archive state: plan-owned body mean 98.7, median 96, p90 130, max 149 (uncensored — bodies spread 97–149). Per-section p75: Goal 7, Scope 26, AC 28, Coverage 11, Tasks 25; preamble ~11. `## Decisions` is implement/review-owned and still counted (D-030/D-046) — mean 7.1 but p90 21, max 35 — so it grows after plan time and a plan-time budget must reserve for it, not spend it.
- 2026-07-20: implement gate — archive template is a comment-free skeleton with budgets stated in the review skill (a house-style comment block would spend a fifth of a 25-line budget); `cairn_budget.py` requires a path and prints usage bare, deliberately breaking the sibling reporters' optional-ROOT argv shape.
- 2026-07-20: created by /milestone-plan. Graduates the budget-first-drafting candidate (lineage: M69 Out, "prevention (budget-first drafting) → candidate"); gate took all four recommendations — cover every capped artifact, templates-only budget home plus a new archive template, advisory per-section budgets, no M95 dependency.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->

**PR:** #96 · reviewed 2026-07-20 · fan-out 3 lenses + scorer.

### Acceptance-criteria evidence (fresh, by command)

- **AC1 ✓** — 13 tests in `scripts/tests/test_cairn_budget.py`. All six classes
  classify (`test_each_capped_artifact_resolves_to_its_own_class`); item, mass,
  body, archive, CLAUDE-section and non-item-line axes each pass under cap and
  fail over it; `test_outside_a_cairn_repo_it_exits_2` and
  `test_no_argument_prints_usage_and_exits_2` green.
- **AC2 ✓** — `test_every_cap_comes_from_cairn_scripts_and_none_is_restated`
  (docstring-stripped, word-boundaried, paired with a positive `cs.` presence
  assert) and `test_the_reported_body_is_the_gates_own_measure` green;
  `test_the_work_log_is_excluded_exactly_as_the_gate_excludes_it` proves the
  D-046 exemption is the gate's, not a second rule.
- **AC3 ✓** — budgets derived from n=99 files recovered from git history,
  recorded in the work log. `test_the_stated_preamble_matches_the_templates_actual_preamble`
  re-derives 63−42=21 from disk rather than pinning digits;
  `test_the_stated_total_is_the_sum_of_the_stated_parts` and
  `test_the_stated_spare_is_the_gap_to_the_cap` confirm 97+21+21=139 of 149,
  10 spare.
- **AC4 ✓** — `skills/shared/templates/archive-summary.md` exists, comment-free,
  15 lines ≤ 25; allocation now cross-checked against the skeleton's own fixed-line
  count by `test_the_archive_allocation_matches_the_templates_actual_fixed_lines`;
  step 9 authors from it.
- **AC5 ✓** — fence guards green for both skills; 4 mutation-registry entries
  across 4 targets, harness green; verified by INVERSION as well as blanking
  (rewording the budgets as "an enforced per-section cap" reddens, restoring greens).
- **AC6 — deferred to the step-9 hygiene commit.** Its milestone-file half is
  verified: `cairn_budget.py` reports 117/149, headroom 32, on first draft. Its
  archive-summary half is not verifiable until step 9 authors that artifact,
  which is inside this review phase but after the merge. NOT ticked on the
  verified half alone — that is the charitable reading the rules forbid.
- **AC7 ✓** — three suites from the repo root, exit codes checked separately:
  skills 509 / scripts 269 / hooks 72, all exit 0. `cairn_validate` exit 0,
  15 PASS, 8 advisories OK, no FAIL or WARN.

### Consistency gate

`cairn_validate` exit 0 — including `coverage complete` and `roadmap<->disk orphans`.
Profile is `generic`, whose `consistency-gate` slot names no toolchain checks
beyond the universal ones, so that half is a clean no-op. No principle changed
(`Principles touched: GP1`, worked under and not modified), so `cairn_impact --changed`
was correctly skipped.

### Findings

Three lenses; the prior-PR lens reported **no prior-PR evidence** after querying
inline comments and review bodies across ~70 merged PRs touching these files —
all empty, the expected result for this repo. Its secondary pass over archived
`## Review` sections verified the M60/M85 template-registration lesson was
honoured rather than regressed. Scorer: fresh Sonnet agent, did not generate the
findings.

Actioned (≥80), all fixed on the branch:

- **F1 (92)** — `cairn_budget.py`: the per-line non-item-line axis printed
  "OVER by N" but was excluded from the exit-code verdict, contradicting the
  module's own stated contract ("Exit 0 within every axis, 1 if any axis is
  over"). A ROADMAP.md whose only line was a 502-char stamp printed `OVER by 103`
  and exited 0, so any wrapper checking `$?` read clean on a file the tool had
  just called over. The existing test asserted only on rendered text, pinning the
  bug rather than catching it. **Fixed:** the longest non-item line is now a real
  `Axis`, so it reaches the verdict like every other; new
  `test_an_over_length_non_item_line_reaches_the_exit_code` asserts the VERDICT,
  with a paired clean direction. Re-ran the original reproduction: exit 1.
- **F2 (88)** — `cairn_budget.py`: a readable root `CLAUDE.md` with no
  `## Project tracking` section was reported "unreadable" and exited 2 — this
  repo's not-a-cairn-repo signal per DESIGN.md — over a file that is fine.
  `claude_section_line_count`'s own docstring calls a missing section explicitly
  not a cap failure, and `check_caps` passes it silently. Hits the repo-mid-adoption
  case exactly. **Fixed:** reports "no cairn section — nothing capped here" and
  exits 0; two new tests cover it and the genuinely-absent direction.
- **F4 (85)** — `/milestone-review` step 9 no longer disposed of the live
  milestone file. The prior text compressed the file itself and moved it, so the
  move removed the live copy implicitly; authoring a fresh summary from a template
  makes disposal an explicit step, and the rewrite omitted it. Following step 9
  literally left the file on disk until `roadmap<->disk orphans` fired later in
  the same paragraph — a self-inflicted rework loop the step previously prevented.
  **Fixed:** step 9 now says the summary REPLACES the milestone file and names the
  deletion; `test_review_step_9_still_disposes_of_the_live_milestone_file` locks it.

Logged sub-threshold (surfaced, not silently dropped — IP3), both fixed anyway on
operator judgment per the M73 lesson that a score gates the actioned list, not the
operator's judgment:

- **F3 (72)** — the T1 work-log entry recorded an archive allocation whose every
  component disagreed with the one that shipped (fixed lines 5 vs 7, Goal 3 vs 2,
  Outcome 8 vs 7; both summing to 22). Raised independently by two lenses. Fixed
  despite the score because a false measurement in an append-only record is read
  by every later plan-time harvest — the harm D-045 exists to prevent. Corrected by
  an appended superseding entry (IP4), and a new guard derives the fixed-line count
  from the template on disk so the two records cannot re-diverge.
- **F5 (35)** — a mutation-registry comment said "three targets" where the four
  entries name four distinct target files. Pure prose accuracy; fixed in passing.

No finding was rejected. No criterion was reinterpreted; no plan-owned text was
edited review-side.
