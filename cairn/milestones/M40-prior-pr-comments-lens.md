<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M40: Prior-PR-comments reviewer lens

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m40-prior-pr-comments-lens   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Add a third distinct-evidence lens to `/milestone-review`'s fan-out — a
prior-PR-comments reviewer that flags where the current diff regresses a
lesson a past PR review already taught on the touched files.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a new `[S]` prior-PR-comments lens in `milestone-review/SKILL.md`
step 5, alongside the existing diff-bug and blame-history lenses. It gets a
documented gh/git **discovery recipe** (modified files → prior PRs that
touched them → `gh api` review comments), a **narrow judgment scope**
(regression/contradiction of a prior PR review comment on those files), the
same false-positive taxonomy and ref-based-git-only constraint the other
lenses receive, and **always-spawn / no-op-when-empty** behavior. Its
findings feed the existing `[S]` scorer unchanged. Plus the `tracking-rules.md`
model-strategy update (two → three reviewers) and the guard-test extension.

**Out:**
- A `cairn_*` helper script for comment gathering → stays a candidate; the
  recipe-in-prose approach was chosen at the plan gate (matches the blame
  lens; avoids a script with no other consumer). Revisit only if the recipe
  proves fragile in practice.
- Any change to the diff-bug or blame-history lenses, or to the scorer's 80
  threshold / IP3 logging → not in this milestone; the lens is purely
  additive.
- A conditional-spawn threshold heuristic (spawn only above N prior PRs) →
  rejected at the gate in favor of always-spawn/no-op; not a future item.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `milestone-review/SKILL.md` step 5 adds a third lens: an `[S]`
      prior-PR-comments reviewer (Sonnet) with a documented discovery recipe
      (modified files → prior PRs → `gh api` review comments) and a **narrow**
      judgment scope (flags only where the diff reintroduces or contradicts a
      prior PR review comment on the touched files).
- [ ] AC2 — the new lens is handed the same false-positive taxonomy and the
      same ref-based-git-only (shared-checkout) constraint as the other two
      lenses.
- [ ] AC3 — the lens **always spawns and no-ops cleanly**: with no prior-PR
      evidence (few/no PRs, or no GitHub remote) it reports "no prior-PR
      evidence" and contributes zero findings — never errors, never blocks the
      gate.
- [ ] AC4 — the lens's findings feed the **existing** `[S]` scorer unchanged
      (same 80 cutoff, same sub-threshold-logged-not-dropped mechanics — IP3);
      the diff-bug and blame lenses and the scorer threshold are untouched.
- [ ] AC5 — `tracking-rules.md` model-strategy section describes **three**
      distinct-evidence reviewers (was two), names the new lens, and keeps the
      blanket "Never Haiku" rule intact.
- [ ] AC6 — `skills/tests/test_review_fanout.py` is extended to lock the third
      lens (its Sonnet tier tag, discovery recipe, narrow scope, and
      no-op-when-empty behavior), and the full `skills/tests` suite passes
      green (`python3 -m unittest discover -s skills/tests`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2
- AC2 → T2
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T1, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Extend `skills/tests/test_review_fanout.py`: update
      `test_two_distinct_evidence_lenses` to assert **three** lenses, and add
      assertions for the prior-PR lens (Sonnet tier tag, discovery-recipe
      tokens, narrow-scope phrasing, no-op-when-empty phrasing). Run it and
      confirm it fails red against the current SKILL (tests-first). Anchor each
      asserted phrase on a single contiguous line per the M23/M26/M39 lessons.
- [x] T2 — Add the `[S]` prior-PR-comments lens to
      `skills/milestone-review/SKILL.md` step 5: discovery recipe, narrow
      "regression of a prior review comment" judgment scope, always-spawn /
      no-op-when-empty behavior, and the shared false-positive taxonomy +
      ref-based-git-only constraint. State that its findings flow into the
      existing scorer. (Satisfies AC1–AC3.)
- [x] T3 — Confirm/keep the scorer wiring unchanged: the new lens routes into
      the existing `[S]` scorer with no new threshold and no change to the 80
      cutoff or IP3 logging; adjust only the surrounding prose so the scorer
      reads all three lenses. (Satisfies AC4.)
- [x] T4 — Update `skills/shared/tracking-rules.md` model-strategy section:
      "two distinct-evidence reviewers" → three, name the prior-PR lens, keep
      the "Never Haiku" blanket rule. (Satisfies AC5.)
- [x] T5 — Run `python3 -m unittest discover -s skills/tests`; confirm T1 now
      passes and nothing else regressed. (Satisfies AC6 with T1.)
- [ ] T6 — Conservation hygiene (executes at review post-merge): graduate the
      "Prior-PR-comments reviewer lens" candidate row into M40 lineage, and
      mark item 3(d) of the steal-list in `cairn/references/anthropic-code-review.md`
      as shipped.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan. Promotes the "Prior-PR-comments
  reviewer lens" candidate (split 2026-07-11 from the review-pipeline
  candidate → M17/M18). Gate: recipe-in-prose (not a script), narrow
  regression scope, always-spawn/no-op-when-empty — all recommended, accepted.
- 2026-07-12: T1 — extended test_review_fanout.py (new TestPriorPRLens + a
  three-reviewer rulebook lock); 5 red by design (tests-first), rest green.
- 2026-07-12: T2–T5 — added the [S] prior-PR-comments lens to milestone-review
  SKILL step 5 (recipe-in-prose, narrow regression scope, always-spawn/no-op),
  updated tracking-rules model-strategy (two → three reviewers). T3 needed no
  edit — the scorer already reads "every surviving finding", lens-agnostic.
  Reflowed the rulebook so "Three distinct-evidence reviewers" is one physical
  line (M23 rule, bit my own assertion). skills 94 + scripts 53 green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
