<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M85: Extraction-status shape — the templates teach what the classifier reads

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m85-extraction-status-shape`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Make both `references/` templates teach the *shape* of an extraction status the
staleness classifier can read, and prove each sanctioned form classifies as its
author intends.

## Scope

**In:** state, in `source-note.md` and `synthesis-note.md`, what makes an
`Extraction:` status readable at all — it claims a verification, or carries a
date, or says it has nothing to re-verify — so an author writing novel wording
knows what to include. Extend the M80 pairing test
(`skills/tests/test_references_pages.py:180`) to select each alternative the
templates offer and assert the real `_last_verified` classification of each,
closing the gap where instantiating the dates was mistaken for instantiating
the choice.

**Out:** widening `_VERIFY_VERB` or any parser mechanism — M83/M83-D3 settled
classification and the narrowness here is the templates', not the parser's; a
`cairn_validate` CHECK on status shape (advisory doctrine has never been a
validate gate — D-029, M33/M42/M49; the `references staleness` WARN stays the
only reader); restructuring the `<a | b | c>` template idiom (kept, per the
plan gate — the test splits on the bar instead); the provenance
block-concatenation candidate, which has no live trigger and stays a ROADMAP
row.

## Acceptance criteria

- [ ] Both templates state the readable-status shape — a verification claim, a
      date, or an explicit nothing-to-re-verify — as a rule an author can apply
      to wording the template does not list, not as an enumeration of accepted
      phrases.
- [ ] The pairing test selects each alternative offered by each template's
      `Extraction:` field and asserts the state the real
      `cairn_validate._last_verified` returns for it; every sanctioned
      alternative classifies as its wording intends (no `ambiguous`, no
      `unrecognized`).
- [ ] A guard proves the whole-template (unchosen) form is what collapses:
      the source template reads `ambiguous` and the synthesis template reads
      `exempt` before a choice is made, so the per-choice assertions are shown
      non-vacuous. Paired with a positive signal that the classifier path
      actually ran, per the M84 lesson.
- [ ] The four forms this repo's own pages write that neither template lists —
      `verified at ingestion`, `partly verified at ingestion`, `read against
      the … artifacts at assessment time`, `verified by live probe DATE` — each
      satisfy the stated shape rule, demonstrated by a test that classifies
      them through the real classifier.
- [ ] `verify` clean per `cairn/PROFILE.md` (the three `python3 -m unittest`
      suites, each run from the repo root with its exit code checked — LESSONS
      M56/M65), and `cairn_validate` exit 0.

## Coverage

- AC1 → T2
- AC2 → T3
- AC3 → T3, T4
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1. Record the classification baseline: run `_last_verified` over both
      instantiated templates and over the four shipped forms, capturing the
      states in the work log so the milestone's before/after is evidence, not
      recall (the M83 before/after table is the precedent).
- [x] T2. Write the shape rule into both templates' `Extraction:` guidance
      (`source-note.md:19`, `synthesis-note.md:23` and their comment headers).
      Anchor any guarded phrase on one physical line, column 0 where it is a
      field — LESSONS M60/M78/M80 — and re-run the skills suite after any
      rewording near a registered block.
- [x] T3. Extend `TestTemplateProducesAValidPage` to split each template's
      `Extraction:` field on the `|` bar, build one page per alternative, and
      assert the real `_last_verified` state for each; add the non-vacuity
      guard that the unchosen whole-template form collapses to
      `ambiguous`/`exempt`.
- [x] T4. Add the shipped-form classification test covering the four forms in
      AC4, so the vocabulary the repo actually writes is pinned against a
      future parser or template change.
- [x] T5. Author the shape-rule prose-guard (`TestTemplatesTeachTheShapeRule`)
      and register its blocks in `skills/tests/test_mutation_harness.py`
      (registration is per file and a new `assertIn` in an already-registered
      file still needs its own entry — LESSONS M53/M54), then run the three
      suites and `cairn_validate`.

## Work log

- 2026-07-18: created by /milestone-plan. Promoted from the "References note-template vocabulary" candidate; the plan gate superseded that row's list-the-phrases framing with a shape rule after investigation found M83's parser is generative, and folded in the live pairing-test gap (instantiated templates classify `ambiguous` / `exempt`).
- 2026-07-18: T1 baseline via the real `_last_verified` — unchosen: source `ambiguous`, synthesis `exempt`; each chosen alternative: source `ok`/`never`, synthesis `ok`/`exempt`/`ok`, all as their wording intends; all four shipped forms `ok`. The templates are correct once a choice is made; only the unchosen form collapses.
- 2026-07-18: T2 wrote the shape rule into both templates' comment headers (not body prose — M80 F2: a page authored from the template must not commit a sentence about a test guard). Both templates now state the three-way shape, name the verb set and clause-scoped negation, and say the alternatives are examples rather than the accepted list. Three suites + validate exit 0.
- 2026-07-18: T3 added `TestEachSanctionedStatusClassifies` (3 tests) — it selects each alternative the `<a | b | c>` field offers, builds a page from it, and asserts the real `_last_verified` state against an INTENT table, so a new alternative matching no entry fails rather than passing unexamined. Landed in a new class rather than extending `TestTemplateProducesAValidPage`, whose subject is the existence checkers; falsified by mutation (swapping one alternative for unreadable wording failed all 3, restored green).
- 2026-07-18: T4 added `TestUnlistedShippedFormsSatisfyTheShapeRule` (3 tests) — the four unlisted forms each classify `ok`, each is still written by a committed page (so the list cannot go fictional), and none is offered by a template (the class premise). Refactored the shared helpers into `StatusClassificationMixin` first: the class had inherited the T3 TestCase, which re-ran its 3 tests under the child's name. Falsified by mutating a shipped page's status prefix. Skills 369 (was 363), scripts 174, hooks 72, validate all exit 0.
- 2026-07-18: T5 minor amendment — the task presupposed the prose-guards existed, but T2 had written the shape rule with nothing asserting it, so AC1 had no evidence and the rule was silently deletable; T5 now authors the guard as well as registering it. Added `TestTemplatesTeachTheShapeRule` (4 tests) and 8 harness entries, one per (test, template) pair so blanking either template's copy fails. Reflowed the verb set onto one physical line first (M74/M76: a label→SET guard pins label and members together). Skills 373, scripts 174, hooks 72, validate all exit 0.

## Decisions

## Review
