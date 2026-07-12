<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M17: Review fan-out + confidence scoring

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m17-review-fanout · https://github.com/jmgirard/cairn/pull/15   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Strengthen `/milestone-review`'s independent review with a second orthogonal
evidence lens and a generate-then-verify confidence scorer that filters — but
never silently drops — low-confidence findings.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Rework `/milestone-review` step 5 (currently one fresh Opus reviewer,
[SKILL.md:71-78](../../skills/milestone-review/SKILL.md)) into a two-lens
fan-out plus a scoring pass:
- a **diff-bug reviewer** (Opus, current doctrine) and a **blame-history
  reviewer** (Sonnet), each with a distinct evidence base named in its prompt;
- a **confidence scorer** (Sonnet) that scores every flagged finding 0–100
  against a verbatim rubric, excludes sub-threshold findings from the actioned
  list but logs them in the Review section;
- a false-positive taxonomy embedded in the reviewer/scorer prompt text;
- the `tracking-rules.md` model-strategy section updated to describe the
  fan-out and scorer tiers, keeping "Never Haiku" intact;
- D-016 recording the never-Haiku decision (keep blanket; scorer on Sonnet).

**Out:**
- prior-PR-comments reviewer lens → candidate row (marginal until a repo has a
  thick PR history; needs `gh` API plumbing).
- Evidence-before-checkbox AC fencing + criterion→task coverage table → M18.
- Relaxing "Never Haiku" → decided against this milestone (D-016).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] `/milestone-review` step 5 spawns two distinct-evidence reviewers — a
      diff-bug reviewer ([O]-tagged, Opus) and a blame-history reviewer
      ([S]-tagged, Sonnet) — each with its own evidence base stated in its
      prompt. (behavior tested by the guard test below)
- [ ] A confidence scorer scores each flagged finding 0–100 against a rubric
      quoted verbatim in the skill; findings below the threshold (80) are
      excluded from the actioned triage list **but logged in the Review
      section** (count + one line each), never silently discarded.
- [ ] A false-positive taxonomy (pre-existing issue, linter-catchable,
      nitpick, unmodified line, intentional change) is embedded verbatim in the
      reviewer/scorer prompt text in the skill.
- [ ] `tracking-rules.md` "Model and agent strategy" describes the fan-out
      (Opus diff reviewer + Sonnet blame lens + Sonnet scorer) and the
      "Never Haiku. For anything." line is intact.
- [ ] `cairn/DECISIONS.md` has D-016 recording the never-Haiku decision (keep
      blanket rule; scorer on Sonnet) with rationale.
- [ ] `skills/tests/test_review_fanout.py` asserts the review skill contains
      both lenses, the scorer with its threshold, and the sub-threshold logging
      mandate — so the mechanics can't silently regress. Test passes.

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] Rework `/milestone-review` step 5 into the two-lens fan-out: diff-bug
      reviewer (Opus) + blame-history reviewer (Sonnet), each prompt naming its
      evidence base; embed the false-positive taxonomy.
      ([SKILL.md:71-78](../../skills/milestone-review/SKILL.md))
- [x] Add the generate-then-verify scorer sub-step: verbatim 0–100 rubric,
      threshold 80, exclude-but-log wired into the Review-section write.
- [x] Update `tracking-rules.md` "Model and agent strategy" (lines ~288–307)
      to describe the fan-out + scorer tiers; keep the "Never Haiku" line.
- [x] Append D-016 to `cairn/DECISIONS.md` (never-Haiku kept; scorer on Sonnet;
      rationale: review runs once per milestone, scorer gates what the user
      sees, blanket invariant is worth more than the marginal saving).
- [x] Write `skills/tests/test_review_fanout.py` locking the two lenses,
      scorer + threshold, and logging mandate; run it green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (split from the "Review pipeline
  upgrades" candidate; sibling M18 covers AC traceability).
- 2026-07-11: in-progress on m17-review-fanout; step 5 reworked into two-lens
  fan-out (Opus diff + Sonnet blame) + Sonnet confidence scorer (rubric,
  threshold 80, exclude-but-log). Tasks 1–2 done.
- 2026-07-11: model-strategy section updated to describe the fan-out; D-016
  appended (never-Haiku kept, scorer on Sonnet). Tasks 3–4 done.
- 2026-07-11: test_review_fanout.py added (9 checks); full suite 35/35 green.
  Task 5 done; all tasks complete → review.
- 2026-07-11: correction — test_review_fanout.py has 8 test methods, not 9
  (prior line's count was wrong).
- 2026-07-11: review — evidence gathered per criterion; fan-out review found
  one actioned issue (IP2→IP3 miscite, fixed) + two logged sub-threshold.
  Suite 35/35 after fix.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

Reviewed 2026-07-11 · PR #15 · diff `main..HEAD` = 6 files, +161/−17.

**Acceptance criteria (fresh evidence):**
- [x] C1 two distinct-evidence lenses — `milestone-review/SKILL.md:74,77`
      tier-tagged `[O] diff-bug reviewer (Opus)` + `[S] blame-history reviewer
      (Sonnet)`; "distinct evidence base" stated (:73).
- [x] C2 scorer + threshold + exclude-but-log — verbatim 0–100 rubric (:92),
      "below 80 are excluded … but logged … never silently dropped" (:97-99).
- [x] C3 false-positive taxonomy embedded verbatim in prompt text (:85-87).
- [x] C4 tracking-rules model-strategy describes the fan-out (:301-306);
      "Never Haiku. For anything." intact (:308).
- [x] C5 D-016 present in DECISIONS.md (:204).
- [x] C6 `test_review_fanout.py` (8 methods) locks lenses/scorer/threshold/log
      mandate; full suite 35/35 green.

**Consistency gate:** `cairn_validate.py` exit 0. No DESIGN principle changed →
impact report skipped. R gates waived (plugin repo, per CLAUDE.md). No CHANGELOG
entry — matches the M13–M16 precedent that tracking-mechanics milestones don't
get user-facing changelog lines.

**Independent review (two lenses + scorer):**
- Blame-history lens (Sonnet): no findings — confirmed the step-5 rework is
  plan-called-for, not a silent capability loss; never-Haiku byte-identical.
- Diff-bug lens (Opus): 3 findings → scorer (Sonnet) rated them.
  - **Fixed (92):** `SKILL.md:99` cited `(IP2)` for "never silently dropped";
    that verb is IP3 (conservation), and `cairn_impact.py` traces citations by
    whole word so the miscite mattered mechanically. Changed to `(IP3)` in the
    skill and the test docstring; suite still 35/35.
  - **Logged, not actioned (40):** AC3's "reviewer/scorer prompt text" read as
    requiring the taxonomy in the scorer prompt too. Scorer judged it an
    arguable overreading (taxonomy was intentionally scoped to reviewers). Kept
    as a possible future polish, not a defect.
  - **Logged, not actioned (25):** the 2026-07-11 work-log said "9 checks";
    the file has 8 methods — record slip, corrected below.
