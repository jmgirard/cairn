<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M100: Review-finding enforcement — findings travel verbatim, outcomes meet projections

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP1, IP3, GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

An RR's binding findings reach the merge gate unsoftened: criteria travel
verbatim under a mechanical diff, deviations are shown rather than slipped,
projections meet outcomes on a mandatory surface, and the implementer never
authors the durable verdict on the review constraining it (RR04 rec 8).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-brief` ingest protocol (SKILL.md:68-70 area): an RR
carrying a "Binding criteria" section is ingested verbatim into the ingesting
milestone's AC block, deviations legal only via a "Deviations from RR<NN>"
table shown verbatim at the ingest gate (IP3 applied to review findings);
`templates/brief.md` asks the reviewer for the section as measurable
assertions. A `cairn_validate` CHECK string-comparing such a milestone's AC
block against its named RR (first `reviews/`-reading check; `_section_body`,
cairn_validate.py:578-590, is the pattern). `/milestone-review` step 7 +
Review section: measured-vs-projected printed side by side for numeric
projections carried from the driving RR (copied in at plan time —
`/milestone-plan` states this); a shortfall past the milestone's stated
tolerance forces an explicit "accept shortfall, recorded as such" chip
option. Rulebook: the adjudication-asymmetry sentence and the
script-measurable-AC/committed-ledger preference (~4 lines total, RR04's Q8
budget). Guards + mutation-harness registrations; the milestone counts its
own always-read delta.

**Out:** decommissioning of measured no-ops → M101. D-056's narrow
supersession → parked candidate row (parked by D-057). A mechanical
always-read budget (RR04 rec 6, `consider`) → stays with RR04's archived
record; maintainer-initiated only. Retroactive "Binding criteria" sections
for RR01–RR04 → never: review records are history (IP4); the check binds
from the first RR that carries the section.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: `/milestone-brief` states the ingest rule — an RR "Binding
      criteria" section is ingested verbatim into the AC block, deviations
      legal only through a "Deviations from RR<NN>" table shown verbatim at
      the ingest gate — and `templates/brief.md` requests the section as
      measurable assertions. Both guard-pinned.
- [ ] AC2: A `cairn_validate` CHECK fails a milestone whose named driving RR
      carries Binding criteria that its AC block does not contain verbatim
      and no Deviations table names; quiet on verbatim ingestion, on tabled
      deviations, and on RRs or milestones without the section. Proven in
      each direction by fixtures (M90: reddens for EACH input it covers).
- [ ] AC3: `/milestone-review` mandates measured-vs-projected side by side in
      the Review section and in chat above the merge chip; a shortfall past
      the stated tolerance forces an explicit "accept shortfall, recorded as
      such" chip option. Guard-pinned; no-driving-RR case no-ops cleanly.
- [ ] AC4: The rulebook carries the adjudication-asymmetry sentence (the
      implementing session never authors the durable verdict on the review
      constraining it; such claims route to a new RB or the maintainer's own
      words at the gate) and the script-measurable-AC/committed-ledger
      preference; both guard-pinned and harness-registered; ≤4 rulebook
      lines added by this milestone, counted by diff.
- [ ] AC5: The milestone's always-read delta (rulebook + CLAUDE.md cairn
      section) is recorded in the work log, counted by diff (RR02's
      presumed-guilty standard).
- [ ] AC6: The active profile's `verify` slot is clean — all three suites
      green from the repo root, exit codes checked individually, never
      behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T5
- AC2 → T2
- AC3 → T3, T5
- AC4 → T4, T5
- AC5 → T6
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Author the ingest rule in `/milestone-brief` (SKILL.md:68-70 area)
      and add "Binding criteria" to `templates/brief.md`; place the
      Deviations table within the milestone file against the
      section-ownership table and `test_section_allow_lists.py`.
- [ ] T2: Implement the CHECK (CHECKS list, cairn_validate.py:1513-1529;
      `_section_body` pattern) with both-direction fixtures.
- [ ] T3: Amend `/milestone-review` step 7 (SKILL.md:146-158) and the Review
      section instructions: projection-vs-outcome juxtaposition + the
      accept-shortfall chip option; add the plan-time projection copy to
      `/milestone-plan` where ACs are authored.
- [ ] T4: Add the two rulebook sentences (adjudication asymmetry;
      script-measurable preference), drafted against the ≤4-line budget.
- [ ] T5: Guards for T1/T3/T4 prose + mutation-harness registrations;
      anchors copied from the target files' actual bytes (M95).
- [ ] T6: Count the always-read delta by diff; run the three suites from the
      repo root, exit codes individually; record both in the work log.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-20: created by /milestone-plan from the NEXT UP candidate row (RR04 rec 8, mechanisms 1-4); split from the decommissioning half (M101) at the sizing tripwires, per the row's own instruction.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
