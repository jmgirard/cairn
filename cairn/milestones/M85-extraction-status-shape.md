<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M85: Extraction-status shape — the templates teach what the classifier reads

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m85-extraction-status-shape` · https://github.com/jmgirard/cairn/pull/84   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] Both templates state the readable-status shape — a verification claim, a
      date, or an explicit nothing-to-re-verify — as a rule an author can apply
      to wording the template does not list, not as an enumeration of accepted
      phrases.
- [x] The pairing test selects each alternative offered by each template's
      `Extraction:` field and asserts the state the real
      `cairn_validate._last_verified` returns for it; every sanctioned
      alternative classifies as its wording intends (no `ambiguous`, no
      `unrecognized`).
- [x] A guard proves the whole-template (unchosen) form is what collapses:
      the source template reads `ambiguous` and the synthesis template reads
      `exempt` before a choice is made, so the per-choice assertions are shown
      non-vacuous. Paired with a positive signal that the classifier path
      actually ran, per the M84 lesson.
- [x] The four forms this repo's own pages write that neither template lists —
      `verified at ingestion`, `partly verified at ingestion`, `read against
      the … artifacts at assessment time`, `verified by live probe DATE` — each
      satisfy the stated shape rule, demonstrated by a test that classifies
      them through the real classifier.
- [x] `verify` clean per `cairn/PROFILE.md` (the three `python3 -m unittest`
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
- 2026-07-18: review — 3 lenses + scorer. Two lenses clean; the diff-bug lens found 3, scored 93/80/62, all reproduced independently and all fixed on the branch (F1 false coverage introduced in a pre-existing guard, F2 the taught rule wrong about `unverified`, F3 an exact-equality test not enforcing its docstring). Each fix falsified by mutation after landing. Skills 374, scripts 174, hooks 72, validate exit 0; all 5 criteria ticked against recorded evidence.

## Decisions

## Review

**Reviewed 2026-07-18 · PR #84 · no CI on this repo (LESSONS M16).**

**Criterion evidence** (all fresh, by command, from the repo root):

- **AC1** — `TestTemplatesTeachTheShapeRule`, 4 tests, exit 0. Both templates
  state the three-way shape, name the verb set on one physical line with its
  label, mark the alternatives as examples rather than the accepted list, and
  state the consequence (an unreadable status is reported, not assumed
  verified). Falsified: deleting the rule line from the **synthesis** template
  alone failed the guard, proving the per-template registration is not carried
  by the source template's copy.
- **AC2** — `TestEachSanctionedStatusClassifies`, 3 tests, exit 0. All five
  offered alternatives (2 source, 3 synthesis) are selected in turn and
  classified by the real `cairn_validate._last_verified`: `ok`/`never` and
  `ok`/`exempt`/`ok`, each matching its INTENT entry; none classifies
  `ambiguous` or `unrecognized`. Falsified: swapping one alternative for
  unreadable wording (`reviewed at ingestion`) failed all 3.
- **AC3** — `test_the_unchosen_template_is_what_collapses` asserts the
  unchosen instantiated source template is `ambiguous` and the synthesis
  template `exempt` — positive equality assertions on named states, not
  absence-asserts. The positive signal the M84 lesson requires is
  `assertIn(state, STATES)` in `classify()`, which fails on a crash producing
  no verdict rather than passing vacuously.
- **AC4** — `TestUnlistedShippedFormsSatisfyTheShapeRule`, 3 tests, exit 0.
  Each of the four forms classifies `ok` through the real classifier; each is
  still written by a committed page; none is offered by a template. Falsified:
  rewording `desktop-toc-mechanism.md`'s status prefix failed the
  stale-list guard.
- **AC5** — skills 373 (was 363 on `main`), scripts 174, hooks 72; each
  discovered from the repo root and each exit code read individually, never
  piped (LESSONS M56/M65). `cairn_validate` exit 0, 15 PASS + 6 advisories all
  `OK`.

**Consistency gate.** `cairn_validate` exit 0. Profile is `generic`, whose
`consistency-gate` slot names no toolchain checks, so that half is a clean
no-op. `Principles touched: —`, so `cairn_impact` was not run. Mutation
harness: 191 entries total, 10 added here — one per (test, template) pair.

**Independent review — 3 lenses + scorer.** Blame-history: no findings (it
confirmed the M80 F2/F3 boundaries hold, `cairn_validate.py` has zero diff so
M83's scoped-out territory was not re-entered, and the verb-set reflow preceded
any harness entry referencing it). Prior-PR: no findings; no inline PR-comment
evidence exists for these files across 11 merged PRs, so that half no-opped as
designed, and it mined the archived Review paragraphs instead. Diff-bug lens:
three findings, all reproduced independently before triage.

- **F1/93 — fixed.** The new header sentence naming the verb set added a
  SECOND occurrence of `unverified` to `source-note.md`, degrading the
  pre-existing `test_unverified_extraction_is_an_expressible_state` (a bare
  `assertIn("unverified", <whole template>)`) into false coverage: the
  `| unverified — first pass, …` alternative could be deleted outright and the
  guard stayed green, where on `main` that deletion failed it. This milestone
  introduced the regression, and it is M80's F3/65 trap one word over.
  Re-anchored the guard on the `Extraction:` field line via `extraction_line()`;
  deleting the alternative now fails it with the header prose still present.
- **F2/80 — fixed.** Both templates taught a rule the classifier does not
  implement: they listed `unverified` among the four affirmative verbs and then
  said a verb "counts as negated when a negator precedes it in that same
  clause". `unverified` is `_UNVERIFIED`, not `_VERIFY_VERB`, and
  `_clause_claims` adds `never` for it unconditionally — so
  `Extraction: unverified pending a second pass`, with no negator anywhere,
  classifies `never`, the opposite of what the taught rule implies. Because the
  rule IS AC1's deliverable and was already pinned by a guard and two registry
  entries, the error was locked in on both templates. Removed `unverified` from
  the verb list and stated the exception explicitly, with a new guard
  (`test_each_template_marks_unverified_as_self_negating`) and two more registry
  entries. Verified after: all four listed verbs now behave exactly as stated
  (bare → `verified`, negated → `never`).
- **F3/62 — below threshold, fixed anyway.** `test_no_unlisted_form_is_offered_by_a_template`
  compared a whole `FORMS` string against the offered alternatives by exact
  equality, so only a byte-exact paste tripped it; a shortened variant
  (`verified at ingestion — full source read`) passed, though the docstring
  claimed the premise was enforced. The sibling INTENT table did fail loudly on
  the same input, so the premise was defended — by a different test. Actioned
  despite the score because the fix is one line and the alternative was leaving
  an overclaiming docstring in place. Now matched on the form's distinguishing
  prefix; the variant that slipped through is caught.

Nothing was logged-and-dropped. Each fix was falsified by mutation after
landing, not accepted on inspection. Re-verified: skills 374, scripts 174,
hooks 72, `cairn_validate` — each exit 0.

**One judgment call left visible for the gate.** `TestUnlistedShippedFormsSatisfyTheShapeRule`
asserts against this repo's own `cairn/references/` pages, so a plugin test
reads repo content. There is precedent (`TestBackfilledPages`), and it is what
stops the four-form list going fictional, but it is the seam most likely to
behave differently in an adopting repo.
