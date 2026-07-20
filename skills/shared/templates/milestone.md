<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below.

     DRAFTING BUDGETS (M99) — guidance, not a gate; the only size check that
     can fail is cairn_validate's <150 over the plan-owned body.
     Goal 7 · Scope 26 · AC 28 · Coverage 11 · Tasks 25 — each the measured p75
     over 99 milestone files, so three drafts in four already fit, and the
     fourth is the one that thrashed. Those 97 plus this 21-line preamble leave
     ≥21 RESERVED for ## Decisions: implement/review-owned, still counted
     (D-030/D-046), measured to p90 21 / max 35, so plan spends none of it.
     139 of 149 permitted; 10 spare. Every figure here is measured, never
     assumed (D-049). /milestone-plan step 4 names the counter. -->
# M<NN>: <Title>

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
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
      that exists, the active profile's verify/check output. Never vibes.
- [ ] Code milestones always include: the active profile's `verify` slot clean
      (`cairn/PROFILE.md`; for a toolchain whose profile names a fuller
      pre-review check, that check too).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] Ordered concrete steps, each ≤ one working session, with file:line
      references where known.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- YYYY-MM-DD: created by /milestone-plan.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
