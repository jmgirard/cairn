<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M<NN>: <Title>

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

One sentence.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** what this milestone does.

**Out:** what it refuses to do — and where that work lives instead
(e.g., `Out: batch scoring → M13`). "Out" means not in *this* milestone,
never "never".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] Each objectively checkable with evidence — a test that passes, a file
      that exists, `devtools::check()` output. Never vibes.
- [ ] Code milestones always include: `devtools::check()` clean.

## Coverage
<!-- owner: plan · create/amend-via-gate; maps each acceptance criterion to
     the task(s) that satisfy it. AC and Task numbers are positional
     (top-to-bottom in their sections). Every criterion maps to ≥1 task; a
     criterion with no task is a planning gap. Review reads this to fence
     evidence — see tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] Ordered concrete steps, each ≤ one working session, with file:line
      references where known.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- YYYY-MM-DD: created by /milestone-plan.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
