# M131: A scripted edit is verified to have landed before the record claiming it did

**Status:** done (2026-08-02, PR #131 https://github.com/jmgirard/cairn/pull/131)

**Goal:** Close the three-instance class where a batched or scripted edit lands
somewhere other than its aimed site — or not at all — while the record claiming
it landed is written anyway.

**Outcome:** `tracking-rules.md` "Universal tracking rules" gains a three-clause
conduct rule: verify a batched or scripted edit landed before any record claims
it; anchor a section-targeted edit on text occurring exactly once in the target
file; sequence a check-off strictly after its evidence write has succeeded,
never in the same unverified batch. Pinned by `test_scripted_edit_landing.py`
(5 asserts), registered per assert in the mutation harness (5 blocks),
13 mutations all RED including subject transposition and whole-bullet deletion.

**Decisions:** none promoted. Plan gate: rulebook over a LESSONS line (no suite
asserts lesson content); uniqueness alone over banning bare-header anchors.

**Review:** 2 rounds. Round 1 (3 lenses, 20 scored) returned under M130's floor
— F3d/90 and F3e/90 broke AC3, anchors pinning predicates but not subjects.
Round 2 (delta + scorer, 10 scored) confirmed all six fixes closed; N1/90,
N2/88, N9/82 corrected the review record itself; N3/85, N7/85 closed in code.
Defect returns: 1. First exercise of the return floor.
