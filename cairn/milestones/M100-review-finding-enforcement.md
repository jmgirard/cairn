<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M100: Review-finding enforcement — findings travel verbatim, outcomes meet projections

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP1, IP3, GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m100-review-finding-enforcement · https://github.com/jmgirard/cairn/pull/98   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: `/milestone-brief` states the ingest rule — an RR "Binding
      criteria" section is ingested verbatim into the AC block, deviations
      legal only through a "Deviations from RR<NN>" table shown verbatim at
      the ingest gate — and `templates/brief.md` requests the section as
      measurable assertions. Both guard-pinned.
- [x] AC2: A `cairn_validate` CHECK fails a milestone whose named driving RR
      carries Binding criteria that its AC block does not contain verbatim
      and no Deviations table names; quiet on verbatim ingestion, on tabled
      deviations, and on RRs or milestones without the section. Proven in
      each direction by fixtures (M90: reddens for EACH input it covers).
- [x] AC3: `/milestone-review` mandates measured-vs-projected side by side in
      the Review section and in chat above the merge chip; a shortfall past
      the stated tolerance forces an explicit "accept shortfall, recorded as
      such" chip option. Guard-pinned; no-driving-RR case no-ops cleanly.
- [x] AC4: The rulebook carries the adjudication-asymmetry sentence (the
      implementing session never authors the durable verdict on the review
      constraining it; such claims route to a new RB or the maintainer's own
      words at the gate) and the script-measurable-AC/committed-ledger
      preference; both guard-pinned and harness-registered; ≤4 rulebook
      lines added by this milestone, counted by diff.
- [x] AC5: The milestone's always-read delta (rulebook + CLAUDE.md cairn
      section) is recorded in the work log, counted by diff (RR02's
      presumed-guilty standard).
- [x] AC6: The active profile's `verify` slot is clean — all three suites
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

- [x] T1: Author the ingest rule in `/milestone-brief` (SKILL.md:68-70 area)
      and add "Binding criteria" to `templates/brief.md`; place the
      Deviations table within the milestone file against the
      section-ownership table and `test_section_allow_lists.py`.
- [x] T2: Implement the CHECK (CHECKS list, cairn_validate.py:1513-1529;
      `_section_body` pattern) with both-direction fixtures.
- [x] T3: Amend `/milestone-review` step 7 (SKILL.md:146-158) and the Review
      section instructions: projection-vs-outcome juxtaposition + the
      accept-shortfall chip option; add the plan-time projection copy to
      `/milestone-plan` where ACs are authored.
- [x] T4: Add the two rulebook sentences (adjudication asymmetry;
      script-measurable preference), drafted against the ≤4-line budget.
- [x] T5: Guards for T1/T3/T4 prose + mutation-harness registrations;
      anchors copied from the target files' actual bytes (M95).
- [x] T6: Count the always-read delta by diff; run the three suites from the
      repo root, exit codes individually; record both in the work log.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-20: created by /milestone-plan from the NEXT UP candidate row (RR04 rec 8, mechanisms 1-4); split from the decommissioning half (M101) at the sizing tripwires, per the row's own instruction.
- 2026-07-20: implement gate chose: Driving RR header slot, deviations table inside the AC section, whitespace-normalized matching, strict default tolerance. T1 done — ingest rule in /milestone-brief step 3, Binding criteria in brief.md, Driving RR slot + AC comment in milestone.md, ownership-table row updated; skills suite green (530 OK). Pre-existing red found on main (undated ledger extraction status) fixed there as a trivial commit and the branch rebased.
- 2026-07-20: T2 done — `binding criteria` CHECK (`check_binding_criteria` + `_binding_criteria`/`_rr_file`/`_norm_ws`) registered in CHECKS; 13 fixture tests in scripts/tests/test_binding_criteria.py cover both directions per input (verbatim-rewrapped quiet; softened fires; tabled quiet; no/dash slot quiet with positive twin; sectionless RR quiet; missing RR file fires; archived RR binds; pre-marker BC token doesn't excuse). Both suites green; validate PASS on tree.
- 2026-07-20: T3 done — projection-vs-outcome block in review step 3 (Review-section side) and step 7 (chip side, with the accept-shortfall option); Driving RR bullet added to plan step 4 (slot + verbatim ingest + projection copy). Both suites green.
- 2026-07-20: T4 done — script-measurable-AC bullet in Universal tracking rules; adjudication-asymmetry sentence appended to the Fable/RB-RR bullet. Rulebook diff vs main now +5/−1 (4 new lines + the T1 ownership-row modification), net +4 — both numbers to be shown at review against AC4's ≤4 budget.
- 2026-07-20: T5 done — skills/tests/test_finding_enforcement.py (12 asserts over 6 files) + 8 mutation-harness entries, all proven to redden (first run failed all 8: the guard used open() and the engine patches Path.read_text — switched to pathlib; the failure was the harness doing its job on an invisible guard). 542 skills tests green.
- 2026-07-20: T6 done — always-read delta measured by `git diff main..HEAD --numstat`: tracking-rules.md +5/−1 (net +4, AC4/AC5 evidence), CLAUDE.md cairn section untouched. Three suites green from repo root, exit codes individually (skills 542 / scripts 222 / hooks 72), cairn_validate exit 0. All tasks done → status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->

- 2026-07-20 evidence (all fresh, PR #98):
- AC1: PASS — test_finding_enforcement TestIngestRule (4 asserts) + TestBriefTemplate green; ingest rule at milestone-brief SKILL.md:70-82, template request at brief.md:38-44.
- AC2: PASS — scripts/tests/test_binding_criteria.py 13/13: softened fires (bare and archived-RR), verbatim/tabled/no-slot/dash-slot/sectionless quiet each beside a positive twin, missing RR file fires, pre-marker BC token doesn't excuse; check registered in CHECKS and PASS on the real tree.
- AC3: PASS — TestReviewSurfaces green (Review-section block SKILL.md:57-63; merge-chip block with "accept shortfall, recorded as such"); no-op clause guard-pinned; real tree quiet (TestWiring.test_current_tree_is_quiet).
- AC4: PASS, borderline shown — sentences at tracking-rules.md:210-211 and :597-598; guards green; harness pairs redden (TestRegisteredGuardsFailWhenBlanked 9/9 under discover). Measured +5 insertions/−1 deletion against projected ≤4 added: the two T4 sentences cost 4 new lines; the fifth insertion is T1's ownership-row modification paired with its own deletion (net +4). Pair presented verbatim at the merge gate for the maintainer's call — not adjudicated here, per the adjudication-asymmetry rule this milestone ships.
- AC5: PASS — T6 work-log line records the delta; fresh `git diff main..HEAD --numstat` matches (+5/−1 tracking-rules.md; CLAUDE.md untouched).
- AC6: PASS — three suites green from repo root, exit codes individually (skills 542 OK/0 · scripts 222 OK/0 · hooks 72 OK/0); cairn_validate exit 0.
- Consistency gate: cairn_validate all green incl. `binding criteria` PASS; no DESIGN.md principle changed → cairn_impact skipped; generic profile → toolchain half a clean no-op. CI: repo has no configured checks ("no checks reported").
- Projection-vs-outcome: M100 predates its own Driving RR slot and RR04 carries no Binding criteria section, so the mechanical surface no-ops; the one numeric projection in scope (RR04 Q8's ~4 rulebook lines) is juxtaposed under AC4: measured net +4 (gross +5/−1) against projected ≤4.
