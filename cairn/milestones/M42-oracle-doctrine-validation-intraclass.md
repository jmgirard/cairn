<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M42: Oracle-doctrine validation against intraclass

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M41   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m42-oracle-doctrine-validation-intraclass   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Validate cairn's D-024 oracle-type doctrine and the two deferred oracle candidates
against intraclass's real oracle system — the practice cairn's doctrine descends
from — recording fit findings that sharpen (but do not yet build) the registry.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** classify intraclass's 34 `data-raw/oracle-*.R` scripts + `PRINCIPLES.md` #1
against cairn's D-024 doctrine (frozen/live/invariant/closed-form vocabulary, the
≥2-independent-types bar, the reproducibility hard-stop); assess whether the two
deferred candidates — the `ORACLES.md` registry and the R-provenance guard — fit
intraclass's actual practice; record the assessment in a cairn reference file and
sharpen the two candidate rows with the evidence; fix in cairn any concrete defect
the assessment exposes in the Validation-doctrine text (guard-tested).

**Out:** building `ORACLES.md` as a cairn tracking file (the deferred candidate,
entangled with toolchain-profiles — this milestone informs it, does not build it);
building the R-provenance guard test (the deferred R-profile-slot candidate); any
change to the intraclass repo (read-only assessment); promoting either candidate
to a `planned` milestone (that is a later plan-gate decision, fed by these findings).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: Every `data-raw/oracle-*.R` script in intraclass is classified into one
      of cairn's four oracle types (frozen/live/invariant/closed-form) in a table in
      the findings file, with a per-type count; any script fitting no type is flagged
      as a doctrine gap. (Evidence: the findings table + the script list it covers.)
- [ ] AC2: intraclass `PRINCIPLES.md` #1 (≥2 independent oracle types) is compared
      against cairn's D-024 ≥2-types bar, with an explicit agree/diverge verdict
      citing `PRINCIPLES.md` #1 and the tracking-rules "Validation doctrine" section.
- [ ] AC3: Each of the two deferred candidates (ORACLES.md registry; R-provenance
      guard) is assessed for fit against intraclass's real system with a
      keep-deferred / revise / promote verdict, and its ROADMAP candidate row is
      updated to cite this evidence. (Evidence: the diff of the two candidate rows +
      the findings section.)
- [ ] AC4: Any concrete defect the assessment exposes in cairn's Validation-doctrine
      text (D-024) is fixed this milestone with a `test_oracle_doctrine.py` update
      that fails before the fix; if none is found, that null result is recorded in
      the findings file.
- [ ] AC5: cairn's own guard-test suite passes
      (`python3 -m unittest discover -s scripts/tests` and the `skills/tests`
      suite). (R gates are waived here — cairn is a plugin, not an R package.)

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Read intraclass's 34 `data-raw/oracle-*.R` scripts (+ the `tests/testthat`
      oracle tests that assert against them) and record what each oracle actually is
      — its source and how it is reproduced.
- [x] T2: Classify each script against the four cairn oracle types in a table with
      per-type counts; flag any that fit no type; compare intraclass `PRINCIPLES.md`
      #1 to cairn's ≥2-types bar with an agree/diverge verdict. Write both into a new
      `references/oracle-doctrine-intraclass-notes.md` (declares its own scope).
- [x] T3: Assess the two deferred candidates against the real system — does the
      `ORACLES.md` registry shape (ID, type, asserting test:line, source, provenance)
      match intraclass's oracles; does the `provenance`-attr + guard-test convention
      match intraclass's fixture practice — with a keep-deferred/revise/promote
      verdict each; update the two ROADMAP candidate rows to cite the findings.
- [ ] T4: Fix any concrete Validation-doctrine defect the assessment exposes (with a
      `test_oracle_doctrine.py` update that fails first); if none, record the null
      result; run the cairn guard-test suites green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (oracle-doctrine reality-check; depends on M41 per user's follow-on choice).
- 2026-07-12: T1+T2 — read all 34 intraclass oracle scripts + test consumption; wrote references/oracle-doctrine-intraclass-notes.md. Finding: 31/34 use simulation-coverage (SC), an oracle mapping to NONE of cairn's four types (defining oracle for 21). PRINCIPLES.md #1 AGREES on the ≥2-types bar, DIVERGES on taxonomy (its cat (c) = SC, unnamed by cairn). intraclass's frozen-when-expensive / live-when-cheap split corroborates D-024.
- 2026-07-12: T3 — both deferred candidate rows → REVISE/keep-deferred. Registry: shape matches + earns keep at scale, but intraclass proves a distributed shape and it's downstream of the taxonomy fix. R-provenance guard: content corroborated, but mechanism varies across the two exemplars (attr+guard vs. embedded-fields-no-guard) → mandate content, leave shape to the repo.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
