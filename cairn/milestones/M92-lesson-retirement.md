<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M92: Lesson retirement — a lesson leaves LESSONS.md when a guard enforces it or another file owns it

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP1, GP4
- **Branch/PR:** `m92-lesson-retirement`

## Goal

Give `cairn/LESSONS.md` an outflow, so the file stops being append-only-in-practice against a hard cap it has now reached.

## Scope

**In:** Two retirement criteria stated as a named rulebook rule — **enforcement**
(a test fails on the mistake the lesson warns about) and **ownership** (another
tracking file's slot owns the content, which this milestone may *move* there
rather than requiring it already be duplicated) — plus a **partial
disposition**: a lesson covered only in part is trimmed to its uncovered
remainder, never kept whole. The check wired into `/milestone-review` post-merge
hygiene, scoped to what the milestone shipped; a D-entry recording the criteria,
the partial disposition, the tombstone, and the rejected alternatives; a guard
test with mutation registration; and a first application pass over the current
49 lessons that leaves real headroom on both axes, relocating owned content into
`cairn/PROFILE.md`'s slots and consolidating related lessons where the criteria
alone do not reach the bar.

**Out:**
- Age-based retirement beyond D-015's existing "prune the stalest when full" →
  D-015 stands unchanged and stays the last-resort remedy; not re-opened here.
- An in-file graduation breadcrumb, or a separate graduated-lessons file →
  both rejected at the plan gate; the rationale is recorded in the D-entry (T1),
  not left implicit.
- The same outflow for `references/` pages or `DESIGN.md` → a `candidate` row if
  a second file ever shows the same pressure; LESSONS is the one at its cap.
- Changing either the 50-line cap or the 20,500-char threshold → M87/D-049 own
  those values. This milestone changes *outflow*, never the budget.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md` states the retirement rule under its
      own name, giving both criteria with their *discriminating* tests —
      enforcement is "a test fails on the mistake the lesson warns about", never
      "a guard exists in this area"; ownership covers content this milestone
      moves into its owner, not only content already duplicated there — plus the
      partial disposition (a partly-covered lesson is trimmed to its uncovered
      remainder), and stating that retirement is distinct from D-045's in-place
      correction, since a retired lesson is not a false one.
- [ ] AC2: `skills/milestone-review/SKILL.md`'s post-merge hygiene performs the
      retirement check beside the existing capture step, scoped to what the
      milestone shipped rather than sweeping all lessons.
- [ ] AC3: The rule and the D-entry both state that a retired lesson leaves no
      line in `LESSONS.md` and that the retiring milestone's archive summary is
      the record (the form `archive/M53-prose-guard-mutation-harness.md:17`
      already uses).
- [ ] AC4: A guard test locks the rule with label-inclusive asserts, is
      registered in `skills/tests/test_mutation_harness.py`, and each registered
      block fails its guard when blanked by the mutation driver.
- [ ] AC5: The first application pass leaves `cairn/LESSONS.md` with ≥2 lines of
      item headroom and ≥500 chars of weight headroom, measured by
      `cairn_scripts.line_count`/`char_count` against `LINE_CAPS`/`CHAR_CAPS`,
      with the measurement recorded as evidence.
- [ ] AC6: All three `verify` suites green (`cairn/PROFILE.md`) and
      `cairn_validate` PASS on every check with no new advisory raised.

## Coverage

- AC1 → T1, T2, T4
- AC2 → T3
- AC3 → T1, T2
- AC4 → T5, T6
- AC5 → T7
- AC6 → T8

## Tasks

- [x] T1: Draft `D-051` in `cairn/DECISIONS.md`: both criteria and their
      discriminating tests; the archive-summary tombstone; the rejected
      alternatives (in-file breadcrumbs — D-049 already retired that pattern as
      restating archive-owned history; a separate graduated file — the
      divergence vector M56 rejected; mechanized age-pruning). Annotate D-015
      (its prune-the-stalest survives as last resort) and cross-reference D-045
      (retirement ≠ correction).
- [x] T2: Write the rule into `skills/shared/tracking-rules.md`, at the
      weight-caps remedies and the `cairn/LESSONS.md` file-map row. Author each
      anchor on its own physical line with its label and members together
      (M74/M90); do not reflow neighbouring registered blocks (M78/M82).
- [ ] T3: Wire the check into `skills/milestone-review/SKILL.md` post-merge
      hygiene, beside "Capture durable lessons", scoped to what shipped.
- [ ] T4: Correct `cairn/LESSONS.md`'s own header prose, which currently teaches
      the 50-line prune as the file's only outflow — a third encoding of the
      rule, the shape M87/F1 caught teaching a retired number.
- [ ] T5: Extend `skills/tests/test_lessons_loop.py` with the retirement guard:
      label-inclusive asserts (M74), word-bounded `assertRegex` where a new name
      could be a substring of an existing anchor (M60/M80/M85), target read
      per-test rather than cached in `setUpClass` (M61).
- [ ] T6: Register the new blocks in `skills/tests/test_mutation_harness.py` —
      one entry per new positive assertion, not one per file (M53) — and run the
      driver to confirm each blanked block reddens.
- [ ] T7: First application pass: evaluate all 49 lessons against both criteria,
      retire or trim what qualifies, relocating owned content into the matching
      `cairn/PROFILE.md` slot as part of the move, and collect the graduation
      list for the archive summary. Where the criteria do not reach AC5's
      headroom bar, consolidate related lessons rather than stretching a
      criterion to fit; D-015's prune-by-age stays the untouched last resort. Use
      targeted `Edit` calls, never a bulk string script (M61), and never
      `replace_all` on a line whose indentation varies (M90).
- [ ] T8: Run all three suites and `cairn_validate` from the repo root, checking
      each exit code explicitly (M56/M65); grep every word the new prose adds
      against the anchors existing guards assert on (M85).

## Work log

- 2026-07-19: created by /milestone-plan.
- 2026-07-19: in-progress on `m92-lesson-retirement`, cut from main at 16289bf.
- 2026-07-19: step-3 gate amended Scope + AC1 + T7 — ownership permits MOVING content to its owner (not duplication-only), a partly-covered lesson is trimmed to its uncovered remainder, and consolidation (not D-015 prune) is AC5's headroom fallback. Preliminary sweep showed strict enforcement alone retires ~0 lessons, putting AC5 at risk; user chose all three recommendations.
- 2026-07-19: T2 — rule written into tracking-rules beside "Correcting a record proven false" (the contrast D-051 turns on) + the LESSONS file-map row; 7 anchors verified unique and unwrapped; `archive summary`/`post-merge hygiene` each gained an occurrence, checked against every guard anchor (M85) — both existing guards use longer phrases, no degradation.
- 2026-07-19: T1 — D-051 appended: enforcement + ownership criteria, trim-to-remainder for partial coverage, archive-summary tombstone; four alternatives rejected with rationale.

## Decisions

## Review
