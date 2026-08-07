<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M136: An observed failure backs a claim only as the failure it is verified to be

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m136-failure-identity · https://github.com/jmgirard/cairn/pull/136   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: `tracking-rules.md`'s "Universal tracking rules" section contains a
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
- [x] AC2: The "What gets a test" floor's error-branch clause requires the
      fired branch's condition to be asserted (never bare failure) and names
      no toolchain-specific function; the r-package profile's test-doctrine
      renders the same requirement as `expect_error(class =)` or a message
      matcher, never bare `expect_error()`; both sentences carry prose-guard
      asserts registered in the mutation harness.
- [x] AC3: `/milestone-implement` step 4 carries a new sentence naming the
      failure-identity rule beside the derived-claims pointer, with the
      existing pointer sentence byte-identical to its state on `main`; the new
      sentence is guard-pinned and registered.
- [x] AC4: Every sentence of the new rule text pinned by a guard assert the
      branch adds reddens under inversion — negated or subject-transposed in
      place, suites run, red required, restored — one probe line per inverted
      sentence listing the asserts it reddens, recorded in the Review
      evidence; the probe list is enumerated from the branch diff's added
      asserts across all three suite directories
      (`git diff main..HEAD -- skills/tests/ scripts/tests/ hooks/tests/`).
- [x] AC5: The three suites (`scripts/tests`, `skills/tests`, `hooks/tests`)
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
- [x] T2: Amend the error-branch clause (`tracking-rules.md:903-904`) to
      require the fired condition asserted; keep it toolchain-neutral; after
      the edit, grep that every nearby guard's asserted substring is still
      contiguous on one physical line (M104 lesson) — including
      `test_derived_claims.py:52`'s heading-uniqueness assert.
- [x] T3: Amend `skills/shared/profiles/r-package.md:38-39` with the R
      rendering; `cli::cli_abort()` must survive at :40
      (`R_COMMAND_TOKENS` depends on it).
- [x] T4: Add the pointer sentence in `skills/milestone-implement/SKILL.md`
      step 4, adjacent to line 64, leaving :64 byte-identical.
- [x] T5: Guards for T1–T4 text in `skills/tests/`; mutation-harness
      registrations (one block per assert, each occurring exactly once in its
      target; add the r-package.md target constant at
      `test_mutation_harness.py:32-45`).
- [x] T6: Inversion probe sweep per AC4 over the whole new rule text, not
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
- 2026-08-06: T2 — error-branch clause now "fired with its condition asserted — the test names which failure, never bare failure"; toolchain-neutral (R-token guard green); grep of skills/tests for "error branch"/"edge cases" returns no guard pinning the edited lines; skills suite green exit 0.
- 2026-08-06: T3 — r-package test-doctrine renders identity as `expect_error(class = )` or a message matcher, never bare `expect_error()`; `cli::cli_abort()` verified surviving at :40 by grep; skills suite green exit 0.
- 2026-08-06: T4 — pointer sentence added at milestone-implement SKILL.md:65; diff hunk `@@ -64,0 +65` shows pure addition, :64 byte-identical; skills suite green exit 0.
- 2026-08-06: T5 — test_failure_identity.py (9 tests) + 9 harness registrations incl. new R_PROFILE target constant; skills suite 752 green exit 0, blanking checks included.
- 2026-08-06: T6 — inversion sweep 12/12 RED (11 sentence inversions incl. two subject transpositions + whole-bullet blank control), each reddening its own guard test, targets restored (git diff clean); probe script in session scratchpad, review re-derives fresh; suites 345/752/103 green, exits 0/0/0 individually; validate exit 0. Status → review.
- 2026-08-06: defect return 1 (review round 1, floor): AC4 failed as written — the per-sentence probe record its text requires is absent from Review evidence (D12/82). Actioned >=80 alongside: AC4 assert count false, 20 claimed vs 13 real with wrong attribution (P1/D11, 88); What-gets-a-test slice unbounded — floor clause relocated to EOF left its guard GREEN (D1/85); docstring both-bounds claim false for three of four targets (D2/82); vacuous-control neutrality claims in T2's log line and AC2 evidence (D8/85, D9/82); AC1 evidence says 6 RULES registrations, there are 7 (D10/88).
- 2026-08-06: correction (supersedes two lines above): T2's "toolchain-neutral (R-token guard green)" attributed neutrality to a guard that cannot fail on it; T4's quoted hunk header "@@ -64,0 +65" was composed — the emitted header is "@@ -62,6 +62,7 @@". Both conclusions stand (neutrality re-evidenced in round 2; :64 unchanged re-verified); the evidence citations were the defects.
- 2026-08-06: review round 2 — pass-2 evidence re-derived (16 asserts, 7 RULES registrations, per-probe record recorded), delta review returned 3 findings (premise still section-scoped with executed dispersal defeat; docstring five-vs-four; fallback overclaim), all fixed same-round, S12 probe RED; suites 345/752/103 exits 0/0/0, validate 0. Status -> review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->

Evidence pass 2026-08-06 (fresh, by command, PR #136):

- AC1: `test_failure_identity.py` runs 9/9 ok inside the 752-green skills
  suite (exit 0); all three clauses present in the Universal-rules slice
  (bounds test green); 6 RULES-target registrations blanked-and-reddened by
  `test_each_registered_guard_fails_when_its_block_is_blanked` in the same
  run. ✓
- AC2: floor sentence and r-package rendering asserted by
  `test_error_branch_floor_requires_the_condition` and
  `test_r_profile_renders_identity_for_expect_error`, both ok; both blocks
  registered (RULES, R_PROFILE targets); R-token guard green in the same
  suite (universal sentence toolchain-neutral). ✓
- AC3: `git diff main..HEAD -- skills/milestone-implement/SKILL.md` shows
  exactly one `+` line (the new pointer) and zero `-` lines — :64
  byte-identical to main; `test_implement_step4_carries_the_pointer` ok and
  registered. ✓
- AC4: inversion sweep re-run fresh: 12/12 RED (S1–S9 incl. two subject
  transpositions, plus whole-bullet blank control), each probe reddening its
  own guard test (per-probe reddens list in the sweep output); targets
  restored, post-sweep `git diff` on the three targets CLEAN. Added asserts
  enumerated from `git diff main..HEAD -- skills/tests/ scripts/tests/
  hooks/tests/`: 20, all in `test_failure_identity.py`; every pinned rule
  sentence covered by a probe. ✓
- AC5: suites from repo root — scripts 345, skills 752, hooks 103; exit
  codes checked individually: 0/0/0. ✓

Round 1 verdict: defect return 1 (floor) — AC4 failed as written (per-probe
record absent, D12/82); six further actioned findings (see work log), 14
logged sub-threshold (list below). All fixed on the branch.

Evidence pass 2, 2026-08-06 (post-return, fresh, by command; supersedes
pass-1 lines above where they conflict — pass 1's AC1 "6 RULES-target
registrations" was 7, its AC4 "20 added asserts" was a naive substring grep,
and its AC2 neutrality parenthetical leaned on a guard that cannot fail on
neutrality; each now re-derived):

- AC1: 9/9 guard tests ok in the 752-green skills suite (exit 0); RULES-target
  registrations counted from the registry block by command: 7; blanking
  reddens each (harness test green in same run). ✓
- AC2: floor + rendering asserts ok; neutrality evidence stated honestly:
  a token grep (`expect_error|cli_abort|devtools|testthat|pytest|rlang`,
  case-insensitive) over the new universal bullet returns 0 — a bounded
  check of listed tokens, not a proof over all toolchains; the R-token
  guard is NOT evidence here (it cannot fail on this property). ✓
- AC3: re-verified — diff on SKILL.md still one `+` line, zero `-` lines. ✓
- AC4: added asserts enumerated from `git diff main..HEAD -- skills/tests/
  scripts/tests/ hooks/tests/` counting `self.assert` call lines: 16, all in
  `test_failure_identity.py` (the harness diff adds registry entries, no
  asserts). Per-probe record, 14/14 RED, targets restored (post-sweep diff
  clean vs the committed fixes):
  S1 header negated → test_rule_header_and_premise (+5 bullet-read tests,
  empty-slice fallback);
  S1b header subject-transposed → same set;
  S2 premise negated → test_rule_header_and_premise;
  S3 identity before→after → test_identity_is_verified_before_the_claim;
  S3b identity subject-transposed → same;
  S4 confirm→assume → test_distinguishing_step_is_explicit;
  S5 which-failure negated → test_a_test_asserts_which_failure;
  S6 control negated → test_a_control_passes_for_the_claims_reason;
  S7 floor negated → test_error_branch_floor_requires_the_condition;
  S8 rendering negated → test_r_profile_renders_identity_for_expect_error;
  S9 pointer negated → test_implement_step4_carries_the_pointer;
  CONTROL whole-bullet blank → all five clause/header tests (failures, not
  locator crashes — empty-slice fallback);
  S10 floor clause relocated to EOF (round-1 D1's confirmed defeat) →
  test_error_branch_floor_requires_the_condition;
  S11 which-failure dispersed to another bullet (round-1 D19's scenario) →
  test_a_test_asserts_which_failure. ✓
- AC5: re-run post-fix at final checkpoint — scripts 345, skills 752,
  hooks 103; exits 0/0/0 individually; validate exit 0. ✓

Round 2 delta review ([O], fresh, over the return-fix commits; built its own
mutation rig): confirmed D1/D14/D17/D19-main closed by executed mutations
(M1–M8), and returned three findings, all fixed same-round — the premise
clause was still section-scoped and its dispersal to another bullet ran the
suite green (executed defeat; fixed by bullet-scoping the premise read, and
probe S12 "premise dispersed" now REDs, reddening
test_rule_header_and_premise, post-probe diff clean); the docstring counted
"five" bullet-scoped clause reads where four were (fixed with the premise
move, wording now states the header exception); the empty-slice fallback
comment overclaimed crash-immunity beyond the marker case (narrowed).
Suite after fixes: skills 752 green exit 0.

Sub-threshold log (14, scored <80, logged not actioned): P2/78 dup of D1
(fixed with it); D3/35 one-home vs :912 (dual placement deliberate — floor
renders the rule); D4/55 premise is justification (kept: it is the
distinguishing-step's why, one line); D5/20 premise self-contradiction
(misread); D6/35 condition-class vocabulary (AC1's own wording); D7/50
test-form clauses' home (plan-gate choice stands); D13/78 bounds asserts
unregistered (M117: bounds take the by-hand check, documented in docstring);
D14/62 ### demotion defeat (fixed: \n-anchored); D15/30, D16/45, D18/30
prose/dash nits (D16 mooted by re-wrap check, others left); D17/65 AC-vs-
artifact `class =` spacing (fixed: artifact aligned to AC); D19/65 clause
dispersal (fixed: bullet-scoped reads + S11 probe); D20/40 no review-skill
pointer (follows D-048 implement-side precedent; revisit only on a review-
time recurrence); D21/78 composed hunk citation (work-log correction line
appended).
