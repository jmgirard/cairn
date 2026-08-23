<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M154: The maturation exit's doctrine modules gain budgets

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1, GP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m154-doctrine-module-budgets · https://github.com/jmgirard/cairn/pull/155   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: The maturation exit in `skills/shared/tracking-rules.md`
      ("Retiring a lesson that no longer earns its line") states that the
      graduating milestone writes the module's line and byte budget into its
      own header, set from the graduated size plus stated headroom; the
      shipped clause itself states the budget is hand-read with `wc -l -c`
      at the repo's hygiene passes and covered by no validator. Evidence:
      the shipped sentence(s) quoted verbatim from the merged file.
- [x] AC2: Both hygiene-pass sites D-119 names — `/milestone-review`'s
      post-merge hygiene step and `/milestone`'s health audit — name
      doctrine-module header budgets in their hand-run size checks, read
      with `wc -l -c`, beside the `ROADMAP.md`/`LESSONS.md` byte budgets
      they already carry. Evidence: the shipped sentences quoted verbatim
      from both merged files.
- [x] AC3: `skills/shared/records-hygiene.md`'s header states its own line
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
- [x] T2: Wire both hygiene sites: the post-merge hygiene hand-check
      sentence at `skills/milestone-review/SKILL.md:336-338` and the health
      audit's byte-budget line at `skills/milestone/SKILL.md:58` each name
      doctrine-module header budgets, read `wc -l -c`.
- [x] T3: Retrofit `skills/shared/records-hygiene.md` with a header budget
      (proposed < 45 lines / < 4,000 bytes from 38 / 2,193 measured
      2026-08-22 plus roughly one entry of headroom; implement fixes the
      final figures against the file as merged — headroom must exceed the
      header sentence's own addition, per the audit's round-2 note).
- [x] T4: Append the D-entry annotating D-055 (the maturation exit gains
      the budget clause), recording D-108's trigger as met (hygiene-step
      blindness to its own exit's output, measured in circumplex,
      hosted per D-098) — the D-119 door-walk shape.
- [x] T5: Re-seed the three rulebook-mass pins (M149 lesson: the
      `/milestone` skill line, `skills/tests/test_cost_audit_line.py:67`,
      `skills/tests/test_mutation_harness.py:117`); run both gating suites
      and hand-run `skills/tests` (M148/M56 lessons — edits land near
      guarded prose regions). The candidate row stays on the ROADMAP and
      graduates at this milestone's post-merge hygiene (records-hygiene §1;
      the plan-time prune was reverted on main, f911896).

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
- 2026-08-22: T2 — module-budget reading added to the health audit (milestone/SKILL.md:58-63) and post-merge hygiene (milestone-review/SKILL.md:337-341); all three suites exit 0.
- 2026-08-22: reading records-hygiene.md for T3 surfaced that its §1 forbids the plan-time candidate-row prune the plan commit performed; the row was restored verbatim on main (f911896) with a promoted-to-M154 note, the branch rebased, and T5's wording amended (minor) — the row graduates at post-merge hygiene.
- 2026-08-22: T3 — records-hygiene.md retrofitted with a budget header: under 55 lines / under 4,000 bytes from the retrofitted 44 / 2,575 (the stated byte figure was stabilized against the M99 fixed-point by same-width digits); measures under both; all three suites exit 0.
- 2026-08-22: T4 — D-122 appended (annotates D-055; records D-108's trigger and the gate's rejected alternatives), previewed verbatim in chat; validate and all three suites exit 0.
- 2026-08-22: T5 — rulebook-mass pins re-seeded 413/37,567 → 415/37,807 (wc -l -m) at milestone/SKILL.md:94, test_cost_audit_line.py:67, test_mutation_harness.py:117; validate and all three suites exit 0; the candidate row stands for post-merge graduation.
- 2026-08-22: motivating measurements recorded so D-122's pointer resolves after the candidate row graduates (review F6): circumplex aef79279 measured cairn/test-craft.md at 26 lines / 7,293 bytes at graduation and capped it under 35 lines / 9,000 bytes; the candidate row's 5.7 KB was an earlier reading of the same file.
- 2026-08-22: review-gate fix batch (maintainer-approved dispositions): step-9 graduation now writes the budget header and the module read covers the minted module (F1/F9); Weight caps gains the module-budget bullet with the compress-or-retire remedy (F4/F5/F7); both hygiene sites scoped to "the repo's doctrine modules" (F3); validation-doctrine.md and migration-protocol.md retrofitted with headers, under 115 ln/8,000 B from 99/6,480 and under 200 ln/14,000 B from 185/11,924 (F2); stale pin comment fixed (F10); milestone/SKILL.md paragraph rewrapped (F14); DESIGN.md module list notes the budgets (F15); rulebook-mass pins re-seeded 415/37,807 → 418/38,127.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->

- 2026-08-22 AC1: PASS — tracking-rules.md:124-126 ships, verbatim: "The graduating milestone writes the module's line and byte budget into the module's own header — set from the graduated size plus stated headroom — hand-read with `wc -l -c` at the repo's hygiene passes and covered by no validator." The clause states the hand-read and the no-validator coverage itself, inside the maturation exit.
- 2026-08-22 AC2: PASS — milestone/SKILL.md:59-61 ships "and `wc -l -c` on each doctrine module against the budget its own header states (the maturation exit's rule)" inside the health audit's byte-budget hand check; milestone-review/SKILL.md:338-340 ships "and each doctrine module by hand against the budget its own header states (`wc -l -c`; the maturation exit's rule)" inside the post-merge hygiene verify sentence — both D-119 sites, beside the ROADMAP/LESSONS budgets.
- 2026-08-22 AC3: PASS — records-hygiene.md:8-12 header states "**under 55 lines and under 4,000 bytes**, set from the retrofitted size (44 lines / 2,575 bytes) plus roughly one section of headroom, hand-read with `wc -l -c` … covered by no validator"; fresh `wc -l -c` reads 44 / 2,575 — under both stated figures, and matching the stated size exactly (M99 fixed-point held by same-width digits). Deviation, accepted at the gate (F11): AC3's parenthetical pins the pre-retrofit base (38 / 2,193) while the shipped header derives from the retrofitted size (44 / 2,575), as T3's implement-fixes-the-figures clause licensed; the budget remains set from the measured size plus headroom as the criterion promises.
- 2026-08-22 fan-out (three lenses, findings and dispositions — IP3): [O] diff-bug F1 fix (step-9 check ordered before graduation), F2 fix (two modules headerless — both retrofitted), F3 fix (scope to the repo's modules), F4/F5/F7 fix (remedy/Weight-caps home unified in one bullet), F6 fix (measurement pointer resolved via work-log line), F8 reject (falsifiers live in the work log; D-122 append-only, not every entry carries one), F9 fix (graduation prose writes the header), F10 fix (stale comment), F11 accept-with-deviation (recorded above), F12 reject (its arithmetic assumes constant line density; the byte axis binds exactly under the width failure it exists for), F13 reject (the header figure is the historical derivation base, not a live self-measurement), F14 fix (rewrap), F15 fix (DESIGN list). [S] blame-history: one finding — the plan-time §1 prune, self-corrected on main (f911896) before shipping; measurements, additive edits, and D-122 consistency verified clean. [S] prior-review: no shipped regressions; flagged that M153's archive recorded the identical §1 prune one milestone earlier — LESSONS candidate at hygiene; no PR-thread evidence exists (probe returned empty).
- 2026-08-22 consistency gate: cairn_validate exit 0; scripts/hooks/skills suites exit 0 (re-run after the fix batch); generic profile — no toolchain checks; no principle change — impact skipped. No CI is configured on the repo (gh pr checks: no checks reported).
