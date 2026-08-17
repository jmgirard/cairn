<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M148: Review returns narrow the promises, never widen them

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m148-returns-narrow   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

After a defect return the amendment surface recommends narrowing or holding
the criteria set — widening is the user's explicit, never-recommended
decision — and the plan gate's full audit flags criteria whose promises bind
the verification instrument rather than the deliverable.

## Scope

**Surface tier: user-facing** — downstream cairn-tracked repos rely on the
amendment and audit conduct these skills ship (the motivating defect was
measured in intraclass M123: three defect returns, the amendment after
return 2 widening the criteria set into instrument-binding clauses that
produced return 3 and a thrash firing; hosted per D-098, D-090/D-108's door
cleared by its trigger clause).

**In:** the return-adjacent amendment direction rule (`/milestone-implement`
step 6); the instrument-binding question in the full criteria audit
(`/milestone-plan` step 3); the step-6 re-entry clarification, absorbing the
re-entry half of the "Stakes-tier follow-through" candidate row; one
D-entry; a restatement sweep.

**Out:** extending the instrument question to the reduced audit → the
D-entry's falsifier clause decides re-entry; tier-recording support (the
candidate row's other half) → stays parked as the trimmed row; any prose
guard over the new rules → none owed (D-109).

## Acceptance criteria

- [ ] AC1: `/milestone-implement` step 6's substantive-amendment path states
      the return-adjacent direction rule: on a milestone whose work log
      records one or more defect returns, a proposed amendment that widens
      the criteria set — adding an acceptance criterion, or extending an
      existing criterion's promise to a property or domain it did not
      previously bind — is presented with narrowing or holding the criteria
      set as the recommended option and the widening as an explicitly
      non-recommended alternative, the motivating finding offered a
      follow-up home (candidate row or split milestone) instead; a widening
      adopted at the user's selection records a work-log line naming each
      criterion widened or added; amendments executing a
      widening-test-reclassified return are carved out by name — D-101's
      inadmissibility governs them unchanged. Verified by reading the
      shipped step-6 text for each named element.
- [ ] AC2: `/milestone-plan` step 3's criteria audit asks, in full mode (per
      the D-entry AC4 appends; the reduced form stands at its two
      questions), of each criterion whether its promise states a property of
      the milestone's deliverable or a property of an instrument that
      verifies it (a test harness, a floor, a plant matrix, a checker's own
      prose among others); a criterion binding an instrument property is a
      finding, disposed at the gate like the audit's other findings — the
      instrument property moved to tasks or gate procedure, or the criterion
      narrowed to the deliverable property it certifies. Verified by reading
      the shipped step-3 text.
- [ ] AC3: step 6's re-entry sentence states that amended
      acceptance-criterion wording is asked every question the assigned mode
      asks — the proportionality question and, in full mode, the instrument
      question included. Verified by reading the shipped step-6 text.
- [ ] AC4: one appended `DECISIONS.md` entry records both rules with their
      trigger (intraclass M123 as the Scope states), its heading naming
      "annotates D-101" and "narrowly supersedes D-111's full-mode question
      enumeration"; shown verbatim in chat before its commit. Verified: the
      entry is present and its heading carries those two relations.
- [ ] AC5: a recorded grep sweep — command verbatim in the work log — over
      the repo's markdown for restatements of the two edited doctrine sites
      (the step-6 amendment protocol; the criteria-audit question list)
      returns hits each dispositioned in the work log as updated or
      correct-as-written; the promise quantifies over the sweep's hits.
- [ ] AC6: both gating suites (`python3 -m unittest discover -s
      scripts/tests`; same for `hooks/tests`) and `cairn_validate` pass on
      the branch.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T4
- AC5 → T3
- AC6 → T5

## Tasks

- [x] T1: Edit `skills/milestone-implement/SKILL.md` step 6: add the
      return-adjacent direction rule (AC1's elements, D-101 carve-out
      included) and clarify the re-entry sentence (AC3); cite
      `/milestone-plan` step 3 rather than restating its question list.
- [x] T2: Edit `skills/milestone-plan/SKILL.md` step 3: add the
      instrument-binding question to the full audit's question list with
      AC2's disposal shape; leave the reduced-mode sentence untouched.
- [x] T3: Run AC5's sweep, disposition every hit; trim the "Stakes-tier
      follow-through" candidate row to its tier-recording remainder,
      lineage noted.
- [ ] T4: Draft the D-entry (AC4's relations), preview verbatim in chat,
      append to `cairn/DECISIONS.md`.
- [ ] T5: Run both gating suites + `cairn_validate`; hand-run `python3 -m
      unittest discover -s skills/tests`, dispositioning every red (fixture
      updated to the shipped bytes / intentional note / pre-existing note)
      per D-109.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046). -->

- 2026-08-17: created by /milestone-plan (motivated by intraclass M123's three-return thrash; cross-repo surfacing hosted per D-098; D-090/D-108's door cleared by its trigger clause — a defect in shipped skill conduct measured in a user repo).
- 2026-08-17: criteria audit ran in FULL mode (user-facing tier): 7 findings; 5 fixed into the criteria before the gate (D-101 carve-out added to AC1; the skills/tests promise narrowed off the instrument into T5 after the audit flagged it under AC2's own rule; AC2 now cites the appended D-entry; "amends" replaced with supersession vocabulary; the heading-relation set named); 2 went to the gate and resolved full-mode-only and absorb-the-row-half.
- 2026-08-17: plan gate chose a user-decidable, never-recommended widening over D-101-style flat inadmissibility for voluntary post-return widenings because genuine scope discovery can legitimately widen and user overrides are logged, never resisted; falsified by a user-approved widening amendment producing a further return of the same shape.
- 2026-08-17: plan gate chose full-mode-only for the instrument question over both modes because D-111 had just descoped the reduced audit and no internal-tier instance of the defect is on record; falsified by an internal-tier milestone shipping an instrument-binding criterion that costs a defect return.
- 2026-08-17: plan gate chose one milestone over a split despite the goal-sentence "and" tripwire because the combined diff is a few sentences in two skill files plus one D-entry; falsified by review returning on one rule's surface while the other ships clean.
- 2026-08-17: plan gate chose absorbing the re-entry half of the stakes-tier candidate row over leaving it parked because T1 opens that exact sentence; falsified by the clarified re-entry itself costing an amendment return.
- 2026-08-17: T1 done — step 6 gains the return-adjacent direction rule (D-101 carve-out by name) and the re-entry sentence now says every question in the assigned mode, proportionality and full-mode instrument included; both gating suites green (308 + hooks OK). Question gate skipped: plan gate settled every open choice, no tripwire tags.
- 2026-08-17: T2 done — full audit gains the instrument-binding question with AC2's disposal shape (move to tasks/gate procedure, or narrow to the deliverable property); reduced-mode sentence untouched; both suites green.
- 2026-08-17: T3 sweep — `grep -rniE 'criteria audit|satisfiability|amendment protocol|amendment gate|amend-via-gate|proportionality|instrument question' --include='*.md' .` — dispositions: hits in DECISIONS.md, milestones/archive/, reviews/archive/, legacy/, and CHANGELOG.md are correct-as-written (history, never edited); tracking-rules/template ownership-vocab hits and the brief/review step-6 pointers are correct-as-written (they cite the site, never restate it); references-page hits (self-verification-ledger, m127-ac1-ledger, INDEX) correct-as-written (dated first-hand records); README.md:12 correct-as-written (still true of the stakes-scaled audit); milestone-plan/implement hits are the edited sites themselves; updated: the reduced-audit drop-list enumeration now names the instrument question (the operative two-question clause untouched); updated: the stakes-tier ROADMAP row trimmed to its tier-recording remainder, lineage noted in the row.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. EXEMPT from the 150-line cap (D-074). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->
