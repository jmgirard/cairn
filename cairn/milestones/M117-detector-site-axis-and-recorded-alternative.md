# M117: Detector coverage on the site axis, and a plan gate that records the alternative it rejected

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP4
- **Branch/PR:** m117-detector-site-axis-and-recorded-alternative · https://github.com/jmgirard/cairn/pull/117

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
mutation registrations for every block added, with the existing trigger-(b)
locators verified to still resolve against the edited bytes.

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

- [x] AC1: `skills/shared/guard-doctrine.md` §3 names the site axis of a
      detector's renderings — the branches, message literals, or code paths at
      which the target can appear — beside the numeric-format axis its existing
      prescription covers, and states separately that exercising every number
      format of one literal is not coverage of a surface that has several. Each
      of those two claims is pinned by its own assert in
      `skills/tests/test_lesson_graduation.py`, matched with `\s+` wherever the
      shipped text wraps.
- [x] AC2: The same section states that a count of hand-enumerated entries
      measures the enumeration and not the surface — the `checked == N` shape
      over a hand-listed set — and prescribes the producer-derived remedy:
      sweep the producer's own outputs and assert the invariant over them
      rather than enumerating renderings. The text builds on §3's shipped
      author-cannot-enumerate sentence rather than restating it, and §7 gains
      at most a one-line pointer. Negative claim and remedy pinned separately.
- [x] AC3: Every prose block this milestone adds to an already-registered guard
      file carries its own entry in `skills/tests/test_mutation_harness.py`
      (registration is per file, so a sibling entry does not cover a new
      assert), every existing registry locator whose bytes this milestone
      re-wraps resolves against the shipped bytes, and
      `TestRegisteredGuardsFailWhenBlanked` passes.
- [x] AC4: `skills/milestone-plan/SKILL.md` obliges the plan author, at step 4
      where the milestone file is created, to append one work-log line per
      choice between approaches the gate actually weighed — the alternative
      rejected, why it lost, and the class of evidence that would falsify the
      choice — and states that a plan weighing none writes no line, so absence
      means none was weighed. `skills/shared/templates/milestone.md` shows the
      form in its work-log comment. Evidence: asserts in
      `skills/tests/test_thrash_rule.py` pinning the obligation and the
      no-line-when-none-weighed clause separately.
- [x] AC5: `skills/milestone-review/SKILL.md`'s trigger (b) names the work log
      as where that record is read from, and `test_thrash_rule.py`'s existing
      anchor `reconsider the alternative the plan gate recorded\s+against`
      still matches the shipped bytes.
- [x] AC6: The `verify` slot's three suites are green (`Ran N tests … OK` for
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
      §3's existing author-cannot-enumerate sentence and leaving §7 itself
      untouched — the one-line pointer runs from §3 to §7, not the reverse.
- [x] T2: Add one assert per claim to `skills/tests/test_lesson_graduation.py`
      — anchors copied from the target's actual bytes (M95), read via
      `Path.read_text` (M100), `\s+` over shipped wraps (M105) — and register
      each new block in `skills/tests/test_mutation_harness.py`.
- [x] T3: Add the recorded-alternative obligation to
      `skills/milestone-plan/SKILL.md` step 4 and the work-log pointer to
      `skills/milestone-review/SKILL.md` trigger (b); then re-resolve
      `test_mutation_harness.py`'s existing trigger-(b) locators against the
      edited bytes, updating them if the wrap moved (it did not — the edit was
      authored to leave every span in that bullet intact).
- [x] T4: After both prose edits, grep every guard assertion anchored near the
      edited lines for contiguity on one physical line (M104), and grep the
      guards for any short phrase the new prose repeats, which can hand an
      existing bare `assertIn` false coverage (M113).
- [x] T5: Add a plan-skill reader and the gap-B asserts to
      `skills/tests/test_thrash_rule.py`; register every added block in the
      mutation harness.
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
- 2026-07-27: correcting the T4 line above — the sweep extracted string literals appearing inside assertion CALLS (path arguments included), not assertion literals only, and the 8 were flagged rows over 2 guard files, not 8 call sites; the finding it reports is unchanged, no literal went from unique to ambiguous.
- 2026-07-27: §8 description-layer certification (fresh-context [O]) returned 8 discrepancies, all fixed: AC4's template clause and the cardinality clause were unasserted (2 asserts + 3 registry entries added), shipped prose said "per approach" where the AC says per approach CHOICE (corrected in skill + template), a class docstring counted asserts and a registry comment claimed a remedy the site paragraph does not have (both rewritten as pointers, M116), a comment stated a firing count the shipped predicate does not yield, and one comment cited a downstream count not checkable in this repo.
- 2026-07-27: gated amendment (user approved) — Scope's "whose bytes the edit re-wraps" replaced with the two locators "verified to still resolve against the edited bytes"; the predicted re-wrap did not occur, T3's text corrected with it. No scope change.
- 2026-07-27: superseding the T7 line's counts — after the certification rounds added asserts, verify is skills/tests 671 OK, scripts/tests 280 OK, hooks/tests 91 OK; cairn_validate 16 PASS exit 0, `all checks passed`; registry 433 blocks (421 at M116 + 12).
- 2026-07-27: superseding the T3+T5 line's "both trigger-(b) locators" — trigger (b)'s bullet carries four registry locators, not two; all four resolve unchanged, as does every other block in the registry.
- 2026-07-27: re-certification round 2 returned 6 discrepancies, all fixed: the template example moved INTO the work-log comment (as a body line it shipped a placeholder into every instantiated milestone, and made AC4's wording false), a new assert pins the obligation inside step 4 by its surrounding numbered steps (review's pointer names step 4 and was pinned; the bullet it points at was not), a registry comment re-pointed off an enumeration, T1's §7 claim disambiguated, and Scope's locator count dropped by gated amendment (user approved).
- 2026-07-27: re-certification round 3 returned 6, all fixed. Three were one class — the ACs name a LOCATION (§3, trigger (b), the template's work-log comment) and every assert matched the whole file, so each paragraph could move with the suite green; closed with containment asserts bounded by surrounding headings, the shape round 2 added on the plan side. Also: this file's module docstring and the gap-B class docstring both enumerated properties and had gone stale against their own additions (re-pointed at the methods, no list), and T5's "two asserts / both blocks" corrected.
- 2026-07-27: the three containment asserts take guard-doctrine §2's by-hand check rather than a registry entry — each fails against pre-milestone content (§3 lacks both paragraphs, trigger (b) lacks the pointer, the template lacks the form) — and their section markers are scaffolding, which the rulebook warns against pinning. Registry stays 433.
- 2026-07-27: superseding the 671 above — final measured state, taken after the last code edit so nothing re-stales it: skills/tests 672 OK, scripts/tests 280 OK, hooks/tests 91 OK; cairn_validate 16 PASS, exit 0, `all checks passed`; registry 433 blocks.
- 2026-07-27: round 4 returned 2, both record-accuracy, both fixed: the count above, and this guard's module docstring partitioning M117's additions as plan-side when one of them (trigger (b)'s work-log pointer) is review-side — the missing bullet added. Rounds ran 8 -> 6 -> 6 -> 2 with the last two rounds finding no artifact defect.

## Decisions

## Review

**Evidence gathered 2026-07-27 by command, on branch HEAD; every inversion
restored the file byte-identical (verified in the same run).**

- **AC1** — both claims present in the `## 3. Absence assertions` slice.
  Inversion: deleting the site-axis naming sentence RED; deleting the
  "Exercising every number format of one literal is not coverage" consequence
  RED — separately, so neither is masked by the other. Relocating both new
  paragraphs from §3 into §7 RED, so the criterion's `§3` home is pinned and
  not merely its text.
- **AC2** — negative claim and remedy both present in the same slice.
  Inversion: deleting the `**A count of enumerated entries…**` heading RED;
  deleting the producer-sweep remedy RED, separately. §7 byte-identical to
  `main` (`git diff --stat main..HEAD -- skills/shared/guard-doctrine.md`
  shows the §3 insertion only), so "§7 gains at most a one-line pointer"
  holds; the pointer runs §3→§7.
- **AC3** — `TestRegisteredGuardsFailWhenBlanked` OK (1 test). Registry 433
  blocks against 421 on `main`; all 12 M117 entries enumerated by target and
  block, all resolving (a non-resolving locator raises, so green is proof).
  The three containment asserts take guard-doctrine §2's by-hand check
  instead: each fails against pre-milestone content, shown by the relocation
  inversions under AC1/AC4/AC5 rather than asserted.
- **AC4** — inversion, each separately RED: whole obligation bullet deleted;
  cardinality clause deleted; absence case deleted; bullet MOVED out of step 4
  into step 5; the template form deleted from the work-log comment; and the
  template form MOVED from the comment into the body — the regression that
  would ship a `<approach>` placeholder into every instantiated milestone.
- **AC5** — inversion: deleting trigger (b)'s work-log pointer RED, and MOVING
  it out of trigger (b) into the composition paragraph RED. The pre-existing
  anchor `reconsider the alternative the plan gate recorded\s+against` still
  matches (suite green, and its registry locator resolves).
- **AC6** — `skills/tests` Ran 672 OK · `scripts/tests` Ran 280 OK ·
  `hooks/tests` Ran 91 OK · `cairn_validate` exit 0, 16 PASS, `all checks
  passed`. Counts read from command output.

**Consistency gate.** `cairn_validate` exit 0, 16 PASS / 7 advisory OK, no
FAIL. `cairn_impact` skipped — `DESIGN.md` is untouched by the diff, so no
principle changed (the `Principles touched: GP1, GP4` slot records the
principles worked under, not changed). Profile `generic`: the
`consistency-gate` slot names no toolchain checks, so that half is a clean
no-op. No CI in this repo.

**Thrash rule.** Zero returns — first review pass, no re-cut. Neither trigger
fires.

**Description-layer certification (guard-doctrine §8).** Four fresh-context
[O] rounds before the gate: 8 → 6 → 6 → 2 discrepancies, all closed. Rounds 1
and 2 found defects in the work (two unsatisfiable criteria; a template
placeholder that would ship into every milestone; four AC clauses naming a
location no assert pinned); rounds 3 and 4 found none in the artifact. The
gate was entered after round 4's two record-accuracy items were fixed, without
a fifth round auditing only those fixes — a judgment call recorded here rather
than presented as a clean round.

