<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M17: Review fan-out + confidence scoring

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m17-review-fanout   <!-- owner: implement (branch) / review (PR URL) · create -->

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
- [ ] Write `skills/tests/test_review_fanout.py` locking the two lenses,
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

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
