# M117: Detector coverage on the site axis, and a plan gate that records the alternative it rejected

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP4
- **Branch/PR:** m117-detector-site-axis-and-recorded-alternative

## Goal

Close the two doctrine gaps intraclass M93's four-pass evidence-quality return
loop exposed in cairn's own rules.

## Scope

**In:** `guard-doctrine.md` §3 gains the **site** axis of a detector's
renderings — branches, message literals, code paths — beside the numeric-format
axis it already prescribes for, plus the rule that a count of hand-enumerated
entries measures the enumeration and not the surface, and the producer-derived
remedy that enumerates nothing. `/milestone-plan` gains an obligation to record
the alternative the gate rejected as a work-log line; `/milestone-review`'s
thrash trigger (b) names the work log as where it reads that record. Guards and
mutation registrations for every block added, and re-resolution of the two
existing trigger-(b) locators whose bytes the edit re-wraps.

Evidence base: the intraclass M93 post-mortem brief (2026-07-27) — four
consecutive AC5 failures, passes 6–9, no `R/` file changed after pass 6. Pass 9:
`boundary_method_hint()` renders three message literals, the guard hand-listed
two and asserted `checked == 2L`, and a leak placed only in the un-listed
singular lead passed at FAIL 0 / PASS 720 — a lead measured at 74 of 1,680
real aborts.

**Out:**
- Promoting the one-surface-pin row (ROADMAP one-surface pin) → stays parked;
  its evaluation is recorded on the row at this plan gate, not here.
- A `cairn_validate` check for either rule → D-064 choice 6 already rejected
  mechanizing this family; no new row.
- Editing §7's sweep-count rule beyond a one-line pointer → §7 stands as
  shipped.

## Acceptance criteria

- [ ] AC1: `skills/shared/guard-doctrine.md` §3 names the site axis of a
      detector's renderings — the branches, message literals, or code paths at
      which the target can appear — beside the numeric-format axis its existing
      prescription covers, and states separately that exercising every number
      format of one literal is not coverage of a surface that has several. Each
      of those two claims is pinned by its own assert in
      `skills/tests/test_lesson_graduation.py`, matched with `\s+` wherever the
      shipped text wraps.
- [ ] AC2: The same section states that a count of hand-enumerated entries
      measures the enumeration and not the surface — the `checked == N` shape
      over a hand-listed set — and prescribes the producer-derived remedy:
      sweep the producer's own outputs and assert the invariant over them
      rather than enumerating renderings. The text builds on §3's shipped
      author-cannot-enumerate sentence rather than restating it, and §7 gains
      at most a one-line pointer. Negative claim and remedy pinned separately.
- [ ] AC3: Every prose block this milestone adds to an already-registered guard
      file carries its own entry in `skills/tests/test_mutation_harness.py`
      (registration is per file, so a sibling entry does not cover a new
      assert), every existing registry locator whose bytes this milestone
      re-wraps resolves against the shipped bytes, and
      `TestRegisteredGuardsFailWhenBlanked` passes.
- [ ] AC4: `skills/milestone-plan/SKILL.md` obliges the plan author, at step 4
      where the milestone file is created, to append one work-log line per
      choice between approaches the gate actually weighed — the alternative
      rejected, why it lost, and the class of evidence that would falsify the
      choice — and states that a plan weighing none writes no line, so absence
      means none was weighed. `skills/shared/templates/milestone.md` shows the
      form in its work-log comment. Evidence: asserts in
      `skills/tests/test_thrash_rule.py` pinning the obligation and the
      no-line-when-none-weighed clause separately.
- [ ] AC5: `skills/milestone-review/SKILL.md`'s trigger (b) names the work log
      as where that record is read from, and `test_thrash_rule.py`'s existing
      anchor `reconsider the alternative the plan gate recorded\s+against`
      still matches the shipped bytes.
- [ ] AC6: The `verify` slot's three suites are green (`Ran N tests … OK` for
      `skills/tests`, `scripts/tests`, `hooks/tests`) and
      `python3 scripts/cairn_validate.py` exits 0 printing `all checks passed`
      — every count written from command output, never memory.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2, T3, T5
- AC4 → T3, T5, T6
- AC5 → T3, T5
- AC6 → T4, T7

## Tasks

- [x] T1: Re-read `guard-doctrine.md` §7 and §8 for the single-home check, then
      author §3's new text: the site-axis claim, the not-coverage claim, the
      enumeration-count claim, and the producer-sweep remedy, building on
      §3's existing author-cannot-enumerate sentence and leaving §7 a
      one-line pointer.
- [x] T2: Add one assert per claim to `skills/tests/test_lesson_graduation.py`
      — anchors copied from the target's actual bytes (M95), read via
      `Path.read_text` (M100), `\s+` over shipped wraps (M105) — and register
      each new block in `skills/tests/test_mutation_harness.py`.
- [x] T3: Add the recorded-alternative obligation to
      `skills/milestone-plan/SKILL.md` step 4 and the work-log pointer to
      `skills/milestone-review/SKILL.md` trigger (b); then re-resolve
      `test_mutation_harness.py`'s two trigger-(b) locators against the
      reflowed bytes and update them where the wrap moved.
- [x] T4: After both prose edits, grep every guard assertion anchored near the
      edited lines for contiguity on one physical line (M104), and grep the
      guards for any short phrase the new prose repeats, which can hand an
      existing bare `assertIn` false coverage (M113).
- [x] T5: Add a plan-skill reader and the two gap-B asserts to
      `skills/tests/test_thrash_rule.py`; register both blocks in the mutation
      harness.
- [x] T6: Add the work-log example line to
      `skills/shared/templates/milestone.md`'s work-log comment.
- [x] T7: Run the three `verify` suites and `cairn_validate`; record every
      count from the command's own output.

## Work log

- 2026-07-27: created by /milestone-plan.
- 2026-07-27: plan gate weighed the record's home — work log over the Scope section, because a re-cut supersedes Scope and unticks criteria while the work log stands (D-064's own argument for the thrash count); falsified by a review pass that cannot find the record where trigger (b) looks.
- 2026-07-27: plan gate weighed §3 over §7 as the home for the enumeration-count rule — §7's remedy is a positive count, which the failing guard already passed at `checked == 2L`; falsified by a later count defect whose fix belongs to §7's sweep machinery rather than to detector visibility.
- 2026-07-27: T1+T2 — guard-doctrine §3 gains the site-axis and enumeration-count paragraphs (`guard-doctrine.md:109-126`), four asserts in `test_lesson_graduation.py`, four registry entries; suites 665/280/91 OK.
- 2026-07-27: T3+T5 — plan step 4 gains the rejected-alternative obligation, review trigger (b) points at the work log; both trigger-(b) registry locators re-resolved unchanged (deliberate re-wrap kept them contiguous); 4 asserts, 4 registry entries.
- 2026-07-27: T4 — diff-based sweep of every assertion literal in `skills/tests` against the four edited files: zero literals went from unique to ambiguous; the 8 flagged were `read("milestone-plan", ...)` path arguments, already multi-occurrence.
- 2026-07-27: T6 — template work-log comment names the record and shows a one-line example.
- 2026-07-27: T7 — verify clean: skills/tests 668 OK, scripts/tests 280 OK, hooks/tests 91 OK; cairn_validate 16 PASS, exit 0, `all checks passed`.

## Decisions

## Review
