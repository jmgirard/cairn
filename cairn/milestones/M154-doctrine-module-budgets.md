<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M154: The maturation exit's doctrine modules gain budgets

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1, GP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m154-doctrine-module-budgets   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A lesson family graduating through the maturation exit lands in a module with
a stated size budget the repo's hygiene passes read — closing the gap
circumplex M104 measured, where the exit's output (`cairn/test-craft.md`)
stood outside every cap until a same-day hand repair (circumplex aef79279).
Surface tier: user-facing — the deliverable is shipped skill prose adopting
repos consume.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** one budget clause in the tracking-rules maturation exit; the two
hygiene-pass sites D-119 names read module header budgets; a retrofit header
for `skills/shared/records-hygiene.md`; a D-entry annotating D-055 that
records D-108's door-walk (trigger: the shipped hygiene step stamps "caps ok"
while blind to the file its own exit creates, measured in circumplex, hosted
per D-098); the candidate row absorbed.

**Out:** pointer/reachability verification at graduation → unmandated until a
pointer actually breaks (gate choice 2026-08-22); mechanizing the check in
`cairn_validate` → refused at this gate (D-119's prose precedent; the
checker-regress rule); location doctrine → already owned by
tracking-rules:127-128 and the LESSONS-header pointer convention.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: The maturation exit in `skills/shared/tracking-rules.md`
      ("Retiring a lesson that no longer earns its line") states that the
      graduating milestone writes the module's line and byte budget into its
      own header, set from the graduated size plus stated headroom; the
      shipped clause itself states the budget is hand-read with `wc -l -c`
      at the repo's hygiene passes and covered by no validator. Evidence:
      the shipped sentence(s) quoted verbatim from the merged file.
- [ ] AC2: Both hygiene-pass sites D-119 names — `/milestone-review`'s
      post-merge hygiene step and `/milestone`'s health audit — name
      doctrine-module header budgets in their hand-run size checks, read
      with `wc -l -c`, beside the `ROADMAP.md`/`LESSONS.md` byte budgets
      they already carry. Evidence: the shipped sentences quoted verbatim
      from both merged files.
- [ ] AC3: `skills/shared/records-hygiene.md`'s header states its own line
      and byte budget, set from its measured size (38 lines / 2,193 bytes
      on 2026-08-22) plus headroom, and the file measures under both stated
      figures at the merge commit. Evidence: the header sentence quoted
      verbatim plus the `wc -l -c` reading at merge.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Add the budget clause to the maturation exit at
      `skills/shared/tracking-rules.md:120-128`: the graduating milestone
      states the module's line and byte budget in the module header (set
      from the graduated size plus stated headroom), hand-read with
      `wc -l -c` at hygiene passes, covered by no validator.
- [ ] T2: Wire both hygiene sites: the post-merge hygiene hand-check
      sentence at `skills/milestone-review/SKILL.md:336-338` and the health
      audit's byte-budget line at `skills/milestone/SKILL.md:58` each name
      doctrine-module header budgets, read `wc -l -c`.
- [ ] T3: Retrofit `skills/shared/records-hygiene.md` with a header budget
      (proposed < 45 lines / < 4,000 bytes from 38 / 2,193 measured
      2026-08-22 plus roughly one entry of headroom; implement fixes the
      final figures against the file as merged — headroom must exceed the
      header sentence's own addition, per the audit's round-2 note).
- [ ] T4: Append the D-entry annotating D-055 (the maturation exit gains
      the budget clause), recording D-108's trigger as met (hygiene-step
      blindness to its own exit's output, measured in circumplex,
      hosted per D-098) — the D-119 door-walk shape.
- [ ] T5: Re-seed the three rulebook-mass pins (M149 lesson: the
      `/milestone` skill line, `skills/tests/test_cost_audit_line.py:67`,
      `skills/tests/test_mutation_harness.py:117`); run both gating suites
      and hand-run `skills/tests` (M148/M56 lessons — edits land near
      guarded prose regions); absorb the ROADMAP candidate row with lineage
      noted here.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-08-22: created by /milestone-plan, promoting the 2026-08-22 candidate row (circumplex M104 review) at the user's direction; the row's wait-for-drift promotion condition was weighed and overridden — the gap is structural (every future graduation in any repo reproduces it) and circumplex's fix covered one module only.
- 2026-08-22: plan gate chose walking D-108's door with the trigger stated over leaving the row parked because the shipped hygiene step's blindness to its own exit's output is a shipped-behavior defect on D-119's pattern, measured in circumplex and hosted per D-098; falsified by a reading that classes hygiene-stamp blindness as apparatus-coverage, which D-098 bars from a milestone.
- 2026-08-22: plan gate chose retrofitting records-hygiene.md over forward-binding-only because otherwise neither hygiene site reads any budget until the next graduation; falsified by the retrofitted header drifting unread across consecutive hygiene passes.
- 2026-08-22: plan gate chose the budget-only clause over budget-plus-pointer-check because pointer breakage is unobserved and each rulebook sentence is carried in the three mass pins; falsified by a graduated module going unreachable through a broken LESSONS pointer.
- 2026-08-22: criteria audit ran in full mode ([O] fresh reader, two rounds): round 1 returned 9 findings — 3 wording fixes applied (validator-clause scoping, `wc -l -c` in the check AC2 names, both D-119 hygiene sites in scope), 2 became gate questions (D-108 door, retrofit), rest informational; round 2 re-read the final wording above and returned two notes — the door-walk must be on the record (it is: Scope, T4, this log) and AC3's headroom must exceed the header's own addition (T3 carries it) — no criterion defects.

- 2026-08-22: T1 — budget clause added to the maturation exit (tracking-rules.md:124-126); scripts/hooks/skills suites all exit 0.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->
