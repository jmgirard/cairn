<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M136: An observed failure backs a claim only as the failure it is verified to be

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m136-failure-identity   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Close the confounded-measurement class where an execution's observed failure
is read as evidence about the behavior under test when it is an artifact of
malformed inputs or an unmet precondition — and the test pinning the claim
passes its control for an unrelated reason.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a failure-identity conduct rule in `tracking-rules.md` "Universal
tracking rules", adjacent to the derived-claims rule (M134) it extends —
step-0 checked 2026-08-06: derived-claims covers deriving from an execution's
observed output; the identity of an observed *failure* is covered nowhere.
Plus: the "What gets a test" error-branch clause gains the identity
requirement (toolchain-neutral by stated intent — the R-token guard would not
catch `expect_error` leaking in); the r-package profile's test-doctrine gains
the R rendering (`expect_error(class =)` or a message matcher, never bare
`expect_error()`); `/milestone-implement` step 4 gains a new adjacent pointer
sentence (line 64 stays byte-identical — it is pinned verbatim by
`test_derived_claims.py:83-88` and a mutation-registry block). Guards +
mutation-harness registrations (new target constant for
`skills/shared/profiles/r-package.md`) + inversion probes.

**Trigger (D-090/D-098):** a defect in shipped skill behavior, measured in a
user repo — tidymedia M54 review 2: a wrong argument name produced a
jobs-schema error misread as blame-attribution behavior, propagating a false
claim into NEWS, that repo's ROADMAP, and a vacuous control test
(`test-nvenc.R:147` passed `inset` for `overlay`, so the "control" passed on
a schema error independent of the behavior claimed). Hosted here per D-098:
the surfacing milestone lives in another repo.

**Out:** a recorded per-claim verification line (evidence bookkeeping) —
declined at the 2026-08-06 plan gate, conduct-only like the sibling rules;
re-raise as a candidate only if review misses recur. Any change to the
review fan-out or scorer → none planned (D-090's door). tidymedia's own M54
repairs → tidymedia's milestone.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `tracking-rules.md`'s "Universal tracking rules" section contains a
      failure-identity rule stating all three clauses: (i) a claim attributing
      behavior to an artifact on the evidence of an observed failure verifies
      the failure's identity — condition class, message, or signaling site —
      against the failure the claim is about, before the claim is written;
      (ii) the distinguishing step is explicit — the inputs are confirmed to
      reach the behavior under test, by succeeding when the condition under
      test is removed or by checking the input contract against the artifact's
      own signature; (iii) a test asserting a failure asserts which failure,
      never that some failure occurred, and a discriminating test's passing
      control is shown to pass for the claim's reason. Each clause is pinned
      by a prose-guard assert in `skills/tests/` registered in the mutation
      harness, and blanking each registered block reddens its guard.
- [ ] AC2: The "What gets a test" floor's error-branch clause requires the
      fired branch's condition to be asserted (never bare failure) and names
      no toolchain-specific function; the r-package profile's test-doctrine
      renders the same requirement as `expect_error(class =)` or a message
      matcher, never bare `expect_error()`; both sentences carry prose-guard
      asserts registered in the mutation harness.
- [ ] AC3: `/milestone-implement` step 4 carries a new sentence naming the
      failure-identity rule beside the derived-claims pointer, with the
      existing pointer sentence byte-identical to its state on `main`; the new
      sentence is guard-pinned and registered.
- [ ] AC4: Every sentence of the new rule text pinned by a guard assert the
      branch adds reddens under inversion — negated or subject-transposed in
      place, suites run, red required, restored — one probe line per inverted
      sentence listing the asserts it reddens, recorded in the Review
      evidence; the probe list is enumerated from the branch diff's added
      asserts across all three suite directories
      (`git diff main..HEAD -- skills/tests/ scripts/tests/ hooks/tests/`).
- [ ] AC5: The three suites (`scripts/tests`, `skills/tests`, `hooks/tests`)
      pass from the repo root with each suite's exit code checked
      individually.

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence. -->

- AC1 → T1, T5
- AC2 → T2, T3, T5
- AC3 → T4, T5
- AC4 → T6
- AC5 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Author the failure-identity bullet in `tracking-rules.md` "Universal
      tracking rules" (heading at :209), each clause on its own single
      physical line (M134 shape, :233-234); anchor guard text by copying the
      landed bytes, never the draft.
- [ ] T2: Amend the error-branch clause (`tracking-rules.md:903-904`) to
      require the fired condition asserted; keep it toolchain-neutral; after
      the edit, grep that every nearby guard's asserted substring is still
      contiguous on one physical line (M104 lesson) — including
      `test_derived_claims.py:52`'s heading-uniqueness assert.
- [ ] T3: Amend `skills/shared/profiles/r-package.md:38-39` with the R
      rendering; `cli::cli_abort()` must survive at :40
      (`R_COMMAND_TOKENS` depends on it).
- [ ] T4: Add the pointer sentence in `skills/milestone-implement/SKILL.md`
      step 4, adjacent to line 64, leaving :64 byte-identical.
- [ ] T5: Guards for T1–T4 text in `skills/tests/`; mutation-harness
      registrations (one block per assert, each occurring exactly once in its
      target; add the r-package.md target constant at
      `test_mutation_harness.py:32-45`).
- [ ] T6: Inversion probe sweep per AC4 over the whole new rule text, not
      only the diff's phrases (M121 lesson); run the three suites from the
      repo root, exit codes checked individually.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-06: created by /milestone-plan, from tidymedia M54 review 2's confounded measurement (cross-repo host per D-098; D-090 trigger stated in Scope).
- 2026-08-06: criteria audit ([O] fresh reader) returned four findings, all fixed at the gate — D-090 classification stated in Scope; AC4's diff pathspec widened to all three suite dirs and probe unit changed to per-sentence; AC3 recast as a new adjacent sentence leaving the doubly-pinned :64 untouched; AC2 gains the toolchain-neutral clause the R-token guard cannot enforce.
- 2026-08-06: plan gate chose the universal rulebook over the guard-doctrine module because the failure occurs at measurement time in any session and modules load only at guard-authoring (D-098's §6 observation); falsified by a confounded-measurement defect recurring in a repo with the rule live at session start.
- 2026-08-06: plan gate chose full scope (rule + test floor + R rendering) over conduct-rule-only because tidymedia showed both halves — the misread error and the vacuous control; falsified by the test-floor half producing gate friction without catching a vacuous test.
- 2026-08-06: plan gate chose conduct-only over a recorded per-claim verification line because the sibling rules are conduct-only and a per-claim record is standing bookkeeping in every repo; falsified by a review missing a confounded claim the record would have exposed.
- 2026-08-06: T1 — failure-identity bullet landed in tracking-rules "Universal tracking rules" after the derived-claims rule, five physical lines, three suites green (743/345/103, exits 0/0/0).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
